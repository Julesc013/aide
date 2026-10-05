"""Qualify the unchanged C1 and custody suites from the exact delivered payload."""
import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[3]
TMP = Path(os.environ["AIDE_JOB_TMP"]).resolve(strict=True)
OUTPUT = Path(os.environ["AIDE_JOB_OUTPUT"]).resolve(strict=True)
CANARIES = REPO / ".aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/canaries"
WORKER = REPO / ".aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/worker.py"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip-sha256", required=True)
    parser.add_argument("--tar-sha256", required=True)
    args = parser.parse_args()
    identity = ctypes.create_unicode_buffer(256)
    length = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(length)):
        raise ctypes.WinError()
    if "CodexSandboxOffline" not in identity.value:
        raise AssertionError("restricted worker identity required")
    if list(TMP.iterdir()):
        raise AssertionError("expected the existing empty allocated TMP")
    helper = load("delivered_archive_helpers", CANARIES / "consumer_canary_base.py")
    worker = load("delivered_fixture_retirement", WORKER)
    helper.MAX_MEMBER = 8 * 1024 * 1024
    helper.MAX_ARCHIVE_CONTENT = 16 * 1024 * 1024
    stable = REPO / ".aide/release/stable"
    archives = {kind: stable / ("aide-lite-v1.0.0." + suffix)
                for kind, suffix in (("zip", "zip"), ("tar", "tar.gz"))}
    expected = {"zip": args.zip_sha256, "tar": args.tar_sha256}
    for kind, path in archives.items():
        if sha(path) != expected[kind]:
            raise AssertionError("delivered archive identity changed")
    case = TMP / "case-delivered-additions"
    case.mkdir()
    mappings = {kind: helper.extract_archive(path, case / kind, kind)
                for kind, path in archives.items()}
    if mappings["zip"] != mappings["tar"] or len(mappings["zip"]) != 852:
        raise AssertionError("full delivered ZIP/TAR file mapping differs")
    delivered = case / "zip/aide-lite-pack-v0/files"
    fixture_parent = case / "fixtures"
    fixture_parent.mkdir()
    env = {**os.environ, "AIDE_RESOURCE_TEST_PARENT": str(fixture_parent),
           "TEMP": str(fixture_parent), "TMP": str(fixture_parent),
           "TMPDIR": str(fixture_parent), "PYTHONDONTWRITEBYTECODE": "1"}
    proof = {"schema": "aide.delivered-additions-qualification.v1",
             "windows_identity": identity.value, "archives": expected,
             "full_archive_file_count": 852, "full_archive_maps_equal": True,
             "nested_model_calls": 0, "outer_session_contained": False,
             "read_isolation": "unqualified", "suites": [], "status": "RUNNING"}
    path = OUTPUT / "delivered-additions.json"
    def save():
        path.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")
    save()
    for name, count in (("test_x_os_02_capability_reality.py", 18),
                        ("test_retired_evidence.py", 23)):
        test = delivered / ".aide/scripts/tests" / name
        member = "aide-lite-pack-v0/files/.aide/scripts/tests/" + name
        if sha(test) != mappings["zip"][member]:
            raise AssertionError("delivered test bytes changed")
        argv = [sys.executable, "-I", "-B", str(test)]
        result = subprocess.run(argv, cwd=delivered, env=env,
                                capture_output=True, timeout=180)
        out = OUTPUT / (name + ".stdout")
        err = OUTPUT / (name + ".stderr")
        out.write_bytes(result.stdout)
        err.write_bytes(result.stderr)
        text = (result.stdout + result.stderr).decode("utf-8", errors="replace")
        row = {"test": name, "delivered_test_sha256": sha(test),
               "argv": argv, "exit_code": result.returncode,
               "tests_expected": count,
               "count_verified": bool(re.search(r"Ran " + str(count) + r" tests? in ", text)),
               "stdout_sha256": sha(out), "stderr_sha256": sha(err),
               "skip_marker_absent": "skipped=" not in text}
        proof["suites"].append(row)
        save()
        if result.returncode or not row["count_verified"] or not row["skip_marker_absent"]:
            raise AssertionError("delivered suite failed; complete raw output retained")
    if list(fixture_parent.iterdir()):
        raise AssertionError("delivered suite fixtures were not retired")
    proof["delivered_inputs"] = {name: sha(delivered / name) for name in (
        ".aide/scripts/aide_lite.py", "core/execution/retired_evidence.py",
        ".aide/capabilities/capability-evidence-bindings.schema.json",
        ".aide/capabilities/capability-seeds.yaml",
        ".aide/policies/capability-reality.yaml")}
    if any(digest != mappings["zip"]["aide-lite-pack-v0/files/" + name]
           for name, digest in proof["delivered_inputs"].items()):
        raise AssertionError("delivered operative bytes changed")
    worker.retire_owned_fixture(case)
    proof.update(status="PASS", tests_qualified=41,
                 delivered_fixture_retired=not case.exists())
    save()
    print(json.dumps({"status": "PASS", "tests": 41,
                      "delivered_fixture_retired": proof["delivered_fixture_retired"]}), flush=True)

if __name__ == "__main__":
    main()
