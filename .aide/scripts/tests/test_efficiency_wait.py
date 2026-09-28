"""Tiny portable observer tests; no model, process launch or bulk fixture."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("aide_lite_efficiency_test", REPO / ".aide/scripts/aide_lite.py")
lite = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lite
SPEC.loader.exec_module(lite)
JOB_ID = "a" * 32
SOURCE_COMMIT = "b" * 40
SOURCE_TREE = "c" * 40


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")


class EfficiencyWaitTests(unittest.TestCase):
    def setUp(self):
        parent = Path(os.environ["AIDE_JOB_TMP"])
        self.temp = tempfile.TemporaryDirectory(prefix="efficiency-wait-", dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.control = self.root / "control"
        self.retained = self.root / "retained"
        self.control.mkdir()
        self.retained.mkdir()
        self.config = self.root / "execution.json"
        write(self.config, {"schema": "aide.managed-workspace.local.v1",
                            "roots": {"control": str(self.control), "retained": str(self.retained)}})
        self.job = {"source_commit": SOURCE_COMMIT, "source_tree": SOURCE_TREE}
        self.manifest = digest(self.job)

    def receipt(self, *, phase="retired", exit_code=0, reason="exited", owner=True):
        target = self.retained / JOB_ID
        target.mkdir(exist_ok=True)
        if owner:
            write(target / "owner.json", {"job_id": JOB_ID, "manifest_digest": self.manifest})
        write(target / "receipt.json", {"job_id": JOB_ID, "manifest_digest": self.manifest,
             "job": self.job, "phase": phase, "scratch_absent": True,
             "reservation_released": True, "result": {"job_id": JOB_ID, "reason": reason,
             "exit_code": exit_code, "quiescent": True}, "raw_log": "x" * 3000})

    def wait(self, timeout=0, clock=lambda: 0, sleeper=lambda _: None):
        return lite.wait_for_managed_job(self.config, JOB_ID, self.manifest,
                                          timeout, 1, clock=clock, sleeper=sleeper)

    def test_terminal_is_bounded_repeatable_and_read_only(self):
        self.receipt()
        before = (self.retained / JOB_ID / "receipt.json").read_bytes()
        first, second = self.wait(), self.wait()
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "PASS")
        self.assertEqual(first["model_requests_started_by_observer"], 0)
        self.assertEqual(first["host_model_requests"], "unknown")
        self.assertEqual(first["evidence_status"], "receipt_present_outputs_unverified")
        self.assertLess(len(json.dumps(first)), 1400)
        self.assertEqual((self.retained / JOB_ID / "receipt.json").read_bytes(), before)

    def test_unchanged_wait_emits_only_terminal_view(self):
        write(self.control / "active.json", {"job_id": JOB_ID, "manifest_digest": self.manifest,
                                                  "job": self.job, "phase": "running"})
        tick = [0]
        def advance(seconds):
            tick[0] += seconds
            if tick[0] == 3:
                self.receipt()
                (self.control / "active.json").unlink()
        result = self.wait(timeout=5, clock=lambda: tick[0], sleeper=advance)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["observations"], 4)
        self.assertEqual(result["unchanged_observations"], 2)

    def test_timeout_is_pending_and_does_not_remove_active(self):
        write(self.control / "active.json", {"job_id": JOB_ID, "manifest_digest": self.manifest,
                                                  "job": self.job, "phase": "running"})
        result = self.wait()
        self.assertEqual(result["status"], "PENDING")
        self.assertFalse(result["terminal"])
        self.assertTrue((self.control / "active.json").exists())

    def test_missing_mismatch_and_nonterminal_receipt_cannot_pass(self):
        self.assertEqual(self.wait()["status"], "MISSING")
        write(self.control / "active.json", {"job_id": "d" * 32,
                                                  "manifest_digest": self.manifest, "phase": "running"})
        self.assertEqual(self.wait()["status"], "OTHER_ATTEMPT")
        (self.control / "active.json").unlink()
        self.receipt(phase="collected")
        self.assertEqual(self.wait()["status"], "ACTION_REQUIRED")
        self.receipt()
        write(self.retained / JOB_ID / "owner.json", {"job_id": JOB_ID, "manifest_digest": "0" * 64})
        self.assertEqual(self.wait()["status"], "EVIDENCE_UNAVAILABLE")

    def test_failure_oversize_and_redirected_root_cannot_pass(self):
        self.receipt(exit_code=1)
        self.assertEqual(self.wait()["status"], "FAIL")
        (self.retained / JOB_ID / "receipt.json").write_bytes(b"x" * (1024 * 1024 + 1))
        self.assertEqual(self.wait()["status"], "EVIDENCE_UNAVAILABLE")
        write(self.config, {"schema": "aide.managed-workspace.local.v1",
                            "roots": {"control": str(self.control),
                                      "retained": str(self.retained / ".." / "retained")}})
        with self.assertRaisesRegex(ValueError, "absolute child"):
            self.wait()

    def test_portable_cli_without_source_checkout(self):
        self.receipt()
        consumer = self.root / "consumer" / ".aide" / "scripts"
        consumer.mkdir(parents=True)
        script = consumer / "aide_lite.py"
        script.write_bytes((REPO / ".aide/scripts/aide_lite.py").read_bytes())
        command = [sys.executable, "-I", "-B", str(script), "--repo-root", str(self.root / "consumer"),
                   "job", "wait", "--config", str(self.config), "--job-id", JOB_ID,
                   "--manifest-digest", self.manifest, "--timeout-seconds", "0"]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=15)
        self.assertEqual(completed.returncode, 0, completed.stderr[-500:])
        self.assertEqual(json.loads(completed.stdout)["status"], "PASS")
        self.assertFalse((self.root / "consumer" / "core").exists())


if __name__ == "__main__":
    unittest.main()
