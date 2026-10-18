"""Real fresh-process continuity, preserved legacy behavior and unchanged artifacts."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib, json, os, subprocess, tempfile, types, unittest
from pathlib import Path
ROOT=Path.cwd(); TASK=ROOT/".aide/queue/AIDE-DEPENDENCY-REBIND-01"
OUTPUT=Path(os.environ["AIDE_JOB_OUTPUT"]); SCRATCH=Path(os.environ["AIDE_JOB_TMP"])
assert Path(tempfile.gettempdir())==SCRATCH and SCRATCH.parent==OUTPUT.parent
sys.path.insert(0,str(ROOT/".aide/scripts/tests"))
tests=importlib.import_module("test_continuous_worker_request_rebinding")
cancellation=importlib.import_module("test_continuous_worker_request_cancellation")
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(tests.RebindingWorkflowTests),
                         unittest.defaultTestLoader.loadTestsFromTestCase(cancellation.CancellationWorkflowTests)])
assert suite.countTestCases()==2
with (OUTPUT/"workflow-tests.log").open("x",encoding="utf-8") as stream:
 result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
record={"tests_run":result.testsRun,"failures":len(result.failures),"errors":len(result.errors),
        "skips":[(t.id(),why) for t,why in result.skipped]}
(OUTPUT/"workflow-tests.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
assert result.wasSuccessful() and result.testsRun==2 and not result.skipped
from core.runtime.continuous_worker.state import State,Refused,digest
from core.runtime.continuous_worker.requests import Requests
from test_continuous_worker_requests import configuration,ref
base="ceac70a6fefefde93d2fb7435e8825c173302757"
raw=subprocess.check_output(["git","show",base+":core/runtime/continuous_worker/requests.py"],timeout=15)
expected=json.loads((TASK/"evidence/workflow-qualification-inputs.json").read_text())
assert hashlib.sha256(raw).hexdigest()==expected["old_reader_sha256"]
legacy=types.ModuleType("core.runtime.continuous_worker.legacy_requests")
legacy.__package__="core.runtime.continuous_worker"
exec(compile(raw,base+":requests.py","exec"),legacy.__dict__)
for schema in ("aide.dependency-configuration.v1","aide.dependency-configuration.v2"):
 with tempfile.TemporaryDirectory(prefix="rebind-legacy-") as directory:
  root=Path(directory).resolve(); config=configuration(root)|{"schema":schema}
  state=State(root)
  try:
   Requests.initialize(state,config)
   old=legacy.Requests(state,digest(config))
   state.control("pause-dispatch")
   current=Requests(state,digest(config))
   proposal={"configuration":config|{"expires_at":config["expires_at"]+1000},
             "decision":ref("owner-renewal"),"evidence":[ref("native-inspection")]}
   plan=current.reconfiguration_plan(proposal); receipt=current.reconfigure(plan)
   before=list(state.db.iterdump())
   recovered=Requests(state,digest(plan["configuration"]))
   assert recovered.reconfigure(plan)==receipt
   assert list(state.db.iterdump())==before
   try:legacy.Requests(state,digest(config))
   except Refused:pass
   else:raise AssertionError("old reader accepted obsolete configuration")
   compatible=legacy.Requests(state,digest(plan["configuration"]))
   state.control("resume")
   try:old.guard()
   except Refused:pass
   else:raise AssertionError("cached old writer passed after resume")
   compatible.guard()
  finally:state.close()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pack=ROOT/".aide/export/aide-lite-pack-v0"
actual={p.relative_to(pack).as_posix():sha(p) for p in pack.rglob("*") if p.is_file()}
assert actual==expected["pack"] and len(actual)==870
for p,h in expected["releases"].items():assert sha(ROOT/p)==h,p
record.update(result="PASS",legacy_schemas_preserved=2,old_reader_sha256=expected["old_reader_sha256"],
              pack_files_unchanged=len(actual),release_files_unchanged=len(expected["releases"]),
              live_reconfigurations=0,models_requested=0,native_ownership_transferred=False)
(OUTPUT/"workflow-result.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
print(json.dumps(record))
