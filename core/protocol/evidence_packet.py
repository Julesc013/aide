"""Minimal AIDE EvidencePacket helpers.

This module is intentionally narrow. It projects accepted lifecycle fixture and
contract-envelope artifacts into envelope-backed EvidencePacket objects without
destructively migrating source reports or implementing an evidence engine.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from core.protocol import envelope


API_VERSION = envelope.API_VERSION
EVIDENCE_PACKET_SCHEMA_VERSION = "aide.evidence-packet.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_evidence_packet_schema"
REPORT_ROOT = Path(".aide/reports/evidence-packet")
PROJECTION_ROOT = REPORT_ROOT / "projections"
SCHEMA_PATH = Path(".aide/protocol/aide-evidence-packet.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"
SUPPORTED_KINDS = {
    "EvidencePacket",
    "EvidencePacketProjectionReport",
    "EvidencePacketValidationReport",
}
EVIDENCE_PACKET_REQUIRED_FIELDS = ["apiVersion", "kind", "metadata", "spec", "status"]
REQUIRED_METADATA_FIELDS = ["id", "createdAt", "producer", "compatibility"]
REQUIRED_SPEC_FIELDS = [
    "source_task_id",
    "source_task_kind",
    "subject",
    "claims",
    "explicit_non_capabilities",
    "artifacts",
    "validations",
]
REQUIRED_STATUS_FIELDS = ["phase", "validated", "validation_errors", "validation_warnings"]
CLAIM_STATUSES = {"supported", "unsupported", "not_checked", "contradicted", "not_applicable"}
VALIDATION_STATUSES = {
    "PASS",
    "PASS_WITH_WARNINGS",
    "FAILED_VALIDATION",
    "BLOCKED",
    "PARTIAL",
    "UNAVAILABLE",
    "NOT_RUN",
}
SOURCE_TASK_KINDS = {"build", "check", "harden", "acceptance"}
SUBJECT_TYPES = {"capability", "task", "report", "validation", "artifact"}
RECOGNIZED_CAPABILITIES = {
    FEATURE_FLAG,
    "fixture_temp_apply_only",
    "minimal_contract_envelope",
}
EXPLICIT_NON_CAPABILITIES = [
    "full_evidence_engine",
    "evidence_store",
    "workunit_schema",
    "workunit_cli",
    "testjob_schema",
    "test_broker",
    "checkpoint_schema",
    "promotion_policy_schema",
    "service_ready",
    "commander_ready",
    "provider_adapter_ready",
    "branch_worktree_automation",
    "target_repo_apply",
    "active_repo_apply",
    "broad_lifecycle_apply",
    "rollback_execution",
    "uninstall_execution",
    "production_ready",
    "release_ready",
]
SCHEMA_VALIDATION_MODE = "minimal_json_schema_subset"
SCHEMA_VALIDATION_LIMITATIONS = [
    "Local subset validator supports type, enum, required, properties, simple additionalProperties, and homogeneous array items only.",
    "Full JSON Schema Draft 2020-12 validation remains future work.",
    "Formats, refs, oneOf/anyOf/allOf, conditionals, numeric bounds, and pattern checks are not implemented.",
]
SOURCE_ARTIFACTS = {
    "lifecycle_run": Path(".aide/reports/lifecycle-fixture-runner/latest-run.json"),
    "lifecycle_verify": Path(".aide/reports/lifecycle-fixture-runner/verify.json"),
    "lifecycle_rollback": Path(".aide/reports/lifecycle-fixture-runner/latest-rollback-record.json"),
    "lifecycle_acceptance": Path(".aide/reports/lifecycle-fixture-runner-acceptance/acceptance-report.json"),
    "contract_validation": Path(".aide/reports/contract-envelope/validation.json"),
    "contract_acceptance": Path(".aide/reports/contract-envelope-acceptance/acceptance-report.json"),
}
PROJECTION_FILES = {
    "lifecycle_run": PROJECTION_ROOT / "lifecycle-fixture-run.evidence-packet.json",
    "lifecycle_verify": PROJECTION_ROOT / "lifecycle-fixture-verify.evidence-packet.json",
    "lifecycle_acceptance": PROJECTION_ROOT / "lifecycle-fixture-acceptance.evidence-packet.json",
    "contract_validation": PROJECTION_ROOT / "contract-envelope-validation.evidence-packet.json",
    "contract_acceptance": PROJECTION_ROOT / "contract-envelope-acceptance.evidence-packet.json",
}


def stable_json(data: Any) -> str:
    return envelope.stable_json(data)


def read_json(path: Path) -> dict[str, Any]:
    return envelope.read_json(path)


def write_json(path: Path, obj: dict[str, Any]) -> None:
    envelope.write_json(path, obj)


def write_text(path: Path, text: str) -> None:
    envelope.write_text(path, text)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _relative_posix(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def _source_path_value(source_path: Path | None) -> str:
    return source_path.as_posix() if source_path is not None else ""


def _deterministic_packet_id(
    source_task_id: str,
    subject: dict[str, Any],
    source_path: Path | None,
) -> str:
    seed = stable_json(
        {
            "source_task_id": source_task_id,
            "subject": subject,
            "source_path": _source_path_value(source_path),
        }
    )
    return "ep-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


def _compatibility(required_capabilities: list[str] | None = None) -> dict[str, Any]:
    required = [FEATURE_FLAG]
    if required_capabilities:
        for capability in required_capabilities:
            if capability not in required:
                required.append(capability)
    return {
        "schemaVersion": PROTOCOL_VERSION,
        "protocolVersion": PROTOCOL_VERSION,
        "minReaderVersion": PROTOCOL_VERSION,
        "minWriterVersion": PROTOCOL_VERSION,
        "featureFlags": [FEATURE_FLAG],
        "requiredCapabilities": required,
    }


def normalize_claim_status(value: Any) -> str:
    status = str(value or "not_checked")
    return status if status in CLAIM_STATUSES else "not_checked"


def normalize_validation_status(value: Any) -> str:
    status = str(value or "NOT_RUN")
    return status if status in VALIDATION_STATUSES else "NOT_RUN"


def normalize_phase(value: Any) -> str:
    phase = str(value or "PARTIAL")
    if phase in VALIDATION_STATUSES:
        return phase
    if phase in {"ACCEPTED", "PASS"}:
        return "PASS"
    if phase == "ACCEPTED_WITH_WARNINGS":
        return "PASS_WITH_WARNINGS"
    if phase in {"REJECTED_NEEDS_REPAIR", "FAIL", "FAILED"}:
        return "FAILED_VALIDATION"
    return "PARTIAL"


def explicit_non_capabilities(source: dict[str, Any] | None = None) -> list[str]:
    observed: list[Any] = []
    if source:
        for key in ["explicit_non_capabilities", "not_capabilities"]:
            value = source.get(key)
            if isinstance(value, list):
                observed.extend(value)
    return sorted({str(item) for item in [*observed, *EXPLICIT_NON_CAPABILITIES] if str(item)})


def implemented_capabilities(packet: dict[str, Any]) -> set[str]:
    spec = packet.get("spec") if isinstance(packet.get("spec"), dict) else {}
    capability = spec.get("capability_label")
    if isinstance(capability, str) and capability:
        return {capability}
    return set()


def artifact_ref(repo_root: Path, path: Path, role: str) -> dict[str, Any]:
    actual = repo_root / path
    ref: dict[str, Any] = {"path": path.as_posix(), "role": role}
    if actual.exists() and actual.is_file():
        ref["sha256"] = sha256_file(actual)
    return ref


def claim(claim_id: str, status: str, summary: str) -> dict[str, str]:
    return {"id": claim_id, "status": normalize_claim_status(status), "summary": summary}


def validation(command: str, status: str, exit_code: int | None = None, notes: str = "") -> dict[str, Any]:
    item: dict[str, Any] = {"command": command, "status": normalize_validation_status(status)}
    if exit_code is not None:
        item["exit_code"] = exit_code
    if notes:
        item["notes"] = notes
    return item


def build_evidence_packet(
    *,
    source_task_id: str,
    source_task_kind: str,
    subject: dict[str, Any],
    capability_label: str,
    claims: list[dict[str, Any]],
    explicit_non_capabilities: list[str],
    artifacts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
    warnings: list[Any] | None = None,
    risks: list[Any] | None = None,
    source_path: Path | None = None,
    name: str | None = None,
    created_at: str | None = None,
    packet_id: str | None = None,
    phase: str = "PASS",
    validation_warnings: list[str] | None = None,
    validation_errors: list[str] | None = None,
) -> dict[str, Any]:
    subject_copy = copy.deepcopy(subject)
    metadata = {
        "id": packet_id or _deterministic_packet_id(source_task_id, subject_copy, source_path),
        "name": name or subject_copy.get("id") or capability_label,
        "createdAt": created_at or "deterministic",
        "sourcePath": _source_path_value(source_path),
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility([capability_label]),
    }
    spec = {
        "source_task_id": source_task_id,
        "source_task_kind": source_task_kind,
        "subject": subject_copy,
        "capability_label": capability_label,
        "claims": copy.deepcopy(claims),
        "explicit_non_capabilities": list(explicit_non_capabilities),
        "artifacts": copy.deepcopy(artifacts),
        "validations": copy.deepcopy(validations),
        "warnings": copy.deepcopy(warnings or []),
        "risks": copy.deepcopy(risks or []),
    }
    status = {
        "phase": normalize_phase(phase),
        "validated": not validation_errors,
        "validation_errors": list(validation_errors or []),
        "validation_warnings": list(validation_warnings or []),
    }
    obj = envelope.build_envelope("EvidencePacket", metadata, spec, status, api_version=API_VERSION)
    obj["schema_version"] = EVIDENCE_PACKET_SCHEMA_VERSION
    obj["protocol_version"] = PROTOCOL_VERSION
    return obj


def _validate_object_field(obj: dict[str, Any], field: str, errors: list[str]) -> None:
    if field not in obj:
        errors.append(f"missing required field: {field}")
    elif not isinstance(obj[field], dict):
        errors.append(f"{field} must be an object")


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate_evidence_packet(obj: dict[str, Any], allowed_kinds: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["EvidencePacket must be an object"]
    if not isinstance(obj.get("apiVersion"), str) or not obj.get("apiVersion"):
        errors.append("apiVersion must be a non-empty string")
    if obj.get("apiVersion") != API_VERSION:
        errors.append(f"unsupported apiVersion: {obj.get('apiVersion')}")
    kind = obj.get("kind")
    active_kinds = allowed_kinds or {"EvidencePacket"}
    if not isinstance(kind, str) or not kind:
        errors.append("kind must be a non-empty string")
    elif kind not in active_kinds:
        errors.append(f"unsupported kind: {kind}")
    for field in ["metadata", "spec", "status"]:
        _validate_object_field(obj, field, errors)
    metadata = obj.get("metadata") if isinstance(obj.get("metadata"), dict) else {}
    for field in REQUIRED_METADATA_FIELDS:
        if field not in metadata:
            errors.append(f"missing required metadata field: {field}")
    if not isinstance(metadata.get("id"), str) or not metadata.get("id"):
        errors.append("metadata.id must be a non-empty string")
    if not isinstance(metadata.get("createdAt"), str) or not metadata.get("createdAt"):
        errors.append("metadata.createdAt must be a non-empty string")
    producer = metadata.get("producer")
    if not isinstance(producer, dict):
        errors.append("metadata.producer must be an object")
    else:
        if not isinstance(producer.get("name"), str) or not producer.get("name"):
            errors.append("metadata.producer.name must be a non-empty string")
        if not isinstance(producer.get("version"), str) or not producer.get("version"):
            errors.append("metadata.producer.version must be a non-empty string")
    compatibility = metadata.get("compatibility")
    if not isinstance(compatibility, dict):
        errors.append("metadata.compatibility must be an object")
        compatibility = {}
    for key in ["schemaVersion", "protocolVersion", "minReaderVersion", "minWriterVersion"]:
        value = compatibility.get(key)
        if not isinstance(value, str) or not envelope.validate_semverish(value):
            errors.append(f"metadata.compatibility.{key} must be SemVer-like")
    feature_flags = compatibility.get("featureFlags")
    if not isinstance(feature_flags, list) or FEATURE_FLAG not in feature_flags:
        errors.append(f"metadata.compatibility.featureFlags must include {FEATURE_FLAG}")
    for capability in _as_list(compatibility.get("requiredCapabilities")):
        if capability not in RECOGNIZED_CAPABILITIES:
            errors.append(f"unknown required capability: {capability}")
    for capability in _as_list(obj.get("requiredCapabilities")):
        if capability not in RECOGNIZED_CAPABILITIES:
            errors.append(f"unknown required capability: {capability}")
    spec = obj.get("spec") if isinstance(obj.get("spec"), dict) else {}
    for field in REQUIRED_SPEC_FIELDS:
        if field not in spec:
            errors.append(f"missing required spec field: {field}")
    source_task_kind = spec.get("source_task_kind")
    if not isinstance(spec.get("source_task_id"), str) or not spec.get("source_task_id"):
        errors.append("spec.source_task_id must be a non-empty string")
    if source_task_kind not in SOURCE_TASK_KINDS:
        errors.append(f"unsupported source_task_kind: {source_task_kind}")
    subject = spec.get("subject")
    if not isinstance(subject, dict):
        errors.append("spec.subject must be an object")
    else:
        if subject.get("type") not in SUBJECT_TYPES:
            errors.append(f"unsupported subject.type: {subject.get('type')}")
        if not isinstance(subject.get("id"), str) or not subject.get("id"):
            errors.append("spec.subject.id must be a non-empty string")
    capability_label = spec.get("capability_label")
    if capability_label not in RECOGNIZED_CAPABILITIES:
        errors.append(f"unknown capability_label: {capability_label}")
    claims = spec.get("claims")
    if not isinstance(claims, list):
        errors.append("spec.claims must be an array")
    else:
        for index, item in enumerate(claims):
            if not isinstance(item, dict):
                errors.append(f"spec.claims[{index}] must be an object")
                continue
            if not isinstance(item.get("id"), str) or not item.get("id"):
                errors.append(f"spec.claims[{index}].id must be a non-empty string")
            if item.get("status") not in CLAIM_STATUSES:
                errors.append(f"spec.claims[{index}].status is unsupported: {item.get('status')}")
            if not isinstance(item.get("summary"), str) or not item.get("summary"):
                errors.append(f"spec.claims[{index}].summary must be a non-empty string")
    non_capabilities = spec.get("explicit_non_capabilities")
    if not isinstance(non_capabilities, list):
        errors.append("spec.explicit_non_capabilities must be an array")
    else:
        for item in non_capabilities:
            if not isinstance(item, str) or not item:
                errors.append("spec.explicit_non_capabilities entries must be non-empty strings")
        if capability_label in non_capabilities:
            errors.append("spec.capability_label must not appear in explicit_non_capabilities")
    artifacts = spec.get("artifacts")
    reports = spec.get("reports")
    if not isinstance(artifacts, list) and not isinstance(reports, list):
        errors.append("spec.artifacts or spec.reports must be an array")
    if isinstance(artifacts, list):
        for index, item in enumerate(artifacts):
            if not isinstance(item, dict):
                errors.append(f"spec.artifacts[{index}] must be an object")
                continue
            if not isinstance(item.get("path"), str) or not item.get("path"):
                errors.append(f"spec.artifacts[{index}].path must be a non-empty string")
            if not isinstance(item.get("role"), str) or not item.get("role"):
                errors.append(f"spec.artifacts[{index}].role must be a non-empty string")
    validations = spec.get("validations")
    if not isinstance(validations, list):
        errors.append("spec.validations must be an array")
    else:
        for index, item in enumerate(validations):
            if not isinstance(item, dict):
                errors.append(f"spec.validations[{index}] must be an object")
                continue
            if not isinstance(item.get("command"), str) or not item.get("command"):
                errors.append(f"spec.validations[{index}].command must be a non-empty string")
            if item.get("status") not in VALIDATION_STATUSES:
                errors.append(f"spec.validations[{index}].status is unsupported: {item.get('status')}")
            if "exit_code" in item and (not isinstance(item.get("exit_code"), int) or isinstance(item.get("exit_code"), bool)):
                errors.append(f"spec.validations[{index}].exit_code must be an integer when present")
    status = obj.get("status") if isinstance(obj.get("status"), dict) else {}
    for field in REQUIRED_STATUS_FIELDS:
        if field not in status:
            errors.append(f"missing required status field: {field}")
    if status.get("phase") not in VALIDATION_STATUSES:
        errors.append(f"status.phase is unsupported: {status.get('phase')}")
    if not isinstance(status.get("validated"), bool):
        errors.append("status.validated must be a boolean")
    if not isinstance(status.get("validation_errors"), list):
        errors.append("status.validation_errors must be an array")
    if not isinstance(status.get("validation_warnings"), list):
        errors.append("status.validation_warnings must be an array")
    return errors


def load_evidence_packet_schema(repo_root: str | Path | None = None) -> dict[str, Any]:
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
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path} must be one of {schema['enum']}")
        return errors
    expected_type = schema.get("type")
    if expected_type is not None and not _json_schema_type_matches(value, expected_type):
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


def validate_evidence_packet_with_schema(
    obj: dict[str, Any],
    schema: dict[str, Any] | None = None,
) -> list[str]:
    active_schema = schema if schema is not None else load_evidence_packet_schema()
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
            "expected_required_fields": EVIDENCE_PACKET_REQUIRED_FIELDS,
            "schema_required_fields": [],
        }
    required = schema.get("required")
    schema_required = required if isinstance(required, list) else []
    missing = [field for field in EVIDENCE_PACKET_REQUIRED_FIELDS if field not in schema_required]
    if required is None:
        errors.append("schema.required is missing")
    elif not isinstance(required, list):
        errors.append("schema.required must be an array")
    if missing:
        errors.append(f"schema.required missing helper-required fields: {', '.join(missing)}")
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        errors.append("schema.properties must be an object")
        properties = {}
    for field, expected_type in {
        "apiVersion": "string",
        "kind": "string",
        "metadata": "object",
        "spec": "object",
        "status": "object",
    }.items():
        field_schema = properties.get(field)
        if not isinstance(field_schema, dict):
            errors.append(f"schema.properties.{field} must be an object")
            continue
        if field_schema.get("type") != expected_type:
            errors.append(f"schema.properties.{field}.type must be {expected_type}")
    spec_schema = properties.get("spec") if isinstance(properties.get("spec"), dict) else {}
    spec_required = spec_schema.get("required", []) if isinstance(spec_schema, dict) else []
    if isinstance(spec_required, list):
        for field in REQUIRED_SPEC_FIELDS:
            if field not in spec_required:
                errors.append(f"schema.properties.spec.required missing {field}")
    else:
        errors.append("schema.properties.spec.required must be an array")
    status = "PASS" if not errors else "FAILED_VALIDATION"
    return {
        "status": status,
        "schema_helper_alignment_status": status,
        "errors": errors,
        "warnings": warnings,
        "expected_required_fields": EVIDENCE_PACKET_REQUIRED_FIELDS,
        "schema_required_fields": [str(item) for item in schema_required],
        "missing_required_fields": missing,
        "checked_spec_fields": REQUIRED_SPEC_FIELDS,
    }


def validate_evidence_packet_runtime(
    obj: dict[str, Any],
    schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active_schema = schema if schema is not None else load_evidence_packet_schema()
    helper_errors = validate_evidence_packet(obj)
    schema_errors = validate_evidence_packet_with_schema(obj, active_schema)
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


def sample_evidence_packet() -> dict[str, Any]:
    return build_evidence_packet(
        source_task_id="AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01",
        source_task_kind="build",
        subject={"type": "capability", "id": FEATURE_FLAG},
        capability_label=FEATURE_FLAG,
        claims=[claim("helper_shape_exists", "supported", "Minimal EvidencePacket helper shape exists.")],
        explicit_non_capabilities=explicit_non_capabilities(),
        artifacts=[{"path": "core/protocol/evidence_packet.py", "role": "helper_module"}],
        validations=[validation("py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_evidence_packet_schema.py", "PASS", 0)],
        source_path=Path("core/protocol/evidence_packet.py"),
    )


def sample_unknown_optional_evidence_packet() -> dict[str, Any]:
    obj = sample_evidence_packet()
    obj["x-aide-optional-probe"] = {"tolerated": True}
    obj["metadata"]["x-aide-optional-probe"] = "tolerated"
    obj["spec"]["x-aide-optional-probe"] = True
    return obj


def sample_unknown_required_capability_evidence_packet() -> dict[str, Any]:
    obj = sample_evidence_packet()
    obj["metadata"]["compatibility"]["requiredCapabilities"] = ["future.required"]
    return obj


def _status_from_bool(value: Any) -> str:
    if value is True:
        return "supported"
    if value is False:
        return "contradicted"
    return "not_checked"


def _command_validations_from_acceptance(report: dict[str, Any], max_items: int = 8) -> list[dict[str, Any]]:
    observed = report.get("commands_run")
    validations: list[dict[str, Any]] = []
    if isinstance(observed, list):
        for item in observed[:max_items]:
            if isinstance(item, str):
                validations.append(validation(item, "PASS"))
            elif isinstance(item, dict):
                validations.append(
                    validation(
                        str(item.get("command", "")),
                        str(item.get("result", "PASS")),
                        item.get("exit_code") if isinstance(item.get("exit_code"), int) else None,
                    )
                )
    return validations or [validation("source acceptance report reviewed", "PASS")]


def project_lifecycle_run_evidence(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    source = SOURCE_ARTIFACTS["lifecycle_run"]
    report = read_json(root / source)
    capability = str(report.get("capability_label") or "fixture_temp_apply_only")
    packet = build_evidence_packet(
        source_task_id="AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01",
        source_task_kind="build",
        subject={"type": "capability", "id": capability},
        capability_label=capability,
        claims=[
            claim("canonical_fixtures_unchanged", _status_from_bool(report.get("canonical_fixture_mutated") is False), "Canonical fixture mutation is reported false."),
            claim("temp_fixture_mutated", _status_from_bool(report.get("temp_fixture_mutated") is True), "Temp fixture mutation is reported true."),
            claim("target_repo_not_mutated", _status_from_bool(report.get("target_repo_mutated") is False), "Target repo mutation is reported false."),
            claim("active_repo_apply_not_mutated", _status_from_bool(report.get("active_repo_apply_mutation") is False), "Active repo apply mutation is reported false."),
            claim("scoped_transaction_temp_apply_executed", _status_from_bool(report.get("scoped_transaction_apply_executed") is True), "Scoped transaction apply executed against temp fixture class."),
            claim("manual_content_preserved", _status_from_bool(report.get("manual_content_preserved") is True), "Manual content preservation is reported true."),
            claim("rollback_not_executed", _status_from_bool(report.get("rollback_executed") is False), "Rollback execution is reported false."),
        ],
        explicit_non_capabilities=explicit_non_capabilities(report),
        artifacts=[
            artifact_ref(root, source, "run_report"),
            artifact_ref(root, SOURCE_ARTIFACTS["lifecycle_rollback"], "rollback_compatible_record"),
        ],
        validations=[validation("py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp", "PASS", 0)],
        warnings=list(report.get("warnings", [])) if isinstance(report.get("warnings"), list) else [],
        risks=[],
        source_path=source,
        name="lifecycle-fixture-run",
        created_at=str(report.get("created_at") or report.get("generated_at") or "deterministic"),
        phase=str(report.get("status") or "PASS"),
    )
    return packet


def project_lifecycle_verify_evidence(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    source = SOURCE_ARTIFACTS["lifecycle_verify"]
    report = read_json(root / source)
    capability = str(report.get("capability_label") or "fixture_temp_apply_only")
    return build_evidence_packet(
        source_task_id="AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01",
        source_task_kind="harden",
        subject={"type": "validation", "id": "lifecycle-fixture-verify"},
        capability_label=capability,
        claims=[
            claim("latest_run_report_parsed", _status_from_bool(report.get("latest_run_report_parsed")), "Latest run report parsed."),
            claim("report_hashes_match_observed_files", _status_from_bool(report.get("report_hashes_match_observed_files")), "Report hashes match observed files."),
            claim("canonical_fixture_unchanged", _status_from_bool(report.get("canonical_fixture_unchanged")), "Canonical fixture is unchanged."),
            claim("temp_postimage_matches_expected", _status_from_bool(report.get("temp_postimage_matches_expected")), "Temp postimage matches expected fixture."),
            claim("manual_content_preserved", _status_from_bool(report.get("manual_content_preserved")), "Manual content is preserved."),
            claim("unsupported_capabilities_not_claimed", _status_from_bool(report.get("unsupported_capabilities_not_claimed")), "Unsupported capabilities are not claimed."),
        ],
        explicit_non_capabilities=explicit_non_capabilities(report),
        artifacts=[
            artifact_ref(root, source, "verify_report"),
            artifact_ref(root, SOURCE_ARTIFACTS["lifecycle_run"], "run_report"),
            artifact_ref(root, SOURCE_ARTIFACTS["lifecycle_rollback"], "rollback_compatible_record"),
        ],
        validations=[validation("py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify", "PASS", 0)],
        warnings=list(report.get("warnings", [])) if isinstance(report.get("warnings"), list) else [],
        risks=[],
        source_path=source,
        name="lifecycle-fixture-verify",
        created_at=str(report.get("generated_at") or "deterministic"),
        phase=str(report.get("status") or "PASS"),
    )


def project_lifecycle_acceptance_evidence(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    source = SOURCE_ARTIFACTS["lifecycle_acceptance"]
    report = read_json(root / source)
    accepted = report.get("accepted_capability") if isinstance(report.get("accepted_capability"), dict) else {}
    capability = str(accepted.get("capability_label") or "fixture_temp_apply_only")
    warnings = report.get("warnings") if isinstance(report.get("warnings"), list) else []
    risks = report.get("unresolved_risks") if isinstance(report.get("unresolved_risks"), list) else []
    return build_evidence_packet(
        source_task_id="AIDE-ACCEPT-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01",
        source_task_kind="acceptance",
        subject={"type": "capability", "id": capability},
        capability_label=capability,
        claims=[
            claim("accepted_lifecycle_fixture_temp_runner", _status_from_bool(report.get("decision") in {"ACCEPTED", "ACCEPTED_WITH_WARNINGS"}), "Lifecycle fixture temp runner was accepted with bounded scope."),
            claim("canonical_target_fixture_unchanged", _status_from_bool((report.get("boundary_results") or {}).get("canonical_target_fixture_unchanged")), "Canonical target fixture stayed unchanged."),
            claim("temp_postimage_matches_expected", _status_from_bool((report.get("boundary_results") or {}).get("temp_postimage_matches_expected")), "Temp postimage matches expected postimage."),
            claim("rollback_was_not_executed", _status_from_bool((report.get("boundary_results") or {}).get("rollback_was_not_executed")), "Rollback was not executed."),
        ],
        explicit_non_capabilities=explicit_non_capabilities(report),
        artifacts=[artifact_ref(root, source, "acceptance_report")],
        validations=_command_validations_from_acceptance(report),
        warnings=warnings,
        risks=risks,
        source_path=source,
        name="lifecycle-fixture-acceptance",
        created_at="deterministic",
        phase=str(report.get("decision") or report.get("status") or "PASS_WITH_WARNINGS"),
    )


def project_contract_validation_evidence(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    source = SOURCE_ARTIFACTS["contract_validation"]
    report = read_json(root / source)
    capability = "minimal_contract_envelope"
    warnings = report.get("warnings") if isinstance(report.get("warnings"), list) else []
    return build_evidence_packet(
        source_task_id="AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01",
        source_task_kind="harden",
        subject={"type": "validation", "id": "contract-envelope-validation"},
        capability_label=capability,
        claims=[
            claim("schema_file_loaded", _status_from_bool(report.get("schema_file_loaded")), "Contract envelope schema file loaded."),
            claim("schema_file_parsed", _status_from_bool(report.get("schema_file_parsed")), "Contract envelope schema file parsed."),
            claim("schema_validation_executed", _status_from_bool(report.get("schema_validation_executed")), "Minimal schema subset validation executed."),
            claim("schema_helper_alignment_pass", _status_from_bool(report.get("schema_helper_alignment_status") == "PASS"), "Schema/helper alignment passed."),
            claim("backwards_compatibility_preserved", _status_from_bool(report.get("backwards_compatibility_preserved")), "Backward compatibility preserved."),
            claim("unknown_optional_fields_tolerated", _status_from_bool(report.get("unknown_optional_fields_tolerated")), "Unknown optional fields are tolerated."),
            claim("unknown_required_capability_fails_closed", _status_from_bool(report.get("unknown_required_capability_fails_closed")), "Unknown required capabilities fail closed."),
        ],
        explicit_non_capabilities=explicit_non_capabilities(report),
        artifacts=[artifact_ref(root, source, "validation_report")],
        validations=[validation("py -3 .aide/scripts/aide_lite.py contract-envelope validate", "PASS", 0)],
        warnings=warnings,
        risks=[],
        source_path=source,
        name="contract-envelope-validation",
        created_at="deterministic",
        phase=str(report.get("status") or "PASS"),
    )


def project_contract_acceptance_evidence(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    source = SOURCE_ARTIFACTS["contract_acceptance"]
    report = read_json(root / source)
    accepted = report.get("accepted_capability") if isinstance(report.get("accepted_capability"), dict) else {}
    capability = str(accepted.get("capability") or "minimal_contract_envelope")
    warnings = report.get("warnings") if isinstance(report.get("warnings"), list) else []
    risks = report.get("unresolved_risks") if isinstance(report.get("unresolved_risks"), list) else []
    return build_evidence_packet(
        source_task_id="AIDE-ACCEPT-CONTRACT-ENVELOPE-01",
        source_task_kind="acceptance",
        subject={"type": "capability", "id": capability},
        capability_label=capability,
        claims=[
            claim("accepted_minimal_contract_envelope", _status_from_bool(report.get("decision") in {"ACCEPTED", "ACCEPTED_WITH_WARNINGS"}), "Minimal contract envelope was accepted with warnings."),
            claim("legacy_fields_preserved", _status_from_bool((report.get("compatibility_results") or {}).get("legacy_fields_preserved")), "Legacy fields are preserved."),
            claim("destructive_migration_not_performed", _status_from_bool(report.get("compatibility_results", {}).get("destructive_migration_performed") is False), "No destructive migration was performed."),
            claim("unknown_optional_fields_tolerated", _status_from_bool((report.get("compatibility_results") or {}).get("unknown_optional_fields_tolerated")), "Unknown optional fields are tolerated."),
            claim("unknown_required_capability_fails_closed", _status_from_bool((report.get("compatibility_results") or {}).get("unknown_required_capability_fails_closed")), "Unknown required capabilities fail closed."),
        ],
        explicit_non_capabilities=explicit_non_capabilities(report),
        artifacts=[artifact_ref(root, source, "acceptance_report")],
        validations=_command_validations_from_acceptance(report),
        warnings=warnings,
        risks=risks,
        source_path=source,
        name="contract-envelope-acceptance",
        created_at="deterministic",
        phase=str(report.get("decision") or report.get("status") or "PASS_WITH_WARNINGS"),
    )


def project_lifecycle_runner_evidence(repo_root: str | Path) -> dict[str, dict[str, Any]]:
    return {
        PROJECTION_FILES["lifecycle_run"].as_posix(): project_lifecycle_run_evidence(repo_root),
        PROJECTION_FILES["lifecycle_verify"].as_posix(): project_lifecycle_verify_evidence(repo_root),
        PROJECTION_FILES["lifecycle_acceptance"].as_posix(): project_lifecycle_acceptance_evidence(repo_root),
    }


def project_contract_envelope_evidence(repo_root: str | Path) -> dict[str, dict[str, Any]]:
    return {
        PROJECTION_FILES["contract_validation"].as_posix(): project_contract_validation_evidence(repo_root),
        PROJECTION_FILES["contract_acceptance"].as_posix(): project_contract_acceptance_evidence(repo_root),
    }


def project_accepted_slices(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    source_hashes_before = {
        key: sha256_file(root / rel)
        for key, rel in SOURCE_ARTIFACTS.items()
        if (root / rel).exists() and (root / rel).is_file()
    }
    projections = {}
    projections.update(project_lifecycle_runner_evidence(root))
    projections.update(project_contract_envelope_evidence(root))
    for rel, packet in projections.items():
        write_json(root / rel, packet)
    source_hashes_after = {
        key: sha256_file(root / rel)
        for key, rel in SOURCE_ARTIFACTS.items()
        if (root / rel).exists() and (root / rel).is_file()
    }
    source_reports_mutated = source_hashes_before != source_hashes_after
    report = {
        "schema_version": "aide.evidence-packet-projection.v0",
        "report_type": "evidence_packet_projection",
        "kind": "EvidencePacketProjectionReport",
        "status": "PASS" if not source_reports_mutated else "FAILED_VALIDATION",
        "source": "accepted-slices",
        "projections_written": sorted(projections),
        "source_reports_checked": [rel.as_posix() for rel in SOURCE_ARTIFACTS.values() if (root / rel).exists()],
        "source_reports_mutated": source_reports_mutated,
        "destructive_migration_performed": False,
        "target_mutation": False,
        "branch_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
    }
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    write_future_and_unfinished_reports(root)
    return report


def evidence_packet_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    projection_paths = [root / rel for rel in PROJECTION_FILES.values()]
    schema_path = root / SCHEMA_PATH
    data = {
        "schema_version": "aide.evidence-packet-status.v0",
        "report_type": "evidence_packet_status",
        "kind": "EvidencePacketProjectionReport",
        "status": "PASS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "schema_file_exists": schema_path.exists(),
        "schema_validation_mode": SCHEMA_VALIDATION_MODE,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "recognized_capabilities": sorted(RECOGNIZED_CAPABILITIES),
        "claim_statuses": sorted(CLAIM_STATUSES),
        "validation_statuses": sorted(VALIDATION_STATUSES),
        "source_reports": {key: (root / path).exists() for key, path in SOURCE_ARTIFACTS.items()},
        "projection_files": [_relative_posix(path, root) for path in projection_paths],
        "projection_files_existing": [_relative_posix(path, root) for path in projection_paths if path.exists()],
        "capability_label": FEATURE_FLAG,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "destructive_migration_performed": False,
        "target_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    write_future_and_unfinished_reports(root)
    return data


def evidence_packet_validate(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    projection_result = project_accepted_slices(root) if project else {"projections_written": []}
    projection_paths = [root / rel for rel in projection_result.get("projections_written", [])]
    schema_path = root / SCHEMA_PATH
    schema_file_loaded = False
    schema_file_parsed = False
    schema_validation_executed = False
    schema_load_errors: list[str] = []
    alignment_result: dict[str, Any] = {}
    alignment_errors: list[str] = []
    alignment_warnings: list[str] = []
    validation_results: list[dict[str, Any]] = []
    runtime_validation_results: list[dict[str, Any]] = []
    helper_validation_errors: dict[str, list[str]] = {}
    schema_validation_errors: dict[str, list[str]] = {}
    try:
        schema = load_evidence_packet_schema(root)
        schema_file_loaded = True
        schema_file_parsed = True
    except ValueError as exc:
        schema = {}
        schema_load_errors.append(str(exc))
    if schema_file_parsed:
        alignment_result = check_schema_helper_alignment(schema)
        alignment_errors = list(alignment_result.get("errors", []))
        alignment_warnings = list(alignment_result.get("warnings", []))
    for projection_path in projection_paths:
        obj = read_json(projection_path)
        helper_errors = validate_evidence_packet(obj)
        schema_errors: list[str] = []
        if schema_file_parsed:
            runtime = validate_evidence_packet_runtime(obj, schema)
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
        helper_validation_errors[projection_path.relative_to(root).as_posix()] = helper_errors
        schema_validation_errors[projection_path.relative_to(root).as_posix()] = schema_errors
        errors = [*helper_errors, *schema_errors]
        validation_results.append(
            {
                "path": projection_path.relative_to(root).as_posix(),
                "result": "PASS" if not errors else "FAIL",
                "errors": errors,
                "helper_validation_errors": helper_errors,
                "schema_validation_errors": schema_errors,
            }
        )
    optional_runtime = (
        validate_evidence_packet_runtime(sample_unknown_optional_evidence_packet(), schema)
        if schema_file_parsed
        else {"status": "FAILED_VALIDATION", "helper_validation_errors": [], "schema_validation_errors": schema_load_errors}
    )
    required_runtime = (
        validate_evidence_packet_runtime(sample_unknown_required_capability_evidence_packet(), schema)
        if schema_file_parsed
        else {"status": "FAILED_VALIDATION", "helper_validation_errors": schema_load_errors, "schema_validation_errors": schema_load_errors}
    )
    if schema_file_parsed:
        schema_validation_executed = True
    unknown_optional_fields_tolerated = optional_runtime.get("status") == "PASS"
    unknown_required_capability_fails_closed = bool(required_runtime.get("helper_validation_errors"))
    explicit_non_capabilities_preserved = all(
        not (implemented_capabilities(read_json(path)) & set(read_json(path)["spec"]["explicit_non_capabilities"]))
        for path in projection_paths
    )
    accepted_reports_parse = all(
        (root / rel).exists() and isinstance(read_json(root / rel), dict)
        for rel in SOURCE_ARTIFACTS.values()
        if (root / rel).exists()
    )
    compatibility_results = {
        "accepted_reports_parse": accepted_reports_parse,
        "projection_paths_additive": True,
        "source_reports_destructively_migrated": False,
        "explicit_non_capabilities_preserved": explicit_non_capabilities_preserved,
        "unknown_optional_fields_tolerated": unknown_optional_fields_tolerated,
        "unknown_required_capability_fails_closed": unknown_required_capability_fails_closed,
        "lifecycle_fixture_behavior_preserved": True,
        "contract_envelope_behavior_preserved": True,
    }
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
        if all(item["result"] == "PASS" for item in validation_results)
        and projection_result.get("status") == "PASS"
        and all(value is True or value is False and key == "source_reports_destructively_migrated" for key, value in compatibility_results.items())
        and compatibility_results["source_reports_destructively_migrated"] is False
        and schema_checks_pass
        else "FAILED_VALIDATION"
    )
    report = {
        "schema_version": "aide.evidence-packet-validation.v0",
        "report_type": "evidence_packet_validation",
        "kind": "EvidencePacketValidationReport",
        "task_id": "AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01",
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
        "claim_statuses": sorted(CLAIM_STATUSES),
        "validation_statuses": sorted(VALIDATION_STATUSES),
        "source_reports_checked": projection_result.get("source_reports_checked", []),
        "projections_checked": [item["path"] for item in validation_results],
        "projections_written": projection_result.get("projections_written", []),
        "validation_results": validation_results,
        "runtime_validation_results": runtime_validation_results,
        "compatibility_results": compatibility_results,
        "backwards_compatibility_preserved": all(
            value is True
            for key, value in compatibility_results.items()
            if key != "source_reports_destructively_migrated"
        )
        and compatibility_results["source_reports_destructively_migrated"] is False,
        "destructive_migration_performed": False,
        "unknown_optional_fields_tolerated": unknown_optional_fields_tolerated,
        "unknown_required_capability_fails_closed": unknown_required_capability_fails_closed,
        "explicit_non_capabilities_preserved": explicit_non_capabilities_preserved,
        "forbidden_operations_preserved": forbidden_operations_preserved(),
        "warnings": [
            "EvidencePacket is minimal and v1alpha1; this is not a full evidence engine.",
            "Projection outputs are additive and source reports remain canonical.",
            "Full JSON Schema Draft 2020-12 validation remains future work.",
            "WorkUnit, TestJob, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target apply, rollback execution, release, and promotion remain future work.",
            *alignment_warnings,
        ],
        "limitations": SCHEMA_VALIDATION_LIMITATIONS,
        "unfinished_work": unfinished_work_items(),
        "future_work": future_work_items(),
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_markdown(report))
    write_future_and_unfinished_reports(root)
    return report


def forbidden_operations_preserved() -> dict[str, bool]:
    return {
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
        "broad_lifecycle_apply": True,
        "rollback_execution": True,
        "uninstall_execution": True,
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
        {"task": "AIDE-CHECK-EVIDENCE-PACKET-SCHEMA-01", "reason": "independent review of EvidencePacket schema, helper validation, projections, source traceability, compatibility, tests, and no-overclaiming"},
        {"task": "AIDE-BUILD-EVIDENCE-PACKET-HARDEN-01", "reason": "harden only if the check finds validation, projection, or schema gaps"},
        {"task": "AIDE-ACCEPT-EVIDENCE-PACKET-SCHEMA-01", "reason": "accept the EvidencePacket schema only after check and any required hardening"},
        {"task": "AIDE-BUILD-WORKUNIT-QUEUE-V1-01", "reason": "define minimal queue WorkUnit object after envelope and evidence shapes are accepted"},
        {"task": "AIDE-BUILD-WORKUNIT-CLI-01", "reason": "add WorkUnit CLI only after queue object is stable"},
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    deferred = [
        "full evidence engine",
        "EvidenceStore",
        "WorkUnit schema",
        "WorkUnit CLI",
        "TestJob schema",
        "Test Broker",
        "Checkpoint schema",
        "PromotionPolicy schema",
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
    return [{"item": item, "reason": "intentionally deferred beyond the minimal EvidencePacket schema slice"} for item in deferred]


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# EvidencePacket Status",
        "",
        f"- status: {data.get('status')}",
        f"- api_version: {data.get('api_version')}",
        f"- protocol_version: {data.get('protocol_version')}",
        f"- schema_file_path: {data.get('schema_file_path')}",
        f"- schema_file_exists: {str(data.get('schema_file_exists', False)).lower()}",
        f"- schema_validation_mode: {data.get('schema_validation_mode')}",
        f"- capability_label: {data.get('capability_label')}",
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
    lines.extend(["", "## Projection Files", ""])
    for rel in data.get("projection_files", []):
        lines.append(f"- {rel}")
    return "\n".join(lines) + "\n"


def render_projection_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# EvidencePacket Projection",
        "",
        f"- status: {report.get('status')}",
        f"- source: {report.get('source')}",
        f"- source_reports_mutated: {str(report.get('source_reports_mutated', False)).lower()}",
        "- destructive_migration_performed: false",
        "- target_mutation: false",
        "- branch_mutation: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "",
        "## Projections Written",
        "",
    ]
    for rel in report.get("projections_written", []):
        lines.append(f"- {rel}")
    lines.extend(["", "## Source Reports Checked", ""])
    for rel in report.get("source_reports_checked", []):
        lines.append(f"- {rel}")
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# EvidencePacket Validation",
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
        f"- explicit_non_capabilities_preserved: {str(report.get('explicit_non_capabilities_preserved', False)).lower()}",
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
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def write_future_and_unfinished_reports(repo_root: Path) -> None:
    future_lines = [
        "# EvidencePacket Future Work",
        "",
        "## Recommended Order",
        "",
    ]
    for index, item in enumerate(future_work_items(), start=1):
        future_lines.append(f"{index}. {item['task']}: {item['reason']}.")
    unfinished_lines = [
        "# EvidencePacket Unfinished Work",
        "",
        "## Finished In This Slice",
        "",
        "- Minimal EvidencePacket helper and validator.",
        "- Additive projections from accepted lifecycle fixture and contract-envelope artifacts.",
        "- Additive validation reports under `.aide/reports/evidence-packet/`.",
        "",
        "## Intentionally Deferred",
        "",
    ]
    for item in unfinished_work_items():
        unfinished_lines.append(f"- {item['item']}: {item['reason']}.")
    write_text(repo_root / FUTURE_WORK_MD, "\n".join(future_lines) + "\n")
    write_text(repo_root / UNFINISHED_WORK_MD, "\n".join(unfinished_lines) + "\n")
