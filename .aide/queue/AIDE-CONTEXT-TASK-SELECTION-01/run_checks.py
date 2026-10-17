"""Qualify selected-task context using actual source or delivered CLI in scratch."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path.cwd()
SUBJECT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
SCRATCH = Path(os.environ['AIDE_JOB_TMP'])
assert Path(tempfile.gettempdir()) == SCRATCH
BASE = '9a22aa0913965c41685105d0781a70ecad16696c'
TASK = ROOT / '.aide/queue/AIDE-CONTEXT-TASK-SELECTION-01'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

label = 'source' if SUBJECT == ROOT else 'delivered'
inputs = {'.aide/scripts/aide_lite.py': sha(SUBJECT / '.aide/scripts/aide_lite.py')}
suite = unittest.TestSuite()
modules = {}
for name in ['test_task_binding', 'test_task_current', 'test_resume_plan', 'test_aide_lite']:
    relative = '.aide/scripts/tests/' + name + '.py'
    module = load('context_' + name, SUBJECT / relative)
    modules[name] = module
    owner = module.aide_lite if name == 'test_aide_lite' else module.aide
    assert Path(owner.__file__).resolve() == (SUBJECT / '.aide/scripts/aide_lite.py').resolve()
    inputs[relative] = sha(SUBJECT / relative)
    if name == 'test_aide_lite':
        suite.addTest(module.AideLiteWorkflowTests('test_context_compiler_generates_maps_and_packet_refs'))
    else:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))

if label == 'source':
    relative = 'core/harness/tests/test_aide_lite.py'
    module = load('context_harness_tests', SUBJECT / relative)
    inputs[relative] = sha(SUBJECT / relative)
    suite.addTest(module.AideLiteTests('test_context_index_outputs_maps_and_packet_refs'))
    original = subprocess.check_output(['git', 'show', BASE + ':.aide/scripts/aide_lite.py'])
    baseline = json.loads((TASK / 'evidence/baseline.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(original).hexdigest() == baseline['inputs']['.aide/scripts/aide_lite.py']
    old_path = SCRATCH / 'context-original.py'
    old_path.write_bytes(original)
    old = load('context_original', old_path)
    candidate = modules['test_task_binding'].aide
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        selected = 'PROJECT-SELECTED-01'
        old.write_text(root / '.aide/queue/index.yaml',
                       f'items:\n  - id: {selected}\n    status: blocked\n')
        old.write_text(root / old.LATEST_PACKET_PATH, f'task_id: {selected}\n')
        old.write_text(root / f'.aide/queue/{selected}/task.yaml', f'id: {selected}\n')
        old.write_text(root / f'.aide/queue/{selected}/status.yaml', 'status: blocked\n')
        old.write_text(root / '.aide/queue/Q17-router-profile-v0/status.yaml', 'status: passed\n')
        observed = {name: owner.current_queue_ref(root) for name, owner in [('original', old), ('candidate', candidate)]}
        assert observed['original'] == '.aide/queue/Q17-router-profile-v0/'
        assert observed['candidate'] == f'.aide/queue/{selected}/'
    (OUTPUT / 'baseline-comparison.json').write_text(json.dumps(observed, indent=2) + '\n', encoding='utf-8')

def identities(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from identities(test)
        else:
            yield test.id()

expected = list(identities(suite))
count = 61 if label == 'source' else 60
assert len(expected) == count and len(set(expected)) == count
with (OUTPUT / (label + '-tests.log')).open('w', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
record = {'subject': label, 'test_ids': expected, 'tests_run': result.testsRun,
          'failures': len(result.failures), 'errors': len(result.errors),
          'skips': [(case.id(), why) for case, why in result.skipped], 'inputs': inputs,
          'actual_cli': str(SUBJECT / '.aide/scripts/aide_lite.py'), 'models_requested': 0,
          'whole_outcome_usage': 'unknown'}
(OUTPUT / (label + '-tests.json')).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
assert result.testsRun == count and result.wasSuccessful() and not result.skipped
for path, digest in inputs.items():
    assert sha(SUBJECT / path) == digest
print(json.dumps({'status': 'PASS', 'subject': label, 'tests': count}))
