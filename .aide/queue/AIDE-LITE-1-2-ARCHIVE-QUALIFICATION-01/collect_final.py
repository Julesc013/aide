"""Preserve final terminal records before classifying complete acceptance."""
import base64
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'
E = TASK / 'evidence'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    h = load('final_preservation_owner', TASK / 'collect_hosted.py')
    verify = load('final_roundtrip_owner', TASK / 'verify_profile_collection.py')
    group = json.loads((E / 'final-checkpoint.log').read_bytes())
    files = {'final-checkpoint.log': base64.b64encode((E / 'final-checkpoint.log').read_bytes()).decode()}
    for operation in group['operations']:
        for name, value in operation.get('streams', {}).items():
            path = E / 'final-checkpoint-streams.log' / name
            assert path.stat().st_size == value['bytes'] and h.sha(path) == value['sha256']
            files['final-checkpoint-streams.log/' + name] = base64.b64encode(path.read_bytes()).decode()
    path = E / 'final-controller-retained.json'
    h.preserve(path, files)
    assert verify.restore(path) == {name: base64.b64decode(raw) for name, raw in files.items()}
    assert 'job_result' in group, 'controller bytes retained; reconcile actual admission before any continuation'
    record = group['job_result']
    effect = json.loads((E / 'final-effect.json').read_bytes())
    template = json.loads((E / 'final-job-template.json').read_bytes())
    submitted = dict(template, source_commit=group['commit']['candidate_commit'], source_tree=group['commit']['expected_tree'])
    assert group['job'] == record['job'] == submitted
    assert record['manifest_digest'] == workspace.digest(submitted)
    assert record['config_digest'] == effect['qualification_config_digest']
    assert record['phase'] == 'retired' and record['scratch_absent'] and record['reservation_released']
    assert not Path(record['scratch']).exists()
    retained = Path(record['retained'])
    for name, value in record['collected_manifest'].items():
        assert workspace.content_digest(retained / name) == value
    files = {p.relative_to(retained).as_posix(): base64.b64encode(p.read_bytes()).decode()
             for p in retained.rglob('*') if p.is_file()}
    path = E / 'final-job-retained.json'
    h.preserve(path, files)
    assert verify.restore(path) == {name: base64.b64decode(raw) for name, raw in files.items()}
    for name, value in effect['stable_assets'].items():
        assert h.sha(ROOT / name) == value
    frozen = json.loads((E / 'revised-pack-subject.json').read_bytes())
    assert len(frozen) == 879 and all(h.sha(ROOT / name) == value for name, value in frozen.items())
    output = retained / 'output'
    phase_path = output / 'final-group.json'
    phases = json.loads(phase_path.read_bytes()) if phase_path.exists() else {'status': 'INCOMPLETE', 'phases': []}
    passed = (record['result'].get('exit_code') == 0 and record['result'].get('quiescent')
        and not record['result'].get('io_errors') and phases['status'] == 'PASS'
        and len(phases['phases']) == 3 and all(p['state'] == 'PASS' and p['fixture_retired'] for p in phases['phases']))
    summaries = {}
    for label, relative in [('managed', 'managed/consumer-result.json'), ('brownfield', 'brownfield/predecessor-result.json'),
                            ('replay', 'replay/replay-result.json'), ('primary_identity', 'replay/primary-revised-identity.json')]:
        path = output / relative
        if path.exists():
            summaries[label] = json.loads(path.read_bytes())
    if passed:
        assert set(summaries) == {'managed', 'brownfield', 'replay', 'primary_identity'}
        built = json.loads((E / 'profile-build-result.json').read_bytes())
        managed, predecessor, replay = (summaries[k] for k in ('managed', 'brownfield', 'replay'))
        assert managed['status'] == 'PASS' and managed['case'] == 6 and managed['fixture_retired']
        assert managed['assets'] == predecessor['assets'] == built['assets']
        assert predecessor['status'] == 'PASS' and predecessor['fixture_retired'] and len(predecessor['cases']) == 1
        assert predecessor['cases'][0]['shape'] == 'published-upgrade-brownfield' and predecessor['cases'][0]['native_acceptance']
        assert replay['status'] == 'PASS' and replay['fixture_retired'] and replay['preserved_pack_files'] == 879
        assert replay['identity'] == built['identity']
        assert all(value == built['assets'][name] for name, value in replay['replay'].items())
        assert all(value['state'] == 'completed' and value['exit_code'] == 0 for value in replay['operations'].values())
        for label, summary in summaries.items():
            h.h.save(E / ('final-' + label + '-result.json'), summary)
    summary = {'state': 'PASS_FINAL_LOCAL_GROUP_AND_EXACT_REPLAY' if passed else 'TERMINAL_FINAL_LOCAL_INCOMPLETE',
        'qualification_pass': passed, 'job_id': record['job_id'], 'subject': {'commit': submitted['source_commit'], 'tree': submitted['source_tree']},
        'manifest_digest': record['manifest_digest'], 'config_digest': record['config_digest'],
        'collected_manifest': record['collected_manifest'], 'retained': record['retained'], 'retained_files': len(files),
        'controller_operations': len(group['operations']), 'controller_retained_sha256': h.sha(E / 'final-controller-retained.json'),
        'job_retained_sha256': h.sha(E / 'final-job-retained.json'), 'lossless_roundtrip_verified': True,
        'phases': phases, 'peaks': record['peaks'], 'result': record['result'], 'scratch_absent': True, 'reservation_released': True,
        'local_jobs_consumed': 17, 'local_job_ceiling': 17, 'hosted_runs_consumed': 2, 'hosted_jobs_consumed': 5,
        'export_refreshes_consumed': 2, 'support_activated': False, 'published': False,
        'worker_model_requests': 0, 'whole_model_usage': 'unknown',
        'next_boundary': 'Independent evidence closure and separately reviewed integration/publication/acquisition; no automatic retry.'}
    h.h.save(E / 'final-qualified.json', summary)
    print(json.dumps({'state': summary['state'], 'subject': summary['subject'], 'job_id': record['job_id'],
        'retained_files': len(files), 'phase_seconds': {p['phase']: (p['finished_unix_ns'] - p['started_unix_ns']) / 1e9 for p in phases['phases']}}))


if __name__ == '__main__':
    main()
