"""One bounded offline job; every database and CLI fixture uses owned TEMP."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

root = Path.cwd()
scratch, output = map(Path, (os.environ['AIDE_JOB_TMP'], os.environ['AIDE_JOB_OUTPUT']))
assert scratch.is_dir() and output.is_dir() and scratch.parent == output.parent
assert Path(tempfile.gettempdir()) == scratch
suite = unittest.TestSuite()
inputs = {}
for name in ('test_continuous_worker_requests', 'test_continuous_worker_state'):
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
assert expected and len(expected) == len(set(expected))
with (output / 'tests.log').open('w', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
observed = {'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
            'skips': [(test.id(), why) for test, why in result.skipped], 'test_ids': expected,
            'test_inputs': inputs, 'mode': 'disposable_cooperative_fixtures', 'live_deliveries': 0,
            'models_requested': 0, 'whole_task_usage': 'unknown'}
(output / 'tests.json').write_text(json.dumps(observed, indent=2) + '\n', encoding='utf-8')
assert result.testsRun == len(expected)
assert result.wasSuccessful() and not result.skipped
for relative, sha256 in inputs.items():
    assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == sha256
print(json.dumps({'status': 'PASS', 'tests': result.testsRun, 'live_deliveries': 0}))
