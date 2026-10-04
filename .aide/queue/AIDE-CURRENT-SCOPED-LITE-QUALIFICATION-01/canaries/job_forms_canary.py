"""Exercise delivered Lite job commands against approved local execution state."""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from consumer_canary_base import extract_archive, verify_pack


ROOT = Path(__file__).resolve().parents[4]
CONFIG = Path(__file__).with_name("legacy-config-template.json")
APPROVED_PARENT = Path(r"D:\Projects\AIDE\.aide.local\execution")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def invoke(cli, payload, label, *args, stdin=None, exits=(0,)):
    command = [sys.executable, "-I", "-B", str(cli), "--repo-root", str(payload), "job", *args]
    process = subprocess.run(command, cwd=ROOT, input=stdin, capture_output=True,
                             text=stdin is None, timeout=120)
    if process.returncode not in exits:
        raise AssertionError(f"{label} exited {process.returncode}: {process.stderr[-500:]!r}")
    stdout = process.stdout if isinstance(process.stdout, bytes) else process.stdout.encode()
    proof = Path(os.environ["AIDE_JOB_OUTPUT"]) / "command_outputs"
    proof.mkdir(exist_ok=True)
    stderr = process.stderr.decode(errors="replace") if isinstance(process.stderr, bytes) else process.stderr
    (proof / (label + ".json")).write_text(json.dumps({
        "argv": command, "exit_code": process.returncode,
        "stdout": stdout.decode(errors="replace"), "stderr": stderr,
    }, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    result = json.loads(stdout)
    return result, {"label": label, "exit_code": process.returncode,
                    "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
                    "status": result.get("status", result.get("result", ""))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True)
    parser.add_argument("--zip-sha256", required=True)
    parser.add_argument("--cli-sha256", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    archive = Path(args.zip).resolve()
    job_output = os.environ.get("AIDE_JOB_OUTPUT")
    output = (Path(job_output) / "summary.json" if job_output else Path(args.out)).resolve()
    if sha(archive) != args.zip_sha256:
        raise AssertionError("candidate ZIP digest changed")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    if {key: Path(value) for key, value in config["roots"].items()} != {
        "scratch": APPROVED_PARENT / "scratch",
        "retained": APPROVED_PARENT / "retained",
        "control": APPROVED_PARENT / "control",
    }:
        raise AssertionError("approved D roots changed")
    if ROOT.as_posix().lower() not in {Path(value).as_posix().lower() for value in config["working_roots"]}:
        raise AssertionError("primary working root not approved")
    if git("status", "--porcelain=v1"):
        raise AssertionError("source worktree must be clean")
    job_scratch = os.environ.get("AIDE_JOB_TMP")
    scratch = Path(job_scratch).resolve(strict=True) if job_scratch else Path(config["roots"]["scratch"])
    if job_scratch and not scratch.is_relative_to(Path(config["roots"]["scratch"]).resolve(strict=True)):
        raise AssertionError("job scratch escaped approved root")
    records = []
    with tempfile.TemporaryDirectory(prefix="lite-job-forms-", dir=scratch) as temporary:
        temp = Path(temporary)
        asset_root = temp / "asset"
        checks = extract_archive(archive, asset_root, "zip")
        pack = asset_root / "aide-lite-pack-v0"
        verify_pack(pack, checks)
        payload = pack / "files"
        cli = payload / ".aide/scripts/aide_lite.py"
        if sha(cli) != args.cli_sha256:
            raise AssertionError("delivered CLI digest changed")

        fixture = temp / "consumer"
        work = fixture / "project"
        work.mkdir(parents=True)
        (work / ".gitignore").write_text(".aide.local/\n", encoding="utf-8", newline="\n")
        source_script = work / "probe.py"
        source_script.write_text("print('AIDE_LITE_JOB_FORM_PROBE_PASS')\n", encoding="utf-8", newline="\n")
        for command in (("init",), ("config", "user.name", "AIDE Fixture"),
                        ("config", "user.email", "aide-fixture@example.invalid"),
                        ("add", ".gitignore", "probe.py"), ("commit", "-m", "fixture: probe")):
            subprocess.run(["git", *command], cwd=work, check=True, capture_output=True, timeout=15)
        roots = {key: str(fixture / key) for key in ("scratch", "retained", "control")}
        selection = fixture / "selection.json"
        selection.write_text(json.dumps({"schema": config["schema"], "roots": roots,
                                         "working_roots": [str(work)], "limits": config["limits"],
                                         "volume_ids": config["volume_ids"]}, sort_keys=True, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
        local_config = work / ".aide.local/execution.json"
        setup_fresh, record = invoke(cli, payload, "job-setup-fresh", "setup", "--config", str(local_config),
                                     "--selection", str(selection), "--approved-parent", str(fixture))
        records.append(record)
        if setup_fresh.get("result") != "CONFIGURED" or setup_fresh.get("writes") is not True:
            raise AssertionError("fresh consumer setup was not created")

        setup, record = invoke(cli, payload, "job-setup-existing", "setup", "--config", str(local_config),
                               "--selection", str(selection), "--approved-parent", str(fixture))
        records.append(record)
        if setup.get("result") != "ALREADY_CONFIGURED" or setup.get("writes") is not False:
            raise AssertionError("existing approved setup was not idempotent")

        probe = work / ".aide.local/current-job-form-probe.json"
        job = {
            "schema": "aide.maintainer-job.v1", "owner": "AIDE campaign controller",
            "workunit": "AIDE-STABLE-LITE-RELEASE-EFFECT-01", "adapter": "python",
            "cwd": str(work), "argv": [sys.executable, "probe.py"],
            "source_commit": subprocess.check_output(["git", "-C", str(work), "rev-parse", "HEAD"], text=True).strip(),
            "source_tree": subprocess.check_output(["git", "-C", str(work), "rev-parse", "HEAD^{tree}"], text=True).strip(),
            "inputs": {"probe.py": sha(source_script)},
            "executable_sha256": sha(Path(sys.executable)), "canonical_outputs": {},
        }
        probe.write_text(json.dumps(job, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
        inspected, record = invoke(cli, payload, "job-inspect", "inspect", "--config", str(local_config),
                                   "--manifest", str(probe))
        records.append(record)
        if inspected.get("writes") is not False:
            raise AssertionError("job inspect wrote state")
        boundary = inspected.get("execution_boundary", {})
        if (boundary.get("worker_write_placement") != "not_enforced_by_Windows_Job"
                or boundary.get("configuration_only") is not True
                or boundary.get("controls_outer_session") is not False
                or boundary.get("provides_hard_filesystem_quota") is not False):
            raise AssertionError("delivered legacy inspection misrepresented placement")

        run, record = invoke(cli, payload, "job-run", "run", "--config", str(local_config),
                             "--manifest", str(probe))
        records.append(record)
        if run.get("status") != "PASS" or run.get("exit_code") != 0:
            raise AssertionError("delivered job run did not pass")
        if run.get("model_requests_started_by_observer") != 0:
            raise AssertionError("observer started model request")

        full, record = invoke(cli, payload, "job-run-full", "run", "--config", str(local_config),
                              "--manifest", str(probe), "--full")
        records.append(record)
        if full.get("job_id") is None or full.get("result", {}).get("exit_code") != 0:
            raise AssertionError("delivered full job result failed")

        waited, record = invoke(cli, payload, "job-wait", "wait", "--config", str(local_config),
                                "--job-id", run["job_id"], "--manifest-digest", run["manifest_digest"],
                                "--timeout-seconds", "0")
        records.append(record)
        if waited.get("status") != "PASS" or waited.get("receipt_sha256") != run.get("receipt_sha256"):
            raise AssertionError("delivered wait lost exact terminal receipt")

        waited_default, record = invoke(cli, payload, "job-wait-default", "wait", "--config", str(local_config),
                                        "--job-id", run["job_id"], "--manifest-digest", run["manifest_digest"])
        records.append(record)
        if waited_default.get("status") != "PASS":
            raise AssertionError("delivered default wait lost terminal receipt")

        recovered, record = invoke(cli, payload, "job-recover", "recover", "--config", str(local_config))
        records.append(record)
        if recovered.get("result") == "REFUSED":
            raise AssertionError("delivered recovery refused quiescent control")

        stream = temp / "synthetic-codex.jsonl"
        stream.write_text("\n".join(json.dumps(item) for item in (
            {"type": "thread.started", "thread_id": "00000000-0000-0000-0000-000000000001"},
            {"type": "turn.started"},
            {"type": "turn.completed", "usage": {"input_tokens": 20, "cached_input_tokens": 5,
                                                  "output_tokens": 7, "reasoning_output_tokens": 2}},
        )) + "\n", encoding="utf-8", newline="\n")
        usage, record = invoke(cli, payload, "job-usage", "usage", "--stream", str(stream),
                               "--stream", str(stream))
        records.append(record)
        if usage.get("status") != "COMPLETE" or usage.get("completed_turns") != 1:
            raise AssertionError("delivered usage importer did not deduplicate")
        if usage.get("duplicate_streams_excluded") != 1:
            raise AssertionError("duplicate stream was not excluded")

        child_stream = temp / "synthetic-child.jsonl"
        child_stream.write_text("\n".join(json.dumps(item) for item in (
            {"type": "thread.started", "thread_id": "00000000-0000-0000-0000-000000000002"},
            {"type": "turn.started"},
            {"type": "turn.completed", "usage": {"input_tokens": 6, "cached_input_tokens": 1,
                                                  "output_tokens": 2, "reasoning_output_tokens": 0}},
        )) + "\n", encoding="utf-8", newline="\n")
        attempts = [
            {"attempt_id": "parent-1", "role": "parent", "parent_attempt_id": None,
             "stream": stream.name, "stream_sha256": sha(stream)},
            {"attempt_id": "child-1", "role": "child", "parent_attempt_id": "parent-1",
             "stream": child_stream.name, "stream_sha256": sha(child_stream)},
            {"attempt_id": "review-1", "role": "review", "parent_attempt_id": "parent-1",
             "stream": None, "stream_sha256": None},
        ]
        roster = temp / "synthetic-attempt-roster.json"
        roster.write_text(json.dumps({"schema": "aide.codex-exec-attempt-roster.v1",
                                      "work_id": "delivered-consumer-1", "attempts": attempts}),
                          encoding="utf-8", newline="\n")
        attributed, record = invoke(cli, payload, "job-usage-attempt-set", "usage",
                                    "--attempt-set", str(roster), exits=(2,))
        records.append(record)
        if (attributed.get("status") != "PARTIAL" or attributed.get("attempt_count") != 3
                or attributed.get("supplied_known_usage_totals", {}).get("input_tokens") != 26
                or attributed.get("role_known_usage_totals", {}).get("parent", {}).get("input_tokens") != 20
                or attributed.get("role_known_usage_totals", {}).get("child", {}).get("input_tokens") != 6
                or attributed.get("work_usage_totals", {}).get("input_tokens") is not None
                or attributed.get("model_requests") != "unknown"
                or "attempt_stream_unavailable" not in attributed.get("coverage_gaps", [])
                or "synthetic-child.jsonl" in json.dumps(attributed)):
            raise AssertionError("delivered attempt attribution misstated usage or coverage")
        invalid = {"schema": "aide.codex-exec-attempt-roster.v1",
                   "work_id": "delivered-consumer-1",
                   "attempts": [attempts[0], {**attempts[1], "parent_attempt_id": ["parent-1"]}]}
        roster.write_text(json.dumps(invalid), encoding="utf-8", newline="\n")
        refused, record = invoke(cli, payload, "job-usage-invalid-parent", "usage",
                                 "--attempt-set", str(roster), exits=(1,))
        records.append(record)
        if refused.get("status") != "REFUSED":
            raise AssertionError("delivered malformed attempt roster was not refused")

        raw = json.dumps([{"type": "message", "role": "user", "content": [
            {"type": "text", "text": "private-canary-marker"}]}]).encode()
        context, record = invoke(cli, payload, "job-context", "context", stdin=raw)
        records.append(record)
        if context.get("status") != "COMPLETE" or b"private-canary-marker" in json.dumps(context).encode():
            raise AssertionError("context summary failed or echoed text")

        receipt = Path(run["receipt_ref"])
        data = json.loads(receipt.read_text(encoding="utf-8"))
        if sha(receipt) != run["receipt_sha256"] or data["phase"] != "retired":
            raise AssertionError("run receipt not retained and retired")
        if not data["scratch_absent"] or not data["reservation_released"]:
            raise AssertionError("managed run failed retirement")
        receipt_copy = output.with_suffix(".receipt.json")
        receipt_copy.write_bytes(receipt.read_bytes())
        summary = {
            "schema": "aide.lite-job-forms-canary.v1", "status": "PASS",
            "asset_sha256": args.zip_sha256, "delivered_cli_sha256": args.cli_sha256,
            "source_commit": job["source_commit"], "source_tree": job["source_tree"],
            "forms": records, "managed_job_id": run["job_id"],
            "managed_receipt_sha256": run["receipt_sha256"],
            "scratch_retired": True, "reservation_released": True,
            "consumer_kind": "fresh disposable Git project under approved D scratch",
            "limitations": ["synthetic consumer only; no arbitrary project rollout or live model turn"],
        }
    if temp.exists():
        raise AssertionError("disposable consumer was not retired")
    summary["temporary_consumer_retired"] = True
    output.write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "forms": len(records), "summary_sha256": sha(output),
                      "managed_job_id": summary["managed_job_id"]}, sort_keys=True))


if __name__ == "__main__":
    main()
