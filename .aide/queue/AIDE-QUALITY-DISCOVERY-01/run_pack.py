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
TASK = ROOT / '.aide/queue/AIDE-QUALITY-DISCOVERY-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

refresh = load('quality_pack_refresh', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
inventory = TASK / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(ROOT)),
            '--inventory-sha256', hashlib.sha256(inventory.read_bytes()).hexdigest()]
refresh.main()
after = refresh.inventory_bytes(ROOT / refresh.PACK_REL)
old = {name: value['sha256'] for name, value in before['files'].items()}
assert set(old) == set(after), 'unexpected pack membership change'
changed = {name for name in old if old[name] != after[name]}
payload = {'files/.aide/scripts/aide_lite.py', 'files/.aide/scripts/tests/test_q38_file_quality.py',
           'files/.aide/quality/file-quality-ledger.schema.json',
           'files/.aide/reports/file-quality-ledger.schema.json',
           'files/docs/reference/file-quality-ledger.md'}
assert changed - {'manifest.yaml', 'checksums.json', 'export-report.md'} == payload, sorted(changed)
for name in payload:
    assert refresh.sha(ROOT / refresh.PACK_REL / name) == refresh.sha(ROOT / name.removeprefix('files/'))

# Import the delivered tests and CLI from the exported files, not source copies.
module = load('quality_delivered_tests', ROOT / refresh.PACK_REL / 'files/.aide/scripts/tests/test_q38_file_quality.py')
suite = unittest.defaultTestLoader.loadTestsFromModule(module)
with (OUTPUT / 'delivered-tests.log').open('w', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
observed = {'tests_run': result.testsRun, 'failures': len(result.failures),
            'errors': len(result.errors), 'skips': len(result.skipped),
            'cli': str(module.MODULE_PATH), 'changed_paths': sorted(changed),
            'after_sha256s': after, 'status': 'PASS' if result.wasSuccessful() and not result.skipped else 'FAIL'}
(OUTPUT / 'delivered-result.json').write_text(json.dumps(observed, indent=2) + '\n', encoding='utf-8')
assert result.testsRun == 16 and result.wasSuccessful() and not result.skipped
assert refresh.inventory_bytes(ROOT / refresh.PACK_REL) == after, 'delivered lookup mutated the pack'
print(json.dumps({'status': 'PASS', 'delivered_tests': result.testsRun, 'changed_paths': sorted(changed)}))
