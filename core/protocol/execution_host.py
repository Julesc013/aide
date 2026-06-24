"""Projection-only ExecutionHost contract v0.

This module defines the neutral contract shape for future bounded worker/session
execution hosts. It does not implement a live host, start workers, schedule
runs, call providers, open transports, or mutate repositories.
"""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from typing import Any

from core.protocol import envelope


API_VERSION = envelope.API_VERSION
EXECUTION_HOST_SCHEMA_VERSION = "aide.execution-host-contract.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "execution_host_contract_v0"
ACCEPTED_PROVIDER_CAPABILITY = "registered_process_execution_provider_v0"
TASK_ID = "AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01"

REPORT_ROOT = Path(".aide/reports/execution-host-contract")
PROJECTION_ROOT = REPORT_ROOT / "projections"
SCHEMA_PATH = Path(".aide/protocol/aide-execution-host.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"

SUPPORTED_KINDS = {
    "ExecutionHostDescriptor",
    "ExecutionHostRunBinding",
    "ExecutionHostEvent",
    "ExecutionHostArtifact",
    "ExecutionHostApproval",
    "ExecutionHostUsage",
    "ExecutionHostContractProjectionReport",
    "ExecutionHostContractValidationReport",
}
RECORD_KINDS = {
    "ExecutionHostDescriptor",
    "ExecutionHostRunBinding",
    "ExecutionHostEvent",
    "ExecutionHostArtifact",
    "ExecutionHostApproval",
    "ExecutionHostUsage",
}
EXECUTION_HOST_REQUIRED_FIELDS = ["apiVersion", "kind", "metadata", "spec", "status"]
REQUIRED_METADATA_FIELDS = ["id", "createdAt", "sourcePath", "producer", "compatibility"]
REQUIRED_STATUS_FIELDS = ["validated", "projection_only", "validation_errors", "validation_warnings"]
REQUIRED_SPEC_FIELDS_BY_KIND = {
    "ExecutionHostDescriptor": [
        "host_id",
        "host_kind",
        "transport_modes",
        "supported_operations",
        "capability_execution_distinct",
        "worker_session_contract",
        "explicit_non_capabilities",
    ],
    "ExecutionHostRunBinding": [
        "binding_id",
        "host_ref",
        "run_ref",
        "workunit_ref",
        "context_refs",
        "execution_started",
        "worker_process_started",
    ],
    "ExecutionHostEvent": ["event_ref", "run_ref", "event_type", "sequence", "payload", "delivered"],
    "ExecutionHostArtifact": ["artifact_ref", "run_ref", "artifact_role", "digest", "persisted"],
    "ExecutionHostApproval": ["approval_ref", "run_ref", "approval_kind", "approval_status", "resolved"],
    "ExecutionHostUsage": ["usage_ref", "run_ref", "meters", "limits", "measured"],
}
HOST_KINDS = {
    "contract_projection",
    "local_process",
    "remote_sandbox",
    "ci",
    "human",
    "offline_mailbox",
    "unknown",
}
TRANSPORT_MODES = {"projection_only", "stdio", "local_socket", "localhost_http", "filesystem_mailbox", "unknown"}
OPERATION_NAMES = {
    "probe",
    "create_run",
    "attach",
    "send_input",
    "stream_events",
    "resolve_runtime_approval",
    "interrupt",
    "collect_artifacts",
    "finish",
    "reconcile",
}
EVENT_TYPES = {"RunObserved", "HostProbed", "ArtifactObserved", "ApprovalObserved", "UsageObserved"}
ARTIFACT_ROLES = {"contract_projection", "stdout", "stderr", "log", "result", "proposal", "unknown"}
APPROVAL_KINDS = {"runtime_approval", "tool_approval", "human_checkpoint", "unknown"}
APPROVAL_STATUSES = {"not_requested", "requested", "approved", "refused", "expired", "unknown"}
RESULT_VALUES = {"PASS", "PASS_WITH_WARNINGS", "FAILED_VALIDATION", "BLOCKED", "PARTIAL", "UNKNOWN"}
SCHEMA_VALIDATION_MODE = "minimal_json_schema_subset"
SCHEMA_VALIDATION_LIMITATIONS = [
    "Local subset validator supports type, enum, required, properties, simple additionalProperties, and homogeneous array items only.",
    "Full JSON Schema Draft 2020-12 validation remains future work.",
    "Kind-specific schema discrimination is supported structurally by oneOf and enforced by the helper validator.",
]
RECOGNIZED_CAPABILITIES = {
    FEATURE_FLAG,
    ACCEPTED_PROVIDER_CAPABILITY,
    "minimal_worker_run_schema",
    "minimal_workunit_queue_v1",
    "minimal_evidence_packet_schema",
    "minimal_event_record_schema",
}
EXPLICIT_NON_CAPABILITIES = [
    "live_execution_host",
    "local_process_execution_host",
    "remote_execution_host",
    "worker_execution",
    "worker_harness",
    "worker_process_start",
    "worker_lease",
    "scheduler",
    "supervisor",
    "provider_model_calls",
    "network_calls",
    "service_runtime",
    "workbench_runtime",
    "preview_session",
    "development_transaction",
    "patch_transaction_apply",
    "repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
]
FALSE_BOUNDARY_FIELDS = [
    "execution_host_runtime_implemented",
    "local_process_execution_host_implemented",
    "remote_execution_host_implemented",
    "worker_execution_implemented",
    "worker_process_started",
    "worker_lease_created",
    "scheduler_implemented",
    "supervisor_implemented",
    "provider_model_calls_performed",
    "network_calls_performed",
    "service_runtime_implemented",
    "workbench_runtime_implemented",
    "preview_apply_implemented",
    "repository_mutation_performed",
    "branch_worktree_mutation_performed",
    "github_mutation_performed",
    "release_or_promotion_performed",
]
PROJECTION_FILES = {
    "descriptor": PROJECTION_ROOT / "execution-host-descriptor.json",
    "run_binding": PROJECTION_ROOT / "execution-host-run-binding.json",
    "event": PROJECTION_ROOT / "execution-host-event.json",
    "artifact": PROJECTION_ROOT / "execution-host-artifact.json",
    "approval": PROJECTION_ROOT / "execution-host-approval.json",
    "usage": PROJECTION_ROOT / "execution-host-usage.json",
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


def _source_path_value(source_path: Path | None) -> str:
    return source_path.as_posix() if source_path is not None else ""


def _compatibility(required_capabilities: list[str] | None = None) -> dict[str, Any]:
    required = [FEATURE_FLAG]
    for capability in required_capabilities or []:
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


def _metadata(record_id: str, name: str, source_path: Path | None = None) -> dict[str, Any]:
    return {
        "id": record_id,
        "name": name,
        "createdAt": "deterministic",
        "sourcePath": _source_path_value(source_path),
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility([ACCEPTED_PROVIDER_CAPABILITY]),
    }


def _false_boundaries() -> dict[str, bool]:
    return {field: False for field in FALSE_BOUNDARY_FIELDS}


def _status(*, warnings: list[str] | None = None, errors: list[str] | None = None) -> dict[str, Any]:
    return {
        "validated": not errors,
        "projection_only": True,
        "recorded": False,
        "validation_errors": list(errors or []),
        "validation_warnings": list(warnings or []),
    }


def _build_record(kind: str, metadata: dict[str, Any], spec: dict[str, Any], status: dict[str, Any]) -> dict[str, Any]:
    obj = envelope.build_envelope(kind, metadata, spec, status, api_version=API_VERSION)
    obj["schema_version"] = EXECUTION_HOST_SCHEMA_VERSION
    obj["protocol_version"] = PROTOCOL_VERSION
    return obj


def build_execution_host_descriptor() -> dict[str, Any]:
    spec = {
        "host_id": "aide://execution-host/contract-v0",
        "host_kind": "contract_projection",
        "transport_modes": ["projection_only"],
        "supported_operations": sorted(OPERATION_NAMES),
        "capability_execution_distinct": True,
        "capability_provider_ref": ACCEPTED_PROVIDER_CAPABILITY,
        "worker_session_contract": True,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "capability_label": FEATURE_FLAG,
        **_false_boundaries(),
    }
    return _build_record(
        "ExecutionHostDescriptor",
        _metadata("execution-host-descriptor-contract-v0", "ExecutionHostDescriptor v0", SCHEMA_PATH),
        spec,
        _status(warnings=["Projection-only descriptor; no live ExecutionHost is implemented."]),
    )


def build_execution_host_run_binding() -> dict[str, Any]:
    spec = {
        "binding_id": "aide://execution-host-binding/contract-v0",
        "host_ref": "aide://execution-host/contract-v0",
        "run_ref": "aide://execution-host-run/contract-v0",
        "workunit_ref": "AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01",
        "context_refs": [],
        "execution_started": False,
        "worker_process_started": False,
        "scheduler_enqueued": False,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "capability_label": FEATURE_FLAG,
        **_false_boundaries(),
    }
    return _build_record(
        "ExecutionHostRunBinding",
        _metadata("execution-host-run-binding-contract-v0", "ExecutionHostRunBinding v0", SCHEMA_PATH),
        spec,
        _status(warnings=["Run binding is a contract projection; no run is created."]),
    )


def build_execution_host_event() -> dict[str, Any]:
    spec = {
        "event_ref": "aide://execution-host-event/contract-v0-0001",
        "run_ref": "aide://execution-host-run/contract-v0",
        "event_type": "RunObserved",
        "sequence": 1,
        "payload": {"projection": True},
        "delivered": False,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "capability_label": FEATURE_FLAG,
        **_false_boundaries(),
    }
    return _build_record(
        "ExecutionHostEvent",
        _metadata("execution-host-event-contract-v0", "ExecutionHostEvent v0", SCHEMA_PATH),
        spec,
        _status(warnings=["Event is not appended to a runtime event stream."]),
    )


def build_execution_host_artifact() -> dict[str, Any]:
    spec = {
        "artifact_ref": "aide://execution-host-artifact/contract-v0",
        "run_ref": "aide://execution-host-run/contract-v0",
        "artifact_role": "contract_projection",
        "media_type": "application/json",
        "digest": "sha256:" + ("0" * 64),
        "persisted": False,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "capability_label": FEATURE_FLAG,
        **_false_boundaries(),
    }
    return _build_record(
        "ExecutionHostArtifact",
        _metadata("execution-host-artifact-contract-v0", "ExecutionHostArtifact v0", SCHEMA_PATH),
        spec,
        _status(warnings=["Artifact record is a projection; no artifact store is implemented."]),
    )


def build_execution_host_approval() -> dict[str, Any]:
    spec = {
        "approval_ref": "aide://execution-host-approval/contract-v0",
        "run_ref": "aide://execution-host-run/contract-v0",
        "approval_kind": "runtime_approval",
        "approval_status": "not_requested",
        "required": False,
        "resolved": False,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "capability_label": FEATURE_FLAG,
        **_false_boundaries(),
    }
    return _build_record(
        "ExecutionHostApproval",
        _metadata("execution-host-approval-contract-v0", "ExecutionHostApproval v0", SCHEMA_PATH),
        spec,
        _status(warnings=["Approval record is a contract placeholder; no approval runtime exists."]),
    )


def build_execution_host_usage() -> dict[str, Any]:
    spec = {
        "usage_ref": "aide://execution-host-usage/contract-v0",
        "run_ref": "aide://execution-host-run/contract-v0",
        "meters": {"tokens": 0, "processes": 0, "network_calls": 0},
        "limits": {},
        "measured": False,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "capability_label": FEATURE_FLAG,
        **_false_boundaries(),
    }
    return _build_record(
        "ExecutionHostUsage",
        _metadata("execution-host-usage-contract-v0", "ExecutionHostUsage v0", SCHEMA_PATH),
        spec,
        _status(warnings=["Usage is not measured by a runtime host in this slice."]),
    )


def sample_records() -> dict[str, dict[str, Any]]:
    return {
        "descriptor": build_execution_host_descriptor(),
        "run_binding": build_execution_host_run_binding(),
        "event": build_execution_host_event(),
        "artifact": build_execution_host_artifact(),
        "approval": build_execution_host_approval(),
        "usage": build_execution_host_usage(),
    }


def sample_unknown_optional_record() -> dict[str, Any]:
    obj = build_execution_host_descriptor()
    obj["x-aide-optional-probe"] = {"tolerated": True}
    obj["metadata"]["x-aide-optional-probe"] = "tolerated"
    obj["spec"]["x-aide-optional-probe"] = True
    return obj


def sample_unknown_required_capability_record() -> dict[str, Any]:
    obj = build_execution_host_descriptor()
    obj["metadata"]["compatibility"]["requiredCapabilities"] = ["future.required"]
    return obj


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def implemented_capabilities(record: dict[str, Any]) -> set[str]:
    spec = record.get("spec") if isinstance(record.get("spec"), dict) else {}
    capability = spec.get("capability_label")
    if isinstance(capability, str) and capability:
        return {capability}
    return set()


def validate_execution_host_contract(obj: dict[str, Any], allowed_kinds: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["ExecutionHost contract record must be an object"]
    if obj.get("apiVersion") != API_VERSION:
        errors.append(f"unsupported apiVersion: {obj.get('apiVersion')}")
    kind = obj.get("kind")
    active_kinds = allowed_kinds or RECORD_KINDS
    if not isinstance(kind, str) or not kind:
        errors.append("kind must be a non-empty string")
    elif kind not in active_kinds:
        errors.append(f"unsupported kind: {kind}")
    for field in ["metadata", "spec", "status"]:
        if field not in obj:
            errors.append(f"missing required field: {field}")
        elif not isinstance(obj[field], dict):
            errors.append(f"{field} must be an object")
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
    spec = obj.get("spec") if isinstance(obj.get("spec"), dict) else {}
    for field in REQUIRED_SPEC_FIELDS_BY_KIND.get(str(kind), []):
        if field not in spec:
            errors.append(f"missing required spec field: {field}")
    non_capabilities = spec.get("explicit_non_capabilities")
    if not isinstance(non_capabilities, list):
        errors.append("spec.explicit_non_capabilities must be an array")
    else:
        for item in non_capabilities:
            if not isinstance(item, str) or not item:
                errors.append("spec.explicit_non_capabilities entries must be non-empty strings")
        if spec.get("capability_label") in non_capabilities:
            errors.append("spec.capability_label must not appear in explicit_non_capabilities")
    for field in FALSE_BOUNDARY_FIELDS:
        if field in spec and spec[field] is not False:
            errors.append(f"spec.{field} must be false in projection-only contract")
    if kind == "ExecutionHostDescriptor":
        if spec.get("host_kind") not in HOST_KINDS:
            errors.append(f"unsupported host_kind: {spec.get('host_kind')}")
        if not isinstance(spec.get("transport_modes"), list) or not spec.get("transport_modes"):
            errors.append("spec.transport_modes must be a non-empty array")
        else:
            for item in spec["transport_modes"]:
                if item not in TRANSPORT_MODES:
                    errors.append(f"unsupported transport_mode: {item}")
        operations = spec.get("supported_operations")
        if not isinstance(operations, list) or sorted(operations) != sorted(OPERATION_NAMES):
            errors.append("spec.supported_operations must equal the v0 operation set")
        if spec.get("capability_execution_distinct") is not True:
            errors.append("spec.capability_execution_distinct must be true")
        if spec.get("capability_provider_ref") != ACCEPTED_PROVIDER_CAPABILITY:
            errors.append("spec.capability_provider_ref must reference the accepted registered process provider")
        if spec.get("worker_session_contract") is not True:
            errors.append("spec.worker_session_contract must be true")
    if kind == "ExecutionHostRunBinding":
        for field in ["binding_id", "host_ref", "run_ref", "workunit_ref"]:
            if not isinstance(spec.get(field), str) or not spec.get(field):
                errors.append(f"spec.{field} must be a non-empty string")
        if not isinstance(spec.get("context_refs"), list):
            errors.append("spec.context_refs must be an array")
        if spec.get("execution_started") is not False:
            errors.append("spec.execution_started must be false")
        if spec.get("worker_process_started") is not False:
            errors.append("spec.worker_process_started must be false")
    if kind == "ExecutionHostEvent":
        if spec.get("event_type") not in EVENT_TYPES:
            errors.append(f"unsupported event_type: {spec.get('event_type')}")
        if not isinstance(spec.get("sequence"), int) or isinstance(spec.get("sequence"), bool) or spec.get("sequence") < 1:
            errors.append("spec.sequence must be an integer >= 1")
        if not isinstance(spec.get("payload"), dict):
            errors.append("spec.payload must be an object")
        if spec.get("delivered") is not False:
            errors.append("spec.delivered must be false")
    if kind == "ExecutionHostArtifact":
        if spec.get("artifact_role") not in ARTIFACT_ROLES:
            errors.append(f"unsupported artifact_role: {spec.get('artifact_role')}")
        digest = spec.get("digest")
        if not isinstance(digest, str) or not digest.startswith("sha256:") or len(digest) != 71:
            errors.append("spec.digest must be a sha256 digest string")
        if spec.get("persisted") is not False:
            errors.append("spec.persisted must be false")
    if kind == "ExecutionHostApproval":
        if spec.get("approval_kind") not in APPROVAL_KINDS:
            errors.append(f"unsupported approval_kind: {spec.get('approval_kind')}")
        if spec.get("approval_status") not in APPROVAL_STATUSES:
            errors.append(f"unsupported approval_status: {spec.get('approval_status')}")
        if spec.get("resolved") is not False:
            errors.append("spec.resolved must be false")
    if kind == "ExecutionHostUsage":
        if not isinstance(spec.get("meters"), dict):
            errors.append("spec.meters must be an object")
        if not isinstance(spec.get("limits"), dict):
            errors.append("spec.limits must be an object")
        if spec.get("measured") is not False:
            errors.append("spec.measured must be false")
    status = obj.get("status") if isinstance(obj.get("status"), dict) else {}
    for field in REQUIRED_STATUS_FIELDS:
        if field not in status:
            errors.append(f"missing required status field: {field}")
    if not isinstance(status.get("validated"), bool):
        errors.append("status.validated must be a boolean")
    if status.get("projection_only") is not True:
        errors.append("status.projection_only must be true")
    if not isinstance(status.get("validation_errors"), list):
        errors.append("status.validation_errors must be an array")
    if not isinstance(status.get("validation_warnings"), list):
        errors.append("status.validation_warnings must be an array")
    return errors


def load_execution_host_schema(repo_root: str | Path | None = None) -> dict[str, Any]:
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
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def _schema_node_errors(value: Any, schema: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path} must be one of {schema['enum']}")
        return errors
    expected_type = schema.get("type")
    if expected_type is not None and not _json_schema_type_matches(value, expected_type):
        errors.append(f"{path} must be {expected_type}")
        return errors
    if isinstance(value, dict):
        required = schema.get("required", [])
        if required is not None and not isinstance(required, list):
            errors.append(f"{path}.required must be an array")
        else:
            for field in required:
                if isinstance(field, str) and field not in value:
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
    if isinstance(value, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(_schema_node_errors(item, item_schema, f"{path}[{index}]"))
    return errors


def validate_execution_host_with_schema(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    active_schema = schema if schema is not None else load_execution_host_schema()
    if not isinstance(active_schema, dict):
        return ["schema must be an object"]
    return _schema_node_errors(obj, active_schema, "$")


def check_schema_helper_alignment(schema: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(schema, dict):
        return {"schema_helper_alignment_status": "FAILED_VALIDATION", "errors": ["schema must be an object"], "warnings": []}
    required = schema.get("required")
    schema_required = required if isinstance(required, list) else []
    for field in EXECUTION_HOST_REQUIRED_FIELDS:
        if field not in schema_required:
            errors.append(f"schema.required missing helper-required field: {field}")
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        errors.append("schema.properties must be an object")
        properties = {}
    kind_schema = properties.get("kind", {}) if isinstance(properties.get("kind"), dict) else {}
    kind_enum = set(kind_schema.get("enum", [])) if isinstance(kind_schema.get("enum"), list) else set()
    missing_kinds = sorted(SUPPORTED_KINDS - kind_enum)
    if missing_kinds:
        errors.append(f"schema kind enum missing supported kinds: {', '.join(missing_kinds)}")
    status_schema = properties.get("status", {}) if isinstance(properties.get("status"), dict) else {}
    status_required = status_schema.get("required", []) if isinstance(status_schema.get("required"), list) else []
    for field in REQUIRED_STATUS_FIELDS:
        if field not in status_required:
            errors.append(f"schema.status.required missing field: {field}")
    if "oneOf" not in schema:
        warnings.append("schema oneOf kind discrimination is absent; helper enforces kind-specific fields")
    status = "PASS" if not errors else "FAILED_VALIDATION"
    return {
        "schema_helper_alignment_status": status,
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "schema_kind_enum": sorted(kind_enum),
    }


def validate_execution_host_runtime(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> dict[str, Any]:
    active_schema = schema if schema is not None else load_execution_host_schema()
    helper_errors = validate_execution_host_contract(obj)
    schema_errors = validate_execution_host_with_schema(obj, active_schema)
    status = "PASS" if not helper_errors and not schema_errors else "FAILED_VALIDATION"
    return {
        "status": status,
        "helper_valid": not helper_errors,
        "schema_valid": not schema_errors,
        "helper_validation_errors": helper_errors,
        "schema_validation_errors": schema_errors,
    }


def project_execution_host_contract(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    records = sample_records()
    for key, rel in PROJECTION_FILES.items():
        write_json(root / rel, records[key])
    report = {
        "schema_version": "aide.execution-host-contract-projection.v0",
        "report_type": "execution_host_contract_projection",
        "kind": "ExecutionHostContractProjectionReport",
        "task_id": TASK_ID,
        "status": "PASS_WITH_WARNINGS",
        "capability_label": FEATURE_FLAG,
        "accepted_provider_capability": ACCEPTED_PROVIDER_CAPABILITY,
        "projection_only": True,
        "record_kinds_written": sorted(record["kind"] for record in records.values()),
        "projections_written": [rel.as_posix() for rel in PROJECTION_FILES.values()],
        "operation_names": sorted(OPERATION_NAMES),
        "capability_execution_distinct": True,
        "worker_session_contract_defined": True,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "forbidden_operations_preserved": forbidden_operations_preserved(),
        **_false_boundaries(),
        "warnings": [
            "ExecutionHost contract is projection-only; no live host, worker execution, runtime, or transport is implemented.",
            "Capability execution remains separate and is represented only by the accepted provider capability reference.",
        ],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    write_future_and_unfinished_reports(root)
    return report


def execution_host_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    schema_path = root / SCHEMA_PATH
    data = {
        "schema_version": "aide.execution-host-contract-status.v0",
        "report_type": "execution_host_contract_status",
        "status": "PASS_WITH_WARNINGS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "schema_file_exists": schema_path.exists(),
        "schema_validation_mode": SCHEMA_VALIDATION_MODE,
        "capability_label": FEATURE_FLAG,
        "accepted_provider_capability": ACCEPTED_PROVIDER_CAPABILITY,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "operation_names": sorted(OPERATION_NAMES),
        "projection_only": True,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "forbidden_operations_preserved": forbidden_operations_preserved(),
        **_false_boundaries(),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    write_future_and_unfinished_reports(root)
    return data


def execution_host_validate(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    projection_result = project_execution_host_contract(root) if project else {"projections_written": []}
    projection_paths = [root / rel for rel in projection_result.get("projections_written", [])]
    schema_file_loaded = False
    schema_file_parsed = False
    schema_validation_executed = False
    schema_load_errors: list[str] = []
    alignment_result: dict[str, Any] = {}
    alignment_errors: list[str] = []
    alignment_warnings: list[str] = []
    validation_results: list[dict[str, Any]] = []
    runtime_validation_results: list[dict[str, Any]] = []
    try:
        schema = load_execution_host_schema(root)
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
        helper_errors = validate_execution_host_contract(obj)
        schema_errors: list[str] = []
        if schema_file_parsed:
            runtime = validate_execution_host_runtime(obj, schema)
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
        validation_results.append(
            {
                "path": projection_path.relative_to(root).as_posix(),
                "result": "PASS" if not errors else "FAILED_VALIDATION",
                "errors": errors,
                "helper_validation_errors": helper_errors,
                "schema_validation_errors": schema_errors,
            }
        )
    optional_runtime = (
        validate_execution_host_runtime(sample_unknown_optional_record(), schema)
        if schema_file_parsed
        else {"status": "FAILED_VALIDATION", "helper_validation_errors": [], "schema_validation_errors": schema_load_errors}
    )
    required_runtime = (
        validate_execution_host_runtime(sample_unknown_required_capability_record(), schema)
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
    projection_only_truthful = all(read_json(path)["status"]["projection_only"] is True for path in projection_paths)
    forbidden = forbidden_operations_preserved()
    all_records_valid = bool(validation_results) and all(item["result"] == "PASS" for item in validation_results)
    validation_errors = [*schema_load_errors, *alignment_errors, *[error for item in validation_results for error in item["errors"]]]
    status = (
        "PASS_WITH_WARNINGS"
        if not validation_errors
        and all_records_valid
        and projection_result.get("status") in {"PASS", "PASS_WITH_WARNINGS"}
        and schema_file_loaded
        and schema_file_parsed
        and schema_validation_executed
        and unknown_optional_fields_tolerated
        and unknown_required_capability_fails_closed
        and explicit_non_capabilities_preserved
        and projection_only_truthful
        and all(forbidden.values())
        else "FAILED_VALIDATION"
    )
    report = {
        "schema_version": "aide.execution-host-contract-validation.v0",
        "report_type": "execution_host_contract_validation",
        "kind": "ExecutionHostContractValidationReport",
        "task_id": TASK_ID,
        "status": status,
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_label": FEATURE_FLAG,
        "accepted_provider_capability": ACCEPTED_PROVIDER_CAPABILITY,
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "schema_file_exists": (root / SCHEMA_PATH).exists(),
        "schema_file_loaded": schema_file_loaded,
        "schema_file_parsed": schema_file_parsed,
        "schema_validation_executed": schema_validation_executed,
        "schema_validation_mode": SCHEMA_VALIDATION_MODE if schema_validation_executed else "unavailable",
        "schema_validation_limitations": SCHEMA_VALIDATION_LIMITATIONS,
        "schema_helper_alignment_checked": schema_file_parsed,
        "schema_helper_alignment_status": alignment_result.get("schema_helper_alignment_status", "FAILED_VALIDATION"),
        "alignment_errors": alignment_errors,
        "alignment_warnings": alignment_warnings,
        "validation_errors": validation_errors,
        "validation_results": validation_results,
        "runtime_validation_results": runtime_validation_results,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "record_kinds": sorted(RECORD_KINDS),
        "operation_names": sorted(OPERATION_NAMES),
        "projection_only_truthful": projection_only_truthful,
        "capability_execution_distinct": True,
        "worker_session_contract_defined": True,
        "explicit_non_capabilities_preserved": explicit_non_capabilities_preserved,
        "unknown_optional_fields_tolerated": unknown_optional_fields_tolerated,
        "unknown_required_capability_fails_closed": unknown_required_capability_fails_closed,
        "forbidden_operations_preserved": forbidden,
        **_false_boundaries(),
        "warnings": [
            "ExecutionHost contract v0 is projection-only and does not implement a live host.",
            "Worker/session execution remains separate from deterministic capability execution.",
            "LocalProcessExecutionHost is intentionally deferred to the next build after independent check and acceptance.",
            *alignment_warnings,
        ],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "unfinished_work": unfinished_work_items(),
        "future_work": future_work_items(),
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_markdown(report))
    write_future_and_unfinished_reports(root)
    return report


def forbidden_operations_preserved() -> dict[str, bool]:
    return {field: True for field in EXPLICIT_NON_CAPABILITIES}


def future_work_items() -> list[dict[str, str]]:
    return [
        {"task": "AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01", "reason": "independent review of projection-only contract, schema, helper validation, CLI, reports, tests, and non-capability boundaries"},
        {"task": "AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01", "reason": "accept the contract only after check and any required repair"},
        {"task": "AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01", "reason": "first live local reference host after contract acceptance"},
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    return [{"item": item, "reason": "intentionally deferred beyond the projection-only ExecutionHost contract v0 slice"} for item in EXPLICIT_NON_CAPABILITIES]


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# ExecutionHost Contract Status",
        "",
        f"- status: {data.get('status')}",
        f"- api_version: {data.get('api_version')}",
        f"- protocol_version: {data.get('protocol_version')}",
        f"- capability_label: {data.get('capability_label')}",
        f"- accepted_provider_capability: {data.get('accepted_provider_capability')}",
        f"- schema_file_path: {data.get('schema_file_path')}",
        f"- schema_file_exists: {str(data.get('schema_file_exists', False)).lower()}",
        f"- schema_validation_mode: {data.get('schema_validation_mode')}",
        "- projection_only: true",
        "- execution_host_runtime_implemented: false",
        "- worker_execution_implemented: false",
        "- provider_or_model_calls: none",
        "- network_calls: none",
        "- repository_mutation_performed: false",
        f"- recommended_next_task: {data.get('recommended_next_task')}",
        "",
        "## Supported Kinds",
        "",
    ]
    for kind in data.get("supported_kinds", []):
        lines.append(f"- {kind}")
    lines.extend(["", "## Operations", ""])
    for operation in data.get("operation_names", []):
        lines.append(f"- {operation}")
    lines.extend(["", "## Explicit Non-Capabilities", ""])
    for item in data.get("explicit_non_capabilities", []):
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def render_projection_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# ExecutionHost Contract Projection",
        "",
        f"- status: {report.get('status')}",
        f"- task_id: {report.get('task_id')}",
        f"- capability_label: {report.get('capability_label')}",
        f"- accepted_provider_capability: {report.get('accepted_provider_capability')}",
        "- projection_only: true",
        "- execution_host_runtime_implemented: false",
        "- worker_execution_implemented: false",
        "- provider_or_model_calls: none",
        "- network_calls: none",
        "- repository_mutation_performed: false",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Projections Written",
        "",
    ]
    for rel in report.get("projections_written", []):
        lines.append(f"- {rel}")
    lines.extend(["", "## Operations", ""])
    for operation in report.get("operation_names", []):
        lines.append(f"- {operation}")
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# ExecutionHost Contract Validation",
        "",
        f"- status: {report.get('status')}",
        f"- api_version: {report.get('api_version')}",
        f"- protocol_version: {report.get('protocol_version')}",
        f"- capability_label: {report.get('capability_label')}",
        f"- accepted_provider_capability: {report.get('accepted_provider_capability')}",
        f"- schema_file_path: {report.get('schema_file_path')}",
        f"- schema_file_loaded: {str(report.get('schema_file_loaded', False)).lower()}",
        f"- schema_file_parsed: {str(report.get('schema_file_parsed', False)).lower()}",
        f"- schema_validation_executed: {str(report.get('schema_validation_executed', False)).lower()}",
        f"- schema_validation_mode: {report.get('schema_validation_mode')}",
        f"- schema_helper_alignment_checked: {str(report.get('schema_helper_alignment_checked', False)).lower()}",
        f"- schema_helper_alignment_status: {report.get('schema_helper_alignment_status')}",
        f"- projection_only_truthful: {str(report.get('projection_only_truthful', False)).lower()}",
        f"- capability_execution_distinct: {str(report.get('capability_execution_distinct', False)).lower()}",
        f"- worker_session_contract_defined: {str(report.get('worker_session_contract_defined', False)).lower()}",
        f"- explicit_non_capabilities_preserved: {str(report.get('explicit_non_capabilities_preserved', False)).lower()}",
        f"- unknown_optional_fields_tolerated: {str(report.get('unknown_optional_fields_tolerated', False)).lower()}",
        f"- unknown_required_capability_fails_closed: {str(report.get('unknown_required_capability_fails_closed', False)).lower()}",
        "- execution_host_runtime_implemented: false",
        "- worker_execution_implemented: false",
        "- provider_or_model_calls: none",
        "- network_calls: none",
        "- repository_mutation_performed: false",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Validation Results",
        "",
    ]
    for item in report.get("validation_results", []):
        lines.append(f"- {item.get('result')}: {item.get('path')}")
    lines.extend(["", "## Operations", ""])
    for operation in report.get("operation_names", []):
        lines.append(f"- {operation}")
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    if report.get("validation_errors"):
        lines.extend(["", "## Errors", ""])
        for error in report.get("validation_errors", []):
            lines.append(f"- {error}")
    return "\n".join(lines) + "\n"


def write_future_and_unfinished_reports(repo_root: Path) -> None:
    future_lines = ["# ExecutionHost Contract Future Work", "", "## Recommended Order", ""]
    for index, item in enumerate(future_work_items(), start=1):
        future_lines.append(f"{index}. {item['task']}: {item['reason']}.")
    unfinished_lines = [
        "# ExecutionHost Contract Unfinished Work",
        "",
        "## Finished In This Slice",
        "",
        "- Projection-only ExecutionHost contract helper and validator.",
        "- Descriptor, run binding, event, artifact, approval, and usage record projections.",
        "- AIDE Lite status/project/validate command surface.",
        "- Local reports under `.aide/reports/execution-host-contract/`.",
        "",
        "## Not Attempted By Design",
        "",
    ]
    for item in unfinished_work_items():
        unfinished_lines.append(f"- {item['item']}: {item['reason']}.")
    write_text(repo_root / FUTURE_WORK_MD, "\n".join(future_lines) + "\n")
    write_text(repo_root / UNFINISHED_WORK_MD, "\n".join(unfinished_lines) + "\n")
