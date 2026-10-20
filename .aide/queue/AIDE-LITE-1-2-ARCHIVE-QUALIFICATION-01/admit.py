"""One exact reviewed branch-only admission; no implementation or job effects."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace

TASK = Path(__file__).parent
EVIDENCE = TASK / "evidence"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, timeout=30).strip()


def main():
    source, effect = (EVIDENCE / name for name in ("admission-source.json", "admission-effect.json"))
    assert len(sys.argv) == 3 and [sha(source), sha(effect)] == sys.argv[1:]
    mapped, plan = (json.loads(p.read_bytes()) for p in (source, effect))
    assert mapped["effect_sha256"] == sha(effect)
    review = EVIDENCE / "admission-review.json"
    verdict = json.loads(review.read_bytes())
    assert verdict["decision"] == "ACCEPT" and not verdict["required_fixes"]
    assert verdict["reviewer"] == "/root/review_disked_continuation"
    assert [verdict["source_sha256"], verdict["effect_sha256"], verdict["controller_sha256"]] == [sha(source), sha(effect), sha(Path(__file__))]
    allowed = set(mapped["files"]) | {p.relative_to(ROOT).as_posix() for p in (source, review)}
    path = EVIDENCE / "admission-execution.log"
    with path.open("x", encoding="utf-8") as stream:
        stream.write("{}\n")
    record = {"state": "started"}

    def save():
        path.write_bytes((json.dumps(record, indent=2) + "\n").encode())

    config, roots, _ = workspace.load_config(ROOT / ".aide.local/execution.json")
    assert workspace.digest(config) == plan["control_config_digest"]
    try:
        with workspace.estate_lock(roots["control"]), workspace.estate_lock(roots["control"], "dispatch.lock"):
            assert workspace.dispatch_state(roots["control"])["mode"] == "running"
            assert not (roots["control"] / "active.json").exists()
            assert git("branch", "--show-current") == "main"
            for ref in ("HEAD", "main", "dev", "origin/main", "origin/dev"):
                assert git("rev-parse", ref) == plan["base"]
            assert git("show-ref").splitlines() == plan["preserved_refs"]
            assert not git("diff", "--cached", "--name-only")
            changed = set(git("diff", "--name-only").splitlines()) | set(git("ls-files", "--others", "--exclude-standard").splitlines())
            assert changed == allowed, sorted(changed ^ allowed)
            assert all(sha(ROOT / name) == value for name, value in mapped["files"].items())
            baseline = json.loads((EVIDENCE / "baseline.json").read_bytes())
            assert all(sha(ROOT / name) == value for name, value in baseline["stable_assets"].items())
            for flags in (("--all",), ("--push", "--all")):
                assert git("remote", "get-url", *flags, "origin") == plan["origin_url"]
            remote = dict(line.split()[::-1] for line in git("ls-remote", "--heads", "origin", "main", "dev").splitlines())
            assert remote == {"refs/heads/main": plan["base"], "refs/heads/dev": plan["base"]}
            assert not git("branch", "--list", plan["task_branch"])
            assert not git("ls-remote", "--heads", "origin", plan["task_branch"])
            spec = importlib.util.spec_from_file_location("release_admission_lite", ROOT / ".aide/scripts/aide_lite.py")
            lite = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = lite
            spec.loader.exec_module(lite)
            helper = lite.make_git_helper_plan(ROOT, "plan", dry_run=True)
            record["helper_plan"] = helper
            save()
            assert helper["status"] == "blocked" and helper["blockers"] == ["dirty_tree_requires_classification"]
            git("diff", "--check")
            git("switch", "--no-track", "-c", plan["task_branch"], "main")
            assert git("branch", "--show-current") == plan["task_branch"] and git("rev-parse", "HEAD") == plan["base"]
            actual = git("show-ref").splitlines()
            assert actual == sorted(plan["preserved_refs"] + [plan["base"] + " refs/heads/" + plan["task_branch"]], key=lambda line: line.split()[1])
            record.update(state="admitted_branch_created", task_branch=plan["task_branch"], base=plan["base"], implementation_or_job_executed=False)
            save()
        print(json.dumps({k: v for k, v in record.items() if k != "helper_plan"}))
    except BaseException as error:
        record.update(state="stopped_reconcile_before_retry", error_type=type(error).__name__, error=str(error))
        save()
        raise


if __name__ == "__main__":
    main()
