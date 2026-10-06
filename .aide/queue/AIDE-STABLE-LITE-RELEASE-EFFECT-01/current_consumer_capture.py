"""Preserve raw consumer streams using qualified capture; reuse original acceptance."""
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
TASK = Path(__file__).resolve().parent

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def phase(argv):
    if (len(argv) != 4 or argv[1] not in ("consumer-first", "consumer-rest", "consumer-tail")
            or argv[2] != "--zip-sha256" or len(argv[3]) != 64
            or any(c not in "0123456789abcdef" for c in argv[3])):
        raise AssertionError("only exact current consumer phases and SHA256 admitted")
    return argv[1]

def tail(worker, zip_sha256):
    worker.os.environ.update(AIDE_RESOURCE_TEST_PARENT=str(worker.TMP), GIT_CONFIG_COUNT="1",
                             GIT_CONFIG_KEY_0="safe.directory", GIT_CONFIG_VALUE_0=str(worker.REPO))
    identity = worker.ctypes.create_unicode_buffer(256)
    size = worker.ctypes.c_ulong(len(identity))
    if not worker.ctypes.windll.secur32.GetUserNameExW(2, identity, worker.ctypes.byref(size)):
        raise worker.ctypes.WinError()
    if "CodexSandboxOffline" not in identity.value:
        raise AssertionError("expected restricted worker identity")
    asset = worker.asset_identity()
    if asset["zip_sha256"] != zip_sha256:
        raise AssertionError("consumer subject changed")
    z, zs, cs = str(worker.ZIP), asset["zip_sha256"], asset["cli_sha256"]
    hs = worker.sha(worker.CAN / "lifecycle_helper.py")
    cases = (
        (4, "public_cli_canary.py", [z, zs, hs]),
        (5, "forced_restart_runner.py", [z, zs]),
        (6, "job_forms_canary.py", ["--zip", z, "--zip-sha256", zs, "--cli-sha256", cs,
                                  "--out", "unused.json"]),
        (7, "taskos_delivered_canary.py", [z, zs, cs]),
    )
    result = {"phase": "consumer-tail", "windows_identity": identity.value, "model_calls": 0,
              "outer_session_contained": False, "read_isolation": "unqualified",
              "case_indices": [4, 5, 6, 7], "whole_suite_definition_cases": 8,
              "cases_executed": 4, "retired_fixtures": [], "asset": asset}
    for index, name, parameters in cases:
        label = f"case-{index:02d}"
        scratch, retained = worker.TMP / label, worker.OUTPUT / label
        scratch.mkdir(); retained.mkdir()
        env = {**worker.os.environ, "AIDE_JOB_TMP": str(scratch), "AIDE_JOB_OUTPUT": str(retained),
               "TEMP": str(scratch), "TMP": str(scratch), "TMPDIR": str(scratch)}
        worker.invoke(label, [sys.executable, "-I", "-B", str(worker.CAN / name), *parameters],
                      env=env, destination=retained)
        worker.retire_owned_fixture(scratch)
        result["retired_fixtures"].append(label)
    result["status"] = "PASS"
    worker.write(worker.OUTPUT / "qualification.json", result)
    print(json.dumps({"status": "PASS", "phase": result["phase"], "cases_executed": 4,
                      "qualification_sha256": worker.sha(worker.OUTPUT / "qualification.json")}), flush=True)

def main():
    selected_phase = phase(sys.argv)
    selected = load("current_consumer_original", TASK / "capability_payload_refresh.py")
    worker = selected.worker
    capture = load("current_consumer_capture", TASK / "delivered_additions.py")
    def invoke(label, argv, *, env=None, destination=worker.OUTPUT):
        out = destination / (label + ".stdout")
        err = destination / (label + ".stderr")
        process = destination / (label + "-process.json")
        began = time.monotonic()
        record = {"argv": argv, "exit_code": None, "stdout": "", "stderr": "",
                  "status": "RUNNING", "timeout_seconds": 600, "started_at_unix_ns": time.time_ns()}
        worker.write(process, record)
        failure = None
        result = None
        try:
            result = capture.capture_streams(argv, cwd=worker.REPO, env=env,
                                            stdout_path=out, stderr_path=err, timeout=600)
            record["exit_code"] = result.returncode
        except (subprocess.TimeoutExpired, OSError) as exc:
            failure = exc
            record.update(failure_type=type(exc).__name__, failure=str(exc),
                          timed_out=isinstance(exc, subprocess.TimeoutExpired))
        for name, path in (("stdout", out), ("stderr", err)):
            if path.exists():
                # Match the original text=True universal-newline process fields;
                # the separate retained files preserve the exact original bytes.
                record[name] = path.read_bytes().decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
                record[name + "_raw_sha256"] = worker.sha(path)
                record[name + "_raw_bytes"] = path.stat().st_size
        record["status"] = "PASS" if failure is None and record["exit_code"] == 0 else "FAILED"
        record["elapsed_seconds"] = time.monotonic() - began
        worker.write(process, record)
        print(json.dumps({"stage": label, "exit_code": record["exit_code"],
                          "status": record["status"]}), flush=True)
        if failure is not None:
            raise failure
        if result.returncode:
            raise AssertionError(f"{label} failed; full process output retained")
        return subprocess.CompletedProcess(argv, result.returncode, record["stdout"], record["stderr"])
    worker.invoke = invoke
    if selected_phase == "consumer-tail":
        tail(worker, sys.argv[3])
    else:
        worker.main()

if __name__ == "__main__":
    main()
