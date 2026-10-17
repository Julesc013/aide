"""One admitted offline test/smoke job; fixtures use the runner-owned TEMP."""
import sys
sys.dont_write_bytecode = True

import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import unittest

root = Path.cwd()
output = Path(os.environ['AIDE_JOB_OUTPUT'])
temporary = Path(os.environ['AIDE_JOB_TMP'])
assert output.is_dir() and temporary.is_dir() and output.parent == temporary.parent
assert Path(os.environ['TEMP']) == temporary
modules = ['test_task_binding', 'test_x_os_01_task_os_commands', 'test_task_current']
suite = unittest.TestSuite()
inputs = {}
for name in modules:
    path = root / '.aide/scripts/tests' / (name + '.py')
    inputs[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))

def identities(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from identities(test)
        else:
            yield test.id()

expected = list(identities(suite))
assert len(expected) == len(set(expected)) and expected
with (output / 'tests.stderr').open('w', encoding='utf8', newline='\n') as stream:
    with (output / 'tests.stdout').open('w', encoding='utf8', newline='\n') as stdout:
        with contextlib.redirect_stdout(stdout):
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
counts = {'tests_run': result.testsRun, 'failures': len(result.failures),
          'errors': len(result.errors), 'skipped': [(t.id(), why) for t, why in result.skipped],
          'expected_test_ids': expected, 'inputs': inputs}
(output / 'tests.json').write_bytes((json.dumps(counts, indent=2) + '\n').encode())
assert result.testsRun == len(expected)
assert result.wasSuccessful() and not result.skipped

commands = [
    ['--task-id', 'AIDE-DAILY-DISKED-EXPORT-01', '--json'],
    ['--task-id', 'AIDE-DAILY-DISKED-EXPORT-01'],
    ['--task-id', '../../outside', '--json'],
]
smokes = []
for number, args in enumerate(commands):
    completed = subprocess.run([sys.executable, '-I', '-B', str(root / '.aide/scripts/aide_lite.py'),
        '--repo-root', str(root), 'task', 'current', *args], capture_output=True, timeout=20)
    expected_code = 1 if number == 2 else 0
    for stream in ('stdout', 'stderr'):
        (output / f'smoke-{number}.{stream}').write_bytes(getattr(completed, stream))
    smokes.append({'args': args, 'exit_code': completed.returncode,
                   'stdout_sha256': hashlib.sha256(completed.stdout).hexdigest(),
                   'stderr_sha256': hashlib.sha256(completed.stderr).hexdigest()})
    assert completed.returncode == expected_code
    if number == 0:
        view = json.loads(completed.stdout)
        assert view['task_id'] == 'AIDE-DAILY-DISKED-EXPORT-01' and view['status'] == 'passed'
        assert view['scope']['target_mutated'] is False and view['scope']['product_qualified'] is False
        assert view['next_action'] == 'prepare_separate_native_owner_admission_no_further_fixture_jobs'
        assert view['acceptance_verified'] is False
    if number == 2:
        assert json.loads(completed.stdout)['task_id'] == ''
for relative, digest in inputs.items():
    assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
(output / 'smokes.json').write_bytes((json.dumps(smokes, indent=2) + '\n').encode())
print(json.dumps({'status': 'PASS', 'tests': result.testsRun, 'cli_smokes': len(smokes),
                  'models_requested': 0, 'target_mutated': False, 'whole_task_usage': 'unknown'}))
