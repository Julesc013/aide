"""Exercise retained raw streams on real completion and timeout, then qualify payload."""
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
TASK = Path(__file__).resolve().parent
TMP = Path(os.environ["AIDE_JOB_TMP"]).resolve(strict=True)
OUTPUT = Path(os.environ["AIDE_JOB_OUTPUT"]).resolve(strict=True)

def main():
    spec = importlib.util.spec_from_file_location("qualified_delivered_additions", TASK / "delivered_additions.py")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    case = TMP / "case-delivered-capture-fault"
    case.mkdir()
    proof = {"schema": "aide.delivered-capture-fault.v1", "status": "RUNNING",
             "rows": [], "nested_model_calls": 0, "outer_contained": False}
    target = OUTPUT / "delivered-capture-fault.json"
    def save():
        target.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    identity = ctypes.create_unicode_buffer(256)
    length = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(length)):
        raise ctypes.WinError()
    if not identity.value.endswith("\\CodexSandboxOffline"):
        raise AssertionError("restricted fixture identity required")
    proof["identity"] = identity.value
    save()
    env = {**os.environ, "TEMP": str(case), "TMP": str(case), "TMPDIR": str(case),
           "PYTHONDONTWRITEBYTECODE": "1"}
    for label, code, timeout, expected in (
        ("completed", "import sys; print('complete-out',flush=True); print('complete-err',file=sys.stderr,flush=True)", 10, False),
        ("timeout", "import sys,time; print('partial-out',flush=True); print('partial-err',file=sys.stderr,flush=True); time.sleep(30)", 2, True)):
        out, err = OUTPUT / ("capture-" + label + ".stdout"), OUTPUT / ("capture-" + label + ".stderr")
        row = {"label": label, "status": "RUNNING", "timeout_seconds": timeout, "exception_observed": False}
        proof["rows"].append(row)
        save()
        try:
            result = helper.capture_streams([sys.executable, "-I", "-B", "-c", code], cwd=case, env=env,
                                            stdout_path=out, stderr_path=err, timeout=timeout)
            if expected or result.returncode != 0:
                raise AssertionError("actual command result differs from fixture expectation")
            row["exit_code"] = result.returncode
        except subprocess.TimeoutExpired:
            if not expected:
                raise
            row.update(exception_observed=True, exit_code=None)
        expected_out = b"partial-out\n" if expected else b"complete-out\n"
        expected_err = b"partial-err\n" if expected else b"complete-err\n"
        if out.read_bytes().replace(b"\r\n", b"\n") != expected_out or err.read_bytes().replace(b"\r\n", b"\n") != expected_err:
            raise AssertionError("partial raw bytes were lost or changed")
        row.update(status="PASS", stdout_sha256=helper.sha(out), stderr_sha256=helper.sha(err),
                   stdout_bytes=out.stat().st_size, stderr_bytes=err.stat().st_size)
        save()
    worker = helper.load("capture_fixture_retirement", helper.WORKER)
    worker.retire_owned_fixture(case)
    if case.exists():
        raise AssertionError("owned fault fixture was not retired")
    proof.update(status="PASS", owned_fixture_retired=True, timeout_child_not_accepted_as_success=True)
    save()
    helper.main()

if __name__ == "__main__":
    main()
