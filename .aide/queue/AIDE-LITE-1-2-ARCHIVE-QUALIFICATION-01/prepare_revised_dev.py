"""Prepare one zero-job checkpoint and dev-only synchronization under exact independent review."""
import ast
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
SOURCE = 'afe3981287098d951996274949b8c56072170d23'
DEV = 'd256a6010183a4b6d70b98071a6e534f5624760d'
MAIN = 'ed4a90046eba12a717a9962f21523285667a669b'
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('revised_dev_preparation_helpers', TASK / 'prepare_link.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def main():
    assert h.git('rev-parse', 'HEAD') == SOURCE
    assert h.git('branch', '--show-current') == 'task/aide-lite-1-2-archive-qualification-01'
    assert not h.git('diff', '--cached', '--name-only')
    for name, expected in (('dev', DEV), ('origin/dev', DEV), ('main', MAIN), ('origin/main', MAIN)):
        assert h.git('rev-parse', name) == expected
    previous = json.loads((E / 'dev-effect.json').read_bytes())
    result = json.loads((E / 'revised-build-qualified.json').read_bytes())
    assert result['state'] == 'PASS_REVISED_BUILD_AND_COMPLETE_DELTA_ONLY'
    assert result['subject']['commit'] == SOURCE and result['local_jobs_consumed'] == 15
    assert result['scratch_absent'] and result['reservation_released']
    baseline = json.loads((E / 'baseline.json').read_bytes())['stable_assets']
    stable = baseline | {name: row['sha256'] for name, row in result['assets'].items()}
    assert len(stable) == 12 and all(h.sha(ROOT / name) == value for name, value in stable.items())
    canonical = {name: h.sha(ROOT / name) for name in previous['canonical_preimages']}
    assert canonical == previous['canonical_preimages']
    pins = set(json.loads((E / 'package-inputs.json').read_bytes())['files'])
    pins.update((TASK / name).relative_to(ROOT).as_posix() for name in
                ('sync_revised_dev.py', 'precheck_revised_dev.py', 'collect_revised_build.py'))
    pins.update((E / name).relative_to(ROOT).as_posix() for name in
                ('revised-build-qualified.json', 'revised-build-result.json', 'revised-archive-member-delta.json',
                 'link-qualified-result.json', 'link-qualified-export.json'))
    h.save(E / 'revised-checkpoint-inputs.json', {'schema': 'aide.exact-checkpoint-inputs.v1',
        'files': {name: h.sha(ROOT / name) for name in sorted(pins)},
        'boundary': 'Current checkpoint material only; original qualification files retain their own subjects and no old result is rebound here.'})
    config, roots, _ = h.workspace.load_config(ROOT / '.aide.local/execution.json')
    assert h.workspace.digest(config) == previous['control_config_digest']
    assert h.workspace.dispatch_state(roots['control'])['mode'] == 'running'
    assert not (roots['control'] / 'active.json').exists()
    refs = {line.split()[1]: line.split()[0] for line in h.git('show-ref').splitlines()}
    symbolic = {}
    for line in h.git('for-each-ref', '--format=%(refname) %(symref)').splitlines():
        parts = line.split()
        if len(parts) == 2:
            symbolic[parts[0]] = parts[1]
    commits = h.git('rev-list', DEV + '..' + SOURCE).splitlines()
    assert len(commits) == 4 and commits[0] == SOURCE
    message = ('chore(lite): share qualified repair and revised candidate on dev\n\n'
        '- Preserve twenty passing live-scan regressions, the qualified export and revised 879-member candidate with full ZIP/TAR deltas.\n'
        '- Keep original passes and failures under their actual subjects; consumer applicability, hosted profiles and final replay remain open.\n'
        '- Prepare a dev-only fast-forward and normal push with exact inputs, source/range checks and identical task-local previews; preserve main and all unrelated refs.\n\n'
        'Validation: PASS - qualified source/build collections, retirement, preserved assets and read-only doctor/validate/pack-status/commit-range preflight; synchronization pending\n'
        'Changelog: Fixed: share the qualified live-scan repair and corrected Lite 1.2 candidate without changing release support\n'
        'Risk: Lite 1.2 is unpublished and current consumer/profile qualification remains incomplete.\n'
        'Follow-up: Exact dev effect review, then dependency applicability, hosted profiles and final affected-consumer/replay group.\n'
        'AIDE-Task: AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01\nAIDE-Format: compact-v1\n')
    path = E / 'revised-dev-message.txt'
    assert not path.exists()
    path.write_bytes(message.encode())
    effect = {'base': DEV, 'main_base': MAIN, 'source_parent': SOURCE, 'source_commits': commits,
        'task_branch': 'task/aide-lite-1-2-archive-qualification-01', 'origin_url': previous['origin_url'],
        'control_config_digest': previous['control_config_digest'],
        'controller_sha256': h.sha(TASK / 'sync_revised_dev.py'), 'attempt_directory': 'revised-dev-attempt-01.log',
        'all_refs': refs, 'symbolic_refs': symbolic, 'stable_assets': stable, 'candidate_assets': result['assets'],
        'canonical_preimages': canonical, 'maximum_additional_jobs': 0,
        'maximum_new_integration_attempts': 1, 'test_reruns': 0, 'export_regenerations': 0,
        'effects': ['One exact managed evidence/docs/candidate checkpoint; no portable source changes after the qualified export.',
                    'Fresh shared locks,pause,no-active-job,origin,all-ref,input and helper checks precede dev-only fast-forward and normal no-follow-tags push.',
                    'Validate current source and exact five-commit range; produce identical local/dev task previews while preserving canonical outputs.',
                    'Keep main,active task branch and unrelated refs; retain actual local/tracking/remote equality and every command stream.'],
        'forbidden': ['new jobs,test reruns,hosted runs,source/export/archive regeneration,support activation',
                      'main promotion,task branch retirement,tags/publication,force,remote branch creation/pruning,hosting settings,other targets/processes,models/providers/spending,roots/reserves/privileges'],
        'review_attestation': {'actual_independent_accept_only': True,
            'path': 'evidence/revised-dev-review.json', 'included_in_commit': True,
            'binds': ['source_sha256', 'effect_sha256', 'controller_sha256']}}
    h.save(E / 'revised-dev-effect.json', effect)
    process = subprocess.run([sys.executable, '-B', str(TASK / 'precheck_revised_dev.py')], cwd=ROOT,
                             check=True, stdin=subprocess.DEVNULL, timeout=120)
    assert process.returncode == 0
    source_path, verdict = E / 'revised-dev-source.json', E / 'revised-dev-review.json'
    excluded = {source_path.relative_to(ROOT).as_posix(), verdict.relative_to(ROOT).as_posix()}
    changed = set(h.git('diff', '--name-only').splitlines()) | set(h.git('ls-files', '--others', '--exclude-standard').splitlines())
    files = {name: h.sha(ROOT / name) for name in sorted(changed - excluded)}
    for name in files:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
    h.git('diff', '--check')
    h.save(source_path, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': SOURCE,
        'effect_sha256': h.sha(E / 'revised-dev-effect.json'), 'files': files,
        'qualification_state': 'Source/build evidence retained; read-only dev preflight passed. Exact synchronization effect pending review.'})
    print(json.dumps({'source_sha256': h.sha(source_path), 'effect_sha256': h.sha(E / 'revised-dev-effect.json'),
                      'controller_sha256': effect['controller_sha256'], 'mapped_files': len(files), 'new_jobs': 0}))


if __name__ == '__main__':
    main()
