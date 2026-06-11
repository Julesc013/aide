"""Minimal AIDE contract envelope helpers.

This module is intentionally narrow. It projects the accepted lifecycle fixture
runner reports into a small apiVersion/kind/metadata/spec/status envelope
without destructively migrating the source reports.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any


API_VERSION = "aide.dev/v1alpha1"
ENVELOPE_SCHEMA_VERSION = "aide.contract-envelope.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = "aide-lite"
PRODUCER_VERSION = "0.1.0"
REPORT_ROOT = Path(".aide/reports/contract-envelope")
PROJECTION_ROOT = REPORT_ROOT / "projections"
SCHEMA_PATH = Path(".aide/protocol/aide-envelope.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"
LIFECYCLE_RUN_SOURCE = Path(".aide/reports/lifecycle-fixture-runner/latest-run.json")
LIFECYCLE_VERIFY_SOURCE = Path(".aide/reports/lifecycle-fixture-runner/verify.json")
LIFECYCLE_ACCEPTANCE_SOURCE = Path(".aide/reports/lifecycle-fixture-runner-acceptance/acceptance-report.json")
LIFECYCLE_RUN_PROJECTION = PROJECTION_ROOT / "lifecycle-fixture-latest-run.envelope.json"
LIFECYCLE_VERIFY_PROJECTION = PROJECTION_ROOT / "lifecycle-fixture-verify.envelope.json"
LIFECYCLE_ACCEPTANCE_PROJECTION = PROJECTION_ROOT / "lifecycle-fixture-acceptance.envelope.json"
SUPPORTED_KINDS = {
    "LifecycleFixtureRunReport",
    "LifecycleFixtureVerifyReport",
    "LifecycleFixtureAcceptanceReport",
}
ENVELOPE_REQUIRED_FIELDS = ["apiVersion", "kind", "metadata", "spec", "status"]
RECOGNIZED_CAPABILITIES = {"fixture_temp_apply_only"}
EXPLICIT_NON_CAPABILITIES = [
    "active_repo_apply",
    "target_repo_apply",
    "broad_lifecycle_apply",
    "rollback_execution",
    "uninstall_execution",
    "service_ready",
    "commander_ready",
    "provider_adapter_ready",
    "branch_worktree_automation",
    "production_ready",
    "release_ready",
]
SEMVERISH = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
SCHEMA_VALIDATION_MODE = "minimal_json_schema_subset"
SCHEMA_VALIDATION_LIMITATIONS = [
    "Local subset validator supports type, required, properties, simple additionalProperties, and homogeneous array items only.",
    "Full JSON Schema Draft 2020-12 validation remains future work.",
    "Formats, refs, oneOf/anyOf/allOf, conditionals, numeric bounds, and pattern checks are not implemented.",
]


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not load JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(obj), encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def validate_semverish(value: str) -> bool:
    return bool(isinstance(value, str) and SEMVERISH.match(value))


def _compatibility(metadata: dict[str, Any]) -> dict[str, Any]:
    compatibility = metadata.get("compatibility")
    if isinstance(compatibility, dict):
        result = copy.deepcopy(compatibility)
    else:
        result = {}
    result.setdefault("schemaVersion", PROTOCOL_VERSION)
    result.setdefault("protocolVersion", PROTOCOL_VERSION)
    result.setdefault("minReaderVersion", PROTOCOL_VERSION)
    result.setdefault("minWriterVersion", PROTOCOL_VERSION)
    result.setdefault("featureFlags", [])
    return result


def build_envelope(
    kind: str,
    metadata: dict[str, Any],
    spec: dict[str, Any],
    status: dict[str, Any],
    api_version: str = API_VERSION,
) -> dict[str, Any]:
    envelope_metadata = copy.deepcopy(metadata)
    envelope_metadata.setdefault(
        "producer",
        {
            "name": PRODUCER_NAME,
            "version": PRODUCER_VERSION,
        },
    )
    envelope_metadata["compatibility"] = _compatibility(envelope_metadata)
    return {
        "apiVersion": api_version,
        "kind": kind,
        "schema_version": ENVELOPE_SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "metadata": envelope_metadata,
        "spec": copy.deepcopy(spec),
        "status": copy.deepcopy(status),
    }


def _validate_object_field(obj: dict[str, Any], field: str, errors: list[str]) -> None:
    if field not in obj:
        errors.append(f"missing required field: {field}")
    elif not isinstance(obj[field], dict):
        errors.append(f"{field} must be an object")


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate_envelope(obj: dict[str, Any], allowed_kinds: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["envelope must be an object"]
    if not isinstance(obj.get("apiVersion"), str) or not obj.get("apiVersion"):
        errors.append("apiVersion must be a non-empty string")
    if not isinstance(obj.get("kind"), str) or not obj.get("kind"):
        errors.append("kind must be a non-empty string")
    elif allowed_kinds is not None and obj["kind"] not in allowed_kinds:
        errors.append(f"unsupported kind: {obj['kind']}")
    for field in ["metadata", "spec", "status"]:
        _validate_object_field(obj, field, errors)
    metadata = obj.get("metadata") if isinstance(obj.get("metadata"), dict) else {}
    compatibility = metadata.get("compatibility")
    if compatibility is not None and not isinstance(compatibility, dict):
        errors.append("metadata.compatibility must be an object when present")
        compatibility = {}
    if isinstance(compatibility, dict):
        for key in ["schemaVersion", "protocolVersion", "minReaderVersion", "minWriterVersion"]:
            value = compatibility.get(key)
            if value is not None and not validate_semverish(str(value)):
                errors.append(f"metadata.compatibility.{key} must be SemVer-like")
        required = _as_list(compatibility.get("requiredCapabilities"))
        for capability in required:
            if capability not in RECOGNIZED_CAPABILITIES:
                errors.append(f"unknown required capability: {capability}")
    top_required = _as_list(obj.get("requiredCapabilities"))
    for capability in top_required:
        if capability not in RECOGNIZED_CAPABILITIES:
            errors.append(f"unknown required capability: {capability}")
    status = obj.get("status") if isinstance(obj.get("status"), dict) else {}
    capability_label = status.get("capability_label")
    if capability_label is not None and capability_label not in RECOGNIZED_CAPABILITIES:
        errors.append(f"unknown capability_label: {capability_label}")
    return errors


def load_envelope_schema(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(repo_root) if repo_root is not None else Path(".")
    return read_json(root / SCHEMA_PATH)


def _json_schema_type_matches(value: Any, expected: Any) -> bool:
    if isinstance(expected, list):
        return any(_json_schema_type_matches(value, item) for item in expected)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def _expected_type_label(expected: Any) -> str:
    if isinstance(expected, list):
        return "|".join(str(item) for item in expected)
    return str(expected)


def _schema_node_errors(value: Any, schema: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type is not None:
        if not _json_schema_type_matches(value, expected_type):
            errors.append(f"{path} must be {_expected_type_label(expected_type)}")
            return errors
    if isinstance(value, dict):
        required = schema.get("required", [])
        if required is not None and not isinstance(required, list):
            errors.append(f"{path}.required must be an array")
        else:
            for field in required:
                if not isinstance(field, str):
                    errors.append(f"{path}.required entries must be strings")
                elif field not in value:
                    errors.append(f"missing required field: {path}.{field}")
        properties = schema.get("properties", {})
        if properties is not None and not isinstance(properties, dict):
            errors.append(f"{path}.properties must be an object")
            properties = {}
        for key, child_schema in properties.items():
            if key in value:
                if isinstance(child_schema, dict):
                    errors.extend(_schema_node_errors(value[key], child_schema, f"{path}.{key}"))
                else:
                    errors.append(f"{path}.properties.{key} must be an object")
        additional = schema.get("additionalProperties", True)
        if additional is False:
            for key in value:
                if key not in properties:
                    errors.append(f"unknown field not allowed by schema: {path}.{key}")
        elif additional is not True and not isinstance(additional, dict):
            errors.append(f"{path}.additionalProperties must be boolean or object")
    if isinstance(value, list):
        item_schema = schema.get("items")
        if item_schema is not None:
            if not isinstance(item_schema, dict):
                errors.append(f"{path}.items must be an object")
            else:
                for index, item in enumerate(value):
                    errors.extend(_schema_node_errors(item, item_schema, f"{path}[{index}]"))
    return errors


def validate_envelope_with_schema(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    active_schema = schema if schema is not None else load_envelope_schema()
    if not isinstance(active_schema, dict):
        return ["schema must be an object"]
    return _schema_node_errors(obj, active_schema, "$")


def check_schema_helper_alignment(schema: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(schema, dict):
        return {
            "status": "FAILED_VALIDATION",
            "schema_helper_alignment_status": "FAILED_VALIDATION",
            "errors": ["schema must be an object"],
            "warnings": [],
            "expected_required_fields": ENVELOPE_REQUIRED_FIELDS,
            "schema_required_fields": [],
        }
    required = schema.get("required")
    schema_required = required if isinstance(required, list) else []
    missing = [field for field in ENVELOPE_REQUIRED_FIELDS if field not in schema_required]
    extra_required = [str(field) for field in schema_required if field not in ENVELOPE_REQUIRED_FIELDS]
    if required is None:
        errors.append("schema.required is missing")
    elif not isinstance(required, list):
        errors.append("schema.required must be an array")
    if missing:
        errors.append(f"schema.required missing helper-required fields: {', '.join(missing)}")
    if extra_required:
        warnings.append(f"schema declares extra required fields: {', '.join(extra_required)}")
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        errors.append("schema.properties must be an object")
        properties = {}
    expected_types = {
        "apiVersion": "string",
        "kind": "string",
        "metadata": "object",
        "spec": "object",
        "status": "object",
    }
    for field, expected_type in expected_types.items():
        field_schema = properties.get(field)
        if not isinstance(field_schema, dict):
            errors.append(f"schema.properties.{field} must be an object")
            continue
        if field_schema.get("type") != expected_type:
            errors.append(f"schema.properties.{field}.type must be {expected_type}")
    metadata_schema = properties.get("metadata", {}) if isinstance(properties.get("metadata"), dict) else {}
    compatibility_schema = metadata_schema.get("properties", {}).get("compatibility") if isinstance(metadata_schema.get("properties"), dict) else None
    if compatibility_schema is not None and not isinstance(compatibility_schema, dict):
        errors.append("schema.properties.metadata.properties.compatibility must be an object")
    status = "PASS" if not errors else "FAILED_VALIDATION"
    return {
        "status": status,
        "schema_helper_alignment_status": status,
        "errors": errors,
        "warnings": warnings,
        "expected_required_fields": ENVELOPE_REQUIRED_FIELDS,
        "schema_required_fields": [str(item) for item in schema_required],
        "missing_required_fields": missing,
        "extra_required_fields": extra_required,
        "checked_properties": sorted(expected_types),
    }


def validate_envelope_runtime(
    obj: dict[str, Any],
    schema: dict[str, Any] | None = None,
    allowed_kinds: set[str] | None = None,
) -> dict[str, Any]:
    active_schema = schema if schema is not None else load_envelope_schema()
    helper_errors = validate_envelope(obj, allowed_kinds)
    schema_errors = validate_envelope_with_schema(obj, active_schema)
    status = "PASS" if not helper_errors and not schema_errors else "FAILED_VALIDATION"
    return {
        "status": status,
        "schema_validation_executed": True,
        "schema_validation_mode": SCHEMA_VALIDATION_MODE,
        "helper_validation_errors": helper_errors,
        "schema_validation_errors": schema_errors,
        "helper_valid": not helper_errors,
        "schema_valid": not schema_errors,
    }


def sample_optional_field_envelope() -> dict[str, Any]:
    obj = build_envelope(
        "LifecycleFixtureRunReport",
        {"id": "optional-field-probe"},
        {"scenario_id": "install-managed-section", "mode": "apply-temp"},
        {"phase": "PASS", "capability_label": "fixture_temp_apply_only"},
    )
    obj["x-aide-optional-probe"] = {"tolerated": True}
    metadata = obj.get("metadata")
    if isinstance(metadata, dict):
        metadata["x-aide-optional-probe"] = "tolerated"
    return obj


def sample_unknown_required_capability_envelope() -> dict[str, Any]:
    obj = build_envelope(
        "LifecycleFixtureRunReport",
        {"id": "unknown-required-capability-probe"},
        {"scenario_id": "install-managed-section", "mode": "apply-temp"},
        {"phase": "PASS", "capability_label": "fixture_temp_apply_only"},
    )
    metadata = obj.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("compatibility"), dict):
        metadata["compatibility"]["requiredCapabilities"] = ["future.required"]
    return obj


def _source_path_value(source_path: Path | None) -> str:
    return source_path.as_posix() if source_path is not None else ""


def _source_metadata(report: dict[str, Any], source_path: Path | None, default_id: str) -> dict[str, Any]:
    capability = str(report.get("capability_label") or "fixture_temp_apply_only")
    feature_flags = [capability] if capability else []
    return {
        "id": str(report.get("run_id") or report.get("task_id") or default_id),
        "name": default_id,
        "createdAt": str(report.get("created_at") or report.get("generated_at") or "deterministic"),
        "sourcePath": _source_path_value(source_path),
        "producer": {
            "name": PRODUCER_NAME,
            "version": PRODUCER_VERSION,
        },
        "compatibility": {
            "schemaVersion": PROTOCOL_VERSION,
            "protocolVersion": str(report.get("protocol_version") or PROTOCOL_VERSION)
            if validate_semverish(str(report.get("protocol_version") or PROTOCOL_VERSION))
            else PROTOCOL_VERSION,
            "minReaderVersion": PROTOCOL_VERSION,
            "minWriterVersion": PROTOCOL_VERSION,
            "featureFlags": feature_flags,
            "requiredCapabilities": feature_flags,
            "sourceSchemaVersion": str(report.get("schema_version", "")),
        },
    }


def _explicit_non_capabilities(report: dict[str, Any]) -> list[str]:
    observed = report.get("not_capabilities", [])
    if not isinstance(observed, list):
        observed = []
    return sorted({str(item) for item in [*observed, *EXPLICIT_NON_CAPABILITIES] if str(item)})


def project_lifecycle_run_report(report: dict[str, Any], source_path: Path | None = None) -> dict[str, Any]:
    metadata = _source_metadata(report, source_path, "lifecycle-fixture-latest-run")
    spec = {
        "scenario_id": report.get("scenario_id", ""),
        "mode": report.get("mode", ""),
        "operation_type": report.get("operation_type", ""),
        "mutation_scope": report.get("mutation_scope", ""),
        "source_report_path": _source_path_value(source_path),
    }
    status = {
        "phase": report.get("status", ""),
        "result": report.get("result", report.get("status", "")),
        "capability_label": report.get("capability_label", ""),
        "explicit_non_capabilities": _explicit_non_capabilities(report),
        "canonical_fixture_mutated": report.get("canonical_fixture_mutated"),
        "temp_fixture_mutated": report.get("temp_fixture_mutated"),
        "target_repo_mutated": report.get("target_repo_mutated"),
        "active_repo_apply_mutation": report.get("active_repo_apply_mutation"),
        "rollback_execution_implemented": report.get("rollback_execution_implemented"),
        "rollback_executed": report.get("rollback_executed"),
    }
    return build_envelope("LifecycleFixtureRunReport", metadata, spec, status)


def project_lifecycle_verify_report(report: dict[str, Any], source_path: Path | None = None) -> dict[str, Any]:
    metadata = _source_metadata(report, source_path, "lifecycle-fixture-verify")
    spec = {
        "verified_run_id": report.get("verified_run_id", report.get("run_id", "")),
        "verified_report_path": report.get("verified_report_path", ""),
        "source_report_path": _source_path_value(source_path),
    }
    status = {
        "phase": report.get("status", ""),
        "result": report.get("result", report.get("status", "")),
        "capability_label": report.get("capability_label", ""),
        "explicit_non_capabilities": _explicit_non_capabilities(report),
        "latest_run_report_parsed": report.get("latest_run_report_parsed"),
        "report_hashes_match_observed_files": report.get("report_hashes_match_observed_files"),
        "canonical_fixture_unchanged": report.get("canonical_fixture_unchanged"),
        "temp_postimage_matches_expected": report.get("temp_postimage_matches_expected"),
        "manual_content_preserved": report.get("manual_content_preserved"),
        "no_overclaiming_detected": report.get("no_overclaiming_detected"),
        "unsupported_capabilities_not_claimed": report.get("unsupported_capabilities_not_claimed"),
    }
    return build_envelope("LifecycleFixtureVerifyReport", metadata, spec, status)


def project_acceptance_report(report: dict[str, Any], source_path: Path | None = None) -> dict[str, Any]:
    accepted = report.get("accepted_capability", {}) if isinstance(report.get("accepted_capability"), dict) else {}
    metadata = _source_metadata(
        {"capability_label": accepted.get("capability_label"), "task_id": report.get("task_id"), "schema_version": report.get("schema_version")},
        source_path,
        "lifecycle-fixture-acceptance",
    )
    spec = {
        "reviewed_tasks": report.get("reviewed_tasks", []),
        "reviewed_commits": report.get("reviewed_commits", []),
        "accepted_capability": accepted,
        "source_report_path": _source_path_value(source_path),
    }
    status = {
        "phase": report.get("status", ""),
        "decision": report.get("decision", report.get("status", "")),
        "capability_label": accepted.get("capability_label", ""),
        "explicit_non_capabilities": _explicit_non_capabilities({"not_capabilities": report.get("explicit_non_capabilities", [])}),
        "forbidden_operations_preserved": report.get("forbidden_operations_preserved", {}),
        "warnings": report.get("warnings", []),
    }
    return build_envelope("LifecycleFixtureAcceptanceReport", metadata, spec, status)


def source_report_paths(repo_root: Path) -> dict[str, Path]:
    return {
        "lifecycle_run": repo_root / LIFECYCLE_RUN_SOURCE,
        "lifecycle_verify": repo_root / LIFECYCLE_VERIFY_SOURCE,
        "lifecycle_acceptance": repo_root / LIFECYCLE_ACCEPTANCE_SOURCE,
    }


def _relative_posix(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def project_lifecycle_fixture_runner(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    paths = source_report_paths(root)
    projections: dict[str, dict[str, Any]] = {}
    run = read_json(paths["lifecycle_run"])
    verify = read_json(paths["lifecycle_verify"])
    projections[LIFECYCLE_RUN_PROJECTION.as_posix()] = project_lifecycle_run_report(run, LIFECYCLE_RUN_SOURCE)
    projections[LIFECYCLE_VERIFY_PROJECTION.as_posix()] = project_lifecycle_verify_report(verify, LIFECYCLE_VERIFY_SOURCE)
    if paths["lifecycle_acceptance"].exists():
        acceptance = read_json(paths["lifecycle_acceptance"])
        projections[LIFECYCLE_ACCEPTANCE_PROJECTION.as_posix()] = project_acceptance_report(
            acceptance,
            LIFECYCLE_ACCEPTANCE_SOURCE,
        )
    for rel, obj in projections.items():
        write_json(root / rel, obj)
    write_future_and_unfinished_reports(root)
    return {
        "status": "PASS",
        "projections_written": sorted(projections),
        "source_reports_checked": [_relative_posix(path, root) for path in paths.values() if path.exists()],
    }


def contract_envelope_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    paths = source_report_paths(root)
    schema_path = root / SCHEMA_PATH
    data = {
        "schema_version": "aide.contract-envelope-status.v0",
        "report_type": "contract_envelope_status",
        "status": "PASS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "schema_file_exists": schema_path.exists(),
        "schema_validation_mode": SCHEMA_VALIDATION_MODE,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "recognized_capabilities": sorted(RECOGNIZED_CAPABILITIES),
        "source_reports": {key: path.exists() for key, path in paths.items()},
        "destructive_migration_performed": False,
        "target_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    write_future_and_unfinished_reports(root)
    return data


def contract_envelope_validate(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    projection_result = project_lifecycle_fixture_runner(root) if project else {"projections_written": []}
    projections = [root / rel for rel in projection_result.get("projections_written", [])]
    validation_results: list[dict[str, Any]] = []
    schema_path = root / SCHEMA_PATH
    schema_file_loaded = False
    schema_file_parsed = False
    schema_validation_executed = False
    schema_load_errors: list[str] = []
    alignment_errors: list[str] = []
    alignment_warnings: list[str] = []
    alignment_result: dict[str, Any] = {}
    helper_validation_errors: dict[str, list[str]] = {}
    schema_validation_errors: dict[str, list[str]] = {}
    runtime_validation_results: list[dict[str, Any]] = []
    try:
        schema = load_envelope_schema(root)
        schema_file_loaded = True
        schema_file_parsed = True
    except ValueError as exc:
        schema = {}
        schema_load_errors.append(str(exc))
    if schema_file_parsed:
        alignment_result = check_schema_helper_alignment(schema)
        alignment_errors = list(alignment_result.get("errors", []))
        alignment_warnings = list(alignment_result.get("warnings", []))
    for projection_path in projections:
        obj = read_json(projection_path)
        helper_errors = validate_envelope(obj, SUPPORTED_KINDS)
        schema_errors: list[str] = []
        if schema_file_parsed:
            runtime = validate_envelope_runtime(obj, schema, SUPPORTED_KINDS)
            schema_validation_executed = True
            helper_errors = runtime["helper_validation_errors"]
            schema_errors = runtime["schema_validation_errors"]
            runtime_validation_results.append(
                {
                    "path": projection_path.relative_to(root).as_posix(),
                    "result": runtime["status"],
                    "helper_valid": runtime["helper_valid"],
                    "schema_valid": runtime["schema_valid"],
                }
            )
        else:
            schema_errors = schema_load_errors
        errors = [*helper_errors, *schema_errors]
        helper_validation_errors[projection_path.relative_to(root).as_posix()] = helper_errors
        schema_validation_errors[projection_path.relative_to(root).as_posix()] = schema_errors
        validation_results.append(
            {
                "path": projection_path.relative_to(root).as_posix(),
                "result": "PASS" if not errors else "FAIL",
                "errors": errors,
                "helper_validation_errors": helper_errors,
                "schema_validation_errors": schema_errors,
            }
        )
    sources = source_report_paths(root)
    run_report = read_json(sources["lifecycle_run"])
    verify_report = read_json(sources["lifecycle_verify"])
    compatibility_results = {
        "latest_run_json_parses": True,
        "verify_json_parses": True,
        "latest_run_top_level_status_scalar_preserved": isinstance(run_report.get("status"), str),
        "verify_top_level_status_scalar_preserved": isinstance(verify_report.get("status"), str),
        "latest_run_legacy_capability_label_preserved": run_report.get("capability_label") == "fixture_temp_apply_only",
        "verify_legacy_capability_label_preserved": verify_report.get("capability_label") == "fixture_temp_apply_only",
        "source_reports_destructively_migrated": False,
    }
    unknown_optional_envelope = sample_optional_field_envelope()
    unknown_required_envelope = sample_unknown_required_capability_envelope()
    optional_runtime = (
        validate_envelope_runtime(unknown_optional_envelope, schema, SUPPORTED_KINDS)
        if schema_file_parsed
        else {"status": "FAILED_VALIDATION", "helper_validation_errors": [], "schema_validation_errors": schema_load_errors}
    )
    required_runtime = (
        validate_envelope_runtime(unknown_required_envelope, schema, SUPPORTED_KINDS)
        if schema_file_parsed
        else {"status": "FAILED_VALIDATION", "helper_validation_errors": schema_load_errors, "schema_validation_errors": schema_load_errors}
    )
    if schema_file_parsed:
        schema_validation_executed = True
    unknown_optional_fields_tolerated = optional_runtime.get("status") == "PASS"
    unknown_required_capability_fails_closed = bool(required_runtime.get("helper_validation_errors"))
    compatibility_pass = all(
        value is True
        for key, value in compatibility_results.items()
        if key != "source_reports_destructively_migrated"
    ) and compatibility_results["source_reports_destructively_migrated"] is False
    schema_checks_pass = (
        schema_path.exists()
        and schema_file_loaded
        and schema_file_parsed
        and schema_validation_executed
        and not schema_load_errors
        and not alignment_errors
        and unknown_optional_fields_tolerated
        and unknown_required_capability_fails_closed
    )
    status = (
        "PASS"
        if all(item["result"] == "PASS" for item in validation_results) and compatibility_pass and schema_checks_pass
        else "FAILED_VALIDATION"
    )
    report = {
        "schema_version": "aide.contract-envelope-validation.v0",
        "report_type": "contract_envelope_validation",
        "task_id": "AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01",
        "status": status,
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "schema_file_exists": schema_path.exists(),
        "schema_file_loaded": schema_file_loaded,
        "schema_file_parsed": schema_file_parsed,
        "schema_validation_executed": schema_validation_executed,
        "schema_validation_mode": SCHEMA_VALIDATION_MODE if schema_validation_executed else "unavailable",
        "schema_helper_alignment_checked": schema_file_parsed,
        "schema_helper_alignment_status": alignment_result.get("schema_helper_alignment_status", "FAILED_VALIDATION"),
        "schema_validation_limitations": SCHEMA_VALIDATION_LIMITATIONS,
        "helper_validation_errors": helper_validation_errors,
        "schema_validation_errors": schema_validation_errors,
        "schema_load_errors": schema_load_errors,
        "alignment_errors": alignment_errors,
        "alignment_warnings": alignment_warnings,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "recognized_capabilities": sorted(RECOGNIZED_CAPABILITIES),
        "source_reports_checked": projection_result.get("source_reports_checked", []),
        "projections_checked": [item["path"] for item in validation_results],
        "projections_written": projection_result.get("projections_written", []),
        "validation_results": validation_results,
        "runtime_validation_results": runtime_validation_results,
        "compatibility_results": compatibility_results,
        "backwards_compatibility_preserved": compatibility_pass,
        "destructive_migration_performed": False,
        "unknown_optional_fields_tolerated": unknown_optional_fields_tolerated,
        "unknown_required_capability_fails_closed": unknown_required_capability_fails_closed,
        "forbidden_operations_preserved": forbidden_operations_preserved(),
        "warnings": [
            "Minimal envelope helper is v1alpha1 and is not a full protocol stability claim.",
            "Minimal schema subset validation is executed; full JSON Schema Draft 2020-12 validation remains future work.",
            "WorkUnit, EvidencePacket, TestJob, Checkpoint, ProviderAdapter, Service, and Commander schemas remain future work.",
            *alignment_warnings,
        ],
        "unfinished_work": unfinished_work_items(),
        "future_work": future_work_items(),
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_markdown(report))
    write_future_and_unfinished_reports(root)
    return report


def forbidden_operations_preserved() -> dict[str, bool]:
    return {
        "evidencepacket_schema": True,
        "workunit_schema": True,
        "workunit_cli": True,
        "testjob_schema": True,
        "test_broker": True,
        "service": True,
        "commander": True,
        "provider_adapters": True,
        "branch_worktree_automation": True,
        "target_repo_apply": True,
        "active_repo_apply": True,
        "rollback_execution": True,
        "release": True,
        "promotion": True,
        "merge": True,
        "push": True,
        "network": True,
        "gateway": True,
        "github_mutation": True,
        "model_provider_calls": True,
    }


def future_work_items() -> list[dict[str, str]]:
    return [
        {"task": "AIDE-CHECK-CONTRACT-ENVELOPE-HARDEN-01", "reason": "independent review of schema runtime loading, helper/schema alignment, compatibility, tests, and no-overclaiming"},
        {"task": "AIDE-ACCEPT-CONTRACT-ENVELOPE-01", "reason": "accept the envelope only after the hardening check passes"},
        {"task": "AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01", "reason": "extract minimal EvidencePacket shape after the envelope is accepted"},
        {"task": "AIDE-BUILD-WORKUNIT-QUEUE-V1-01", "reason": "define minimal queue WorkUnit object after envelope and evidence shapes are accepted"},
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    deferred = [
        "WorkUnit schema",
        "EvidencePacket schema",
        "TestJob schema",
        "Checkpoint schema",
        "PromotionPolicy schema",
        "WorkUnit CLI",
        "Test Broker",
        "Service",
        "Commander",
        "provider adapters",
        "branch/worktree allocator",
        "target repo apply",
        "rollback execution",
        "release/promotion",
        "OpenTelemetry",
        "SARIF",
        "SPDX",
        "CycloneDX",
        "SLSA",
        "in-toto",
        "OpenAPI",
    ]
    return [{"item": item, "reason": "intentionally deferred beyond the minimal envelope slice"} for item in deferred]


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Contract Envelope Status",
        "",
        f"- status: {data.get('status')}",
        f"- api_version: {data.get('api_version')}",
        f"- protocol_version: {data.get('protocol_version')}",
        f"- schema_file_path: {data.get('schema_file_path')}",
        f"- schema_file_exists: {str(data.get('schema_file_exists', False)).lower()}",
        f"- schema_validation_mode: {data.get('schema_validation_mode')}",
        "- destructive_migration_performed: false",
        "- target_mutation: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "",
        "## Supported Kinds",
        "",
    ]
    for kind in data.get("supported_kinds", []):
        lines.append(f"- {kind}")
    lines.extend(["", "## Recognized Capabilities", ""])
    for capability in data.get("recognized_capabilities", []):
        lines.append(f"- {capability}")
    lines.extend(["", "## Source Reports", ""])
    reports = data.get("source_reports", {}) if isinstance(data.get("source_reports"), dict) else {}
    for key, present in reports.items():
        lines.append(f"- {key}: {str(present).lower()}")
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Contract Envelope Validation",
        "",
        f"- status: {report.get('status')}",
        f"- api_version: {report.get('api_version')}",
        f"- protocol_version: {report.get('protocol_version')}",
        f"- schema_file_path: {report.get('schema_file_path')}",
        f"- schema_file_loaded: {str(report.get('schema_file_loaded', False)).lower()}",
        f"- schema_file_parsed: {str(report.get('schema_file_parsed', False)).lower()}",
        f"- schema_validation_executed: {str(report.get('schema_validation_executed', False)).lower()}",
        f"- schema_validation_mode: {report.get('schema_validation_mode')}",
        f"- schema_helper_alignment_checked: {str(report.get('schema_helper_alignment_checked', False)).lower()}",
        f"- schema_helper_alignment_status: {report.get('schema_helper_alignment_status')}",
        "- destructive_migration_performed: false",
        f"- backwards_compatibility_preserved: {str(report.get('backwards_compatibility_preserved', False)).lower()}",
        f"- unknown_optional_fields_tolerated: {str(report.get('unknown_optional_fields_tolerated', False)).lower()}",
        f"- unknown_required_capability_fails_closed: {str(report.get('unknown_required_capability_fails_closed', False)).lower()}",
        "",
        "## Projections",
        "",
    ]
    for rel in report.get("projections_written", []):
        lines.append(f"- {rel}")
    lines.extend(["", "## Validation Results", ""])
    for item in report.get("validation_results", []):
        lines.append(f"- {item.get('result')}: {item.get('path')}")
    lines.extend(["", "## Compatibility", ""])
    compatibility = report.get("compatibility_results", {}) if isinstance(report.get("compatibility_results"), dict) else {}
    for key, value in compatibility.items():
        lines.append(f"- {key}: {str(value).lower()}")
    lines.extend(["", "## Schema Alignment", ""])
    for error in report.get("alignment_errors", []):
        lines.append(f"- error: {error}")
    if not report.get("alignment_errors"):
        lines.append("- alignment_errors: none")
    lines.extend(["", "## Schema Validation Limitations", ""])
    for limitation in report.get("schema_validation_limitations", []):
        lines.append(f"- {limitation}")
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def write_future_and_unfinished_reports(repo_root: Path) -> None:
    future_lines = [
        "# Contract Envelope Future Work",
        "",
        "## Recommended Order",
        "",
    ]
    for index, item in enumerate(future_work_items(), start=1):
        future_lines.append(f"{index}. {item['task']}: {item['reason']}.")
    unfinished_lines = [
        "# Contract Envelope Unfinished Work",
        "",
        "## Finished In This Slice",
        "",
        "- Minimal envelope builder and validator.",
        "- Lifecycle fixture run, verify, and acceptance report projections.",
        "- Additive validation reports under `.aide/reports/contract-envelope/`.",
        "",
        "## Intentionally Deferred",
        "",
    ]
    for item in unfinished_work_items():
        unfinished_lines.append(f"- {item['item']}: {item['reason']}.")
    write_text(repo_root / FUTURE_WORK_MD, "\n".join(future_lines) + "\n")
    write_text(repo_root / UNFINISHED_WORK_MD, "\n".join(unfinished_lines) + "\n")
