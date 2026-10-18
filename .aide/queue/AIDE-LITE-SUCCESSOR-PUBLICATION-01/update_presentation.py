"""One reviewed metadata-only correction; receipts make retries explicit."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
TASK = Path(__file__).resolve().parent
EVIDENCE = TASK / "evidence"
sys.path.insert(0, str(ROOT))
from core.execution.managed_workspace import load_config, digest, estate_lock, dispatch_state, inspect

API = "repos/Julesc013/aide"
HEADER = ["-H", "X-GitHub-Api-Version: 2026-03-10"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def projection(release):
    keys = ["id", "tag_name", "name", "body", "draft", "prerelease",
            "published_at", "target_commitish", "immutable"]
    asset_keys = ["id", "name", "label", "size", "digest", "state", "browser_download_url"]
    return {**{key: release.get(key) for key in keys},
            "assets": sorted([{key: row.get(key) for key in asset_keys}
                              for row in release["assets"]], key=lambda row: row["id"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--tree", required=True)
    parser.add_argument("--effect-sha256", required=True)
    args = parser.parse_args()
    effect_path = EVIDENCE / "presentation-effect.json"
    assert sha(effect_path) == args.effect_sha256
    effect = json.loads(effect_path.read_text(encoding="utf-8"))
    for path, expected in effect["files"].items():
        assert sha(ROOT / path) == expected, path
    assert sha(Path(effect["gh_executable"])) == effect["gh_sha256"]
    config_path = ROOT / ".aide.local/execution.json"
    config, roots, _ = load_config(config_path)
    assert digest(config) == effect["config_digest"]
    result_path = EVIDENCE / "presentation-result.log"
    assert not result_path.exists(), "Existing intent requires reconciliation, not replay"
    deadline = time.monotonic() + 240
    receipt = {"status": "STARTED", "source_commit": args.commit, "source_tree": args.tree,
               "effect_sha256": args.effect_sha256, "operations": [], "model_requests": 0,
               "containment": "cooperative bounded parent operations", "whole_outcome_usage": "unknown"}

    def save():
        result_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")

    def invoke(label, command):
        remaining = deadline - time.monotonic()
        assert remaining > 0, "Presentation deadline expired"
        out = EVIDENCE / ("presentation-" + label + ".stdout.log")
        err = EVIDENCE / ("presentation-" + label + ".stderr.log")
        row = {"label": label, "argv": command, "status": "STARTED", "exit_code": None}
        receipt["operations"].append(row)
        save()
        try:
            with out.open("xb") as stdout, err.open("xb") as stderr:
                completed = subprocess.run(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                                           stdout=stdout, stderr=stderr, timeout=min(30, remaining))
            row.update(status="COMPLETED", exit_code=completed.returncode)
            assert completed.returncode == 0, label + " failed; reconcile actual state"
        except BaseException as error:
            row.update(status="UNCERTAIN_OR_FAILED", failure_type=type(error).__name__)
            raise
        finally:
            row["streams"] = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)}
                              for p in [out, err] if p.exists()}
            save()
        assert out.stat().st_size <= 1024 * 1024, label + " response exceeds bound"
        return out.read_text(encoding="utf-8")

    gh = effect["gh_executable"]

    def api(label, endpoint, payload=None):
        command = [gh, "api", *HEADER]
        if payload is not None:
            command += ["--method", "PATCH", "--input", str(ROOT / payload)]
        return json.loads(invoke(label, command + [endpoint]))

    def local_guard():
        assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == args.commit
        assert subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip() == args.tree
        assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).strip()
        assert dispatch_state(roots["control"])["mode"] == "running"
        assert not (roots["control"] / "active.json").exists()
        for path, expected_sha in effect["files"].items():
            assert sha(ROOT / path) == expected_sha, path

    expected = projection(json.loads((ROOT / effect["before"]).read_text(encoding="utf-8")))
    try:
        with estate_lock(roots["control"]), estate_lock(roots["control"], "dispatch.lock"):
            local_guard()
            receipt["admission"] = inspect(config_path)
            assert receipt["admission"]["active"] is None
            save()
            endpoint = API + "/releases/" + str(expected["id"])
            observed = api("before", endpoint)
            assert projection(observed) == expected, "Release changed since preparation"
            tags = invoke("tags-before", ["git", "ls-remote", "--tags", "origin",
                         "refs/tags/aide-lite-v1.0.0", "refs/tags/aide-lite-v1.0.0^{}"])
            assert dict(line.split()[::-1] for line in tags.splitlines()) == effect["tag_refs"]
            changes = [("body", endpoint, effect["body_payload"])]
            changes += [(str(row["id"]), API + "/releases/assets/" + str(row["id"]), row["payload"])
                        for row in effect["labels"]]
            for label, target, payload in changes:
                local_guard()
                current = api(label + "-pre", endpoint)
                assert projection(current) == expected, "Concurrent release metadata change"
                api(label + "-patch", target, payload)
                if label == "body":
                    expected["body"] = json.loads((ROOT / payload).read_text(encoding="utf-8"))["body"]
                else:
                    value = json.loads((ROOT / payload).read_text(encoding="utf-8"))["label"]
                    next(item for item in expected["assets"] if item["id"] == int(label))["label"] = value
                current = api(label + "-post", endpoint)
                assert projection(current) == expected, "Unexpected or uncertain metadata result"
            tags_after = invoke("tags-after", ["git", "ls-remote", "--tags", "origin",
                                "refs/tags/aide-lite-v1.0.0", "refs/tags/aide-lite-v1.0.0^{}"])
            assert tags_after == tags, "Tag identity changed"
            local_guard()
            receipt.update(status="PASS", final=expected,
                           immutable_release_fields_preserved=True, asset_bytes_and_names_preserved=True,
                           tag_unchanged=True, mutations=5)
    except BaseException as error:
        receipt.update(status="STOPPED_RECONCILE", failure_type=type(error).__name__)
        raise
    finally:
        save()
    print(json.dumps({"result": receipt["status"], "release": expected["tag_name"], "mutations": 5}))


if __name__ == "__main__":
    main()
