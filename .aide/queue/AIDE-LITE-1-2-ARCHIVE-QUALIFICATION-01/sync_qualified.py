"""One-shot qualified evidence checkpoint and nonforce dev/main synchronization."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace
from core.apply.managed_commit import create_commit

TASK = Path(__file__).parent
EVIDENCE = TASK / "evidence"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_lite():
    spec = importlib.util.spec_from_file_location("aide_profile_projection", ROOT / ".aide/scripts/aide_lite.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_source_output(validation):
    lines = validation.splitlines()
    assert lines.count("status: PASS") == 1
    summary = [line for line in lines if line.startswith("checks:")]
    assert len(summary) == 1
    counts = re.fullmatch(r"checks: (\d+); PASS: (\d+); WARN: (\d+); FAIL: (\d+); OTHER: (\d+)", summary[0])
    assert counts and tuple(map(int, counts.groups()[2:])) == (1, 0, 0)
    assert int(counts[1]) == int(counts[2]) + 1
    nonpass = [line for line in lines if line.startswith("- ") and not line.startswith("- PASS ")]
    assert nonpass == ["- WARN review packet review ref missing: .aide/prompts/evidence-review.md"]


def project_preview(lite, base, commit, label, canonical_preimages, plan_commits):
    """Admitted task evidence only; never invoke the guarded canonical writer."""
    def canonical_unchanged():
        assert all(sha(ROOT / name) == value for name, value in canonical_preimages.items())
    canonical_unchanged()
    output = EVIDENCE / ("qualified-projection-" + label + ".log")
    assert not output.exists()
    relative = output.relative_to(ROOT).as_posix()
    ignored = subprocess.run(["git", "check-ignore", "--quiet", relative], cwd=ROOT)
    assert ignored.returncode == 0
    revision_range = base + ".." + commit
    data = lite.make_changelog_preview(ROOT, revision_range=revision_range, limit=None)
    expected = subprocess.check_output(["git", "rev-list", revision_range], cwd=ROOT, text=True).splitlines()
    assert expected == [commit, *plan_commits]
    assert data["commit_count"] == len(expected)
    assert data["source_range"] == revision_range and data["source_head"] == commit
    assert data["malformed_count"] == 0 and not data["malformed_commits"]
    assert {entry["commit_sha"] for entry in data["entries"]} == set(expected)
    assert data["preview_only"] is True and data["release_publishing"] is False
    release = lite.make_release_notes_preview_data(data)
    paths = lite.output_changelog_paths(ROOT, output_dir=relative)
    content = {
        "changelog_json": lite.stable_json_text(data),
        "release_notes_json": lite.stable_json_text(release),
        "changelog_md": lite.render_changelog_preview(data),
        "release_notes_md": lite.render_release_notes_preview(data, release),
        "malformed_md": lite.render_malformed_commits_report(data),
        "report_md": lite.render_changelog_report(data, release),
    }
    assert set(paths) == set(content) and len(content) == 6
    assert sum(len(text.encode("utf-8")) for text in content.values()) <= 1024 * 1024
    output.mkdir()
    for key, text in content.items():
        assert paths[key].parent == output
        with paths[key].open("xb") as stream:
            stream.write(text.encode("utf-8"))
    checks = lite.validate_changelog_outputs(ROOT, output_dir=relative)
    assert checks and all(check.severity == "PASS" for check in checks)
    canonical_unchanged()
    return {path.name: sha(path) for path in paths.values()}


def main():
    assert len(sys.argv) == 3, "exact source/effect hashes required"
    source = EVIDENCE / "qualified-integration-source.json"
    effect = EVIDENCE / "qualified-integration-effect.json"
    assert sha(source) == sys.argv[1] and sha(effect) == sys.argv[2]
    mapped = json.loads(source.read_bytes())
    plan = json.loads(effect.read_bytes())
    assert sha(effect) == mapped["effect_sha256"]
    attempt = EVIDENCE / plan["attempt_directory"]
    assert attempt.parent == EVIDENCE and attempt.name == "qualified-integration-attempt-01.log"
    attempt.mkdir()
    receipt = attempt / "result.json"
    with receipt.open("x", encoding="utf-8") as out:
        out.write("{}\n")
    record = {"status": "RUNNING", "operations": []}
    deadline = time.monotonic() + 420

    def save():
        receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")

    def run(label, args):
        assert time.monotonic() < deadline
        row = {"label": label, "argv": args, "state": "started"}
        record["operations"].append(row)
        save()
        outputs = [attempt / (label + suffix) for suffix in (".stdout.log", ".stderr.log")]
        try:
            with outputs[0].open("xb") as out, outputs[1].open("xb") as err:
                result = subprocess.run(args, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=out,
                                        stderr=err, timeout=min(120, max(1, deadline - time.monotonic())))
            row.update(state="completed", exit_code=result.returncode)
        except BaseException as error:
            row.update(state="exception", error_type=type(error).__name__, error=str(error))
            raise
        finally:
            row["streams"] = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)} for p in outputs if p.exists()}
            save()
        assert result.returncode == 0, label
        return outputs[0].read_text(encoding="utf-8").strip()

    def git(label, *args):
        return run(label, ["git", *args])

    config, roots, _ = workspace.load_config(ROOT / ".aide.local/execution.json")
    assert workspace.digest(config) == plan["control_config_digest"]
    state = {"dev": plan["base"], "main": plan["main_base"]}
    attestation = EVIDENCE / "qualified-integration-review.json"
    expected = set(mapped["files"]) | {source.relative_to(ROOT).as_posix(), attestation.relative_to(ROOT).as_posix()}
    lite = load_lite()

    def inputs():
        assert sha(source) == sys.argv[1] and sha(effect) == sys.argv[2]
        verdict = json.loads(attestation.read_bytes())
        assert verdict["decision"] == "ACCEPT" and not verdict["required_fixes"]
        assert verdict["reviewer"] == "/root/review_disked_continuation"
        assert verdict["source_sha256"] == sys.argv[1] and verdict["effect_sha256"] == sys.argv[2]
        assert verdict["controller_sha256"] == sha(Path(__file__))
        for name, value in mapped["files"].items():
            assert sha(ROOT / name) == value, name
        pins = json.loads((EVIDENCE / "qualified-integration-inputs.json").read_bytes())
        assert all(sha(ROOT / name) == value for name, value in pins["files"].items())
        assert all(sha(ROOT / name) == value for name, value in plan["stable_assets"].items())
        closure_path = EVIDENCE / 'qualification-closure-review.json'
        closure = json.loads(closure_path.read_bytes())
        assert closure['decision'] == 'ACCEPT' and not closure['required_fixes']
        assert closure['proposal_sha256'] == sha(EVIDENCE / 'qualification-closure-proposal.json')
        proof = json.loads((EVIDENCE / 'final-qualified.json').read_bytes())
        assert proof['state'] == 'PASS_FINAL_LOCAL_GROUP_AND_EXACT_REPLAY' and proof['qualification_pass']
        assert proof['scratch_absent'] and proof['reservation_released']
        assert all(workspace.content_digest(Path(proof['retained']) / name) == value for name,value in proof['collected_manifest'].items())
        assert proof['subject']['commit'] == plan['source_parent']
        assert json.loads((EVIDENCE / 'profile-build-result.json').read_bytes())['assets'] == plan['candidate_assets']
        assert proof['local_jobs_consumed'] == 17 and proof['export_refreshes_consumed'] == 2
        assert workspace.dispatch_state(roots["control"])["mode"] == "running"
        assert not (roots["control"] / "active.json").exists()
        for name, value in state.items():
            assert subprocess.check_output(["git", "rev-parse", name], cwd=ROOT, text=True).strip() == value
        assert subprocess.check_output(["git", "show-ref"], cwd=ROOT, text=True).splitlines() == preserved_refs()

    def preserved_refs():
        allowed = {"refs/heads/dev": state["dev"], "refs/heads/main": state["main"],
                   "refs/heads/" + plan["task_branch"]: record.get("commit", plan["source_parent"]),
                   "refs/remotes/origin/dev": state["dev"], "refs/remotes/origin/main": state["main"]}
        expected_refs = plan["all_refs"] | allowed
        if record.get("task_branch_retired"):
            del expected_refs["refs/heads/" + plan["task_branch"]]
        for name, target in plan["symbolic_refs"].items():
            assert subprocess.check_output(["git", "symbolic-ref", name], cwd=ROOT, text=True).strip() == target
            expected_refs[name] = expected_refs[target]
        return [value + " " + name for name, value in sorted(expected_refs.items())]

    def remote(label):
        rows = git(label, "ls-remote", "--heads", "origin", "dev", "main").splitlines()
        actual = {line.split()[1].split("/")[-1]: line.split()[0] for line in rows}
        assert actual == state, actual

    def origin(label):
        assert git(label + "-fetch-url", "remote", "get-url", "--all", "origin").splitlines() == [plan["origin_url"]]
        assert git(label + "-push-url", "remote", "get-url", "--push", "--all", "origin").splitlines() == [plan["origin_url"]]

    def helper(label):
        result = run(label, [sys.executable, "-B", ".aide/scripts/aide_lite.py", "git", "plan"])
        assert "result: ready_dry_run" in result

    def fetch(label):
        origin(label)
        remote(label + "-before")
        git(label, "fetch", "--no-tags", "origin", "refs/heads/dev:refs/remotes/origin/dev",
            "refs/heads/main:refs/remotes/origin/main")
        remote(label + "-after")
        inputs()

    try:
        with workspace.estate_lock(roots["control"]), workspace.estate_lock(roots["control"], "dispatch.lock"):
            inputs()
            assert git("branch", "branch", "--show-current") == plan["task_branch"]
            assert git("base", "rev-parse", "HEAD") == plan["source_parent"]
            assert not git("index", "diff", "--cached", "--name-only")
            changed = set(git("changed", "diff", "--name-only").splitlines())
            changed |= set(git("untracked", "ls-files", "--others", "--exclude-standard").splitlines())
            assert changed == expected, changed ^ expected
            fetch("fetch-commit")
            run("message", [sys.executable, "-B", ".aide/scripts/aide_lite.py", "commit", "check",
                            "--message-file", str(EVIDENCE / "qualified-integration-message.txt")])
            git("stage", "add", "--", *sorted(expected))
            assert set(git("staged", "diff", "--cached", "--name-only").splitlines()) == expected
            inputs()
            for index, name in enumerate(sorted(expected)):
                assert git("raw-" + str(index), "hash-object", "--no-filters", "--", name) == git("blob-" + str(index), "rev-parse", ":" + name), name
            tree = git("tree", "write-tree")
            message = (EVIDENCE / "qualified-integration-message.txt").read_bytes()
            outcome = create_commit(
                ROOT, message=message, expected_message_sha256=sha(EVIDENCE / "qualified-integration-message.txt"),
                expected_ref="refs/heads/" + plan["task_branch"], expected_head=plan["source_parent"],
                expected_tree=tree, allowed_paths=sorted(expected),
                validator=lambda text: [check.message for check in lite.validate_commit_message_text(text) if check.severity == "FAIL"],
                apply=True,
            )
            record["managed_commit"] = outcome
            save()
            assert outcome["status"] == "COMMITTED", outcome
            commit = outcome["candidate_commit"]
            record.update(commit=commit, tree=tree)
            save()
            assert not git("clean", "status", "--porcelain")
            run("commit-check", [sys.executable, "-B", ".aide/scripts/aide_lite.py", "commit", "check", "--latest"])
            run('commit-range-before-sync', [sys.executable, '-B', '.aide/scripts/aide_lite.py', 'commit', 'check',
                                             '--range', plan['base'] + '..' + commit])
            validation = run('validate-before-sync', [sys.executable, '-B', '.aide/scripts/aide_lite.py', 'validate'])
            validate_source_output(validation)
            record["preview_sha256s"] = project_preview(lite, plan["base"], commit, "local", plan["canonical_preimages"], plan["source_commits"])
            save()
            for target in ("dev", "main"):
                fetch("fetch-" + target)
                helper("helper-" + target)
                assert git("head-" + target, "rev-parse", "HEAD") == commit
                assert not git("clean-" + target, "status", "--porcelain")
                git("ancestor-" + target, "merge-base", "--is-ancestor", state[target], commit)
                git("ref-" + target, "update-ref", "refs/heads/" + target, commit, state[target])
                state[target] = commit
                origin("push-" + target)
                git("push-" + target, "push", "--no-follow-tags", "origin", commit + ":refs/heads/" + target)
                remote("remote-" + target)
                if target == "dev":
                    validation = run("validate-dev", [sys.executable, "-B", ".aide/scripts/aide_lite.py", "validate"])
                    validate_source_output(validation)
                    run("commit-range", [sys.executable, "-B", ".aide/scripts/aide_lite.py", "commit", "check", "--range", "main..dev"])
                hashes = project_preview(lite, plan["base"], commit, target, plan["canonical_preimages"], plan["source_commits"])
                assert hashes == record["preview_sha256s"]
                save()
                # A push updates tracking refs only when the matching fetchspec exists.
                git("tracking-" + target, "fetch", "--no-tags", "origin", "refs/heads/" + target + ":refs/remotes/origin/" + target)
                inputs()
            assert git("retained-task-branch", "branch", "--show-current") == plan["task_branch"]
            inputs()
            assert not git("final-clean", "status", "--porcelain")
            remote("remote-final")
            record.update(status="PASS", refs=state)
            save()
        print(json.dumps({k: v for k, v in record.items() if k != "operations"}))
    except BaseException as error:
        record.update(status="FAILED_RECONCILE_BEFORE_RETRY", error_type=type(error).__name__, error=str(error))
        save()
        raise


if __name__ == "__main__":
    main()
