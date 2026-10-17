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
def load(name):
    path = root / '.aide/scripts/tests' / (name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

new = load('test_installed_changelog_guard')
q31 = load('test_q31_export_pack_governance')
suite = unittest.TestSuite([
    unittest.defaultTestLoader.loadTestsFromModule(new),
    q31.Q31ExportPackGovernanceTests('test_fixture_import_runs_governance_commands_without_hook_install'),
    new.fixtures.ExportImportTests('test_source_checkout_missing_queue_index_cannot_bypass_job_guard'),
])
inputs = {str(path.relative_to(root)).replace('\\', '/'): hashlib.sha256(path.read_bytes()).hexdigest()
          for path in [root / '.aide/scripts/aide_lite.py', root / '.aide/scripts/tests/test_installed_changelog_guard.py',
                       root / '.aide/scripts/tests/test_q31_export_pack_governance.py', root / '.aide/scripts/tests/test_export_import.py']}

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
          'fixture_destination': 'owned_temporary_fixture', 'model_calls': 0}
(output / 'tests.json').write_bytes((json.dumps(record, indent=2) + '\n').encode())
for relative, digest in inputs.items():
    assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
assert result.testsRun == len(expected) and result.wasSuccessful() and not result.skipped
assert not subprocess.check_output([str(git), 'status', '--porcelain'], cwd=root).strip()
print(json.dumps({'result': 'PASS', 'tests': result.testsRun, 'model_calls': 0,
                  'remote_effects': False, 'whole_task_usage': 'unknown'}))
