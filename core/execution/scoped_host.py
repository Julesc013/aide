"""Readonly scoped worker adapter for the existing pinned managed owner.

Placement is delegated to the installed Codex command sandbox; this module
does not sandbox its caller, promise read isolation, allocate pools or retire
jobs. Aggregate admission runs while the existing owner holds its estate lock.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
import time


class ScopeRefused(ValueError):
    pass


def sha(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1048576), b''):
            value.update(chunk)
    return value.hexdigest()


def ordinary(path, *, directory=False):
    path = Path(path)
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 1024:
        raise ScopeRefused('scope link/reparse path refused')
    if directory:
        if not stat.S_ISDIR(info.st_mode):
            raise ScopeRefused('scope directory required')
    elif not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ScopeRefused('scope ordinary single-link file required')
    return info


def bounded_path(value, *, directory=False):
    path = Path(value)
    if not path.is_absolute() or '..' in path.parts or path == Path(path.anchor):
        raise ScopeRefused('scope absolute bounded path required')
    for parent in reversed(path.parents):
        ordinary(parent, directory=True)
    ordinary(path, directory=directory)
    if path.resolve() != path:
        raise ScopeRefused('scope path alias refused')
    return path


def validate_selection(selection, repo):
    expected = {'schema', 'kind', 'codex_executable', 'codex_sha256',
                'read_roots', 'aggregate_bytes', 'runtime'}
    if (not isinstance(selection, dict) or set(selection) != expected
            or selection['schema'] != 'aide.scoped-host.local.v1'
            or selection['kind'] != 'codex_sandbox_readonly'):
        raise ScopeRefused('exact readonly scoped host selection required')
    cap = selection['aggregate_bytes']
    if type(cap) is not int or cap <= 0:
        raise ScopeRefused('finite positive aggregate pool limit required')
    exe = bounded_path(selection['codex_executable'])
    if sha(exe) != selection['codex_sha256']:
        raise ScopeRefused('scoped host executable changed')
    reads = selection['read_roots']
    if not isinstance(reads, list) or not reads:
        raise ScopeRefused('explicit toolchain read roots required')
    for value in reads:
        bounded_path(value, directory=True)
    pin = selection['runtime']
    if not isinstance(pin, dict) or set(pin) != {'root', 'files'}:
        raise ScopeRefused('exact pinned execution runtime required')
    relative = Path(pin['root'])
    if relative.is_absolute() or '..' in relative.parts:
        raise ScopeRefused('runtime root must be repository relative')
    frozen = bounded_path(str(repo / relative), directory=True)
    files = pin['files']
    if not isinstance(files, dict) or not 1 <= len(files) <= 128:
        raise ScopeRefused('bounded runtime dependency closure required')
    required = {str(relative / p).replace('\\', '/') for p in (
        'core/execution/managed_workspace.py',
        'core/runtime/continuous_worker/windows_job.py')}
    if not required.issubset(files):
        raise ScopeRefused('runtime owner and process host must be pinned')
    for name, expected_sha in files.items():
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts or not (repo / rel).is_relative_to(frozen):
            raise ScopeRefused('runtime dependency escapes pinned root')
        path = bounded_path(str(repo / rel))
        if sha(path) != expected_sha:
            raise ScopeRefused('pinned execution component changed: ' + name)
    # Python may read an existing bytecode cache even with -B. Refuse it rather
    # than execute bytes absent from the accepted source identity.
    entries = 0
    for path in (frozen / 'core').rglob('*'):
        entries += 1
        if entries > 1024:
            raise ScopeRefused('runtime dependency observation incomplete')
        ordinary(path, directory=path.is_dir())
        if path.suffix == '.pyc':
            raise ScopeRefused('unpinned runtime bytecode cache refused')
        if path.suffix == '.py' and path.relative_to(repo).as_posix() not in files:
            raise ScopeRefused('unpinned runtime source refused')
    return frozen


def load_owner(selection, repo):
    """Load the accepted owner before edited source can become its supervisor."""
    repo = bounded_path(str(repo), directory=True)
    frozen = validate_selection(selection, repo)
    if any(name == 'core' or name.startswith('core.') for name in sys.modules):
        raise ScopeRefused('execution core already loaded; use a fresh job entry process')
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(frozen))
    owner = importlib.import_module('core.execution.managed_workspace')
    for name, module in tuple(sys.modules.items()):
        if name.startswith('core.') and getattr(module, '__file__', None):
            path = Path(module.__file__).resolve()
            if (not path.is_relative_to(frozen)
                    or path.relative_to(repo).as_posix() not in selection['runtime']['files']):
                raise ScopeRefused('runtime import escaped pinned dependency closure')
    return owner


def aggregate_admission(roots, limits, ceiling, *, seconds=20):
    """Complete bounded logical-byte inventory plus worst-case next allocation."""
    began = time.monotonic()
    used = entries = 0
    by_pool = {}
    for key in ('scratch', 'retained', 'control'):
        pool_used = 0
        pending = [roots[key]]
        while pending:
            with os.scandir(pending.pop()) as iterator:
                for entry in iterator:
                    entries += 1
                    if entries > limits['max_files'] or time.monotonic() - began > seconds:
                        raise ScopeRefused('aggregate pool observation incomplete')
                    info = ordinary(entry.path, directory=entry.is_dir(follow_symlinks=False))
                    if stat.S_ISDIR(info.st_mode):
                        pending.append(Path(entry.path))
                    else:
                        pool_used += info.st_size
        used += pool_used
        by_pool[key] = pool_used
    reserved = (limits['scratch_bytes'] + limits['retained_bytes']
                + 2 * limits['log_bytes'] + 2 * 1048576)
    if used + reserved > ceiling:
        raise ScopeRefused('aggregate pool budget cannot admit the next job')
    return {'logical_bytes': used, 'by_pool': by_pool,
            'reserved_bytes': reserved, 'limit_bytes': ceiling,
            'enforcement': 'cooperative_admission_and_monitored_growth'}


def prepare(config_path, repo):
    """Return the pinned owner and its thin host; never allocate or fallback."""
    config_path = bounded_path(str(Path(config_path).absolute()))
    if ordinary(config_path).st_size > 1048576:
        raise ScopeRefused('scoped config too large')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ScopeRefused('duplicate scoped config key')
            result[key] = value
        return result
    config = json.loads(config_path.read_text(encoding='utf-8'), object_pairs_hook=unique)
    selection = config['execution_host']
    owner = load_owner(selection, Path(repo))
    _, roots, _ = owner.load_config(config_path)

    class ScopedHost(owner.WindowsJobHost):
        inventory = None

        def admission_probe(self, observed_roots):
            # owner.run calls this first under estate_lock, before allocation.
            # Later samples use OS counters; no repeated pool-wide scans.
            if self.inventory is None:
                self.inventory = aggregate_admission(
                    roots, config['limits'], selection['aggregate_bytes'])
            return owner.capacity(observed_roots)

        def run(self, argv, **kwargs):
            if self.inventory is None:
                raise ScopeRefused('scoped launch has no locked aggregate admission')
            scratch = Path(kwargs['output_dir']).parent
            rules = {':root': 'deny', ':minimal': 'read', str(Path(repo)): 'read'}
            for value in selection['read_roots']:
                rules[value] = 'read'
            rules.update({str(Path(repo) / '.aide.local'): 'deny',
                          str(config_path): 'deny', str(roots['control']): 'deny',
                          str(roots['control'] / 'active.json'): 'read',
                          str(scratch): 'read'})
            for member in ('tmp', 'cache', 'output'):
                rules[str(scratch / member)] = 'write'
            profile = 'aide_readonly_' + kwargs['job_id']
            inline = '{' + ','.join(json.dumps(k) + '=' + json.dumps(v) for k, v in rules.items()) + '}'
            scoped = [selection['codex_executable'], 'sandbox', '-P', profile,
                      '-c', 'permissions.' + profile + '.filesystem=' + inline,
                      '-c', 'permissions.' + profile + '.network.enabled=false', '--', *argv]
            owner.write_json(scratch / 'output/effective-scope.json', {
                'schema': 'aide.scoped-host.observation.v1', 'filesystem': rules,
                'network_enabled': False, 'aggregate_admission': self.inventory,
                'outer_session_contained': False, 'read_isolation': 'unqualified',
                'host_executable_sha256': selection['codex_sha256']})
            return super().run(scoped, **kwargs)

    return owner, ScopedHost()


def run(owner, host, config_path, job):
    if job.get('adapter') != 'python' or job.get('canonical_outputs'):
        raise ScopeRefused('scoped entry currently permits readonly Python checks only')
    return owner.run(config_path, job, host=host, probe=host.admission_probe)
