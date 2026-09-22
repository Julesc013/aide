"""One-use task controller for the separately reviewed public-input probe."""
from __future__ import annotations
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0, str(HERE))
from h2_system_input import (REPOSITORY, ReadPlan, Refused, decode, exact, _canonical,
                             _finite, _digest, _identity, MAX_INPUT, MAX_OUTPUT, validate_result)
from core.runtime.continuous_worker import windows_security_objects as native
from core.runtime.continuous_worker.windows_image import SourceDirectory, _reserve_journal, _root
from core.runtime.continuous_worker.windows_job import WindowsJobHost
from core.runtime.continuous_worker.windows_security import current_user_sid

BASE = '0c7788fd3660dc18e2751108ac49afe96d446801'
RELATIVE = '.aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/'
SOURCES = tuple(sorted([RELATIVE + name for name in
    ('h2_system_input.py', 'h2_system_input_controller.py', 'h2_system_input_tests.py')] +
    ['core/runtime/continuous_worker/' + name for name in (
     '__init__.py', 'state.py', 'windows_image.py', 'windows_job.py', 'windows_security.py',
     'windows_security_objects.py', 'windows_system_observation.py', 'windows_python_image.py',
     'windows_python_contract.py', 'windows_pe.py')]))
USER = 'S-1-5-21-2168396775-1281633702-301206425-1001'
PYTHON = r'C:\Program Files\Python314\python.exe'
PARENT = r'C:\Users\Jules\AppData\Local\Temp\aide-h1-source-4m92pvi5'
MAX_SOURCE = 2 * 1024 * 1024


def read_effect(value):
    exact(value, ('schema', 'source_base', 'repository', 'source_files', 'interpreter',
                  'user_sid', 'output_parent', 'plan', 'limits', 'effects'))
    if (value['schema'] != 'aide.host.system-input-effect.v1' or value['source_base'] != BASE or
            value['repository'] != str(REPOSITORY) or value['user_sid'] != USER):
        raise Refused('exact reviewed repository/base/controller required')
    pins = exact(value['source_files'], SOURCES)
    for digest in pins.values(): _digest(digest)
    interpreter = exact(value['interpreter'], ('path', 'size', 'sha256'))
    if interpreter['path'] != PYTHON or type(interpreter['size']) is not int or not 1 <= interpreter['size'] <= MAX_SOURCE:
        raise Refused('exact existing bounded interpreter required')
    _digest(interpreter['sha256'])
    parent = exact(value['output_parent'], ('path', 'identity', 'owner_marker', 'owner_sha256'))
    if str(_root(parent['path'])) != PARENT or parent['owner_marker'] != 'owner.json':
        raise Refused('exact previously owned output parent required')
    _identity(parent['identity']); _digest(parent['owner_sha256'])
    plan = ReadPlan.read(value['plan'])
    if value['limits'] != {'child_seconds': 30, 'child_memory': 268435456,
                           'child_processes': 1, 'output_bytes': MAX_OUTPUT}:
        raise Refused('fixed owned-child limits required')
    if value['effects'] != {'ordinary_children': 1, 'read_files': 8, 'selected_mappings': 0,
                            'profile_creations': 0, 'acl_changes': 0, 'network_calls': 0,
                            'cleanup': 'retain_only', 'operational_activation': False}:
        raise Refused('exact read-only effect ceiling required')
    # Reject bool-as-int aliases in the fixed scalar contracts.
    for mapping in (value['limits'], value['effects']):
        for key, item in mapping.items():
            if key not in ('cleanup', 'operational_activation') and type(item) is not int:
                raise Refused('literal integer effect limit required')
    if value['effects']['operational_activation'] is not False: raise Refused('activation refused')
    return plan


def file_hash(path, limit=MAX_SOURCE):
    with open(path, 'rb') as stream:
        data = stream.read(limit + 1)
    if len(data) > limit: raise Refused('bounded source/control bytes required')
    return len(data), hashlib.sha256(data).hexdigest()


class NativeController:
    def verify(self, effect):
        if current_user_sid() != effect['user_sid']: raise Refused('wrong real Windows identity')
        for rel, digest in effect['source_files'].items():
            if file_hash(REPOSITORY / rel)[1] != digest: raise Refused('reviewed source changed')
        # Namespace packages must not gain unpinned initializer code.
        if (REPOSITORY / 'core/__init__.py').exists() or (REPOSITORY / 'core/runtime/__init__.py').exists():
            raise Refused('unreviewed package initializer appeared')
        item = effect['interpreter']
        if file_hash(item['path']) != (item['size'], item['sha256']): raise Refused('interpreter changed')
        parent = effect['output_parent']
        if file_hash(Path(parent['path']) / parent['owner_marker'], 65536)[1] != parent['owner_sha256']:
            raise Refused('owned output origin marker changed')

    @contextmanager
    def parent(self, effect, guard):
        row = effect['output_parent']; lease = SourceDirectory(row['path'], _identity(row['identity']), guard)
        try: yield lease
        finally: lease.close()

    @contextmanager
    def reserve(self, path, parent, guard):
        with _reserve_journal(str(path), parent, guard) as stream:
            yield stream

    def append(self, stream, row):
        data = _canonical(row) + b'\n'
        if len(data) > MAX_OUTPUT: raise Refused('bounded retained journal row required')
        if stream.write(data) != len(data): raise Refused('durable journal write incomplete')
        stream.flush(); os.fsync(stream.fileno())
        return hashlib.sha256(data).hexdigest()

    def run_child(self, *args, **kwargs): return WindowsJobHost().run(*args, **kwargs)

    def output(self, path):
        with open(path / 'stdout', 'rb') as stream: data = stream.read(MAX_OUTPUT + 1)
        with open(path / 'stderr', 'rb') as stream: stderr = stream.read(MAX_OUTPUT + 1)
        if len(data) + len(stderr) > MAX_OUTPUT or stderr:
            raise Refused('child output incomplete or unexpected stderr')
        return data


class Controller:
    def __init__(self, effect, api, *, clock=time.monotonic, wall=time.time):
        self.plan = read_effect(effect)
        self.effect = decode(_canonical(effect))
        self.fingerprint = hashlib.sha256(_canonical(effect)).hexdigest()
        self.api, self.clock, self.wall = api, clock, wall
        self.consumed = False
        self.guard_calls = 0
        self.failure = None
        self.result = None
        self.start = self.last = clock(); self.wall_start = wall()

    def check_time(self):
        now, wall = self.clock(), self.wall()
        if (not all(_finite(item) for item in (now, wall, self.start, self.last, self.wall_start)) or
                now < self.last or wall < self.wall_start or now - self.start >= 90 or
                not 0 < self.plan.expires_at - wall <= 3600):
            raise Refused('effect expired or controller clock invalid')
        self.last = now

    def guard(self):
        self.check_time()
        if self.guard_calls >= 4096: raise Refused('controller observation budget exceeded')
        self.guard_calls += 1
        if hashlib.sha256(_canonical(self.effect)).hexdigest() != self.fingerprint:
            raise Refused('effect differs from frozen controller admission')
        if self.api.verify(self.effect) is False: raise Refused('controller verification refused')
        self.check_time()

    def run(self):
        if self.consumed: raise Refused('controller attempt consumed; no replay')
        self.consumed = True
        request = self.plan.request_id
        parent_path = Path(self.effect['output_parent']['path'])
        output = parent_path / ('system-input-' + request)
        reservation = parent_path / ('system-input-' + request + '.intent.jsonl')
        try:
            self.guard()
            with self.api.parent(self.effect, self.guard) as parent:
                parent.check(); self.guard()
                with self.api.reserve(reservation, parent, self.guard) as journal:
                    intent = {'schema': 'aide.host.system-input-intent.v1', 'effect_sha256': self.fingerprint,
                              'plan_sha256': self.plan.sha256, 'request_id': request, 'output': str(output),
                              'consumed': True, 'replay_permitted': False}
                    acknowledgement = self.api.append(journal, intent)
                    if acknowledgement != hashlib.sha256(_canonical(intent) + b'\n').hexdigest():
                        raise Refused('exact durable intent acknowledgement required')
                    def boundary(_stage=None):
                        parent.check(); self.guard()
                    def cancelled():
                        try: boundary(); return False
                        except Exception: return True
                    boundary()
                    args = [self.effect['interpreter']['path'], '-I', '-S', '-B',
                            str(HERE / 'h2_system_input.py'), '--child', self.plan.sha256]
                    host = self.api.run_child(args, cwd=REPOSITORY, input_bytes=_canonical(self.plan.value()),
                        output_dir=output, job_id=request, timeout=30, output_limit=MAX_OUTPUT,
                        memory_limit=268435456, process_limit=1, cancelled=cancelled, checkpoint=boundary)
                    self.result = {'host': host}
                    if (type(host) is not dict or host.get('exit_code') != 0 or host.get('reason') != 'exited' or
                            host.get('quiescent') is not True or host.get('io_errors') != [] or host.get('job_id') != request):
                        raise Refused('owned child did not finish successfully and quiesce')
                    boundary()
                    raw = self.api.output(output)
                    value = validate_result(raw, self.plan)
                    boundary()
                    result = {'schema': 'aide.host.system-input-controller-result.v1', 'result': 'PASS',
                              'effect_sha256': self.fingerprint, 'host': host,
                              'stdout_sha256': hashlib.sha256(raw).hexdigest(), 'observation': value}
                    observed = {'schema': 'aide.host.system-input-observed.v1',
                                'final_controller_status': 'pending_final_guard', 'observation': result}
                    ack = self.api.append(journal, observed)
                    if ack != hashlib.sha256(_canonical(observed) + b'\n').hexdigest():
                        raise Refused('observed journal acknowledgement differs')
                    self.result = result
            self.guard()
            return self.result
        except Exception as error:
            self.failure = {'error_type': type(error).__name__, 'consumed': True,
                            'effect_sha256': self.fingerprint, 'replay_permitted': False}
            raise Refused('controller refused; retain reservation/output without replay') from error


def main():
    controller = None
    try:
        if len(sys.argv) != 4 or sys.argv[1] != '--run': raise Refused('exact reviewed invocation required')
        expected = _digest(sys.argv[3])
        with open(sys.argv[2], 'rb') as stream: data = stream.read(MAX_INPUT + 1)
        if hashlib.sha256(data).hexdigest() != expected: raise Refused('effect file differs from reviewed raw bytes')
        effect = decode(data)
        controller = Controller(effect, NativeController())
        result = controller.run()
        sys.stdout.buffer.write(_canonical(result)); sys.stdout.buffer.flush()
        return 0
    except Exception as error:
        result = {'result': 'FAIL', 'error_type': type(error).__name__,
                  'failure': controller.failure if controller else None,
                  'replay_permitted': False}
        sys.stdout.buffer.write(_canonical(result)); sys.stdout.buffer.flush()
        return 2


if __name__ == '__main__': raise SystemExit(main())
