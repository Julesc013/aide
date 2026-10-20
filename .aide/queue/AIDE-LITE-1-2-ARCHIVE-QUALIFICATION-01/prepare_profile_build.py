"""Freeze a separately reviewed metadata-only build; preparation submits no job."""
import ast
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
BASE = '4f85bb0c95ef7fc29667edd351346d684a80bb48'
spec = importlib.util.spec_from_file_location('profile_preparation_helpers', TASK / 'prepare_link.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def main():
    assert h.git('rev-parse', 'HEAD') == BASE and not h.git('diff', '--cached', '--name-only')
    amendment = json.loads((E / 'hosted-correction-amendment-review.json').read_bytes())
    assert amendment['decision'] == 'ACCEPT' and not amendment['required_fixes']
    assert h.sha(E / 'hosted-correction-amendment.md') == amendment['amendment_sha256']
    hosted = json.loads((E / 'hosted-qualified.json').read_bytes())
    assert hosted['hosted_runs_consumed'] == 1 and hosted['local_allocations_consumed'] == 15
    assert hosted['profiles']['macos-15-arm64']['qualification_pass']
    assert json.loads((E / 'hosted-collection-verified.json').read_bytes())['state'] == 'PASS_LOSSLESS_ROUNDTRIP'
    pack = json.loads((E / 'revised-pack-subject.json').read_bytes())
    assert len(pack) == 879 and all(h.sha(ROOT / name) == value for name, value in pack.items())
    before = {}
    for path in sorted((ROOT / '.aide/release').rglob('*')):
        h.workspace.ordinary(path, directory=path.is_dir())
        if path.is_file():
            before[path.relative_to(ROOT).as_posix()] = {'sha256': h.sha(path), 'size_bytes': path.stat().st_size}
    assert len(before) == 62
    h.save(E / 'profile-release-before.json', before)
    old = json.loads((E / 'revised-build-result.json').read_bytes())
    assert all(before[name] == value for name, value in old['assets'].items())
    baseline = json.loads((E / 'baseline.json').read_bytes())
    assert all(h.sha(ROOT / name) == value for name, value in baseline['stable_assets'].items())
    # Replay actual producer text, including original bytes, with the corrected
    # line framing. This is preparation, not another product execution.
    text_checks = {}
    pattern = r'checks: (\d+); PASS: (\d+); WARN: (\d+); FAIL: (\d+); OTHER: (\d+)'
    for profile in ('windows-2025-x64', 'macos-15-arm64'):
        path = E / 'hosted-logs.log' / profile / 'ordinary-validate.stdout'
        text = path.read_bytes().decode('utf-8')
        rows = [line for line in text.splitlines() if line.startswith('checks:')]
        assert len(rows) == 1 and text.splitlines().count('status: PASS') == 1
        counts = re.fullmatch(pattern, rows[0])
        assert counts and tuple(map(int, counts.groups())) == (27, 25, 2, 0, 0)
        text_checks[profile] = {'stdout_sha256': h.sha(path), 'counts': list(map(int, counts.groups()))}
    prior = json.loads((E / 'revised-build-effect.json').read_bytes())
    control, roots, _ = h.workspace.load_config(ROOT / '.aide.local/execution.json')
    qualification, _, working = h.workspace.load_config(ROOT / prior['qualification_config'])
    assert h.workspace.digest(control) == prior['control_config_digest']
    assert h.workspace.digest(qualification) == prior['qualification_config_digest']
    assert h.workspace.dispatch_state(roots['control'])['mode'] == 'running' and not (roots['control'] / 'active.json').exists()
    job = json.loads((E / 'revised-build-job-template.json').read_bytes())
    worker = (TASK / 'run_profile_build.py').relative_to(ROOT).as_posix()
    job['argv'] = [sys.executable, worker]
    inputs = set(job['inputs']) | {worker, '.aide/release/successor-candidate.json'} | {(E / name).relative_to(ROOT).as_posix() for name in
        ('profile-release-before.json', 'profile-candidate-delta.json', 'revised-build-result.json',
         'hosted-correction-amendment-review.json', 'hosted-qualified.json', 'hosted-collection-verified.json')}
    job['inputs'] = {name: h.sha(ROOT / name) for name in sorted(inputs)}
    h.save(E / 'profile-build-job-template.json', job)
    h.workspace.validate_job(dict(job, source_commit=BASE, source_tree=h.git('rev-parse', BASE + '^{tree}')), working)
    message = ('fix(lite): preserve hosted outcomes and correct candidate profile\n\n'
        '- Preserve the 49-form macOS pass, Linux environment refusal, Windows CRLF wrapper failure and all lossless controller/profile evidence.\n'
        '- Correct source-only line framing and the unpublished Linux kernel declaration without changing executable product bytes or the export.\n'
        '- Prepare one metadata-only existing-owner build with complete archive/identity deltas; missing Windows/Linux execution and final local checks stay gated.\n\n'
        'Validation: PASS - complete hosted receipt roundtrip, actual LF/CRLF producer text, 879 unchanged export files, historical assets and finite job preflight; metadata build pending\n'
        'Changelog: Fixed: correct Linux candidate environment metadata and hosted CRLF qualification parsing\n'
        'Risk: Published support is unchanged; macOS retains its actual archive subject and later reuse requires independent acceptance.\n'
        'Follow-up: Collect metadata-only deltas, separately review two-profile hosted execution and final local qualification.\n'
        'AIDE-Task: AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01\nAIDE-Format: compact-v1\n')
    lite = h.load('profile_preparation_commit_owner', ROOT / '.aide/scripts/aide_lite.py')
    assert not [c for c in lite.validate_commit_message_text(message) if c.severity == 'FAIL']
    (E / 'profile-build-message.txt').write_bytes(message.encode())
    h.save(E / 'profile-build-prechecks.json', {'state': 'PASS_METADATA_BUILD_PREPARATION', 'base': BASE,
        'producer_text_checks': text_checks, 'export_files_preserved': 879, 'release_files': len(before),
        'candidate_is_portable_source': '.aide/release/successor-candidate.json' in lite.PORTABLE_SOURCE_FILES,
        'local_jobs_consumed': 15, 'new_jobs': 0, 'job_input_count': len(inputs)})
    assert '.aide/release/successor-candidate.json' not in lite.PORTABLE_SOURCE_FILES
    refs = {ref: h.git('rev-parse', ref) for ref in ('dev', 'main', 'origin/dev', 'origin/main')}
    assert refs['dev'] == refs['origin/dev'] == '03929beb3c7278975f9c0b3b1378712aeca2ac91'
    assert refs['main'] == refs['origin/main'] == 'ed4a90046eba12a717a9962f21523285667a669b'
    effect = {k: prior[k] for k in ('task_branch', 'origin_url', 'control_config_digest', 'qualification_config', 'qualification_config_digest')}
    effect.update(base=BASE, expected_refs=refs, controller_sha256=h.sha(TASK / 'commit_and_profile_build.py'),
        maximum_local_allocations=1, total_local_ceiling=17, local_jobs_already_consumed=15,
        maximum_hosted_runs=0, maximum_export_refreshes=0, live_model_requests=0,
        expected_build_changes=sorted(old['assets']),
        effects=['One exact task checkpoint and one existing-runner metadata build/validation bounded to 600 seconds.',
                 'Only four unpublished assets may change; require precisely stable-release/checksums archive-member changes.',
                 'Preserve all executable/export bytes, source provenance, other profiles, historical assets and all original evidence.',
                 'Retain every actual result and retire quiescently; no automatic retry.'],
        forbidden=['export or executable product change,hosted dispatch,integration,push,tag,publication,support activation',
                   'other repositories/processes,models/providers/spending,new roots,limits,reserves,privileges'])
    h.save(E / 'profile-build-effect.json', effect)
    source_path, verdict = E / 'profile-build-source.json', E / 'profile-build-review.json'
    excluded = {p.relative_to(ROOT).as_posix() for p in (source_path, verdict)}
    changed = set(h.git('diff', '--name-only').splitlines()) | set(h.git('ls-files', '--others', '--exclude-standard').splitlines())
    files = {name: h.sha(ROOT / name) for name in sorted(changed - excluded)}
    for name in files:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
    h.git('diff', '--check')
    h.save(source_path, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': BASE,
                        'effect_sha256': h.sha(E / 'profile-build-effect.json'), 'files': files})
    print(json.dumps({'source_sha256': h.sha(source_path), 'effect_sha256': h.sha(E / 'profile-build-effect.json'),
                      'controller_sha256': effect['controller_sha256'], 'mapped_files': len(files), 'new_jobs': 0}))


if __name__ == '__main__':
    main()
