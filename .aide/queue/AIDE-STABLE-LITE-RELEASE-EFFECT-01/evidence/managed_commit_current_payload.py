"""Affected release checks, current build and new delivered commit behavior only."""
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[4]
TMP = Path(os.environ["AIDE_JOB_TMP"]).resolve(strict=True)
OUTPUT = Path(os.environ["AIDE_JOB_OUTPUT"]).resolve(strict=True)
PROOF = OUTPUT / "current-payload.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def main():
    identity = ctypes.create_unicode_buffer(256)
    length = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(length)):
        raise ctypes.WinError()
    if not identity.value.endswith("\\CodexSandboxOffline") or list(TMP.iterdir()):
        raise AssertionError("restricted identity and empty owned TMP required")
    fixtures = TMP / "fixtures"
    fixtures.mkdir()
    env = {**os.environ, "AIDE_RESOURCE_TEST_PARENT": str(fixtures),
           "TEMP": str(fixtures), "TMP": str(fixtures), "TMPDIR": str(fixtures),
           "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_COUNT": "1",
           "GIT_CONFIG_KEY_0": "safe.directory", "GIT_CONFIG_VALUE_0": str(REPO)}
    proof = {"schema": "aide.current-managed-commit-payload.v1", "status": "RUNNING",
             "identity": identity.value, "model_calls": 0, "outer_contained": False,
             "hard_disk_quota": False, "source_suites": [], "commands": [],
             "old_consumer8_and_delivered41_replayed": False}

    def save():
        PROOF.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n",
                         encoding="utf-8", newline="\n")

    def command(label, argv, cwd, expected_tests=None):
        result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, timeout=180)
        out, err = OUTPUT / (label + ".stdout"), OUTPUT / (label + ".stderr")
        out.write_bytes(result.stdout)
        err.write_bytes(result.stderr)
        text = (result.stdout + result.stderr).decode("utf-8", errors="replace")
        row = {"label": label, "argv": argv, "exit": result.returncode,
               "stdout_sha256": sha(out), "stderr_sha256": sha(err)}
        if expected_tests is not None:
            row.update(tests=expected_tests,
                       count_verified=bool(re.search(r"Ran " + str(expected_tests) + r" tests? in ", text)),
                       no_skips="skipped=" not in text)
        proof["commands"].append(row)
        save()
        if result.returncode or (expected_tests is not None and
                                (not row["count_verified"] or not row["no_skips"])):
            raise AssertionError(label + " failed; exact raw streams retained")
        return row

    save()
    for name, count in (("test_q47_release_bundle.py", 24),
                        ("test_q48_github_release_draft.py", 12),
                        ("test_public_archive_fixture.py", 8),
                        ("test_stable_release_admission.py", 5)):
        test = REPO / ".aide/scripts/tests" / name
        row = command(name.removesuffix(".py"), [sys.executable, "-I", "-B", str(test)], REPO, count)
        proof["source_suites"].append({**row, "source_test_sha256": sha(test)})
    if list(fixtures.iterdir()):
        raise AssertionError("source fixtures did not retire")
    cli = REPO / ".aide/scripts/aide_lite.py"
    for name in ("stable-build", "stable-validate"):
        command(name, [sys.executable, "-I", "-B", str(cli), "release", name,
                       "--version", "1.0.0"], REPO)
    stable = REPO / ".aide/release/stable"
    names = ["aide-lite-v1.0.0.zip", "aide-lite-v1.0.0.tar.gz",
             "aide-lite-v1.0.0.manifest.json", "aide-lite-v1.0.0.SHA256SUMS.txt"]
    proof["assets"] = {name: {"sha256": sha(stable / name), "bytes": (stable / name).stat().st_size}
                       for name in names}
    save()
    canaries = REPO / ".aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/canaries"
    helper = load("managed_payload_archive", canaries / "consumer_canary_base.py")
    helper.MAX_MEMBER = 8 * 1024 * 1024
    helper.MAX_ARCHIVE_CONTENT = 16 * 1024 * 1024
    retirement = load("managed_payload_retirement", canaries.parent / "worker.py")
    case = TMP / "case-managed-commit-payload"
    case.mkdir()
    maps = {kind: helper.extract_archive(stable / name, case / kind, kind)
            for kind, name in (("zip", names[0]), ("tar", names[1]))}
    if maps["zip"] != maps["tar"] or len(maps["zip"]) != 854:
        raise AssertionError("complete current ZIP/TAR mappings differ")
    delivered = case / "zip/aide-lite-pack-v0/files"
    paths = [".aide/scripts/aide_lite.py", "core/apply/managed_commit.py",
             ".aide/scripts/tests/test_managed_commit_create.py"]
    proof["delivered_inputs"] = {name: sha(delivered / name) for name in paths}
    if any(sha(delivered / name) != sha(REPO / name) for name in paths):
        raise AssertionError("qualified current delivered inputs differ from source")
    test = delivered / paths[2]
    code = ("import importlib.util,json,sys,unittest; "
            "s=importlib.util.spec_from_file_location('delivered_commit',sys.argv[1]); "
            "m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m); "
            "suite=unittest.defaultTestLoader.loadTestsFromTestCase(m.ManagedCommitTests); "
            "assert suite.countTestCases()==49; "
            "result=unittest.TextTestRunner(verbosity=2).run(suite); "
            "print(json.dumps({'tests_run':result.testsRun,'failures':len(result.failures),"
            "'errors':len(result.errors),'skipped':len(result.skipped),'source':str(m.SOURCE)})); "
            "sys.exit(0 if result.wasSuccessful() else 1)")
    command("delivered-commit49", [sys.executable, "-I", "-B", "-c", code, str(test)], delivered, 49)
    if list(fixtures.iterdir()):
        raise AssertionError("delivered Git fixtures did not retire")
    for kind in maps:
        if any(sha(case / kind / name) != digest for name, digest in maps[kind].items()):
            raise AssertionError("original delivered bytes changed")
    if any(sha(stable / name) != binding["sha256"] for name, binding in proof["assets"].items()):
        raise AssertionError("stable assets changed during delivered qualification")
    retirement.retire_owned_fixture(case)
    fixtures.rmdir()
    proof.update(status="PASS", source_tests=49, delivered_tests=49, archive_members=854,
                 maps_equal=True, delivered_source_override=False, fixture_overlays=0,
                 original_archive_members_unchanged=True, fixture_retired=not case.exists())
    save()
    print(json.dumps({"status": "PASS", "source_tests": 49, "delivered_tests": 49,
                      "archive_members": 854, "model_calls": 0}), flush=True)


if __name__ == "__main__":
    main()
