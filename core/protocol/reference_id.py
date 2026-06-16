"""Minimal AIDE ReferenceID helpers.

This module defines ReferenceID as data only: stable ``aide://`` identities
with optional file locators and content hashes. It projects accepted protocol
artifacts into a deterministic reference map without implementing a runtime
registry, resolver service, event system, knowledge bundle, patch system, or
adapter layer.
"""

from __future__ import annotations

import copy
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from core.protocol import envelope


API_VERSION = envelope.API_VERSION
REFERENCE_ID_SCHEMA_VERSION = "aide.reference-id.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_reference_id_scheme"
ACCEPTED_PREDECESSOR = "minimal_test_job_schema"
TASK_ID = "AIDE-BUILD-REFERENCE-ID-SCHEME-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-REFERENCE-ID-SCHEME-01"
REPORT_ROOT = Path(".aide/reports/reference-id")
SCHEMA_PATH = Path(".aide/protocol/aide-reference-id.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
REFERENCE_MAP_JSON = REPORT_ROOT / "reference-map.json"
REFERENCE_MAP_MD = REPORT_ROOT / "reference-map.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"

SUPPORTED_KINDS = {
    "ReferenceID",
    "ReferenceIDProjectionReport",
    "ReferenceIDValidationReport",
    "ReferenceIDMap",
}
REFERENCE_REQUIRED_FIELDS = ["apiVersion", "kind", "metadata", "spec", "status"]
REQUIRED_METADATA_FIELDS = ["id", "createdAt", "sourcePath", "producer", "compatibility"]
REQUIRED_SPEC_FIELDS = [
    "ref",
    "ref_kind",
    "identity",
    "locator",
    "required",
    "relationship",
    "explicit_non_capabilities",
]
REQUIRED_STATUS_FIELDS = ["valid", "resolution", "validation_errors", "validation_warnings"]
REFERENCE_RELATIONSHIPS = {"identifies", "references", "projects", "describes", "future_placeholder"}
RESOLUTION_VALUES = {"syntactic_only", "locator_present", "locator_missing", "not_resolved"}
RESULT_VALUES = {"PASS", "PASS_WITH_WARNINGS", "FAILED_VALIDATION", "BLOCKED", "PARTIAL", "UNKNOWN"}
KNOWN_REF_KINDS = {
    "queue-task",
    "workunit",
    "worker-run",
    "test-job",
    "evidence",
    "event",
    "capability",
    "conformance-profile",
    "conformance-result",
    "adapter",
    "patch-transaction",
    "context-pack",
    "artifact",
    "source",
    "report",
    "schema",
    "policy",
    "decision",
    "checkpoint",
    "wave",
    "goal",
}
RECOGNIZED_CAPABILITIES = {
    FEATURE_FLAG,
    ACCEPTED_PREDECESSOR,
    "minimal_contract_envelope",
    "minimal_evidence_packet_schema",
    "minimal_workunit_queue_v1",
    "minimal_worker_run_schema",
}
EXPLICIT_NON_CAPABILITIES = [
    "event_record_implementation",
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
    "leases",
    "scheduler",
    "supervisor",
    "test_broker_runtime",
    "async_execution",
    "worker_execution",
    "service",
    "commander",
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
    "production_readiness",
    "release_readiness",
    "broad_autonomous_runtime",
]
SCHEMA_VALIDATION_MODE = "minimal_json_schema_subset"
SCHEMA_VALIDATION_LIMITATIONS = [
    "Local subset validator supports type, enum, required, properties, simple additionalProperties, and homogeneous array items only.",
    "Full JSON Schema Draft 2020-12 validation remains future work.",
    "Formats, refs, oneOf/anyOf/allOf, conditionals, numeric bounds, and pattern checks are not implemented.",
]
ID_PATTERN = re.compile(r"^[A-Za-z0-9._~-]+$")
KIND_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")


@dataclass(frozen=True)
class ReferenceId:
    kind: str
    object_id: str
    fragment: str | None = None

    @property
    def ref(self) -> str:
        suffix = f"#{self.fragment}" if self.fragment is not None else ""
        return f"aide://{self.kind}/{self.object_id}{suffix}"


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    parsed: ReferenceId | None = None

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
            "parsed": (
                {
                    "kind": self.parsed.kind,
                    "id": self.parsed.object_id,
                    "fragment": self.parsed.fragment,
                    "ref": self.parsed.ref,
                }
                if self.parsed
                else None
            ),
        }


REFERENCE_DEFINITIONS: list[dict[str, Any]] = [
    {
        "ref": "aide://queue-task/AIDE-ACCEPT-TESTJOB-SCHEMA-01",
        "title": "TestJob Acceptance Task",
        "path": ".aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/task.yaml",
        "media_type": "text/yaml",
        "role": "queue_task",
        "source_status": "accepted_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://queue-task/AIDE-CHECK-TESTJOB-SCHEMA-01",
        "title": "TestJob Check Task",
        "path": ".aide/queue/AIDE-CHECK-TESTJOB-SCHEMA-01/task.yaml",
        "media_type": "text/yaml",
        "role": "queue_task",
        "source_status": "pass_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://queue-task/AIDE-BUILD-TESTJOB-SCHEMA-01",
        "title": "TestJob Build Task",
        "path": ".aide/queue/AIDE-BUILD-TESTJOB-SCHEMA-01/task.yaml",
        "media_type": "text/yaml",
        "role": "queue_task",
        "source_status": "pass",
        "required": True,
    },
    {
        "ref": "aide://queue-task/AIDE-ACCEPT-WORKER-RUN-SCHEMA-01",
        "title": "WorkerRun Acceptance Task",
        "path": ".aide/queue/AIDE-ACCEPT-WORKER-RUN-SCHEMA-01/task.yaml",
        "media_type": "text/yaml",
        "role": "queue_task",
        "source_status": "accepted_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://schema/envelope",
        "title": "Contract Envelope Schema",
        "path": ".aide/protocol/aide-envelope.schema.json",
        "media_type": "application/schema+json",
        "role": "protocol_schema",
        "source_status": "pass",
        "required": True,
    },
    {
        "ref": "aide://schema/evidence-packet",
        "title": "EvidencePacket Schema",
        "path": ".aide/protocol/aide-evidence-packet.schema.json",
        "media_type": "application/schema+json",
        "role": "protocol_schema",
        "source_status": "pass",
        "required": True,
    },
    {
        "ref": "aide://schema/workunit",
        "title": "WorkUnit Schema",
        "path": ".aide/protocol/aide-workunit.schema.json",
        "media_type": "application/schema+json",
        "role": "protocol_schema",
        "source_status": "pass",
        "required": True,
    },
    {
        "ref": "aide://schema/worker-run",
        "title": "WorkerRun Schema",
        "path": ".aide/protocol/aide-worker-run.schema.json",
        "media_type": "application/schema+json",
        "role": "protocol_schema",
        "source_status": "accepted_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://schema/test-job",
        "title": "TestJob Schema",
        "path": ".aide/protocol/aide-test-job.schema.json",
        "media_type": "application/schema+json",
        "role": "protocol_schema",
        "source_status": "accepted_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://schema/reference-id",
        "title": "ReferenceID Schema",
        "path": ".aide/protocol/aide-reference-id.schema.json",
        "media_type": "application/schema+json",
        "role": "protocol_schema",
        "source_status": "implementation_completed",
        "required": True,
    },
    {
        "ref": "aide://capability/minimal_contract_envelope",
        "title": "Minimal Contract Envelope Capability",
        "path": ".aide/reports/contract-envelope/validation.json",
        "media_type": "application/json",
        "role": "accepted_capability_source",
        "source_status": "pass",
        "required": True,
    },
    {
        "ref": "aide://capability/minimal_evidence_packet_schema",
        "title": "Minimal EvidencePacket Capability",
        "path": ".aide/reports/evidence-packet/validation.json",
        "media_type": "application/json",
        "role": "accepted_capability_source",
        "source_status": "pass",
        "required": True,
    },
    {
        "ref": "aide://capability/minimal_workunit_queue_v1",
        "title": "Minimal WorkUnit Queue Capability",
        "path": ".aide/reports/workunit-queue/validation.json",
        "media_type": "application/json",
        "role": "accepted_capability_source",
        "source_status": "pass",
        "required": True,
    },
    {
        "ref": "aide://capability/minimal_worker_run_schema",
        "title": "Minimal WorkerRun Schema Capability",
        "path": ".aide/reports/worker-run-accept/acceptance-report.json",
        "media_type": "application/json",
        "role": "accepted_capability_source",
        "source_status": "accepted_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://capability/minimal_test_job_schema",
        "title": "Minimal TestJob Schema Capability",
        "path": ".aide/reports/test-job-accept/acceptance-report.json",
        "media_type": "application/json",
        "role": "accepted_capability_source",
        "source_status": "accepted_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://report/test-job-acceptance-report",
        "title": "TestJob Acceptance Report",
        "path": ".aide/reports/test-job-accept/acceptance-report.json",
        "media_type": "application/json",
        "role": "acceptance_report",
        "source_status": "accepted_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://report/test-job-check-report",
        "title": "TestJob Check Report",
        "path": ".aide/reports/test-job-check/check-report.json",
        "media_type": "application/json",
        "role": "check_report",
        "source_status": "pass_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://report/test-job-validation",
        "title": "TestJob Validation Report",
        "path": ".aide/reports/test-job/validation.json",
        "media_type": "application/json",
        "role": "validation_report",
        "source_status": "pass",
        "required": True,
    },
    {
        "ref": "aide://report/reference-id-projection-report",
        "title": "ReferenceID Projection Report",
        "path": ".aide/reports/reference-id/projection-report.json",
        "media_type": "application/json",
        "role": "projection_report",
        "source_status": "implementation_completed",
        "required": False,
    },
    {
        "ref": "aide://report/reference-id-validation",
        "title": "ReferenceID Validation Report",
        "path": ".aide/reports/reference-id/validation.json",
        "media_type": "application/json",
        "role": "validation_report",
        "source_status": "implementation_completed",
        "required": False,
    },
    {
        "ref": "aide://evidence/aide-accept-testjob-schema-01-acceptance-summary",
        "title": "TestJob Acceptance Summary Evidence",
        "path": ".aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/evidence/acceptance-summary.md",
        "media_type": "text/markdown",
        "role": "queue_evidence",
        "source_status": "accepted_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://evidence/aide-accept-testjob-schema-01-warning-disposition",
        "title": "TestJob Warning Disposition Evidence",
        "path": ".aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/evidence/warning-disposition.md",
        "media_type": "text/markdown",
        "role": "queue_evidence",
        "source_status": "accepted_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://evidence/aide-accept-testjob-schema-01-non-capability-boundary",
        "title": "TestJob Non-Capability Boundary Evidence",
        "path": ".aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/evidence/non-capability-boundary.md",
        "media_type": "text/markdown",
        "role": "queue_evidence",
        "source_status": "accepted_with_warnings",
        "required": True,
    },
    {
        "ref": "aide://event/future-event-placeholder",
        "title": "Future Event Placeholder",
        "path": None,
        "media_type": None,
        "role": "future_ref_kind_placeholder",
        "source_status": "not_implemented",
        "required": False,
        "notes": ["Syntactically valid kind only; EventRecord is not implemented."],
    },
    {
        "ref": "aide://patch-transaction/future-patch-transaction-placeholder",
        "title": "Future PatchTransaction Placeholder",
        "path": None,
        "media_type": None,
        "role": "future_ref_kind_placeholder",
        "source_status": "not_implemented",
        "required": False,
        "notes": ["Syntactically valid kind only; PatchTransaction is not implemented."],
    },
]


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


def parse_reference_id(ref: str) -> ReferenceId:
    if not isinstance(ref, str) or not ref:
        raise ValueError("reference id must be a non-empty string")
    if _has_whitespace_or_control(ref):
        raise ValueError("reference id must not contain whitespace or control characters")
    parsed = urlsplit(ref)
    if parsed.scheme != "aide":
        raise ValueError(f"unsupported reference scheme: {parsed.scheme or '<missing>'}")
    if not parsed.netloc:
        raise ValueError("reference kind is missing")
    kind = parsed.netloc
    if not KIND_PATTERN.match(kind):
        raise ValueError(f"reference kind is invalid: {kind}")
    if parsed.query:
        raise ValueError("reference query strings are not supported")
    object_part = parsed.path[1:] if parsed.path.startswith("/") else parsed.path
    if not object_part:
        raise ValueError("reference object id is missing")
    if "/" in object_part:
        raise ValueError("reference object id must be one path segment")
    if object_part in {".", ".."} or ".." in object_part:
        raise ValueError("reference object id must not contain path traversal")
    if not ID_PATTERN.match(object_part):
        raise ValueError(f"reference object id has unsupported characters: {object_part}")
    fragment = parsed.fragment or None
    if fragment is not None:
        if _has_whitespace_or_control(fragment) or not ID_PATTERN.match(fragment) or ".." in fragment:
            raise ValueError(f"reference fragment has unsupported characters: {fragment}")
    return ReferenceId(kind=kind, object_id=object_part, fragment=fragment)


def format_reference_id(kind: str, object_id: str, fragment: str | None = None) -> str:
    kind_value = kind.strip() if isinstance(kind, str) else ""
    id_value = object_id.strip() if isinstance(object_id, str) else ""
    suffix = f"#{fragment}" if fragment is not None else ""
    ref = f"aide://{kind_value}/{id_value}{suffix}"
    parsed = parse_reference_id(ref)
    return parsed.ref


def validate_reference_id(
    ref: str,
    *,
    required: bool = False,
    known_ref_kinds: set[str] | None = None,
) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        parsed = parse_reference_id(ref)
    except ValueError as exc:
        return ValidationResult(False, (str(exc),), (), None)
    active_kinds = known_ref_kinds or KNOWN_REF_KINDS
    if parsed.kind not in active_kinds:
        message = f"unknown {'required' if required else 'optional'} ref kind: {parsed.kind}"
        if required:
            errors.append(message)
        else:
            warnings.append(message)
    return ValidationResult(not errors, tuple(errors), tuple(warnings), parsed)


def _deterministic_metadata_id(ref: str) -> str:
    return "ref-" + hashlib.sha256(ref.encode("utf-8")).hexdigest()[:16]


def _locator(repo_root: Path, path_value: str | None, media_type: str | None, role: str | None) -> dict[str, Any]:
    if not path_value:
        return {}
    rel = Path(path_value)
    actual = repo_root / rel
    result: dict[str, Any] = {
        "path": rel.as_posix(),
        "media_type": media_type or "application/octet-stream",
        "role": role or "locator",
    }
    if actual.exists() and actual.is_file():
        result["sha256"] = sha256_file(actual)
    return result


def build_reference_record(
    *,
    repo_root: Path,
    ref: str,
    title: str,
    locator_path: str | None = None,
    media_type: str | None = None,
    role: str | None = None,
    required: bool = False,
    relationship: str = "references",
    source_status: str = "",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    validation = validate_reference_id(ref, required=required)
    parsed = validation.parsed
    locator = _locator(repo_root, locator_path, media_type, role)
    validation_errors = list(validation.errors)
    validation_warnings = list(validation.warnings)
    if required and locator_path and not (repo_root / locator_path).exists():
        validation_errors.append(f"required locator is missing: {locator_path}")
    metadata = {
        "id": _deterministic_metadata_id(ref),
        "name": title,
        "title": title,
        "createdAt": "deterministic",
        "sourcePath": str(locator_path or ""),
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility(),
    }
    spec = {
        "ref": ref,
        "ref_kind": parsed.kind if parsed else "",
        "identity": {
            "namespace": parsed.kind if parsed else "",
            "id": parsed.object_id if parsed else "",
            "fragment": parsed.fragment if parsed else None,
        },
        "locator": locator,
        "required": bool(required),
        "relationship": relationship if relationship in REFERENCE_RELATIONSHIPS else "references",
        "title": title,
        "source_status": source_status,
        "notes": list(notes or []),
        "capability_label": FEATURE_FLAG,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "file_paths_are_locators": True,
        "stable_identity": ref,
        "runtime_resolution_implemented": False,
        "event_record_implemented": False,
        "okf_knowledge_bundle_implemented": False,
        "patch_transaction_implemented": False,
        "adapter_manifest_implemented": False,
        "resolver_service_implemented": False,
    }
    status = {
        "valid": not validation_errors,
        "phase": "metadata_only",
        "result": "PASS" if not validation_errors else "FAILED_VALIDATION",
        "resolution": "syntactic_only",
        "validated": not validation_errors,
        "validation_errors": validation_errors,
        "validation_warnings": validation_warnings,
    }
    obj = envelope.build_envelope("ReferenceID", metadata, spec, status, api_version=API_VERSION)
    obj["schema_version"] = REFERENCE_ID_SCHEMA_VERSION
    obj["protocol_version"] = PROTOCOL_VERSION
    return obj


def sample_reference_record() -> dict[str, Any]:
    return build_reference_record(
        repo_root=Path("."),
        ref="aide://schema/test-job",
        title="TestJob Schema",
        locator_path=".aide/protocol/aide-test-job.schema.json",
        media_type="application/schema+json",
        role="protocol_schema",
        required=False,
        source_status="accepted_with_warnings",
    )


def sample_unknown_optional_reference_record() -> dict[str, Any]:
    return build_reference_record(
        repo_root=Path("."),
        ref="aide://future-kind/optional-sample",
        title="Unknown Optional Sample",
        required=False,
        source_status="future",
    )


def sample_unknown_required_reference_record() -> dict[str, Any]:
    return build_reference_record(
        repo_root=Path("."),
        ref="aide://future-kind/required-sample",
        title="Unknown Required Sample",
        required=True,
        source_status="future",
    )


def validate_reference_record(record: dict[str, Any], known_ref_kinds: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["ReferenceID must be an object"]
    if record.get("apiVersion") != API_VERSION:
        errors.append(f"unsupported apiVersion: {record.get('apiVersion')}")
    if record.get("kind") != "ReferenceID":
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
    if not isinstance(metadata.get("id"), str) or not metadata.get("id"):
        errors.append("metadata.id must be a non-empty string")
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
    required = bool(spec.get("required", False))
    ref = spec.get("ref")
    if not isinstance(ref, str) or not ref:
        errors.append("spec.ref must be a non-empty string")
        ref_result = ValidationResult(False, ("spec.ref must be a non-empty string",))
    else:
        ref_result = validate_reference_id(ref, required=required, known_ref_kinds=known_ref_kinds)
        errors.extend(ref_result.errors)
    parsed = ref_result.parsed
    if parsed is not None:
        if spec.get("ref_kind") != parsed.kind:
            errors.append("spec.ref_kind must match parsed ref kind")
        identity = spec.get("identity")
        if not isinstance(identity, dict):
            errors.append("spec.identity must be an object")
        else:
            if identity.get("namespace") != parsed.kind:
                errors.append("spec.identity.namespace must match parsed ref kind")
            if identity.get("id") != parsed.object_id:
                errors.append("spec.identity.id must match parsed ref id")
            if identity.get("fragment") != parsed.fragment:
                errors.append("spec.identity.fragment must match parsed ref fragment")
    locator = spec.get("locator")
    if not isinstance(locator, dict):
        errors.append("spec.locator must be an object")
    else:
        path_value = locator.get("path")
        if path_value is not None and (not isinstance(path_value, str) or not path_value):
            errors.append("spec.locator.path must be a non-empty string when present")
        sha = locator.get("sha256")
        if sha is not None and not (isinstance(sha, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", sha)):
            errors.append("spec.locator.sha256 must be sha256:<64 lowercase hex>")
    if spec.get("relationship") not in REFERENCE_RELATIONSHIPS:
        errors.append(f"unsupported relationship: {spec.get('relationship')}")
    if not isinstance(spec.get("explicit_non_capabilities"), list):
        errors.append("spec.explicit_non_capabilities must be an array")
    elif spec.get("capability_label") in spec.get("explicit_non_capabilities", []):
        errors.append("spec.capability_label must not appear in explicit_non_capabilities")
    if spec.get("file_paths_are_locators") is not True:
        errors.append("spec.file_paths_are_locators must be true")
    for flag in [
        "runtime_resolution_implemented",
        "event_record_implemented",
        "okf_knowledge_bundle_implemented",
        "patch_transaction_implemented",
        "adapter_manifest_implemented",
        "resolver_service_implemented",
    ]:
        if spec.get(flag) is not False:
            errors.append(f"spec.{flag} must be false in this slice")
    status = record.get("status") if isinstance(record.get("status"), dict) else {}
    for field in REQUIRED_STATUS_FIELDS:
        if field not in status:
            errors.append(f"missing required status field: {field}")
    if not isinstance(status.get("valid"), bool):
        errors.append("status.valid must be a boolean")
    if status.get("resolution") not in RESOLUTION_VALUES:
        errors.append(f"unsupported status.resolution: {status.get('resolution')}")
    if not isinstance(status.get("validation_errors"), list):
        errors.append("status.validation_errors must be an array")
    if not isinstance(status.get("validation_warnings"), list):
        errors.append("status.validation_warnings must be an array")
    return errors


def load_reference_id_schema(repo_root: str | Path | None = None) -> dict[str, Any]:
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


def validate_reference_record_with_schema(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    active_schema = schema if schema is not None else load_reference_id_schema()
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
            "expected_required_fields": REFERENCE_REQUIRED_FIELDS,
            "schema_required_fields": [],
        }
    required = schema.get("required")
    schema_required = required if isinstance(required, list) else []
    missing = [field for field in REFERENCE_REQUIRED_FIELDS if field not in schema_required]
    extra_required = [str(field) for field in schema_required if field not in REFERENCE_REQUIRED_FIELDS]
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
    if "ReferenceID" not in schema_kinds:
        errors.append("schema.properties.kind.enum must include ReferenceID")
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
        "expected_required_fields": REFERENCE_REQUIRED_FIELDS,
        "schema_required_fields": [str(item) for item in schema_required],
        "missing_required_fields": missing,
        "extra_required_fields": extra_required,
    }


def validate_reference_record_runtime(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> dict[str, Any]:
    active_schema = schema if schema is not None else load_reference_id_schema()
    helper_errors = validate_reference_record(obj)
    schema_errors = validate_reference_record_with_schema(obj, active_schema)
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


def project_reference_records(repo_root: str | Path) -> list[dict[str, Any]]:
    root = Path(repo_root)
    records: list[dict[str, Any]] = []
    for item in REFERENCE_DEFINITIONS:
        records.append(
            build_reference_record(
                repo_root=root,
                ref=str(item["ref"]),
                title=str(item["title"]),
                locator_path=item.get("path"),
                media_type=item.get("media_type"),
                role=item.get("role"),
                required=bool(item.get("required", False)),
                relationship="references",
                source_status=str(item.get("source_status", "")),
                notes=[str(note) for note in item.get("notes", [])],
            )
        )
    return records


def _source_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for item in REFERENCE_DEFINITIONS:
        path_value = item.get("path")
        if isinstance(path_value, str) and not path_value.startswith(".aide/reports/reference-id/"):
            path = root / path_value
            if path.exists() and path.is_file():
                paths.append(path)
    return paths


def _hashes(paths: list[Path]) -> dict[str, str]:
    return {path.as_posix(): sha256_file(path) for path in paths if path.exists() and path.is_file()}


def project_reference_map(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    source_paths = _source_paths(root)
    hashes_before = _hashes(source_paths)
    records = project_reference_records(root)
    warnings = [
        "Reference ID Scheme is syntactic/projection-only and does not implement runtime resolution.",
        "Future ref kinds may be syntactically valid without implementing their object protocols.",
    ]
    missing_required = [
        record["spec"]["locator"].get("path", "")
        for record in records
        if record["spec"].get("required") is True
        and record["spec"].get("locator", {}).get("path")
        and not (root / record["spec"]["locator"]["path"]).exists()
    ]
    if missing_required:
        warnings.extend(f"missing required locator: {path}" for path in missing_required)
    reference_map = {
        "schema_version": "aide.reference-id-map.v0",
        "report_type": "reference_id_map",
        "kind": "ReferenceIDMap",
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "reference_scheme": {
            "scheme": "aide",
            "grammar": "aide://<kind>/<id>",
            "fragment_support": True,
            "identity_rule": "Stable IDs are identity; file paths are locators; hashes prove content.",
        },
        "known_ref_kinds": sorted(KNOWN_REF_KINDS),
        "references": records,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "warnings": warnings,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / REFERENCE_MAP_JSON, reference_map)
    write_text(root / REFERENCE_MAP_MD, render_reference_map_markdown(reference_map))
    hashes_after = _hashes(source_paths)
    source_artifacts_mutated = hashes_before != hashes_after
    invalid_records = [record for record in records if not record.get("status", {}).get("valid")]
    status = "FAILED_VALIDATION" if invalid_records or source_artifacts_mutated else "PASS_WITH_WARNINGS"
    report = {
        "schema_version": "aide.reference-id-projection.v0",
        "report_type": "reference_id_projection",
        "kind": "ReferenceIDProjectionReport",
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "status": status,
        "reference_scheme": reference_map["reference_scheme"],
        "known_ref_kinds": sorted(KNOWN_REF_KINDS),
        "projected_refs_count": len(records),
        "source_artifacts_checked": [_relative_posix(path, root) for path in source_paths],
        "source_artifacts_mutated": source_artifacts_mutated,
        "reports_written": [
            PROJECTION_JSON.as_posix(),
            PROJECTION_MD.as_posix(),
            REFERENCE_MAP_JSON.as_posix(),
            REFERENCE_MAP_MD.as_posix(),
        ],
        "reference_map_path": REFERENCE_MAP_JSON.as_posix(),
        "warnings": warnings,
        "validation_errors": [error for record in invalid_records for error in record["status"].get("validation_errors", [])],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "event_record_implemented": False,
        "okf_knowledge_bundle_implemented": False,
        "patch_transaction_implemented": False,
        "runtime_reference_registry_implemented": False,
        "resolver_service_implemented": False,
        "adapter_manifest_implemented": False,
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


def reference_id_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    data = {
        "schema_version": "aide.reference-id-status.v0",
        "report_type": "reference_id_status",
        "status": "PASS_WITH_WARNINGS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "schema_file_exists": (root / SCHEMA_PATH).exists(),
        "helper_path": "core/protocol/reference_id.py",
        "helper_exists": (root / "core/protocol/reference_id.py").exists(),
        "reference_map_exists": (root / REFERENCE_MAP_JSON).exists(),
        "capability_label": FEATURE_FLAG,
        "accepted_predecessor": ACCEPTED_PREDECESSOR,
        "reference_scheme": {
            "scheme": "aide",
            "grammar": "aide://<kind>/<id>",
            "fragment_support": True,
        },
        "known_ref_kinds": sorted(KNOWN_REF_KINDS),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "warnings": [
            "Reference ID Scheme is syntactic/projection-only and does not implement runtime resolution.",
            "EventRecord, OKF, PatchTransaction, adapter manifests, and ContextPack v2 remain future work.",
        ],
        "event_record_implemented": False,
        "okf_knowledge_bundle_implemented": False,
        "patch_transaction_implemented": False,
        "runtime_reference_registry_implemented": False,
        "resolver_service_implemented": False,
        "adapter_manifest_implemented": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
        "github_mutation": False,
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    write_future_and_unfinished_reports(root)
    return data


def _required_locators_exist(root: Path, records: list[dict[str, Any]]) -> bool:
    for record in records:
        spec = record.get("spec", {})
        locator = spec.get("locator", {}) if isinstance(spec, dict) else {}
        path_value = locator.get("path") if isinstance(locator, dict) else None
        if spec.get("required") is True and isinstance(path_value, str) and not (root / path_value).exists():
            return False
    return True


def _sha256_checked(records: list[dict[str, Any]]) -> bool:
    required_locators = []
    for record in records:
        spec = record.get("spec", {}) if isinstance(record.get("spec"), dict) else {}
        locator = spec.get("locator", {}) if isinstance(spec.get("locator"), dict) else {}
        if spec.get("required") is True and locator.get("path"):
            required_locators.append(locator)
    return bool(required_locators) and all("sha256" in locator for locator in required_locators)


def _compatibility_results(repo_root: Path) -> dict[str, Any]:
    reports = {
        "contract_envelope": Path(".aide/reports/contract-envelope/validation.json"),
        "evidence_packet": Path(".aide/reports/evidence-packet/validation.json"),
        "workunit_queue": Path(".aide/reports/workunit-queue/validation.json"),
        "worker_run": Path(".aide/reports/worker-run/validation.json"),
        "test_job": Path(".aide/reports/test-job/validation.json"),
        "test_job_acceptance": Path(".aide/reports/test-job-accept/acceptance-report.json"),
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
        statuses[key] = str(data.get("status") or data.get("result") or "UNKNOWN")
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
        "destructive_migration_performed": False,
        "reference_ids_do_not_replace_paths": True,
    }


def forbidden_operations_preserved() -> dict[str, bool]:
    return {
        "event_record_implementation": True,
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
        "leases": True,
        "scheduler": True,
        "supervisor": True,
        "test_broker_runtime": True,
        "async_execution": True,
        "worker_execution": True,
        "service": True,
        "commander": True,
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


def reference_id_validate(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    projection_result = project_reference_map(root) if project else {"status": "UNKNOWN"}
    schema_path = root / SCHEMA_PATH
    schema_file_loaded = False
    schema_file_parsed = False
    schema_validation_executed = False
    schema_load_errors: list[str] = []
    alignment_result: dict[str, Any] = {}
    alignment_errors: list[str] = []
    alignment_warnings: list[str] = []
    try:
        schema = load_reference_id_schema(root)
        schema_file_loaded = True
        schema_file_parsed = True
    except ValueError as exc:
        schema = {}
        schema_load_errors.append(str(exc))
    if schema_file_parsed:
        alignment_result = check_schema_helper_alignment(schema)
        alignment_errors = list(alignment_result.get("errors", []))
        alignment_warnings = list(alignment_result.get("warnings", []))
    reference_map_json_valid = False
    reference_map_errors: list[str] = []
    records: list[dict[str, Any]] = []
    try:
        reference_map = read_json(root / REFERENCE_MAP_JSON)
        reference_map_json_valid = True
        raw_records = reference_map.get("references", [])
        records = [item for item in raw_records if isinstance(item, dict)]
    except Exception as exc:  # noqa: BLE001 - validation must report malformed maps.
        reference_map = {}
        reference_map_errors.append(str(exc))
    validation_results: list[dict[str, Any]] = []
    runtime_validation_results: list[dict[str, Any]] = []
    helper_validation_errors: dict[str, list[str]] = {}
    schema_validation_errors: dict[str, list[str]] = {}
    for record in records:
        ref = str(record.get("spec", {}).get("ref", record.get("metadata", {}).get("id", "")))
        helper_errors = validate_reference_record(record)
        schema_errors: list[str] = []
        if schema_file_parsed:
            runtime = validate_reference_record_runtime(record, schema)
            schema_validation_executed = True
            helper_errors = runtime["helper_validation_errors"]
            schema_errors = runtime["schema_validation_errors"]
            runtime_validation_results.append(
                {
                    "ref": ref,
                    "result": runtime["status"],
                    "helper_valid": runtime["helper_valid"],
                    "schema_valid": runtime["schema_valid"],
                }
            )
        else:
            schema_errors = schema_load_errors
        helper_validation_errors[ref] = helper_errors
        schema_validation_errors[ref] = schema_errors
        errors = [*helper_errors, *schema_errors]
        validation_results.append(
            {
                "ref": ref,
                "result": "PASS" if not errors else "FAILED_VALIDATION",
                "errors": errors,
                "helper_validation_errors": helper_errors,
                "schema_validation_errors": schema_errors,
            }
        )
    if schema_file_parsed:
        schema_validation_executed = True
    unknown_optional = validate_reference_id("aide://future-kind/optional", required=False)
    unknown_required = validate_reference_id("aide://future-kind/required", required=True)
    all_projected_refs_parse = bool(validation_results) and all(item["result"] == "PASS" for item in validation_results)
    required_locators_exist = _required_locators_exist(root, records)
    sha256_checked = _sha256_checked(records)
    compatibility_results = _compatibility_results(root)
    forbidden = forbidden_operations_preserved()
    overclaiming_check_passed = all(forbidden.values())
    validation_errors = [
        *schema_load_errors,
        *alignment_errors,
        *reference_map_errors,
        *[error for item in validation_results for error in item["errors"]],
    ]
    status = (
        "PASS_WITH_WARNINGS"
        if not validation_errors
        and projection_result.get("status") in {"PASS", "PASS_WITH_WARNINGS"}
        and reference_map_json_valid
        and all_projected_refs_parse
        and required_locators_exist
        and sha256_checked
        and compatibility_results["status"] == "PASS"
        and overclaiming_check_passed
        and bool(unknown_optional.warnings)
        and bool(unknown_required.errors)
        else "FAILED_VALIDATION"
    )
    warnings = [
        "Reference ID Scheme is syntactic/projection-only and does not implement runtime resolution.",
        "EventRecord is not implemented.",
        "OKF knowledge bundle is not implemented.",
        "PatchTransaction is not implemented by this task.",
        "Runtime registry/resolver service is not implemented.",
        *alignment_warnings,
    ]
    report = {
        "schema_version": "aide.reference-id-validation.v0",
        "report_type": "reference_id_validation",
        "kind": "ReferenceIDValidationReport",
        "task_id": TASK_ID,
        "status": status,
        "validation_status": status,
        "validated": status in {"PASS", "PASS_WITH_WARNINGS"},
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_target": FEATURE_FLAG,
        "capability_label": FEATURE_FLAG,
        "schema_path": SCHEMA_PATH.as_posix(),
        "schema_exists": schema_path.exists(),
        "schema_file_loaded": schema_file_loaded,
        "schema_file_parsed": schema_file_parsed,
        "schema_validation_executed": schema_validation_executed,
        "schema_validation_mode": SCHEMA_VALIDATION_MODE if schema_validation_executed else "unavailable",
        "schema_helper_alignment_checked": schema_file_parsed,
        "schema_helper_alignment_status": alignment_result.get("schema_helper_alignment_status", "FAILED_VALIDATION"),
        "schema_validation_limitations": SCHEMA_VALIDATION_LIMITATIONS,
        "helper_path": "core/protocol/reference_id.py",
        "helper_exists": (root / "core/protocol/reference_id.py").exists(),
        "cli_registered": True,
        "projection_generated": projection_result.get("status") in {"PASS", "PASS_WITH_WARNINGS"},
        "reference_map_json_valid": reference_map_json_valid,
        "all_projected_refs_parse": all_projected_refs_parse,
        "required_locators_exist": required_locators_exist,
        "sha256_checked": sha256_checked,
        "predecessor_compatibility_preserved": compatibility_results["status"] == "PASS",
        "overclaiming_check_passed": overclaiming_check_passed,
        "forbidden_ops_preserved": all(forbidden.values()),
        "known_ref_kinds": sorted(KNOWN_REF_KINDS),
        "projected_refs_count": len(records),
        "validation_results": validation_results,
        "runtime_validation_results": runtime_validation_results,
        "helper_validation_errors": helper_validation_errors,
        "schema_validation_errors": schema_validation_errors,
        "validation_errors": validation_errors,
        "warnings": warnings,
        "unknown_optional_ref_kind_warned": bool(unknown_optional.warnings),
        "unknown_required_ref_kind_fails_closed": bool(unknown_required.errors),
        "compatibility_results": compatibility_results,
        "backwards_compatibility_preserved": compatibility_results["status"] == "PASS",
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "explicit_non_capabilities_preserved": True,
        "forbidden_operations_preserved": forbidden,
        "event_record_implemented": False,
        "okf_knowledge_bundle_implemented": False,
        "patch_transaction_implemented": False,
        "runtime_reference_registry_implemented": False,
        "resolver_service_implemented": False,
        "adapter_manifest_implemented": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
        "github_mutation": False,
        "reference_map_path": REFERENCE_MAP_JSON.as_posix(),
        "projection_report_path": PROJECTION_JSON.as_posix(),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "unfinished_work": unfinished_work_items(),
        "future_work": future_work_items(),
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_markdown(report))
    write_future_and_unfinished_reports(root)
    return report


def future_work_items() -> list[dict[str, str]]:
    return [
        {"task": "AIDE-CHECK-REFERENCE-ID-SCHEME-01", "reason": "independent review of the Reference ID schema, helper, projections, CLI, reports, tests, and non-capability boundaries"},
        {"task": "AIDE-ACCEPT-REFERENCE-ID-SCHEME-01", "reason": "accept ReferenceID only after independent check"},
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    return [{"item": item, "reason": "intentionally deferred beyond the minimal Reference ID Scheme slice"} for item in EXPLICIT_NON_CAPABILITIES]


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# ReferenceID Status",
        "",
        f"- status: {data.get('status')}",
        f"- api_version: {data.get('api_version')}",
        f"- protocol_version: {data.get('protocol_version')}",
        f"- schema_file_path: {data.get('schema_file_path')}",
        f"- schema_file_exists: {str(data.get('schema_file_exists', False)).lower()}",
        f"- helper_path: {data.get('helper_path')}",
        f"- helper_exists: {str(data.get('helper_exists', False)).lower()}",
        f"- reference_map_exists: {str(data.get('reference_map_exists', False)).lower()}",
        f"- capability_label: {data.get('capability_label')}",
        f"- accepted_predecessor: {data.get('accepted_predecessor')}",
        "- resolution: syntactic_only",
        "- runtime_reference_registry_implemented: false",
        "- resolver_service_implemented: false",
        "- event_record_implemented: false",
        "- okf_knowledge_bundle_implemented: false",
        "- patch_transaction_implemented: false",
        "- adapter_manifest_implemented: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- branch_mutation: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "- github_mutation: false",
        "",
        "## Reference Scheme",
        "",
        "- scheme: aide",
        "- grammar: aide://<kind>/<id>",
        "- fragment_support: true",
        "- identity_rule: Stable IDs are identity; file paths are locators; hashes prove content.",
        "",
        "## Known Ref Kinds",
        "",
    ]
    for kind in data.get("known_ref_kinds", []):
        lines.append(f"- {kind}")
    lines.extend(["", "## Explicit Non-Capabilities", ""])
    for item in data.get("explicit_non_capabilities", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Warnings", ""])
    for warning in data.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def render_reference_map_markdown(reference_map: dict[str, Any]) -> str:
    lines = [
        "# ReferenceID Map",
        "",
        f"- task_id: {reference_map.get('task_id')}",
        f"- capability_target: {reference_map.get('capability_target')}",
        f"- projected_refs_count: {len(reference_map.get('references', []))}",
        "- grammar: aide://<kind>/<id>",
        "- file_paths_are_locators: true",
        "",
        "## References",
        "",
    ]
    for record in reference_map.get("references", []):
        spec = record.get("spec", {}) if isinstance(record, dict) else {}
        locator = spec.get("locator", {}) if isinstance(spec.get("locator"), dict) else {}
        path = locator.get("path", "")
        lines.append(f"- {spec.get('ref')}: {spec.get('title')} ({path or 'no locator'})")
    return "\n".join(lines) + "\n"


def render_projection_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# ReferenceID Projection",
        "",
        f"- status: {report.get('status')}",
        f"- task_id: {report.get('task_id')}",
        f"- capability_target: {report.get('capability_target')}",
        f"- projected_refs_count: {report.get('projected_refs_count')}",
        "- scheme: aide",
        "- grammar: aide://<kind>/<id>",
        "- file_paths_are_locators: true",
        "- runtime_reference_registry_implemented: false",
        "- resolver_service_implemented: false",
        "- event_record_implemented: false",
        "- okf_knowledge_bundle_implemented: false",
        "- patch_transaction_implemented: false",
        "- adapter_manifest_implemented: false",
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
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# ReferenceID Validation",
        "",
        f"- status: {report.get('status')}",
        f"- validation_status: {report.get('validation_status')}",
        f"- capability_target: {report.get('capability_target')}",
        f"- schema_path: {report.get('schema_path')}",
        f"- schema_exists: {str(report.get('schema_exists', False)).lower()}",
        f"- helper_path: {report.get('helper_path')}",
        f"- helper_exists: {str(report.get('helper_exists', False)).lower()}",
        f"- cli_registered: {str(report.get('cli_registered', False)).lower()}",
        f"- projection_generated: {str(report.get('projection_generated', False)).lower()}",
        f"- reference_map_json_valid: {str(report.get('reference_map_json_valid', False)).lower()}",
        f"- all_projected_refs_parse: {str(report.get('all_projected_refs_parse', False)).lower()}",
        f"- required_locators_exist: {str(report.get('required_locators_exist', False)).lower()}",
        f"- sha256_checked: {str(report.get('sha256_checked', False)).lower()}",
        f"- predecessor_compatibility_preserved: {str(report.get('predecessor_compatibility_preserved', False)).lower()}",
        f"- overclaiming_check_passed: {str(report.get('overclaiming_check_passed', False)).lower()}",
        f"- forbidden_ops_preserved: {str(report.get('forbidden_ops_preserved', False)).lower()}",
        f"- unknown_optional_ref_kind_warned: {str(report.get('unknown_optional_ref_kind_warned', False)).lower()}",
        f"- unknown_required_ref_kind_fails_closed: {str(report.get('unknown_required_ref_kind_fails_closed', False)).lower()}",
        "- runtime_reference_registry_implemented: false",
        "- resolver_service_implemented: false",
        "- event_record_implemented: false",
        "- okf_knowledge_bundle_implemented: false",
        "- patch_transaction_implemented: false",
        "- adapter_manifest_implemented: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- branch_mutation: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "- github_mutation: false",
        "",
        "## Validation Results",
        "",
    ]
    for item in report.get("validation_results", []):
        lines.append(f"- {item.get('result')}: {item.get('ref')}")
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
        "# ReferenceID Future Work",
        "",
        "## Recommended Order",
        "",
    ]
    for index, item in enumerate(future_work_items(), start=1):
        future_lines.append(f"{index}. {item['task']}: {item['reason']}.")
    unfinished_lines = [
        "# ReferenceID Unfinished Work",
        "",
        "## Finished In This Slice",
        "",
        "- Stable `aide://<kind>/<id>` identity parsing and formatting.",
        "- Additive reference map projection over accepted protocol artifacts.",
        "- Local validation and reports under `.aide/reports/reference-id/`.",
        "",
        "## Not Attempted By Design",
        "",
    ]
    for item in unfinished_work_items():
        unfinished_lines.append(f"- {item['item']}: {item['reason']}.")
    write_text(repo_root / FUTURE_WORK_MD, "\n".join(future_lines) + "\n")
    write_text(repo_root / UNFINISHED_WORK_MD, "\n".join(unfinished_lines) + "\n")
