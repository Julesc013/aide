"""Preserve the revised candidate's exact build result, full inventory delta and collection."""
import base64
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

spec = importlib.util.spec_from_file_location('revised_build_collection_helpers', TASK / 'collect_remaining.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
raw = (E / 'revised-build-execution.log').read_bytes()
group = json.loads(raw)
record = group['job_result']
assert group['state'] == 'local_terminal' and 'error_type' not in group
assert record['phase'] == 'retired' and record['result']['exit_code'] == 0
assert record['result']['quiescent'] and not record['result']['io_errors']
assert record['scratch_absent'] and record['reservation_released'] and not Path(record['scratch']).exists()
effect = json.loads((E / 'revised-build-effect.json').read_bytes())
template = json.loads((E / 'revised-build-job-template.json').read_bytes())
submitted = dict(template, source_commit=group['commit']['candidate_commit'], source_tree=group['commit']['expected_tree'])
assert record['job'] == group['job'] == submitted and workspace.digest(submitted) == record['manifest_digest']
assert record['config_digest'] == effect['qualification_config_digest']
retained = Path(record['retained'])
for name, expected in record['collected_manifest'].items():
    assert workspace.content_digest(retained / name) == expected
files = {p.relative_to(retained).as_posix(): base64.b64encode(p.read_bytes()).decode('ascii')
         for p in sorted(retained.rglob('*')) if p.is_file()}
h.save(E / 'revised-build-retained.json', h.bundle(json.dumps(files, sort_keys=True, separators=(',', ':')).encode(), files=len(files)))
h.save(E / 'revised-build-source-execution.json', h.bundle(raw))
result = json.loads((retained / 'output/revised-build-result.json').read_bytes())
delta = json.loads((retained / 'output/archive-member-delta.json').read_bytes())
assert result['status'] == 'PASS_BUILD_ONLY' and result['archive_members'] == 879
assert result['identity']['source_commit'] == '158a5cdcac7afecbc180a6324ea02e46617d1bc9'
assert delta['status'] == 'PASS_COMPLETE_MEMBER_DELTA'
assert delta['original_assets'] == json.loads((E / 'build-result.json').read_bytes())['assets']
assert delta['revised_assets'] == result['assets']
assert delta['changed_executable_functions'] == ['core/execution/managed_workspace.py:tree_usage']
for kind in ('zip', 'tar.gz'):
    entry = delta['inventories'][kind]
    assert len(entry['old']) == len(entry['new']) == 879 and len(entry['changed']) == 4
for name, value in result['assets'].items():
    assert workspace.file_digest(ROOT / name) == value['sha256']
for name, digest in json.loads((E / 'baseline.json').read_bytes())['stable_assets'].items():
    assert workspace.file_digest(ROOT / name) == digest
for name, digest in json.loads((E / 'revised-pack-subject.json').read_bytes()).items():
    assert workspace.file_digest(ROOT / name) == digest
h.save(E / 'revised-build-result.json', result)
h.save(E / 'revised-archive-member-delta.json', delta)
h.save(E / 'revised-build-qualified.json', {'state': 'PASS_REVISED_BUILD_AND_COMPLETE_DELTA_ONLY',
    'job_id': record['job_id'], 'subject': {'commit': submitted['source_commit'], 'tree': submitted['source_tree']},
    'assets': result['assets'], 'payload_source': result['identity']['source_commit'],
    'manifest_digest': record['manifest_digest'], 'collected_manifest': record['collected_manifest'],
    'retained': record['retained'], 'retained_files': len(files), 'peaks': record['peaks'],
    'scratch_absent': True, 'reservation_released': True, 'local_jobs_consumed': 15,
    'total_local_ceiling': 16, 'export_refreshes_consumed': 2, 'total_export_ceiling': 2,
    'qualification': 'Reuse applicability, affected consumers, hosted profiles and final replay remain separately gated.'})
print(json.dumps({'state': 'PASS_REVISED_BUILD_AND_COMPLETE_DELTA_ONLY', 'source': submitted['source_commit'],
                  'job_id': record['job_id'], 'retained_files': len(files), 'archive_members': 879,
                  'changed_members_per_archive': 4, 'payload_source': result['identity']['source_commit']}))
