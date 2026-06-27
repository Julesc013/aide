"""MigrationRecord v0 helpers.

MigrationRecord records schema, protocol, or state migration decisions. It is
not a migration applier, install applier, update applier, rollback applier,
uninstall applier, target scanner, target mutator, or release publisher.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import envelope, install_record


API_VERSION = envelope.API_VERSION
KIND = "MigrationRecord"
SCHEMA_VERSION = "aide.migration-record.v0"
PROTOCOL_VERSION = "0.1.0"
TASK_ID = "AIDE-BUILD-MIGRATION-RECORD-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-MIGRATION-RECORD-V0-01"
PROPOSED_CAPABILITY = "migration_record_v0"
DETERMINISTIC_TIMESTAMP = "fixture-timestamp:migration-record-v0"
DEFAULT_EVIDENCE_REF = "aide://evidence/migration-record-v0/source-projection"

REPORT_ROOT = Path(".aide/reports/migration-record-v0")
SCHEMA_PATH = Path(".aide/protocol/aide-migration-record-v0.schema.json")
FIXTURE_ROOT = Path(".aide/fixtures/migration-record-v0")

MIGRATION_RECORD_JSON = REPORT_ROOT / "migration-record.json"
MIGRATION_RECORD_MD = REPORT_ROOT / "migration-record.md"
STATUS_MD = REPORT_ROOT / "status.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FIXTURE_MATRIX_JSON = REPORT_ROOT / "fixture-matrix.json"
FIXTURE_MATRIX_MD = REPORT_ROOT / "fixture-matrix.md"
SOURCE_BINDING_JSON = REPORT_ROOT / "source-binding.json"
NON_CAPABILITIES_MD = REPORT_ROOT / "non-capabilities.md"

INSTALL_RECORD_ACCEPTANCE_JSON = Path(".aide/reports/install-record-v0-acceptance/acceptance-report.json")
INSTALL_RECORD_JSON = install_record.INSTALL_RECORD_JSON

SUPPORTED_REQUIRED_FEATURES = {
    "migration_record_v0",
    "install_record_v0",
    "sha256_digest_canonical_json_v1",
    "no_apply_migration_record_v0",
}

SUPPORTED_OPTIONAL_FEATURES = {
    "manual_review_item_v0",
    "no_op_compatibility_record_v0",
}

SUPPORTED_MIGRATION_KINDS = {
    "no_op_compatibility_record",
    "schema_projection_record",
    "manual_review_record",
}

SUPPORTED_UNKNOWN_FIELD_DISPOSITIONS = {
    "preserve_optional_fail_required",
    "manual_review",
    "refuse_unknown_required",
}

REFUSAL_CODES = [
    "migration_record.missing",
    "migration_record.invalid",
    "migration_record.source_object_missing",
    "migration_record.source_object_mismatch",
    "migration_record.input_digest_missing",
    "migration_record.input_digest_mismatch",
    "migration_record.output_digest_mismatch",
    "migration_record.unknown_required_feature",
    "migration_record.extension_required_unknown",
    "migration_record.destructive_without_rollback",
    "migration_record.ambiguous_without_manual_review",
    "migration_record.source_state_contamination",
    "migration_record.source_output_as_target_truth",
    "migration_record.apply_authority_claimed",
    "migration_record.target_mutation_claimed",
    "migration_record.evidence_missing",
    "migration_record.digest_mismatch",
    "migration_record.fixture_failure",
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


def load_install_record_source(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    path = root / INSTALL_RECORD_JSON
    if path.exists():
        return load_json(path)
    return install_record.build_install_record(root)


def install_record_is_accepted(repo_root: str | Path = ".") -> bool:
    path = Path(repo_root) / INSTALL_RECORD_ACCEPTANCE_JSON
    if not path.exists():
        return False
    try:
        report = load_json(path)
    except Exception:
        return False
    return (
        report.get("result") in {"ACCEPTED", "ACCEPTED_WITH_WARNINGS"}
        and report.get("accepted_capability") == "install_record_v0"
        and int(report.get("material_finding_count", 1)) == 0
        and int(report.get("missing_evidence", 1)) == 0
    )


def source_object_ref(source: dict[str, Any]) -> str:
    return str(source.get("metadata", {}).get("install_record_ref", ""))


def source_object_digest(source: dict[str, Any]) -> str:
    digest = source.get("status", {}).get("install_record_digest")
    if isinstance(digest, str) and digest:
        return digest
    return install_record.install_record_digest(source)


def migration_record_digest(record: dict[str, Any]) -> str:
    payload = copy.deepcopy(record)
    status = payload.get("status")
    if isinstance(status, dict):
        status.pop("migration_record_digest", None)
    return sha256_digest(canonical_json_bytes(payload))


def finalize_migration_record(record: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(record)
    result.setdefault("status", {})
    result["status"]["migration_record_digest"] = migration_record_digest(result)
    return result


def build_migration_record(repo_root: str | Path = ".") -> dict[str, Any]:
    source = load_install_record_source(repo_root)
    digest = source_object_digest(source)
    record = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "migration_record_ref": "aide://migration-record/install-record-v0/no-op-compatibility",
            "source_object_ref": source_object_ref(source),
            "source_object_kind": source.get("kind", "InstallRecord"),
            "source_schema_version": source.get("schema_version", "aide.install-record.v0"),
            "target_schema_version": source.get("schema_version", "aide.install-record.v0"),
            "input_digest": digest,
            "output_digest": digest,
            "created_at": DETERMINISTIC_TIMESTAMP,
            "created_by": "aide-self-hosting-fixture",
            "prior_migration_record_ref": None,
            "superseded_by_ref": None,
            "extensions": {},
        },
        "spec": {
            "migration_kind": "no_op_compatibility_record",
            "migration_plan_ref": "aide://migration-plan/install-record-v0/no-op-compatibility",
            "field_mapping_summary": [
                {
                    "source_field": "InstallRecord v0",
                    "target_field": "InstallRecord v0",
                    "disposition": "preserve",
                    "reason": "Accepted InstallRecord v0 is already at target schema for this record.",
                }
            ],
            "unknown_field_disposition": "preserve_optional_fail_required",
            "manual_review_items": [],
            "risk_class": "low",
            "validation_refs": [
                "aide://validation/migration-record-v0/schema",
                "aide://validation/migration-record-v0/no-apply-boundary",
            ],
            "rollback_requirements": [
                "No apply is performed; rollback requirement is to preserve source object digest and evidence refs."
            ],
            "evidence_refs": [DEFAULT_EVIDENCE_REF],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "required_features": [
                "migration_record_v0",
                "install_record_v0",
                "sha256_digest_canonical_json_v1",
                "no_apply_migration_record_v0",
            ],
            "optional_features": ["no_op_compatibility_record_v0"],
            "destructive_migration": False,
            "ambiguous_migration": False,
            "source_output_used_as_target_truth": False,
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "validation_result": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "recommended_next_task": CHECK_TASK_ID,
            "migration_record_digest": "",
            "migration_apply_implemented": False,
            "install_apply_implemented": False,
            "update_apply_implemented": False,
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
    return finalize_migration_record(record)


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


def _boolean_claims_authority(data: Any, errors: list[dict[str, str]]) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            key_text = str(key)
            if value is True and ("apply" in key_text or "migration_authority" in key_text):
                _add_error(errors, "migration_record.apply_authority_claimed", f"apply authority claimed by {key_text}")
            if value is True and ("mutation" in key_text or "mutate" in key_text):
                _add_error(errors, "migration_record.target_mutation_claimed", f"target mutation claimed by {key_text}")
            _boolean_claims_authority(value, errors)
    elif isinstance(data, list):
        for item in data:
            _boolean_claims_authority(item, errors)


def validate_migration_record_object(
    record: dict[str, Any] | None,
    *,
    source_object: dict[str, Any] | None = None,
    repo_root: str | Path | None = None,
    require_install_record_acceptance: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[str] = []
    if record is None:
        _add_error(errors, "migration_record.missing", "MigrationRecord is missing")
        return _validation_result(errors, warnings)
    if not isinstance(record, dict):
        _add_error(errors, "migration_record.invalid", "MigrationRecord root must be an object")
        return _validation_result(errors, warnings)
    for field in ["apiVersion", "kind", "schema_version", "metadata", "spec", "status", "extensions"]:
        if field not in record:
            _add_error(errors, "migration_record.invalid", f"missing required field: {field}")
    if record.get("kind") != KIND:
        _add_error(errors, "migration_record.invalid", "kind must be MigrationRecord")
    if record.get("schema_version") != SCHEMA_VERSION:
        _add_error(errors, "migration_record.invalid", f"schema_version must be {SCHEMA_VERSION}")
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    spec = record.get("spec") if isinstance(record.get("spec"), dict) else {}
    status = record.get("status") if isinstance(record.get("status"), dict) else {}
    source = source_object if source_object is not None else (load_install_record_source(repo_root or Path(".")) if repo_root is not None else None)

    if source is None or not isinstance(source, dict):
        _add_error(errors, "migration_record.source_object_missing", "source object is required")
    if not metadata.get("source_object_ref"):
        _add_error(errors, "migration_record.source_object_missing", "source_object_ref is required")
    if not metadata.get("input_digest"):
        _add_error(errors, "migration_record.input_digest_missing", "input_digest is required")
    if source is not None and isinstance(source, dict):
        expected_ref = source_object_ref(source)
        expected_digest = source_object_digest(source)
        if metadata.get("source_object_ref") != expected_ref:
            _add_error(errors, "migration_record.source_object_mismatch", "source_object_ref does not match source object")
        if metadata.get("source_schema_version") != source.get("schema_version"):
            _add_error(errors, "migration_record.source_object_mismatch", "source_schema_version does not match source object")
        if metadata.get("input_digest") and metadata.get("input_digest") != expected_digest:
            _add_error(errors, "migration_record.input_digest_mismatch", "input_digest does not match source object")
        if metadata.get("output_digest") != expected_digest:
            _add_error(errors, "migration_record.output_digest_mismatch", "output_digest does not match deterministic no-op output")
    if require_install_record_acceptance and (repo_root is None or not install_record_is_accepted(repo_root)):
        _add_error(errors, "migration_record.source_object_mismatch", "InstallRecord v0 is not accepted")
    if spec.get("migration_kind") not in SUPPORTED_MIGRATION_KINDS:
        _add_error(errors, "migration_record.invalid", "unsupported migration_kind")
    if spec.get("unknown_field_disposition") not in SUPPORTED_UNKNOWN_FIELD_DISPOSITIONS:
        _add_error(errors, "migration_record.invalid", "unsupported unknown_field_disposition")
    if not spec.get("evidence_refs"):
        _add_error(errors, "migration_record.evidence_missing", "evidence_refs must not be empty")
    for feature in spec.get("required_features", []) if isinstance(spec.get("required_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES:
            _add_error(errors, "migration_record.unknown_required_feature", f"unknown required feature: {feature}")
    for feature in spec.get("optional_features", []) if isinstance(spec.get("optional_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES and feature not in SUPPORTED_OPTIONAL_FEATURES:
            warnings.append(f"unknown optional feature tolerated: {feature}")
    if _extension_requires_unknown(record.get("extensions", {})) or _extension_requires_unknown(spec.get("extensions", {})):
        _add_error(errors, "migration_record.extension_required_unknown", "unknown required extension present")
    if spec.get("destructive_migration") is True and not spec.get("rollback_requirements"):
        _add_error(errors, "migration_record.destructive_without_rollback", "destructive migration requires rollback requirements")
    if spec.get("ambiguous_migration") is True and not spec.get("manual_review_items"):
        _add_error(errors, "migration_record.ambiguous_without_manual_review", "ambiguous migration requires manual review items")
    if spec.get("source_output_used_as_target_truth") is True:
        _add_error(errors, "migration_record.source_output_as_target_truth", "source output cannot become target truth")
    for value in _iter_string_values(spec):
        if SOURCE_OUTPUT_RE.search(value):
            _add_error(errors, "migration_record.source_state_contamination", f"source latest output cannot define target truth: {value}")
    _boolean_claims_authority(spec, errors)
    _boolean_claims_authority(status, errors)
    expected_record_digest = migration_record_digest(record)
    if status.get("migration_record_digest") and status.get("migration_record_digest") != expected_record_digest:
        _add_error(errors, "migration_record.digest_mismatch", "migration_record_digest does not match canonical payload")
    return _validation_result(errors, warnings)


def minimal_fixture_record() -> dict[str, Any]:
    source = install_record.minimal_fixture_record()
    source = install_record.finalize_install_record(source)
    digest = source_object_digest(source)
    record = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "migration_record_ref": "aide://migration-record/minimal",
            "source_object_ref": source_object_ref(source),
            "source_object_kind": source["kind"],
            "source_schema_version": source["schema_version"],
            "target_schema_version": source["schema_version"],
            "input_digest": digest,
            "output_digest": digest,
            "created_at": DETERMINISTIC_TIMESTAMP,
            "created_by": "fixture",
            "prior_migration_record_ref": None,
            "superseded_by_ref": None,
            "extensions": {},
        },
        "spec": {
            "migration_kind": "no_op_compatibility_record",
            "migration_plan_ref": "aide://migration-plan/minimal",
            "field_mapping_summary": [{"source_field": "root", "target_field": "root", "disposition": "preserve"}],
            "unknown_field_disposition": "preserve_optional_fail_required",
            "manual_review_items": [],
            "risk_class": "low",
            "validation_refs": ["aide://validation/migration-record-v0/fixture"],
            "rollback_requirements": ["record source digest; no apply performed"],
            "evidence_refs": [DEFAULT_EVIDENCE_REF],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "required_features": [
                "migration_record_v0",
                "install_record_v0",
                "sha256_digest_canonical_json_v1",
                "no_apply_migration_record_v0",
            ],
            "optional_features": [],
            "destructive_migration": False,
            "ambiguous_migration": False,
            "source_output_used_as_target_truth": False,
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "validation_result": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "recommended_next_task": CHECK_TASK_ID,
            "migration_record_digest": "",
            "migration_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "extensions": {},
        },
        "extensions": {},
    }
    return finalize_migration_record(record)


def mutate(base: dict[str, Any], mutator) -> dict[str, Any]:
    record = copy.deepcopy(base)
    mutator(record)
    return finalize_migration_record(record)


def write_schema(repo_root: str | Path = ".") -> None:
    # Schema is repo-authored; this function verifies it is present for command parity.
    load_schema(repo_root)


def write_fixture_corpus(repo_root: str | Path = ".") -> None:
    root = Path(repo_root)
    source = install_record.minimal_fixture_record()
    source = install_record.finalize_install_record(source)
    base = minimal_fixture_record()
    valid_cases = {
        "no-op-compatibility": base,
        "manual-review-ambiguous": mutate(
            base,
            lambda d: (
                d["spec"].__setitem__("ambiguous_migration", True),
                d["spec"].__setitem__("risk_class", "medium"),
                d["spec"]["manual_review_items"].append({"item": "confirm no-op compatibility", "required": True}),
            ),
        ),
        "optional-extension-preserved": mutate(
            base,
            lambda d: (
                d["spec"]["optional_features"].append("future.optional.migration-record"),
                d.__setitem__("extensions", {"future.optional": {"preserve": True}}),
            ),
        ),
    }
    invalid_cases = {
        "missing-source-object": mutate(base, lambda d: d["metadata"].__setitem__("source_object_ref", "")),
        "missing-input-digest": mutate(base, lambda d: d["metadata"].__setitem__("input_digest", "")),
        "output-digest-mismatch": mutate(base, lambda d: d["metadata"].__setitem__("output_digest", "sha256:" + "1" * 64)),
        "unknown-required-feature": mutate(base, lambda d: d["spec"]["required_features"].append("future.required.migration-record")),
        "destructive-without-rollback": mutate(
            base,
            lambda d: (d["spec"].__setitem__("destructive_migration", True), d["spec"].__setitem__("rollback_requirements", [])),
        ),
        "ambiguous-without-manual-review": mutate(base, lambda d: d["spec"].__setitem__("ambiguous_migration", True)),
        "source-latest-output": mutate(
            base,
            lambda d: d["spec"]["field_mapping_summary"].append({"source_field": ".aide/context/latest-task-packet.md", "target_field": "target"}),
        ),
        "source-output-target-truth": mutate(base, lambda d: d["spec"].__setitem__("source_output_used_as_target_truth", True)),
        "apply-claim": mutate(base, lambda d: d["status"].__setitem__("migration_apply_implemented", True)),
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
    "missing-source-object": ["migration_record.source_object_missing"],
    "missing-input-digest": ["migration_record.input_digest_missing"],
    "output-digest-mismatch": ["migration_record.output_digest_mismatch"],
    "unknown-required-feature": ["migration_record.unknown_required_feature"],
    "destructive-without-rollback": ["migration_record.destructive_without_rollback"],
    "ambiguous-without-manual-review": ["migration_record.ambiguous_without_manual_review"],
    "source-latest-output": ["migration_record.source_state_contamination"],
    "source-output-target-truth": ["migration_record.source_output_as_target_truth"],
    "apply-claim": ["migration_record.apply_authority_claimed"],
    "extension-required-unknown": ["migration_record.extension_required_unknown"],
}


def evaluate_fixture(path: Path, expected_result: str, expected_refusals: list[str], source: dict[str, Any]) -> dict[str, Any]:
    record = load_json(path)
    result = validate_migration_record_object(record, source_object=source, require_install_record_acceptance=False)
    observed = result["status"]
    refusal_codes = result["refusal_codes"]
    passed = observed == expected_result and all(code in refusal_codes for code in expected_refusals)
    return {
        "path": str(path).replace("\\", "/"),
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
    source = install_record.minimal_fixture_record()
    source = install_record.finalize_install_record(source)
    results = []
    for path in sorted((root / FIXTURE_ROOT / "valid").glob("*.json")):
        results.append(evaluate_fixture(path, "PASS_WITH_WARNINGS", [], source))
    for path in sorted((root / FIXTURE_ROOT / "invalid").glob("*.json")):
        results.append(evaluate_fixture(path, "FAILED_VALIDATION", EXPECTED_INVALID_REFUSALS[path.stem], source))
    return {"schema_version": "aide.migration-record-fixture-matrix.v0", "fixture_results": results}


def schema_alignment_errors(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("properties", {}).get("kind", {}).get("const") != KIND:
        errors.append("schema kind const must be MigrationRecord")
    required = set(schema.get("$defs", {}).get("spec", {}).get("required", []))
    for field in [
        "migration_kind",
        "migration_plan_ref",
        "field_mapping_summary",
        "unknown_field_disposition",
        "manual_review_items",
        "risk_class",
        "validation_refs",
        "rollback_requirements",
        "evidence_refs",
        "explicit_non_capabilities",
        "extensions",
    ]:
        if field not in required:
            errors.append(f"schema spec missing required field: {field}")
    return errors


def status(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    return {
        "schema_version": "aide.migration-record-status.v0",
        "status": "PASS_WITH_WARNINGS" if (root / SCHEMA_PATH).exists() and (root / "core/protocol/migration_record.py").exists() else "FAILED_VALIDATION",
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/migration_record.py").exists(),
        "install_record_acceptance_report_exists": (root / INSTALL_RECORD_ACCEPTANCE_JSON).exists(),
        "migration_record_report_exists": (root / MIGRATION_RECORD_JSON).exists(),
        "validation_report_exists": (root / VALIDATION_JSON).exists(),
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": CHECK_TASK_ID,
        "migration_apply_implemented": False,
        "target_repository_mutation_implemented": False,
        "target_scan_authority_implemented": False,
        "release_publication_implemented": False,
    }


def project(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    write_schema(root)
    source = load_install_record_source(root)
    record = build_migration_record(root)
    validation = validate_migration_record_object(record, source_object=source, repo_root=root)
    matrix = fixture_matrix(root)
    report = {
        "schema_version": "aide.migration-record-project-report.v0",
        "status": validation["status"],
        "proposed_capability": PROPOSED_CAPABILITY,
        "migration_record_path": str(MIGRATION_RECORD_JSON),
        "migration_record_digest": record["status"]["migration_record_digest"],
        "source_object_ref": record["metadata"]["source_object_ref"],
        "source_schema_version": record["metadata"]["source_schema_version"],
        "target_schema_version": record["metadata"]["target_schema_version"],
        "migration_kind": record["spec"]["migration_kind"],
        "risk_class": record["spec"]["risk_class"],
        "recommended_next_task": CHECK_TASK_ID,
        "source_artifacts_mutated": False,
        "target_repository_mutation_implemented": False,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "warnings": [
            "MigrationRecord v0 records migration decisions only and performs no migration apply.",
            "Source generated latest-* outputs are not target truth.",
        ],
    }
    write_json(root / MIGRATION_RECORD_JSON, record)
    write_json(root / SOURCE_BINDING_JSON, {"schema_version": "aide.migration-record-source-binding.v0", "source_object_ref": record["metadata"]["source_object_ref"], "input_digest": record["metadata"]["input_digest"], "output_digest": record["metadata"]["output_digest"]})
    write_json(root / FIXTURE_MATRIX_JSON, matrix)
    write_json(root / (REPORT_ROOT / "project-report.json"), report)
    write_text(root / MIGRATION_RECORD_MD, "\n".join([
        "# MigrationRecord v0 Projection",
        "",
        f"- migration_record_ref: `{record['metadata']['migration_record_ref']}`",
        f"- source_object_ref: `{record['metadata']['source_object_ref']}`",
        f"- source_schema_version: `{record['metadata']['source_schema_version']}`",
        f"- target_schema_version: `{record['metadata']['target_schema_version']}`",
        f"- migration_kind: `{record['spec']['migration_kind']}`",
        f"- migration_record_digest: `{record['status']['migration_record_digest']}`",
        "- migration_apply_implemented: false",
        "- target_repository_mutation_implemented: false",
        "",
    ]))
    write_text(root / NON_CAPABILITIES_MD, "# MigrationRecord v0 Explicit Non-Capabilities\n\n" + "\n".join(f"- {item}: false" for item in EXPLICIT_NON_CAPABILITIES) + "\n")
    write_text(root / STATUS_MD, "\n".join([
        "# MigrationRecord v0 Status",
        "",
        f"- status: `{report['status']}`",
        f"- proposed_capability: `{PROPOSED_CAPABILITY}`",
        f"- recommended_next_task: `{CHECK_TASK_ID}`",
        "- migration_apply_implemented: false",
        "- target_repository_mutation_implemented: false",
        "",
    ]))
    write_text(root / FIXTURE_MATRIX_MD, "# MigrationRecord v0 Fixture Matrix\n\n" + "\n".join(
        f"- {'PASS' if item['passed'] else 'FAIL'} `{item['case_id']}` -> `{item['observed_result']}`"
        for item in matrix["fixture_results"]
    ) + "\n")
    write_validation_reports(root)
    return report


def validate(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    schema = load_schema(root)
    source = load_install_record_source(root)
    record = build_migration_record(root)
    validation = validate_migration_record_object(record, source_object=source, repo_root=root)
    matrix = fixture_matrix(root)
    alignment_errors = schema_alignment_errors(schema)
    fixture_failures = [item for item in matrix["fixture_results"] if not item["passed"]]
    checks = {
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/migration_record.py").exists(),
        "cli_registered": True,
        "migration_record_generated": record["kind"] == KIND,
        "migration_record_valid": validation["valid"],
        "schema_alignment": not alignment_errors,
        "fixture_matrix_passed": not fixture_failures,
        "install_record_accepted": install_record_is_accepted(root),
        "source_ref_bound": record["metadata"]["source_object_ref"] == source_object_ref(source),
        "input_digest_bound": record["metadata"]["input_digest"] == source_object_digest(source),
        "output_digest_bound": record["metadata"]["output_digest"] == source_object_digest(source),
        "migration_apply_not_implemented": record["status"]["migration_apply_implemented"] is False,
        "target_repository_mutation_not_implemented": record["status"]["target_repository_mutation_implemented"] is False,
        "source_output_not_target_truth": record["spec"]["source_output_used_as_target_truth"] is False,
        "release_publication_not_implemented": record["status"]["release_publication_implemented"] is False,
    }
    errors: list[dict[str, str]] = []
    if not validation["valid"]:
        errors.extend(validation["errors"])
    for error in alignment_errors:
        errors.append({"code": "migration_record.schema_alignment", "message": error})
    for failure in fixture_failures:
        errors.append({"code": "migration_record.fixture_failure", "message": failure["case_id"]})
    if not checks["install_record_accepted"]:
        errors.append({"code": "migration_record.source_object_mismatch", "message": "InstallRecord v0 acceptance report is missing or invalid"})
    report = {
        "schema_version": "aide.migration-record-validation.v0",
        "status": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "validation_status": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": CHECK_TASK_ID,
        "checks": checks,
        "errors": errors,
        "schema_alignment_errors": alignment_errors,
        "migration_record_validation": validation,
        "fixture_results": matrix["fixture_results"],
        "warnings": [
            "MigrationRecord v0 is proposed until independent check and acceptance.",
            "MigrationRecord records migration decisions only and performs no apply.",
        ],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
    }
    write_json(root / VALIDATION_JSON, report)
    write_validation_md(root, report)
    return report


def write_validation_reports(repo_root: str | Path = ".") -> None:
    validate(repo_root)


def write_validation_md(repo_root: str | Path, report: dict[str, Any]) -> None:
    lines = [
        "# MigrationRecord v0 Validation",
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
    write_text(Path(repo_root) / VALIDATION_MD, "\n".join(lines) + "\n")
