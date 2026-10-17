"""Bounded source/delivered regressions; TEMP is owned managed scratch."""
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

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
output = Path(os.environ['AIDE_JOB_OUTPUT'])
assert Path(tempfile.gettempdir()) == Path(os.environ['AIDE_JOB_TMP'])
suite = unittest.TestSuite()
inputs = {}
source_only = []
for name in ('test_task_current', 'test_task_binding', 'test_x_os_01_task_os_commands', 'test_resume_plan'):
    path = root / '.aide/scripts/tests' / (name + '.py')
    inputs[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    if len(sys.argv) > 1 and name == 'test_x_os_01_task_os_commands':
        # These two assertions concern the self-hosting source history/registry.
        # They run unchanged on source; the export intentionally omits that history.
        source_only = ['test_current_repo_validation_registration_passes',
                       'test_x_os_01_golden_runners_pass']
        for method in unittest.defaultTestLoader.getTestCaseNames(module.XOS01TaskOSCommandTests):
            if method not in source_only:
                suite.addTest(module.XOS01TaskOSCommandTests(method))
    else:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
def identities(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from identities(test)
        else:
            yield test.id()
expected = list(identities(suite))
assert expected and len(expected) == len(set(expected))
label = 'delivered' if 'export' in root.parts else 'source'
with (output / (label + '-tests.log')).open('w', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
(output / (label + '-tests.json')).write_text(json.dumps({
    'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
    'skips': [(test.id(), why) for test, why in result.skipped], 'test_ids': expected,
    'test_inputs': inputs, 'subject': label, 'source_only_tests': source_only}, indent=2) + '\n', encoding='utf-8')
assert result.testsRun == len(expected) and result.wasSuccessful() and not result.skipped
for relative, digest in inputs.items():
    assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
bootstrap = "import os,sys,tempfile,runpy; tempfile.tempdir=os.environ['AIDE_JOB_TMP']; sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')"
consumer = Path(__file__).with_name('run_consumer.py')
subprocess.run([sys.executable, '-B', '-c', bootstrap, str(consumer), str(root)], check=True, timeout=45)
print(json.dumps({'status': 'PASS', 'tests': result.testsRun, 'subject': label}))
