"""Original release checks plus successor fixtures in owned managed scratch."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
output = Path(os.environ['AIDE_JOB_OUTPUT'])
assert Path(tempfile.gettempdir()) == Path(os.environ['AIDE_JOB_TMP'])
suite = unittest.TestSuite()
inputs = {}
for name in ('test_q47_release_bundle', 'test_q48_github_release_draft',
             'test_stable_release_admission', 'test_public_archive_fixture', 'test_stable_successor'):
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
assert len(expected) == 60 and len(expected) == len(set(expected)), expected
label = 'delivered' if 'export' in root.parts else 'source'
with (output / (label + '-tests.log')).open('w', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
(output / (label + '-tests.json')).write_text(json.dumps({
    'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
    'skips': [(test.id(), why) for test, why in result.skipped], 'test_ids': expected,
    'test_inputs': inputs, 'subject': label,
    'scope': 'synthetic release lineage; not actual published-predecessor upgrade evidence'}, indent=2) + '\n', encoding='utf-8')
assert result.testsRun == len(expected) and result.wasSuccessful() and not result.skipped
for relative, digest in inputs.items():
    assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
print(json.dumps({'status': 'PASS', 'tests': result.testsRun, 'subject': label}))
