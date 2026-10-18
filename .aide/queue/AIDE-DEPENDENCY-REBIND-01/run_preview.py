"""Refresh owned pack provenance, then use existing preview checks on exact outputs."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, subprocess
from pathlib import Path
ROOT = Path.cwd()
TASK = ROOT / ".aide/queue/AIDE-DEPENDENCY-REBIND-01"
def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
owner = load("rebind_preview_owner", ".aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py")
owner.BASE = "ceac70a6fefefde93d2fb7435e8825c173302757"
refresh = load("rebind_pack_owner", ".aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py")
pack = ROOT / refresh.PACK_REL
prior = json.loads((ROOT / ".aide/queue/AIDE-LITE-SUCCESSOR-INTEGRATION-01/evidence/attempt-02-delivered-result.json").read_text(encoding="utf-8"))["after_sha256s"]
release = json.loads((ROOT / ".aide/queue/AIDE-LITE-SUCCESSOR-INTEGRATION-01/evidence/attempt-02-release-before.json").read_text(encoding="utf-8"))
def check_pack():
    actual = refresh.inventory_bytes(pack)
    assert len(actual) == 870 and set(actual) == set(prior)
    assert all(actual[name] == sha for name, sha in prior.items() if name not in refresh.EXCLUDED)
    for name, sha in release.items(): assert owner.sha(ROOT / name) == sha, name
    return actual
assert sys.argv[1:] in (["generate"], ["verify"])
if sys.argv[1:] == ["verify"]:
    check_pack()
    print(json.dumps(owner.verify(), indent=2))
else:
    assert not subprocess.check_output(["git", "status", "--porcelain"]).strip()
    output = Path(os.environ["AIDE_JOB_OUTPUT"])
    before_pack = check_pack()
    inventory = TASK / "evidence/prior-pack-inventory.json"
    sys.argv = [__file__, "refresh", "--inventory", str(inventory.relative_to(ROOT)),
                "--inventory-sha256", owner.sha(inventory)]
    refresh.main()
    after_pack = check_pack()
    metadata = {refresh.PACK_REL + "/" + name for name in refresh.EXCLUDED
                if after_pack[name] != before_pack[name]}
    assert set(subprocess.check_output(["git", "diff", "--name-only"], text=True).splitlines()) == metadata
    assert not subprocess.check_output(["git", "diff", "--cached", "--name-only"]).strip()
    assert not subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"]).strip()
    preview = ROOT / ".aide/changelog"
    before, directories = owner.inventory(preview)
    assert owner.NAMES <= set(before)
    saved = output / "prior-preview"; saved.mkdir()
    for name in owner.NAMES: (saved / name).write_bytes((preview / name).read_bytes())
    endpoint = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    operations = {}
    for label, args in [
            ("preview", ["changelog", "preview", "--range", owner.BASE + ".." + endpoint, "--limit", "100"]),
            ("preview-validate", ["changelog", "validate"]), ("preview-status", ["changelog", "status"])]:
        operations[label] = refresh.invoke(label, [sys.executable, "-B", ".aide/scripts/aide_lite.py", *args], output)
        assert operations[label]["exit_code"] == 0, label
    after, after_directories = owner.inventory(preview)
    assert directories == after_directories and set(before) == set(after)
    assert all(after[name] == sha for name, sha in before.items() if name not in owner.NAMES)
    assert check_pack() == after_pack
    result = owner.verify()
    assert result["source_head"] == endpoint
    result.update(operations=operations, pack_metadata_changed=sorted(metadata),
                  pack_payload_unchanged=867, frozen_release_files_unchanged=len(release))
    (output / "preview-result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "preview_commits": len(result["commits"]),
                      "pack_payload_unchanged": 867, "models_requested": 0}))
