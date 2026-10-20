"""Checkpoint an exact reviewed payload/evidence diff; reuse bounded hosted observation."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.apply.managed_commit import create_commit
from core.execution import managed_workspace as workspace

TASK = Path(__file__).parent
EVIDENCE = TASK / "evidence"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, timeout=30).strip()


def main():
    source = EVIDENCE / "source-03.json"
    effect = EVIDENCE / "source-effect-03.json"
    assert len(sys.argv) == 3 and [sha(source), sha(effect)] == sys.argv[1:]
    mapped, plan = (json.loads(p.read_bytes()) for p in (source, effect))
    assert mapped["effect_sha256"] == sha(effect)
    verdict_path = EVIDENCE / "source-review-03.json"
    verdict = json.loads(verdict_path.read_bytes())
    assert verdict["decision"] == "ACCEPT" and not verdict["required_fixes"]
    assert verdict["reviewer"] == "/root/review_disked_continuation"
    assert [verdict["source_sha256"], verdict["effect_sha256"], verdict["controller_sha256"]] == [sha(source), sha(effect), sha(Path(__file__))]
    allowed = set(mapped["files"]) | {p.relative_to(ROOT).as_posix() for p in (source, verdict_path)}
    path = EVIDENCE / "source-execution-03.log"
    with path.open("x", encoding="utf-8") as stream:
        stream.write("{}\n")
    outcome = {"state": "started", "source_sha256": sha(source), "effect_sha256": sha(effect)}

    def save():
        path.write_bytes((json.dumps(outcome, indent=2) + "\n").encode())

    config, roots, _ = workspace.load_config(ROOT / ".aide.local/execution.json")
    assert workspace.digest(config) == plan["control_config_digest"]
    spec = importlib.util.spec_from_file_location("posix_checkpoint_lite", ROOT / ".aide/scripts/aide_lite.py")
    lite = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lite
    spec.loader.exec_module(lite)
    try:
        with workspace.estate_lock(roots["control"]), workspace.estate_lock(roots["control"], "dispatch.lock"):
            assert workspace.dispatch_state(roots["control"])["mode"] == "running"
            assert not (roots["control"] / "active.json").exists()
            assert git("branch", "--show-current") == plan["task_branch"]
            assert git("rev-parse", "HEAD") == plan["checkpoint_parent"]
            for ref in ("main", "dev", "origin/main", "origin/dev"):
                assert git("rev-parse", ref) == plan["integration_base"]
            assert not git("diff", "--cached", "--name-only")
            changed = set(git("diff", "--name-only").splitlines()) | set(git("ls-files", "--others", "--exclude-standard").splitlines())
            assert changed == allowed, sorted(changed ^ allowed)
            for name, value in mapped["files"].items():
                assert sha(ROOT / name) == value if value is not None else not (ROOT / name).exists(), name
            pins = json.loads((EVIDENCE / "package-inputs.json").read_bytes())
            assert all(sha(ROOT / n) == v for n, v in pins["files"].items())
            for flags in (("--all",), ("--push", "--all")):
                assert git("remote", "get-url", *flags, "origin") == plan["origin_url"]
            remote = dict(line.split()[::-1] for line in git("ls-remote", "--heads", "origin", "dev", "main").splitlines())
            assert remote == {"refs/heads/dev": plan["integration_base"], "refs/heads/main": plan["integration_base"]}
            helper = lite.make_git_helper_plan(ROOT, "plan", dry_run=True)
            outcome["helper_plan"] = helper
            save()
            assert helper["status"] == "blocked" and helper["blockers"] == ["dirty_tree_requires_classification"]
            git("diff", "--check")
            git("add", "--", *sorted(allowed))
            assert set(git("diff", "--cached", "--name-only").splitlines()) == allowed
            for name in allowed:
                if name in mapped["files"] and mapped["files"][name] is None:
                    assert not git("ls-files", "--stage", "--", name)
                else:
                    assert git("hash-object", "--no-filters", "--", name) == git("rev-parse", ":" + name), name
            tree = git("write-tree")
            message_path = EVIDENCE / "source-message-03.txt"
            commit = create_commit(ROOT, message=message_path.read_bytes(), expected_message_sha256=sha(message_path),
                expected_ref="refs/heads/" + plan["task_branch"], expected_head=plan["checkpoint_parent"],
                expected_tree=tree, allowed_paths=sorted(allowed), apply=True,
                validator=lambda text: [c.message for c in lite.validate_commit_message_text(text) if c.severity == "FAIL"])
            outcome.update(state="checkpointed", commit=commit)
            save()
            assert commit["status"] == "COMMITTED" and not git("status", "--porcelain")
            subprocess.run(["py", "-3", "-B", ".aide/scripts/aide_lite.py", "commit", "check", "--latest"],
                cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        observer = TASK / "observe_hosted.py"
        subprocess.run([sys.executable, "-B", str(observer), sha(source), sha(effect)], cwd=ROOT, check=True)
        outcome["state"] = "hosted_observed"
        save()
    except BaseException as error:
        outcome.update(state="stopped", error_type=type(error).__name__, error=str(error))
        save()
        raise


if __name__ == "__main__":
    main()
