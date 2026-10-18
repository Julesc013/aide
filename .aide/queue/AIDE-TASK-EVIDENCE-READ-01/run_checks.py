"""Qualify bounded evidence reads and preserve all 162 affected assertions."""
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
for name in ['test_task_current', 'test_task_handoff', 'test_task_binding', 'test_task_brief_symbols', 'test_task_brief', 'test_task_brief_view', 'test_quality_symbols']:
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
expected_count = 168
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
    import subprocess, tempfile
    from html.parser import HTMLParser
    TASK = ROOT / '.aide/queue/AIDE-TASK-EVIDENCE-READ-01'
    selected_task = 'AIDE-TASK-BRIEF-BROWSER-01'
    selected_path = '.aide/scripts/aide_lite.py'
    refs = ['.aide/controller/outcome-ledger.jsonl', '.aide/reports/file-quality-ledger.json',
            '.aide/queue/' + selected_task + '/task.yaml',
            '.aide/queue/' + selected_task + '/status.yaml', '.aide/queue/index.yaml',
            selected_path]
    refs += ['.aide/queue/' + selected_task + '/evidence/' + name for name in
             ['source-attempt-01.json', 'preview-attempt-02.json', 'visual-review.json']]
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    before = {p:sha(ROOT/p) for p in refs}
    def invoke(label, command):
        out, err = OUTPUT/(label+'.stdout'), OUTPUT/(label+'.stderr')
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
    with tempfile.TemporaryDirectory(prefix='evidence-small-') as directory:
        fixture=Path(directory); task_dir=fixture/'.aide/queue/PROJECT-WORK-01'; task_dir.mkdir(parents=True)
        (task_dir/'task.yaml').write_text('id: PROJECT-WORK-01\ntitle: Preserve small evidence\n',encoding='utf-8')
        (task_dir/'status.yaml').write_text('status: passed\nresult: FIXTURE\nfinal_ref: result.txt\n',encoding='utf-8')
        (task_dir/'result.txt').write_bytes(b'small evidence\n')
        fixture_before={p.relative_to(fixture).as_posix():sha(p) for p in fixture.rglob('*') if p.is_file()}
        small={}
        for mode,flags in [('text',[]),('json',['--json'])]:
            args=['--repo-root',str(fixture),'task','current','--task-id','PROJECT-WORK-01',*flags]
            old=invoke('small-old-'+mode,[sys.executable,'-I',str(original),*args])
            new=invoke('small-new-'+mode,[sys.executable,'-I',str(current),*args])
            assert old==new
            small[mode]={'byte_identical':True,'sha256':hashlib.sha256(new[1]).hexdigest()}
        assert fixture_before=={p.relative_to(fixture).as_posix():sha(p) for p in fixture.rglob('*') if p.is_file()}
    args=['--repo-root',str(ROOT),'task','current','--task-id',selected_task,'--json']
    old=json.loads(invoke('actual-old-current',[sys.executable,'-I',str(original),*args])[1])
    new=json.loads(invoke('actual-current',[sys.executable,'-I',str(current),*args])[1])
    for key in old:
        if key!='evidence': assert old[key]==new[key],key
    old_refs={r['field']:r for r in old['evidence']}; new_refs={r['field']:r for r in new['evidence']}
    assert old_refs.keys()==new_refs.keys()
    for name in ['source_ref','preview_ref']:
        assert old_refs[name]['availability']=='record_too_large' and old_refs[name]['path'] is None
        assert new_refs[name]['availability']=='present'
        assert new_refs[name]['path']=='.aide/queue/'+selected_task+'/evidence/'+(
            'source-attempt-01.json' if name=='source_ref' else 'preview-attempt-02.json')
        assert new_refs[name]['applicability']=='unverified'
    assert old_refs['visual_ref']==new_refs['visual_ref']
    assert new['result']=='OBSERVED_VIEWPORTS_PASS' and not new['acceptance_verified']
    args=['--repo-root',str(ROOT),'task','resume-plan','--task-id',selected_task,'--json']
    resumed=json.loads(invoke('actual-resume',[sys.executable,'-I',str(current),*args])[1])
    assert resumed['recommendation']=='inspect_completed_evidence'
    assert not resumed['execution_admitted'] and resumed['safe_to_resume'] is None
    outputs={}
    args=['--repo-root',str(ROOT),'task','brief','--task-id',selected_task,'--path',selected_path]
    for mode in ['json','html']:
        outputs[mode]=invoke('actual-brief-'+mode,[sys.executable,'-I',str(current),*args,'--'+mode])
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
    assert data['continuation']==resumed
    assert not data['execution_admitted'] and not data['acceptance_verified']
    assert all(sha(ROOT/p)==h for p,h in before.items())
    canonical=json.dumps(data,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode('ascii')
    record={'result':'PASS','task_id':selected_task,'source_records':before,
            'canonical_observation_sha256':hashlib.sha256(canonical).hexdigest(),
            'small_predecessor_comparison':small,'source_records_unchanged':True,
            'prior_failure_reproduced':True,'large_evidence_present':True,
            'recommendation':resumed['recommendation'],'browser_render':'NOT_RUN'}
    (OUTPUT/'actual-consumer.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'result':'PASS','actual_task':selected_task,'large_evidence_present':True}))
