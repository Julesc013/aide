"""Deliver one reviewed documentation checkpoint and the frozen Lite release."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
TASK = Path(__file__).resolve().parent
EVIDENCE = TASK / "evidence"
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace

API = "repos/Julesc013/aide"
TAG = "aide-lite-v1.1.0"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--tree", required=True)
    parser.add_argument("--effect-sha256", required=True)
    args = parser.parse_args()
    effect_file = EVIDENCE / "delivery-effect.json"
    assert sha(effect_file) == args.effect_sha256
    plan = json.loads(effect_file.read_bytes())
    assert sha(Path(__file__)) == plan["controller_sha256"]
    config_file = ROOT / ".aide.local/execution.json"
    config, roots, _ = workspace.load_config(config_file)
    assert workspace.digest(config) == plan["config_digest"]
    assert sha(Path(plan["gh_executable"])) == plan["gh_sha256"]
    assert sha(Path(sys.executable)) == plan["python_sha256"]
    receipt_file = EVIDENCE / "delivery-result.log"
    assert not receipt_file.exists(), "Reconcile an existing delivery; never replay"
    deadline = time.monotonic() + 900
    record = {"status": "STARTED", "commit": args.commit, "tree": args.tree,
              "effect_sha256": args.effect_sha256, "operations": [], "model_requests": 0}
    state = {"dev": plan["base"], "main": plan["base"],
             "task_remote": plan["task_remote_before"]}

    def save():
        receipt_file.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")

    def run(label, command, maximum=60):
        remaining = deadline - time.monotonic()
        assert remaining > 0, "Delivery deadline expired"
        row = {"label": label, "argv": command, "status": "STARTED", "at_unix_ns": time.time_ns()}
        record["operations"].append(row)
        save()
        out = EVIDENCE / ("delivery-" + label + ".stdout.log")
        err = EVIDENCE / ("delivery-" + label + ".stderr.log")
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

    def api(label, suffix):
        return json.loads(run(label, [plan["gh_executable"], "api", "-H",
                                     "X-GitHub-Api-Version: 2026-03-10", API + suffix]))

    def guards(label):
        actual, _, _ = workspace.load_config(config_file)
        assert workspace.digest(actual) == plan["config_digest"]
        assert workspace.dispatch_state(roots["control"])["mode"] == "running"
        assert not (roots["control"] / "active.json").exists()
        assert git(label + "-head", "rev-parse", "HEAD") == args.commit
        assert git(label + "-tree", "rev-parse", "HEAD^{tree}") == args.tree
        assert git(label + "-branch", "symbolic-ref", "--short", "HEAD") == plan["task_branch"]
        assert not git(label + "-clean", "status", "--porcelain")
        for branch in ("dev", "main"):
            assert git(label + "-" + branch, "rev-parse", "refs/heads/" + branch) == state[branch]
        for ref, expected in plan["preserved_local_refs"].items():
            assert git(label + "-preserve-" + ref.split("/")[-1], "rev-parse", ref) == expected
        for path, expected in plan["files"].items():
            assert sha(ROOT / path) == expected, path

    def remote(label):
        refs = git(label, "ls-remote", "--heads", "--tags", "origin",
                   "refs/heads/dev", "refs/heads/main", "refs/heads/" + plan["task_branch"],
                   "refs/heads/task/aide-lite-successor-qualification-01",
                   "refs/tags/aide-lite-v1.0.0", "refs/tags/aide-lite-v1.0.0^{}",
                   "refs/tags/" + TAG, "refs/tags/" + TAG + "^{}")
        observed = dict(line.split()[::-1] for line in refs.splitlines())
        expected = {**plan["preserved_remote_refs"], "refs/heads/dev": state["dev"],
                    "refs/heads/main": state["main"],
                    "refs/heads/" + plan["task_branch"]: state["task_remote"]}
        if "tag_object" in record:
            expected.update({"refs/tags/" + TAG: record["tag_object"],
                             "refs/tags/" + TAG + "^{}": args.commit})
        assert observed == expected, observed

    def admission(label):
        value = workspace.inspect(config_file)
        assert value["active"] is None and value["dispatch"]["mode"] == "running"
        record[label] = value
        save()

    def range_check(label):
        result = lite(label, "commit", "check", "--range", plan["base"] + ".." + args.commit)
        assert result.splitlines()[1] == "result: PASS"
        rows = [line.split() for line in result.splitlines() if line.startswith("- ")]
        assert all(row[2] == "PASS" for row in rows)
        assert len(rows) == int(git(label + "-count", "rev-list", "--count", plan["base"] + ".." + args.commit))

    def release_check(value, draft, asset_ids=None):
        assert value["tag_name"] == TAG and value["name"] == "AIDE Lite 1.1.0"
        assert value["body"] == (TASK / "release-notes.md").read_text(encoding="utf-8")
        assert value["target_commitish"] == args.commit
        assert value["draft"] is draft and value["prerelease"] is False
        assert bool(value["published_at"]) is (not draft)
        assets = value["assets"]
        assert len(assets) == 4 and len({item["id"] for item in assets}) == 4
        assert {item["name"] for item in assets} == set(plan["assets"])
        for item in assets:
            expected = plan["assets"][item["name"]]
            assert item["label"] == expected["label"] and item["size"] == expected["size_bytes"]
            assert item["digest"] == "sha256:" + expected["sha256"] and item["state"] == "uploaded"
        if asset_ids is not None:
            assert sorted(item["id"] for item in assets) == asset_ids
        return sorted(item["id"] for item in assets)

    def release_list(label, candidate=None):
        values = api(label, "/releases?per_page=100")
        assert isinstance(values, list) and len(values) < 100, "Incomplete release enumeration"
        expected_ids = {plan["previous_release"]["id"]}
        if candidate is not None:
            expected_ids.add(candidate)
        assert {item["id"] for item in values} == expected_ids
        previous = next(item for item in values if item["id"] == plan["previous_release"]["id"])
        assert previous["tag_name"] == "aide-lite-v1.0.0"
        assert not previous["draft"] and not previous["prerelease"]
        assert previous["published_at"] == plan["previous_release"]["published_at"]
        keys = plan["previous_release"]
        actual = {key: previous.get(key) for key in keys if key != "assets"}
        actual["assets"] = sorted([{key: item.get(key) for key in keys["assets"][0]}
                                   for item in previous["assets"]], key=lambda item: item["id"])
        assert actual == plan["previous_release"], "Published predecessor metadata changed"
        return values

    try:
        with workspace.estate_lock(roots["control"]), workspace.estate_lock(roots["control"], "dispatch.lock"):
            guards("before")
            admission("initial_admission")
            assert git("origin", "remote", "get-url", "origin") == plan["remote_url"]
            trees = git("worktrees", "worktree", "list", "--porcelain")
            assert sum(line.startswith("worktree ") for line in trees.splitlines()) == 1
            assert "worktree " + ROOT.as_posix() in trees
            git("base-ancestor", "merge-base", "--is-ancestor", plan["base"], args.commit)
            git("qualification-ancestor", "merge-base", "--is-ancestor", plan["qualification"], args.commit)
            assert "ready_dry_run" in lite("git-plan", "git", "plan")
            remote("refs-before")
            git("fetch", "fetch", "--no-tags", "origin", "refs/heads/dev:refs/remotes/origin/dev",
                "refs/heads/main:refs/remotes/origin/main")
            remote("refs-after-fetch")
            range_check("range-before")
            assert lite("validate-before", "validate").splitlines()[1] == "status: PASS"
            assert lite("doctor-before", "doctor").splitlines()[1] == "status: PASS"
            assert "PASS" in lite("pack-before", "pack-status")
            for branch in ("dev", "main"):
                guards("pre-" + branch)
                remote("remote-pre-" + branch)
                admission(branch + "_admission")
                git("cas-" + branch, "update-ref", "refs/heads/" + branch, args.commit, plan["base"])
                state[branch] = args.commit
                git("push-" + branch, "push", "origin", args.commit + ":refs/heads/" + branch)
                remote("remote-post-" + branch)
                if branch == "dev":
                    assert lite("validate-dev", "validate").splitlines()[1] == "status: PASS"
                    range_check("range-dev")
            git("push-task", "push", "origin", args.commit + ":refs/heads/" + plan["task_branch"])
            state["task_remote"] = args.commit
            remote("refs-integrated")
            record["post_main_preview"] = {"status": "STARTED"}
            save()
            preview_path = ROOT / ".aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py"
            spec = importlib.util.spec_from_file_location("delivery_fixed_preview", preview_path)
            preview = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = preview
            spec.loader.exec_module(preview)
            preview.BASE = plan["base"]
            verified = preview.verify()
            assert verified["status"] == "PASS" and verified["source_head"] == plan["fixed_preview_head"]
            record["post_main_preview"] = verified
            save()
            guards("pre-tag")
            admission("tag_admission")
            repository = api("repository", "")
            assert repository["full_name"] == "Julesc013/aide"
            assert not repository["archived"] and not repository["disabled"] and repository["permissions"]["push"]
            release_list("releases-before")
            assert not git("local-tag-absence", "tag", "--list", TAG)
            git("annotate", "-c", "tag.gpgSign=false", "tag", "-a", TAG, args.commit,
                "-F", str(TASK / "tag-message.txt"))
            record["tag_object"] = git("tag-object", "rev-parse", "refs/tags/" + TAG)
            assert git("tag-type", "cat-file", "-t", record["tag_object"]) == "tag"
            assert git("tag-target", "rev-parse", TAG + "^{}") == args.commit
            assert git("tag-tree", "rev-parse", TAG + "^{tree}") == args.tree
            tag_contents = git("tag-contents", "cat-file", "tag", record["tag_object"])
            assert tag_contents.split("\n\n", 1)[1] == (TASK / "tag-message.txt").read_text(encoding="utf-8").strip()
            save()
            git("push-tag", "push", "origin", "refs/tags/" + TAG + ":refs/tags/" + TAG)
            remote("tag-readback")
            guards("pre-draft")
            run("create-draft", [plan["gh_executable"], "release", "create", TAG, "--repo", "Julesc013/aide",
                "--draft", "--verify-tag", "--target", args.commit, "--title", "AIDE Lite 1.1.0",
                "--notes-file", str(TASK / "release-notes.md")])
            values = api("draft-list", "/releases?per_page=100")
            assert isinstance(values, list) and len(values) < 100
            matches = [item for item in values if item["tag_name"] == TAG]
            assert len(matches) == 1, "Draft creation needs exact ID reconciliation"
            draft = api("draft", "/releases/" + str(matches[0]["id"]))
            assert draft["tag_name"] == TAG and draft["name"] == "AIDE Lite 1.1.0"
            assert draft["body"] == (TASK / "release-notes.md").read_text(encoding="utf-8")
            assert draft["target_commitish"] == args.commit
            assert draft["draft"] and not draft["prerelease"] and not draft["assets"]
            record["release_id"] = draft["id"]
            save()
            uploads = [str(ROOT / row["path"]) + "#" + row["label"] for row in plan["assets"].values()]
            run("upload", [plan["gh_executable"], "release", "upload", TAG, *uploads,
                           "--repo", "Julesc013/aide"], 120)
            uploaded = api("uploaded", "/releases/" + str(draft["id"]))
            ids = release_check(uploaded, True)
            guards("pre-publish")
            remote("refs-pre-publish")
            admission("publication_admission")
            release_list("releases-pre-publish", draft["id"])
            release_check(api("draft-pre-publish", "/releases/" + str(draft["id"])), True, ids)
            run("publish", [plan["gh_executable"], "release", "edit", TAG, "--repo", "Julesc013/aide",
                "--draft=false", "--prerelease=false", "--latest", "--verify-tag"])
            published = api("published", "/releases/" + str(draft["id"]))
            release_check(published, False, ids)
            assert api("latest", "/releases/latest")["id"] == draft["id"]
            remote("refs-published")
            guards("pre-acquire")
            admission("acquisition_admission")
            destination = ROOT / ".aide/release/acquired-aide-lite-v1.1.0.log"
            assert not destination.exists() and not destination.is_symlink()
            assert shutil.disk_usage(ROOT / ".aide/release").free >= config["limits"]["disk_reserve_bytes"] + 4 * 1024 * 1024
            run("acquire", [sys.executable, "-I", "-B", str(TASK / "acquire.py")], 200)
            acquired = json.loads((destination / "acquisition.json").read_bytes())
            assert acquired["status"] == "PASS"
            identities = {}
            for name, expected in plan["assets"].items():
                path = destination / name
                assert path.stat().st_size == expected["size_bytes"] and sha(path) == expected["sha256"]
                identities[name] = {"size_bytes": path.stat().st_size, "sha256": sha(path)}
            record.update(status="PUBLISHED_ACQUIRED_CONSUMER_PENDING", published=published,
                          acquired=identities, acquisition_receipt_sha256=sha(destination / "acquisition.json"),
                          task_branch_retired=False)
            guards("final")
            remote("refs-final")
    except BaseException as error:
        record.update(status="STOPPED_RECONCILE", failure_type=type(error).__name__, failure=str(error))
        raise
    finally:
        save()
    print(json.dumps({"status": record["status"], "commit": args.commit, "release_id": record["release_id"],
                      "tag_object": record["tag_object"], "asset_count": 4}))


if __name__ == "__main__":
    main()
