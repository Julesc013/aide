"""Synthetic pipeline tests. These are NOT the required live two-task acceptance."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import uuid
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker.contract import file_hash, read_activation, snapshot, changed
from core.runtime.continuous_worker.coordinator import Coordinator
from core.runtime.continuous_worker.state import Refused, digest
from core.runtime.continuous_worker.locking import supervisor_lock
from core.runtime.continuous_worker.windows_job import WindowsJobHost


def registered(exe, *args, inputs=None):
    return {"argv": [str(exe), *args], "sha256": file_hash(exe), "inputs": inputs or {}}


class SyntheticHost:
    """Fakes model/broker boundaries; executes the independent test command for real."""
    def __init__(self, *, fail_test=False, lose_merge=False, fail_code=False):
        self.sessions = []
        self.integrated = {}
        self.applies = 0
        self.fail_test, self.lose_merge, self.fail_code = fail_test, lose_merge, fail_code
        self.jobs = []

    def reconcile(self, job_id):
        return {"quiescent": True, "observation": "synthetic reconciliation"}

    def run(self, command, **options):
        self.jobs.append(options["job_id"])
        output = options["output_dir"]
        payload = options["input_bytes"].decode()
        if any("synthetic_broker.py" in arg for arg in command):
            request = json.loads(payload)
            if command[-1] == "apply":
                self.applies += 1
                self.integrated[request["attempt"]] = request
                if self.lose_merge:
                    self.lose_merge = False
                    raise OSError("injected lost merge response")
            done = request["attempt"] in self.integrated
            text = json.dumps({"status": "integrated" if done else "absent", "request_digest": digest(request),
                               "integrated_identity": request["subject"]["identity"] if done else "",
                               "receipt_ref": "synthetic://observed-integration" if done else ""})
        elif "exec" in command:
            session = str(uuid.uuid4())
            self.sessions.append(session)
            review = "Independently review" in payload
            identity = payload.split("subject_identity=")[1].split()[0]
            if not review:
                (Path(options["cwd"]) / "value.py").write_text("VALUE = 2\n", encoding="utf-8")
            result = {"status": "fail" if self.fail_code else "pass", "summary": "synthetic worker",
                      "subject_identity": identity, "findings": []}
            events = [{"type": "thread.started", "thread_id": session},
                      {"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps(result)}},
                      {"type": "turn.completed", "usage": {"input_tokens": 1, "output_tokens": 1}}]
            text = "\n".join(json.dumps(e) for e in events)
        else:
            if not self.fail_test:
                return WindowsJobHost().run(command, **options)
            text = "injected test failure"
        output.mkdir(parents=True)
        (output / "stdin").write_bytes(options["input_bytes"])
        (output / "stdout").write_text(text, encoding="utf-8")
        (output / "stderr").write_text("", encoding="utf-8")
        return {"exit_code": 1 if self.fail_test and "exec" not in command and not any("synthetic_broker.py" in arg for arg in command) else 0,
                "reason": "exited", "quiescent": True, "job_id": options["job_id"],
                "bytes": len(text), "io_errors": []}


@unittest.skipUnless(os.name == "nt", "pipeline uses the Windows owned observation host")
class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aide-continuous-pipeline-")
        self.root = Path(self.temp.name)
        self.git = Path(shutil.which("git")).resolve()
        self.config = self.make_config()
        self.path = self.root / "activation.json"
        self.write_config()
        self.runners = []

    def tearDown(self):
        for runner in self.runners:
            runner.state.close()
        self.temp.cleanup()

    def git_run(self, root, *args):
        return subprocess.run([str(self.git), "-C", str(root), *args], check=True, capture_output=True).stdout.decode().strip()

    def make_config(self):
        tasks = []
        qualification = self.root / "synthetic-qualification.txt"
        qualification.write_text("TEST FIXTURE ONLY; not actual host or integration authority.")
        broker = self.root / "synthetic_broker.py"
        broker.write_text("# Synthetic test double; never a live integration broker.")
        for name in ("one", "two"):
            workspace = self.root / name
            workspace.mkdir()
            self.git_run(workspace, "init", "-q")
            self.git_run(workspace, "config", "user.name", "AIDE test")
            self.git_run(workspace, "config", "user.email", "aide-test@example.invalid")
            self.git_run(workspace, "config", "core.autocrlf", "false")
            (workspace / "value.py").write_text("VALUE = 1\n", encoding="utf-8")
            self.git_run(workspace, "add", "value.py")
            self.git_run(workspace, "commit", "-qm", "test fixture")
            source = self.root / (name + ".admission")
            source.write_text("synthetic task " + name)
            tasks.append({"id": name, "source": str(source), "source_sha256": file_hash(source),
                          "workspace": str(workspace), "base": self.git_run(workspace, "rev-parse", "HEAD"),
                          "allowed_paths": ["value.py"], "depends_on": [] if name == "one" else ["one"],
                          "instructions": "Change fixture VALUE to 2. This is a synthetic test.",
                          "test_commands": [registered(sys.executable, "-c", "import runpy; assert runpy.run_path('value.py')['VALUE'] == 2")],
                          "repository": "synthetic-" + name})
        return {"schema": "aide.continuous-worker.activation.v0",
                "runtime_files": {p.name: file_hash(p) for p in (ROOT / "core/runtime/continuous_worker").glob("*.py")},
                "state_root": str(self.root / "state"), "expires_at": time.time() + 600,
                "limits": {"max_attempts": 2, "max_sessions": 4, "max_processes": 8,
                           "max_integration_queries": 6, "process_seconds": 10, "programme_seconds": 600,
                           "output_bytes": 65536, "memory_bytes": 536870912,
                           "max_state_bytes": 104857600, "min_free_bytes": 1048576},
                "codex": registered(sys.executable), "git": registered(self.git), "tasks": tasks,
                "worker_models": {"coding": "synthetic-coder", "assurance": "synthetic-reviewer"},
                "qualification": {key: {"path": str(qualification), "sha256": file_hash(qualification)}
                                  for key in ("isolated_worker_host", "credential_boundary", "integration_delegation")},
                "integration": {"cwd": str(self.root),
                                "query": registered(sys.executable, "-I", "-B", str(broker), "query",
                                                    inputs={str(broker): file_hash(broker)}),
                                "apply": registered(sys.executable, "-I", "-B", str(broker), "apply",
                                                    inputs={str(broker): file_hash(broker)})}}

    def write_config(self):
        self.path.write_text(json.dumps(self.config), encoding="utf-8")
        self.approval = file_hash(self.path)

    def runner(self, host=None):
        runner = Coordinator(self.path, self.approval, host=host or SyntheticHost())
        self.runners.append(runner)
        return runner

    def test_two_tasks_automatically_complete_with_fresh_sessions_and_real_tests(self):
        host = SyntheticHost()
        result = self.runner(host).run()
        self.assertEqual([t["status"] for t in result["tasks"]], ["succeeded", "succeeded"])
        self.assertEqual(len(set(host.sessions)), 4)
        self.assertEqual(host.applies, 2)

    def test_failing_real_validation_never_reaches_integration(self):
        # Configure a genuine failing command, executed through the real owned process host.
        self.config["tasks"][0]["test_commands"] = [registered(sys.executable, "-c", "raise SystemExit(3)")]
        self.write_config()
        host = SyntheticHost()
        result = self.runner(host).run()
        self.assertEqual(result["tasks"][0]["status"], "blocked")
        self.assertEqual(host.applies, 0)

    def test_lost_merge_response_queries_without_duplicate_apply(self):
        host = SyntheticHost(lose_merge=True)
        runner = self.runner(host)
        first = runner.run()
        self.assertEqual(first["active"]["stage"], "integration_pending")
        self.assertEqual(host.applies, 1)
        # Same durable ledger, new coordinator instance and process ownership pass.
        second = self.runner(host).run()
        self.assertEqual([t["status"] for t in second["tasks"]], ["succeeded", "succeeded"])
        self.assertEqual(host.applies, 2)

    def test_interrupted_coding_keeps_patch_and_blocks_duplicate_writer(self):
        runner = self.runner()
        attempt = runner.state.claim(2)
        runner.state.intent(attempt["id"], "coding", {"job_id": uuid.uuid4().hex})
        path = Path(attempt["spec"]["workspace"]) / "value.py"
        path.write_text("VALUE = 99\n")
        result = runner.run()
        self.assertEqual(result["tasks"][0]["status"], "blocked")
        self.assertEqual(path.read_text(), "VALUE = 99\n")
        self.assertFalse(result["unresolved_effects"])

    def test_source_drift_refuses_before_claim(self):
        runner = self.runner()
        Path(self.config["tasks"][0]["source"]).write_text("changed authority")
        with self.assertRaisesRegex(Refused, "admission source drift"):
            runner.run()
        self.assertIsNone(runner.state.active())

    def test_moved_base_blocks_without_coding(self):
        self.config["tasks"][0]["base"] = "0" * 40
        self.write_config()
        host = SyntheticHost()
        result = self.runner(host).run()
        self.assertEqual(result["tasks"][0]["status"], "blocked")
        self.assertFalse(host.sessions)

    def test_pause_and_resume_keep_durable_tasks(self):
        runner = self.runner()
        runner.state.control("pause-dispatch")
        result = runner.run()
        self.assertEqual([t["status"] for t in result["tasks"]], ["ready", "ready"])
        runner.state.control("resume")
        self.assertEqual([t["status"] for t in runner.run()["tasks"]], ["succeeded", "succeeded"])

    def test_cross_ledger_same_workspace_lock_refuses(self):
        runner = self.runner()
        with supervisor_lock(Path(self.config["tasks"][0]["workspace"]) / ".git"):
            with self.assertRaisesRegex(Refused, "another supervisor"):
                runner.run()
        self.assertFalse(runner.state.unresolved())

    def test_nan_expiry_refused(self):
        self.config["expires_at"] = float("nan")
        self.write_config()
        with self.assertRaisesRegex(Refused, "expiry"):
            self.runner()

    def test_storage_floor_refuses_dispatch(self):
        runner = self.runner()
        with patch("core.runtime.continuous_worker.coordinator.shutil.disk_usage") as usage:
            usage.return_value.free = 0
            with self.assertRaisesRegex(Refused, "storage"):
                runner.run()
        self.assertFalse(runner.state.unresolved())

    def test_worker_session_budget_blocks_second_task(self):
        self.config["limits"]["max_sessions"] = 2
        self.write_config()
        host = SyntheticHost()
        result = self.runner(host).run()
        self.assertEqual([t["status"] for t in result["tasks"]], ["succeeded", "blocked"])
        self.assertEqual(len(host.sessions), 2)

    def test_integration_broker_input_drift_refused(self):
        source = self.root / "broker.py"
        source.write_text("print('before')")
        self.config["integration"]["query"] = registered(sys.executable, str(source), inputs={str(source): file_hash(source)})
        self.write_config()
        source.write_text("print('after')")
        with self.assertRaisesRegex(Refused, "input drift"):
            self.runner()

    def test_index_only_mutation_refused(self):
        spec = self.config["tasks"][0]
        before = snapshot([str(self.git)], spec["workspace"])
        self.git_run(spec["workspace"], "update-index", "--chmod=+x", "value.py")
        after = snapshot([str(self.git)], spec["workspace"])
        with self.assertRaisesRegex(Refused, "Git index"):
            changed(before, after, ["value.py"])

    def test_permission_file_edit_refused(self):
        spec = self.config["tasks"][0]
        before = snapshot([str(self.git)], spec["workspace"])
        path = Path(spec["workspace"]) / ".github"
        path.mkdir()
        (path / "policy").write_text("widened")
        after = snapshot([str(self.git)], spec["workspace"])
        with self.assertRaisesRegex(Refused, "escaped"):
            changed(before, after, ["value.py"])


    def test_unpinned_broker_entrypoint_refused_even_with_unrelated_input(self):
        script = self.root / "untrusted_broker.py"
        script.write_text("print('unpinned')")
        other = self.root / "unrelated"
        other.write_text("pinned but not executable")
        self.config["integration"]["query"] = registered(sys.executable, "-I", "-B", str(script), "query",
                                                         inputs={str(other): file_hash(other)})
        self.write_config()
        with self.assertRaisesRegex(Refused, "entrypoint"):
            self.runner()

    def test_cross_task_authority_in_writer_clone_refused(self):
        source = Path(self.config["tasks"][0]["workspace"]) / "second.admission"
        source.write_text("would let first writer change second task")
        self.config["tasks"][1]["source"] = str(source)
        self.config["tasks"][1]["source_sha256"] = file_hash(source)
        self.write_config()
        with self.assertRaisesRegex(Refused, "programme authority"):
            self.runner()

    def test_corrupt_completed_test_evidence_refused_after_restart(self):
        host = SyntheticHost(lose_merge=True)
        runner = self.runner(host)
        first = runner.run()
        ident = first["active"]["id"]
        evidence = json.loads(runner.state.active()["evidence"])
        (Path(evidence["tests"][0]["output"]) / "stdout").write_text("tampered")
        second = self.runner(host).run()
        self.assertEqual(second["active"]["id"], ident)
        self.assertEqual(host.applies, 1)
        last = runner.state.db.execute("SELECT body FROM events WHERE kind='uncertain' ORDER BY seq DESC").fetchone()
        self.assertIn("evidence changed", last[0])

    def test_null_broker_payload_refused(self):
        path = self.root / "broker-output"
        path.mkdir()
        (path / "stdout").write_text("null")
        with self.assertRaises(Refused):
            Coordinator.parse_broker(path, {})


    def test_inflight_admission_drift_stops_real_owned_process(self):
        runner = self.runner()
        runner.host = WindowsJobHost()
        attempt = runner.state.claim(2)
        source = self.config["tasks"][0]["source"]
        code = "from pathlib import Path; import time; Path(" + repr(source) + ").write_text('injected drift'); time.sleep(60)"
        _, receipt = runner.effect(attempt, "test.0", [sys.executable, "-c", code], attempt["spec"]["workspace"], "")
        self.assertTrue(receipt["quiescent"])
        self.assertEqual(receipt["reason"], "cancelled")
        self.assertIn("admission source drift", receipt["monitor_reason"])

    def test_inflight_state_growth_stops_real_owned_process(self):
        self.config["limits"]["max_state_bytes"] = 1048576
        self.write_config()
        runner = self.runner()
        runner.host = WindowsJobHost()
        attempt = runner.state.claim(2)
        flood = runner.state.root / "synthetic-state-growth"
        code = "from pathlib import Path; import time; Path(" + repr(str(flood)) + ").write_bytes(b'x'*1048577); time.sleep(60)"
        _, receipt = runner.effect(attempt, "test.0", [sys.executable, "-c", code], attempt["spec"]["workspace"], "")
        self.assertTrue(receipt["quiescent"])
        self.assertEqual(receipt["reason"], "cancelled")
        self.assertIn("storage budget", receipt["monitor_reason"])

    def test_failed_durable_intent_never_dispatches(self):
        host = SyntheticHost()
        runner = self.runner(host)
        attempt = runner.state.claim(2)
        runner.state.db.execute("PRAGMA query_only=ON")
        import sqlite3
        with self.assertRaises(sqlite3.DatabaseError):
            runner.effect(attempt, "coding", [sys.executable, "-c", "print('must not run')"],
                          attempt["spec"]["workspace"], "")
        self.assertFalse(host.jobs)


if __name__ == "__main__":
    unittest.main()

