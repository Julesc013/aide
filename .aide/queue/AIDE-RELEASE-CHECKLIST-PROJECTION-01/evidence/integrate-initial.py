"""Reviewed nonforce integration of one qualified checklist correction."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, subprocess, time
from pathlib import Path
ROOT=Path.cwd()
sys.path.insert(0,str(ROOT))
from core.execution import managed_workspace as workspace
TASK=ROOT/".aide/queue/AIDE-RELEASE-CHECKLIST-PROJECTION-01"
EVIDENCE=TASK/"evidence"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    assert len(sys.argv)==3
    effect=EVIDENCE/"integration-effect.json"
    source=EVIDENCE/"closure-source.json"
    assert sha(effect)==sys.argv[1] and sha(source)==sys.argv[2]
    plan=json.loads(effect.read_bytes())
    mapped=json.loads(source.read_bytes())
    committed=json.loads((EVIDENCE/"closure-commit-result.log").read_bytes())
    commit=committed["commit"]
    assert committed["base"]==mapped["base"]==plan["source_commit"]
    receipt=EVIDENCE/"integration-result.log"
    with receipt.open("x",encoding="utf-8") as stream:
        stream.write("{}\n")
    record={"status":"RUNNING","commit":commit,"tree":committed["tree"],"operations":[]}
    deadline=time.monotonic()+240
    def save():
        receipt.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8",newline="\n")
    def run(label,args):
        assert time.monotonic()<deadline
        out=EVIDENCE/("integration-"+label+".stdout.log")
        err=EVIDENCE/("integration-"+label+".stderr.log")
        row={"label":label,"argv":args,"state":"started","exit_code":None}
        record["operations"].append(row);save()
        try:
            with out.open("xb") as stdout,err.open("xb") as stderr:
                result=subprocess.run(args,cwd=ROOT,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,
                                      timeout=min(120,max(1,deadline-time.monotonic())))
            row.update(state="completed",exit_code=result.returncode)
        except BaseException as error:
            row.update(state="exception",error_type=type(error).__name__,error=str(error));raise
        finally:
            row["streams"]={p.name:{"bytes":p.stat().st_size,"sha256":sha(p)} for p in (out,err) if p.exists()};save()
        assert result.returncode==0,label
        return out.read_text(encoding="utf-8").strip()
    def git(label,*args):
        return run(label,["git",*args])
    state={"dev":plan["base"],"main":plan["base"]}
    config,roots,_=workspace.load_config(ROOT/".aide.local/execution.json")
    assert workspace.digest(config)==plan["control_config_digest"]
    def evidence():
        attempt=json.loads((EVIDENCE/"attempt-01.json").read_bytes())
        assert attempt["phase"]=="retired" and attempt["result"]["exit_code"]==0 and attempt["result"]["quiescent"]
        assert attempt["scratch_absent"] and attempt["reservation_released"]
        assert not (roots["scratch"]/attempt["job_id"]).exists()
        for name,digest in attempt["collected_manifest"].items():
            assert workspace.content_digest(Path(attempt["retained"])/name)==digest
        qualified=json.loads((EVIDENCE/"attempt-01-qualified.json").read_bytes())
        for name,digest in qualified["pack_sha256s"].items():
            assert sha(ROOT/".aide/export/aide-lite-pack-v0"/name)==digest
        for name,digest in plan["release_postimages"].items():
            assert sha(ROOT/name)==digest
    def guards(label):
        assert workspace.dispatch_state(roots["control"])["mode"]=="running"
        assert not (roots["control"]/"active.json").exists()
        assert git(label+"-head","rev-parse","HEAD")==commit
        assert git(label+"-tree","rev-parse","HEAD^{tree}")==committed["tree"]
        assert not git(label+"-clean","status","--porcelain")
        for name,digest in mapped["files"].items():
            assert sha(ROOT/name)==digest,name
        assert sha(source)==sys.argv[2] and sha(effect)==sys.argv[1]
        for branch,value in state.items():
            assert git(label+"-"+branch,"rev-parse",branch)==value
        for ref,value in plan["preserved_local_refs"].items():
            assert git(label+"-keep-"+ref.split("/")[-1],"rev-parse",ref)==value
        assert workspace.inspect(ROOT/".aide.local/execution.json")["active"] is None
    def remote(label):
        lines=git(label,"ls-remote","--heads","--tags","origin").splitlines()
        refs={line.split()[1]:line.split()[0] for line in lines}
        for branch,value in state.items():
            assert refs["refs/heads/"+branch]==value
        for ref,value in plan["preserved_remote_refs"].items():
            assert refs[ref]==value,ref
        return refs
    try:
        with workspace.estate_lock(roots["control"]),workspace.estate_lock(roots["control"],"dispatch.lock"):
            guards("before")
            assert git("origin","remote","get-url","origin")==plan["remote_url"]
            assert sum(line.startswith("worktree ") for line in git("worktrees","worktree","list","--porcelain").splitlines())==1
            assert "ready_dry_run" in run("helper-plan",["py","-3","-B",".aide/scripts/aide_lite.py","git","plan"])
            remote("remote-before");evidence()
            for branch in ("dev","main"):
                assert git("tracking-"+branch,"rev-parse","origin/"+branch)==plan["base"]
            validation=run("validate",["py","-3","-B",".aide/scripts/aide_lite.py","validate"])
            assert validation.splitlines()[1]=="status: PASS"
            checked=run("commits",["py","-3","-B",".aide/scripts/aide_lite.py","commit","check","--range",plan["base"]+".."+commit])
            assert checked.splitlines()[1]=="result: PASS"
            for branch in ("dev","main"):
                guards("pre-"+branch);remote("remote-pre-"+branch)
                git("ancestor-"+branch,"merge-base","--is-ancestor",state[branch],commit)
                git("cas-"+branch,"update-ref","refs/heads/"+branch,commit,state[branch])
                state[branch]=commit
                git("push-"+branch,"push","origin",commit+":refs/heads/"+branch)
                remote("remote-post-"+branch)
            path=ROOT/".aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py"
            spec=importlib.util.spec_from_file_location("checklist_final_preview",path)
            preview=importlib.util.module_from_spec(spec);sys.modules[spec.name]=preview;spec.loader.exec_module(preview)
            preview.BASE=plan["base"]
            record["preview"]=preview.verify()
            assert record["preview"]["source_head"]==plan["source_commit"]
            evidence();guards("pre-retirement")
            assert git("own-ref","rev-parse",plan["task_branch"])==commit
            git("own-ancestor","merge-base","--is-ancestor",plan["task_branch"],"dev")
            git("switch-dev","switch","dev")
            git("retire-own-local","branch","-d",plan["task_branch"])
            assert not git("final-clean","status","--porcelain")
            for ref in ("dev","main","origin/dev","origin/main"):
                assert git("final-"+ref.replace("/","-"),"rev-parse",ref)==commit
            record.update(status="PASS",local_task_retired=True,remote_task_created=False,new_jobs=0,
                          frozen_local_release_assets_unchanged=True,published_asset_mutations=0,dev=commit,main=commit)
            save()
    except BaseException as error:
        record.update(status="STOPPED_RECONCILE",error_type=type(error).__name__,error=str(error));save();raise
    print(json.dumps({k:v for k,v in record.items() if k not in ("operations","preview")}))

if __name__=="__main__":
    main()
