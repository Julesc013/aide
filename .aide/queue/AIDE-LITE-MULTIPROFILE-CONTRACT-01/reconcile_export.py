"""Read-only reconciliation after completed tests/export; never retry effects."""
import base64
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
TASK = Path(__file__).parent
EVIDENCE = TASK / "evidence"
sys.path.insert(0, str(ROOT))
from core.execution.managed_workspace import content_digest


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    data = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()
    if path.exists():
        assert path.read_bytes() == data, "retained evidence cannot be overwritten"
        return
    with path.open("xb") as stream:
        stream.write(data)


execution = json.loads((EVIDENCE / "source-execution.log").read_bytes())
job = execution["job_result"]
assert job["job_id"] == "9d6ec5bc23354109842c7a8b39f75aec"
assert job["phase"] == "retired" and job["result"]["exit_code"] == 1
assert job["result"]["quiescent"] and job["scratch_absent"] and job["reservation_released"]
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == job["job"]["source_commit"]
assert all(sha(ROOT / name) == digest for name, digest in job["job"]["inputs"].items())
retained = Path(job["retained"])
assert all(content_digest(retained / name) == digest for name, digest in job["collected_manifest"].items())
raw = {p.relative_to(retained).as_posix(): base64.b64encode(p.read_bytes()).decode("ascii")
       for group in ("output", "logs") for p in sorted((retained / group).rglob("*")) if p.is_file()}
bundle = json.dumps(raw, sort_keys=True, separators=(",", ":")).encode()
assert len(raw) < 32 and len(bundle) < 2 * 1024 * 1024
packed = gzip.compress(bundle, mtime=0)
save(EVIDENCE / "retained-evidence.json", {"encoding": "gzip+base64", "files": len(raw),
     "uncompressed_bytes": len(bundle), "sha256": hashlib.sha256(bundle).hexdigest(),
     "gzip_sha256": hashlib.sha256(packed).hexdigest(), "data": base64.b64encode(packed).decode("ascii")})
save(EVIDENCE / "local-job-result.json", job)
partial = json.loads((retained / "output/result.json").read_bytes())
save(EVIDENCE / "original-failed-result.json", partial)
assert partial["export_refreshed"] and partial["error_type"] == "FileNotFoundError"
assert partial["source_head"] == job["job"]["source_commit"]
assert [(suite["module"], suite["exit_code"], suite["expected_tests"]) for suite in partial["suites"]] == [
    ("test_stable_release_admission", 0, 5), ("test_stable_successor", 0, 15)]
spec = importlib.util.spec_from_file_location("profile_readonly_reconciliation", ROOT / ".aide/scripts/aide_lite.py")
lite = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lite
spec.loader.exec_module(lite)
pack = lite.export_pack_root(ROOT)
members = {p.relative_to(pack).as_posix(): sha(p) for p in sorted(pack.rglob("*")) if p.is_file()}
valid, problems = lite.validate_pack_checksums(pack)
assert valid and not problems and not lite.validate_export_pack_boundary(pack)
assert (pack / "files/.aide/scripts/aide_lite.py").read_bytes() == lite.portable_cli_text(
    (ROOT / ".aide/scripts/aide_lite.py").read_text(encoding="utf-8")).encode("utf-8")
for name in (".aide/policies/release-versioning.yaml", "docs/reference/lite-release-profiles.md",
             "docs/reference/portable-lifecycle-filesystems.md"):
    assert (pack / "files" / name).read_bytes() == (ROOT / name).read_bytes(), name
source_only = "docs/reference/portability-and-build-profiles.md"
assert repr(str(pack / "files" / source_only)) in partial["error"]
assert source_only not in lite.PORTABLE_SOURCE_FILES and not (pack / "files" / source_only).exists()
contract = lite.stable_release_contract(ROOT, "1.2.0")
baseline = json.loads((EVIDENCE / "baseline.json").read_bytes())["stable_assets"]
assert set(p.relative_to(ROOT).as_posix() for p in (ROOT / ".aide/release/stable").iterdir()) == set(baseline)
assert all(sha(ROOT / name) == value for name, value in baseline.items())
assert {p.relative_to(pack).as_posix(): sha(p) for p in sorted(pack.rglob("*")) if p.is_file()} == members
save(EVIDENCE / "package-inputs.json", {"source_commit": partial["source_head"],
     "files": job["job"]["inputs"] | {lite.EXPORT_PACK_PATH + "/" + n: v for n, v in members.items()},
     "members": members})
save(EVIDENCE / "reconciliation.json", {"result": "PASS_READ_ONLY_RECONCILIATION", "job_result": "FAIL_PRESERVED",
     "job_id": job["job_id"], "source_commit": partial["source_head"], "tests_passed": 20,
     "test_reruns": 0, "additional_jobs": 0, "export_regenerations": 0, "export_files": len(members),
     "collected_manifest": job["collected_manifest"], "stable_assets_unchanged": len(baseline),
     "profiles": len(contract["profiles"]), "public_forms": len(contract["forms"]),
     "source_only_reference": source_only, "read_only_tail_completed": True,
     "support_claimed": False, "production_archives_built": False})
print("PASS read-only reconciliation; original job FAIL and all 20 completed test passes preserved")
