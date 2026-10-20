"""One admitted release-fixture allocation and owned export refresh; no release."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path.cwd()
TASK = Path(__file__).parent
scratch = Path(os.environ["AIDE_JOB_TMP"]).resolve(strict=True)
output = Path(os.environ["AIDE_JOB_OUTPUT"]).resolve(strict=True)
sys.dont_write_bytecode = True


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


record = {"state": "started", "export_refreshed": False, "suites": [],
          "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
          "support_claimed": False, "production_archives_built": False}
started = time.monotonic()
try:
    assert not subprocess.check_output(["git", "status", "--porcelain"]).strip()
    baseline = json.loads((TASK / "evidence/baseline.json").read_bytes())
    stable = baseline["stable_assets"]
    assert all(sha(ROOT / name) == value for name, value in stable.items())
    ownership = load("profile_export_ownership", ROOT / ".aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py")
    expected = json.loads((TASK / "evidence/prior-export-inventory.json").read_bytes())
    save(output / "export-before.json", ownership.require_same(expected))
    env = {**os.environ, "TMP": str(scratch), "TEMP": str(scratch), "TMPDIR": str(scratch),
           "PYTHONDONTWRITEBYTECODE": "1"}
    for module, count in (("test_stable_release_admission", 5), ("test_stable_successor", 15)):
        argv = [sys.executable, "-I", "-B", "-m", "unittest", "discover", "-s", ".aide/scripts/tests",
                "-p", module + ".py", "-v"]
        entry = {"module": module, "argv": argv, "state": "started", "expected_tests": count}
        record["suites"].append(entry)
        save(output / "result.json", record)
        streams = [output / (module + suffix) for suffix in (".stdout", ".stderr")]
        with streams[0].open("xb") as stdout, streams[1].open("xb") as stderr:
            result = subprocess.run(argv, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                                    stdout=stdout, stderr=stderr,
                                    timeout=max(1, 530 - (time.monotonic() - started)))
        entry.update(state="completed", exit_code=result.returncode,
                     streams={p.name: {"bytes": p.stat().st_size, "sha256": sha(p)} for p in streams})
        save(output / (module + ".result.json"), entry)
        save(output / "result.json", record)
        assert result.returncode == 0, "fixture failure retained; no automatic retry"
        text = streams[1].read_text(encoding="utf-8")
        assert re.search(r"Ran " + str(count) + r" tests? in ", text) and text.rstrip().endswith("OK"), text[-1000:]
    assert not subprocess.check_output(["git", "status", "--porcelain"]).strip()
    ownership.require_same(expected)
    metadata = output / "prior-metadata"
    metadata.mkdir()
    for name in sorted(ownership.EXCLUDED):
        (metadata / name).write_bytes((ROOT / ownership.PACK_REL / name).read_bytes())
    lite = load("profile_export_owner", ROOT / ".aide/scripts/aide_lite.py")
    ownership.require_same(expected)
    pack, exported = lite.build_export_pack(ROOT)
    record.update(state="export_refreshed", export_refreshed=True, export=exported)
    save(output / "result.json", record)
    valid, problems = lite.validate_pack_checksums(pack)
    assert valid and not problems and not lite.validate_export_pack_boundary(pack)
    assert (pack / "files/.aide/scripts/aide_lite.py").read_bytes() == lite.portable_cli_text(
        (ROOT / ".aide/scripts/aide_lite.py").read_text(encoding="utf-8")).encode("utf-8")
    for name in (".aide/policies/release-versioning.yaml",
                 "docs/reference/lite-release-profiles.md", "docs/reference/portable-lifecycle-filesystems.md",
                 "docs/reference/portability-and-build-profiles.md"):
        assert (pack / "files" / name).read_bytes() == (ROOT / name).read_bytes(), name
    members = {p.relative_to(pack).as_posix(): sha(p) for p in sorted(pack.rglob("*")) if p.is_file()}
    save(output / "export-after.json", {"source_head": record["source_head"], "members": members})
    contract = lite.stable_release_contract(ROOT, "1.2.0")
    save(output / "contract.json", {"profile_id": contract["profile_id"], "profiles": contract["profiles"],
                                    "forms": contract["forms"], "digest": contract["digest"]})
    assert set(p.relative_to(ROOT).as_posix() for p in (ROOT / ".aide/release/stable").iterdir()) == set(stable)
    assert all(sha(ROOT / name) == value for name, value in stable.items())
    record.update(state="passed", stable_assets_unchanged=len(stable), export_files=len(members),
                  elapsed_seconds=time.monotonic() - started)
except BaseException as error:
    record.update(state="stopped", error_type=type(error).__name__, error=str(error))
    raise
finally:
    record["output_streams"] = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)}
                                for p in output.iterdir() if p.suffix in (".stdout", ".stderr")}
    save(output / "result.json", record)
print(json.dumps({"state": record["state"], "export_files": record.get("export_files"), "support_claimed": False}))
