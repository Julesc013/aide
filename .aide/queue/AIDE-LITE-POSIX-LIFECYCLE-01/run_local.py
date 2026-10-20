"""One admitted export refresh and native lifecycle qualification allocation."""
import base64
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
scratch = Path(os.environ["AIDE_JOB_TMP"]).resolve(strict=True)
output = Path(os.environ["AIDE_JOB_OUTPUT"]).resolve(strict=True)
sys.dont_write_bytecode = True
continue_local = sys.argv[1:] == ["continue-local"]
assert sys.argv[1:] in ([], ["continue-local"])


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_bytes((json.dumps(value, sort_keys=True, indent=2) + "\n").encode())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


record = {"state": "started", "export_refreshed": False, "exit_code": None,
          "mode": "bounded_continuation" if continue_local else "initial",
          "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()}
record_path = output / "local.command.json"
save(record_path, record)
streams = [output / ("evaluator" + suffix) for suffix in (".stdout", ".stderr")]
try:
    assert not subprocess.check_output(["git", "status", "--porcelain"]).strip()
    ownership = load("posix_export_ownership", ROOT / ".aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py")
    inventory_name = "prior-export-inventory-02.json" if continue_local else "prior-export-inventory.json"
    expected = json.loads((TASK / "evidence" / inventory_name).read_bytes())
    observed = ownership.require_same(expected)
    save(output / "export-before.json", observed)
    metadata = output / "prior-metadata"
    metadata.mkdir()
    for name in sorted(ownership.EXCLUDED):
        (metadata / name).write_bytes((ROOT / ownership.PACK_REL / name).read_bytes())
    stable = {p.relative_to(ROOT).as_posix(): sha(p) for p in (ROOT / ".aide/release/stable").iterdir() if p.is_file()}
    save(output / "stable-before.json", stable)
    lite = load("posix_export_owner", ROOT / ".aide/scripts/aide_lite.py")
    ownership.require_same(expected)
    pack, exported = lite.build_export_pack(ROOT)
    record.update(state="export_refreshed", export_refreshed=True, export=exported)
    save(record_path, record)
    valid, problems = lite.validate_pack_checksums(pack)
    assert valid and not problems and not lite.validate_export_pack_boundary(pack)
    assert (pack / "files/.aide/scripts/posix_filesystem.py").read_bytes() == (ROOT / ".aide/scripts/posix_filesystem.py").read_bytes()
    assert {p.relative_to(ROOT).as_posix(): sha(p) for p in (ROOT / ".aide/release/stable").iterdir() if p.is_file()} == stable
    members = {p.relative_to(pack).as_posix(): sha(p) for p in sorted(pack.rglob("*")) if p.is_file()}
    prior = json.loads((ROOT / ".aide/queue/AIDE-LITE-MODERN-LIFECYCLE-01/evidence/package-inputs.json").read_bytes())
    files = {name: sha(ROOT / name) for name in prior["files"] if not name.startswith(ownership.PACK_REL + "/")}
    files.update({ownership.PACK_REL + "/" + name: value for name, value in members.items()})
    for name in (".aide/scripts/aide_lite.py", ".aide/scripts/posix_filesystem.py",
                 ".aide/scripts/tests/test_posix_filesystem.py", ".aide/scripts/tests/test_posix_lifecycle.py",
                 ".aide/scripts/tests/test_export_import.py", "evals/lite/lifecycle.py"):
        files[name] = sha(ROOT / name)
    pinned = {key: value for key, value in prior.items() if key not in {"files", "development_members"}}
    pinned.update(files=files, development_members=members, workunit="AIDE-LITE-POSIX-LIFECYCLE-01")
    if continue_local:
        conserved = json.loads((TASK / "evidence/conserved-evidence.json").read_bytes())
        assert all(sha(ROOT / name) == value for name, value in conserved["files"].items())
        pinned["conserved_evidence"] = conserved
        pinned["files"].update(conserved["files"])
    save(output / "package-inputs.json", pinned)
    argv = [sys.executable, "-I", "-B", "evals/lite/lifecycle.py", "--scratch-parent", str(scratch),
            "--output", str(output / "receipts"), "--emit-log", "--workunit", "AIDE-LITE-POSIX-LIFECYCLE-01",
            "--input-manifest", str(output / "package-inputs.json")]
    if continue_local:
        argv.append("--continue-local")
    record.update(state="evaluator_started", argv=argv)
    save(record_path, record)
    with streams[0].open("xb") as stdout, streams[1].open("xb") as stderr:
        result = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=500)
    record.update(state="evaluator_completed", exit_code=result.returncode)
    save(record_path, record)
    assert result.returncode == 0
    data = json.loads((output / "receipts/result.json").read_bytes())
    assert data["observation_complete"] and data["source_head"] == record["source_head"]
    lines = [line.split() for line in streams[0].read_text(encoding="utf-8").splitlines() if line.startswith("AIDE_RECEIPT_V1 ")]
    assert lines and all(len(line) == 4 and line[2] == lines[0][2] for line in lines)
    assert [line[1] for line in lines] == [f"{i+1}/{len(lines)}" for i in range(len(lines))]
    packed = base64.b64decode("".join(line[3] for line in lines), validate=True)
    assert len(packed) <= 2 * 1024 * 1024 and hashlib.sha256(packed).hexdigest() == lines[0][2]
    with gzip.GzipFile(fileobj=io.BytesIO(packed), mode="rb") as stream:
        decoded = stream.read(12 * 1024 * 1024 + 1)
    assert len(decoded) <= 12 * 1024 * 1024
    bundle = json.loads(decoded)
    expected_files = {p.name: p for p in (output / "receipts").iterdir() if p.is_file()}
    assert set(bundle) == set(expected_files) and len(bundle) <= 256
    total = 0
    for name, path in expected_files.items():
        raw = base64.b64decode(bundle[name], validate=True)
        assert raw == path.read_bytes()
        total += len(raw)
    assert total <= 8 * 1024 * 1024
    save(output / "transport.json", {"status": "PASS", "files": len(bundle), "bytes": total,
        "compressed_sha256": hashlib.sha256(packed).hexdigest(), "raw_sha256": hashlib.sha256(decoded).hexdigest()})
    assert {p.relative_to(pack).as_posix(): sha(p) for p in sorted(pack.rglob("*")) if p.is_file()} == members
    assert {p.relative_to(ROOT).as_posix(): sha(p) for p in (ROOT / ".aide/release/stable").iterdir() if p.is_file()} == stable
    record.update(state="qualified" if data["native_lifecycle_pass"] else "product_failure_preserved",
                  native_lifecycle_pass=data["native_lifecycle_pass"], support_claimed=False)
    assert data["native_lifecycle_pass"], "native failures retained; no automatic retry"
except BaseException as error:
    record.update(state="stopped", error_type=type(error).__name__, error=str(error))
    raise
finally:
    record["streams"] = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)} for p in streams if p.exists()}
    save(record_path, record)
print(json.dumps({"state": record["state"], "support_claimed": False}))
