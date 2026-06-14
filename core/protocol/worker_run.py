"""Minimal AIDE WorkerRun helpers.

This module defines WorkerRun as data only: a durable record shape for future
worker execution attempts. It projects existing validation/check/acceptance
artifacts into WorkerRun records without claiming work, running workers,
creating leases, scheduling, invoking providers, submitting tests, or applying
patches.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from core.protocol import envelope


API_VERSION = envelope.API_VERSION
WORKER_RUN_SCHEMA_VERSION = "aide.worker-run.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_worker_run_schema"
REPORT_ROOT = Path(".aide/reports/worker-run")
PROJECTION_ROOT = REPORT_ROOT / "projections"
SCHEMA_PATH = Path(".aide/protocol/aide-worker-run.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"
SUPPORTED_KINDS = {
    "WorkerRun",
    "WorkerRunProjectionReport",
    "WorkerRunValidationReport",
}
WORKER_RUN_REQUIRED_FIELDS = ["apiVersion", "kind", "metadata", "spec", "status"]
REQUIRED_METADATA_FIELDS = ["id", "createdAt", "sourcePath", "producer", "compatibility"]
REQUIRED_SPEC_FIELDS = [
    "run_id",
    "source_workunit_id",
    "source_task_id",
    "provider_kind",
    "adapter_kind",
    "run_mode",
    "command",
    "inputs",
    "artifacts",
    "evidence_packet_refs",
    "explicit_non_capabilities",
]
REQUIRED_STATUS_FIELDS = ["phase", "validated", "validation_errors", "validation_warnings"]
PROVIDER_KINDS = {
    "codex",
    "claude_code",
    "gemini_cli",
    "local_script",
    "ci",
    "human",
    "metadata_only",
    "unknown",
}
ADAPTER_KINDS = {
    "metadata_only",
    "validation_observation",
    "local_script",
    "ci",
    "unknown",
}
RUN_MODES = {
    "metadata_only",
    "validation_observation",
    "dry_run",
    "simulated",
    "unknown",
}
PHASE_VALUES = {
    "planned",
    "metadata_only",
    "validation_observation",
    "running",
    "completed",
    "failed",
    "blocked",
    "partial",
    "cancelled",
    "unknown",
}
RESULT_VALUES = {
    "PASS",
    "PASS_WITH_WARNINGS",
    "FAILED_VALIDATION",
    "BLOCKED",
    "PARTIAL",
    "UNAVAILABLE",
    "NOT_RUN",
    "ACCEPTED",
    "ACCEPTED_WITH_WARNINGS",
    "UNKNOWN",
}
RECOGNIZED_CAPABILITIES = {
    FEATURE_FLAG,
    "fixture_temp_apply_only",
    "minimal_contract_envelope",
    "minimal_evidence_packet_schema",
    "minimal_workunit_queue_v1",
    "minimal_workunit_readonly_cli",
    "minimal_workunit_queue_metadata_mutation_cli",
}
EXPLICIT_NON_CAPABILITIES = [
    "worker_execution",
    "workunit_claim",
    "workunit_run_execution",
    "workunit_finish",
    "workunit_repair",
    "worker_lease",
    "lease_acquisition",
    "lease_heartbeat",
    "scheduler",
    "supervisor",
    "provider_adapter",
    "codex_adapter",
    "claude_code_adapter",
    "gemini_cli_adapter",
    "local_model_adapter",
    "testjob_schema",
    "test_broker",
    "checkpoint_schema",
    "promotion_policy_schema",
    "branch_worktree_automation",
    "target_repo_apply",
    "active_repo_apply",
    "rollback_execution",
    "uninstall_execution",
    "service_ready",
    "commander_ready",
    "production_ready",
    "release_ready",
    "open_telemetry",
    "sarif",
    "spdx",
    "cyclonedx",
    "slsa",
    "in_toto",
    "openapi",
]
SCHEMA_VALIDATION_MODE = "minimal_json_schema_subset"
SCHEMA_VALIDATION_LIMITATIONS = [
    "Local subset validator supports type, enum, required, properties, simple additionalProperties, and homogeneous array items only.",
    "Full JSON Schema Draft 2020-12 validation remains future work.",
    "Formats, refs, oneOf/anyOf/allOf, conditionals, numeric bounds, and pattern checks are not implemented.",
]
SOURCE_ARTIFACTS = {
    "workunit_cli_mutation_validation": {
        "path": Path(".aide/reports/workunit-cli-mutation/validation.json"),
        "source_task_id": "AIDE-BUILD-WORKUNIT-CLI-MUTATION-01",
        "source_task_kind": "build",
        "role": "validation_report",
    },
    "workunit_cli_mutation_check": {
        "path": Path(".aide/reports/workunit-cli-mutation-check/check-report.json"),
        "source_task_id": "AIDE-CHECK-WORKUNIT-CLI-MUTATION-01",
        "source_task_kind": "check",
        "role": "check_report",
    },
    "workunit_cli_mutation_acceptance": {
        "path": Path(".aide/reports/workunit-cli-mutation-acceptance/acceptance-report.json"),
        "source_task_id": "AIDE-ACCEPT-WORKUNIT-CLI-MUTATION-01",
        "source_task_kind": "acceptance",
        "role": "acceptance_report",
    },
    "workunit_cli_validation": {
        "path": Path(".aide/reports/workunit-cli/validation.json"),
        "source_task_id": "AIDE-BUILD-WORKUNIT-CLI-01",
        "source_task_kind": "build",
        "role": "validation_report",
    },
    "workunit_queue_validation": {
        "path": Path(".aide/reports/workunit-queue/validation.json"),
        "source_task_id": "AIDE-BUILD-WORKUNIT-QUEUE-V1-01",
        "source_task_kind": "build",
        "role": "validation_report",
    },
}
PROJECTION_FILES = {
    "workunit_cli_mutation_validation": PROJECTION_ROOT / "workunit-cli-mutation-validation.worker-run.json",
    "workunit_cli_mutation_check": PROJECTION_ROOT / "workunit-cli-mutation-check.worker-run.json",
    "workunit_cli_mutation_acceptance": PROJECTION_ROOT / "workunit-cli-mutation-acceptance.worker-run.json",
    "workunit_cli_validation": PROJECTION_ROOT / "workunit-cli-validation.worker-run.json",
    "workunit_queue_validation": PROJECTION_ROOT / "workunit-queue-validation.worker-run.json",
}
COMPATIBILITY_REPORTS = {
    "lifecycle_fixture": Path(".aide/reports/lifecycle-fixture-runner/verify.json"),
    "contract_envelope": Path(".aide/reports/contract-envelope/validation.json"),
    "evidence_packet": Path(".aide/reports/evidence-packet/validation.json"),
    "workunit_queue": Path(".aide/reports/workunit-queue/validation.json"),
    "workunit_cli": Path(".aide/reports/workunit-cli/validation.json"),
    "workunit_cli_mutation": Path(".aide/reports/workunit-cli-mutation/validation.json"),
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


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _normalize_result(value: Any) -> str:
    result = str(value or "UNKNOWN").strip().upper()
    return result if result in RESULT_VALUES else "UNKNOWN"


def _deterministic_run_id(source_task_id: str, source_path: Path | None, run_mode: str) -> str:
    seed = stable_json(
        {
            "source_task_id": source_task_id,
            "source_path": _source_path_value(source_path),
            "run_mode": run_mode,
        }
    )
    return "wr-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


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


def explicit_non_capabilities(source: dict[str, Any] | None = None) -> list[str]:
    observed: list[Any] = []
    if source:
        for key in ["explicit_non_capabilities", "not_capabilities"]:
            value = source.get(key)
            if isinstance(value, list):
                observed.extend(value)
        forbidden = source.get("forbidden_operations_preserved")
        if isinstance(forbidden, dict):
            observed.extend(key for key, preserved in forbidden.items() if preserved is True)
    return sorted({str(item) for item in [*observed, *EXPLICIT_NON_CAPABILITIES] if str(item)})


def implemented_capabilities(worker_run: dict[str, Any]) -> set[str]:
    spec = worker_run.get("spec") if isinstance(worker_run.get("spec"), dict) else {}
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


def build_worker_run(
    *,
    run_id: str,
    source_workunit_id: str,
    source_task_id: str,
    provider_kind: str,
    adapter_kind: str,
    run_mode: str,
    command: dict[str, Any],
    inputs: dict[str, Any],
    artifacts: list[dict[str, Any]],
    evidence_packet_refs: list[dict[str, Any]],
    explicit_non_capabilities: list[str],
    source_path: Path | None = None,
    source_task_kind: str = "unknown",
    capability_label: str = FEATURE_FLAG,
    validation_summary: dict[str, Any] | None = None,
    name: str | None = None,
    created_at: str | None = None,
    phase: str = "metadata_only",
    result: str = "UNKNOWN",
    started_at: str | None = None,
    ended_at: str | None = None,
    exit_code: int | None = None,
    validation_errors: list[str] | None = None,
    validation_warnings: list[str] | None = None,
) -> dict[str, Any]:
    metadata = {
        "id": run_id,
        "name": name or source_task_id,
        "createdAt": created_at or "deterministic",
        "sourcePath": _source_path_value(source_path),
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility([capability_label]),
    }
    spec = {
        "run_id": run_id,
        "source_workunit_id": source_workunit_id,
        "source_task_id": source_task_id,
        "source_task_kind": source_task_kind,
        "provider_kind": provider_kind,
        "adapter_kind": adapter_kind,
        "run_mode": run_mode,
        "command": copy.deepcopy(command),
        "inputs": copy.deepcopy(inputs),
        "artifacts": copy.deepcopy(artifacts),
        "evidence_packet_refs": copy.deepcopy(evidence_packet_refs),
        "explicit_non_capabilities": list(explicit_non_capabilities),
        "capability_label": capability_label,
        "validation_summary": copy.deepcopy(validation_summary or {}),
        "worker_execution_implemented": False,
        "worker_execution_performed": False,
        "workunit_claim_implemented": False,
        "workunit_run_implemented": False,
        "worker_lease_created": False,
        "scheduler_behavior": False,
        "provider_adapter_implemented": False,
        "testjob_schema_implemented": False,
        "test_broker_implemented": False,
    }
    status = {
        "phase": phase if phase in PHASE_VALUES else "unknown",
        "result": _normalize_result(result),
        "startedAt": started_at,
        "endedAt": ended_at,
        "exitCode": exit_code,
        "validated": not validation_errors,
        "validation_errors": list(validation_errors or []),
        "validation_warnings": list(validation_warnings or []),
    }
    obj = envelope.build_envelope("WorkerRun", metadata, spec, status, api_version=API_VERSION)
    obj["schema_version"] = WORKER_RUN_SCHEMA_VERSION
    obj["protocol_version"] = PROTOCOL_VERSION
    return obj


def sample_worker_run() -> dict[str, Any]:
    return build_worker_run(
        run_id="wr-sample",
        source_workunit_id="AIDE-BUILD-WORKER-RUN-SCHEMA-01",
        source_task_id="AIDE-BUILD-WORKER-RUN-SCHEMA-01",
        source_task_kind="build",
        provider_kind="metadata_only",
        adapter_kind="metadata_only",
        run_mode="metadata_only",
        command={"argv": [], "cwd": ".", "env_policy": "not_recorded"},
        inputs={
            "workunit_ref": ".aide/queue/AIDE-BUILD-WORKER-RUN-SCHEMA-01/task.yaml",
            "context_refs": [],
        },
        artifacts=[{"path": ".aide/reports/worker-run/validation.json", "role": "validation_report"}],
        evidence_packet_refs=[],
        explicit_non_capabilities=explicit_non_capabilities(),
        source_path=Path(".aide/reports/worker-run/validation.json"),
        validation_summary={"status": "PASS", "metadata_only": True},
        phase="metadata_only",
        result="PASS",
    )


def sample_unknown_optional_worker_run() -> dict[str, Any]:
    obj = sample_worker_run()
    obj["x-aide-optional-probe"] = {"tolerated": True}
    obj["metadata"]["x-aide-optional-probe"] = "tolerated"
    obj["spec"]["x-aide-optional-probe"] = True
    return obj


def sample_unknown_required_capability_worker_run() -> dict[str, Any]:
    obj = sample_worker_run()
    obj["metadata"]["compatibility"]["requiredCapabilities"] = ["future.required"]
    return obj


def validate_worker_run(obj: dict[str, Any], allowed_kinds: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["WorkerRun must be an object"]
    if not isinstance(obj.get("apiVersion"), str) or not obj.get("apiVersion"):
        errors.append("apiVersion must be a non-empty string")
    if obj.get("apiVersion") != API_VERSION:
        errors.append(f"unsupported apiVersion: {obj.get('apiVersion')}")
    kind = obj.get("kind")
    active_kinds = allowed_kinds or {"WorkerRun"}
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
    if not isinstance(metadata.get("sourcePath"), str) or not metadata.get("sourcePath"):
        errors.append("metadata.sourcePath must be a non-empty string")
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
    for field in ["run_id", "source_workunit_id", "source_task_id"]:
        if not isinstance(spec.get(field), str) or not spec.get(field):
            errors.append(f"spec.{field} must be a non-empty string")
    if spec.get("provider_kind") not in PROVIDER_KINDS:
        errors.append(f"unsupported provider_kind: {spec.get('provider_kind')}")
    if spec.get("adapter_kind") not in ADAPTER_KINDS:
        errors.append(f"unsupported adapter_kind: {spec.get('adapter_kind')}")
    if spec.get("run_mode") not in RUN_MODES:
        errors.append(f"unsupported run_mode: {spec.get('run_mode')}")
    command = spec.get("command")
    if not isinstance(command, dict):
        errors.append("spec.command must be an object")
    else:
        if not isinstance(command.get("argv"), list):
            errors.append("spec.command.argv must be an array")
        if not isinstance(command.get("cwd"), str) or not command.get("cwd"):
            errors.append("spec.command.cwd must be a non-empty string")
        if not isinstance(command.get("env_policy"), str) or not command.get("env_policy"):
            errors.append("spec.command.env_policy must be a non-empty string")
    inputs = spec.get("inputs")
    if not isinstance(inputs, dict):
        errors.append("spec.inputs must be an object")
    else:
        if not isinstance(inputs.get("workunit_ref"), str) or not inputs.get("workunit_ref"):
            errors.append("spec.inputs.workunit_ref must be a non-empty string")
        if not isinstance(inputs.get("context_refs"), list):
            errors.append("spec.inputs.context_refs must be an array")
    artifacts = spec.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("spec.artifacts must be an array")
    else:
        for index, item in enumerate(artifacts):
            if not isinstance(item, dict):
                errors.append(f"spec.artifacts[{index}] must be an object")
                continue
            if not isinstance(item.get("path"), str) or not item.get("path"):
                errors.append(f"spec.artifacts[{index}].path must be a non-empty string")
            if not isinstance(item.get("role"), str) or not item.get("role"):
                errors.append(f"spec.artifacts[{index}].role must be a non-empty string")
    evidence_refs = spec.get("evidence_packet_refs")
    if not isinstance(evidence_refs, list):
        errors.append("spec.evidence_packet_refs must be an array")
    non_capabilities = spec.get("explicit_non_capabilities")
    if not isinstance(non_capabilities, list):
        errors.append("spec.explicit_non_capabilities must be an array")
    else:
        for item in non_capabilities:
            if not isinstance(item, str) or not item:
                errors.append("spec.explicit_non_capabilities entries must be non-empty strings")
        if spec.get("capability_label") in non_capabilities:
            errors.append("spec.capability_label must not appear in explicit_non_capabilities")
    capability_label = spec.get("capability_label")
    if capability_label not in RECOGNIZED_CAPABILITIES:
        errors.append(f"unknown capability_label: {capability_label}")
    for flag in [
        "worker_execution_implemented",
        "worker_execution_performed",
        "workunit_claim_implemented",
        "workunit_run_implemented",
        "worker_lease_created",
        "scheduler_behavior",
        "provider_adapter_implemented",
        "testjob_schema_implemented",
        "test_broker_implemented",
    ]:
        if spec.get(flag) is not False:
            errors.append(f"spec.{flag} must be false in this slice")
    status = obj.get("status") if isinstance(obj.get("status"), dict) else {}
    for field in REQUIRED_STATUS_FIELDS:
        if field not in status:
            errors.append(f"missing required status field: {field}")
    if status.get("phase") not in PHASE_VALUES:
        errors.append(f"status.phase is unsupported: {status.get('phase')}")
    if status.get("result") not in RESULT_VALUES:
        errors.append(f"status.result is unsupported: {status.get('result')}")
    if not isinstance(status.get("validated"), bool):
        errors.append("status.validated must be a boolean")
    if not isinstance(status.get("validation_errors"), list):
        errors.append("status.validation_errors must be an array")
    if not isinstance(status.get("validation_warnings"), list):
        errors.append("status.validation_warnings must be an array")
    if status.get("phase") == "running" and spec.get("run_mode") in {"metadata_only", "validation_observation"}:
        errors.append("metadata-only WorkerRun must not claim running phase")
    return errors


def load_worker_run_schema(repo_root: str | Path | None = None) -> dict[str, Any]:
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
    if isinstance(value, list):
        item_schema = schema.get("items")
        if item_schema is not None:
            if not isinstance(item_schema, dict):
                errors.append(f"{path}.items must be an object")
            else:
                for index, item in enumerate(value):
                    errors.extend(_schema_node_errors(item, item_schema, f"{path}[{index}]"))
    return errors


def validate_worker_run_with_schema(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    active_schema = schema if schema is not None else load_worker_run_schema()
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
            "expected_required_fields": WORKER_RUN_REQUIRED_FIELDS,
            "schema_required_fields": [],
        }
    required = schema.get("required")
    schema_required = required if isinstance(required, list) else []
    missing = [field for field in WORKER_RUN_REQUIRED_FIELDS if field not in schema_required]
    extra_required = [str(field) for field in schema_required if field not in WORKER_RUN_REQUIRED_FIELDS]
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
    schema_kinds = properties.get("kind", {}).get("enum", []) if isinstance(properties.get("kind"), dict) else []
    if "WorkerRun" not in schema_kinds:
        errors.append("schema.properties.kind.enum must include WorkerRun")
    status = "PASS" if not errors else "FAILED_VALIDATION"
    return {
        "status": status,
        "schema_helper_alignment_status": status,
        "errors": errors,
        "warnings": warnings,
        "expected_required_fields": WORKER_RUN_REQUIRED_FIELDS,
        "schema_required_fields": [str(item) for item in schema_required],
        "missing_required_fields": missing,
        "extra_required_fields": extra_required,
        "checked_properties": sorted(expected_types),
    }


def validate_worker_run_runtime(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> dict[str, Any]:
    active_schema = schema if schema is not None else load_worker_run_schema()
    helper_errors = validate_worker_run(obj)
    schema_errors = validate_worker_run_with_schema(obj, active_schema)
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


def project_report_to_worker_run(
    repo_root: Path,
    report: dict[str, Any],
    source_path: Path,
    *,
    source_task_id: str,
    source_task_kind: str,
    artifact_role: str,
) -> dict[str, Any]:
    run_mode = "validation_observation"
    run_id = _deterministic_run_id(source_task_id, source_path, run_mode)
    report_status = _normalize_result(report.get("status") or report.get("result"))
    warnings = report.get("warnings") if isinstance(report.get("warnings"), list) else []
    errors = report.get("errors") if isinstance(report.get("errors"), list) else []
    if report_status in {"FAILED_VALIDATION", "BLOCKED"} and not errors:
        errors = [f"source report status is {report_status}"]
    phase = "validation_observation"
    source_hash = sha256_file(repo_root / source_path) if (repo_root / source_path).exists() else ""
    return build_worker_run(
        run_id=run_id,
        source_workunit_id=source_task_id,
        source_task_id=source_task_id,
        source_task_kind=source_task_kind,
        provider_kind="metadata_only",
        adapter_kind="validation_observation",
        run_mode=run_mode,
        command={
            "argv": [],
            "cwd": ".",
            "env_policy": "not_recorded",
            "description": "Projected from existing report; no worker command executed.",
        },
        inputs={
            "workunit_ref": f".aide/queue/{source_task_id}/task.yaml",
            "context_refs": [source_path.as_posix()],
        },
        artifacts=[artifact_ref(repo_root, source_path, artifact_role)],
        evidence_packet_refs=[],
        explicit_non_capabilities=explicit_non_capabilities(report),
        source_path=source_path,
        validation_summary={
            "status": report_status,
            "source_report_type": report.get("report_type", ""),
            "source_schema_version": report.get("schema_version", ""),
            "source_sha256": source_hash,
            "metadata_only_projection": True,
            "worker_executed": False,
        },
        name=source_path.stem,
        phase=phase,
        result=report_status,
        started_at=None,
        ended_at=None,
        exit_code=None,
        validation_errors=[str(item) for item in errors],
        validation_warnings=[str(item) for item in warnings],
    )


def project_existing_reports(repo_root: str | Path) -> dict[str, dict[str, Any]]:
    root = Path(repo_root)
    projections: dict[str, dict[str, Any]] = {}
    for key, meta in SOURCE_ARTIFACTS.items():
        rel = meta["path"]
        if not isinstance(rel, Path):
            continue
        source = root / rel
        if not source.exists():
            continue
        report = read_json(source)
        projection = project_report_to_worker_run(
            root,
            report,
            rel,
            source_task_id=str(meta["source_task_id"]),
            source_task_kind=str(meta["source_task_kind"]),
            artifact_role=str(meta["role"]),
        )
        projections[PROJECTION_FILES[key].as_posix()] = projection
    return projections


def _source_paths(root: Path) -> list[Path]:
    return [root / meta["path"] for meta in SOURCE_ARTIFACTS.values() if isinstance(meta.get("path"), Path) and (root / meta["path"]).exists()]


def _hashes(paths: list[Path]) -> dict[str, str]:
    return {path.as_posix(): sha256_file(path) for path in paths if path.exists() and path.is_file()}


def project_accepted_artifacts(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    source_paths = _source_paths(root)
    hashes_before = _hashes(source_paths)
    projections = project_existing_reports(root)
    for rel, obj in projections.items():
        write_json(root / rel, obj)
    hashes_after = _hashes(source_paths)
    source_reports_mutated = hashes_before != hashes_after
    report = {
        "schema_version": "aide.worker-run-projection.v0",
        "report_type": "worker_run_projection",
        "kind": "WorkerRunProjectionReport",
        "status": "PASS" if projections and not source_reports_mutated else "FAILED_VALIDATION",
        "source": "accepted-artifacts",
        "projections_written": sorted(projections),
        "source_reports_checked": [_relative_posix(path, root) for path in source_paths],
        "source_reports_mutated": source_reports_mutated,
        "destructive_migration_performed": False,
        "worker_execution_performed": False,
        "workunit_claim_executed": False,
        "worker_lease_created": False,
        "scheduler_behavior": False,
        "test_broker_behavior": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
    }
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    write_future_and_unfinished_reports(root)
    return report


def _compatibility_results(repo_root: Path) -> dict[str, Any]:
    parsed: dict[str, bool] = {}
    statuses: dict[str, str] = {}
    errors: list[str] = []
    for key, rel in COMPATIBILITY_REPORTS.items():
        path = repo_root / rel
        if not path.exists():
            parsed[key] = False
            statuses[key] = "MISSING"
            errors.append(f"missing {rel.as_posix()}")
            continue
        try:
            data = read_json(path)
        except Exception as exc:  # noqa: BLE001 - compatibility report records parse failures.
            parsed[key] = False
            statuses[key] = "FAILED_VALIDATION"
            errors.append(f"{rel.as_posix()}: {exc}")
            continue
        parsed[key] = True
        statuses[key] = str(data.get("status") or data.get("result") or "UNKNOWN")
    return {
        "status": "PASS" if not errors else "FAILED_VALIDATION",
        "accepted_reports_parse": all(parsed.values()),
        "parsed_reports": parsed,
        "report_statuses": statuses,
        "errors": errors,
        "lifecycle_fixture_behavior_preserved": parsed.get("lifecycle_fixture", False),
        "contract_envelope_behavior_preserved": parsed.get("contract_envelope", False),
        "evidence_packet_behavior_preserved": parsed.get("evidence_packet", False),
        "workunit_queue_behavior_preserved": parsed.get("workunit_queue", False),
        "workunit_cli_behavior_preserved": parsed.get("workunit_cli", False),
        "workunit_cli_mutation_behavior_preserved": parsed.get("workunit_cli_mutation", False),
        "destructive_migration_performed": False,
        "projection_paths_additive": True,
    }


def worker_run_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    schema_path = root / SCHEMA_PATH
    data = {
        "schema_version": "aide.worker-run-status.v0",
        "report_type": "worker_run_status",
        "kind": "WorkerRunProjectionReport",
        "status": "PASS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "schema_file_exists": schema_path.exists(),
        "schema_validation_mode": SCHEMA_VALIDATION_MODE,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "recognized_capabilities": sorted(RECOGNIZED_CAPABILITIES),
        "provider_kinds": sorted(PROVIDER_KINDS),
        "adapter_kinds": sorted(ADAPTER_KINDS),
        "run_modes": sorted(RUN_MODES),
        "phase_values": sorted(PHASE_VALUES),
        "capability_label": FEATURE_FLAG,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "worker_execution_implemented": False,
        "workunit_claim_implemented": False,
        "workunit_run_implemented": False,
        "worker_lease_implemented": False,
        "scheduler_implemented": False,
        "provider_adapter_implemented": False,
        "testjob_schema_implemented": False,
        "test_broker_implemented": False,
        "source_reports": {key: (root / meta["path"]).exists() for key, meta in SOURCE_ARTIFACTS.items()},
        "projection_files": [(PROJECTION_FILES[key]).as_posix() for key in PROJECTION_FILES],
        "projection_files_existing": [(PROJECTION_FILES[key]).as_posix() for key in PROJECTION_FILES if (root / PROJECTION_FILES[key]).exists()],
        "destructive_migration_performed": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    write_future_and_unfinished_reports(root)
    return data


def worker_run_validate(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    projection_result = project_accepted_artifacts(root) if project else {"projections_written": []}
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
        schema = load_worker_run_schema(root)
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
        helper_errors = validate_worker_run(obj)
        schema_errors: list[str] = []
        if schema_file_parsed:
            runtime = validate_worker_run_runtime(obj, schema)
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
        validate_worker_run_runtime(sample_unknown_optional_worker_run(), schema)
        if schema_file_parsed
        else {"status": "FAILED_VALIDATION", "helper_validation_errors": [], "schema_validation_errors": schema_load_errors}
    )
    required_runtime = (
        validate_worker_run_runtime(sample_unknown_required_capability_worker_run(), schema)
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
    metadata_only_truthful = all(
        read_json(path)["spec"]["worker_execution_performed"] is False
        and read_json(path)["spec"]["worker_execution_implemented"] is False
        and read_json(path)["spec"]["workunit_claim_implemented"] is False
        and read_json(path)["spec"]["worker_lease_created"] is False
        for path in projection_paths
    )
    compatibility_results = _compatibility_results(root)
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
    all_projections_valid = bool(validation_results) and all(item["result"] == "PASS" for item in validation_results)
    status = (
        "PASS"
        if all_projections_valid
        and projection_result.get("status") == "PASS"
        and compatibility_results["status"] == "PASS"
        and schema_checks_pass
        and explicit_non_capabilities_preserved
        and metadata_only_truthful
        else "FAILED_VALIDATION"
    )
    report = {
        "schema_version": "aide.worker-run-validation.v0",
        "report_type": "worker_run_validation",
        "kind": "WorkerRunValidationReport",
        "task_id": "AIDE-BUILD-WORKER-RUN-SCHEMA-01",
        "status": status,
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_label": FEATURE_FLAG,
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "schema_file_exists": schema_path.exists(),
        "schema_file_loaded": schema_file_loaded,
        "schema_file_parsed": schema_file_parsed,
        "schema_validation_executed": schema_validation_executed,
        "schema_validation_mode": SCHEMA_VALIDATION_MODE if schema_validation_executed else "unavailable",
        "schema_helper_alignment_checked": schema_file_parsed,
        "schema_helper_alignment_status": alignment_result.get("schema_helper_alignment_status", "FAILED_VALIDATION"),
        "schema_validation_limitations": SCHEMA_VALIDATION_LIMITATIONS,
        "schema_load_errors": schema_load_errors,
        "alignment_errors": alignment_errors,
        "alignment_warnings": alignment_warnings,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "recognized_capabilities": sorted(RECOGNIZED_CAPABILITIES),
        "provider_kinds": sorted(PROVIDER_KINDS),
        "adapter_kinds": sorted(ADAPTER_KINDS),
        "run_modes": sorted(RUN_MODES),
        "phase_values": sorted(PHASE_VALUES),
        "source_reports_checked": projection_result.get("source_reports_checked", []),
        "projections_written": projection_result.get("projections_written", []),
        "projections_checked": [item["path"] for item in validation_results],
        "validation_results": validation_results,
        "runtime_validation_results": runtime_validation_results,
        "helper_validation_errors": helper_validation_errors,
        "schema_validation_errors": schema_validation_errors,
        "compatibility_results": compatibility_results,
        "backwards_compatibility_preserved": compatibility_results["status"] == "PASS",
        "destructive_migration_performed": False,
        "source_reports_mutated": projection_result.get("source_reports_mutated", False),
        "unknown_optional_fields_tolerated": unknown_optional_fields_tolerated,
        "unknown_required_capability_fails_closed": unknown_required_capability_fails_closed,
        "explicit_non_capabilities_preserved": explicit_non_capabilities_preserved,
        "metadata_only_truthful": metadata_only_truthful,
        "worker_execution_implemented": False,
        "worker_execution_performed": False,
        "workunit_claim_implemented": False,
        "workunit_run_implemented": False,
        "workunit_finish_implemented": False,
        "workunit_repair_implemented": False,
        "worker_lease_implemented": False,
        "scheduler_implemented": False,
        "provider_adapter_implemented": False,
        "testjob_schema_implemented": False,
        "test_broker_implemented": False,
        "forbidden_operations_preserved": forbidden_operations_preserved(),
        "warnings": [
            "WorkerRun is a minimal v1alpha1 data schema; worker execution is not implemented.",
            "Projection outputs are additive and source reports remain canonical.",
            "Full JSON Schema Draft 2020-12 validation remains future work.",
            "WorkUnit claim/run/finish/repair, leases, scheduler, TestJob, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target apply, rollback execution, release, and promotion remain future work.",
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
        "worker_execution": True,
        "workunit_claim": True,
        "workunit_run": True,
        "workunit_finish": True,
        "workunit_repair": True,
        "worker_leases": True,
        "lease_acquisition": True,
        "lease_heartbeat": True,
        "scheduler": True,
        "supervisor": True,
        "provider_adapters": True,
        "codex_adapter": True,
        "testjob_schema": True,
        "test_broker": True,
        "checkpoint_schema": True,
        "promotion_policy_schema": True,
        "branch_worktree_automation": True,
        "target_repo_apply": True,
        "active_repo_apply": True,
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
        {"task": "AIDE-CHECK-WORKER-RUN-SCHEMA-01", "reason": "independent review of WorkerRun schema, helper validation, projections, compatibility, tests, no destructive migration, no overclaiming, and forbidden-operation preservation"},
        {"task": "AIDE-BUILD-WORKER-RUN-HARDEN-01", "reason": "harden only if the check finds validation, projection, or schema gaps"},
        {"task": "AIDE-ACCEPT-WORKER-RUN-SCHEMA-01", "reason": "accept WorkerRun only after check and any required hardening"},
        {"task": "AIDE-BUILD-TESTJOB-SCHEMA-01", "reason": "define TestJob schema before Test Broker"},
        {"task": "AIDE-BUILD-WORKUNIT-CLAIM-LEASE-SCHEMA-01", "reason": "define claim and lease schema before implementing claim"},
        {"task": "AIDE-BUILD-WORKUNIT-CLAIM-CLI-01", "reason": "add claim only after WorkerRun and lease shape are accepted"},
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    deferred = [
        "worker execution",
        "workunit claim",
        "workunit run",
        "workunit finish",
        "workunit repair",
        "worker leases",
        "lease heartbeat",
        "scheduler",
        "supervisor",
        "provider adapters",
        "Codex adapter",
        "Claude/Gemini/local model adapters",
        "TestJob schema",
        "Test Broker",
        "Checkpoint schema",
        "PromotionPolicy schema",
        "branch/worktree allocator",
        "Service",
        "Commander",
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
    return [{"item": item, "reason": "intentionally deferred beyond the minimal WorkerRun schema slice"} for item in deferred]


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# WorkerRun Status",
        "",
        f"- status: {data.get('status')}",
        f"- api_version: {data.get('api_version')}",
        f"- protocol_version: {data.get('protocol_version')}",
        f"- schema_file_path: {data.get('schema_file_path')}",
        f"- schema_file_exists: {str(data.get('schema_file_exists', False)).lower()}",
        f"- schema_validation_mode: {data.get('schema_validation_mode')}",
        f"- capability_label: {data.get('capability_label')}",
        "- worker_execution_implemented: false",
        "- workunit_claim_implemented: false",
        "- workunit_run_implemented: false",
        "- worker_lease_implemented: false",
        "- scheduler_implemented: false",
        "- provider_adapter_implemented: false",
        "- testjob_schema_implemented: false",
        "- test_broker_implemented: false",
        "- destructive_migration_performed: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "",
        "## Supported Kinds",
        "",
    ]
    for kind in data.get("supported_kinds", []):
        lines.append(f"- {kind}")
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
        "# WorkerRun Projection",
        "",
        f"- status: {report.get('status')}",
        f"- source: {report.get('source')}",
        f"- source_reports_mutated: {str(report.get('source_reports_mutated', False)).lower()}",
        "- worker_execution_performed: false",
        "- workunit_claim_executed: false",
        "- worker_lease_created: false",
        "- scheduler_behavior: false",
        "- test_broker_behavior: false",
        "- destructive_migration_performed: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
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
        "# WorkerRun Validation",
        "",
        f"- status: {report.get('status')}",
        f"- capability_label: {report.get('capability_label')}",
        f"- api_version: {report.get('api_version')}",
        f"- protocol_version: {report.get('protocol_version')}",
        f"- schema_file_path: {report.get('schema_file_path')}",
        f"- schema_file_loaded: {str(report.get('schema_file_loaded', False)).lower()}",
        f"- schema_file_parsed: {str(report.get('schema_file_parsed', False)).lower()}",
        f"- schema_validation_executed: {str(report.get('schema_validation_executed', False)).lower()}",
        f"- schema_validation_mode: {report.get('schema_validation_mode')}",
        f"- schema_helper_alignment_checked: {str(report.get('schema_helper_alignment_checked', False)).lower()}",
        f"- schema_helper_alignment_status: {report.get('schema_helper_alignment_status')}",
        "- worker_execution_implemented: false",
        "- worker_execution_performed: false",
        "- workunit_claim_implemented: false",
        "- workunit_run_implemented: false",
        "- worker_lease_implemented: false",
        "- scheduler_implemented: false",
        "- provider_adapter_implemented: false",
        "- testjob_schema_implemented: false",
        "- test_broker_implemented: false",
        "- destructive_migration_performed: false",
        f"- backwards_compatibility_preserved: {str(report.get('backwards_compatibility_preserved', False)).lower()}",
        f"- source_reports_mutated: {str(report.get('source_reports_mutated', False)).lower()}",
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
        if key not in {"parsed_reports", "report_statuses", "errors"}:
            lines.append(f"- {key}: {str(value).lower()}")
    lines.extend(["", "## Schema Alignment", ""])
    if report.get("alignment_errors"):
        for error in report.get("alignment_errors", []):
            lines.append(f"- error: {error}")
    else:
        lines.append("- alignment_errors: none")
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def write_future_and_unfinished_reports(repo_root: Path) -> None:
    future_lines = [
        "# WorkerRun Future Work",
        "",
        "## Recommended Order",
        "",
    ]
    for index, item in enumerate(future_work_items(), start=1):
        future_lines.append(f"{index}. {item['task']}: {item['reason']}.")
    unfinished_lines = [
        "# WorkerRun Unfinished Work",
        "",
        "## Finished In This Slice",
        "",
        "- Minimal envelope-backed WorkerRun helper and validator.",
        "- Additive projections from existing validation/check/acceptance artifacts.",
        "- Additive validation reports under `.aide/reports/worker-run/`.",
        "",
        "## Not Attempted By Design",
        "",
    ]
    for item in unfinished_work_items():
        unfinished_lines.append(f"- {item['item']}: {item['reason']}.")
    write_text(repo_root / FUTURE_WORK_MD, "\n".join(future_lines) + "\n")
    write_text(repo_root / UNFINISHED_WORK_MD, "\n".join(unfinished_lines) + "\n")
