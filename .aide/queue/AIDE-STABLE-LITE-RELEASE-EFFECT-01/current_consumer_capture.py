"""Preserve raw consumer streams using qualified capture; reuse original acceptance."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
TASK = Path(__file__).resolve().parent

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    selected = load("current_consumer_original", TASK / "capability_payload_refresh.py")
    worker = selected.worker
    capture = load("current_consumer_capture", TASK / "delivered_additions.py")
    if len(sys.argv) != 4 or sys.argv[1] not in ("consumer-first", "consumer-rest") or sys.argv[2] != "--zip-sha256":
        raise AssertionError("only exact current consumer phases admitted")
    def invoke(label, argv, *, env=None, destination=worker.OUTPUT):
        out = destination / (label + ".stdout")
        err = destination / (label + ".stderr")
        process = destination / (label + "-process.json")
        record = {"argv": argv, "exit_code": None, "stdout": "", "stderr": "",
                  "status": "RUNNING", "timeout_seconds": 600}
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
        worker.write(process, record)
        print(json.dumps({"stage": label, "exit_code": record["exit_code"],
                          "status": record["status"]}), flush=True)
        if failure is not None:
            raise failure
        if result.returncode:
            raise AssertionError(f"{label} failed; full process output retained")
        return subprocess.CompletedProcess(argv, result.returncode, record["stdout"], record["stderr"])
    worker.invoke = invoke
    worker.main()

if __name__ == "__main__":
    main()
