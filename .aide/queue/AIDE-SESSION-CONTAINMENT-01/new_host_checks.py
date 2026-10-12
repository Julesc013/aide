"""Run only pure task-local prerequisite checks under the existing job owner."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import json
import os
from pathlib import Path
import unittest

tests_path = Path(__file__).with_name('test_probe_mxc_backend.py')
spec = importlib.util.spec_from_file_location('new_host_prerequisite_tests', tests_path)
tests = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tests)
result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
record = {'schema': 'aide.new-host-source-check.v1', 'tests_run': result.testsRun,
          'failures': len(result.failures), 'errors': len(result.errors),
          'skipped': len(result.skipped), 'status': 'PASS' if result.wasSuccessful() else 'FAIL',
          'job_id': os.environ['AIDE_JOB_ID'], 'models_requested': 0,
          'native_sandbox_requested': False, 'whole_session_contained': False}
output = Path(os.environ['AIDE_JOB_OUTPUT']) / 'source-checks.json'
output.write_text(json.dumps(record, sort_keys=True, indent=2) + '\n', encoding='utf-8', newline='\n')
raise SystemExit(0 if result.wasSuccessful() else 1)
