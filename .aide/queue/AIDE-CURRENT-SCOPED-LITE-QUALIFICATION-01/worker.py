"""Current-byte qualification; fixtures stay inside one managed allocation."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import zipfile

REPO = Path(__file__).resolve().parents[3]
TASK = Path(__file__).resolve().parent
CAN = TASK / "canaries"
TMP = Path(os.environ["AIDE_JOB_TMP"]).resolve(strict=True)
OUTPUT = Path(os.environ["AIDE_JOB_OUTPUT"]).resolve(strict=True)
CLI = REPO / ".aide/scripts/aide_lite.py"
STABLE = REPO / ".aide/release/stable"
ZIP = STABLE / "aide-lite-v1.0.0.zip"
TAR = STABLE / "aide-lite-v1.0.0.tar.gz"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def invoke(label, argv, *, env=None, destination=OUTPUT):
    result = subprocess.run(argv, cwd=REPO, env=env, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=600)
    write(destination / (label + "-process.json"), {
        "argv": argv, "exit_code": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr,
    })
    print(json.dumps({"stage": label, "exit_code": result.returncode}), flush=True)
    if result.returncode:
        raise AssertionError(f"{label} failed; full process output retained")
    return result


def retire_owned_fixture(root):
    # Only our newly allocated exact case directory, after its process exited.
    # Verify every path before deleting anything; never follow redirected entries.
    resolved = root.resolve(strict=True)
    if root.parent != TMP or resolved.parent != TMP or not root.name.startswith("case-"):
        raise AssertionError("fixture retirement target outside this job")
    paths = [root, *root.rglob("*")]
    if len(paths) > 100000:
        raise AssertionError("fixture retirement exceeds declared file envelope")
    for path in paths:
        info = path.lstat()
        if (stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400
                or not path.resolve(strict=True).is_relative_to(root)
                or not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode))
                or (stat.S_ISREG(info.st_mode) and info.st_nlink != 1)):
            raise AssertionError("redirected, shared or unknown fixture entry")
    for path in sorted(paths, key=lambda item: len(item.parts), reverse=True):
        if path.is_dir():
            path.rmdir()
        else:
            path.chmod(stat.S_IWRITE | stat.S_IREAD)
            path.unlink()
    if root.exists():
        raise AssertionError("fixture retirement incomplete")


def asset_identity():
    manifest = json.loads((STABLE / "aide-lite-v1.0.0.manifest.json").read_text())
    with zipfile.ZipFile(ZIP) as archive:
        delivered_cli = hashlib.sha256(archive.read("aide-lite-pack-v0/files/.aide/scripts/aide_lite.py")).hexdigest()
    return {"zip_sha256": sha(ZIP), "tar_sha256": sha(TAR),
            "cli_sha256": delivered_cli, "identity": manifest["identity"],
            "assets": {p.name: sha(p) for p in STABLE.iterdir()}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("repair", "build", "consumer", "replay"))
    parser.add_argument("--zip-sha256")
    parser.add_argument("--source-proof-sha256")
    args = parser.parse_args()
    os.environ.update(AIDE_RESOURCE_TEST_PARENT=str(TMP), GIT_CONFIG_COUNT="1",
                      GIT_CONFIG_KEY_0="safe.directory", GIT_CONFIG_VALUE_0=str(REPO))
    identity = ctypes.create_unicode_buffer(256)
    size = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(size)):
        raise ctypes.WinError()
    if "CodexSandboxOffline" not in identity.value:
        raise AssertionError("expected restricted worker identity")
    result = {"phase": args.phase, "windows_identity": identity.value,
              "model_calls": 0, "outer_session_contained": False,
              "read_isolation": "unqualified", "retired_fixtures": []}
    if args.phase == "repair":
        tests = invoke("stable-admission", [sys.executable, "-B", "-m", "unittest", "discover",
                                            "-s", ".aide/scripts/tests", "-p", "test_stable_release_admission.py"])
        if not re.search(r"Ran 5 tests? in ", tests.stdout + tests.stderr):
            raise AssertionError("admission regression count changed")
        public = invoke("public-fixtures", [sys.executable, "-B", "-m", "unittest", "discover",
                                            "-s", ".aide/scripts/tests", "-p", "test_public_archive_fixture.py"])
        if not re.search(r"Ran 8 tests? in ", public.stdout + public.stderr) or "skipped=" in public.stdout + public.stderr:
            raise AssertionError("public fixture regression count changed or checks skipped")
        release = invoke("q47q48", [sys.executable, "-B", "-m", "unittest", "discover",
                                   "-s", ".aide/scripts/tests", "-p", "test_q4[78]*.py"])
        if not re.search(r"Ran 36 tests? in ", release.stdout + release.stderr) or "skipped=" in release.stdout + release.stderr:
            raise AssertionError("release regression count changed or checks skipped")
        for name in ("export-pack", "validate"):
            # Full validation goes to the admitted 6 MiB log, not the tiny
            # result allowance. Preserve its exit code and complete log.
            run = subprocess.run([sys.executable, "-B", str(CLI), name], cwd=REPO, timeout=240)
            result[name + "_exit_code"] = run.returncode
            if run.returncode:
                raise AssertionError(name + " failed")
        result.update(status="PASS", admission_tests={"run": 5, "failures": 0, "errors": 0, "skips": 0},
                      public_fixture_tests={"run": 8, "failures": 0, "errors": 0, "skips": 0},
                      release_tests={"run": 36, "failures": 0, "errors": 0, "skips": 0},
                      source_inputs={name: sha(REPO / name) for name in (
                          ".aide/scripts/aide_lite.py", ".aide/scripts/tests/test_public_archive_fixture.py",
                          ".aide/scripts/tests/test_q47_release_bundle.py", ".aide/scripts/tests/test_q48_github_release_draft.py",
                          ".aide/scripts/tests/test_stable_release_admission.py")})
    elif args.phase in ("build", "replay"):
        if args.phase == "build":
            proof_path = TASK / "evidence/source-qualification.json"
            if sha(proof_path) != args.source_proof_sha256:
                raise AssertionError("accepted source proof changed")
            proof = json.loads(proof_path.read_text())
            if (proof["status"] != "PASS" or proof["release_tests"] != {"run": 36, "failures": 0, "errors": 0, "skips": 0}
                    or any(sha(REPO / name) != digest for name, digest in proof["source_inputs"].items())):
                raise AssertionError("source suite subject changed")
            result["release_tests"] = dict(proof["release_tests"], reused=True,
                                           source_proof_sha256=args.source_proof_sha256)
        before = {p.name: sha(p) for p in STABLE.iterdir()}
        if args.phase == "replay" and sha(ZIP) != args.zip_sha256:
            raise AssertionError("replay subject changed")
        invoke("stable-build", [sys.executable, "-B", str(CLI), "release", "stable-build", "--version", "1.0.0"])
        invoke("stable-validate", [sys.executable, "-B", str(CLI), "release", "stable-validate", "--version", "1.0.0"])
        current = asset_identity()
        if args.phase == "replay" and current["assets"] != before:
            raise AssertionError("deterministic replay changed frozen bytes")
        result.update(status="PASS", asset=current, replay_unchanged=args.phase == "replay")
    else:
        asset = asset_identity()
        if asset["zip_sha256"] != args.zip_sha256:
            raise AssertionError("consumer subject changed")
        z, t, zs, ts, cs = str(ZIP), str(TAR), asset["zip_sha256"], asset["tar_sha256"], asset["cli_sha256"]
        hs = sha(CAN / "lifecycle_helper.py")
        cases = [
            ("consumer_canary_runner.py", ["--candidate-zip", z, "--candidate-tar", t,
                "--candidate-zip-sha256", zs, "--candidate-tar-sha256", ts,
                "--bundled-cli-sha256", cs, "--source-commit", asset["identity"]["source_commit"]]),
            ("lifecycle_canary_runner.py", [z, zs, hs]),
            ("context_offline_canary.py", [z, zs, hs]),
            ("partial_cli_canary.py", [z, t, zs, ts, cs]),
            ("public_cli_canary.py", [z, zs, hs]),
            ("forced_restart_runner.py", [z, zs]),
            ("job_forms_canary.py", ["--zip", z, "--zip-sha256", zs, "--cli-sha256", cs,
                                    "--out", "unused.json"]),
            ("taskos_delivered_canary.py", [z, zs, cs]),
        ]
        for index, (name, parameters) in enumerate(cases):
            label = f"case-{index:02d}"
            scratch = TMP / label
            retained = OUTPUT / label
            scratch.mkdir(); retained.mkdir()
            env = {**os.environ, "AIDE_JOB_TMP": str(scratch), "AIDE_JOB_OUTPUT": str(retained),
                   "TEMP": str(scratch), "TMP": str(scratch), "TMPDIR": str(scratch)}
            invoke(label, [sys.executable, "-I", "-B", str(CAN / name), *parameters],
                   env=env, destination=retained)
            retire_owned_fixture(scratch)
            result["retired_fixtures"].append(label)
        result.update(status="PASS", asset=asset, cases=len(cases))
    write(OUTPUT / "qualification.json", result)
    print(json.dumps({"status": result["status"], "phase": args.phase,
                      "qualification_sha256": sha(OUTPUT / "qualification.json")}), flush=True)


if __name__ == "__main__":
    main()
