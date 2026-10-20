"""Adapt the preceding bounded observer for one exact lifecycle checkpoint.

Polling, stream caps, receipt decoding and the collection loop are unchanged.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace

TASK = Path(__file__).parent
EVIDENCE = TASK / "evidence"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = EVIDENCE / "hosted-source.json"
    effect = EVIDENCE / "hosted-effect.json"
    assert len(sys.argv) == 3 and [sha(source), sha(effect)] == sys.argv[1:]
    mapped = json.loads(source.read_bytes())
    plan = json.loads(effect.read_bytes())
    assert mapped["effect_sha256"] == sha(effect)
    verdict = json.loads((EVIDENCE / "hosted-review.json").read_bytes())
    assert verdict["decision"] == "ACCEPT" and not verdict["required_fixes"]
    assert verdict["reviewer"] == "/root/review_disked_continuation"
    assert [verdict["source_sha256"], verdict["effect_sha256"], verdict["controller_sha256"]] == [sha(source), sha(effect), sha(TASK / "checkpoint_and_host.py")]
    assert plan["observer_sha256"] == sha(Path(__file__))
    checkpoint = json.loads((EVIDENCE / "hosted-checkpoint.log").read_bytes())
    assert checkpoint["state"] == "checkpointed"
    assert checkpoint["source_sha256"] == sha(source) and checkpoint["effect_sha256"] == sha(effect)
    assert checkpoint["commit"]["status"] == "COMMITTED"
    assert plan["source_commit"] == "EXACT_REVIEWED_CHECKPOINT"
    plan["source_commit"] = checkpoint["commit"]["candidate_commit"]
    logs = EVIDENCE / "hosted-logs.log"
    logs.mkdir()
    receipt = EVIDENCE / "hosted-execution.log"
    with receipt.open("x", encoding="utf-8") as stream:
        stream.write("{}\n")
    record = {"state": "started", "operations": [], "source_commit": plan["source_commit"]}
    deadline = time.monotonic() + 1200
    byte_lock = threading.Lock()
    retained_bytes = 0

    def remaining():
        value = deadline - time.monotonic()
        if value <= 0:
            raise TimeoutError("overall observer deadline; never redispatch")
        return value

    def save():
        body = (json.dumps(record, indent=2) + "\n").encode()
        assert len(body) <= 2 * 1024 * 1024, "controller metadata cap"
        receipt.write_bytes(body)

    def run(args, timeout=45):
        nonlocal retained_bytes
        row = {"argv": args, "state": "started"}
        number = len(record["operations"])
        record["operations"].append(row)
        save()
        paths = [logs / (f"{number:03}" + suffix) for suffix in (".stdout", ".stderr")]
        process = None
        readers = []
        stop = threading.Event()
        errors = []
        operation_deadline = min(deadline, time.monotonic() + timeout)

        def drain(source, path):
            nonlocal retained_bytes
            used = 0
            try:
                with source, path.open("xb") as target:
                    while chunk := source.read(8192):
                        with byte_lock:
                            take = min(len(chunk), max(0, 16 * 1024 * 1024 - used),
                                       max(0, 64 * 1024 * 1024 - retained_bytes))
                            if take:
                                target.write(chunk[:take])
                                used += take
                                retained_bytes += take
                            if take != len(chunk):
                                errors.append("stream_or_total_byte_limit")
                                stop.set()
                                break
            except BaseException as error:
                errors.append(type(error).__name__)
                stop.set()

        try:
            remaining()
            process = subprocess.Popen(args, cwd=ROOT, stdin=subprocess.DEVNULL,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            row.update(pid=process.pid, state="running")
            save()
            for source, path in zip((process.stdout, process.stderr), paths):
                reader = threading.Thread(target=drain, args=(source, path), daemon=True)
                reader.start()
                readers.append(reader)
            while process.poll() is None:
                if stop.is_set():
                    raise RuntimeError("bounded stream drain stopped")
                if time.monotonic() >= operation_deadline:
                    raise TimeoutError("owned operation deadline")
                time.sleep(min(0.05, max(0, operation_deadline - time.monotonic())))
            for reader in readers:
                reader.join(timeout=max(0, operation_deadline - time.monotonic()))
            if any(reader.is_alive() for reader in readers) or errors:
                raise RuntimeError("bounded stream drain failed or exceeded deadline: " + repr(errors))
            remaining()
            row.update(state="completed", exit_code=process.returncode)
        except BaseException as error:
            row.update(state="exception", error_type=type(error).__name__, error=str(error))
            raise
        finally:
            # Only this Popen child is terminated; no PID enumeration or unrelated cleanup.
            cleanup_deadline = time.monotonic() + 5
            if process is not None and process.poll() is None:
                try:
                    process.kill()
                except ProcessLookupError:
                    pass
                try:
                    process.wait(timeout=max(0.001, cleanup_deadline - time.monotonic()))
                except subprocess.TimeoutExpired:
                    row["owned_child_quiescence"] = "unknown"
            for reader in readers:
                reader.join(timeout=max(0, cleanup_deadline - time.monotonic()))
            row["reader_threads_stopped"] = all(not reader.is_alive() for reader in readers)
            row["drain_errors"] = errors
            row["streams"] = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)} for p in paths if p.exists()}
            save()
        assert process.returncode == 0, f"operation {number} failed; inspect retained raw streams"
        remaining()
        return paths[0].read_bytes()

    def git(*args):
        return run(["git", *args]).decode("utf-8").strip()

    def api(endpoint):
        return json.loads(run(["gh", "api", "--hostname", "github.com", endpoint]))

    config, roots, _ = workspace.load_config(ROOT / ".aide.local/execution.json")
    assert workspace.digest(config) == plan["control_config_digest"]
    try:
        with workspace.estate_lock(roots["control"]), workspace.estate_lock(roots["control"], "dispatch.lock"):
            assert workspace.dispatch_state(roots["control"])["mode"] == "running"
            assert not (roots["control"] / "active.json").exists()
            assert all((sha(ROOT / name) == value if value is not None else not (ROOT / name).exists()) for name, value in mapped["files"].items())
            assert git("rev-parse", "HEAD") == plan["source_commit"]
            assert git("branch", "--show-current") == plan["task_branch"]
            assert not git("diff", "--name-only") and not git("diff", "--cached", "--name-only")
            assert not git("ls-files", "--others", "--exclude-standard")
            assert git("rev-parse", "HEAD^") == plan["checkpoint_parent"]
            for ref in ("dev", "origin/dev"):
                assert git("rev-parse", ref) == plan["dev_base"]
            for ref in ("main", "origin/main"):
                assert git("rev-parse", ref) == plan["main_base"]
            remote = dict(line.split()[::-1] for line in git("ls-remote", "--heads", "origin", "dev", "main").splitlines())
            assert remote == {"refs/heads/dev": plan["dev_base"], "refs/heads/main": plan["main_base"]}
            for flags in (("--all",), ("--push", "--all")):
                assert git("remote", "get-url", *flags, "origin") == plan["origin_url"]
            # The managed checkpoint must leave a clean tree and an unblocked helper.
            import importlib.util
            spec = importlib.util.spec_from_file_location("modern_hosted_git_plan", ROOT / ".aide/scripts/aide_lite.py")
            lite = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = lite
            spec.loader.exec_module(lite)
            helper = lite.make_git_helper_plan(ROOT, "plan", dry_run=True)
            record["helper_plan"] = helper
            save()
            assert helper["status"] != "blocked" and not helper["blockers"]
            pins = json.loads((EVIDENCE / "hosted-inputs.json").read_bytes())
            assert sha(EVIDENCE / "hosted-inputs.json") == plan["package_inputs_sha256"]
            assert all(sha(ROOT / name) == value for name, value in pins["files"].items())
            build = json.loads((EVIDENCE / "revised-build-qualified.json").read_bytes())
            assert build["state"] == "PASS_REVISED_BUILD_AND_COMPLETE_DELTA_ONLY"
            assert build["scratch_absent"] and build["reservation_released"]
            assert all(workspace.content_digest(Path(build["retained"]) / name) == value
                       for name, value in build["collected_manifest"].items())
            reuse = json.loads((EVIDENCE / "revised-behavior-reuse-review.json").read_bytes())
            assert reuse["decision"] == "ACCEPT" and not reuse["required_fixes"]
            assert all(sha(ROOT / name) == value for name, value in plan["stable_assets"].items())
            repo = api("repos/Julesc013/aide")
            assert repo["visibility"] == "public" and not repo["private"] and not repo["archived"] and not repo["disabled"]
            assert repo["permissions"]["push"]
            permissions = api("repos/Julesc013/aide/actions/permissions")
            assert permissions["enabled"] and permissions["allowed_actions"] == "all"
            assert not git("ls-remote", "--heads", "origin", plan["task_branch"]), "reconcile existing branch/run; never blindly push again"
            record.update(state="push_intent", expected_remote_ref="refs/heads/" + plan["task_branch"])
            save()
            git("push", "--no-follow-tags", "origin", plan["source_commit"] + ":refs/heads/" + plan["task_branch"])
            assert git("ls-remote", "--heads", "origin", plan["task_branch"]).split() == [plan["source_commit"], record["expected_remote_ref"]]
            record.update(state="pushed_waiting_for_run")
            save()
        run_id = None
        previous = None
        while time.monotonic() < deadline:
            if run_id is None:
                listing = api("repos/Julesc013/aide/actions/runs?branch=" + plan["task_branch"] + "&event=push&per_page=10")
                matches = [r for r in listing["workflow_runs"] if r["head_sha"] == plan["source_commit"] and r["path"] == ".github/workflows/lite-modern-lifecycle.yml"]
                assert len(matches) <= 1, "multiple matching runs require reconciliation"
                if matches:
                    run_id = matches[0]["id"]
                    record.update(run_id=run_id, run_url=matches[0]["html_url"])
            if run_id is not None:
                observed = api(f"repos/Julesc013/aide/actions/runs/{run_id}")
                assert observed["head_sha"] == plan["source_commit"] and observed["run_attempt"] == 1
                assert observed["event"] == "push" and observed["head_branch"] == plan["task_branch"]
                state = (observed["status"], observed["conclusion"])
                record.update(state="observing", observed_run=observed)
                save()
                if state != previous:
                    print(json.dumps({"run_id": run_id, "status": state[0], "conclusion": state[1]}), flush=True)
                    previous = state
                if observed["status"] == "completed":
                    break
            time.sleep(min(15, max(0, deadline - time.monotonic())))
        else:
            record.update(state="terminal_observer_deadline", redispatched=False)
            save()
            raise TimeoutError("one retained observer deadline; inspect existing run before any new effect")
        jobs = api(f"repos/Julesc013/aide/actions/runs/{run_id}/attempts/1/jobs?per_page=10")
        assert jobs["total_count"] == len(jobs["jobs"]) == 3
        expected_jobs = {profile + " actual archive qualification" for profile in plan["profiles"]}
        assert {j["name"] for j in jobs["jobs"]} == expected_jobs
        assert all(j["run_id"] == run_id and j["head_sha"] == plan["source_commit"] and j["status"] == "completed" for j in jobs["jobs"])
        record["jobs"] = jobs["jobs"]
        save()
        raw_zip = run(["gh", "api", "--hostname", "github.com", f"repos/Julesc013/aide/actions/runs/{run_id}/attempts/1/logs"], timeout=120)
        bundles = {}
        with zipfile.ZipFile(io.BytesIO(raw_zip)) as archive:
            assert len(archive.infolist()) <= 4096
            assert sum(info.file_size for info in archive.infolist()) <= 64 * 1024 * 1024
            for info in archive.infolist():
                remaining()
                if info.is_dir():
                    continue
                text = archive.read(info).decode("utf-8", errors="replace")
                rows = re.findall(r"AIDE_RECEIPT_V1 (\d+)/(\d+) ([0-9a-f]{64}) ([A-Za-z0-9+/=]+)", text)
                if not rows:
                    continue
                assert len(rows) == int(rows[0][1]) and [int(r[0]) for r in rows] == list(range(1, len(rows) + 1))
                assert all(r[1:3] == rows[0][1:3] for r in rows)
                packed = base64.b64decode("".join(r[3] for r in rows), validate=True)
                digest = hashlib.sha256(packed).hexdigest()
                assert len(packed) <= 2 * 1024 * 1024 and digest == rows[0][2]
                if digest in bundles:
                    continue
                with gzip.GzipFile(fileobj=io.BytesIO(packed)) as compressed:
                    body = compressed.read(12 * 1024 * 1024 + 1)
                assert len(body) <= 12 * 1024 * 1024
                remaining()
                decoded = json.loads(body)
                assert 1 <= len(decoded) <= 512
                files = {}
                for name, encoded in decoded.items():
                    assert re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", name)
                    files[name] = base64.b64decode(encoded, validate=True)
                assert sum(len(raw) for raw in files.values()) <= 8 * 1024 * 1024
                index = json.loads(files["receipt-index.json"])
                assert set(index) == set(files) - {"receipt-index.json"}
                for name, identity in index.items():
                    assert {"bytes": len(files[name]), "sha256": hashlib.sha256(files[name]).hexdigest()} == identity
                data = json.loads(files["release-result.json"])
                assert data["source_commit"] == plan["source_commit"]
                profile = {"aide-lite-local-windows-server": "windows-2025-x64",
                           "aide-lite-local-linux": "ubuntu-24.04-x64",
                           "aide-lite-local-macos": "macos-15-arm64"}[data["profile_id"]]
                nested = json.loads(files.get("nested-receipt-map.json", b"{}"))
                for name, item in nested.items():
                    assert not name.startswith("/") and ".." not in Path(name).parts
                    assert hashlib.sha256(files[item["transport_member"]]).hexdigest() == item["sha256"]
                destination = logs / profile
                destination.mkdir()
                for name, raw in files.items():
                    remaining()
                    with byte_lock:
                        assert retained_bytes + len(raw) <= 64 * 1024 * 1024
                        retained_bytes += len(raw)
                    with (destination / name).open("xb") as stream:
                        stream.write(raw)
                bundles[digest] = {"profile": profile, "data": data, "index": index,
                                   "receipt_index_sha256": hashlib.sha256(files["receipt-index.json"]).hexdigest()}
        profiles = {b["profile"]: b for b in bundles.values()}
        assert set(profiles) == set(plan["profiles"]) and len(bundles) == 3
        final_run = api(f"repos/Julesc013/aide/actions/runs/{run_id}")
        assert final_run["id"] == run_id and final_run["head_sha"] == plan["source_commit"]
        assert final_run["run_attempt"] == 1 and final_run["status"] == "completed"
        assert final_run["head_branch"] == plan["task_branch"] and final_run["event"] == "push"
        record["final_run_identity"] = final_run
        summary = {"run_id": run_id, "run_url": record["run_url"], "source_commit": plan["source_commit"],
                   "workflow_conclusion": record["observed_run"]["conclusion"], "profiles": {},
                   "new_os_support_claimed": False, "whole_model_usage": "unknown"}
        for profile, bundle in profiles.items():
            data = bundle["data"]
            passed = (data["status"] == "PASS" and data["fixture_retired"]
                      and data.get("input_sha256") == plan["package_inputs_sha256"]
                      and len(data.get("forms", [])) == 49
                      and len(data.get("unqualified_cli_forms", [])) == 7)
            summary["profiles"][profile] = {"status": data["status"], "qualification_pass": passed,
                "environment": data.get("environment"), "declared_environment": data.get("declared_environment"),
                "forms": data.get("forms", []), "cases": data.get("cases", []),
                "fixture_retired": data["fixture_retired"],
                "receipt_index_sha256": bundle["receipt_index_sha256"],
                "error": data.get("error"), "error_type": data.get("error_type")}
        summary["qualification_pass"] = all(p["qualification_pass"] for p in summary["profiles"].values())
        remaining()
        summary_bytes = (json.dumps(summary, indent=2) + "\n").encode()
        assert len(summary_bytes) <= 2 * 1024 * 1024
        (EVIDENCE / "hosted-observed.json").write_bytes(summary_bytes)
        record.update(state="observed_terminal", summary_sha256=sha(EVIDENCE / "hosted-observed.json"))
        save()
        print(json.dumps({"state": record["state"], "run_id": run_id,
                         "qualification_pass": summary["qualification_pass"],
                         "profiles": {p: b["qualification_pass"] for p, b in summary["profiles"].items()}}), flush=True)
    except BaseException as error:
        record.update(state="stopped", error_type=type(error).__name__, error=str(error), redispatched=False)
        save()
        raise


if __name__ == "__main__":
    main()
