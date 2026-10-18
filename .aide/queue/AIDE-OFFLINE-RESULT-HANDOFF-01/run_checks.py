"""Qualify source/delivered result exchange, retaining every original assertion."""
import sys
sys.dont_write_bytecode = True
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import unittest

ROOT = Path.cwd()
SUBJECT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
label = 'source' if SUBJECT == ROOT else 'delivered'
suite = unittest.TestSuite()
inputs = {}
for name in ['test_task_handoff', 'test_task_binding', 'test_task_current', 'test_resume_plan']:
    path = SUBJECT / '.aide/scripts/tests' / (name + '.py')
    spec = importlib.util.spec_from_file_location('handoff_' + name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    assert Path(module.aide.__file__).resolve() == SUBJECT / '.aide/scripts/aide_lite.py'
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    inputs[path.relative_to(SUBJECT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
for relative in ['.aide/scripts/aide_lite.py', '.aide/scripts/task_handoff.py']:
    inputs[relative] = hashlib.sha256((SUBJECT / relative).read_bytes()).hexdigest()

def ids(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from ids(test)
        else:
            yield test.id()

expected = list(ids(suite))
prior = json.loads((ROOT / '.aide/queue/AIDE-PORTABLE-TASK-HANDOFF-01/evidence/attempt-01-source-tests.json').read_text())
assert len(expected) == 97 and len(set(expected)) == 97
assert len(prior['test_ids']) == 79 and set(prior['test_ids']) <= set(expected)
with (OUTPUT / (label + '-tests.log')).open('w', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
record = {'subject': label, 'test_ids': expected, 'tests_run': result.testsRun,
          'failures': len(result.failures), 'errors': len(result.errors),
          'skips': [(case.id(), why) for case, why in result.skipped], 'inputs': inputs,
          'original_tests_retained': 79, 'models_requested': 0, 'whole_outcome_usage': 'unknown'}
(OUTPUT / (label + '-tests.json')).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
assert result.testsRun == 97 and result.wasSuccessful() and not result.skipped
for path, digest in inputs.items():
    assert hashlib.sha256((SUBJECT / path).read_bytes()).hexdigest() == digest
print(json.dumps({'status': 'PASS', 'subject': label, 'tests': result.testsRun}))
