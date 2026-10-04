"""Disposable delivered-artifact canary for frozen AIDE rollback and removal.

Prepared only: requires exact frozen ZIP/tar identities. All effects stay in a
new run-* directory directly beneath this script's external scratch directory.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path, PurePosixPath
from unittest import mock


PREP = Path(__file__).resolve().parent
PACK_NAME = "aide-lite-pack-v0"
MANAGED_REL = ".aide/prompts/compact-task.md"
RELEASE_MUTABLE = {"checksums.json", "manifest.yaml", "export-report.md"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_sha(value: str, label: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError(f"{label} must be an exact lowercase SHA256")
    return value


def safe_member(name: str) -> PurePosixPath:
    parts = name.split("/")
    rel = PurePosixPath(name)
    if (
        name.startswith("/")
        or "\\" in name
        or any(not part or part in {".", ".."} or part.endswith((" ", ".")) for part in parts)
        or any(any(ord(char) < 32 or char in '<>"|?*:' for char in part) for part in parts)
        or not rel.parts
        or rel.parts[0] != PACK_NAME
        or any(re.match(r"^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)", part, re.I) for part in parts)
    ):
        raise ValueError(f"unsafe archive member: {name}")
    return rel


def extract_zip(archive: Path, destination: Path) -> dict[str, str]:
    members: dict[str, str] = {}
    folded: set[str] = set()
    with zipfile.ZipFile(archive) as zipped:
        if zipped.testzip() is not None:
            raise ValueError(f"damaged ZIP: {archive}")
        for info in zipped.infolist():
            rel = safe_member(info.filename)
            mode = (info.external_attr >> 16) & 0o170000
            if info.is_dir() or mode not in {0, 0o100000}:
                raise ValueError(f"non-regular ZIP member: {info.filename}")
            if info.filename in members or info.filename.casefold() in folded:
                raise ValueError(f"duplicate ZIP member: {info.filename}")
            body = zipped.read(info)
            members[info.filename] = sha(body)
            folded.add(info.filename.casefold())
            target = destination.joinpath(*rel.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
    verify_pack(destination / PACK_NAME, members)
    return members


def extract_tar(archive: Path, destination: Path) -> dict[str, str]:
    members: dict[str, str] = {}
    folded: set[str] = set()
    with tarfile.open(archive, "r:gz") as tarred:
        for info in tarred.getmembers():
            rel = safe_member(info.name)
            if not info.isfile() or info.linkname:
                raise ValueError(f"non-regular tar member: {info.name}")
            if info.name in members or info.name.casefold() in folded:
                raise ValueError(f"duplicate tar member: {info.name}")
            source = tarred.extractfile(info)
            if source is None:
                raise ValueError(f"unreadable tar member: {info.name}")
            body = source.read()
            members[info.name] = sha(body)
            folded.add(info.name.casefold())
            target = destination.joinpath(*rel.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
    verify_pack(destination / PACK_NAME, members)
    return members


def verify_pack(pack: Path, archive_members: dict[str, str]) -> None:
    embedded = json.loads((pack / "checksums.json").read_text("utf-8"))["checksums"]
    payload = {name.removeprefix(PACK_NAME + "/"): value for name, value in archive_members.items()}
    if set(embedded) != set(payload) - RELEASE_MUTABLE:
        raise ValueError("pack checksum coverage mismatch")
    if any(payload[name] != value for name, value in embedded.items()):
        raise ValueError("pack payload checksum mismatch")


def verify_install_guides(pack: Path, release_guide: Path) -> dict[str, str]:
    """Check the two repaired generated guides against their stated contract."""
    pack_path = pack / "install.md"
    normalized_pack = " ".join(pack_path.read_text("utf-8").split())
    normalized_release = " ".join(release_guide.read_text("utf-8").split())
    required_pack = (
        "The preview's `apply_allowed: false` describes the read-only `plan-removal` command; the separate `apply-removal` command accepts its exact digest on Windows.",
        "A stale preview refuses before deletion.",
        "the command stops with `RECOVERY_REQUIRED`; earlier deletions may have occurred, and the intent remains.",
        "In an authored `AGENTS.md`, it removes only the managed section recorded by the receipt while preserving every outside byte.",
        "Changed or already absent recorded paths retain the runner and receipt as `PARTIAL_REMOVAL` (exit code 2).",
        "Keep the extracted pack available for recovery after full detach.",
    )
    required_release = (
        "`plan-removal` reports `apply_allowed: false` because that command is read-only; the separate `apply-removal` command accepts its exact digest on Windows.",
        "A stale preview refuses before deletion",
        "a change after removal begins returns `RECOVERY_REQUIRED` with the intent retained and earlier effects possible",
        "it removes only the receipt-owned managed section inside authored `AGENTS.md`, preserving every outside byte.",
        "Changed or already absent recorded paths remain partial: the runner and receipt stay and the command reports `PARTIAL_REMOVAL`.",
    )
    for phrase in required_pack:
        if phrase not in normalized_pack:
            raise AssertionError(f"pack install guide lacks repaired contract: {phrase}")
    for phrase in required_release:
        if phrase not in normalized_release:
            raise AssertionError(f"release install guide lacks repaired contract: {phrase}")
    return {"pack_install_sha256": file_sha(pack_path), "release_install_sha256": file_sha(release_guide)}


def load_delivered(pack: Path):
    script = pack / "files/.aide/scripts/aide_lite.py"
    spec = importlib.util.spec_from_file_location("aide_removal_delivered_canary", script)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load delivered script: {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def tree_hashes(root: Path) -> dict[str, str]:
    return {path.relative_to(root).as_posix(): file_sha(path) for path in sorted(root.rglob("*")) if path.is_file()}


class Recorder:
    def __init__(self, out: Path) -> None:
        self.out = out
        self.commands: list[dict[str, object]] = []

    def run(self, label: str, script: Path, root: Path, *parts: str, exits: tuple[int, ...] = (0,), offline_text: bool = False) -> subprocess.CompletedProcess[str]:
        argv = [sys.executable, "-I", "-B", str(script), "--repo-root", str(root), *parts]
        result = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
        log = {"argv": argv, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        path = self.out / f"{label}.json"
        path.write_text(json.dumps(log, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        self.commands.append({"label": label, "path": str(path), "sha256": file_sha(path), "exit_code": result.returncode})
        if result.returncode not in exits:
            raise AssertionError(f"{label} exit {result.returncode}; see {path}")
        if offline_text and "network_calls: none" not in result.stdout:
            raise AssertionError(f"{label} did not declare offline execution")
        return result

    def pack(self, label: str, pack: Path, *parts: str, exits: tuple[int, ...] = (0,), offline_text: bool = False) -> subprocess.CompletedProcess[str]:
        return self.run(label, pack / "files/.aide/scripts/aide_lite.py", pack, *parts, exits=exits, offline_text=offline_text)

    def installed(self, label: str, target: Path, *parts: str, exits: tuple[int, ...] = (0,), offline_text: bool = False) -> subprocess.CompletedProcess[str]:
        return self.run(label, target / ".aide/scripts/aide_lite.py", target, *parts, exits=exits, offline_text=offline_text)


def field(output: str, name: str) -> str:
    for line in output.splitlines():
        if line.startswith(name + ": "):
            return line.split(": ", 1)[1]
    raise AssertionError(f"missing {name}: {output[-500:]}")


def install(rec: Recorder, label: str, pack: Path, target: Path) -> None:
    argv = ("import-pack", "--pack", str(pack), "--target", str(target), "--mode", "safe")
    preview = rec.pack(label + "-preview", pack, *argv, "--dry-run", offline_text=True)
    if field(preview.stdout, "status") != "PLANNED":
        raise AssertionError(f"{label} did not produce a complete import plan")
    applied = rec.pack(label + "-apply", pack, *argv, "--expect-plan", field(preview.stdout, "plan_digest"), offline_text=True)
    if field(applied.stdout, "status") != "APPLIED":
        raise AssertionError(f"{label} import did not apply")


def plan_removal(rec: Recorder, label: str, target: Path) -> dict[str, object]:
    before = tree_hashes(target)
    result = rec.installed(label, target, "plan-removal", "--target", str(target), "--json", exits=(0, 2, 3))
    plan = json.loads(result.stdout)
    if plan.get("read_only") is not True or plan.get("apply_allowed") is not False or plan.get("network_calls") is not False:
        raise AssertionError(f"{label} planning flags are not conservative")
    if tree_hashes(target) != before:
        raise AssertionError(f"{label} planning changed the target")
    return plan


def assert_detached(target: Path, managed: set[str], module, unknown: dict[str, str] | None = None, *, authored_agents: bytes | None = None) -> None:
    for rel in managed:
        if rel == "AGENTS.md" and authored_agents is not None:
            if (target / rel).read_bytes() != authored_agents:
                raise AssertionError("authored AGENTS outside bytes changed during detach")
            continue
        if (target / rel).exists():
            raise AssertionError(f"managed target survived full detach: {rel}")
    for rel in (module.PORTABLE_IMPORT_RECEIPT_PATH, module.PORTABLE_REMOVAL_INTENT_PATH, module.PORTABLE_REMOVAL_RUNNER_PATH):
        if (target / rel).exists():
            raise AssertionError(f"removal state survived full detach: {rel}")
    for rel, expected in (unknown or {}).items():
        if file_sha(target / rel) != expected:
            raise AssertionError(f"unknown target-owned file changed: {rel}")


def make_disposable_v2_fixture(base_pack: Path, fixture: Path, module) -> dict[str, str]:
    """Derive one explicit update oracle from delivered bytes, not a release."""
    shutil.copytree(base_pack, fixture)
    payload = fixture / "files" / MANAGED_REL
    original = payload.read_bytes()
    changed = original + b"\n# Disposable v2 rollback oracle.\n"
    payload.write_bytes(changed)
    module.write_text(fixture / "checksums.json", module.stable_json_text(module.build_pack_checksums(fixture)))
    valid, problems = module.validate_pack_checksums(fixture)
    if not valid:
        raise AssertionError(f"disposable v2 checksum validation failed: {problems}")
    if module.import_pack_identity(base_pack) == module.import_pack_identity(fixture):
        raise AssertionError("disposable v2 has no distinct pack identity")
    return {"path": str(fixture), "changed_path": MANAGED_REL, "v1_payload_sha256": sha(original),
            "v2_payload_sha256": sha(changed), "v2_checksums_sha256": file_sha(fixture / "checksums.json")}


def update(rec: Recorder, label: str, current: Path, predecessor: Path, target: Path) -> None:
    argv = ("import-pack", "--pack", str(current), "--from-pack", str(predecessor), "--target", str(target), "--mode", "safe")
    preview = rec.pack(label + "-preview", current, *argv, "--dry-run", offline_text=True)
    if field(preview.stdout, "status") != "PLANNED":
        raise AssertionError(f"{label} did not produce a complete update plan")
    applied = rec.pack(label + "-apply", current, *argv, "--expect-plan", field(preview.stdout, "plan_digest"), offline_text=True)
    if field(applied.stdout, "status") != "APPLIED":
        raise AssertionError(f"{label} update did not apply")


def rollback_plan(rec: Recorder, label: str, runner: Path, current: Path, previous: Path, target: Path) -> dict[str, object]:
    before = tree_hashes(target)
    result = rec.pack(label, runner, "rollback-pack", "--current-pack", str(current), "--previous-pack", str(previous),
                      "--target", str(target), "--dry-run", "--json")
    plan = json.loads(result.stdout)
    if plan.get("status") != "PLANNED" or not re.fullmatch(r"[0-9a-f]{64}", str(plan.get("plan_digest", ""))):
        raise AssertionError(f"{label} did not produce an exact rollback plan")
    if tree_hashes(target) != before:
        raise AssertionError(f"{label} changed target during rollback preview")
    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-zip", required=True, type=Path)
    parser.add_argument("--candidate-tar", required=True, type=Path)
    parser.add_argument("--candidate-zip-sha256", required=True)
    parser.add_argument("--candidate-tar-sha256", required=True)
    parser.add_argument("--release-install-guide", required=True, type=Path)
    parser.add_argument("--release-install-guide-sha256", required=True)
    parser.add_argument("--candidate-source-commit", required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if os.name != "nt":
        raise ValueError("removal apply canary requires Windows pinned-file implementation")
    expected = {"zip": exact_sha(args.candidate_zip_sha256, "candidate ZIP"), "tar": exact_sha(args.candidate_tar_sha256, "candidate tar")}
    if not re.fullmatch(r"[0-9a-f]{40}", args.candidate_source_commit):
        raise ValueError("candidate source commit must be a full lowercase Git object ID")
    archives = {"zip": args.candidate_zip.resolve(strict=True), "tar": args.candidate_tar.resolve(strict=True)}
    for kind, archive in archives.items():
        if not archive.is_file() or file_sha(archive) != expected[kind]:
            raise ValueError(f"frozen {kind} archive identity mismatch")
    release_guide = args.release_install_guide.resolve(strict=True)
    guide_sha = exact_sha(args.release_install_guide_sha256, "release install guide")
    if not release_guide.is_file() or file_sha(release_guide) != guide_sha:
        raise ValueError("frozen release install guide identity mismatch")
    out = args.out.resolve()
    if out.parent != PREP or not out.name.startswith("run-") or out.exists():
        raise ValueError("output must be a new run-* child of this prep directory")
    out.mkdir()
    rec = Recorder(out)
    zip_members = extract_zip(archives["zip"], out / "candidate-zip")
    tar_members = extract_tar(archives["tar"], out / "candidate-tar")
    if zip_members != tar_members:
        raise AssertionError("candidate ZIP and tar members differ")
    zip_pack = out / "candidate-zip" / PACK_NAME
    tar_pack = out / "candidate-tar" / PACK_NAME
    manifest_lines = (zip_pack / "manifest.yaml").read_text("utf-8").splitlines()
    if (manifest_lines.count("source_commit: " + args.candidate_source_commit) != 1 or
            manifest_lines.count("source_dirty_state: false") != 1 or
            manifest_lines.count("pack_id: " + PACK_NAME) != 1):
        raise AssertionError("candidate source provenance mismatch")
    guide_checks = verify_install_guides(zip_pack, release_guide)
    if guide_checks["pack_install_sha256"] != file_sha(tar_pack / "install.md") or guide_checks["release_install_sha256"] != guide_sha:
        raise AssertionError("candidate install guide identity changed or differs by archive")
    module = load_delivered(zip_pack)
    if not all(hasattr(module, name) for name in ("apply_portable_removal", "apply_portable_rollback", "build_portable_rollback_plan")):
        raise AssertionError("delivered candidate lacks rollback or removal apply")

    # Fresh ZIP consumer: exact plan and complete detach of wholly generated guidance.
    fresh = out / "fresh-target"
    install(rec, "fresh", zip_pack, fresh)
    unknown_path = fresh / "unknown.txt"
    unknown_path.write_bytes(b"Target-owned data stays after AIDE detach.\n")
    unknown = {"unknown.txt": file_sha(unknown_path)}
    receipt = module.load_portable_import_receipt(fresh)
    managed = set(receipt["managed"])
    if "AGENTS.md" not in managed or module.PORTABLE_REMOVAL_RUNNER_PATH not in managed:
        raise AssertionError("fresh receipt lacks generated guidance or installed removal runner")
    doctor = rec.installed("fresh-installed-doctor", fresh, "doctor")
    if "status: PASS" not in doctor.stdout:
        raise AssertionError("fresh installed doctor did not pass")
    plan = plan_removal(rec, "fresh-removal-plan-json", fresh)
    if plan["status"] != "PLANNED" or set(plan["candidate_targets"]) != managed:
        raise AssertionError("fresh removal did not cover every managed target")
    text_plan = rec.installed("fresh-removal-plan-text", fresh, "plan-removal", "--target", str(fresh), offline_text=True)
    if field(text_plan.stdout, "plan_digest") != plan["plan_digest"]:
        raise AssertionError("fresh text and JSON removal plans differ")
    applied = rec.installed("fresh-apply-removal", fresh, "apply-removal", "--target", str(fresh), "--expect-plan", plan["plan_digest"], offline_text=True)
    if field(applied.stdout, "status") != "DETACHED" or field(applied.stdout, "receipt_retained") != "false":
        raise AssertionError("fresh full removal did not detach")
    assert_detached(fresh, managed, module, unknown)
    detached_plan = rec.pack("fresh-post-detach-plan-refusal", zip_pack, "plan-removal", "--target", str(fresh), "--json", exits=(3,))
    if json.loads(detached_plan.stdout)["status"] != "REFUSED":
        raise AssertionError("full detach still has an import receipt")

    # Brownfield tar consumer: detach only the exact managed section.
    brown = out / "brownfield-target"
    brown.mkdir()
    authored_prefix = b"# Authored project guidance\r\n\r\nPreserve this policy.\r\n"
    authored_suffix = b"\r\n# Project-owned closing note.\r\n"
    (brown / "AGENTS.md").write_bytes(authored_prefix)
    (brown / "unknown.txt").write_bytes(b"Project-owned file.\n")
    memory = brown / ".aide/memory/project-state.md"
    memory.parent.mkdir(parents=True)
    memory.write_bytes(b"# Project memory\n")
    authored = tree_hashes(brown)
    install(rec, "brown", tar_pack, brown)
    agents_before = (brown / "AGENTS.md").read_bytes()
    if not agents_before.startswith(authored_prefix):
        raise AssertionError("import changed authored AGENTS prefix")
    (brown / "AGENTS.md").write_bytes(agents_before + authored_suffix)
    agents_before = (brown / "AGENTS.md").read_bytes()
    receipt = module.load_portable_import_receipt(brown)
    brown_managed = set(receipt["managed"])
    begin = b"<!-- AIDE-PORTABLE:BEGIN section=aide-lite-pack-v0"
    end = b"<!-- AIDE-PORTABLE:END section=aide-lite-pack-v0 -->"
    if agents_before.count(begin) != 1 or agents_before.count(end) != 1:
        raise AssertionError("brownfield imported AGENTS block is not unique")
    block_start = agents_before.index(begin)
    block_end = agents_before.index(end, block_start) + len(end)
    if sha(agents_before[block_start:block_end]) != receipt["managed"]["AGENTS.md"]["installed_digest"]:
        raise AssertionError("brownfield imported AGENTS block differs from receipt")
    expected_agents = agents_before[:block_start] + agents_before[block_end:]
    if not expected_agents.startswith(authored_prefix) or not expected_agents.endswith(authored_suffix):
        raise AssertionError("brownfield expected outside bytes differ")
    brown_plan = plan_removal(rec, "brown-removal-plan", brown)
    if brown_plan["status"] != "PLANNED" or set(brown_plan["candidate_targets"]) != brown_managed:
        raise AssertionError("brownfield removal did not cover every managed target")
    brown_applied = rec.installed("brown-apply-removal", brown, "apply-removal", "--target", str(brown), "--expect-plan", brown_plan["plan_digest"], "--json")
    brown_result = json.loads(brown_applied.stdout)
    if brown_result["status"] != "DETACHED" or brown_result["receipt_retained"]:
        raise AssertionError("authored brownfield managed section did not detach")
    for rel in ("unknown.txt", ".aide/memory/project-state.md"):
        if file_sha(brown / rel) != authored[rel]:
            raise AssertionError(f"brownfield authored file changed: {rel}")
    assert_detached(brown, brown_managed, module, {rel: authored[rel] for rel in ("unknown.txt", ".aide/memory/project-state.md")}, authored_agents=expected_agents)
    brown_repeat = rec.pack("brown-post-detach-plan-refusal", tar_pack, "plan-removal", "--target", str(brown), "--json", exits=(3,))
    if json.loads(brown_repeat.stdout)["status"] != "REFUSED":
        raise AssertionError("brownfield detach still has an import receipt")

    # Exact v1 -> disposable v2 -> v1 rollback, using only extracted runner bytes.
    v2_pack = out / "disposable-v2-fixture-pack"
    v2_fixture = make_disposable_v2_fixture(tar_pack, v2_pack, module)
    rolled = out / "rollback-target"
    rolled.mkdir()
    authored_rollback = b"# Authored rollback guidance\r\n"
    (rolled / "AGENTS.md").write_bytes(authored_rollback)
    install(rec, "rollback-v1", zip_pack, rolled)
    rolled_agents = (rolled / "AGENTS.md").read_bytes()
    v1_payload = (rolled / MANAGED_REL).read_bytes()
    update(rec, "rollback-v2", v2_pack, zip_pack, rolled)
    if (rolled / MANAGED_REL).read_bytes() == v1_payload or (rolled / "AGENTS.md").read_bytes() != rolled_agents:
        raise AssertionError("v2 update did not preserve authored guidance or change owned payload")
    exact_rollback = rollback_plan(rec, "rollback-preview", zip_pack, v2_pack, zip_pack, rolled)
    rolled_apply = rec.installed("rollback-apply", rolled, "rollback-pack", "--current-pack", str(v2_pack),
                                 "--previous-pack", str(zip_pack), "--target", str(rolled),
                                 "--expect-plan", exact_rollback["plan_digest"], "--json")
    if json.loads(rolled_apply.stdout)["status"] != "ROLLED_BACK":
        raise AssertionError("exact predecessor rollback did not apply")
    if (rolled / MANAGED_REL).read_bytes() != v1_payload or (rolled / "AGENTS.md").read_bytes() != rolled_agents:
        raise AssertionError("rollback did not restore v1 payload and authored guidance")
    if module.load_portable_import_receipt(rolled)["pack"] != module.import_pack_identity(zip_pack):
        raise AssertionError("rollback receipt does not identify the exact v1 pack")

    # A direct edit after the rollback preview makes that digest stale.
    changed_rollback = out / "rollback-changed-target"
    install(rec, "rollback-changed-v1", zip_pack, changed_rollback)
    update(rec, "rollback-changed-v2", v2_pack, zip_pack, changed_rollback)
    stale_rollback = rollback_plan(rec, "rollback-changed-preview", zip_pack, v2_pack, zip_pack, changed_rollback)
    edited_rollback = b"# Direct project edit after rollback preview.\n"
    (changed_rollback / MANAGED_REL).write_bytes(edited_rollback)
    edited_state = tree_hashes(changed_rollback)
    refused_rollback = rec.installed("rollback-stale-refusal", changed_rollback, "rollback-pack", "--current-pack", str(v2_pack),
                                     "--previous-pack", str(zip_pack), "--target", str(changed_rollback),
                                     "--expect-plan", stale_rollback["plan_digest"], "--json", exits=(3,))
    if json.loads(refused_rollback.stdout)["status"] != "STALE_PLAN" or tree_hashes(changed_rollback) != edited_state:
        raise AssertionError("direct edit after rollback preview was not preserved")
    conflict_rollback = rec.installed("rollback-changed-conflict", changed_rollback, "rollback-pack", "--current-pack", str(v2_pack),
                                      "--previous-pack", str(zip_pack), "--target", str(changed_rollback),
                                      "--dry-run", "--json", exits=(2,))
    if json.loads(conflict_rollback.stdout)["status"] != "CONFLICT" or tree_hashes(changed_rollback) != edited_state:
        raise AssertionError("changed rollback target was not classified as a conflict")

    # A pending removal intent preempts both rollback preview and apply.
    pending = out / "rollback-pending-removal-target"
    install(rec, "rollback-pending-v1", zip_pack, pending)
    update(rec, "rollback-pending-v2", v2_pack, zip_pack, pending)
    pending_rollback = rollback_plan(rec, "rollback-pending-preview", zip_pack, v2_pack, zip_pack, pending)
    pending_removal = module.build_portable_removal_plan(pending)
    partial = module.apply_portable_removal(pending, pending_removal["plan_digest"], fail_after_removals=1)
    if partial["status"] != "INTERRUPTED" or not (pending / module.PORTABLE_REMOVAL_INTENT_PATH).is_file():
        raise AssertionError("pending removal intent was not established")
    pending_state = tree_hashes(pending)
    for label, suffix in (("rollback-pending-preview-refusal", ("--dry-run",)),
                          ("rollback-pending-apply-refusal", ("--expect-plan", pending_rollback["plan_digest"]))):
        blocked = rec.pack(label, zip_pack, "rollback-pack", "--current-pack", str(v2_pack),
                           "--previous-pack", str(zip_pack), "--target", str(pending), *suffix, exits=(1,))
        if "portable removal recovery must complete before rollback" not in blocked.stderr or tree_hashes(pending) != pending_state:
            raise AssertionError("pending removal failed to block rollback without further target effects")

    # A failed post-publication AGENTS backup disposition must reconcile before detach.
    backup_target = out / "authored-backup-recovery-target"
    backup_target.mkdir()
    authored_backup = b"# Authored policy survives.\r\n"
    (backup_target / "AGENTS.md").write_bytes(authored_backup)
    install(rec, "authored-backup", tar_pack, backup_target)
    backup_receipt = module.load_portable_import_receipt(backup_target)
    backup_managed = set(backup_receipt["managed"])
    before_section = (backup_target / "AGENTS.md").read_bytes()
    expected_section = module.portable_agents_section_postimage(
        before_section, backup_receipt["managed"]["AGENTS.md"]["installed_digest"]
    )
    if expected_section is None or not expected_section.startswith(authored_backup):
        raise AssertionError("backup recovery fixture lacks exact authored outside bytes")
    backup_plan = module.build_portable_removal_plan(backup_target)
    backup_path = backup_target / (".AGENTS.md.aide-import-backup-" + backup_plan["plan_digest"][:20])
    original_disposition = module.portable_import_delete_open_leaf
    injected_backup_failure = []
    def fail_backup_disposition(kernel, handle):
        if (not injected_backup_failure and backup_path.is_file() and
                (backup_target / "AGENTS.md").is_file() and
                (backup_target / "AGENTS.md").read_bytes() == expected_section):
            injected_backup_failure.append(True)
            raise OSError("disposable post-publication backup disposition failure")
        return original_disposition(kernel, handle)
    with mock.patch.object(module, "portable_import_delete_open_leaf", side_effect=fail_backup_disposition):
        uncertain_backup = module.apply_portable_removal(backup_target, backup_plan["plan_digest"])
    if (uncertain_backup["status"] != "RECOVERY_REQUIRED" or injected_backup_failure != [True] or
            backup_path.read_bytes() != before_section or
            not (backup_target / module.PORTABLE_IMPORT_RECEIPT_PATH).is_file() or
            not (backup_target / module.PORTABLE_REMOVAL_INTENT_PATH).is_file()):
        raise AssertionError("post-publication failure lost exact backup recovery state")
    backup_recovered = rec.pack("authored-backup-resume", tar_pack, "apply-removal", "--target", str(backup_target),
                                "--expect-plan", backup_plan["plan_digest"], "--json")
    if json.loads(backup_recovered.stdout)["status"] != "DETACHED" or os.path.lexists(backup_path):
        raise AssertionError("backup recovery did not remove the exact original before detach")
    assert_detached(backup_target, backup_managed, module, authored_agents=expected_section)

    # Changed leaf between preview and apply refuses the stale plan before any effect.
    stale = out / "changed-leaf-target"
    install(rec, "changed", zip_pack, stale)
    stale_plan = plan_removal(rec, "changed-removal-plan", stale)
    changed_leaf = stale / MANAGED_REL
    changed_bytes = b"Project edit after removal preview.\n"
    changed_leaf.write_bytes(changed_bytes)
    changed_state = tree_hashes(stale)
    stale_apply = rec.installed("changed-stale-apply", stale, "apply-removal", "--target", str(stale), "--expect-plan", stale_plan["plan_digest"], "--json", exits=(3,))
    if json.loads(stale_apply.stdout)["status"] != "STALE_PLAN" or tree_hashes(stale) != changed_state:
        raise AssertionError("changed leaf was deleted or stale plan applied")
    changed_plan = plan_removal(rec, "changed-new-plan", stale)
    if changed_plan["status"] != "PRESERVATION_REQUIRED" or MANAGED_REL not in changed_plan["preserved_recorded_targets"]:
        raise AssertionError("changed leaf was not classified for preservation")

    # Effect-time edit is checked again on the same opened file before disposition.
    race = out / "effect-time-target"
    install(rec, "effect-time", zip_pack, race)
    race_plan = module.build_portable_removal_plan(race)
    race_leaf = race / MANAGED_REL
    original_unlink = module.windows_unlink_exact_portable_file
    race_bytes = b"Project edit at removal disposition boundary.\n"
    intercepted = False

    def change_before_unlink(path: Path, expected_digest: str, before_disposition=None) -> None:
        nonlocal intercepted
        if Path(path) == race_leaf and not intercepted:
            intercepted = True
            race_leaf.write_bytes(race_bytes)
        original_unlink(path, expected_digest, before_disposition)

    with mock.patch.object(module, "windows_unlink_exact_portable_file", side_effect=change_before_unlink):
        race_result = module.apply_portable_removal(race, race_plan["plan_digest"])
    if not intercepted or race_result["status"] != "RECOVERY_REQUIRED" or race_leaf.read_bytes() != race_bytes:
        raise AssertionError("effect-time changed leaf was not preserved")
    if not (race / module.PORTABLE_IMPORT_RECEIPT_PATH).is_file() or not (race / module.PORTABLE_REMOVAL_INTENT_PATH).is_file():
        raise AssertionError("effect-time refusal lost receipt or recovery intent")

    # Interruption after one deletion retains intent and safely resumes.
    interrupted_target = out / "interrupted-target"
    install(rec, "interrupted", zip_pack, interrupted_target)
    interrupted_plan = module.build_portable_removal_plan(interrupted_target)
    interrupted_managed = set(module.load_portable_import_receipt(interrupted_target)["managed"])
    interrupted = module.apply_portable_removal(interrupted_target, interrupted_plan["plan_digest"], fail_after_removals=1)
    if interrupted["status"] != "INTERRUPTED" or len(interrupted["removed"]) != 1:
        raise AssertionError("one-removal interruption was not established")
    if not (interrupted_target / module.PORTABLE_REMOVAL_INTENT_PATH).is_file():
        raise AssertionError("interruption intent missing")
    pending_plan = rec.installed("interrupted-new-plan-refusal", interrupted_target, "plan-removal", "--target", str(interrupted_target), "--json", exits=(3,))
    if json.loads(pending_plan.stdout)["status"] != "REFUSED":
        raise AssertionError("new plan ignored a pending removal intent")
    resumed = rec.installed("interrupted-resume", interrupted_target, "apply-removal", "--target", str(interrupted_target), "--expect-plan", interrupted_plan["plan_digest"], "--json")
    if json.loads(resumed.stdout)["status"] != "DETACHED":
        raise AssertionError("interrupted removal did not resume")
    assert_detached(interrupted_target, interrupted_managed, module)

    # Receipt-boundary interruption needs the pack runner because the installed runner is gone.
    retired = out / "receipt-boundary-target"
    install(rec, "receipt-boundary", tar_pack, retired)
    retired_plan = module.build_portable_removal_plan(retired)
    retired_managed = set(module.load_portable_import_receipt(retired)["managed"])
    boundary = module.apply_portable_removal(retired, retired_plan["plan_digest"], fail_after_receipt=True)
    if boundary["status"] != "INTERRUPTED" or (retired / module.PORTABLE_IMPORT_RECEIPT_PATH).exists() or not (retired / module.PORTABLE_REMOVAL_INTENT_PATH).is_file():
        raise AssertionError("receipt-boundary interruption was not established")
    recovered = rec.pack("receipt-boundary-recover", tar_pack, "apply-removal", "--target", str(retired), "--expect-plan", retired_plan["plan_digest"], "--json")
    if json.loads(recovered.stdout)["status"] != "DETACHED_RECOVERED":
        raise AssertionError("receipt-boundary retirement did not recover")
    assert_detached(retired, retired_managed, module)

    after = {kind: file_sha(path) for kind, path in archives.items()}
    if after != expected or file_sha(release_guide) != guide_sha:
        raise AssertionError("frozen archive or release guide bytes changed during canary")
    direct = {
        "effect_time_status": race_result["status"], "effect_time_leaf_digest": file_sha(race_leaf),
        "interrupted_status": interrupted["status"], "interrupted_removed": interrupted["removed"],
        "receipt_boundary_status": boundary["status"], "brownfield_detach_status": brown_result["status"],
        "exact_rollback_status": json.loads(rolled_apply.stdout)["status"],
        "stale_rollback_status": json.loads(refused_rollback.stdout)["status"],
        "changed_rollback_status": json.loads(conflict_rollback.stdout)["status"],
        "pending_removal_status": partial["status"],
        "backup_uncertain_status": uncertain_backup["status"],
        "backup_recovered_status": json.loads(backup_recovered.stdout)["status"],
    }
    (out / "direct-results.json").write_text(json.dumps(direct, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    summary = {
        "candidate_source_commit": args.candidate_source_commit,
        "canary_sha256": file_sha(Path(__file__)),
        "candidate_archive_sha256": after,
        "generated_install_guides": guide_checks,
        "candidate_member_count": len(zip_members),
        "fresh_full_detach": True,
        "brownfield_full_detach_outside_bytes_preserved": True,
        "rollback_v1_v2_v1_exact": True,
        "rollback_v2_fixture": v2_fixture,
        "pending_removal_blocks_rollback": True,
        "backup_recovery_before_detach": True,
        "changed_leaf_refused": True,
        "effect_time_changed_leaf_preserved": True,
        "interruption_resumed": True,
        "receipt_boundary_recovered": True,
        "commands": rec.commands,
        "limitations": ["Windows-only rollback and removal apply", "the v2 update is an explicitly modified disposable copy of delivered bytes, not an earlier or published AIDE release", "fault injection uses the delivered Python API in-process because the CLI has no failure-injection switch", "local pack paths and CLI declarations do not constitute an OS-level network trace", "consumer canary does not establish native-host, hosted, main, tag or publication acceptance"],
    }
    (out / "canary-summary.json").write_text(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "out": str(out), "commands": len(rec.commands), "candidate_members": len(zip_members)}, sort_keys=True))


if __name__ == "__main__":
    main()
