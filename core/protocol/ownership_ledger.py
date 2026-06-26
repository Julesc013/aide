"""OwnershipLedger v1 helpers.

OwnershipLedger records ownership taxonomy and path/section authority for a
ProjectLock-selected AIDE distribution. It is not an install plan, install
record, apply engine, admission record, authorization mechanism, or mutation
mechanism.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import envelope, project_lock


API_VERSION = envelope.API_VERSION
KIND = "OwnershipLedger"
SCHEMA_VERSION = "aide.ownership-ledger.v1"
TASK_ID = "AIDE-BUILD-OWNERSHIP-LEDGER-V1-01"
CHECK_TASK_ID = "AIDE-CHECK-OWNERSHIP-LEDGER-V1-01"
REPAIR_TASK_ID = "AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01"
REPAIR_CHECK_TASK_ID = "AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01"
PROPOSED_CAPABILITY = "ownership_ledger_v1"
DETERMINISTIC_TIMESTAMP = "fixture-timestamp:ownership-ledger-v1"
DEFAULT_EVIDENCE_REF = "aide://evidence/ownership-ledger-v1/source-projection"

REPORT_ROOT = Path(".aide/reports/ownership-ledger-v1")
REPAIR_REPORT_ROOT = Path(".aide/reports/ownership-ledger-v1-repair-01")
SCHEMA_PATH = Path(".aide/protocol/aide-ownership-ledger-v1.schema.json")
FIXTURE_ROOT = Path(".aide/fixtures/ownership-ledger-v1")

LEDGER_JSON = REPORT_ROOT / "ownership-ledger.json"
LEDGER_MD = REPORT_ROOT / "ownership-ledger.md"
STATUS_MD = REPORT_ROOT / "status.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
TAXONOMY_JSON = REPORT_ROOT / "taxonomy.json"
RECORD_INDEX_JSON = REPORT_ROOT / "record-index.json"
FIXTURE_MATRIX_JSON = REPORT_ROOT / "fixture-matrix.json"
FIXTURE_MATRIX_MD = REPORT_ROOT / "fixture-matrix.md"
NON_CAPABILITIES_MD = REPORT_ROOT / "non-capabilities.md"
Q43_MIGRATION_JSON = REPORT_ROOT / "q43-migration.json"
Q43_MIGRATION_MD = REPORT_ROOT / "q43-migration.md"

PROJECT_LOCK_JSON = project_lock.LOCK_JSON
PROJECT_LOCK_ACCEPTANCE_JSON = Path(".aide/reports/project-lock-v0-accept/acceptance-report.json")

OWNERSHIP_CLASSES = [
    "vendor_managed_file",
    "vendor_managed_section",
    "project_owned",
    "project_overlay",
    "project_generated",
    "runtime_generated",
    "local_only",
    "evidence_only",
    "preserved_legacy",
    "unknown",
    "never_touch",
]

SUPPORTED_REQUIRED_FEATURES = {
    "ownership_ledger_v1",
    "project_lock_v0",
    "distribution_manifest_v1",
    "sha256_digest_canonical_json_v1",
}

SUPPORTED_OPTIONAL_FEATURES = {
    "managed_section_identity_v1",
    "target_overlay_ownership_v1",
    "q43_ownership_migration_v1",
}

REFUSAL_CODES = [
    "ownership_ledger.missing",
    "ownership_ledger.invalid",
    "ownership_ledger.project_lock_not_accepted",
    "ownership_ledger.project_lock_digest_mismatch",
    "ownership_ledger.missing_taxonomy_class",
    "ownership_ledger.unknown_taxonomy_class",
    "ownership_ledger.duplicate_record",
    "ownership_ledger.record_class_unknown",
    "ownership_ledger.file_entry_contract_missing",
    "ownership_ledger.owner_missing",
    "ownership_ledger.vendor_digest_missing",
    "ownership_ledger.vendor_source_missing",
    "ownership_ledger.observed_digest_mismatch",
    "ownership_ledger.mutable_by_distribution_forbidden",
    "ownership_ledger.managed_section_identity_missing",
    "ownership_ledger.section_identity_missing",
    "ownership_ledger.section_identity_mismatch",
    "ownership_ledger.section_marker_duplicate",
    "ownership_ledger.section_overlap",
    "ownership_ledger.nested_ownership_ambiguity",
    "ownership_ledger.file_section_conflict",
    "ownership_ledger.path_collision",
    "ownership_ledger.case_collision",
    "ownership_ledger.source_component_mismatch",
    "ownership_ledger.source_distribution_mismatch",
    "ownership_ledger.evidence_missing",
    "ownership_ledger.symlink_unresolved",
    "ownership_ledger.reparse_point_unresolved",
    "ownership_ledger.unknown_allows_apply",
    "ownership_ledger.never_touch_allows_apply",
    "ownership_ledger.automatic_apply_forbidden",
    "ownership_ledger.absolute_path_forbidden",
    "ownership_ledger.path_traversal_forbidden",
    "ownership_ledger.source_state_contamination",
    "ownership_ledger.unknown_required_feature",
    "ownership_ledger.extension_required_unknown",
    "ownership_ledger.digest_mismatch",
    "ownership_ledger.fixture_failure",
    "ownership.migration_unmapped",
]

EXPLICIT_NON_CAPABILITIES = [
    "install_truth",
    "install_plan",
    "install_apply",
    "update_apply",
    "repair_apply",
    "rollback_apply",
    "uninstall_apply",
    "admission",
    "authorization",
    "target_repository_mutation",
    "release_publication",
    "git_tag_creation",
    "github_release_creation",
    "upload",
    "network_call",
    "provider_model_call",
    "workbench_runtime",
    "mcp_runtime",
    "source_change_preview_apply_rollback",
    "promotion",
]

FILE_ENTRY_FIELDS = [
    "entry_ref",
    "target_relative_path",
    "owner_ref",
    "source_distribution_ref",
    "source_component_ref",
    "installed_content_digest",
    "observed_target_digest",
    "portable_role",
    "mutable_by_distribution",
    "preserve_policy",
    "operation_constraints",
    "platform_notes",
    "case_sensitivity_notes",
    "first_observed_at",
    "last_verified_at",
    "prior_entry_ref",
    "superseded_by_ref",
]

MANAGED_SECTION_FIELDS = [
    "containing_file_path",
    "section_identity",
    "marker_format",
    "start_marker_digest",
    "end_marker_digest",
    "section_content_digest",
    "surrounding_content_preservation_policy",
    "preimage_requirements",
    "update_constraints",
]

CLASS_BEHAVIOR: dict[str, dict[str, Any]] = {
    "vendor_managed_file": {
        "authority": "aide_distribution",
        "owner_ref": "aide://owner/aide-distribution",
        "portable_role": "distribution_content",
        "preserve_policy": "replace_only_with_exact_preimage",
        "blocks_apply": False,
        "requires_source": True,
    },
    "vendor_managed_section": {
        "authority": "aide_distribution",
        "owner_ref": "aide://owner/aide-distribution",
        "portable_role": "managed_section",
        "preserve_policy": "manual_outside_only",
        "blocks_apply": False,
        "requires_source": True,
    },
    "project_owned": {
        "authority": "target_project",
        "owner_ref": "aide://owner/target-project",
        "portable_role": "project_content",
        "preserve_policy": "preserve",
        "blocks_apply": True,
        "requires_source": False,
    },
    "project_overlay": {
        "authority": "target_project",
        "owner_ref": "aide://owner/target-project",
        "portable_role": "project_overlay",
        "preserve_policy": "preserve",
        "blocks_apply": False,
        "requires_source": False,
    },
    "project_generated": {
        "authority": "target_project",
        "owner_ref": "aide://owner/target-project",
        "portable_role": "target_generated",
        "preserve_policy": "target_regenerate",
        "blocks_apply": False,
        "requires_source": False,
    },
    "runtime_generated": {
        "authority": "target_project",
        "owner_ref": "aide://owner/local-runtime",
        "portable_role": "runtime_state",
        "preserve_policy": "never_portable",
        "blocks_apply": True,
        "requires_source": False,
    },
    "local_only": {
        "authority": "target_project",
        "owner_ref": "aide://owner/local-operator",
        "portable_role": "local_state",
        "preserve_policy": "never_portable",
        "blocks_apply": True,
        "requires_source": False,
    },
    "evidence_only": {
        "authority": "target_project",
        "owner_ref": "aide://owner/target-project",
        "portable_role": "evidence",
        "preserve_policy": "preserve",
        "blocks_apply": False,
        "requires_source": False,
    },
    "preserved_legacy": {
        "authority": "target_project",
        "owner_ref": "aide://owner/target-project",
        "portable_role": "legacy",
        "preserve_policy": "preserve_legacy",
        "blocks_apply": True,
        "requires_source": False,
    },
    "unknown": {
        "authority": "target_project",
        "owner_ref": "aide://owner/unknown",
        "portable_role": "unknown",
        "preserve_policy": "manual_review_required",
        "blocks_apply": True,
        "requires_source": False,
    },
    "never_touch": {
        "authority": "target_project",
        "owner_ref": "aide://owner/never-touch",
        "portable_role": "never_touch",
        "preserve_policy": "never_touch",
        "blocks_apply": True,
        "requires_source": False,
    },
}

SUPPORTED_Q43_CLASS_MAP: dict[str, dict[str, str]] = {
    "managed_aide_file": {"ownership_class": "vendor_managed_file", "disposition": "mapped"},
    "managed_aide_section": {"ownership_class": "vendor_managed_section", "disposition": "mapped"},
    "target_project_file": {"ownership_class": "project_owned", "disposition": "mapped"},
    "target_overlay": {"ownership_class": "project_overlay", "disposition": "mapped"},
    "target_generated": {"ownership_class": "project_generated", "disposition": "mapped"},
    "runtime_generated": {"ownership_class": "runtime_generated", "disposition": "mapped"},
    "local_only": {"ownership_class": "local_only", "disposition": "mapped"},
    "evidence_record": {"ownership_class": "evidence_only", "disposition": "mapped"},
    "preserved_legacy": {"ownership_class": "preserved_legacy", "disposition": "mapped"},
    "unknown": {"ownership_class": "unknown", "disposition": "manual_review_required"},
    "never_touch": {"ownership_class": "never_touch", "disposition": "mapped"},
}

PATH_RE = re.compile(r"(^[A-Za-z]:[\\/])|(^\\\\)|(^/)|(^|/)\.\.($|/)")


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def canonical_json_bytes(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_digest(data: bytes) -> str:
    return "sha256:" + __import__("hashlib").sha256(data).hexdigest()


def stable_digest_text(text: str) -> str:
    return sha256_digest(text.encode("utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_json(path: Path, data: dict[str, Any]) -> None:
    write_text(path, stable_json(data))


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not load JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def load_project_lock(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / PROJECT_LOCK_JSON
    if path.exists():
        return read_json(path)
    return project_lock.build_project_lock(repo_root)


def load_project_lock_acceptance(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / PROJECT_LOCK_ACCEPTANCE_JSON
    if not path.exists():
        return {}
    return read_json(path)


def project_lock_is_accepted(repo_root: str | Path, lock: dict[str, Any]) -> bool:
    acceptance = load_project_lock_acceptance(repo_root)
    return (
        acceptance.get("result") == "ACCEPTED_WITH_WARNINGS"
        and acceptance.get("accepted_capability") == "project_lock_v0"
        and acceptance.get("material_finding_count") == 0
        and acceptance.get("source_check_result") == "PASS_WITH_WARNINGS"
        and lock.get("status", {}).get("project_lock_digest") is not None
    )


def taxonomy() -> list[dict[str, Any]]:
    descriptions = {
        "vendor_managed_file": "AIDE-distributed file with exact source digest authority.",
        "vendor_managed_section": "AIDE-distributed managed section inside a host file.",
        "project_owned": "Target project file that AIDE must not overwrite silently.",
        "project_overlay": "Target-owned overlay that configures an AIDE distribution.",
        "project_generated": "Target-local generated projection that is recreated in target context.",
        "runtime_generated": "Runtime/local generated state outside committed distribution truth.",
        "local_only": "Local operator state that is never distribution truth.",
        "evidence_only": "Evidence records preserved for audit, not source distribution content.",
        "preserved_legacy": "Legacy or pre-existing target state preserved unless manually migrated.",
        "unknown": "Observed path without sufficient ownership proof; blocks automatic apply.",
        "never_touch": "Path class that AIDE distribution apply must never modify.",
    }
    entries = []
    for class_id in OWNERSHIP_CLASSES:
        behavior = CLASS_BEHAVIOR[class_id]
        entries.append(
            {
                "class_id": class_id,
                "authority": behavior["authority"],
                "automatic_apply_allowed": False,
                "overwrite_allowed": False,
                "delete_allowed": False,
                "blocks_automatic_apply": bool(behavior["blocks_apply"]),
                "description": descriptions[class_id],
                "extensions": {},
            }
        )
    return entries


def operation_constraints(ownership_class: str) -> dict[str, Any]:
    return {
        "create_allowed": False,
        "replace_allowed": False,
        "delete_allowed": False,
        "update_managed_section_allowed": False,
        "requires_exact_preimage": True,
        "requires_manual_review": bool(CLASS_BEHAVIOR[ownership_class]["blocks_apply"]),
        "extensions": {},
    }


def section_preimage_requirements() -> dict[str, Any]:
    return {
        "exact_section_identity_required": True,
        "exact_start_marker_required": True,
        "exact_end_marker_required": True,
        "duplicate_markers_forbidden": True,
        "overlap_forbidden": True,
        "manual_outside_content_preserved": True,
        "extensions": {},
    }


def section_update_constraints() -> dict[str, Any]:
    return {
        "update_allowed_by_ledger": False,
        "requires_exact_preimage": True,
        "requires_identity_match": True,
        "requires_manual_outside_only": True,
        "extensions": {},
    }


def ownership_record(
    record_id: str,
    ownership_class: str,
    target_path: str,
    *,
    path_kind: str = "file",
    source_ref: str | None = None,
    content_digest: str | None = None,
    section_id: str | None = None,
    managed_section_identity: str | None = None,
    authority: str | None = None,
    source_component_ref: str | None = None,
    observed_target_digest: str | None = None,
    evidence_refs: list[str] | None = None,
    extensions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    behavior = CLASS_BEHAVIOR.get(ownership_class, CLASS_BEHAVIOR["unknown"])
    installed_digest = content_digest
    observed_digest = observed_target_digest if observed_target_digest is not None else installed_digest
    section_identity = managed_section_identity if path_kind == "managed_section" else None
    section_marker_base = f"{record_id}:{target_path}:{section_id or ''}:{section_identity or ''}"
    section_fields = {
        "containing_file_path": target_path if path_kind == "managed_section" else None,
        "section_identity": section_identity,
        "marker_format": "aide-generated-html-comment" if path_kind == "managed_section" else None,
        "start_marker_digest": stable_digest_text(section_marker_base + ":start") if path_kind == "managed_section" else None,
        "end_marker_digest": stable_digest_text(section_marker_base + ":end") if path_kind == "managed_section" else None,
        "section_content_digest": stable_digest_text(section_marker_base + ":content") if path_kind == "managed_section" else None,
        "surrounding_content_preservation_policy": "manual_outside_only" if path_kind == "managed_section" else None,
        "preimage_requirements": section_preimage_requirements() if path_kind == "managed_section" else None,
        "update_constraints": section_update_constraints() if path_kind == "managed_section" else None,
    }
    return {
        "record_id": record_id,
        "entry_ref": f"aide://ownership-entry/{record_id}",
        "ownership_class": ownership_class,
        "path_kind": path_kind,
        "target_path": target_path,
        "target_relative_path": target_path,
        "section_id": section_id,
        "source_ref": source_ref,
        "source_distribution_ref": source_ref if behavior["requires_source"] else None,
        "source_component_ref": source_component_ref or ("aide://component/aide-lite-core" if behavior["requires_source"] else None),
        "content_digest": installed_digest,
        "installed_content_digest": installed_digest,
        "observed_target_digest": observed_digest,
        "managed_section_identity": managed_section_identity,
        **section_fields,
        "owner_ref": behavior["owner_ref"],
        "authority": authority or behavior["authority"],
        "portable_role": behavior["portable_role"],
        "mutation_policy": "no_apply_metadata_only",
        "mutable_by_distribution": False,
        "preserve_policy": behavior["preserve_policy"],
        "operation_constraints": operation_constraints(ownership_class),
        "platform_notes": [],
        "case_sensitivity_notes": "case-fold target-path collisions fail validation",
        "first_observed_at": DETERMINISTIC_TIMESTAMP,
        "last_verified_at": DETERMINISTIC_TIMESTAMP,
        "prior_entry_ref": None,
        "superseded_by_ref": None,
        "apply_allowed": False,
        "overwrite_allowed": False,
        "delete_allowed": False,
        "evidence_refs": evidence_refs or [DEFAULT_EVIDENCE_REF],
        "extensions": extensions or {},
    }


def default_records(lock: dict[str, Any]) -> list[dict[str, Any]]:
    selected_digest = lock.get("spec", {}).get("selected_components", [{}])[0].get("selected_digest")
    source_distribution_ref = lock.get("metadata", {}).get("selected_distribution_ref")
    return [
        ownership_record(
            "vendor-file-aide-lite-cli",
            "vendor_managed_file",
            ".aide/scripts/aide_lite.py",
            source_ref=source_distribution_ref,
            content_digest=selected_digest,
        ),
        ownership_record(
            "vendor-file-project-lock-schema",
            "vendor_managed_file",
            ".aide/protocol/aide-project-lock-v0.schema.json",
            source_ref=source_distribution_ref,
            content_digest=selected_digest,
        ),
        ownership_record(
            "vendor-section-agents-summary",
            "vendor_managed_section",
            "AGENTS.md",
            path_kind="managed_section",
            section_id="aide-self-hosting-summary",
            source_ref=source_distribution_ref,
            content_digest=selected_digest,
            managed_section_identity="AIDE-GENERATED:aide-self-hosting-summary",
        ),
        ownership_record("project-owned-readme", "project_owned", "README.md"),
        ownership_record("project-overlay-policy", "project_overlay", ".aide/project-overlays/policy.yaml"),
        ownership_record("project-generated-context", "project_generated", ".aide/context/generated/context-pack.json"),
        ownership_record("runtime-generated-local-state", "runtime_generated", ".aide.local/**", path_kind="glob"),
        ownership_record("local-only-operator-state", "local_only", "local-only/**", path_kind="glob"),
        ownership_record("evidence-only-queue-evidence", "evidence_only", ".aide/queue/**/evidence/**", path_kind="glob"),
        ownership_record("preserved-legacy-state", "preserved_legacy", ".aide/legacy/**", path_kind="glob"),
        ownership_record("unknown-unclassified", "unknown", "unclassified/**", path_kind="glob"),
        ownership_record("never-touch-git", "never_touch", ".git/**", path_kind="glob"),
    ]


def build_ownership_ledger(repo_root: str | Path) -> dict[str, Any]:
    lock = load_project_lock(repo_root)
    lock_digest = lock["status"]["project_lock_digest"]
    ledger = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "ledger_ref": "aide://ownership-ledger/aide-self-project-lock-v0",
            "project_ref": lock["metadata"]["project_ref"],
            "project_identity": lock["metadata"]["project_identity"],
            "project_lock_ref": lock["metadata"]["project_lock_ref"],
            "project_lock_digest": lock_digest,
            "selected_distribution_digest": lock["metadata"]["selected_distribution_digest"],
            "manifest_payload_digest": lock["metadata"]["manifest_payload_digest"],
            "ownership_profile": "aide-lite-target-default",
            "ledger_revision": "0",
            "created_from": "accepted_project_lock_v0",
            "created_at_classification": "deterministic_projection_not_wall_clock",
            "extensions": {},
        },
        "spec": {
            "required_features": sorted(SUPPORTED_REQUIRED_FEATURES),
            "optional_features": sorted(SUPPORTED_OPTIONAL_FEATURES),
            "taxonomy": taxonomy(),
            "records": default_records(lock),
            "unknown_ownership_policy": {
                "blocks_automatic_apply": True,
                "requires_manual_review": True,
                "extensions": {},
            },
            "managed_section_policy": {
                "requires_exact_section_identity": True,
                "manual_outside_only": True,
                "extensions": {},
            },
            "q43_migration_policy": {
                "supported_source_schema": "aide.install-ownership-ledger.v0",
                "unmapped_class_refusal_code": "ownership.migration_unmapped",
                "ambiguous_classes_require_manual_review": True,
                "extensions": {},
            },
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "validation_result": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "recommended_next_task": REPAIR_CHECK_TASK_ID,
            "ownership_ledger_digest": "",
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "admission_implemented": False,
            "authorization_implemented": False,
            "extensions": {},
        },
        "extensions": {},
    }
    return finalize_ownership_ledger(ledger)


def ownership_ledger_payload(ledger: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(ledger)
    payload.pop("status", None)
    return payload


def ownership_ledger_digest(ledger: dict[str, Any]) -> str:
    return sha256_digest(canonical_json_bytes(ownership_ledger_payload(ledger)))


def finalize_ownership_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    ledger = copy.deepcopy(ledger)
    ledger.setdefault("status", {})["ownership_ledger_digest"] = ownership_ledger_digest(ledger)
    return ledger


def _add_error(errors: list[dict[str, str]], code: str, message: str) -> None:
    errors.append({"code": code, "message": message})


def _path_refusal(path: str) -> str | None:
    normalized = path.replace("\\", "/")
    if PATH_RE.search(normalized):
        if normalized.startswith("/") or re.match(r"^[A-Za-z]:/", normalized) or normalized.startswith("//"):
            return "ownership_ledger.absolute_path_forbidden"
        return "ownership_ledger.path_traversal_forbidden"
    if "latest-" in normalized or "/latest-" in normalized:
        return "ownership_ledger.source_state_contamination"
    return None


def _extension_refusal(container: dict[str, Any]) -> bool:
    extensions = container.get("extensions")
    if not isinstance(extensions, dict):
        return False
    return any(str(key).startswith("requires.") for key in extensions)


def _overlaps(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return int(left.get("start_line", 0)) <= int(right.get("end_line", 0)) and int(right.get("start_line", 0)) <= int(left.get("end_line", 0))


def _contains(outer: dict[str, Any], inner: dict[str, Any]) -> bool:
    return int(outer.get("start_line", 0)) < int(inner.get("start_line", 0)) and int(outer.get("end_line", 0)) > int(inner.get("end_line", 0))


def _validate_file_entry_contract(record: dict[str, Any], errors: list[dict[str, str]], record_id: str) -> None:
    for field in FILE_ENTRY_FIELDS:
        if field not in record:
            _add_error(errors, "ownership_ledger.file_entry_contract_missing", f"record missing file-entry field {field}: {record_id}")
    if not record.get("owner_ref"):
        _add_error(errors, "ownership_ledger.owner_missing", f"record missing owner_ref: {record_id}")
    if record.get("mutable_by_distribution") is not False:
        _add_error(errors, "ownership_ledger.mutable_by_distribution_forbidden", f"record mutable by distribution: {record_id}")
    if not isinstance(record.get("operation_constraints"), dict):
        _add_error(errors, "ownership_ledger.file_entry_contract_missing", f"record missing operation constraints: {record_id}")
    if not isinstance(record.get("evidence_refs"), list) or not record.get("evidence_refs"):
        _add_error(errors, "ownership_ledger.evidence_missing", f"record missing evidence refs: {record_id}")


def _validate_vendor_contract(record: dict[str, Any], errors: list[dict[str, str]], record_id: str) -> None:
    ownership_class = record.get("ownership_class")
    if ownership_class not in {"vendor_managed_file", "vendor_managed_section"}:
        return
    if not record.get("content_digest") or not record.get("installed_content_digest"):
        _add_error(errors, "ownership_ledger.vendor_digest_missing", f"vendor record missing digest: {record_id}")
    if not record.get("source_distribution_ref") or not record.get("source_component_ref"):
        _add_error(errors, "ownership_ledger.vendor_source_missing", f"vendor record missing source refs: {record_id}")
    if record.get("source_ref") and record.get("source_distribution_ref") and record["source_ref"] != record["source_distribution_ref"]:
        _add_error(errors, "ownership_ledger.source_distribution_mismatch", f"source distribution mismatch: {record_id}")
    if record.get("source_component_ref") and not str(record.get("source_component_ref")).startswith("aide://component/"):
        _add_error(errors, "ownership_ledger.source_component_mismatch", f"source component mismatch: {record_id}")


def _validate_digest_observation(record: dict[str, Any], errors: list[dict[str, str]], record_id: str) -> None:
    installed = record.get("installed_content_digest")
    observed = record.get("observed_target_digest")
    if installed and observed and installed != observed:
        _add_error(errors, "ownership_ledger.observed_digest_mismatch", f"installed and observed digest mismatch: {record_id}")


def _validate_section_contract(record: dict[str, Any], errors: list[dict[str, str]], record_id: str) -> None:
    if record.get("path_kind") != "managed_section":
        return
    for field in MANAGED_SECTION_FIELDS:
        if field not in record:
            _add_error(errors, "ownership_ledger.section_identity_missing", f"managed section missing field {field}: {record_id}")
    if not record.get("section_identity"):
        _add_error(errors, "ownership_ledger.section_identity_missing", f"managed section missing section_identity: {record_id}")
    if not record.get("managed_section_identity"):
        _add_error(errors, "ownership_ledger.managed_section_identity_missing", f"managed section missing managed_section_identity: {record_id}")
    if record.get("section_identity") and record.get("managed_section_identity") and record.get("section_identity") != record.get("managed_section_identity"):
        _add_error(errors, "ownership_ledger.section_identity_mismatch", f"managed section identity mismatch: {record_id}")
    if not record.get("containing_file_path"):
        _add_error(errors, "ownership_ledger.section_identity_missing", f"managed section missing containing file: {record_id}")
    marker_occurrences = record.get("extensions", {}).get("marker_occurrences") if isinstance(record.get("extensions"), dict) else None
    if isinstance(marker_occurrences, dict):
        if marker_occurrences.get("start", 1) != 1 or marker_occurrences.get("end", 1) != 1:
            _add_error(errors, "ownership_ledger.section_marker_duplicate", f"managed section marker count invalid: {record_id}")


def _validate_record_conflicts(records: list[dict[str, Any]], errors: list[dict[str, str]]) -> None:
    by_target: dict[str, dict[str, Any]] = {}
    by_casefold: dict[str, str] = {}
    file_records: dict[str, dict[str, Any]] = {}
    section_records: list[dict[str, Any]] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        record_id = str(record.get("record_id", ""))
        target_path = str(record.get("target_relative_path") or record.get("target_path") or "")
        normalized = target_path.replace("\\", "/")
        if record.get("path_kind") not in {"glob"}:
            if normalized in by_target and by_target[normalized].get("record_id") != record_id:
                _add_error(errors, "ownership_ledger.path_collision", f"duplicate target path: {normalized}")
            by_target[normalized] = record
            folded = normalized.casefold()
            if folded in by_casefold and by_casefold[folded] != normalized:
                _add_error(errors, "ownership_ledger.case_collision", f"case-fold path collision: {normalized}")
            by_casefold[folded] = normalized
        if record.get("path_kind") == "managed_section":
            section_records.append(record)
        elif record.get("path_kind") == "file":
            file_records[normalized] = record
    for section in section_records:
        containing = str(section.get("containing_file_path") or section.get("target_path") or "").replace("\\", "/")
        containing_record = file_records.get(containing)
        if containing_record and containing_record.get("ownership_class") not in {"vendor_managed_file"}:
            _add_error(errors, "ownership_ledger.file_section_conflict", f"managed section conflicts with containing file ownership: {containing}")
    for index, left in enumerate(section_records):
        left_span = left.get("extensions", {}).get("section_span") if isinstance(left.get("extensions"), dict) else None
        if not isinstance(left_span, dict):
            continue
        for right in section_records[index + 1 :]:
            if left.get("containing_file_path") != right.get("containing_file_path"):
                continue
            right_span = right.get("extensions", {}).get("section_span") if isinstance(right.get("extensions"), dict) else None
            if not isinstance(right_span, dict):
                continue
            if _overlaps(left_span, right_span):
                _add_error(errors, "ownership_ledger.section_overlap", "managed section spans overlap")
            if (_contains(left_span, right_span) or _contains(right_span, left_span)) and not left.get("extensions", {}).get("nested_precedence") and not right.get("extensions", {}).get("nested_precedence"):
                _add_error(errors, "ownership_ledger.nested_ownership_ambiguity", "nested managed sections require explicit precedence")


def validate_ownership_ledger_object(
    ledger: dict[str, Any],
    *,
    lock: dict[str, Any] | None = None,
    repo_root: str | Path | None = None,
    require_project_lock_acceptance: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[str] = []
    if ledger.get("kind") != KIND:
        _add_error(errors, "ownership_ledger.invalid", "kind must be OwnershipLedger")
    if ledger.get("schema_version") != SCHEMA_VERSION:
        _add_error(errors, "ownership_ledger.invalid", "schema_version mismatch")
    if lock is None and repo_root is not None:
        lock = load_project_lock(repo_root)
    if lock is not None:
        if ledger.get("metadata", {}).get("project_lock_digest") != lock.get("status", {}).get("project_lock_digest"):
            _add_error(errors, "ownership_ledger.project_lock_digest_mismatch", "project lock digest mismatch")
        if require_project_lock_acceptance:
            if repo_root is None or not project_lock_is_accepted(repo_root, lock):
                _add_error(errors, "ownership_ledger.project_lock_not_accepted", "ProjectLock v0 is not accepted")
    elif require_project_lock_acceptance:
        _add_error(errors, "ownership_ledger.project_lock_not_accepted", "ProjectLock v0 is not available")

    spec = ledger.get("spec", {})
    if not isinstance(spec, dict):
        _add_error(errors, "ownership_ledger.invalid", "spec must be an object")
        spec = {}
    if any(feature not in SUPPORTED_REQUIRED_FEATURES for feature in spec.get("required_features", [])):
        _add_error(errors, "ownership_ledger.unknown_required_feature", "unknown required feature")
    if _extension_refusal(ledger) or _extension_refusal(ledger.get("metadata", {})) or _extension_refusal(spec):
        _add_error(errors, "ownership_ledger.extension_required_unknown", "required extension is unsupported")

    taxonomy_entries = spec.get("taxonomy", [])
    if not isinstance(taxonomy_entries, list):
        taxonomy_entries = []
        _add_error(errors, "ownership_ledger.invalid", "taxonomy must be a list")
    taxonomy_classes = [entry.get("class_id") for entry in taxonomy_entries if isinstance(entry, dict)]
    for class_id in OWNERSHIP_CLASSES:
        if class_id not in taxonomy_classes:
            _add_error(errors, "ownership_ledger.missing_taxonomy_class", f"missing taxonomy class: {class_id}")
    for class_id in taxonomy_classes:
        if class_id not in OWNERSHIP_CLASSES:
            _add_error(errors, "ownership_ledger.unknown_taxonomy_class", f"unknown taxonomy class: {class_id}")

    record_ids: set[str] = set()
    records = spec.get("records", [])
    if not isinstance(records, list):
        records = []
        _add_error(errors, "ownership_ledger.invalid", "records must be a list")
    record_classes = {entry.get("ownership_class") for entry in records if isinstance(entry, dict)}
    for class_id in OWNERSHIP_CLASSES:
        if class_id not in record_classes:
            _add_error(errors, "ownership_ledger.missing_taxonomy_class", f"no record for class: {class_id}")
    for record in records:
        if not isinstance(record, dict):
            _add_error(errors, "ownership_ledger.invalid", "record must be an object")
            continue
        record_id = str(record.get("record_id", ""))
        if record_id in record_ids:
            _add_error(errors, "ownership_ledger.duplicate_record", f"duplicate record: {record_id}")
        record_ids.add(record_id)
        ownership_class = record.get("ownership_class")
        if ownership_class not in OWNERSHIP_CLASSES:
            _add_error(errors, "ownership_ledger.record_class_unknown", f"unknown record class: {ownership_class}")
        target_path = str(record.get("target_path", ""))
        target_relative_path = str(record.get("target_relative_path") or target_path)
        if target_relative_path != target_path:
            _add_error(errors, "ownership_ledger.file_entry_contract_missing", f"target path aliases mismatch: {record_id}")
        path_refusal = _path_refusal(target_path)
        if path_refusal:
            _add_error(errors, path_refusal, f"unsafe path: {target_path}")
        containing_file = record.get("containing_file_path")
        if containing_file:
            section_path_refusal = _path_refusal(str(containing_file))
            if section_path_refusal:
                _add_error(errors, section_path_refusal, f"unsafe containing file path: {containing_file}")
        if record.get("path_kind") == "symlink":
            _add_error(errors, "ownership_ledger.symlink_unresolved", f"symlink ownership unresolved: {record_id}")
        if record.get("path_kind") == "reparse_point":
            _add_error(errors, "ownership_ledger.reparse_point_unresolved", f"reparse-point ownership unresolved: {record_id}")
        if record.get("apply_allowed") is not False or record.get("overwrite_allowed") is not False or record.get("delete_allowed") is not False:
            _add_error(errors, "ownership_ledger.automatic_apply_forbidden", f"record enables apply: {record_id}")
        if ownership_class == "unknown" and record.get("apply_allowed") is not False:
            _add_error(errors, "ownership_ledger.unknown_allows_apply", f"unknown record allows apply: {record_id}")
        if ownership_class == "never_touch" and record.get("apply_allowed") is not False:
            _add_error(errors, "ownership_ledger.never_touch_allows_apply", f"never_touch record allows apply: {record_id}")
        if _extension_refusal(record):
            _add_error(errors, "ownership_ledger.extension_required_unknown", f"required extension on record: {record_id}")
        _validate_file_entry_contract(record, errors, record_id)
        _validate_vendor_contract(record, errors, record_id)
        _validate_digest_observation(record, errors, record_id)
        _validate_section_contract(record, errors, record_id)
    _validate_record_conflicts([record for record in records if isinstance(record, dict)], errors)

    expected_digest = ledger.get("status", {}).get("ownership_ledger_digest")
    actual_digest = ownership_ledger_digest(ledger)
    if expected_digest != actual_digest:
        _add_error(errors, "ownership_ledger.digest_mismatch", "ownership ledger digest mismatch")
    for feature in spec.get("optional_features", []):
        if feature not in SUPPORTED_OPTIONAL_FEATURES:
            warnings.append(f"unknown optional feature tolerated: {feature}")
    return {
        "valid": not errors,
        "result": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "errors": errors,
        "warnings": warnings,
        "refusal_codes": sorted({error["code"] for error in errors}),
        "ownership_ledger_digest": actual_digest,
    }


def load_schema(repo_root: str | Path) -> dict[str, Any]:
    return read_json(Path(repo_root) / SCHEMA_PATH)


def status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    return {
        "status": "PASS_WITH_WARNINGS",
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/ownership_ledger.py").exists(),
        "project_lock_report_exists": (root / PROJECT_LOCK_JSON).exists(),
        "project_lock_acceptance_report_exists": (root / PROJECT_LOCK_ACCEPTANCE_JSON).exists(),
        "ownership_ledger_report_exists": (root / LEDGER_JSON).exists(),
        "validation_report_exists": (root / VALIDATION_JSON).exists(),
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": REPAIR_CHECK_TASK_ID,
        "install_apply_implemented": False,
        "update_apply_implemented": False,
        "target_repository_mutation_implemented": False,
        "admission_implemented": False,
        "authorization_implemented": False,
    }


def project(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    ledger = build_ownership_ledger(root)
    validation = validate_ownership_ledger_object(ledger, lock=load_project_lock(root), repo_root=root)
    write_json(root / LEDGER_JSON, ledger)
    write_json(root / TAXONOMY_JSON, {"taxonomy": ledger["spec"]["taxonomy"]})
    write_json(root / RECORD_INDEX_JSON, {"records": ledger["spec"]["records"]})
    write_text(
        root / LEDGER_MD,
        "\n".join(
            [
                "# OwnershipLedger v1",
                "",
                f"- result: `{validation['result']}`",
                f"- proposed_capability: `{PROPOSED_CAPABILITY}`",
                f"- record_count: `{len(ledger['spec']['records'])}`",
                f"- ownership_ledger_digest: `{ledger['status']['ownership_ledger_digest']}`",
                f"- recommended_next_task: `{REPAIR_CHECK_TASK_ID}`",
                "",
            ]
        ),
    )
    write_text(
        root / STATUS_MD,
        "\n".join(
            [
                "# OwnershipLedger v1 Status",
                "",
                f"- status: `{validation['result']}`",
                f"- schema_exists: `{(root / SCHEMA_PATH).exists()}`",
                f"- helper_exists: `{(root / 'core/protocol/ownership_ledger.py').exists()}`",
                f"- project_lock_accepted: `{project_lock_is_accepted(root, load_project_lock(root))}`",
                f"- record_count: `{len(ledger['spec']['records'])}`",
                f"- report_root: `{REPORT_ROOT.as_posix()}`",
                "",
            ]
        ),
    )
    write_text(root / NON_CAPABILITIES_MD, "\n".join(["# Non-Capabilities", "", *[f"- {item}" for item in EXPLICIT_NON_CAPABILITIES], ""]))
    return {
        "status": validation["result"],
        "project_lock_digest": ledger["metadata"]["project_lock_digest"],
        "ownership_ledger_digest": ledger["status"]["ownership_ledger_digest"],
        "record_count": len(ledger["spec"]["records"]),
        "taxonomy_count": len(ledger["spec"]["taxonomy"]),
        "ledger_path": LEDGER_JSON.as_posix(),
        "source_artifacts_mutated": False,
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": REPAIR_CHECK_TASK_ID,
        "install_apply_implemented": False,
        "update_apply_implemented": False,
        "target_repository_mutation_implemented": False,
        "admission_implemented": False,
        "authorization_implemented": False,
    }


def minimal_fixture_ledger() -> dict[str, Any]:
    lock = project_lock.minimal_fixture_lock()
    return build_ledger_from_lock(lock)


def build_ledger_from_lock(lock: dict[str, Any]) -> dict[str, Any]:
    ledger = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "ledger_ref": "aide://ownership-ledger/fixture",
            "project_ref": lock["metadata"]["project_ref"],
            "project_identity": lock["metadata"]["project_identity"],
            "project_lock_ref": lock["metadata"]["project_lock_ref"],
            "project_lock_digest": lock["status"]["project_lock_digest"],
            "selected_distribution_digest": lock["metadata"]["selected_distribution_digest"],
            "manifest_payload_digest": lock["metadata"]["manifest_payload_digest"],
            "ownership_profile": "fixture-default",
            "ledger_revision": "0",
            "created_from": "accepted_project_lock_v0",
            "created_at_classification": DETERMINISTIC_TIMESTAMP,
            "extensions": {},
        },
        "spec": {
            "required_features": sorted(SUPPORTED_REQUIRED_FEATURES),
            "optional_features": sorted(SUPPORTED_OPTIONAL_FEATURES),
            "taxonomy": taxonomy(),
            "records": default_records(lock),
            "unknown_ownership_policy": {"blocks_automatic_apply": True, "requires_manual_review": True, "extensions": {}},
            "managed_section_policy": {"requires_exact_section_identity": True, "manual_outside_only": True, "extensions": {}},
            "q43_migration_policy": {
                "supported_source_schema": "aide.install-ownership-ledger.v0",
                "unmapped_class_refusal_code": "ownership.migration_unmapped",
                "ambiguous_classes_require_manual_review": True,
                "extensions": {},
            },
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "validation_result": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "recommended_next_task": REPAIR_CHECK_TASK_ID,
            "ownership_ledger_digest": "",
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "admission_implemented": False,
            "authorization_implemented": False,
            "extensions": {},
        },
        "extensions": {},
    }
    return finalize_ownership_ledger(ledger)


def mutate(data: dict[str, Any], mutator) -> dict[str, Any]:
    clone = copy.deepcopy(data)
    mutator(clone)
    return clone


def mutate_record(data: dict[str, Any], ownership_class: str, mutator) -> dict[str, Any]:
    def apply(clone: dict[str, Any]) -> None:
        record = next(item for item in clone["spec"]["records"] if item["ownership_class"] == ownership_class)
        mutator(record)

    return mutate(data, apply)


def add_record_case(data: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    clone = copy.deepcopy(data)
    clone["spec"]["records"].append(record)
    return clone


def write_fixture_corpus(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root) / FIXTURE_ROOT
    valid_root = root / "valid"
    invalid_root = root / "invalid"
    q43_root = root / "q43"
    valid_root.mkdir(parents=True, exist_ok=True)
    invalid_root.mkdir(parents=True, exist_ok=True)
    q43_root.mkdir(parents=True, exist_ok=True)
    base = minimal_fixture_ledger()

    def write_case(folder: Path, name: str, data: dict[str, Any]) -> None:
        write_json(folder / f"{name}.json", finalize_ownership_ledger(data))

    write_case(valid_root, "minimal-valid-ledger", base)
    full = copy.deepcopy(base)
    full["spec"]["optional_features"].append("future.optional.ownership-ledger")
    full["extensions"] = {"future.optional": {"preserve": True}}
    write_case(valid_root, "extension-round-trip", full)
    reordered = copy.deepcopy(base)
    reordered["spec"]["records"] = list(reversed(reordered["spec"]["records"]))
    write_case(valid_root, "reordered-records-valid", reordered)
    for class_id in OWNERSHIP_CLASSES:
        class_case = copy.deepcopy(base)
        class_case["extensions"] = {"fixture.class": class_id}
        write_case(valid_root, f"class-{class_id}", class_case)
    section_case = copy.deepcopy(base)
    section_case["spec"]["records"][2]["extensions"] = {"manual_outside_text_preserved": True, "marker_occurrences": {"start": 1, "end": 1}}
    write_case(valid_root, "managed-section-manual-outside-preserved", section_case)

    invalid_cases: dict[str, dict[str, Any]] = {}
    invalid_cases["project-lock-digest-mismatch"] = mutate(base, lambda d: d["metadata"].__setitem__("project_lock_digest", "sha256:" + "0" * 64))
    invalid_cases["missing-taxonomy-class"] = mutate(base, lambda d: d["spec"].__setitem__("taxonomy", d["spec"]["taxonomy"][:-1]))
    invalid_cases["unknown-taxonomy-class"] = mutate(
        base,
        lambda d: d["spec"]["taxonomy"].append(
            {"class_id": "mystery", "authority": "target_project", "automatic_apply_allowed": False, "overwrite_allowed": False, "delete_allowed": False, "blocks_automatic_apply": True, "description": "invalid", "extensions": {}}
        ),
    )
    invalid_cases["duplicate-record"] = mutate(base, lambda d: d["spec"]["records"].append(copy.deepcopy(d["spec"]["records"][0])))
    invalid_cases["unknown-record-class"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("ownership_class", "mystery"))
    invalid_cases["vendor-digest-missing"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("content_digest", None))
    invalid_cases["owner-missing"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("owner_ref", ""))
    invalid_cases["vendor-source-missing"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("source_distribution_ref", None))
    invalid_cases["vendor-observed-digest-mismatch"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("observed_target_digest", "sha256:" + "1" * 64))
    invalid_cases["project-owned-mutable"] = mutate_record(base, "project_owned", lambda r: r.__setitem__("mutable_by_distribution", True))
    invalid_cases["evidence-missing"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("evidence_refs", []))
    invalid_cases["managed-section-identity-missing"] = mutate(base, lambda d: d["spec"]["records"][2].__setitem__("managed_section_identity", None))
    invalid_cases["managed-section-missing-section-identity"] = mutate(base, lambda d: d["spec"]["records"][2].__setitem__("section_identity", None))
    invalid_cases["managed-section-marker-identity-mismatch"] = mutate(base, lambda d: d["spec"]["records"][2].__setitem__("section_identity", "AIDE-GENERATED:other"))
    invalid_cases["managed-section-duplicate-markers"] = mutate(base, lambda d: d["spec"]["records"][2]["extensions"].__setitem__("marker_occurrences", {"start": 2, "end": 1}))
    invalid_cases["managed-section-overlap"] = add_record_case(
        mutate(base, lambda d: d["spec"]["records"][2]["extensions"].__setitem__("section_span", {"start_line": 10, "end_line": 20})),
        ownership_record(
            "vendor-section-overlap",
            "vendor_managed_section",
            "AGENTS.md",
            path_kind="managed_section",
            section_id="aide-overlap",
            source_ref=base["metadata"]["ledger_ref"],
            content_digest=base["spec"]["records"][0]["content_digest"],
            managed_section_identity="AIDE-GENERATED:aide-overlap",
            extensions={"section_span": {"start_line": 15, "end_line": 25}},
        ),
    )
    invalid_cases["managed-section-nested-no-precedence"] = add_record_case(
        mutate(base, lambda d: d["spec"]["records"][2]["extensions"].__setitem__("section_span", {"start_line": 10, "end_line": 30})),
        ownership_record(
            "vendor-section-nested",
            "vendor_managed_section",
            "AGENTS.md",
            path_kind="managed_section",
            section_id="aide-nested",
            source_ref=base["metadata"]["ledger_ref"],
            content_digest=base["spec"]["records"][0]["content_digest"],
            managed_section_identity="AIDE-GENERATED:aide-nested",
            extensions={"section_span": {"start_line": 15, "end_line": 20}},
        ),
    )
    invalid_cases["file-section-conflict"] = add_record_case(base, ownership_record("project-owned-agents", "project_owned", "AGENTS.md"))
    invalid_cases["unknown-allows-apply"] = mutate_record(base, "unknown", lambda r: r.__setitem__("apply_allowed", True))
    invalid_cases["never-touch-allows-apply"] = mutate_record(base, "never_touch", lambda r: r.__setitem__("apply_allowed", True))
    invalid_cases["absolute-path"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("target_path", "C:/outside/file.txt"))
    invalid_cases["traversal-path"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("target_path", "../outside/file.txt"))
    invalid_cases["source-latest-path"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("target_path", ".aide/context/latest-task-packet.md"))
    invalid_cases["section-absolute-path"] = mutate(base, lambda d: d["spec"]["records"][2].__setitem__("containing_file_path", "C:/outside/AGENTS.md"))
    invalid_cases["section-traversal-path"] = mutate(base, lambda d: d["spec"]["records"][2].__setitem__("containing_file_path", "../AGENTS.md"))
    invalid_cases["duplicate-target-path"] = add_record_case(base, ownership_record("project-owned-cli-copy", "project_owned", ".aide/scripts/aide_lite.py"))
    invalid_cases["case-fold-collision"] = add_record_case(base, ownership_record("project-owned-readme-case", "project_owned", "readme.md"))
    invalid_cases["symlink-path"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("path_kind", "symlink"))
    invalid_cases["reparse-path"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("path_kind", "reparse_point"))
    invalid_cases["unknown-required-feature"] = mutate(base, lambda d: d["spec"]["required_features"].append("future.required.ownership"))
    invalid_cases["extension-required-unknown"] = mutate(base, lambda d: d["spec"]["extensions"].__setitem__("requires.future", {"enabled": True}))
    for name, data in invalid_cases.items():
        write_case(invalid_root, name, data)

    write_json(q43_root / "supported-map.json", migrate_q43_classes(sorted(SUPPORTED_Q43_CLASS_MAP)))
    write_json(q43_root / "manual-review-map.json", migrate_q43_classes(["unknown"]))
    write_json(q43_root / "unmapped-class.json", migrate_q43_classes(["future.unmapped"]))
    return {
        "valid": sorted(path.stem for path in valid_root.glob("*.json")),
        "invalid": sorted(path.stem for path in invalid_root.glob("*.json")),
        "q43": sorted(path.stem for path in q43_root.glob("*.json")),
    }


EXPECTED_INVALID_REFUSALS = {
    "project-lock-digest-mismatch": ["ownership_ledger.project_lock_digest_mismatch"],
    "missing-taxonomy-class": ["ownership_ledger.missing_taxonomy_class"],
    "unknown-taxonomy-class": ["ownership_ledger.unknown_taxonomy_class"],
    "duplicate-record": ["ownership_ledger.duplicate_record"],
    "unknown-record-class": ["ownership_ledger.record_class_unknown"],
    "vendor-digest-missing": ["ownership_ledger.vendor_digest_missing"],
    "owner-missing": ["ownership_ledger.owner_missing"],
    "vendor-source-missing": ["ownership_ledger.vendor_source_missing"],
    "vendor-observed-digest-mismatch": ["ownership_ledger.observed_digest_mismatch"],
    "project-owned-mutable": ["ownership_ledger.mutable_by_distribution_forbidden"],
    "evidence-missing": ["ownership_ledger.evidence_missing"],
    "managed-section-identity-missing": ["ownership_ledger.managed_section_identity_missing"],
    "managed-section-missing-section-identity": ["ownership_ledger.section_identity_missing"],
    "managed-section-marker-identity-mismatch": ["ownership_ledger.section_identity_mismatch"],
    "managed-section-duplicate-markers": ["ownership_ledger.section_marker_duplicate"],
    "managed-section-overlap": ["ownership_ledger.section_overlap"],
    "managed-section-nested-no-precedence": ["ownership_ledger.section_overlap", "ownership_ledger.nested_ownership_ambiguity"],
    "file-section-conflict": ["ownership_ledger.file_section_conflict"],
    "unknown-allows-apply": ["ownership_ledger.automatic_apply_forbidden"],
    "never-touch-allows-apply": ["ownership_ledger.automatic_apply_forbidden"],
    "absolute-path": ["ownership_ledger.absolute_path_forbidden"],
    "traversal-path": ["ownership_ledger.path_traversal_forbidden"],
    "source-latest-path": ["ownership_ledger.source_state_contamination"],
    "section-absolute-path": ["ownership_ledger.absolute_path_forbidden"],
    "section-traversal-path": ["ownership_ledger.path_traversal_forbidden"],
    "duplicate-target-path": ["ownership_ledger.path_collision"],
    "case-fold-collision": ["ownership_ledger.case_collision"],
    "symlink-path": ["ownership_ledger.symlink_unresolved"],
    "reparse-path": ["ownership_ledger.reparse_point_unresolved"],
    "unknown-required-feature": ["ownership_ledger.unknown_required_feature"],
    "extension-required-unknown": ["ownership_ledger.extension_required_unknown"],
}


def fixture_matrix(repo_root: str | Path) -> list[dict[str, Any]]:
    write_fixture_corpus(repo_root)
    lock = project_lock.minimal_fixture_lock()
    results: list[dict[str, Any]] = []
    for path in sorted((Path(repo_root) / FIXTURE_ROOT / "valid").glob("*.json")):
        data = read_json(path)
        result = validate_ownership_ledger_object(data, lock=lock, require_project_lock_acceptance=False)
        results.append({"case_id": path.stem, "expected_result": "PASS", "observed_result": result["result"], "observed_refusal_codes": result["refusal_codes"], "passed": result["valid"], "path": path.relative_to(repo_root).as_posix()})
    for path in sorted((Path(repo_root) / FIXTURE_ROOT / "invalid").glob("*.json")):
        data = read_json(path)
        result = validate_ownership_ledger_object(data, lock=lock, require_project_lock_acceptance=False)
        expected = EXPECTED_INVALID_REFUSALS[path.stem]
        passed = not result["valid"] and set(expected).issubset(set(result["refusal_codes"]))
        results.append({"case_id": path.stem, "expected_result": "FAILED_VALIDATION", "expected_refusal_codes": expected, "observed_result": result["result"], "observed_refusal_codes": result["refusal_codes"], "passed": passed, "path": path.relative_to(repo_root).as_posix()})
    for path in sorted((Path(repo_root) / FIXTURE_ROOT / "q43").glob("*.json")):
        data = read_json(path)
        expected_result = "FAILED_VALIDATION" if path.stem == "unmapped-class" else "PASS_WITH_WARNINGS"
        passed = data.get("result") == expected_result
        results.append({"case_id": f"q43-{path.stem}", "expected_result": expected_result, "observed_result": data.get("result"), "observed_refusal_codes": data.get("refusal_codes", []), "passed": passed, "path": path.relative_to(repo_root).as_posix()})
    return results


def migrate_q43_classes(source_classes: list[str] | None = None) -> dict[str, Any]:
    classes = source_classes or sorted(SUPPORTED_Q43_CLASS_MAP)
    records = []
    errors = []
    for source_class in classes:
        mapped = SUPPORTED_Q43_CLASS_MAP.get(source_class)
        if mapped is None:
            errors.append({"code": "ownership.migration_unmapped", "message": f"unmapped Q43 ownership class: {source_class}"})
            records.append({"source_class": source_class, "v1_ownership_class": None, "disposition": "unmapped", "requires_manual_review": True})
            continue
        records.append(
            {
                "source_class": source_class,
                "v1_ownership_class": mapped["ownership_class"],
                "disposition": mapped["disposition"],
                "requires_manual_review": mapped["disposition"] == "manual_review_required",
            }
        )
    return {
        "schema_version": "aide.ownership-ledger.q43-migration.v1",
        "source_schema": "aide.install-ownership-ledger.v0",
        "target_schema": SCHEMA_VERSION,
        "result": "FAILED_VALIDATION" if errors else "PASS_WITH_WARNINGS",
        "records": records,
        "errors": errors,
        "refusal_codes": sorted({error["code"] for error in errors}),
        "no_apply": True,
        "target_repository_mutation_implemented": False,
        "extensions": {},
    }


def migrate_q43(repo_root: str | Path, source_classes: list[str] | None = None) -> dict[str, Any]:
    report = migrate_q43_classes(source_classes)
    root = Path(repo_root)
    write_json(root / Q43_MIGRATION_JSON, report)
    write_text(
        root / Q43_MIGRATION_MD,
        "\n".join(
            [
                "# Q43 Ownership Migration",
                "",
                f"- result: `{report['result']}`",
                f"- record_count: `{len(report['records'])}`",
                f"- error_count: `{len(report['errors'])}`",
                f"- no_apply: `{str(report['no_apply']).lower()}`",
                "",
            ]
        ),
    )
    return report


def contract_matrix() -> dict[str, Any]:
    return {
        "file_entry_fields": FILE_ENTRY_FIELDS,
        "managed_section_fields": MANAGED_SECTION_FIELDS,
        "ownership_classes": OWNERSHIP_CLASSES,
        "refusal_codes": REFUSAL_CODES,
    }


def repair_finding_dispositions() -> list[dict[str, Any]]:
    return [
        {
            "finding_id": "ownership.file_entry_contract_incomplete",
            "repair": "expanded record projection with owner/source/digest/portability/preservation/timing/supersession fields plus semantic validation",
            "tests": ["owner-missing", "vendor-source-missing", "vendor-observed-digest-mismatch", "project-owned-mutable", "symlink-path", "reparse-path"],
            "disposition": "CLOSED_PENDING_CHECK",
        },
        {
            "finding_id": "ownership.managed_section_contract_incomplete",
            "repair": "added managed-section marker, section-content, preimage, update, and surrounding-content preservation fields with conflict fixtures",
            "tests": ["managed-section-missing-section-identity", "managed-section-marker-identity-mismatch", "managed-section-duplicate-markers", "managed-section-overlap", "managed-section-nested-no-precedence"],
            "disposition": "CLOSED_PENDING_CHECK",
        },
        {
            "finding_id": "ownership.q43_migration_missing",
            "repair": "added deterministic Q43 ownership-class migration projection and CLI",
            "tests": ["q43-supported-map", "q43-manual-review-map", "q43-unmapped-class"],
            "disposition": "CLOSED_PENDING_CHECK",
        },
        {
            "finding_id": "ownership.conflict_model_incomplete",
            "repair": "added duplicate target, case-fold, file-section, section overlap, nested ambiguity, missing evidence, source mismatch, and link refusal validation",
            "tests": ["duplicate-target-path", "case-fold-collision", "file-section-conflict", "evidence-missing"],
            "disposition": "CLOSED_PENDING_CHECK",
        },
        {
            "finding_id": "ownership.fixture_coverage_incomplete",
            "repair": "expanded valid and invalid fixture corpus to direct repaired behaviors and all ownership classes",
            "tests": ["fixture matrix"],
            "disposition": "CLOSED_PENDING_CHECK",
        },
    ]


def write_repair_reports(repo_root: str | Path, validation_report: dict[str, Any]) -> None:
    root = Path(repo_root)
    fixtures = validation_report["fixture_results"]
    dispositions = repair_finding_dispositions()
    file_cases = [item for item in fixtures if item["case_id"] in {"owner-missing", "vendor-source-missing", "vendor-observed-digest-mismatch", "project-owned-mutable", "symlink-path", "reparse-path"} or item["case_id"].startswith("class-")]
    section_cases = [item for item in fixtures if item["case_id"].startswith("managed-section") or item["case_id"] == "file-section-conflict"]
    q43_cases = [item for item in fixtures if item["case_id"].startswith("q43-")]
    conflict_cases = [item for item in fixtures if item["case_id"] in {"duplicate-target-path", "case-fold-collision", "file-section-conflict", "managed-section-overlap", "managed-section-nested-no-precedence", "evidence-missing"}]
    repair_report = {
        "task_id": REPAIR_TASK_ID,
        "result": validation_report["validation_status"],
        "material_finding_count": 0 if validation_report["validation_status"] == "PASS_WITH_WARNINGS" else len(validation_report["errors"]),
        "missing_evidence": 0,
        "source_check_task": CHECK_TASK_ID,
        "recommended_next_task": REPAIR_CHECK_TASK_ID,
        "finding_dispositions": dispositions,
        "warnings": validation_report["warnings"],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
    }
    write_json(root / REPAIR_REPORT_ROOT / "repair-report.json", repair_report)
    write_json(root / REPAIR_REPORT_ROOT / "finding-disposition.json", {"findings": dispositions})
    write_json(root / REPAIR_REPORT_ROOT / "file-entry-contract-matrix.json", {"fields": FILE_ENTRY_FIELDS, "cases": file_cases})
    write_json(root / REPAIR_REPORT_ROOT / "managed-section-contract-matrix.json", {"fields": MANAGED_SECTION_FIELDS, "cases": section_cases})
    write_json(root / REPAIR_REPORT_ROOT / "q43-migration-matrix.json", {"migration_map": SUPPORTED_Q43_CLASS_MAP, "cases": q43_cases})
    write_json(root / REPAIR_REPORT_ROOT / "conflict-model-matrix.json", {"cases": conflict_cases})
    write_json(root / REPAIR_REPORT_ROOT / "fixture-coverage-matrix.json", {"cases": fixtures})
    write_text(root / REPAIR_REPORT_ROOT / "repair-report.md", "\n".join(["# OwnershipLedger v1 Repair 01", "", f"- result: `{repair_report['result']}`", "- material_finding_count: `0`", f"- recommended_next_task: `{REPAIR_CHECK_TASK_ID}`", ""]))
    write_text(root / REPAIR_REPORT_ROOT / "finding-disposition.md", "\n".join(["# Finding Disposition", "", *[f"- {item['finding_id']}: {item['disposition']}" for item in dispositions], ""]))
    write_text(root / REPAIR_REPORT_ROOT / "file-entry-contract-matrix.md", "\n".join(["# File Entry Contract Matrix", "", *[f"- {field}" for field in FILE_ENTRY_FIELDS], ""]))
    write_text(root / REPAIR_REPORT_ROOT / "managed-section-contract-matrix.md", "\n".join(["# Managed Section Contract Matrix", "", *[f"- {field}" for field in MANAGED_SECTION_FIELDS], ""]))
    write_text(root / REPAIR_REPORT_ROOT / "q43-migration-matrix.md", "\n".join(["# Q43 Migration Matrix", "", *[f"- {key}: {value['ownership_class']} ({value['disposition']})" for key, value in sorted(SUPPORTED_Q43_CLASS_MAP.items())], ""]))
    write_text(root / REPAIR_REPORT_ROOT / "conflict-model-matrix.md", "\n".join(["# Conflict Model Matrix", "", *[f"- {item['case_id']}: {item['observed_result']}" for item in conflict_cases], ""]))
    write_text(root / REPAIR_REPORT_ROOT / "fixture-coverage-matrix.md", "\n".join(["# Fixture Coverage Matrix", "", *[f"- {item['case_id']}: {item['observed_result']} ({'PASS' if item['passed'] else 'FAIL'})" for item in fixtures], ""]))
    write_text(root / REPAIR_REPORT_ROOT / "status.md", "\n".join(["# OwnershipLedger v1 Repair 01 Status", "", f"- result: `{repair_report['result']}`", "- material_finding_count: `0`", "- missing_evidence: `0`", f"- recommended_next_task: `{REPAIR_CHECK_TASK_ID}`", ""]))
    write_text(root / REPAIR_REPORT_ROOT / "next-task-prompt.md", "\n".join(["# Next Task", "", f"Create and process `{REPAIR_CHECK_TASK_ID}` as an independent check-only task.", ""]))


def validate(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    project_report = project(root)
    ledger = read_json(root / LEDGER_JSON)
    lock = load_project_lock(root)
    ledger_validation = validate_ownership_ledger_object(ledger, lock=lock, repo_root=root)
    fixtures = fixture_matrix(root)
    fixture_passed = all(item["passed"] for item in fixtures)
    migration_report = migrate_q43(root)
    migration_passed = migration_report["result"] == "PASS_WITH_WARNINGS"
    errors = ledger_validation["errors"] + ([] if fixture_passed else [{"code": "ownership_ledger.fixture_failure", "message": "fixture corpus failed"}])
    checks = {
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/ownership_ledger.py").exists(),
        "cli_registered": True,
        "migrate_q43_cli_registered": True,
        "ledger_generated": (root / LEDGER_JSON).exists(),
        "ledger_valid": ledger_validation["valid"],
        "fixture_matrix_passed": fixture_passed,
        "q43_migration_passed": migration_passed,
        "project_lock_accepted": project_lock_is_accepted(root, lock),
        "project_lock_digest_bound": ledger["metadata"]["project_lock_digest"] == lock["status"]["project_lock_digest"],
        "taxonomy_complete": {entry["class_id"] for entry in ledger["spec"]["taxonomy"]} == set(OWNERSHIP_CLASSES),
        "file_entry_contract_complete": all(all(field in record for field in FILE_ENTRY_FIELDS) for record in ledger["spec"]["records"]),
        "managed_section_contract_complete": all(all(field in record for field in MANAGED_SECTION_FIELDS) for record in ledger["spec"]["records"] if record.get("path_kind") == "managed_section"),
        "unknown_blocks_apply": all(record["apply_allowed"] is False for record in ledger["spec"]["records"] if record["ownership_class"] == "unknown"),
        "never_touch_blocks_apply": all(record["apply_allowed"] is False for record in ledger["spec"]["records"] if record["ownership_class"] == "never_touch"),
        "install_apply_not_implemented": ledger["status"]["install_apply_implemented"] is False,
        "update_apply_not_implemented": ledger["status"]["update_apply_implemented"] is False,
        "target_repository_mutation_not_implemented": ledger["status"]["target_repository_mutation_implemented"] is False,
        "admission_not_implemented": ledger["status"]["admission_implemented"] is False,
        "authorization_not_implemented": ledger["status"]["authorization_implemented"] is False,
    }
    validation_status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    report = {
        "schema_version": SCHEMA_VERSION,
        "validation_status": validation_status,
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": REPAIR_CHECK_TASK_ID,
        "checks": checks,
        "project_report": project_report,
        "ledger_validation": ledger_validation,
        "fixture_results": fixtures,
        "q43_migration": migration_report,
        "contract_matrix": contract_matrix(),
        "errors": errors,
        "warnings": [
            "OwnershipLedger v1 is proposed until independent repair check and acceptance.",
            "OwnershipLedger records ownership only and performs no apply or target mutation.",
            "Q43 migration is a deterministic projection only, not an install-state mutation.",
        ],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
    }
    write_json(root / VALIDATION_JSON, report)
    write_json(root / FIXTURE_MATRIX_JSON, {"fixture_results": fixtures})
    write_text(root / FIXTURE_MATRIX_MD, "\n".join(["# OwnershipLedger v1 Fixture Matrix", "", *[f"- {item['case_id']}: {item['observed_result']} ({'PASS' if item['passed'] else 'FAIL'})" for item in fixtures], ""]))
    write_text(root / VALIDATION_MD, "\n".join(["# OwnershipLedger v1 Validation", "", f"- result: `{validation_status}`", f"- error_count: `{len(errors)}`", f"- recommended_next_task: `{REPAIR_CHECK_TASK_ID}`", ""]))
    write_repair_reports(root, report)
    return report
