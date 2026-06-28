"""Fixture operation execution for DistributionApplyEngine v0."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.distribution.temp_workspace import safe_join, sha256_text


ALLOWED_OPERATION_CLASSES = {
    "add_managed_file",
    "update_managed_file",
    "remove_managed_file",
    "add_managed_section",
    "update_managed_section",
    "remove_managed_section",
    "preserve_project_owned",
    "preserve_project_overlay",
    "preserve_local_only",
    "preserve_runtime_generated",
    "preserve_evidence_only",
    "preserve_legacy",
    "manual_review_required",
    "refuse",
}

PROTECTED_OWNERSHIP = {
    "project_owned": "distribution_apply_engine.project_owned_overwrite_refused",
    "project_overlay": "distribution_apply_engine.project_overlay_overwrite_refused",
    "local_only": "distribution_apply_engine.local_only_overwrite_refused",
    "runtime_generated": "distribution_apply_engine.runtime_generated_overwrite_refused",
    "evidence_only": "distribution_apply_engine.evidence_only_overwrite_refused",
    "never_touch": "distribution_apply_engine.never_touch_update_refused",
    "unknown": "distribution_apply_engine.unknown_ownership_update_refused",
}

WRITE_OPERATION_CLASSES = {
    "add_managed_file",
    "update_managed_file",
    "remove_managed_file",
    "add_managed_section",
    "update_managed_section",
    "remove_managed_section",
}


def _failure(code: str, message: str, operation: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "status": "FAILED_VALIDATION",
        "refusal_code": code,
        "message": message,
        "operation_ref": operation.get("operation_ref") if operation else None,
        "target_relative_path": operation.get("target_relative_path") if operation else None,
    }


def _path_refusal(path: str) -> str | None:
    normalized = path.replace("\\", "/")
    if normalized.startswith("/") or normalized.startswith("//") or (len(normalized) >= 3 and normalized[1] == ":" and normalized[2] == "/"):
        return "distribution_apply_engine.absolute_path_refused"
    if any(part == ".." for part in normalized.split("/")):
        return "distribution_apply_engine.path_traversal_refused"
    if ".aide/context/latest-" in normalized or ".aide/reports/latest-" in normalized:
        return "distribution_apply_engine.source_latest_output_refused"
    return None


def _content(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _verify_preimage(path: Path, operation: dict[str, Any]) -> dict[str, Any] | None:
    operation_class = str(operation.get("operation_class"))
    if operation_class.startswith("add_"):
        return None
    if operation.get("preimage_missing"):
        return _failure("distribution_apply_engine.missing_preimage_refused", "preimage is marked missing", operation)
    if not path.exists():
        return _failure("distribution_apply_engine.missing_preimage_refused", "target preimage file is missing", operation)
    expected = operation.get("preimage_digest") or sha256_text(str(operation.get("preimage", _content(path))))
    observed = sha256_text(_content(path))
    if operation.get("preimage_digest_mismatch") or expected != observed:
        return _failure("distribution_apply_engine.preimage_digest_mismatch_refused", "preimage digest mismatch", operation)
    return None


def _verify_postimage(path: Path, operation: dict[str, Any]) -> dict[str, Any] | None:
    expected = operation.get("postimage_digest")
    if not expected:
        return None
    observed = sha256_text(_content(path)) if path.exists() else sha256_text("")
    if operation.get("postimage_digest_mismatch") or expected != observed:
        return _failure("distribution_apply_engine.postimage_digest_mismatch_refused", "postimage digest mismatch", operation)
    return None


def _replace_section(content: str, identity: str, section_content: str) -> str | None:
    begin = f"# AIDE:BEGIN {identity}"
    end = f"# AIDE:END {identity}"
    start = content.find(begin)
    finish = content.find(end)
    if start < 0 or finish < 0 or finish < start:
        return None
    finish += len(end)
    return content[:start] + begin + "\n" + section_content + "\n" + end + content[finish:]


def _remove_section(content: str, identity: str) -> str | None:
    begin = f"# AIDE:BEGIN {identity}"
    end = f"# AIDE:END {identity}"
    start = content.find(begin)
    finish = content.find(end)
    if start < 0 or finish < 0 or finish < start:
        return None
    finish += len(end)
    left = content[:start].rstrip()
    right = content[finish:].lstrip()
    return (left + "\n" + right).strip() + "\n"


def execute_operation(workspace_root: Path, operation: dict[str, Any]) -> dict[str, Any]:
    operation_class = str(operation.get("operation_class"))
    target_path = str(operation.get("target_relative_path", ""))
    ownership_class = str(operation.get("ownership_class", "unknown"))
    path_code = _path_refusal(target_path)
    if path_code:
        return _failure(path_code, "unsafe path refused", operation)
    if operation_class == "regenerate_project_output":
        return _failure("distribution_apply_engine.regenerate_project_output_refused", "regeneration is unsupported in v0", operation)
    if operation_class not in ALLOWED_OPERATION_CLASSES:
        return _failure("distribution_apply_engine.unsupported_operation_refused", "unsupported operation class", operation)
    if operation.get("operation_not_in_plan"):
        return _failure("distribution_apply_engine.operation_not_in_plan_refused", "operation is not in the accepted UpdatePlan fixture", operation)
    if operation.get("symlink_reparse_uncertain"):
        return _failure("distribution_apply_engine.symlink_reparse_refused", "symlink or reparse uncertainty", operation)
    if operation.get("missing_rollback_requirement"):
        return _failure("distribution_apply_engine.missing_rollback_requirement_refused", "rollback requirement missing", operation)
    if operation_class in WRITE_OPERATION_CLASSES and not operation.get("rollback_covered", False):
        return _failure("distribution_apply_engine.operation_lacking_rollback_coverage_refused", "rollback coverage missing", operation)
    if operation_class in WRITE_OPERATION_CLASSES and ownership_class in PROTECTED_OWNERSHIP:
        return _failure(PROTECTED_OWNERSHIP[ownership_class], "protected ownership refused", operation)
    if operation_class in {"manual_review_required", "refuse"}:
        return {
            "status": "SKIPPED",
            "operation_ref": operation.get("operation_ref"),
            "receipt_class": "manual_review_recorded" if operation_class == "manual_review_required" else "operation_refused",
            "target_relative_path": target_path,
        }
    target = safe_join(workspace_root, target_path)
    preimage_failure = _verify_preimage(target, operation)
    if preimage_failure:
        return preimage_failure
    if operation_class == "add_managed_file":
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(operation.get("postimage", "")), encoding="utf-8", newline="\n")
        receipt_class = "managed_file_added"
    elif operation_class == "update_managed_file":
        target.write_text(str(operation.get("postimage", "")), encoding="utf-8", newline="\n")
        receipt_class = "managed_file_updated"
    elif operation_class == "remove_managed_file":
        target.unlink()
        receipt_class = "managed_file_removed"
    elif operation_class == "add_managed_section":
        target.parent.mkdir(parents=True, exist_ok=True)
        base = _content(target)
        identity = str(operation.get("section_identity", "section"))
        section = f"# AIDE:BEGIN {identity}\n{operation.get('section_content', '')}\n# AIDE:END {identity}\n"
        target.write_text(base + ("" if base.endswith("\n") or not base else "\n") + section, encoding="utf-8", newline="\n")
        receipt_class = "managed_section_added"
    elif operation_class == "update_managed_section":
        identity = str(operation.get("section_identity", "section"))
        replaced = _replace_section(_content(target), identity, str(operation.get("section_content", "")))
        if replaced is None:
            return _failure("distribution_apply_engine.missing_preimage_refused", "managed section preimage missing", operation)
        target.write_text(replaced, encoding="utf-8", newline="\n")
        receipt_class = "managed_section_updated"
    elif operation_class == "remove_managed_section":
        identity = str(operation.get("section_identity", "section"))
        replaced = _remove_section(_content(target), identity)
        if replaced is None:
            return _failure("distribution_apply_engine.missing_preimage_refused", "managed section preimage missing", operation)
        target.write_text(replaced, encoding="utf-8", newline="\n")
        receipt_class = "managed_section_removed"
    else:
        receipt_class = operation_class.replace("preserve_", "") + "_preserved"
    postimage_failure = _verify_postimage(target, operation)
    if postimage_failure:
        return postimage_failure
    return {
        "status": "APPLIED_TEMP",
        "operation_ref": operation.get("operation_ref"),
        "receipt_class": receipt_class,
        "target_relative_path": target_path,
        "preimage_digest": operation.get("preimage_digest"),
        "postimage_digest": operation.get("postimage_digest"),
    }


def detect_case_collisions(paths: list[str]) -> list[str]:
    seen: dict[str, str] = {}
    collisions: list[str] = []
    for path in paths:
        folded = path.replace("\\", "/").lower()
        if folded in seen and seen[folded] != path:
            collisions.append(path)
        seen[folded] = path
    return collisions
