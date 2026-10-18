"""Qualify actual source/delivered development brief with preserved existing assertions."""
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
for name in ['test_task_brief', 'test_task_current', 'test_resume_plan', 'test_q38_file_quality', 'test_outcome_lessons']:
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
expected_count = 84
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
    selected_task = 'AIDE-VALIDATION-OUTPUT-01'
    selected_path = '.aide/scripts/tests/test_validation_output.py'
    observed_refs = ['.aide/controller/outcome-ledger.jsonl', '.aide/reports/file-quality-ledger.json',
        '.aide/queue/' + selected_task + '/task.yaml', '.aide/queue/' + selected_task + '/status.yaml']
    before = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in observed_refs}
    command = [sys.executable, '-I', '-B', str(ROOT / '.aide/scripts/aide_lite.py'), 'task', 'brief',
               '--task-id', selected_task, '--path', selected_path, '--json']
    called = subprocess.run(command, capture_output=True, timeout=30)
    (OUTPUT / 'actual-brief.stdout').write_bytes(called.stdout)
    (OUTPUT / 'actual-brief.stderr').write_bytes(called.stderr)
    assert called.returncode in (0, 2)
    actual = json.loads(called.stdout)
    assert actual['result'] in ('OBSERVED', 'PARTIAL')
    assert actual['continuation']['task']['task_id'] == selected_task
    assert actual['continuation']['recommendation'] == 'inspect_completed_evidence'
    assert [x['id'] for x in actual['lessons']['selected']] == ['portable-validation-fixture']
    assert all(x['state'] == 'matching' for x in actual['lessons']['selected'][0]['evidence'])
    assert actual['quality']['result'] in ('PASS', 'MISSING')
    assert actual['quality'].get('freshness', 'unverified') == 'unverified'
    assert not actual['acceptance_verified'] and not actual['execution_admitted']
    assert {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in observed_refs} == before
    (OUTPUT / 'actual-brief.json').write_text(json.dumps(actual, indent=2) + '\n', encoding='utf-8')
