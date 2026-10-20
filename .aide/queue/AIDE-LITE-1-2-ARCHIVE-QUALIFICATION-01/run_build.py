"""One reviewed versioned build through the existing release owner."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path.cwd()
TASK = Path(__file__).parent
OUT = Path(os.environ["AIDE_JOB_OUTPUT"]).resolve(strict=True)
sys.dont_write_bytecode = True


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory():
    return {p.relative_to(ROOT).as_posix(): {"sha256": sha(p), "size_bytes": p.stat().st_size}
            for p in sorted((ROOT / ".aide/release").rglob("*")) if p.is_file()}


def save(path, value):
    path.write_bytes((json.dumps(value, sort_keys=True, indent=2) + "\n").encode())


record = {"state": "started", "production_assets_created": False, "qualification": "pending",
          "support_claimed": False, "publication": "unchanged_1.1.0"}
try:
    assert not subprocess.check_output(["git", "status", "--porcelain"]).strip()
    before = json.loads((TASK / "evidence/release-before.json").read_bytes())
    pack = json.loads((TASK / "evidence/pack-subject.json").read_bytes())
    assert inventory() == before
    assert all(sha(ROOT / name) == digest for name, digest in pack.items())
    expected = {".aide/release/stable/aide-lite-v1.2.0." + suffix
                for suffix in ("zip", "tar.gz", "manifest.json", "SHA256SUMS.txt")}
    assert not expected.intersection(before)
    for action in ("stable-build", "stable-validate"):
        argv = [sys.executable, "-I", "-B", ".aide/scripts/aide_lite.py", "release", action,
                "--version", "1.2.0"]
        entry = {"argv": argv, "state": "started", "exit_code": None}
        save(OUT / (action + ".json"), entry)
        streams = [OUT / (action + suffix) for suffix in (".stdout", ".stderr")]
        try:
            with streams[0].open("xb") as stdout, streams[1].open("xb") as stderr:
                result = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=stdout,
                                        stderr=stderr, timeout=240)
            entry.update(state="completed", exit_code=result.returncode)
        except BaseException as error:
            entry.update(state="exception", error_type=type(error).__name__, error=str(error))
            raise
        finally:
            entry["streams"] = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)}
                                for p in streams if p.exists()}
            save(OUT / (action + ".json"), entry)
        assert result.returncode == 0, action + " failed; exact outputs retained"
    after = inventory()
    assert set(after) == set(before) | expected
    assert all(after[name] == value for name, value in before.items())
    assert all(sha(ROOT / name) == digest for name, digest in pack.items())
    manifest = json.loads((ROOT / ".aide/release/stable/aide-lite-v1.2.0.manifest.json").read_bytes())
    identity = manifest["identity"]
    declaration = json.loads((ROOT / ".aide/release/successor-candidate.json").read_bytes())
    assert identity["schema_version"] == "aide.stable-release-identity.v2" and identity["version"] == "1.2.0"
    assert identity["profiles"] == declaration["profiles"]
    assert identity["predecessor_matrix"][0]["version"] == "1.1.0"
    assert identity["predecessor_matrix"][0]["tag_commit"] == declaration["predecessor"]["tag_commit"]
    assert len(identity["public_cli_forms"]) == 56 and len(identity["profiles"]) == 4
    with zipfile.ZipFile(ROOT / ".aide/release/stable/aide-lite-v1.2.0.zip") as archive:
        cli_sha = hashlib.sha256(archive.read("aide-lite-pack-v0/files/.aide/scripts/aide_lite.py")).hexdigest()
        assert json.loads(archive.read("aide-lite-pack-v0/stable-release.json")) == identity
    save(OUT / "build-result.json", {"status": "PASS_BUILD_ONLY", "assets": {n: after[n] for n in sorted(expected)},
         "identity": identity, "delivered_cli_sha256": cli_sha, "preserved_release_files": len(before),
         "preserved_pack_files": len(pack), "qualification": "pending", "support_claimed": False,
         "publication": "unchanged_1.1.0", "worker_model_requests": 0, "controller_usage": "unknown"})
    record.update(state="passed_build_only", production_assets_created=True,
                  assets={n: after[n] for n in sorted(expected)})
except BaseException as error:
    record.update(state="stopped", error_type=type(error).__name__, error=str(error))
    raise
finally:
    observed = {p.relative_to(ROOT).as_posix(): {"sha256": sha(p), "size_bytes": p.stat().st_size}
                for p in (ROOT / ".aide/release/stable").glob("aide-lite-v1.2.0.*") if p.is_file()}
    record.update(production_assets_created=bool(observed), observed_candidate_assets=observed)
    save(OUT / "build-command.json", record)
print("PASS build/validation only; actual consumers, profile qualification and publication remain pending")
