"""Independent continuity and refusal checks; all ledgers are disposable fixtures."""
import concurrent.futures
import copy
import hashlib
import json
import subprocess
import sys
import threading
from unittest.mock import patch

from test_continuous_worker_request_cancellation import CancellationFixture, CancellationWorkflowTests, ROOT
from test_continuous_worker_requests import ref
from core.runtime.continuous_worker.state import State, Refused, digest
from core.runtime.continuous_worker.requests import Requests, CONFIG_KEY, RECONFIGURED
from core.runtime.continuous_worker.dependency_mcp import DependencyTools, TOOLS


class RebindingFixture(CancellationFixture):
    def proposal(self):
        config = copy.deepcopy(self.config)
        config["participants"]["setup"].update(host="replacement-host", session="replacement-session", generation=2)
        config["expires_at"] += 1000
        return {"configuration": config, "decision": ref("operator-native-reconciliation"),
                "evidence": [ref("native-checkpoint-and-effects-inspection")]}

    def plan(self):
        self.state.control("pause-dispatch")
        return self.channel.reconfiguration_plan(self.proposal())

    def rows(self, table):
        return [tuple(row) for row in self.state.db.execute("SELECT * FROM " + table)]

    def refreshed(self, config):
        return Requests(self.state, digest(config))


class RebindingTests(RebindingFixture):
    def test_pending_work_and_original_actors_survive_session_replacement(self):
        for stage in ("delivered", "accepted"):
            self.channel.observe(self.normal(stage))
        plan = self.plan()
        tables = {name: self.rows(name) for name in ("dependency_requests", "tasks", "attempts", "effects", "controls")}
        history = self.rows("events")
        receipt = self.channel.reconfigure(plan)
        self.assertEqual(receipt["previous_configuration"], self.config)
        self.assertFalse(receipt["execution_authorized"])
        self.assertEqual(self.state.mode(), "pause-dispatch")
        self.assertEqual({name: self.rows(name) for name in tables}, tables)
        self.assertEqual(self.rows("events")[:-1], history)
        self.assertEqual(self.rows("events")[-1][3], RECONFIGURED)
        self.state.control("resume")
        with self.assertRaisesRegex(Refused, "configuration changed"):
            self.channel.observe(self.normal("returned"))
        with self.assertRaisesRegex(Refused, "digest mismatch"):
            self.refreshed(self.config)
        old_actor = self.actor("setup")
        self.config = plan["configuration"]
        current = self.refreshed(self.config)
        with self.assertRaisesRegex(Refused, "stale binding"):
            current.observe(self.normal("returned") | {"actor": old_actor})
        current.observe(self.normal("returned"))
        result = current.observe(self.normal("adopted"))
        self.assertEqual(result["stage"], "adopted")
        self.assertEqual(result["observations"]["accepted"]["actor"], old_actor)
        self.assertEqual(result["observations"]["returned"]["actor"], self.actor("setup"))

    def test_expired_configuration_can_be_reconciled_without_auto_resume(self):
        self.channel = Requests(self.state, digest(self.config), now=lambda: self.config["expires_at"] + 1)
        plan = self.plan()
        self.channel.reconfigure(plan)
        current = Requests(self.state, digest(plan["configuration"]), now=lambda: self.config["expires_at"] + 1)
        self.assertFalse(current.inspect(self.body["id"])["configuration_expired"])
        with self.assertRaisesRegex(Refused, "controls"):
            current.submit({"actor": self.actor("facman"), "request": self.body | {"id": "other"}})

    def test_renewal_preserves_bindings_and_rejects_noop_or_shortening(self):
        self.state.control("pause-dispatch")
        proposal = self.proposal()
        proposal["configuration"]["participants"] = copy.deepcopy(self.config["participants"])
        plan = self.channel.reconfiguration_plan(proposal)
        receipt = self.channel.reconfigure(plan)
        self.assertEqual(receipt["bindings"], {k: digest(v) for k, v in self.config["participants"].items()})
        current = self.refreshed(plan["configuration"])
        for expiry in (plan["configuration"]["expires_at"], self.config["expires_at"], 0):
            with self.subTest(expiry=expiry), self.assertRaises(Refused):
                current.reconfiguration_plan(proposal | {"configuration": plan["configuration"] | {"expires_at": expiry}})

    def test_ownership_schema_participant_bounds_and_generation_changes_refuse(self):
        self.state.control("pause-dispatch")
        changes = [("schema", "aide.dependency-configuration.v1"), ("state_root", str(self.root / "other")),
                   ("max_requests", 3), ("message_bytes", 4096)]
        proposals = [self.proposal() | {"configuration": self.proposal()["configuration"] | {key: value}}
                     for key, value in changes]
        for key, value in (("owner", "other"), ("repository", "other/repo"), ("workspace", "other"),
                           ("generation", 1), ("generation", 3)):
            proposal = self.proposal(); proposal["configuration"]["participants"]["setup"][key] = value
            proposals.append(proposal)
        for name in ("facman", "setup"):
            proposal = self.proposal(); del proposal["configuration"]["participants"][name]
            proposals.append(proposal)
        proposal = self.proposal(); proposal["configuration"]["participants"]["facman"]["generation"] = 2
        proposals.append(proposal)
        before = self.snapshot()
        for proposal in proposals:
            with self.subTest(proposal=proposal), self.assertRaises(Refused):
                self.channel.reconfiguration_plan(proposal)
        self.assertEqual(before, self.snapshot())

    def test_other_control_modes_refuse_without_mutation(self):
        for mode in ("resume", "drain", "emergency-stop"):
            self.state.control(mode); before = self.snapshot()
            with self.subTest(mode=mode), self.assertRaisesRegex(Refused, "pause-dispatch"):
                self.channel.reconfiguration_plan(self.proposal())
            self.assertEqual(before, self.snapshot())

    def test_active_attempt_and_unresolved_intent_refuse(self):
        attempt = self.state.claim(1)
        self.state.control("pause-dispatch")
        with self.assertRaisesRegex(Refused, "attempt still active"):
            self.channel.reconfiguration_plan(self.proposal())
        effect = self.state.intent(attempt["id"], "fixture", {"effect": "uncertain"})
        # Deliberately inconsistent terminal attempt: recovery must still catch the intent.
        self.state.db.execute("UPDATE attempts SET stage='blocked' WHERE id=?", (attempt["id"],))
        before = self.snapshot()
        with self.assertRaisesRegex(Refused, "effect remains unresolved"):
            self.channel.reconfiguration_plan(self.proposal())
        self.assertEqual(before, self.snapshot())
        self.assertEqual(self.state.unresolved()[0]["id"], effect)

    def test_pause_resume_pause_invalidates_plan(self):
        plan = self.plan()
        self.state.control("resume"); self.state.control("pause-dispatch")
        before = self.snapshot()
        with self.assertRaisesRegex(Refused, "snapshot changed"):
            self.channel.reconfigure(plan)
        self.assertEqual(before, self.snapshot())

    def test_changed_dependency_or_native_state_invalidates_plan(self):
        for table, command in (("dependency_requests", "UPDATE dependency_requests SET stage='delivered'"),
                               ("tasks", "UPDATE tasks SET reason='new native information'")):
            with self.subTest(table=table):
                fixture = RebindingFixture(); fixture.setUp()
                try:
                    plan = fixture.plan(); fixture.state.db.execute(command)
                    before = fixture.snapshot()
                    with self.assertRaisesRegex(Refused, "snapshot changed"):
                        fixture.channel.reconfigure(plan)
                    self.assertEqual(before, fixture.snapshot())
                finally:
                    fixture.tearDown()

    def test_exact_receipt_replay_and_superseded_plan(self):
        plan = self.plan(); receipt = self.channel.reconfigure(plan)
        current = self.refreshed(plan["configuration"])
        before = self.snapshot()
        self.assertEqual(current.reconfigure(plan), receipt)
        self.assertEqual(self.snapshot(), before)
        proposed = {key: plan[key] for key in ("configuration", "decision", "evidence")}
        proposed["configuration"] = plan["configuration"] | {"expires_at": plan["configuration"]["expires_at"] + 1}
        later = current.reconfiguration_plan(proposed); current.reconfigure(later)
        with self.assertRaisesRegex(Refused, "superseded"):
            current.reconfigure(plan)

    def test_event_failure_rolls_back_config_and_history(self):
        plan = self.plan(); before = self.snapshot()
        with patch.object(self.state, "event", side_effect=OSError("interrupted receipt")):
            with self.assertRaises(OSError): self.channel.reconfigure(plan)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(self.refreshed(self.config).inspect(self.body["id"])["stage"], "recorded")

    def test_competing_connections_preserve_one_reconciliation(self):
        plan = self.plan(); barrier = threading.Barrier(2)
        competing = copy.deepcopy(plan)
        competing["configuration"]["participants"]["setup"]["session"] = "competing-session"
        def apply(candidate):
            state = State(self.root)
            try:
                channel = Requests(state, digest(self.config))
                barrier.wait(timeout=10)
                try: return channel.reconfigure(candidate)["configuration_sha256"]
                except Refused: return "refused"
            finally: state.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(apply, candidate) for candidate in (plan, competing)]
            results = [future.result(timeout=15) for future in futures]
        self.assertEqual(results.count("refused"), 1)
        self.assertEqual(self.state.db.execute("SELECT COUNT(*) FROM events WHERE kind=?", (RECONFIGURED,)).fetchone()[0], 1)
        self.assertEqual(self.rows("dependency_requests")[0][3], "recorded")

    def test_readonly_plan_is_deterministic_and_has_no_ledger_dump(self):
        self.state.control("pause-dispatch")
        state = State(self.root, read_only=True)
        try:
            current = Requests(state, digest(self.config)); statements = []
            state.db.set_trace_callback(statements.append)
            before = self.snapshot()
            first = current.reconfiguration_plan(self.proposal())
            self.assertEqual(first, current.reconfiguration_plan(self.proposal()))
            self.assertEqual(before, self.snapshot())
            self.assertNotIn(self.body["objective"], json.dumps(first))
            self.assertEqual(len(first["snapshot_sha256"]), 64)
            self.assertTrue(all(s.startswith(("BEGIN", "SELECT", "ROLLBACK")) for s in statements))
        finally: state.close()

    def test_snapshot_and_reconfiguration_count_are_bounded(self):
        self.state.control("pause-dispatch")
        with patch("core.runtime.continuous_worker.requests.SNAPSHOT_BYTES", 64):
            with self.assertRaisesRegex(Refused, "snapshot exceeds"):
                self.channel.reconfiguration_plan(self.proposal())
        current, config = self.channel, self.config
        for count in range(16):
            proposal = self.proposal() | {"configuration": config | {"expires_at": config["expires_at"] + 1}}
            plan = current.reconfiguration_plan(proposal); current.reconfigure(plan)
            config = plan["configuration"]; current = self.refreshed(config)
        with self.assertRaisesRegex(Refused, "allowance exhausted"):
            current.reconfiguration_plan(proposal | {"configuration": config | {"expires_at": config["expires_at"] + 1}})

    def test_malformed_proposals_and_plan_pins_refuse(self):
        plan = self.plan(); before = self.snapshot()
        for changed in (plan | {"unexpected": True}, plan | {"schema": "unknown"},
                        plan | {"snapshot_sha256": "0" * 64}, plan | {"configuration_sha256": "0" * 64}):
            with self.subTest(changed=changed), self.assertRaises(Refused): self.channel.reconfigure(changed)
        for changed in (self.proposal() | {"decision": {}}, self.proposal() | {"evidence": []}):
            with self.assertRaises(Refused): self.channel.reconfiguration_plan(changed)
        self.assertEqual(before, self.snapshot())

    def test_mcp_has_no_reconfiguration_authority_and_stale_binding_refuses(self):
        tools = DependencyTools(self.root, digest(self.config), "setup", self.actor("setup")["binding_sha256"])
        self.assertEqual({tool["name"] for tool in TOOLS}, {"dependency_inbox", "dependency_status", "dependency_submit", "dependency_observe"})
        with self.assertRaises(Refused): tools.call("dependency_reconfigure", self.proposal())
        plan = self.plan(); self.channel.reconfigure(plan); self.state.control("resume")
        with self.assertRaisesRegex(Refused, "digest mismatch"):
            tools.call("dependency_status", {"request_id": self.body["id"]})


class RebindingWorkflowTests(RebindingFixture):
    cli = CancellationWorkflowTests.cli
    mcp = CancellationWorkflowTests.mcp

    def reconfiguration_cli(self, message, *, apply=False, sha=None, expected=0):
        path = self.root / "reconfiguration.json"
        path.write_text(json.dumps(message), encoding="utf-8")
        args = [sys.executable, "-B", "-m", "core.runtime.continuous_worker", "request-reconfigure",
                "--state-root", str(self.root), "--configuration-sha256", digest(self.config), "--input", str(path)]
        if apply: args += ["--apply", "--sha256", sha or hashlib.sha256(path.read_bytes()).hexdigest()]
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_fresh_process_replacement_continues_exact_native_work(self):
        other = self.body | {"id": "preserved-cancellation"}
        self.cli("request-submit", message={"actor": self.actor("facman"), "request": other})
        cancellation = self.cancel(); cancellation["request_id"] = other["id"]
        cancellation["request_sha256"] = digest(other)
        self.cli("request-observe", message=cancellation)
        for stage in ("delivered", "accepted"):
            self.cli("request-observe", message=self.normal(stage))
        self.state.control("pause-dispatch")
        native = {key: self.rows(key) for key in ("tasks", "attempts", "effects", "controls")}
        cancelled = tuple(self.state.db.execute("SELECT * FROM dependency_requests WHERE id=?", (other["id"],)).fetchone())
        plan = self.reconfiguration_cli(self.proposal())
        self.reconfiguration_cli(plan, apply=True, sha="0" * 64, expected=2)
        receipt = self.reconfiguration_cli(plan, apply=True)
        self.assertEqual(native, {key: self.rows(key) for key in native})
        self.cli("request-status", expected=2)
        old_actor = self.actor("setup")
        self.config = plan["configuration"]
        before = self.snapshot()
        self.assertEqual(self.reconfiguration_cli(plan, apply=True), receipt)
        self.assertEqual(before, self.snapshot())
        self.cli("request-observe", message=self.normal("returned"), expected=2)
        self.state.control("resume")
        self.cli("request-observe", message=self.normal("returned") | {"actor": old_actor}, expected=2)
        message = self.normal("returned")
        returned = self.mcp("setup", "dependency_observe", {key: value for key, value in message.items() if key != "actor"})
        adopted = self.cli("request-observe", message=self.normal("adopted"))
        self.assertEqual(adopted["stage"], "adopted")
        self.assertEqual(returned["observations"]["accepted"]["actor"], old_actor)
        self.assertEqual(returned["observations"]["accepted"]["detail"]["native_work"], ref("native-task"))
        self.assertEqual(cancelled, tuple(self.state.db.execute("SELECT * FROM dependency_requests WHERE id=?", (other["id"],)).fetchone()))
        self.assertEqual({key: native[key] for key in ("tasks", "attempts", "effects")},
                         {key: self.rows(key) for key in ("tasks", "attempts", "effects")})
