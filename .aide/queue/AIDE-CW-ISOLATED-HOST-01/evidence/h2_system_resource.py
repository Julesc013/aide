"""Task-only two-API resource feasibility; actual effects need a separate review."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0, str(HERE))
from h2_system_input import (REPOSITORY, Refused, ReadOnlyApi, NAMES, decode, exact,
                             _canonical, _finite, _digest, MAX_INPUT, MAX_OUTPUT)
from core.runtime.continuous_worker import windows_system_observation as obs
from core.runtime.continuous_worker import windows_security_objects as native

API_NAMES = ('api-ms-win-core-path-l1-1-0.dll', 'api-ms-win-crt-runtime-l1-1-0.dll')
SECONDS = 25


def read_plan(value):
    plan = obs.ObservationPlan.read(value)
    if (tuple(row.name for row in plan.files) != NAMES or plan.api_names != API_NAMES or
            type(plan.max_seconds) is not int or plan.max_seconds != SECONDS):
        raise Refused('exact eight files, two APIs and25-second observation required')
    return plan


def reservation_record(plan, effect):
    return {'schema': 'aide.host.system-resource-reservation.v1', 'request_id': plan.request_id,
            'plan_sha256': plan.fingerprint, 'effect_sha256': effect,
            'consumed': True, 'replay_permitted': False}


def mapping_intents(plan):
    return tuple({'schema': 'aide.host.system-mapping-intent.v1', 'request_id': plan.request_id,
                  'plan_sha256': plan.fingerprint, 'sequence': i, 'api_name': name,
                  'flags': obs.RESOURCE_FLAGS} for i, name in enumerate(plan.api_names))


def line_sha(row): return hashlib.sha256(_canonical(row) + b'\n').hexdigest()


@dataclass(frozen=True)
class Transfer:
    plan: obs.ObservationPlan
    effect: str
    paths: tuple[tuple[str, str], ...]
    reservation_line: str
    intent_lines: tuple[str, ...]

    @classmethod
    def read(cls, value):
        exact(value, ('schema', 'plan', 'effect_sha256', 'observed_paths',
                      'reservation_line_sha256', 'intent_line_sha256s'))
        if value['schema'] != 'aide.host.system-resource-transfer.v1': raise Refused('known resource transfer required')
        plan, effect = read_plan(value['plan']), _digest(value['effect_sha256'])
        paths = exact(value['observed_paths'], NAMES)
        for name, path in paths.items():
            if type(path) is not str or path.casefold() != (plan.native_root + '\\' + name).casefold():
                raise Refused('exact N1 observed native spelling required')
        reserved = _digest(value['reservation_line_sha256'])
        lines = value['intent_line_sha256s']
        if (reserved != line_sha(reservation_record(plan, effect)) or type(lines) is not list or len(lines) != 2 or
                tuple(_digest(item) for item in lines) != tuple(line_sha(row) for row in mapping_intents(plan))):
            raise Refused('exact parent-persisted reservation and both mapping lines required')
        return cls(plan, effect, tuple(sorted(paths.items())), reserved, tuple(lines))

    def value(self):
        return {'schema': 'aide.host.system-resource-transfer.v1', 'plan': self.plan.value(),
                'effect_sha256': self.effect, 'observed_paths': dict(self.paths),
                'reservation_line_sha256': self.reservation_line, 'intent_line_sha256s': list(self.intent_lines)}

    def validate(self):
        if Transfer.read(self.value()) != self: raise Refused('resource transfer changed after admission')
        return self

    @property
    def fingerprint(self): return hashlib.sha256(_canonical(self.value())).hexdigest()


class ParentPaidJournal:
    """Hash tickets acknowledge already-flushed parent rows, not new authority.

    Authentic parent/namespace and trusted ordinary child remain explicit probe
    premises. These hashes are not signatures or proof of adversarial isolation.
    """
    def __init__(self, transfer):
        self.transfer = transfer.validate()
        self.reserved, self.position, self.failed = False, 0, False

    def reserve(self, fingerprint):
        if self.failed or self.reserved or fingerprint != self.transfer.plan.fingerprint:
            self.failed = True
            raise Refused('prepaid reservation differs or has been consumed')
        self.reserved = True
        return fingerprint

    def intent(self, value):
        if self.failed or not self.reserved or self.position >= 2:
            self.failed = True
            raise Refused('prepaid mapping sequence is unavailable')
        expected = mapping_intents(self.transfer.plan)[self.position]
        if _canonical(value) != _canonical(expected) or line_sha(value) != self.transfer.intent_lines[self.position]:
            self.failed = True
            raise Refused('mapping intent differs from the parent-paid exact sequence')
        self.position += 1
        return hashlib.sha256(_canonical(value)).hexdigest()


class Deadline:
    def __init__(self, expiry, *, clock=time.monotonic, wall=time.time):
        self.expiry, self.clock, self.wall = expiry, clock, wall
        self.start = self.last = clock(); self.wall_start = wall()
        self.calls = 0
    def __call__(self):
        now, wall = self.clock(), self.wall()
        if (not all(_finite(v) for v in (now, wall, self.start, self.last, self.wall_start, self.expiry)) or
                now < self.last or wall < self.wall_start or now - self.start >= SECONDS or
                not 0 < self.expiry - wall <= 3600 or self.calls >= 32768):
            raise Refused('resource child deadline/guard budget refused')
        self.last = now; self.calls += 1


class NativeResourceApi(obs.NativeSystemApi):
    def __init__(self):
        super().__init__()
        self.native_refusal = None
        self._directory = native.bind(native.K, 'GetSystemDirectoryW', [obs.W.LPWSTR, obs.W.UINT], obs.W.UINT)
        self._wow = native.bind(native.K, 'IsWow64Process2',
            [obs.W.HANDLE, obs.C.POINTER(obs.W.WORD), obs.C.POINTER(obs.W.WORD)], obs.W.BOOL)
    environment = ReadOnlyApi.environment

    def map_resource(self, name):
        if name not in API_NAMES: raise Refused('only the two exact admitted API requests may map')
        self.native_refusal = None
        try:
            return super().map_resource(name)
        except Refused:
            self.native_refusal = {'operation': 'LoadLibraryExW', 'api_name': name,
                                   'flags': obs.RESOURCE_FLAGS, 'win32_error': obs.C.get_last_error()}
            raise


def environment(api, transfer, guard):
    guard(); value = api.environment(); guard()
    exact(value, ('system_directory', 'native_root', 'process_machine', 'native_machine'))
    if (type(value['system_directory']) is not str or value['system_directory'].casefold() != r'c:\windows\system32' or
            type(value['native_root']) is not str or value['native_root'].casefold() != transfer.plan.native_root.casefold() or
            type(value['process_machine']) is not int or value['process_machine'] != 0 or
            type(value['native_machine']) is not int or value['native_machine'] != 0x8664):
        raise Refused('resource effect native context differs from admission')
    return value


def validate_observation(value, transfer):
    fields = ('schema', 'request_id', 'plan_sha256', 'reservation_acknowledgement', 'root', 'files',
              'mappings', 'native_calls', 'mapping_attempts', 'system_ownership_qualified',
              'api_context_qualified', 'loader_qualified', 'boundary', 'all_owned_handles_released')
    exact(value, fields)
    plan = transfer.plan
    if (value['schema'] != 'aide.host.system-observation-result.v1' or value['request_id'] != plan.request_id or
            value['plan_sha256'] != plan.fingerprint or value['reservation_acknowledgement'] != plan.fingerprint or
            _canonical(value['root']) != _canonical(plan.value()['root']) or
            _canonical(value['files']) != _canonical(plan.value()['files']) or
            type(value['native_calls']) is not int or not 1 <= value['native_calls'] <= obs.MAX_NATIVE_CALLS or
            type(value['mapping_attempts']) is not int or value['mapping_attempts'] != 2 or
            value['all_owned_handles_released'] is not True or
            any(value[key] is not False for key in ('system_ownership_qualified', 'api_context_qualified', 'loader_qualified')) or
            type(value['boundary']) is not str or not 1 <= len(value['boundary']) <= 512):
        raise Refused('resource observation is incomplete, mismatched or overqualified')
    rows = value['mappings']; pins = {pin.name: pin for pin in plan.files}; paths = dict(transfer.paths)
    if type(rows) is not list or len(rows) != 2: raise Refused('exact two mapping outcomes required')
    for row, intent in zip(rows, mapping_intents(plan)):
        exact(row, ('api_name', 'physical_name', 'identity', 'sha256', 'mapped_path', 'mapping_kind', 'intent_acknowledgement'))
        name = row['physical_name']
        if type(name) is not str or name not in pins: raise Refused('unadmitted physical mapping host')
        pin = pins[name]
        if (row['api_name'] != intent['api_name'] or _canonical(row['identity']) != _canonical(list(pin.identity)) or
                row['sha256'] != pin.sha256 or row['mapped_path'] != paths[name] or
                row['mapping_kind'] not in ('resource', 'prior_executable') or
                row['intent_acknowledgement'] != hashlib.sha256(_canonical(intent)).hexdigest()):
            raise Refused('resource mapping result differs from exact paid pins')
    return value


def validate_result(data, transfer):
    value = decode(data)
    exact(value, ('schema', 'result', 'transfer_sha256', 'effect_sha256', 'environment',
                  'observation', 'paid_intents_consumed', 'operational_activation'))
    if (value['schema'] != 'aide.host.system-resource-result.v1' or value['result'] != 'PASS' or
            value['transfer_sha256'] != transfer.fingerprint or value['effect_sha256'] != transfer.effect or
            type(value['paid_intents_consumed']) is not int or value['paid_intents_consumed'] != 2 or
            value['operational_activation'] is not False):
        raise Refused('resource child result differs from its exact transfer')
    # Reuse the same pure environment predicate without a native read.
    class Recorded:
        def environment(self): return value['environment']
    environment(Recorded(), transfer, lambda: None)
    validate_observation(value['observation'], transfer)
    return value


class ResourceProbe:
    def __init__(self, transfer, api, guard, *, clock=time.monotonic, wall=time.time):
        self.transfer, self.api, self.guard = transfer.validate(), api, guard
        self.journal = ParentPaidJournal(transfer)
        self.session = obs.ObservationSession(transfer.plan, api, self.journal, guard, clock=clock, wall_clock=wall)
        self.consumed, self.failure = False, None
    def run(self):
        if self.consumed: raise Refused('resource probe consumed; no replay')
        self.consumed = True
        try:
            before = environment(self.api, self.transfer, self.guard)
            raw = self.session.run()
            after = environment(self.api, self.transfer, self.guard)
            if before != after or self.journal.position != 2: raise Refused('resource context or paid completion changed')
            value = {'schema': 'aide.host.system-resource-result.v1', 'result': 'PASS',
                     'transfer_sha256': self.transfer.fingerprint, 'effect_sha256': self.transfer.effect,
                     'environment': before, 'observation': decode(raw), 'paid_intents_consumed': self.journal.position,
                     'operational_activation': False}
            data = _canonical(value)
            if len(data) > MAX_OUTPUT: raise Refused('resource result exceeds child output bound')
            validate_result(data, self.transfer); self.guard()
            return data
        except Exception as error:
            self.failure = {'error_type': type(error).__name__, 'consumed': True,
                            'session_failure': self.session.failure, 'mapping_attempts': len(self.session.attempts),
                            'paid_intents_consumed': self.journal.position, 'release_failures': self.session.release_failures,
                            'native_refusal': getattr(self.api, 'native_refusal', None),
                            'replay_permitted': False}
            raise Refused('resource feasibility refused; retain without replay') from error


def child(expected):
    probe = None
    try:
        _digest(expected)
        transfer = Transfer.read(decode(sys.stdin.buffer.read(MAX_INPUT + 1)))
        if transfer.fingerprint != expected: raise Refused('parent transfer differs from reviewed input')
        guard = Deadline(transfer.plan.expires_at); guard()
        api = NativeResourceApi(); guard()
        probe = ResourceProbe(transfer, api, guard)
        sys.stdout.buffer.write(probe.run()); sys.stdout.buffer.flush()
        return 0
    except Exception as error:
        value = {'result': 'FAIL', 'error_type': type(error).__name__,
                 'failure': probe.failure if probe else None, 'replay_permitted': False}
        raw = _canonical(value)
        if len(raw) > MAX_OUTPUT: raw = b'{"result":"FAIL","error_type":"output_bound"}'
        sys.stdout.buffer.write(raw); sys.stdout.buffer.flush()
        return 2


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] != '--child': raise SystemExit(2)
    raise SystemExit(child(sys.argv[2]))
