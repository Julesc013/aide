"""Roundtrip all collected bytes and compose explicitly scoped behavioral coverage."""
import base64
import gzip
import hashlib
import json
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    assert not path.exists(), path
    path.write_bytes((json.dumps(value, indent=2) + '\n').encode())


def restore(path):
    value = json.loads(path.read_bytes())
    assert value['encoding'] == 'ordered-gzip+base64-json-chunks'
    raw = []
    for chunk in value['chunks']:
        part = E / chunk['path']
        assert sha(part) == chunk['sha256']
        item = json.loads(part.read_bytes())
        packed = base64.b64decode(item['data'], validate=True)
        assert hashlib.sha256(packed).hexdigest() == item['gzip_sha256']
        body = gzip.decompress(packed)
        assert len(body) == item['uncompressed_bytes'] == chunk['raw_bytes'] <= 1024 * 1024
        assert hashlib.sha256(body).hexdigest() == item['sha256'] == chunk['raw_sha256']
        raw.append(body)
    body = b''.join(raw)
    assert len(body) == value['raw_bytes'] and hashlib.sha256(body).hexdigest() == value['sha256']
    decoded = json.loads(body)
    assert len(decoded) == value['files']
    return {name: base64.b64decode(encoded, validate=True) for name, encoded in decoded.items()}


def main():
    observed = json.loads((E / 'profile-hosted-observed.json').read_bytes())
    qualified = json.loads((E / 'profile-hosted-qualified.json').read_bytes())
    execution = json.loads((E / 'profile-hosted-execution.log').read_bytes())
    build = json.loads((E / 'profile-build-result.json').read_bytes())
    assert qualified['qualification_pass'] and observed['qualification_pass']
    counts = {}
    for label in ('controller', 'windows-2025-x64', 'ubuntu-24.04-x64'):
        path = E / ('profile-hosted-' + label + '-retained.json')
        files = restore(path)
        for name, raw in files.items():
            original = E / name if label == 'controller' else E / 'profile-hosted-logs.log' / label / name
            assert original.read_bytes() == raw
        counts[label] = len(files)
        if label != 'controller':
            result = json.loads(files['release-result.json'])
            assert result['assets'] == build['assets'] and result['status'] == 'PASS'
            assert result['fixture_retired'] and result['source_commit'] == qualified['source_commit']
    review = json.loads((E / 'profile-macos-reuse-review.json').read_bytes())
    assert review['decision'] == 'ACCEPT' and not review['required_fixes']
    assert review['proposal_sha256'] == sha(E / 'profile-macos-reuse-proposal.json')
    old = json.loads((E / 'hosted-qualified.json').read_bytes())
    mac = old['profiles']['macos-15-arm64']
    assert mac['qualification_pass'] and mac['fixture_retired']
    profiles = {name: {'method': 'fresh_actual_archive_execution', 'run_id': qualified['run_id'],
        'source_commit': qualified['source_commit'], 'assets': build['assets'],
        'evidence': 'evidence/profile-hosted-qualified.json', 'evidence_sha256': sha(E / 'profile-hosted-qualified.json'),
        'forms': len(row['forms']), 'predecessor_scenarios': len(row['cases']), 'fixture_retired': row['fixture_retired']}
        for name, row in qualified['profiles'].items()}
    profiles['macos-15-arm64'] = {'method': 'retained_behavioral_applicability', 'original_run_id': old['run_id'],
        'original_source_commit': old['source_commit'], 'original_assets': json.loads((E / 'revised-build-result.json').read_bytes())['assets'],
        'applies_to_assets': build['assets'], 'original_evidence': 'evidence/hosted-qualified.json',
        'original_evidence_sha256': sha(E / 'hosted-qualified.json'), 'review': 'evidence/profile-macos-reuse-review.json',
        'review_sha256': sha(E / 'profile-macos-reuse-review.json'), 'forms': len(mac['forms']),
        'predecessor_scenarios': len(mac['cases']), 'fixture_retired': True,
        'boundary': 'Original observations, receipts, plans, ownership hashes, times and resources retain their original identities. No new macOS execution.'}
    coverage = {'state': 'SCOPED_BEHAVIORAL_COVERAGE_COMPLETE_PRIMARY_IDENTITY_AND_FINAL_GROUP_REQUIRED',
        'behavioral_coverage_pass': True, 'assets': build['assets'], 'profiles': profiles,
        'fresh_primary_identity_required': True, 'release_accepted': False, 'support_activated': False,
        'remaining': ['affected original managed case6', 'primary unfinished published-upgrade brownfield',
                      'fresh revised primary identity/ownership', 'complete release replay and final acceptance'],
        'local_jobs_consumed': 16, 'local_job_ceiling': 17, 'hosted_runs_consumed': 2,
        'hosted_run_ceiling': 2, 'hosted_jobs_consumed': 5, 'export_refreshes_consumed': 2}
    save(E / 'profile-coverage.json', coverage)
    times = {j['name']: (datetime.fromisoformat(j['completed_at'].replace('Z', '+00:00')) -
             datetime.fromisoformat(j['started_at'].replace('Z', '+00:00'))).total_seconds() for j in execution['jobs']}
    verified = {'state': 'PASS_LOSSLESS_ROUNDTRIP', 'files': counts, 'controller_operations': qualified['controller_operations'],
        'controller_streams': qualified['controller_streams'], 'run_id': qualified['run_id'],
        'coverage_sha256': sha(E / 'profile-coverage.json'), 'hosted_whole_job_seconds': times,
        'timing_boundary': 'Whole hosted jobs include setup and all49forms/bothscenarios; not primary-local timing guarantees.',
        'new_jobs': 0, 'worker_model_requests': 0, 'whole_model_usage': 'unknown'}
    save(E / 'profile-hosted-collection-verified.json', verified)
    print(json.dumps(verified))


if __name__ == '__main__':
    main()
