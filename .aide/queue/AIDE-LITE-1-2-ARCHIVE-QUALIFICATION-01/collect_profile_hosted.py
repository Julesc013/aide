"""Verify all terminal hosted receipts, preserving passes and incomplete profiles."""
import base64
import hashlib
import gzip
import importlib.util
import json
from pathlib import Path

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'
E = TASK / 'evidence'
spec = importlib.util.spec_from_file_location('hosted_collection_helpers', TASK / 'collect_remaining.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preserve(path, files):
    body = json.dumps(files, sort_keys=True, separators=(',', ':')).encode()
    if path.exists():
        existing = json.loads(path.read_bytes())
        if existing.get('encoding') == 'gzip+base64':
            packed = base64.b64decode(existing['data'], validate=True)
            assert hashlib.sha256(packed).hexdigest() == existing['gzip_sha256']
            assert gzip.decompress(packed) == body and existing['files'] == len(files)
            # A prior collection step already preserved this exact body. Retire
            # only freshly generated redundant chunks with verified same bytes.
            for index, offset in enumerate(range(0, len(body), 1024 * 1024)):
                duplicate = E / (path.stem + '-' + f'{index:02d}' + '.json')
                if duplicate.exists():
                    assert json.loads(duplicate.read_bytes()) == h.bundle(body[offset:offset + 1024 * 1024])
                    duplicate.unlink()
            return
    chunks = []
    for offset in range(0, len(body), 1024 * 1024):
        name = path.stem + '-' + f'{len(chunks):02d}' + '.json'
        value = h.bundle(body[offset:offset + 1024 * 1024])
        h.save(E / name, value)
        chunks.append({'path': name, 'sha256': sha(E / name), 'raw_sha256': value['sha256'], 'raw_bytes': value['uncompressed_bytes']})
    h.save(path, {'encoding': 'ordered-gzip+base64-json-chunks', 'files': len(files),
                  'raw_bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(), 'chunks': chunks})


def main():
    checkpoint = json.loads((E / 'profile-hosted-checkpoint.log').read_bytes())
    observation = json.loads((E / 'profile-hosted-execution.log').read_bytes())
    summary = json.loads((E / 'profile-hosted-observed.json').read_bytes())
    assert checkpoint['state'] == 'hosted_observed' and checkpoint['commit']['status'] == 'COMMITTED'
    assert observation['state'] == 'observed_terminal'
    commit = checkpoint['commit']['candidate_commit']
    assert commit == observation['source_commit'] == summary['source_commit'] == checkpoint['dev_synced']
    assert observation['run_id'] == summary['run_id']
    assert sha(E / 'profile-hosted-observed.json') == observation['summary_sha256']
    controller_files = {}
    operations = 0
    for record, folder in ((checkpoint, E / 'profile-hosted-checkpoint-streams.log'), (observation, E / 'profile-hosted-logs.log')):
        for row in record['operations']:
            assert row['state'] == 'completed' and row['exit_code'] == 0
            operations += 1
            for name, expected in row['streams'].items():
                path = folder / name
                assert path.stat().st_size == expected['bytes'] and sha(path) == expected['sha256']
                key = folder.name + '/' + name
                assert key not in controller_files
                controller_files[key] = base64.b64encode(path.read_bytes()).decode('ascii')
    for name in ('profile-hosted-checkpoint.log', 'profile-hosted-execution.log', 'profile-hosted-observed.json'):
        controller_files[name] = base64.b64encode((E / name).read_bytes()).decode('ascii')
    preserve(E / 'profile-hosted-controller-retained.json', controller_files)
    rows = {}
    for profile in ('windows-2025-x64', 'ubuntu-24.04-x64'):
        folder = E / 'profile-hosted-logs.log' / profile
        files = {p.name: p.read_bytes() for p in folder.iterdir() if p.is_file()}
        index = json.loads(files['receipt-index.json'])
        assert set(index) == set(files) - {'receipt-index.json'}
        for name, expected in index.items():
            assert {'bytes': len(files[name]), 'sha256': hashlib.sha256(files[name]).hexdigest()} == expected
        result = json.loads(files['release-result.json'])
        assert result['source_commit'] == commit and not result['support_claimed'] and result['model_requests'] == 0
        encoded = {name: base64.b64encode(raw).decode('ascii') for name, raw in files.items()}
        path = E / ('profile-hosted-' + profile + '-retained.json')
        preserve(path, encoded)
        row = {'status': result['status'], 'qualification_pass': summary['profiles'][profile]['qualification_pass'],
               'environment': result['environment'], 'declared_environment': result['declared_environment'],
               'receipt_bundle': path.relative_to(ROOT).as_posix(), 'receipt_bundle_sha256': sha(path),
               'retained_files': len(files), 'receipt_index_sha256': hashlib.sha256(files['receipt-index.json']).hexdigest(),
               'forms': result.get('forms', []), 'cases': result.get('cases', []),
               'fixture_retired': result['fixture_retired'], 'error_type': result.get('error_type'), 'error': result.get('error')}
        if row['qualification_pass']:
            assert row['status'] == 'PASS' and row['fixture_retired']
            assert len(row['forms']) == 49 and len(row['cases']) == 2 and all(c['native_acceptance'] for c in row['cases'])
        rows[profile] = row
    effect = json.loads((E / 'profile-hosted-effect.json').read_bytes())
    assert all(sha(ROOT / name) == expected for name, expected in effect['stable_assets'].items())
    result = {'state': 'WINDOWS_LINUX_PASS_MACOS_RETAINED_SEPARATELY' if summary['qualification_pass'] else 'TERMINAL_HOSTED_INCOMPLETE',
        'source_commit': commit, 'run_id': summary['run_id'], 'run_url': summary['run_url'],
        'qualification_pass': summary['qualification_pass'], 'profiles': rows, 'controller_operations': operations,
        'controller_streams': len(controller_files) - 3, 'hosted_runs_consumed': 2, 'hosted_run_ceiling': 2,
        'local_allocations_consumed': 16, 'local_allocation_ceiling': 17, 'export_refreshes_consumed': 2,
        'support_claimed': False, 'worker_model_requests': 0, 'whole_model_usage': 'unknown',
        'next_boundary': 'No automatic retry. Final affected local group, fresh primary identity and complete replay remain separately gated.'}
    h.save(E / 'profile-hosted-qualified.json', result)
    print(json.dumps({'state': result['state'], 'operations': operations, 'streams': result['controller_streams'],
                      'retained_profile_files': {name: row['retained_files'] for name, row in rows.items()}, 'new_jobs': 0}))


if __name__ == '__main__':
    main()
