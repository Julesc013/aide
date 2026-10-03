"""Task-local host qualification; allocation/lifetime/cleanup stay with AIDE."""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

# The supervising interpreter is outside the worker filesystem profile. Its
# trusted imports must never create caches in the frozen execution component.
sys.dont_write_bytecode = True

TASK = Path(__file__).resolve().parent
REPO = TASK.parents[2]
SUBJECT = TASK / 'subject.json'
CONFIG = REPO / '.aide.local/execution.json'
MANIFEST = REPO / '.aide.local/session-containment-01-job.json'
RUN_CONFIG = REPO / '.aide.local/session-containment-01-execution.json'


def sha(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def load_runtime(subject):
    for relative, expected in subject['trusted_files'].items():
        if sha(REPO / relative) != expected:
            raise RuntimeError('frozen execution component changed: ' + relative)
    frozen = REPO / subject['runtime_root']
    sys.path.insert(0, str(frozen))
    from core.execution import managed_workspace as runtime
    if not Path(runtime.__file__).resolve().is_relative_to(frozen):
        raise RuntimeError('runtime did not load from the pinned export')
    return runtime


def logical_usage(root, max_entries=100000, seconds=20):
    """Read only the selected ordinary tree, with explicit incomplete coverage."""
    pending = [Path(root)]
    total = entries = 0
    began = time.monotonic()
    while pending:
        if time.monotonic() - began > seconds:
            return {'complete': False, 'logical_bytes': total, 'entries': entries}
        current = pending.pop()
        with os.scandir(current) as iterator:
            for entry in iterator:
                entries += 1
                if entries > max_entries or time.monotonic() - began > seconds:
                    return {'complete': False, 'logical_bytes': total, 'entries': entries}
                info = entry.stat(follow_symlinks=False)
                if getattr(info, 'st_file_attributes', 0) & 1024 or entry.is_symlink():
                    raise RuntimeError('linked entry in the observed resource root')
                if entry.is_dir(follow_symlinks=False):
                    pending.append(Path(entry.path))
                else:
                    total += info.st_size
    return {'complete': True, 'logical_bytes': total, 'entries': entries}


def retention_admission(root, pool_limit, limits):
    observed = logical_usage(root, max_entries=limits['max_files'])
    reservation = limits['retained_bytes'] + limits['log_bytes'] + 1024 * 1024
    if not observed['complete']:
        raise RuntimeError('aggregate retention observation incomplete')
    if observed['logical_bytes'] + reservation > pool_limit:
        raise RuntimeError('aggregate retained budget cannot admit this attempt')
    return {'observed': observed, 'reserved_bytes': reservation,
            'pool_limit_bytes': pool_limit}


def worker(subject, real_task):
    runtime = load_runtime(subject)
    job_id = os.environ['AIDE_JOB_ID']
    temporary = Path(os.environ['AIDE_JOB_TMP'])
    output = Path(os.environ['AIDE_JOB_OUTPUT'])
    identity = ctypes.create_unicode_buffer(256)
    identity_size = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(identity_size)):
        raise ctypes.WinError()
    result = {'schema': 'aide.session-containment.observation.v1',
              'job_id': job_id, 'windows_identity': identity.value,
              'model_calls': 0, 'real_task_requested': real_task}
    try:
        result['named_job_membership'] = runtime.WindowsJobHost().contains_current_process(job_id)
    except OSError as exc:
        result['named_job_membership'] = None
        result['membership_error'] = {'type': type(exc).__name__, 'winerror': exc.winerror}
    allowed = temporary / 'allowed.txt'
    try:
        allowed.write_text('owned fixture\n', encoding='utf-8')
        result['allowed_write'] = allowed.read_text(encoding='utf-8') == 'owned fixture\n'
    except OSError as exc:
        result['allowed_write'] = False
        result['allowed_write_error'] = {'type': type(exc).__name__, 'winerror': exc.winerror}
    forbidden = temporary / 'forbidden' / 'must-not-exist.txt'
    try:
        forbidden.write_bytes(b'negative fixture')
        result['unapproved_write_denied'] = False
    except PermissionError:
        result['unapproved_write_denied'] = True
    child = subprocess.run([sys.executable, '-B', '-c',
        'import pathlib,sys\np=pathlib.Path(sys.argv[1])\n'
        'try: p.write_bytes(b"child fixture")\n'
        'except PermissionError: sys.exit(19)\n', str(forbidden.with_name('child.txt'))],
        capture_output=True, timeout=15)
    result['child_unapproved_write_denied'] = child.returncode == 19
    try:
        with CONFIG.open('rb') as stream:
            stream.read(1)
        result['supervisor_config_read_denied'] = False
    except PermissionError:
        result['supervisor_config_read_denied'] = True
    try:
        with CONFIG.open('r+b'):
            pass
        result['supervisor_config_write_denied'] = False
    except PermissionError:
        result['supervisor_config_write_denied'] = True
    result['filesystem_profile_passed'] = all(result[key] is True for key in (
        'allowed_write', 'unapproved_write_denied', 'child_unapproved_write_denied',
        'supervisor_config_read_denied', 'supervisor_config_write_denied'))
    result['write_boundary_passed'] = all(result[key] is True for key in (
        'allowed_write', 'unapproved_write_denied', 'child_unapproved_write_denied',
        'supervisor_config_write_denied'))
    # Preserve the failed read-isolation result. This repository-only validation
    # has no private inputs or model/network step and can qualify its narrower
    # write/process boundary without claiming the requested full profile works.
    result['preflight_passed'] = (result['write_boundary_passed']
        and result['named_job_membership'] is True
        and identity.value.casefold() != 'blackglass-win1\\jules')
    if result['preflight_passed']:
        git = subprocess.run([subject['git'], '-c', 'safe.directory=' + str(REPO),
            '-C', str(REPO), 'diff', '--check'], capture_output=True, timeout=30)
        result['git_diff_check_exit'] = git.returncode
        if git.returncode:
            result['git_failure'] = git.stderr.decode('utf-8', errors='replace')[:1024]
        if real_task and git.returncode == 0:
            import unittest
            sys.path.insert(0, str(REPO / '.aide/scripts/tests'))
            from test_managed_workspace import ManagedWorkspaceTests
            cases = ('test_disk_and_memory_refusal_allocate_nothing',
                'test_concurrent_reservation_refused_by_os_lock',
                'test_missing_pool_wrong_volume_and_escape_have_no_fallback',
                'test_interrupted_retirement_recovers_without_losing_collected_output')
            checks = unittest.TextTestRunner(verbosity=1).run(unittest.TestSuite(
                ManagedWorkspaceTests(name) for name in cases))
            result['existing_resource_tests'] = {'run': checks.testsRun,
                'failures': len(checks.failures), 'errors': len(checks.errors),
                'skipped': len(checks.skipped), 'passed': checks.wasSuccessful()}
            fixture = temporary / 'aggregate-fixture'
            fixture.mkdir()
            (fixture / 'retained.txt').write_bytes(b'12345678')
            limits = {'retained_bytes': 8, 'log_bytes': 8, 'max_files': 10}
            tight = 1024 * 1024 + 24
            retention_admission(fixture, tight, limits)
            try:
                retention_admission(fixture, tight - 1, limits)
                result['aggregate_budget_boundary_passed'] = False
            except RuntimeError:
                result['aggregate_budget_boundary_passed'] = True
            # Keep the original acceptance command and stream into the owner's
            # bounded retained pipes, not into the controller's context.
            environment = dict(os.environ, GIT_CONFIG_COUNT='1',
                GIT_CONFIG_KEY_0='safe.directory', GIT_CONFIG_VALUE_0=str(REPO))
            started = time.monotonic()
            if checks.wasSuccessful() and result['aggregate_budget_boundary_passed']:
                validation = subprocess.run([sys.executable, '-B',
                    str(REPO / '.aide/scripts/aide_lite.py'), 'validate'],
                    cwd=REPO, env=environment, timeout=900)
                result['validation_exit'] = validation.returncode
            result['validation_seconds'] = round(time.monotonic() - started, 3)
    result['workload_passed'] = (result['preflight_passed']
        and result.get('git_diff_check_exit') == 0
        and (not real_task or result.get('validation_exit') == 0))
    result['result'] = ('PASS' if result['workload_passed'] and result['filesystem_profile_passed']
        else 'PARTIAL' if result['workload_passed'] else 'FAIL')
    (output / 'scope-result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result), flush=True)
    return 0 if result['workload_passed'] else 1


def supervise(subject, real_task):
    runtime = load_runtime(subject)
    for key in ('codex', 'python', 'git'):
        if sha(subject[key]) != subject[key + '_sha256']:
            raise RuntimeError('registered executable changed: ' + key)
    if sha(CONFIG) != subject['local_config_sha256']:
        raise RuntimeError('local execution envelope changed')
    config, roots, working = runtime.load_config(CONFIG)
    if runtime.inspect(CONFIG)['active'] is not None:
        raise RuntimeError('existing job must be reconciled; no duplicate allocation')
    before = {key: logical_usage(path) for key, path in roots.items()}
    if not all(value['complete'] for value in before.values()):
        raise RuntimeError('bounded aggregate observation incomplete; no allocation')
    # A finite, narrower per-attempt envelope. The original selection is intact;
    # all locations, volume identities, memory and process bounds are inherited.
    effective = json.loads(json.dumps(config))
    effective['limits']['scratch_bytes'] = min(config['limits']['scratch_bytes'], 32 * 1024 * 1024)
    effective['limits']['retained_bytes'] = min(config['limits']['retained_bytes'], 64 * 1024)
    effective['limits']['runtime_seconds'] = min(config['limits']['runtime_seconds'], 900)
    RUN_CONFIG.write_text(json.dumps(effective, indent=2) + '\n', encoding='utf-8')
    pool_limit = config['limits']['retained_bytes']
    admitted = {}

    class ScopedHost(runtime.WindowsJobHost):
        def run(self, argv, **kwargs):
            # runtime.run holds the existing shared estate lock here. No second
            # allocator or independent reservation can race this same pool.
            admitted.update(retention_admission(roots['retained'], pool_limit, effective['limits']))
            scratch = Path(kwargs['output_dir']).parent
            denied = scratch / 'tmp/forbidden'
            denied.mkdir()
            rules = {':root': 'deny', ':minimal': 'read', str(REPO): 'read',
                str(REPO / '.aide.local'): 'deny',
                str(CONFIG): 'deny',
                str(Path(subject['python']).parent): 'read',
                str(Path(subject['git']).parent.parent): 'read',
                str(Path(subject['codex']).parent): 'read',
                str(scratch): 'read', str(scratch / 'tmp'): 'write',
                str(scratch / 'cache'): 'write', str(scratch / 'output'): 'write',
                str(denied): 'read'}
            profile = 'aide_qualification_' + kwargs['job_id']
            inline = '{' + ','.join(json.dumps(k) + '=' + json.dumps(v) for k, v in rules.items()) + '}'
            scoped = [subject['codex'], 'sandbox', '-P', profile,
                '-c', 'permissions.' + profile + '.filesystem=' + inline,
                '-c', 'permissions.' + profile + '.network.enabled=false',
                '--', *argv]
            (scratch / 'output/effective-scope.json').write_text(json.dumps({
                'profile': profile, 'filesystem': rules, 'network_enabled': False,
                'outer_session_contained': False}, indent=2) + '\n', encoding='utf-8')
            return super().run(scoped, **kwargs)

    def git(*args):
        return subprocess.run([subject['git'], '-C', str(REPO), *args],
            capture_output=True, text=True, timeout=15, check=True).stdout.strip()
    inputs = {str(Path(__file__).relative_to(REPO)).replace('\\', '/'): sha(__file__),
              str(SUBJECT.relative_to(REPO)).replace('\\', '/'): sha(SUBJECT),
              '.aide/scripts/aide_lite.py': sha(REPO / '.aide/scripts/aide_lite.py'),
              '.aide/scripts/tests/test_managed_workspace.py': sha(REPO / '.aide/scripts/tests/test_managed_workspace.py'),
              **subject['trusted_files']}
    job = {'schema': 'aide.maintainer-job.v1', 'owner': 'session-containment-01',
        'workunit': 'AIDE-SESSION-CONTAINMENT-01', 'adapter': 'python',
        'source_commit': git('rev-parse', 'HEAD'), 'source_tree': git('rev-parse', 'HEAD^{tree}'),
        'cwd': str(REPO), 'argv': [subject['python'], str(Path(__file__).relative_to(REPO)),
            '--worker', *(['--real-task'] if real_task else [])],
        'executable_sha256': subject['python_sha256'], 'inputs': inputs}
    MANIFEST.write_text(json.dumps(job, indent=2) + '\n', encoding='utf-8')
    record = runtime.run(RUN_CONFIG, job, host=ScopedHost())
    after = {key: logical_usage(path) for key, path in roots.items()}
    summary = {'schema': 'aide.session-containment.attempt.v1',
        'job_id': record['job_id'], 'result': record['result'],
        'phase': record['phase'], 'scratch_absent': record.get('scratch_absent'),
        'reservation_released': record.get('reservation_released'),
        'retained': record.get('retained'), 'peaks': record['peaks'],
        'aggregate_before': before, 'aggregate_after': after,
        'aggregate_retention_admission': admitted,
        'effective_limits': effective['limits'],
        'effective_config_sha256': sha(RUN_CONFIG),
        'aggregate_hard_cap': False, 'outer_session_contained': False,
        'subject_sha256': sha(SUBJECT), 'manifest_sha256': sha(MANIFEST),
        'local_config_unchanged': sha(CONFIG) == subject['local_config_sha256']}
    evidence = TASK / 'evidence' / ('attempt-' + record['job_id'] + '.json')
    evidence.parent.mkdir(exist_ok=True)
    evidence.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary), flush=True)
    return 0 if record['result'].get('exit_code') == 0 and record.get('scratch_absent') else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--real-task', action='store_true')
    args = parser.parse_args()
    subject = json.loads(SUBJECT.read_text(encoding='utf-8'))
    raise SystemExit(worker(subject, args.real_task) if args.worker else supervise(subject, args.real_task))
