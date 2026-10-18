"""Reuse the existing fixed-range preview owner; keep qualified package bytes."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json
from pathlib import Path
ROOT = Path.cwd()
path = ROOT / ".aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py"
spec = importlib.util.spec_from_file_location("cancellation_preview_owner", path)
owner = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = owner
spec.loader.exec_module(owner)
owner.BASE = "8fe2d12cbc9d91f034cf7f68c58beda09809dc58"
pack = ROOT / ".aide/export/aide-lite-pack-v0"
prior = json.loads((ROOT / ".aide/queue/AIDE-LITE-SUCCESSOR-INTEGRATION-01/evidence/attempt-02-delivered-result.json").read_text(encoding="utf-8"))["after_sha256s"]
def check_pack():
    actual = {p.relative_to(pack).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in pack.rglob("*") if p.is_file()}
    assert len(actual) == 870 and actual == prior
check_pack()
owner.main()
check_pack()
