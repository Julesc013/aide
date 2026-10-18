"""Qualify HTML presentation and preserve all 84 existing brief-related assertions."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT = Path.cwd()
repair = False
SUBJECT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 and not repair else ROOT
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
label = 'source-repair' if repair else ('source' if SUBJECT == ROOT else 'delivered')
suite = unittest.TestSuite()
inputs = {}
for name in ['test_task_brief_view', 'test_task_brief', 'test_task_current', 'test_resume_plan', 'test_q38_file_quality', 'test_outcome_lessons']:
    path = SUBJECT / '.aide/scripts/tests' / (name + '.py')
    spec = importlib.util.spec_from_file_location('validation_' + name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    assert Path(getattr(module, 'aide', getattr(module, 'aide_lite', None)).__file__).resolve() == SUBJECT / '.aide/scripts/aide_lite.py'
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    inputs[path.relative_to(SUBJECT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
for relative in ['.aide/scripts/aide_lite.py', '.aide/scripts/outcome_lessons.py', '.aide/scripts/task_brief_view.py']:
    inputs[relative] = hashlib.sha256((SUBJECT / relative).read_bytes()).hexdigest()
def ids(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from ids(test)
        else:
            yield test.id()
expected = list(ids(suite))
expected_count = 104
assert len(expected) == expected_count and len(set(expected)) == expected_count
with (OUTPUT / (label + '-tests.log')).open('w', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
record = {'subject': label, 'test_ids': expected, 'tests_run': result.testsRun,
          'failures': len(result.failures), 'errors': len(result.errors),
          'skips': [(case.id(), why) for case, why in result.skipped], 'inputs': inputs,
          'models_requested': 0, 'whole_outcome_usage': 'unknown'}
(OUTPUT / (label + '-tests.json')).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
assert result.testsRun == expected_count and result.wasSuccessful() and not result.skipped
for path, digest in inputs.items():
    assert hashlib.sha256((SUBJECT / path).read_bytes()).hexdigest() == digest
print(json.dumps({'status': 'PASS', 'subject': label, 'tests': result.testsRun}))


if SUBJECT == ROOT:
    import subprocess
    from html.parser import HTMLParser
    selected_task = 'AIDE-VALIDATION-OUTPUT-01'
    selected_path = '.aide/scripts/tests/test_validation_output.py'
    observed_refs = ['.aide/controller/outcome-ledger.jsonl', '.aide/reports/file-quality-ledger.json',
        '.aide/queue/' + selected_task + '/task.yaml', '.aide/queue/' + selected_task + '/status.yaml']
    before = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in observed_refs}
    results = {}
    for mode in ['json', 'html']:
        args = [sys.executable, '-I', '-B', str(ROOT/'.aide/scripts/aide_lite.py'),
                'task', 'brief', '--task-id', selected_task, '--path', selected_path, '--'+mode]
        stdout = OUTPUT/('actual-brief.'+mode)
        stderr = OUTPUT/('actual-brief-'+mode+'.stderr')
        receipt = OUTPUT/('actual-brief-'+mode+'.invocation.json')
        record = {'command': args, 'cwd': str(ROOT), 'state': 'started', 'exit_code': None}
        def save():
            receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
        save()
        try:
            with stdout.open('xb') as out, stderr.open('xb') as err:
                called = subprocess.run(args, cwd=ROOT, stdin=subprocess.DEVNULL,
                                        stdout=out, stderr=err, timeout=30)
            record.update(state='completed', exit_code=called.returncode)
        except (OSError, subprocess.SubprocessError) as error:
            record.update(state='exception', error_type=type(error).__name__, error=str(error))
            raise
        finally:
            record['streams']={p.name:{'bytes':p.stat().st_size,
                'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (stdout,stderr) if p.exists()}
            save()
        assert called.returncode in (0,2) and not stderr.read_bytes()
        results[mode] = {'exit_code': called.returncode, 'stdout': stdout.read_bytes()}
    class Observation(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.selected = False; self.parts = []
        def handle_starttag(self, tag, attrs):
            if tag == 'pre' and dict(attrs).get('id') == 'observation-json': self.selected = True
        def handle_endtag(self, tag):
            if tag == 'pre': self.selected = False
        def handle_data(self, data):
            if self.selected: self.parts.append(data)
    parsed=Observation(); parsed.feed(results['html']['stdout'].decode('ascii')); parsed.close()
    data=json.loads(results['json']['stdout'])
    assert json.loads(''.join(parsed.parts)) == data
    assert results['html']['exit_code'] == results['json']['exit_code']
    assert data['continuation']['task']['task_id'] == selected_task
    assert data['continuation']['recommendation'] == 'inspect_completed_evidence'
    assert not data['acceptance_verified'] and not data['execution_admitted']
    assert {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in observed_refs} == before
    (OUTPUT/'actual-consumer.json').write_text(json.dumps({
        'result':'PASS','task_id':selected_task,'source_records':before,
        'canonical_observation_sha256':hashlib.sha256(''.join(parsed.parts).encode('ascii')).hexdigest(),
        'html_sha256':hashlib.sha256(results['html']['stdout']).hexdigest(),
        'recorded_state':data['result'],'browser_render':'NOT_RUN','source_records_unchanged':True
    },indent=2)+'\n',encoding='utf-8',newline='\n')
