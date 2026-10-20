"""Verify all terminal hosted receipts, preserving passes and incomplete profiles."""
import base64
import hashlib
import gzip
import importlib.util
import json
from pathlib import Path

ROOT = Path.cwd()
TASK = Path(__file__).parent
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
    checkpoint = json.loads((E / 'hosted-checkpoint.log').read_bytes())
    observation = json.loads((E / 'hosted-execution.log').read_bytes())
    summary = json.loads((E / 'hosted-observed.json').read_bytes())
    assert checkpoint['state'] == 'hosted_observed' and checkpoint['commit']['status'] == 'COMMITTED'
    assert observation['state'] == 'observed_terminal'
    commit = checkpoint['commit']['candidate_commit']
    assert commit == observation['source_commit'] == summary['source_commit'] == '4f85bb0c95ef7fc29667edd351346d684a80bb48'
    assert observation['run_id'] == summary['run_id'] == 39456159304
    assert sha(E / 'hosted-observed.json') == observation['summary_sha256']
    assert summary['workflow_conclusion'] == 'failure' and not summary['qualification_pass']
    controller_files = {}
    operations = 0
    for record, folder in ((checkpoint, E / 'hosted-checkpoint-streams.log'), (observation, E / 'hosted-logs.log')):
        for row in record['operations']:
            assert row['state'] == 'completed' and row['exit_code'] == 0
            operations += 1
            for name, expected in row['streams'].items():
                path = folder / name
                assert path.stat().st_size == expected['bytes'] and sha(path) == expected['sha256']
                key = folder.name + '/' + name
                assert key not in controller_files
                controller_files[key] = base64.b64encode(path.read_bytes()).decode('ascii')
    for name in ('hosted-checkpoint.log', 'hosted-execution.log', 'hosted-observed.json'):
        controller_files[name] = base64.b64encode((E / name).read_bytes()).decode('ascii')
    preserve(E / 'hosted-controller-retained.json', controller_files)
    rows = {}
    for profile in ('windows-2025-x64', 'ubuntu-24.04-x64', 'macos-15-arm64'):
        folder = E / 'hosted-logs.log' / profile
        files = {p.name: p.read_bytes() for p in folder.iterdir() if p.is_file()}
        index = json.loads(files['receipt-index.json'])
        assert set(index) == set(files) - {'receipt-index.json'}
        for name, expected in index.items():
            assert {'bytes': len(files[name]), 'sha256': hashlib.sha256(files[name]).hexdigest()} == expected
        result = json.loads(files['release-result.json'])
        assert result['source_commit'] == commit and not result['support_claimed'] and result['model_requests'] == 0
        encoded = {name: base64.b64encode(raw).decode('ascii') for name, raw in files.items()}
        path = E / ('hosted-' + profile + '-retained.json')
        preserve(path, encoded)
        row = {'status': result['status'], 'qualification_pass': summary['profiles'][profile]['qualification_pass'],
               'environment': result['environment'], 'declared_environment': result['declared_environment'],
               'receipt_bundle': path.relative_to(ROOT).as_posix(), 'receipt_bundle_sha256': sha(path),
               'retained_files': len(files), 'receipt_index_sha256': hashlib.sha256(files['receipt-index.json']).hexdigest(),
               'forms': result.get('forms', []), 'cases': result.get('cases', []),
               'fixture_retired': result['fixture_retired'], 'error_type': result.get('error_type'), 'error': result.get('error')}
        if profile == 'macos-15-arm64':
            assert row['qualification_pass'] and row['status'] == 'PASS' and row['fixture_retired']
            assert len(row['forms']) == 49 and len(row['cases']) == 2 and all(c['native_acceptance'] for c in row['cases'])
        elif profile == 'ubuntu-24.04-x64':
            assert row['error'] == 'host tuple changed; no implicit profile substitution' and not row['forms']
            row['fixture_disposition'] = 'not allocated: exact environment gate precedes mkdtemp in frozen evaluator'
        else:
            assert row['fixture_retired'] and 'ordinary-validate.stdout' in files
            text = files['ordinary-validate.stdout'].decode('utf-8')
            assert '\r\n' in text and 'status: PASS\r\n' in text and 'checks: 27; PASS: 25; WARN: 2; FAIL: 0; OTHER: 0\r\n' in text
            row['classification'] = 'wrapper regex rejects CRLF, not a product validation failure'
            row['partial_successful_commands'] = [n for n in index if n.endswith('.json') and isinstance(json.loads(files[n]), dict)
                and json.loads(files[n]).get('exit_code') == 0 and 'argv' in json.loads(files[n])]
        rows[profile] = row
    effect = json.loads((E / 'hosted-effect.json').read_bytes())
    assert all(sha(ROOT / name) == expected for name, expected in effect['stable_assets'].items())
    result = {'state': 'MACOS_PASS_LINUX_ENVIRONMENT_CHANGED_WINDOWS_WRAPPER_INCOMPLETE',
        'source_commit': commit, 'run_id': summary['run_id'], 'run_url': summary['run_url'],
        'qualification_pass': False, 'profiles': rows, 'controller_operations': operations,
        'controller_streams': len(controller_files) - 3, 'hosted_runs_consumed': 1, 'hosted_run_ceiling': 1,
        'local_allocations_consumed': 15, 'local_allocation_ceiling': 16, 'export_refreshes_consumed': 2,
        'support_claimed': False, 'worker_model_requests': 0, 'whole_model_usage': 'unknown',
        'next_boundary': 'No automatic retry. Preserve macOS and partial successes. A finite independently reviewed environment-metadata/wrapper correction is required before new effects.'}
    h.save(E / 'hosted-qualified.json', result)
    print(json.dumps({'state': result['state'], 'operations': operations, 'streams': result['controller_streams'],
                      'retained_profile_files': {name: row['retained_files'] for name, row in rows.items()}, 'new_jobs': 0}))


if __name__ == '__main__':
    main()
