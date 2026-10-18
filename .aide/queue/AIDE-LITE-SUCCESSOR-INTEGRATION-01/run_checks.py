"""Combined-source qualification using the unchanged held and current suites."""
import sys
sys.dont_write_bytecode = True
import importlib.util, json, os, subprocess, unittest
from pathlib import Path
ROOT = Path.cwd()
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
accounting = OUTPUT / 'accounting'
accounting.mkdir()
command = [sys.executable, '-B',
    '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01/run_effort_repair.py']
receipt = {'command': command, 'state': 'started'}
def save():
    (OUTPUT / 'accounting-process.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
save()
try:
    with (OUTPUT / 'accounting-process.log').open('xb') as stream:
        r = subprocess.run(command, env={**os.environ, 'AIDE_JOB_OUTPUT': str(accounting)},
            stdin=subprocess.DEVNULL, stdout=stream, stderr=subprocess.STDOUT, timeout=140)
    receipt.update(state='completed', exit_code=r.returncode)
    assert r.returncode == 0
except BaseException as error:
    receipt.update(state='exception', error_type=type(error).__name__, error=str(error))
    raise
finally:
    save()
observed = json.loads((accounting / 'tests.json').read_text(encoding='utf-8'))
assert observed['tests_run'] == 21 and not observed['failures'] and not observed['errors'] and not observed['skips']
path = ROOT / '.aide/scripts/tests/test_compact_communication.py'
spec = importlib.util.spec_from_file_location('combined_compact', path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
suite = unittest.defaultTestLoader.loadTestsFromModule(module)
expected = [t.id() for group in suite for t in group]
assert len(expected) == 26
with (OUTPUT / 'compact-tests.log').open('w', encoding='utf-8') as log:
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
record = {'test_ids': expected, 'tests_run': result.testsRun, 'failures': len(result.failures),
    'errors': len(result.errors), 'skips': [(t.id(), reason) for t, reason in result.skipped]}
(OUTPUT / 'compact-tests.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
assert result.wasSuccessful() and result.testsRun == 26 and not result.skipped
(OUTPUT / 'source-result.json').write_text(json.dumps({'result': 'PASS', 'accounting': 21,
    'compact': 26, 'models_requested': 0, 'archive_qualification': False}, indent=2) + '\n', encoding='utf-8')
print('PASS: 21 existing accounting/export and 26 compact-message checks')
