import copy,hashlib,io,json,sys,unittest
from pathlib import Path
from unittest import mock
R=Path(r"D:\Projects\AIDE\aide");E=R/".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=E/"h2-resource-source-manifest.json";assert sha(manifest)=="84d5621e634989b7bf2ad62ed3472c6989b2d9b4a9b44acfd1e465319991a1a6"
m=json.loads(manifest.read_bytes())
for path,digest in dict(m["files"],**m["unchanged_dependencies"]).items():assert sha(R/path)==digest,path
sys.path[:0]=[str(E),str(R),str(R/".aide/scripts/tests")]
import h2_system_resource_tests as t
import h2_system_input_tests as n
import test_continuous_worker_system_observation as o
r,c=t.r,t.c
class Independent(unittest.TestCase):
 def make(self):
  self.clock=n.Clock();self.api=t.FakeResource();self.transfer=r.Transfer.read(t.transfer_value())
  self.probe=r.ResourceProbe(self.transfer,self.api,r.Deadline(self.transfer.plan.expires_at,clock=self.clock.tick,wall=self.clock.utc),clock=self.clock.tick,wall=self.clock.utc)
 def test_second_mapping_expiry_releases_both_exact_handles(self):
  self.make()
  def hook(stage):
   if stage=="map" and len(self.api.maps)==2:self.clock.wall=1100.0
  self.api.resource_hook=hook
  with self.assertRaises(r.Refused):self.probe.run()
  self.assertEqual(self.api.maps,list(r.API_NAMES));self.assertEqual(self.api.frees,[0x10002,0x20002]);self.assertEqual(sorted(self.api.closed),sorted(self.api.opened))
  with self.assertRaises(r.Refused):self.probe.run()
  self.assertEqual(len(self.api.maps),2)
 def test_each_uncertain_file_close_still_attempts_all_releases(self):
  for target in range(10,19):
   with self.subTest(target=target):
    self.make();original=self.api.close_file
    def close(handle):
     original(handle)
     return False if handle==target else True
    self.api.close_file=close
    with self.assertRaises(r.Refused):self.probe.run()
    self.assertEqual(sorted(self.api.closed),list(range(10,19)));self.assertEqual(self.api.frees,[0x10002,0x20002])
    self.assertEqual(len(self.probe.session.release_failures),1)
 def test_environment_integer_aliases_refuse_before_mapping(self):
  for key,value in (("process_machine",False),("native_machine",float(0x8664))):
   self.make();original=self.api.environment;self.api.environment=lambda:dict(original(),**{key:value})
   with self.assertRaises(r.Refused):self.probe.run()
   self.assertEqual(self.api.maps,[]);self.assertEqual(self.api.opened,[])
 def test_false_last_durable_ack_prevents_dispatch(self):
  clock=n.Clock();api=t.FakeParent();controller=c.Controller(t.effect(),api,clock=clock.tick,wall=clock.utc);original=api.append
  def append(stream,row):
   result=original(stream,row)
   return "f"*64 if row.get("sequence")==1 else result
  api.append=append
  with self.assertRaises(r.Refused):controller.run()
  self.assertEqual(api.dispatched,0);self.assertEqual(len(api.rows),3)
  with self.assertRaises(r.Refused):controller.run()
 def test_final_parent_release_expiry_blocks_controller_success(self):
  for kind in ("expiry","backward","nan"):
   clock=n.Clock();api=t.FakeParent();controller=c.Controller(t.effect(),api,clock=clock.tick,wall=clock.utc)
   def hook(stage):
    if stage=="parent_close":
     if kind=="expiry":clock.wall=1100.0
     elif kind=="backward":clock.mono=0.0
     else:clock.mono=float("nan")
   api.hook=hook
   with self.assertRaises(r.Refused):controller.run()
   self.assertEqual(api.dispatched,1)
   self.assertEqual(api.rows[-1]["final_controller_status"],"pending_final_guard")
 def test_boolean_host_exit_is_not_success(self):
  clock=n.Clock();api=t.FakeParent();controller=c.Controller(t.effect(),api,clock=clock.tick,wall=clock.utc);original=api.run_child
  def run(*args,**kwargs):return dict(original(*args,**kwargs),exit_code=False)
  api.run_child=run
  with self.assertRaises(r.Refused):controller.run()
  self.assertEqual(len(api.rows),3)
 def test_boolean_observation_fields_do_not_alias_counts(self):
  self.make();valid=r.decode(self.probe.run())
  for key,value in (("native_calls",True),("mapping_attempts",2.0),("all_owned_handles_released",1),("system_ownership_qualified",0),("loader_qualified",0)):
   bad=copy.deepcopy(valid);bad["observation"][key]=value
   with self.assertRaises(r.Refused):r.validate_result(r._canonical(bad),self.transfer)
suite=unittest.TestSuite()
for module in (t,n,o):suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Independent))
log=E/"h2-resource-root-tests.log";assert not log.exists()
with mock.patch.object(r.NativeResourceApi,"__init__",side_effect=AssertionError("native effect forbidden")),mock.patch.object(n.read.ReadOnlyApi,"__init__",side_effect=AssertionError("native read forbidden")),mock.patch.object(r.obs.NativeSystemApi,"__init__",side_effect=AssertionError("native observer forbidden")):
 with log.open("x",encoding="utf-8",newline="\n") as out:result=unittest.TextTestRunner(stream=out,verbosity=2).run(suite)
for path,digest in dict(m["files"],**m["unchanged_dependencies"]).items():assert sha(R/path)==digest,path
record={"schema":"aide.host.resource-root-source-review.v1","result":"PASS" if result.wasSuccessful() else "FAIL_RETAINED","source_manifest_sha256":sha(manifest),"source_aggregate":m["aggregate"],"tests_run":result.testsRun,"independent_test_methods":7,"test_log_sha256":sha(log),"actual_native_constructors_forbidden":True,"source_dependencies_unchanged":True,"review_scope":"Read all three sources plus inherited parent guards and observer mapping/release checks. Added second-mapping expiry, all nine uncertain closes, environment integer aliases, false final durable acknowledgement, final controller release clock faults, boolean host status and observation aliases.","native_effect_executed":False,"effect_manifest_admitted":False,"limitations":"Trusted finite ordinary probe premises remain; full API inventory/cap, private loader and operational host qualification remain open."}
dest=E/"h2-resource-root-source-review.json";assert not dest.exists();dest.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps(record));assert result.wasSuccessful()
