"""Qualify actual source/delivered validation CLI with preserved existing assertions."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT = Path.cwd()
repair = False
SUBJECT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 and not repair else ROOT
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
label = 'source-repair' if repair else ('source' if SUBJECT == ROOT else 'delivered')
suite = unittest.TestSuite()
inputs = {}
for name in ['test_outcome_lessons', 'test_outcome_controller']:
    path = SUBJECT / '.aide/scripts/tests' / (name + '.py')
    spec = importlib.util.spec_from_file_location('validation_' + name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    assert Path(getattr(module, 'aide', getattr(module, 'aide_lite', None)).__file__).resolve() == SUBJECT / '.aide/scripts/aide_lite.py'
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    inputs[path.relative_to(SUBJECT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
for relative in ['.aide/scripts/aide_lite.py', '.aide/scripts/outcome_lessons.py']:
    inputs[relative] = hashlib.sha256((SUBJECT / relative).read_bytes()).hexdigest()
def ids(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from ids(test)
        else:
            yield test.id()
expected = list(ids(suite))
expected_count = 36
assert len(expected) == expected_count and len(set(expected)) == expected_count
with (OUTPUT / (label + '-tests.log')).open('w', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
record = {'subject': label, 'test_ids': expected, 'tests_run': result.testsRun,
          'failures': len(result.failures), 'errors': len(result.errors),
          'skips': [(case.id(), why) for case, why in result.skipped], 'inputs': inputs,
          'models_requested': 0, 'whole_outcome_usage': 'unknown'}
(OUTPUT / (label + '-tests.json')).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
assert result.testsRun == expected_count and result.wasSuccessful() and not result.skipped
for path, digest in inputs.items():
    assert hashlib.sha256((SUBJECT / path).read_bytes()).hexdigest() == digest
print(json.dumps({'status': 'PASS', 'subject': label, 'tests': result.testsRun}))

if SUBJECT == ROOT:
    import subprocess
    command = [sys.executable, '-I', '-B', str(ROOT / '.aide/scripts/aide_lite.py'),
               'outcome', 'lessons', '--path', '.aide/scripts/tests/test_validation_output.py', '--json']
    called = subprocess.run(command, capture_output=True, timeout=30)
    (OUTPUT / 'actual-lesson.stdout').write_bytes(called.stdout)
    (OUTPUT / 'actual-lesson.stderr').write_bytes(called.stderr)
    assert called.returncode == 0
    actual = json.loads(called.stdout)
    assert [item['id'] for item in actual['selected']] == ['portable-validation-fixture']
    assert all(item['state'] == 'matching' for item in actual['selected'][0]['evidence'])
    assert actual['advisory_only'] and not actual['authorship_verified']
    record = json.loads((ROOT / '.aide/queue/AIDE-OUTCOME-LESSONS-01/evidence/lesson-append.json').read_text(encoding='utf-8'))
    ledger = (ROOT / '.aide/controller/outcome-ledger.jsonl').read_bytes()
    assert hashlib.sha256(ledger).hexdigest() == record['after_sha256']
    assert hashlib.sha256(ledger[:record['before_bytes']]).hexdigest() == record['before_sha256']
    (OUTPUT / 'actual-lesson.json').write_text(json.dumps(actual, indent=2) + '\n', encoding='utf-8')
