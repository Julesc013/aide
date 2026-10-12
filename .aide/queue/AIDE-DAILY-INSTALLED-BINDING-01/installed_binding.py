"""Scratch-only installed consumer qualification through existing Lite owners."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

TASK = Path(__file__).resolve().parent
REPO = TASK.parents[2]
SELECTED = 'PROJECT-TASK-17'
OTHER = 'AIDE-OTHER-01'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def main():
    inputs = json.loads((TASK / 'evidence/installed-inputs.json').read_text(encoding='utf-8'))
    scratch = Path(os.environ['AIDE_JOB_TMP'])
    output = Path(os.environ['AIDE_JOB_OUTPUT'])
    stages = []
    environment = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    environment.update(GIT_CONFIG_GLOBAL='NUL', GIT_CONFIG_SYSTEM='NUL',
                       GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1')
    environment.pop('PYTHONPATH', None)
    git = inputs['git_executable']
    assert sha(git) == inputs['git_executable_sha256']
    assert Path(shutil.which('git')).resolve() == Path(git).resolve()

    def invoke(label, argv, cwd, expected=0):
        out, err = output / (label + '.stdout'), output / (label + '.stderr')
        began = time.monotonic()
        write(output / 'active-stage.json', json.dumps({'stage': label, 'argv': argv,
              'started_at_unix_ns': time.time_ns(), 'status': 'INCOMPLETE'}) + '\n')
        with out.open('xb') as stdout, err.open('xb') as stderr:
            completed = subprocess.run(argv, cwd=cwd, env=environment,
                                       stdin=subprocess.DEVNULL, stdout=stdout,
                                       stderr=stderr, timeout=60)
        record = {'stage': label, 'exit_code': completed.returncode,
                  'elapsed_seconds': time.monotonic() - began,
                  'stdout_bytes': out.stat().st_size, 'stdout_sha256': sha(out),
                  'stderr_bytes': err.stat().st_size, 'stderr_sha256': sha(err)}
        stages.append(record)
        write(output / 'stages.json', json.dumps(stages, indent=2) + '\n')
        write(output / 'active-stage.json', json.dumps({'stage': label, 'status': 'TERMINAL',
              'exit_code': completed.returncode}) + '\n')
        print(json.dumps(record), flush=True)
        if (expected == 'nonzero' and completed.returncode == 0
                or expected != 'nonzero' and completed.returncode != expected):
            raise AssertionError(label + ': unexpected exit; original full streams retained')
        return out.read_text(encoding='utf-8', errors='replace'), err.read_text(encoding='utf-8', errors='replace')

    # Reuse the previously qualified read-only ownership oracle, never its reset.
    oracle = REPO / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py'
    spec = importlib.util.spec_from_file_location('installed_pack_ownership', oracle)
    ownership = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ownership)
    observed = ownership.observe()
    assert {k: v['sha256'] for k, v in observed['files'].items()} == inputs['pack_sha256s']
    assert observed['total_bytes'] == inputs['pack_bytes']
    source = REPO / inputs['pack_ref']
    pack = scratch / 'consumer-pack'
    shutil.copytree(source, pack)
    copied = {p.relative_to(pack).as_posix(): sha(p) for p in pack.rglob('*') if p.is_file()}
    assert copied == inputs['pack_sha256s']
    exported_cli = pack / 'files/.aide/scripts/aide_lite.py'
    assert sha(exported_cli) == inputs['shipped_helper_sha256']
    tests = pack / 'files/.aide/scripts/tests/test_task_binding.py'
    assert sha(tests) == inputs['shipped_regression_sha256']
    _, test_log = invoke('shipped-original-17', [sys.executable, '-I', '-B', '-m',
                           'unittest', 'discover', '-s', str(tests.parent),
                           '-p', tests.name, '-v'], scratch)
    assert 'Ran 17 tests' in test_log and '\nOK\n' in test_log
    assert 'skipped=' not in test_log and 'FAILED' not in test_log

    target = scratch / 'project'
    target.mkdir()
    sentinel = b'Project authored instructions and customization remain owned here.\n'
    (target / 'AGENTS.md').write_bytes(sentinel)
    write(target / 'source/selected/helper.py', 'value = 1\n')
    write(target / 'source/other/helper.py', 'value = 1\n')
    write(target / 'source/forbidden/helper.py', 'value = 1\n')
    authored = target / 'customization.txt'
    authored.write_bytes(b'target-owned customization\n')
    invoke('safe-import', [sys.executable, '-I', '-B', str(exported_cli),
                           '--repo-root', str(target), 'import-pack', '--pack',
                           str(pack), '--target', str(target)], target)
    cli = target / '.aide/scripts/aide_lite.py'
    assert sha(cli) == inputs['shipped_helper_sha256']
    assert (target / 'AGENTS.md').read_bytes().startswith(sentinel)
    authored_after_import = sha(target / 'AGENTS.md')
    customization_sha = sha(authored)
    queue = target / '.aide/queue'
    index = 'schema_version: aide.queue-index.v0\nitems:\n'
    for identity, paths in ((SELECTED, ['source/selected/**']), (OTHER, ['source/**'])):
        index += ('  - id: ' + identity + '\n    status: running\n    task: '
                  + '.aide/queue/' + identity + '/task.yaml\n')
        text = ('id: ' + identity + '\ntitle: Useful bounded fixture change\n'
                'scope:\n  allowed_paths:\n'
                + ''.join('    - ' + value + '\n' for value in paths)
                + '    - .aide/context/**\n    - .aide/memory/**\n    - .aide/reports/**\n'
                + '    - .aide/queue/' + identity + '/evidence/**\n'
                + '  forbidden_paths:\n    - .aide.local/**\n    - source/forbidden/**\n')
        write(queue / identity / 'task.yaml', text)
        write(queue / identity / 'status.yaml', 'schema_version: aide.queue-status.v0\n'
              + 'task_id: ' + identity + '\nstatus: running\nresult: PENDING\n')
    write(queue / 'index.yaml', index)
    old_report = target / '.aide/reports/task-os-next-plan.md'
    report_sentinel = 'Older retained report snapshot\n'
    write(old_report, report_sentinel)
    hooks = scratch / 'empty-hooks'
    hooks.mkdir()
    git_prefix = [git, '-c', 'core.hooksPath=' + str(hooks), '-c', 'commit.gpgSign=false',
                  '-c', 'user.name=AIDE Fixture', '-c', 'user.email=fixture@invalid']
    invoke('fixture-git-init', git_prefix + ['init'], target)
    invoke('fixture-git-add', git_prefix + ['add', '--', '.'], target)
    invoke('fixture-git-baseline', git_prefix + ['commit', '-m', 'Disposable consumer baseline'], target)

    def command(label, *parts, expected=0):
        return invoke(label, [sys.executable, '-I', '-B', str(cli),
                              '--repo-root', str(target), *parts], target, expected)

    def verification(label, expected=0):
        relative = '.aide/reports/' + label + '.md'
        stdout, _ = command(label, 'verify', '--changed-files', '--write-report',
                            relative, expected=expected)
        report_path = target / relative
        data = report_path.read_bytes()
        with (output / (label + '.verification.md')).open('xb') as retained:
            retained.write(data)
        return stdout, data.decode('utf-8')

    command('named-packet', 'pack', '--task', SELECTED)
    packet = target / '.aide/context/latest-task-packet.md'
    text = packet.read_text(encoding='utf-8')
    assert 'task_id: ' + SELECTED in text and 'source/selected/**' in text
    allowed = text.split('## ALLOWED_PATHS\n', 1)[1].split('## FORBIDDEN_PATHS', 1)[0]
    assert 'source/**' not in allowed and '<fill' not in allowed
    write(target / 'source/selected/helper.py', 'value = 2\n')
    positive, positive_report = verification('selected-edit-verification')
    assert 'result: PASS' in positive
    assert '- allowed: `source/selected/helper.py`' in positive_report
    write(target / 'source/other/helper.py', 'value = 2\n')
    unknown, unknown_report = verification('undeclared-edit-advisory')
    assert 'result: FAIL' not in unknown and 'errors: 0' in unknown.splitlines()
    assert '- unknown: `source/other/helper.py`' in unknown_report
    warnings = unknown_report.split('## WARNINGS', 1)[1].split('## ERRORS', 1)[0]
    assert any('diff_scope:' in line and '`source/other/helper.py`' in line
               for line in warnings.splitlines())
    write(target / 'source/other/helper.py', 'value = 1\n')
    write(target / 'source/forbidden/helper.py', 'value = 2\n')
    forbidden, forbidden_report = verification('forbidden-edit-refusal', expected='nonzero')
    assert 'result: FAIL' in forbidden and '- forbidden: `source/forbidden/helper.py`' in forbidden_report
    errors = forbidden_report.split('## ERRORS', 1)[1].split('## EVIDENCE_REFS', 1)[0]
    assert any('diff_scope:' in line and '`source/forbidden/helper.py`' in line
               for line in errors.splitlines())
    write(target / 'source/forbidden/helper.py', 'value = 1\n')
    original_packet = packet.read_bytes()
    packet.write_bytes(original_packet + b'\n## EVIDENCE\n\nOld Q20 example is context only.\n')
    current, _ = command('incidental-Q-identity', 'task', 'inspect')
    assert 'task_id: ' + SELECTED in current.splitlines()
    snapshot_path = target / '.aide/context/repo-snapshot.json'
    assert snapshot_path.is_file()
    snapshot_sha = sha(snapshot_path)
    before_unknown = packet.read_bytes()
    command('unknown-named-task-refusal', 'pack', '--task', 'AIDE-MISSING-01', expected='nonzero')
    assert packet.read_bytes() == before_unknown
    assert sha(snapshot_path) == snapshot_sha
    invalid_cases = (('', 'invalid declared task identity'),
                     ('../../outside', 'invalid declared task identity'),
                     ('AIDE-MISSING-01', 'declared task is missing: AIDE-MISSING-01'),
                     (SELECTED + '\nphase: ' + OTHER, 'conflicting declared task identities'))
    valid_text = before_unknown.decode('utf-8')
    assert valid_text.count('task_id: ' + SELECTED + '\n') == 1
    for number, (identity, cause) in enumerate(invalid_cases):
        write(packet, valid_text.replace('task_id: ' + SELECTED + '\n',
                                        'task_id: ' + identity + '\n', 1))
        _, invalid_report = verification('invalid-identity-' + str(number), expected='nonzero')
        errors = invalid_report.split('## ERRORS', 1)[1].split('## EVIDENCE_REFS', 1)[0]
        assert '- diff_scope: ' + cause in errors
    packet.write_bytes(before_unknown)
    task_path = queue / SELECTED / 'task.yaml'
    task_bytes = task_path.read_bytes()
    task_path.write_bytes(task_bytes.replace(('id: ' + SELECTED).encode(), ('id: ' + OTHER).encode(), 1))
    _, mismatch_report = verification('mismatched-owner-refusal', expected='nonzero')
    errors = mismatch_report.split('## ERRORS', 1)[1].split('## EVIDENCE_REFS', 1)[0]
    assert '- diff_scope: declared task identity mismatch: ' + SELECTED in errors
    task_path.write_bytes(task_bytes)
    inspected, _ = command('task-os-read-only', 'task', 'next-plan')
    assert 'non_mutating: true' in inspected and 'lifecycle_apply_authorized: false' in inspected
    assert old_report.read_text(encoding='utf-8') == report_sentinel
    projected, _ = command('task-os-explicit-report', 'task', 'next-plan', '--write-report')
    assert 'non_mutating: false' in projected and 'report: .aide/reports/task-os-next-plan.md' in projected
    assert old_report.read_text(encoding='utf-8') != report_sentinel
    command('stable-packet-before-resume', 'pack', '--task', SELECTED)
    stable_packet = packet.read_bytes()
    completed_record = queue / SELECTED / 'evidence/completed-checks.json'
    write(completed_record, json.dumps({'task_id': SELECTED, 'shipped_regression_count': 17,
                                      'completed': ['selected-edit', 'refusals']}) + '\n')
    completed_sha = sha(completed_record)
    command('selected-default-review-evidence', 'review-pack')
    review_text = (target / '.aide/context/latest-review-packet.md').read_text(encoding='utf-8')
    assert '.aide/queue/' + SELECTED + '/evidence' in review_text
    assert '.aide/queue/' + OTHER + '/evidence' not in review_text
    resumed, _ = command('separate-process-resume-inspection', 'task', 'inspect')
    assert 'task_id: ' + SELECTED in resumed.splitlines()
    command('separate-process-resume-packet', 'pack', '--task', SELECTED)
    assert packet.read_bytes() == stable_packet and sha(completed_record) == completed_sha
    command('separate-process-resume-verification', 'verify', '--changed-files')
    assert sha(target / 'AGENTS.md') == authored_after_import and sha(authored) == customization_sha
    summary = {'schema': 'aide.installed-task-binding-qualification.v1', 'status': 'PASS',
               'job_id': os.environ['AIDE_JOB_ID'], 'source_helper_sha256': sha(cli),
               'original_regression_tests': 17, 'task_id': SELECTED,
               'shipped_import_no_source_fallback': True, 'real_Git_scope_verified': True,
               'undeclared_path_warns_without_grant': True, 'explicit_forbidden_path_refuses': True,
               'valid_packet_snapshot_preserved_on_unknown_task': True,
               'authored_content_preserved': True, 'same_fixture_workunit_resumed': True,
               'default_review_same_selected_task': True, 'task_os_inspection_behavior_preserved': True,
               'completed_result_sha256': completed_sha, 'stages': len(stages),
               'general_interruption_recovery_qualified': False,
               'outer_containment_qualified': False, 'model_requests': 0,
               'whole_task_model_usage': 'unknown', 'real_target_activated': False}
    write(output / 'qualification.json', json.dumps(summary, sort_keys=True, indent=2) + '\n')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
