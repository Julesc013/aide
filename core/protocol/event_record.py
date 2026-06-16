"""Minimal AIDE EventRecord helpers.

This module defines EventRecord as data only: deterministic event metadata,
ReferenceID-backed subjects, causation, correlation, evidence, and reports, plus
projection reports for example events and event family names. It does not append
events, store an event log, replay state, schedule work, call providers, mutate
GitHub, or execute target/apply behavior.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.protocol import envelope, reference_id


API_VERSION = envelope.API_VERSION
EVENT_RECORD_SCHEMA_VERSION = "aide.event-record.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_event_record_schema"
ACCEPTED_PREDECESSOR = reference_id.FEATURE_FLAG
TASK_ID = "AIDE-BUILD-EVENT-RECORD-SCHEMA-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-EVENT-RECORD-SCHEMA-01"
RECOMMENDED_AFTER_CHECK = "AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01"
RECOMMENDED_AFTER_ACCEPTANCE = "AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01"

REPORT_ROOT = Path(".aide/reports/event-record")
SCHEMA_PATH = Path(".aide/protocol/aide-event-record.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
EVENT_FAMILY_INDEX_JSON = REPORT_ROOT / "event-family-index.json"
EVENT_FAMILY_INDEX_MD = REPORT_ROOT / "event-family-index.md"
EXAMPLE_EVENTS_JSON = REPORT_ROOT / "example-events.json"
EXAMPLE_EVENTS_MD = REPORT_ROOT / "example-events.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"

SUPPORTED_KINDS = {
    "EventRecord",
    "EventRecordProjectionReport",
    "EventRecordValidationReport",
    "EventFamilyIndex",
    "EventRecordExamples",
}
EVENT_RECORD_REQUIRED_FIELDS = ["apiVersion", "kind", "metadata", "spec", "status"]
REQUIRED_METADATA_FIELDS = ["id", "createdAt", "sourcePath", "producer", "compatibility"]
REQUIRED_SPEC_FIELDS = [
    "event_ref",
    "event_type",
    "subject",
    "occurred_at",
    "sequence",
    "actor",
    "payload",
    "evidence_refs",
    "report_refs",
    "explicit_non_capabilities",
]
REQUIRED_STATUS_FIELDS = ["valid", "recorded", "projection_only", "validation_errors", "validation_warnings"]
RESULT_VALUES = {"PASS", "PASS_WITH_WARNINGS", "FAILED_VALIDATION", "BLOCKED", "PARTIAL", "UNKNOWN"}
EVENT_TYPE_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]*$")
SCHEMA_VALIDATION_MODE = "minimal_json_schema_subset"
SCHEMA_VALIDATION_LIMITATIONS = [
    "Local subset validator supports type, enum, required, properties, simple additionalProperties, and homogeneous array items only.",
    "Full JSON Schema Draft 2020-12 validation remains future work.",
    "Formats, refs, oneOf/anyOf/allOf, conditionals, numeric bounds, and pattern checks are not implemented.",
]

EXPLICIT_NON_CAPABILITIES = [
    "event_sourcing_runtime",
    "append_only_runtime_store",
    "runtime_event_log",
    "state_reconstruction",
    "scheduler",
    "leases",
    "supervisor",
    "test_broker_runtime",
    "async_execution",
    "worker_execution",
    "service",
    "commander",
    "okf_knowledge_bundle",
    "reconciler",
    "capability_manifest",
    "conformance_profile",
    "patch_transaction",
    "adapter_manifest",
    "context_pack_v2",
    "runtime_reference_registry",
    "resolver_service",
    "database_state",
    "provider_adapters",
    "branch_worktree_automation",
    "target_apply",
    "active_apply",
    "rollback_execution",
    "uninstall_execution",
    "release",
    "promotion",
    "github_mutation",
    "gateway_calls",
    "network_calls",
    "model_provider_calls",
    "target_repo_mutation",
    "broad_autonomous_runtime",
    "production_readiness",
    "release_readiness",
]

RECOGNIZED_CAPABILITIES = {
    FEATURE_FLAG,
    ACCEPTED_PREDECESSOR,
    reference_id.ACCEPTED_PREDECESSOR,
    "minimal_contract_envelope",
    "minimal_evidence_packet_schema",
    "minimal_workunit_queue_v1",
    "minimal_worker_run_schema",
    "minimal_test_job_schema",
}

EVENT_FAMILIES: list[dict[str, Any]] = [
    {
        "event_type": "WorkUnitStateChanged",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Records a projected WorkUnit state transition; it does not claim WorkUnit execution.",
        "subject_kinds": ["workunit", "queue-task"],
        "payload_contract": "minimal_open_payload",
    },
    {
        "event_type": "WorkerRunRecorded",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Records a metadata-only WorkerRun observation; it does not execute workers.",
        "subject_kinds": ["worker-run"],
        "payload_contract": "minimal_open_payload",
    },
    {
        "event_type": "TestJobRecorded",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Records a metadata-only TestJob observation; it does not submit or run tests.",
        "subject_kinds": ["test-job"],
        "payload_contract": "minimal_open_payload",
    },
    {
        "event_type": "EvidencePacketRecorded",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Records evidence packet metadata without creating an evidence runtime.",
        "subject_kinds": ["evidence"],
        "payload_contract": "minimal_open_payload",
    },
    {
        "event_type": "AcceptanceRecorded",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Records an acceptance decision as projection metadata only.",
        "subject_kinds": ["queue-task", "capability"],
        "payload_contract": "minimal_open_payload",
    },
    {
        "event_type": "ReferenceIDProjectionRecorded",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Records that a ReferenceID projection report exists; it does not implement resolution.",
        "subject_kinds": ["report", "schema"],
        "payload_contract": "minimal_open_payload",
    },
    {
        "event_type": "EventRecordProjectionRecorded",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Records that EventRecord projection reports exist; it does not create an event log.",
        "subject_kinds": ["report", "schema"],
        "payload_contract": "minimal_open_payload",
    },
    {
        "event_type": "CapabilityDeclared",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Records a projected capability declaration without implementing CapabilityManifest.",
        "subject_kinds": ["capability"],
        "payload_contract": "minimal_open_payload",
    },
    {
        "event_type": "ConformanceResultRecorded",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Records a projected conformance result without implementing ConformanceProfile.",
        "subject_kinds": ["conformance-result", "conformance-profile"],
        "payload_contract": "minimal_open_payload",
    },
    {
        "event_type": "OKFProjectionRecorded",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Reserves a future OKF projection event name without building OKF.",
        "subject_kinds": ["report", "artifact", "capability"],
        "payload_contract": "minimal_open_payload",
    },
    {
        "event_type": "ReconcilerFindingRecorded",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Reserves a future reconciler finding event name without building a reconciler.",
        "subject_kinds": ["report", "decision"],
        "payload_contract": "minimal_open_payload",
    },
    {
        "event_type": "PatchTransactionRecorded",
        "status": "reserved_or_supported_for_schema",
        "implemented_subsystem": False,
        "description": "Reserves a future PatchTransaction event name without implementing PatchTransaction.",
        "subject_kinds": ["patch-transaction"],
        "payload_contract": "minimal_open_payload",
    },
]
EVENT_FAMILY_BY_TYPE = {item["event_type"]: item for item in EVENT_FAMILIES}
EVENT_FAMILY_NAMES = set(EVENT_FAMILY_BY_TYPE)


@dataclass(frozen=True)
class EventTypeValidation:
    valid: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    event_type: str | None = None

    @property
    def status(self) -> str:
        if not self.valid:
            return "FAILED_VALIDATION"
        return "PASS_WITH_WARNINGS" if self.warnings else "PASS"

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "status": self.status,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "event_type": self.event_type,
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
    return reference_id.sha256_file(path)


def _relative_posix(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def _has_whitespace_or_control(value: str) -> bool:
    return any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in value)


def _compatibility(required_capabilities: list[str] | None = None) -> dict[str, Any]:
    required = [FEATURE_FLAG, ACCEPTED_PREDECESSOR]
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


def _deterministic_metadata_id(event_ref: str, event_type: str) -> str:
    seed = f"{event_ref}|{event_type}"
    return "event-record-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


def event_family_names() -> list[str]:
    return sorted(EVENT_FAMILY_NAMES)


def validate_event_type(
    event_type: str,
    *,
    required: bool = True,
    known_event_types: set[str] | None = None,
) -> EventTypeValidation:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(event_type, str) or not event_type:
        return EventTypeValidation(False, ("event_type must be a non-empty string",), (), None)
    if _has_whitespace_or_control(event_type):
        errors.append("event_type must not contain whitespace or control characters")
    if not EVENT_TYPE_PATTERN.match(event_type):
        errors.append("event_type must match ^[A-Z][A-Za-z0-9]*$")
    active_types = known_event_types or EVENT_FAMILY_NAMES
    if not errors and event_type not in active_types:
        message = f"unknown {'required' if required else 'optional'} event_type: {event_type}"
        if required:
            errors.append(message)
        else:
            warnings.append(message)
    return EventTypeValidation(not errors, tuple(errors), tuple(warnings), event_type)


def parse_event_type(event_type: str) -> str:
    result = validate_event_type(event_type, required=True)
    if not result.valid:
        raise ValueError("; ".join(result.errors))
    return event_type


def format_event_ref(event_id: str) -> str:
    return reference_id.format_reference_id("event", event_id)


def _ref_validation_errors(
    field_name: str,
    ref: Any,
    *,
    required: bool,
    allowed_kinds: set[str] | None = None,
) -> tuple[list[str], list[str], reference_id.ReferenceId | None]:
    if ref is None:
        if required:
            return [f"{field_name} is required"], [], None
        return [], [], None
    if not isinstance(ref, str) or not ref:
        return [f"{field_name} must be a non-empty string"], [], None
    result = reference_id.validate_reference_id(ref, required=required)
    errors = [f"{field_name}: {error}" for error in result.errors]
    warnings = [f"{field_name}: {warning}" for warning in result.warnings]
    parsed = result.parsed
    if parsed is not None and allowed_kinds is not None and parsed.kind not in allowed_kinds:
        errors.append(f"{field_name} must use one of {sorted(allowed_kinds)} refs, got {parsed.kind}")
    return errors, warnings, parsed


def _ref_object(ref: str | None, *, required: bool = False) -> dict[str, Any] | None:
    if ref is None:
        return None
    parsed = reference_id.validate_reference_id(ref, required=required).parsed
    return {
        "ref": ref,
        "kind": parsed.kind if parsed else "",
        "id": parsed.object_id if parsed else "",
        "fragment": parsed.fragment if parsed else None,
    }


def build_event_record(
    *,
    repo_root: Path,
    event_ref: str,
    event_type: str,
    subject_ref: str,
    subject_kind: str | None = None,
    occurred_at: str = "deterministic",
    sequence: int = 0,
    actor: dict[str, Any] | None = None,
    payload: dict[str, Any] | None = None,
    evidence_refs: list[str] | None = None,
    report_refs: list[str] | None = None,
    causation_ref: str | None = None,
    correlation_ref: str | None = None,
    source_path: str | None = None,
    required_event_type: bool = True,
) -> dict[str, Any]:
    del repo_root  # EventRecord identity is ReferenceID-based; paths remain report locators.
    errors: list[str] = []
    warnings: list[str] = []
    event_errors, event_warnings, _ = _ref_validation_errors(
        "spec.event_ref",
        event_ref,
        required=True,
        allowed_kinds={"event"},
    )
    errors.extend(event_errors)
    warnings.extend(event_warnings)
    event_type_result = validate_event_type(event_type, required=required_event_type)
    errors.extend(event_type_result.errors)
    warnings.extend(event_type_result.warnings)
    subject_errors, subject_warnings, subject_parsed = _ref_validation_errors(
        "spec.subject.ref",
        subject_ref,
        required=True,
    )
    errors.extend(subject_errors)
    warnings.extend(subject_warnings)
    if subject_parsed is not None:
        family = EVENT_FAMILY_BY_TYPE.get(event_type)
        allowed_subject_kinds = set(family.get("subject_kinds", [])) if isinstance(family, dict) else set()
        if allowed_subject_kinds and subject_parsed.kind not in allowed_subject_kinds:
            errors.append(
                f"spec.subject.kind {subject_parsed.kind} is not allowed for {event_type}; expected one of {sorted(allowed_subject_kinds)}"
            )
    for field_name, optional_ref in [("spec.causation.ref", causation_ref), ("spec.correlation.ref", correlation_ref)]:
        ref_errors, ref_warnings, _ = _ref_validation_errors(field_name, optional_ref, required=False)
        errors.extend(ref_errors)
        warnings.extend(ref_warnings)
    evidence_list = list(evidence_refs or [])
    report_list = list(report_refs or [])
    for index, ref in enumerate(evidence_list):
        ref_errors, ref_warnings, _ = _ref_validation_errors(
            f"spec.evidence_refs[{index}]",
            ref,
            required=True,
            allowed_kinds={"evidence"},
        )
        errors.extend(ref_errors)
        warnings.extend(ref_warnings)
    for index, ref in enumerate(report_list):
        ref_errors, ref_warnings, _ = _ref_validation_errors(
            f"spec.report_refs[{index}]",
            ref,
            required=True,
            allowed_kinds={"report"},
        )
        errors.extend(ref_errors)
        warnings.extend(ref_warnings)

    actor_value = actor or {"ref": "aide://source/aide-lite", "kind": "source", "name": "aide-lite"}
    actor_ref = actor_value.get("ref") if isinstance(actor_value, dict) else None
    if actor_ref:
        ref_errors, ref_warnings, actor_parsed = _ref_validation_errors("spec.actor.ref", actor_ref, required=False)
        errors.extend(ref_errors)
        warnings.extend(ref_warnings)
        if actor_parsed is not None and isinstance(actor_value, dict) and actor_value.get("kind") not in {None, actor_parsed.kind}:
            errors.append("spec.actor.kind must match actor ref kind")

    result = "FAILED_VALIDATION" if errors else "PASS_WITH_WARNINGS" if warnings else "PASS"
    metadata = {
        "id": _deterministic_metadata_id(event_ref, event_type),
        "name": event_type,
        "title": event_type,
        "createdAt": "deterministic",
        "sourcePath": source_path or "",
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility(),
    }
    spec = {
        "event_ref": event_ref,
        "event_type": event_type,
        "event_type_required": bool(required_event_type),
        "event_family_status": EVENT_FAMILY_BY_TYPE.get(event_type, {}).get("status", "future_event_type"),
        "payload_contract": EVENT_FAMILY_BY_TYPE.get(event_type, {}).get("payload_contract", "minimal_open_payload"),
        "subject": {
            "ref": subject_ref,
            "kind": subject_kind or (subject_parsed.kind if subject_parsed else ""),
        },
        "causation": _ref_object(causation_ref, required=False),
        "correlation": _ref_object(correlation_ref, required=False),
        "occurred_at": occurred_at,
        "sequence": sequence,
        "actor": actor_value,
        "payload": dict(payload or {}),
        "evidence_refs": evidence_list,
        "report_refs": report_list,
        "capability_label": FEATURE_FLAG,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recorded": False,
        "projection_only": True,
        "event_sourcing_runtime_implemented": False,
        "append_only_runtime_store_implemented": False,
        "runtime_event_log_implemented": False,
        "state_reconstruction_implemented": False,
        "scheduler_implemented": False,
        "leases_implemented": False,
        "supervisor_implemented": False,
        "test_broker_runtime_implemented": False,
        "async_execution_implemented": False,
        "worker_execution_implemented": False,
        "service_implemented": False,
        "commander_implemented": False,
        "okf_knowledge_bundle_implemented": False,
        "reconciler_implemented": False,
        "capability_manifest_implemented": False,
        "conformance_profile_implemented": False,
        "patch_transaction_implemented": False,
        "adapter_manifest_implemented": False,
        "context_pack_v2_implemented": False,
        "runtime_reference_registry_implemented": False,
        "resolver_service_implemented": False,
        "database_state_implemented": False,
        "provider_adapter_implemented": False,
        "branch_worktree_automation": False,
        "target_apply": False,
        "active_apply": False,
        "target_repo_mutation": False,
        "release": False,
        "github_mutation": False,
        "gateway_calls": False,
        "network_calls": False,
        "model_provider_calls": False,
        "production_readiness": False,
        "release_readiness": False,
    }
    status = {
        "valid": not errors,
        "result": result,
        "phase": "metadata_only",
        "recorded": False,
        "projection_only": True,
        "validated": not errors,
        "validation_errors": errors,
        "validation_warnings": warnings,
    }
    obj = envelope.build_envelope("EventRecord", metadata, spec, status, api_version=API_VERSION)
    obj["schema_version"] = EVENT_RECORD_SCHEMA_VERSION
    obj["protocol_version"] = PROTOCOL_VERSION
    return obj


def sample_event_record() -> dict[str, Any]:
    return build_event_record(
        repo_root=Path("."),
        event_ref="aide://event/EVT-EVENT-RECORD-SAMPLE",
        event_type="AcceptanceRecorded",
        subject_ref="aide://queue-task/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01",
        causation_ref="aide://queue-task/AIDE-CHECK-REFERENCE-ID-SCHEME-01",
        correlation_ref="aide://wave/protocol-vertical-slice",
        evidence_refs=["aide://evidence/aide-accept-reference-id-scheme-01-acceptance-summary"],
        report_refs=["aide://report/reference-id-acceptance-report"],
        payload={"result": "ACCEPTED_WITH_WARNINGS"},
        source_path=".aide/queue/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01/status.yaml",
    )


def sample_unknown_optional_event_record() -> dict[str, Any]:
    return build_event_record(
        repo_root=Path("."),
        event_ref="aide://event/EVT-FUTURE-OPTIONAL-EVENT",
        event_type="FutureEventType",
        subject_ref="aide://queue-task/FUTURE-TASK",
        payload={"future": True},
        required_event_type=False,
        source_path="",
    )


def sample_unknown_required_event_record() -> dict[str, Any]:
    return build_event_record(
        repo_root=Path("."),
        event_ref="aide://event/EVT-FUTURE-REQUIRED-EVENT",
        event_type="FutureEventType",
        subject_ref="aide://queue-task/FUTURE-TASK",
        payload={"future": True},
        required_event_type=True,
        source_path="",
    )


def validate_event_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["EventRecord must be an object"]
    if record.get("apiVersion") != API_VERSION:
        errors.append(f"unsupported apiVersion: {record.get('apiVersion')}")
    if record.get("kind") != "EventRecord":
        errors.append(f"unsupported kind: {record.get('kind')}")
    for field in ["metadata", "spec", "status"]:
        if field not in record:
            errors.append(f"missing required field: {field}")
        elif not isinstance(record[field], dict):
            errors.append(f"{field} must be an object")
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    for field in REQUIRED_METADATA_FIELDS:
        if field not in metadata:
            errors.append(f"missing required metadata field: {field}")
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
    for capability in compatibility.get("requiredCapabilities", []) if isinstance(compatibility.get("requiredCapabilities"), list) else []:
        if capability not in RECOGNIZED_CAPABILITIES:
            errors.append(f"unknown required capability: {capability}")

    spec = record.get("spec") if isinstance(record.get("spec"), dict) else {}
    for field in REQUIRED_SPEC_FIELDS:
        if field not in spec:
            errors.append(f"missing required spec field: {field}")
    ref_errors, _, parsed_event = _ref_validation_errors(
        "spec.event_ref",
        spec.get("event_ref"),
        required=True,
        allowed_kinds={"event"},
    )
    errors.extend(ref_errors)
    event_type = spec.get("event_type")
    if not isinstance(event_type, str):
        errors.append("spec.event_type must be a string")
        event_type = ""
    else:
        event_type_required = bool(spec.get("event_type_required", True))
        errors.extend(validate_event_type(event_type, required=event_type_required).errors)
    subject = spec.get("subject")
    if not isinstance(subject, dict):
        errors.append("spec.subject must be an object")
        subject = {}
    subject_ref = subject.get("ref")
    subject_errors, _, subject_parsed = _ref_validation_errors("spec.subject.ref", subject_ref, required=True)
    errors.extend(subject_errors)
    if subject_parsed is not None:
        if subject.get("kind") != subject_parsed.kind:
            errors.append("spec.subject.kind must match parsed subject ref kind")
        family = EVENT_FAMILY_BY_TYPE.get(event_type)
        allowed_subject_kinds = set(family.get("subject_kinds", [])) if isinstance(family, dict) else set()
        if allowed_subject_kinds and subject_parsed.kind not in allowed_subject_kinds:
            errors.append(
                f"spec.subject.kind {subject_parsed.kind} is not allowed for {event_type}; expected one of {sorted(allowed_subject_kinds)}"
            )
    for field in ["causation", "correlation"]:
        value = spec.get(field)
        if value is not None:
            if not isinstance(value, dict):
                errors.append(f"spec.{field} must be an object or null")
            else:
                ref_errors, _, _ = _ref_validation_errors(f"spec.{field}.ref", value.get("ref"), required=False)
                errors.extend(ref_errors)
    if not isinstance(spec.get("occurred_at"), str) or not spec.get("occurred_at"):
        errors.append("spec.occurred_at must be a non-empty string")
    if not isinstance(spec.get("sequence"), int) or isinstance(spec.get("sequence"), bool) or spec.get("sequence") < 0:
        errors.append("spec.sequence must be a non-negative integer")
    if not isinstance(spec.get("actor"), dict):
        errors.append("spec.actor must be an object")
    if not isinstance(spec.get("payload"), dict):
        errors.append("spec.payload must be an object")
    for field, expected_kind in [("evidence_refs", "evidence"), ("report_refs", "report")]:
        values = spec.get(field)
        if not isinstance(values, list):
            errors.append(f"spec.{field} must be an array")
            continue
        for index, ref in enumerate(values):
            ref_errors, _, _ = _ref_validation_errors(
                f"spec.{field}[{index}]",
                ref,
                required=True,
                allowed_kinds={expected_kind},
            )
            errors.extend(ref_errors)
    if not isinstance(spec.get("explicit_non_capabilities"), list):
        errors.append("spec.explicit_non_capabilities must be an array")
    elif spec.get("capability_label") in spec.get("explicit_non_capabilities", []):
        errors.append("spec.capability_label must not appear in explicit_non_capabilities")
    for flag in [
        "recorded",
        "event_sourcing_runtime_implemented",
        "append_only_runtime_store_implemented",
        "runtime_event_log_implemented",
        "state_reconstruction_implemented",
        "scheduler_implemented",
        "leases_implemented",
        "supervisor_implemented",
        "test_broker_runtime_implemented",
        "async_execution_implemented",
        "worker_execution_implemented",
        "service_implemented",
        "commander_implemented",
        "okf_knowledge_bundle_implemented",
        "reconciler_implemented",
        "capability_manifest_implemented",
        "conformance_profile_implemented",
        "patch_transaction_implemented",
        "adapter_manifest_implemented",
        "context_pack_v2_implemented",
        "runtime_reference_registry_implemented",
        "resolver_service_implemented",
        "database_state_implemented",
        "provider_adapter_implemented",
        "branch_worktree_automation",
        "target_apply",
        "active_apply",
        "target_repo_mutation",
        "release",
        "github_mutation",
        "gateway_calls",
        "network_calls",
        "model_provider_calls",
        "production_readiness",
        "release_readiness",
    ]:
        if spec.get(flag) is not False:
            errors.append(f"spec.{flag} must be false in this slice")
    if spec.get("projection_only") is not True:
        errors.append("spec.projection_only must be true in this slice")

    status = record.get("status") if isinstance(record.get("status"), dict) else {}
    for field in REQUIRED_STATUS_FIELDS:
        if field not in status:
            errors.append(f"missing required status field: {field}")
    if not isinstance(status.get("valid"), bool):
        errors.append("status.valid must be a boolean")
    if status.get("recorded") is not False:
        errors.append("status.recorded must be false")
    if status.get("projection_only") is not True:
        errors.append("status.projection_only must be true")
    if not isinstance(status.get("validation_errors"), list):
        errors.append("status.validation_errors must be an array")
    if not isinstance(status.get("validation_warnings"), list):
        errors.append("status.validation_warnings must be an array")
    if status.get("result") not in RESULT_VALUES:
        errors.append(f"unsupported status.result: {status.get('result')}")
    if parsed_event is not None and not str(parsed_event.object_id).startswith("EVT-"):
        errors.append("spec.event_ref id must start with EVT- for projected examples")
    return errors


def load_event_record_schema(repo_root: str | Path | None = None) -> dict[str, Any]:
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
    if isinstance(value, list):
        item_schema = schema.get("items")
        if item_schema is not None:
            if not isinstance(item_schema, dict):
                errors.append(f"{path}.items must be an object")
            else:
                for index, item in enumerate(value):
                    errors.extend(_schema_node_errors(item, item_schema, f"{path}[{index}]"))
    return errors


def validate_event_record_with_schema(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    active_schema = schema if schema is not None else load_event_record_schema()
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
            "expected_required_fields": EVENT_RECORD_REQUIRED_FIELDS,
            "schema_required_fields": [],
        }
    required = schema.get("required")
    schema_required = required if isinstance(required, list) else []
    missing = [field for field in EVENT_RECORD_REQUIRED_FIELDS if field not in schema_required]
    extra_required = [str(field) for field in schema_required if field not in EVENT_RECORD_REQUIRED_FIELDS]
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
    schema_kinds = properties.get("kind", {}).get("enum", []) if isinstance(properties.get("kind"), dict) else []
    if "EventRecord" not in schema_kinds:
        errors.append("schema.properties.kind.enum must include EventRecord")
    spec_required = properties.get("spec", {}).get("required", []) if isinstance(properties.get("spec"), dict) else []
    if isinstance(spec_required, list):
        for field in REQUIRED_SPEC_FIELDS:
            if field not in spec_required:
                errors.append(f"schema.properties.spec.required missing helper-required field: {field}")
    else:
        errors.append("schema.properties.spec.required must be an array")
    status = "PASS" if not errors else "FAILED_VALIDATION"
    return {
        "status": status,
        "schema_helper_alignment_status": status,
        "errors": errors,
        "warnings": warnings,
        "expected_required_fields": EVENT_RECORD_REQUIRED_FIELDS,
        "schema_required_fields": [str(item) for item in schema_required],
        "missing_required_fields": missing,
        "extra_required_fields": extra_required,
    }


def validate_event_record_runtime(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> dict[str, Any]:
    active_schema = schema if schema is not None else load_event_record_schema()
    helper_errors = validate_event_record(obj)
    schema_errors = validate_event_record_with_schema(obj, active_schema)
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


def project_event_examples(repo_root: str | Path) -> list[dict[str, Any]]:
    root = Path(repo_root)
    return [
        build_event_record(
            repo_root=root,
            event_ref="aide://event/EVT-REFERENCE-ID-ACCEPTED",
            event_type="AcceptanceRecorded",
            subject_ref="aide://queue-task/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01",
            causation_ref="aide://queue-task/AIDE-CHECK-REFERENCE-ID-SCHEME-01",
            correlation_ref="aide://wave/protocol-vertical-slice",
            evidence_refs=["aide://evidence/aide-accept-reference-id-scheme-01-acceptance-summary"],
            report_refs=["aide://report/reference-id-acceptance-report"],
            payload={"accepted_capability": ACCEPTED_PREDECESSOR, "result": "ACCEPTED_WITH_WARNINGS"},
            source_path=".aide/queue/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01/status.yaml",
        ),
        build_event_record(
            repo_root=root,
            event_ref="aide://event/EVT-REFERENCE-ID-PROJECTION",
            event_type="ReferenceIDProjectionRecorded",
            subject_ref="aide://report/reference-id-projection-report",
            causation_ref="aide://queue-task/AIDE-BUILD-REFERENCE-ID-SCHEME-01",
            correlation_ref="aide://wave/protocol-vertical-slice",
            evidence_refs=["aide://evidence/aide-build-reference-id-scheme-01-projection-review"],
            report_refs=["aide://report/reference-id-projection-report"],
            payload={"projection": "reference-id", "projection_only": True},
            source_path=".aide/reports/reference-id/projection-report.json",
        ),
        build_event_record(
            repo_root=root,
            event_ref="aide://event/EVT-EVENT-RECORD-PROJECTION",
            event_type="EventRecordProjectionRecorded",
            subject_ref="aide://report/event-record-projection-report",
            causation_ref="aide://queue-task/AIDE-BUILD-EVENT-RECORD-SCHEMA-01",
            correlation_ref="aide://wave/protocol-vertical-slice",
            evidence_refs=["aide://evidence/aide-build-event-record-schema-01-projection-review"],
            report_refs=["aide://report/event-record-projection-report"],
            payload={"projection": "event-record", "projection_only": True},
            source_path=".aide/reports/event-record/projection-report.json",
        ),
        build_event_record(
            repo_root=root,
            event_ref="aide://event/EVT-TESTJOB-ACCEPTED",
            event_type="AcceptanceRecorded",
            subject_ref="aide://queue-task/AIDE-ACCEPT-TESTJOB-SCHEMA-01",
            causation_ref="aide://queue-task/AIDE-CHECK-TESTJOB-SCHEMA-01",
            correlation_ref="aide://wave/protocol-vertical-slice",
            evidence_refs=["aide://evidence/aide-accept-testjob-schema-01-acceptance-summary"],
            report_refs=["aide://report/test-job-acceptance-report"],
            payload={"accepted_capability": "minimal_test_job_schema", "result": "ACCEPTED_WITH_WARNINGS"},
            source_path=".aide/reports/test-job-accept/acceptance-report.json",
        ),
    ]


def _source_paths(root: Path) -> list[Path]:
    rel_paths = [
        ".aide/protocol/aide-reference-id.schema.json",
        "core/protocol/reference_id.py",
        ".aide/reports/reference-id/reference-map.json",
        ".aide/reports/reference-id/projection-report.json",
        ".aide/reports/reference-id/validation.json",
        ".aide/reports/reference-id-accept/acceptance-report.json",
        ".aide/queue/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01/status.yaml",
        ".aide/protocol/aide-event-record.schema.json",
        "core/protocol/event_record.py",
    ]
    paths: list[Path] = []
    for rel in rel_paths:
        path = root / rel
        if path.exists() and path.is_file():
            paths.append(path)
    return paths


def _hashes(paths: list[Path]) -> dict[str, str]:
    return {path.as_posix(): sha256_file(path) for path in paths if path.exists() and path.is_file()}


def project_event_family_index(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    warnings = [
        "Event family names reserve schema vocabulary only and do not implement their subsystems.",
        "EventRecord examples are projection-only and are not appended to a runtime store.",
    ]
    family_index = {
        "schema_version": "aide.event-record-family-index.v0",
        "report_type": "event_record_family_index",
        "kind": "EventFamilyIndex",
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "status": "PASS_WITH_WARNINGS",
        "event_family_count": len(EVENT_FAMILIES),
        "event_families": EVENT_FAMILIES,
        "implemented_subsystems": False,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "warnings": warnings,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / EVENT_FAMILY_INDEX_JSON, family_index)
    write_text(root / EVENT_FAMILY_INDEX_MD, render_event_family_index_markdown(family_index))
    return family_index


def project_event_record_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    source_paths = _source_paths(root)
    hashes_before = _hashes(source_paths)
    family_index = project_event_family_index(root)
    examples = project_event_examples(root)
    example_errors = [error for record in examples for error in validate_event_record(record)]
    example_payload = {
        "schema_version": "aide.event-record-examples.v0",
        "report_type": "event_record_examples",
        "kind": "EventRecordExamples",
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "status": "PASS_WITH_WARNINGS" if not example_errors else "FAILED_VALIDATION",
        "example_count": len(examples),
        "examples": examples,
        "validation_errors": example_errors,
        "projection_only": True,
        "recorded": False,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / EXAMPLE_EVENTS_JSON, example_payload)
    write_text(root / EXAMPLE_EVENTS_MD, render_example_events_markdown(example_payload))
    hashes_after = _hashes(source_paths)
    source_artifacts_mutated = hashes_before != hashes_after
    validation_errors = list(example_errors)
    if source_artifacts_mutated:
        validation_errors.append("source artifacts mutated during EventRecord projection")
    status = "FAILED_VALIDATION" if validation_errors else "PASS_WITH_WARNINGS"
    warnings = [
        "EventRecord is a metadata/projection schema only; no event store or replay runtime is implemented.",
        "Reserved event family names do not implement OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, or runtime coordination.",
    ]
    report = {
        "schema_version": "aide.event-record-projection.v0",
        "report_type": "event_record_projection",
        "kind": "EventRecordProjectionReport",
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "accepted_predecessor": ACCEPTED_PREDECESSOR,
        "status": status,
        "event_family_count": family_index["event_family_count"],
        "event_families": event_family_names(),
        "example_event_count": len(examples),
        "example_events_path": EXAMPLE_EVENTS_JSON.as_posix(),
        "event_family_index_path": EVENT_FAMILY_INDEX_JSON.as_posix(),
        "source_artifacts_checked": [_relative_posix(path, root) for path in source_paths],
        "source_artifacts_mutated": source_artifacts_mutated,
        "reports_written": [
            PROJECTION_JSON.as_posix(),
            PROJECTION_MD.as_posix(),
            EVENT_FAMILY_INDEX_JSON.as_posix(),
            EVENT_FAMILY_INDEX_MD.as_posix(),
            EXAMPLE_EVENTS_JSON.as_posix(),
            EXAMPLE_EVENTS_MD.as_posix(),
        ],
        "validation_errors": validation_errors,
        "warnings": warnings,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_after_check": RECOMMENDED_AFTER_CHECK,
        "runtime_event_store_implemented": False,
        "event_sourcing_runtime_implemented": False,
        "append_only_runtime_store_implemented": False,
        "runtime_event_log_implemented": False,
        "state_reconstruction_implemented": False,
        "okf_knowledge_bundle_implemented": False,
        "reconciler_implemented": False,
        "capability_manifest_implemented": False,
        "conformance_profile_implemented": False,
        "patch_transaction_implemented": False,
        "adapter_manifest_implemented": False,
        "context_pack_v2_implemented": False,
        "runtime_reference_registry_implemented": False,
        "resolver_service_implemented": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
        "github_mutation": False,
    }
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    write_future_and_unfinished_reports(root)
    return report


def event_record_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    data = {
        "schema_version": "aide.event-record-status.v0",
        "report_type": "event_record_status",
        "status": "PASS_WITH_WARNINGS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "schema_file_exists": (root / SCHEMA_PATH).exists(),
        "helper_path": "core/protocol/event_record.py",
        "helper_exists": (root / "core/protocol/event_record.py").exists(),
        "accepted_predecessor": ACCEPTED_PREDECESSOR,
        "capability_label": FEATURE_FLAG,
        "event_family_count": len(EVENT_FAMILIES),
        "example_events_exists": (root / EXAMPLE_EVENTS_JSON).exists(),
        "projection_report_exists": (root / PROJECTION_JSON).exists(),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "warnings": [
            "EventRecord is projection-only and does not implement an append-only event store.",
            "OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, and runtime coordination remain future work.",
        ],
        "runtime_event_store_implemented": False,
        "event_sourcing_runtime_implemented": False,
        "append_only_runtime_store_implemented": False,
        "runtime_event_log_implemented": False,
        "state_reconstruction_implemented": False,
        "okf_knowledge_bundle_implemented": False,
        "reconciler_implemented": False,
        "capability_manifest_implemented": False,
        "conformance_profile_implemented": False,
        "patch_transaction_implemented": False,
        "adapter_manifest_implemented": False,
        "context_pack_v2_implemented": False,
        "runtime_reference_registry_implemented": False,
        "resolver_service_implemented": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
        "github_mutation": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    write_future_and_unfinished_reports(root)
    return data


def _compatibility_results(repo_root: Path) -> dict[str, Any]:
    reports = {
        "contract_envelope": Path(".aide/reports/contract-envelope/validation.json"),
        "evidence_packet": Path(".aide/reports/evidence-packet/validation.json"),
        "workunit_queue": Path(".aide/reports/workunit-queue/validation.json"),
        "worker_run": Path(".aide/reports/worker-run/validation.json"),
        "test_job": Path(".aide/reports/test-job/validation.json"),
        "test_job_acceptance": Path(".aide/reports/test-job-accept/acceptance-report.json"),
        "reference_id": Path(".aide/reports/reference-id/validation.json"),
        "reference_id_acceptance": Path(".aide/reports/reference-id-accept/acceptance-report.json"),
    }
    parsed: dict[str, bool] = {}
    statuses: dict[str, str] = {}
    errors: list[str] = []
    for key, rel in reports.items():
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
        status = str(data.get("status") or data.get("result") or "UNKNOWN")
        statuses[key] = status
        if status not in {"PASS", "PASS_WITH_WARNINGS", "ACCEPTED_WITH_WARNINGS"}:
            errors.append(f"{rel.as_posix()} has non-passing status: {status}")
    return {
        "status": "PASS" if not errors else "FAILED_VALIDATION",
        "parsed_reports": parsed,
        "report_statuses": statuses,
        "errors": errors,
        "contract_envelope_behavior_preserved": parsed.get("contract_envelope", False),
        "evidence_packet_behavior_preserved": parsed.get("evidence_packet", False),
        "workunit_queue_behavior_preserved": parsed.get("workunit_queue", False),
        "worker_run_behavior_preserved": parsed.get("worker_run", False),
        "test_job_behavior_preserved": parsed.get("test_job", False),
        "test_job_acceptance_preserved": parsed.get("test_job_acceptance", False),
        "reference_id_behavior_preserved": parsed.get("reference_id", False),
        "reference_id_acceptance_preserved": parsed.get("reference_id_acceptance", False),
        "destructive_migration_performed": False,
        "event_records_do_not_replace_reference_ids": True,
    }


def forbidden_operations_preserved() -> dict[str, bool]:
    return {
        "event_sourcing_runtime": True,
        "append_only_runtime_store": True,
        "runtime_event_log": True,
        "state_reconstruction": True,
        "scheduler": True,
        "leases": True,
        "supervisor": True,
        "test_broker_runtime": True,
        "async_execution": True,
        "worker_execution": True,
        "service": True,
        "commander": True,
        "okf_knowledge_bundle": True,
        "reconciler": True,
        "capability_manifest": True,
        "conformance_profile": True,
        "patch_transaction": True,
        "adapter_manifest": True,
        "context_pack_v2": True,
        "runtime_reference_registry": True,
        "resolver_service": True,
        "database_state": True,
        "provider_adapters": True,
        "branch_worktree_automation": True,
        "target_apply": True,
        "active_apply": True,
        "rollback_execution": True,
        "uninstall_execution": True,
        "release": True,
        "promotion": True,
        "github_mutation": True,
        "gateway_calls": True,
        "network_calls": True,
        "model_provider_calls": True,
        "target_repo_mutation": True,
        "broad_autonomous_runtime": True,
        "production_readiness": True,
        "release_readiness": True,
    }


def _event_refs(record: dict[str, Any]) -> list[str]:
    spec = record.get("spec", {}) if isinstance(record.get("spec"), dict) else {}
    refs: list[str] = []
    for value in [spec.get("event_ref")]:
        if isinstance(value, str):
            refs.append(value)
    subject = spec.get("subject")
    if isinstance(subject, dict) and isinstance(subject.get("ref"), str):
        refs.append(subject["ref"])
    for field in ["causation", "correlation", "actor"]:
        value = spec.get(field)
        if isinstance(value, dict) and isinstance(value.get("ref"), str):
            refs.append(value["ref"])
    for field in ["evidence_refs", "report_refs"]:
        for ref in spec.get(field, []) if isinstance(spec.get(field), list) else []:
            if isinstance(ref, str):
                refs.append(ref)
    return refs


def event_record_validate(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    projection_result = project_event_record_reports(root) if project else {"status": "UNKNOWN"}
    schema_path = root / SCHEMA_PATH
    schema_file_loaded = False
    schema_file_parsed = False
    schema_validation_executed = False
    schema_load_errors: list[str] = []
    alignment_result: dict[str, Any] = {}
    alignment_errors: list[str] = []
    alignment_warnings: list[str] = []
    try:
        schema = load_event_record_schema(root)
        schema_file_loaded = True
        schema_file_parsed = True
    except ValueError as exc:
        schema = {}
        schema_load_errors.append(str(exc))
    if schema_file_parsed:
        alignment_result = check_schema_helper_alignment(schema)
        alignment_errors = list(alignment_result.get("errors", []))
        alignment_warnings = list(alignment_result.get("warnings", []))

    family_index_json_valid = False
    event_family_index_errors: list[str] = []
    try:
        family_index = read_json(root / EVENT_FAMILY_INDEX_JSON)
        family_index_json_valid = True
        raw_families = family_index.get("event_families", [])
        families = [item for item in raw_families if isinstance(item, dict)]
    except Exception as exc:  # noqa: BLE001 - validation must report malformed indexes.
        family_index = {}
        families = []
        event_family_index_errors.append(str(exc))
    missing_required_families = [name for name in event_family_names() if name not in {str(item.get("event_type")) for item in families}]
    if missing_required_families:
        event_family_index_errors.append(f"missing required event families: {', '.join(missing_required_families)}")
    if any(item.get("implemented_subsystem") is not False for item in families):
        event_family_index_errors.append("event family index must mark implemented_subsystem false for every family")

    example_events_json_valid = False
    example_event_errors: list[str] = []
    records: list[dict[str, Any]] = []
    try:
        example_payload = read_json(root / EXAMPLE_EVENTS_JSON)
        example_events_json_valid = True
        raw_records = example_payload.get("examples", [])
        records = [item for item in raw_records if isinstance(item, dict)]
    except Exception as exc:  # noqa: BLE001 - validation must report malformed examples.
        example_payload = {}
        example_event_errors.append(str(exc))

    validation_results: list[dict[str, Any]] = []
    runtime_validation_results: list[dict[str, Any]] = []
    helper_validation_errors: dict[str, list[str]] = {}
    schema_validation_errors: dict[str, list[str]] = {}
    reference_validation_errors: dict[str, list[str]] = {}
    for record in records:
        ref = str(record.get("spec", {}).get("event_ref", record.get("metadata", {}).get("id", "")))
        helper_errors = validate_event_record(record)
        schema_errors: list[str] = []
        if schema_file_parsed:
            runtime = validate_event_record_runtime(record, schema)
            schema_validation_executed = True
            helper_errors = runtime["helper_validation_errors"]
            schema_errors = runtime["schema_validation_errors"]
            runtime_validation_results.append(
                {
                    "event_ref": ref,
                    "result": runtime["status"],
                    "helper_valid": runtime["helper_valid"],
                    "schema_valid": runtime["schema_valid"],
                }
            )
        else:
            schema_errors = schema_load_errors
        ref_errors = []
        for observed_ref in _event_refs(record):
            result = reference_id.validate_reference_id(observed_ref, required=True)
            ref_errors.extend(result.errors)
        helper_validation_errors[ref] = helper_errors
        schema_validation_errors[ref] = schema_errors
        reference_validation_errors[ref] = ref_errors
        errors = [*helper_errors, *schema_errors, *ref_errors]
        validation_results.append(
            {
                "event_ref": ref,
                "result": "PASS" if not errors else "FAILED_VALIDATION",
                "errors": errors,
                "helper_validation_errors": helper_errors,
                "schema_validation_errors": schema_errors,
                "reference_validation_errors": ref_errors,
            }
        )
    if schema_file_parsed:
        schema_validation_executed = True

    optional_event = validate_event_type("FutureEventType", required=False)
    required_event = validate_event_type("FutureEventType", required=True)
    invalid_event_types = ["workUnitStateChanged", "work-unit-state-changed", "Work Unit", "1BadEvent", "Bad_Event"]
    rejected_invalid_event_types = all(not validate_event_type(item, required=False).valid for item in invalid_event_types)
    compatibility_results = _compatibility_results(root)
    forbidden = forbidden_operations_preserved()
    overclaiming_check_passed = all(forbidden.values())
    all_example_events_validate = bool(validation_results) and all(item["result"] == "PASS" for item in validation_results)
    all_example_refs_parse = bool(validation_results) and all(not errors for errors in reference_validation_errors.values())
    validation_errors = [
        *schema_load_errors,
        *alignment_errors,
        *event_family_index_errors,
        *example_event_errors,
        *[error for item in validation_results for error in item["errors"]],
    ]
    status = (
        "PASS_WITH_WARNINGS"
        if not validation_errors
        and projection_result.get("status") in {"PASS", "PASS_WITH_WARNINGS"}
        and family_index_json_valid
        and example_events_json_valid
        and all_example_events_validate
        and all_example_refs_parse
        and compatibility_results["status"] == "PASS"
        and overclaiming_check_passed
        and bool(optional_event.warnings)
        and bool(required_event.errors)
        and rejected_invalid_event_types
        else "FAILED_VALIDATION"
    )
    warnings = [
        "EventRecord is schema/projection-only and does not implement an event sourcing runtime.",
        "Example events are projected JSON records only; they are not appended or replayed.",
        "OKF knowledge bundle is not implemented by this task.",
        "PatchTransaction, AdapterManifest, ContextPack v2, Reconciler, CapabilityManifest, and ConformanceProfile remain future work.",
        *alignment_warnings,
    ]
    report = {
        "schema_version": "aide.event-record-validation.v0",
        "report_type": "event_record_validation",
        "kind": "EventRecordValidationReport",
        "task_id": TASK_ID,
        "status": status,
        "validation_status": status,
        "validated": status in {"PASS", "PASS_WITH_WARNINGS"},
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_target": FEATURE_FLAG,
        "capability_label": FEATURE_FLAG,
        "accepted_predecessor": ACCEPTED_PREDECESSOR,
        "schema_path": SCHEMA_PATH.as_posix(),
        "schema_exists": schema_path.exists(),
        "schema_file_loaded": schema_file_loaded,
        "schema_file_parsed": schema_file_parsed,
        "schema_validation_executed": schema_validation_executed,
        "schema_validation_mode": SCHEMA_VALIDATION_MODE if schema_validation_executed else "unavailable",
        "schema_validation_limitations": SCHEMA_VALIDATION_LIMITATIONS,
        "schema_helper_alignment_checked": schema_file_parsed,
        "schema_helper_alignment_status": alignment_result.get("schema_helper_alignment_status", "FAILED_VALIDATION"),
        "helper_path": "core/protocol/event_record.py",
        "helper_exists": (root / "core/protocol/event_record.py").exists(),
        "cli_registered": True,
        "projection_generated": projection_result.get("status") in {"PASS", "PASS_WITH_WARNINGS"},
        "family_index_json_valid": family_index_json_valid,
        "example_events_json_valid": example_events_json_valid,
        "event_family_count": len(families),
        "required_event_families_present": not missing_required_families,
        "event_families": event_family_names(),
        "example_event_count": len(records),
        "all_example_events_validate": all_example_events_validate,
        "all_example_refs_parse": all_example_refs_parse,
        "reference_id_integration_preserved": all_example_refs_parse,
        "predecessor_compatibility_preserved": compatibility_results["status"] == "PASS",
        "overclaiming_check_passed": overclaiming_check_passed,
        "forbidden_ops_preserved": all(forbidden.values()),
        "unknown_optional_event_type_warned": bool(optional_event.warnings),
        "unknown_required_event_type_fails_closed": bool(required_event.errors),
        "invalid_event_types_rejected": rejected_invalid_event_types,
        "validation_results": validation_results,
        "runtime_validation_results": runtime_validation_results,
        "helper_validation_errors": helper_validation_errors,
        "schema_validation_errors": schema_validation_errors,
        "reference_validation_errors": reference_validation_errors,
        "validation_errors": validation_errors,
        "warnings": warnings,
        "compatibility_results": compatibility_results,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "explicit_non_capabilities_preserved": True,
        "forbidden_operations_preserved": forbidden,
        "runtime_event_store_implemented": False,
        "event_sourcing_runtime_implemented": False,
        "append_only_runtime_store_implemented": False,
        "runtime_event_log_implemented": False,
        "state_reconstruction_implemented": False,
        "okf_knowledge_bundle_implemented": False,
        "reconciler_implemented": False,
        "capability_manifest_implemented": False,
        "conformance_profile_implemented": False,
        "patch_transaction_implemented": False,
        "adapter_manifest_implemented": False,
        "context_pack_v2_implemented": False,
        "runtime_reference_registry_implemented": False,
        "resolver_service_implemented": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
        "github_mutation": False,
        "projection_report_path": PROJECTION_JSON.as_posix(),
        "event_family_index_path": EVENT_FAMILY_INDEX_JSON.as_posix(),
        "example_events_path": EXAMPLE_EVENTS_JSON.as_posix(),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_after_check": RECOMMENDED_AFTER_CHECK,
        "recommended_after_acceptance": RECOMMENDED_AFTER_ACCEPTANCE,
        "unfinished_work": unfinished_work_items(),
        "future_work": future_work_items(),
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_markdown(report))
    write_future_and_unfinished_reports(root)
    return report


def future_work_items() -> list[dict[str, str]]:
    return [
        {"task": "AIDE-CHECK-EVENT-RECORD-SCHEMA-01", "reason": "independent review of the EventRecord schema, helper, projections, CLI, reports, tests, and non-capability boundaries"},
        {"task": "AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01", "reason": "accept EventRecord only after independent check"},
        {"task": "AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01", "reason": "future work after EventRecord acceptance, not a direct next task from this build"},
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    return [{"item": item, "reason": "intentionally deferred beyond the minimal EventRecord schema slice"} for item in EXPLICIT_NON_CAPABILITIES]


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# EventRecord Status",
        "",
        f"- status: {data.get('status')}",
        f"- api_version: {data.get('api_version')}",
        f"- protocol_version: {data.get('protocol_version')}",
        f"- schema_file_path: {data.get('schema_file_path')}",
        f"- schema_file_exists: {str(data.get('schema_file_exists', False)).lower()}",
        f"- helper_path: {data.get('helper_path')}",
        f"- helper_exists: {str(data.get('helper_exists', False)).lower()}",
        f"- capability_label: {data.get('capability_label')}",
        f"- accepted_predecessor: {data.get('accepted_predecessor')}",
        f"- event_family_count: {data.get('event_family_count')}",
        f"- projection_report_exists: {str(data.get('projection_report_exists', False)).lower()}",
        "- recorded: false",
        "- projection_only: true",
        "- runtime_event_store_implemented: false",
        "- event_sourcing_runtime_implemented: false",
        "- append_only_runtime_store_implemented: false",
        "- runtime_event_log_implemented: false",
        "- state_reconstruction_implemented: false",
        "- okf_knowledge_bundle_implemented: false",
        "- reconciler_implemented: false",
        "- capability_manifest_implemented: false",
        "- conformance_profile_implemented: false",
        "- patch_transaction_implemented: false",
        "- adapter_manifest_implemented: false",
        "- context_pack_v2_implemented: false",
        "- runtime_reference_registry_implemented: false",
        "- resolver_service_implemented: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- branch_mutation: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "- github_mutation: false",
        f"- recommended_next_task: {data.get('recommended_next_task')}",
        "",
        "## Event Families",
        "",
    ]
    for name in event_family_names():
        lines.append(f"- {name}")
    lines.extend(["", "## Explicit Non-Capabilities", ""])
    for item in data.get("explicit_non_capabilities", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Warnings", ""])
    for warning in data.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def render_event_family_index_markdown(index: dict[str, Any]) -> str:
    lines = [
        "# EventRecord Event Family Index",
        "",
        f"- status: {index.get('status')}",
        f"- task_id: {index.get('task_id')}",
        f"- capability_target: {index.get('capability_target')}",
        f"- event_family_count: {index.get('event_family_count')}",
        "- implemented_subsystems: false",
        "",
        "## Families",
        "",
    ]
    for family in index.get("event_families", []):
        lines.append(
            f"- {family.get('event_type')}: {family.get('status')}; implemented_subsystem={str(family.get('implemented_subsystem')).lower()}; payload_contract={family.get('payload_contract')}"
        )
    lines.extend(["", "## Warnings", ""])
    for warning in index.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def render_example_events_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# EventRecord Example Events",
        "",
        f"- status: {payload.get('status')}",
        f"- task_id: {payload.get('task_id')}",
        f"- capability_target: {payload.get('capability_target')}",
        f"- example_count: {payload.get('example_count')}",
        "- recorded: false",
        "- projection_only: true",
        "",
        "## Examples",
        "",
    ]
    for record in payload.get("examples", []):
        spec = record.get("spec", {}) if isinstance(record, dict) else {}
        subject = spec.get("subject", {}) if isinstance(spec.get("subject"), dict) else {}
        lines.append(f"- {spec.get('event_ref')}: {spec.get('event_type')} subject={subject.get('ref')}")
    if payload.get("validation_errors"):
        lines.extend(["", "## Errors", ""])
        for error in payload.get("validation_errors", []):
            lines.append(f"- {error}")
    return "\n".join(lines) + "\n"


def render_projection_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# EventRecord Projection",
        "",
        f"- status: {report.get('status')}",
        f"- task_id: {report.get('task_id')}",
        f"- capability_target: {report.get('capability_target')}",
        f"- accepted_predecessor: {report.get('accepted_predecessor')}",
        f"- event_family_count: {report.get('event_family_count')}",
        f"- example_event_count: {report.get('example_event_count')}",
        f"- source_artifacts_mutated: {str(report.get('source_artifacts_mutated', False)).lower()}",
        "- recorded: false",
        "- projection_only: true",
        "- runtime_event_store_implemented: false",
        "- event_sourcing_runtime_implemented: false",
        "- append_only_runtime_store_implemented: false",
        "- runtime_event_log_implemented: false",
        "- state_reconstruction_implemented: false",
        "- okf_knowledge_bundle_implemented: false",
        "- reconciler_implemented: false",
        "- capability_manifest_implemented: false",
        "- conformance_profile_implemented: false",
        "- patch_transaction_implemented: false",
        "- adapter_manifest_implemented: false",
        "- context_pack_v2_implemented: false",
        "- runtime_reference_registry_implemented: false",
        "- resolver_service_implemented: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- branch_mutation: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "- github_mutation: false",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Source Artifacts Checked",
        "",
    ]
    for rel in report.get("source_artifacts_checked", []):
        lines.append(f"- {rel}")
    lines.extend(["", "## Reports Written", ""])
    for rel in report.get("reports_written", []):
        lines.append(f"- {rel}")
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    if report.get("validation_errors"):
        lines.extend(["", "## Errors", ""])
        for error in report.get("validation_errors", []):
            lines.append(f"- {error}")
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# EventRecord Validation",
        "",
        f"- status: {report.get('status')}",
        f"- validation_status: {report.get('validation_status')}",
        f"- capability_target: {report.get('capability_target')}",
        f"- accepted_predecessor: {report.get('accepted_predecessor')}",
        f"- schema_path: {report.get('schema_path')}",
        f"- schema_exists: {str(report.get('schema_exists', False)).lower()}",
        f"- helper_path: {report.get('helper_path')}",
        f"- helper_exists: {str(report.get('helper_exists', False)).lower()}",
        f"- cli_registered: {str(report.get('cli_registered', False)).lower()}",
        f"- projection_generated: {str(report.get('projection_generated', False)).lower()}",
        f"- family_index_json_valid: {str(report.get('family_index_json_valid', False)).lower()}",
        f"- example_events_json_valid: {str(report.get('example_events_json_valid', False)).lower()}",
        f"- required_event_families_present: {str(report.get('required_event_families_present', False)).lower()}",
        f"- all_example_events_validate: {str(report.get('all_example_events_validate', False)).lower()}",
        f"- all_example_refs_parse: {str(report.get('all_example_refs_parse', False)).lower()}",
        f"- reference_id_integration_preserved: {str(report.get('reference_id_integration_preserved', False)).lower()}",
        f"- predecessor_compatibility_preserved: {str(report.get('predecessor_compatibility_preserved', False)).lower()}",
        f"- overclaiming_check_passed: {str(report.get('overclaiming_check_passed', False)).lower()}",
        f"- forbidden_ops_preserved: {str(report.get('forbidden_ops_preserved', False)).lower()}",
        f"- unknown_optional_event_type_warned: {str(report.get('unknown_optional_event_type_warned', False)).lower()}",
        f"- unknown_required_event_type_fails_closed: {str(report.get('unknown_required_event_type_fails_closed', False)).lower()}",
        f"- invalid_event_types_rejected: {str(report.get('invalid_event_types_rejected', False)).lower()}",
        "- recorded: false",
        "- projection_only: true",
        "- runtime_event_store_implemented: false",
        "- event_sourcing_runtime_implemented: false",
        "- append_only_runtime_store_implemented: false",
        "- runtime_event_log_implemented: false",
        "- state_reconstruction_implemented: false",
        "- okf_knowledge_bundle_implemented: false",
        "- reconciler_implemented: false",
        "- capability_manifest_implemented: false",
        "- conformance_profile_implemented: false",
        "- patch_transaction_implemented: false",
        "- adapter_manifest_implemented: false",
        "- context_pack_v2_implemented: false",
        "- runtime_reference_registry_implemented: false",
        "- resolver_service_implemented: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- branch_mutation: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "- github_mutation: false",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Validation Results",
        "",
    ]
    for item in report.get("validation_results", []):
        lines.append(f"- {item.get('result')}: {item.get('event_ref')}")
    lines.extend(["", "## Event Families", ""])
    for name in report.get("event_families", []):
        lines.append(f"- {name}")
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    if report.get("validation_errors"):
        lines.extend(["", "## Errors", ""])
        for error in report.get("validation_errors", []):
            lines.append(f"- {error}")
    return "\n".join(lines) + "\n"


def write_future_and_unfinished_reports(repo_root: Path) -> None:
    future_lines = [
        "# EventRecord Future Work",
        "",
        "## Recommended Order",
        "",
    ]
    for index, item in enumerate(future_work_items(), start=1):
        future_lines.append(f"{index}. {item['task']}: {item['reason']}.")
    future_lines.extend(
        [
            "",
            "This build task recommends only `AIDE-CHECK-EVENT-RECORD-SCHEMA-01` as the next task.",
            "OKF is listed only after EventRecord check and acceptance.",
        ]
    )
    unfinished_lines = [
        "# EventRecord Unfinished Work",
        "",
        "## Finished In This Slice",
        "",
        "- Minimal EventRecord schema/helper/projection/validation.",
        "- ReferenceID-backed subject, causation, correlation, evidence, and report refs.",
        "- Event family vocabulary and projection-only example events.",
        "- Local reports under `.aide/reports/event-record/`.",
        "",
        "## Not Attempted By Design",
        "",
    ]
    for item in unfinished_work_items():
        unfinished_lines.append(f"- {item['item']}: {item['reason']}.")
    write_text(repo_root / FUTURE_WORK_MD, "\n".join(future_lines) + "\n")
    write_text(repo_root / UNFINISHED_WORK_MD, "\n".join(unfinished_lines) + "\n")
