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
import re
import shutil
import stat
import subprocess
import time
import uuid

from core.runtime.continuous_worker.windows_job import WindowsJobHost, sanitized_environment


class WorkspaceRefused(ValueError):
    pass


# Existing repository-owned generator/evaluation destinations only. These are
# retained canonical outputs, never disposable pools or arbitrary caller paths.
CANONICAL_OUTPUT_PATHS = frozenset(('.aide/export/aide-lite-pack-v0',
                                  '.aide/release', '.aide/evals/runs'))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def file_digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''): value.update(chunk)
    return value.hexdigest()


def unique_json_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise WorkspaceRefused('duplicate JSON object key')
        value[key] = item
    return value


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
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      object_pairs_hook=unique_json_object)


def write_json(path, value):
    path = Path(path)
    if os.path.lexists(path):
        ordinary(path)
    temporary = path.with_name(path.name + '.next')
    with temporary.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    # A Windows reader can briefly deny replacement of the current record.
    # Retry the same fsynced staging file; persistent failure leaves it for
    # explicit recovery instead of starting a competing checkpoint write.
    for attempt in range(21):
        try:
            os.replace(temporary, path)
            return
        except PermissionError:
            if attempt == 20:
                raise
            time.sleep(0.05)


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


def validate_config(config):
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
    if 'canonical_bytes' in config['limits']:
        value = config['limits']['canonical_bytes']
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise WorkspaceRefused('finite positive canonical output limit required')
    if 'codex_exec' in config:
        permission = config['codex_exec']
        if (not isinstance(permission, dict)
                or set(permission) != {'account', 'model', 'effort', 'max_turns'}
                or permission['account'] != 'chatgpt'
                or not isinstance(permission['model'], str)
                or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}', permission['model'])
                or permission['effort'] not in ('low', 'medium', 'high', 'xhigh', 'max', 'ultra')
                or type(permission['max_turns']) is not int
                or not 0 < permission['max_turns'] <= 100):
            raise WorkspaceRefused('exact finite local Codex permission required')
    working = [root_path(value) for value in config['working_roots']]
    if not working or any(root.is_relative_to(work) for root in roots.values() for work in working):
        raise WorkspaceRefused('storage inside working source refused')
    return config, roots, working


def load_config(path):
    return validate_config(read_json(path))


def configure(config_path, selection_path, approved_parent, *, probe=None):
    """Create only explicitly selected local roots and one source-local config.

    The selection has the existing config fields; supplied volume IDs are
    replaced by observed IDs. No machine or process default can select a root.
    """
    selection = read_json(selection_path)
    probe = probe or capacity
    if not isinstance(selection, dict) or set(selection) - {
        'schema', 'roots', 'volume_ids', 'working_roots', 'limits'
    }:
        raise WorkspaceRefused('unsupported setup selection fields')
    if selection.get('schema') != 'aide.managed-workspace.local.v1':
        raise WorkspaceRefused('unsupported local workspace config')
    if not isinstance(selection.get('roots'), dict) or set(selection['roots']) != {'scratch', 'retained', 'control'}:
        raise WorkspaceRefused('three exact selected storage roots required')
    required_limits = {'disk_reserve_bytes', 'physical_reserve_bytes', 'commit_reserve_bytes',
        'scratch_bytes', 'retained_bytes', 'canonical_bytes', 'memory_bytes', 'log_bytes',
        'runtime_seconds', 'processes', 'max_files'}
    limits = selection.get('limits')
    if not isinstance(limits, dict) or set(limits) != required_limits:
        raise WorkspaceRefused('exact finite setup limits required')
    for key, value in limits.items():
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise WorkspaceRefused('finite positive limit required: ' + key)
    if limits['runtime_seconds'] > 86400 or limits['processes'] > 128:
        raise WorkspaceRefused('runtime/process limit outside maintainer profile')
    selected_working = selection.get('working_roots')
    if not isinstance(selected_working, list) or not selected_working or any(not isinstance(v, str) for v in selected_working):
        raise WorkspaceRefused('exact existing working roots required')
    working = [root_path(value) for value in selected_working]
    if len(set(working)) != len(working):
        raise WorkspaceRefused('duplicate working root')
    parent = root_path(approved_parent)
    if any(parent.is_relative_to(work) for work in working):
        raise WorkspaceRefused('approved storage parent inside source')
    chosen = {}
    for key, value in selection['roots'].items():
        if not isinstance(value, str):
            raise WorkspaceRefused('absolute bounded root required')
        path = Path(value)
        if (not path.is_absolute() or '..' in path.parts or path == parent
                or not path.is_relative_to(parent) or path.resolve() != path
                or any(path.is_relative_to(work) or work.is_relative_to(path) for work in working)):
            raise WorkspaceRefused('selected root escapes approved storage parent or source')
        chosen[key] = path
    values = list(chosen.values())
    if any(left.is_relative_to(right) or right.is_relative_to(left)
           for i, left in enumerate(values) for right in values[i+1:]):
        raise WorkspaceRefused('storage roots must be distinct and nonoverlapping')
    supplied_destination = Path(config_path)
    if '..' in supplied_destination.parts:
        raise WorkspaceRefused('config path escape refused')
    destination = supplied_destination if supplied_destination.is_absolute() else Path.cwd() / supplied_destination
    if not any(destination == work / '.aide.local' / 'execution.json' for work in working):
        raise WorkspaceRefused('config must be in an approved working root local boundary')
    if os.path.lexists(destination.parent):
        root_path(destination.parent)
    for path in chosen.values():
        ancestor = path
        while not os.path.lexists(ancestor):
            ancestor = ancestor.parent
        root_path(ancestor)
        if not ancestor.is_relative_to(parent):
            raise WorkspaceRefused('selected root lacks approved existing ancestor')
    # Observe capacity and volume on existing parents before creating anything.
    proxies = {}
    for key, path in chosen.items():
        ancestor = path
        while not os.path.lexists(ancestor):
            ancestor = ancestor.parent
        proxies[key] = ancestor
    config_ancestor = destination.parent
    while not os.path.lexists(config_ancestor):
        config_ancestor = config_ancestor.parent
    root_path(config_ancestor)
    proxies['config'] = config_ancestor
    config = {'schema': selection['schema'], 'roots': {key: str(value) for key, value in chosen.items()},
        'volume_ids': {key: volume_identity(proxies[key]) for key in chosen},
        'working_roots': [str(value) for value in working], 'limits': dict(limits)}
    def check_config_capacity(observed, path, reservations):
        identity = volume_identity(path)
        if observed['disk_free'][identity] - reservations.get(identity, 0) - 1024 * 1024 < limits['disk_reserve_bytes']:
            raise WorkspaceRefused('local config would consume free-space reserve')
    observed = probe(proxies)
    reservations = admission(config, proxies, observed)
    check_config_capacity(observed, config_ancestor, reservations)
    if os.path.lexists(destination):
        if read_json(destination) != config:
            raise WorkspaceRefused('existing local config differs; preserve it for review')
        validate_config(config)
        return {'result': 'ALREADY_CONFIGURED', 'writes': False, 'config_digest': digest(config),
                'volume_ids': config['volume_ids'], 'capacity': observed}
    existing_populated = any(path.exists() and any(path.iterdir()) for path in chosen.values())
    if existing_populated:
        if os.path.lexists(chosen['control'] / 'active.json'):
            raise WorkspaceRefused('active job prevents shared storage setup')
        peers = [work / '.aide.local' / 'execution.json' for work in working if work / '.aide.local' / 'execution.json' != destination]
        if not any(os.path.lexists(peer) and root_path(peer.parent) and read_json(peer) == config for peer in peers):
            raise WorkspaceRefused('existing nonempty storage lacks matching shared config')
    created = []
    try:
        for path in (*chosen.values(), destination.parent):
            missing = []
            ancestor = path
            while not os.path.lexists(ancestor):
                missing.append(ancestor); ancestor = ancestor.parent
            root_path(ancestor)
            for child in reversed(missing):
                ordinary(child.parent, directory=True)
                child.mkdir()
                ordinary(child, directory=True)
                created.append(child)
        config['volume_ids'] = {key: volume_identity(value) for key, value in chosen.items()}
        if config['volume_ids'] != {key: volume_identity(proxies[key]) for key in chosen}:
            raise WorkspaceRefused('selected volume identity changed during setup')
        validate_config(config)
        observed = probe({**chosen, 'config': destination.parent})
        reservations = admission(config, chosen, observed)
        check_config_capacity(observed, destination.parent, reservations)
        temporary = destination.with_name(destination.name + '.setup-next')
        with temporary.open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(config, stream, sort_keys=True, indent=2)
            stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
        try:
            if os.path.lexists(destination):
                raise WorkspaceRefused('local config appeared during setup')
            if os.name == 'nt':
                os.rename(temporary, destination)  # Windows refuses an existing destination.
            else:
                os.link(temporary, destination)  # Exclusive publication on POSIX.
        finally:
            if os.path.lexists(temporary):
                ordinary(temporary); temporary.unlink()
    except BaseException:
        if not os.path.lexists(destination):
            for path in reversed(created):
                try: path.rmdir()  # Only our empty directory; never recursive.
                except OSError: pass
        raise
    return {'result': 'CONFIGURED', 'writes': True, 'config_digest': digest(config),
            'volume_ids': config['volume_ids'], 'capacity': observed}


@contextmanager
def estate_lock(control, name='admission.lock'):
    # All admitted campaign workspaces use this one configured control root.
    # OS handle locking survives PID reuse and releases on interpreter death.
    if name not in ('admission.lock', 'dispatch.lock'):
        raise WorkspaceRefused('unknown estate lock')
    path = control / name
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
            reason = ('another heavy job owns the estate reservation' if name == 'admission.lock'
                      else 'dispatch control is busy')
            raise WorkspaceRefused(reason) from exc
        yield
    finally:
        os.close(fd)


def dispatch_state(control):
    path = control / 'dispatch.json'
    if os.path.lexists(path.with_name('dispatch.json.next')):
        raise WorkspaceRefused('interrupted dispatch-control write requires reconciliation')
    if os.path.lexists(path):
        if ordinary(path).st_size > 1024 * 1024:
            raise WorkspaceRefused('dispatch-control record too large')
        value = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_json_object)
    else:
        value = {'schema': 'aide.job-dispatch.v1', 'mode': 'running', 'epoch': 0,
                 'codex_admitted': 0, 'codex_request_digests': []}
    if (not isinstance(value, dict)
            or set(value) not in ({'schema', 'mode', 'epoch'},
                                  {'schema', 'mode', 'epoch', 'codex_admitted'},
                                  {'schema', 'mode', 'epoch', 'codex_admitted',
                                   'codex_request_digests'})
            or value['schema'] != 'aide.job-dispatch.v1'
            or value['mode'] not in ('running', 'paused')
            or type(value['epoch']) is not int or value['epoch'] < 0
            or type(value.get('codex_admitted', 0)) is not int
            or not 0 <= value.get('codex_admitted', 0) <= 100):
        raise WorkspaceRefused('dispatch-control state is invalid')
    count = value.get('codex_admitted', 0)
    # Older positive-count records cannot prove which requests consumed turns.
    # Preserve that uncertainty instead of silently allowing their replay.
    requests = value.get('codex_request_digests', [] if count == 0 else None)
    if requests is not None:
        if (not isinstance(requests, list) or len(requests) != count
                or any(not isinstance(item, str)
                       or not re.fullmatch(r'[0-9a-f]{64}', item) for item in requests)
                or len(set(requests)) != len(requests)):
            raise WorkspaceRefused('dispatch-control Codex request history is invalid')
    elif count == 0:
        raise WorkspaceRefused('dispatch-control Codex request history is invalid')
    return {**value, 'codex_admitted': count, 'codex_request_digests': requests}


def codex_request_digest(job):
    # Windows path spellings can alias the same directory and input files.
    # Labels and filename casing do not make the same content a new request.
    cwd_info = ordinary(job['cwd'], directory=True)
    if cwd_info.st_ino <= 0:
        raise WorkspaceRefused('Codex request requires stable working-root identity')
    return digest({'cwd_identity': [cwd_info.st_dev, cwd_info.st_ino],
        'source_commit': job['source_commit'], 'source_tree': job['source_tree'],
        'executable_sha256': job['executable_sha256'],
        'input_sha256s': sorted(set(job['inputs'].values())),
        'prompt_sha256': job['inputs'][job['prompt_file']],
        'schema_sha256': job['inputs'][job['schema_file']],
        'model': job['model'].casefold(), 'effort': job['effort']})


def require_codex_permission(config, job, dispatch):
    if job.get('adapter') != 'codex_exec':
        return
    permission = config.get('codex_exec')
    if (not permission or job['model'] != permission['model']
            or job['effort'] != permission['effort']):
        raise WorkspaceRefused('Codex job has no matching local model permission')
    if dispatch['codex_admitted'] >= permission['max_turns']:
        raise WorkspaceRefused('finite Codex turn budget exhausted')
    if dispatch['codex_request_digests'] is None:
        raise WorkspaceRefused('prior Codex request identities require reconciliation')
    if codex_request_digest(job) in dispatch['codex_request_digests']:
        raise WorkspaceRefused('Codex request already admitted without new bound input')


def admit_codex_turn(control, expected, maximum, request_digest):
    with estate_lock(control, 'dispatch.lock'):
        current = dispatch_state(control)
        if current != expected or current['mode'] != 'running':
            raise WorkspaceRefused('dispatch epoch changed before Codex admission')
        if current['codex_admitted'] >= maximum:
            raise WorkspaceRefused('finite Codex turn budget exhausted')
        if current['codex_request_digests'] is None:
            raise WorkspaceRefused('prior Codex request identities require reconciliation')
        if request_digest in current['codex_request_digests']:
            raise WorkspaceRefused('Codex request already admitted without new bound input')
        admitted = {**current, 'codex_admitted': current['codex_admitted'] + 1,
                    'codex_request_digests': [*current['codex_request_digests'], request_digest]}
        write_json(control / 'dispatch.json', admitted)
        return admitted


def set_dispatch(config_path, mode):
    if mode not in ('running', 'paused'):
        raise WorkspaceRefused('invalid dispatch mode')
    _, roots, _ = load_config(config_path)
    with estate_lock(roots['control'], 'dispatch.lock'):
        current = dispatch_state(roots['control'])
        changed = current['mode'] != mode
        if changed:
            current = {**current, 'mode': mode, 'epoch': current['epoch'] + 1}
            write_json(roots['control'] / 'dispatch.json', current)
        return {**current, 'writes': changed}


def capacity(roots):
    disks = {volume_identity(root): shutil.disk_usage(root).free for root in roots.values()}
    return {'disk_free': disks, **memory_capacity()}


def admission(config, roots, observed, canonical=None):
    limits = config['limits']; reservations = {}
    # Collection may temporarily hold both copies on this volume. Include the
    # metadata/staging allowance that collection and retirement already accept.
    for key, amount in (('scratch', limits['scratch_bytes'] + limits['log_bytes'] + 1024 * 1024),
                        ('retained', limits['retained_bytes'] + limits['log_bytes'] + 1024 * 1024),
                        ('control', 1024 * 1024)):
        identity = volume_identity(roots[key])
        reservations[identity] = reservations.get(identity, 0) + amount
    for relative, declared in (canonical or {}).items():
        identity = volume_identity(roots['canonical:' + relative])
        reservations[identity] = reservations.get(identity, 0) + declared['bytes']
    for identity, amount in reservations.items():
        if observed['disk_free'][identity] - amount < limits['disk_reserve_bytes']:
            raise WorkspaceRefused('disk reservation would consume free-space reserve')
    for resource, reserve in (('physical_free', 'physical_reserve_bytes'), ('commit_free', 'commit_reserve_bytes')):
        if observed[resource] - limits['memory_bytes'] < limits[reserve]:
            raise WorkspaceRefused('memory reservation would consume ' + resource)
    return reservations


def canonical_roots(config, job, cwd):
    declarations = job.get('canonical_outputs', {})
    if not isinstance(declarations, dict) or any(rel not in CANONICAL_OUTPUT_PATHS for rel in declarations):
        raise WorkspaceRefused('unknown canonical output destination')
    roots = {}; total = 0
    for relative, declared in declarations.items():
        if not isinstance(declared, dict): raise WorkspaceRefused('canonical output declaration required')
        amount = declared.get('bytes')
        if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
            raise WorkspaceRefused('finite positive canonical reservation required')
        total += amount
        path = root_path(str(cwd/relative))
        if volume_identity(path) != declared.get('volume_id', '').casefold():
            raise WorkspaceRefused('canonical output volume identity changed')
        roots['canonical:' + relative] = path
    if total > config['limits'].get('canonical_bytes', 0):
        raise WorkspaceRefused('canonical reservation exceeds configured output allowance')
    return roots


def canonical_usage(config, job, roots):
    for relative, declared in job.get('canonical_outputs', {}).items():
        if volume_identity(roots['canonical:' + relative]) != declared['volume_id'].casefold():
            raise WorkspaceRefused('canonical output volume identity changed')
    return {relative: tree_usage(roots['canonical:' + relative], maximum=declared['bytes'],
                                max_files=config['limits']['max_files'])
            for relative, declared in job.get('canonical_outputs', {}).items()}


def qualify_canonical_outputs(record, config, roots, working):
    """Required on both normal completion and interrupted-controller recovery."""
    try:
        cwd = Path(record['job']['cwd'])
        if cwd not in working: raise WorkspaceRefused('canonical working root no longer approved')
        roots.update(canonical_roots(config, record['job'], cwd))
        record['canonical_after'] = canonical_usage(config, record['job'], roots)
        peaks = record['peaks'].setdefault('canonical_bytes', {})
        for relative, used in record['canonical_after'].items():
            peaks[relative] = max(peaks.get(relative, 0), used)
    except (OSError, WorkspaceRefused) as exc:
        # Never change a resource failure into success during later recovery.
        # Preserve canonical files/aliases; only verified scratch is retired.
        record['canonical_after_error'] = str(exc)
        record.setdefault('prior_result', record.get('result'))
        record['result'] = {'reason': 'canonical_output_limit_or_identity', 'message': str(exc), 'exit_code': None}


def tree_usage(root, *, maximum, max_files, allow_transient_absence=False,
               allow_transient_hardlinks=False):
    total = count = 0; pending = [root]
    linked_members: dict[tuple[int, int], list[int]] = {}
    while pending:
        directory = pending.pop()
        try:
            ordinary(directory, directory=True)
            entries = os.scandir(directory)
        except FileNotFoundError:
            if allow_transient_absence: continue
            raise
        with entries:
            for entry in entries:
                # Windows DirEntry's cached enumeration omits link/device
                # identity (st_nlink=0). Use lstat for ownership validation.
                try:
                    info = Path(entry.path).lstat()
                except FileNotFoundError:
                    if allow_transient_absence: continue
                    raise
                count += 1
                if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                    raise WorkspaceRefused('linked job member preserved for recovery')
                if stat.S_ISDIR(info.st_mode):
                    pending.append(Path(entry.path))
                elif stat.S_ISREG(info.st_mode) and (
                    info.st_nlink == 1 or (allow_transient_hardlinks and info.st_nlink > 1)
                ):
                    # During live observation, a job-owned atomic create can
                    # briefly expose its temporary and final names together.
                    # Require every link name to be inside this scanned root;
                    # otherwise an outside link could alias external bytes.
                    # Count each name conservatively. Collection remains
                    # strict once the child is quiescent.
                    if info.st_nlink > 1:
                        linked_members.setdefault((info.st_dev, info.st_ino), []).append(info.st_nlink)
                    total += info.st_size
                else:
                    raise WorkspaceRefused(
                        'unexpected job member preserved for recovery: '
                        f'{Path(entry.path).relative_to(root)} '
                        f'mode={info.st_mode:o} nlink={info.st_nlink} '
                        f'attributes={getattr(info, "st_file_attributes", 0):x}'
                    )
                if total > maximum or count > max_files:
                    raise WorkspaceRefused('workspace size/file threshold exceeded')
    if any(len(counts) != counts[0] or any(value != counts[0] for value in counts)
           for counts in linked_members.values()):
        raise WorkspaceRefused('hardlink outside owned scratch or transient link set')
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
    exe = Path(argv[0])
    if not exe.is_absolute():
        raise WorkspaceRefused('absolute executable required')
    adapter = job.get('adapter')
    if adapter == 'codex_exec':
        root_path(str(exe.parent))
    ordinary(exe)
    if file_digest(exe) != job['executable_sha256']:
        raise WorkspaceRefused('executable changed')
    if adapter == 'python':
        if exe.name.casefold() not in ('python.exe', 'python', 'python3'):
            raise WorkspaceRefused('explicit Python executable required')
        if len(argv) < 2 or (argv[1].startswith('-') and (argv[1] != '-m' or len(argv) < 3)):
            raise WorkspaceRefused('Python module or script command required')
    elif adapter == 'codex_exec':
        if exe.name.casefold() != 'codex.exe' or len(argv) != 1 or job.get('canonical_outputs'):
            raise WorkspaceRefused('one explicit Codex executable without canonical outputs required')
        if not isinstance(job.get('model'), str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}', job['model']):
            raise WorkspaceRefused('explicit bounded Codex model required')
        if job.get('effort') not in ('low', 'medium', 'high', 'xhigh', 'max', 'ultra'):
            raise WorkspaceRefused('explicit Codex reasoning effort required')
    else:
        raise WorkspaceRefused('qualified placement adapter required')
    inputs = job.get('inputs', {})
    if not inputs:
        raise WorkspaceRefused('source/dependency/oracle inputs required')
    codex_input_identities = set()
    for relative, expected in inputs.items():
        path = cwd / relative
        if not path.is_relative_to(cwd) or '..' in Path(relative).parts or Path(relative).is_absolute():
            raise WorkspaceRefused('source input escape')
        info = ordinary(path)
        if adapter == 'codex_exec':
            if info.st_ino <= 0:
                raise WorkspaceRefused('Codex request requires stable input identity')
            identity = (info.st_dev, info.st_ino)
            if identity in codex_input_identities:
                raise WorkspaceRefused('duplicate Codex input alias')
            codex_input_identities.add(identity)
        for parent in path.parents:
            ordinary(parent, directory=True)
            if parent == cwd: break
        if file_digest(path) != expected:
            raise WorkspaceRefused('source input changed: ' + relative)
    if adapter == 'python' and argv[1] != '-m':
        script = Path(argv[1]) if Path(argv[1]).is_absolute() else cwd/argv[1]
        if not script.is_relative_to(cwd) or script.relative_to(cwd).as_posix() not in inputs:
            raise WorkspaceRefused('script must be a bound source input')
    if adapter == 'codex_exec':
        for name in ('prompt_file', 'schema_file'):
            relative = job.get(name)
            if not isinstance(relative, str) or relative not in inputs:
                raise WorkspaceRefused(name + ' must be a bound source input')
            size = ordinary(cwd / relative).st_size
            if not 0 < size <= 65536:
                raise WorkspaceRefused(name + ' exceeds the one-turn input limit')
        try:
            schema = json.loads((cwd / job['schema_file']).read_text(encoding='utf-8'),
                                object_pairs_hook=unique_json_object)
        except (UnicodeError, ValueError) as exc:
            raise WorkspaceRefused('Codex result schema is malformed') from exc
        if not isinstance(schema, dict) or schema.get('type') != 'object':
            raise WorkspaceRefused('Codex result schema must be an object')
    # Small immutable Git identities; no tracked-report generation.
    def git(*args):
        return subprocess.run(['git', '-C', str(cwd), *args], capture_output=True, text=True, timeout=15, check=True).stdout.strip()
    if git('rev-parse', 'HEAD') != job['source_commit'] or git('rev-parse', 'HEAD^{tree}') != job['source_tree']:
        raise WorkspaceRefused('source commit/tree changed')
    return cwd


def inspect(config_path, job=None):
    config, roots, working = load_config(config_path)
    if job is not None:
        cwd = validate_job(job, working)
        roots.update(canonical_roots(config, job, cwd))
        canonical_usage(config, job, roots)
    observed = capacity(roots)
    reservations = admission(config, roots, observed, (job or {}).get('canonical_outputs'))
    active = roots['control'] / 'active.json'
    dispatch = dispatch_state(roots['control'])
    if job is not None:
        require_codex_permission(config, job, dispatch)
    return {'config_digest': digest(config), 'capacity': observed, 'reservations': reservations,
            'active': read_json(active) if os.path.lexists(active) else None,
            'dispatch': dispatch,
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


def make_owned_scratch_writable(root, *, max_files):
    """Retire readonly Windows fixtures only after the owned tree is verified."""
    pending = [root]; readonly = []; count = 0
    def is_readonly(info):
        return not info.st_mode & stat.S_IWRITE or bool(
            getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_READONLY', 1))
    while pending:
        directory = pending.pop()
        info = ordinary(directory, directory=True)
        if is_readonly(info):
            readonly.append((directory, True))
        for child in directory.iterdir():
            info = child.lstat(); count += 1
            if count > max_files:
                raise WorkspaceRefused('scratch retirement entry limit exceeded')
            if stat.S_ISDIR(info.st_mode):
                ordinary(child, directory=True)
                pending.append(child)
            else:
                ordinary(child)
                if is_readonly(info):
                    readonly.append((child, False))
    # No attributes are changed until the whole tree passed type/link checks.
    for path, directory in readonly:
        info = ordinary(path, directory=directory)
        os.chmod(path, info.st_mode | stat.S_IWRITE)
        if is_readonly(ordinary(path, directory=directory)):
            raise WorkspaceRefused('scratch readonly attribute could not be cleared')
    return len(readonly)


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
        record['scratch_readonly_cleared'] = make_owned_scratch_writable(root, max_files=limits['max_files'])
        shutil.rmtree(root)
    record.update(phase='retired', scratch_absent=not os.path.lexists(root), reservation_released=True)
    write_json(retained/'receipt.json', record)
    (roots['control']/'active.json').unlink()
    return record


def collect_and_retire(record, config, roots):
    root = owned_scratch(record, roots); limits = config['limits']
    if any(p.name not in ('tmp', 'cache', 'output', 'logs', 'owner.json') for p in root.iterdir()):
        raise WorkspaceRefused('unexpected root output preserved')
    used = tree_usage(root, maximum=limits['scratch_bytes'] + limits['log_bytes'] + 1024 * 1024, max_files=limits['max_files'])
    record['peaks']['scratch_bytes'] = max(record['peaks']['scratch_bytes'], used)
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
            tree_usage(logs, maximum=limits['log_bytes'], max_files=5)
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
    roots.update(canonical_roots(config, job, cwd))
    codex_input = codex_schema = b''
    if job['adapter'] == 'codex_exec':
        with (cwd / job['prompt_file']).open('rb') as stream:
            codex_input = stream.read(65537)
        with (cwd / job['schema_file']).open('rb') as stream:
            codex_schema = stream.read(65537)
        if not 0 < len(codex_input) <= 65536 or not 0 < len(codex_schema) <= 65536:
            raise WorkspaceRefused('Codex input exceeded the one-turn limit')
        if (hashlib.sha256(codex_input).hexdigest() != job['inputs'][job['prompt_file']]
                or hashlib.sha256(codex_schema).hexdigest() != job['inputs'][job['schema_file']]):
            raise WorkspaceRefused('Codex input changed before admission')
    host = host or WindowsJobHost(); limits = config['limits']; active = roots['control'] / 'active.json'
    if job['adapter'] == 'codex_exec' and len(codex_input) >= limits['log_bytes']:
        raise WorkspaceRefused('Codex input consumes the finite retained log allowance')
    with estate_lock(roots['control']):
        with estate_lock(roots['control'], 'dispatch.lock'):
            admitted_dispatch = dispatch_state(roots['control'])
            if admitted_dispatch['mode'] != 'running':
                raise WorkspaceRefused('job dispatch is paused')
            require_codex_permission(config, job, admitted_dispatch)
        if os.path.lexists(active):
            raise WorkspaceRefused('previous job requires explicit reconciliation')
        if os.path.lexists(active.with_name('active.json.next')):
            raise WorkspaceRefused('interrupted admission staging record requires reconciliation')
        canonical_before = canonical_usage(config, job, roots)
        before = probe(roots); reservations = admission(config, roots, before, job.get('canonical_outputs'))
        job_id = uuid.uuid4().hex; root = roots['scratch'] / job_id
        record = {'job_id': job_id, 'manifest_digest': digest(job), 'config_digest': digest(config),
                  'job': job, 'phase': 'reserved', 'reservations': reservations, 'before': before,
                  'created_at_unix_ns': time.time_ns(), 'limits': limits, 'scratch': str(root),
                  'reservation_released': False, 'canonical_before': canonical_before,
                  'peaks': {'scratch_bytes': 0, 'memory_bytes': 0, 'canonical_bytes': canonical_before.copy()}}
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
                used = tree_usage(root, maximum=limits['scratch_bytes'] + limits['log_bytes'],
                                  max_files=limits['max_files'], allow_transient_absence=True,
                                  allow_transient_hardlinks=True)
                record['peaks']['scratch_bytes'] = max(record['peaks']['scratch_bytes'], used)
                for relative, used in canonical_usage(config, job, roots).items():
                    record['peaks']['canonical_bytes'][relative] = max(record['peaks']['canonical_bytes'][relative], used)
                next_scan = now + 30.0
            write_json(active, record)
        dispatch_guard = None
        def checkpoint(stage):
            nonlocal dispatch_guard
            if stage == 'before_create' and job['adapter'] == 'codex_exec':
                # The local executable path is trusted against hostile same-user
                # mutation; check its ordinary parent chain and bytes again at
                # the last host checkpoint before CreateProcessW.
                root_path(str(Path(job['argv'][0]).parent))
                ordinary(job['argv'][0])
                if file_digest(job['argv'][0]) != job['executable_sha256']:
                    raise WorkspaceRefused('executable changed before process creation')
            if stage == 'created_suspended':
                guard = estate_lock(roots['control'], 'dispatch.lock')
                guard.__enter__()
                dispatch_guard = guard
                current = dispatch_state(roots['control'])
                if current != admitted_dispatch:
                    raise WorkspaceRefused('dispatch epoch changed before child resume')
            elif stage == 'resumed' and dispatch_guard is not None:
                dispatch_guard.__exit__(None, None, None)
                dispatch_guard = None
            record['phase'] = stage; write_json(active, record)
        if job['adapter'] == 'python':
            # Python tempfile cannot fall back when the admitted pool disappears.
            bootstrap = "import os,sys,tempfile,runpy; tempfile.tempdir=os.environ['AIDE_JOB_TMP']; a=sys.argv[1:]; sys.argv=([a[1],*a[2:]] if a[0]=='-m' else a); runpy.run_module(a[1],run_name='__main__',alter_sys=True) if a[0]=='-m' else runpy.run_path(a[0],run_name='__main__')"
            argv = [job['argv'][0], '-B', '-u', '-c', bootstrap, *job['argv'][1:]]
            input_bytes = b''
            process_cwd = cwd
        else:
            input_bytes = codex_input
            schema_copy = root / 'tmp' / 'result-schema.json'
            process_cwd = root / 'tmp'
            argv = [job['argv'][0], 'exec', '--ephemeral', '--ignore-user-config', '--json',
                    '--skip-git-repo-check', '--cd', str(process_cwd), '--sandbox', 'read-only',
                    '--output-schema', str(schema_copy), '--model', job['model'],
                    '-c', f'model_reasoning_effort="{job["effort"]}"',
                    '-c', 'approval_policy="never"', '-c', 'forced_login_method="chatgpt"',
                    '-c', 'agents.enabled=false', '-c', 'features.multi_agent=false',
                    '-c', 'features.apps=false', '-c', 'features.hooks=false',
                    '-c', 'features.remote_plugin=false', '-c', 'web_search="disabled"', '-']
        try:
            if job['adapter'] == 'codex_exec':
                admitted_dispatch = admit_codex_turn(roots['control'], admitted_dispatch,
                    config['codex_exec']['max_turns'], codex_request_digest(job))
                schema_copy.write_bytes(codex_schema)
            record['result'] = host.run(argv, cwd=process_cwd, input_bytes=input_bytes, output_dir=root/'logs', job_id=job_id,
                timeout=limits['runtime_seconds'], output_limit=limits['log_bytes'] - len(input_bytes), memory_limit=limits['memory_bytes'],
                process_limit=limits['processes'], cancelled=cancelled, checkpoint=checkpoint, environment=env, observed=observe)
        except BaseException as exc:
            record['result'] = {'reason': type(exc).__name__, 'message': str(exc), 'exit_code': None}
            record['reconciliation'] = host.reconcile(job_id)
        finally:
            if dispatch_guard is not None:
                dispatch_guard.__exit__(None, None, None)
        record['phase'] = 'quiescent'; write_json(active, record)
        record['after'] = probe(roots)
        qualify_canonical_outputs(record, config, roots, working)
        return collect_and_retire(record, config, roots)


def recover(config_path):
    config, roots, working = load_config(config_path)
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
        qualify_canonical_outputs(record, config, roots, working)
        write_json(active, record)
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
    canonical_roots({'limits': record['limits']}, record['job'], root)
    task_id = record['job']['workunit']
    if not isinstance(task_id, str) or not task_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in task_id):
        raise WorkspaceRefused('bounded WorkUnit identifier required')
    ordinary(root/'.aide/queue'/task_id/'task.yaml')
    return record


def require_canonical_outputs(record, paths):
    if not set(paths).issubset(record['job'].get('canonical_outputs', {})):
        raise WorkspaceRefused('command requires declared canonical output reservations')
