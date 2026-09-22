"""Task-only parent for a separately reviewed two-API resource experiment."""
from __future__ import annotations
import hashlib
import io
import json
from pathlib import Path
import sys
import time
import zipfile

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0, str(HERE))
import h2_system_input_controller as previous
import h2_system_input as read
import h2_system_resource as resource
from h2_system_resource import Refused, _canonical, _digest, exact, decode

BASE = '2a44f17eb7232757133df549ac6fc519d535e71b'
PREFIX = previous.RELATIVE
ARCHIVE = PREFIX + 'h2-input-evidence.zip'
ARCHIVE_SHA = 'df1c3d806c40777e65d5567968f93c909c79d7c091a96f916584bd8213d920fc'
N1_MEMBERS = {
    'h2-input-root-actual-review.json': '9830b14e4cf47a12db25794ee453f9ee7549c41d2dd303b0485a9a6830168513',
    'h2-input-effect-manifest.json': 'e5655f469eef408b87669b5e55700fae6fe9b5a2c5d7bdbee0d05359e537df08',
    'h2-input-actual-controller-stdout.txt': '8c2e3a795bdb1ffab630d216b22ea415693a5658f955366e792bec13019cc2a1'}
SOURCES = tuple(sorted((*previous.SOURCES, ARCHIVE, *(PREFIX + name for name in
    ('h2_system_resource.py', 'h2_system_resource_controller.py', 'h2_system_resource_tests.py')))))


def read_effect(value):
    exact(value, ('schema', 'source_base', 'repository', 'source_files', 'interpreter',
                  'user_sid', 'output_parent', 'plan', 'observed_paths', 'limits', 'effects'))
    if (value['schema'] != 'aide.host.system-resource-effect.v1' or value['source_base'] != BASE or
            value['repository'] != str(previous.REPOSITORY) or value['user_sid'] != previous.USER):
        raise Refused('exact reviewed resource effect repository/base/user required')
    pins = exact(value['source_files'], SOURCES)
    for digest in pins.values(): _digest(digest)
    if pins[ARCHIVE] != ARCHIVE_SHA: raise Refused('exact audited N1 archive required')
    interpreter = exact(value['interpreter'], ('path', 'size', 'sha256'))
    if (interpreter['path'] != previous.PYTHON or type(interpreter['size']) is not int or
            not 1 <= interpreter['size'] <= previous.MAX_SOURCE): raise Refused('bounded existing interpreter pin required')
    _digest(interpreter['sha256'])
    parent = exact(value['output_parent'], ('path', 'identity', 'owner_marker', 'owner_sha256'))
    if str(previous._root(parent['path'])) != previous.PARENT or parent['owner_marker'] != 'owner.json':
        raise Refused('exact previously owned output parent required')
    previous._identity(parent['identity']); _digest(parent['owner_sha256'])
    plan = resource.read_plan(value['plan'])
    expected_limits = {'child_seconds': 30, 'child_memory': 268435456, 'child_processes': 1, 'output_bytes': read.MAX_OUTPUT}
    expected_effects = {'ordinary_children': 1, 'read_files': 8, 'selected_mappings': 2,
        'profile_creations': 0, 'acl_changes': 0, 'network_calls': 0, 'cleanup': 'retain_only', 'operational_activation': False}
    if _canonical(value['limits']) != _canonical(expected_limits) or _canonical(value['effects']) != _canonical(expected_effects):
        raise Refused('fixed bounded two-API effect ceiling required')
    paths = exact(value['observed_paths'], read.NAMES)
    for name, path in paths.items():
        if type(path) is not str or path.casefold() != (plan.native_root + '\\' + name).casefold():
            raise Refused('exact observed native input spelling required')
    return plan


def plan_from_n1(observation, request_id, expires_at):
    root = observation['root']
    identity = lambda row: {'volume': row['identity'][0], 'file_id': row['identity'][1]}
    files = []
    for row in observation['files']:
        facts = row['facts']
        files.append({'name': row['name'], 'identity': identity(facts), 'owner_sid': facts['owner_sid'],
                      'security_sha256': facts['security_sha256'], 'size': facts['size'],
                      'sha256': row['sha256'], 'links': facts['links']})
    value = {'schema': 'aide.host.system-observation.v1', 'request_id': request_id,
             'root': {'path': root['path'], 'identity': identity(root), 'owner_sid': root['owner_sid'],
                      'security_sha256': root['security_sha256']}, 'files': files,
             'api_names': list(resource.API_NAMES), 'expires_at': expires_at, 'max_seconds': resource.SECONDS}
    return resource.read_plan(value)


def audited_n1(raw):
    if type(raw) is not bytes or len(raw) > previous.MAX_SOURCE or hashlib.sha256(raw).hexdigest() != ARCHIVE_SHA:
        raise Refused('bounded byte-exact N1 custody archive required')
    rows = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        infos = archive.infolist()
        if len(infos) > 128 or len({info.filename for info in infos}) != len(infos):
            raise Refused('bounded unambiguous N1 archive directory required')
        for name, digest in N1_MEMBERS.items():
            info = archive.getinfo('files/' + PREFIX + name)
            if not 0 < info.file_size <= read.MAX_INPUT or info.compress_size > len(raw):
                raise Refused('bounded exact N1 member required')
            value = archive.read(info)
            if hashlib.sha256(value).hexdigest() != digest: raise Refused('N1 original member differs')
            rows[name] = decode(value)
    original_plan = read.ReadPlan.read(rows['h2-input-effect-manifest.json']['plan'])
    controller = rows['h2-input-actual-controller-stdout.txt']
    observation = read.validate_result(_canonical(controller['observation']), original_plan)
    return observation


class NativeParent(previous.NativeController):
    def __init__(self): self.observation = None
    def verify(self, effect):
        super().verify(effect)
        if self.observation is None:
            with open(previous.REPOSITORY / ARCHIVE, 'rb') as stream: raw = stream.read(previous.MAX_SOURCE + 1)
            self.observation = audited_n1(raw)
        plan = resource.read_plan(effect['plan'])
        expected = plan_from_n1(self.observation, plan.request_id, plan.expires_at)
        paths = {row['name']: row['facts']['path'] for row in self.observation['files']}
        if plan != expected or effect['observed_paths'] != paths:
            raise Refused('resource pins differ from independently audited N1 facts')


class Controller(previous.Controller):
    def __init__(self, effect, api, *, clock=time.monotonic, wall=time.time):
        self.plan = read_effect(effect)
        self.effect = decode(_canonical(effect))
        self.fingerprint = hashlib.sha256(_canonical(effect)).hexdigest()
        self.api, self.clock, self.wall = api, clock, wall
        self.consumed, self.guard_calls = False, 0
        self.failure, self.result = None, None
        self.start = self.last = clock(); self.wall_start = wall()

    def run(self):
        if self.consumed: raise Refused('resource controller consumed; no replay')
        self.consumed = True
        request = self.plan.request_id
        parent_path = Path(self.effect['output_parent']['path'])
        output = parent_path / ('system-resource-' + request)
        reservation = parent_path / ('system-resource-' + request + '.intent.jsonl')
        try:
            self.guard()
            with self.api.parent(self.effect, self.guard) as parent:
                parent.check(); self.guard()
                with self.api.reserve(reservation, parent, self.guard) as journal:
                    def persist(row):
                        expected = resource.line_sha(row)
                        if self.api.append(journal, row) != expected: raise Refused('exact durable parent row acknowledgement required')
                        return expected
                    reserved = persist(resource.reservation_record(self.plan, self.fingerprint))
                    intents = []
                    for row in resource.mapping_intents(self.plan):
                        parent.check(); self.guard(); intents.append(persist(row))
                    transfer = resource.Transfer.read({'schema': 'aide.host.system-resource-transfer.v1',
                        'plan': self.plan.value(), 'effect_sha256': self.fingerprint,
                        'observed_paths': self.effect['observed_paths'], 'reservation_line_sha256': reserved,
                        'intent_line_sha256s': intents})
                    def boundary(_stage=None): parent.check(); self.guard()
                    def cancelled():
                        try: boundary(); return False
                        except Exception: return True
                    boundary()
                    args = [self.effect['interpreter']['path'], '-I', '-S', '-B',
                            str(HERE / 'h2_system_resource.py'), '--child', transfer.fingerprint]
                    host = self.api.run_child(args, cwd=previous.REPOSITORY, input_bytes=_canonical(transfer.value()),
                        output_dir=output, job_id=request, timeout=30, output_limit=read.MAX_OUTPUT,
                        memory_limit=268435456, process_limit=1, cancelled=cancelled, checkpoint=boundary)
                    self.result = {'host': host}
                    if (type(host) is not dict or type(host.get('exit_code')) is not int or host['exit_code'] != 0 or
                            host.get('reason') != 'exited' or host.get('quiescent') is not True or
                            host.get('io_errors') != [] or host.get('job_id') != request):
                        raise Refused('resource child did not finish and quiesce')
                    boundary(); raw = self.api.output(output)
                    value = resource.validate_result(raw, transfer); boundary()
                    result = {'schema': 'aide.host.system-resource-controller-result.v1', 'result': 'PASS',
                              'effect_sha256': self.fingerprint, 'host': host,
                              'stdout_sha256': hashlib.sha256(raw).hexdigest(), 'observation': value}
                    persist({'schema': 'aide.host.system-resource-observed.v1',
                             'final_controller_status': 'pending_final_guard', 'observation': result})
                    self.result = result
            self.guard()
            return self.result
        except Exception as error:
            self.failure = {'error_type': type(error).__name__, 'consumed': True,
                            'effect_sha256': self.fingerprint, 'replay_permitted': False}
            raise Refused('resource controller refused; retain intent/output without replay') from error


def main():
    controller = None
    try:
        if len(sys.argv) != 4 or sys.argv[1] != '--run': raise Refused('exact separately reviewed invocation required')
        expected = _digest(sys.argv[3])
        with open(sys.argv[2], 'rb') as stream: raw = stream.read(read.MAX_INPUT + 1)
        if hashlib.sha256(raw).hexdigest() != expected: raise Refused('resource effect differs from reviewed bytes')
        controller = Controller(decode(raw), NativeParent())
        value = controller.run()
        sys.stdout.buffer.write(_canonical(value)); sys.stdout.buffer.flush()
        return 0
    except Exception as error:
        value = {'result': 'FAIL', 'error_type': type(error).__name__,
                 'failure': controller.failure if controller else None, 'replay_permitted': False}
        sys.stdout.buffer.write(_canonical(value)); sys.stdout.buffer.flush()
        return 2


if __name__ == '__main__': raise SystemExit(main())
