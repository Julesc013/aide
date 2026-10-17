"""One unchanged installed-consumer method against the actual development pack."""
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
PACK = ROOT / '.aide/export/aide-lite-pack-v0'
OUT = Path(os.environ['AIDE_JOB_OUTPUT'])
assert Path(tempfile.gettempdir()) == Path(os.environ['AIDE_JOB_TMP'])
def inventory():
    return {p.relative_to(PACK).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in PACK.rglob('*') if p.is_file()}

expected = json.loads((ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01/evidence/pack-repair-first-pack-repair-delta.json').read_text(encoding='utf-8'))['after_sha256s']
assert inventory() == expected
path = PACK / 'files/.aide/scripts/tests/test_work_effort.py'
spec = importlib.util.spec_from_file_location('delivered_effort_consumer', path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

class InstalledPackEffort(module.WorkEffortTests):
    def export_fixture(self):
        # Source construction was qualified separately. This consumer uses the
        # exact already-built artifact, never reconstructing another source repo.
        return PACK / 'files', PACK

method = 'test_safe_installed_effort_preserves_project_core_and_never_falls_back'
record = {'status': 'INCOMPLETE', 'test_method': method,
          'delivered_test_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
          'fixture': 'actual_owned_development_pack', 'model_calls': 0,
          'archive_qualification': False}
result_path = OUT / 'direct-installed.json'
result_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
with (OUT / 'direct-installed-tests.log').open('x', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
        unittest.TestSuite([InstalledPackEffort(method)]))
record.update(tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
              skipped=len(result.skipped), pack_unchanged=inventory() == expected)
record['status'] = 'PASS' if result.wasSuccessful() and not result.skipped and record['pack_unchanged'] else 'FAIL'
result_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
assert record['status'] == 'PASS' and result.testsRun == 1
print('PASS actual pack safe-installed fresh and brownfield accounting; archive checks pending')
