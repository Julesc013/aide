"""Integrate verified release outcomes; preserve release identities and important refs."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path.cwd()
EVIDENCE = ROOT / ".aide/queue/AIDE-LITE-SUCCESSOR-PUBLICATION-01/evidence"
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    assert len(sys.argv) == 2
    effect = EVIDENCE / "closure-effect.json"
    assert sha(effect) == sys.argv[1]
    plan = json.loads(effect.read_bytes())
    candidate = json.loads((EVIDENCE / "closure-commit-result.log").read_bytes())
    commit, tree = candidate["commit"], candidate["tree"]
    assert sha(Path(__file__)) == plan["controller_sha256"]
    assert sha(Path(plan["gh_executable"])) == plan["gh_sha256"]
    config, roots, _ = workspace.load_config(ROOT / ".aide.local/execution.json")
    assert workspace.digest(config) == plan["config_digest"]
    receipt = EVIDENCE / "closure-integration-result.log"
    assert not receipt.exists(), "Reconcile previous intent; never replay"
    record = {"status": "STARTED", "commit": commit, "tree": tree, "operations": []}
    state = {"dev": plan["base"], "main": plan["base"], "task": plan["task_remote_before"]}
    deadline = time.monotonic() + 360

    def save():
        receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")

    def run(label, command, maximum=60):
        remaining = deadline - time.monotonic()
        assert remaining > 0
        row = {"label": label, "argv": command, "status": "STARTED", "at_unix_ns": time.time_ns()}
        record["operations"].append(row)
        save()
        out = EVIDENCE / ("closure-" + label + ".stdout.log")
        err = EVIDENCE / ("closure-" + label + ".stderr.log")
        try:
            with out.open("xb") as stdout, err.open("xb") as stderr:
                result = subprocess.run(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                                        stdout=stdout, stderr=stderr, timeout=min(maximum, remaining))
            row.update(status="COMPLETED", exit_code=result.returncode)
            assert result.returncode == 0, label + " failed; reconcile actual effects"
        except BaseException as error:
            row.update(status="UNCERTAIN_OR_FAILED", failure_type=type(error).__name__)
            raise
        finally:
            row["streams"] = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)}
                              for p in (out, err) if p.exists()}
            save()
        assert out.stat().st_size <= 1024 * 1024 and err.stat().st_size <= 1024 * 1024
        return out.read_text(encoding="utf-8").strip()

    def git(label, *argv):
        return run(label, ["git", *argv])

    def lite(label, *argv):
        return run(label, ["py", "-3", "-B", ".aide/scripts/aide_lite.py", *argv], 120)

    def remote(label):
        expected = {**plan["preserved_remote_refs"], "refs/heads/dev": state["dev"],
                    "refs/heads/main": state["main"], "refs/heads/" + plan["task_branch"]: state["task"]}
        text = git(label, "ls-remote", "--heads", "--tags", "origin", *expected)
        assert dict(line.split()[::-1] for line in text.splitlines()) == expected

    def guards(label):
        current, _, _ = workspace.load_config(ROOT / ".aide.local/execution.json")
        assert workspace.digest(current) == plan["config_digest"]
        assert workspace.dispatch_state(roots["control"])["mode"] == "running"
        assert not (roots["control"] / "active.json").exists()
        assert git(label + "-head", "rev-parse", "HEAD") == commit
        assert git(label + "-tree", "rev-parse", "HEAD^{tree}") == tree
        assert git(label + "-branch", "symbolic-ref", "--short", "HEAD") == plan["task_branch"]
        assert not git(label + "-clean", "status", "--porcelain")
        for branch in ("dev", "main"):
            assert git(label + "-" + branch, "rev-parse", branch) == state[branch]
        for ref, value in plan["preserved_local_refs"].items():
            assert git(label + "-preserved-" + ref.split("/")[-1], "rev-parse", ref) == value
        for path, value in plan["files"].items():
            assert sha(ROOT / path) == value, path

    def range_check(label):
        result = lite(label, "commit", "check", "--range", plan["range_base"] + ".." + commit)
        assert result.splitlines()[1] == "result: PASS"
        rows = [line.split() for line in result.splitlines() if line.startswith("- ")]
        assert all(row[2] == "PASS" for row in rows)
        assert len(rows) == int(git(label + "-count", "rev-list", "--count", plan["range_base"] + ".." + commit))

    def load(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        value = importlib.util.module_from_spec(spec)
        sys.modules[name] = value
        spec.loader.exec_module(value)
        return value

    def evidence():
        for filename in plan["attempts"]:
            attempt = json.loads((EVIDENCE / filename).read_bytes())
            assert attempt["phase"] == "retired" and attempt["result"]["quiescent"]
            assert attempt["scratch_absent"] and attempt["reservation_released"]
            assert not (roots["scratch"] / attempt["job_id"]).exists()
            for name, expected in attempt["collected_manifest"].items():
                assert workspace.content_digest(Path(attempt["retained"]) / name) == expected
        for path, expected in plan["frozen_assets"].items():
            assert sha(ROOT / path) == expected

    def public_readback(label):
        raw = run(label, [plan["gh_executable"], "api", "-H", "X-GitHub-Api-Version: 2026-03-10",
                         "repos/Julesc013/aide/releases/416392381"])
        helper = load(label + "_projection", ROOT / ".aide/queue/AIDE-LITE-SUCCESSOR-PUBLICATION-01/update_presentation.py")
        assert helper.projection(json.loads(raw)) == plan["release_projection"]

    try:
        with workspace.estate_lock(roots["control"]), workspace.estate_lock(roots["control"], "dispatch.lock"):
            guards("before")
            record["admission"] = workspace.inspect(ROOT / ".aide.local/execution.json")
            assert record["admission"]["active"] is None
            save()
            assert git("origin", "remote", "get-url", "origin") == plan["remote_url"]
            assert sum(line.startswith("worktree ") for line in git("worktrees", "worktree", "list", "--porcelain").splitlines()) == 1
            assert "ready_dry_run" in lite("helper-plan", "git", "plan")
            git("base-ancestor", "merge-base", "--is-ancestor", plan["base"], commit)
            remote("refs-before")
            git("fetch", "fetch", "--no-tags", "origin", "refs/heads/dev:refs/remotes/origin/dev",
                "refs/heads/main:refs/remotes/origin/main")
            remote("refs-after-fetch")
            evidence()
            public_readback("release-before")
            assert lite("latest", "commit", "check", "--latest").splitlines()[1] == "result: PASS"
            range_check("range-before")
            assert lite("validate-before", "validate").splitlines()[1] == "status: PASS"
            for branch in ("dev", "main"):
                guards("pre-" + branch)
                remote("remote-pre-" + branch)
                record[branch + "_admission"] = workspace.inspect(ROOT / ".aide.local/execution.json")
                assert record[branch + "_admission"]["active"] is None
                save()
                git("cas-" + branch, "update-ref", "refs/heads/" + branch, commit, plan["base"])
                state[branch] = commit
                git("push-" + branch, "push", "origin", commit + ":refs/heads/" + branch)
                remote("remote-post-" + branch)
                if branch == "dev":
                    assert lite("validate-dev", "validate").splitlines()[1] == "status: PASS"
                    range_check("range-dev")
            preview = load("closure_fixed_preview", ROOT / ".aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py")
            preview.BASE = plan["range_base"]
            record["post_main_preview"] = preview.verify()
            assert record["post_main_preview"]["source_head"] == plan["preview_head"]
            save()
            git("push-important-checkpoint", "push", "origin", commit + ":refs/heads/" + plan["task_branch"])
            state["task"] = commit
            remote("refs-final")
            guards("pre-retirement")
            evidence()
            public_readback("release-final")
            git("switch-dev", "switch", "dev")
            assert not git("dev-clean", "status", "--porcelain")
            assert git("own-task-ref", "rev-parse", "refs/heads/" + plan["task_branch"]) == commit
            git("own-task-ancestor", "merge-base", "--is-ancestor", plan["task_branch"], "dev")
            git("retire-own-local-task", "branch", "-d", plan["task_branch"])
            for ref in ("dev", "main", "origin/dev", "origin/main", "origin/" + plan["task_branch"]):
                assert git("final-" + ref.replace("/", "-"), "rev-parse", ref) == commit
            for ref, value in plan["preserved_local_refs"].items():
                assert git("final-preserved-" + ref.split("/")[-1], "rev-parse", ref) == value
            record.update(status="PASS", task_local_retired=True, remote_important_checkpoint_preserved=True,
                          release_unchanged=True, new_jobs=0)
            save()
    except BaseException as error:
        record.update(status="STOPPED_RECONCILE", failure_type=type(error).__name__, failure=str(error))
        save()
        raise
    print(json.dumps({"status": record["status"], "dev": commit, "main": commit, "local_task_retired": True,
                      "remote_important_checkpoint_preserved": True}))


if __name__ == "__main__":
    main()
