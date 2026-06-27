"""InstallRecord v0 helpers.

InstallRecord records observed or completed AIDE distribution installation
state. It is not an installer, update engine, migration applier, rollback
applier, uninstall applier, target scanner, or mutation authority.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import distribution_manifest, envelope, ownership_ledger, project_lock


API_VERSION = envelope.API_VERSION
KIND = "InstallRecord"
SCHEMA_VERSION = "aide.install-record.v0"
PROTOCOL_VERSION = "0.1.0"
TASK_ID = "AIDE-BUILD-INSTALL-RECORD-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-INSTALL-RECORD-V0-01"
PROPOSED_CAPABILITY = "install_record_v0"
DETERMINISTIC_TIMESTAMP = "fixture-timestamp:install-record-v0"
DEFAULT_EVIDENCE_REF = "aide://evidence/install-record-v0/source-projection"

REPORT_ROOT = Path(".aide/reports/install-record-v0")
SCHEMA_PATH = Path(".aide/protocol/aide-install-record-v0.schema.json")
FIXTURE_ROOT = Path(".aide/fixtures/install-record-v0")

INSTALL_RECORD_JSON = REPORT_ROOT / "install-record.json"
INSTALL_RECORD_MD = REPORT_ROOT / "install-record.md"
STATUS_MD = REPORT_ROOT / "status.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FIXTURE_MATRIX_JSON = REPORT_ROOT / "fixture-matrix.json"
FIXTURE_MATRIX_MD = REPORT_ROOT / "fixture-matrix.md"
COMPONENT_BINDING_JSON = REPORT_ROOT / "component-binding.json"
OWNERSHIP_ENTRY_BINDING_JSON = REPORT_ROOT / "ownership-entry-binding.json"
NON_CAPABILITIES_MD = REPORT_ROOT / "non-capabilities.md"

OWNERSHIP_LEDGER_JSON = ownership_ledger.LEDGER_JSON
OWNERSHIP_LEDGER_ACCEPTANCE_JSON = Path(".aide/reports/ownership-ledger-v1-acceptance/acceptance-report.json")

SUPPORTED_REQUIRED_FEATURES = {
    "install_record_v0",
    "distribution_manifest_v1",
    "project_lock_v0",
    "ownership_ledger_v1",
    "sha256_digest_canonical_json_v1",
}

SUPPORTED_OPTIONAL_FEATURES = {
    "partial_observation_warning_v0",
    "install_mode_observed_existing_v0",
}

SUPPORTED_INSTALL_MODES = {
    "observed_fresh_no_apply",
    "observed_existing_no_apply",
    "metadata_only_no_apply",
}

SUPPORTED_INSTALL_SOURCES = {
    "accepted_distribution_manifest",
    "accepted_project_lock",
    "accepted_ownership_ledger",
    "fixture_projection",
}

REFUSAL_CODES = [
    "install_record.missing",
    "install_record.invalid",
    "install_record.distribution_missing",
    "install_record.project_lock_missing",
    "install_record.ownership_ledger_missing",
    "install_record.distribution_mismatch",
    "install_record.project_lock_mismatch",
    "install_record.ownership_ledger_mismatch",
    "install_record.component_ref_unknown",
    "install_record.ownership_entry_ref_unknown",
    "install_record.managed_section_ref_unknown",
    "install_record.apply_authority_claimed",
    "install_record.target_mutation_claimed",
    "install_record.unknown_required_feature",
    "install_record.extension_required_unknown",
    "install_record.absolute_path_forbidden",
    "install_record.path_traversal_forbidden",
    "install_record.source_state_contamination",
    "install_record.source_output_as_target_truth",
    "install_record.evidence_missing",
    "install_record.digest_mismatch",
    "install_record.fixture_failure",
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


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def load_distribution_manifest(repo_root: str | Path) -> dict[str, Any]:
    return project_lock.load_distribution_manifest(repo_root)


def load_project_lock(repo_root: str | Path) -> dict[str, Any]:
    return ownership_ledger.load_project_lock(repo_root)


def load_ownership_ledger(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / OWNERSHIP_LEDGER_JSON
    if path.exists():
        return read_json(path)
    return ownership_ledger.build_ownership_ledger(repo_root)


def load_ownership_ledger_acceptance(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / OWNERSHIP_LEDGER_ACCEPTANCE_JSON
    if not path.exists():
        return {}
    return read_json(path)


def ownership_ledger_is_accepted(repo_root: str | Path) -> bool:
    acceptance = load_ownership_ledger_acceptance(repo_root)
    return (
        acceptance.get("result") in {"ACCEPTED", "ACCEPTED_WITH_WARNINGS"}
        and acceptance.get("accepted_capability") == "ownership_ledger_v1"
        and acceptance.get("material_finding_count") == 0
        and acceptance.get("missing_evidence") == 0
    )


def component_refs(lock: dict[str, Any]) -> list[str]:
    components = lock.get("spec", {}).get("selected_components", [])
    return sorted(str(component.get("component_ref")) for component in components if isinstance(component, dict) and component.get("component_ref"))


def ledger_file_entry_refs(ledger: dict[str, Any]) -> list[str]:
    return sorted(
        str(record.get("entry_ref"))
        for record in ledger.get("spec", {}).get("records", [])
        if isinstance(record, dict) and record.get("path_kind") != "managed_section" and record.get("entry_ref")
    )


def ledger_managed_section_refs(ledger: dict[str, Any]) -> list[str]:
    return sorted(
        str(record.get("entry_ref"))
        for record in ledger.get("spec", {}).get("records", [])
        if isinstance(record, dict) and record.get("path_kind") == "managed_section" and record.get("entry_ref")
    )


def observed_paths_from_ledger(ledger: dict[str, Any]) -> list[str]:
    paths = []
    for record in ledger.get("spec", {}).get("records", []):
        if not isinstance(record, dict):
            continue
        path = record.get("target_relative_path") or record.get("target_path")
        if isinstance(path, str):
            paths.append(path)
    return sorted(set(paths))


def build_install_record(repo_root: str | Path) -> dict[str, Any]:
    manifest = load_distribution_manifest(repo_root)
    lock = load_project_lock(repo_root)
    ledger = load_ownership_ledger(repo_root)
    record = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "install_record_ref": "aide://install-record/aide-self-install-record-v0",
            "target_project_ref": lock["metadata"]["project_ref"],
            "target_project_identity": lock["metadata"]["project_identity"],
            "source_distribution_ref": manifest["metadata"]["distribution_ref"],
            "source_distribution_digest": manifest["status"]["distribution_digest"],
            "project_lock_ref": lock["metadata"]["project_lock_ref"],
            "project_lock_digest": lock["status"]["project_lock_digest"],
            "ownership_ledger_ref": ledger["metadata"]["ledger_ref"],
            "ownership_ledger_digest": ledger["status"]["ownership_ledger_digest"],
            "created_at": DETERMINISTIC_TIMESTAMP,
            "created_by": "aide-self-hosting-fixture",
            "created_from": "accepted_distribution_manifest_project_lock_ownership_ledger",
            "prior_install_record_ref": None,
            "superseded_by_ref": None,
            "extensions": {},
        },
        "spec": {
            "install_mode": "metadata_only_no_apply",
            "install_source": "accepted_ownership_ledger",
            "observed_existing_state": {
                "state_kind": "source_projection_only_no_target_scan",
                "observed_paths": observed_paths_from_ledger(ledger),
                "source_output_used_as_target_truth": False,
                "target_repository_mutation_performed": False,
                "extensions": {},
            },
            "installed_component_refs": component_refs(lock),
            "installed_file_entry_refs": ledger_file_entry_refs(ledger),
            "installed_managed_section_refs": ledger_managed_section_refs(ledger),
            "validation_refs": [
                "aide://validation/distribution-manifest-v1",
                "aide://validation/project-lock-v0",
                "aide://validation/ownership-ledger-v1",
            ],
            "evidence_refs": [DEFAULT_EVIDENCE_REF],
            "warnings": [
                "InstallRecord v0 records install state metadata only and performs no install apply.",
                "Observed paths come from accepted OwnershipLedger projection, not a target scan authority.",
            ],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "required_features": [
                "install_record_v0",
                "distribution_manifest_v1",
                "project_lock_v0",
                "ownership_ledger_v1",
                "sha256_digest_canonical_json_v1",
            ],
            "optional_features": [
                "partial_observation_warning_v0",
                "install_mode_observed_existing_v0",
            ],
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "validation_result": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "recommended_next_task": CHECK_TASK_ID,
            "install_record_digest": "",
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "migration_apply_implemented": False,
            "rollback_apply_implemented": False,
            "uninstall_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "target_scan_authority_implemented": False,
            "release_publication_implemented": False,
            "extensions": {},
        },
        "extensions": {},
    }
    return finalize_install_record(record)


def canonicalize_install_record(record: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(record)
    spec = data.get("spec")
    if isinstance(spec, dict):
        for key in [
            "installed_component_refs",
            "installed_file_entry_refs",
            "installed_managed_section_refs",
            "validation_refs",
            "evidence_refs",
            "warnings",
            "explicit_non_capabilities",
            "required_features",
            "optional_features",
        ]:
            if isinstance(spec.get(key), list):
                spec[key] = sorted(spec[key], key=lambda item: json.dumps(item, sort_keys=True))
        observed = spec.get("observed_existing_state")
        if isinstance(observed, dict) and isinstance(observed.get("observed_paths"), list):
            observed["observed_paths"] = sorted(str(item) for item in observed["observed_paths"])
    return data


def install_record_payload_for_digest(record: dict[str, Any]) -> dict[str, Any]:
    data = canonicalize_install_record(record)
    status = data.get("status")
    if isinstance(status, dict):
        status.pop("install_record_digest", None)
    return data


def install_record_digest(record: dict[str, Any]) -> str:
    return sha256_digest(canonical_json_bytes(install_record_payload_for_digest(record)))


def finalize_install_record(record: dict[str, Any]) -> dict[str, Any]:
    data = canonicalize_install_record(record)
    data.setdefault("status", {})["install_record_digest"] = install_record_digest(data)
    return data


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


def _path_refusal_code(value: str) -> str | None:
    if value.startswith("aide://"):
        return None
    normalized = value.replace("\\", "/")
    if SOURCE_OUTPUT_RE.search(normalized):
        return "install_record.source_state_contamination"
    if PATH_RE.search(normalized):
        if ".." in [part for part in normalized.split("/") if part]:
            return "install_record.path_traversal_forbidden"
        return "install_record.absolute_path_forbidden"
    if normalized.startswith(".aide/reports/latest-"):
        return "install_record.source_state_contamination"
    return None


def _iter_string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
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


def _boolean_claims_authority(data: Any, errors: list[dict[str, str]]) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            key_text = str(key)
            if value is True and ("apply" in key_text or "install_authority" in key_text):
                _add_error(errors, "install_record.apply_authority_claimed", f"apply authority claimed by {key_text}")
            if value is True and ("mutation" in key_text or "mutate" in key_text):
                _add_error(errors, "install_record.target_mutation_claimed", f"target mutation claimed by {key_text}")
            _boolean_claims_authority(value, errors)
    elif isinstance(data, list):
        for item in data:
            _boolean_claims_authority(item, errors)


def validate_install_record_object(
    record: dict[str, Any] | None,
    *,
    distribution: dict[str, Any] | None = None,
    lock: dict[str, Any] | None = None,
    ledger: dict[str, Any] | None = None,
    repo_root: str | Path | None = None,
    require_ownership_acceptance: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[str] = []
    if record is None:
        _add_error(errors, "install_record.missing", "InstallRecord is missing")
        return _validation_result(errors, warnings)
    if not isinstance(record, dict):
        _add_error(errors, "install_record.invalid", "InstallRecord root must be an object")
        return _validation_result(errors, warnings)
    for field in ["apiVersion", "kind", "schema_version", "metadata", "spec", "status", "extensions"]:
        if field not in record:
            _add_error(errors, "install_record.invalid", f"missing required field: {field}")
    if record.get("kind") != KIND:
        _add_error(errors, "install_record.invalid", "kind must be InstallRecord")
    if record.get("schema_version") != SCHEMA_VERSION:
        _add_error(errors, "install_record.invalid", f"schema_version must be {SCHEMA_VERSION}")
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    spec = record.get("spec") if isinstance(record.get("spec"), dict) else {}
    status = record.get("status") if isinstance(record.get("status"), dict) else {}
    manifest = distribution if distribution is not None else load_distribution_manifest(repo_root or Path("."))
    project_lock_data = lock if lock is not None else load_project_lock(repo_root or Path("."))
    ownership_data = ledger if ledger is not None else load_ownership_ledger(repo_root or Path("."))
    if not metadata.get("source_distribution_ref"):
        _add_error(errors, "install_record.distribution_missing", "source_distribution_ref is required")
    if not metadata.get("project_lock_ref"):
        _add_error(errors, "install_record.project_lock_missing", "project_lock_ref is required")
    if not metadata.get("ownership_ledger_ref"):
        _add_error(errors, "install_record.ownership_ledger_missing", "ownership_ledger_ref is required")
    if metadata.get("source_distribution_ref") != manifest.get("metadata", {}).get("distribution_ref"):
        _add_error(errors, "install_record.distribution_mismatch", "source_distribution_ref does not match DistributionManifest")
    if metadata.get("source_distribution_digest") != manifest.get("status", {}).get("distribution_digest"):
        _add_error(errors, "install_record.distribution_mismatch", "source_distribution_digest does not match DistributionManifest")
    if metadata.get("project_lock_ref") != project_lock_data.get("metadata", {}).get("project_lock_ref"):
        _add_error(errors, "install_record.project_lock_mismatch", "project_lock_ref does not match ProjectLock")
    if metadata.get("project_lock_digest") != project_lock_data.get("status", {}).get("project_lock_digest"):
        _add_error(errors, "install_record.project_lock_mismatch", "project_lock_digest does not match ProjectLock")
    if metadata.get("ownership_ledger_ref") != ownership_data.get("metadata", {}).get("ledger_ref"):
        _add_error(errors, "install_record.ownership_ledger_mismatch", "ownership_ledger_ref does not match OwnershipLedger")
    if metadata.get("ownership_ledger_digest") != ownership_data.get("status", {}).get("ownership_ledger_digest"):
        _add_error(errors, "install_record.ownership_ledger_mismatch", "ownership_ledger_digest does not match OwnershipLedger")
    if require_ownership_acceptance and (repo_root is None or not ownership_ledger_is_accepted(repo_root)):
        _add_error(errors, "install_record.ownership_ledger_mismatch", "OwnershipLedger v1 is not accepted")
    if spec.get("install_mode") not in SUPPORTED_INSTALL_MODES:
        _add_error(errors, "install_record.invalid", "unsupported install_mode")
    if spec.get("install_source") not in SUPPORTED_INSTALL_SOURCES:
        _add_error(errors, "install_record.invalid", "unsupported install_source")
    known_components = set(component_refs(project_lock_data))
    for ref in spec.get("installed_component_refs", []) if isinstance(spec.get("installed_component_refs"), list) else []:
        if ref not in known_components:
            _add_error(errors, "install_record.component_ref_unknown", f"component ref is not selected by ProjectLock: {ref}")
    known_file_entries = set(ledger_file_entry_refs(ownership_data))
    for ref in spec.get("installed_file_entry_refs", []) if isinstance(spec.get("installed_file_entry_refs"), list) else []:
        if ref not in known_file_entries:
            _add_error(errors, "install_record.ownership_entry_ref_unknown", f"file entry ref is not in OwnershipLedger: {ref}")
    known_sections = set(ledger_managed_section_refs(ownership_data))
    for ref in spec.get("installed_managed_section_refs", []) if isinstance(spec.get("installed_managed_section_refs"), list) else []:
        if ref not in known_sections:
            _add_error(errors, "install_record.managed_section_ref_unknown", f"managed section ref is not in OwnershipLedger: {ref}")
    if not spec.get("evidence_refs"):
        _add_error(errors, "install_record.evidence_missing", "evidence_refs must not be empty")
    for feature in spec.get("required_features", []) if isinstance(spec.get("required_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES:
            _add_error(errors, "install_record.unknown_required_feature", f"unknown required feature: {feature}")
    for feature in spec.get("optional_features", []) if isinstance(spec.get("optional_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES and feature not in SUPPORTED_OPTIONAL_FEATURES:
            warnings.append(f"unknown optional feature tolerated: {feature}")
    if _extension_requires_unknown(record.get("extensions", {})) or _extension_requires_unknown(spec.get("extensions", {})):
        _add_error(errors, "install_record.extension_required_unknown", "unknown required extension present")
    observed = spec.get("observed_existing_state") if isinstance(spec.get("observed_existing_state"), dict) else {}
    if observed.get("source_output_used_as_target_truth") is True:
        _add_error(errors, "install_record.source_output_as_target_truth", "source output cannot become target truth")
    if observed.get("target_repository_mutation_performed") is True:
        _add_error(errors, "install_record.target_mutation_claimed", "target mutation is not allowed")
    for value in _iter_string_values(observed):
        code = _path_refusal_code(value)
        if code:
            _add_error(errors, code, f"forbidden observed path/source reference: {value}")
    _boolean_claims_authority(status, errors)
    _boolean_claims_authority(spec, errors)
    expected_digest = install_record_digest(record)
    if status.get("install_record_digest") and status.get("install_record_digest") != expected_digest:
        _add_error(errors, "install_record.digest_mismatch", "install_record_digest does not match canonical payload")
    return _validation_result(errors, warnings)


def minimal_fixture_record() -> dict[str, Any]:
    manifest = distribution_manifest.minimal_fixture_manifest()
    lock = project_lock.minimal_fixture_lock()
    ledger = ownership_ledger.minimal_fixture_ledger()
    record = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "install_record_ref": "aide://install-record/minimal",
            "target_project_ref": lock["metadata"]["project_ref"],
            "target_project_identity": lock["metadata"]["project_identity"],
            "source_distribution_ref": manifest["metadata"]["distribution_ref"],
            "source_distribution_digest": manifest["status"]["distribution_digest"],
            "project_lock_ref": lock["metadata"]["project_lock_ref"],
            "project_lock_digest": lock["status"]["project_lock_digest"],
            "ownership_ledger_ref": ledger["metadata"]["ledger_ref"],
            "ownership_ledger_digest": ledger["status"]["ownership_ledger_digest"],
            "created_at": DETERMINISTIC_TIMESTAMP,
            "created_by": "fixture",
            "created_from": "fixture_projection",
            "prior_install_record_ref": None,
            "superseded_by_ref": None,
            "extensions": {},
        },
        "spec": {
            "install_mode": "observed_fresh_no_apply",
            "install_source": "fixture_projection",
            "observed_existing_state": {
                "state_kind": "fresh_fixture_no_apply",
                "observed_paths": observed_paths_from_ledger(ledger),
                "source_output_used_as_target_truth": False,
                "target_repository_mutation_performed": False,
                "extensions": {},
            },
            "installed_component_refs": component_refs(lock),
            "installed_file_entry_refs": ledger_file_entry_refs(ledger),
            "installed_managed_section_refs": ledger_managed_section_refs(ledger),
            "validation_refs": ["aide://validation/install-record-v0/fixture"],
            "evidence_refs": [DEFAULT_EVIDENCE_REF],
            "warnings": [],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "required_features": [
                "install_record_v0",
                "distribution_manifest_v1",
                "project_lock_v0",
                "ownership_ledger_v1",
                "sha256_digest_canonical_json_v1",
            ],
            "optional_features": [],
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "validation_result": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "recommended_next_task": CHECK_TASK_ID,
            "install_record_digest": "",
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "migration_apply_implemented": False,
            "rollback_apply_implemented": False,
            "uninstall_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "target_scan_authority_implemented": False,
            "release_publication_implemented": False,
            "extensions": {},
        },
        "extensions": {},
    }
    return finalize_install_record(record)


def mutate(data: dict[str, Any], mutator: Any) -> dict[str, Any]:
    copy_data = copy.deepcopy(data)
    mutator(copy_data)
    return finalize_install_record(copy_data)


def write_fixture_corpus(repo_root: str | Path) -> None:
    root = Path(repo_root)
    valid_root = root / FIXTURE_ROOT / "valid"
    invalid_root = root / FIXTURE_ROOT / "invalid"
    valid_root.mkdir(parents=True, exist_ok=True)
    invalid_root.mkdir(parents=True, exist_ok=True)
    base = minimal_fixture_record()
    write_json(valid_root / "fresh-observed-install.json", base)
    existing = mutate(base, lambda d: d["spec"].__setitem__("install_mode", "observed_existing_no_apply"))
    existing["spec"]["observed_existing_state"]["state_kind"] = "existing_fixture_no_apply"
    write_json(valid_root / "existing-observed-install.json", finalize_install_record(existing))
    managed_file = copy.deepcopy(base)
    managed_file["spec"]["installed_managed_section_refs"] = []
    write_json(valid_root / "managed-file-observation.json", finalize_install_record(managed_file))
    managed_section = copy.deepcopy(base)
    managed_section["spec"]["installed_file_entry_refs"] = []
    write_json(valid_root / "managed-section-observation.json", finalize_install_record(managed_section))
    partial = copy.deepcopy(base)
    partial["spec"]["warnings"] = ["partial observation is warning-only and no-apply"]
    partial["spec"]["optional_features"].append("partial_observation_warning_v0")
    write_json(valid_root / "warning-only-partial-observation.json", finalize_install_record(partial))
    extension = copy.deepcopy(base)
    extension["spec"]["optional_features"].append("future.optional.install-record")
    extension["spec"]["extensions"] = {"future.optional": {"preserve": True}}
    write_json(valid_root / "optional-extension-preserved.json", finalize_install_record(extension))
    invalid_cases = {
        "missing-distribution": lambda d: d["metadata"].__setitem__("source_distribution_ref", ""),
        "missing-lock": lambda d: d["metadata"].__setitem__("project_lock_ref", ""),
        "missing-ownership-ledger": lambda d: d["metadata"].__setitem__("ownership_ledger_ref", ""),
        "source-mismatch": lambda d: d["metadata"].__setitem__("source_distribution_digest", "sha256:" + "1" * 64),
        "project-lock-mismatch": lambda d: d["metadata"].__setitem__("project_lock_digest", "sha256:" + "2" * 64),
        "ownership-ledger-mismatch": lambda d: d["metadata"].__setitem__("ownership_ledger_digest", "sha256:" + "3" * 64),
        "unknown-component-ref": lambda d: d["spec"]["installed_component_refs"].append("aide://distribution/component/missing"),
        "unknown-ownership-entry-ref": lambda d: d["spec"]["installed_file_entry_refs"].append("aide://ownership-entry/missing"),
        "unknown-managed-section-ref": lambda d: d["spec"]["installed_managed_section_refs"].append("aide://ownership-entry/missing-section"),
        "apply-claim": lambda d: d["status"].__setitem__("install_apply_implemented", True),
        "target-mutation-claim": lambda d: d["status"].__setitem__("target_repository_mutation_implemented", True),
        "unknown-required-feature": lambda d: d["spec"]["required_features"].append("future.required.install-record"),
        "absolute-path": lambda d: d["spec"]["observed_existing_state"]["observed_paths"].append("C:/outside/file.txt"),
        "traversal-path": lambda d: d["spec"]["observed_existing_state"]["observed_paths"].append("../outside/file.txt"),
        "source-latest-output": lambda d: d["spec"]["observed_existing_state"]["observed_paths"].append(".aide/context/latest-task-packet.md"),
        "source-output-target-truth": lambda d: d["spec"]["observed_existing_state"].__setitem__("source_output_used_as_target_truth", True),
        "missing-evidence": lambda d: d["spec"].__setitem__("evidence_refs", []),
        "extension-required-unknown": lambda d: d["spec"]["extensions"].__setitem__("requires.future", {"enabled": True}),
    }
    for name, mutator in invalid_cases.items():
        write_json(invalid_root / f"{name}.json", mutate(base, mutator))


EXPECTED_INVALID_REFUSALS = {
    "missing-distribution": ["install_record.distribution_missing", "install_record.distribution_mismatch"],
    "missing-lock": ["install_record.project_lock_missing", "install_record.project_lock_mismatch"],
    "missing-ownership-ledger": ["install_record.ownership_ledger_missing", "install_record.ownership_ledger_mismatch"],
    "source-mismatch": ["install_record.distribution_mismatch"],
    "project-lock-mismatch": ["install_record.project_lock_mismatch"],
    "ownership-ledger-mismatch": ["install_record.ownership_ledger_mismatch"],
    "unknown-component-ref": ["install_record.component_ref_unknown"],
    "unknown-ownership-entry-ref": ["install_record.ownership_entry_ref_unknown"],
    "unknown-managed-section-ref": ["install_record.managed_section_ref_unknown"],
    "apply-claim": ["install_record.apply_authority_claimed"],
    "target-mutation-claim": ["install_record.target_mutation_claimed"],
    "unknown-required-feature": ["install_record.unknown_required_feature"],
    "absolute-path": ["install_record.absolute_path_forbidden"],
    "traversal-path": ["install_record.path_traversal_forbidden"],
    "source-latest-output": ["install_record.source_state_contamination"],
    "source-output-target-truth": ["install_record.source_output_as_target_truth"],
    "missing-evidence": ["install_record.evidence_missing"],
    "extension-required-unknown": ["install_record.extension_required_unknown"],
}


def fixture_matrix(repo_root: str | Path) -> list[dict[str, Any]]:
    write_fixture_corpus(repo_root)
    manifest = distribution_manifest.minimal_fixture_manifest()
    lock = project_lock.minimal_fixture_lock()
    ledger = ownership_ledger.minimal_fixture_ledger()
    results: list[dict[str, Any]] = []
    for path in sorted((Path(repo_root) / FIXTURE_ROOT / "valid").glob("*.json")):
        data = read_json(path)
        result = validate_install_record_object(data, distribution=manifest, lock=lock, ledger=ledger, require_ownership_acceptance=False)
        results.append({"case_id": path.stem, "expected_result": "PASS_WITH_WARNINGS", "observed_result": result["status"], "observed_refusal_codes": result["refusal_codes"], "passed": result["valid"], "path": path.relative_to(repo_root).as_posix()})
    for path in sorted((Path(repo_root) / FIXTURE_ROOT / "invalid").glob("*.json")):
        data = read_json(path)
        result = validate_install_record_object(data, distribution=manifest, lock=lock, ledger=ledger, require_ownership_acceptance=False)
        expected = EXPECTED_INVALID_REFUSALS[path.stem]
        passed = not result["valid"] and set(expected).issubset(set(result["refusal_codes"]))
        results.append({"case_id": path.stem, "expected_result": "FAILED_VALIDATION", "expected_refusal_codes": expected, "observed_result": result["status"], "observed_refusal_codes": result["refusal_codes"], "passed": passed, "path": path.relative_to(repo_root).as_posix()})
    return results


def load_schema(repo_root: str | Path) -> dict[str, Any]:
    return read_json(Path(repo_root) / SCHEMA_PATH)


def status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    report = {
        "schema_version": "aide.install-record-status.v0",
        "status": "PASS_WITH_WARNINGS",
        "proposed_capability": PROPOSED_CAPABILITY,
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/install_record.py").exists(),
        "distribution_manifest_report_exists": (root / distribution_manifest.MANIFEST_JSON).exists(),
        "project_lock_report_exists": (root / project_lock.LOCK_JSON).exists(),
        "ownership_ledger_report_exists": (root / ownership_ledger.LEDGER_JSON).exists(),
        "ownership_ledger_acceptance_report_exists": (root / OWNERSHIP_LEDGER_ACCEPTANCE_JSON).exists(),
        "install_record_report_exists": (root / INSTALL_RECORD_JSON).exists(),
        "validation_report_exists": (root / VALIDATION_JSON).exists(),
        "refusal_codes": REFUSAL_CODES,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "recommended_next_task": CHECK_TASK_ID,
        "install_apply_implemented": False,
        "update_apply_implemented": False,
        "migration_apply_implemented": False,
        "rollback_apply_implemented": False,
        "uninstall_apply_implemented": False,
        "target_repository_mutation_implemented": False,
        "target_scan_authority_implemented": False,
        "release_publication_implemented": False,
        "warnings": ["InstallRecord v0 remains proposed until independent check and acceptance."],
    }
    write_text(root / STATUS_MD, render_status_md(report))
    return report


def project(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    record = build_install_record(root)
    write_json(root / INSTALL_RECORD_JSON, record)
    write_text(root / INSTALL_RECORD_MD, render_install_record_md(record))
    write_fixture_corpus(root)
    write_json(root / COMPONENT_BINDING_JSON, {"schema_version": "aide.install-record-component-binding.v0", "installed_component_refs": record["spec"]["installed_component_refs"]})
    write_json(root / OWNERSHIP_ENTRY_BINDING_JSON, {"schema_version": "aide.install-record-ownership-entry-binding.v0", "installed_file_entry_refs": record["spec"]["installed_file_entry_refs"], "installed_managed_section_refs": record["spec"]["installed_managed_section_refs"]})
    matrix = fixture_matrix(root)
    write_json(root / FIXTURE_MATRIX_JSON, {"schema_version": "aide.install-record-fixture-matrix.v0", "fixture_results": matrix})
    write_text(root / FIXTURE_MATRIX_MD, render_fixture_matrix_md(matrix))
    write_text(root / NON_CAPABILITIES_MD, render_non_capabilities_md())
    report = {
        "schema_version": "aide.install-record-project-report.v0",
        "status": "PASS_WITH_WARNINGS",
        "proposed_capability": PROPOSED_CAPABILITY,
        "install_record_path": INSTALL_RECORD_JSON.as_posix(),
        "install_record_digest": record["status"]["install_record_digest"],
        "installed_component_count": len(record["spec"]["installed_component_refs"]),
        "installed_file_entry_count": len(record["spec"]["installed_file_entry_refs"]),
        "installed_managed_section_count": len(record["spec"]["installed_managed_section_refs"]),
        "source_artifacts_mutated": False,
        "target_repository_mutation_implemented": False,
        "recommended_next_task": CHECK_TASK_ID,
        "warnings": record["spec"]["warnings"],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
    }
    status(root)
    return report


def validate(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    project_report = project(root)
    record = read_json(root / INSTALL_RECORD_JSON)
    manifest = load_distribution_manifest(root)
    lock = load_project_lock(root)
    ledger = load_ownership_ledger(root)
    record_validation = validate_install_record_object(record, distribution=manifest, lock=lock, ledger=ledger, repo_root=root)
    schema = load_schema(root)
    schema_alignment_errors = schema_alignment_errors_for(schema)
    fixtures = fixture_matrix(root)
    fixture_passed = all(item["passed"] for item in fixtures)
    errors = record_validation["errors"] + ([] if fixture_passed else [{"code": "install_record.fixture_failure", "message": "fixture corpus failed"}])
    checks = {
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/install_record.py").exists(),
        "cli_registered": cli_registered(root),
        "install_record_generated": (root / INSTALL_RECORD_JSON).exists(),
        "install_record_valid": record_validation["valid"],
        "schema_alignment": not schema_alignment_errors,
        "fixture_matrix_passed": fixture_passed,
        "ownership_ledger_accepted": ownership_ledger_is_accepted(root),
        "distribution_ref_bound": record["metadata"]["source_distribution_ref"] == manifest["metadata"]["distribution_ref"],
        "project_lock_digest_bound": record["metadata"]["project_lock_digest"] == lock["status"]["project_lock_digest"],
        "ownership_ledger_digest_bound": record["metadata"]["ownership_ledger_digest"] == ledger["status"]["ownership_ledger_digest"],
        "component_refs_known": set(record["spec"]["installed_component_refs"]).issubset(set(component_refs(lock))),
        "file_entry_refs_known": set(record["spec"]["installed_file_entry_refs"]).issubset(set(ledger_file_entry_refs(ledger))),
        "managed_section_refs_known": set(record["spec"]["installed_managed_section_refs"]).issubset(set(ledger_managed_section_refs(ledger))),
        "install_apply_not_implemented": record["status"]["install_apply_implemented"] is False,
        "update_apply_not_implemented": record["status"]["update_apply_implemented"] is False,
        "migration_apply_not_implemented": record["status"]["migration_apply_implemented"] is False,
        "rollback_apply_not_implemented": record["status"]["rollback_apply_implemented"] is False,
        "uninstall_apply_not_implemented": record["status"]["uninstall_apply_implemented"] is False,
        "target_repository_mutation_not_implemented": record["status"]["target_repository_mutation_implemented"] is False,
        "target_scan_authority_not_implemented": record["status"]["target_scan_authority_implemented"] is False,
        "release_publication_not_implemented": record["status"]["release_publication_implemented"] is False,
        "source_output_not_target_truth": record["spec"]["observed_existing_state"]["source_output_used_as_target_truth"] is False,
    }
    validation_status = "PASS_WITH_WARNINGS" if not errors and not schema_alignment_errors else "FAILED_VALIDATION"
    report = {
        "schema_version": "aide.install-record-validation.v0",
        "validation_status": validation_status,
        "status": validation_status,
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": CHECK_TASK_ID,
        "checks": checks,
        "errors": errors,
        "schema_alignment_errors": schema_alignment_errors,
        "install_record_validation": record_validation,
        "fixture_results": fixtures,
        "project_report": project_report,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "warnings": [
            "InstallRecord v0 is proposed until independent check and acceptance.",
            "InstallRecord records install metadata only and performs no install or target mutation.",
        ],
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_md(report))
    return report


def schema_alignment_errors_for(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema must declare Draft 2020-12")
    if schema.get("title") != "AIDE InstallRecord v0":
        errors.append("schema title mismatch")
    for field in ["apiVersion", "kind", "schema_version", "metadata", "spec", "status", "extensions"]:
        if field not in schema.get("required", []):
            errors.append(f"schema missing required field: {field}")
    return errors


def cli_registered(repo_root: Path) -> bool:
    script = repo_root / ".aide/scripts/aide_lite.py"
    if not script.exists():
        return False
    text = script.read_text(encoding="utf-8")
    return "install-record" in text and "command_install_record_validate" in text


def render_status_md(data: dict[str, Any]) -> str:
    lines = [
        "# InstallRecord v0 Status",
        "",
        f"- status: {data.get('status')}",
        f"- proposed_capability: {data.get('proposed_capability')}",
        f"- schema_exists: {str(data.get('schema_exists')).lower()}",
        f"- helper_exists: {str(data.get('helper_exists')).lower()}",
        f"- ownership_ledger_acceptance_report_exists: {str(data.get('ownership_ledger_acceptance_report_exists')).lower()}",
        f"- recommended_next_task: {data.get('recommended_next_task')}",
        "",
        "## Explicit Non-Capabilities",
        "",
    ]
    for item in EXPLICIT_NON_CAPABILITIES:
        lines.append(f"- {item}: false")
    return "\n".join(lines) + "\n"


def render_install_record_md(record: dict[str, Any]) -> str:
    lines = [
        "# InstallRecord v0 Projection",
        "",
        f"- install_record_ref: `{record['metadata']['install_record_ref']}`",
        f"- source_distribution_ref: `{record['metadata']['source_distribution_ref']}`",
        f"- project_lock_ref: `{record['metadata']['project_lock_ref']}`",
        f"- ownership_ledger_ref: `{record['metadata']['ownership_ledger_ref']}`",
        f"- install_record_digest: `{record['status']['install_record_digest']}`",
        f"- installed_component_count: {len(record['spec']['installed_component_refs'])}",
        f"- installed_file_entry_count: {len(record['spec']['installed_file_entry_refs'])}",
        f"- installed_managed_section_count: {len(record['spec']['installed_managed_section_refs'])}",
        "- install_apply_implemented: false",
        "- target_repository_mutation_implemented: false",
        "- target_scan_authority_implemented: false",
    ]
    return "\n".join(lines) + "\n"


def render_fixture_matrix_md(fixtures: list[dict[str, Any]]) -> str:
    lines = ["# InstallRecord v0 Fixture Matrix", "", "| Case | Expected | Observed | Codes | Pass |", "| --- | --- | --- | --- | --- |"]
    for fixture in fixtures:
        codes = ", ".join(fixture.get("observed_refusal_codes", [])) or "none"
        lines.append(f"| {fixture['case_id']} | {fixture['expected_result']} | {fixture['observed_result']} | {codes} | {str(fixture['passed']).lower()} |")
    return "\n".join(lines) + "\n"


def render_non_capabilities_md() -> str:
    lines = ["# InstallRecord v0 Explicit Non-Capabilities", ""]
    for item in EXPLICIT_NON_CAPABILITIES:
        lines.append(f"- {item}: false")
    return "\n".join(lines) + "\n"


def render_validation_md(report: dict[str, Any]) -> str:
    lines = [
        "# InstallRecord v0 Validation",
        "",
        f"- result: {report.get('validation_status')}",
        f"- proposed_capability: {report.get('proposed_capability')}",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Checks",
        "",
    ]
    for key, value in report.get("checks", {}).items():
        lines.append(f"- {key}: {str(value).lower()}")
    lines.extend(["", "## Fixture Results", ""])
    for item in report.get("fixture_results", []):
        lines.append(f"- {item['case_id']}: {str(item['passed']).lower()} ({item['observed_result']})")
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"
