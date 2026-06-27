"""UpdatePlan v1 helpers.

UpdatePlan records a dry-run, reviewable distribution update plan. It decides
what would happen, but it is not an updater, installer, migration applier,
rollback applier, uninstaller, target scanner, target mutator, or release
publisher.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import distribution_manifest, envelope, install_record, migration_record, ownership_ledger, project_lock


API_VERSION = envelope.API_VERSION
KIND = "UpdatePlan"
SCHEMA_VERSION = "aide.update-plan.v1"
PROTOCOL_VERSION = "0.1.0"
TASK_ID = "AIDE-BUILD-UPDATE-PLAN-V1-01"
CHECK_TASK_ID = "AIDE-CHECK-UPDATE-PLAN-V1-01"
PROPOSED_CAPABILITY = "update_plan_v1"
DETERMINISTIC_TIMESTAMP = "fixture-timestamp:update-plan-v1"
DEFAULT_EVIDENCE_REF = "aide://evidence/update-plan-v1/source-projection"

REPORT_ROOT = Path(".aide/reports/update-plan-v1")
SCHEMA_PATH = Path(".aide/protocol/aide-update-plan-v1.schema.json")
FIXTURE_ROOT = Path(".aide/fixtures/update-plan-v1")

PROJECTION_JSON = REPORT_ROOT / "projection.json"
PROJECT_REPORT_JSON = REPORT_ROOT / "project-report.json"
STATUS_MD = REPORT_ROOT / "status.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FIXTURE_MATRIX_JSON = REPORT_ROOT / "fixture-matrix.json"
FIXTURE_MATRIX_MD = REPORT_ROOT / "fixture-matrix.md"
CONFLICT_SUMMARY_MD = REPORT_ROOT / "conflict-summary.md"
NO_APPLY_BOUNDARY_MD = REPORT_ROOT / "no-apply-boundary.md"

INSTALL_RECORD_ACCEPTANCE_JSON = Path(".aide/reports/install-record-v0-acceptance/acceptance-report.json")
MIGRATION_RECORD_ACCEPTANCE_JSON = Path(".aide/reports/migration-record-v0-acceptance/acceptance-report.json")

SUPPORTED_REQUIRED_FEATURES = {
    "update_plan_v1",
    "distribution_manifest_v1",
    "project_lock_v0",
    "ownership_ledger_v1",
    "install_record_v0",
    "migration_record_v0",
    "sha256_digest_canonical_json_v1",
    "no_apply_update_plan_v1",
}

SUPPORTED_OPTIONAL_FEATURES = {
    "manual_review_item_v0",
    "conflict_only_plan_v1",
    "project_overlay_preservation_v1",
}

SUPPORTED_OPERATION_CLASSES = {
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
    "regenerate_project_output",
    "manual_review_required",
    "refuse",
}

OWNERSHIP_PRESERVE_OPERATION = {
    "project_owned": "preserve_project_owned",
    "project_overlay": "preserve_project_overlay",
    "local_only": "preserve_local_only",
    "runtime_generated": "preserve_runtime_generated",
    "evidence_only": "preserve_evidence_only",
    "preserved_legacy": "preserve_legacy",
    "project_generated": "regenerate_project_output",
}

UNSAFE_OWNERSHIP_CLASSES = {
    "project_owned",
    "project_overlay",
    "local_only",
    "runtime_generated",
    "evidence_only",
    "preserved_legacy",
}

MANAGED_OPERATION_CLASSES = {
    "add_managed_file",
    "update_managed_file",
    "remove_managed_file",
    "add_managed_section",
    "update_managed_section",
    "remove_managed_section",
}

REFUSAL_CODES = [
    "update_plan.missing",
    "update_plan.invalid",
    "update_plan.distribution_missing",
    "update_plan.project_lock_missing",
    "update_plan.ownership_ledger_missing",
    "update_plan.install_record_missing",
    "update_plan.migration_record_missing",
    "update_plan.distribution_mismatch",
    "update_plan.project_lock_mismatch",
    "update_plan.ownership_ledger_mismatch",
    "update_plan.install_record_mismatch",
    "update_plan.migration_record_mismatch",
    "update_plan.unknown_ownership",
    "update_plan.never_touch_target",
    "update_plan.project_owned_overwrite",
    "update_plan.project_overlay_overwrite",
    "update_plan.local_only_overwrite",
    "update_plan.runtime_generated_overwrite",
    "update_plan.evidence_only_overwrite",
    "update_plan.case_collision",
    "update_plan.symlink_reparse_uncertain",
    "update_plan.absolute_path_forbidden",
    "update_plan.path_traversal_forbidden",
    "update_plan.source_state_contamination",
    "update_plan.source_output_as_target_truth",
    "update_plan.preimage_digest_missing",
    "update_plan.postimage_digest_missing",
    "update_plan.rollback_requirement_missing",
    "update_plan.unknown_required_feature",
    "update_plan.extension_required_unknown",
    "update_plan.apply_authority_claimed",
    "update_plan.target_mutation_claimed",
    "update_plan.evidence_missing",
    "update_plan.digest_mismatch",
    "update_plan.fixture_failure",
]

EXPLICIT_NON_CAPABILITIES = [
    "install_apply",
    "update_apply",
    "migration_apply",
    "repair_apply",
    "rollback_apply",
    "uninstall_apply",
    "target_repository_mutation",
    "target_scan_authority",
    "release_archive_creation",
    "release_publication",
    "git_tag_creation",
    "github_release_creation",
    "upload",
    "network_call",
    "provider_model_call",
    "workbench_runtime",
    "commander",
    "omnigent",
    "worker_execution",
    "preview_session_apply",
    "development_transaction_apply",
    "patch_transaction_apply",
    "branch_worktree_automation",
    "real_project_canary",
]

PATH_RE = re.compile(r"(^[A-Za-z]:[\\/])|(^\\\\)|(^/)|(^|/)\.\.($|/)")
SOURCE_OUTPUT_RE = re.compile(r"(^|/)\.aide/(context|reports|repo|roots|tools|install|repair|upgrade|rollback|uninstall)/latest[-_/]", re.IGNORECASE)


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def canonical_json_bytes(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, data: Any) -> None:
    write_text(path, stable_json(data))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schema(repo_root: str | Path = ".") -> dict[str, Any]:
    return load_json(Path(repo_root) / SCHEMA_PATH)


def load_distribution_manifest(repo_root: str | Path = ".") -> dict[str, Any]:
    return install_record.load_distribution_manifest(repo_root)


def load_project_lock(repo_root: str | Path = ".") -> dict[str, Any]:
    return install_record.load_project_lock(repo_root)


def load_ownership_ledger(repo_root: str | Path = ".") -> dict[str, Any]:
    return install_record.load_ownership_ledger(repo_root)


def load_install_record_source(repo_root: str | Path = ".") -> dict[str, Any]:
    return migration_record.load_install_record_source(repo_root)


def load_migration_record_source(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    path = root / migration_record.MIGRATION_RECORD_JSON
    if path.exists():
        return load_json(path)
    return migration_record.build_migration_record(root)


def _accepted_report(repo_root: str | Path, path: Path, capability: str) -> bool:
    report_path = Path(repo_root) / path
    if not report_path.exists():
        return False
    try:
        report = load_json(report_path)
    except Exception:
        return False
    return (
        report.get("result") in {"ACCEPTED", "ACCEPTED_WITH_WARNINGS"}
        and report.get("accepted_capability") == capability
        and int(report.get("material_finding_count", 1)) == 0
        and int(report.get("missing_evidence", 1)) == 0
    )


def install_record_is_accepted(repo_root: str | Path = ".") -> bool:
    return _accepted_report(repo_root, INSTALL_RECORD_ACCEPTANCE_JSON, "install_record_v0")


def migration_record_is_accepted(repo_root: str | Path = ".") -> bool:
    return _accepted_report(repo_root, MIGRATION_RECORD_ACCEPTANCE_JSON, "migration_record_v0")


def object_digest(record: dict[str, Any], status_key: str, digest_func: Any) -> str:
    digest = record.get("status", {}).get(status_key)
    if isinstance(digest, str) and digest:
        return digest
    return digest_func(record)


def ledger_records(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in ledger.get("spec", {}).get("records", []) if isinstance(item, dict)]


def ledger_record_by_ref(ledger: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("entry_ref")): item for item in ledger_records(ledger) if item.get("entry_ref")}


def target_path_for(record: dict[str, Any]) -> str:
    return str(record.get("target_relative_path") or record.get("target_path") or record.get("containing_file_path") or "")


def update_plan_digest(record: dict[str, Any]) -> str:
    payload = copy.deepcopy(record)
    status = payload.get("status")
    if isinstance(status, dict):
        status.pop("update_plan_digest", None)
    return sha256_digest(canonical_json_bytes(payload))


def finalize_update_plan(record: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(record)
    result.setdefault("status", {})["update_plan_digest"] = update_plan_digest(result)
    return result


def _operation_for_record(record: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    ownership_class = str(record.get("ownership_class", "unknown"))
    path_kind = str(record.get("path_kind", "file"))
    target_path = target_path_for(record)
    preimage = str(record.get("observed_target_digest") or record.get("content_digest") or record.get("installed_content_digest") or "")
    postimage = str(record.get("installed_content_digest") or record.get("content_digest") or record.get("observed_target_digest") or "")
    base = {
        "operation_ref": "aide://update-plan/operation/" + str(record.get("record_id") or record.get("entry_ref", "unknown")).split("/")[-1],
        "target_relative_path": target_path,
        "ownership_entry_ref": record.get("entry_ref"),
        "ownership_class": ownership_class,
        "owner_ref": record.get("owner_ref"),
        "source_distribution_ref": record.get("source_distribution_ref") or manifest.get("metadata", {}).get("distribution_ref"),
        "source_component_ref": record.get("source_component_ref"),
        "preimage_digest": preimage,
        "postimage_digest": postimage,
        "rollback_requirement_ref": "aide://rollback-requirement/update-plan-v1/preimage-required",
        "manual_review_required": False,
        "evidence_refs": list(record.get("evidence_refs", [DEFAULT_EVIDENCE_REF])),
        "source_output_used_as_target_truth": False,
        "symlink_reparse_uncertain": False,
        "target_repository_mutation_performed": False,
        "update_apply_implemented": False,
        "extensions": {},
    }
    if ownership_class == "vendor_managed_section" or path_kind == "managed_section":
        base["operation_class"] = "update_managed_section"
    elif ownership_class == "vendor_managed_file":
        base["operation_class"] = "update_managed_file"
    elif ownership_class in OWNERSHIP_PRESERVE_OPERATION:
        base["operation_class"] = OWNERSHIP_PRESERVE_OPERATION[ownership_class]
    elif ownership_class == "never_touch":
        base["operation_class"] = "refuse"
        base["manual_review_required"] = True
    elif ownership_class == "unknown":
        base["operation_class"] = "manual_review_required"
        base["manual_review_required"] = True
    else:
        base["operation_class"] = "manual_review_required"
        base["manual_review_required"] = True
    return base


def _operation_sort_key(operation: dict[str, Any]) -> str:
    return str(operation.get("target_relative_path", "")) + "\0" + str(operation.get("operation_class", ""))


def build_update_plan(
    repo_root: str | Path = ".",
    *,
    manifest: dict[str, Any] | None = None,
    current_lock: dict[str, Any] | None = None,
    candidate_lock: dict[str, Any] | None = None,
    ledger: dict[str, Any] | None = None,
    install_source: dict[str, Any] | None = None,
    migration_source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    distribution = manifest if manifest is not None else load_distribution_manifest(repo_root)
    current = current_lock if current_lock is not None else load_project_lock(repo_root)
    candidate = candidate_lock if candidate_lock is not None else current
    ownership = ledger if ledger is not None else load_ownership_ledger(repo_root)
    install_source = install_source if install_source is not None else load_install_record_source(repo_root)
    migration_source = migration_source if migration_source is not None else load_migration_record_source(repo_root)
    operations = sorted([_operation_for_record(item, distribution) for item in ledger_records(ownership)], key=_operation_sort_key)
    preserved_paths = sorted(
        {
            str(operation.get("target_relative_path"))
            for operation in operations
            if str(operation.get("operation_class", "")).startswith("preserve_")
        }
    )
    managed_file_updates = [operation for operation in operations if operation.get("operation_class") in {"add_managed_file", "update_managed_file", "remove_managed_file"}]
    managed_section_updates = [operation for operation in operations if operation.get("operation_class") in {"add_managed_section", "update_managed_section", "remove_managed_section"}]
    conflicts = [
        {
            "conflict_ref": "aide://update-plan/conflict/" + str(operation.get("ownership_entry_ref", "unknown")).split("/")[-1],
            "conflict_type": "manual_review_required" if operation.get("operation_class") == "manual_review_required" else "never_touch_refusal",
            "target_relative_path": operation.get("target_relative_path"),
            "operation_ref": operation.get("operation_ref"),
            "disposition": "fail_closed_no_apply",
            "evidence_refs": operation.get("evidence_refs", []),
            "extensions": {},
        }
        for operation in operations
        if operation.get("operation_class") in {"manual_review_required", "refuse"}
    ]
    current_lock_digest = object_digest(current, "project_lock_digest", project_lock.project_lock_digest)
    candidate_lock_digest = object_digest(candidate, "project_lock_digest", project_lock.project_lock_digest)
    distribution_digest = object_digest(distribution, "distribution_digest", distribution_manifest.distribution_digest)
    ownership_digest = object_digest(ownership, "ownership_ledger_digest", ownership_ledger.ownership_ledger_digest)
    install_digest = object_digest(install_source, "install_record_digest", install_record.install_record_digest)
    migration_digest = object_digest(migration_source, "migration_record_digest", migration_record.migration_record_digest)
    record = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "update_plan_ref": "aide://update-plan/aide-self-no-apply-update-plan-v1",
            "target_project_ref": current.get("metadata", {}).get("project_ref"),
            "target_project_identity": current.get("metadata", {}).get("project_identity"),
            "current_project_lock_ref": current.get("metadata", {}).get("project_lock_ref"),
            "current_project_lock_digest": current_lock_digest,
            "candidate_distribution_ref": distribution.get("metadata", {}).get("distribution_ref"),
            "candidate_distribution_digest": distribution_digest,
            "candidate_project_lock_ref": candidate.get("metadata", {}).get("project_lock_ref"),
            "candidate_project_lock_digest": candidate_lock_digest,
            "ownership_ledger_ref": ownership.get("metadata", {}).get("ledger_ref"),
            "ownership_ledger_digest": ownership_digest,
            "created_at": DETERMINISTIC_TIMESTAMP,
            "created_by": "aide-self-hosting-fixture",
            "prior_update_plan_ref": None,
            "superseded_by_ref": None,
            "extensions": {},
        },
        "spec": {
            "install_record_refs": [install_source.get("metadata", {}).get("install_record_ref")],
            "install_record_digests": [install_digest],
            "migration_record_refs": [migration_source.get("metadata", {}).get("migration_record_ref")],
            "migration_record_digests": [migration_digest],
            "planned_operations": operations,
            "preserved_paths": preserved_paths,
            "managed_file_updates": managed_file_updates,
            "managed_section_updates": managed_section_updates,
            "conflicts": conflicts,
            "manual_review_items": [
                {
                    "item_ref": conflict["conflict_ref"],
                    "reason": conflict["conflict_type"],
                    "required": True,
                    "extensions": {},
                }
                for conflict in conflicts
                if conflict["conflict_type"] == "manual_review_required"
            ],
            "validation_plan": [
                "validate predecessor DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, and MigrationRecord refs",
                "validate every planned operation against OwnershipLedger ownership class and digest requirements",
                "validate rollback requirements before any future apply-capable task",
            ],
            "rollback_requirements": [
                "Every managed update/remove operation must carry a preimage digest and rollback requirement ref.",
                "A future RollbackBundle task must materialize recovery artifacts before any fixture apply.",
            ],
            "risk_class": "medium" if conflicts else "low",
            "approval_requirements": [
                "independent UpdatePlan check",
                "acceptance gate",
                "future RollbackBundle acceptance before apply-engine work",
            ],
            "evidence_refs": [DEFAULT_EVIDENCE_REF],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "required_features": [
                "update_plan_v1",
                "distribution_manifest_v1",
                "project_lock_v0",
                "ownership_ledger_v1",
                "install_record_v0",
                "migration_record_v0",
                "sha256_digest_canonical_json_v1",
                "no_apply_update_plan_v1",
            ],
            "optional_features": ["conflict_only_plan_v1", "project_overlay_preservation_v1"],
            "source_output_used_as_target_truth": False,
            "target_repository_mutation_performed": False,
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "validation_result": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "recommended_next_task": CHECK_TASK_ID,
            "update_plan_digest": "",
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "migration_apply_implemented": False,
            "repair_apply_implemented": False,
            "rollback_apply_implemented": False,
            "uninstall_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "target_scan_authority_implemented": False,
            "release_publication_implemented": False,
            "network_calls_implemented": False,
            "provider_model_calls_implemented": False,
            "workbench_runtime_implemented": False,
            "commander_implemented": False,
            "omnigent_implemented": False,
            "branch_worktree_automation_implemented": False,
            "extensions": {},
        },
        "extensions": {},
    }
    return finalize_update_plan(record)


def _add_error(errors: list[dict[str, str]], code: str, message: str) -> None:
    errors.append({"code": code, "message": message})


def _validation_result(errors: list[dict[str, str]], warnings: list[str]) -> dict[str, Any]:
    return {
        "valid": not errors,
        "status": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "error_count": len(errors),
        "errors": errors,
        "refusal_codes": sorted({error["code"] for error in errors}),
        "warnings": warnings,
    }


def _iter_string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value.replace("\\", "/")]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(_iter_string_values(item))
        return result
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(_iter_string_values(item))
        return result
    return []


def _extension_requires_unknown(data: Any) -> bool:
    if isinstance(data, dict):
        return any(str(key).startswith("requires.") for key in data) or any(_extension_requires_unknown(value) for value in data.values())
    if isinstance(data, list):
        return any(_extension_requires_unknown(item) for item in data)
    return False


def _boolean_claims_authority(data: Any, errors: list[dict[str, str]]) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            key_text = str(key)
            if value is True and ("apply" in key_text or "update_authority" in key_text):
                _add_error(errors, "update_plan.apply_authority_claimed", f"apply authority claimed by {key_text}")
            if value is True and ("mutation" in key_text or "mutate" in key_text):
                _add_error(errors, "update_plan.target_mutation_claimed", f"target mutation claimed by {key_text}")
            _boolean_claims_authority(value, errors)
    elif isinstance(data, list):
        for item in data:
            _boolean_claims_authority(item, errors)


def _path_error(value: str) -> str | None:
    if value.startswith("aide://") or value.startswith("sha256:"):
        return None
    normalized = value.replace("\\", "/")
    if SOURCE_OUTPUT_RE.search(normalized):
        return "update_plan.source_state_contamination"
    if PATH_RE.search(normalized):
        if ".." in [part for part in normalized.split("/") if part]:
            return "update_plan.path_traversal_forbidden"
        return "update_plan.absolute_path_forbidden"
    return None


def _operation_is_managed(operation: dict[str, Any]) -> bool:
    return operation.get("operation_class") in MANAGED_OPERATION_CLASSES


def _operation_requires_preimage(operation_class: str) -> bool:
    return operation_class in {"update_managed_file", "remove_managed_file", "update_managed_section", "remove_managed_section"}


def _operation_requires_postimage(operation_class: str) -> bool:
    return operation_class in {"add_managed_file", "update_managed_file", "add_managed_section", "update_managed_section"}


def _validate_operations(
    plan: dict[str, Any],
    *,
    manifest: dict[str, Any],
    ledger: dict[str, Any],
    errors: list[dict[str, str]],
) -> None:
    operations = plan.get("spec", {}).get("planned_operations", [])
    if not isinstance(operations, list):
        _add_error(errors, "update_plan.invalid", "planned_operations must be a list")
        return
    records = ledger_record_by_ref(ledger)
    path_case_map: dict[str, str] = {}
    for operation in operations:
        if not isinstance(operation, dict):
            _add_error(errors, "update_plan.invalid", "planned operation must be an object")
            continue
        operation_class = str(operation.get("operation_class", ""))
        ownership_class = str(operation.get("ownership_class", ""))
        target_path = str(operation.get("target_relative_path", ""))
        if operation_class not in SUPPORTED_OPERATION_CLASSES:
            _add_error(errors, "update_plan.invalid", f"unsupported operation_class: {operation_class}")
        path_code = _path_error(target_path)
        if path_code:
            _add_error(errors, path_code, f"unsafe target path: {target_path}")
        normalized = target_path.replace("\\", "/")
        folded = normalized.lower()
        if folded in path_case_map and path_case_map[folded] != normalized:
            _add_error(errors, "update_plan.case_collision", f"case-fold collision: {path_case_map[folded]} vs {normalized}")
        if normalized:
            path_case_map[folded] = normalized
        entry_ref = str(operation.get("ownership_entry_ref", ""))
        if entry_ref and entry_ref not in records:
            _add_error(errors, "update_plan.unknown_ownership", f"operation references unknown ownership entry: {entry_ref}")
        if ownership_class == "unknown" and operation_class not in {"manual_review_required", "refuse"}:
            _add_error(errors, "update_plan.unknown_ownership", "unknown ownership cannot be auto-updated")
        if ownership_class == "never_touch" and operation_class != "refuse":
            _add_error(errors, "update_plan.never_touch_target", "never_touch targets must be refused")
        if _operation_is_managed(operation):
            if ownership_class == "project_owned":
                _add_error(errors, "update_plan.project_owned_overwrite", "project_owned targets cannot be overwritten")
            if ownership_class == "project_overlay":
                _add_error(errors, "update_plan.project_overlay_overwrite", "project_overlay targets cannot be overwritten")
            if ownership_class == "local_only":
                _add_error(errors, "update_plan.local_only_overwrite", "local_only targets cannot be overwritten")
            if ownership_class == "runtime_generated":
                _add_error(errors, "update_plan.runtime_generated_overwrite", "runtime_generated targets cannot be overwritten")
            if ownership_class == "evidence_only":
                _add_error(errors, "update_plan.evidence_only_overwrite", "evidence_only targets cannot be overwritten")
            if ownership_class == "preserved_legacy":
                _add_error(errors, "update_plan.project_owned_overwrite", "preserved_legacy targets require preservation or manual review")
        if operation.get("symlink_reparse_uncertain") is True and operation_class != "refuse":
            _add_error(errors, "update_plan.symlink_reparse_uncertain", "symlink or reparse uncertainty must fail closed")
        if operation.get("source_distribution_ref") and operation.get("source_distribution_ref") != manifest.get("metadata", {}).get("distribution_ref"):
            _add_error(errors, "update_plan.distribution_mismatch", "operation source_distribution_ref does not match candidate distribution")
        if _operation_requires_preimage(operation_class) and not operation.get("preimage_digest"):
            _add_error(errors, "update_plan.preimage_digest_missing", f"preimage_digest is required for {operation_class}")
        if _operation_requires_postimage(operation_class) and not operation.get("postimage_digest"):
            _add_error(errors, "update_plan.postimage_digest_missing", f"postimage_digest is required for {operation_class}")
        if operation_class in MANAGED_OPERATION_CLASSES | {"regenerate_project_output"} and not operation.get("rollback_requirement_ref"):
            _add_error(errors, "update_plan.rollback_requirement_missing", f"rollback requirement is required for {operation_class}")
        if operation.get("source_output_used_as_target_truth") is True:
            _add_error(errors, "update_plan.source_output_as_target_truth", "operation cannot use source output as target truth")
        if not operation.get("evidence_refs"):
            _add_error(errors, "update_plan.evidence_missing", "operation evidence_refs must not be empty")


def validate_update_plan_object(
    plan: dict[str, Any] | None,
    *,
    manifest: dict[str, Any] | None = None,
    current_lock: dict[str, Any] | None = None,
    candidate_lock: dict[str, Any] | None = None,
    ledger: dict[str, Any] | None = None,
    install_source: dict[str, Any] | None = None,
    migration_source: dict[str, Any] | None = None,
    repo_root: str | Path | None = None,
    require_predecessor_acceptance: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[str] = []
    if plan is None:
        _add_error(errors, "update_plan.missing", "UpdatePlan is missing")
        return _validation_result(errors, warnings)
    if not isinstance(plan, dict):
        _add_error(errors, "update_plan.invalid", "UpdatePlan root must be an object")
        return _validation_result(errors, warnings)
    for field in ["apiVersion", "kind", "schema_version", "metadata", "spec", "status", "extensions"]:
        if field not in plan:
            _add_error(errors, "update_plan.invalid", f"missing required field: {field}")
    if plan.get("kind") != KIND:
        _add_error(errors, "update_plan.invalid", "kind must be UpdatePlan")
    if plan.get("schema_version") != SCHEMA_VERSION:
        _add_error(errors, "update_plan.invalid", f"schema_version must be {SCHEMA_VERSION}")
    metadata = plan.get("metadata") if isinstance(plan.get("metadata"), dict) else {}
    spec = plan.get("spec") if isinstance(plan.get("spec"), dict) else {}
    status = plan.get("status") if isinstance(plan.get("status"), dict) else {}
    distribution = manifest if manifest is not None else load_distribution_manifest(repo_root or Path("."))
    current = current_lock if current_lock is not None else load_project_lock(repo_root or Path("."))
    candidate = candidate_lock if candidate_lock is not None else current
    ownership = ledger if ledger is not None else load_ownership_ledger(repo_root or Path("."))
    install_source = install_source if install_source is not None else load_install_record_source(repo_root or Path("."))
    migration_source = migration_source if migration_source is not None else load_migration_record_source(repo_root or Path("."))

    if not metadata.get("candidate_distribution_ref"):
        _add_error(errors, "update_plan.distribution_missing", "candidate_distribution_ref is required")
    if not metadata.get("current_project_lock_ref") or not metadata.get("candidate_project_lock_ref"):
        _add_error(errors, "update_plan.project_lock_missing", "current and candidate project lock refs are required")
    if not metadata.get("ownership_ledger_ref"):
        _add_error(errors, "update_plan.ownership_ledger_missing", "ownership_ledger_ref is required")
    if not spec.get("install_record_refs"):
        _add_error(errors, "update_plan.install_record_missing", "install_record_refs are required")
    if not spec.get("migration_record_refs"):
        _add_error(errors, "update_plan.migration_record_missing", "migration_record_refs are required")
    expected_distribution_ref = distribution.get("metadata", {}).get("distribution_ref")
    expected_distribution_digest = object_digest(distribution, "distribution_digest", distribution_manifest.distribution_digest)
    if metadata.get("candidate_distribution_ref") != expected_distribution_ref:
        _add_error(errors, "update_plan.distribution_mismatch", "candidate_distribution_ref does not match DistributionManifest")
    if metadata.get("candidate_distribution_digest") != expected_distribution_digest:
        _add_error(errors, "update_plan.distribution_mismatch", "candidate_distribution_digest does not match DistributionManifest")
    expected_current_ref = current.get("metadata", {}).get("project_lock_ref")
    expected_current_digest = object_digest(current, "project_lock_digest", project_lock.project_lock_digest)
    expected_candidate_ref = candidate.get("metadata", {}).get("project_lock_ref")
    expected_candidate_digest = object_digest(candidate, "project_lock_digest", project_lock.project_lock_digest)
    if metadata.get("current_project_lock_ref") != expected_current_ref:
        _add_error(errors, "update_plan.project_lock_mismatch", "current_project_lock_ref does not match ProjectLock")
    if metadata.get("current_project_lock_digest") != expected_current_digest:
        _add_error(errors, "update_plan.project_lock_mismatch", "current_project_lock_digest does not match ProjectLock")
    if metadata.get("candidate_project_lock_ref") != expected_candidate_ref:
        _add_error(errors, "update_plan.project_lock_mismatch", "candidate_project_lock_ref does not match ProjectLock")
    if metadata.get("candidate_project_lock_digest") != expected_candidate_digest:
        _add_error(errors, "update_plan.project_lock_mismatch", "candidate_project_lock_digest does not match ProjectLock")
    if metadata.get("ownership_ledger_ref") != ownership.get("metadata", {}).get("ledger_ref"):
        _add_error(errors, "update_plan.ownership_ledger_mismatch", "ownership_ledger_ref does not match OwnershipLedger")
    if metadata.get("ownership_ledger_digest") != object_digest(ownership, "ownership_ledger_digest", ownership_ledger.ownership_ledger_digest):
        _add_error(errors, "update_plan.ownership_ledger_mismatch", "ownership_ledger_digest does not match OwnershipLedger")
    install_ref = install_source.get("metadata", {}).get("install_record_ref")
    install_digest = object_digest(install_source, "install_record_digest", install_record.install_record_digest)
    if install_ref not in (spec.get("install_record_refs") or []):
        _add_error(errors, "update_plan.install_record_mismatch", "accepted InstallRecord ref is not cited")
    if install_digest not in (spec.get("install_record_digests") or []):
        _add_error(errors, "update_plan.install_record_mismatch", "accepted InstallRecord digest is not cited")
    migration_ref = migration_source.get("metadata", {}).get("migration_record_ref")
    migration_digest = object_digest(migration_source, "migration_record_digest", migration_record.migration_record_digest)
    if migration_ref not in (spec.get("migration_record_refs") or []):
        _add_error(errors, "update_plan.migration_record_mismatch", "accepted MigrationRecord ref is not cited")
    if migration_digest not in (spec.get("migration_record_digests") or []):
        _add_error(errors, "update_plan.migration_record_mismatch", "accepted MigrationRecord digest is not cited")
    if require_predecessor_acceptance:
        if repo_root is None or not install_record_is_accepted(repo_root):
            _add_error(errors, "update_plan.install_record_mismatch", "InstallRecord v0 is not accepted")
        if repo_root is None or not migration_record_is_accepted(repo_root):
            _add_error(errors, "update_plan.migration_record_mismatch", "MigrationRecord v0 is not accepted")
    for feature in spec.get("required_features", []) if isinstance(spec.get("required_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES:
            _add_error(errors, "update_plan.unknown_required_feature", f"unknown required feature: {feature}")
    for feature in spec.get("optional_features", []) if isinstance(spec.get("optional_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES and feature not in SUPPORTED_OPTIONAL_FEATURES:
            warnings.append(f"unknown optional feature tolerated: {feature}")
    if _extension_requires_unknown(plan.get("extensions", {})) or _extension_requires_unknown(spec.get("extensions", {})):
        _add_error(errors, "update_plan.extension_required_unknown", "unknown required extension present")
    if not spec.get("validation_plan"):
        _add_error(errors, "update_plan.invalid", "validation_plan must not be empty")
    if not spec.get("rollback_requirements"):
        _add_error(errors, "update_plan.rollback_requirement_missing", "rollback_requirements must not be empty")
    if not spec.get("approval_requirements"):
        _add_error(errors, "update_plan.invalid", "approval_requirements must not be empty")
    if not spec.get("evidence_refs"):
        _add_error(errors, "update_plan.evidence_missing", "evidence_refs must not be empty")
    if spec.get("source_output_used_as_target_truth") is True:
        _add_error(errors, "update_plan.source_output_as_target_truth", "source output cannot become target truth")
    for value in _iter_string_values(spec):
        path_code = _path_error(value)
        if path_code:
            _add_error(errors, path_code, f"unsafe source or target string: {value}")
    _validate_operations(plan, manifest=distribution, ledger=ownership, errors=errors)
    _boolean_claims_authority(spec, errors)
    _boolean_claims_authority(status, errors)
    expected_digest = update_plan_digest(plan)
    if status.get("update_plan_digest") and status.get("update_plan_digest") != expected_digest:
        _add_error(errors, "update_plan.digest_mismatch", "update_plan_digest does not match canonical payload")
    return _validation_result(errors, warnings)


def minimal_fixture_record() -> dict[str, Any]:
    manifest = distribution_manifest.minimal_fixture_manifest()
    lock = project_lock.minimal_fixture_lock()
    ledger = ownership_ledger.minimal_fixture_ledger()
    install_source = install_record.minimal_fixture_record()
    migration_source = migration_record.minimal_fixture_record()
    return build_update_plan(
        manifest=manifest,
        current_lock=lock,
        candidate_lock=lock,
        ledger=ledger,
        install_source=install_source,
        migration_source=migration_source,
    )


def mutate(base: dict[str, Any], mutator: Any) -> dict[str, Any]:
    record = copy.deepcopy(base)
    mutator(record)
    return finalize_update_plan(record)


def _replace_first_managed_operation(record: dict[str, Any], *, operation_class: str, ownership_class: str, path: str | None = None) -> None:
    for operation in record["spec"]["planned_operations"]:
        if operation.get("operation_class") in MANAGED_OPERATION_CLASSES:
            operation["operation_class"] = operation_class
            operation["ownership_class"] = ownership_class
            if path is not None:
                operation["target_relative_path"] = path
            return
    raise AssertionError("fixture missing managed operation")


def _first_operation(record: dict[str, Any]) -> dict[str, Any]:
    return record["spec"]["planned_operations"][0]


def write_fixture_corpus(repo_root: str | Path = ".") -> None:
    root = Path(repo_root)
    base = minimal_fixture_record()
    valid_cases = {
        "no-op-update": base,
        "managed-file-add": mutate(base, lambda d: _replace_first_managed_operation(d, operation_class="add_managed_file", ownership_class="vendor_managed_file", path=".aide/new-managed-file.txt")),
        "managed-file-update": mutate(base, lambda d: _replace_first_managed_operation(d, operation_class="update_managed_file", ownership_class="vendor_managed_file")),
        "managed-section-add": mutate(base, lambda d: _replace_first_managed_operation(d, operation_class="add_managed_section", ownership_class="vendor_managed_section", path="AGENTS.md")),
        "managed-section-update": mutate(base, lambda d: _replace_first_managed_operation(d, operation_class="update_managed_section", ownership_class="vendor_managed_section", path="AGENTS.md")),
        "project-owned-preservation": mutate(base, lambda d: _replace_first_managed_operation(d, operation_class="preserve_project_owned", ownership_class="project_owned", path="README.md")),
        "local-only-preservation": mutate(base, lambda d: _replace_first_managed_operation(d, operation_class="preserve_local_only", ownership_class="local_only", path="local-only/settings.json")),
        "legacy-preservation": mutate(base, lambda d: _replace_first_managed_operation(d, operation_class="preserve_legacy", ownership_class="preserved_legacy", path=".aide/legacy/state.json")),
        "manual-review-item": mutate(
            base,
            lambda d: (
                _replace_first_managed_operation(d, operation_class="manual_review_required", ownership_class="unknown", path="unclassified/file.txt"),
                d["spec"]["manual_review_items"].append({"item_ref": "aide://manual-review/update-plan-v1/unknown", "required": True}),
            ),
        ),
        "migration-dependent-plan": mutate(base, lambda d: d["spec"]["migration_record_refs"].append("aide://migration-record/future-accepted-no-apply")),
        "conflict-only-plan": mutate(
            base,
            lambda d: (
                _replace_first_managed_operation(d, operation_class="refuse", ownership_class="never_touch", path=".git/config"),
                d["spec"]["conflicts"].append({"conflict_ref": "aide://update-plan/conflict/never-touch", "conflict_type": "never_touch_refusal", "disposition": "fail_closed_no_apply"}),
            ),
        ),
        "optional-extension-preserved": mutate(
            base,
            lambda d: (
                d["spec"]["optional_features"].append("future.optional.update-plan"),
                d.__setitem__("extensions", {"future.optional": {"preserve": True}}),
            ),
        ),
    }
    invalid_cases = {
        "unknown-ownership-auto-update": mutate(base, lambda d: _replace_first_managed_operation(d, operation_class="update_managed_file", ownership_class="unknown", path="unclassified/file.txt")),
        "never-touch-update": mutate(base, lambda d: _replace_first_managed_operation(d, operation_class="update_managed_file", ownership_class="never_touch", path=".git/config")),
        "project-owned-overwrite": mutate(base, lambda d: _replace_first_managed_operation(d, operation_class="update_managed_file", ownership_class="project_owned", path="README.md")),
        "local-only-overwrite": mutate(base, lambda d: _replace_first_managed_operation(d, operation_class="update_managed_file", ownership_class="local_only", path="local-only/settings.json")),
        "path-traversal": mutate(base, lambda d: _first_operation(d).__setitem__("target_relative_path", "../outside/file.txt")),
        "absolute-path": mutate(base, lambda d: _first_operation(d).__setitem__("target_relative_path", "C:/outside/file.txt")),
        "case-collision": mutate(
            base,
            lambda d: d["spec"]["planned_operations"].append(
                {**copy.deepcopy(d["spec"]["planned_operations"][0]), "operation_ref": "aide://update-plan/operation/case-collision", "target_relative_path": str(d["spec"]["planned_operations"][0]["target_relative_path"]).upper()}
            ),
        ),
        "symlink-reparse-uncertainty": mutate(base, lambda d: _first_operation(d).__setitem__("symlink_reparse_uncertain", True)),
        "missing-rollback-requirement": mutate(
            base,
            lambda d: (
                _replace_first_managed_operation(d, operation_class="update_managed_file", ownership_class="vendor_managed_file"),
                next(operation for operation in d["spec"]["planned_operations"] if operation.get("operation_class") == "update_managed_file").__setitem__("rollback_requirement_ref", ""),
            ),
        ),
        "mismatched-distribution": mutate(base, lambda d: d["metadata"].__setitem__("candidate_distribution_digest", "sha256:" + "1" * 64)),
        "mismatched-project-lock": mutate(base, lambda d: d["metadata"].__setitem__("candidate_project_lock_digest", "sha256:" + "2" * 64)),
        "mismatched-ownership-ledger": mutate(base, lambda d: d["metadata"].__setitem__("ownership_ledger_digest", "sha256:" + "3" * 64)),
        "unknown-required-feature": mutate(base, lambda d: d["spec"]["required_features"].append("future.required.update-plan")),
        "apply-claim": mutate(base, lambda d: d["status"].__setitem__("update_apply_implemented", True)),
        "target-mutation-claim": mutate(base, lambda d: d["status"].__setitem__("target_repository_mutation_implemented", True)),
        "source-output-target-truth": mutate(base, lambda d: d["spec"].__setitem__("source_output_used_as_target_truth", True)),
        "extension-required-unknown": mutate(base, lambda d: d["spec"]["extensions"].__setitem__("requires.future", {"enabled": True})),
    }
    for path in (root / FIXTURE_ROOT / "valid").glob("*.json"):
        path.unlink()
    for path in (root / FIXTURE_ROOT / "invalid").glob("*.json"):
        path.unlink()
    for name, record in valid_cases.items():
        write_json(root / FIXTURE_ROOT / "valid" / f"{name}.json", record)
    for name, record in invalid_cases.items():
        write_json(root / FIXTURE_ROOT / "invalid" / f"{name}.json", record)


EXPECTED_INVALID_REFUSALS = {
    "unknown-ownership-auto-update": ["update_plan.unknown_ownership"],
    "never-touch-update": ["update_plan.never_touch_target"],
    "project-owned-overwrite": ["update_plan.project_owned_overwrite"],
    "local-only-overwrite": ["update_plan.local_only_overwrite"],
    "path-traversal": ["update_plan.path_traversal_forbidden"],
    "absolute-path": ["update_plan.absolute_path_forbidden"],
    "case-collision": ["update_plan.case_collision"],
    "symlink-reparse-uncertainty": ["update_plan.symlink_reparse_uncertain"],
    "missing-rollback-requirement": ["update_plan.rollback_requirement_missing"],
    "mismatched-distribution": ["update_plan.distribution_mismatch"],
    "mismatched-project-lock": ["update_plan.project_lock_mismatch"],
    "mismatched-ownership-ledger": ["update_plan.ownership_ledger_mismatch"],
    "unknown-required-feature": ["update_plan.unknown_required_feature"],
    "apply-claim": ["update_plan.apply_authority_claimed"],
    "target-mutation-claim": ["update_plan.target_mutation_claimed"],
    "source-output-target-truth": ["update_plan.source_output_as_target_truth"],
    "extension-required-unknown": ["update_plan.extension_required_unknown"],
}


def display_path(path: Path, repo_root: str | Path = ".") -> str:
    try:
        return str(path.resolve().relative_to(Path(repo_root).resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def evaluate_fixture(path: Path, expected_result: str, expected_refusals: list[str], repo_root: str | Path = ".") -> dict[str, Any]:
    record = load_json(path)
    manifest = distribution_manifest.minimal_fixture_manifest()
    lock = project_lock.minimal_fixture_lock()
    ledger = ownership_ledger.minimal_fixture_ledger()
    install_source = install_record.minimal_fixture_record()
    migration_source = migration_record.minimal_fixture_record()
    result = validate_update_plan_object(
        record,
        manifest=manifest,
        current_lock=lock,
        candidate_lock=lock,
        ledger=ledger,
        install_source=install_source,
        migration_source=migration_source,
        require_predecessor_acceptance=False,
    )
    observed = result["status"]
    refusal_codes = result["refusal_codes"]
    passed = observed == expected_result and all(code in refusal_codes for code in expected_refusals)
    return {
        "path": display_path(path, repo_root),
        "case_id": path.stem,
        "expected_result": expected_result,
        "expected_refusal_codes": expected_refusals,
        "observed_result": observed,
        "observed_refusal_codes": refusal_codes,
        "passed": passed,
    }


def fixture_matrix(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    write_fixture_corpus(root)
    results = []
    for path in sorted((root / FIXTURE_ROOT / "valid").glob("*.json")):
        results.append(evaluate_fixture(path, "PASS_WITH_WARNINGS", [], root))
    for path in sorted((root / FIXTURE_ROOT / "invalid").glob("*.json")):
        results.append(evaluate_fixture(path, "FAILED_VALIDATION", EXPECTED_INVALID_REFUSALS[path.stem], root))
    return {"schema_version": "aide.update-plan-fixture-matrix.v1", "fixture_results": results}


def schema_alignment_errors(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema must declare Draft 2020-12")
    if schema.get("properties", {}).get("kind", {}).get("const") != KIND:
        errors.append("schema kind const must be UpdatePlan")
    required = set(schema.get("$defs", {}).get("spec", {}).get("required", []))
    for field in [
        "install_record_refs",
        "migration_record_refs",
        "planned_operations",
        "preserved_paths",
        "managed_file_updates",
        "managed_section_updates",
        "conflicts",
        "manual_review_items",
        "validation_plan",
        "rollback_requirements",
        "risk_class",
        "approval_requirements",
        "evidence_refs",
        "explicit_non_capabilities",
        "extensions",
    ]:
        if field not in required:
            errors.append(f"schema spec missing required field: {field}")
    return errors


def status(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    data = {
        "schema_version": "aide.update-plan-status.v1",
        "status": "PASS_WITH_WARNINGS" if (root / SCHEMA_PATH).exists() and (root / "core/protocol/update_plan.py").exists() else "FAILED_VALIDATION",
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/update_plan.py").exists(),
        "install_record_acceptance_report_exists": (root / INSTALL_RECORD_ACCEPTANCE_JSON).exists(),
        "migration_record_acceptance_report_exists": (root / MIGRATION_RECORD_ACCEPTANCE_JSON).exists(),
        "update_plan_projection_exists": (root / PROJECTION_JSON).exists(),
        "validation_report_exists": (root / VALIDATION_JSON).exists(),
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": CHECK_TASK_ID,
        "install_apply_implemented": False,
        "update_apply_implemented": False,
        "migration_apply_implemented": False,
        "rollback_apply_implemented": False,
        "uninstall_apply_implemented": False,
        "target_repository_mutation_implemented": False,
        "target_scan_authority_implemented": False,
        "release_publication_implemented": False,
        "warnings": ["UpdatePlan v1 remains proposed until independent check and acceptance."],
    }
    write_text(root / STATUS_MD, render_status_md(data))
    return data


def project(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    plan = build_update_plan(root)
    validation = validate_update_plan_object(plan, repo_root=root)
    matrix = fixture_matrix(root)
    report = {
        "schema_version": "aide.update-plan-project-report.v1",
        "status": validation["status"],
        "proposed_capability": PROPOSED_CAPABILITY,
        "update_plan_path": PROJECTION_JSON.as_posix(),
        "update_plan_digest": plan["status"]["update_plan_digest"],
        "planned_operation_count": len(plan["spec"]["planned_operations"]),
        "managed_file_update_count": len(plan["spec"]["managed_file_updates"]),
        "managed_section_update_count": len(plan["spec"]["managed_section_updates"]),
        "preserved_path_count": len(plan["spec"]["preserved_paths"]),
        "conflict_count": len(plan["spec"]["conflicts"]),
        "risk_class": plan["spec"]["risk_class"],
        "recommended_next_task": CHECK_TASK_ID,
        "source_artifacts_mutated": False,
        "target_repository_mutation_implemented": False,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "warnings": [
            "UpdatePlan v1 is a dry-run plan only and performs no update apply.",
            "Source generated latest-* outputs are not target truth.",
        ],
    }
    write_json(root / PROJECTION_JSON, plan)
    write_json(root / PROJECT_REPORT_JSON, report)
    write_json(root / FIXTURE_MATRIX_JSON, matrix)
    write_text(root / FIXTURE_MATRIX_MD, render_fixture_matrix_md(matrix["fixture_results"]))
    write_text(root / CONFLICT_SUMMARY_MD, render_conflict_summary_md(plan))
    write_text(root / NO_APPLY_BOUNDARY_MD, render_no_apply_boundary_md())
    status(root)
    write_validation_reports(root)
    return report


def validate(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    schema = load_schema(root)
    manifest = load_distribution_manifest(root)
    current = load_project_lock(root)
    candidate = current
    ledger = load_ownership_ledger(root)
    install_source = load_install_record_source(root)
    migration_source = load_migration_record_source(root)
    plan = build_update_plan(
        root,
        manifest=manifest,
        current_lock=current,
        candidate_lock=candidate,
        ledger=ledger,
        install_source=install_source,
        migration_source=migration_source,
    )
    validation = validate_update_plan_object(
        plan,
        manifest=manifest,
        current_lock=current,
        candidate_lock=candidate,
        ledger=ledger,
        install_source=install_source,
        migration_source=migration_source,
        repo_root=root,
    )
    matrix = fixture_matrix(root)
    alignment_errors = schema_alignment_errors(schema)
    fixture_failures = [item for item in matrix["fixture_results"] if not item["passed"]]
    checks = {
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/update_plan.py").exists(),
        "cli_registered": cli_registered(root),
        "update_plan_generated": plan["kind"] == KIND,
        "update_plan_valid": validation["valid"],
        "schema_alignment": not alignment_errors,
        "fixture_matrix_passed": not fixture_failures,
        "install_record_accepted": install_record_is_accepted(root),
        "migration_record_accepted": migration_record_is_accepted(root),
        "distribution_ref_bound": plan["metadata"]["candidate_distribution_ref"] == manifest["metadata"]["distribution_ref"],
        "current_project_lock_bound": plan["metadata"]["current_project_lock_digest"] == current["status"]["project_lock_digest"],
        "candidate_project_lock_bound": plan["metadata"]["candidate_project_lock_digest"] == candidate["status"]["project_lock_digest"],
        "ownership_ledger_bound": plan["metadata"]["ownership_ledger_digest"] == ledger["status"]["ownership_ledger_digest"],
        "install_record_bound": install_source["metadata"]["install_record_ref"] in plan["spec"]["install_record_refs"],
        "migration_record_bound": migration_source["metadata"]["migration_record_ref"] in plan["spec"]["migration_record_refs"],
        "update_apply_not_implemented": plan["status"]["update_apply_implemented"] is False,
        "install_apply_not_implemented": plan["status"]["install_apply_implemented"] is False,
        "migration_apply_not_implemented": plan["status"]["migration_apply_implemented"] is False,
        "rollback_apply_not_implemented": plan["status"]["rollback_apply_implemented"] is False,
        "target_repository_mutation_not_implemented": plan["status"]["target_repository_mutation_implemented"] is False,
        "target_scan_authority_not_implemented": plan["status"]["target_scan_authority_implemented"] is False,
        "release_publication_not_implemented": plan["status"]["release_publication_implemented"] is False,
        "source_output_not_target_truth": plan["spec"]["source_output_used_as_target_truth"] is False,
    }
    errors: list[dict[str, str]] = []
    if not validation["valid"]:
        errors.extend(validation["errors"])
    for error in alignment_errors:
        errors.append({"code": "update_plan.schema_alignment", "message": error})
    for failure in fixture_failures:
        errors.append({"code": "update_plan.fixture_failure", "message": failure["case_id"]})
    if not checks["install_record_accepted"]:
        errors.append({"code": "update_plan.install_record_mismatch", "message": "InstallRecord v0 acceptance report is missing or invalid"})
    if not checks["migration_record_accepted"]:
        errors.append({"code": "update_plan.migration_record_mismatch", "message": "MigrationRecord v0 acceptance report is missing or invalid"})
    validation_status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    report = {
        "schema_version": "aide.update-plan-validation.v1",
        "status": validation_status,
        "validation_status": validation_status,
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": CHECK_TASK_ID,
        "checks": checks,
        "errors": errors,
        "schema_alignment_errors": alignment_errors,
        "update_plan_validation": validation,
        "fixture_results": matrix["fixture_results"],
        "warnings": [
            "UpdatePlan v1 is proposed until independent check and acceptance.",
            "UpdatePlan records dry-run planning metadata only and performs no update apply.",
            "RollbackBundle remains a future dependency before any fixture apply engine work.",
        ],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
    }
    write_json(root / PROJECTION_JSON, plan)
    write_json(root / VALIDATION_JSON, report)
    write_json(root / FIXTURE_MATRIX_JSON, matrix)
    write_text(root / VALIDATION_MD, render_validation_md(report))
    write_text(root / FIXTURE_MATRIX_MD, render_fixture_matrix_md(matrix["fixture_results"]))
    write_text(root / CONFLICT_SUMMARY_MD, render_conflict_summary_md(plan))
    write_text(root / NO_APPLY_BOUNDARY_MD, render_no_apply_boundary_md())
    status(root)
    return report


def write_validation_reports(repo_root: str | Path = ".") -> None:
    validate(repo_root)


def cli_registered(repo_root: Path) -> bool:
    script = repo_root / ".aide/scripts/aide_lite.py"
    if not script.exists():
        return False
    text = script.read_text(encoding="utf-8")
    return "update-plan" in text and "command_update_plan_validate" in text


def render_status_md(data: dict[str, Any]) -> str:
    lines = [
        "# UpdatePlan v1 Status",
        "",
        f"- status: `{data.get('status')}`",
        f"- proposed_capability: `{data.get('proposed_capability')}`",
        f"- schema_exists: `{str(data.get('schema_exists', False)).lower()}`",
        f"- helper_exists: `{str(data.get('helper_exists', False)).lower()}`",
        f"- install_record_acceptance_report_exists: `{str(data.get('install_record_acceptance_report_exists', False)).lower()}`",
        f"- migration_record_acceptance_report_exists: `{str(data.get('migration_record_acceptance_report_exists', False)).lower()}`",
        f"- recommended_next_task: `{data.get('recommended_next_task')}`",
        "",
        "## Explicit Non-Capabilities",
        "",
    ]
    for item in EXPLICIT_NON_CAPABILITIES:
        lines.append(f"- {item}: false")
    return "\n".join(lines) + "\n"


def render_validation_md(report: dict[str, Any]) -> str:
    lines = [
        "# UpdatePlan v1 Validation",
        "",
        f"- result: `{report['validation_status']}`",
        f"- proposed_capability: `{PROPOSED_CAPABILITY}`",
        f"- recommended_next_task: `{CHECK_TASK_ID}`",
        f"- error_count: {len(report['errors'])}",
        "",
        "## Checks",
        "",
    ]
    for key, value in sorted(report["checks"].items()):
        lines.append(f"- {key}: `{str(value).lower()}`")
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def render_fixture_matrix_md(fixtures: list[dict[str, Any]]) -> str:
    lines = ["# UpdatePlan v1 Fixture Matrix", "", "| Case | Expected | Observed | Codes | Pass |", "| --- | --- | --- | --- | --- |"]
    for fixture in fixtures:
        codes = ", ".join(fixture.get("observed_refusal_codes", [])) or "none"
        lines.append(f"| {fixture['case_id']} | {fixture['expected_result']} | {fixture['observed_result']} | {codes} | {str(fixture['passed']).lower()} |")
    return "\n".join(lines) + "\n"


def render_conflict_summary_md(plan: dict[str, Any]) -> str:
    lines = [
        "# UpdatePlan v1 Conflict Summary",
        "",
        f"- conflict_count: {len(plan.get('spec', {}).get('conflicts', []))}",
        "- conflict_disposition: fail_closed_no_apply",
        "",
    ]
    for conflict in plan.get("spec", {}).get("conflicts", []):
        lines.append(f"- `{conflict.get('conflict_ref')}` {conflict.get('conflict_type')} at `{conflict.get('target_relative_path')}`")
    return "\n".join(lines) + "\n"


def render_no_apply_boundary_md() -> str:
    lines = [
        "# UpdatePlan v1 No-Apply Boundary",
        "",
        "UpdatePlan v1 is dry-run planning metadata. It does not perform install, update, migration, repair, rollback, or uninstall apply.",
        "",
    ]
    for item in EXPLICIT_NON_CAPABILITIES:
        lines.append(f"- {item}: false")
    return "\n".join(lines) + "\n"
