"""Freeze exact source and finite publication effects; no Git/network/job mutations."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
QE = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/evidence'
BASE = '3fec7ac375da0e17f035336e080d75ebd26a9920'
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    assert not path.exists(), path
    path.write_bytes((json.dumps(value, indent=2) + '\n').encode('utf-8'))


def git(*argv):
    return subprocess.check_output(['git', *argv], cwd=ROOT, text=True, timeout=30).strip()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    assert git('rev-parse', 'HEAD') == BASE and git('branch', '--show-current') == 'task/aide-lite-1-2-publication-01'
    assert not git('diff', '--cached', '--name-only')
    baseline = json.loads((E / 'baseline.json').read_bytes())
    assert all(sha(ROOT / name) == value for name, value in (baseline['stable_assets'] | baseline['export_files']).items())
    assert json.loads((QE / 'qualification-closure-review.json').read_bytes())['decision'] == 'ACCEPT'
    prior = json.loads((QE / 'qualified-integration-effect.json').read_bytes())
    config, roots, _ = workspace.load_config(ROOT / '.aide.local/execution.json')
    assert workspace.digest(config) == prior['control_config_digest']
    assert workspace.dispatch_state(roots['control'])['mode'] == 'running' and not (roots['control'] / 'active.json').exists()
    build = json.loads((QE / 'profile-build-result.json').read_bytes())
    save(E / 'release-selection.json', {'version': '1.2.0', 'tag': 'aide-lite-v1.2.0',
        'archive_source': build['identity']['source_commit'], 'archive_tree': build['identity']['source_tree'],
        'assets': build['assets'], 'qualification_review_sha256': sha(QE / 'qualification-closure-review.json'),
        'qualification_proposal_sha256': sha(QE / 'qualification-closure-proposal.json')})
    labels = {'zip': 'Portable package - ZIP', 'tar.gz': 'Portable package - TAR.GZ',
        'manifest.json': 'Release manifest', 'SHA256SUMS.txt': 'SHA-256 checksums'}
    assets = {}
    for path, identity in build['assets'].items():
        name = Path(path).name
        suffix = name.removeprefix('aide-lite-v1.2.0.')
        assets[name] = dict(identity, path=path, label=labels[suffix])
    presentation = load('publication_projection', ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-PUBLICATION-01/update_presentation.py')
    previous = json.loads((E / 'next-preparation.log/releases.json').read_bytes())
    assert {r['tag_name'] for r in previous} == {'aide-lite-v1.0.0', 'aide-lite-v1.1.0'}
    gh = Path(shutil.which('gh')).resolve(strict=True)
    all_refs = {line.split()[1]: line.split()[0] for line in git('show-ref').splitlines()}
    symbolic = prior['symbolic_refs']
    variable = {'refs/heads/dev', 'refs/heads/main', 'refs/remotes/origin/dev', 'refs/remotes/origin/main',
        'refs/heads/task/aide-lite-1-2-publication-01'} | set(symbolic)
    preserved = {k: v for k, v in all_refs.items() if k not in variable}
    remote_refs = dict(line.split()[::-1] for line in git('ls-remote', '--heads', '--tags', 'origin').splitlines())
    assert remote_refs['refs/heads/dev'] == remote_refs['refs/heads/main'] == BASE
    assert not any('aide-lite-v1.2.0' in ref or ref == 'refs/heads/task/aide-lite-1-2-publication-01' for ref in remote_refs)
    remote_refs = {k: v for k, v in remote_refs.items() if k not in {'refs/heads/dev', 'refs/heads/main'}}
    files = baseline['stable_assets'] | baseline['export_files']
    for name in ('acquire.py', 'deliver.py', 'checkpoint.py', 'run_acquired_consumer.py', 'release-notes.md', 'tag-message.txt', 'evidence/release-selection.json'):
        path = TASK / name
        files[path.relative_to(ROOT).as_posix()] = sha(path)
    delivery = {'base': BASE, 'qualification': BASE, 'task_branch': 'task/aide-lite-1-2-publication-01',
        'task_remote_before': None, 'remote_url': prior['origin_url'], 'config_digest': workspace.digest(config),
        'controller_sha256': sha(TASK / 'deliver.py'), 'python_sha256': sha(Path(sys.executable)),
        'gh_executable': str(gh), 'gh_sha256': sha(gh), 'files': files, 'assets': assets,
        'preserved_local_refs': preserved, 'preserved_remote_refs': remote_refs,
        'previous_releases': [presentation.projection(r) for r in previous],
        'support_activation': 'exact_four_declared_T3_L1_companion_profiles_only',
        'effects': ['Use the exact successful reviewed pre-tag checkpoint from the adjacent checkpoint receipt, already synced to dev/main.',
            'One new annotated aide-lite-v1.2.0 tag, normal no-follow-tags push, one draft created/discovered by ID, four exact labelled uploads, verified stable/latest publication.',
            'Acquire four exact public assets once, bounded180s/4MiB, exclusive writes, approved HTTPS redirects; retain partial evidence and stop on uncertain effects.'],
        'forbidden': ['force/retag/asset clobber/rebuild/export refresh/qualification restart/provider spending/other repositories or processes',
            'new task remote branch, automatic retries, model jobs or consumer allocation from delivery alone'],
        'deadline_seconds': 900, 'new_releases': 1, 'new_assets': 4}
    save(E / 'delivery-effect.json', delivery)
    old_inputs = json.loads((QE / 'qualified-integration-inputs.json').read_bytes())
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    inputs = {'files': {n: sha(ROOT / n) for n in sorted(set(old_inputs['files']) | changed)},
        'boundary': 'Shared source identities and immutable qualification evidence; no product, export, build or job effect.'}
    save(E / 'publication-checkpoint-inputs.json', inputs)
    message = ('chore(lite): prepare qualified 1.2 publication and exact platform notes\n\n'
        '- Preserve completed qualification/dev/main and branch-admission receipts with lossless roundtrip verification.\n'
        '- Reconcile README, docs, TODO, plans, roadmap, changelog and the release-policy status paragraph before tagging.\n'
        '- Adapt existing release owners for four immutable labelled assets, both preserved predecessors and bounded public acquisition.\n\n'
        'Validation: PASS - accepted exact archive qualification and input hashes; pre-tag source checks and strict known-warning classification; original failures retained.\n'
        'Changelog: Changed: prepare Lite 1.2 modern companion release, adoption/exit and staged native-product documentation\n'
        'Risk: Publication and acquired-byte consumer remain pending; exact profiles do not imply legacy native or IDE parity.\n'
        'Follow-up: Execute only exact independently accepted publication/acquisition effects, then one original acquired-byte consumer.\n'
        'AIDE-Task: AIDE-LITE-1-2-PUBLICATION-01\nAIDE-Format: compact-v1\n')
    (E / 'publication-checkpoint-message.txt').write_bytes(message.encode('utf-8'))
    lite = load('publication_freeze_lite', ROOT / '.aide/scripts/aide_lite.py')
    assert not [c for c in lite.validate_commit_message_text(message) if c.severity == 'FAIL']
    logs = E / 'pre-tag-checks.log'
    logs.mkdir()
    checks = {}
    for label, argv in [('doctor', ['doctor']), ('validate', ['validate']), ('pack-status', ['pack-status'])]:
        out, err = logs / (label + '.stdout'), logs / (label + '.stderr')
        with out.open('xb') as stdout, err.open('xb') as stderr:
            result = subprocess.run([sys.executable, '-B', '.aide/scripts/aide_lite.py', *argv], cwd=ROOT,
                stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=120)
        checks[label] = {'exit_code': result.returncode, 'stdout_sha256': sha(out), 'stderr_sha256': sha(err),
            'stdout': out.read_text(encoding='utf-8'), 'stderr': err.read_text(encoding='utf-8')}
        assert result.returncode == 0, checks[label]
    owner = load('publication_check_owner', TASK / 'checkpoint.py')
    owner.validate_source_output(checks['validate']['stdout'])
    assert 'status: PASS' in checks['doctor']['stdout'] and 'PASS' in checks['pack-status']['stdout']
    save(E / 'pre-tag-checks.json', checks)
    effect = {'base': BASE, 'main_base': BASE, 'source_parent': BASE, 'qualification_source': '1806ec46d0342b2b3da9ddc49667e5c89ccbda10',
        'source_commits': [], 'task_branch': delivery['task_branch'], 'origin_url': prior['origin_url'],
        'control_config_digest': workspace.digest(config), 'controller_sha256': sha(TASK / 'checkpoint.py'),
        'attempt_directory': 'publication-checkpoint-attempt-01.log', 'all_refs': all_refs, 'symbolic_refs': symbolic,
        'stable_assets': baseline['stable_assets'], 'candidate_assets': build['assets'], 'canonical_preimages': prior['canonical_preimages'],
        'effects': ['One exact managed pre-tag docs/evidence checkpoint; existing guarded dev/main FF/nonforce sync and identical task-local six-output previews.'],
        'maximum_additional_jobs': 0, 'maximum_new_integration_attempts': 1, 'test_reruns': 0, 'export_regenerations': 0}
    save(E / 'publication-checkpoint-effect.json', effect)
    source, review = E / 'publication-checkpoint-source.json', E / 'publication-checkpoint-review.json'
    excluded = {p.relative_to(ROOT).as_posix() for p in (source, review)}
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    mapped = {n: sha(ROOT / n) for n in sorted(changed - excluded)}
    for name in mapped:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
        assert git('hash-object', '--no-filters', '--', name) == git('hash-object', '--path=' + name, '--', name), name
    git('diff', '--check')
    save(source, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': BASE,
        'effect_sha256': sha(E / 'publication-checkpoint-effect.json'), 'files': mapped})
    print(json.dumps({'source_sha256': sha(source), 'effect_sha256': sha(E / 'publication-checkpoint-effect.json'),
        'controller_sha256': sha(TASK / 'checkpoint.py'), 'delivery_effect_sha256': sha(E / 'delivery-effect.json'),
        'delivery_controller_sha256': sha(TASK / 'deliver.py'), 'mapped_files': len(mapped)}))


if __name__ == '__main__':
    main()
