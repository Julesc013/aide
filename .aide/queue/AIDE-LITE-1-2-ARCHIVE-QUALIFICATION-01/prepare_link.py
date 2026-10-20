"""Freeze the bounded correction and single regression/export effect for independent review."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'
E = TASK / 'evidence'
BASE = '9ee1880e553e692ad697e0e8699b29439c47317e'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace


def git(*args):
    return subprocess.check_output(['git', *args], text=True, cwd=ROOT, timeout=30).strip()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    data = (json.dumps(value, indent=2) + '\n').encode()
    if path.exists():
        assert path.read_bytes() == data, 'preparation record changed: ' + str(path)
    else:
        path.write_bytes(data)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def nodes(raw):
    return {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(raw).body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}


def main():
    assert git('rev-parse', 'HEAD') == BASE
    assert git('branch', '--show-current') == 'task/aide-lite-1-2-archive-qualification-01'
    assert not git('diff', '--cached', '--name-only')
    review = json.loads((E / 'live-link-amendment-review.json').read_bytes())
    assert review['decision'] == 'ACCEPT' and not review['execution_authorized']
    assert review['amendment_sha256'] == sha(E / 'live-link-observation-amendment.md')
    path = 'core/execution/managed_workspace.py'
    old = subprocess.check_output(['git', 'show', BASE + ':' + path])
    before, after = nodes(old), nodes((ROOT / path).read_bytes())
    assert set(before) == set(after)
    assert {name for name in before if before[name] != after[name]} == {'tree_usage'}
    path = '.aide/scripts/tests/test_managed_workspace.py'
    old_tests = ast.parse(subprocess.check_output(['git', 'show', BASE + ':' + path]))
    new_tests = ast.parse((ROOT / path).read_bytes())
    original = {n.name: ast.dump(n, include_attributes=False) for n in ast.walk(old_tests)
                if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}
    revised = {n.name: ast.dump(n, include_attributes=False) for n in ast.walk(new_tests)
               if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}
    assert len(original) == 75 and len(revised) == 82
    assert all(revised[name] == value for name, value in original.items())
    ownership = load('link_prepare_ownership', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py')
    inventory = ownership.observe()
    assert inventory['file_count'] == 879
    save(E / 'link-prior-export.json', inventory)
    baseline = json.loads((E / 'baseline.json').read_bytes())['stable_assets']
    built = json.loads((E / 'build-result.json').read_bytes())
    stable = dict(baseline)
    stable.update({name: value['sha256'] for name, value in built['assets'].items()})
    assert len(stable) == 12 and all(sha(ROOT / name) == digest for name, digest in stable.items())
    assert {p.relative_to(ROOT).as_posix() for p in (ROOT / '.aide/release/stable').iterdir()} == set(stable)
    for name in stable:
        assert git('hash-object', '--no-filters', '--', name) == git('rev-parse', BASE + ':' + name)
    save(E / 'link-baseline.json', {'source_commit': BASE, 'workspace_sha256': hashlib.sha256(old).hexdigest(),
                                  'stable_assets': stable, 'original_candidate_checkpoint': BASE})
    prior_effect = json.loads((E / 'remaining-effect.json').read_bytes())
    control, roots, _ = workspace.load_config(ROOT / '.aide.local/execution.json')
    qualification, _, working = workspace.load_config(ROOT / prior_effect['qualification_config'])
    assert workspace.digest(control) == prior_effect['control_config_digest']
    assert workspace.digest(qualification) == prior_effect['qualification_config_digest']
    assert workspace.dispatch_state(roots['control'])['mode'] == 'running'
    assert not (roots['control'] / 'active.json').exists()
    job = json.loads((E / 'local-job-template.json').read_bytes())
    job['argv'] = [sys.executable, (TASK / 'run_link_repair.py').relative_to(ROOT).as_posix()]
    inputs = set(job['inputs']) | {job['argv'][1], (E / 'link-baseline.json').relative_to(ROOT).as_posix(),
                                  (E / 'link-prior-export.json').relative_to(ROOT).as_posix(),
                                  prior_effect['qualification_config']}
    job['inputs'] = {name: sha(ROOT / name) for name in sorted(inputs)}
    save(E / 'link-job-template.json', job)
    actual = dict(job, source_commit=BASE, source_tree=git('rev-parse', BASE + '^{tree}'))
    workspace.validate_job(actual, working)
    owner = load('link_prepare_commit_owner', ROOT / '.aide/scripts/aide_lite.py')
    message = ('fix(execution): settle live hardlink observations before refusal\n\n'
               'Preserve the incomplete predecessor attempt, 18 passing additions and 56 current form witnesses. Correct only the existing live scan and retain strict collection, all 75 original test bodies and unchanged resource policy.\n\n'
               '- Scope: one bounded re-observation, seven new regressions and exact regression/export preparation.\n'
               '- Follow-up: one owned export only after tests; revised archives, dependency proof, affected consumers, hosted profiles, replay and publication remain gated.\n\n'
               'AIDE-Format: compact-v1\nAIDE-Task: AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01\n'
               'Validation: PASS - source AST, 879 owned preimages, 12 stable assets and literal job preflight; runtime group pending\n'
               'Changelog: Fixed: prepare bounded live hardlink re-observation with original evidence retained\n')
    failures = [c.message for c in owner.validate_commit_message_text(message) if c.severity == 'FAIL']
    assert not failures, failures
    path = E / 'link-message.txt'
    if path.exists():
        assert path.read_bytes() == message.encode()
    else:
        path.write_bytes(message.encode())
    save(E / 'link-prechecks.json', {'status': 'PASS_STRUCTURAL_PRECHECK', 'base': BASE,
         'original_methods_preserved': 75, 'new_methods': 7, 'changed_owner_functions': ['tree_usage'],
         'export_preimages': 879, 'stable_assets_preserved': 12, 'job_inputs': len(inputs),
         'job_preflight': 'PASS', 'new_jobs_started': 0, 'runtime_tests_run': 0,
         'prior_incomplete_reconciled': True, 'scope': 'Preparation only; runtime success is not inferred.'})
    effect = {key: prior_effect[key] for key in ('task_branch', 'origin_url', 'control_config_digest',
              'qualification_config', 'qualification_config_digest', 'expected_refs')}
    effect.update(base=BASE, controller_sha256=sha(TASK / 'commit_and_repair_scan.py'),
        maximum_local_allocations=1, total_local_ceiling=16, local_jobs_already_consumed=12,
        maximum_hosted_runs=0, live_model_requests=0,
        expected_export_changes=['.aide/export/aide-lite-pack-v0/' + name for name in
                                 ('checksums.json', 'manifest.yaml', 'files/core/execution/managed_workspace.py')],
        effects=['One exact reviewed task checkpoint; no integration or push.',
                 'One600second managed group: original-source legal-transition rejection demonstration,then20 corrected-source methods with zero skips.',
                 'Only successful selected regressions permit one existing-owner export refresh,with879 recoverable preimages and12 stable assets preserved.',
                 'Preserve exact job/manifest/source/config identities,collection,quiescence and retirement;stop on any failure,no retry.'],
        forbidden=['archive rebuild,dev/main integration,push,hosted dispatch,tag,publication or support activation',
                   'other targets/processes,providers/models/spending,new roots,reserves,limits,configuration or privileges'],
        review_attestation={'path': (E / 'link-review.json').relative_to(ROOT).as_posix(),
                            'actual_independent_accept_only': True, 'included_in_commit': True,
                            'binds': ['source_sha256', 'effect_sha256', 'controller_sha256']})
    save(E / 'link-effect.json', effect)
    source_path, verdict_path = E / 'link-source.json', E / 'link-review.json'
    excluded = {source_path.relative_to(ROOT).as_posix(), verdict_path.relative_to(ROOT).as_posix()}
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    files = {name: sha(ROOT / name) for name in sorted(changed - excluded)}
    for name in files:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
    git('diff', '--check')
    save(source_path, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': BASE,
         'effect_sha256': sha(E / 'link-effect.json'), 'files': files,
         'qualification_state': 'Preparation preflight passed; original-race demonstration,20regressions and owned export pending.'})
    print(json.dumps({'source_sha256': sha(source_path), 'effect_sha256': sha(E / 'link-effect.json'),
                      'controller_sha256': effect['controller_sha256'], 'mapped_files': len(files),
                      'tests_run': 0, 'jobs_started': 0}))


if __name__ == '__main__':
    main()
