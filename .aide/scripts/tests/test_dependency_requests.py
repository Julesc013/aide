"""Independent lifecycle/CLI oracles; all state belongs to disposable fixtures."""
import concurrent.futures
from contextlib import closing
import copy
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker.state import State, Refused, digest
from core.runtime.continuous_worker.requests import Requests, decode


def ref(name):
    return {"ref": name, "sha256": hashlib.sha256(name.encode()).hexdigest()}


def configuration(root):
    return {"schema": "aide.dependency-configuration.v1", "state_root": str(root),
            "participants": {name: {"repository": name + "/repo", "owner": name,
                                     "workspace": "fixture/" + name, "host": "fixture-host",
                                     "session": name + "-session", "generation": 1}
                             for name in ("facman", "setup")},
            "expires_at": 4102444800, "max_requests": 2, "message_bytes": 8192}


class DependencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aide-dependency-")
        self.root = Path(self.temp.name).resolve()
        self.config = configuration(self.root)
        self.state = State(self.root)
        self.state.bind({"tasks": [{"id": "unrelated", "depends_on": []}]})
        Requests.initialize(self.state, self.config)
        self.channel = Requests(self.state, digest(self.config))
        self.request = {"schema": "aide.dependency-request.v1", "id": "setup-fix", "sender": "facman",
                        "recipient": "setup", "sender_work": ref("FM-1"), "objective": "Return a tested setup fix",
                        "acceptance": "The reproduction and original checks pass", "references": [ref("base")],
                        "completion": ["candidate", "validated"]}

    def tearDown(self):
        self.state.close()
        self.temp.cleanup()

    def actor(self, name):
        return {"participant": name, "binding_sha256": digest(self.config["participants"][name])}

    def submit(self, body=None):
        return self.channel.submit({"actor": self.actor("facman"), "request": body or self.request})

    def observation(self, stage):
        details = {"delivered": {"receipt": ref("delivery")},
                   "accepted": {"native_work": ref("SETUP-2"), "evidence": [ref("native-admission")]},
                   "returned": {"subject": ref("candidate-commit"),
                                "claims": {"candidate": "PASS", "validated": "PASS"},
                                "evidence": [ref("target-checks")]}}
        if stage == "adopted":
            details[stage] = {"returned_sha256": digest(self.observation("returned")),
                              "verification": [ref("facman-consumer-check")]}
        return {"request_id": self.request["id"], "request_sha256": digest(self.request),
                "actor": self.actor("facman" if stage == "adopted" else "setup"),
                "stage": stage, "detail": details[stage]}

    def advance(self, *stages):
        for stage in stages:
            result = self.channel.observe(self.observation(stage))
        return result

    def test_complete_loop_preserves_native_authority_and_separate_adoption(self):
        before = [tuple(r) for r in self.state.db.execute("SELECT * FROM tasks")]
        self.assertEqual(self.submit()["stage"], "recorded")
        returned = self.advance("delivered", "accepted", "returned")
        self.assertEqual(returned["next_owner"], "facman")
        self.assertEqual(returned["stage"], "returned")
        self.assertFalse(returned["claims_independently_verified"])
        self.assertFalse(returned["execution_authorized"])
        adopted = self.advance("adopted")
        self.assertEqual(adopted["stage"], "adopted")
        self.assertEqual(adopted["observations"]["accepted"]["detail"]["native_work"], ref("SETUP-2"))
        self.assertEqual(before, [tuple(r) for r in self.state.db.execute("SELECT * FROM tasks")])
        self.assertEqual(self.state.db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0], 0)
        self.assertEqual(self.state.db.execute("SELECT COUNT(*) FROM effects").fetchone()[0], 0)

    def test_duplicates_after_later_progress_do_not_add_events(self):
        self.submit(); self.advance("delivered", "accepted")
        events = self.state.status()["events"]
        self.submit(); self.advance("delivered", "accepted")
        self.assertEqual(self.state.status()["events"], events)
        self.assertEqual(self.channel.inspect("setup-fix")["stage"], "accepted")

    def test_conflicting_identity_and_observation_are_refused(self):
        self.submit(); self.advance("delivered")
        changed = copy.deepcopy(self.request); changed["objective"] = "A different task"
        with self.assertRaisesRegex(Refused, "identity conflicts"):
            self.submit(changed)
        message = self.observation("delivered"); message["detail"] = {"receipt": ref("different")}
        with self.assertRaisesRegex(Refused, "conflicting duplicate"):
            self.channel.observe(message)

    def test_receiver_cannot_claim_sender_adoption_and_wrong_revision_refuses(self):
        self.submit()
        message = self.observation("delivered"); message["request_sha256"] = "0" * 64
        with self.assertRaisesRegex(Refused, "revision"):
            self.channel.observe(message)
        message = self.observation("delivered"); message["actor"] = self.actor("facman")
        with self.assertRaisesRegex(Refused, "participant"):
            self.channel.observe(message)
        self.advance("delivered", "accepted", "returned")
        message = self.observation("adopted"); message["actor"] = self.actor("setup")
        with self.assertRaisesRegex(Refused, "participant"):
            self.channel.observe(message)

    def test_out_of_order_and_wrong_result_binding_refuse(self):
        self.submit()
        with self.assertRaisesRegex(Refused, "out-of-order"):
            self.advance("accepted")
        self.advance("delivered", "accepted", "returned")
        message = self.observation("adopted"); message["detail"]["returned_sha256"] = "0" * 64
        with self.assertRaisesRegex(Refused, "returned result"):
            self.channel.observe(message)

    def test_return_must_account_for_all_obligations_and_failed_result_cannot_close(self):
        self.submit(); self.advance("delivered", "accepted")
        message = self.observation("returned"); del message["detail"]["claims"]["validated"]
        with self.assertRaisesRegex(Refused, "every requested"):
            self.channel.observe(message)
        message["detail"]["claims"]["validated"] = "NOT_RUN"
        observed = self.channel.observe(message)
        self.assertEqual(observed["unmet_obligations"], {"validated": "NOT_RUN"})
        self.assertEqual(observed["next_action"], "reconcile_unmet_obligations_with_native_owner_before_successor_request")
        adoption = self.observation("adopted"); adoption["detail"]["returned_sha256"] = digest(message)
        with self.assertRaisesRegex(Refused, "unmet completion"):
            self.channel.observe(adoption)

    def test_stale_generation_and_changed_configuration_refuse(self):
        self.submit()
        message = self.observation("delivered")
        binding = self.config["participants"]["setup"] | {"generation": 2}
        message["actor"]["binding_sha256"] = digest(binding)
        with self.assertRaisesRegex(Refused, "stale binding"):
            self.channel.observe(message)
        config = copy.deepcopy(self.config); config["participants"]["setup"] = binding
        with self.assertRaisesRegex(Refused, "configuration changed"):
            Requests.initialize(self.state, config)
        with self.assertRaisesRegex(Refused, "digest mismatch"):
            Requests(self.state, digest(config))

    def test_expiry_and_controls_stop_new_observations_but_preserve_inspection(self):
        self.submit()
        expired = Requests(self.state, digest(self.config), now=lambda: 4102444801)
        with self.assertRaisesRegex(Refused, "expired"):
            expired.observe(self.observation("delivered"))
        self.assertTrue(expired.inspect("setup-fix")["configuration_expired"])
        self.state.control("pause-dispatch")
        with self.assertRaisesRegex(Refused, "controls"):
            self.advance("delivered")
        self.assertEqual(self.channel.inspect("setup-fix")["stage"], "recorded")

    def test_allowance_and_size_do_not_change_existing_records(self):
        self.submit()
        second = self.request | {"id": "another"}; self.submit(second)
        with self.assertRaisesRegex(Refused, "allowance"):
            self.submit(self.request | {"id": "excess"})
        with self.assertRaisesRegex(Refused, "byte limit"):
            self.submit(self.request | {"objective": "x" * 9000})
        self.assertEqual(self.state.db.execute("SELECT COUNT(*) FROM dependency_requests").fetchone()[0], 2)

    def test_event_failure_rolls_back_submission_and_transition(self):
        with patch.object(self.state, "event", side_effect=OSError("fixture interrupted write")):
            with self.assertRaises(OSError): self.submit()
        with self.assertRaisesRegex(Refused, "unknown dependency"):
            self.channel.inspect("setup-fix")
        self.submit()
        with patch.object(self.state, "event", side_effect=OSError("fixture interrupted write")):
            with self.assertRaises(OSError): self.advance("delivered")
        self.assertEqual(self.channel.inspect("setup-fix")["observations"], {})

    def test_two_connections_submit_one_logical_request(self):
        def submit(_):
            state = State(self.root)
            try:
                return Requests(state, digest(self.config)).submit({"actor": self.actor("facman"), "request": self.request})
            finally:
                state.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(submit, range(2)))
        self.assertEqual([r["stage"] for r in results], ["recorded", "recorded"])
        self.assertEqual(self.state.db.execute("SELECT COUNT(*) FROM dependency_requests").fetchone()[0], 1)

    def test_waiting_dependency_does_not_block_unrelated_native_work(self):
        self.submit()
        self.assertEqual(self.state.claim(1)["task"], "unrelated")

    def test_read_only_state_cannot_write_and_inspection_does_not_add_events(self):
        self.submit(); self.advance("delivered")
        before = self.state.status()["events"]
        readonly = State(self.root, read_only=True)
        try:
            self.assertEqual(Requests(readonly, digest(self.config)).inspect("setup-fix")["stage"], "delivered")
            with self.assertRaises(sqlite3.OperationalError): readonly.event(None, "forbidden", {})
        finally:
            readonly.close()
        self.assertEqual(self.state.status()["events"], before)

    def test_unknown_fields_schema_and_bad_json_refuse(self):
        for changed in (self.request | {"execute": True}, self.request | {"schema": "future.v99"}):
            with self.assertRaises(Refused): self.submit(changed)
        for raw in (b'{"id":1,"id":2}', b'{"x":NaN}', b'x', b'"' + b'x' * 65536 + b'"'):
            with self.assertRaises(Refused): decode(raw)
        self.assertEqual(self.state.db.execute("SELECT COUNT(*) FROM dependency_requests").fetchone()[0], 0)

    def cli(self, command, *, payload=None, extra=(), expected=0):
        args = [sys.executable, "-B", "-m", "core.runtime.continuous_worker", command,
                "--state-root", str(self.root)]
        if command != "request-init": args += ["--configuration-sha256", digest(self.config)]
        if payload is not None:
            source = self.root / "message.json"; source.write_text(json.dumps(payload), encoding="utf-8")
            args += ["--input", str(source)]
        process = subprocess.run([*args, *extra], cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(process.returncode, expected, process.stdout + process.stderr)
        return json.loads(process.stdout)

    def test_actual_cli_exchange_resumes_between_separate_processes(self):
        config_file = self.root / "message.json"
        raw = json.dumps(self.config).encode()
        self.cli("request-init", payload=self.config, extra=("--sha256", hashlib.sha256(raw).hexdigest()))
        self.cli("request-submit", payload={"actor": self.actor("facman"), "request": self.request})
        for stage in ("delivered", "accepted", "returned", "adopted"):
            actual = self.cli("request-observe", payload=self.observation(stage))
            self.assertEqual(actual["stage"], stage)
        result = self.cli("request-status", extra=("--request-id", "setup-fix"))
        self.assertEqual(result["stage"], "adopted")
        self.assertEqual(result["mode"], "cooperative")
        self.assertFalse(result["claims_independently_verified"])
        config_file.unlink()

    def test_crash_after_record_before_acknowledgement_recovers_without_duplicate(self):
        message = {"actor": self.actor("facman"), "request": self.request}
        code = ("import json,os,sys; from pathlib import Path; "
                "from core.runtime.continuous_worker.state import State; "
                "from core.runtime.continuous_worker.requests import Requests; "
                "s=State(Path(sys.argv[1])); Requests(s,sys.argv[2]).submit(json.loads(sys.argv[3])); os._exit(77)")
        process = subprocess.run([sys.executable, "-B", "-c", code, str(self.root), digest(self.config),
                                  json.dumps(message)], cwd=ROOT, capture_output=True, timeout=15)
        self.assertEqual(process.returncode, 77, process.stderr)
        self.assertEqual(self.cli("request-submit", payload=message)["stage"], "recorded")
        self.assertEqual(self.state.db.execute("SELECT COUNT(*) FROM dependency_requests").fetchone()[0], 1)

    def test_cli_unknown_state_does_not_initialize_or_create_root(self):
        missing = self.root / "not-owned"
        process = subprocess.run([sys.executable, "-B", "-m", "core.runtime.continuous_worker", "request-status",
                                  "--state-root", str(missing), "--configuration-sha256", digest(self.config),
                                  "--request-id", "setup-fix"], cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(process.returncode, 2, process.stderr)
        self.assertFalse(missing.exists())

    def test_cli_refuses_existing_empty_uninitialized_and_unsupported_database_without_mutation(self):
        for kind in ("empty", "uninitialized", "unsupported"):
            with self.subTest(kind=kind):
                folder = self.root / kind; folder.mkdir()
                database = folder / "coordinator.sqlite3"
                if kind == "empty":
                    database.write_bytes(b'')
                elif kind == "uninitialized":
                    old = State(folder); old.close()
                else:
                    with closing(sqlite3.connect(database, isolation_level=None)) as db:
                        db.execute("CREATE TABLE preserve(value TEXT)")
                        db.execute("INSERT INTO preserve VALUES('owned original')")
                        db.execute("PRAGMA user_version=999")
                payload = folder / 'request.json'
                payload.write_text(json.dumps({"actor": self.actor("facman"), "request": self.request}))
                before = {p.name: p.read_bytes() for p in folder.iterdir() if p.name.startswith('coordinator.')}
                process = subprocess.run([sys.executable, '-B', '-m', 'core.runtime.continuous_worker',
                    'request-submit', '--state-root', str(folder), '--configuration-sha256', digest(self.config),
                    '--input', str(payload)], cwd=ROOT, capture_output=True, text=True, timeout=15)
                self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
                self.assertEqual(before, {p.name: p.read_bytes() for p in folder.iterdir() if p.name.startswith('coordinator.')})

    def test_cli_configuration_mismatch_preserves_database_and_journal_mode(self):
        self.state.close()
        with closing(sqlite3.connect(self.root / 'coordinator.sqlite3')) as db:
            db.execute('PRAGMA journal_mode=DELETE')
        database = self.root / 'coordinator.sqlite3'; before = database.read_bytes()
        payload = self.root / 'request.json'
        payload.write_text(json.dumps({"actor": self.actor("facman"), "request": self.request}))
        process = subprocess.run([sys.executable, '-B', '-m', 'core.runtime.continuous_worker',
            'request-submit', '--state-root', str(self.root), '--configuration-sha256', '0' * 64,
            '--input', str(payload)], cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
        self.assertEqual(database.read_bytes(), before)
        self.assertFalse((self.root / 'coordinator.sqlite3-wal').exists())
        changed = self.config | {"max_requests": 3}; raw = json.dumps(changed).encode()
        payload.write_bytes(raw)
        process = subprocess.run([sys.executable, '-B', '-m', 'core.runtime.continuous_worker',
            'request-init', '--state-root', str(self.root), '--sha256', hashlib.sha256(raw).hexdigest(),
            '--input', str(payload)], cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
        self.assertEqual(database.read_bytes(), before)
        self.assertFalse((self.root / 'coordinator.sqlite3-wal').exists())
        self.state = State(self.root)

    def test_explicit_init_preserves_sidecars_with_missing_or_empty_database(self):
        for empty in (False, True):
            for sidecars in (("-wal",), ("-shm",), ("-wal", "-shm")):
                with self.subTest(empty=empty, sidecars=sidecars):
                    folder = self.root / (str(empty) + "".join(sidecars)); folder.mkdir()
                    if empty:
                        (folder / "coordinator.sqlite3").write_bytes(b"")
                    for suffix in sidecars:
                        (folder / ("coordinator.sqlite3" + suffix)).write_bytes(b"preserve uncertain state" + suffix.encode())
                    raw = json.dumps(configuration(folder)).encode()
                    path = folder / "config.json"; path.write_bytes(raw)
                    before = {p.name: p.read_bytes() for p in folder.iterdir()}
                    process = subprocess.run([sys.executable, "-B", "-m", "core.runtime.continuous_worker",
                        "request-init", "--state-root", str(folder), "--input", str(path),
                        "--sha256", hashlib.sha256(raw).hexdigest()], cwd=ROOT, capture_output=True, text=True, timeout=15)
                    self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
                    self.assertIn("reconciliation", json.loads(process.stdout)["reason"])
                    self.assertEqual(before, {p.name: p.read_bytes() for p in folder.iterdir()})

    def test_explicit_init_preserves_unsupported_database(self):
        folder = self.root / 'unsupported-init'; folder.mkdir()
        database = folder / 'coordinator.sqlite3'
        with closing(sqlite3.connect(database)) as db: db.execute('PRAGMA user_version=999')
        config = configuration(folder); raw = json.dumps(config).encode()
        path = folder / 'config.json'; path.write_bytes(raw)
        before = database.read_bytes()
        process = subprocess.run([sys.executable, '-B', '-m', 'core.runtime.continuous_worker',
            'request-init', '--state-root', str(folder), '--input', str(path),
            '--sha256', hashlib.sha256(raw).hexdigest()], cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
        self.assertEqual(database.read_bytes(), before)
        self.assertFalse((folder / 'coordinator.sqlite3-wal').exists())


if __name__ == "__main__":
    unittest.main()
