"""Focused accounting and real export/import regressions in owned scratch."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path.cwd()
OUT = Path(os.environ['AIDE_JOB_OUTPUT'])
assert Path(tempfile.gettempdir()) == Path(os.environ['AIDE_JOB_TMP'])
suite = unittest.TestSuite()
inputs = {}
for name in ('test_work_effort', 'test_export_import', 'test_aide_lite'):
    path = ROOT / '.aide/scripts/tests' / (name + '.py')
    inputs[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    if name == 'test_work_effort':
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    elif name == 'test_export_import':
        for method in ('test_export_checksums_match_and_are_deterministic',
                       'test_import_safe_mode_skips_broad_source_roots',
                       'test_extracted_export_pack_waits_and_runs_job_without_source_checkout'):
            suite.addTest(module.ExportImportTests(method))
    else:
        suite.addTest(module.AideLiteWorkflowTests('test_portable_apply_descriptions_match_shipped_modules'))

def identities(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from identities(test)
        else:
            yield test.id()

expected = list(identities(suite))
assert len(expected) == 21 and len(set(expected)) == 21
with (OUT / 'tests-events.jsonl').open('x', encoding='utf-8') as journal:
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
        def addSkip(self, test, why):
            super().addSkip(test, why)
            self.record(test, 'skipped')
        def addSubTest(self, test, subtest, err):
            super().addSubTest(test, subtest, err)
            if err is not None:
                self.record(test, 'failed' if issubclass(err[0], test.failureException) else 'error')
    with (OUT / 'tests.log').open('w', encoding='utf-8') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=DurableResult).run(suite)
record = {'tests_run': result.testsRun, 'failures': len(result.failures),
          'errors': len(result.errors), 'skips': [(test.id(), why) for test, why in result.skipped],
          'test_ids': expected, 'test_inputs': inputs, 'models_requested': 0,
          'subject': 'source accounting and generated minimal safe-install fixtures',
          'archive_qualification': False}
(OUT / 'tests.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
assert result.testsRun == 21 and result.wasSuccessful() and not result.skipped
assert all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest for path, digest in inputs.items())
print('PASS 21 focused source and safe-import regressions; actual archives pending')
