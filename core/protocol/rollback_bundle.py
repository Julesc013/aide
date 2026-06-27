"""RollbackBundle v0 helpers.

RollbackBundle prepares recovery metadata for an accepted UpdatePlan. It is
not a rollback applier, update applier, installer, uninstaller, target scanner,
target mutator, or release publisher.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import distribution_manifest, envelope, install_record, ownership_ledger, project_lock, update_plan


API_VERSION = envelope.API_VERSION
KIND = "RollbackBundle"
SCHEMA_VERSION = "aide.rollback-bundle.v0"
PROTOCOL_VERSION = "0.1.0"
TASK_ID = "AIDE-BUILD-ROLLBACK-BUNDLE-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-ROLLBACK-BUNDLE-V0-01"
PROPOSED_CAPABILITY = "rollback_bundle_v0"
DETERMINISTIC_TIMESTAMP = "fixture-timestamp:rollback-bundle-v0"
DEFAULT_EVIDENCE_REF = "aide://evidence/rollback-bundle-v0/source-projection"

REPORT_ROOT = Path(".aide/reports/rollback-bundle-v0")
SCHEMA_PATH = Path(".aide/protocol/aide-rollback-bundle-v0.schema.json")
FIXTURE_ROOT = Path(".aide/fixtures/rollback-bundle-v0")

PROJECTION_JSON = REPORT_ROOT / "projection.json"
PROJECT_REPORT_JSON = REPORT_ROOT / "project-report.json"
STATUS_MD = REPORT_ROOT / "status.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FIXTURE_MATRIX_JSON = REPORT_ROOT / "fixture-matrix.json"
FIXTURE_MATRIX_MD = REPORT_ROOT / "fixture-matrix.md"
REVERSE_OPERATION_SUMMARY_MD = REPORT_ROOT / "reverse-operation-summary.md"
NO_APPLY_BOUNDARY_MD = REPORT_ROOT / "no-apply-boundary.md"
LIMITATIONS_MD = REPORT_ROOT / "limitations.md"

UPDATE_PLAN_ACCEPTANCE_JSON = Path(".aide/reports/update-plan-v1-acceptance/validation-summary.json")

SUPPORTED_REQUIRED_FEATURES = {
    "rollback_bundle_v0",
    "distribution_manifest_v1",
    "project_lock_v0",
    "ownership_ledger_v1",
    "install_record_v0",
    "update_plan_v1",
    "sha256_digest_canonical_json_v1",
    "no_apply_rollback_bundle_v0",
}

SUPPORTED_OPTIONAL_FEATURES = {
    "manual_review_item_v0",
    "rollback_unavailable_limitation_v0",
    "mixed_managed_file_section_rollback_v0",
}

SUPPORTED_REVERSE_OPERATION_CLASSES = {
    "restore_managed_file_preimage",
    "restore_managed_section_preimage",
    "remove_added_managed_file",
    "remove_added_managed_section",
    "restore_project_lock",
    "restore_install_record",
    "restore_ownership_ledger",
    "regenerate_project_output",
    "manual_review_required",
    "rollback_unavailable",
    "refuse",
}

PREIMAGE_REVERSE_OPERATION_CLASSES = {
    "restore_managed_file_preimage",
    "restore_managed_section_preimage",
}

TARGET_TOUCHING_REVERSE_OPERATION_CLASSES = {
    "restore_managed_file_preimage",
    "restore_managed_section_preimage",
    "remove_added_managed_file",
    "remove_added_managed_section",
    "regenerate_project_output",
}

UNSAFE_OWNERSHIP_CLASSES = {
    "project_owned",
    "project_overlay",
    "local_only",
    "runtime_generated",
    "evidence_only",
    "never_touch",
    "unknown",
}

REFUSAL_CODES = [
    "rollback_bundle.missing",
    "rollback_bundle.invalid",
    "rollback_bundle.update_plan_missing",
    "rollback_bundle.target_project_missing",
    "rollback_bundle.project_lock_missing",
    "rollback_bundle.candidate_project_lock_missing",
    "rollback_bundle.ownership_ledger_missing",
    "rollback_bundle.install_record_missing",
    "rollback_bundle.preimage_artifact_missing",
    "rollback_bundle.preimage_digest_mismatch",
    "rollback_bundle.candidate_distribution_mismatch",
    "rollback_bundle.source_distribution_mismatch",
    "rollback_bundle.project_lock_mismatch",
    "rollback_bundle.ownership_ledger_mismatch",
    "rollback_bundle.install_record_mismatch",
    "rollback_bundle.project_owned_reverse_mutation",
    "rollback_bundle.project_overlay_reverse_mutation",
    "rollback_bundle.local_only_reverse_mutation",
    "rollback_bundle.runtime_generated_reverse_mutation",
    "rollback_bundle.evidence_only_reverse_mutation",
    "rollback_bundle.never_touch_reverse_mutation",
    "rollback_bundle.unknown_ownership_reverse_operation",
    "rollback_bundle.reverse_operation_evidence_missing",
    "rollback_bundle.rollback_apply_authority_claimed",
    "rollback_bundle.apply_authority_claimed",
    "rollback_bundle.target_mutation_claimed",
    "rollback_bundle.unknown_required_feature",
    "rollback_bundle.extension_required_unknown",
    "rollback_bundle.absolute_path_forbidden",
    "rollback_bundle.path_traversal_forbidden",
    "rollback_bundle.source_state_contamination",
    "rollback_bundle.source_output_as_target_truth",
    "rollback_bundle.digest_mismatch",
    "rollback_bundle.fixture_failure",
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
SOURCE_OUTPUT_RE = re.compile(
    r"(^|/)\.aide/(context|reports|repo|roots|tools|install|repair|upgrade|rollback|uninstall)/latest[-_/]",
    re.IGNORECASE,
)


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
    return update_plan.load_distribution_manifest(repo_root)


def load_project_lock(repo_root: str | Path = ".") -> dict[str, Any]:
    return update_plan.load_project_lock(repo_root)


def load_ownership_ledger(repo_root: str | Path = ".") -> dict[str, Any]:
    return update_plan.load_ownership_ledger(repo_root)


def load_install_record_source(repo_root: str | Path = ".") -> dict[str, Any]:
    return update_plan.load_install_record_source(repo_root)


def load_update_plan_source(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    path = root / update_plan.PROJECTION_JSON
    if path.exists():
        return load_json(path)
    return update_plan.build_update_plan(root)


def update_plan_is_accepted(repo_root: str | Path = ".") -> bool:
    path = Path(repo_root) / UPDATE_PLAN_ACCEPTANCE_JSON
    if not path.exists():
        return False
    try:
        report = load_json(path)
    except Exception:
        return False
    return (
        report.get("result") in {"ACCEPTED", "ACCEPTED_WITH_WARNINGS"}
        and report.get("accepted_capability") == "update_plan_v1"
        and int(report.get("material_finding_count", 1)) == 0
        and int(report.get("missing_evidence", 1)) == 0
    )


def object_digest(record: dict[str, Any], status_key: str, digest_func: Any) -> str:
    digest = record.get("status", {}).get(status_key)
    if isinstance(digest, str) and digest:
        return digest
    return digest_func(record)


def rollback_bundle_digest(record: dict[str, Any]) -> str:
    payload = copy.deepcopy(record)
    status = payload.get("status")
    if isinstance(status, dict):
        status.pop("rollback_bundle_digest", None)
    return sha256_digest(canonical_json_bytes(payload))


def finalize_rollback_bundle(record: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(record)
    result.setdefault("status", {})["rollback_bundle_digest"] = rollback_bundle_digest(result)
    return result


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower() or "unknown"


def _operation_sort_key(operation: dict[str, Any]) -> str:
    return str(operation.get("target_relative_path", "")) + "\0" + str(operation.get("operation_ref", ""))


def _preimage_record(operation: dict[str, Any], *, section: bool = False) -> dict[str, Any]:
    operation_ref = str(operation.get("operation_ref", "aide://update-plan/operation/unknown"))
    suffix = _slug(operation_ref.split("/")[-1])
    artifact_ref = "aide://rollback-bundle/preimage/" + suffix
    return {
        "preimage_ref": artifact_ref,
        "operation_ref": operation_ref,
        "target_relative_path": operation.get("target_relative_path"),
        "ownership_entry_ref": operation.get("ownership_entry_ref"),
        "ownership_class": operation.get("ownership_class"),
        "preimage_digest": operation.get("preimage_digest"),
        "postimage_digest": operation.get("postimage_digest"),
        "section_identity": operation.get("section_identity") if section else None,
        "artifact_kind": "managed_section_preimage" if section else "managed_file_preimage",
        "evidence_refs": list(operation.get("evidence_refs", [DEFAULT_EVIDENCE_REF])),
        "extensions": {},
    }


def _reverse_class_for(operation_class: str) -> str:
    mapping = {
        "add_managed_file": "remove_added_managed_file",
        "update_managed_file": "restore_managed_file_preimage",
        "remove_managed_file": "restore_managed_file_preimage",
        "add_managed_section": "remove_added_managed_section",
        "update_managed_section": "restore_managed_section_preimage",
        "remove_managed_section": "restore_managed_section_preimage",
        "regenerate_project_output": "regenerate_project_output",
        "manual_review_required": "manual_review_required",
        "refuse": "refuse",
    }
    if operation_class.startswith("preserve_"):
        return "manual_review_required"
    return mapping.get(operation_class, "manual_review_required")


def _reverse_operation(operation: dict[str, Any]) -> dict[str, Any]:
    operation_ref = str(operation.get("operation_ref", "aide://update-plan/operation/unknown"))
    reverse_class = _reverse_class_for(str(operation.get("operation_class", "")))
    suffix = _slug(operation_ref.split("/")[-1])
    preimage_ref = "aide://rollback-bundle/preimage/" + suffix
    evidence_refs = list(operation.get("evidence_refs", [DEFAULT_EVIDENCE_REF]))
    return {
        "reverse_operation_ref": "aide://rollback-bundle/reverse-operation/" + suffix,
        "source_operation_ref": operation_ref,
        "reverse_operation_class": reverse_class,
        "target_relative_path": operation.get("target_relative_path"),
        "ownership_entry_ref": operation.get("ownership_entry_ref"),
        "ownership_class": operation.get("ownership_class"),
        "preimage_artifact_ref": preimage_ref if reverse_class in PREIMAGE_REVERSE_OPERATION_CLASSES else None,
        "preimage_digest": operation.get("preimage_digest"),
        "postimage_digest": operation.get("postimage_digest"),
        "manual_review_required": reverse_class in {"manual_review_required", "rollback_unavailable", "refuse"},
        "rollback_apply_implemented": False,
        "target_repository_mutation_performed": False,
        "source_output_used_as_target_truth": False,
        "evidence_refs": evidence_refs,
        "extensions": {},
    }


def _metadata_reverse_operation(kind: str, ref: str, digest: str) -> dict[str, Any]:
    suffix = _slug(kind)
    return {
        "reverse_operation_ref": f"aide://rollback-bundle/reverse-operation/{suffix}",
        "source_operation_ref": f"aide://update-plan/metadata/{suffix}",
        "reverse_operation_class": kind,
        "target_relative_path": None,
        "ownership_entry_ref": None,
        "ownership_class": "metadata_only",
        "preimage_artifact_ref": f"aide://rollback-bundle/preimage/{suffix}",
        "preimage_digest": digest,
        "postimage_digest": digest,
        "restore_ref": ref,
        "manual_review_required": False,
        "rollback_apply_implemented": False,
        "target_repository_mutation_performed": False,
        "source_output_used_as_target_truth": False,
        "evidence_refs": [DEFAULT_EVIDENCE_REF],
        "extensions": {},
    }


def build_rollback_bundle(
    repo_root: str | Path = ".",
    *,
    plan: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
    lock: dict[str, Any] | None = None,
    ledger: dict[str, Any] | None = None,
    install_source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    root = Path(repo_root)
    update_source = plan if plan is not None else load_update_plan_source(root)
    distribution = manifest if manifest is not None else load_distribution_manifest(root)
    project_lock_data = lock if lock is not None else load_project_lock(root)
    ownership = ledger if ledger is not None else load_ownership_ledger(root)
    install_source = install_source if install_source is not None else load_install_record_source(root)

    operations = sorted(update_source.get("spec", {}).get("planned_operations", []), key=_operation_sort_key)
    managed_file_preimages = [
        _preimage_record(operation, section=False)
        for operation in operations
        if str(operation.get("operation_class")) in {"update_managed_file", "remove_managed_file"}
    ]
    managed_section_preimages = [
        _preimage_record(operation, section=True)
        for operation in operations
        if str(operation.get("operation_class")) in {"update_managed_section", "remove_managed_section"}
    ]
    reverse_operations = [_reverse_operation(operation) for operation in operations]

    current_lock_ref = update_source.get("metadata", {}).get("current_project_lock_ref") or project_lock_data.get("metadata", {}).get("project_lock_ref")
    candidate_lock_ref = update_source.get("metadata", {}).get("candidate_project_lock_ref") or project_lock_data.get("metadata", {}).get("project_lock_ref")
    current_lock_digest = update_source.get("metadata", {}).get("current_project_lock_digest") or object_digest(project_lock_data, "project_lock_digest", project_lock.project_lock_digest)
    candidate_lock_digest = update_source.get("metadata", {}).get("candidate_project_lock_digest") or object_digest(project_lock_data, "project_lock_digest", project_lock.project_lock_digest)
    install_ref = install_source.get("metadata", {}).get("install_record_ref")
    install_digest = object_digest(install_source, "install_record_digest", install_record.install_record_digest)
    ledger_ref = update_source.get("metadata", {}).get("ownership_ledger_ref") or ownership.get("metadata", {}).get("ledger_ref")
    ledger_digest = update_source.get("metadata", {}).get("ownership_ledger_digest") or object_digest(ownership, "ownership_ledger_digest", ownership_ledger.ownership_ledger_digest)
    source_distribution_ref = distribution.get("metadata", {}).get("distribution_ref")
    distribution_digest = object_digest(distribution, "distribution_digest", distribution_manifest.distribution_digest)

    reverse_operations.extend(
        [
            _metadata_reverse_operation("restore_project_lock", str(current_lock_ref), str(current_lock_digest)),
            _metadata_reverse_operation("restore_install_record", str(install_ref), str(install_digest)),
            _metadata_reverse_operation("restore_ownership_ledger", str(ledger_ref), str(ledger_digest)),
        ]
    )
    preimage_artifact_refs = sorted(
        {
            str(item.get("preimage_ref") or item.get("preimage_artifact_ref"))
            for item in managed_file_preimages + managed_section_preimages + reverse_operations
            if item.get("preimage_ref") or item.get("preimage_artifact_ref")
        }
    )
    operation_rollback_map = [
        {
            "source_operation_ref": operation.get("source_operation_ref"),
            "reverse_operation_ref": operation.get("reverse_operation_ref"),
            "reverse_operation_class": operation.get("reverse_operation_class"),
            "disposition": "prepared_no_apply" if operation.get("reverse_operation_class") not in {"manual_review_required", "rollback_unavailable", "refuse"} else "fail_closed_no_apply",
            "evidence_refs": operation.get("evidence_refs", []),
            "extensions": {},
        }
        for operation in reverse_operations
    ]
    limitations = [
        {
            "limitation_ref": "aide://rollback-bundle/limitation/no-apply-authority",
            "limitation_class": "no_apply_authority",
            "disposition": "future apply tasks must be separately accepted",
            "evidence_refs": [DEFAULT_EVIDENCE_REF],
            "extensions": {},
        }
    ]
    conflicts = update_source.get("spec", {}).get("conflicts", [])
    if conflicts:
        limitations.append(
            {
                "limitation_ref": "aide://rollback-bundle/limitation/update-plan-conflicts",
                "limitation_class": "manual_review_required",
                "disposition": "UpdatePlan conflicts remain fail-closed and are not rollback actions.",
                "evidence_refs": [DEFAULT_EVIDENCE_REF],
                "extensions": {},
            }
        )
    record = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "rollback_bundle_ref": "aide://rollback-bundle/aide-self-no-apply-rollback-bundle-v0",
            "update_plan_ref": update_source.get("metadata", {}).get("update_plan_ref"),
            "update_plan_digest": object_digest(update_source, "update_plan_digest", update_plan.update_plan_digest),
            "target_project_ref": update_source.get("metadata", {}).get("target_project_ref"),
            "target_project_identity": update_source.get("metadata", {}).get("target_project_identity"),
            "prior_project_lock_ref": current_lock_ref,
            "prior_project_lock_digest": current_lock_digest,
            "candidate_project_lock_ref": candidate_lock_ref,
            "candidate_project_lock_digest": candidate_lock_digest,
            "prior_ownership_ledger_ref": ledger_ref,
            "prior_ownership_ledger_digest": ledger_digest,
            "source_distribution_ref": source_distribution_ref,
            "source_distribution_digest": distribution_digest,
            "candidate_distribution_ref": update_source.get("metadata", {}).get("candidate_distribution_ref"),
            "candidate_distribution_digest": update_source.get("metadata", {}).get("candidate_distribution_digest"),
            "created_at": DETERMINISTIC_TIMESTAMP,
            "created_by": "aide-self-hosting-fixture",
            "prior_rollback_bundle_ref": None,
            "superseded_by_ref": None,
            "extensions": {},
        },
        "spec": {
            "prior_install_record_refs": [install_ref],
            "prior_install_record_digests": [install_digest],
            "preimage_artifact_refs": preimage_artifact_refs,
            "managed_file_preimages": managed_file_preimages,
            "managed_section_preimages": managed_section_preimages,
            "reverse_operations": reverse_operations,
            "operation_rollback_map": operation_rollback_map,
            "validation_plan": [
                "validate accepted UpdatePlan binding and predecessor refs",
                "validate every reverse operation remains no-apply metadata",
                "validate preimage digest and evidence refs before any future apply-capable task",
            ],
            "integrity_checks": [
                "canonical rollback bundle digest",
                "preimage digest equality to UpdatePlan operation preimages",
                "no source latest output as target truth",
            ],
            "manual_review_items": [
                {
                    "item_ref": conflict.get("conflict_ref"),
                    "reason": conflict.get("conflict_type"),
                    "required": True,
                    "extensions": {},
                }
                for conflict in conflicts
            ],
            "limitations": limitations,
            "risk_class": "medium" if conflicts else "low",
            "evidence_refs": [DEFAULT_EVIDENCE_REF],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "required_features": [
                "rollback_bundle_v0",
                "distribution_manifest_v1",
                "project_lock_v0",
                "ownership_ledger_v1",
                "install_record_v0",
                "update_plan_v1",
                "sha256_digest_canonical_json_v1",
                "no_apply_rollback_bundle_v0",
            ],
            "optional_features": ["manual_review_item_v0", "rollback_unavailable_limitation_v0"],
            "source_output_used_as_target_truth": False,
            "target_repository_mutation_performed": False,
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "validation_result": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "recommended_next_task": CHECK_TASK_ID,
            "rollback_bundle_digest": "",
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
    return finalize_rollback_bundle(record)


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
        result = []
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


def _path_error(value: str) -> str | None:
    if not value or value.startswith("aide://") or value.startswith("fixture-timestamp:"):
        return None
    normalized = value.replace("\\", "/")
    if SOURCE_OUTPUT_RE.search(normalized):
        return "rollback_bundle.source_state_contamination"
    if PATH_RE.search(normalized):
        if ".." in [part for part in normalized.split("/") if part]:
            return "rollback_bundle.path_traversal_forbidden"
        return "rollback_bundle.absolute_path_forbidden"
    return None


def _boolean_claims_authority(data: Any, errors: list[dict[str, str]]) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            key_text = str(key)
            if value is True and "rollback_apply" in key_text:
                _add_error(errors, "rollback_bundle.rollback_apply_authority_claimed", f"rollback apply authority claimed by {key_text}")
            elif value is True and ("apply" in key_text or "install_authority" in key_text or "update_authority" in key_text or "uninstall_authority" in key_text):
                _add_error(errors, "rollback_bundle.apply_authority_claimed", f"apply authority claimed by {key_text}")
            if value is True and ("mutation" in key_text or "mutate" in key_text):
                _add_error(errors, "rollback_bundle.target_mutation_claimed", f"target mutation claimed by {key_text}")
            _boolean_claims_authority(value, errors)
    elif isinstance(data, list):
        for item in data:
            _boolean_claims_authority(item, errors)


def _preimage_index(bundle: dict[str, Any]) -> dict[str, dict[str, Any]]:
    spec = bundle.get("spec", {}) if isinstance(bundle.get("spec"), dict) else {}
    items = []
    items.extend(spec.get("managed_file_preimages", []) if isinstance(spec.get("managed_file_preimages"), list) else [])
    items.extend(spec.get("managed_section_preimages", []) if isinstance(spec.get("managed_section_preimages"), list) else [])
    return {str(item.get("preimage_ref")): item for item in items if isinstance(item, dict) and item.get("preimage_ref")}


def _update_operation_index(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    operations = plan.get("spec", {}).get("planned_operations", [])
    return {str(item.get("operation_ref")): item for item in operations if isinstance(item, dict) and item.get("operation_ref")}


def _validate_reverse_operations(bundle: dict[str, Any], plan: dict[str, Any], errors: list[dict[str, str]]) -> None:
    spec = bundle.get("spec", {}) if isinstance(bundle.get("spec"), dict) else {}
    preimages = _preimage_index(bundle)
    plan_operations = _update_operation_index(plan)
    artifact_refs = set(str(item) for item in spec.get("preimage_artifact_refs", []) if isinstance(item, str))
    for operation in spec.get("reverse_operations", []) if isinstance(spec.get("reverse_operations"), list) else []:
        if not isinstance(operation, dict):
            _add_error(errors, "rollback_bundle.invalid", "reverse operation must be an object")
            continue
        reverse_class = str(operation.get("reverse_operation_class", ""))
        ownership_class = str(operation.get("ownership_class", ""))
        target_path = operation.get("target_relative_path")
        if reverse_class not in SUPPORTED_REVERSE_OPERATION_CLASSES:
            _add_error(errors, "rollback_bundle.invalid", f"unsupported reverse operation class: {reverse_class}")
        if not operation.get("evidence_refs"):
            _add_error(errors, "rollback_bundle.reverse_operation_evidence_missing", "reverse operation evidence refs are required")
        if operation.get("source_output_used_as_target_truth") is True:
            _add_error(errors, "rollback_bundle.source_output_as_target_truth", "source output cannot become target truth")
        if operation.get("target_repository_mutation_performed") is True:
            _add_error(errors, "rollback_bundle.target_mutation_claimed", "reverse operation claims target mutation")
        if reverse_class in TARGET_TOUCHING_REVERSE_OPERATION_CLASSES and ownership_class in UNSAFE_OWNERSHIP_CLASSES:
            code_by_class = {
                "project_owned": "rollback_bundle.project_owned_reverse_mutation",
                "project_overlay": "rollback_bundle.project_overlay_reverse_mutation",
                "local_only": "rollback_bundle.local_only_reverse_mutation",
                "runtime_generated": "rollback_bundle.runtime_generated_reverse_mutation",
                "evidence_only": "rollback_bundle.evidence_only_reverse_mutation",
                "never_touch": "rollback_bundle.never_touch_reverse_mutation",
                "unknown": "rollback_bundle.unknown_ownership_reverse_operation",
            }
            _add_error(errors, code_by_class[ownership_class], f"reverse operation touches {ownership_class}: {operation.get('reverse_operation_ref')}")
        if isinstance(target_path, str):
            path_code = _path_error(target_path)
            if path_code:
                _add_error(errors, path_code, f"unsafe target path: {target_path}")
        if reverse_class in PREIMAGE_REVERSE_OPERATION_CLASSES:
            artifact_ref = str(operation.get("preimage_artifact_ref") or "")
            if not artifact_ref or artifact_ref not in artifact_refs or artifact_ref not in preimages:
                _add_error(errors, "rollback_bundle.preimage_artifact_missing", "preimage artifact ref is missing or not declared")
                continue
            preimage = preimages[artifact_ref]
            if operation.get("preimage_digest") != preimage.get("preimage_digest"):
                _add_error(errors, "rollback_bundle.preimage_digest_mismatch", "reverse operation preimage digest does not match preimage artifact")
            source_operation = plan_operations.get(str(operation.get("source_operation_ref")))
            if source_operation and operation.get("preimage_digest") != source_operation.get("preimage_digest"):
                _add_error(errors, "rollback_bundle.preimage_digest_mismatch", "reverse operation preimage digest does not match UpdatePlan operation")


def validate_rollback_bundle_object(
    bundle: dict[str, Any] | None,
    *,
    plan: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
    lock: dict[str, Any] | None = None,
    ledger: dict[str, Any] | None = None,
    install_source: dict[str, Any] | None = None,
    repo_root: str | Path | None = None,
    require_update_plan_acceptance: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[str] = []
    if bundle is None:
        _add_error(errors, "rollback_bundle.missing", "RollbackBundle is missing")
        return _validation_result(errors, warnings)
    if not isinstance(bundle, dict):
        _add_error(errors, "rollback_bundle.invalid", "RollbackBundle root must be an object")
        return _validation_result(errors, warnings)
    for field in ["apiVersion", "kind", "schema_version", "metadata", "spec", "status", "extensions"]:
        if field not in bundle:
            _add_error(errors, "rollback_bundle.invalid", f"missing required field: {field}")
    if bundle.get("kind") != KIND:
        _add_error(errors, "rollback_bundle.invalid", "kind must be RollbackBundle")
    if bundle.get("schema_version") != SCHEMA_VERSION:
        _add_error(errors, "rollback_bundle.invalid", f"schema_version must be {SCHEMA_VERSION}")

    root = Path(repo_root or ".")
    update_source = plan if plan is not None else load_update_plan_source(root)
    distribution = manifest if manifest is not None else load_distribution_manifest(root)
    project_lock_data = lock if lock is not None else load_project_lock(root)
    ownership = ledger if ledger is not None else load_ownership_ledger(root)
    install_source = install_source if install_source is not None else load_install_record_source(root)
    metadata = bundle.get("metadata") if isinstance(bundle.get("metadata"), dict) else {}
    spec = bundle.get("spec") if isinstance(bundle.get("spec"), dict) else {}
    status = bundle.get("status") if isinstance(bundle.get("status"), dict) else {}

    if not metadata.get("update_plan_ref"):
        _add_error(errors, "rollback_bundle.update_plan_missing", "update_plan_ref is required")
    if not metadata.get("target_project_ref"):
        _add_error(errors, "rollback_bundle.target_project_missing", "target_project_ref is required")
    if not metadata.get("prior_project_lock_ref"):
        _add_error(errors, "rollback_bundle.project_lock_missing", "prior_project_lock_ref is required")
    if not metadata.get("candidate_project_lock_ref"):
        _add_error(errors, "rollback_bundle.candidate_project_lock_missing", "candidate_project_lock_ref is required")
    if not metadata.get("prior_ownership_ledger_ref"):
        _add_error(errors, "rollback_bundle.ownership_ledger_missing", "prior_ownership_ledger_ref is required")
    if not spec.get("prior_install_record_refs"):
        _add_error(errors, "rollback_bundle.install_record_missing", "prior_install_record_refs are required")
    if not spec.get("evidence_refs"):
        _add_error(errors, "rollback_bundle.reverse_operation_evidence_missing", "bundle evidence_refs are required")

    expected_plan_ref = update_source.get("metadata", {}).get("update_plan_ref")
    expected_plan_digest = object_digest(update_source, "update_plan_digest", update_plan.update_plan_digest)
    if metadata.get("update_plan_ref") != expected_plan_ref or metadata.get("update_plan_digest") != expected_plan_digest:
        _add_error(errors, "rollback_bundle.update_plan_missing", "accepted UpdatePlan ref or digest is not cited")
    expected_distribution_ref = distribution.get("metadata", {}).get("distribution_ref")
    expected_distribution_digest = object_digest(distribution, "distribution_digest", distribution_manifest.distribution_digest)
    if metadata.get("source_distribution_ref") != expected_distribution_ref or metadata.get("source_distribution_digest") != expected_distribution_digest:
        _add_error(errors, "rollback_bundle.source_distribution_mismatch", "source distribution does not match DistributionManifest")
    if metadata.get("candidate_distribution_ref") != update_source.get("metadata", {}).get("candidate_distribution_ref") or metadata.get("candidate_distribution_digest") != update_source.get("metadata", {}).get("candidate_distribution_digest"):
        _add_error(errors, "rollback_bundle.candidate_distribution_mismatch", "candidate distribution does not match UpdatePlan")
    expected_lock_ref = project_lock_data.get("metadata", {}).get("project_lock_ref")
    expected_lock_digest = object_digest(project_lock_data, "project_lock_digest", project_lock.project_lock_digest)
    if metadata.get("prior_project_lock_ref") != expected_lock_ref or metadata.get("prior_project_lock_digest") != expected_lock_digest:
        _add_error(errors, "rollback_bundle.project_lock_mismatch", "prior ProjectLock ref or digest does not match")
    if metadata.get("candidate_project_lock_ref") != update_source.get("metadata", {}).get("candidate_project_lock_ref") or metadata.get("candidate_project_lock_digest") != update_source.get("metadata", {}).get("candidate_project_lock_digest"):
        _add_error(errors, "rollback_bundle.project_lock_mismatch", "candidate ProjectLock ref or digest does not match UpdatePlan")
    expected_ledger_ref = ownership.get("metadata", {}).get("ledger_ref")
    expected_ledger_digest = object_digest(ownership, "ownership_ledger_digest", ownership_ledger.ownership_ledger_digest)
    if metadata.get("prior_ownership_ledger_ref") != expected_ledger_ref or metadata.get("prior_ownership_ledger_digest") != expected_ledger_digest:
        _add_error(errors, "rollback_bundle.ownership_ledger_mismatch", "OwnershipLedger ref or digest does not match")
    expected_install_ref = install_source.get("metadata", {}).get("install_record_ref")
    expected_install_digest = object_digest(install_source, "install_record_digest", install_record.install_record_digest)
    if expected_install_ref not in (spec.get("prior_install_record_refs") or []) or expected_install_digest not in (spec.get("prior_install_record_digests") or []):
        _add_error(errors, "rollback_bundle.install_record_mismatch", "InstallRecord ref or digest is not cited")
    if require_update_plan_acceptance and (repo_root is None or not update_plan_is_accepted(root)):
        _add_error(errors, "rollback_bundle.update_plan_missing", "UpdatePlan v1 is not accepted")

    for feature in spec.get("required_features", []) if isinstance(spec.get("required_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES:
            _add_error(errors, "rollback_bundle.unknown_required_feature", f"unknown required feature: {feature}")
    for feature in spec.get("optional_features", []) if isinstance(spec.get("optional_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES and feature not in SUPPORTED_OPTIONAL_FEATURES:
            warnings.append(f"unknown optional feature tolerated: {feature}")
    if _extension_requires_unknown(bundle.get("extensions", {})) or _extension_requires_unknown(spec.get("extensions", {})):
        _add_error(errors, "rollback_bundle.extension_required_unknown", "unknown required extension present")
    if spec.get("source_output_used_as_target_truth") is True:
        _add_error(errors, "rollback_bundle.source_output_as_target_truth", "source output cannot become target truth")
    if spec.get("target_repository_mutation_performed") is True:
        _add_error(errors, "rollback_bundle.target_mutation_claimed", "target mutation claimed by bundle")
    for value in _iter_string_values(spec):
        path_code = _path_error(value)
        if path_code:
            _add_error(errors, path_code, f"unsafe source or target string: {value}")
    _validate_reverse_operations(bundle, update_source, errors)
    _boolean_claims_authority(spec, errors)
    _boolean_claims_authority(status, errors)
    expected_digest = rollback_bundle_digest(bundle)
    if status.get("rollback_bundle_digest") and status.get("rollback_bundle_digest") != expected_digest:
        _add_error(errors, "rollback_bundle.digest_mismatch", "rollback_bundle_digest does not match canonical payload")
    return _validation_result(errors, warnings)


def minimal_fixture_record() -> dict[str, Any]:
    manifest = distribution_manifest.minimal_fixture_manifest()
    lock = project_lock.minimal_fixture_lock()
    ledger = ownership_ledger.minimal_fixture_ledger()
    install_source = install_record.minimal_fixture_record()
    plan = update_plan.minimal_fixture_record()
    return build_rollback_bundle(
        manifest=manifest,
        lock=lock,
        ledger=ledger,
        install_source=install_source,
        plan=plan,
    )


def mutate(base: dict[str, Any], mutator: Any) -> dict[str, Any]:
    record = copy.deepcopy(base)
    mutator(record)
    return finalize_rollback_bundle(record)


def _first_reverse_operation(record: dict[str, Any]) -> dict[str, Any]:
    return record["spec"]["reverse_operations"][0]


def _first_preimage_reverse_operation(record: dict[str, Any]) -> dict[str, Any]:
    for operation in record["spec"]["reverse_operations"]:
        if operation.get("reverse_operation_class") in PREIMAGE_REVERSE_OPERATION_CLASSES:
            return operation
    raise AssertionError("fixture missing preimage reverse operation")


def _replace_first_reverse(record: dict[str, Any], *, reverse_class: str, ownership_class: str, path: str | None = None) -> None:
    operation = _first_reverse_operation(record)
    operation["reverse_operation_class"] = reverse_class
    operation["ownership_class"] = ownership_class
    if path is not None:
        operation["target_relative_path"] = path


def _with_single_reverse(record: dict[str, Any], reverse_class: str) -> None:
    keep = None
    for operation in record["spec"]["reverse_operations"]:
        if operation.get("reverse_operation_class") == reverse_class:
            keep = operation
            break
    if keep is None:
        keep = _first_reverse_operation(record)
        keep["reverse_operation_class"] = reverse_class
    record["spec"]["reverse_operations"] = [keep]
    record["spec"]["operation_rollback_map"] = [
        {
            "source_operation_ref": keep.get("source_operation_ref"),
            "reverse_operation_ref": keep.get("reverse_operation_ref"),
            "reverse_operation_class": keep.get("reverse_operation_class"),
            "disposition": "prepared_no_apply",
            "evidence_refs": keep.get("evidence_refs", []),
            "extensions": {},
        }
    ]


def write_fixture_corpus(repo_root: str | Path = ".") -> None:
    root = Path(repo_root)
    base = minimal_fixture_record()
    valid_cases = {
        "no-op-rollback-bundle": mutate(base, lambda d: d["spec"].__setitem__("limitations", d["spec"]["limitations"] + [{"limitation_ref": "aide://rollback-bundle/limitation/no-op", "limitation_class": "no_op", "evidence_refs": [DEFAULT_EVIDENCE_REF], "extensions": {}}])),
        "managed-file-preimage-rollback-plan": mutate(base, lambda d: _with_single_reverse(d, "restore_managed_file_preimage")),
        "managed-section-preimage-rollback-plan": mutate(base, lambda d: _with_single_reverse(d, "restore_managed_section_preimage")),
        "remove-added-managed-file-reverse-plan": mutate(base, lambda d: _replace_first_reverse(d, reverse_class="remove_added_managed_file", ownership_class="vendor_managed_file", path=".aide/new-managed-file.txt")),
        "remove-added-managed-section-reverse-plan": mutate(base, lambda d: _replace_first_reverse(d, reverse_class="remove_added_managed_section", ownership_class="vendor_managed_section", path="AGENTS.md")),
        "project-lock-restore-plan": mutate(base, lambda d: _with_single_reverse(d, "restore_project_lock")),
        "install-record-restore-plan": mutate(base, lambda d: _with_single_reverse(d, "restore_install_record")),
        "ownership-ledger-restore-plan": mutate(base, lambda d: _with_single_reverse(d, "restore_ownership_ledger")),
        "manual-review-limitation": mutate(base, lambda d: d["spec"]["manual_review_items"].append({"item_ref": "aide://manual-review/rollback-bundle/fixture", "reason": "fixture manual review", "required": True, "extensions": {}})),
        "rollback-unavailable-limitation": mutate(base, lambda d: (d["spec"]["limitations"].append({"limitation_ref": "aide://rollback-bundle/limitation/unavailable-fixture", "limitation_class": "rollback_unavailable", "evidence_refs": [DEFAULT_EVIDENCE_REF], "extensions": {}}), _replace_first_reverse(d, reverse_class="rollback_unavailable", ownership_class="vendor_managed_file", path=".aide/unavailable.txt"))),
        "mixed-managed-file-and-section-plan": base,
        "conflict-only-rollback-bundle": mutate(base, lambda d: (d["spec"].__setitem__("managed_file_preimages", []), d["spec"].__setitem__("managed_section_preimages", []), d["spec"].__setitem__("preimage_artifact_refs", []), d["spec"].__setitem__("reverse_operations", [copy.deepcopy(op) for op in d["spec"]["reverse_operations"] if op.get("reverse_operation_class") in {"manual_review_required", "refuse"}]))),
        "optional-extensions-preservation": mutate(base, lambda d: (d["spec"]["optional_features"].append("future.optional.rollback-bundle"), d.__setitem__("extensions", {"future.optional": {"preserve": True}}))),
    }
    invalid_cases = {
        "missing-update-plan-ref": mutate(base, lambda d: d["metadata"].__setitem__("update_plan_ref", "")),
        "missing-prior-lock": mutate(base, lambda d: d["metadata"].__setitem__("prior_project_lock_ref", "")),
        "missing-ownership-ledger": mutate(base, lambda d: d["metadata"].__setitem__("prior_ownership_ledger_ref", "")),
        "missing-preimage": mutate(base, lambda d: (d["spec"].__setitem__("managed_file_preimages", []), d["spec"].__setitem__("managed_section_preimages", []), d["spec"].__setitem__("preimage_artifact_refs", []))),
        "preimage-digest-mismatch": mutate(base, lambda d: _first_preimage_reverse_operation(d).__setitem__("preimage_digest", "sha256:" + "1" * 64)),
        "reverse-project-owned-mutation": mutate(base, lambda d: _replace_first_reverse(d, reverse_class="restore_managed_file_preimage", ownership_class="project_owned", path="README.md")),
        "reverse-local-only-mutation": mutate(base, lambda d: _replace_first_reverse(d, reverse_class="restore_managed_file_preimage", ownership_class="local_only", path="local-only/settings.json")),
        "reverse-never-touch-mutation": mutate(base, lambda d: _replace_first_reverse(d, reverse_class="restore_managed_file_preimage", ownership_class="never_touch", path=".git/config")),
        "unknown-ownership-reverse-operation": mutate(base, lambda d: _replace_first_reverse(d, reverse_class="restore_managed_file_preimage", ownership_class="unknown", path="unknown/file.txt")),
        "missing-rollback-evidence": mutate(base, lambda d: _first_reverse_operation(d).__setitem__("evidence_refs", [])),
        "absolute-path": mutate(base, lambda d: _first_reverse_operation(d).__setitem__("target_relative_path", "C:/outside/file.txt")),
        "traversal-path": mutate(base, lambda d: _first_reverse_operation(d).__setitem__("target_relative_path", "../outside/file.txt")),
        "source-latest-as-target-truth": mutate(base, lambda d: d["spec"]["limitations"].append({"limitation_ref": ".aide/context/latest-task-packet.md", "limitation_class": "source_output_misuse", "evidence_refs": [DEFAULT_EVIDENCE_REF], "extensions": {}})),
        "unknown-required-feature": mutate(base, lambda d: d["spec"]["required_features"].append("future.required.rollback-bundle")),
        "rollback-apply-authority-claim": mutate(base, lambda d: d["status"].__setitem__("rollback_apply_implemented", True)),
        "target-mutation-authority-claim": mutate(base, lambda d: d["status"].__setitem__("target_repository_mutation_implemented", True)),
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
    "missing-update-plan-ref": ["rollback_bundle.update_plan_missing"],
    "missing-prior-lock": ["rollback_bundle.project_lock_missing", "rollback_bundle.project_lock_mismatch"],
    "missing-ownership-ledger": ["rollback_bundle.ownership_ledger_missing", "rollback_bundle.ownership_ledger_mismatch"],
    "missing-preimage": ["rollback_bundle.preimage_artifact_missing"],
    "preimage-digest-mismatch": ["rollback_bundle.preimage_digest_mismatch"],
    "reverse-project-owned-mutation": ["rollback_bundle.project_owned_reverse_mutation"],
    "reverse-local-only-mutation": ["rollback_bundle.local_only_reverse_mutation"],
    "reverse-never-touch-mutation": ["rollback_bundle.never_touch_reverse_mutation"],
    "unknown-ownership-reverse-operation": ["rollback_bundle.unknown_ownership_reverse_operation"],
    "missing-rollback-evidence": ["rollback_bundle.reverse_operation_evidence_missing"],
    "absolute-path": ["rollback_bundle.absolute_path_forbidden"],
    "traversal-path": ["rollback_bundle.path_traversal_forbidden"],
    "source-latest-as-target-truth": ["rollback_bundle.source_state_contamination"],
    "unknown-required-feature": ["rollback_bundle.unknown_required_feature"],
    "rollback-apply-authority-claim": ["rollback_bundle.rollback_apply_authority_claimed"],
    "target-mutation-authority-claim": ["rollback_bundle.target_mutation_claimed"],
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
    plan = update_plan.minimal_fixture_record()
    result = validate_rollback_bundle_object(
        record,
        manifest=manifest,
        lock=lock,
        ledger=ledger,
        install_source=install_source,
        plan=plan,
        require_update_plan_acceptance=False,
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
    return {"schema_version": "aide.rollback-bundle-fixture-matrix.v0", "fixture_results": results}


def schema_alignment_errors(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema must declare Draft 2020-12")
    if schema.get("properties", {}).get("kind", {}).get("const") != KIND:
        errors.append("schema kind const must be RollbackBundle")
    metadata_required = set(schema.get("$defs", {}).get("metadata", {}).get("required", []))
    for field in [
        "rollback_bundle_ref",
        "update_plan_ref",
        "target_project_ref",
        "prior_project_lock_ref",
        "candidate_project_lock_ref",
        "prior_ownership_ledger_ref",
        "source_distribution_ref",
        "candidate_distribution_ref",
        "created_at",
        "created_by",
        "extensions",
    ]:
        if field not in metadata_required:
            errors.append(f"schema metadata missing required field: {field}")
    spec_required = set(schema.get("$defs", {}).get("spec", {}).get("required", []))
    for field in [
        "prior_install_record_refs",
        "preimage_artifact_refs",
        "managed_file_preimages",
        "managed_section_preimages",
        "reverse_operations",
        "operation_rollback_map",
        "validation_plan",
        "integrity_checks",
        "manual_review_items",
        "limitations",
        "risk_class",
        "evidence_refs",
        "explicit_non_capabilities",
        "extensions",
    ]:
        if field not in spec_required:
            errors.append(f"schema spec missing required field: {field}")
    return errors


def status(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    data = {
        "schema_version": "aide.rollback-bundle-status.v0",
        "status": "PASS_WITH_WARNINGS" if (root / SCHEMA_PATH).exists() and (root / "core/protocol/rollback_bundle.py").exists() else "FAILED_VALIDATION",
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/rollback_bundle.py").exists(),
        "update_plan_acceptance_report_exists": (root / UPDATE_PLAN_ACCEPTANCE_JSON).exists(),
        "rollback_bundle_projection_exists": (root / PROJECTION_JSON).exists(),
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
        "warnings": ["RollbackBundle v0 remains proposed until independent check and acceptance."],
    }
    write_text(root / STATUS_MD, render_status_md(data))
    return data


def project(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    bundle = build_rollback_bundle(root)
    validation = validate_rollback_bundle_object(bundle, repo_root=root)
    matrix = fixture_matrix(root)
    report = {
        "schema_version": "aide.rollback-bundle-project-report.v0",
        "status": validation["status"],
        "proposed_capability": PROPOSED_CAPABILITY,
        "rollback_bundle_path": PROJECTION_JSON.as_posix(),
        "rollback_bundle_digest": bundle["status"]["rollback_bundle_digest"],
        "reverse_operation_count": len(bundle["spec"]["reverse_operations"]),
        "preimage_artifact_count": len(bundle["spec"]["preimage_artifact_refs"]),
        "managed_file_preimage_count": len(bundle["spec"]["managed_file_preimages"]),
        "managed_section_preimage_count": len(bundle["spec"]["managed_section_preimages"]),
        "limitation_count": len(bundle["spec"]["limitations"]),
        "risk_class": bundle["spec"]["risk_class"],
        "recommended_next_task": CHECK_TASK_ID,
        "source_artifacts_mutated": False,
        "target_repository_mutation_implemented": False,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "warnings": [
            "RollbackBundle v0 prepares recovery metadata only and performs no rollback apply.",
            "Source generated latest-* outputs are not target truth.",
        ],
    }
    write_json(root / PROJECTION_JSON, bundle)
    write_json(root / PROJECT_REPORT_JSON, report)
    write_json(root / FIXTURE_MATRIX_JSON, matrix)
    write_text(root / FIXTURE_MATRIX_MD, render_fixture_matrix_md(matrix["fixture_results"]))
    write_text(root / REVERSE_OPERATION_SUMMARY_MD, render_reverse_operation_summary_md(bundle))
    write_text(root / NO_APPLY_BOUNDARY_MD, render_no_apply_boundary_md())
    write_text(root / LIMITATIONS_MD, render_limitations_md(bundle))
    status(root)
    write_validation_reports(root)
    return report


def validate(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    schema = load_schema(root)
    plan = load_update_plan_source(root)
    manifest = load_distribution_manifest(root)
    lock = load_project_lock(root)
    ledger = load_ownership_ledger(root)
    install_source = load_install_record_source(root)
    bundle = build_rollback_bundle(root, plan=plan, manifest=manifest, lock=lock, ledger=ledger, install_source=install_source)
    validation = validate_rollback_bundle_object(
        bundle,
        plan=plan,
        manifest=manifest,
        lock=lock,
        ledger=ledger,
        install_source=install_source,
        repo_root=root,
    )
    matrix = fixture_matrix(root)
    alignment_errors = schema_alignment_errors(schema)
    fixture_failures = [item for item in matrix["fixture_results"] if not item["passed"]]
    checks = {
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/rollback_bundle.py").exists(),
        "cli_registered": cli_registered(root),
        "rollback_bundle_generated": bundle["kind"] == KIND,
        "rollback_bundle_valid": validation["valid"],
        "schema_alignment": not alignment_errors,
        "fixture_matrix_passed": not fixture_failures,
        "update_plan_accepted": update_plan_is_accepted(root),
        "update_plan_bound": bundle["metadata"]["update_plan_ref"] == plan["metadata"]["update_plan_ref"],
        "source_distribution_bound": bundle["metadata"]["source_distribution_ref"] == manifest["metadata"]["distribution_ref"],
        "candidate_distribution_bound": bundle["metadata"]["candidate_distribution_ref"] == plan["metadata"]["candidate_distribution_ref"],
        "prior_project_lock_bound": bundle["metadata"]["prior_project_lock_digest"] == lock["status"]["project_lock_digest"],
        "candidate_project_lock_bound": bundle["metadata"]["candidate_project_lock_digest"] == plan["metadata"]["candidate_project_lock_digest"],
        "ownership_ledger_bound": bundle["metadata"]["prior_ownership_ledger_digest"] == ledger["status"]["ownership_ledger_digest"],
        "install_record_bound": install_source["metadata"]["install_record_ref"] in bundle["spec"]["prior_install_record_refs"],
        "rollback_apply_not_implemented": bundle["status"]["rollback_apply_implemented"] is False,
        "update_apply_not_implemented": bundle["status"]["update_apply_implemented"] is False,
        "install_apply_not_implemented": bundle["status"]["install_apply_implemented"] is False,
        "uninstall_apply_not_implemented": bundle["status"]["uninstall_apply_implemented"] is False,
        "target_repository_mutation_not_implemented": bundle["status"]["target_repository_mutation_implemented"] is False,
        "source_output_not_target_truth": bundle["spec"]["source_output_used_as_target_truth"] is False,
    }
    errors: list[dict[str, str]] = []
    if not validation["valid"]:
        errors.extend(validation["errors"])
    for error in alignment_errors:
        errors.append({"code": "rollback_bundle.schema_alignment", "message": error})
    for failure in fixture_failures:
        errors.append({"code": "rollback_bundle.fixture_failure", "message": failure["case_id"]})
    if not checks["update_plan_accepted"]:
        errors.append({"code": "rollback_bundle.update_plan_missing", "message": "UpdatePlan v1 acceptance report is missing or invalid"})
    validation_status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    report = {
        "schema_version": "aide.rollback-bundle-validation.v0",
        "status": validation_status,
        "validation_status": validation_status,
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": CHECK_TASK_ID,
        "checks": checks,
        "errors": errors,
        "schema_alignment_errors": alignment_errors,
        "rollback_bundle_validation": validation,
        "fixture_results": matrix["fixture_results"],
        "warnings": [
            "RollbackBundle v0 is proposed until independent check and acceptance.",
            "RollbackBundle records rollback preparation metadata only and performs no rollback apply.",
            "UpdateReceipt remains a future dependency after acceptance.",
        ],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
    }
    write_json(root / PROJECTION_JSON, bundle)
    write_json(root / VALIDATION_JSON, report)
    write_json(root / FIXTURE_MATRIX_JSON, matrix)
    write_text(root / VALIDATION_MD, render_validation_md(report))
    write_text(root / FIXTURE_MATRIX_MD, render_fixture_matrix_md(matrix["fixture_results"]))
    write_text(root / REVERSE_OPERATION_SUMMARY_MD, render_reverse_operation_summary_md(bundle))
    write_text(root / NO_APPLY_BOUNDARY_MD, render_no_apply_boundary_md())
    write_text(root / LIMITATIONS_MD, render_limitations_md(bundle))
    status(root)
    return report


def write_validation_reports(repo_root: str | Path = ".") -> None:
    validate(repo_root)


def cli_registered(repo_root: Path) -> bool:
    script = repo_root / ".aide/scripts/aide_lite.py"
    if not script.exists():
        return False
    text = script.read_text(encoding="utf-8")
    return "rollback-bundle" in text and "command_rollback_bundle_validate" in text


def render_status_md(data: dict[str, Any]) -> str:
    lines = [
        "# RollbackBundle v0 Status",
        "",
        f"- status: `{data.get('status')}`",
        f"- proposed_capability: `{data.get('proposed_capability')}`",
        f"- schema_exists: `{str(data.get('schema_exists', False)).lower()}`",
        f"- helper_exists: `{str(data.get('helper_exists', False)).lower()}`",
        f"- update_plan_acceptance_report_exists: `{str(data.get('update_plan_acceptance_report_exists', False)).lower()}`",
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
        "# RollbackBundle v0 Validation",
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
    lines = ["# RollbackBundle v0 Fixture Matrix", "", "| Case | Expected | Observed | Codes | Pass |", "| --- | --- | --- | --- | --- |"]
    for fixture in fixtures:
        codes = ", ".join(fixture.get("observed_refusal_codes", [])) or "none"
        lines.append(f"| {fixture['case_id']} | {fixture['expected_result']} | {fixture['observed_result']} | {codes} | {str(fixture['passed']).lower()} |")
    return "\n".join(lines) + "\n"


def render_reverse_operation_summary_md(bundle: dict[str, Any]) -> str:
    reverse_operations = bundle.get("spec", {}).get("reverse_operations", [])
    lines = [
        "# RollbackBundle v0 Reverse Operation Summary",
        "",
        f"- reverse_operation_count: {len(reverse_operations)}",
        "- reverse_operations_are_plans_not_actions: true",
        "",
    ]
    for operation in reverse_operations:
        lines.append(f"- `{operation.get('reverse_operation_ref')}` {operation.get('reverse_operation_class')} for `{operation.get('target_relative_path')}`")
    return "\n".join(lines) + "\n"


def render_no_apply_boundary_md() -> str:
    lines = [
        "# RollbackBundle v0 No-Apply Boundary",
        "",
        "RollbackBundle v0 prepares recovery metadata and preimage references only. It does not perform rollback, update, install, migration, repair, or uninstall apply.",
        "",
    ]
    for item in EXPLICIT_NON_CAPABILITIES:
        lines.append(f"- {item}: false")
    return "\n".join(lines) + "\n"


def render_limitations_md(bundle: dict[str, Any]) -> str:
    lines = [
        "# RollbackBundle v0 Limitations",
        "",
        f"- limitation_count: {len(bundle.get('spec', {}).get('limitations', []))}",
        "",
    ]
    for limitation in bundle.get("spec", {}).get("limitations", []):
        lines.append(f"- `{limitation.get('limitation_ref')}` {limitation.get('limitation_class')}")
    return "\n".join(lines) + "\n"
