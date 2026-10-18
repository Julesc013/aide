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
repair = '--repair' in sys.argv
SUBJECT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 and not repair else ROOT
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
label = 'source-repair' if repair else ('source' if SUBJECT == ROOT else 'delivered')
suite = unittest.TestSuite()
inputs = {}
for name in ['test_validation_output', 'test_aide_lite', 'test_review_pack']:
    if repair and name == 'test_review_pack':
        continue
    path = SUBJECT / '.aide/scripts/tests' / (name + '.py')
    spec = importlib.util.spec_from_file_location('validation_' + name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    assert Path(getattr(module, 'aide', getattr(module, 'aide_lite', None)).__file__).resolve() == SUBJECT / '.aide/scripts/aide_lite.py'
    if repair and name == 'test_aide_lite':
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName(
            'AideLiteWorkflowTests.test_portable_apply_descriptions_match_shipped_modules', module))
    else:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    inputs[path.relative_to(SUBJECT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
for relative in ['.aide/scripts/aide_lite.py']:
    inputs[relative] = hashlib.sha256((SUBJECT / relative).read_bytes()).hexdigest()
def ids(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from ids(test)
        else:
            yield test.id()
expected = list(ids(suite))
expected_count = 10 if repair else 36
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
