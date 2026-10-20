"""Freeze one actual-archive hosted effect after read-only preparation checks."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
PARENT = '03929beb3c7278975f9c0b3b1378712aeca2ac91'
MAIN = 'ed4a90046eba12a717a9962f21523285667a669b'
spec = importlib.util.spec_from_file_location('hosted_preparation_helpers', TASK / 'prepare_link.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def main():
    assert h.git('rev-parse', 'HEAD') == PARENT
    assert h.git('branch', '--show-current') == 'task/aide-lite-1-2-archive-qualification-01'
    assert not h.git('diff', '--cached', '--name-only')
    for ref, value in (('dev', PARENT), ('origin/dev', PARENT), ('main', MAIN), ('origin/main', MAIN)):
        assert h.git('rev-parse', ref) == value
    prior = json.loads((E / 'revised-dev-effect.json').read_bytes())
    qualified = json.loads((E / 'revised-build-qualified.json').read_bytes())
    subject = json.loads((E / 'revised-build-result.json').read_bytes())
    assert qualified['local_jobs_consumed'] == 15 and qualified['export_refreshes_consumed'] == 2
    assert qualified['scratch_absent'] and qualified['reservation_released']
    reuse = json.loads((E / 'revised-behavior-reuse-review.json').read_bytes())
    assert reuse['decision'] == 'ACCEPT' and not reuse['required_fixes']
    assert h.sha(E / 'revised-behavior-reuse-proposal.json') == reuse['proof_sha256']
    stable = prior['stable_assets']
    assert len(stable) == 12 and all(h.sha(ROOT / n) == v for n, v in stable.items())
    pins = {n: h.sha(ROOT / n) for n in json.loads((E / 'revised-checkpoint-inputs.json').read_bytes())['files']}
    for name in ('evals/lite/release.py', 'evals/lite/lifecycle.py', '.github/workflows/lite-modern-lifecycle.yml',
                 '.aide/queue/AIDE-STABLE-LITE-RELEASE-EFFECT-01/delivered_additions.py',
                 '.aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/worker.py',
                 *(p.relative_to(ROOT).as_posix() for p in (TASK / 'run_additions.py', TASK / 'run_consumer.py', TASK / 'run_predecessor.py', E / 'revised-build-result.json', E / 'revised-behavior-reuse-review.json', E / 'revised-behavior-reuse-proposal.json'))):
        pins[name] = h.sha(ROOT / name)
    pins.update(stable)
    h.save(E / 'hosted-inputs.json', {'schema': 'aide.exact-checkpoint-inputs.v1', 'workunit': TASK.name,
        'files': dict(sorted(pins.items())), 'actual_archive_subject': subject['assets'],
        'boundary': 'Exact actual-archive evaluation inputs; original observations retain their own subjects.'})
    # Preserve all original assertion expressions, not only a total count.
    assertions = {}
    for name in ('run_additions.py', 'run_consumer.py', 'run_predecessor.py'):
        path = TASK / name
        before = h.git('show', 'HEAD:' + path.relative_to(ROOT).as_posix())
        after = path.read_text(encoding='utf-8')
        a = sorted(ast.dump(n.test) for n in ast.walk(ast.parse(before)) if isinstance(n, ast.Assert))
        b = sorted(ast.dump(n.test) for n in ast.walk(ast.parse(after)) if isinstance(n, ast.Assert))
        assert a == b, name
        assertions[name] = len(a)
    path = ROOT / 'evals/lite/lifecycle.py'
    before = h.git('show', 'HEAD:evals/lite/lifecycle.py')
    old = next(n for n in ast.parse(before).body if isinstance(n, ast.FunctionDef) and n.name == 'qualify_successor')
    new = next(n for n in ast.parse(path.read_bytes()).body if isinstance(n, ast.FunctionDef) and n.name == 'qualify_successor')
    a = sorted(ast.dump(n.test) for n in ast.walk(old) if isinstance(n, ast.Assert))
    b = sorted(ast.dump(n.test) for n in ast.walk(new) if isinstance(n, ast.Assert))
    assert a == b and len(a) == 28
    assertions['qualify_successor'] = len(a)
    preparation = {'assertion_expressions_preserved': assertions,
        'pure_form_matcher_retained_argv_checks': 56, 'runtime_qualification': 'not executed',
        'authoring_corrections': ['Cancelled inefficient all-function AST extraction before any proof output; narrowed it to one function.',
            'Replaced whitespace-specific safe-import-prefix check with AST literal verification.',
            'Independent preliminary review found successful validate includes FAIL:0; replaced substring refusal with exact status/count parsing.',
            'Removed redundant nested partial-canary launch; retained shared actual-predecessor recovery oracle and focused fresh-partial semantics.',
            'Added shared480s evaluator deadline and bounded command timeouts, reserving time within10min hosted job for cleanup/receipts.'],
        'commands': []}
    folder = E / 'hosted-prechecks.log'
    folder.mkdir()
    for label, args in [('doctor', ['doctor']), ('validate', ['validate']), ('pack-status', ['pack-status']), ('git-plan', ['git', 'plan'])]:
        argv = [sys.executable, '-B', '.aide/scripts/aide_lite.py', *args]
        streams = [folder / (label + suffix) for suffix in ('.stdout', '.stderr')]
        with streams[0].open('xb') as stdout, streams[1].open('xb') as stderr:
            process = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=90)
        preparation['commands'].append({'argv': argv, 'exit_code': process.returncode,
            'streams': {p.name: {'bytes': p.stat().st_size, 'sha256': h.sha(p)} for p in streams}})
        assert process.returncode == 0
        text = streams[0].read_text(encoding='utf-8')
        if label == 'validate':
            assert 'status: PASS' in text and '; FAIL: 0;' in text
        if label == 'pack-status':
            assert 'PASS_SOURCE_ANCESTOR' in text
        if label == 'git-plan':
            assert 'dirty_tree_requires_classification' in text
    h.save(E / 'hosted-prechecks.json', preparation)
    message = ('test(lite): qualify actual archives on declared modern profiles\n\n'
        '- Reuse existing lifecycle, task/git/review/quality/usage assertions for49 ordinary delivered CLI forms and real1.1-to-1.2 recovery.\n'
        '- Preserve original behavioral observations under independently accepted dependency applicability; revised managed forms and final local replay remain open.\n'
        '- Bind one three-profile hosted run to exact archives, environment tuples and inputs with a finite observer, raw receipts and guarded fixture retirement.\n\n'
        'Validation: PASS - source syntax, preserved assertion expressions, retained argv matcher and read-only doctor/validate/pack-status/Git preflight; hosted qualification pending\n'
        'Changelog: Changed: prepare exact archive-based Windows Server, Linux and macOS qualification without changing portable product bytes\n'
        'Risk: Hosted observations may refuse changed environments; no new support or publication claim.\n'
        'Follow-up: Collect all hosted outcomes, then independently review the remaining local affected-consumer and release-replay group.\n'
        'AIDE-Task: AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01\nAIDE-Format: compact-v1\n')
    (E / 'hosted-message.txt').write_bytes(message.encode())
    config, roots, _ = h.workspace.load_config(ROOT / '.aide.local/execution.json')
    assert h.workspace.digest(config) == prior['control_config_digest']
    assert h.workspace.dispatch_state(roots['control'])['mode'] == 'running'
    assert not (roots['control'] / 'active.json').exists()
    effect = {'checkpoint_parent': PARENT, 'dev_base': PARENT, 'main_base': MAIN,
        'task_branch': 'task/aide-lite-1-2-archive-qualification-01', 'origin_url': prior['origin_url'],
        'all_refs': {line.split()[1]: line.split()[0] for line in h.git('show-ref').splitlines()},
        'source_commit': 'EXACT_REVIEWED_CHECKPOINT', 'control_config_digest': prior['control_config_digest'],
        'controller_sha256': h.sha(TASK / 'checkpoint_and_host.py'), 'observer_sha256': h.sha(TASK / 'observe_hosted.py'),
        'observer_provenance': '.aide/queue/AIDE-LITE-POSIX-LIFECYCLE-01/observe_hosted.py',
        'observer_provenance_sha256': h.sha(ROOT / '.aide/queue/AIDE-LITE-POSIX-LIFECYCLE-01/observe_hosted.py'),
        'stable_assets': stable, 'package_inputs_sha256': h.sha(E / 'hosted-inputs.json'),
        'profiles': ['windows-2025-x64', 'ubuntu-24.04-x64', 'macos-15-arm64'],
        'hosted_runs_before': 0, 'maximum_new_hosted_runs': 1, 'jobs': 3, 'minutes_per_job': 10,
        'evaluator_deadline_seconds': 480, 'observer_deadline_seconds': 1200,
        'maximum_local_allocations': 0, 'maximum_export_refreshes': 0, 'maximum_archive_rebuilds': 0,
        'receipt_bounds': {'files_per_profile': 512, 'raw_bytes_per_profile': 8 * 1024 * 1024, 'compressed_bytes_per_profile': 2 * 1024 * 1024,
                           'controller_metadata_bytes': 2 * 1024 * 1024, 'controller_retained_bytes': 64 * 1024 * 1024},
        'effects': ['One reviewed exact task checkpoint and important remote task-branch publication triggers one existing three-job hosted workflow.',
                    'Code owns bounded observation and complete log collection; unchanged waiting causes no model invocation.',
                    'All outcomes including failures/environment changes are retained without automatic redispatch.',
                    'Keep dev/main and unrelated refs, all stable assets, portable export and canonical preview bytes unchanged.'],
        'forbidden': ['local test allocation, source/export/archive regeneration, support activation, dev/main promotion',
                      'tags/releases/artifact/cache uploads, force,pruning,hosting settings,other repositories/processes,models/providers/spending,roots/reserves/privileges']}
    h.save(E / 'hosted-effect.json', effect)
    source_path, verdict = E / 'hosted-source.json', E / 'hosted-review.json'
    excluded = {p.relative_to(ROOT).as_posix() for p in (source_path, verdict)}
    changed = set(h.git('diff', '--name-only').splitlines()) | set(h.git('ls-files', '--others', '--exclude-standard').splitlines())
    files = {n: h.sha(ROOT / n) for n in sorted(changed - excluded)}
    for name in files:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
    h.git('diff', '--check')
    h.save(source_path, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': PARENT,
                        'effect_sha256': h.sha(E / 'hosted-effect.json'), 'files': files})
    print(json.dumps({'source_sha256': h.sha(source_path), 'effect_sha256': h.sha(E / 'hosted-effect.json'),
                      'controller_sha256': effect['controller_sha256'], 'mapped_files': len(files), 'input_pins': len(pins)}))


if __name__ == '__main__':
    main()
