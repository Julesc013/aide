"""Verify actual campaign views and preserved records; generate existing preview only."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, re, subprocess
from pathlib import Path
ROOT = Path.cwd()
TASK = ROOT / ".aide/queue/AIDE-CAMPAIGN-CURRENT-STATE-01"
PARENT = ROOT / ".aide/queue/AIDE-CONVERGENCE-AND-DELIVERY-01"
BASE = "29f4bf5c1f23a923b0ea97e1826ab9fff4c734fc"
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    spec.loader.exec_module(module); return module
def git(*args): return subprocess.check_output(["git", *args], text=True, encoding="utf-8").strip()
owner = load("campaign_preview", ROOT / ".aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py")
owner.BASE = BASE

def check_records():
    claims = json.loads((TASK / "evidence/claim-sources.json").read_text(encoding="utf-8"))
    for name, value in claims["sources"].items(): assert sha(ROOT / name) == value, name
    for name in ("task.yaml", "status.yaml"):
        original = subprocess.check_output(["git", "show", BASE + ":" + (PARENT / name).relative_to(ROOT).as_posix()])
        assert (TASK / "evidence" / ("prior-" + name)).read_bytes() == original, name
        if name == "task.yaml":
            expected = original.replace(b"planning_state: source_documentation_aligned_bulk_qualification_held",
                b"planning_state: scoped_daily_use_foundations_qualified_full_workflow_incomplete").replace(
                b"updated_at: 2026-09-21", b"updated_at: 2026-10-18")
            assert (PARENT / name).read_bytes() == expected
    old_plan = subprocess.check_output(["git", "show", BASE + ":" + (PARENT / "ExecPlan.md").relative_to(ROOT).as_posix()])
    assert hashlib.sha256(old_plan).hexdigest() == claims["prior_plan_sha256"]
    assert (PARENT / "ExecPlan.md").read_bytes() == claims["plan_prefix"].encode() + old_plan
    publication = claims["publication"]
    old = subprocess.check_output(["git", "show", publication["commit"] + ":" + publication["path"]])
    assert old == (ROOT / publication["local_snapshot"]).read_bytes()
    assert hashlib.sha256(old).hexdigest() == publication["sha256"]
    assert not (ROOT / publication["path"]).exists()
    assert "github_cli_interactive_authentication" in old.decode()
    git("merge-base", "--is-ancestor", "dfae9356241dda6a03e2cc48cf9acb245c9a6be1", "HEAD")
    inventory = json.loads((TASK / "evidence/immutable-inventory.json").read_text(encoding="utf-8"))
    for group in inventory.values():
        for name, value in group.items(): assert sha(ROOT / name) == value, name
    pack = ROOT / ".aide/export/aide-lite-pack-v0"
    assert {p.relative_to(ROOT).as_posix() for p in pack.rglob("*") if p.is_file()} == set(inventory["pack"])
    links = re.findall(r"\]\(([^)]+)\)", (PARENT / "CURRENT.md").read_text(encoding="utf-8"))
    for link in links:
        path = (PARENT / link).resolve()
        assert path.is_relative_to(ROOT) and path.is_file(), link
    return {"pinned_claim_sources": len(claims["sources"]), "valid_links": len(links),
            "pack_files_unchanged": len(inventory["pack"]), "release_files_unchanged": len(inventory["release"]),
            "historical_records": "original task/status bytes and complete ExecPlan body preserved",
            "publication": "frozen branch snapshot only; authentication not re-probed"}

def run(label, args, output):
    path = output / (label + ".log")
    with path.open("xb") as stream:
        result = subprocess.run([sys.executable, "-B", ".aide/scripts/aide_lite.py", *args],
                                stdin=subprocess.DEVNULL, stdout=stream, stderr=subprocess.STDOUT, timeout=120)
    assert result.returncode == 0, label
    return path.read_text(encoding="utf-8")

def main():
    assert sys.argv[1:] in (["generate"], ["verify"])
    evidence = check_records()
    if sys.argv[1:] == ["verify"]:
        print(json.dumps({"status": "PASS", **evidence, "preview": owner.verify()}, indent=2))
        return
    assert not git("status", "--porcelain")
    output = Path(os.environ["AIDE_JOB_OUTPUT"])
    current = json.loads(run("current-json", ["task", "current", "--task-id", PARENT.name, "--json"], output))
    assert current["task_id"] == PARENT.name and current["status"] == "running" and current["result"] == "PENDING"
    assert current["owner"] and current["next_action"] and len(current["remaining_obligations"]) == 6
    assert current["declared_status"] == current["index_status"] == current["status"]
    assert not current["issues"] and len(current["evidence"]) == 11
    assert all(x["availability"] == "present" and x["applicability"] == "unverified" for x in current["evidence"])
    assert sum(x.get("digest_verified") is True for x in current["evidence"]) == 3
    assert current["read_only"] is True and current["acceptance_verified"] is False
    human = run("current-human", ["task", "current", "--task-id", PARENT.name], output)
    assert PARENT.name in human and current["next_action"] in human and current["owner"] in human
    resume = json.loads(run("resume-json", ["task", "resume-plan", "--task-id", PARENT.name, "--json"], output))
    assert resume["task"] == current and resume["recommendation"] == "reconcile_attempt"
    assert resume["safe_to_resume"] is None and resume["execution_admitted"] is False and resume["read_only"] is True
    for label, args in [("doctor", ["doctor"]), ("validation", ["validate"]), ("pack-status", ["pack-status"])]:
        run(label, args, output)
    assert not git("status", "--porcelain")
    assert check_records() == evidence
    sys.argv = [str(TASK / "run_checks.py"), "generate"]
    owner.main()
    assert check_records() == evidence
    result = {"result": "PASS", **evidence, "current_references": len(current["evidence"]),
              "current_issues": current["issues"], "remaining_obligations": current["remaining_obligations"],
              "owner": current["owner"], "next_action": current["next_action"],
              "source_commit": git("rev-parse", "HEAD"), "models_requested": 0,
              "whole_task_usage": "unknown", "product_tests_reused_unchanged": True,
              "qualification_scope": "Actual current/resume CLI, preserved records, doctor/full structural validation, unchanged pack/release and fixed preview"}
    (output / "qualification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
if __name__ == "__main__": main()

