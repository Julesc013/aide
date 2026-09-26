"""Maintainer job storage admission for the existing Windows process owner.

One estate-wide lock serializes reservations and heavy commands. This is an
application reservation with monitored disk thresholds, not a filesystem or
credential sandbox. The Windows host enforces process/memory/log limits.
No configured pool means no allocation; inspection never writes reports.
"""
from __future__ import annotations

from contextlib import contextmanager
import ctypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import time
import uuid

from core.runtime.continuous_worker.windows_job import WindowsJobHost, sanitized_environment


class WorkspaceRefused(ValueError):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def file_digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''): value.update(chunk)
    return value.hexdigest()


def ordinary(path, *, directory=False):
    info = Path(path).lstat()
    if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
        raise WorkspaceRefused('link/reparse path refused')
    if directory and not stat.S_ISDIR(info.st_mode):
        raise WorkspaceRefused('directory required')
    if not directory and (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1):
        raise WorkspaceRefused('ordinary single-link file required')
    return info


def root_path(value):
    path = Path(value)
    if not path.is_absolute() or '..' in path.parts or path == Path(path.anchor):
        raise WorkspaceRefused('absolute bounded root required')
    for ancestor in reversed((path, *path.parents)):
        ordinary(ancestor, directory=True)
    if path.resolve() != path:
        raise WorkspaceRefused('root alias refused')
    return path


def read_json(path):
    info = ordinary(path)
    if info.st_size > 1024 * 1024:
        raise WorkspaceRefused('record too large')
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, value):
    path = Path(path)
    if os.path.lexists(path):
        ordinary(path)
    temporary = path.with_name(path.name + '.next')
    with temporary.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, path)


def volume_identity(path):
    if os.name != 'nt':
        return 'device:' + str(Path(path).stat().st_dev)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    for name in ('GetVolumePathNameW', 'GetVolumeNameForVolumeMountPointW'):
        fn = getattr(kernel, name)
        fn.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32]
        fn.restype = ctypes.c_int
    mount, identity = ctypes.create_unicode_buffer(32768), ctypes.create_unicode_buffer(128)
    if not kernel.GetVolumePathNameW(str(path), mount, len(mount)) or not kernel.GetVolumeNameForVolumeMountPointW(mount.value, identity, len(identity)):
        raise ctypes.WinError(ctypes.get_last_error())
    return identity.value.casefold()


def memory_capacity():
    if os.name != 'nt':
        raise WorkspaceRefused('memory observation is currently Windows-qualified only')
    from ctypes import wintypes as W
    class Memory(ctypes.Structure):
        _fields_ = [('length', W.DWORD), ('load', W.DWORD)] + [(n, ctypes.c_ulonglong) for n in
            ('physical_total', 'physical_free', 'page_total', 'page_free', 'virtual_total', 'virtual_free', 'extended')]
    class Performance(ctypes.Structure):
        _fields_ = [('size', W.DWORD)] + [(n, ctypes.c_size_t) for n in
            ('commit', 'commit_limit', 'commit_peak', 'physical_total', 'physical_free', 'system_cache',
             'kernel_total', 'kernel_paged', 'kernel_nonpaged', 'page_size')] + [(n, W.DWORD) for n in ('handles', 'processes', 'threads')]
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    psapi = ctypes.WinDLL('psapi', use_last_error=True)
    mem, perf = Memory(), Performance(); mem.length = ctypes.sizeof(mem); perf.size = ctypes.sizeof(perf)
    if not kernel.GlobalMemoryStatusEx(ctypes.byref(mem)) or not psapi.GetPerformanceInfo(ctypes.byref(perf), ctypes.sizeof(perf)):
        raise ctypes.WinError(ctypes.get_last_error())
    return {'physical_free': mem.physical_free, 'commit_free': (perf.commit_limit - perf.commit) * perf.page_size}


def load_config(path):
    config = read_json(path)
    if config.get('schema') != 'aide.managed-workspace.local.v1':
        raise WorkspaceRefused('unsupported local workspace config')
    roots = {key: root_path(config['roots'][key]) for key in ('scratch', 'retained', 'control')}
    for key, root in roots.items():
        if volume_identity(root) != config['volume_ids'][key].casefold():
            raise WorkspaceRefused('configured volume identity mismatch: ' + key)
    for key, root in roots.items():
        if any(key != other and (root.is_relative_to(value) or value.is_relative_to(root)) for other, value in roots.items()):
            raise WorkspaceRefused('storage roots must be distinct and nonoverlapping')
    for key in ('disk_reserve_bytes', 'physical_reserve_bytes', 'commit_reserve_bytes',
                'scratch_bytes', 'retained_bytes', 'memory_bytes', 'log_bytes', 'runtime_seconds', 'processes', 'max_files'):
        value = config['limits'][key]
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise WorkspaceRefused('finite positive limit required: ' + key)
    if config['limits']['runtime_seconds'] > 86400 or config['limits']['processes'] > 128:
        raise WorkspaceRefused('runtime/process limit outside maintainer profile')
    working = [root_path(value) for value in config['working_roots']]
    if not working or any(root.is_relative_to(work) for root in roots.values() for work in working):
        raise WorkspaceRefused('storage inside working source refused')
    return config, roots, working


@contextmanager
def estate_lock(control):
    # All admitted campaign workspaces use this one configured control root.
    # OS handle locking survives PID reuse and releases on interpreter death.
    path = control / 'admission.lock'
    if os.path.lexists(path):
        ordinary(path)
    fd = os.open(path, os.O_CREAT | os.O_RDWR | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise WorkspaceRefused('unsafe admission lock')
        if info.st_size == 0:
            os.write(fd, b'0')
        os.lseek(fd, 0, os.SEEK_SET)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise WorkspaceRefused('another heavy job owns the estate reservation') from exc
        yield
    finally:
        os.close(fd)


def capacity(roots):
    disks = {volume_identity(root): shutil.disk_usage(root).free for root in roots.values()}
    return {'disk_free': disks, **memory_capacity()}


def admission(config, roots, observed):
    limits = config['limits']; reservations = {}
    for key, amount in (('scratch', limits['scratch_bytes'] + limits['log_bytes']),
                        ('retained', limits['retained_bytes'] + limits['log_bytes']), ('control', 1024 * 1024)):
        identity = volume_identity(roots[key])
        reservations[identity] = reservations.get(identity, 0) + amount
    for identity, amount in reservations.items():
        if observed['disk_free'][identity] - amount < limits['disk_reserve_bytes']:
            raise WorkspaceRefused('disk reservation would consume free-space reserve')
    for resource, reserve in (('physical_free', 'physical_reserve_bytes'), ('commit_free', 'commit_reserve_bytes')):
        if observed[resource] - limits['memory_bytes'] < limits[reserve]:
            raise WorkspaceRefused('memory reservation would consume ' + resource)
    return reservations


def tree_usage(root, *, maximum, max_files):
    total = count = 0; pending = [root]
    while pending:
        directory = pending.pop(); ordinary(directory, directory=True)
        with os.scandir(directory) as entries:
            for entry in entries:
                # Windows DirEntry's cached enumeration omits link/device
                # identity (st_nlink=0). Use lstat for ownership validation.
                info = Path(entry.path).lstat()
                count += 1
                if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                    raise WorkspaceRefused('linked job member preserved for recovery')
                if stat.S_ISDIR(info.st_mode):
                    pending.append(Path(entry.path))
                elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
                    total += info.st_size
                else:
                    raise WorkspaceRefused('unexpected job member preserved for recovery')
                if total > maximum or count > max_files:
                    raise WorkspaceRefused('workspace size/file threshold exceeded')
    return total


def validate_job(job, working):
    if job.get('schema') != 'aide.maintainer-job.v1' or not job.get('owner') or not job.get('workunit'):
        raise WorkspaceRefused('identified maintainer job required')
    cwd = root_path(job['cwd'])
    if cwd not in working:
        raise WorkspaceRefused('working root is not approved')
    argv = job['argv']
    if not isinstance(argv, list) or not argv or any(not isinstance(v, str) or '\0' in v for v in argv):
        raise WorkspaceRefused('literal argv required')
    exe = Path(argv[0]); ordinary(exe)
    if not exe.is_absolute():
        raise WorkspaceRefused('absolute executable required')
    if file_digest(exe) != job['executable_sha256']:
        raise WorkspaceRefused('executable changed')
    if job.get('adapter') != 'python' or exe.name.casefold() not in ('python.exe', 'python', 'python3'):
        raise WorkspaceRefused('only explicit Python placement adapter is qualified')
    if len(argv) < 2 or (argv[1].startswith('-') and (argv[1] != '-m' or len(argv) < 3)):
        raise WorkspaceRefused('Python module or script command required')
    inputs = job.get('inputs', {})
    if not inputs:
        raise WorkspaceRefused('source/dependency/oracle inputs required')
    for relative, expected in inputs.items():
        path = cwd / relative
        if not path.is_relative_to(cwd) or '..' in Path(relative).parts or Path(relative).is_absolute():
            raise WorkspaceRefused('source input escape')
        ordinary(path)
        for parent in path.parents:
            ordinary(parent, directory=True)
            if parent == cwd: break
        if file_digest(path) != expected:
            raise WorkspaceRefused('source input changed: ' + relative)
    if argv[1] != '-m':
        script = Path(argv[1]) if Path(argv[1]).is_absolute() else cwd/argv[1]
        if not script.is_relative_to(cwd) or script.relative_to(cwd).as_posix() not in inputs:
            raise WorkspaceRefused('script must be a bound source input')
    # Small immutable Git identities; no tracked-report generation.
    def git(*args):
        return subprocess.run(['git', '-C', str(cwd), *args], capture_output=True, text=True, timeout=15, check=True).stdout.strip()
    if git('rev-parse', 'HEAD') != job['source_commit'] or git('rev-parse', 'HEAD^{tree}') != job['source_tree']:
        raise WorkspaceRefused('source commit/tree changed')
    return cwd


def inspect(config_path, job=None):
    config, roots, working = load_config(config_path)
    if job is not None: validate_job(job, working)
    observed = capacity(roots)
    reservations = admission(config, roots, observed)
    active = roots['control'] / 'active.json'
    return {'config_digest': digest(config), 'capacity': observed, 'reservations': reservations,
            'active': read_json(active) if os.path.lexists(active) else None,
            'writes': False, 'disk_enforcement': 'reservation_and_monitored_threshold',
            'memory_enforcement': 'Windows_Job_commit_limit', 'log_enforcement': 'bounded_pipe_drain'}


def owned_scratch(record, roots):
    job_id = record['job_id']
    if len(job_id) != 32 or any(c not in '0123456789abcdef' for c in job_id):
        raise WorkspaceRefused('invalid owned job identity')
    root = roots['scratch'] / job_id
    ordinary(root, directory=True)
    if read_json(root / 'owner.json') != {'job_id': job_id, 'manifest_digest': record['manifest_digest']}:
        raise WorkspaceRefused('scratch ownership mismatch')
    return root


def content_digest(root):
    result = hashlib.sha256()
    def visit(directory):
        ordinary(directory, directory=True)
        for item in sorted(directory.iterdir(), key=lambda p: p.name):
            info = item.lstat(); relative = item.relative_to(root).as_posix()
            if stat.S_ISDIR(info.st_mode):
                ordinary(item, directory=True)
                result.update(json.dumps(['dir', relative]).encode()); visit(item)
            else:
                ordinary(item)
                result.update(json.dumps(['file', relative, file_digest(item)]).encode())
    visit(root)
    return result.hexdigest()


def finish_collected(record, config, roots):
    """Finish a previously verified collection without recopies or PID killing."""
    limits = config['limits']; retained = roots['retained']/record['job_id']
    ordinary(retained, directory=True)
    if read_json(retained/'owner.json') != {'job_id': record['job_id'], 'manifest_digest': record['manifest_digest']}:
        raise WorkspaceRefused('retained owner changed')
    for member, expected in record['collected_manifest'].items():
        tree_usage(retained/member, maximum=limits['retained_bytes']+limits['log_bytes'], max_files=limits['max_files'])
        if content_digest(retained/member) != expected: raise WorkspaceRefused('retained content changed')
    root = roots['scratch']/record['job_id']
    if os.path.lexists(root):
        info = ordinary(root, directory=True)
        if [info.st_dev, info.st_ino] != record['scratch_identity']:
            raise WorkspaceRefused('scratch directory identity changed')
        if any(p.name not in ('tmp', 'cache', 'output', 'logs', 'owner.json') for p in root.iterdir()):
            raise WorkspaceRefused('unexpected root output preserved')
        tree_usage(root, maximum=limits['scratch_bytes']+limits['log_bytes']+1024*1024, max_files=limits['max_files'])
        # A crash during retirement can leave only a subset of the collected
        # files. Every remaining unique output must still match retained bytes.
        def verify_remaining(source, target):
            ordinary(source, directory=True); ordinary(target, directory=True)
            for item in source.iterdir():
                if item.is_dir(): verify_remaining(item, target/item.name)
                else:
                    ordinary(item); ordinary(target/item.name)
                    if file_digest(item) != file_digest(target/item.name):
                        raise WorkspaceRefused('post-collection output changed')
        for member in ('output', 'logs'):
            if (root/member).exists(): verify_remaining(root/member, retained/member)
        shutil.rmtree(root)
    record.update(phase='retired', scratch_absent=not os.path.lexists(root), reservation_released=True)
    write_json(retained/'receipt.json', record)
    (roots['control']/'active.json').unlink()
    return record


def collect_and_retire(record, config, roots):
    root = owned_scratch(record, roots); limits = config['limits']
    if any(p.name not in ('tmp', 'cache', 'output', 'logs', 'owner.json') for p in root.iterdir()):
        raise WorkspaceRefused('unexpected root output preserved')
    tree_usage(root, maximum=limits['scratch_bytes'] + limits['log_bytes'] + 1024 * 1024, max_files=limits['max_files'])
    # Output is always retained, including cancellation/crash output. TMP/cache
    # are explicitly disposable; no unique source data belongs in these pools.
    output = root / 'output'
    tree_usage(output, maximum=limits['retained_bytes'], max_files=limits['max_files'])
    retained = roots['retained'] / record['job_id']
    owner = {'job_id': record['job_id'], 'manifest_digest': record['manifest_digest']}
    if os.path.lexists(retained):
        ordinary(retained, directory=True)
        if read_json(retained/'owner.json') != owner:
            raise WorkspaceRefused('retention ownership mismatch')
    else:
        retained.mkdir(); write_json(retained/'owner.json', owner)
    def collect(source, target):
        ordinary(source, directory=True)
        if not os.path.lexists(target): target.mkdir()
        ordinary(target, directory=True)
        for entry in source.iterdir():
            if entry.is_dir():
                collect(entry, target/entry.name)
            else:
                ordinary(entry); destination = target/entry.name
                if os.path.lexists(destination):
                    ordinary(destination)
                    if entry.stat().st_size != destination.stat().st_size or file_digest(entry) != file_digest(destination):
                        raise WorkspaceRefused('conflicting partial collection preserved')
                else:
                    with entry.open('rb') as src, destination.open('xb') as dst:
                        shutil.copyfileobj(src, dst, 1024 * 1024)
    try:
        collect(output, retained / 'output')
        logs = root / 'logs'
        if logs.exists():
            tree_usage(logs, maximum=limits['log_bytes'] + 1024 * 1024, max_files=5)
            collect(logs, retained / 'logs')
        record['collected_manifest'] = {member: content_digest(retained/member) for member in ('output', 'logs') if (retained/member).exists()}
        record.update(phase='collected', retained=str(retained), reservation_released=False)
        write_json(retained / 'receipt.json', record)
        write_json(roots['control'] / 'active.json', record)
        return finish_collected(record, config, roots)
    except BaseException:
        record['phase'] = 'collection_recovery_required'
        write_json(roots['control'] / 'active.json', record)
        raise


def run(config_path, job, *, host=None, cancelled=lambda: False, probe=capacity):
    config, roots, working = load_config(config_path); cwd = validate_job(job, working)
    host = host or WindowsJobHost(); limits = config['limits']; active = roots['control'] / 'active.json'
    with estate_lock(roots['control']):
        if os.path.lexists(active):
            raise WorkspaceRefused('previous job requires explicit reconciliation')
        if os.path.lexists(active.with_name('active.json.next')):
            raise WorkspaceRefused('interrupted admission staging record requires reconciliation')
        before = probe(roots); reservations = admission(config, roots, before)
        job_id = uuid.uuid4().hex; root = roots['scratch'] / job_id
        record = {'job_id': job_id, 'manifest_digest': digest(job), 'config_digest': digest(config),
                  'job': job, 'phase': 'reserved', 'reservations': reservations, 'before': before,
                  'created_at_unix_ns': time.time_ns(), 'limits': limits, 'scratch': str(root),
                  'reservation_released': False, 'peaks': {'scratch_bytes': 0, 'memory_bytes': 0}}
        # Durable intent precedes allocation. Crash before owner marker refuses
        # destructive reconciliation instead of inferring ownership from a name.
        write_json(active, record)
        root.mkdir(); write_json(root / 'owner.json', {'job_id': job_id, 'manifest_digest': record['manifest_digest']})
        info = root.lstat(); record['scratch_identity'] = [info.st_dev, info.st_ino]
        for member in ('tmp', 'cache', 'output'): (root / member).mkdir()
        env = sanitized_environment()
        env.update(TEMP=str(root/'tmp'), TMP=str(root/'tmp'), TMPDIR=str(root/'tmp'),
                   AIDE_JOB_TMP=str(root/'tmp'), AIDE_JOB_OUTPUT=str(root/'output'),
                   AIDE_RESOURCE_TEST_PARENT=str(root/'tmp'), AIDE_JOB_ID=job_id,
                   AIDE_JOB_CONTROL=str(roots['control']),
                   XDG_CACHE_HOME=str(root/'cache'), PIP_CACHE_DIR=str(root/'cache'),
                   UV_CACHE_DIR=str(root/'cache'), PYTHONUNBUFFERED='1')
        record['environment_digest'] = digest(env)
        next_probe = next_scan = 0.0
        def observe(sample):
            nonlocal next_probe, next_scan
            record['process'] = sample
            record['peaks']['memory_bytes'] = max(record['peaks']['memory_bytes'], sample.get('peak_memory_bytes', 0))
            now = time.monotonic()
            if now >= next_probe:
                current = probe(roots)
                for free in current['disk_free'].values():
                    if free < limits['disk_reserve_bytes']: raise WorkspaceRefused('disk reserve danger')
                if current['physical_free'] < limits['physical_reserve_bytes'] or current['commit_free'] < limits['commit_reserve_bytes']:
                    raise WorkspaceRefused('memory reserve danger')
                record['last_capacity'] = current; next_probe = now + 1.0
            # Only this owned scratch, every 30 seconds, with bounded enumeration.
            # Disk/memory samples use OS counters and never scan estate/source.
            if now >= next_scan:
                used = tree_usage(root, maximum=limits['scratch_bytes'] + limits['log_bytes'], max_files=limits['max_files'])
                record['peaks']['scratch_bytes'] = max(record['peaks']['scratch_bytes'], used)
                next_scan = now + 30.0
            write_json(active, record)
        def checkpoint(stage):
            record['phase'] = stage; write_json(active, record)
        # Force Python tempfile's explicit parent: it cannot fall back when the
        # admitted pool disappears. Tool scripts must use AIDE_JOB_OUTPUT/cache.
        bootstrap = "import os,sys,tempfile,runpy; tempfile.tempdir=os.environ['AIDE_JOB_TMP']; a=sys.argv[1:]; sys.argv=([a[1],*a[2:]] if a[0]=='-m' else a); runpy.run_module(a[1],run_name='__main__',alter_sys=True) if a[0]=='-m' else runpy.run_path(a[0],run_name='__main__')"
        argv = [job['argv'][0], '-B', '-u', '-c', bootstrap, *job['argv'][1:]]
        try:
            record['result'] = host.run(argv, cwd=cwd, input_bytes=b'', output_dir=root/'logs', job_id=job_id,
                timeout=limits['runtime_seconds'], output_limit=limits['log_bytes'], memory_limit=limits['memory_bytes'],
                process_limit=limits['processes'], cancelled=cancelled, checkpoint=checkpoint, environment=env, observed=observe)
        except BaseException as exc:
            record['result'] = {'reason': type(exc).__name__, 'message': str(exc), 'exit_code': None}
            record['reconciliation'] = host.reconcile(job_id)
        record['phase'] = 'quiescent'; write_json(active, record)
        record['after'] = probe(roots)
        return collect_and_retire(record, config, roots)


def recover(config_path):
    config, roots, _ = load_config(config_path)
    with estate_lock(roots['control']):
        active = roots['control'] / 'active.json'
        if not os.path.lexists(active): return {'phase': 'no_pending_job', 'writes': False}
        record = read_json(active)
        if record['config_digest'] != digest(config): raise WorkspaceRefused('recovery config changed')
        if not record.get('collected_manifest'): owned_scratch(record, roots)
        record['reconciliation'] = WindowsJobHost().reconcile(record['job_id'])
        if not record['reconciliation']['quiescent']: raise WorkspaceRefused('owned job not quiescent')
        # A terminated controller can leave its generated checkpoint staging
        # file. Once ownership and quiescence are established, discard only
        # that regular single-link staging file; output remains untouched.
        staging = active.with_name('active.json.next')
        if os.path.lexists(staging):
            if ordinary(staging).st_size > 1024 * 1024: raise WorkspaceRefused('unexpected checkpoint staging size')
            staging.unlink()
        record['result'] = record.get('result', {'reason': 'controller_interrupted', 'exit_code': None})
        if record.get('collected_manifest'): return finish_collected(record, config, roots)
        return collect_and_retire(record, config, roots)


def current_context(working_root):
    """Source-maintainer admission proof; environment alone cannot grant it."""
    job_id = os.environ.get('AIDE_JOB_ID', '')
    if os.name != 'nt' or len(job_id) != 32 or any(c not in '0123456789abcdef' for c in job_id) or not WindowsJobHost().contains_current_process(job_id):
        raise WorkspaceRefused('source maintainer command requires an admitted Windows Job')
    control = root_path(os.environ['AIDE_JOB_CONTROL'])
    record = read_json(control/'active.json')
    if record['job_id'] != job_id or digest(record['job']) != record['manifest_digest']:
        raise WorkspaceRefused('managed context identity mismatch')
    root = root_path(str(working_root))
    if Path(record['job']['cwd']) != root:
        raise WorkspaceRefused('managed context working root mismatch')
    # Check exact declared source/executable/Git identities again at effect entry.
    validate_job(record['job'], [root])
    if '.aide/scripts/aide_lite.py' not in record['job']['inputs']:
        raise WorkspaceRefused('source CLI must be a bound input')
    task_id = record['job']['workunit']
    if not isinstance(task_id, str) or not task_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in task_id):
        raise WorkspaceRefused('bounded WorkUnit identifier required')
    ordinary(root/'.aide/queue'/task_id/'task.yaml')
    return record
