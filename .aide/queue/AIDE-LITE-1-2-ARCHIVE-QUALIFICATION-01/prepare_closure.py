"""Compose exact qualification evidence without relabelling retained observations."""
import hashlib
import json
from pathlib import Path

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    built = json.loads((E / 'profile-build-result.json').read_bytes())
    final = json.loads((E / 'final-qualified.json').read_bytes())
    coverage = json.loads((E / 'profile-coverage.json').read_bytes())
    assert final['qualification_pass'] and final['lossless_roundtrip_verified']
    assert final['scratch_absent'] and final['reservation_released']
    assert final['local_jobs_consumed'] == 17 and final['hosted_runs_consumed'] == 2
    assert coverage['behavioral_coverage_pass'] and coverage['assets'] == built['assets']
    proof_names = ['revised-behavior-reuse-proposal.json', 'revised-behavior-reuse-review.json',
        'profile-macos-reuse-proposal.json', 'profile-macos-reuse-review.json', 'profile-archive-member-delta.json',
        'profile-build-qualified.json', 'profile-coverage.json', 'profile-hosted-qualified.json',
        'profile-hosted-collection-verified.json', 'current-cli-coverage.json', 'final-qualified.json',
        'final-managed-result.json', 'final-brownfield-result.json', 'final-replay-result.json', 'final-primary_identity-result.json']
    for name in ('revised-behavior-reuse-review.json', 'profile-macos-reuse-review.json'):
        review = json.loads((E / name).read_bytes())
        assert review['decision'] == 'ACCEPT' and not review['required_fixes']
    old_revised = json.loads((E / 'revised-build-result.json').read_bytes())
    old_windows = next(p for p in old_revised['identity']['profiles'] if p['profile_id'] == 'aide-lite-local-windows')
    new_windows = next(p for p in built['identity']['profiles'] if p['profile_id'] == 'aide-lite-local-windows')
    assert old_windows == new_windows
    assert built['delivered_cli_sha256'] == old_revised['delivered_cli_sha256']
    forms = json.loads((E / 'current-cli-coverage.json').read_bytes())['forms']
    assert len(forms) == len({f['form'] for f in forms}) == 56
    assert set(new_windows['supported_cli_forms']) == {f['form'] for f in forms}
    retained = Path(final['retained'])
    witnesses = []
    for row in forms:
        old = row['evidence']
        if old['job_id'] == '282e45c890d04122bbe30e1b96d0f837':
            name = 'output/managed/' + old['member'].removeprefix('output/')
            path = retained / name
            command = json.loads(path.read_bytes())
            assert command['exit_code'] == old['exit_code']
            witnesses.append({'form': row['form'], 'method': 'fresh_affected_original_case6',
                'job_id': final['job_id'], 'subject': final['subject'], 'assets': built['assets'],
                'bundle': 'evidence/final-job-retained.json', 'member': name, 'member_sha256': sha(path),
                'actual_argv': command['argv'], 'exit_code': command['exit_code']})
        else:
            witnesses.append({'form': row['form'], 'method': 'retained_behavioral_applicability',
                'original_observation': old, 'original_assets': json.loads((E / 'current-cli-coverage.json').read_bytes())['subject_assets'],
                'applies_to_assets': built['assets'], 'reason': 'Accepted dependency envelope plus executable/payload-identical metadata correction; Windows profile unchanged; fresh identity/ownership and exact replay now passed.'})
    assert sum(w['method'] == 'fresh_affected_original_case6' for w in witnesses) == 10
    assert sum(w['method'] == 'retained_behavioral_applicability' for w in witnesses) == 46
    for name, value in built['assets'].items():
        assert sha(ROOT / name) == value['sha256'] and (ROOT / name).stat().st_size == value['size_bytes']
    result = {'state': 'EXACT_QUALIFICATION_CLOSURE_PENDING_INDEPENDENT_REVIEW', 'assets': built['assets'],
        'payload_source': built['identity']['source_commit'], 'profiles': built['identity']['profiles'],
        'proofs': {name: {'path': (E / name).relative_to(ROOT).as_posix(), 'sha256': sha(E / name)} for name in proof_names},
        'primary_form_witnesses': witnesses, 'additional_profiles': coverage['profiles'],
        'final_group': {'job_id': final['job_id'], 'subject': final['subject'], 'manifest_digest': final['manifest_digest'],
            'phases': final['phases'], 'scratch_absent': True, 'reservation_released': True},
        'closure_reason': 'All fresh obligations in the accepted dependency proof are now met: changed managed owner/case6, exact current identity/ownership, unfinished primary brownfield and complete release replay. The later correction changes only top-level metadata/checksums; executable/installed payload and Windows/macOS profiles are unchanged. Retained observations stay bound to their original source/assets/times.',
        'retained_fresh_predecessor': 'Original primary fresh scenario remains an old-subject behavioral observation under the accepted dependency proof; fresh revised identity/detach and both current WindowsServer/Linux predecessor scenarios supplement it. No new primary fresh full-scenario execution is claimed.',
        'acceptance_requested': 'Exact candidate qualification and transitive retained-behavior applicability only; prepare reviewed integration and separate publication/acquired-byte task.',
        'limits': ['Exact CPython3.14.8/profile tuples only;56primary forms,49additional-profile ordinary forms;seven additional-profile managed forms remain unqualified.',
            'Cooperative POSIX mutation ownership; no outer-client read/write containment or OS network-isolation claim.',
            'No generic native legacy/IDE/runtime/model/provider/whole-outcome-efficiency qualification.',
            'Historical cross-path rollback/refusal and retained-state recovery limits remain.',
            'Original interrupted, failed and successful attempts preserve their identities; no all-green parent run is fabricated.'],
        'local_jobs_consumed': 17, 'hosted_runs_consumed': 2, 'hosted_jobs_consumed': 5, 'export_refreshes_consumed': 2,
        'worker_model_requests': 0, 'whole_model_usage': 'unknown', 'support_activated': False, 'published': False}
    path = E / 'qualification-closure-proposal.json'
    assert not path.exists()
    path.write_bytes((json.dumps(result, indent=2) + '\n').encode())
    print(json.dumps({'proposal_sha256': sha(path), 'generator_sha256': sha(Path(__file__)),
        'forms': len(witnesses), 'fresh': 10, 'retained': 46, 'new_jobs': 0}))


if __name__ == '__main__':
    main()
