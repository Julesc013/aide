"""Preserve the terminal link-regression attempt before its fixture correction."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace

spec = importlib.util.spec_from_file_location('link_collection_helpers', TASK / 'collect_remaining.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
raw = (E / 'link-execution.log').read_bytes()
group = json.loads(raw)
record = group['job_result']
assert group['state'] == 'stopped' and record['phase'] == 'retired'
assert record['result']['exit_code'] == 1 and record['result']['quiescent'] and not record['result']['io_errors']
assert record['scratch_absent'] and record['reservation_released'] and not Path(record['scratch']).exists()
assert record['job'] == group['job'] and workspace.digest(record['job']) == record['manifest_digest']
retained = Path(record['retained'])
for name, expected in record['collected_manifest'].items():
    assert workspace.content_digest(retained / name) == expected
import base64
files = {p.relative_to(retained).as_posix(): base64.b64encode(p.read_bytes()).decode('ascii')
         for p in sorted(retained.rglob('*')) if p.is_file()}
helper.save(E / 'link-initial-retained.json', helper.bundle(json.dumps(files, sort_keys=True, separators=(',', ':')).encode(), files=len(files)))
helper.save(E / 'link-initial-source-execution.json', helper.bundle(raw))
result = json.loads((retained / 'output/link-result.json').read_bytes())
assert not result['export_refreshed'] and result['state'] == 'stopped'
original = json.loads((retained / 'output/original-legal-transition.json').read_bytes())
assert original['tests_run'] == 1 and len(original['errors']) == 1 and not original['failures'] and not original['skips']
assert "TypeError: '_GeneratorContextManager' object is not iterable" in original['errors'][0][1]
assert not (retained / 'output/link-regressions.json').exists()
prior = json.loads((E / 'link-prior-export.json').read_bytes())
for name, value in prior['files'].items():
    assert workspace.file_digest(ROOT / '.aide/export/aide-lite-pack-v0' / name) == value['sha256']
helper.save(E / 'link-initial-result.json', {'state': 'FAIL_TEST_FIXTURE_PROTOCOL_BEFORE_REGRESSIONS_OR_EXPORT',
    'job_id': record['job_id'], 'source': group['commit']['candidate_commit'], 'result': record['result'],
    'original_probe': original, 'retained_files': len(files), 'collected_manifest': record['collected_manifest'],
    'retained': record['retained'], 'scratch_absent': True, 'reservation_released': True,
    'corrected_checks_run': 0, 'export_refreshed': False, 'local_jobs_consumed': 13,
    'meaning': 'The new fixture supplied only a context manager; the original scanner also requires an iterable. No product or original incident verdict follows.'})
print(json.dumps({'state': 'RETAINED_ORIGINAL_FIXTURE_FAILURE', 'files': len(files), 'job_id': record['job_id'], 'new_jobs': 0}))
