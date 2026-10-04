"""Select existing current qualification machinery for the capability payload."""
import importlib.util
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

TASK = Path(__file__).resolve().parent
REPO = TASK.parents[2]
worker_path = REPO / ".aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/worker.py"
spec = importlib.util.spec_from_file_location("current_lite_qualification", worker_path)
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)
# Only the accepted source-proof owner changes; existing canaries and assertions remain.
worker.TASK = TASK
if __name__ == "__main__":
    worker.main()
    if sys.argv[1] == "repair":
        proof_path = worker.OUTPUT / "qualification.json"
        proof = json.loads(proof_path.read_text(encoding="utf-8"))
        proof["status"] = "CAPABILITY_CHECK_PENDING"
        worker.write(proof_path, proof)
        argv = [sys.executable, "-B", str(REPO / ".aide/scripts/tests/test_x_os_02_capability_reality.py")]
        result = subprocess.run(argv, cwd=REPO, capture_output=True, timeout=180)
        print("=== current capability source tests ===", flush=True)
        sys.stdout.buffer.write(result.stdout); sys.stdout.buffer.flush()
        sys.stderr.buffer.write(result.stderr); sys.stderr.buffer.flush()
        text = (result.stdout + result.stderr).decode("utf-8", errors="replace")
        if result.returncode or not re.search(r"Ran 18 tests? in ", text) or "skipped=" in text:
            raise AssertionError("current capability source tests failed or count/skips changed")
        proof["capability_tests"] = {"run": 18, "failures": 0, "errors": 0, "skips": 0,
                                    "stdout_raw_sha256": hashlib.sha256(result.stdout).hexdigest(),
                                    "stderr_raw_sha256": hashlib.sha256(result.stderr).hexdigest()}
        for name in (".aide/scripts/tests/test_x_os_02_capability_reality.py",
                     ".aide/capabilities/capability-evidence-bindings.schema.json",
                     ".aide/capabilities/capability-seeds.yaml",
                     ".aide/policies/capability-reality.yaml",
                     "docs/reference/capability-reality-ledger.md"):
            proof["source_inputs"][name] = worker.sha(REPO / name)
        proof["status"] = "PASS"
        worker.write(proof_path, proof)
        print(json.dumps({"stage": "capability-payload-source-complete", "tests": 67,
                          "qualification_sha256": worker.sha(proof_path)}), flush=True)
