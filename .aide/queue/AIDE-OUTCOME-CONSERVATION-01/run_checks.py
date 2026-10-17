"""Qualify the existing outcome owner in admitted scratch, source or delivered."""
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
BASE = '442c2cccb5640c3e2a21157802935af4e53a4f68'
TASK = ROOT / '.aide/queue/AIDE-OUTCOME-CONSERVATION-01'
TEST = '.aide/scripts/tests/test_outcome_controller.py'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

module = load('outcome_subject_tests', SUBJECT / TEST)
assert module.MODULE_PATH.resolve() == (SUBJECT / '.aide/scripts/aide_lite.py').resolve()
inputs = {TEST: sha(SUBJECT / TEST), '.aide/scripts/aide_lite.py': sha(module.MODULE_PATH)}
label = 'source' if SUBJECT == ROOT else 'delivered'
if label == 'source':
    original = subprocess.check_output(['git', 'show', BASE + ':.aide/scripts/aide_lite.py'])
    baseline = json.loads((TASK / 'evidence/baseline.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(original).hexdigest() == baseline['inputs']['.aide/scripts/aide_lite.py']
    old_path = SCRATCH / 'outcome-original.py'
    old_path.write_bytes(original)
    old = load('outcome_original', old_path)
    data = {'run_id': 'original-failure', 'phase': 'check', 'source': 'validation',
            'result': 'FAIL', 'project_provenance': {'subject': 'A', 'lesson': 'keep'}}
    observed = {name: owner.outcome_record_to_dict(owner.outcome_record_from_dict(data))
                for name, owner in [('original', old), ('candidate', module.aide_lite)]}
    assert 'project_provenance' not in observed['original']
    assert observed['candidate']['project_provenance'] == data['project_provenance']
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        ledger = root / old.OUTCOME_LEDGER_PATH
        ledger.parent.mkdir(parents=True)
        ledger.write_text(json.dumps(data) + '\n{\n', encoding='utf-8')
        before = ledger.read_bytes()
        assert len(old.read_outcome_records(root)) == 1
        try:
            module.aide_lite.read_outcome_records(root)
        except ValueError as exc:
            assert 'outcome-ledger.jsonl:2' in str(exc)
            observed['malformed_candidate'] = str(exc)
        else:
            raise AssertionError('candidate silently accepted corrupt ledger')
        assert ledger.read_bytes() == before
    (OUTPUT / 'baseline-comparison.json').write_text(json.dumps(observed, indent=2) + '\n', encoding='utf-8')

suite = unittest.defaultTestLoader.loadTestsFromModule(module)
def identities(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from identities(test)
        else:
            yield test.id()
expected = list(identities(suite))
assert len(expected) == 20 and len(set(expected)) == 20
with (OUTPUT / (label + '-tests.log')).open('w', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
record = {'subject': label, 'test_ids': expected, 'tests_run': result.testsRun,
          'failures': len(result.failures), 'errors': len(result.errors),
          'skips': [(case.id(), why) for case, why in result.skipped], 'inputs': inputs,
          'actual_cli': str(module.MODULE_PATH), 'models_requested': 0,
          'whole_outcome_usage': 'unknown'}
(OUTPUT / (label + '-tests.json')).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
assert result.testsRun == len(expected) and result.wasSuccessful() and not result.skipped
for p, digest in inputs.items():
    assert sha(SUBJECT / p) == digest
print(json.dumps({'status': 'PASS', 'subject': label, 'tests': result.testsRun}))
