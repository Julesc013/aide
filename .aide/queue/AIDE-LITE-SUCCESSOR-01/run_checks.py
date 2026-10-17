"""Finite reviewed test partitions with durable per-method terminal records."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

task = Path(__file__).resolve().parent
roster = json.loads((task / 'evidence/batch-roster.json').read_text(encoding='utf-8'))
batch = sys.argv[1]
groups = {**roster['source_batches'], **roster['delivered_batches']}
assert batch in groups
root = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path.cwd()
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

all_ids = list(identities(suite))
assert len(all_ids) == 60 and set(all_ids) == set(roster['all_source_test_ids'])
expected = groups[batch]
assert expected and len(expected) == len(set(expected)) and set(expected) <= set(all_ids)

def selected(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from selected(test)
        elif test.id() in expected:
            yield test

suite = unittest.TestSuite(selected(suite))
assert set(identities(suite)) == set(expected)
label = 'delivered' if 'export' in root.parts else 'source'
assert batch.startswith(label)
with (output / (batch + '-events.jsonl')).open('x', encoding='utf-8') as journal:
    class DurableResult(unittest.TextTestResult):
        def record(self, test, outcome):
            journal.write(json.dumps({'test_id': test.id(), 'outcome': outcome}) + '\n')
            journal.flush()
            os.fsync(journal.fileno())
        def startTest(self, test):
            super().startTest(test)
            self.record(test, 'started')
        def addSuccess(self, test):
            super().addSuccess(test)
            self.record(test, 'passed')
        def addFailure(self, test, err):
            super().addFailure(test, err)
            self.record(test, 'failed')
        def addError(self, test, err):
            super().addError(test, err)
            self.record(test, 'error')
        def addSkip(self, test, reason):
            super().addSkip(test, reason)
            self.record(test, 'skipped')
        def addSubTest(self, test, subtest, err):
            super().addSubTest(test, subtest, err)
            if err is not None:
                self.record(test, 'failed' if issubclass(err[0], test.failureException) else 'error')
    with (output / (batch + '-tests.log')).open('w', encoding='utf-8') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=DurableResult).run(suite)
(output / (batch + '-tests.json')).write_text(json.dumps({
    'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
    'skips': [(test.id(), why) for test, why in result.skipped], 'test_ids': expected,
    'test_inputs': inputs, 'subject': label, 'batch': batch,
    'scope': 'synthetic release lineage; not actual published-predecessor upgrade evidence'}, indent=2) + '\n', encoding='utf-8')
assert result.testsRun == len(expected) and result.wasSuccessful() and not result.skipped
for relative, digest in inputs.items():
    assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
print(json.dumps({'status': 'PASS', 'tests': result.testsRun, 'subject': label, 'batch': batch}))
