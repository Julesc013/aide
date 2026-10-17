"""Focused existing Git behavior and new portable choices in owned job fixtures."""
import sys
sys.dont_write_bytecode = True
import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import unittest

root = Path.cwd()
output = Path(os.environ['AIDE_JOB_OUTPUT'])
temporary = Path(os.environ['AIDE_JOB_TMP'])
assert Path(os.environ['TEMP']) == temporary and output.parent == temporary.parent
for key in list(os.environ):
    if key.startswith('GIT_'):
        os.environ.pop(key)
os.environ.update(GIT_CONFIG_GLOBAL='NUL', GIT_CONFIG_SYSTEM='NUL', GIT_TERMINAL_PROMPT='0')
tools = json.loads((root / '.aide/queue/AIDE-GIT-DEFAULTS-01/evidence/tool-identities.json').read_bytes())
git = Path(shutil.which('git')).resolve()
assert git == Path(tools['git_executable']).resolve()
assert hashlib.sha256(git.read_bytes()).hexdigest() == tools['git_executable_sha256']
assert not subprocess.check_output([str(git), 'status', '--porcelain'], cwd=root).strip()
modules = ['test_q28_git_workflow', 'test_q29_git_helper', 'test_q35_github_advisory',
           'test_git_defaults']
suite = unittest.TestSuite()
inputs = {}
for name in modules:
    path = root / '.aide/scripts/tests' / (name + '.py')
    inputs[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    if name == 'test_q35_github_advisory':
        # Preserve original assertions but redirect its report-writing commands.
        fixture = temporary / 'github-advisory-fixture'
        aide = module.aide_lite
        for relative in [*aide.github_policy_paths(), aide.GITHUB_README_PATH,
                         '.aide/scripts/aide_lite.py']:
            source = root / relative
            assert source.is_file(), relative
            target = fixture / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        module.REPO_ROOT = fixture
        module.MODULE_PATH = fixture / '.aide/scripts/aide_lite.py'
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))

def identities(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from identities(test)
        else:
            yield test.id()

expected = list(identities(suite))
assert expected and len(expected) == len(set(expected))
with (output / 'tests.stderr').open('w', encoding='utf8', newline='\n') as stream:
    with (output / 'tests.stdout').open('w', encoding='utf8', newline='\n') as stdout:
        with contextlib.redirect_stdout(stdout):
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
record = {'tests_run': result.testsRun, 'failures': len(result.failures),
          'errors': len(result.errors), 'skipped': [(t.id(), why) for t, why in result.skipped],
          'expected_test_ids': expected, 'input_hashes': inputs,
          'q35_report_destination': 'owned_temporary_fixture', 'model_calls': 0}
(output / 'tests.json').write_bytes((json.dumps(record, indent=2) + '\n').encode())
for relative, digest in inputs.items():
    assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
assert result.testsRun == len(expected) and result.wasSuccessful() and not result.skipped
assert not subprocess.check_output([str(git), 'status', '--porcelain'], cwd=root).strip()
print(json.dumps({'result': 'PASS', 'tests': result.testsRun, 'model_calls': 0,
                  'remote_effects': False, 'whole_task_usage': 'unknown'}))
