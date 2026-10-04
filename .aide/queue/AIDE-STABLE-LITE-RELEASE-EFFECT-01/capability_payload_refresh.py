"""Select existing current qualification machinery for the capability payload."""
import importlib.util
import ctypes
import os
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
def qualify_capability(proof):
    proof_path = worker.OUTPUT / "qualification.json"
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
    print(json.dumps({"stage": "capability-payload-source-complete", "tests_qualified": 67,
                      "tests_executed_here": 18 if proof.get("source49_reuse") else 67,
                      "qualification_sha256": worker.sha(proof_path)}), flush=True)


def resume_source():
    if len(sys.argv) != 2:
        raise AssertionError("resume-source accepts no overrides")
    partial_path = TASK / "evidence/capability-payload-source-failure.json"
    if worker.sha(partial_path) != "d87fb2f2565752ff8cc4f8bcae1e2d3839975ec5fb029070bd93a606d76146a0":
        raise AssertionError("accepted partial result changed")
    partial = json.loads(partial_path.read_text(encoding="utf-8"))
    if (partial["status"] != "FAIL_VALIDATION_CONTEXT_AND_UNBOUND_LEDGER_C1_NOT_RUN"
            or partial["source49_passed"] != {"admission": 5, "public_fixtures": 8, "release": 36,
                                               "failures": 0, "errors": 0, "skips": 0}
            or not partial["collection_verified"] or not partial["retired"]
            or not partial["full_validation_failed"] or partial["capability18_executed"]):
        raise AssertionError("partial source evidence is not the reviewed subject")
    expected = {".aide/scripts/aide_lite.py", ".aide/scripts/tests/test_public_archive_fixture.py",
                ".aide/scripts/tests/test_q47_release_bundle.py", ".aide/scripts/tests/test_q48_github_release_draft.py",
                ".aide/scripts/tests/test_stable_release_admission.py", ".aide/policies/release-versioning.yaml"}
    inputs = partial["source_inputs_for_49_reuse"]
    if set(inputs) != expected or any(worker.sha(REPO / name) != digest for name, digest in inputs.items()):
        raise AssertionError("the 49 passing tests no longer cover these source inputs")
    os.environ.update(AIDE_RESOURCE_TEST_PARENT=str(worker.TMP), GIT_CONFIG_COUNT="1",
                      GIT_CONFIG_KEY_0="safe.directory", GIT_CONFIG_VALUE_0=str(REPO))
    identity = ctypes.create_unicode_buffer(256)
    size = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(size)):
        raise ctypes.WinError()
    if "CodexSandboxOffline" not in identity.value:
        raise AssertionError("expected restricted worker identity")
    proof = {"phase": "resume-source", "windows_identity": identity.value, "model_calls": 0,
             "outer_session_contained": False, "read_isolation": "unqualified", "retired_fixtures": [],
             "admission_tests": {"run": 5, "failures": 0, "errors": 0, "skips": 0},
             "public_fixture_tests": {"run": 8, "failures": 0, "errors": 0, "skips": 0},
             "release_tests": {"run": 36, "failures": 0, "errors": 0, "skips": 0},
             "source_inputs": dict(inputs),
             "source49_reuse": {"job_id": partial["job_id"], "source_commit": partial["source_commit"],
                                "source_tree": partial["source_tree"], "partial_proof_sha256": worker.sha(partial_path),
                                "receipt_sha256": partial["receipt_sha256"],
                                "entire_previous_job_passed": False}}
    for name in ("export-pack", "validate"):
        run = subprocess.run([sys.executable, "-B", str(worker.CLI), name], cwd=REPO, timeout=240)
        proof[name + "_exit_code"] = run.returncode
        if run.returncode:
            raise AssertionError(name + " failed")
    qualify_capability(proof)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "resume-source":
        resume_source()
    else:
        worker.main()
        if sys.argv[1] == "repair":
            proof = json.loads((worker.OUTPUT / "qualification.json").read_text(encoding="utf-8"))
            qualify_capability(proof)
