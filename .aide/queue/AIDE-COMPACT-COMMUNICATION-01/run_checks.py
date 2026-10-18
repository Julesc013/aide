import sys
sys.dont_write_bytecode = True
import hashlib,importlib.util,json,os,unittest
from pathlib import Path
ROOT=Path.cwd()
SUBJECT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT
OUTPUT=Path(os.environ['AIDE_JOB_OUTPUT'])
names=['test_compact_communication', 'test_q27_commit_recovery', 'test_q34_changelog_release', 'test_managed_commit_create']
if SUBJECT != ROOT: names.remove('test_managed_commit_create')
counts={'test_compact_communication': 26, 'test_q27_commit_recovery': 33, 'test_q34_changelog_release': 12, 'test_managed_commit_create': 49}
suite=unittest.TestSuite(); inputs={}
for name in names:
 p=SUBJECT/'.aide/scripts/tests'/(name+'.py')
 spec=importlib.util.spec_from_file_location('communication_'+name,p)
 module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
 suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
 inputs[p.relative_to(SUBJECT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
def ids(tests):
 for item in tests:
  if isinstance(item,unittest.TestSuite):yield from ids(item)
  else:yield item.id()
expected=list(ids(suite)); assert len(expected)==sum(counts[n] for n in names)
label='source' if SUBJECT==ROOT else 'delivered'
with (OUTPUT/(label+'-tests.log')).open('w',encoding='utf-8') as log:
 result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
record={'test_ids':expected,'tests_run':result.testsRun,'failures':len(result.failures),
 'errors':len(result.errors),'skips':[(t.id(),r) for t,r in result.skipped],
 'inputs':inputs,'cli_sha256':hashlib.sha256((SUBJECT/'.aide/scripts/aide_lite.py').read_bytes()).hexdigest(),
 'models_requested':0,'whole_outcome_usage':'unknown'}
(OUTPUT/(label+'-tests.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
assert result.wasSuccessful() and result.testsRun==len(expected) and not result.skipped
assert all(hashlib.sha256((SUBJECT/p).read_bytes()).hexdigest()==h for p,h in inputs.items())
print(json.dumps({'result':'PASS','tests':result.testsRun,'subject':label}))
