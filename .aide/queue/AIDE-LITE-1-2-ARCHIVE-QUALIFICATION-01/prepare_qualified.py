"""Freeze zero-job evidence closeout and guarded dev/main synchronization."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
BASE = '1806ec46d0342b2b3da9ddc49667e5c89ccbda10'
sys.dont_write_bytecode = True
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
    previous = json.loads((E / 'profile-hosted-effect.json').read_bytes())
    review = json.loads((E / 'qualification-closure-review.json').read_bytes())
    assert review['decision'] == 'ACCEPT' and not review['required_fixes']
    assert review['proposal_sha256'] == sha(E / 'qualification-closure-proposal.json')
    assert review['generator_sha256'] == sha(TASK / 'prepare_closure.py')
    final = json.loads((E / 'final-qualified.json').read_bytes())
    assert final['qualification_pass'] and final['subject']['commit'] == BASE
    assert final['scratch_absent'] and final['reservation_released']
    assert all(workspace.content_digest(Path(final['retained']) / n) == value for n, value in final['collected_manifest'].items())
    control, roots, _ = workspace.load_config(ROOT / '.aide.local/execution.json')
    assert workspace.digest(control) == previous['control_config_digest']
    assert workspace.dispatch_state(roots['control'])['mode'] == 'running' and not (roots['control'] / 'active.json').exists()
    dev, main = (git('rev-parse', r) for r in ('dev', 'main'))
    assert dev == git('rev-parse', 'origin/dev') == '52ddd31908ac96b3e891933a066936e72c90b137'
    assert main == git('rev-parse', 'origin/main') == previous['main_base']
    assets = previous['stable_assets']
    assert all(sha(ROOT / n) == value for n, value in assets.items())
    prior = json.loads((E / 'revised-dev-effect.json').read_bytes())
    canonical = prior['canonical_preimages']
    assert all(sha(ROOT / n) == value for n, value in canonical.items())
    parent = ROOT / '.aide/queue/AIDE-CONVERGENCE-AND-DELIVERY-01'
    assert 'current_state_sha256: ' + sha(parent / 'CURRENT.md') in (parent / 'status.yaml').read_text(encoding='utf-8')
    inputs = json.loads((E / 'final-inputs.json').read_bytes())
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    files = set(inputs['files']) | changed | {p.relative_to(ROOT).as_posix() for p in (ROOT / '.github/workflows').iterdir() if p.is_file()}
    inputs['files'] = {n: sha(ROOT / n) for n in sorted(files)}
    inputs['boundary'] = 'Local qualification/integration checkpoint inputs; no hosted dispatch or new native qualification.'
    save(E / 'qualified-integration-inputs.json', inputs)
    message = ('chore(lite): accept qualified candidate and share release evidence\n\n'
        '- Preserve exact final managed, brownfield, identity and replay passes with full lossless collection and original failures.\n'
        '- Record independent qualification acceptance for the exact candidate and bounded retained evidence; reconcile current docs, status and view digest.\n'
        '- Prepare guarded dev/main synchronization through the existing owner, exact source/range validation and matching task-local previews.\n\n'
        'Validation: PASS - independent candidate closure acceptance; final17th allocation retired;56primary forms and49ordinary forms per additional profile accounted for; exact replay and complete receipt roundtrips.\n'
        'Changelog: Changed: qualify Lite 1.2 candidate and reconcile current delivery evidence\n'
        'Risk: Lite 1.1 remains published; no support activation, tag, publication or acquired-byte acceptance is claimed.\n'
        'Follow-up: Separately admit publication and acquired-download acceptance; preserve active task checkpoints.\n'
        'AIDE-Task: AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01\nAIDE-Format: compact-v1\n')
    spec = importlib.util.spec_from_file_location('qualified_checkpoint_lite', ROOT / '.aide/scripts/aide_lite.py')
    lite = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lite
    spec.loader.exec_module(lite)
    assert not [c for c in lite.validate_commit_message_text(message) if c.severity == 'FAIL']
    (E / 'qualified-integration-message.txt').write_bytes(message.encode())
    helper = lite.make_git_helper_plan(ROOT, 'plan', dry_run=True)
    assert helper['status'] == 'blocked' and helper['blockers'] == ['dirty_tree_requires_classification']
    save(E / 'qualified-integration-prechecks.json', {'state': 'PASS_ZERO_JOB_PREPARATION', 'base': BASE,
        'helper_plan': helper, 'input_files': len(inputs['files']), 'parent_current_digest_verified': True,
        'new_jobs': 0, 'test_reruns': 0, 'archive_export_regenerations': 0})
    effect = {'base': dev, 'main_base': main, 'source_parent': BASE,
        'source_commits': git('rev-list', dev + '..' + BASE).splitlines(), 'task_branch': previous['task_branch'],
        'origin_url': previous['origin_url'], 'control_config_digest': previous['control_config_digest'],
        'controller_sha256': sha(TASK / 'sync_qualified.py'), 'attempt_directory': 'qualified-integration-attempt-01.log',
        'all_refs': {r.split()[1]: r.split()[0] for r in git('show-ref').splitlines()}, 'symbolic_refs': prior['symbolic_refs'],
        'stable_assets': assets, 'candidate_assets': json.loads((E / 'profile-build-result.json').read_bytes())['assets'],
        'canonical_preimages': canonical, 'maximum_additional_jobs': 0, 'maximum_new_integration_attempts': 1,
        'test_reruns': 0, 'export_regenerations': 0,
        'effects': ['One exact managed evidence/docs checkpoint after accepted native qualification; no product or frozen artifact change.',
            'Fresh shared locks,pause,ownership,input,origin,all-ref,source/range and helper checks precede dev then main fast-forwards and normal no-follow-tags pushes.',
            'Require matching task-local six-output previews for local/dev/main; preserve canonical previews and all assets/export bytes.',
            'Keep active local/important remote task branch and unrelated refs; retain every operation/stream and actual ref equality.'],
        'forbidden': ['new jobs,test reruns,hosted runs,export/archive regeneration,support activation,tags/publication',
            'branch retirement,force,pruning,hosting settings,other repositories/processes,models/providers/spending,roots/reserves/privileges']}
    save(E / 'qualified-integration-effect.json', effect)
    source, verdict = E / 'qualified-integration-source.json', E / 'qualified-integration-review.json'
    excluded = {p.relative_to(ROOT).as_posix() for p in (source, verdict)}
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    mapped = {n: sha(ROOT / n) for n in sorted(changed - excluded)}
    assert len(mapped) <= 256
    for name in mapped:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
        assert git('hash-object', '--no-filters', '--', name) == git('hash-object', '--path=' + name, '--', name), name
    git('diff', '--check')
    save(source, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': BASE,
        'effect_sha256': sha(E / 'qualified-integration-effect.json'), 'files': mapped})
    print(json.dumps({'source_sha256': sha(source), 'effect_sha256': sha(E / 'qualified-integration-effect.json'),
        'controller_sha256': effect['controller_sha256'], 'mapped_files': len(mapped), 'new_jobs': 0}))


if __name__ == '__main__':
    main()
