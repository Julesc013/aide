"""Qualify the original entry after its reviewed, additive runtime promotion."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

REPO = Path(__file__).resolve().parents[3]
TASK = Path(__file__).resolve().parent
CONFIG = REPO / ".aide.local/scoped-job-entry-01-execution.json"
EFFECT = TASK / "evidence/runtime-promotion-effect.json"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    effect = json.loads(EFFECT.read_text(encoding="utf-8"))
    if sha(CONFIG) != effect["after_sha256"]:
        raise AssertionError("selected original configuration differs from reviewed promotion")
    if sha(REPO / effect["archive"]) != effect["archive_sha256"]:
        raise AssertionError("promoted archive identity changed")
    identity = ctypes.create_unicode_buffer(256)
    size = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(size)):
        raise ctypes.WinError()
    if identity.value != "BLACKGLASS-WIN1\\CodexSandboxOffline":
        raise AssertionError("expected qualified restricted worker")
    process = subprocess.run(
        [sys.executable, "-B", str(REPO / ".aide/scripts/aide_lite.py"),
         "job", "inspect", "--config", str(CONFIG)],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8", timeout=60,
    )
    output = Path(os.environ["AIDE_JOB_OUTPUT"])
    raw = output / "original-entry-inspect.json"
    raw.write_text(json.dumps({"argv": process.args, "exit_code": process.returncode,
                               "stdout": process.stdout, "stderr": process.stderr},
                              sort_keys=True, indent=2) + "\n", encoding="utf-8")
    if process.returncode:
        raise AssertionError("promoted original entry inspection failed")
    inspected = json.loads(process.stdout)
    boundary = inspected["execution_boundary"]
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    digest = hashlib.sha256(json.dumps(config, sort_keys=True,
                                      separators=(",", ":")).encode()).hexdigest()
    if (inspected["writes"] is not False or inspected["config_digest"] != digest
            or inspected["active"]["job_id"] != os.environ["AIDE_JOB_ID"]
            or boundary["controls_outer_session"] is not False
            or boundary["provides_hard_filesystem_quota"] is not False
            or boundary["aggregate_admission_checked_by_inspection"] is not False
            or boundary["aggregate_limit_bytes"] != 268435456):
        raise AssertionError("effective original entry or inspection boundary mismatch")
    result = {"status": "PASS", "windows_identity": identity.value,
              "job_id": os.environ["AIDE_JOB_ID"], "configuration_sha256": sha(CONFIG),
              "runtime_archive_sha256": effect["archive_sha256"],
              "runtime_closure_count": effect["closure_count_after"],
              "python_version": sys.version, "platform": platform.platform(),
              "inspect_raw_sha256": sha(raw), "nested_model_calls": 0,
              "whole_session_contained": False, "hard_filesystem_quota": False,
              "worker_read_isolation": "unqualified"}
    (output / "qualified-runtime-probe.json").write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
