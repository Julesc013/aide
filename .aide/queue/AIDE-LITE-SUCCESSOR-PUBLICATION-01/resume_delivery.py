"""Resume only the verified existing draft; never replay completed delivery."""
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


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--tree", required=True)
    parser.add_argument("--effect-sha256", required=True)
    args = parser.parse_args()
    effect = EVIDENCE / "recovery-effect.json"
    assert sha(effect) == args.effect_sha256
    plan = json.loads(effect.read_bytes())
    original = json.loads((EVIDENCE / "delivery-effect.json").read_bytes())
    assert sha(Path(__file__)) == plan["controller_sha256"]
    assert sha(Path(original["gh_executable"])) == original["gh_sha256"]
    assert sha(Path(sys.executable)) == original["python_sha256"]
    config_file = ROOT / ".aide.local/execution.json"
    config, roots, _ = workspace.load_config(config_file)
    assert workspace.digest(config) == original["config_digest"]
    receipt = EVIDENCE / "delivery-recovery-result.log"
    assert not receipt.exists(), "Existing recovery intent must be reconciled"
    deadline = time.monotonic() + 480
    record = {"status": "STARTED", "commit": args.commit, "tree": args.tree,
              "release_target": plan["release_target"], "release_id": plan["release_id"],
              "tag_object": plan["tag_object"], "operations": [], "model_requests": 0}
    task_remote = plan["release_target"]

    def save():
        receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")

    def run(label, command, maximum=60):
        remaining = deadline - time.monotonic()
        assert remaining > 0
        row = {"label": label, "argv": command, "status": "STARTED", "at_unix_ns": time.time_ns()}
        record["operations"].append(row)
        save()
        paths = [EVIDENCE / ("recovery-" + label + suffix) for suffix in (".stdout.log", ".stderr.log")]
        try:
            with paths[0].open("xb") as out, paths[1].open("xb") as err:
                result = subprocess.run(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                                        stdout=out, stderr=err, timeout=min(maximum, remaining))
            row.update(status="COMPLETED", exit_code=result.returncode)
            assert result.returncode == 0, label + " failed; reconcile actual effects"
        except BaseException as error:
            row.update(status="UNCERTAIN_OR_FAILED", failure_type=type(error).__name__)
            raise
        finally:
            row["streams"] = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)}
                              for p in paths if p.exists()}
            save()
        assert all(p.stat().st_size <= 1024 * 1024 for p in paths)
        return paths[0].read_text(encoding="utf-8").strip()

    def git(label, *argv):
        return run(label, ["git", *argv])

    def api(label, endpoint):
        return json.loads(run(label, [original["gh_executable"], "api", "-H",
            "X-GitHub-Api-Version: 2026-03-10", "repos/Julesc013/aide" + endpoint]))

    def guard(label):
        actual, _, _ = workspace.load_config(config_file)
        assert workspace.digest(actual) == original["config_digest"]
        assert workspace.dispatch_state(roots["control"])["mode"] == "running"
        assert not (roots["control"] / "active.json").exists()
        assert git(label + "-head", "rev-parse", "HEAD") == args.commit
        assert git(label + "-tree", "rev-parse", "HEAD^{tree}") == args.tree
        assert git(label + "-branch", "symbolic-ref", "--short", "HEAD") == original["task_branch"]
        assert not git(label + "-clean", "status", "--porcelain")
        for name in ("dev", "main"):
            assert git(label + "-" + name, "rev-parse", name) == plan["release_target"]
        for name, value in original["preserved_local_refs"].items():
            assert git(label + "-preserved-" + name.split("/")[-1], "rev-parse", name) == value
        expected = {**original["preserved_remote_refs"], "refs/heads/dev": plan["release_target"],
                    "refs/heads/main": plan["release_target"],
                    "refs/heads/" + original["task_branch"]: task_remote,
                    "refs/tags/aide-lite-v1.1.0": plan["tag_object"],
                    "refs/tags/aide-lite-v1.1.0^{}": plan["release_target"]}
        text = git(label + "-remote", "ls-remote", "--heads", "--tags", "origin", *expected)
        assert dict(line.split()[::-1] for line in text.splitlines()) == expected
        assert git(label + "-tag", "rev-parse", "refs/tags/aide-lite-v1.1.0") == plan["tag_object"]
        for path, value in plan["files"].items():
            assert sha(ROOT / path) == value, path

    def admit(label):
        record[label] = workspace.inspect(config_file)
        assert record[label]["active"] is None and record[label]["dispatch"]["mode"] == "running"
        save()

    def check_release(value, draft, ids=None):
        assert value["id"] == plan["release_id"] and value["tag_name"] == "aide-lite-v1.1.0"
        assert value["name"] == "AIDE Lite 1.1.0"
        assert value["body"] == (TASK / "release-notes.md").read_text(encoding="utf-8")
        assert value["target_commitish"] == plan["release_target"]
        assert value["draft"] is draft and not value["prerelease"]
        assert bool(value["published_at"]) is (not draft)
        assert {row["name"] for row in value["assets"]} == set(original["assets"])
        assert len(value["assets"]) == 4 and len({row["id"] for row in value["assets"]}) == 4
        for row in value["assets"]:
            expected = original["assets"][row["name"]]
            assert row["label"] == expected["label"] and row["size"] == expected["size_bytes"]
            assert row["state"] == "uploaded" and row["digest"] == "sha256:" + expected["sha256"]
        actual = sorted(row["id"] for row in value["assets"])
        assert ids is None or ids == actual
        return actual

    spec = importlib.util.spec_from_file_location("existing_release_projection", TASK / "update_presentation.py")
    projection = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = projection
    spec.loader.exec_module(projection)

    def listing(label):
        values = api(label, "/releases?per_page=100")
        assert isinstance(values, list) and len(values) == 2
        assert {row["id"] for row in values} == {plan["release_id"], original["previous_release"]["id"]}
        old = next(row for row in values if row["id"] == original["previous_release"]["id"])
        assert projection.projection(old) == original["previous_release"]

    endpoint = "/releases/" + str(plan["release_id"])
    try:
        with workspace.estate_lock(roots["control"]), workspace.estate_lock(roots["control"], "dispatch.lock"):
            guard("before")
            admit("initial_admission")
            listing("list-before")
            before = api("draft-before", endpoint)
            assert projection.projection(before) == projection.projection(json.loads((EVIDENCE / "recovery-draft-before.json").read_bytes()))
            assert before["draft"] and not before["prerelease"] and before["published_at"] is None and not before["assets"]
            assert before["tag_name"] == "aide-lite-v1.1.0" and before["name"] == "AIDE Lite 1.1.0"
            assert before["body"] == (TASK / "release-notes.md").read_text(encoding="utf-8")
            assert before["target_commitish"] == plan["release_target"]
            git("push-recovery-checkpoint", "push", "origin", args.commit + ":refs/heads/" + original["task_branch"])
            task_remote = args.commit
            guard("pre-upload")
            admit("upload_admission")
            assert projection.projection(api("draft-pre-upload", endpoint)) == projection.projection(before)
            uploads = [str(ROOT / row["path"]) + "#" + row["label"] for row in original["assets"].values()]
            run("upload", [original["gh_executable"], "release", "upload", "aide-lite-v1.1.0",
                *uploads, "--repo", "Julesc013/aide"], 120)
            uploaded = api("uploaded", endpoint)
            ids = check_release(uploaded, True)
            record["asset_ids"] = ids
            save()
            guard("pre-publish")
            admit("publication_admission")
            listing("list-pre-publish")
            check_release(api("draft-pre-publish", endpoint), True, ids)
            run("publish", [original["gh_executable"], "release", "edit", "aide-lite-v1.1.0",
                "--repo", "Julesc013/aide", "--draft=false", "--prerelease=false", "--latest", "--verify-tag"])
            published = api("published", endpoint)
            check_release(published, False, ids)
            assert api("latest", "/releases/latest")["id"] == plan["release_id"]
            guard("pre-acquire")
            admit("acquisition_admission")
            destination = ROOT / ".aide/release/acquired-aide-lite-v1.1.0.log"
            assert not destination.exists() and not destination.is_symlink()
            assert shutil.disk_usage(ROOT / ".aide/release").free >= config["limits"]["disk_reserve_bytes"] + 4 * 1024 * 1024
            run("acquire", [sys.executable, "-I", "-B", str(TASK / "acquire.py")], 200)
            acquired = json.loads((destination / "acquisition.json").read_bytes())
            assert acquired["status"] == "PASS"
            identities = {}
            for name, expected in original["assets"].items():
                path = destination / name
                assert path.stat().st_size == expected["size_bytes"] and sha(path) == expected["sha256"]
                identities[name] = {"size_bytes": path.stat().st_size, "sha256": sha(path)}
            record.update(status="PUBLISHED_ACQUIRED_CONSUMER_PENDING", published=published, acquired=identities,
                          acquisition_receipt_sha256=sha(destination / "acquisition.json"))
            guard("final")
    except BaseException as error:
        record.update(status="STOPPED_RECONCILE", failure_type=type(error).__name__, failure=str(error))
        raise
    finally:
        save()
    print(json.dumps({"status": record["status"], "release_id": plan["release_id"],
                      "tag_target": plan["release_target"], "execution_source": args.commit, "assets": 4}))


if __name__ == "__main__":
    main()
