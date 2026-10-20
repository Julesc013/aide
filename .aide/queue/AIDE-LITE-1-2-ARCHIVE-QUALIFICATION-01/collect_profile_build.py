"""Preserve the metadata-only build, exact member delta and retired job identity."""
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
spec = importlib.util.spec_from_file_location('profile_collection_helpers', TASK / 'collect_remaining.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
raw = (E / 'profile-build-execution.log').read_bytes()
group = json.loads(raw)
record = group['job_result']
assert group['state'] == 'local_terminal' and group['commit']['status'] == 'COMMITTED'
assert record['phase'] == 'retired' and record['result']['exit_code'] == 0
assert record['result']['quiescent'] and not record['result']['io_errors']
assert record['scratch_absent'] and record['reservation_released'] and not Path(record['scratch']).exists()
effect = json.loads((E / 'profile-build-effect.json').read_bytes())
template = json.loads((E / 'profile-build-job-template.json').read_bytes())
submitted = dict(template, source_commit=group['commit']['candidate_commit'], source_tree=group['commit']['expected_tree'])
assert record['job'] == group['job'] == submitted and workspace.digest(submitted) == record['manifest_digest']
assert record['config_digest'] == effect['qualification_config_digest']
retained = Path(record['retained'])
for name, expected in record['collected_manifest'].items():
    assert workspace.content_digest(retained / name) == expected
files = {p.relative_to(retained).as_posix(): base64.b64encode(p.read_bytes()).decode('ascii')
         for p in sorted(retained.rglob('*')) if p.is_file()}
h.save(E / 'profile-build-retained.json', h.bundle(json.dumps(files, sort_keys=True, separators=(',', ':')).encode(), files=len(files)))
h.save(E / 'profile-build-source-execution.json', h.bundle(raw))
result = json.loads((retained / 'output/profile-build-result.json').read_bytes())
delta = json.loads((retained / 'output/profile-archive-member-delta.json').read_bytes())
assert result['status'] == 'PASS_BUILD_ONLY' and result['archive_members'] == 879
assert delta['state'] == 'PASS_METADATA_ONLY_COMPLETE_DELTA' and not delta['changed_executable_files']
assert delta['unchanged_members_per_archive'] == 877
assert result['identity']['source_commit'] == '158a5cdcac7afecbc180a6324ea02e46617d1bc9'
for kind in ('zip', 'tar.gz'):
    part = delta['inventories'][kind]
    assert len(part['old']) == len(part['new']) == 879 and len(part['changed']) == 2
    assert set(part['changed']) == {'aide-lite-pack-v0/stable-release.json', 'aide-lite-pack-v0/checksums.json'}
for name, value in result['assets'].items():
    assert workspace.file_digest(ROOT / name) == value['sha256']
for name, expected in json.loads((E / 'baseline.json').read_bytes())['stable_assets'].items():
    assert workspace.file_digest(ROOT / name) == expected
for name, expected in json.loads((E / 'revised-pack-subject.json').read_bytes()).items():
    assert workspace.file_digest(ROOT / name) == expected
h.save(E / 'profile-build-result.json', result)
h.save(E / 'profile-archive-member-delta.json', delta)
summary = {'state': 'PASS_METADATA_BUILD_AND_COMPLETE_DELTA_ONLY', 'job_id': record['job_id'],
    'subject': {'commit': submitted['source_commit'], 'tree': submitted['source_tree']},
    'assets': result['assets'], 'payload_source': result['identity']['source_commit'],
    'manifest_digest': record['manifest_digest'], 'config_digest': record['config_digest'],
    'collected_manifest': record['collected_manifest'], 'retained': record['retained'], 'retained_files': len(files),
    'peaks': record['peaks'], 'scratch_absent': True, 'reservation_released': True,
    'local_jobs_consumed': 16, 'local_job_ceiling': 17, 'export_refreshes_consumed': 2,
    'hosted_runs_consumed': 1, 'hosted_run_ceiling': 2,
    'qualification': 'Metadata-only equivalence; macOS applicability, two-profile hosted execution and final local group remain separately gated.'}
h.save(E / 'profile-build-qualified.json', summary)
print(json.dumps({'state': summary['state'], 'subject': summary['subject'], 'job_id': record['job_id'],
    'retained_files': len(files), 'changed_members_per_archive': 2, 'assets': result['assets']}))
