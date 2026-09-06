from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker.windows_job import WindowsJobHost, sanitized_environment


@unittest.skipUnless(os.name == "nt", "Windows owned host qualification")
class WindowsHostTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aide-continuous-host-")
        self.root = Path(self.temp.name)
        self.host = WindowsJobHost()

    def tearDown(self):
        self.temp.cleanup()

    def run_code(self, source, **overrides):
        options = dict(cwd=self.root, input_bytes=b"", output_dir=self.root / uuid.uuid4().hex,
                       job_id=uuid.uuid4().hex, timeout=5, output_limit=65536,
                       memory_limit=536870912, process_limit=8)
        options.update(overrides)
        receipt = self.host.run([sys.executable, "-c", source], **options)
        return receipt, options["output_dir"]

    def test_real_process_output_and_quiescence(self):
        receipt, output = self.run_code("print('real owned process')")
        self.assertEqual(receipt["exit_code"], 0)
        self.assertTrue(receipt["quiescent"])
        self.assertIn("real owned process", (output / "stdout").read_text())

    def test_stdin_and_stderr(self):
        receipt, output = self.run_code("import sys; print(sys.stdin.read()); print('err', file=sys.stderr)",
                                        input_bytes=b"bounded input")
        self.assertEqual(receipt["reason"], "exited")
        self.assertIn("bounded input", (output / "stdout").read_text())
        self.assertIn("err", (output / "stderr").read_text())

    def test_output_flood_is_bounded(self):
        receipt, output = self.run_code("import os; b=b'x'*8192\nwhile True: os.write(1,b)", output_limit=4096)
        self.assertEqual(receipt["reason"], "output_limit_or_io_error")
        self.assertLessEqual(sum((output / n).stat().st_size for n in ("stdout", "stderr")), 4096)
        self.assertTrue(receipt["quiescent"])

    def test_timeout_kills_child_and_grandchild(self):
        heartbeat = self.root / "heartbeat"
        grandchild = "import pathlib,time\np=pathlib.Path(" + repr(str(heartbeat)) + ")\nwhile True:\n p.write_text(str(time.time()))\n time.sleep(.02)"
        child = "import subprocess,sys,time\nsubprocess.Popen([sys.executable,'-c'," + repr(grandchild) + "])\ntime.sleep(60)"
        parent = "import subprocess,sys,time\nsubprocess.Popen([sys.executable,'-c'," + repr(child) + "])\ntime.sleep(60)"
        receipt, _ = self.run_code(parent, timeout=1)
        self.assertEqual(receipt["reason"], "timeout")
        self.assertTrue(heartbeat.exists(), "descendant must actually run before containment is tested")
        last = heartbeat.read_bytes()
        time.sleep(.15)
        self.assertEqual(heartbeat.read_bytes(), last)

    def test_parent_success_still_cleans_descendants(self):
        marker = self.root / "late-write"
        child = "import time,pathlib; time.sleep(1); pathlib.Path(" + repr(str(marker)) + ").write_text('escaped')"
        parent = "import subprocess,sys; subprocess.Popen([sys.executable,'-c'," + repr(child) + "])"
        receipt, _ = self.run_code(parent)
        self.assertTrue(receipt["quiescent"])
        time.sleep(1.1)
        self.assertFalse(marker.exists())

    def test_cancel_kills_owned_work(self):
        start = time.monotonic()
        receipt, _ = self.run_code("import time; time.sleep(60)", cancelled=lambda: time.monotonic() - start > .15)
        self.assertEqual(receipt["reason"], "cancelled")
        self.assertTrue(receipt["quiescent"])

    def test_supervisor_hard_death_kills_descendants(self):
        marker = self.root / "supervisor-heartbeat"
        child = "import pathlib,time\np=pathlib.Path(" + repr(str(marker)) + ")\nwhile True:\n p.write_text(str(time.time()))\n time.sleep(.02)"
        job_id = uuid.uuid4().hex
        source = (
            "import sys\nsys.path.insert(0," + repr(str(ROOT)) + ")\n"
            "from core.runtime.continuous_worker.windows_job import WindowsJobHost\n"
            "from pathlib import Path\n"
            "WindowsJobHost().run([" + repr(sys.executable) + ",'-c'," + repr(child) + "],"
            "cwd=Path(" + repr(str(self.root)) + "),input_bytes=b'',output_dir=Path(" +
            repr(str(self.root / "hard-death")) + "),job_id=" + repr(job_id) +
            ",timeout=60,output_limit=8192,memory_limit=536870912,process_limit=8)\n")
        supervisor = subprocess.Popen([sys.executable, "-c", source], env=sanitized_environment(),
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            deadline = time.monotonic() + 10
            while not marker.exists() and time.monotonic() < deadline and supervisor.poll() is None:
                time.sleep(.02)
            self.assertTrue(marker.exists(), "real child must start")
            supervisor.kill()  # Only this test-created owned supervisor handle.
            supervisor.communicate(timeout=10)
            observation = self.host.reconcile(job_id)
            self.assertTrue(observation["quiescent"])
            last = marker.read_bytes()
            time.sleep(.15)
            self.assertEqual(marker.read_bytes(), last)
        finally:
            if supervisor.poll() is None:
                supervisor.kill()
            supervisor.communicate(timeout=10)

    def test_absent_job_reconciliation_never_kills_pid(self):
        self.assertTrue(self.host.reconcile(uuid.uuid4().hex)["quiescent"])

    def test_no_secret_environment_forwarding(self):
        original = os.environ.get("CODEX_API_KEY")
        os.environ["CODEX_API_KEY"] = "synthetic-test-only"
        try:
            self.assertNotIn("CODEX_API_KEY", sanitized_environment())
            receipt, output = self.run_code("import os; print('CODEX_API_KEY' in os.environ)")
            self.assertEqual(receipt["exit_code"], 0)
            self.assertEqual((output / "stdout").read_text().strip(), "False")
        finally:
            if original is None:
                os.environ.pop("CODEX_API_KEY", None)
            else:
                os.environ["CODEX_API_KEY"] = original


    def test_supervisor_death_at_each_atomic_creation_boundary(self):
        for stage in ("before_create", "created_suspended", "resumed"):
            with self.subTest(stage=stage):
                checkpoint = self.root / (stage + ".checkpoint")
                effect = self.root / (stage + ".effect")
                job_id = uuid.uuid4().hex
                worker = "import pathlib,time; pathlib.Path(" + repr(str(effect)) + ").write_text('started'); time.sleep(60)"
                source = (
                    "import sys,time\nsys.path.insert(0," + repr(str(ROOT)) + ")\n"
                    "from core.runtime.continuous_worker.windows_job import WindowsJobHost\n"
                    "from pathlib import Path\n"
                    "def checkpoint(stage):\n"
                    " if stage == " + repr(stage) + ":\n"
                    "  Path(" + repr(str(checkpoint)) + ").write_text(stage)\n"
                    "  time.sleep(60)\n"
                    "WindowsJobHost().run([" + repr(sys.executable) + ",'-c'," + repr(worker) + "],"
                    "cwd=Path(" + repr(str(self.root)) + "),input_bytes=b'',output_dir=Path(" +
                    repr(str(self.root / (stage + "-output"))) + "),job_id=" + repr(job_id) +
                    ",timeout=60,output_limit=8192,memory_limit=536870912,process_limit=8,checkpoint=checkpoint)\n")
                supervisor = subprocess.Popen([sys.executable, "-c", source], env=sanitized_environment(),
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                              creationflags=subprocess.CREATE_NO_WINDOW)
                try:
                    deadline = time.monotonic() + 10
                    while not checkpoint.exists() and supervisor.poll() is None and time.monotonic() < deadline:
                        time.sleep(.02)
                    self.assertTrue(checkpoint.exists(), "supervisor must reach the tested boundary")
                    supervisor.kill()
                    supervisor.communicate(timeout=10)
                    self.assertTrue(self.host.reconcile(job_id)["quiescent"])
                    if stage in ("before_create", "created_suspended"):
                        self.assertFalse(effect.exists(), "worker code ran before permitted resume")
                finally:
                    if supervisor.poll() is None:
                        supervisor.kill()
                    supervisor.communicate(timeout=10)


if __name__ == "__main__":
    unittest.main()

