"""One admitted live turn via existing pinned owner; no alternate supervisor."""
import importlib.util,json,sys
from pathlib import Path
REPO=Path(__file__).resolve().parents[3]
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location("aide_canary_scope",REPO/"core/execution/scoped_host.py")
scoped=importlib.util.module_from_spec(spec);spec.loader.exec_module(scoped)
config=REPO/".aide.local/efficiency-live-host-permission.json"
job=json.loads((REPO/".aide.local/efficiency-live-host-job.json").read_text(encoding="utf-8"))
owner,admission_host=scoped.prepare(config,REPO)
# codex_exec configures its own read-only tool sandbox and existing ChatGPT auth.
# The Python-only scoped.run path is deliberately not used for a model turn.
result=owner.run(config,job,host=owner.WindowsJobHost(),probe=admission_host.admission_probe)
print(json.dumps({k:result.get(k) for k in ("job_id","manifest_digest","result","scratch_absent","reservation_released","peaks")},sort_keys=True))
sys.exit(0 if result.get("result",{}).get("exit_code")==0 and result.get("scratch_absent") and result.get("reservation_released") else 1)
