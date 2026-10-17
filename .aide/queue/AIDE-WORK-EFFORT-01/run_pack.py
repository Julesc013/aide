"""Qualify the changed portable payload through the existing export owner."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import unittest

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-WORK-EFFORT-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

refresh = load('review_pack_refresh', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
inventory = TASK / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(ROOT)),
            '--inventory-sha256', hashlib.sha256(inventory.read_bytes()).hexdigest()]
refresh.main()
after = refresh.inventory_bytes(ROOT / refresh.PACK_REL)
old = {name: value['sha256'] for name, value in before['files'].items()}
added = {'files/core/execution/work_effort.py', 'files/.aide/scripts/tests/test_work_effort.py'}
assert set(after) - set(old) == added and not set(old) - set(after), 'unexpected pack membership'
changed = {name for name in old if old[name] != after[name]} | added
payload = added | {'files/.aide/scripts/aide_lite.py', 'files/docs/reference/aide-lite-test-runner.md'}
assert changed - {'manifest.yaml', 'checksums.json', 'export-report.md'} == payload, sorted(changed)
for name in payload:
    assert refresh.sha(ROOT / refresh.PACK_REL / name) == refresh.sha(ROOT / name.removeprefix('files/'))

# A fresh process imports the actual exported test/module subjects.
bootstrap = "import os,sys,tempfile,runpy; tempfile.tempdir=os.environ['AIDE_JOB_TMP']; sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')"
result = subprocess.run([sys.executable, '-B', '-c', bootstrap, str(TASK / 'run_delivered.py')], timeout=90)
assert result.returncode == 0, 'delivered checks failed; retain original output'
assert refresh.inventory_bytes(ROOT / refresh.PACK_REL) == after, 'delivered lookup mutated the pack'
(OUTPUT / 'pack-delta.json').write_text(json.dumps({'changed_paths': sorted(changed), 'after_sha256s': after}, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'PASS', 'delivered_tests': 42, 'changed_paths': sorted(changed)}))
