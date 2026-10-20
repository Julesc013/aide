"""Qualify frozen release archives on one exact declared modern environment.

This composes existing lifecycle and additive CLI oracles. It does not build a
pack, launch managed jobs, change support state, or call an inference provider.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
import time
import traceback

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'
CAN = ROOT / '.aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/canaries'
DEADLINE = None


def load(name, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_bytes((json.dumps(value, sort_keys=True, indent=2) + '\n').encode())


def parts(tokens):
    result, key = {'positionals': []}, 'positionals'
    for token in tokens:
        if token.startswith('--'):
            if token in result and token != '--stream':
                raise ValueError('duplicate CLI option')
            key = token
            result.setdefault(key, [])
        else:
            result[key].append(token)
    return result


def match(form, argv):
    expected, actual = parts(form.split()), parts(argv)
    if '--json' not in expected and actual.get('--json') == []:
        del actual['--json']
    if set(expected) != set(actual):
        return False
    for key, values in expected.items():
        if key == '--stream':
            values = values * len(actual[key])
        if len(values) != len(actual[key]):
            return False
        for pattern, value in zip(values, actual[key]):
            if pattern.startswith('<') and pattern.endswith('>'):
                if not value or value.startswith('--'):
                    return False
                if pattern == '<digest>' and not re.fullmatch('[0-9a-f]{64}', value):
                    return False
            elif pattern != value:
                return False
    return True


def recorder(helper, out):
    class Recorder(helper.Recorder):
        def run(self, label, script, root, *args, exits=(0,), offline_text=False, input_data=None):
            argv = [sys.executable, '-I', '-B', str(script), '--repo-root', str(root), *args]
            row = {'argv': argv, 'exit_code': None, 'state': 'started', 'started_unix_ns': time.time_ns()}
            path = out / (label + '.json')
            streams = [out / (label + suffix) for suffix in ('.stdout', '.stderr')]
            save(path, row)
            start = time.monotonic()
            try:
                remaining = DEADLINE - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError('one evaluator deadline; retain completed observations')
                with streams[0].open('xb') as stdout, streams[1].open('xb') as stderr:
                    process = subprocess.run(argv, cwd=ROOT, stdout=stdout, stderr=stderr,
                        stdin=subprocess.DEVNULL if input_data is None else None,
                        input=input_data, timeout=min(60, remaining))
                row.update(state='completed', exit_code=process.returncode)
            except Exception as error:
                row.update(state='exception', error_type=type(error).__name__, error=str(error))
                raise
            finally:
                row['elapsed_seconds'] = time.monotonic() - start
                row['streams'] = {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in streams if p.exists()}
                save(path, row)
                self.commands.append({'label': label, 'record': path.name, 'sha256': sha(path)})
            if any(p.stat().st_size > 1024 * 1024 for p in streams):
                raise ValueError('command stream exceeds receipt bound')
            text, error = (p.read_bytes().decode('utf-8', errors='replace') for p in streams)
            assert process.returncode in exits, (label, process.returncode)
            if offline_text:
                assert 'network_calls: none' in text
            return subprocess.CompletedProcess(argv, process.returncode, text, error)
    return Recorder(out)


def ordinary_forms(fixture, pack, target, module, helper, unused_rec, unused_command, write):
    """Ten ordinary forms adjacent to the unchanged eighteen-form oracle."""
    rec = recorder(helper, OUTPUT)
    installed = target / '.aide/scripts/aide_lite.py'
    before = helper.tree_hashes(target)
    rec.installed('ordinary-doctor', target, 'doctor')
    validation = rec.installed('ordinary-validate', target, 'validate')
    assert validation.stdout.splitlines().count('status: PASS') == 1
    count_lines = [line for line in validation.stdout.splitlines() if line.startswith('checks:')]
    assert len(count_lines) == 1
    counts = re.fullmatch(r'checks: (\d+); PASS: (\d+); WARN: (\d+); FAIL: (\d+); OTHER: (\d+)', count_lines[0])
    assert counts and int(counts[4]) == int(counts[5]) == 0
    assert int(counts[1]) == int(counts[2]) + int(counts[3])
    save(OUTPUT / 'ordinary-validation-classification.json', {'warnings': [line for line in validation.stdout.splitlines() if line.startswith('- WARN ')]})
    assert helper.tree_hashes(target) == before
    context = rec.installed('ordinary-context', target, 'context')
    assert 'contents_inline: false' in context.stdout
    assert (target / '.aide/context/latest-context-packet.md').is_file()
    rec.installed('ordinary-pack', target, 'pack', '--task', 'Inspect a disposable target')
    assert (target / '.aide/context/latest-task-packet.md').is_file()
    context_oracle = load('release_context_evidence', CAN / 'context_offline_canary.py')
    evidence = write('.aide/queue/LOCAL-CONTEXT-CANARY-01/evidence/validation.md', context_oracle.evidence_text())
    verified = rec.installed('ordinary-verify', target, 'verify', '--evidence', str(evidence.relative_to(target)))
    assert helper.field(verified.stdout, 'result') in ('PASS', 'WARN')
    assert helper.field(verified.stdout, 'errors') == '0'
    before = helper.tree_hashes(target)
    missing = rec.installed('ordinary-task-inspect', target, 'task', 'inspect', exits=(1,))
    assert 'classification: missing' in missing.stdout
    assert helper.tree_hashes(target) == before
    write('.aide/queue/index.yaml', 'schema_version: aide.queue-index.v0\nitems:\n  - id: LOCAL-CONTEXT-CANARY-01\n    status: running\n    task: .aide/queue/LOCAL-CONTEXT-CANARY-01/task.yaml\n')
    write('.aide/queue/LOCAL-CONTEXT-CANARY-01/task.yaml', 'schema_version: aide.queue-task.v0\nid: LOCAL-CONTEXT-CANARY-01\nstatus: running\n')
    before = helper.tree_hashes(target)
    status = rec.installed('ordinary-task-status', target, 'task', 'status')
    assert 'LOCAL-CONTEXT-CANARY-01' in status.stdout and helper.tree_hashes(target) == before

    stream = fixture / 'synthetic-parent.jsonl'
    child = fixture / 'synthetic-child.jsonl'
    for path, ident, usage in ((stream, '1', 20), (child, '2', 6)):
        path.write_text('\n'.join(json.dumps(item) for item in (
            {'type': 'thread.started', 'thread_id': '00000000-0000-0000-0000-00000000000' + ident},
            {'type': 'turn.started'}, {'type': 'turn.completed', 'usage': {
                'input_tokens': usage, 'cached_input_tokens': 1, 'output_tokens': 2, 'reasoning_output_tokens': 0}})) + '\n', encoding='utf-8')
    usage = json.loads(rec.installed('ordinary-job-usage', target, 'job', 'usage', '--stream', str(stream), '--stream', str(stream)).stdout)
    assert usage['status'] == 'COMPLETE' and usage['completed_turns'] == 1 and usage['duplicate_streams_excluded'] == 1
    attempts = [{'attempt_id': 'parent-1', 'role': 'parent', 'parent_attempt_id': None, 'stream': stream.name, 'stream_sha256': sha(stream)},
                {'attempt_id': 'child-1', 'role': 'child', 'parent_attempt_id': 'parent-1', 'stream': child.name, 'stream_sha256': sha(child)},
                {'attempt_id': 'review-1', 'role': 'review', 'parent_attempt_id': 'parent-1', 'stream': None, 'stream_sha256': None}]
    roster = fixture / 'synthetic-attempt-roster.json'
    save(roster, {'schema': 'aide.codex-exec-attempt-roster.v1', 'work_id': 'delivered-consumer-1', 'attempts': attempts})
    usage = json.loads(rec.installed('ordinary-job-attempts', target, 'job', 'usage', '--attempt-set', str(roster), exits=(2,)).stdout)
    assert usage['status'] == 'PARTIAL' and usage['attempt_count'] == 3
    assert usage['supplied_known_usage_totals']['input_tokens'] == 26
    assert usage['role_known_usage_totals']['parent']['input_tokens'] == 20
    assert usage['role_known_usage_totals']['child']['input_tokens'] == 6
    assert usage['work_usage_totals']['input_tokens'] is None and usage['model_requests'] == 'unknown'
    assert 'attempt_stream_unavailable' in usage['coverage_gaps'] and 'synthetic-child.jsonl' not in json.dumps(usage)
    save(roster, {'schema': 'aide.codex-exec-attempt-roster.v1', 'work_id': 'delivered-consumer-1',
                  'attempts': [attempts[0], dict(attempts[1], parent_attempt_id=['parent-1'])]})
    refused = json.loads(rec.installed('ordinary-job-invalid-parent', target, 'job', 'usage', '--attempt-set', str(roster), exits=(1,)).stdout)
    assert refused['status'] == 'REFUSED'
    raw = json.dumps([{'type': 'message', 'role': 'user', 'content': [{'type': 'text', 'text': 'private-canary-marker'}]}]).encode()
    summary = json.loads(rec.run('ordinary-job-context', installed, target, 'job', 'context', input_data=raw).stdout)
    assert summary['status'] == 'COMPLETE' and 'private-canary-marker' not in json.dumps(summary)
    receipt = module.load_portable_import_receipt(target)
    assert receipt['pack'] == module.import_pack_identity(pack)
    save(OUTPUT / 'revised-installed-ownership.json', {'pack': receipt['pack'], 'receipt': receipt,
        'actual_owned_target_sha256s': {p: sha(target / p) for p in receipt['managed']},
        'installed_cli_sha256': sha(installed), 'core_installed': (target / 'core').exists()})
    assert not (target / 'core').exists()


def lifecycle_forms(work, out, pack, helper, rec):
    """Bounded positive/refusal/recovery checks for the lifecycle public forms."""
    module = helper.load_delivered(pack)
    base = load('release_existing_import_oracle', CAN / 'consumer_canary_base.py')
    second = base.make_synthetic_update(pack, work / 'synthetic-v2', 2, module)
    third = base.make_synthetic_update(pack, work / 'synthetic-v3', 3, module)
    target = work / 'form-target'
    target.mkdir()
    authored = b'# Project-owned guidance\r\n'
    (target / 'AGENTS.md').write_bytes(authored)
    (target / 'project.txt').write_bytes(b'Project-owned bytes.\r\n')
    helper.install(rec, 'forms-install', pack, target)

    def invoke(label, incoming, previous=None, resolution=None, *extra, exits=(0,)):
        args = ['import-pack', '--pack', str(incoming), '--target', str(target), '--mode', 'safe']
        if previous:
            args += ['--from-pack', str(previous)]
        if resolution:
            args += ['--resolve', base.MANAGED, str(resolution)]
        return rec.pack(label, incoming, *args, *extra, exits=exits, offline_text=True)

    def preview_variants(prefix, incoming, previous=None, resolution=None):
        before = helper.tree_hashes(target)
        plan = invoke(prefix + '-plain', incoming, previous, resolution, '--dry-run')
        explained = invoke(prefix + '-explain', incoming, previous, resolution, '--dry-run', '--explain')
        feedback = work / (prefix + '-feedback.json')
        assert not feedback.exists()
        invoke(prefix + '-feedback', incoming, previous, resolution, '--dry-run', '--explain', '--feedback-out', str(feedback))
        packet = json.loads(feedback.read_bytes())
        assert packet['sharing'] == 'manual_only' and packet['network_calls'] is False
        assert packet['explanations'] and all('observed_digest' in p and 'incoming_digest' in p for p in packet['explanations'])
        assert helper.field(plan.stdout, 'status') == helper.field(explained.stdout, 'status') == 'PLANNED'
        assert helper.tree_hashes(target) == before
        save(out / (prefix + '-feedback-packet.json'), packet)
        return helper.field(plan.stdout, 'plan_digest')

    preview_variants('forms-fresh', pack)
    digest = preview_variants('forms-update', second, pack)
    applied = invoke('forms-update-apply', second, pack, None, '--expect-plan', digest)
    assert helper.field(applied.stdout, 'status') == 'APPLIED'
    selected = work / 'selected-resolution.txt'
    selected.write_bytes(b'Project-selected combination.\n')
    (target / base.MANAGED).write_bytes(b'Local direct edit.\n')
    before = helper.tree_hashes(target)
    conflict = invoke('forms-conflict-preview', third, second, None, '--dry-run', exits=(2,))
    assert helper.field(conflict.stdout, 'status') == 'PLANNED_CONFLICT'
    refused = invoke('forms-conflict-refusal', third, second, None, '--expect-plan', helper.field(conflict.stdout, 'plan_digest'), exits=(2,))
    assert helper.field(refused.stdout, 'status') == 'CONFLICT' and helper.tree_hashes(target) == before
    digest = preview_variants('forms-resolved', third, second, selected)
    applied = invoke('forms-resolved-apply', third, second, selected, '--expect-plan', digest)
    assert helper.field(applied.stdout, 'status') == 'APPLIED'
    assert (target / base.MANAGED).read_bytes() == selected.read_bytes()
    receipt = module.load_portable_import_receipt(target)
    assert receipt['managed'][base.MANAGED]['local_overlay']
    assert (target / 'AGENTS.md').read_bytes().startswith(authored)
    assert (target / 'project.txt').read_bytes() == b'Project-owned bytes.\r\n'

    # Fresh-partial semantics come from partial_cli_canary. The complete actual
    # update/resolution recovery oracle runs once below via qualify_successor.
    partial = work / 'fresh-partial-target'
    partial.mkdir()
    project = partial / 'project-owned.txt'
    project.write_bytes(b'Project bytes survive recovery.\r\n')
    original = sha(project)
    interrupted = module.apply_import_pack(pack, partial, fail_after_writes=1)
    save(out / 'fresh-partial-interrupted.json', interrupted)
    assert interrupted['status'] == 'INTERRUPTED' and interrupted['recovery']['classification'] == 'partial'
    args = ['import-pack', '--pack', str(pack), '--target', str(partial), '--mode', 'safe']
    before = helper.tree_hashes(partial)
    ordinary = rec.pack('fresh-partial-ordinary-refusal', pack, *args, exits=(3,))
    wrong = rec.pack('fresh-partial-wrong-plan-refusal', pack, *args, '--recover-partial', '--expect-plan', '0' * 64, exits=(3,))
    assert all(helper.field(p.stdout, 'status') == 'RECOVERY_REQUIRED' for p in (ordinary, wrong))
    assert helper.tree_hashes(partial) == before
    recovered = rec.pack('fresh-partial-exact-recovery', pack, *args, '--recover-partial', '--expect-plan', interrupted['plan_digest'])
    assert helper.field(recovered.stdout, 'status') == 'RECOVERED'
    assert sha(project) == original and not (partial / module.PORTABLE_IMPORT_INTENT_PATH).exists()
    assert module.load_portable_import_receipt(partial)['pack'] == module.import_pack_identity(pack)
    # Existing same-path rollback oracle remains explicitly synthetic.
    old = load('release_existing_lifecycle_oracles', CAN / 'lifecycle_canary_base.py')
    rollback = old.rollback_case(work, pack, module, rec, helper)
    assert rollback['rollback_status'] == 'ROLLED_BACK'
    # Repair the exact original prompt in a clean receipt-owned target.
    repair_target = work / 'repair-target'
    helper.install(rec, 'forms-repair-install', pack, repair_target)
    relative = old.MANAGED
    leaf = repair_target / relative
    expected = leaf.read_bytes()
    leaf.unlink()
    args = ['repair-owned-file', '--pack', str(pack), '--target', str(repair_target), '--path', relative]
    preview = rec.installed('forms-repair-preview', repair_target, *args, '--dry-run')
    digest = helper.field(preview.stdout, 'plan_digest')
    before = helper.tree_hashes(repair_target)
    refused = rec.installed('forms-repair-wrong-plan', repair_target, *args, '--expect-plan', '0' * 64, exits=(3,))
    assert helper.field(refused.stdout, 'status') == 'STALE_PLAN' and helper.tree_hashes(repair_target) == before
    applied = rec.installed('forms-repair-apply', repair_target, *args, '--expect-plan', digest)
    assert helper.field(applied.stdout, 'status') == 'APPLIED' and leaf.read_bytes() == expected
    managed = set(module.load_portable_import_receipt(repair_target)['managed'])
    plan = helper.plan_removal(rec, 'forms-removal-preview', repair_target)
    assert set(plan['candidate_targets']) == managed
    detached = rec.installed('forms-removal-apply', repair_target, 'apply-removal', '--target', str(repair_target), '--expect-plan', plan['plan_digest'], '--json')
    assert json.loads(detached.stdout)['status'] == 'DETACHED'
    helper.assert_detached(repair_target, managed, module)
    save(out / 'lifecycle-form-result.json', {'status': 'PASS', 'synthetic_rollback': rollback, 'actual_pack': module.import_pack_identity(pack)})


def coverage(out, forms):
    witnesses = []
    for path in sorted(out.rglob('*.json')):
        data = json.loads(path.read_bytes())
        if not isinstance(data, dict) or '--repo-root' not in data.get('argv', []):
            continue
        argv = data['argv']
        tail = argv[argv.index('--repo-root') + 2:]
        witnesses.append((path, data, tail))
    rows = []
    for form in forms:
        expected = 2 if form.startswith('job effort ') or form.startswith('job usage --attempt-set') else (1 if form == 'task inspect' else 0)
        found = [(p, d, tail) for p, d, tail in witnesses if d.get('exit_code') == expected and match(form, tail)]
        assert found, ('missing real public-form witness', form)
        path, data, tail = found[0]
        rows.append({'form': form, 'member': path.relative_to(out).as_posix(), 'sha256': sha(path), 'argv': tail, 'exit_code': data['exit_code']})
    assert len(rows) == len(set(r['form'] for r in rows)) == 49
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', required=True, choices=('aide-lite-local-windows-server', 'aide-lite-local-linux', 'aide-lite-local-macos'))
    parser.add_argument('--emit-log', action='store_true')
    args = parser.parse_args()
    scratch = Path(os.environ['RUNNER_TEMP']).resolve(strict=True)
    global OUTPUT, DEADLINE
    DEADLINE = time.monotonic() + 480
    OUTPUT = scratch / 'aide-release-receipts'
    assert not OUTPUT.exists()
    OUTPUT.mkdir()
    lifecycle = load('release_lifecycle_owner', ROOT / 'evals/lite/lifecycle.py')
    result = {'status': 'INCOMPLETE', 'profile_id': args.profile, 'support_claimed': False,
              'model_requests': 0, 'whole_model_usage': 'unknown', 'fixture_retired': False,
              'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'limitations': ['cooperative project mutation ownership', 'seven managed forms unqualified',
                              'no outer-client or native network isolation', 'synthetic usage does not measure actual model cost']}
    work = None
    try:
        assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT).strip()
        subject = json.loads((TASK / 'evidence/revised-build-result.json').read_bytes())
        inputs = json.loads((TASK / 'evidence/hosted-inputs.json').read_bytes())
        assert inputs['workunit'] == TASK.name and inputs['actual_archive_subject'] == subject['assets']
        assert all(sha(ROOT / name) == digest for name, digest in inputs['files'].items()), 'frozen hosted input changed'
        result['input_sha256'] = sha(TASK / 'evidence/hosted-inputs.json')
        profile = next(p for p in subject['identity']['profiles'] if p['profile_id'] == args.profile)
        actual = {'system': platform.system(), 'release': platform.release(), 'version': platform.version(),
                  'machine': platform.machine(), 'runtime': {'implementation': platform.python_implementation(), 'version': platform.python_version()}}
        result.update(environment=actual, declared_environment=profile['environment'], image_version=os.environ.get('ImageVersion'),
                      executable_sha256=sha(Path(sys.executable)), assets=subject['assets'])
        assert actual == profile['environment'], 'host tuple changed; no implicit profile substitution'
        predecessor = subject['identity']['predecessor_matrix'][0]
        pins = {n: v['sha256'] for n, v in subject['assets'].items()}
        pins.update({v['path']: v['sha256'] for v in predecessor['assets']})
        assert all(sha(ROOT / n) == digest for n, digest in pins.items())
        helper = load('release_original_helpers', CAN / 'lifecycle_helper.py')
        work = Path(tempfile.mkdtemp(prefix='case-release-', dir=scratch))
        os.environ.update(AIDE_JOB_TMP=str(work), AIDE_JOB_OUTPUT=str(OUTPUT), TMP=str(work), TEMP=str(work), TMPDIR=str(work))
        tempfile.tempdir = str(work)
        packs = {}
        for version in ('1.1.0', '1.2.0'):
            stable = ROOT / '.aide/release/stable'
            left = helper.extract_zip(stable / f'aide-lite-v{version}.zip', work / ('zip-' + version))
            right = helper.extract_tar(stable / f'aide-lite-v{version}.tar.gz', work / ('tar-' + version))
            assert left == right
            packs[version] = work / ('zip-' + version) / helper.PACK_NAME
        assert len(left) == 879
        additions = load('release_additive_oracle', TASK / 'run_additions.py')
        additions.main(subject_name='revised-build-result.json', before_forms=ordinary_forms, deadline=DEADLINE)
        rec = recorder(helper, OUTPUT)
        lifecycle_forms(work, OUTPUT, packs['1.2.0'], helper, rec)
        cases = lifecycle.qualify_successor(work, OUTPUT, rec, helper, packs['1.1.0'], packs['1.2.0'], subject='aide-lite-v1.2.0-actual-archive')
        assert len(cases) == 2 and all(c['native_acceptance'] for c in cases)
        forms = coverage(OUTPUT, profile['supported_cli_forms'])
        assert len(profile['unqualified_cli_forms']) == 7 and not profile['refused_cli_forms']
        assert all(sha(ROOT / n) == digest for n, digest in pins.items())
        result.update(status='PASS', cases=cases, forms=forms, unqualified_cli_forms=profile['unqualified_cli_forms'])
    except Exception as error:
        result.update(error_type=type(error).__name__, error=str(error), traceback=traceback.format_exc())
    finally:
        if work is not None:
            try:
                # The existing guarded retirement owner accepts only its exact TMP child.
                os.environ['AIDE_JOB_TMP'] = str(scratch)
                retirement = load('release_fixture_retirement', ROOT / '.aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/worker.py')
                retirement.retire_owned_fixture(work)
                result['fixture_retired'] = True
            except Exception as error:
                result.update(status='INCOMPLETE', retirement_error=str(error), retirement_traceback=traceback.format_exc())
        save(OUTPUT / 'release-result.json', result)
        if args.emit_log:
            assert all(p.is_file() for p in OUTPUT.iterdir()), 'receipt transport requires flat ordinary files'
            save(OUTPUT / 'receipt-index.json', {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)}
                                              for p in OUTPUT.iterdir() if p.is_file()})
            lifecycle.emit_receipts(OUTPUT)
    print(json.dumps({k: result[k] for k in ('status', 'profile_id', 'fixture_retired', 'support_claimed')}))
    return 0 if result['status'] == 'PASS' and result['fixture_retired'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
