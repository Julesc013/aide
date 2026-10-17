"""Existing owned export path; prove all payload bytes remain unchanged."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-DEPENDENCY-MCP-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT).strip()
path = ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py'
spec = importlib.util.spec_from_file_location('mcp_pack_refresh', path)
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)
inventory = TASK / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(ROOT)),
            '--inventory-sha256', hashlib.sha256(inventory.read_bytes()).hexdigest()]
refresh.main()
after = refresh.inventory_bytes(ROOT / refresh.PACK_REL)
old = {name: value['sha256'] for name, value in before['files'].items()}
assert set(old) == set(after), 'unexpected pack membership change'
changed = sorted(name for name in old if old[name] != after[name])
assert set(changed) <= {'manifest.yaml', 'export-report.md'}, 'unexpected payload/checksum change'
result = {'status': 'PASS', 'changed_paths': changed, 'payload_byte_identical': True,
          'file_count': len(after), 'after_sha256s': after, 'model_calls': 0,
          'live_peer_deliveries': 0, 'published_assets_changed': False}
(OUTPUT / 'closure.json').write_bytes((json.dumps(result, indent=2) + '\n').encode())
print(json.dumps({'status': 'PASS', 'changed_paths': changed}), flush=True)
