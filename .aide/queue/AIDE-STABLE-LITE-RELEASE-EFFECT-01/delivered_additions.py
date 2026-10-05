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

def capture_streams(argv, *, cwd, env, stdout_path, stderr_path, timeout=180):
    """Own raw streams before dispatch, including timeout and launch failures."""
    with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
        return subprocess.run(argv, cwd=cwd, env=env, stdout=stdout,
                              stderr=stderr, timeout=timeout)

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
    if mappings["zip"] != mappings["tar"] or len(mappings["zip"]) != 854:
        raise AssertionError("full delivered ZIP/TAR file mapping differs")
    delivered = case / "zip/aide-lite-pack-v0/files"
    support = json.loads((Path(__file__).parent / "delivered_fixture_support.json").read_text(encoding="utf-8"))
    if support["schema"] != "aide.delivered-tests-explicit-fixture-support.v1":
        raise AssertionError("unknown fixture support")
    overlays = {}
    fixture_bytes = 0
    for name, binding in support["missing_non_executable_source_fixtures"].items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or relative.suffix in (".py", ".ps1", ".exe", ".dll"):
            raise AssertionError("non-executable bounded fixture data required")
        source = REPO / relative
        destination = delivered / relative
        content = source.read_bytes()
        fixture_bytes += len(content)
        if destination.exists() or len(content) != binding["bytes"] or sha(source) != binding["sha256"]:
            raise AssertionError("exact missing fixture dependency changed")
        if fixture_bytes > support["maximum_total_fixture_bytes"]:
            raise AssertionError("fixture data bound exceeded")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        overlays[name] = sha(destination)
    config_name = support["configuration_fixture_destination"]
    if config_name != ".aide/queue/AIDE-RETIRED-EVIDENCE-CUSTODY-01/evidence/native-fixture-configuration.json":
        raise AssertionError("unexpected configuration fixture")
    destination = delivered / config_name
    if destination.exists():
        raise AssertionError("fixture cannot overwrite delivered files")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(support["configuration_fixture"], indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    overlays[config_name] = sha(destination)
    if fixture_bytes + destination.stat().st_size > support["maximum_total_fixture_bytes"]:
        raise AssertionError("total fixture data bound exceeded")
    fixture_parent = case / "fixtures"
    fixture_parent.mkdir()
    env = {**os.environ, "AIDE_RESOURCE_TEST_PARENT": str(fixture_parent),
           "TEMP": str(fixture_parent), "TMP": str(fixture_parent),
           "TMPDIR": str(fixture_parent), "PYTHONDONTWRITEBYTECODE": "1"}
    proof = {"schema": "aide.delivered-additions-qualification.v1",
             "windows_identity": identity.value, "archives": expected,
             "full_archive_file_count": 854, "full_archive_maps_equal": True,
             "nested_model_calls": 0, "outer_session_contained": False,
             "read_isolation": "unqualified", "suites": [], "status": "RUNNING",
             "explicit_fixture_overlays": overlays,
             "fixture_support_sha256": sha(Path(__file__).parent / "delivered_fixture_support.json"),
             "qualification_limit": support["qualification_limit"]}
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
        out = OUTPUT / (name + ".stdout")
        err = OUTPUT / (name + ".stderr")
        row = {"test": name, "delivered_test_sha256": sha(test),
               "argv": argv, "exit_code": None, "tests_expected": count,
               "status": "RUNNING", "timeout_seconds": 180,
               "timed_out": False}
        proof["suites"].append(row)
        save()
        failure = None
        try:
            result = capture_streams(argv, cwd=delivered, env=env,
                                     stdout_path=out, stderr_path=err)
            row["exit_code"] = result.returncode
        except (subprocess.TimeoutExpired, OSError) as exc:
            failure = exc
            row.update(timed_out=isinstance(exc, subprocess.TimeoutExpired),
                       failure_type=type(exc).__name__, failure=str(exc))
        text = (out.read_bytes() + err.read_bytes()).decode("utf-8", errors="replace")
        row.update(count_verified=bool(re.search(r"Ran " + str(count) + r" tests? in ", text)),
                   stdout_sha256=sha(out), stderr_sha256=sha(err),
                   stdout_bytes=out.stat().st_size, stderr_bytes=err.stat().st_size,
                   skip_marker_absent="skipped=" not in text)
        passed = (failure is None and row["exit_code"] == 0
                  and row["count_verified"] and row["skip_marker_absent"])
        row["status"] = "PASS" if passed else "FAILED"
        if not passed:
            proof["status"] = "FAILED"
        save()
        if failure is not None:
            raise failure
        if not passed:
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
    for name, digest in mappings["zip"].items():
        if sha(case / "zip" / name) != digest:
            raise AssertionError("an original archive file changed")
    if any(sha(delivered / name) != digest for name, digest in overlays.items()):
        raise AssertionError("explicit fixture data changed")
    proof["all_original_archive_files_unchanged"] = True
    worker.retire_owned_fixture(case)
    proof.update(status="PASS", tests_qualified=41,
                 delivered_fixture_retired=not case.exists())
    save()
    print(json.dumps({"status": "PASS", "tests": 41,
                      "delivered_fixture_retired": proof["delivered_fixture_retired"]}), flush=True)

if __name__ == "__main__":
    main()
