"""Fixture-safe managed-section parsing and patch planning.

The functions in this module operate on explicit text or fixture paths only.
They preserve manual content outside marker-bounded generated sections and do
not implement active repository apply behavior.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any


MARKER_FAMILY = "AIDE-GENERATED"
SECTION_NAME_PATTERN = r"[A-Za-z0-9][A-Za-z0-9_.:-]*"
BEGIN_RE = re.compile(
    rf"(?m)^(?P<marker><!--\s*AIDE-GENERATED:BEGIN\s+section=(?P<section>{SECTION_NAME_PATTERN})\b[^>]*-->)\s*\r?$"
)
END_RE = re.compile(
    rf"(?m)^(?P<marker><!--\s*AIDE-GENERATED:END\s+section=(?P<section>{SECTION_NAME_PATTERN})\s*-->)\s*\r?$"
)
CONFLICT_CLASSES = {
    "missing_start_marker",
    "missing_end_marker",
    "duplicate_start_marker",
    "duplicate_end_marker",
    "nested_marker",
    "malformed_marker",
    "marker_order_invalid",
    "existing_hash_mismatch",
    "manual_content_changed",
    "binary_file",
    "unsupported_encoding",
    "destructive_patch",
    "unknown",
}


class ManagedSectionError(ValueError):
    """Raised for invalid fixture path or unsupported file access."""


def compute_text_hash(text: str) -> str:
    """Return a sha256 hash over the exact UTF-8 text."""

    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _next_line_start(text: str, marker_end: int) -> int:
    newline_index = text.find("\n", marker_end)
    return len(text) if newline_index == -1 else newline_index + 1


def _match_records(pattern: re.Pattern[str], text: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for match in pattern.finditer(text):
        records.append(
            {
                "section": match.group("section"),
                "marker": match.group("marker"),
                "start": match.start(),
                "end": match.end(),
                "line": _line_number(text, match.start()),
            }
        )
    return records


def make_managed_section_conflict(
    conflict_class: str,
    path: str = "<memory>",
    section_name: str = "",
    message: str = "",
    severity: str = "error",
) -> dict[str, Any]:
    """Return a JSON-compatible managed-section conflict record."""

    known_class = conflict_class if conflict_class in CONFLICT_CLASSES else "unknown"
    return {
        "schema_version": "aide.managed-section-conflict.v0",
        "conflict_id": f"managed-section-conflict-{known_class}",
        "path": path,
        "section_name": section_name,
        "conflict_class": known_class,
        "message": message or known_class.replace("_", " "),
        "severity": severity,
        "apply_blocked": True,
        "no_real_apply_boundary": True,
    }


def _conflict_section(
    conflict_class: str,
    text: str,
    section_name: str = "",
    path: str = "<memory>",
    message: str = "",
) -> dict[str, Any]:
    conflict = make_managed_section_conflict(conflict_class, path, section_name, message)
    return {
        "schema_version": "aide.managed-section-operation.v0",
        "path": path,
        "section_name": section_name,
        "section_id": section_name,
        "marker_family": MARKER_FAMILY,
        "start_marker": "",
        "end_marker": "",
        "start_line": 0,
        "end_line": 0,
        "content_start": 0,
        "content_end": 0,
        "existing_section_hash": compute_text_hash(""),
        "new_section_hash": compute_text_hash(""),
        "manual_prefix_hash": compute_text_hash(text),
        "manual_suffix_hash": compute_text_hash(""),
        "manual_content_preserved": False,
        "marker_status": "blocked",
        "conflict_status": conflict_class,
        "allowed": False,
        "blocked_reason": conflict_class,
        "conflicts": [conflict],
        "no_real_apply_boundary": True,
        "real_repo_apply_allowed": False,
    }

def _malformed_marker_present(text: str, begin_records: list[dict[str, Any]], end_records: list[dict[str, Any]]) -> bool:
    raw_begin_count = text.count("AIDE-GENERATED:BEGIN")
    raw_end_count = text.count("AIDE-GENERATED:END")
    return raw_begin_count > len(begin_records) or raw_end_count > len(end_records)


def find_managed_sections(text: str, marker_family: str | None = None) -> list[dict[str, Any]]:
    """Find unambiguous managed sections in text."""

    if marker_family not in (None, MARKER_FAMILY):
        return []
    begin_records = _match_records(BEGIN_RE, text)
    names = sorted({record["section"] for record in begin_records})
    sections: list[dict[str, Any]] = []
    for name in names:
        section = parse_managed_section(text, section_name=name, marker_family=marker_family)
        if section.get("marker_status") == "valid":
            sections.append(section)
    return sections


def parse_managed_section(
    text: str,
    section_name: str | None = None,
    marker_family: str | None = None,
    path: str = "<memory>",
) -> dict[str, Any]:
    """Parse one managed section and return an operation-like record.

    Missing, duplicate, nested, malformed, and order-invalid marker cases return
    blocked records with typed conflicts.
    """

    if marker_family not in (None, MARKER_FAMILY):
        return _conflict_section("unknown", text, section_name or "", path, f"unsupported marker family: {marker_family}")

    begin_records = _match_records(BEGIN_RE, text)
    end_records = _match_records(END_RE, text)
    if _malformed_marker_present(text, begin_records, end_records):
        return _conflict_section("malformed_marker", text, section_name or "", path, "Malformed managed-section marker.")

    if section_name is None:
        if not begin_records:
            return _conflict_section("missing_start_marker", text, "", path, "No managed-section start marker was found.")
        if len(begin_records) != 1:
            return _conflict_section("duplicate_start_marker", text, "", path, "More than one managed-section start marker exists.")
        section_name = str(begin_records[0]["section"])

    starts = [record for record in begin_records if record["section"] == section_name]
    ends = [record for record in end_records if record["section"] == section_name]
    if not starts:
        return _conflict_section("missing_start_marker", text, section_name, path, "Required start marker was not found.")
    if not ends:
        return _conflict_section("missing_end_marker", text, section_name, path, "Required end marker was not found.")
    if len(starts) > 1:
        return _conflict_section("duplicate_start_marker", text, section_name, path, "Duplicate start markers were found.")
    if len(ends) > 1:
        return _conflict_section("duplicate_end_marker", text, section_name, path, "Duplicate end markers were found.")

    start = starts[0]
    end = ends[0]
    if int(end["start"]) < int(start["end"]):
        return _conflict_section("marker_order_invalid", text, section_name, path, "End marker appears before start marker.")

    content_start = _next_line_start(text, int(start["end"]))
    content_end = int(end["start"])
    for nested in begin_records:
        nested_start = int(nested["start"])
        if int(start["end"]) <= nested_start < content_end:
            return _conflict_section("nested_marker", text, section_name, path, "Nested managed-section marker was found.")

    content = text[content_start:content_end]
    prefix = text[:content_start]
    suffix = text[content_end:]
    return {
        "schema_version": "aide.managed-section-operation.v0",
        "operation_id": f"op-managed-section-{section_name}",
        "path": path,
        "section_name": section_name,
        "section_id": section_name,
        "marker_family": MARKER_FAMILY,
        "start_marker": start["marker"],
        "end_marker": end["marker"],
        "marker_begin": start["marker"],
        "marker_end": end["marker"],
        "start_line": start["line"],
        "end_line": end["line"],
        "content_start": content_start,
        "content_end": content_end,
        "existing_section_hash": compute_text_hash(content),
        "new_section_hash": compute_text_hash(content),
        "manual_prefix_hash": compute_text_hash(prefix),
        "manual_suffix_hash": compute_text_hash(suffix),
        "manual_content_preserved": True,
        "marker_status": "valid",
        "conflict_status": "none",
        "allowed": True,
        "blocked_reason": "",
        "preimage_ref": "",
        "postimage_ref": "",
        "rollback_ref": "",
        "evidence_refs": [],
        "conflicts": [],
        "no_real_apply_boundary": True,
        "real_repo_apply_allowed": False,
    }


def _replacement_text(replacement_content: str, preserve_trailing_newline: bool = True) -> str:
    if preserve_trailing_newline and replacement_content and not replacement_content.endswith(("\n", "\r")):
        return replacement_content + "\n"
    return replacement_content


def make_managed_section_operation(
    text: str,
    section_name: str,
    replacement_content: str,
    path: str = "<memory>",
    marker_family: str | None = None,
) -> dict[str, Any]:
    """Create a transaction-compatible operation record for a planned patch."""

    section = parse_managed_section(text, section_name, marker_family, path)
    if not section.get("allowed"):
        return section
    replacement = _replacement_text(replacement_content)
    after_text = text[: int(section["content_start"])] + replacement + text[int(section["content_end"]) :]
    operation = dict(section)
    operation.update(
        {
            "operation_id": f"op-managed-section-{section_name}",
            "existing_section_hash": section["existing_section_hash"],
            "new_section_hash": compute_text_hash(replacement),
            "manual_content_preserved": verify_manual_content_preserved(text, after_text, section),
            "preimage_ref": f"preimage-{section_name}",
            "postimage_ref": f"postimage-{section_name}",
            "rollback_ref": f"rollback-{section_name}",
            "evidence_refs": [".aide/reports/managed-section-fixture-validation.md"],
        }
    )
    return operation


def build_managed_section_patch(
    text: str,
    section_name: str,
    replacement_content: str,
    marker_family: str | None = None,
    path: str = "<memory>",
    expected_existing_hash: str | None = None,
    preserve_trailing_newline: bool = True,
) -> dict[str, Any]:
    """Plan a managed-section text patch without mutating files."""

    section = parse_managed_section(text, section_name, marker_family, path)
    replacement = _replacement_text(replacement_content, preserve_trailing_newline)
    conflicts = list(section.get("conflicts", []))
    if section.get("allowed") and expected_existing_hash and expected_existing_hash != section.get("existing_section_hash"):
        conflicts.append(
            make_managed_section_conflict(
                "existing_hash_mismatch",
                path,
                section_name,
                "Existing section hash did not match expected hash.",
            )
        )
    status = "planned" if section.get("allowed") and not conflicts else "blocked"
    after_text = ""
    resulting_file_hash = ""
    if status == "planned":
        after_text = text[: int(section["content_start"])] + replacement + text[int(section["content_end"]) :]
        resulting_file_hash = compute_text_hash(after_text)
    return {
        "schema_version": "aide.managed-section-patch.v0",
        "patch_id": f"patch-managed-section-{section_name}",
        "operation_id": f"op-managed-section-{section_name}",
        "path": path,
        "section_name": section_name,
        "replacement_content": replacement,
        "replacement_hash": compute_text_hash(replacement),
        "preserve_trailing_newline": preserve_trailing_newline,
        "expected_existing_hash": expected_existing_hash or str(section.get("existing_section_hash", "")),
        "existing_section_hash": section.get("existing_section_hash", compute_text_hash("")),
        "resulting_file_hash": resulting_file_hash,
        "status": status,
        "warnings": [],
        "conflicts": conflicts,
        "content_start": section.get("content_start", 0),
        "content_end": section.get("content_end", 0),
        "operation": make_managed_section_operation(text, section_name, replacement, path, marker_family)
        if status == "planned"
        else section,
        "after_text": after_text,
        "no_real_apply_boundary": True,
        "real_repo_apply_allowed": False,
    }


def apply_managed_section_patch_to_text(text: str, patch: dict[str, Any]) -> str:
    """Apply a planned patch to in-memory text only."""

    if patch.get("status") != "planned":
        raise ManagedSectionError("managed-section patch is blocked")
    if patch.get("existing_section_hash") != compute_text_hash(text[int(patch["content_start"]) : int(patch["content_end"])]):
        raise ManagedSectionError("existing managed-section hash mismatch")
    return text[: int(patch["content_start"])] + str(patch.get("replacement_content", "")) + text[int(patch["content_end"]) :]


def verify_manual_content_preserved(before_text: str, after_text: str, operation: dict[str, Any]) -> bool:
    """Verify exact manual prefix and suffix preservation around replacement."""

    content_start = int(operation.get("content_start", 0))
    content_end = int(operation.get("content_end", 0))
    if content_start < 0 or content_end < content_start:
        return False
    prefix = before_text[:content_start]
    suffix = before_text[content_end:]
    return (
        after_text.startswith(prefix)
        and after_text.endswith(suffix)
        and compute_text_hash(prefix) == operation.get("manual_prefix_hash")
        and compute_text_hash(suffix) == operation.get("manual_suffix_hash")
    )


def is_binary_file(path: Path) -> bool:
    """Return True when a file looks binary by NUL-byte inspection."""

    try:
        return b"\0" in path.read_bytes()[:4096]
    except OSError:
        return False


def load_text_file_safely(path: Path) -> str:
    """Read UTF-8 text and reject binary or unsupported encodings."""

    if is_binary_file(path):
        raise ManagedSectionError("binary_file")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ManagedSectionError("unsupported_encoding") from exc


def _safe_fixture_path(root: Path, relative_path: str | Path) -> Path:
    rel = Path(relative_path)
    if rel.is_absolute() or any(part == ".." for part in rel.parts):
        raise ManagedSectionError("fixture relative path must stay inside fixture root")
    root_resolved = root.resolve()
    target = (root_resolved / rel).resolve()
    try:
        target.relative_to(root_resolved)
    except ValueError as exc:
        raise ManagedSectionError("fixture path escaped root") from exc
    return target


def patch_file_in_fixture(
    root: Path,
    relative_path: str | Path,
    section_name: str,
    replacement_content: str,
    marker_family: str | None = None,
) -> dict[str, Any]:
    """Patch a file under an explicit fixture root and return evidence records."""

    target = _safe_fixture_path(root, relative_path)
    before_text = load_text_file_safely(target)
    patch = build_managed_section_patch(
        before_text,
        section_name,
        replacement_content,
        marker_family=marker_family,
        path=Path(relative_path).as_posix(),
    )
    if patch.get("status") != "planned":
        return {"status": "blocked", "patch": patch, "conflicts": patch.get("conflicts", [])}
    after_text = apply_managed_section_patch_to_text(before_text, patch)
    operation = dict(patch["operation"])
    operation["manual_content_preserved"] = verify_manual_content_preserved(before_text, after_text, operation)
    target.write_text(after_text, encoding="utf-8", newline="")
    preimage = {
        "schema_version": "aide.preimage.v0",
        "preimage_id": f"preimage-{section_name}",
        "path": Path(relative_path).as_posix(),
        "exists": True,
        "sha256": compute_text_hash(before_text),
    }
    postimage = {
        "schema_version": "aide.postimage.v0",
        "postimage_id": f"postimage-{section_name}",
        "path": Path(relative_path).as_posix(),
        "exists": True,
        "sha256": compute_text_hash(after_text),
    }
    rollback = {
        "schema_version": "aide.rollback-record.v0",
        "rollback_id": f"rollback-{section_name}",
        "mode": "fixture_only",
        "preimage_ref": preimage["preimage_id"],
        "postimage_ref": postimage["postimage_id"],
        "restore_text_hash": preimage["sha256"],
        "apply_allowed": False,
        "rollback_execution": False,
    }
    return {
        "status": "patched_fixture",
        "operation": operation,
        "patch": patch,
        "preimage": preimage,
        "postimage": postimage,
        "rollback": rollback,
        "manual_content_preserved": operation["manual_content_preserved"],
        "before_hash": preimage["sha256"],
        "after_hash": postimage["sha256"],
        "no_real_apply_boundary": True,
        "real_repo_apply_allowed": False,
    }
