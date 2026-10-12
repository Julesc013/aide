"""Run admitted named unit-test modules; temp fixtures stay in managed scratch."""
import sys
sys.dont_write_bytecode = True
import argparse
import importlib.util
import json
import os
from pathlib import Path
import unittest

parser = argparse.ArgumentParser(allow_abbrev=False)
parser.add_argument('--baseline', action='store_true')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
files = ['test_task_binding.py']
if not args.baseline:
    files += ['test_verifier.py', 'test_review_pack.py', 'test_token_ledger.py', 'test_aide_lite.py']
suite = unittest.TestSuite()
for name in files:
    spec = importlib.util.spec_from_file_location('daily_' + Path(name).stem,
                                                repo / '.aide/scripts/tests' / name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
result = unittest.TextTestRunner(verbosity=2).run(suite)
record = {'schema': 'aide.daily-task-binding.checks.v1',
          'stage': 'baseline' if args.baseline else 'repaired', 'modules': files,
          'tests_run': result.testsRun, 'failures': len(result.failures),
          'errors': len(result.errors), 'skips': len(result.skipped),
          'status': 'PASS' if result.wasSuccessful() else 'FAIL',
          'models_requested': 0, 'job_id': os.environ['AIDE_JOB_ID'],
          'filesystem_containment_claimed': False}
(Path(os.environ['AIDE_JOB_OUTPUT']) / 'checks.json').write_text(
    json.dumps(record, sort_keys=True, indent=2) + '\n', encoding='utf-8', newline='\n')
raise SystemExit(0 if result.wasSuccessful() else 1)
