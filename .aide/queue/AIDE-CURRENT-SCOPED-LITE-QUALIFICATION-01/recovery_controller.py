"""Bounded recovery of the existing job; no replacement dispatch/allocation."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

TASK = Path(__file__).resolve().parent
REPO = TASK.parents[2]
CONFIG = REPO / ".aide.local/scoped-job-entry-01-execution.json"
EFFECT = TASK / "evidence/recovery-effect-46e91fbf.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def retain_observation_logs(owner, scratch, effect):
    """Same-volume evidence renames; every identity/hash is frozen first."""
    pending = []
    for item in effect["observation_log_retention"]:
        source, target = scratch / item["source"], scratch / item["target"]
        if (source.parent != scratch / "logs" or target.parent != scratch / "output"
                or source.exists() == target.exists()):
            raise RuntimeError("unexpected recovery evidence disposition")
        current = source if source.exists() else target
        info = owner.ordinary(current, directory=True)
        if [info.st_dev, info.st_ino] != item["identity"]:
            raise RuntimeError("observation log identity changed")
        if {p.name for p in current.iterdir()} != set(item["files"]):
            raise RuntimeError("unexpected observation evidence entry")
        for name, expected in item["files"].items():
            member = current / name
            value = owner.ordinary(member)
            if ([value.st_dev, value.st_ino] != expected["identity"]
                    or value.st_size != expected["bytes"] or sha(member) != expected["sha256"]):
                raise RuntimeError("observation evidence changed")
        if current == source:
            pending.append((source, target))
    output = owner.tree_usage(scratch / "output", maximum=effect["retained_limit_bytes"],
                              max_files=100000)
    pending_bytes = sum(sum(f["bytes"] for f in item["files"].values())
                        for item in effect["observation_log_retention"]
                        if (scratch / item["source"]).exists())
    if output + pending_bytes + effect["log_limit_bytes"] > effect["retained_limit_bytes"]:
        raise RuntimeError("recovery evidence does not fit original retention allowance")
    for source, target in pending:
        source.rename(target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    effect = json.loads(EFFECT.read_text(encoding="utf-8"))
    if sha(CONFIG) != effect["config_sha256"]:
        raise RuntimeError("recovery configuration changed")
    if (sha(TASK / "recover_fixture.py") != effect["helper_sha256"]
            or sha(Path(__file__)) != effect["controller_sha256"]):
        raise RuntimeError("recovery code changed")
    spec = importlib.util.spec_from_file_location("frozen_recovery_selection", REPO / "core/execution/scoped_host.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    owner, _ = module.prepare(CONFIG, REPO)
    cfg, roots, _ = owner.load_config(CONFIG)
    with owner.estate_lock(roots["control"]):
        active = roots["control"] / "active.json"
        if sha(active) != effect["active_raw_sha256"]:
            raise RuntimeError("recovery lease changed")
        record = owner.read_json(active)
        if record["job_id"] != effect["job_id"] or record["phase"] != "quiescent":
            raise RuntimeError("recovery owner changed")
        if not owner.WindowsJobHost().reconcile(record["job_id"])["quiescent"]:
            raise RuntimeError("original process remains active")
        scratch = owner.owned_scratch(record, roots)
        scratch_info = scratch.lstat()
        if [scratch_info.st_dev, scratch_info.st_ino] != effect["scratch_identity"]:
            raise RuntimeError("strong recovery scratch identity changed")
        if args.apply:
            retain_observation_logs(owner, scratch, effect)
        leaf = scratch / effect["owned_fixture"]
        selection = cfg["execution_host"]
        rules = {":root": "deny", ":minimal": "read", str(REPO): "read"}
        rules.update({path: "read" for path in selection["read_roots"]})
        rules.update({str(REPO / ".aide.local"): "deny", str(roots["control"]): "deny",
                      str(active): "read", str(scratch): "read"})
        # Reuse the original job's approved writable TMP. An exact private
        # leaf grant triggers SDK ACL setup on a directory Jules cannot open.
        rules[str(scratch / "tmp") if args.apply else str(leaf)] = "write" if args.apply else "read"
        profile = "aide_owned_fixture_" + ("apply_" if args.apply else "inspect_") + record["job_id"]
        inline = "{" + ",".join(json.dumps(k) + "=" + json.dumps(v) for k, v in rules.items()) + "}"
        argv = [selection["codex_executable"], "sandbox", "-P", profile,
                "-c", "permissions." + profile + ".filesystem=" + inline,
                "-c", "permissions." + profile + ".network.enabled=false", "--",
                sys.executable, "-B", str(TASK / "recover_fixture.py")]
        if args.apply:
            argv.append("--apply")
        logs = (scratch / effect["retirement_log"] if args.apply
                else scratch / "logs" / "fixture-custody-observation")
        environment = owner.sanitized_environment()
        environment.update(TEMP=str(scratch / "tmp"), TMP=str(scratch / "tmp"),
                           TMPDIR=str(scratch / "tmp"), PYTHONDONTWRITEBYTECODE="1")
        result = owner.WindowsJobHost().run(argv, cwd=REPO, input_bytes=b"", output_dir=logs,
                    job_id=record["job_id"], timeout=effect["timeout_seconds"],
                    output_limit=effect["log_limit_bytes"], memory_limit=effect["memory_limit"],
                    process_limit=4, environment=environment)
        if not result.get("quiescent"):
            raise RuntimeError("recovery helper did not become quiescent")
        print(json.dumps({"original_job_id": record["job_id"], "helper_result": result,
                          "logs": str(logs), "lease_unchanged": sha(active) == effect["active_raw_sha256"],
                          "new_workspace": False, "mode": "apply" if args.apply else "inspect"}, sort_keys=True))
        if result.get("exit_code") != 0:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
