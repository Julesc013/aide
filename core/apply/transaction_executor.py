"""Scoped transaction executor v0.

This module executes explicit transaction plans only. It is intentionally
bounded to managed-section updates, report/validate/noop operations, explicit
path allowlists, preimage hash checks, postimage verification, staged-change
records, and rollback-compatible records.
"""

from __future__ import annotations

import json
import re
import importlib.util
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from core.apply import managed_sections
except ModuleNotFoundError:
    _managed_sections_path = Path(__file__).with_name("managed_sections.py")
    _managed_sections_spec = importlib.util.spec_from_file_location("aide_core_managed_sections_fallback", _managed_sections_path)
    if _managed_sections_spec is None or _managed_sections_spec.loader is None:
        raise
    managed_sections = importlib.util.module_from_spec(_managed_sections_spec)
    _managed_sections_spec.loader.exec_module(managed_sections)


PLAN_SCHEMA_VERSION = "aide.scoped-transaction-plan.v0"
REPORT_SCHEMA_VERSION = "aide.scoped-transaction-executor-report.v0"
ROLLBACK_SCHEMA_VERSION = "aide.scoped-transaction-rollback-record.v0"
STAGED_CHANGE_SCHEMA_VERSION = "aide.scoped-transaction-staged-change.v0"

ALLOWED_OPERATION_TYPES = frozenset({"update_managed_section", "report", "validate", "noop"})
MUTATING_OPERATION_TYPES = frozenset({"update_managed_section"})
FORBIDDEN_OPERATION_TYPES = frozenset(
    {
        "install",
        "install_apply",
        "upgrade",
        "upgrade_apply",
        "repair",
        "repair_apply",
        "rollback",
        "rollback_apply",
        "uninstall",
        "uninstall_apply",
        "target_repo_mutation",
        "branch_mutation",
        "worktree_mutation",
        "merge",
        "push",
        "promotion",
        "release_publication",
        "github_mutation",
        "provider_model_call",
        "gateway_call",
        "network_call",
        "delete",
        "move",
        "broad_delete",
        "broad_move",
        "broad_active_repo_apply",
    }
)
DEFAULT_PROTECTED_ROOTS = (
    ".git",
    ".github",
    ".aide.local",
    ".env",
    ".env.*",
    "secrets",
    "credentials",
    ".aide/release/dist",
    ".aide/release/github-release-*",
    ".aide/release/latest-github-release-draft.*",
)


class ScopedTransactionError(ValueError):
    """Raised when a transaction plan is not structurally executable."""


def compute_text_hash(text: str) -> str:
    """Return the repo-standard managed-section text hash."""

    return managed_sections.compute_text_hash(text)


def load_transaction_plan(path: str | Path) -> dict[str, Any]:
    """Load an explicit JSON transaction plan."""

    plan_path = Path(path)
    try:
        data = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ScopedTransactionError(f"transaction plan could not be loaded: {exc}") from exc
    if not isinstance(data, dict):
        raise ScopedTransactionError("transaction plan root must be an object")
    return data


def execute_plan_file(
    plan_path: str | Path,
    repo_root: str | Path,
    *,
    write_outputs: bool = True,
) -> dict[str, Any]:
    """Load and execute a transaction plan file."""

    return execute_transaction_plan(load_transaction_plan(plan_path), repo_root, write_outputs=write_outputs)


def execute_transaction_plan(
    plan: dict[str, Any],
    repo_root: str | Path,
    *,
    write_outputs: bool = True,
) -> dict[str, Any]:
    """Execute a scoped transaction plan and return the final report.

    Dry-run and report modes never mutate target files. Apply mode is explicit
    and still runs all planning checks before writing any target file.
    """

    root = Path(repo_root).resolve()
    context = _ExecutionContext(plan=plan, repo_root=root)
    report = context.initial_report()

    plan_errors = context.validate_plan_shape()
    if plan_errors:
        report["status"] = "BLOCKED"
        report["result"] = "BLOCKED_MALFORMED_PLAN"
        report["blockers"] = plan_errors
        context.write_available_outputs(report, write_outputs)
        return report

    operation_results: list[dict[str, Any]] = []
    staged_changes: list[dict[str, Any]] = []
    rollback_preimages: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []

    for index, operation in enumerate(context.operations):
        result = context.plan_operation(operation, index)
        operation_results.append(result.operation_report)
        if result.blocker is not None:
            blockers.append(result.blocker)
        if result.staged_change is not None:
            staged_changes.append(result.staged_change)
        if result.rollback_preimage is not None:
            rollback_preimages.append(result.rollback_preimage)

    rollback_record = context.rollback_record(rollback_preimages, staged_changes)
    report["operations"] = operation_results
    report["staged_changes"] = staged_changes
    report["rollback_record"] = rollback_record
    report["records"] = {
        "transaction_plan_record": context.transaction_plan_record(),
        "staged_change_count": len(staged_changes),
        "rollback_compatible_record": True,
        "final_report_record": True,
    }

    if blockers:
        report["status"] = "BLOCKED"
        report["result"] = _first_blocker_class(blockers)
        report["blockers"] = blockers
        context.write_available_outputs(report, write_outputs)
        return report

    if context.mode == "apply" and len(staged_changes) > 1:
        blocker = _blocker(
            "BLOCKED_MULTI_OPERATION_APPLY_NOT_ATOMIC",
            "operations",
            "scoped transaction executor v0 applies at most one mutating operation per transaction",
        )
        report["status"] = "BLOCKED"
        report["result"] = "BLOCKED_MULTI_OPERATION_APPLY_NOT_ATOMIC"
        report["blockers"] = [blocker]
        for operation_report in report["operations"]:
            if operation_report.get("operation_type") in MUTATING_OPERATION_TYPES:
                operation_report["status"] = "blocked"
        context.write_available_outputs(report, write_outputs)
        return report

    if context.mode == "apply":
        apply_blockers = context.apply_staged_changes(staged_changes)
        if apply_blockers:
            report["status"] = "FAILED_VALIDATION"
            report["result"] = "FAILED_POSTIMAGE_VERIFICATION"
            report["blockers"] = apply_blockers
            for operation_report in report["operations"]:
                if operation_report.get("operation_type") in MUTATING_OPERATION_TYPES:
                    operation_report["status"] = "failed_validation"
            context.write_available_outputs(report, write_outputs)
            return report
        report["target_files_mutated"] = bool(staged_changes)
    else:
        report["target_files_mutated"] = False

    for operation_report in report["operations"]:
        if operation_report.get("status") == "planned":
            operation_report["status"] = "applied" if context.mode == "apply" else "dry_run_planned"
    for staged_change in staged_changes:
        staged_change["verification_status"] = "verified" if context.mode == "apply" else "planned"

    report["status"] = "PASS"
    report["result"] = "PASS"
    report["blockers"] = []
    context.write_available_outputs(report, write_outputs)
    return report


class _OperationPlanResult:
    def __init__(
        self,
        operation_report: dict[str, Any],
        staged_change: dict[str, Any] | None = None,
        rollback_preimage: dict[str, Any] | None = None,
        blocker: dict[str, Any] | None = None,
    ) -> None:
        self.operation_report = operation_report
        self.staged_change = staged_change
        self.rollback_preimage = rollback_preimage
        self.blocker = blocker


class _ExecutionContext:
    def __init__(self, plan: dict[str, Any], repo_root: Path) -> None:
        self.plan = plan
        self.repo_root = repo_root
        self.mode = _normalize_mode(plan.get("mode", ""))
        self.transaction_id = str(plan.get("transaction_id", ""))
        self.run_id = str(plan.get("run_id") or f"{self.transaction_id}-run")
        self.allowed_roots = _normalize_root_list(plan.get("allowed_roots", []))
        self.allowed_paths = _normalize_allowed_paths(plan.get("allowed_paths", []))
        self.protected_roots = _normalize_root_list([*DEFAULT_PROTECTED_ROOTS, *list(plan.get("protected_roots", []))])
        self.allowed_operation_types = _normalize_operation_allowlist(plan.get("allowed_operation_types", ALLOWED_OPERATION_TYPES))
        self.operations = plan.get("operations", []) if isinstance(plan.get("operations"), list) else []

    def initial_report(self) -> dict[str, Any]:
        return {
            "schema_version": REPORT_SCHEMA_VERSION,
            "transaction_id": self.transaction_id,
            "run_id": self.run_id,
            "generated_at": _timestamp(self.plan),
            "mode": self.mode or str(self.plan.get("mode", "")),
            "capability_reality": {
                "state": "implemented_tested_review_gated",
                "production_ready": False,
                "release_ready": False,
                "target_repo_capable": False,
                "broad_active_repo_apply": False,
            },
            "boundaries": {
                "scoped_transaction_executor": True,
                "dry_run_no_target_mutation": self.mode != "apply",
                "apply_mode_explicit": self.mode == "apply",
                "allowed_paths_enforced": True,
                "protected_paths_enforced": True,
                "forbidden_operations_enforced": True,
                "install_apply": False,
                "upgrade_apply": False,
                "repair_apply": False,
                "rollback_uninstall_apply": False,
                "target_repo_mutation": False,
                "branch_worktree_mutation": False,
                "merge": False,
                "push": False,
                "promotion": False,
                "release_publication": False,
                "github_mutation": False,
                "provider_model_calls": "none",
                "gateway_calls": "none",
                "network_calls": "none",
                "broad_active_repo_apply": False,
            },
            "operation_allowlist": sorted(self.allowed_operation_types),
            "allowed_roots": self.allowed_roots,
            "allowed_paths": self.allowed_paths,
            "protected_roots": self.protected_roots,
            "target_files_mutated": False,
            "rollback_execution": False,
            "review_gate": "needs_review",
        }

    def validate_plan_shape(self) -> list[dict[str, Any]]:
        blockers: list[dict[str, Any]] = []
        if self.plan.get("schema_version") != PLAN_SCHEMA_VERSION:
            blockers.append(_blocker("BLOCKED_MALFORMED_PLAN", "plan", "unsupported or missing plan schema_version"))
        if not self.transaction_id:
            blockers.append(_blocker("BLOCKED_MALFORMED_PLAN", "transaction_id", "missing transaction_id"))
        if self.mode not in {"dry_run", "report", "apply"}:
            blockers.append(_blocker("BLOCKED_MALFORMED_PLAN", "mode", "mode must be dry-run, report, or apply"))
        if not self.allowed_roots and not self.allowed_paths:
            blockers.append(_blocker("BLOCKED_ALLOWED_PATH", "allowed_roots", "missing explicit allowed roots or allowed paths"))
        if not isinstance(self.plan.get("protected_roots", []), list):
            blockers.append(_blocker("BLOCKED_PROTECTED_PATH", "protected_roots", "protected_roots must be a list"))
        if not isinstance(self.plan.get("operations"), list) or not self.operations:
            blockers.append(_blocker("BLOCKED_MALFORMED_PLAN", "operations", "operations must be a non-empty explicit list"))
        if not self._output_path_valid("report_path"):
            blockers.append(_blocker("BLOCKED_ALLOWED_PATH", "report_path", "report_path must be repo-relative and inside allowed paths"))
        if not self._output_path_valid("rollback_record_path"):
            blockers.append(_blocker("BLOCKED_ALLOWED_PATH", "rollback_record_path", "rollback_record_path must be repo-relative and inside allowed paths"))
        if not self.allowed_operation_types or not self.allowed_operation_types.issubset(ALLOWED_OPERATION_TYPES):
            blockers.append(_blocker("BLOCKED_PROHIBITED_OPERATION", "allowed_operation_types", "operation allowlist contains unsupported operations"))
        return blockers

    def plan_operation(self, operation: Any, index: int) -> _OperationPlanResult:
        if not isinstance(operation, dict):
            blocker = _blocker("BLOCKED_MALFORMED_PLAN", f"operations[{index}]", "operation must be an object")
            return _OperationPlanResult({"operation_index": index, "status": "blocked"}, blocker=blocker)
        operation_id = str(operation.get("operation_id") or f"operation-{index}")
        op_type, op_type_blocker = self._operation_type(operation, operation_id)
        base_report = {
            "operation_index": index,
            "operation_id": operation_id,
            "operation_type": op_type,
            "status": "blocked" if op_type_blocker else "planned",
        }
        if op_type_blocker is not None:
            return _OperationPlanResult(base_report, blocker=op_type_blocker)
        if op_type in {"noop", "report", "validate"}:
            base_report["status"] = "planned"
            base_report["validation_status"] = "pass"
            return _OperationPlanResult(base_report)
        return self._plan_managed_section_update(operation, operation_id, base_report)

    def _plan_managed_section_update(
        self,
        operation: dict[str, Any],
        operation_id: str,
        base_report: dict[str, Any],
    ) -> _OperationPlanResult:
        path_value = operation.get("path")
        path_result = self.validate_target_path(path_value)
        base_report["path"] = path_result.get("path", str(path_value or ""))
        if path_result.get("blocker"):
            return _OperationPlanResult(base_report, blocker=path_result["blocker"])

        rel_path = str(path_result["path"])
        target = path_result["resolved_path"] if isinstance(path_result.get("resolved_path"), Path) else self.repo_root / rel_path
        section_name = str(operation.get("section_name") or operation.get("section_id") or "")
        if not section_name:
            blocker = _blocker("BLOCKED_MANAGED_SECTION", rel_path, "missing managed-section section_name")
            return _OperationPlanResult(base_report, blocker=blocker)
        marker_family = operation.get("marker_family")
        if marker_family not in (None, managed_sections.MARKER_FAMILY):
            blocker = _blocker("BLOCKED_MANAGED_SECTION", rel_path, "ambiguous marker ownership or unsupported marker family")
            return _OperationPlanResult(base_report, blocker=blocker)
        replacement = operation.get("replacement_content", operation.get("replacement"))
        if not isinstance(replacement, str):
            blocker = _blocker("BLOCKED_MANAGED_SECTION", rel_path, "missing replacement_content")
            return _OperationPlanResult(base_report, blocker=blocker)
        expected_preimage_hash = operation.get("expected_preimage_hash")
        if not isinstance(expected_preimage_hash, str) or not expected_preimage_hash:
            blocker = _blocker("BLOCKED_PREIMAGE_HASH_MISSING", rel_path, "missing expected_preimage_hash")
            return _OperationPlanResult(base_report, blocker=blocker)

        try:
            before_text = managed_sections.load_text_file_safely(target)
        except (OSError, managed_sections.ManagedSectionError) as exc:
            blocker = _blocker("BLOCKED_MANAGED_SECTION", rel_path, f"file cannot be read safely: {exc}")
            return _OperationPlanResult(base_report, blocker=blocker)

        preimage_hash = compute_text_hash(before_text)
        base_report["preimage_hash"] = preimage_hash
        if preimage_hash != expected_preimage_hash:
            blocker = _blocker("BLOCKED_PREIMAGE_HASH_MISMATCH", rel_path, "actual preimage hash did not match expected_preimage_hash")
            base_report["expected_preimage_hash"] = expected_preimage_hash
            return _OperationPlanResult(base_report, blocker=blocker)

        patch = managed_sections.build_managed_section_patch(
            before_text,
            section_name,
            replacement,
            marker_family=marker_family,
            path=rel_path,
        )
        if patch.get("status") != "planned":
            conflicts = patch.get("conflicts", [])
            conflict_classes = [str(conflict.get("conflict_class", "unknown")) for conflict in conflicts if isinstance(conflict, dict)]
            blocker = _blocker(
                "BLOCKED_MANAGED_SECTION",
                rel_path,
                "managed-section patch blocked: " + ", ".join(conflict_classes or ["unknown"]),
                conflicts=conflicts if isinstance(conflicts, list) else [],
            )
            base_report["managed_section_conflicts"] = conflict_classes
            return _OperationPlanResult(base_report, blocker=blocker)

        after_text = str(patch.get("after_text", ""))
        postimage_hash = compute_text_hash(after_text)
        expected_postimage_content = operation.get("expected_postimage") or operation.get("expected_postimage_content")
        expected_postimage_hash = operation.get("expected_postimage_hash")
        if isinstance(expected_postimage_content, str) and compute_text_hash(expected_postimage_content) != postimage_hash:
            blocker = _blocker("FAILED_POSTIMAGE_VERIFICATION", rel_path, "expected postimage content did not match planned postimage")
            return _OperationPlanResult(base_report, blocker=blocker)
        if isinstance(expected_postimage_hash, str) and expected_postimage_hash and expected_postimage_hash != postimage_hash:
            blocker = _blocker("FAILED_POSTIMAGE_VERIFICATION", rel_path, "expected_postimage_hash did not match planned postimage")
            base_report["expected_postimage_hash"] = expected_postimage_hash
            base_report["planned_postimage_hash"] = postimage_hash
            return _OperationPlanResult(base_report, blocker=blocker)

        change_id = str(operation.get("change_id") or f"stage-{operation_id}")
        rollback_ref = f"rollback-{operation_id}"
        staged_change = {
            "schema_version": STAGED_CHANGE_SCHEMA_VERSION,
            "change_id": change_id,
            "transaction_id": self.transaction_id,
            "operation_id": operation_id,
            "operation_type": "update_managed_section",
            "path": rel_path,
            "section_name": section_name,
            "preimage_hash": preimage_hash,
            "postimage_hash": postimage_hash,
            "rollback_ref": rollback_ref,
            "verification_status": "planned",
            "manual_content_preserved": bool(patch.get("operation", {}).get("manual_content_preserved", False)),
            "planned_postimage": after_text,
        }
        rollback_preimage = {
            "rollback_ref": rollback_ref,
            "path": rel_path,
            "exists": True,
            "preimage_hash": preimage_hash,
            "postimage_hash": postimage_hash,
            "operation_id": operation_id,
        }
        base_report.update(
            {
                "status": "planned",
                "section_name": section_name,
                "preimage_hash": preimage_hash,
                "postimage_hash": postimage_hash,
                "staged_change_ref": change_id,
                "rollback_ref": rollback_ref,
                "manual_content_preserved": staged_change["manual_content_preserved"],
                "postimage_verification": "planned",
            }
        )
        return _OperationPlanResult(base_report, staged_change=staged_change, rollback_preimage=rollback_preimage)

    def apply_staged_changes(self, staged_changes: list[dict[str, Any]]) -> list[dict[str, Any]]:
        blockers: list[dict[str, Any]] = []
        write_targets: list[tuple[dict[str, Any], Path]] = []
        for staged_change in staged_changes:
            rel_path = str(staged_change["path"])
            path_result = self.validate_target_path(rel_path)
            if path_result.get("blocker"):
                blockers.append(path_result["blocker"])
                staged_change["verification_status"] = "blocked"
                continue
            target = path_result["resolved_path"] if isinstance(path_result.get("resolved_path"), Path) else self.repo_root / rel_path
            write_targets.append((staged_change, target))
        if blockers:
            return blockers

        for staged_change, target in write_targets:
            rel_path = str(staged_change["path"])
            try:
                target.write_text(str(staged_change["planned_postimage"]), encoding="utf-8", newline="")
                actual_hash = compute_text_hash(target.read_text(encoding="utf-8"))
            except OSError as exc:
                blockers.append(_blocker("FAILED_POSTIMAGE_VERIFICATION", rel_path, f"postimage could not be written or read safely: {exc}"))
                staged_change["verification_status"] = "failed"
                continue
            staged_change["actual_postimage_hash"] = actual_hash
            if actual_hash != staged_change.get("postimage_hash"):
                blockers.append(_blocker("FAILED_POSTIMAGE_VERIFICATION", rel_path, "actual postimage hash did not match planned postimage"))
                staged_change["verification_status"] = "failed"
            else:
                staged_change["verification_status"] = "verified"
        return blockers

    def rollback_record(self, preimages: list[dict[str, Any]], staged_changes: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "schema_version": ROLLBACK_SCHEMA_VERSION,
            "rollback_id": str(self.plan.get("rollback_id") or f"rollback-{self.transaction_id}"),
            "transaction_id": self.transaction_id,
            "mode": self.mode,
            "preimages": preimages,
            "inverse_operations": [
                {
                    "operation_id": f"inverse-{change['operation_id']}",
                    "operation_type": "update_managed_section",
                    "path": change["path"],
                    "restore_text_hash": change["preimage_hash"],
                    "apply_allowed": False,
                }
                for change in staged_changes
            ],
            "rollback_execution": False,
            "apply_allowed": False,
            "review_required": True,
        }

    def transaction_plan_record(self) -> dict[str, Any]:
        return {
            "schema_version": PLAN_SCHEMA_VERSION,
            "transaction_id": self.transaction_id,
            "mode": self.mode,
            "operation_count": len(self.operations),
            "allowed_roots": self.allowed_roots,
            "allowed_paths": self.allowed_paths,
            "protected_roots": self.protected_roots,
            "operation_allowlist": sorted(self.allowed_operation_types),
        }

    def validate_target_path(self, path_value: Any) -> dict[str, Any]:
        try:
            rel_path = _normalize_relative_path(path_value, "path")
        except ScopedTransactionError as exc:
            return {"path": str(path_value or ""), "blocker": _blocker("BLOCKED_ALLOWED_PATH", "path", str(exc))}
        if _is_path_protected(rel_path, self.protected_roots):
            return {"path": rel_path, "blocker": _blocker("BLOCKED_PROTECTED_PATH", rel_path, "path is protected")}
        if not _is_path_allowed(rel_path, self.allowed_roots, self.allowed_paths):
            return {"path": rel_path, "blocker": _blocker("BLOCKED_ALLOWED_PATH", rel_path, "path is outside allowed roots and allowed paths")}
        resolved_result = self._resolved_path_result(rel_path, "path")
        if resolved_result.get("blocker"):
            return {"path": rel_path, "blocker": resolved_result["blocker"]}
        return {"path": rel_path, "resolved_path": resolved_result["resolved_path"], "resolved_repo_path": resolved_result["resolved_repo_path"]}

    def _output_path_valid(self, key: str) -> bool:
        value = self.plan.get(key)
        if not isinstance(value, str) or not value:
            return False
        try:
            rel_path = _normalize_relative_path(value, key)
        except ScopedTransactionError:
            return False
        if _is_path_protected(rel_path, self.protected_roots) or not _is_path_allowed(rel_path, self.allowed_roots, self.allowed_paths):
            return False
        return not bool(self._resolved_path_result(rel_path, key).get("blocker"))

    def _operation_type(self, operation: dict[str, Any], operation_id: str) -> tuple[str, dict[str, Any] | None]:
        raw_type = operation.get("operation_type")
        raw_class = operation.get("operation_class")
        if raw_type and raw_class and str(raw_type) != str(raw_class):
            return "", _blocker("BLOCKED_PROHIBITED_OPERATION", operation_id, "ambiguous operation type and operation_class")
        op_type = str(raw_type or raw_class or "")
        if not op_type:
            return "", _blocker("BLOCKED_PROHIBITED_OPERATION", operation_id, "missing operation type")
        if op_type in FORBIDDEN_OPERATION_TYPES or op_type not in self.allowed_operation_types:
            return op_type, _blocker("BLOCKED_PROHIBITED_OPERATION", operation_id, f"unsupported or forbidden operation type: {op_type}")
        return op_type, None

    def write_available_outputs(self, report: dict[str, Any], write_outputs: bool) -> None:
        if not write_outputs:
            return
        rollback_path = self._validated_output_path("rollback_record_path")
        if rollback_path is not None:
            report["rollback_record_path"] = _repo_relative(self.repo_root, rollback_path)
            rollback_path.parent.mkdir(parents=True, exist_ok=True)
            rollback_path.write_text(_stable_json(report.get("rollback_record", {})), encoding="utf-8", newline="\n")
        report_path = self._validated_output_path("report_path")
        if report_path is not None:
            report["report_path"] = _repo_relative(self.repo_root, report_path)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(_stable_json(report), encoding="utf-8", newline="\n")

    def _validated_output_path(self, key: str) -> Path | None:
        value = self.plan.get(key)
        if not isinstance(value, str):
            return None
        try:
            rel_path = _normalize_relative_path(value, key)
        except ScopedTransactionError:
            return None
        if _is_path_protected(rel_path, self.protected_roots):
            return None
        if not _is_path_allowed(rel_path, self.allowed_roots, self.allowed_paths):
            return None
        resolved_result = self._resolved_path_result(rel_path, key)
        if resolved_result.get("blocker"):
            return None
        resolved_path = resolved_result.get("resolved_path")
        return resolved_path if isinstance(resolved_path, Path) else self.repo_root / rel_path

    def _resolved_path_result(self, rel_path: str, label: str) -> dict[str, Any]:
        candidate = self.repo_root / rel_path
        try:
            repo_root = self.repo_root.resolve()
            resolved = candidate.resolve(strict=False)
            resolved_rel = resolved.relative_to(repo_root).as_posix()
        except (OSError, RuntimeError, ValueError) as exc:
            return {
                "path": rel_path,
                "blocker": _blocker(
                    "BLOCKED_RESOLVED_PATH_ESCAPE",
                    rel_path,
                    f"{label} resolved path escaped repo boundary or could not be determined safely: {exc}",
                ),
            }
        if not _is_resolved_repo_path_safe(resolved_rel, self.allowed_roots, self.allowed_paths, self.protected_roots):
            return {
                "path": rel_path,
                "blocker": _blocker(
                    "BLOCKED_RESOLVED_PATH_ESCAPE",
                    rel_path,
                    f"{label} resolved path is outside allowed paths or inside protected paths: {resolved_rel}",
                ),
            }
        return {"path": rel_path, "resolved_path": resolved, "resolved_repo_path": resolved_rel}


def _normalize_mode(mode: Any) -> str:
    value = str(mode or "").strip().lower().replace("_", "-")
    if value == "dry-run":
        return "dry_run"
    return value


def _normalize_root_list(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    roots: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value:
            continue
        if any(ch in value for ch in "\0"):
            continue
        normalized = value.replace("\\", "/").strip("/")
        if not normalized or normalized == ".":
            continue
        roots.append(normalized)
    return sorted(dict.fromkeys(roots))


def _normalize_allowed_paths(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    paths: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value:
            continue
        normalized = value.replace("\\", "/").strip("/")
        if not normalized or normalized == ".":
            continue
        paths.append(normalized)
    return sorted(dict.fromkeys(paths))


def _normalize_operation_allowlist(values: Any) -> frozenset[str]:
    if not isinstance(values, (list, tuple, set, frozenset)):
        return frozenset()
    return frozenset(str(value) for value in values if isinstance(value, str))


def _normalize_relative_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ScopedTransactionError(f"{label} must be a non-empty repo-relative path")
    raw = value.replace("\\", "/")
    if "\0" in raw:
        raise ScopedTransactionError(f"{label} contains NUL byte")
    if raw.startswith("/") or raw.startswith("~") or re.match(r"^[A-Za-z]:", raw):
        raise ScopedTransactionError(f"{label} must not be absolute")
    if any(ch in raw for ch in "*?[]"):
        raise ScopedTransactionError(f"{label} must not contain wildcard or bulk expansion characters")
    path = PurePosixPath(raw)
    if any(part == ".." for part in path.parts):
        raise ScopedTransactionError(f"{label} must not contain path traversal")
    if str(path) in {"", "."}:
        raise ScopedTransactionError(f"{label} must not be repo root")
    return path.as_posix()


def _is_path_allowed(path: str, allowed_roots: list[str], allowed_paths: list[str]) -> bool:
    for allowed_path in allowed_paths:
        if allowed_path.endswith("/**"):
            prefix = allowed_path[:-3].rstrip("/")
            if path == prefix or path.startswith(prefix + "/"):
                return True
        elif path == allowed_path:
            return True
    for root in allowed_roots:
        if path == root or path.startswith(root.rstrip("/") + "/"):
            return True
    return False


def _is_path_protected(path: str, protected_roots: list[str]) -> bool:
    for root in protected_roots:
        if root.endswith(".*"):
            prefix = root[:-1]
            if path.startswith(prefix):
                return True
        if root.endswith("*"):
            prefix = root[:-1]
            if path.startswith(prefix):
                return True
        if path == root or path.startswith(root.rstrip("/") + "/"):
            return True
    return False


def _is_resolved_repo_path_safe(path: str, allowed_roots: list[str], allowed_paths: list[str], protected_roots: list[str]) -> bool:
    return not _is_path_protected(path, protected_roots) and _is_path_allowed(path, allowed_roots, allowed_paths)


def _first_blocker_class(blockers: list[dict[str, Any]]) -> str:
    if not blockers:
        return "BLOCKED"
    return str(blockers[0].get("blocker_class", "BLOCKED"))


def _blocker(blocker_class: str, path: str, message: str, *, conflicts: list[Any] | None = None) -> dict[str, Any]:
    blocker = {
        "blocker_class": blocker_class,
        "path": path,
        "message": message,
        "apply_blocked": True,
    }
    if conflicts is not None:
        blocker["conflicts"] = conflicts
    return blocker


def _timestamp(plan: dict[str, Any]) -> str:
    if isinstance(plan.get("generated_at"), str) and plan["generated_at"]:
        return str(plan["generated_at"])
    if isinstance(plan.get("deterministic"), bool) and plan["deterministic"]:
        return "deterministic"
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def _repo_relative(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
