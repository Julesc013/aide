"""UpdateReceipt v0 helpers.

UpdateReceipt records what a future accepted update execution observed. It is
not an updater, installer, migration applier, rollback applier, uninstaller,
target scanner, target mutator, release publisher, or authorization surface.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import distribution_manifest, envelope, install_record, ownership_ledger, project_lock, rollback_bundle, update_plan


API_VERSION = envelope.API_VERSION
KIND = "UpdateReceipt"
SCHEMA_VERSION = "aide.update-receipt.v0"
PROTOCOL_VERSION = "0.1.0"
TASK_ID = "AIDE-BUILD-UPDATE-RECEIPT-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-UPDATE-RECEIPT-V0-01"
PROPOSED_CAPABILITY = "update_receipt_v0"
DETERMINISTIC_TIMESTAMP = "fixture-timestamp:update-receipt-v0"
DEFAULT_EVIDENCE_REF = "aide://evidence/update-receipt-v0/source-projection"

REPORT_ROOT = Path(".aide/reports/update-receipt-v0")
SCHEMA_PATH = Path(".aide/protocol/aide-update-receipt-v0.schema.json")
FIXTURE_ROOT = Path(".aide/fixtures/update-receipt-v0")

PROJECTION_JSON = REPORT_ROOT / "projection.json"
PROJECT_REPORT_JSON = REPORT_ROOT / "project-report.json"
STATUS_MD = REPORT_ROOT / "status.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FIXTURE_MATRIX_JSON = REPORT_ROOT / "fixture-matrix.json"
FIXTURE_MATRIX_MD = REPORT_ROOT / "fixture-matrix.md"
OPERATION_SUMMARY_MD = REPORT_ROOT / "operation-summary.md"
SKIPPED_OPERATIONS_MD = REPORT_ROOT / "skipped-operations.md"
NO_APPLY_BOUNDARY_MD = REPORT_ROOT / "no-apply-boundary.md"
LIMITATIONS_MD = REPORT_ROOT / "limitations.md"

ROLLBACK_BUNDLE_ACCEPTANCE_JSON = Path(".aide/reports/rollback-bundle-v0-acceptance/validation-summary.json")

SUPPORTED_REQUIRED_FEATURES = {
    "update_receipt_v0",
    "distribution_manifest_v1",
    "project_lock_v0",
    "ownership_ledger_v1",
    "install_record_v0",
    "update_plan_v1",
    "rollback_bundle_v0",
    "sha256_digest_canonical_json_v1",
    "no_apply_update_receipt_v0",
}

SUPPORTED_OPTIONAL_FEATURES = {
    "validation_skipped_with_warning_v0",
    "manual_review_skipped_operation_v0",
    "mixed_operation_receipt_v0",
}

SUPPORTED_OPERATION_RECEIPT_CLASSES = {
    "managed_file_added",
    "managed_file_updated",
    "managed_file_removed",
    "managed_section_added",
    "managed_section_updated",
    "managed_section_removed",
    "project_owned_preserved",
    "project_overlay_preserved",
    "local_only_preserved",
    "runtime_generated_preserved",
    "evidence_only_preserved",
    "legacy_preserved",
    "never_touch_preserved",
    "migration_recorded",
    "lock_updated",
    "ownership_ledger_updated",
    "install_record_updated",
    "validation_run",
    "validation_skipped",
    "manual_review_recorded",
    "operation_refused",
    "operation_failed",
    "rollback_bundle_referenced",
}

SUPPORTED_SKIPPED_REASONS = {
    "manual_review_required",
    "preimage_mismatch",
    "postimage_mismatch",
    "unknown_ownership",
    "never_touch",
    "project_owned",
    "project_overlay",
    "local_only",
    "runtime_generated",
    "evidence_only",
    "symlink_or_reparse_uncertainty",
    "case_collision",
    "missing_rollback_requirement",
    "missing_approval",
    "validation_failed",
    "policy_refusal",
    "unsupported_operation",
    "unknown_required_feature",
}

CHANGED_RECEIPT_CLASSES = {
    "managed_file_added",
    "managed_file_updated",
    "managed_file_removed",
    "managed_section_added",
    "managed_section_updated",
    "managed_section_removed",
}

REFUSAL_CODES = [
    "update_receipt.missing",
    "update_receipt.invalid",
    "update_receipt.update_plan_missing",
    "update_receipt.rollback_bundle_missing",
    "update_receipt.old_project_lock_missing",
    "update_receipt.new_project_lock_missing",
    "update_receipt.target_project_missing",
    "update_receipt.operation_not_in_plan",
    "update_receipt.unplanned_operation_claimed",
    "update_receipt.project_owned_changed",
    "update_receipt.project_overlay_changed",
    "update_receipt.local_only_changed",
    "update_receipt.never_touch_changed",
    "update_receipt.unknown_ownership_changed",
    "update_receipt.preimage_digest_mismatch",
    "update_receipt.postimage_digest_mismatch",
    "update_receipt.changed_artifact_missing",
    "update_receipt.validation_result_missing",
    "update_receipt.approval_ref_missing",
    "update_receipt.rollback_bundle_ref_missing",
    "update_receipt.authorization_claimed",
    "update_receipt.apply_authority_claimed",
    "update_receipt.target_mutation_claimed",
    "update_receipt.release_readiness_claimed",
    "update_receipt.absolute_path_forbidden",
    "update_receipt.path_traversal_forbidden",
    "update_receipt.source_state_contamination",
    "update_receipt.source_output_as_target_truth",
    "update_receipt.unknown_required_feature",
    "update_receipt.extension_required_unknown",
    "update_receipt.digest_mismatch",
    "update_receipt.fixture_failure",
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
    "distribution_apply_engine",
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
    return rollback_bundle.load_distribution_manifest(repo_root)


def load_project_lock(repo_root: str | Path = ".") -> dict[str, Any]:
    return rollback_bundle.load_project_lock(repo_root)


def load_ownership_ledger(repo_root: str | Path = ".") -> dict[str, Any]:
    return rollback_bundle.load_ownership_ledger(repo_root)


def load_install_record_source(repo_root: str | Path = ".") -> dict[str, Any]:
    return rollback_bundle.load_install_record_source(repo_root)


def load_update_plan_source(repo_root: str | Path = ".") -> dict[str, Any]:
    return rollback_bundle.load_update_plan_source(repo_root)


def load_rollback_bundle_source(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    path = root / rollback_bundle.PROJECTION_JSON
    if path.exists():
        return load_json(path)
    return rollback_bundle.build_rollback_bundle(root)


def rollback_bundle_is_accepted(repo_root: str | Path = ".") -> bool:
    path = Path(repo_root) / ROLLBACK_BUNDLE_ACCEPTANCE_JSON
    if not path.exists():
        return False
    try:
        report = load_json(path)
    except Exception:
        return False
    return (
        report.get("result") in {"ACCEPTED", "ACCEPTED_WITH_WARNINGS"}
        and report.get("accepted_capability") == "rollback_bundle_v0"
        and int(report.get("material_finding_count", 1)) == 0
        and int(report.get("missing_evidence", 1)) == 0
    )


def object_digest(record: dict[str, Any], status_key: str, digest_func: Any) -> str:
    digest = record.get("status", {}).get(status_key)
    if isinstance(digest, str) and digest:
        return digest
    return digest_func(record)


def update_receipt_digest(record: dict[str, Any]) -> str:
    payload = copy.deepcopy(record)
    status = payload.get("status")
    if isinstance(status, dict):
        status.pop("update_receipt_digest", None)
    return sha256_digest(canonical_json_bytes(payload))


def finalize_update_receipt(record: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(record)
    result.setdefault("status", {})["update_receipt_digest"] = update_receipt_digest(result)
    return result


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower() or "unknown"


def _operation_sort_key(operation: dict[str, Any]) -> str:
    return str(operation.get("target_relative_path", "")) + "\0" + str(operation.get("operation_ref", ""))


def _receipt_class_for(operation_class: str, ownership_class: str) -> str:
    mapping = {
        "add_managed_file": "managed_file_added",
        "update_managed_file": "managed_file_updated",
        "remove_managed_file": "managed_file_removed",
        "add_managed_section": "managed_section_added",
        "update_managed_section": "managed_section_updated",
        "remove_managed_section": "managed_section_removed",
        "preserve_project_owned": "project_owned_preserved",
        "preserve_project_overlay": "project_overlay_preserved",
        "preserve_local_only": "local_only_preserved",
        "preserve_runtime_generated": "runtime_generated_preserved",
        "preserve_evidence_only": "evidence_only_preserved",
        "preserve_legacy": "legacy_preserved",
        "regenerate_project_output": "validation_skipped",
        "manual_review_required": "manual_review_recorded",
        "refuse": "operation_refused",
    }
    if ownership_class == "never_touch":
        return "never_touch_preserved"
    if ownership_class == "unknown":
        return "operation_refused"
    return mapping.get(operation_class, "manual_review_recorded")


def _skip_reason_for(operation: dict[str, Any], receipt_class: str) -> str | None:
    ownership_class = str(operation.get("ownership_class", ""))
    operation_class = str(operation.get("operation_class", ""))
    if receipt_class in CHANGED_RECEIPT_CLASSES:
        return None
    if ownership_class == "unknown":
        return "unknown_ownership"
    if ownership_class == "never_touch":
        return "never_touch"
    if ownership_class == "project_owned":
        return "project_owned"
    if ownership_class == "project_overlay":
        return "project_overlay"
    if ownership_class == "local_only":
        return "local_only"
    if ownership_class == "runtime_generated":
        return "runtime_generated"
    if ownership_class == "evidence_only":
        return "evidence_only"
    if operation_class == "manual_review_required":
        return "manual_review_required"
    if operation_class == "refuse":
        return "policy_refusal"
    return None


def _operation_receipt(operation: dict[str, Any]) -> dict[str, Any]:
    operation_ref = str(operation.get("operation_ref", "aide://update-plan/operation/unknown"))
    operation_class = str(operation.get("operation_class", ""))
    ownership_class = str(operation.get("ownership_class", ""))
    receipt_class = _receipt_class_for(operation_class, ownership_class)
    suffix = _slug(operation_ref.split("/")[-1])
    artifact_ref = f"aide://update-receipt/artifact/{suffix}" if receipt_class in CHANGED_RECEIPT_CLASSES else None
    validation_ref = f"aide://update-receipt/validation/{suffix}" if receipt_class != "validation_skipped" else None
    return {
        "operation_receipt_ref": f"aide://update-receipt/operation-receipt/{suffix}",
        "operation_ref": operation_ref,
        "operation_receipt_class": receipt_class,
        "operation_class": operation_class,
        "target_relative_path": operation.get("target_relative_path"),
        "ownership_entry_ref": operation.get("ownership_entry_ref"),
        "ownership_class": ownership_class,
        "preimage_digest": operation.get("preimage_digest", ""),
        "postimage_digest": operation.get("postimage_digest", ""),
        "changed_artifact_ref": artifact_ref,
        "validation_result_ref": validation_ref,
        "approval_ref": "aide://approval/update-receipt-v0/fixture-review" if receipt_class in CHANGED_RECEIPT_CLASSES else None,
        "update_apply_implemented": False,
        "target_repository_mutation_performed": False,
        "authorization_claimed": False,
        "source_output_used_as_target_truth": False,
        "evidence_refs": list(operation.get("evidence_refs", [DEFAULT_EVIDENCE_REF])),
        "extensions": {},
    }


def _metadata_receipt(receipt_class: str, source_ref: str, digest: str) -> dict[str, Any]:
    suffix = _slug(receipt_class)
    return {
        "operation_receipt_ref": f"aide://update-receipt/operation-receipt/{suffix}",
        "operation_ref": f"aide://update-receipt/metadata/{suffix}",
        "operation_receipt_class": receipt_class,
        "operation_class": "metadata_recorded",
        "target_relative_path": None,
        "ownership_entry_ref": None,
        "ownership_class": "metadata_only",
        "preimage_digest": digest,
        "postimage_digest": digest,
        "changed_artifact_ref": f"aide://update-receipt/artifact/{suffix}",
        "validation_result_ref": f"aide://update-receipt/validation/{suffix}",
        "approval_ref": "aide://approval/update-receipt-v0/fixture-review",
        "source_ref": source_ref,
        "update_apply_implemented": False,
        "target_repository_mutation_performed": False,
        "authorization_claimed": False,
        "source_output_used_as_target_truth": False,
        "evidence_refs": [DEFAULT_EVIDENCE_REF],
        "extensions": {},
    }


def _validation_result_record(ref: str, result: str = "PASS_WITH_WARNINGS", warning: str | None = None) -> dict[str, Any]:
    record = {
        "validation_result_ref": ref,
        "result": result,
        "update_apply_implemented": False,
        "target_repository_mutation_performed": False,
        "evidence_refs": [DEFAULT_EVIDENCE_REF],
        "extensions": {},
    }
    if warning:
        record["warning"] = warning
    return record


def build_update_receipt(
    repo_root: str | Path = ".",
    *,
    plan: dict[str, Any] | None = None,
    bundle: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
    lock: dict[str, Any] | None = None,
    ledger: dict[str, Any] | None = None,
    install_source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    root = Path(repo_root)
    update_source = plan if plan is not None else load_update_plan_source(root)
    rollback_source = bundle if bundle is not None else load_rollback_bundle_source(root)
    distribution = manifest if manifest is not None else load_distribution_manifest(root)
    project_lock_data = lock if lock is not None else load_project_lock(root)
    ownership = ledger if ledger is not None else load_ownership_ledger(root)
    install_source = install_source if install_source is not None else load_install_record_source(root)

    operations = sorted(update_source.get("spec", {}).get("planned_operations", []), key=_operation_sort_key)
    operation_receipts = [_operation_receipt(operation) for operation in operations]

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
    rollback_ref = rollback_source.get("metadata", {}).get("rollback_bundle_ref")
    rollback_digest = object_digest(rollback_source, "rollback_bundle_digest", rollback_bundle.rollback_bundle_digest)

    operation_receipts.extend(
        [
            _metadata_receipt("migration_recorded", "aide://migration-record/install-record-v0/no-op-compatibility", update_source.get("spec", {}).get("migration_record_digests", ["sha256:" + "0" * 64])[0]),
            _metadata_receipt("lock_updated", str(candidate_lock_ref), str(candidate_lock_digest)),
            _metadata_receipt("ownership_ledger_updated", str(ledger_ref), str(ledger_digest)),
            _metadata_receipt("install_record_updated", str(install_ref), str(install_digest)),
            _metadata_receipt("validation_run", "aide://validation/update-receipt-v0/project", str(rollback_digest)),
            _metadata_receipt("rollback_bundle_referenced", str(rollback_ref), str(rollback_digest)),
        ]
    )

    skipped_operations = []
    for receipt in operation_receipts:
        reason = None
        if receipt["operation_ref"].startswith("aide://update-plan/operation/"):
            source_operation = next((item for item in operations if item.get("operation_ref") == receipt["operation_ref"]), {})
            reason = _skip_reason_for(source_operation, receipt["operation_receipt_class"])
        if reason:
            skipped_operations.append(
                {
                    "skipped_operation_ref": f"aide://update-receipt/skipped/{_slug(receipt['operation_ref'].split('/')[-1])}",
                    "operation_ref": receipt["operation_ref"],
                    "reason": reason,
                    "disposition": "recorded_no_apply",
                    "evidence_refs": receipt.get("evidence_refs", [DEFAULT_EVIDENCE_REF]),
                    "extensions": {},
                }
            )

    changed_file_refs = [
        {
            "changed_file_ref": receipt["changed_artifact_ref"],
            "operation_ref": receipt["operation_ref"],
            "target_relative_path": receipt.get("target_relative_path"),
            "artifact_ref": receipt["changed_artifact_ref"],
            "preimage_digest": receipt.get("preimage_digest", ""),
            "postimage_digest": receipt.get("postimage_digest", ""),
            "evidence_refs": receipt.get("evidence_refs", [DEFAULT_EVIDENCE_REF]),
            "extensions": {},
        }
        for receipt in operation_receipts
        if receipt["operation_receipt_class"] in {"managed_file_added", "managed_file_updated", "managed_file_removed"}
    ]
    changed_section_refs = [
        {
            "changed_section_ref": receipt["changed_artifact_ref"],
            "operation_ref": receipt["operation_ref"],
            "target_relative_path": receipt.get("target_relative_path"),
            "artifact_ref": receipt["changed_artifact_ref"],
            "preimage_digest": receipt.get("preimage_digest", ""),
            "postimage_digest": receipt.get("postimage_digest", ""),
            "evidence_refs": receipt.get("evidence_refs", [DEFAULT_EVIDENCE_REF]),
            "extensions": {},
        }
        for receipt in operation_receipts
        if receipt["operation_receipt_class"] in {"managed_section_added", "managed_section_updated", "managed_section_removed"}
    ]
    validation_results = [
        _validation_result_record("aide://update-receipt/validation/update-plan-binding"),
        _validation_result_record("aide://update-receipt/validation/rollback-bundle-binding"),
        _validation_result_record("aide://update-receipt/validation/no-apply-boundary"),
    ]
    validation_refs = {item["validation_result_ref"] for item in validation_results}
    validation_results.extend(
        _validation_result_record(str(receipt["validation_result_ref"]))
        for receipt in operation_receipts
        if receipt.get("validation_result_ref") and receipt["validation_result_ref"] not in validation_refs
    )
    preimage_digests = {
        receipt["operation_ref"]: receipt.get("preimage_digest", "")
        for receipt in operation_receipts
        if receipt.get("preimage_digest")
    }
    postimage_digests = {
        receipt["operation_ref"]: receipt.get("postimage_digest", "")
        for receipt in operation_receipts
        if receipt.get("postimage_digest")
    }
    artifact_refs = sorted(
        str(ref)
        for ref in {
            *(item.get("artifact_ref") for item in changed_file_refs),
            *(item.get("artifact_ref") for item in changed_section_refs),
            *(receipt.get("changed_artifact_ref") for receipt in operation_receipts),
            rollback_ref,
        }
        if ref
    )
    limitations = [
        {
            "limitation_ref": "aide://update-receipt/limitation/no-apply-authority",
            "limitation_class": "no_apply_authority",
            "disposition": "future apply engines must be separately accepted before receipts can be produced from real execution",
            "evidence_refs": [DEFAULT_EVIDENCE_REF],
            "extensions": {},
        }
    ]
    if skipped_operations:
        limitations.append(
            {
                "limitation_ref": "aide://update-receipt/limitation/skipped-operations",
                "limitation_class": "skipped_operations_recorded",
                "disposition": "skipped operations are receipt facts only and do not authorize retries",
                "evidence_refs": [DEFAULT_EVIDENCE_REF],
                "extensions": {},
            }
        )
    record = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "update_receipt_ref": "aide://update-receipt/aide-self-no-apply-update-receipt-v0",
            "update_plan_ref": update_source.get("metadata", {}).get("update_plan_ref"),
            "update_plan_digest": object_digest(update_source, "update_plan_digest", update_plan.update_plan_digest),
            "rollback_bundle_ref": rollback_ref,
            "rollback_bundle_digest": rollback_digest,
            "target_project_ref": update_source.get("metadata", {}).get("target_project_ref"),
            "target_project_identity": update_source.get("metadata", {}).get("target_project_identity"),
            "old_project_lock_ref": current_lock_ref,
            "old_project_lock_digest": current_lock_digest,
            "new_project_lock_ref": candidate_lock_ref,
            "new_project_lock_digest": candidate_lock_digest,
            "prior_ownership_ledger_ref": ledger_ref,
            "prior_ownership_ledger_digest": ledger_digest,
            "new_ownership_ledger_ref": ledger_ref,
            "new_ownership_ledger_digest": ledger_digest,
            "source_distribution_ref": source_distribution_ref,
            "source_distribution_digest": distribution_digest,
            "candidate_distribution_ref": update_source.get("metadata", {}).get("candidate_distribution_ref"),
            "candidate_distribution_digest": update_source.get("metadata", {}).get("candidate_distribution_digest"),
            "created_at": DETERMINISTIC_TIMESTAMP,
            "created_by": "aide-self-hosting-fixture",
            "prior_update_receipt_ref": None,
            "superseded_by_ref": None,
            "extensions": {},
        },
        "spec": {
            "prior_install_record_refs": [install_ref],
            "prior_install_record_digests": [install_digest],
            "new_install_record_ref": "aide://install-record/aide-self-update-receipt-v0/no-apply-recorded",
            "operation_receipts": operation_receipts,
            "skipped_operations": skipped_operations,
            "failed_operations": [],
            "changed_file_refs": changed_file_refs,
            "changed_section_refs": changed_section_refs,
            "preimage_digests": preimage_digests,
            "postimage_digests": postimage_digests,
            "artifact_refs": artifact_refs,
            "validation_results": validation_results,
            "approval_ref": "aide://approval/update-receipt-v0/fixture-review",
            "executor_ref": "aide://executor/aide-fixture-no-apply",
            "execution_environment": {
                "execution_mode": "no_apply_fixture_receipt",
                "fixture_only": True,
                "network_calls_performed": False,
                "provider_model_calls_performed": False,
                "target_repository_mutation_performed": False,
                "extensions": {},
            },
            "warnings": [
                "UpdateReceipt v0 is proposed until independent check and acceptance.",
                "Receipt records no-apply fixture execution metadata only.",
            ],
            "limitations": limitations,
            "risk_class": "medium" if skipped_operations else "low",
            "evidence_refs": [DEFAULT_EVIDENCE_REF],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "required_features": [
                "update_receipt_v0",
                "distribution_manifest_v1",
                "project_lock_v0",
                "ownership_ledger_v1",
                "install_record_v0",
                "update_plan_v1",
                "rollback_bundle_v0",
                "sha256_digest_canonical_json_v1",
                "no_apply_update_receipt_v0",
            ],
            "optional_features": ["validation_skipped_with_warning_v0", "manual_review_skipped_operation_v0"],
            "source_output_used_as_target_truth": False,
            "target_repository_mutation_performed": False,
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "validation_result": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "recommended_next_task": CHECK_TASK_ID,
            "update_receipt_digest": "",
            "receipt_authorization_claimed": False,
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "migration_apply_implemented": False,
            "repair_apply_implemented": False,
            "rollback_apply_implemented": False,
            "uninstall_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "target_scan_authority_implemented": False,
            "release_publication_implemented": False,
            "release_readiness_claimed": False,
            "network_calls_implemented": False,
            "provider_model_calls_implemented": False,
            "distribution_apply_engine_started": False,
            "workbench_runtime_implemented": False,
            "commander_implemented": False,
            "omnigent_implemented": False,
            "branch_worktree_automation_implemented": False,
            "extensions": {},
        },
        "extensions": {},
    }
    return finalize_update_receipt(record)


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
    if not value or value.startswith("aide://") or value.startswith("fixture-timestamp:") or value.startswith("sha256:"):
        return None
    normalized = value.replace("\\", "/")
    if SOURCE_OUTPUT_RE.search(normalized):
        return "update_receipt.source_state_contamination"
    if PATH_RE.search(normalized):
        if ".." in [part for part in normalized.split("/") if part]:
            return "update_receipt.path_traversal_forbidden"
        return "update_receipt.absolute_path_forbidden"
    return None


def _boolean_claims_authority(data: Any, errors: list[dict[str, str]]) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            key_text = str(key)
            if value is True and ("authorization" in key_text or "authorize" in key_text):
                _add_error(errors, "update_receipt.authorization_claimed", f"authorization claimed by {key_text}")
            elif value is True and ("apply" in key_text or "install_authority" in key_text or "update_authority" in key_text or "rollback_authority" in key_text or "uninstall_authority" in key_text):
                _add_error(errors, "update_receipt.apply_authority_claimed", f"apply authority claimed by {key_text}")
            if value is True and ("mutation" in key_text or "mutate" in key_text):
                _add_error(errors, "update_receipt.target_mutation_claimed", f"target mutation claimed by {key_text}")
            if value is True and ("release_readiness" in key_text or "release_publication" in key_text):
                _add_error(errors, "update_receipt.release_readiness_claimed", f"release readiness claimed by {key_text}")
            _boolean_claims_authority(value, errors)
    elif isinstance(data, list):
        for item in data:
            _boolean_claims_authority(item, errors)


def _update_operation_index(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    operations = plan.get("spec", {}).get("planned_operations", [])
    return {str(item.get("operation_ref")): item for item in operations if isinstance(item, dict) and item.get("operation_ref")}


def _rollback_operation_refs(bundle: dict[str, Any]) -> set[str]:
    spec = bundle.get("spec", {}) if isinstance(bundle.get("spec"), dict) else {}
    result = {str(item.get("source_operation_ref")) for item in spec.get("reverse_operations", []) if isinstance(item, dict) and item.get("source_operation_ref")}
    result.update(str(item.get("source_operation_ref")) for item in spec.get("operation_rollback_map", []) if isinstance(item, dict) and item.get("source_operation_ref"))
    return result


def _validation_refs(receipt: dict[str, Any]) -> set[str]:
    spec = receipt.get("spec", {}) if isinstance(receipt.get("spec"), dict) else {}
    return {str(item.get("validation_result_ref")) for item in spec.get("validation_results", []) if isinstance(item, dict) and item.get("validation_result_ref")}


def _artifact_refs(receipt: dict[str, Any]) -> set[str]:
    spec = receipt.get("spec", {}) if isinstance(receipt.get("spec"), dict) else {}
    return {str(item) for item in spec.get("artifact_refs", []) if isinstance(item, str)}


def _validate_operation_receipts(receipt: dict[str, Any], plan: dict[str, Any], bundle: dict[str, Any], errors: list[dict[str, str]]) -> None:
    spec = receipt.get("spec", {}) if isinstance(receipt.get("spec"), dict) else {}
    plan_operations = _update_operation_index(plan)
    rollback_operations = _rollback_operation_refs(bundle)
    validation_refs = _validation_refs(receipt)
    artifact_refs = _artifact_refs(receipt)
    for operation in spec.get("operation_receipts", []) if isinstance(spec.get("operation_receipts"), list) else []:
        if not isinstance(operation, dict):
            _add_error(errors, "update_receipt.invalid", "operation receipt must be an object")
            continue
        receipt_class = str(operation.get("operation_receipt_class", ""))
        operation_ref = str(operation.get("operation_ref", ""))
        ownership_class = str(operation.get("ownership_class", ""))
        target_path = operation.get("target_relative_path")
        if receipt_class not in SUPPORTED_OPERATION_RECEIPT_CLASSES:
            _add_error(errors, "update_receipt.invalid", f"unsupported operation receipt class: {receipt_class}")
        is_metadata = operation_ref.startswith("aide://update-receipt/metadata/")
        source_operation = plan_operations.get(operation_ref)
        if not source_operation and not is_metadata:
            _add_error(errors, "update_receipt.operation_not_in_plan", f"receipt references operation not in UpdatePlan: {operation_ref}")
        if source_operation and operation_ref not in rollback_operations:
            _add_error(errors, "update_receipt.rollback_bundle_ref_missing", f"receipt operation lacks RollbackBundle preparation: {operation_ref}")
        if operation.get("source_output_used_as_target_truth") is True:
            _add_error(errors, "update_receipt.source_output_as_target_truth", "source output cannot become target truth")
        if operation.get("target_repository_mutation_performed") is True:
            _add_error(errors, "update_receipt.target_mutation_claimed", "operation receipt claims target mutation")
        if operation.get("authorization_claimed") is True:
            _add_error(errors, "update_receipt.authorization_claimed", "operation receipt claims authorization")
        if receipt_class in CHANGED_RECEIPT_CLASSES:
            changed_artifact_ref = str(operation.get("changed_artifact_ref") or "")
            if not changed_artifact_ref or changed_artifact_ref not in artifact_refs:
                _add_error(errors, "update_receipt.changed_artifact_missing", "changed artifact ref is missing or undeclared")
            if not operation.get("validation_result_ref") or str(operation.get("validation_result_ref")) not in validation_refs:
                _add_error(errors, "update_receipt.validation_result_missing", "changed operation receipt lacks validation result")
            if not operation.get("approval_ref"):
                _add_error(errors, "update_receipt.approval_ref_missing", "changed operation receipt lacks approval ref")
            if ownership_class == "project_owned":
                _add_error(errors, "update_receipt.project_owned_changed", "project_owned content cannot be changed by receipt")
            if ownership_class == "project_overlay":
                _add_error(errors, "update_receipt.project_overlay_changed", "project_overlay content cannot be changed by receipt")
            if ownership_class == "local_only":
                _add_error(errors, "update_receipt.local_only_changed", "local_only content cannot be changed by receipt")
            if ownership_class == "never_touch":
                _add_error(errors, "update_receipt.never_touch_changed", "never_touch content cannot be changed by receipt")
            if ownership_class == "unknown":
                _add_error(errors, "update_receipt.unknown_ownership_changed", "unknown ownership content cannot be changed by receipt")
        if source_operation:
            if operation.get("preimage_digest") != source_operation.get("preimage_digest"):
                _add_error(errors, "update_receipt.preimage_digest_mismatch", "operation receipt preimage digest does not match UpdatePlan")
            if operation.get("postimage_digest") != source_operation.get("postimage_digest"):
                _add_error(errors, "update_receipt.postimage_digest_mismatch", "operation receipt postimage digest does not match UpdatePlan")
        if isinstance(target_path, str):
            path_code = _path_error(target_path)
            if path_code:
                _add_error(errors, path_code, f"unsafe target path: {target_path}")


def _validate_changed_refs(receipt: dict[str, Any], plan: dict[str, Any], errors: list[dict[str, str]]) -> None:
    spec = receipt.get("spec", {}) if isinstance(receipt.get("spec"), dict) else {}
    plan_operations = _update_operation_index(plan)
    for collection_name in ["changed_file_refs", "changed_section_refs"]:
        for item in spec.get(collection_name, []) if isinstance(spec.get(collection_name), list) else []:
            if not isinstance(item, dict):
                _add_error(errors, "update_receipt.invalid", f"{collection_name} item must be an object")
                continue
            operation_ref = str(item.get("operation_ref", ""))
            if operation_ref not in plan_operations:
                _add_error(errors, "update_receipt.unplanned_operation_claimed", f"changed artifact references unplanned operation: {operation_ref}")
            if not item.get("artifact_ref"):
                _add_error(errors, "update_receipt.changed_artifact_missing", "changed artifact ref is required")
            target_path = item.get("target_relative_path")
            if isinstance(target_path, str):
                path_code = _path_error(target_path)
                if path_code:
                    _add_error(errors, path_code, f"unsafe changed artifact path: {target_path}")


def validate_update_receipt_object(
    receipt: dict[str, Any] | None,
    *,
    plan: dict[str, Any] | None = None,
    bundle: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
    lock: dict[str, Any] | None = None,
    ledger: dict[str, Any] | None = None,
    install_source: dict[str, Any] | None = None,
    repo_root: str | Path | None = None,
    require_rollback_bundle_acceptance: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[str] = []
    if receipt is None:
        _add_error(errors, "update_receipt.missing", "UpdateReceipt is missing")
        return _validation_result(errors, warnings)
    if not isinstance(receipt, dict):
        _add_error(errors, "update_receipt.invalid", "UpdateReceipt root must be an object")
        return _validation_result(errors, warnings)
    for field in ["apiVersion", "kind", "schema_version", "metadata", "spec", "status", "extensions"]:
        if field not in receipt:
            _add_error(errors, "update_receipt.invalid", f"missing required field: {field}")
    if receipt.get("kind") != KIND:
        _add_error(errors, "update_receipt.invalid", "kind must be UpdateReceipt")
    if receipt.get("schema_version") != SCHEMA_VERSION:
        _add_error(errors, "update_receipt.invalid", f"schema_version must be {SCHEMA_VERSION}")

    root = Path(repo_root or ".")
    update_source = plan if plan is not None else load_update_plan_source(root)
    rollback_source = bundle if bundle is not None else load_rollback_bundle_source(root)
    distribution = manifest if manifest is not None else load_distribution_manifest(root)
    project_lock_data = lock if lock is not None else load_project_lock(root)
    ownership = ledger if ledger is not None else load_ownership_ledger(root)
    install_source = install_source if install_source is not None else load_install_record_source(root)
    metadata = receipt.get("metadata") if isinstance(receipt.get("metadata"), dict) else {}
    spec = receipt.get("spec") if isinstance(receipt.get("spec"), dict) else {}
    status_data = receipt.get("status") if isinstance(receipt.get("status"), dict) else {}

    if not metadata.get("update_plan_ref"):
        _add_error(errors, "update_receipt.update_plan_missing", "update_plan_ref is required")
    if not metadata.get("rollback_bundle_ref"):
        _add_error(errors, "update_receipt.rollback_bundle_missing", "rollback_bundle_ref is required")
    if not metadata.get("old_project_lock_ref"):
        _add_error(errors, "update_receipt.old_project_lock_missing", "old_project_lock_ref is required")
    if not metadata.get("new_project_lock_ref"):
        _add_error(errors, "update_receipt.new_project_lock_missing", "new_project_lock_ref is required")
    if not metadata.get("target_project_ref"):
        _add_error(errors, "update_receipt.target_project_missing", "target_project_ref is required")
    if not spec.get("evidence_refs"):
        _add_error(errors, "update_receipt.validation_result_missing", "receipt evidence_refs are required")
    if not spec.get("operation_receipts"):
        _add_error(errors, "update_receipt.operation_not_in_plan", "operation_receipts are required")
    if not spec.get("validation_results"):
        _add_error(errors, "update_receipt.validation_result_missing", "validation_results are required")
    if not spec.get("approval_ref"):
        _add_error(errors, "update_receipt.approval_ref_missing", "approval_ref is required for receipt review")

    expected_plan_ref = update_source.get("metadata", {}).get("update_plan_ref")
    expected_plan_digest = object_digest(update_source, "update_plan_digest", update_plan.update_plan_digest)
    if metadata.get("update_plan_ref") != expected_plan_ref or metadata.get("update_plan_digest") != expected_plan_digest:
        _add_error(errors, "update_receipt.update_plan_missing", "accepted UpdatePlan ref or digest is not cited")
    expected_bundle_ref = rollback_source.get("metadata", {}).get("rollback_bundle_ref")
    expected_bundle_digest = object_digest(rollback_source, "rollback_bundle_digest", rollback_bundle.rollback_bundle_digest)
    if metadata.get("rollback_bundle_ref") != expected_bundle_ref or metadata.get("rollback_bundle_digest") != expected_bundle_digest:
        _add_error(errors, "update_receipt.rollback_bundle_missing", "accepted RollbackBundle ref or digest is not cited")
    expected_distribution_ref = distribution.get("metadata", {}).get("distribution_ref")
    expected_distribution_digest = object_digest(distribution, "distribution_digest", distribution_manifest.distribution_digest)
    if metadata.get("source_distribution_ref") != expected_distribution_ref or metadata.get("source_distribution_digest") != expected_distribution_digest:
        _add_error(errors, "update_receipt.invalid", "source distribution does not match DistributionManifest")
    if metadata.get("candidate_distribution_ref") != update_source.get("metadata", {}).get("candidate_distribution_ref") or metadata.get("candidate_distribution_digest") != update_source.get("metadata", {}).get("candidate_distribution_digest"):
        _add_error(errors, "update_receipt.invalid", "candidate distribution does not match UpdatePlan")
    expected_lock_ref = project_lock_data.get("metadata", {}).get("project_lock_ref")
    expected_lock_digest = object_digest(project_lock_data, "project_lock_digest", project_lock.project_lock_digest)
    if metadata.get("old_project_lock_ref") != expected_lock_ref or metadata.get("old_project_lock_digest") != expected_lock_digest:
        _add_error(errors, "update_receipt.old_project_lock_missing", "old ProjectLock ref or digest does not match")
    if metadata.get("new_project_lock_ref") != update_source.get("metadata", {}).get("candidate_project_lock_ref") or metadata.get("new_project_lock_digest") != update_source.get("metadata", {}).get("candidate_project_lock_digest"):
        _add_error(errors, "update_receipt.new_project_lock_missing", "new ProjectLock ref or digest does not match UpdatePlan")
    expected_ledger_ref = ownership.get("metadata", {}).get("ledger_ref")
    expected_ledger_digest = object_digest(ownership, "ownership_ledger_digest", ownership_ledger.ownership_ledger_digest)
    if metadata.get("prior_ownership_ledger_ref") != expected_ledger_ref or metadata.get("prior_ownership_ledger_digest") != expected_ledger_digest:
        _add_error(errors, "update_receipt.invalid", "prior OwnershipLedger ref or digest does not match")
    if metadata.get("new_ownership_ledger_ref") != expected_ledger_ref or metadata.get("new_ownership_ledger_digest") != expected_ledger_digest:
        _add_error(errors, "update_receipt.invalid", "new OwnershipLedger ref or digest does not match")
    expected_install_ref = install_source.get("metadata", {}).get("install_record_ref")
    expected_install_digest = object_digest(install_source, "install_record_digest", install_record.install_record_digest)
    if expected_install_ref not in (spec.get("prior_install_record_refs") or []) or expected_install_digest not in (spec.get("prior_install_record_digests") or []):
        _add_error(errors, "update_receipt.invalid", "InstallRecord ref or digest is not cited")
    if not spec.get("new_install_record_ref"):
        _add_error(errors, "update_receipt.invalid", "new_install_record_ref is required")
    if require_rollback_bundle_acceptance and (repo_root is None or not rollback_bundle_is_accepted(root)):
        _add_error(errors, "update_receipt.rollback_bundle_missing", "RollbackBundle v0 is not accepted")

    for feature in spec.get("required_features", []) if isinstance(spec.get("required_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES:
            _add_error(errors, "update_receipt.unknown_required_feature", f"unknown required feature: {feature}")
    for feature in spec.get("optional_features", []) if isinstance(spec.get("optional_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES and feature not in SUPPORTED_OPTIONAL_FEATURES:
            warnings.append(f"unknown optional feature tolerated: {feature}")
    if _extension_requires_unknown(receipt.get("extensions", {})) or _extension_requires_unknown(spec.get("extensions", {})):
        _add_error(errors, "update_receipt.extension_required_unknown", "unknown required extension present")
    if spec.get("source_output_used_as_target_truth") is True:
        _add_error(errors, "update_receipt.source_output_as_target_truth", "source output cannot become target truth")
    if spec.get("target_repository_mutation_performed") is True:
        _add_error(errors, "update_receipt.target_mutation_claimed", "target mutation claimed by receipt")
    for item in spec.get("skipped_operations", []) if isinstance(spec.get("skipped_operations"), list) else []:
        if isinstance(item, dict) and item.get("reason") not in SUPPORTED_SKIPPED_REASONS:
            _add_error(errors, "update_receipt.invalid", f"unsupported skipped reason: {item.get('reason')}")
    for value in _iter_string_values(spec):
        path_code = _path_error(value)
        if path_code:
            _add_error(errors, path_code, f"unsafe source or target string: {value}")
    _validate_operation_receipts(receipt, update_source, rollback_source, errors)
    _validate_changed_refs(receipt, update_source, errors)
    _boolean_claims_authority(spec, errors)
    _boolean_claims_authority(status_data, errors)
    expected_digest = update_receipt_digest(receipt)
    if status_data.get("update_receipt_digest") and status_data.get("update_receipt_digest") != expected_digest:
        _add_error(errors, "update_receipt.digest_mismatch", "update_receipt_digest does not match canonical payload")
    return _validation_result(errors, warnings)


def minimal_fixture_record() -> dict[str, Any]:
    manifest = distribution_manifest.minimal_fixture_manifest()
    lock = project_lock.minimal_fixture_lock()
    ledger = ownership_ledger.minimal_fixture_ledger()
    install_source = install_record.minimal_fixture_record()
    plan = update_plan.minimal_fixture_record()
    bundle = rollback_bundle.minimal_fixture_record()
    return build_update_receipt(
        manifest=manifest,
        lock=lock,
        ledger=ledger,
        install_source=install_source,
        plan=plan,
        bundle=bundle,
    )


def mutate(base: dict[str, Any], mutator: Any) -> dict[str, Any]:
    record = copy.deepcopy(base)
    mutator(record)
    return finalize_update_receipt(record)


def _first_operation_receipt(record: dict[str, Any], receipt_class: str | None = None) -> dict[str, Any]:
    for operation in record["spec"]["operation_receipts"]:
        if receipt_class is None or operation.get("operation_receipt_class") == receipt_class:
            return operation
    raise AssertionError("fixture missing requested operation receipt")


def _with_single_receipt(record: dict[str, Any], receipt_class: str) -> None:
    keep = None
    for operation in record["spec"]["operation_receipts"]:
        if operation.get("operation_receipt_class") == receipt_class:
            keep = operation
            break
    if keep is None:
        keep = copy.deepcopy(_first_operation_receipt(record))
        keep["operation_receipt_class"] = receipt_class
    record["spec"]["operation_receipts"] = [keep]


def _replace_first_receipt(record: dict[str, Any], *, receipt_class: str, ownership_class: str, path: str | None = None) -> None:
    operation = _first_operation_receipt(record)
    operation["operation_receipt_class"] = receipt_class
    operation["ownership_class"] = ownership_class
    if path is not None:
        operation["target_relative_path"] = path
    if receipt_class in CHANGED_RECEIPT_CLASSES:
        suffix = _slug(str(operation.get("operation_receipt_ref", "fixture-changed")).split("/")[-1])
        artifact_ref = f"aide://update-receipt/artifact/{suffix}"
        validation_ref = f"aide://update-receipt/validation/{suffix}"
        operation["changed_artifact_ref"] = artifact_ref
        operation["validation_result_ref"] = validation_ref
        operation["approval_ref"] = "aide://approval/update-receipt-v0/fixture-review"
        if artifact_ref not in record["spec"]["artifact_refs"]:
            record["spec"]["artifact_refs"].append(artifact_ref)
        if not any(item.get("validation_result_ref") == validation_ref for item in record["spec"]["validation_results"]):
            record["spec"]["validation_results"].append(_validation_result_record(validation_ref))


def write_fixture_corpus(repo_root: str | Path = ".") -> None:
    root = Path(repo_root)
    base = minimal_fixture_record()
    valid_cases = {
        "no-op-update-receipt": mutate(base, lambda d: d["spec"].__setitem__("changed_file_refs", [])),
        "managed-file-update-receipt": mutate(base, lambda d: _with_single_receipt(d, "managed_file_updated")),
        "managed-section-update-receipt": mutate(base, lambda d: _with_single_receipt(d, "managed_section_updated")),
        "managed-file-add-receipt": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="managed_file_added", ownership_class="vendor_managed_file", path=".aide/new-managed-file.txt")),
        "managed-section-add-receipt": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="managed_section_added", ownership_class="vendor_managed_section", path="AGENTS.md")),
        "managed-file-remove-receipt": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="managed_file_removed", ownership_class="vendor_managed_file", path=".aide/removed-managed-file.txt")),
        "managed-section-remove-receipt": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="managed_section_removed", ownership_class="vendor_managed_section", path="AGENTS.md")),
        "project-owned-preservation-receipt": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="project_owned_preserved", ownership_class="project_owned", path="README.md")),
        "local-only-preservation-receipt": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="local_only_preserved", ownership_class="local_only", path=".aide.local/config.json")),
        "never-touch-preservation-receipt": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="never_touch_preserved", ownership_class="never_touch", path=".git/**")),
        "legacy-preservation-receipt": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="legacy_preserved", ownership_class="preserved_legacy", path="legacy/state.json")),
        "manual-review-skipped-operation": mutate(base, lambda d: d["spec"]["skipped_operations"].append({"skipped_operation_ref": "aide://update-receipt/skipped/manual-review-fixture", "operation_ref": "aide://update-plan/operation/manual-review-fixture", "reason": "manual_review_required", "disposition": "recorded_no_apply", "evidence_refs": [DEFAULT_EVIDENCE_REF], "extensions": {}})),
        "refused-operation": mutate(base, lambda d: _with_single_receipt(d, "operation_refused")),
        "validation-run-receipt": mutate(base, lambda d: _with_single_receipt(d, "validation_run")),
        "validation-skipped-with-warning-receipt": mutate(base, lambda d: (d["spec"]["warnings"].append("fixture validation skipped with explicit warning"), _with_single_receipt(d, "validation_skipped"))),
        "rollback-bundle-reference-receipt": mutate(base, lambda d: _with_single_receipt(d, "rollback_bundle_referenced")),
        "mixed-operation-receipt": base,
        "optional-extensions-preservation": mutate(base, lambda d: (d["spec"]["optional_features"].append("future.optional.update-receipt"), d.__setitem__("extensions", {"future.optional": {"preserve": True}}))),
    }
    invalid_cases = {
        "missing-update-plan-ref": mutate(base, lambda d: d["metadata"].__setitem__("update_plan_ref", "")),
        "missing-rollback-bundle-ref": mutate(base, lambda d: d["metadata"].__setitem__("rollback_bundle_ref", "")),
        "operation-not-in-plan": mutate(base, lambda d: _first_operation_receipt(d).__setitem__("operation_ref", "aide://update-plan/operation/not-in-plan")),
        "unplanned-changed-file": mutate(base, lambda d: d["spec"]["changed_file_refs"].append({"changed_file_ref": "aide://update-receipt/artifact/unplanned", "operation_ref": "aide://update-plan/operation/unplanned", "target_relative_path": ".aide/unplanned.txt", "artifact_ref": "aide://update-receipt/artifact/unplanned", "evidence_refs": [DEFAULT_EVIDENCE_REF], "extensions": {}})),
        "preimage-digest-mismatch": mutate(base, lambda d: _first_operation_receipt(d, "managed_file_updated").__setitem__("preimage_digest", "sha256:" + "1" * 64)),
        "postimage-digest-mismatch": mutate(base, lambda d: _first_operation_receipt(d, "managed_file_updated").__setitem__("postimage_digest", "sha256:" + "2" * 64)),
        "project-owned-changed": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="managed_file_updated", ownership_class="project_owned", path="README.md")),
        "local-only-changed": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="managed_file_updated", ownership_class="local_only", path=".aide.local/config.json")),
        "never-touch-changed": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="managed_file_updated", ownership_class="never_touch", path=".git/config")),
        "unknown-ownership-changed": mutate(base, lambda d: _replace_first_receipt(d, receipt_class="managed_file_updated", ownership_class="unknown", path="unknown/file.txt")),
        "missing-approval": mutate(base, lambda d: _first_operation_receipt(d, "managed_file_updated").__setitem__("approval_ref", None)),
        "missing-validation": mutate(base, lambda d: _first_operation_receipt(d, "managed_file_updated").__setitem__("validation_result_ref", None)),
        "missing-rollback-bundle": mutate(base, lambda d: d["metadata"].__setitem__("rollback_bundle_ref", "")),
        "receipt-claiming-apply-authority": mutate(base, lambda d: d["status"].__setitem__("update_apply_implemented", True)),
        "receipt-claiming-release-readiness": mutate(base, lambda d: d["status"].__setitem__("release_readiness_claimed", True)),
        "absolute-path": mutate(base, lambda d: _first_operation_receipt(d).__setitem__("target_relative_path", "C:/outside/file.txt")),
        "traversal-path": mutate(base, lambda d: _first_operation_receipt(d).__setitem__("target_relative_path", "../outside/file.txt")),
        "source-latest-as-target-truth": mutate(base, lambda d: d["spec"]["limitations"].append({"limitation_ref": ".aide/context/latest-task-packet.md", "limitation_class": "source_output_misuse", "evidence_refs": [DEFAULT_EVIDENCE_REF], "extensions": {}})),
        "unknown-required-feature": mutate(base, lambda d: d["spec"]["required_features"].append("future.required.update-receipt")),
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
    "missing-update-plan-ref": ["update_receipt.update_plan_missing"],
    "missing-rollback-bundle-ref": ["update_receipt.rollback_bundle_missing"],
    "operation-not-in-plan": ["update_receipt.operation_not_in_plan"],
    "unplanned-changed-file": ["update_receipt.unplanned_operation_claimed"],
    "preimage-digest-mismatch": ["update_receipt.preimage_digest_mismatch"],
    "postimage-digest-mismatch": ["update_receipt.postimage_digest_mismatch"],
    "project-owned-changed": ["update_receipt.project_owned_changed"],
    "local-only-changed": ["update_receipt.local_only_changed"],
    "never-touch-changed": ["update_receipt.never_touch_changed"],
    "unknown-ownership-changed": ["update_receipt.unknown_ownership_changed"],
    "missing-approval": ["update_receipt.approval_ref_missing"],
    "missing-validation": ["update_receipt.validation_result_missing"],
    "missing-rollback-bundle": ["update_receipt.rollback_bundle_missing"],
    "receipt-claiming-apply-authority": ["update_receipt.apply_authority_claimed"],
    "receipt-claiming-release-readiness": ["update_receipt.release_readiness_claimed"],
    "absolute-path": ["update_receipt.absolute_path_forbidden"],
    "traversal-path": ["update_receipt.path_traversal_forbidden"],
    "source-latest-as-target-truth": ["update_receipt.source_state_contamination"],
    "unknown-required-feature": ["update_receipt.unknown_required_feature"],
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
    bundle = rollback_bundle.minimal_fixture_record()
    result = validate_update_receipt_object(
        record,
        manifest=manifest,
        lock=lock,
        ledger=ledger,
        install_source=install_source,
        plan=plan,
        bundle=bundle,
        require_rollback_bundle_acceptance=False,
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
    return {"schema_version": "aide.update-receipt-fixture-matrix.v0", "fixture_results": results}


def schema_alignment_errors(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema must declare Draft 2020-12")
    if schema.get("properties", {}).get("kind", {}).get("const") != KIND:
        errors.append("schema kind const must be UpdateReceipt")
    metadata_required = set(schema.get("$defs", {}).get("metadata", {}).get("required", []))
    for field in [
        "update_receipt_ref",
        "update_plan_ref",
        "rollback_bundle_ref",
        "target_project_ref",
        "old_project_lock_ref",
        "new_project_lock_ref",
        "prior_ownership_ledger_ref",
        "new_ownership_ledger_ref",
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
        "new_install_record_ref",
        "operation_receipts",
        "skipped_operations",
        "failed_operations",
        "changed_file_refs",
        "changed_section_refs",
        "preimage_digests",
        "postimage_digests",
        "artifact_refs",
        "validation_results",
        "approval_ref",
        "executor_ref",
        "execution_environment",
        "warnings",
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
        "schema_version": "aide.update-receipt-status.v0",
        "status": "PASS_WITH_WARNINGS" if (root / SCHEMA_PATH).exists() and (root / "core/protocol/update_receipt.py").exists() else "FAILED_VALIDATION",
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/update_receipt.py").exists(),
        "rollback_bundle_acceptance_report_exists": (root / ROLLBACK_BUNDLE_ACCEPTANCE_JSON).exists(),
        "update_receipt_projection_exists": (root / PROJECTION_JSON).exists(),
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
        "distribution_apply_engine_started": False,
        "warnings": ["UpdateReceipt v0 remains proposed until independent check and acceptance."],
    }
    write_text(root / STATUS_MD, render_status_md(data))
    return data


def project(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    receipt = build_update_receipt(root)
    validation = validate_update_receipt_object(receipt, repo_root=root)
    matrix = fixture_matrix(root)
    report = {
        "schema_version": "aide.update-receipt-project-report.v0",
        "status": validation["status"],
        "proposed_capability": PROPOSED_CAPABILITY,
        "update_receipt_path": PROJECTION_JSON.as_posix(),
        "update_receipt_digest": receipt["status"]["update_receipt_digest"],
        "operation_receipt_count": len(receipt["spec"]["operation_receipts"]),
        "skipped_operation_count": len(receipt["spec"]["skipped_operations"]),
        "failed_operation_count": len(receipt["spec"]["failed_operations"]),
        "changed_file_ref_count": len(receipt["spec"]["changed_file_refs"]),
        "changed_section_ref_count": len(receipt["spec"]["changed_section_refs"]),
        "validation_result_count": len(receipt["spec"]["validation_results"]),
        "risk_class": receipt["spec"]["risk_class"],
        "recommended_next_task": CHECK_TASK_ID,
        "source_artifacts_mutated": False,
        "target_repository_mutation_implemented": False,
        "distribution_apply_engine_started": False,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "warnings": [
            "UpdateReceipt v0 records future execution metadata only and performs no update apply.",
            "Source generated latest-* outputs are not target truth.",
        ],
    }
    write_json(root / PROJECTION_JSON, receipt)
    write_json(root / PROJECT_REPORT_JSON, report)
    write_json(root / FIXTURE_MATRIX_JSON, matrix)
    write_text(root / FIXTURE_MATRIX_MD, render_fixture_matrix_md(matrix["fixture_results"]))
    write_text(root / OPERATION_SUMMARY_MD, render_operation_summary_md(receipt))
    write_text(root / SKIPPED_OPERATIONS_MD, render_skipped_operations_md(receipt))
    write_text(root / NO_APPLY_BOUNDARY_MD, render_no_apply_boundary_md())
    write_text(root / LIMITATIONS_MD, render_limitations_md(receipt))
    status(root)
    write_validation_reports(root)
    return report


def validate(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    schema = load_schema(root)
    plan = load_update_plan_source(root)
    bundle = load_rollback_bundle_source(root)
    manifest = load_distribution_manifest(root)
    lock = load_project_lock(root)
    ledger = load_ownership_ledger(root)
    install_source = load_install_record_source(root)
    receipt = build_update_receipt(root, plan=plan, bundle=bundle, manifest=manifest, lock=lock, ledger=ledger, install_source=install_source)
    validation = validate_update_receipt_object(
        receipt,
        plan=plan,
        bundle=bundle,
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
        "helper_exists": (root / "core/protocol/update_receipt.py").exists(),
        "cli_registered": cli_registered(root),
        "update_receipt_generated": receipt["kind"] == KIND,
        "update_receipt_valid": validation["valid"],
        "schema_alignment": not alignment_errors,
        "fixture_matrix_passed": not fixture_failures,
        "rollback_bundle_accepted": rollback_bundle_is_accepted(root),
        "update_plan_bound": receipt["metadata"]["update_plan_ref"] == plan["metadata"]["update_plan_ref"],
        "rollback_bundle_bound": receipt["metadata"]["rollback_bundle_ref"] == bundle["metadata"]["rollback_bundle_ref"],
        "source_distribution_bound": receipt["metadata"]["source_distribution_ref"] == manifest["metadata"]["distribution_ref"],
        "candidate_distribution_bound": receipt["metadata"]["candidate_distribution_ref"] == plan["metadata"]["candidate_distribution_ref"],
        "old_project_lock_bound": receipt["metadata"]["old_project_lock_digest"] == lock["status"]["project_lock_digest"],
        "new_project_lock_bound": receipt["metadata"]["new_project_lock_digest"] == plan["metadata"]["candidate_project_lock_digest"],
        "ownership_ledger_bound": receipt["metadata"]["prior_ownership_ledger_digest"] == ledger["status"]["ownership_ledger_digest"],
        "install_record_bound": install_source["metadata"]["install_record_ref"] in receipt["spec"]["prior_install_record_refs"],
        "update_apply_not_implemented": receipt["status"]["update_apply_implemented"] is False,
        "install_apply_not_implemented": receipt["status"]["install_apply_implemented"] is False,
        "migration_apply_not_implemented": receipt["status"]["migration_apply_implemented"] is False,
        "rollback_apply_not_implemented": receipt["status"]["rollback_apply_implemented"] is False,
        "uninstall_apply_not_implemented": receipt["status"]["uninstall_apply_implemented"] is False,
        "target_repository_mutation_not_implemented": receipt["status"]["target_repository_mutation_implemented"] is False,
        "distribution_apply_engine_not_started": receipt["status"]["distribution_apply_engine_started"] is False,
        "source_output_not_target_truth": receipt["spec"]["source_output_used_as_target_truth"] is False,
    }
    errors: list[dict[str, str]] = []
    if not validation["valid"]:
        errors.extend(validation["errors"])
    for error in alignment_errors:
        errors.append({"code": "update_receipt.schema_alignment", "message": error})
    for failure in fixture_failures:
        errors.append({"code": "update_receipt.fixture_failure", "message": failure["case_id"]})
    if not checks["rollback_bundle_accepted"]:
        errors.append({"code": "update_receipt.rollback_bundle_missing", "message": "RollbackBundle v0 acceptance report is missing or invalid"})
    validation_status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    report = {
        "schema_version": "aide.update-receipt-validation.v0",
        "status": validation_status,
        "validation_status": validation_status,
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": CHECK_TASK_ID,
        "checks": checks,
        "errors": errors,
        "schema_alignment_errors": alignment_errors,
        "update_receipt_validation": validation,
        "fixture_results": matrix["fixture_results"],
        "warnings": [
            "UpdateReceipt v0 is proposed until independent check and acceptance.",
            "UpdateReceipt records execution receipts only and performs no update apply.",
            "DistributionApplyEngine remains a future dependency after acceptance.",
        ],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
    }
    write_json(root / PROJECTION_JSON, receipt)
    write_json(root / VALIDATION_JSON, report)
    write_json(root / FIXTURE_MATRIX_JSON, matrix)
    write_text(root / VALIDATION_MD, render_validation_md(report))
    write_text(root / FIXTURE_MATRIX_MD, render_fixture_matrix_md(matrix["fixture_results"]))
    write_text(root / OPERATION_SUMMARY_MD, render_operation_summary_md(receipt))
    write_text(root / SKIPPED_OPERATIONS_MD, render_skipped_operations_md(receipt))
    write_text(root / NO_APPLY_BOUNDARY_MD, render_no_apply_boundary_md())
    write_text(root / LIMITATIONS_MD, render_limitations_md(receipt))
    status(root)
    return report


def write_validation_reports(repo_root: str | Path = ".") -> None:
    validate(repo_root)


def cli_registered(repo_root: Path) -> bool:
    script = repo_root / ".aide/scripts/aide_lite.py"
    if not script.exists():
        return False
    text = script.read_text(encoding="utf-8")
    return "update-receipt" in text and "command_update_receipt_validate" in text


def render_status_md(data: dict[str, Any]) -> str:
    lines = [
        "# UpdateReceipt v0 Status",
        "",
        f"- status: `{data.get('status')}`",
        f"- proposed_capability: `{data.get('proposed_capability')}`",
        f"- schema_exists: `{str(data.get('schema_exists', False)).lower()}`",
        f"- helper_exists: `{str(data.get('helper_exists', False)).lower()}`",
        f"- rollback_bundle_acceptance_report_exists: `{str(data.get('rollback_bundle_acceptance_report_exists', False)).lower()}`",
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
        "# UpdateReceipt v0 Validation",
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
    lines = ["# UpdateReceipt v0 Fixture Matrix", "", "| Case | Expected | Observed | Codes | Pass |", "| --- | --- | --- | --- | --- |"]
    for fixture in fixtures:
        codes = ", ".join(fixture.get("observed_refusal_codes", [])) or "none"
        lines.append(f"| {fixture['case_id']} | {fixture['expected_result']} | {fixture['observed_result']} | {codes} | {str(fixture['passed']).lower()} |")
    return "\n".join(lines) + "\n"


def render_operation_summary_md(receipt: dict[str, Any]) -> str:
    operation_receipts = receipt.get("spec", {}).get("operation_receipts", [])
    lines = [
        "# UpdateReceipt v0 Operation Summary",
        "",
        "Operation receipts record observed future execution facts only. They are not actions.",
        "",
        "| Receipt | Class | Source Operation | Path | No Apply | No Mutation |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in operation_receipts:
        lines.append(
            "| {receipt} | {klass} | {source} | {path} | {apply} | {mutation} |".format(
                receipt=item.get("operation_receipt_ref"),
                klass=item.get("operation_receipt_class"),
                source=item.get("operation_ref"),
                path=item.get("target_relative_path") or "metadata",
                apply=str(not item.get("update_apply_implemented", False)).lower(),
                mutation=str(not item.get("target_repository_mutation_performed", False)).lower(),
            )
        )
    return "\n".join(lines) + "\n"


def render_skipped_operations_md(receipt: dict[str, Any]) -> str:
    skipped = receipt.get("spec", {}).get("skipped_operations", [])
    lines = [
        "# UpdateReceipt v0 Skipped Operations",
        "",
        "Skipped operations are recorded as receipt facts only and do not authorize retry or apply.",
        "",
        "| Skipped Operation | Source Operation | Reason | Disposition |",
        "| --- | --- | --- | --- |",
    ]
    for item in skipped:
        lines.append(f"| {item.get('skipped_operation_ref')} | {item.get('operation_ref')} | {item.get('reason')} | {item.get('disposition')} |")
    if not skipped:
        lines.append("| none | none | none | none |")
    return "\n".join(lines) + "\n"


def render_no_apply_boundary_md() -> str:
    lines = [
        "# UpdateReceipt v0 No-Apply Boundary",
        "",
        "UpdateReceipt v0 records execution receipts only.",
        "",
        "It does not:",
        "",
        "- authorize execution;",
        "- perform update apply;",
        "- perform install, migration, rollback, repair, or uninstall apply;",
        "- mutate target repositories;",
        "- create release archives, tags, uploads, or GitHub Releases;",
        "- start DistributionApplyEngine, self-consumer fixtures, or canaries;",
        "- call provider, model, or network services.",
    ]
    return "\n".join(lines) + "\n"


def render_limitations_md(receipt: dict[str, Any]) -> str:
    lines = ["# UpdateReceipt v0 Limitations", ""]
    for item in receipt.get("spec", {}).get("limitations", []):
        lines.append(f"- `{item.get('limitation_ref')}`: {item.get('disposition')}")
    return "\n".join(lines) + "\n"
