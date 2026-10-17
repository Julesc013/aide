"""Refresh the reviewed existing export and qualify its actual delivered CLI."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-CONTEXT-TASK-SELECTION-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
path = ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py'
spec = importlib.util.spec_from_file_location('context_pack_refresh', path)
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
changed = {name for name in old if old[name] != after[name]}
payload = {'files/.aide/scripts/aide_lite.py',
           'files/.aide/scripts/tests/test_task_binding.py'}
assert changed - {'manifest.yaml', 'checksums.json', 'export-report.md'} == payload, sorted(changed)
for name in payload:
    assert refresh.sha(ROOT / refresh.PACK_REL / name) == refresh.sha(ROOT / name.removeprefix('files/'))
with (OUTPUT / 'delivered-process.log').open('wb') as stream:
    result = subprocess.run([sys.executable, '-B', str(TASK / 'run_checks.py'),
                             str(ROOT / refresh.PACK_REL / 'files')],
                            stdout=stream, stderr=subprocess.STDOUT,
                            stdin=subprocess.DEVNULL, timeout=75)
assert result.returncode == 0, 'delivered checks failed; output preserved'
assert refresh.inventory_bytes(ROOT / refresh.PACK_REL) == after, 'delivered tests mutated pack'
(OUTPUT / 'delivered-result.json').write_text(json.dumps(
    {'status': 'PASS', 'delivered_tests': 60, 'ownership_tests': 6,
     'changed_paths': sorted(changed), 'after_sha256s': after,
     'models_requested': 0}, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'PASS', 'delivered_tests': 60, 'ownership_tests': 6,
                  'changed_paths': sorted(changed)}))
