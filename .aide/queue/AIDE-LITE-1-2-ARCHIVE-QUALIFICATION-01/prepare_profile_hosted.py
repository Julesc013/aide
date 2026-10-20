"""Freeze one checkpoint/dev-sync/two-profile effect; preparation dispatches nothing."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
BASE = '79e2e8c91e6b34989dfb5224a944fd1874b0c6f7'
DEV = '03929beb3c7278975f9c0b3b1378712aeca2ac91'
MAIN = 'ed4a90046eba12a717a9962f21523285667a669b'
REMOTE_TASK = '4f85bb0c95ef7fc29667edd351346d684a80bb48'
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    assert not path.exists(), path
    path.write_bytes((json.dumps(data, indent=2) + '\n').encode())


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=30).strip()


def main():
    assert git('rev-parse', 'HEAD') == BASE and not git('diff', '--cached', '--name-only')
    old = json.loads((E / 'hosted-effect.json').read_bytes())
    dev_proof = json.loads((E / 'revised-dev-effect.json').read_bytes())
    for name in ('dev', 'origin/dev'):
        assert git('rev-parse', name) == DEV
    for name in ('main', 'origin/main'):
        assert git('rev-parse', name) == MAIN
    refs = {r.split()[1]: r.split()[0] for r in git('show-ref').splitlines()}
    assert refs['refs/remotes/origin/' + old['task_branch']] == REMOTE_TASK
    assert git('ls-remote', '--heads', 'origin', old['task_branch']).split() == [REMOTE_TASK, 'refs/heads/' + old['task_branch']]
    build = json.loads((E / 'profile-build-qualified.json').read_bytes())
    assert build['state'] == 'PASS_METADATA_BUILD_AND_COMPLETE_DELTA_ONLY'
    assert build['scratch_absent'] and build['reservation_released'] and build['local_jobs_consumed'] == 16
    assert all(workspace.content_digest(Path(build['retained']) / name) == value for name, value in build['collected_manifest'].items())
    reuse = json.loads((E / 'profile-macos-reuse-review.json').read_bytes())
    assert reuse['decision'] == 'ACCEPT' and not reuse['required_fixes']
    assert reuse['proposal_sha256'] == sha(E / 'profile-macos-reuse-proposal.json')
    amendment = json.loads((E / 'hosted-correction-amendment-review.json').read_bytes())
    assert amendment['decision'] == 'ACCEPT' and not amendment['required_fixes']
    assert amendment['amendment_sha256'] == sha(E / 'hosted-correction-amendment.md')
    config, roots, _ = workspace.load_config(ROOT / '.aide.local/execution.json')
    assert workspace.digest(config) == old['control_config_digest']
    assert workspace.dispatch_state(roots['control'])['mode'] == 'running' and not (roots['control'] / 'active.json').exists()
    pack = json.loads((E / 'revised-pack-subject.json').read_bytes())
    assert len(pack) == 879 and all(sha(ROOT / name) == value for name, value in pack.items())
    assets = {name: sha(ROOT / name) for name in old['stable_assets']}
    assert all(assets[name] == value['sha256'] and (ROOT / name).stat().st_size == value['size_bytes'] for name, value in build['assets'].items())
    baseline = json.loads((E / 'baseline.json').read_bytes())
    assert all(assets[name] == value for name, value in baseline['stable_assets'].items())
    canonical = dev_proof['canonical_preimages']
    assert all(sha(ROOT / name) == value for name, value in canonical.items())
    logs = E / 'profile-hosted-prechecks.log'
    prior_checks = E / 'profile-hosted-first-prechecks.json'
    commands = []
    if prior_checks.exists():
        # Only the controller guard, this preparation and the losslessly
        # normalized evidence projection changed. Product/check inputs did not.
        original = json.loads((E / 'profile-hosted-first-inputs.json').read_bytes())
        differences = {name for name, value in original['files'].items() if sha(ROOT / name) != value}
        assert differences == {(TASK / name).relative_to(ROOT).as_posix() for name in (
            'checkpoint_sync_and_host.py', 'prepare_profile_hosted.py', 'evidence/profile-hosted-initial-preparation-result.json')}
        commands = json.loads(prior_checks.read_bytes())['commands']
        assert len(commands) == 4 and all(c['exit_code'] == 0 for c in commands)
        assert all((logs / name).stat().st_size == value['bytes'] and sha(logs / name) == value['sha256']
                   for row in commands for name, value in row['streams'].items())
    else:
        logs.mkdir()
    for label, args in ([] if commands else [('doctor', ['doctor']), ('validate', ['validate']), ('pack-status', ['pack-status']), ('git-plan', ['git', 'plan'])]):
        paths = [logs / (label + suffix) for suffix in ('.stdout', '.stderr')]
        with paths[0].open('xb') as out, paths[1].open('xb') as err:
            result = subprocess.run([sys.executable, '-B', '.aide/scripts/aide_lite.py', *args], cwd=ROOT,
                stdin=subprocess.DEVNULL, stdout=out, stderr=err, timeout=90)
        commands.append({'label': label, 'exit_code': result.returncode,
            'streams': {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in paths}})
        assert result.returncode == 0, label
        if label == 'validate':
            text = paths[0].read_text(encoding='utf-8')
            assert 'status: PASS' in text and '; FAIL: 0;' in text
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    for name in changed:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
    inputs = json.loads((E / 'hosted-inputs.json').read_bytes())
    # No local configuration, self-hash cycles or unstaged hidden prerequisite.
    inputs['files'] = {name: sha(ROOT / name) for name in sorted(set(inputs['files']) | changed)}
    assert not any(name.startswith('.aide.local/') for name in inputs['files'])
    tracked = set(git('ls-files').splitlines())
    assert not set(inputs['files']) - tracked - changed
    inputs['actual_archive_subject'] = build['assets']
    inputs['boundary'] = 'Exact corrected actual-archive inputs; retained macOS observations keep their original subjects.'
    save(E / 'profile-hosted-inputs.json', inputs)
    message = ('test(lite): share candidate and finish hosted profiles\n\n'
        '- Preserve the metadata-only build, full delta and independently accepted macOS behavioral applicability under their original identities.\n'
        '- Select the corrected archive manifest and exactly Windows Server/Linux in the existing evaluator/workflow; retain every original assertion and failure.\n'
        '- Bind one checkpoint, guarded dev fast-forward/nonforce sync and one important task-branch push with bounded observation and complete collection.\n\n'
        'Validation: PASS - metadata build retired; 877 unchanged members; actual independent macOS applicability acceptance; preparation doctor/validate/pack-status and syntax checks. Fresh hosted execution and final local acceptance remain open.\n'
        'Changelog: Fixed: qualify corrected candidate metadata on remaining hosted profiles\n'
        'Risk: No support activation, main promotion or publication; original incomplete outcomes remain; controller/review usage unknown.\n'
        'Follow-up: Collect the two-profile run, then separately review the final affected local group and release replay.\n'
        'AIDE-Task: AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01\nAIDE-Format: compact-v1\n')
    spec = importlib.util.spec_from_file_location('profile_hosted_lite', ROOT / '.aide/scripts/aide_lite.py')
    lite = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lite
    spec.loader.exec_module(lite)
    assert not [c for c in lite.validate_commit_message_text(message) if c.severity == 'FAIL']
    (E / 'profile-hosted-message.txt').write_bytes(message.encode())
    save(E / 'profile-hosted-prechecks.json', {'state': 'PASS_PREPARATION_ONLY', 'base': BASE, 'commands': commands,
        'hosted_input_files': len(inputs['files']), 'checkout_availability': 'All pins tracked or exact checkpoint candidate.',
        'local_allocations_consumed': 16, 'export_refreshes_consumed': 2, 'hosted_runs_consumed': 1,
        'new_jobs_run': 0, 'new_pushes': 0, 'macos_applicability_review': sha(E / 'profile-macos-reuse-review.json'),
        'reused_prechecks_sha256': sha(prior_checks) if prior_checks.exists() else None})
    effect = {k: old[k] for k in ('task_branch', 'origin_url', 'control_config_digest', 'receipt_bounds', 'observer_provenance', 'observer_provenance_sha256')}
    effect.update(checkpoint_parent=BASE, dev_preimage=DEV, dev_base='EXACT_REVIEWED_CHECKPOINT', main_base=MAIN,
        task_remote_preimage=REMOTE_TASK, all_refs=refs, symbolic_refs=dev_proof['symbolic_refs'],
        source_commit='EXACT_REVIEWED_CHECKPOINT', source_commits=git('rev-list', DEV + '..' + BASE).splitlines(),
        canonical_preimages=canonical, controller_sha256=sha(TASK / 'checkpoint_sync_and_host.py'),
        observer_sha256=sha(TASK / 'observe_profile_hosted.py'), stable_assets=assets,
        package_inputs_sha256=sha(E / 'profile-hosted-inputs.json'), profiles=['windows-2025-x64', 'ubuntu-24.04-x64'],
        hosted_runs_before=1, maximum_new_hosted_runs=1, total_hosted_run_ceiling=2, jobs=2, total_hosted_job_ceiling=5,
        minutes_per_job=10, evaluator_deadline_seconds=480, observer_deadline_seconds=1200,
        maximum_local_allocations=0, maximum_export_refreshes=0, maximum_archive_rebuilds=0, live_model_requests=0,
        effects=['One exact task checkpoint, guarded dev-only fast-forward and normal no-follow-tags push after fresh locks, input/ref/origin/ownership checks, source/range validation and identical task-local previews.',
            'One nonforce update of the existing important task branch triggers exactly Windows Server/Linux in the existing hosted workflow.',
            'Code owns the bounded observer and complete raw collection; retain failures and consumed attempts without automatic retry.',
            'Preserve main, unrelated refs, all twelve assets, the export and six canonical previews; macOS is retained applicability, not a new execution.'],
        forbidden=['main promotion,pruning,force,tags,releases,artifact/cache uploads,hosting settings,support activation',
            'local allocations,export/archive/source regeneration,other repositories/processes,models/providers/spending,new roots,reserves,privileges'])
    save(E / 'profile-hosted-effect.json', effect)
    source_path, verdict_path = E / 'profile-hosted-source.json', E / 'profile-hosted-review.json'
    excluded = {p.relative_to(ROOT).as_posix() for p in (source_path, verdict_path)}
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    files = {name: sha(ROOT / name) for name in sorted(changed - excluded)}
    assert len(files) <= 256
    assert all(git('hash-object', '--no-filters', '--', name) == git('hash-object', '--path=' + name, '--', name)
               for name in files), 'raw/clean-filter identity mismatch before staging'
    git('diff', '--check')
    save(source_path, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': BASE,
        'effect_sha256': sha(E / 'profile-hosted-effect.json'), 'files': files})
    print(json.dumps({'source_sha256': sha(source_path), 'effect_sha256': sha(E / 'profile-hosted-effect.json'),
        'controller_sha256': effect['controller_sha256'], 'mapped_files': len(files), 'hosted_pins': len(inputs['files']), 'new_jobs': 0}))


if __name__ == '__main__':
    main()
