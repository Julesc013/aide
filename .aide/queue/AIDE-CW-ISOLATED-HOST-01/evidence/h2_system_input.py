"""Task-owned eight-file read-facts probe; no selected DLL mapping or execution."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
from pathlib import Path
import re
import sys
import time

REPOSITORY = Path(__file__).resolve().parents[4]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))
from core.runtime.continuous_worker.state import Refused
from core.runtime.continuous_worker import windows_security_objects as native
from core.runtime.continuous_worker.windows_system_observation import (
    NativeSystemApi, ObjectFacts, _canonical, _finite, _native_root, _sid)
from core.runtime.continuous_worker.windows_python_contract import _identity, _digest

NAMES = tuple(sorted(('advapi32.dll', 'bcrypt.dll', 'kernel32.dll', 'version.dll',
                      'ws2_32.dll', 'ntdll.dll', 'ucrtbase.dll', 'kernelbase.dll')))
MAX_INPUT = 65536
MAX_OUTPUT = 65536
MAX_FILE = 16 * 1024 * 1024
MAX_CALLS = 4096
SECONDS = 25
CHUNK = 65536


def exact(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        raise Refused('exact known object fields required')
    return value


def decode(data):
    if type(data) is not bytes or not 0 < len(data) <= MAX_INPUT:
        raise Refused('bounded JSON bytes required')
    def pairs(rows):
        result = {}
        for key, value in rows:
            if key in result: raise Refused('duplicate JSON field refused')
            result[key] = value
        return result
    def constant(_): raise Refused('non-finite JSON constant refused')
    try:
        return json.loads(data.decode('utf-8'), object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, UnicodeError, RecursionError) as error:
        raise Refused('well-formed bounded JSON required') from error


@dataclass(frozen=True)
class FilePin:
    name: str
    size: int
    sha256: str


@dataclass(frozen=True)
class ReadPlan:
    request_id: str
    expires_at: float
    system_directory: str
    native_root: str
    files: tuple[FilePin, ...]

    @classmethod
    def read(cls, value):
        exact(value, ('schema', 'request_id', 'expires_at', 'system_directory', 'native_root', 'files'))
        if value['schema'] != 'aide.host.system-input.v1': raise Refused('known input plan required')
        request = value['request_id']
        if type(request) is not str or not re.fullmatch('[0-9a-f]{32}', request):
            raise Refused('literal request identity required')
        expiry = value['expires_at']
        if not _finite(expiry) or expiry <= 0: raise Refused('finite expiry required')
        if value['system_directory'] != r'C:\Windows\System32':
            raise Refused('this reviewed probe admits only the exact Windows system root')
        root = _native_root(value['native_root'])
        rows = value['files']
        if type(rows) is not list or len(rows) != len(NAMES): raise Refused('exact eight files required')
        files = []
        for row in rows:
            exact(row, ('name', 'size', 'sha256'))
            if type(row['name']) is not str or row['name'] not in NAMES:
                raise Refused('unknown public input name refused')
            if type(row['size']) is not int or not 64 <= row['size'] <= MAX_FILE:
                raise Refused('bounded expected input size required')
            files.append(FilePin(row['name'], row['size'], _digest(row['sha256'])))
        files.sort(key=lambda row: row.name)
        if tuple(row.name for row in files) != NAMES: raise Refused('duplicate or missing public input')
        return cls(request, expiry, value['system_directory'], root, tuple(files))

    def value(self):
        return {'schema': 'aide.host.system-input.v1', 'request_id': self.request_id,
                'expires_at': self.expires_at, 'system_directory': self.system_directory,
                'native_root': self.native_root, 'files': [asdict(row) for row in self.files]}

    @property
    def sha256(self): return hashlib.sha256(_canonical(self.value())).hexdigest()


class ReadOnlyApi:
    """Only native read ABI bindings; selected resource/loader methods are absent."""
    def __init__(self):
        if sys.platform != 'win32' or C.sizeof(C.c_void_p) != 8:
            raise Refused('64-bit Windows process required')
        bind = native.bind
        self._read = bind(native.K, 'ReadFile', [W.HANDLE, C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.c_void_p], W.BOOL)
        self._final = bind(native.K, 'GetFinalPathNameByHandleW', [W.HANDLE, W.LPWSTR, W.DWORD, W.DWORD], W.DWORD)
        self._sid = bind(native.A, 'ConvertSidToStringSidW', [C.c_void_p, C.POINTER(W.LPWSTR)], W.BOOL)
        self._directory = bind(native.K, 'GetSystemDirectoryW', [W.LPWSTR, W.UINT], W.UINT)
        self._wow = bind(native.K, 'IsWow64Process2', [W.HANDLE, C.POINTER(W.WORD), C.POINTER(W.WORD)], W.BOOL)
        self._process = bind(native.K, 'GetCurrentProcess', [], W.HANDLE)

    def environment(self):
        process, machine = W.WORD(), W.WORD()
        native._check(self._wow(self._process(), C.byref(process), C.byref(machine)))
        if process.value != 0 or machine.value != 0x8664:
            raise Refused('native AMD64 host/process required; no emulation fallback')
        path = C.create_unicode_buffer(260)
        count = self._directory(path, len(path))
        if not 0 < count < len(path): raise Refused('system directory unavailable or truncated')
        return {'system_directory': path.value, 'native_root': native.native_path(path.value),
                'process_machine': process.value, 'native_machine': machine.value}

    open_root = NativeSystemApi.open_root
    open_file = NativeSystemApi.open_file
    facts = NativeSystemApi.facts
    read_file = NativeSystemApi.read_file
    close_file = NativeSystemApi.close_file


def checked_facts(facts, expected_path, *, directory, size=0):
    if not isinstance(facts, ObjectFacts): raise Refused('typed native facts required')
    if type(facts.identity) is not tuple or len(facts.identity) != 2: raise Refused('exact object identity required')
    _identity({'volume': facts.identity[0], 'file_id': facts.identity[1]})
    _sid(facts.owner_sid); _digest(facts.security_sha256)
    if (type(facts.path) is not str or len(facts.path) > 1023 or
            facts.path.casefold() != expected_path.casefold() or
            facts.directory is not directory or facts.delete_pending is not False or
            type(facts.size) is not int or facts.size != size or
            type(facts.links) is not int or not 1 <= facts.links <= 1024):
        raise Refused('native file kind/name/size/link facts differ')
    return facts


def result_facts(value):
    exact(value, ('path', 'identity', 'directory', 'delete_pending', 'size', 'links',
                  'owner_sid', 'security_sha256'))
    if type(value['identity']) is not list or len(value['identity']) != 2:
        raise Refused('exact serialized native identity required')
    return ObjectFacts(**dict(value, identity=tuple(value['identity'])))


def validate_result(data, plan):
    value = decode(data)
    flags = ('system_ownership_qualified', 'api_context_qualified', 'loader_qualified', 'operational_activation')
    exact(value, ('schema', 'request_id', 'plan_sha256', 'result', 'consumed', 'calls',
                  'root', 'files', 'failure', 'close_attempts', 'release_failures') + flags)
    if (value['schema'] != 'aide.host.system-input-result.v1' or value['request_id'] != plan.request_id or
            value['plan_sha256'] != plan.sha256 or value['result'] != 'PASS' or value['consumed'] is not True or
            type(value['calls']) is not int or not 1 <= value['calls'] <= MAX_CALLS or
            type(value['close_attempts']) is not int or value['close_attempts'] != 9 or
            value['release_failures'] != [] or value['failure'] is not None or
            any(value[key] is not False for key in flags)):
        raise Refused('child result is missing, mismatched or unqualified')
    root = checked_facts(result_facts(value['root']), plan.native_root, directory=True)
    rows = value['files']; identities = {root.identity}
    if type(rows) is not list or len(rows) != 8: raise Refused('all eight observed rows required')
    for row, pin in zip(rows, plan.files):
        exact(row, ('name', 'sha256', 'facts'))
        facts = checked_facts(result_facts(row['facts']), root.path + '\\' + pin.name,
                              directory=False, size=pin.size)
        if (row['name'] != pin.name or row['sha256'] != pin.sha256 or facts.identity in identities or
                facts.identity[0] != root.identity[0]):
            raise Refused('complete distinct observed byte pins required')
        identities.add(facts.identity)
    return value


class ReadProbe:
    def __init__(self, plan, api, guard, *, clock=time.monotonic, wall=time.time):
        if not isinstance(plan, ReadPlan) or ReadPlan.read(plan.value()) != plan or not callable(guard):
            raise Refused('immutable typed input plan and guard required')
        self.plan, self.api, self.guard, self.clock, self.wall = plan, api, guard, clock, wall
        self.consumed = False
        self.calls = 0
        self.owned = []
        self.closed = []
        self.release_failures = []
        self.rows = []
        self.root = None
        self.failure = None
        self.phase = 'admission'

    def check(self):
        for after in (False, True):
            now, wall = self.clock(), self.wall()
            if (not all(_finite(item) for item in (now, wall, self.start, self.last, self.wall_start)) or now < self.last or wall < self.wall_start or
                    now - self.start >= SECONDS or not 0 < self.plan.expires_at - wall <= 3600):
                raise Refused('input probe is stale or clock invalid')
            self.last = now
            if not after and self.guard() is False: raise Refused('controller guard refused')

    def call(self, method, *args, acquire=False):
        self.check()
        if self.calls >= MAX_CALLS: raise Refused('input adapter call limit exceeded')
        self.calls += 1
        value = getattr(self.api, method)(*args)
        if acquire:
            if type(value) is not int or value <= 0 or value in self.owned or value in self.closed:
                raise Refused('distinct owned native handle required')
            self.owned.append(value)
        self.check()
        return value

    def facts(self, handle, expected_path, *, directory, size=0):
        return checked_facts(self.call('facts', handle), expected_path, directory=directory, size=size)

    def environment(self):
        value = self.call('environment')
        exact(value, ('system_directory', 'native_root', 'process_machine', 'native_machine'))
        if (type(value['system_directory']) is not str or type(value['native_root']) is not str or
                value['system_directory'].casefold() != self.plan.system_directory.casefold() or
                value['native_root'].casefold() != self.plan.native_root.casefold() or
                type(value['process_machine']) is not int or value['process_machine'] != 0 or
                type(value['native_machine']) is not int or value['native_machine'] != 0x8664):
            raise Refused('system root/volume/architecture differs from admission')
        return value

    def run(self):
        if self.consumed: raise Refused('input probe is consumed; no replay')
        self.consumed = True
        self.start = self.last = self.clock(); self.wall_start = self.wall()
        error = None
        try:
            self.check(); environment = self.environment()
            self.phase = 'open'
            root_handle = self.call('open_root', self.plan.native_root, acquire=True)
            root = self.facts(root_handle, self.plan.native_root, directory=True)
            self.root = asdict(root)
            held = []; identities = {root.identity}
            for pin in self.plan.files:
                handle = self.call('open_file', root_handle, pin.name, acquire=True)
                facts = self.facts(handle, root.path + '\\' + pin.name, directory=False, size=pin.size)
                if facts.identity in identities or facts.identity[0] != root.identity[0]:
                    raise Refused('distinct same-volume input objects required')
                identities.add(facts.identity); held.append((pin, handle, facts))
            self.phase = 'hash'
            for pin, handle, before in held:
                digest = hashlib.sha256(); remaining = pin.size
                while remaining:
                    chunk = self.call('read_file', handle, min(remaining, CHUNK))
                    if type(chunk) is not bytes or len(chunk) != min(remaining, CHUNK):
                        raise Refused('short or oversized public input read')
                    digest.update(chunk); remaining -= len(chunk)
                if self.call('read_file', handle, 1) != b'' or digest.hexdigest() != pin.sha256:
                    raise Refused('public input bytes differ from historical pin')
                self.rows.append({'name': pin.name, 'sha256': digest.hexdigest(), 'facts': asdict(before)})
            self.phase = 'reobserve'
            for pin, handle, before in held:
                if self.facts(handle, before.path, directory=False, size=pin.size) != before:
                    raise Refused('held public input facts changed')
            if self.facts(root_handle, root.path, directory=True) != root or self.environment() != environment:
                raise Refused('held root or native environment changed')
            self.check()
        except Exception as caught:
            error = caught
        finally:
            # Consume each release before dispatch. Continue others even when one
            # fails, without claiming the uncertain handle was actually closed.
            while self.owned:
                handle = self.owned.pop(); self.closed.append(handle)
                try:
                    if self.api.close_file(handle) is not True: raise Refused('close not acknowledged')
                except Exception as caught:
                    self.release_failures.append(type(caught).__name__)
        try:
            if error is not None: raise error
            if self.release_failures: raise Refused('native release uncertain')
            self.phase = 'final'
            self.check()
            result = self.evidence('PASS')
            output = _canonical(result)
            if len(output) > MAX_OUTPUT: raise Refused('output bound exceeded')
            self.check()
            return output
        except Exception as caught:
            self.failure = {'phase': self.phase, 'error_type': type(caught).__name__}
            raise Refused('read-facts probe refused; consumed evidence retained') from caught

    def evidence(self, result='FAIL'):
        return {'schema': 'aide.host.system-input-result.v1', 'request_id': self.plan.request_id,
                'plan_sha256': self.plan.sha256, 'result': result, 'consumed': self.consumed,
                'calls': self.calls, 'root': self.root, 'files': self.rows, 'failure': self.failure,
                'close_attempts': len(self.closed), 'release_failures': self.release_failures,
                'system_ownership_qualified': False, 'api_context_qualified': False,
                'loader_qualified': False, 'operational_activation': False}


def child(expected):
    probe = None
    try:
        _digest(expected)
        plan = ReadPlan.read(decode(sys.stdin.buffer.read(MAX_INPUT + 1)))
        if plan.sha256 != expected: raise Refused('exact parent-admitted plan required')
        probe = ReadProbe(plan, ReadOnlyApi(), lambda: True)
        sys.stdout.buffer.write(probe.run()); sys.stdout.buffer.flush()
        return 0
    except Exception as error:
        value = probe.evidence() if probe else {'result': 'FAIL', 'error_type': type(error).__name__}
        data = _canonical(value)
        if len(data) > MAX_OUTPUT: data = b'{"result":"FAIL","error_type":"output_bound"}'
        sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
        return 2


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] != '--child': raise SystemExit(2)
    raise SystemExit(child(sys.argv[2]))
