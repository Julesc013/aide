"""Cancellation preserves independent requests and native work; owned fixtures only."""
import concurrent.futures
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker.state import State, Refused, digest
from core.runtime.continuous_worker.requests import Requests, configuration as validate_config
from core.runtime.continuous_worker.dependency_mcp import DependencyTools, TOOLS
from test_continuous_worker_requests import configuration, ref
from test_continuous_worker_mcp import handshake, call


class CancellationFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aide-cancellation-")
        self.root = Path(self.temp.name).resolve()
        self.config = configuration(self.root) | {"schema": "aide.dependency-configuration.v2"}
        self.state = State(self.root)
        self.state.bind({"tasks": [{"id": "native", "depends_on": []}]})
        Requests.initialize(self.state, self.config)
        self.channel = Requests(self.state, digest(self.config))
        self.body = {"schema": "aide.dependency-request.v1", "id": "cancel-me", "sender": "facman",
                     "recipient": "setup", "sender_work": ref("FM-task"), "objective": "Bounded fix",
                     "acceptance": "Consumer check passes", "references": [ref("base")],
                     "completion": ["validated", "published"]}
        self.channel.submit({"actor": self.actor("facman"), "request": self.body})

    def tearDown(self):
        self.state.close()
        self.temp.cleanup()

    def actor(self, name):
        return {"participant": name, "binding_sha256": digest(self.config["participants"][name])}

    def message(self, stage, detail, *, body=None):
        body = body or self.body
        return {"request_id": body["id"], "request_sha256": digest(body), "stage": stage,
                "actor": self.actor("facman" if stage in ("adopted", "cancellation_requested") else "setup"),
                "detail": detail}

    def cancel(self, expected="recorded"):
        return self.message("cancellation_requested", {"expected_stage": expected,
                            "reason": "Dependency is no longer needed", "evidence": [ref("owner-decision")]})

    def acknowledge(self, cancellation, disposition="not_started"):
        return self.message("cancellation_acknowledged", {"cancellation_sha256": digest(cancellation),
                            "disposition": disposition, "evidence": [ref("native-outcome")]})

    def normal(self, stage, *, body=None):
        body = body or self.body
        details = {"delivered": {"receipt": ref("receipt")},
                   "accepted": {"native_work": ref("native-task"), "evidence": [ref("admission")]},
                   "returned": {"subject": ref("result"), "claims": {key: "PASS" for key in body["completion"]},
                                "evidence": [ref("native-checks")]}}
        if stage == "adopted":
            details[stage] = {"returned_sha256": digest(self.normal("returned", body=body)),
                              "verification": [ref("consumer-checks")]}
        return self.message(stage, details[stage], body=body)

    def native(self):
        return {table: [tuple(row) for row in self.state.db.execute("SELECT * FROM " + table)]
                for table in ("tasks", "attempts", "effects", "controls", "meta")}

    def snapshot(self):
        return list(self.state.db.iterdump())

    def refused_unchanged(self, message, *, channel=None):
        before = self.snapshot()
        with self.assertRaises(Refused):
            (channel or self.channel).observe(message)
        self.assertEqual(before, self.snapshot())


class CancellationTests(CancellationFixture):
    def test_cancel_before_delivery_retains_obligations_and_requires_recipient_ack(self):
        native = self.native()
        result = self.channel.observe(self.cancel())
        self.assertEqual(result["stage"], "recorded")
        self.assertEqual(result["schema"], "aide.dependency-status.v2")
        self.assertEqual(result["cancellation_state"], "requested")
        self.assertEqual(result["next_owner"], "setup")
        self.assertEqual(result["next_action"], "reconcile_native_effects_and_acknowledge_cancellation")
        self.assertEqual(result["unmet_obligations"], {"validated": "UNKNOWN", "published": "UNKNOWN"})
        self.assertEqual(result["request"], self.body)
        self.assertFalse(result["execution_authorized"])
        self.assertEqual(native, self.native())
        inbox = self.channel.inbox(self.actor("setup"))["requests"][0]
        self.assertEqual(inbox["cancellation_state"], "requested")
        self.assertEqual(inbox["stage"], "recorded")
        self.assertEqual(inbox["next_action"], result["next_action"])

    def test_every_disposition_retains_work_and_does_not_authorize_or_adopt(self):
        for disposition in ("not_started", "stopped", "already_completed", "uncertain"):
            with self.subTest(disposition=disposition):
                case = CancellationFixture(); case.setUp()
                try:
                    cancellation = case.cancel()
                    case.channel.observe(cancellation)
                    native = case.native()
                    result = case.channel.observe(case.acknowledge(cancellation, disposition))
                    self.assertEqual(result["stage"], "recorded")
                    self.assertEqual(result["cancellation_state"], "acknowledged")
                    self.assertEqual(result["cancellation_disposition"], disposition)
                    self.assertNotIn("adopted", result["observations"])
                    self.assertFalse(result["claims_independently_verified"])
                    self.assertFalse(result["execution_authorized"])
                    self.assertEqual(native, case.native())
                    expected = ("setup", "reconcile_uncertain_native_effects") if disposition == "uncertain" else (
                        "facman", "review_native_cancellation_outcome_before_successor_request")
                    self.assertEqual((result["next_owner"], result["next_action"]), expected)
                finally:
                    case.tearDown()

    def test_after_each_normal_stage_cancellation_keeps_prior_observations(self):
        for stage in ("delivered", "accepted", "returned"):
            case = CancellationFixture(); case.setUp()
            try:
                for previous in ("delivered", "accepted", "returned"):
                    case.channel.observe(case.normal(previous))
                    if previous == stage: break
                before = case.channel.inspect(case.body["id"])
                result = case.channel.observe(case.cancel(stage))
                self.assertEqual(result["stage"], stage)
                for key, observation in before["observations"].items():
                    self.assertEqual(result["observations"][key], observation)
                self.assertEqual(result["request"]["completion"], ["validated", "published"])
            finally:
                case.tearDown()
        for stage in ("delivered", "accepted", "returned"):
            self.channel.observe(self.normal(stage))
        self.channel.observe(self.normal("adopted"))
        self.refused_unchanged(self.cancel("adopted"))

    def test_cancellation_stops_advancement_but_identical_replays_preserve_events(self):
        delivered = self.normal("delivered")
        self.channel.observe(delivered)
        cancellation = self.cancel("delivered")
        self.channel.observe(cancellation)
        acknowledgement = self.acknowledge(cancellation, "stopped")
        self.channel.observe(acknowledgement)
        before = self.snapshot()
        for message in (delivered, cancellation, acknowledgement):
            self.assertEqual(self.channel.observe(message)["cancellation_state"], "acknowledged")
        self.channel.submit({"actor": self.actor("facman"), "request": self.body})
        self.assertEqual(before, self.snapshot())
        for stage in ("accepted", "returned", "adopted"):
            self.refused_unchanged(self.normal(stage))
        for message in (cancellation, acknowledgement):
            changed = copy.deepcopy(message)
            changed["detail"]["evidence"] = [ref("different")]
            self.refused_unchanged(changed)

    def test_stale_stage_ack_without_request_and_wrong_cancellation_digest_refuse(self):
        cancellation = self.cancel()
        self.refused_unchanged(self.acknowledge(cancellation))
        self.channel.observe(self.normal("delivered"))
        self.refused_unchanged(cancellation)
        cancellation = self.cancel("delivered")
        self.channel.observe(cancellation)
        acknowledgement = self.acknowledge(cancellation)
        acknowledgement["detail"]["cancellation_sha256"] = "0" * 64
        self.refused_unchanged(acknowledgement)

    def test_both_observations_require_exact_actor_binding_revision_and_schema(self):
        cancellation = self.cancel()
        for message in (cancellation, self.acknowledge(cancellation)):
            if message["stage"] == "cancellation_acknowledged":
                self.channel.observe(cancellation)
            for key, value in (("actor", self.actor("setup" if message["actor"]["participant"] == "facman" else "facman")),
                               ("actor", message["actor"] | {"binding_sha256": "0" * 64}),
                               ("request_sha256", "0" * 64), ("unexpected", True)):
                with self.subTest(stage=message["stage"], key=key):
                    self.refused_unchanged(message | {key: value})

    def test_expired_paused_and_changed_config_refuse_both_observations(self):
        cancellation = self.cancel()
        for message in (cancellation, self.acknowledge(cancellation)):
            if message["stage"] == "cancellation_acknowledged":
                self.channel.observe(cancellation)
            expired = Requests(self.state, digest(self.config), now=lambda: 4102444801)
            self.refused_unchanged(message, channel=expired)
            for mode in ("pause-dispatch", "drain", "emergency-stop"):
                self.state.control(mode)
                self.refused_unchanged(message)
                self.assertEqual(self.channel.inspect(self.body["id"])["coordinator_mode"], mode)
                self.state.control("resume")
            changed = self.config | {"max_requests": 3}
            with self.assertRaises(Refused):
                Requests.initialize(self.state, changed)

    def test_malformed_and_oversized_details_refuse_atomically(self):
        cancellation = self.cancel()
        for detail in ({}, cancellation["detail"] | {"reason": ""}, cancellation["detail"] | {"reason": "x" * 9000},
                       cancellation["detail"] | {"evidence": []}, cancellation["detail"] | {"expected_stage": []}):
            self.refused_unchanged(cancellation | {"detail": detail})
        self.channel.observe(cancellation)
        acknowledgement = self.acknowledge(cancellation)
        for detail in ({}, acknowledgement["detail"] | {"disposition": "cancelled"},
                       acknowledgement["detail"] | {"disposition": []},
                       acknowledgement["detail"] | {"evidence": [ref("x") | {"sha256": "bad"}]}):
            self.refused_unchanged(acknowledgement | {"detail": detail})

    def test_event_failure_rolls_back_both_observations(self):
        cancellation = self.cancel()
        for message in (cancellation, self.acknowledge(cancellation)):
            if message["stage"] == "cancellation_acknowledged":
                self.channel.observe(cancellation)
            before = self.snapshot()
            with patch.object(self.state, "event", side_effect=OSError("fixture interrupted write")):
                with self.assertRaises(OSError):
                    self.channel.observe(message)
            self.assertEqual(before, self.snapshot())

    def test_cancel_and_delivery_race_has_one_winner_without_lost_observation(self):
        barrier = threading.Barrier(2)
        def submit(message):
            state = State(self.root)
            try:
                channel = Requests(state, digest(self.config))
                barrier.wait(timeout=10)
                try:
                    channel.observe(message)
                    return "recorded"
                except Refused:
                    return "refused"
            finally:
                state.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(submit, message) for message in (self.cancel(), self.normal("delivered"))]
            self.assertCountEqual([future.result(timeout=15) for future in futures], ["recorded", "refused"])
        status = self.channel.inspect(self.body["id"])
        self.assertEqual(len(status["observations"]), 1)
        self.assertEqual(status["stage"], "recorded" if status["cancellation_state"] == "requested" else "delivered")

    def test_restart_preserves_cancel_ack_and_unrelated_request_can_complete(self):
        other = self.body | {"id": "continue-me"}
        self.channel.submit({"actor": self.actor("facman"), "request": other})
        native = self.native()
        cancellation = self.cancel()
        self.channel.observe(cancellation)
        self.state.close()
        self.state = State(self.root)
        self.channel = Requests(self.state, digest(self.config))
        self.channel.observe(self.acknowledge(cancellation, "uncertain"))
        cancelled = self.channel.inspect(self.body["id"])
        for stage in ("delivered", "accepted", "returned", "adopted"):
            result = self.channel.observe(self.normal(stage, body=other))
        self.assertEqual(result["stage"], "adopted")
        self.assertEqual(result["cancellation_state"], "none")
        self.assertEqual(cancelled, self.channel.inspect(self.body["id"]))
        self.assertEqual(native, self.native())

    def test_v1_preserves_status_and_refuses_cancel_without_implicit_migration(self):
        folder = self.root / "legacy"; folder.mkdir()
        config = configuration(folder)
        state = State(folder)
        try:
            Requests.initialize(state, config)
            channel = Requests(state, digest(config))
            channel.submit({"actor": self.actor("facman"), "request": self.body})
            before = list(state.db.iterdump())
            for message in (self.cancel(), self.acknowledge(self.cancel())):
                with self.assertRaisesRegex(Refused, "v2"):
                    channel.observe(message)
            with self.assertRaisesRegex(Refused, "configuration changed"):
                Requests.initialize(state, config | {"schema": "aide.dependency-configuration.v2"})
            self.assertEqual(list(state.db.iterdump()), before)
            status = channel.inspect(self.body["id"])
            self.assertEqual(status["schema"], "aide.dependency-status.v1")
            self.assertNotIn("cancellation_state", status)
        finally:
            state.close()
        for schema in ("aide.dependency-configuration.v3", "", None):
            with self.assertRaises(Refused):
                validate_config(self.config | {"schema": schema}, self.root)

    def test_mcp_uses_same_owner_rules_and_does_not_accept_caller_actor(self):
        sender = DependencyTools(self.root, digest(self.config), "facman", self.actor("facman")["binding_sha256"])
        receiver = DependencyTools(self.root, digest(self.config), "setup", self.actor("setup")["binding_sha256"])
        cancellation = self.cancel()
        arguments = {key: value for key, value in cancellation.items() if key != "actor"}
        before = self.snapshot()
        with self.assertRaises(Refused): receiver.call("dependency_observe", arguments)
        with self.assertRaises(Refused): sender.call("dependency_observe", cancellation)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(sender.call("dependency_observe", arguments)["cancellation_state"], "requested")
        stage_schema = next(tool for tool in TOOLS if tool["name"] == "dependency_observe")["inputSchema"]
        self.assertIn("cancellation_requested", stage_schema["properties"]["stage"]["enum"])
        self.assertIn("cancellation_acknowledged", stage_schema["properties"]["stage"]["enum"])
        self.assertEqual(len(TOOLS), 4)


class CancellationWorkflowTests(CancellationFixture):
    def cli(self, command, *, message=None, expected=0):
        args = [sys.executable, "-B", "-m", "core.runtime.continuous_worker", command,
                "--state-root", str(self.root), "--configuration-sha256", digest(self.config)]
        if message is not None:
            source = self.root / "message.json"
            source.write_text(json.dumps(message), encoding="utf-8")
            args += ["--input", str(source)]
        else:
            args += ["--request-id", self.body["id"]]
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def mcp(self, participant, name, arguments):
        args = [sys.executable, "-B", "-m", "core.runtime.continuous_worker.dependency_mcp",
                "--state-root", str(self.root), "--configuration-sha256", digest(self.config),
                "--participant", participant, "--binding-sha256", self.actor(participant)["binding_sha256"]]
        payload = b"".join(json.dumps(message).encode() + b"\n" for message in handshake() + [call(name, arguments)])
        result = subprocess.run(args, cwd=ROOT, input=payload, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, b"")
        response = json.loads(result.stdout.splitlines()[-1])["result"]
        self.assertFalse(response["isError"], response)
        return json.loads(response["content"][0]["text"])

    def test_two_requests_across_fresh_cli_and_mcp_processes(self):
        native = self.native()
        other = self.body | {"id": "continue-me"}
        self.cli("request-submit", message={"actor": self.actor("facman"), "request": other})
        for stage in ("delivered", "accepted"):
            self.cli("request-observe", message=self.normal(stage))
        cancellation = self.cancel("accepted")
        self.cli("request-observe", message=cancellation)
        acknowledgement = self.acknowledge(cancellation, "uncertain")
        cancelled = self.mcp("setup", "dependency_observe", {k: v for k, v in acknowledgement.items() if k != "actor"})
        before = self.snapshot()
        self.cli("request-observe", message=cancellation)
        self.mcp("setup", "dependency_observe", {k: v for k, v in acknowledgement.items() if k != "actor"})
        self.cli("request-observe", message=self.normal("returned"), expected=2)
        self.assertEqual(before, self.snapshot())
        for stage in ("delivered", "accepted", "returned"):
            message = self.normal(stage, body=other)
            result = self.mcp("setup", "dependency_observe", {k: v for k, v in message.items() if k != "actor"})
            self.assertEqual(result["stage"], stage)
        result = self.cli("request-observe", message=self.normal("adopted", body=other))
        self.assertEqual(result["stage"], "adopted")
        self.assertEqual(result["cancellation_state"], "none")
        self.assertEqual(self.cli("request-status"), cancelled)
        self.assertEqual(cancelled["next_action"], "reconcile_uncertain_native_effects")
        self.assertEqual(cancelled["observations"]["accepted"]["detail"]["native_work"], ref("native-task"))
        self.assertEqual(native, self.native())


if __name__ == "__main__":
    unittest.main()
