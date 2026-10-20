"""Freeze branch-only publication admission, retaining exact completed work."""
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
QUAL = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'
BASE = '3fec7ac375da0e17f035336e080d75ebd26a9920'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    assert not path.exists(), path
    path.write_bytes((json.dumps(value, indent=2) + '\n').encode())


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=30).strip()


def main():
    assert git('rev-parse', 'HEAD') == BASE and not git('diff', '--cached', '--name-only')
    for ref in ('dev', 'main', 'origin/dev', 'origin/main'):
        assert git('rev-parse', ref) == BASE
    previous = json.loads((QUAL / 'evidence/qualified-integration-effect.json').read_bytes())
    integrated = json.loads((QUAL / 'evidence/qualified-integration-verified.json').read_bytes())
    assert integrated['status'] == 'PASS_VERIFIED_DEV_MAIN_SYNC' and integrated['commit'] == BASE
    assert integrated['lossless_roundtrip_verified'] and integrated['operations'] == 165 and integrated['streams'] == 330
    closure = json.loads((QUAL / 'evidence/qualification-closure-review.json').read_bytes())
    assert closure['decision'] == 'ACCEPT' and not closure['required_fixes']
    assert closure['proposal_sha256'] == sha(QUAL / 'evidence/qualification-closure-proposal.json')
    assets = previous['stable_assets']
    assert all(sha(ROOT / name) == value for name, value in assets.items())
    pack = json.loads((QUAL / 'evidence/revised-pack-subject.json').read_bytes())
    assert len(pack) == 879 and all(sha(ROOT / name) == value for name, value in pack.items())
    config, roots, _ = workspace.load_config(ROOT / '.aide.local/execution.json')
    assert workspace.digest(config) == previous['control_config_digest']
    assert workspace.dispatch_state(roots['control'])['mode'] == 'running' and not (roots['control'] / 'active.json').exists()
    branch = 'task/aide-lite-1-2-publication-01'
    assert git('branch', '--show-current') == previous['task_branch']
    assert not git('branch', '--list', branch) and not git('ls-remote', '--heads', 'origin', branch)
    baseline = {'base': BASE, 'stable_assets': assets, 'export_files': pack,
        'qualification_proposal_sha256': closure['proposal_sha256'],
        'qualification_review_sha256': sha(QUAL / 'evidence/qualification-closure-review.json'),
        'integration_verified_sha256': sha(QUAL / 'evidence/qualified-integration-verified.json'),
        'candidate_assets': json.loads((QUAL / 'evidence/profile-build-result.json').read_bytes())['assets'],
        'qualification_budget': {'local_allocations': 17, 'exports': 2, 'hosted_runs': 2, 'hosted_jobs': 5},
        'new_publication_consumer_budget': 1, 'new_effects_run': 0}
    save(E / 'baseline.json', baseline)
    logs = E / 'admission-prechecks.log'
    logs.mkdir()
    commands = []
    for label, argv in [('doctor', ['doctor']), ('validate', ['validate']), ('pack-status', ['pack-status'])]:
        paths = [logs / (label + suffix) for suffix in ('.stdout', '.stderr')]
        with paths[0].open('xb') as out, paths[1].open('xb') as err:
            result = subprocess.run([sys.executable, '-B', '.aide/scripts/aide_lite.py', *argv], cwd=ROOT,
                stdin=subprocess.DEVNULL, stdout=out, stderr=err, timeout=120)
        commands.append({'label': label, 'exit_code': result.returncode,
            'streams': {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in paths}})
        assert result.returncode == 0, label
    spec = importlib.util.spec_from_file_location('publication_admission_lite', ROOT / '.aide/scripts/aide_lite.py')
    lite = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lite
    spec.loader.exec_module(lite)
    helper = lite.make_git_helper_plan(ROOT, 'plan', dry_run=True)
    assert helper['status'] == 'blocked' and helper['blockers'] == ['dirty_tree_requires_classification']
    save(E / 'admission-prechecks.json', {'state': 'PASS_PREPARATION_ONLY', 'commands': commands,
        'helper_plan': helper, 'qualified_source_integrated': BASE, 'new_jobs': 0, 'new_branches': 0,
        'new_tags_releases_downloads': 0})
    effect = {'base': BASE, 'from_branch': previous['task_branch'], 'task_branch': branch,
        'origin_url': previous['origin_url'], 'control_config_digest': previous['control_config_digest'],
        'controller_sha256': sha(TASK / 'admit.py'), 'preserved_refs': git('show-ref').splitlines(),
        'maximum_new_local_branches': 1, 'maximum_local_allocations': 0, 'maximum_hosted_runs': 0,
        'maximum_pushes': 0, 'maximum_tags_releases_downloads': 0,
        'effects': ['Create only the named local publication task branch from the already integrated base in the sole existing checkout.',
            'Carry only exact reviewed dirty preparation/closeout bytes; preserve current archive task branch and every existing ref.',
            'Fresh shared locks,pause,ownership,source,asset,ref,origin and helper checks; retain all command streams and stop on uncertainty.'],
        'forbidden': ['checkpoint,push,merge,promotion,pruning,tag,release,download,job,hosted run,export/archive generation',
            'product changes,support activation,other targets/processes,credentials,models/providers/spending,roots/reserves/privileges']}
    save(E / 'admission-effect.json', effect)
    source, verdict = E / 'admission-source.json', E / 'admission-review.json'
    excluded = {p.relative_to(ROOT).as_posix() for p in (source, verdict)}
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    mapped = {name: sha(ROOT / name) for name in sorted(changed - excluded)}
    assert len(mapped) <= 256
    for name in mapped:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
        assert git('hash-object', '--no-filters', '--', name) == git('hash-object', '--path=' + name, '--', name), name
    git('diff', '--check')
    save(source, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': BASE,
        'effect_sha256': sha(E / 'admission-effect.json'), 'files': mapped})
    print(json.dumps({'source_sha256': sha(source), 'effect_sha256': sha(E / 'admission-effect.json'),
        'controller_sha256': effect['controller_sha256'], 'mapped_files': len(mapped), 'new_effects': 0}))


if __name__ == '__main__':
    main()
