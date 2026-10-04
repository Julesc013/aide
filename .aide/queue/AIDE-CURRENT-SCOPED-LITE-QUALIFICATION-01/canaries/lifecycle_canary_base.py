"""Disposable Windows lifecycle canary for one exact local AIDE Lite ZIP."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import traceback
from pathlib import Path


sys.dont_write_bytecode = True
PREP = Path(__file__).resolve().parent
ZIP = Path(r"D:\Projects\AIDE\aide\.aide\release\dist\aide-lite-pack-v0.zip")
ZIP_SHA = "8c4fbef71470954c64dbd09e181384a3fbff0ec997a799ef197f0f6cce1e07f6"
HELPER = Path(r"D:\Projects\AIDE\_review_scratch\removal-rollback-combined-consumer-prep\canary.py")
HELPER_SHA = "3f3140807520b1481181c34e95e06273e2774698cf2d384e42b5b6214f58a181"
MANAGED = ".aide/prompts/compact-task.md"


def load_pinned_helper():
    if not HELPER.is_file():
        raise ValueError("external extraction/recorder helper is absent")
    digest = hashlib.sha256()
    with HELPER.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    if digest.hexdigest() != HELPER_SHA:
        raise ValueError("external helper identity differs from reviewed preparation")
    spec = importlib.util.spec_from_file_location("aide_pinned_lifecycle_helper", HELPER)
    if spec is None or spec.loader is None:
        raise ValueError("external helper cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def require_status(output: str, expected: str, helper) -> str:
    observed = helper.field(output, "status")
    if observed != expected:
        raise AssertionError(f"expected {expected}, got {observed}")
    return observed


def require_json_status(output: str, expected: str) -> dict[str, object]:
    record = json.loads(output)
    if record.get("status") != expected:
        raise AssertionError(f"expected {expected}, got {record.get('status')}")
    return record


def save_api(out: Path, label: str, result: dict[str, object], helper) -> dict[str, object]:
    path = out / f"{label}.json"
    path.write_text(json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"label": label, "path": str(path), "sha256": helper.file_sha(path), "status": result["status"]}


def recorder_with_long_import_timeout(helper):
    """Keep the pinned recorder's log contract; allow this full pack time to apply."""
    class Recorder(helper.Recorder):
        def run(self, label: str, script: Path, root: Path, *parts: str,
                exits: tuple[int, ...] = (0,), offline_text: bool = False) -> subprocess.CompletedProcess[str]:
            argv = [sys.executable, "-I", "-B", str(script), "--repo-root", str(root), *parts]
            log_path = self.out / f"{label}.json"
            try:
                result = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=900)
            except subprocess.TimeoutExpired as exc:
                log_path.write_text(json.dumps({"argv": argv, "timeout_seconds": 900,
                    "failure": str(exc)}, sort_keys=True, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                self.commands.append({"label": label, "path": str(log_path),
                    "sha256": helper.file_sha(log_path), "exit_code": None})
                raise
            record = {"argv": argv, "exit_code": result.returncode,
                "stdout": result.stdout, "stderr": result.stderr, "timeout_seconds": 900}
            log_path.write_text(json.dumps(record, sort_keys=True, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            self.commands.append({"label": label, "path": str(log_path),
                "sha256": helper.file_sha(log_path), "exit_code": result.returncode})
            if result.returncode not in exits:
                raise AssertionError(f"{label} exit {result.returncode}; see {log_path}")
            if offline_text and "network_calls: none" not in result.stdout:
                raise AssertionError(f"{label} did not declare offline execution")
            return result
    return Recorder


def repair_case(out: Path, pack: Path, module, rec, h) -> dict[str, object]:
    target = out / "fresh-repair"
    h.install(rec, "repair-install", pack, target)
    managed = target / MANAGED
    expected = managed.read_bytes()
    receipt = target / module.PORTABLE_IMPORT_RECEIPT_PATH
    receipt_before = receipt.read_bytes()
    managed.unlink()
    base = ("repair-owned-file", "--pack", str(pack), "--target", str(target), "--path", MANAGED)
    preview = rec.pack("repair-preview", pack, *base, "--dry-run", offline_text=True)
    require_status(preview.stdout, "PLANNED", h)
    digest = h.field(preview.stdout, "plan_digest")
    if re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise AssertionError("repair preview lacks exact digest")
    before = h.tree_hashes(target)
    wrong = rec.pack("repair-wrong-plan", pack, *base, "--expect-plan", "0" * 64, exits=(3,), offline_text=True)
    require_status(wrong.stdout, "STALE_PLAN", h)
    if h.tree_hashes(target) != before:
        raise AssertionError("wrong repair plan changed target")
    rival = b"# Project rival appeared after repair preview.\n"
    managed.write_bytes(rival)
    rival_state = h.tree_hashes(target)
    refused = rec.pack("repair-rival-refusal", pack, *base, "--expect-plan", digest, exits=(2,), offline_text=True)
    require_status(refused.stdout, "CONFLICT", h)
    if h.tree_hashes(target) != rival_state or managed.read_bytes() != rival:
        raise AssertionError("repair clobbered rival leaf")
    managed.unlink()
    retry = rec.pack("repair-repreview", pack, *base, "--dry-run", offline_text=True)
    require_status(retry.stdout, "PLANNED", h)
    applied = rec.pack("repair-apply", pack, *base, "--expect-plan", h.field(retry.stdout, "plan_digest"), offline_text=True)
    require_status(applied.stdout, "APPLIED", h)
    if managed.read_bytes() != expected or receipt.read_bytes() != receipt_before or (target / module.PORTABLE_REPAIR_INTENT_PATH).exists():
        raise AssertionError("exact repair did not restore owned bytes while retaining receipt")

    restart_target = out / "fresh-repair-restart"
    h.install(rec, "repair-restart-install", pack, restart_target)
    restart_file = restart_target / MANAGED
    restart_expected = restart_file.read_bytes()
    restart_file.unlink()
    restart_preview = module.apply_portable_owned_repair(pack, restart_target, MANAGED, dry_run=True)
    if restart_preview["status"] != "PLANNED":
        raise AssertionError("restart fixture lacks repair preview")
    interrupted = module.apply_portable_owned_repair(pack, restart_target, MANAGED,
        expected_plan_digest=restart_preview["plan_digest"], fail_after_write=True)
    api_evidence = save_api(out, "repair-post-write-interruption", interrupted, h)
    intent = restart_target / module.PORTABLE_REPAIR_INTENT_PATH
    if interrupted["status"] != "INTERRUPTED" or not intent.is_file():
        raise AssertionError("repair interruption did not retain intent")
    pending_state = h.tree_hashes(restart_target)
    restart_base = ("repair-owned-file", "--pack", str(pack), "--target", str(restart_target), "--path", MANAGED)
    blocked = rec.pack("repair-restart-preview-refusal", pack, *restart_base, "--dry-run", exits=(3,), offline_text=True)
    require_status(blocked.stdout, "RECOVERY_REQUIRED", h)
    if h.tree_hashes(restart_target) != pending_state:
        raise AssertionError("pending repair preview changed target")
    resumed = rec.pack("repair-restart-resume", pack, *restart_base,
        "--expect-plan", restart_preview["plan_digest"], offline_text=True)
    require_status(resumed.stdout, "RECOVERED", h)
    if restart_file.read_bytes() != restart_expected or intent.exists():
        raise AssertionError("repair restart did not reconcile exact postimage")
    return {"repair_applied": True, "rival_preserved": True, "repair_restart": "RECOVERED", "api_interruption_evidence": api_evidence}


def rollback_case(out: Path, pack: Path, module, rec, h) -> dict[str, object]:
    v2 = out / "synthetic-rollback-v2"
    fixture = h.make_disposable_v2_fixture(pack, v2, module)
    target = out / "rollback-brownfield"
    target.mkdir()
    authored = b"# Project-authored rollback guidance\r\n"
    data = b"Project-owned bytes\r\n"
    (target / "AGENTS.md").write_bytes(authored)
    (target / "project-data.txt").write_bytes(data)
    h.install(rec, "rollback-v1-install", pack, target)
    v1_bytes = (target / MANAGED).read_bytes()
    h.update(rec, "rollback-v2-update", v2, pack, target)
    if (target / MANAGED).read_bytes() == v1_bytes:
        raise AssertionError("synthetic V2 did not change rollback payload")
    plan = h.rollback_plan(rec, "rollback-preview", pack, v2, pack, target)
    before = h.tree_hashes(target)
    base = ("rollback-pack", "--current-pack", str(v2), "--previous-pack", str(pack), "--target", str(target))
    refused = rec.pack("rollback-wrong-plan", pack, *base, "--expect-plan", "0" * 64, "--json", exits=(3,))
    require_json_status(refused.stdout, "STALE_PLAN")
    if h.tree_hashes(target) != before:
        raise AssertionError("wrong rollback plan changed target")
    applied = rec.installed("rollback-apply", target, *base, "--expect-plan", plan["plan_digest"], "--json")
    require_json_status(applied.stdout, "ROLLED_BACK")
    if (target / MANAGED).read_bytes() != v1_bytes or (target / "project-data.txt").read_bytes() != data:
        raise AssertionError("rollback changed owned predecessor or project data")
    if not (target / "AGENTS.md").read_bytes().startswith(authored):
        raise AssertionError("rollback changed authored AGENTS prefix")
    if module.load_portable_import_receipt(target)["pack"] != module.import_pack_identity(pack):
        raise AssertionError("rollback receipt does not identify exact predecessor")
    return {"rollback_status": "ROLLED_BACK", "synthetic_v2": fixture}


def removal_case(out: Path, pack: Path, module, rec, h) -> dict[str, object]:
    fresh = out / "fresh-removal"
    h.install(rec, "fresh-removal-install", pack, fresh)
    managed = set(module.load_portable_import_receipt(fresh)["managed"])
    plan = h.plan_removal(rec, "fresh-removal-preview", fresh)
    if plan["status"] != "PLANNED" or set(plan["candidate_targets"]) != managed:
        raise AssertionError("fresh removal did not cover exact receipt-owned targets")
    before = h.tree_hashes(fresh)
    wrong = rec.installed("fresh-removal-wrong-plan", fresh, "apply-removal", "--target", str(fresh),
        "--expect-plan", "0" * 64, "--json", exits=(3,))
    require_json_status(wrong.stdout, "STALE_PLAN")
    if h.tree_hashes(fresh) != before:
        raise AssertionError("wrong removal plan changed target")
    removed = rec.installed("fresh-removal-apply", fresh, "apply-removal", "--target", str(fresh),
        "--expect-plan", plan["plan_digest"], "--json")
    require_json_status(removed.stdout, "DETACHED")
    h.assert_detached(fresh, managed, module)

    brown = out / "brown-removal"
    brown.mkdir()
    prefix = b"# Authored project guidance\r\nKeep this preface.\r\n"
    tail = b"\r\n# Authored project tail\r\n"
    data = b"Do not remove project data.\r\n"
    (brown / "AGENTS.md").write_bytes(prefix)
    (brown / "project-data.txt").write_bytes(data)
    h.install(rec, "brown-removal-install", pack, brown)
    agents = brown / "AGENTS.md"
    agents.write_bytes(agents.read_bytes() + tail)
    brown_managed = set(module.load_portable_import_receipt(brown)["managed"])
    expected_agents = module.portable_agents_section_postimage(agents.read_bytes(),
        module.load_portable_import_receipt(brown)["managed"]["AGENTS.md"]["installed_digest"])
    if expected_agents is None or not expected_agents.startswith(prefix) or not expected_agents.endswith(tail):
        raise AssertionError("brownfield managed-section fixture is invalid")
    brown_plan = h.plan_removal(rec, "brown-removal-preview", brown)
    if brown_plan["status"] != "PLANNED" or set(brown_plan["candidate_targets"]) != brown_managed:
        raise AssertionError("brownfield plan did not cover exact receipt-owned targets")
    brown_result = rec.installed("brown-removal-apply", brown, "apply-removal", "--target", str(brown),
        "--expect-plan", brown_plan["plan_digest"], "--json")
    require_json_status(brown_result.stdout, "DETACHED")
    h.assert_detached(brown, brown_managed, module,
        unknown={"project-data.txt": h.sha(data)}, authored_agents=expected_agents)
    if (brown / "project-data.txt").read_bytes() != data:
        raise AssertionError("brownfield removal changed project data")

    changed = out / "brown-changed-removal"
    changed.mkdir()
    (changed / "AGENTS.md").write_bytes(prefix)
    h.install(rec, "brown-changed-install", pack, changed)
    edited = b"# Project edit after AIDE installation.\n"
    (changed / MANAGED).write_bytes(edited)
    receipt = changed / module.PORTABLE_IMPORT_RECEIPT_PATH
    receipt_before = receipt.read_bytes()
    changed_plan = h.plan_removal(rec, "brown-changed-plan", changed)
    if changed_plan["status"] != "PRESERVATION_REQUIRED" or MANAGED not in changed_plan["preserved_recorded_targets"]:
        raise AssertionError("changed brownfield file was not classified for preservation")
    partial = rec.installed("brown-changed-apply", changed, "apply-removal", "--target", str(changed),
        "--expect-plan", changed_plan["plan_digest"], "--json", exits=(2,))
    require_json_status(partial.stdout, "PARTIAL_REMOVAL")
    if (changed / MANAGED).read_bytes() != edited or receipt.read_bytes() != receipt_before:
        raise AssertionError("partial removal changed project edit or receipt")
    if not (changed / module.PORTABLE_REMOVAL_RUNNER_PATH).is_file():
        raise AssertionError("partial removal lost recovery runner")
    return {"fresh_removal": "DETACHED", "brown_removal": "DETACHED", "changed_brown": "PARTIAL_REMOVAL"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path, help="New run-* child of this external scratch directory")
    args = parser.parse_args()
    if os.name != "nt":
        raise ValueError("Windows pinned-file lifecycle effects are required")
    h = load_pinned_helper()
    if not ZIP.is_file() or h.file_sha(ZIP) != ZIP_SHA:
        raise ValueError("frozen local ZIP identity mismatch")
    out = args.out.resolve()
    if out.parent != PREP or not out.name.startswith("run-") or out.exists():
        raise ValueError("output must be a new run-* child of this external scratch directory")
    out.mkdir()
    rec = recorder_with_long_import_timeout(h)(out)
    try:
        members = h.extract_zip(ZIP, out / "candidate")
        pack = out / "candidate" / h.PACK_NAME
        module = h.load_delivered(pack)
        required = ("apply_portable_owned_repair", "apply_portable_rollback", "apply_portable_removal")
        if not all(hasattr(module, name) for name in required):
            raise AssertionError("delivered pack lacks required lifecycle API")
        repairs = repair_case(out, pack, module, rec, h)
        rollback = rollback_case(out, pack, module, rec, h)
        removal = removal_case(out, pack, module, rec, h)
        if h.file_sha(ZIP) != ZIP_SHA or h.file_sha(HELPER) != HELPER_SHA:
            raise AssertionError("frozen ZIP or helper changed during run")
        summary = {"status": "PASS", "zip": str(ZIP), "zip_sha256": ZIP_SHA,
            "helper_sha256": HELPER_SHA, "script_sha256": h.file_sha(Path(__file__)),
            "manifest_source_commit_declaration": next((line.partition(": ")[2] for line in
                (pack / "manifest.yaml").read_text("utf-8").splitlines() if line.startswith("source_commit: ")), None),
            "member_count": len(members), "commands": rec.commands,
            "synthetic_successor_is_published": False, **repairs, **rollback, **removal}
        receipt = out / "summary.json"
        receipt.write_text(json.dumps(summary, sort_keys=True, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "PASS", "summary": str(receipt),
            "summary_sha256": h.file_sha(receipt), "command_count": len(rec.commands)}, sort_keys=True))
    except BaseException:
        (out / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
        (out / "commands.json").write_text(json.dumps(rec.commands, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
