"""Two separately admitted existing-owner jobs; one serial observation owner."""
import importlib.util,json,sys
from pathlib import Path
REPO=Path(__file__).resolve().parents[3]
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location("aide_matched_scope",REPO/"core/execution/scoped_host.py")
scoped=importlib.util.module_from_spec(spec);spec.loader.exec_module(scoped)
config=REPO/".aide.local/efficiency-live-host-permission.json"
# Fresh entry process required for each profile's immutable ZIP package binding.
profile=sys.argv[1]
if profile not in ("baseline","compact"): raise ValueError("unadmitted profile")
job=json.loads((REPO/(".aide.local/efficiency-live-host-"+profile+"-job.json")).read_text(encoding="utf-8"))
owner,admission=scoped.prepare(config,REPO)
result=owner.run(config,job,host=owner.WindowsJobHost(),probe=admission.admission_probe)
print(json.dumps({k:result.get(k) for k in ("job_id","manifest_digest","result","scratch_absent","reservation_released","peaks")},sort_keys=True))
sys.exit(0 if result.get("result",{}).get("exit_code")==0 and result.get("scratch_absent") and result.get("reservation_released") else 1)
