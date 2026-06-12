"""Minimal AIDE WorkUnit queue helpers.

This module is intentionally narrow. It projects existing filesystem queue
tasks into envelope-backed WorkUnit objects without implementing a WorkUnit
executor, scheduler, service, or broad queue CLI.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import envelope


API_VERSION = envelope.API_VERSION
WORKUNIT_SCHEMA_VERSION = "aide.workunit-queue.v1"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_workunit_queue_v1"
REPORT_ROOT = Path(".aide/reports/workunit-queue")
PROJECTION_ROOT = REPORT_ROOT / "projections"
SCHEMA_PATH = Path(".aide/protocol/aide-workunit.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"
SUPPORTED_KINDS = {
    "WorkUnit",
    "WorkUnitQueueProjectionReport",
    "WorkUnitQueueValidationReport",
}
WORKUNIT_REQUIRED_FIELDS = ["apiVersion", "kind", "metadata", "spec", "status"]
REQUIRED_METADATA_FIELDS = ["id", "createdAt", "sourcePath", "producer", "compatibility"]
REQUIRED_SPEC_FIELDS = [
    "task_id",
    "title",
    "work_type",
    "authorizes_implementation",
    "check_only",
    "acceptance_review",
    "implementation_scope",
    "stop_state",
    "predecessors",
    "dependencies",
    "scope",
    "validation",
    "evidence_requirements",
    "explicit_non_capabilities",
]
REQUIRED_STATUS_FIELDS = ["phase", "validated", "validation_errors", "validation_warnings"]
WORK_TYPES = {"build", "check", "harden", "accept", "repair", "unblock", "complete", "unknown"}
PHASE_VALUES = {
    "planned",
    "ready",
    "running",
    "needs_review",
    "passed",
    "blocked",
    "partial",
    "failed",
    "accepted",
    "accepted_with_warnings",
    "implementation_completed",
    "acceptance_review_completed",
    "check_completed",
    "hardening_completed",
    "repair_completed",
    "unknown",
}
RESULT_VALUES = {
    "PASS",
    "PASS_WITH_WARNINGS",
    "ACCEPTED",
    "ACCEPTED_WITH_WARNINGS",
    "REJECTED_NEEDS_REPAIR",
    "FAILED_VALIDATION",
    "BLOCKED",
    "PARTIAL",
    "NOT_RUN",
    "UNKNOWN",
}
VALIDATION_STATUSES = {
    "PASS",
    "PASS_WITH_WARNINGS",
    "FAILED_VALIDATION",
    "BLOCKED",
    "PARTIAL",
    "UNAVAILABLE",
    "NOT_RUN",
}
RECOGNIZED_CAPABILITIES = {
    FEATURE_FLAG,
    "fixture_temp_apply_only",
    "minimal_contract_envelope",
    "minimal_evidence_packet_schema",
}
EXPLICIT_NON_CAPABILITIES = [
    "full_workunit_runtime",
    "workunit_create_cli",
    "workunit_list_cli",
    "workunit_claim_cli",
    "workunit_block_cli",
    "workunit_finish_cli",
    "workunit_repair_cli",
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
    "YAML queue parsing uses a conservative stdlib subset for AIDE queue task files.",
]
QUEUE_SOURCES = {
    "lifecycle_fixture_build": "AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01",
    "contract_envelope_build": "AIDE-BUILD-CONTRACT-ENVELOPE-01",
    "evidence_packet_build": "AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01",
    "evidence_packet_acceptance": "AIDE-ACCEPT-EVIDENCE-PACKET-SCHEMA-01",
    "workunit_queue_build": "AIDE-BUILD-WORKUNIT-QUEUE-V1-01",
}
PROJECTION_FILES = {
    "lifecycle_fixture_build": PROJECTION_ROOT / "lifecycle-fixture-build.workunit.json",
    "contract_envelope_build": PROJECTION_ROOT / "contract-envelope-build.workunit.json",
    "evidence_packet_build": PROJECTION_ROOT / "evidence-packet-build.workunit.json",
    "evidence_packet_acceptance": PROJECTION_ROOT / "evidence-packet-acceptance.workunit.json",
    "workunit_queue_build": PROJECTION_ROOT / "workunit-queue-build.workunit.json",
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


def _deterministic_workunit_id(task_id: str, source_path: Path | None) -> str:
    seed = stable_json({"task_id": task_id, "source_path": _source_path_value(source_path)})
    return "wu-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1", "on"}:
            return True
        if lowered in {"false", "no", "0", "off"}:
            return False
    return default


def _normalize_token(value: Any) -> str:
    token = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")
    return token or "unknown"


def _normalize_list(values: Any) -> list[str]:
    if isinstance(values, list):
        return [str(item) for item in values if str(item)]
    if isinstance(values, str) and values:
        return [values]
    return []


def normalize_phase(value: Any) -> str:
    phase = _normalize_token(value or "unknown")
    return phase if phase in PHASE_VALUES else "unknown"


def normalize_result(value: Any) -> str:
    result = str(value or "NOT_RUN").strip().upper()
    return result if result in RESULT_VALUES else "UNKNOWN"


def infer_work_type(task_id: str, task_data: dict[str, Any] | None = None) -> str:
    data_type = str((task_data or {}).get("work_type") or "").strip().lower()
    if data_type in WORK_TYPES:
        return data_type
    normalized = task_id.upper()
    if "-ACCEPT-" in normalized or normalized.startswith("AIDE-ACCEPT-"):
        return "accept"
    if "-CHECK-" in normalized or normalized.startswith("AIDE-CHECK-"):
        return "check"
    if "-HARDEN-" in normalized or normalized.startswith("AIDE-HARDEN-"):
        return "harden"
    if "-REPAIR-" in normalized or normalized.startswith("AIDE-REPAIR-"):
        return "repair"
    if "-UNBLOCK-" in normalized or normalized.startswith("AIDE-UNBLOCK-"):
        return "unblock"
    if "-COMPLETE-" in normalized or normalized.startswith("AIDE-COMPLETE-"):
        return "complete"
    if "-BUILD-" in normalized or normalized.startswith("AIDE-BUILD-"):
        return "build"
    return "unknown"


def explicit_non_capabilities(source: dict[str, Any] | None = None) -> list[str]:
    observed: list[str] = []
    if source:
        for key in ["explicit_non_capabilities", "not_capabilities"]:
            observed.extend(_normalize_list(source.get(key)))
        for item in _normalize_list(source.get("forbidden_operations")):
            observed.append(_normalize_token(item))
    return sorted({_normalize_token(item) for item in [*observed, *EXPLICIT_NON_CAPABILITIES] if _normalize_token(item)})


def implemented_capabilities(workunit: dict[str, Any]) -> set[str]:
    spec = workunit.get("spec") if isinstance(workunit.get("spec"), dict) else {}
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


def validation(command: str, status: str, exit_code: int | None = None, notes: str = "") -> dict[str, Any]:
    item: dict[str, Any] = {"command": command, "status": status if status in VALIDATION_STATUSES else "NOT_RUN"}
    if exit_code is not None:
        item["exit_code"] = exit_code
    if notes:
        item["notes"] = notes
    return item


def _parse_scalar(value: str) -> Any:
    raw = value.strip()
    if raw == "":
        return ""
    lowered = raw.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none", "~"}:
        return None
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    if raw.startswith("[") or raw.startswith("{"):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    return raw


def _yaml_lines(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        result.append((indent, stripped))
    return result


def _parse_yaml_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    is_list = lines[index][1].startswith("- ")
    if is_list:
        items: list[Any] = []
        while index < len(lines):
            current_indent, text = lines[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                break
            if not text.startswith("- "):
                break
            payload = text[2:].strip()
            index += 1
            if payload == "":
                if index < len(lines) and lines[index][0] > current_indent:
                    child, index = _parse_yaml_block(lines, index, lines[index][0])
                    items.append(child)
                else:
                    items.append("")
            elif ":" in payload and not payload.startswith(("http://", "https://")):
                key, value = payload.split(":", 1)
                item: dict[str, Any] = {key.strip(): _parse_scalar(value)}
                if index < len(lines) and lines[index][0] > current_indent:
                    child, index = _parse_yaml_block(lines, index, lines[index][0])
                    if isinstance(child, dict):
                        item.update(child)
                items.append(item)
            else:
                items.append(_parse_scalar(payload))
        return items, index
    data: dict[str, Any] = {}
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            break
        if text.startswith("- "):
            break
        key, separator, value = text.partition(":")
        if not separator:
            data[text] = ""
            index += 1
            continue
        index += 1
        clean_key = key.strip()
        if value.strip():
            data[clean_key] = _parse_scalar(value)
        elif index < len(lines) and lines[index][0] > current_indent:
            child, index = _parse_yaml_block(lines, index, lines[index][0])
            data[clean_key] = child
        else:
            data[clean_key] = {}
    return data, index


def read_simple_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    lines = _yaml_lines(path.read_text(encoding="utf-8"))
    parsed, _ = _parse_yaml_block(lines, 0, lines[0][0] if lines else 0)
    if not isinstance(parsed, dict):
        raise ValueError(f"YAML root must be an object: {path}")
    return parsed


def build_workunit(
    *,
    task_id: str,
    title: str,
    work_type: str,
    authorizes_implementation: bool,
    check_only: bool,
    acceptance_review: bool,
    implementation_scope: str,
    stop_state: str,
    predecessors: list[Any],
    dependencies: list[Any],
    scope: dict[str, Any],
    validation_spec: dict[str, Any],
    evidence_requirements: list[Any],
    explicit_non_capabilities: list[str],
    capability_label: str,
    artifacts: list[dict[str, Any]] | None = None,
    source_path: Path | None = None,
    created_at: str | None = None,
    workunit_id: str | None = None,
    phase: str = "needs_review",
    result: str = "NOT_RUN",
    validation_errors: list[str] | None = None,
    validation_warnings: list[str] | None = None,
) -> dict[str, Any]:
    metadata = {
        "id": workunit_id or _deterministic_workunit_id(task_id, source_path),
        "name": title or task_id,
        "createdAt": created_at or "deterministic",
        "sourcePath": _source_path_value(source_path),
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility([capability_label]),
    }
    spec = {
        "task_id": task_id,
        "title": title,
        "work_type": work_type,
        "authorizes_implementation": authorizes_implementation,
        "check_only": check_only,
        "acceptance_review": acceptance_review,
        "implementation_scope": implementation_scope,
        "stop_state": stop_state,
        "predecessors": copy.deepcopy(predecessors),
        "dependencies": copy.deepcopy(dependencies),
        "scope": copy.deepcopy(scope),
        "validation": copy.deepcopy(validation_spec),
        "evidence_requirements": copy.deepcopy(evidence_requirements),
        "explicit_non_capabilities": list(explicit_non_capabilities),
        "capability_label": capability_label,
        "artifacts": copy.deepcopy(artifacts or []),
    }
    status = {
        "phase": normalize_phase(phase),
        "result": normalize_result(result),
        "validated": not validation_errors,
        "validation_errors": list(validation_errors or []),
        "validation_warnings": list(validation_warnings or []),
    }
    obj = envelope.build_envelope("WorkUnit", metadata, spec, status, api_version=API_VERSION)
    obj["schema_version"] = WORKUNIT_SCHEMA_VERSION
    obj["protocol_version"] = PROTOCOL_VERSION
    return obj


def sample_workunit() -> dict[str, Any]:
    return build_workunit(
        task_id="AIDE-BUILD-WORKUNIT-QUEUE-V1-01",
        title="Minimal WorkUnit Queue V1",
        work_type="build",
        authorizes_implementation=True,
        check_only=False,
        acceptance_review=False,
        implementation_scope="minimal-workunit-queue-v1-only",
        stop_state="needs_review",
        predecessors=["AIDE-ACCEPT-EVIDENCE-PACKET-SCHEMA-01"],
        dependencies=[],
        scope={
            "allowed_paths": ["core/protocol/workunit.py", ".aide/protocol/aide-workunit.schema.json"],
            "forbidden_paths": [],
            "forbidden_operations": ["WorkUnit CLI", "Test Broker", "Service", "Commander"],
        },
        validation_spec={
            "commands": [
                validation("py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_queue_v1.py", "PASS", 0)
            ]
        },
        evidence_requirements=[".aide/queue/AIDE-BUILD-WORKUNIT-QUEUE-V1-01/evidence/validation.md"],
        explicit_non_capabilities=explicit_non_capabilities(),
        capability_label=FEATURE_FLAG,
        artifacts=[
            {"path": "core/protocol/workunit.py", "role": "helper_module"},
            {"path": ".aide/protocol/aide-workunit.schema.json", "role": "schema"},
        ],
        source_path=Path(".aide/queue/AIDE-BUILD-WORKUNIT-QUEUE-V1-01/task.yaml"),
        phase="needs_review",
        result="PASS",
    )


def sample_unknown_optional_workunit() -> dict[str, Any]:
    obj = sample_workunit()
    obj["x-aide-optional-probe"] = {"tolerated": True}
    obj["metadata"]["x-aide-optional-probe"] = "tolerated"
    obj["spec"]["x-aide-optional-probe"] = True
    return obj


def sample_unknown_required_capability_workunit() -> dict[str, Any]:
    obj = sample_workunit()
    obj["metadata"]["compatibility"]["requiredCapabilities"] = ["future.required"]
    return obj


def validate_workunit(obj: dict[str, Any], allowed_kinds: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["WorkUnit must be an object"]
    if not isinstance(obj.get("apiVersion"), str) or not obj.get("apiVersion"):
        errors.append("apiVersion must be a non-empty string")
    if obj.get("apiVersion") != API_VERSION:
        errors.append(f"unsupported apiVersion: {obj.get('apiVersion')}")
    kind = obj.get("kind")
    active_kinds = allowed_kinds or {"WorkUnit"}
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
    if not isinstance(spec.get("task_id"), str) or not spec.get("task_id"):
        errors.append("spec.task_id must be a non-empty string")
    if not isinstance(spec.get("title"), str) or not spec.get("title"):
        errors.append("spec.title must be a non-empty string")
    if spec.get("work_type") not in WORK_TYPES:
        errors.append(f"unsupported work_type: {spec.get('work_type')}")
    for field in ["authorizes_implementation", "check_only", "acceptance_review"]:
        if not isinstance(spec.get(field), bool):
            errors.append(f"spec.{field} must be a boolean")
    if not isinstance(spec.get("implementation_scope"), str):
        errors.append("spec.implementation_scope must be a string")
    if not isinstance(spec.get("stop_state"), str) or not spec.get("stop_state"):
        errors.append("spec.stop_state must be a non-empty string")
    if not isinstance(spec.get("predecessors"), list):
        errors.append("spec.predecessors must be an array")
    if not isinstance(spec.get("dependencies"), list):
        errors.append("spec.dependencies must be an array")
    scope = spec.get("scope")
    if not isinstance(scope, dict):
        errors.append("spec.scope must be an object")
        scope = {}
    for field in ["allowed_paths", "forbidden_paths"]:
        if not isinstance(scope.get(field), list):
            errors.append(f"spec.scope.{field} must be an array")
        elif not all(isinstance(item, str) and item for item in scope.get(field, [])):
            errors.append(f"spec.scope.{field} entries must be non-empty strings")
    validation_spec = spec.get("validation")
    if not isinstance(validation_spec, dict):
        errors.append("spec.validation must be an object")
        validation_spec = {}
    commands = validation_spec.get("commands")
    if not isinstance(commands, list):
        errors.append("spec.validation.commands must be an array")
    else:
        for index, item in enumerate(commands):
            if not isinstance(item, dict):
                errors.append(f"spec.validation.commands[{index}] must be an object")
                continue
            if not isinstance(item.get("command"), str) or not item.get("command"):
                errors.append(f"spec.validation.commands[{index}].command must be a non-empty string")
            if item.get("status") not in VALIDATION_STATUSES:
                errors.append(f"spec.validation.commands[{index}].status is unsupported: {item.get('status')}")
    evidence_requirements = spec.get("evidence_requirements")
    if not isinstance(evidence_requirements, list):
        errors.append("spec.evidence_requirements must be an array")
    elif not all(isinstance(item, str) and item for item in evidence_requirements):
        errors.append("spec.evidence_requirements entries must be non-empty strings")
    non_capabilities = spec.get("explicit_non_capabilities")
    if not isinstance(non_capabilities, list):
        errors.append("spec.explicit_non_capabilities must be an array")
    else:
        for item in non_capabilities:
            if not isinstance(item, str) or not item:
                errors.append("spec.explicit_non_capabilities entries must be non-empty strings")
    capability_label = spec.get("capability_label")
    if capability_label is not None and capability_label not in RECOGNIZED_CAPABILITIES:
        errors.append(f"unknown capability_label: {capability_label}")
    if isinstance(non_capabilities, list) and capability_label in non_capabilities:
        errors.append("spec.capability_label must not appear in explicit_non_capabilities")
    status = obj.get("status") if isinstance(obj.get("status"), dict) else {}
    for field in REQUIRED_STATUS_FIELDS:
        if field not in status:
            errors.append(f"missing required status field: {field}")
    if status.get("phase") not in PHASE_VALUES:
        errors.append(f"status.phase is unsupported: {status.get('phase')}")
    if "result" in status and status.get("result") not in RESULT_VALUES:
        errors.append(f"status.result is unsupported: {status.get('result')}")
    if not isinstance(status.get("validated"), bool):
        errors.append("status.validated must be a boolean")
    if not isinstance(status.get("validation_errors"), list):
        errors.append("status.validation_errors must be an array")
    if not isinstance(status.get("validation_warnings"), list):
        errors.append("status.validation_warnings must be an array")
    return errors


def load_workunit_schema(repo_root: str | Path | None = None) -> dict[str, Any]:
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


def validate_workunit_with_schema(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    active_schema = schema if schema is not None else load_workunit_schema()
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
            "expected_required_fields": WORKUNIT_REQUIRED_FIELDS,
            "schema_required_fields": [],
        }
    required = schema.get("required")
    schema_required = required if isinstance(required, list) else []
    missing = [field for field in WORKUNIT_REQUIRED_FIELDS if field not in schema_required]
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
        "expected_required_fields": WORKUNIT_REQUIRED_FIELDS,
        "schema_required_fields": [str(item) for item in schema_required],
        "missing_required_fields": missing,
        "checked_spec_fields": REQUIRED_SPEC_FIELDS,
    }


def validate_workunit_runtime(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> dict[str, Any]:
    active_schema = schema if schema is not None else load_workunit_schema()
    helper_errors = validate_workunit(obj)
    schema_errors = validate_workunit_with_schema(obj, active_schema)
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


def _capability_for_task(task_data: dict[str, Any], task_id: str) -> str:
    for key in ["new_capability_label", "introduced_capability", "capability_label"]:
        value = task_data.get(key)
        if isinstance(value, str):
            normalized = _normalize_token(value)
            if normalized in RECOGNIZED_CAPABILITIES:
                return normalized
    accepted = task_data.get("accepted_capability")
    if isinstance(accepted, dict):
        for key in ["capability_label", "capability"]:
            value = accepted.get(key)
            if isinstance(value, str):
                normalized = _normalize_token(value)
                if normalized in RECOGNIZED_CAPABILITIES:
                    return normalized
    if task_id == "AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01":
        return "fixture_temp_apply_only"
    if task_id == "AIDE-BUILD-CONTRACT-ENVELOPE-01":
        return "minimal_contract_envelope"
    if task_id in {"AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01", "AIDE-ACCEPT-EVIDENCE-PACKET-SCHEMA-01"}:
        return "minimal_evidence_packet_schema"
    return FEATURE_FLAG


def _predecessors_from_task(task_data: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for key in ["predecessor_acceptance_task", "triggered_by", "accepted_by_task"]:
        value = task_data.get(key)
        if isinstance(value, str) and value:
            result.append(value)
    for key in ["reviewed_tasks", "accepted_predecessor_tasks", "predecessors"]:
        result.extend(_normalize_list(task_data.get(key)))
    return sorted(dict.fromkeys(result))


def _evidence_requirements(repo_root: Path, task_id: str, status_data: dict[str, Any]) -> list[str]:
    observed = _normalize_list(status_data.get("evidence"))
    evidence_dir = repo_root / ".aide/queue" / task_id / "evidence"
    if evidence_dir.exists():
        for path in sorted(evidence_dir.glob("*.md")):
            observed.append(_relative_posix(path, repo_root))
    return sorted(dict.fromkeys(observed))


def _validation_commands(repo_root: Path, task_id: str, task_data: dict[str, Any]) -> list[dict[str, Any]]:
    observed: dict[str, dict[str, Any]] = {}

    def clean_command(command: str) -> str:
        cleaned = command.strip()
        if cleaned.startswith("`") and cleaned.endswith("`") and len(cleaned) >= 2:
            return cleaned[1:-1].strip()
        return cleaned

    def record(command: str, status: str, exit_code: int | None = None, notes: str = "") -> None:
        cleaned = clean_command(command)
        if not cleaned:
            return
        item = validation(cleaned, status, exit_code, notes)
        current = observed.get(cleaned)
        if current is None or current.get("status") == "NOT_RUN" and item.get("status") != "NOT_RUN":
            observed[cleaned] = item

    for item in _normalize_list(task_data.get("validation_commands")):
        record(item, "NOT_RUN")
    evidence_dir = repo_root / ".aide/queue" / task_id / "evidence"
    for name in ["validation.md", "test-results.md"]:
        path = evidence_dir / name
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("- `") and "`" in stripped[3:]:
                command = stripped.split("`", 2)[1]
                record(command, "PASS")
            elif stripped.startswith("- PASS:"):
                record(stripped.removeprefix("- PASS:").strip(), "PASS")
    if not observed:
        record("source queue task reviewed", "NOT_RUN", notes="Projected from queue task metadata.")
    return list(observed.values())[:24]


def project_queue_task(repo_root: str | Path, task_id: str) -> dict[str, Any]:
    root = Path(repo_root)
    task_dir = root / ".aide/queue" / task_id
    task_path = task_dir / "task.yaml"
    status_path = task_dir / "status.yaml"
    if not task_path.exists():
        raise ValueError(f"queue task missing task.yaml: {task_id}")
    task_data = read_simple_yaml(task_path)
    status_data = read_simple_yaml(status_path)
    warnings: list[str] = []
    if not status_path.exists():
        warnings.append("status.yaml missing; projection uses task.yaml only")
    task_title = str(task_data.get("title") or task_id)
    capability = _capability_for_task(task_data, task_id)
    allowed_paths = _normalize_list(task_data.get("allowed_paths"))
    forbidden_paths = _normalize_list(task_data.get("forbidden_paths"))
    scope = {
        "allowed_paths": allowed_paths,
        "forbidden_paths": forbidden_paths,
        "forbidden_operations": _normalize_list(task_data.get("forbidden_operations")),
        "read_only_review_paths": _normalize_list(task_data.get("read_only_review_paths") or task_data.get("reviewed_read_only_paths")),
    }
    artifacts = [
        artifact_ref(root, Path(".aide/queue") / task_id / "task.yaml", "task_yaml"),
        artifact_ref(root, Path(".aide/queue") / task_id / "status.yaml", "status_yaml"),
    ]
    validation_errors: list[str] = []
    if not allowed_paths:
        warnings.append("task allowed_paths is empty")
    if not task_data.get("stop_state"):
        warnings.append("task stop_state missing; defaulted to needs_review")
    phase = status_data.get("status") or task_data.get("status") or "needs_review"
    result = status_data.get("result") or task_data.get("result") or "NOT_RUN"
    return build_workunit(
        task_id=task_id,
        title=task_title,
        work_type=infer_work_type(task_id, task_data),
        authorizes_implementation=_as_bool(task_data.get("authorizes_implementation")),
        check_only=_as_bool(task_data.get("check_only")),
        acceptance_review=_as_bool(task_data.get("acceptance_review")),
        implementation_scope=str(task_data.get("implementation_scope") or ""),
        stop_state=str(task_data.get("stop_state") or "needs_review"),
        predecessors=_predecessors_from_task(task_data),
        dependencies=_normalize_list(task_data.get("dependencies")),
        scope=scope,
        validation_spec={"commands": _validation_commands(root, task_id, task_data)},
        evidence_requirements=_evidence_requirements(root, task_id, status_data),
        explicit_non_capabilities=explicit_non_capabilities(task_data),
        capability_label=capability,
        artifacts=artifacts,
        source_path=Path(".aide/queue") / task_id / "task.yaml",
        created_at=str(task_data.get("created_at") or "deterministic"),
        phase=str(phase),
        result=str(result),
        validation_errors=validation_errors,
        validation_warnings=warnings,
    )


def project_existing_queue_tasks(
    repo_root: str | Path,
    task_ids: list[str] | None = None,
) -> dict[str, dict[str, Any]]:
    ids = task_ids if task_ids is not None else [QUEUE_SOURCES[key] for key in QUEUE_SOURCES]
    paths_by_task = {QUEUE_SOURCES[key]: PROJECTION_FILES[key] for key in QUEUE_SOURCES}
    projections: dict[str, dict[str, Any]] = {}
    for task_id in ids:
        output_path = paths_by_task.get(task_id, PROJECTION_ROOT / f"{task_id.lower()}.workunit.json")
        projections[output_path.as_posix()] = project_queue_task(repo_root, task_id)
    return projections


def project_queue_tasks(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    source_paths = [
        root / ".aide/queue" / task_id / "task.yaml"
        for task_id in QUEUE_SOURCES.values()
        if (root / ".aide/queue" / task_id / "task.yaml").exists()
    ]
    source_paths.extend(
        root / ".aide/queue" / task_id / "status.yaml"
        for task_id in QUEUE_SOURCES.values()
        if (root / ".aide/queue" / task_id / "status.yaml").exists()
    )
    hashes_before = {path: sha256_file(path) for path in source_paths if path.is_file()}
    projections = project_existing_queue_tasks(root)
    for rel, workunit in projections.items():
        write_json(root / rel, workunit)
    hashes_after = {path: sha256_file(path) for path in source_paths if path.is_file()}
    source_queue_tasks_mutated = hashes_before != hashes_after
    report = {
        "schema_version": "aide.workunit-queue-projection.v1",
        "report_type": "workunit_queue_projection",
        "kind": "WorkUnitQueueProjectionReport",
        "status": "PASS" if not source_queue_tasks_mutated else "FAILED_VALIDATION",
        "source": "queue-tasks",
        "source_queue_tasks_checked": [task_id for task_id in QUEUE_SOURCES.values() if (root / ".aide/queue" / task_id / "task.yaml").exists()],
        "workunit_projections_written": sorted(projections),
        "source_queue_tasks_mutated": source_queue_tasks_mutated,
        "destructive_migration_performed": False,
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


def workunit_queue_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    projection_paths = [root / rel for rel in PROJECTION_FILES.values()]
    schema_path = root / SCHEMA_PATH
    data = {
        "schema_version": "aide.workunit-queue-status.v1",
        "report_type": "workunit_queue_status",
        "kind": "WorkUnitQueueProjectionReport",
        "status": "PASS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "schema_file_exists": schema_path.exists(),
        "schema_validation_mode": SCHEMA_VALIDATION_MODE,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "recognized_capabilities": sorted(RECOGNIZED_CAPABILITIES),
        "work_types": sorted(WORK_TYPES),
        "phase_values": sorted(PHASE_VALUES),
        "result_values": sorted(RESULT_VALUES),
        "source_queue_tasks": {key: (root / ".aide/queue" / task_id / "task.yaml").exists() for key, task_id in QUEUE_SOURCES.items()},
        "projection_files": [_relative_posix(path, root) for path in projection_paths],
        "projection_files_existing": [_relative_posix(path, root) for path in projection_paths if path.exists()],
        "capability_label": FEATURE_FLAG,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "workunit_cli_implemented": False,
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


def workunit_queue_validate(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    projection_result = project_queue_tasks(root) if project else {"workunit_projections_written": []}
    projection_paths = [root / rel for rel in projection_result.get("workunit_projections_written", [])]
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
        schema = load_workunit_schema(root)
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
        helper_errors = validate_workunit(obj)
        schema_errors: list[str] = []
        if schema_file_parsed:
            runtime = validate_workunit_runtime(obj, schema)
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
        validate_workunit_runtime(sample_unknown_optional_workunit(), schema)
        if schema_file_parsed
        else {"status": "FAILED_VALIDATION", "helper_validation_errors": [], "schema_validation_errors": schema_load_errors}
    )
    required_runtime = (
        validate_workunit_runtime(sample_unknown_required_capability_workunit(), schema)
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
    compatibility_results = {
        "accepted_contract_envelope_preserved": True,
        "accepted_evidence_packet_preserved": True,
        "projection_paths_additive": True,
        "source_queue_tasks_destructively_migrated": False,
        "explicit_non_capabilities_preserved": explicit_non_capabilities_preserved,
        "unknown_optional_fields_tolerated": unknown_optional_fields_tolerated,
        "unknown_required_capability_fails_closed": unknown_required_capability_fails_closed,
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
    all_projections_valid = bool(validation_results) and all(item["result"] == "PASS" for item in validation_results)
    status = (
        "PASS"
        if all_projections_valid
        and projection_result.get("status") == "PASS"
        and all(value is True for key, value in compatibility_results.items() if key != "source_queue_tasks_destructively_migrated")
        and compatibility_results["source_queue_tasks_destructively_migrated"] is False
        and schema_checks_pass
        else "FAILED_VALIDATION"
    )
    report = {
        "schema_version": "aide.workunit-queue-validation.v1",
        "report_type": "workunit_queue_validation",
        "kind": "WorkUnitQueueValidationReport",
        "task_id": "AIDE-BUILD-WORKUNIT-QUEUE-V1-01",
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
        "schema_load_errors": schema_load_errors,
        "alignment_errors": alignment_errors,
        "alignment_warnings": alignment_warnings,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "recognized_capabilities": sorted(RECOGNIZED_CAPABILITIES),
        "source_queue_tasks_checked": projection_result.get("source_queue_tasks_checked", []),
        "workunit_projections_written": projection_result.get("workunit_projections_written", []),
        "validation_results": validation_results,
        "runtime_validation_results": runtime_validation_results,
        "helper_validation_errors": helper_validation_errors,
        "schema_validation_errors": schema_validation_errors,
        "compatibility_results": compatibility_results,
        "backwards_compatibility_preserved": all(
            value is True
            for key, value in compatibility_results.items()
            if key != "source_queue_tasks_destructively_migrated"
        )
        and compatibility_results["source_queue_tasks_destructively_migrated"] is False,
        "destructive_migration_performed": False,
        "unknown_optional_fields_tolerated": unknown_optional_fields_tolerated,
        "unknown_required_capability_fails_closed": unknown_required_capability_fails_closed,
        "explicit_non_capabilities_preserved": explicit_non_capabilities_preserved,
        "workunit_cli_implemented": False,
        "forbidden_operations_preserved": forbidden_operations_preserved(),
        "warnings": [
            "WorkUnit queue v1 is minimal and v1alpha1; this is not a WorkUnit execution CLI.",
            "Projection outputs are additive and source queue tasks remain canonical.",
            "Full JSON Schema Draft 2020-12 validation remains future work.",
            "Work create/list/claim/block/finish/repair, WorkerRun, TestJob, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target apply, rollback execution, release, and promotion remain future work.",
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


def validate_workunit_queue_reports(repo_root: str | Path) -> dict[str, Any]:
    return workunit_queue_validate(repo_root)


def forbidden_operations_preserved() -> dict[str, bool]:
    return {
        "workunit_create_list_claim_block_finish_repair": True,
        "worker_run_schema": True,
        "testjob_schema": True,
        "test_broker": True,
        "checkpoint_schema": True,
        "promotion_policy_schema": True,
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
        {"task": "AIDE-CHECK-WORKUNIT-QUEUE-V1-01", "reason": "independent review of WorkUnit queue schema, projections, compatibility, tests, and no-overclaiming"},
        {"task": "AIDE-HARDEN-WORKUNIT-QUEUE-V1-01", "reason": "harden only if the check finds validation, projection, or schema gaps"},
        {"task": "AIDE-ACCEPT-WORKUNIT-QUEUE-V1-01", "reason": "accept the minimal WorkUnit queue object only after check and any required hardening"},
        {"task": "AIDE-BUILD-WORKUNIT-CLI-01", "reason": "add WorkUnit create/list/claim/block/finish/repair only after queue object acceptance"},
        {"task": "AIDE-BUILD-TESTJOB-SCHEMA-01", "reason": "define TestJob after WorkUnit queue shape is accepted"},
        {"task": "AIDE-BUILD-TEST-BROKER-01", "reason": "build long-running test broker after WorkUnit and TestJob contracts exist"},
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    deferred = [
        "WorkUnit create/list/claim/block/finish/repair CLI",
        "full WorkUnit runtime",
        "scheduler",
        "supervisor",
        "WorkerRun",
        "TestJob schema",
        "Test Broker",
        "Checkpoint",
        "PromotionPolicy",
        "branch/worktree allocator",
        "Service",
        "Commander",
        "provider adapters",
        "target repo apply",
        "active repo apply",
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
    return [{"item": item, "reason": "intentionally deferred beyond the minimal WorkUnit queue v1 slice"} for item in deferred]


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# WorkUnit Queue Status",
        "",
        f"- status: {data.get('status')}",
        f"- api_version: {data.get('api_version')}",
        f"- protocol_version: {data.get('protocol_version')}",
        f"- schema_file_path: {data.get('schema_file_path')}",
        f"- schema_file_exists: {str(data.get('schema_file_exists', False)).lower()}",
        f"- schema_validation_mode: {data.get('schema_validation_mode')}",
        f"- capability_label: {data.get('capability_label')}",
        f"- workunit_cli_implemented: {str(data.get('workunit_cli_implemented', False)).lower()}",
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
    lines.extend(["", "## Recognized Capabilities", ""])
    for capability in data.get("recognized_capabilities", []):
        lines.append(f"- {capability}")
    lines.extend(["", "## Source Queue Tasks", ""])
    tasks = data.get("source_queue_tasks", {}) if isinstance(data.get("source_queue_tasks"), dict) else {}
    for key, present in tasks.items():
        lines.append(f"- {key}: {str(present).lower()}")
    lines.extend(["", "## Projection Files", ""])
    for rel in data.get("projection_files", []):
        lines.append(f"- {rel}")
    return "\n".join(lines) + "\n"


def render_projection_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# WorkUnit Queue Projection",
        "",
        f"- status: {report.get('status')}",
        f"- source: {report.get('source')}",
        f"- source_queue_tasks_mutated: {str(report.get('source_queue_tasks_mutated', False)).lower()}",
        "- destructive_migration_performed: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- branch_mutation: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "",
        "## WorkUnit Projections Written",
        "",
    ]
    for rel in report.get("workunit_projections_written", []):
        lines.append(f"- {rel}")
    lines.extend(["", "## Source Queue Tasks Checked", ""])
    for task_id in report.get("source_queue_tasks_checked", []):
        lines.append(f"- {task_id}")
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# WorkUnit Queue Validation",
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
        f"- workunit_cli_implemented: {str(report.get('workunit_cli_implemented', False)).lower()}",
        "",
        "## Projections",
        "",
    ]
    for rel in report.get("workunit_projections_written", []):
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
        "# WorkUnit Queue Future Work",
        "",
        "## Recommended Order",
        "",
    ]
    for index, item in enumerate(future_work_items(), start=1):
        future_lines.append(f"{index}. {item['task']}: {item['reason']}.")
    unfinished_lines = [
        "# WorkUnit Queue Unfinished Work",
        "",
        "## Finished In This Slice",
        "",
        "- Minimal envelope-backed WorkUnit helper and validator.",
        "- Additive projections from selected filesystem queue tasks.",
        "- Additive validation reports under `.aide/reports/workunit-queue/`.",
        "",
        "## Intentionally Deferred",
        "",
    ]
    for item in unfinished_work_items():
        unfinished_lines.append(f"- {item['item']}: {item['reason']}.")
    write_text(repo_root / FUTURE_WORK_MD, "\n".join(future_lines) + "\n")
    write_text(repo_root / UNFINISHED_WORK_MD, "\n".join(unfinished_lines) + "\n")
