"""Offline, disposable consumer canary for frozen AIDE three-way update assets.

Supply exact local ZIP/tar paths, SHA256 values, source commit, and reviewed
source CLI SHA256 after the controller freezes the artifacts. This script never
writes to those inputs or to an AIDE checkout. Synthetic V2/V3 packs are
fixture updates, not releases.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tarfile
import traceback
import zipfile
from pathlib import Path, PurePosixPath


sys.dont_write_bytecode = True
PREP = Path(__file__).resolve().parent
PACK_NAME = "aide-lite-pack-v0"
MANAGED = ".aide/prompts/compact-task.md"
OPTIONAL = ".aide.local.example/README.md"
RELEASE_MUTABLE = {"checksums.json", "manifest.yaml", "export-report.md"}
MAX_MEMBER = 256 * 1024 * 1024
MAX_ARCHIVE_CONTENT = 1024 * 1024 * 1024


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(part)
    return value.hexdigest()


def require_hash(value: str, label: str) -> str:
    if re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ValueError(f"{label} must be an exact lowercase SHA256")
    return value


def safe_member(name: str) -> PurePosixPath:
    parts = name.split("/")
    if (
        not name or name.startswith("/") or "\\" in name or "//" in name
        or name.endswith("/") or any(part in {"", ".", ".."} for part in parts)
        or parts[0] != PACK_NAME
        or any(part.endswith((" ", ".")) or ":" in part for part in parts)
        or any(any(ord(char) < 32 or char in '<>"|?*' for char in part) for part in parts)
        or any(re.match(r"^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)", part, re.I) for part in parts)
    ):
        raise ValueError(f"unsafe archive member: {name}")
    return PurePosixPath(*parts)


def extract_archive(archive: Path, destination: Path, kind: str) -> dict[str, str]:
    """Extract regular file members only; reject Windows aliases and bombs."""
    seen: set[str] = set()
    folded: set[str] = set()
    checks: dict[str, str] = {}
    total = 0

    def store(name: str, body: bytes) -> None:
        nonlocal total
        relative = safe_member(name)
        if name in seen or name.casefold() in folded:
            raise ValueError(f"duplicate archive member: {name}")
        if len(body) > MAX_MEMBER:
            raise ValueError(f"archive member exceeds size limit: {name}")
        total += len(body)
        if total > MAX_ARCHIVE_CONTENT:
            raise ValueError("archive content exceeds size limit")
        seen.add(name)
        folded.add(name.casefold())
        checks[name] = sha256_bytes(body)
        target = destination.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)

    if kind == "zip":
        with zipfile.ZipFile(archive) as handle:
            for member in handle.infolist():
                mode = (member.external_attr >> 16) & 0o170000
                if member.is_dir() or mode not in {0, 0o100000} or member.file_size > MAX_MEMBER:
                    raise ValueError(f"non-regular or oversized ZIP member: {member.filename}")
                with handle.open(member) as source:
                    body = source.read(MAX_MEMBER + 1)
                    if source.read(1):
                        raise ValueError(f"ZIP member exceeds size limit: {member.filename}")
                store(member.filename, body)
    elif kind == "tar":
        with tarfile.open(archive, "r:gz") as handle:
            for member in handle.getmembers():
                if not member.isfile() or member.linkname or member.size > MAX_MEMBER:
                    raise ValueError(f"non-regular or oversized tar member: {member.name}")
                source = handle.extractfile(member)
                if source is None:
                    raise ValueError(f"unreadable tar member: {member.name}")
                body = source.read(MAX_MEMBER + 1)
                if source.read(1):
                    raise ValueError(f"tar member exceeds size limit: {member.name}")
                store(member.name, body)
    else:
        raise ValueError(f"unknown archive type: {kind}")
    verify_pack(destination / PACK_NAME, checks)
    return checks


def verify_pack(pack: Path, archive_checks: dict[str, str]) -> None:
    checksums = json.loads((pack / "checksums.json").read_text(encoding="utf-8"))
    expected = checksums.get("checksums")
    if not isinstance(expected, dict):
        raise ValueError("embedded pack checksum mapping is invalid")
    actual = {name.removeprefix(PACK_NAME + "/"): value for name, value in archive_checks.items()}
    if set(expected) != set(actual) - RELEASE_MUTABLE:
        raise ValueError("embedded pack checksum coverage differs from archive members")
    if any(actual[name] != value for name, value in expected.items()):
        raise ValueError("embedded pack checksum mismatch")


def delivered_module(pack: Path):
    script = pack / "files/.aide/scripts/aide_lite.py"
    spec = importlib.util.spec_from_file_location("aide_three_way_delivered_canary", script)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load delivered importer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def make_synthetic_update(base: Path, destination: Path, version: int, delivered) -> Path:
    shutil.copytree(base, destination)
    changes = {
        MANAGED: f"# Disposable AIDE canary upstream v{version}\n",
        OPTIONAL: f"Disposable optional example v{version}\n",
    }
    for relative, content in changes.items():
        payload = destination / "files" / relative
        if not payload.is_file():
            raise AssertionError(f"candidate pack lacks required fixture path: {relative}")
        payload.write_bytes(content.encode("utf-8"))
    manifest = destination / "manifest.yaml"
    with manifest.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(f"canary_fixture: synthetic_update_v{version}\n")
    (destination / "checksums.json").write_text(
        delivered.stable_json_text(delivered.build_pack_checksums(destination)), encoding="utf-8"
    )
    okay, problems = delivered.validate_pack_checksums(destination)
    if not okay:
        raise AssertionError(f"synthetic V{version} pack invalid: {problems}")
    return destination


class Recorder:
    def __init__(self, out: Path) -> None:
        self.out = out
        self.commands: list[dict[str, object]] = []

    def command(self, label: str, pack: Path, target: Path, args: list[str], expected_exit: int = 0, *, installed: bool = False) -> subprocess.CompletedProcess[str]:
        script = pack / (".aide/scripts/aide_lite.py" if installed else "files/.aide/scripts/aide_lite.py")
        argv = [sys.executable, "-I", "-B", str(script), "--repo-root", str(target), *args]
        result = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240)
        record = {"argv": argv, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        log = self.out / f"{label}.json"
        log.write_text(json.dumps(record, sort_keys=True, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.commands.append({"label": label, "log": str(log), "sha256": sha256_file(log), "exit_code": result.returncode})
        if result.returncode != expected_exit:
            raise AssertionError(f"{label}: exit {result.returncode}, expected {expected_exit}; see {log}")
        if args and args[0] in {"import-pack", "repair-owned-file"} and "network_calls: none" not in result.stdout:
            raise AssertionError(f"{label}: delivered effect CLI did not declare offline operation")
        return result


def field(output: str, name: str) -> str:
    for line in output.splitlines():
        if line.startswith(name + ": "):
            return line.partition(": ")[2]
    raise AssertionError(f"missing {name} in delivered CLI output")


def require_unknown_explanation(output: str, target: str, action: str) -> None:
    """Bind the unknown-rationale oracle to one exact delivered explanation row."""
    prefix = f"- {action}: {target}; "
    rows = [line for line in output.splitlines() if line.startswith(prefix)]
    if len(rows) != 1:
        raise AssertionError(f"expected one {action} explanation for {target}, got {len(rows)}")
    match = re.fullmatch(
        rf"- {re.escape(action)}: {re.escape(target)}; basis=[^;]+; reason=.*; rationale_status=([^;]+); project_rationale=(.+)",
        rows[0],
    )
    if match is None or match.group(1) != "unknown" or json.loads(match.group(2)) != "unknown":
        raise AssertionError(f"{action} explanation for {target} fabricated project rationale")


def target_byte_snapshot(target: Path) -> dict[str, str]:
    return {
        path.relative_to(target).as_posix(): sha256_file(path)
        for path in sorted(target.rglob("*")) if path.is_file()
    }


def inspect_health(rec: Recorder, label: str, pack: Path, target: Path, delivered) -> dict[str, object]:
    """Run only the delivered --json inspector and check file-path/byte stasis."""
    before = target_byte_snapshot(target)
    run = rec.command(label, pack, target, ["repair-health", "--pack", str(pack), "--target", str(target), "--json"])
    after = target_byte_snapshot(target)
    if before != after:
        raise AssertionError(f"{label}: repair-health changed target file paths or bytes")
    report = json.loads(run.stdout)
    if report.get("schema_version") != "aide.portable-repair-health.v1":
        raise AssertionError(f"{label}: unexpected repair-health schema")
    if report.get("read_only") is not True or report.get("network_calls") is not False or report.get("provider_or_model_calls") is not False:
        raise AssertionError(f"{label}: repair-health did not declare a read-only, offline result")
    if report.get("pack") != delivered.import_pack_identity(pack):
        raise AssertionError(f"{label}: repair-health pack identity differs")
    receipt = delivered.load_portable_import_receipt(target)
    if report.get("receipt_digest") != receipt["receipt_digest"]:
        raise AssertionError(f"{label}: repair-health receipt identity differs")
    if report.get("target") != str(target):
        raise AssertionError(f"{label}: repair-health target identity differs")
    if report.get("pending_intents"):
        raise AssertionError(f"{label}: unexpected pending intent in disposable consumer")
    return report


def health_row(report: dict[str, object], target_rel: str) -> dict[str, object]:
    rows = [item for item in report["observations"] if item["path"] == target_rel]
    if len(rows) != 1:
        raise AssertionError(f"repair-health lacks one exact row for {target_rel}")
    return rows[0]


def import_args(pack: Path, target: Path, predecessor: Path | None = None, resolve: tuple[str, Path] | None = None) -> list[str]:
    parts = ["import-pack", "--pack", str(pack), "--target", str(target), "--mode", "safe"]
    if predecessor is not None:
        parts.extend(["--from-pack", str(predecessor)])
    if resolve is not None:
        parts.extend(["--resolve", resolve[0], str(resolve[1])])
    return parts


def preview_apply(rec: Recorder, label: str, pack: Path, target: Path, predecessor: Path | None = None, resolve: tuple[str, Path] | None = None, explain: bool = False, feedback_out: Path | None = None) -> tuple[str, str]:
    base = import_args(pack, target, predecessor, resolve)
    preview = rec.command(label + "-preview", pack, target, [*base, "--dry-run", *(["--explain"] if explain else []), *(["--feedback-out", str(feedback_out)] if feedback_out else [])])
    if field(preview.stdout, "status") != "PLANNED":
        raise AssertionError(f"{label}: import preview is not PLANNED")
    plan = field(preview.stdout, "plan_digest")
    applied = rec.command(label + "-apply", pack, target, [*base, "--expect-plan", plan])
    if field(applied.stdout, "status") != "APPLIED":
        raise AssertionError(f"{label}: import apply is not APPLIED")
    return plan, preview.stdout


def require_absent_feedback(out: Path, *targets: Path) -> None:
    if (out / "unsolicited-feedback.json").exists():
        raise AssertionError("feedback appeared without an explicit output request")
    for target in targets:
        if any(path.name.casefold().endswith("feedback.json") for path in target.rglob("*")):
            raise AssertionError(f"target gained unsolicited feedback JSON: {target}")


def run_consumers(out: Path, candidate: Path, candidate_tar: Path, delivered, rec: Recorder) -> dict[str, object]:
    v2 = make_synthetic_update(candidate_tar, out / "synthetic-v2", 2, delivered)
    v3 = make_synthetic_update(candidate_tar, out / "synthetic-v3", 3, delivered)
    if len({json.dumps(delivered.import_pack_identity(pack), sort_keys=True) for pack in (candidate, v2, v3)}) != 3:
        raise AssertionError("V1/V2/V3 fixture identities are not distinct")

    # Fresh consumer uses exact candidate ZIP bytes; its CLI is installed into
    # the disposable target and can run without the source checkout.
    fresh = out / "fresh-target"
    preview_apply(rec, "fresh-v1", candidate, fresh)
    rec.command("fresh-installed-doctor", fresh, fresh, ["doctor"], installed=True)
    if not (fresh / MANAGED).is_file():
        raise AssertionError("fresh target lacks managed payload")
    if not (fresh / ".aide/scripts/aide_lite.py").is_file():
        raise AssertionError("fresh target lacks installed CLI")
    fresh_health = inspect_health(rec, "fresh-v1-repair-health", candidate, fresh, delivered)
    fresh_row = health_row(fresh_health, MANAGED)
    if fresh_health["status"] != "HEALTHY" or fresh_row["state"] != "MATCHING" or fresh_row["repair_eligible"]:
        raise AssertionError("fresh delivered repair-health is not healthy")

    # Project-owned v2 controls disable optional examples across two updates.
    optional_before = (fresh / OPTIONAL).read_bytes()
    controls = fresh / ".aide/customizations.json"
    controls.write_text(json.dumps({
        "schema_version": "aide.project-customizations.v2",
        "entries": {},
        "disabled_features": [{"feature_id": "local_state_examples"}],
    }, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    _, disabled_explanation = preview_apply(rec, "fresh-disabled-v2", v2, fresh, candidate, explain=True)
    require_unknown_explanation(disabled_explanation, OPTIONAL, "preserve_disabled")
    if (fresh / OPTIONAL).read_bytes() != optional_before:
        raise AssertionError("V2 rewrote a disabled optional example")
    preview_apply(rec, "fresh-disabled-v3", v3, fresh, v2)
    if (fresh / OPTIONAL).read_bytes() != optional_before:
        raise AssertionError("V3 rewrote a disabled optional example")
    fresh_receipt = delivered.load_portable_import_receipt(fresh)
    if fresh_receipt["disabled_features"] != ["local_state_examples"] or OPTIONAL in fresh_receipt["managed"]:
        raise AssertionError("V3 receipt claims disabled optional bytes")

    # A missing previously managed path is a conflict even if V3 is rerun.
    missing_before = (fresh / delivered.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes()
    (fresh / MANAGED).unlink()
    missing = rec.command("fresh-missing-owned-preview", v3, fresh, [*import_args(v3, fresh), "--dry-run"], expected_exit=2)
    if field(missing.stdout, "status") != "PLANNED_CONFLICT":
        raise AssertionError("missing receipt-owned path was not a preview conflict")
    missed_apply = rec.command("fresh-missing-owned-apply", v3, fresh, [*import_args(v3, fresh), "--expect-plan", field(missing.stdout, "plan_digest")], expected_exit=2)
    if field(missed_apply.stdout, "status") != "CONFLICT" or (fresh / MANAGED).exists():
        raise AssertionError("missing receipt-owned path was silently recopied")
    if (fresh / delivered.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes() != missing_before:
        raise AssertionError("missing-file conflict changed the receipt")
    missing_health = inspect_health(rec, "fresh-missing-owned-repair-health", v3, fresh, delivered)
    missing_row = health_row(missing_health, MANAGED)
    if missing_health["status"] != "REPAIRABLE" or missing_row["state"] != "MISSING_OWNED" or missing_row["repair_eligible"] is not True:
        raise AssertionError("delivered repair-health failed to identify exact missing owned file")
    missing_state_before_preview = target_byte_snapshot(fresh)
    repair_preview = rec.command("fresh-missing-owned-repair-preview", v3, fresh, ["repair-owned-file", "--pack", str(v3), "--target", str(fresh), "--path", MANAGED, "--dry-run"])
    if field(repair_preview.stdout, "status") != "PLANNED" or missing_row["repair_plan_digest"] != field(repair_preview.stdout, "plan_digest"):
        raise AssertionError("repair-health eligibility digest differs from exact repair preview")
    if target_byte_snapshot(fresh) != missing_state_before_preview:
        raise AssertionError("repair preview changed missing-owned target bytes")

    # Brownfield authored CRLF guidance and unknown content stay project-owned.
    brown = out / "brownfield-target"
    brown.mkdir()
    authored = b"# Project-authored guidance\r\nKeep this text.\r\n"
    (brown / "AGENTS.md").write_bytes(authored)
    (brown / "README.md").write_bytes(b"# Existing project\r\n")
    (brown / "project-data.txt").write_bytes(b"owned data\n")
    preview_apply(rec, "brown-v1", candidate, brown)
    if not (brown / "AGENTS.md").read_bytes().startswith(authored):
        raise AssertionError("brownfield authored AGENTS prefix was changed")
    if (brown / "project-data.txt").read_bytes() != b"owned data\n":
        raise AssertionError("brownfield data changed at import")

    # Direct edit + changed upstream refuses before writes and has unknown why.
    local = b"# Project direct edit with unknown rationale\n"
    (brown / MANAGED).write_bytes(local)
    receipt_v1 = (brown / delivered.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes()
    edited_health = inspect_health(rec, "brown-direct-edit-repair-health", candidate, brown, delivered)
    edited_row = health_row(edited_health, MANAGED)
    if edited_health["status"] != "PRESERVATION_REQUIRED" or edited_row["state"] != "CHANGED" or edited_row["repair_eligible"]:
        raise AssertionError("repair-health misclassified a direct project edit as repairable")
    if edited_row["repair_plan_digest"] is not None or "rationale" in edited_row:
        raise AssertionError("repair-health fabricated eligibility or project rationale for a direct edit")
    conflict = rec.command("brown-v2-conflict-preview", v2, brown, [*import_args(v2, brown, candidate), "--dry-run", "--explain"], expected_exit=2)
    if field(conflict.stdout, "status") != "PLANNED_CONFLICT":
        raise AssertionError("direct edit was not a planned conflict")
    require_unknown_explanation(conflict.stdout, MANAGED, "conflict")
    refused = rec.command("brown-v2-conflict-apply", v2, brown, [*import_args(v2, brown, candidate), "--expect-plan", field(conflict.stdout, "plan_digest")], expected_exit=2)
    if field(refused.stdout, "status") != "CONFLICT" or (brown / MANAGED).read_bytes() != local:
        raise AssertionError("unresolved V2 conflict changed local bytes")
    if (brown / delivered.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes() != receipt_v1:
        raise AssertionError("unresolved V2 conflict changed receipt")

    resolved_v2 = out / "selected-v2-resolution.txt"
    merged_v2 = b"# Project-selected V2 combination\n"
    resolved_v2.write_bytes(merged_v2)
    resolved_feedback = out / "brown-v2-resolved-feedback.json"
    plain_resolved = rec.command(
        "brown-v2-resolved-plain-preview", v2, brown,
        [*import_args(v2, brown, candidate), "--resolve", MANAGED,
         str(resolved_v2), "--dry-run"])
    if field(plain_resolved.stdout, "status") != "PLANNED":
        raise AssertionError("plain project-resolved preview failed")
    _, v2_explanation = preview_apply(rec, "brown-v2-resolved", v2, brown, candidate, (MANAGED, resolved_v2), explain=True, feedback_out=resolved_feedback)
    require_unknown_explanation(v2_explanation, MANAGED, "resolve_owned")
    packet = json.loads(resolved_feedback.read_text(encoding="utf-8"))
    if packet.get("sharing") != "manual_only" or packet.get("network_calls") is not False:
        raise AssertionError("resolved update feedback crossed sharing boundary")
    if not any(item.get("target") == MANAGED and item.get("action") == "resolve_owned"
               and item.get("project_rationale") == "unknown" and "observed_digest" in item
               and "incoming_digest" in item for item in packet.get("explanations", [])):
        raise AssertionError("resolved update feedback lacks bound unknown-rationale explanation")
    if str(resolved_v2) in v2_explanation or (brown / MANAGED).read_bytes() != merged_v2:
        raise AssertionError("V2 resolution path leaked or wrong bytes installed")
    entry_v2 = delivered.load_portable_import_receipt(brown)["managed"][MANAGED]
    if entry_v2["installed_digest"] != sha256_bytes(merged_v2) or not entry_v2["local_overlay"]:
        raise AssertionError("V2 receipt did not record the project overlay")

    # The overlay remains protected when V3 changes the upstream source.
    receipt_v2 = (brown / delivered.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes()
    conflict_v3 = rec.command("brown-v3-conflict-preview", v3, brown, [*import_args(v3, brown, v2), "--dry-run", "--explain"], expected_exit=2)
    if field(conflict_v3.stdout, "status") != "PLANNED_CONFLICT" or (brown / MANAGED).read_bytes() != merged_v2:
        raise AssertionError("V3 silently replaced the V2 project overlay")
    if (brown / delivered.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes() != receipt_v2:
        raise AssertionError("V3 conflict changed receipt")
    resolved_v3 = out / "selected-v3-resolution.txt"
    merged_v3 = b"# Project-selected V3 combination\n"
    resolved_v3.write_bytes(merged_v3)
    preview_apply(rec, "brown-v3-resolved", v3, brown, v2, (MANAGED, resolved_v3), explain=True)
    if (brown / MANAGED).read_bytes() != merged_v3:
        raise AssertionError("V3 manual resolution bytes differ")
    entry_v3 = delivered.load_portable_import_receipt(brown)["managed"][MANAGED]
    if entry_v3["installed_digest"] != sha256_bytes(merged_v3) or not entry_v3["local_overlay"]:
        raise AssertionError("V3 overlay receipt is invalid")
    if not (brown / "AGENTS.md").read_bytes().startswith(authored) or (brown / "project-data.txt").read_bytes() != b"owned data\n":
        raise AssertionError("brownfield authored content changed during updates")
    agents_path = brown / "AGENTS.md"
    heading = b"## AIDE Lite Portable Guidance"
    agents_before = agents_path.read_bytes()
    if agents_before.count(heading) != 1:
        raise AssertionError("brownfield AGENTS fixture lacks one managed heading")
    agents_path.write_bytes(agents_before.replace(heading, b"## Project-adjusted portable guidance", 1))
    _, overlay_explanation = preview_apply(rec, "brown-agents-overlay", v3, brown, explain=True)
    require_unknown_explanation(overlay_explanation, "AGENTS.md", "preserve_local")
    overlay_health = inspect_health(rec, "brown-agents-overlay-repair-health", v3, brown, delivered)
    agents_row = health_row(overlay_health, "AGENTS.md")
    if overlay_health["status"] != "PRESERVATION_REQUIRED" or agents_row["state"] != "MATCHING" or agents_row["repair_eligible"]:
        raise AssertionError("repair-health misclassified project-owned AGENTS overlay")
    if agents_row["ownership"] != "project_overlay_on_aide_managed" or agents_row["local_overlay"] is not True:
        raise AssertionError("repair-health failed to show AGENTS project overlay ownership")
    if "rationale" in agents_row or "project overlay remains project owned" not in agents_row["reason"]:
        raise AssertionError("repair-health invented a reason for the AGENTS project edit")
    if not agents_path.read_bytes().startswith(authored):
        raise AssertionError("AGENTS overlay adoption changed authored CRLF prefix")
    require_absent_feedback(out, fresh, brown)
    return {
        "fixture_pack_identities": {label: delivered.import_pack_identity(pack) for label, pack in (("v1_exact_candidate", candidate), ("v2_synthetic", v2), ("v3_synthetic", v3))},
        "fresh_receipt_digest": fresh_receipt["receipt_digest"],
        "brown_receipt_digest": delivered.load_portable_import_receipt(brown)["receipt_digest"],
        "repair_health_statuses": {"fresh": fresh_health["status"], "missing": missing_health["status"], "direct_edit": edited_health["status"], "agents_overlay": overlay_health["status"]},
        "synthetic_versions_are_published_releases": False,
        "feedback_created_by_default": False,
        "resolved_feedback_sha256": sha256_file(resolved_feedback),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-zip", type=Path, required=True)
    parser.add_argument("--candidate-tar", type=Path, required=True)
    parser.add_argument("--candidate-zip-sha256", required=True)
    parser.add_argument("--candidate-tar-sha256", required=True)
    parser.add_argument("--bundled-cli-sha256", required=True, help="SHA256 of the reviewed source commit's .aide/scripts/aide_lite.py bytes")
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if re.fullmatch(r"[0-9a-f]{40}", args.source_commit) is None:
        raise ValueError("source commit must be a full lowercase Git object ID")
    expected = {
        "zip": require_hash(args.candidate_zip_sha256, "candidate ZIP"),
        "tar": require_hash(args.candidate_tar_sha256, "candidate tar"),
    }
    expected_cli = require_hash(args.bundled_cli_sha256, "reviewed source CLI")
    archives = {"zip": args.candidate_zip.resolve(strict=True), "tar": args.candidate_tar.resolve(strict=True)}
    for label, path in archives.items():
        if not path.is_file() or sha256_file(path) != expected[label]:
            raise ValueError(f"frozen {label} archive identity mismatch")
    out = args.out.resolve()
    if out.parent != PREP or not out.name.startswith("run-") or out.exists():
        raise ValueError("output must be a new run-* child of this prep directory")
    out.mkdir()
    rec = Recorder(out)
    try:
        zip_members = extract_archive(archives["zip"], out / "candidate-zip", "zip")
        tar_members = extract_archive(archives["tar"], out / "candidate-tar", "tar")
        if zip_members != tar_members:
            raise AssertionError("candidate ZIP and tar regular-file members differ")
        cli_member = f"{PACK_NAME}/files/.aide/scripts/aide_lite.py"
        if zip_members.get(cli_member) != expected_cli or tar_members.get(cli_member) != expected_cli:
            raise AssertionError("bundled CLI bytes differ from independently supplied reviewed source digest")
        candidate = out / "candidate-zip" / PACK_NAME
        candidate_tar = out / "candidate-tar" / PACK_NAME
        manifest = (candidate / "manifest.yaml").read_text(encoding="utf-8")
        if f"source_commit: {args.source_commit}" not in manifest.splitlines() or "source_dirty_state: false" not in manifest.splitlines():
            raise AssertionError("candidate pack manifest does not declare the supplied clean commit")
        delivered = delivered_module(candidate)
        if not hasattr(delivered, "PORTABLE_IMPORT_RECEIPT_SCHEMA_V2") or not hasattr(delivered, "read_portable_resolution_bytes"):
            raise AssertionError("delivered CLI lacks three-way importer contracts")
        okay, problems = delivered.validate_pack_checksums(candidate)
        if not okay:
            raise AssertionError(f"delivered pack checksum validation failed: {problems}")
        result = run_consumers(out, candidate, candidate_tar, delivered, rec)
        after = {label: sha256_file(path) for label, path in archives.items()}
        if after != expected:
            raise AssertionError("frozen input archive changed during consumer run")
        summary = {
            "status": "PASS",
            "script_sha256": sha256_file(Path(__file__)),
            "archive_sha256": after,
            "source_commit": args.source_commit,
            "source_commit_binding": "manifest_declaration_and_bundled_cli_digest_only",
            "bundled_cli_sha256": expected_cli,
            "archive_member_count": len(zip_members),
            "commands": rec.commands,
            **result,
        }
        (out / "summary.json").write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "PASS", "out": str(out), "summary_sha256": sha256_file(out / "summary.json"), "command_count": len(rec.commands)}, sort_keys=True))
    except BaseException:
        failure = out / "failure.txt"
        failure.write_text(traceback.format_exc(), encoding="utf-8")
        (out / "commands.json").write_text(json.dumps(rec.commands, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
