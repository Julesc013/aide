"""Freeze one necessary unpublished-candidate rebuild after the qualified shared-owner repair."""
import ast
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
BASE = '158a5cdcac7afecbc180a6324ea02e46617d1bc9'
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('revised_build_preparation_helpers', TASK / 'prepare_link.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def main():
    assert h.git('rev-parse', 'HEAD') == BASE
    assert h.git('branch', '--show-current') == 'task/aide-lite-1-2-archive-qualification-01'
    assert not h.git('diff', '--cached', '--name-only')
    qualified = json.loads((E / 'link-qualified-result.json').read_bytes())
    assert qualified['state'] == 'PASS_SHARED_OWNER_AND_OWNED_EXPORT'
    assert qualified['local_jobs_consumed'] == 14 and qualified['export_refreshes_consumed'] == 2
    assert qualified['scratch_absent'] and qualified['reservation_released']
    exported = json.loads((E / 'link-qualified-export.json').read_bytes())
    assert exported['source_commit'] == BASE and len(exported['members']) == 879
    pack_root = ROOT / '.aide/export/aide-lite-pack-v0'
    h.workspace.root_path(str(pack_root))
    members = {}
    for path in pack_root.rglob('*'):
        h.workspace.ordinary(path, directory=path.is_dir())
        if path.is_file():
            members[path.relative_to(pack_root).as_posix()] = h.sha(path)
    assert members == exported['members']
    pack = {'.aide/export/aide-lite-pack-v0/' + name: digest for name, digest in members.items()}
    h.save(E / 'revised-pack-subject.json', pack)
    before = {}
    for path in sorted((ROOT / '.aide/release').rglob('*')):
        h.workspace.ordinary(path, directory=path.is_dir())
        if path.is_file():
            before[path.relative_to(ROOT).as_posix()] = {'sha256': h.sha(path), 'size_bytes': path.stat().st_size}
    assert len(before) == 62
    h.save(E / 'revised-release-before.json', before)
    baseline = json.loads((E / 'link-baseline.json').read_bytes())
    assert all(h.sha(ROOT / name) == value for name, value in baseline['stable_assets'].items())
    candidate = json.loads((E / 'build-result.json').read_bytes())
    names = sorted(candidate['assets'])
    assert len(names) == 4 and all(h.sha(ROOT / name) == value['sha256'] for name, value in candidate['assets'].items())
    for name in names:
        assert h.git('hash-object', '--no-filters', '--', name) == h.git('rev-parse', baseline['original_candidate_checkpoint'] + ':' + name)
    prior = json.loads((E / 'link-corrected-effect.json').read_bytes())
    control, roots, _ = h.workspace.load_config(ROOT / '.aide.local/execution.json')
    qualification, _, working = h.workspace.load_config(ROOT / prior['qualification_config'])
    assert h.workspace.digest(control) == prior['control_config_digest']
    assert h.workspace.digest(qualification) == prior['qualification_config_digest']
    assert h.workspace.dispatch_state(roots['control'])['mode'] == 'running'
    assert not (roots['control'] / 'active.json').exists()
    job = json.loads((E / 'build-job-template.json').read_bytes())
    job['argv'] = [sys.executable, (TASK / 'run_revised_build.py').relative_to(ROOT).as_posix()]
    inputs = set(job['inputs']) | {job['argv'][1]} | {
        (E / name).relative_to(ROOT).as_posix() for name in
        ('build-result.json', 'link-baseline.json', 'revised-release-before.json', 'revised-pack-subject.json')}
    inputs.add(prior['qualification_config'])
    job['inputs'] = {name: h.sha(ROOT / name) for name in sorted(inputs)}
    h.save(E / 'revised-build-job-template.json', job)
    h.workspace.validate_job(dict(job, source_commit=BASE, source_tree=h.git('rev-parse', BASE + '^{tree}')), working)
    owner = h.load('revised_build_commit_owner', ROOT / '.aide/scripts/aide_lite.py')
    message = ('build(lite): checkpoint the qualified live-scan repair export\n\n'
        '- Retain the original candidate and failed attempts under their exact Git and evidence identities.\n'
        '- Preserve the demonstrated original-source false refusal, twenty passing regressions and second owned 879-file export.\n'
        '- Prepare one existing-owner unpublished 1.2 rebuild with complete ZIP/TAR inventories and explicit changed-member accounting.\n\n'
        'Validation: PASS - twenty corrected-source checks, original-source failure demonstration, exact collection/retirement, 879 export members, 12 preserved stable assets and build preflight; revised build pending\n'
        'Changelog: Fixed: qualify bounded live-scan re-observation and prepare the corrected Lite 1.2 candidate\n'
        'Risk: Earlier behavior evidence retains its original archive subject; reuse and revised operational qualification remain open.\n'
        'Follow-up: Review actual member deltas, affected consumers, hosted profiles and final replay before promotion/publication.\n'
        'AIDE-Task: AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01\nAIDE-Format: compact-v1\n')
    failures = [c.message for c in owner.validate_commit_message_text(message) if c.severity == 'FAIL']
    assert not failures, failures
    path = E / 'revised-build-message.txt'
    assert not path.exists()
    path.write_bytes(message.encode())
    h.save(E / 'revised-build-prechecks.json', {'status': 'PASS_STRUCTURAL_REVISED_BUILD_PRECHECK',
        'base': BASE, 'qualified_export_source': BASE, 'export_members': 879,
        'release_files_preserved_before_build': len(before), 'stable_assets_preserved': 12,
        'old_candidate_recoverable': baseline['original_candidate_checkpoint'],
        'job_inputs': len(inputs), 'job_preflight': 'PASS', 'new_jobs': 0, 'new_archives': 0})
    effect = {key: prior[key] for key in ('task_branch', 'origin_url', 'control_config_digest',
              'qualification_config', 'qualification_config_digest', 'expected_refs')}
    effect.update(base=BASE, controller_sha256=h.sha(TASK / 'commit_and_rebuild.py'),
        maximum_local_allocations=1, total_local_ceiling=16, local_jobs_already_consumed=14,
        maximum_hosted_runs=0, live_model_requests=0, expected_build_changes=names,
        effects=['One exact managed task checkpoint retains the qualified export and original/fixed attempt evidence.',
                 'One600second existing-runner allocation invokes existing stable-build and stable-validate for unpublished1.2 only.',
                 'Preserve original candidate bytes in their committed Git subject, every other release file and all879 export members.',
                 'Collect complete old/new ZIP/TAR path,type,mode,size,hash inventories; require only runner executable content and three derived metadata members to differ.',
                 'Bind exact source/config/job/receipt and retire quiescently; stop on any failure,no retry.'],
        forbidden=['export regeneration,oldasset/tag mutation,consumer rerun,hosted dispatch,integration,push,tag,publication or support activation',
                   'other repositories/processes,models/providers/spending,new roots,limits,reserves,configuration or privileges'],
        review_attestation={'path': (E / 'revised-build-review.json').relative_to(ROOT).as_posix(),
                            'actual_independent_accept_only': True, 'included_in_commit': True,
                            'binds': ['source_sha256', 'effect_sha256', 'controller_sha256']})
    h.save(E / 'revised-build-effect.json', effect)
    source_path, verdict = E / 'revised-build-source.json', E / 'revised-build-review.json'
    excluded = {source_path.relative_to(ROOT).as_posix(), verdict.relative_to(ROOT).as_posix()}
    changed = set(h.git('diff', '--name-only').splitlines()) | set(h.git('ls-files', '--others', '--exclude-standard').splitlines())
    files = {name: h.sha(ROOT / name) for name in sorted(changed - excluded)}
    for name in files:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
    h.git('diff', '--check')
    h.save(source_path, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': BASE,
        'effect_sha256': h.sha(E / 'revised-build-effect.json'), 'files': files,
        'qualification_state': 'Qualified source/export retained; necessary revised candidate build pending exact effect review.'})
    print(json.dumps({'source_sha256': h.sha(source_path), 'effect_sha256': h.sha(E / 'revised-build-effect.json'),
                      'controller_sha256': effect['controller_sha256'], 'mapped_files': len(files), 'new_jobs': 0}))


if __name__ == '__main__':
    main()
