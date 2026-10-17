"""Qualify source first, then the existing export and its actual delivered tests."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-IMPACT-COVERAGE-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()

def checks(label, subject=None):
    command = [sys.executable, '-B', str(TASK / 'run_checks.py')]
    if subject is not None:
        command.append(str(subject))
    with (OUTPUT / (label + '-process.log')).open('wb') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, timeout=60)
    assert result.returncode == 0, label + ' failed; output preserved'

# A fresh process prevents the internal selftest cache from crossing subjects.
checks('source')
path = ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py'
spec = importlib.util.spec_from_file_location('impact_pack_refresh', path)
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
           'files/.aide/scripts/tests/test_x_test_00_validation_tiers.py',
           'files/.aide/policies/impacted-tests.yaml',
           'files/docs/reference/impacted-test-planning.md'}
assert changed - {'manifest.yaml', 'checksums.json', 'export-report.md'} == payload, sorted(changed)
for name in payload:
    assert refresh.sha(ROOT / refresh.PACK_REL / name) == refresh.sha(ROOT / name.removeprefix('files/'))
checks('delivered', ROOT / refresh.PACK_REL / 'files')
assert refresh.inventory_bytes(ROOT / refresh.PACK_REL) == after, 'delivered tests mutated pack'
(OUTPUT / 'delivered-result.json').write_text(json.dumps(
    {'status': 'PASS', 'source_tests': 13, 'delivered_tests': 13,
     'ownership_tests': 6, 'changed_paths': sorted(changed),
     'after_sha256s': after, 'models_requested': 0}, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'PASS', 'source_tests': 13, 'delivered_tests': 13,
                  'ownership_tests': 6, 'changed_paths': sorted(changed)}))
