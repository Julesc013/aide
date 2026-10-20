"""Freeze the final finite local group; preparation allocates no job."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
BASE = '52ddd31908ac96b3e891933a066936e72c90b137'
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    assert not path.exists(), path
    path.write_bytes((json.dumps(value, indent=2) + '\n').encode())


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=30).strip()


def assertions(raw, function_name):
    node = next(n for n in ast.parse(raw).body if isinstance(n, ast.FunctionDef) and n.name == function_name)
    return [ast.dump(n, include_attributes=False) for n in ast.walk(node) if isinstance(n, ast.Assert)]


def main():
    assert git('rev-parse', 'HEAD') == BASE and not git('diff', '--cached', '--name-only')
    previous = json.loads((E / 'profile-hosted-effect.json').read_bytes())
    build = json.loads((E / 'profile-build-result.json').read_bytes())
    coverage = json.loads((E / 'profile-coverage.json').read_bytes())
    verified = json.loads((E / 'profile-hosted-collection-verified.json').read_bytes())
    assert verified['state'] == 'PASS_LOSSLESS_ROUNDTRIP' and verified['coverage_sha256'] == sha(E / 'profile-coverage.json')
    assert coverage['behavioral_coverage_pass'] and coverage['fresh_primary_identity_required'] and not coverage['release_accepted']
    assert coverage['local_jobs_consumed'] == 16 and coverage['hosted_runs_consumed'] == 2 and coverage['hosted_jobs_consumed'] == 5
    assert coverage['assets'] == build['assets']
    refs = {r: git('rev-parse', r) for r in ('dev', 'origin/dev', 'main', 'origin/main')}
    assert refs['dev'] == refs['origin/dev'] == BASE
    assert refs['main'] == refs['origin/main'] == previous['main_base']
    config, roots, _ = workspace.load_config(ROOT / '.aide.local/execution.json')
    assert workspace.digest(config) == previous['control_config_digest']
    assert workspace.dispatch_state(roots['control'])['mode'] == 'running' and not (roots['control'] / 'active.json').exists()
    prior = json.loads((E / 'profile-build-effect.json').read_bytes())
    qualification, _, working = workspace.load_config(ROOT / prior['qualification_config'])
    assert workspace.digest(qualification) == prior['qualification_config_digest']
    assert qualification['limits']['runtime_seconds'] == 600
    actual = {'system': platform.system(), 'release': platform.release(), 'version': platform.version(),
        'machine': platform.machine(), 'runtime': {'implementation': platform.python_implementation(), 'version': platform.python_version()}}
    profile = next(p for p in build['identity']['profiles'] if p['profile_id'] == 'aide-lite-local-windows')
    assert actual == profile['environment']
    assets = previous['stable_assets']
    assert all(sha(ROOT / n) == value for n, value in assets.items())
    pack = json.loads((E / 'revised-pack-subject.json').read_bytes())
    assert len(pack) == 879 and all(sha(ROOT / n) == value for n, value in pack.items())
    # Optional deadlines do not alter the original acceptance expressions.
    preserved = {}
    for name in ('run_consumer.py', 'run_predecessor.py'):
        old = subprocess.check_output(['git', 'show', BASE + ':' + (TASK / name).relative_to(ROOT).as_posix()], cwd=ROOT)
        before, after = assertions(old, 'main'), assertions((TASK / name).read_bytes(), 'main')
        assert before == after
        preserved[name] = len(before)
    replay_old = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01/run_replay.py'
    original = assertions(replay_old.read_bytes(), 'main')
    current = assertions((TASK / 'run_replay.py').read_bytes(), 'main')
    assert all(value in current for value in original)
    preserved['original_replay'] = len(original)
    process = Path('D:/Projects/AIDE/.aide.local/execution/retained/282e45c890d04122bbe30e1b96d0f837/output/case-06/process.json')
    timing = json.loads(process.read_bytes())
    assert timing['case'] == 6 and timing['exit_code'] == 0
    feasibility = {'state': 'BOUNDED_FEASIBILITY_WITH_CLEANUP_RESERVE', 'outer_runner_seconds': 600,
        'active_group_seconds': 540, 'phase_caps_seconds': {'managed': 60, 'brownfield': 240, 'replay': 210},
        'serial_phase_cap_sum_seconds': 510, 'outer_cleanup_reserve_seconds': 60,
        'observed_original_case6_seconds': (timing['finished_unix_ns'] - timing['started_unix_ns']) / 1e9,
        'original_case6_process_sha256': sha(process), 'hosted_whole_job_seconds': verified['hosted_whole_job_seconds'],
        'basis': 'Managed cap exceeds retained14.94s. Brownfield selects one of two unchanged scenarios; hosted Windows385s includes setup,49forms and both scenarios. Replay uses one bounded pair of archive writers, four source checks and one identity/detach fixture. Serial phase retirement prevents combined scratch retention.',
        'limits': 'Observed times are not future guarantees. Shared/phase deadlines stop launches and reject late completion; synchronous replay checks surround projection/archive work. The unchanged600s Job limit is the hard containment limit. No assertion or recovery check is dropped to fit; an overrun stays incomplete without retry.'}
    assert sum(feasibility['phase_caps_seconds'].values()) <= feasibility['active_group_seconds']
    save(E / 'final-feasibility.json', feasibility)
    inputs = json.loads((E / 'profile-hosted-inputs.json').read_bytes())
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    files = set(inputs['files']) | changed | {prior['qualification_config']}
    inputs['files'] = {n: sha(ROOT / n) for n in sorted(files)}
    inputs['actual_archive_subject'] = build['assets']
    inputs['boundary'] = 'Exact local final-group inputs, including approved local config; no hosted reuse of this local-only manifest.'
    save(E / 'final-inputs.json', inputs)
    job = json.loads((E / 'profile-build-job-template.json').read_bytes())
    assert set(job['canonical_outputs']) == {'.aide/release/stable'}
    assert job['canonical_outputs']['.aide/release/stable']['bytes'] == 8 * 1024 * 1024
    job['argv'] = [sys.executable, (TASK / 'run_final.py').relative_to(ROOT).as_posix()]
    job['inputs'] = inputs['files']
    save(E / 'final-job-template.json', job)
    workspace.validate_job(dict(job, source_commit=BASE, source_tree=git('rev-parse', 'HEAD^{tree}')), working)
    message = ('test(lite): finish affected consumers and exact release replay\n\n'
        '- Preserve complete Windows/Linux hosted passes and scoped retained macOS applicability under their exact subjects.\n'
        '- Prepare only original managed case6, unfinished primary brownfield, fresh ownership identity and complete replay in one finite existing-runner group.\n'
        '- Keep original assertions, retired attempts, source/export/archive bytes and actual published predecessor; bind deadlines, evidence and cleanup.\n\n'
        'Validation: PASS - hosted receipt roundtrip, exact inputs/config/environment/assets, original7consumer/10predecessor/8replay assertions, syntax and finite job validation. Final execution remains pending.\n'
        'Changelog: Fixed: complete affected current-archive qualification and release replay\n'
        'Risk: No support activation, integration or publication; late/incomplete work stays incomplete; controller/review usage unknown.\n'
        'Follow-up: Collect and independently accept the final group before dev/main or publication effects.\n'
        'AIDE-Task: AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01\nAIDE-Format: compact-v1\n')
    spec = importlib.util.spec_from_file_location('final_preparation_lite', ROOT / '.aide/scripts/aide_lite.py')
    lite = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lite
    spec.loader.exec_module(lite)
    assert not [c for c in lite.validate_commit_message_text(message) if c.severity == 'FAIL']
    (E / 'final-message.txt').write_bytes(message.encode())
    save(E / 'final-prechecks.json', {'state': 'PASS_PREPARATION_ONLY', 'base': BASE, 'environment': actual,
        'assertions_preserved': preserved, 'input_count': len(job['inputs']), 'new_jobs': 0, 'original_case6_timing': feasibility['observed_original_case6_seconds']})
    effect = {k: previous[k] for k in ('task_branch', 'origin_url', 'control_config_digest')}
    effect.update(checkpoint_parent=BASE, dev_preimage=BASE, main_base=previous['main_base'],
        all_refs={r.split()[1]: r.split()[0] for r in git('show-ref').splitlines()}, stable_assets=assets,
        package_inputs_sha256=sha(E / 'final-inputs.json'), controller_sha256=sha(TASK / 'commit_and_final.py'),
        profile_environment=actual, qualification_config=prior['qualification_config'],
        qualification_config_digest=prior['qualification_config_digest'], maximum_local_allocations=1,
        local_jobs_already_consumed=16, total_local_ceiling=17, maximum_hosted_runs=0, maximum_export_refreshes=0,
        maximum_archive_rebuilds=0, live_model_requests=0,
        effects=['One exact task checkpoint then one existing600s managed runner allocation for the complete serial final group.',
            'Fresh source/config/input/environment/pause/admission checks; retain every result and original incomplete attempt.',
            'Existing8MiB stable custody reservation is retained solely for the guarded stable-validate read; no canonical writer or reserve increase is authorized.',
            'Only admitted scratch/output changes after checkpoint; all assets/export/refs and canonical outputs preserved.'],
        forbidden=['retry,ceiling reset,assertion removal,canonical writes,export/archive regeneration',
            'push,integration,hosted runs,support activation,tags,releases,other repositories/processes,models/providers/spending,roots/reserves/privileges'])
    save(E / 'final-effect.json', effect)
    source_path, verdict_path = E / 'final-source.json', E / 'final-review.json'
    excluded = {p.relative_to(ROOT).as_posix() for p in (source_path, verdict_path)}
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    mapped = {n: sha(ROOT / n) for n in sorted(changed - excluded)}
    assert len(mapped) <= 256
    for name in mapped:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
        assert git('hash-object', '--no-filters', '--', name) == git('hash-object', '--path=' + name, '--', name), name
    git('diff', '--check')
    save(source_path, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': BASE,
        'effect_sha256': sha(E / 'final-effect.json'), 'files': mapped})
    print(json.dumps({'source_sha256': sha(source_path), 'effect_sha256': sha(E / 'final-effect.json'),
        'controller_sha256': effect['controller_sha256'], 'mapped_files': len(mapped), 'new_jobs': 0}))


if __name__ == '__main__':
    main()
