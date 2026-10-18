"""Existing regressions and exact retained history; no source mutation."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, re, subprocess, unittest
from pathlib import Path
ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-HISTORICAL-PRESENTATION-BOUNDARY-02'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
SUBJECT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
def dump(name, obj):
    (OUTPUT / name).write_text(json.dumps(obj, indent=2) + '\n', encoding='utf-8')
def invoke(label, command, expected):
    record = {'command': command, 'state': 'started', 'exit_code': None}
    dump(label + '.invocation.json', record)
    try:
        with (OUTPUT / (label + '.log')).open('xb') as stream:
            r = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                               stdin=subprocess.DEVNULL, timeout=45)
        record.update(state='completed', exit_code=r.returncode)
        assert r.returncode == expected, label
    except BaseException as error:
        record.update(state='exception', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        dump(label + '.invocation.json', record)
    return (OUTPUT / (label + '.log')).read_text(encoding='utf-8')

suite = unittest.TestSuite()
for name in ['test_q27_commit_recovery', 'test_q34_changelog_release']:
    module = load('history_' + name, SUBJECT / '.aide/scripts/tests' / (name + '.py'))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
def ids(tests):
    for item in tests:
        if isinstance(item, unittest.TestSuite):
            yield from ids(item)
        else:
            yield item.id()
expected = list(ids(suite))
assert len(expected) == 45
with (OUTPUT / 'regressions.log').open('w', encoding='utf-8') as log:
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
dump('regressions.json', {'test_ids': expected, 'tests_run': result.testsRun,
    'failures': len(result.failures), 'errors': len(result.errors),
    'skips': [(t.id(), r) for t, r in result.skipped]})
assert result.wasSuccessful() and result.testsRun == 45 and not result.skipped
if SUBJECT != ROOT:
    print('PASS: 45 delivered regressions')
    raise SystemExit(0)
aide = load('historical_actual_cli', ROOT / '.aide/scripts/aide_lite.py')
baseline = json.loads((TASK / 'evidence/history-before.json').read_text(encoding='utf-8'))
scope, boundary = baseline['range'], baseline['boundary']
faults = set(baseline['presentation_failures'])
assert aide.historical_presentation_boundary(ROOT) == boundary
assert aide.commit_is_within_historical_boundary(ROOT, baseline['prior_boundary'], boundary)
assert not aide.commit_is_within_historical_boundary(ROOT, aide.git_commit_for_ref(ROOT, 'HEAD'), boundary)
def git_bytes(*args):
    return subprocess.check_output(['git', *args], env={**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'})
for oid, facts in baseline['objects'].items():
    assert aide.git_commit_object_facts(ROOT, oid) == facts['facts']
    assert hashlib.sha256(git_bytes('cat-file', 'commit', oid)).hexdigest() == facts['object_sha256']
registry = ROOT / '.aide/git/commit-message-dispositions.json'
assert hashlib.sha256(registry.read_bytes()).hexdigest() == baseline['registry_sha256']
commands = {}
for label, extra, code in [('advisory', [], 0), ('raw', ['--no-dispositions'], 1)]:
    cmd = [sys.executable, '-B', str(ROOT / '.aide/scripts/aide_lite.py'),
           'commit', 'check', '--range', scope, *extra]
    text = invoke(label, cmd, code)
    lines = text.splitlines()
    if label == 'advisory':
        assert 'result: PASS_WITH_WARNINGS' in lines
        assert 'original_failure:' in text
        assert not re.search(r'^- [0-9a-f]+ FAIL ', text, re.M)
        found = re.findall(r'^- ([0-9a-f]+) PRESENTATION_ADVISORY ', text, re.M)
    else:
        assert 'result: FAIL' in lines
        found = re.findall(r'^- ([0-9a-f]+) FAIL ', text, re.M)
    assert len(found) == 3 and set(found) == {oid[:len(found[0])] for oid in faults}, found
    commands[label] = {'exit_code': code, 'affected': found}
parsed_failures = set()
for oid, subject, message in aide.git_commit_messages_for_range(ROOT, scope, max_count=100):
    checks = aide.validate_commit_message_text(message)
    if aide.commit_message_result(checks) == 'FAIL':
        parsed_failures.add(oid)
        assert aide.historical_message_is_presentation_only(message, checks)
        assert aide.commit_is_within_historical_boundary(ROOT, oid, boundary)
        parsed = aide.parse_commit_for_changelog(oid, subject, message)
        assert parsed['malformed'] and parsed['entries'] == []
assert parsed_failures == faults
preview = aide.make_changelog_preview(ROOT, revision_range=scope, limit=100)
assert preview == baseline['changelog']
assert preview['commit_count'] == 18 and preview['malformed_count'] == 3
assert {r['commit_sha'] for r in preview['malformed_commits']} == faults
text = invoke('latest', [sys.executable, '-B', str(ROOT / '.aide/scripts/aide_lite.py'),
                         'commit', 'check', '--latest'], 0)
assert 'result: PASS\n' in text
dump('history-result.json', {'result': 'PASS', 'range': scope, 'boundary': boundary,
    'prior_boundary_preserved': True, 'commits': 18, 'presentation_failures': sorted(faults),
    'commands': commands, 'raw_failures_preserved': True, 'changelog_byte_semantics_unchanged': True,
    'objects_and_registry_unchanged': True, 'new_latest_strict_pass': True,
    'models_requested': 0})
print('PASS: 45 regressions and exact 18-commit history; three advisory/raw failures preserved')
