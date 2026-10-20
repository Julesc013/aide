"""Bind retained macOS behavior to an actual metadata-only archive delta."""
import hashlib
import json
from pathlib import Path

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    before = json.loads((E / 'revised-build-result.json').read_bytes())
    after = json.loads((E / 'profile-build-result.json').read_bytes())
    delta = json.loads((E / 'profile-archive-member-delta.json').read_bytes())
    build = json.loads((E / 'profile-build-qualified.json').read_bytes())
    original = json.loads((E / 'hosted-qualified.json').read_bytes())
    row = original['profiles']['macos-15-arm64']
    assert row['status'] == 'PASS' and row['qualification_pass'] and row['fixture_retired']
    assert len(row['forms']) == 49 and len(row['cases']) == 2 and all(c['native_acceptance'] for c in row['cases'])
    assert build['state'] == 'PASS_METADATA_BUILD_AND_COMPLETE_DELTA_ONLY'
    assert build['scratch_absent'] and build['reservation_released']
    assert before['delivered_cli_sha256'] == after['delivered_cli_sha256']
    old_profile = next(p for p in before['identity']['profiles'] if p['profile_id'] == 'aide-lite-local-macos')
    new_profile = next(p for p in after['identity']['profiles'] if p['profile_id'] == 'aide-lite-local-macos')
    assert old_profile == new_profile and row['environment'] == old_profile['environment']
    for key in ('source_commit', 'source_tree', 'source_pack_checksums_sha256', 'predecessor_matrix', 'public_cli_forms', 'version_policy_sha256'):
        assert before['identity'][key] == after['identity'][key]
    for kind in ('zip', 'tar.gz'):
        part = delta['inventories'][kind]
        assert set(part['old']) == set(part['new']) and len(part['old']) == 879
        assert set(part['changed']) == {'aide-lite-pack-v0/stable-release.json', 'aide-lite-pack-v0/checksums.json'}
        assert all(value == part['new'][name] for name, value in part['old'].items() if name.startswith('aide-lite-pack-v0/files/'))
    assert all(sha(ROOT / name) == value['sha256'] for name, value in after['assets'].items())
    evidence = {'state': 'METADATA_ONLY_MACOS_APPLICABILITY_PENDING_REVIEW',
        'original_archive_assets': before['assets'], 'new_archive_assets': after['assets'],
        'original_run_id': original['run_id'], 'original_source_commit': original['source_commit'],
        'original_profile_evidence': row, 'preserved_profile': new_profile,
        'delta_path': (E / 'profile-archive-member-delta.json').relative_to(ROOT).as_posix(),
        'delta_sha256': sha(E / 'profile-archive-member-delta.json'),
        'actual_build_job': build['job_id'], 'actual_build_subject': build['subject'],
        'unchanged': ['all executable and installed payload bytes', 'Mac environment, capability and public-form declarations',
                      'predecessor bytes and scenarios', 'portable source/manifest provenance', 'archive member identities and modes outside two metadata leaves'],
        'changed_identity_effect': 'Whole-pack identity/checksum values differ. Old plans, receipts, feedback and ownership hashes remain old observations. They are not new-archive executions.',
        'dependency_reason': 'The two changed top-level metadata leaves are not installed project payloads. Safe import, context, task/git/review/quality/usage, repair, conflict/recovery and detach use the same payload and platform binding. Their identity comparisons derive from the supplied pack; old synthetic and real predecessor scenarios already exercise distinct pack identities. The Linux environment field does not select a macOS lifecycle branch.',
        'fresh_obligations': ['new primary installed identity/ownership and complete scratch replay',
                              'Windows Server and actual Linux full49-form execution',
                              'primary revised managed case6 and unfinished brownfield',
                              'release acceptance, publication and acquired-byte acceptance'],
        'scope': 'Behavioral applicability only. No new macOS execution, timing, resources, model use, containment, environment or universal support claim.'}
    path = E / 'profile-macos-reuse-proposal.json'
    data = (json.dumps(evidence, indent=2) + '\n').encode()
    assert not path.exists() or path.read_bytes() == data
    path.write_bytes(data)
    print(json.dumps({'state': evidence['state'], 'proposal_sha256': sha(path), 'original_forms': 49, 'unchanged_archive_members': 877}))


if __name__ == '__main__':
    main()
