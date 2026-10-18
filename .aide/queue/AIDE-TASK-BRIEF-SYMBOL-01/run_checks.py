"""Qualify optional fresh helper evidence and retain all 59 directly affected assertions."""
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
for name in ['test_task_brief_symbols', 'test_task_brief', 'test_task_brief_view', 'test_quality_symbols']:
    path = SUBJECT / '.aide/scripts/tests' / (name + '.py')
    spec = importlib.util.spec_from_file_location('validation_' + name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    assert Path(getattr(module, 'aide', getattr(module, 'aide_lite', None)).__file__).resolve() == SUBJECT / '.aide/scripts/aide_lite.py'
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    inputs[path.relative_to(SUBJECT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
for relative in ['.aide/scripts/aide_lite.py', '.aide/scripts/outcome_lessons.py', '.aide/scripts/task_brief_view.py', '.aide/scripts/quality_symbols.py']:
    inputs[relative] = hashlib.sha256((SUBJECT / relative).read_bytes()).hexdigest()
def ids(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from ids(test)
        else:
            yield test.id()
expected = list(ids(suite))
expected_count = 77
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
    task = ROOT / '.aide/queue/AIDE-TASK-BRIEF-SYMBOL-01'
    selected_task = 'AIDE-TASK-BRIEF-VIEW-01'
    selected_path = '.aide/scripts/aide_lite.py'
    related_path = '.aide/scripts/tests/test_task_brief.py'
    refs = ['.aide/controller/outcome-ledger.jsonl', '.aide/reports/file-quality-ledger.json',
            '.aide/queue/' + selected_task + '/task.yaml',
            '.aide/queue/' + selected_task + '/status.yaml', '.aide/queue/index.yaml',
            selected_path, related_path]
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    before = {p:sha(ROOT/p) for p in refs}
    def invoke(label, command):
        out = OUTPUT/(label+'.stdout'); err = OUTPUT/(label+'.stderr')
        receipt = OUTPUT/(label+'.invocation.json')
        record = {'command':command, 'cwd':str(ROOT), 'state':'started', 'exit_code':None}
        def save():
            receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
        save()
        try:
            with out.open('xb') as stdout, err.open('xb') as stderr:
                result = subprocess.run(command,cwd=ROOT,stdin=subprocess.DEVNULL,
                                        stdout=stdout,stderr=stderr,timeout=30)
            record.update(state='completed',exit_code=result.returncode)
        except (OSError,subprocess.SubprocessError) as error:
            record.update(state='exception',error_type=type(error).__name__,error=str(error))
            raise
        finally:
            record['streams']={p.name:{'bytes':p.stat().st_size,'sha256':sha(p)}
                               for p in (out,err) if p.exists()}
            save()
        assert result.returncode in (0,2) and not err.read_bytes(),label
        return result.returncode,out.read_bytes()
    original = ROOT / '.aide/export/aide-lite-pack-v0/files/.aide/scripts/aide_lite.py'
    current = ROOT / selected_path
    args = ['--repo-root',str(ROOT),'task','brief','--task-id',selected_task,'--path',selected_path]
    default = {}
    for mode,flag in [('text',[]),('json',['--json']),('html',['--html'])]:
        old = invoke('baseline-default-'+mode,[sys.executable,'-I',str(original),*args,*flag])
        new = invoke('source-default-'+mode,[sys.executable,'-I',str(current),*args,*flag])
        assert old == new,mode+' default changed'
        default[mode]={'exit_code':new[0],'sha256':hashlib.sha256(new[1]).hexdigest(),'byte_identical':True}
    selections = ['--symbol','build_task_development_brief','--related-path',related_path]
    outputs={}
    for mode in ['json','html']:
        outputs[mode]=invoke('actual-symbol-'+mode,[sys.executable,'-I',str(current),*args,*selections,'--'+mode])
    class Page(HTMLParser):
        def __init__(self,text):
            super().__init__(convert_charrefs=True);self.selected=False;self.parts=[]
            self.feed(text);self.close()
        def handle_starttag(self,tag,attrs):
            if tag=='pre' and dict(attrs).get('id')=='observation-json':self.selected=True
        def handle_endtag(self,tag):
            if tag=='pre':self.selected=False
        def handle_data(self,text):
            if self.selected:self.parts.append(text)
    data=json.loads(outputs['json'][1]);page=Page(outputs['html'][1].decode('ascii'))
    assert json.loads(''.join(page.parts))==data and outputs['html'][0]==outputs['json'][0]
    assert data['continuation']['task']['task_id']==selected_task
    assert not data['execution_admitted'] and not data['acceptance_verified']
    primary,consumer=data['symbol_inspection']['files']
    assert [p['path'] for p in data['symbol_selection']]==[selected_path,related_path]
    definitions=primary['syntax']['definitions']['items']
    expected_line=next(n for n,line in enumerate(current.read_text(encoding='utf-8').splitlines(),1)
                       if line.startswith('def build_task_development_brief('))
    assert any(x['line']==expected_line and x['qualified_name']=='build_task_development_brief' for x in definitions)
    assert any(x['line']==64 and x['scope']=='TaskBriefTests.view' and x['resolution']=='unresolved'
               for x in consumer['syntax']['calls']['items'])
    assert all(sha(ROOT/p)==h for p,h in before.items())
    canonical=json.dumps(data,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode('ascii')
    record={'result':'PASS','task_id':selected_task,'source_records':before,
            'canonical_observation_sha256':hashlib.sha256(canonical).hexdigest(),
            'default_predecessor_comparison':default,'source_records_unchanged':True,
            'actual_definition_and_consumer':True,'browser_render':'NOT_RUN'}
    (OUTPUT/'actual-consumer.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'result':'PASS','actual_task':selected_task,'default_formats_byte_identical':True}))
