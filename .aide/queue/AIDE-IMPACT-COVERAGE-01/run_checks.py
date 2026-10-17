"""Run unchanged and new impact checks in existing owned job scratch."""
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
BASE = '36d388a72b6e6e941ca84c93387d742f85af3064'
TEST = '.aide/scripts/tests/test_x_test_00_validation_tiers.py'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

module = load('impact_subject_tests', SUBJECT / TEST)
assert module.MODULE_PATH.resolve() == (SUBJECT / '.aide/scripts/aide_lite.py').resolve()
inputs = {TEST: sha(SUBJECT / TEST), '.aide/scripts/aide_lite.py': sha(module.MODULE_PATH)}
label = 'source' if SUBJECT == ROOT else 'delivered'
if label == 'source':
    original = subprocess.check_output(['git', 'show', BASE + ':.aide/scripts/aide_lite.py'])
    baseline = json.loads((ROOT / '.aide/queue/AIDE-IMPACT-COVERAGE-01/evidence/baseline.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(original).hexdigest() == baseline['inputs']['.aide/scripts/aide_lite.py']
    old_path = SCRATCH / 'impact-original.py'
    old_path.write_bytes(original)
    old = load('impact_original', old_path)
    fixture = module.ValidationTierCommandTests()
    try:
        root = fixture.make_git_repo()
        old_result = old.build_test_impact_plan(root, 'refs/heads/base-not-present')
        current = module.aide_lite.build_test_impact_plan(root, 'refs/heads/base-not-present')
        observed = {name: {key: value.get(key) for key in
                    ('recommended_tier', 'changed_paths', 'changed_path_observation', 'warnings')}
                    for name, value in [('original', old_result), ('candidate', current)]}
        (OUTPUT / 'missing-base-comparison.json').write_text(json.dumps(observed, indent=2) + '\n', encoding='utf-8')
        assert old_result['recommended_tier'] == 'T0' and 'no_changed_paths_detected' in old_result['warnings']
        assert current['recommended_tier'] == 'T2' and current['changed_path_observation'] == 'incomplete'
        assert 'no_changed_paths_detected' not in current['warnings']
    finally:
        fixture.doCleanups()
suite = unittest.defaultTestLoader.loadTestsFromModule(module)
def identities(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from identities(test)
        else:
            yield test.id()
expected = list(identities(suite))
assert len(expected) == 13 and len(set(expected)) == 13
with (OUTPUT / (label + '-tests.log')).open('w', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
record = {'subject': label, 'test_ids': expected, 'tests_run': result.testsRun,
          'failures': len(result.failures), 'errors': len(result.errors),
          'skips': [(case.id(), why) for case, why in result.skipped], 'inputs': inputs,
          'actual_cli': str(module.MODULE_PATH), 'models_requested': 0,
          'whole_outcome_usage': 'unknown'}
(OUTPUT / (label + '-tests.json')).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
assert result.testsRun == len(expected) and result.wasSuccessful() and not result.skipped
for p,d in inputs.items():
    assert sha(SUBJECT / p) == d
print(json.dumps({'status': 'PASS', 'subject': label, 'tests': result.testsRun}))
