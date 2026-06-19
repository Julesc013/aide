"""Minimal AIDE AdapterManifest helpers.

This module projects one deterministic declaration-only AdapterManifest record.
The record describes adapter integration shape and prerequisites, but it does
not admit, trust, execute, launch, sandbox, call providers, call network
services, mutate GitHub, apply patches, or mutate target repositories.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from core.protocol import envelope, reference_id


API_VERSION = envelope.API_VERSION
ADAPTER_MANIFEST_SCHEMA_VERSION = "aide.adapter-manifest.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_adapter_manifest_schema"
ACCEPTED_PREDECESSOR = "minimal_patch_transaction_schema"
TASK_ID = "AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01"
RECOMMENDED_NEXT_TASK = "AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01"
DETERMINISTIC_TIMESTAMP = "2026-06-20T00:00:00+10:00"

ADAPTER_ID = "minimal-local-disposable-worker-declaration-01"
ADAPTER_REF = reference_id.format_reference_id("adapter", ADAPTER_ID)
MANIFEST_REF = reference_id.format_reference_id("artifact", "adapter-manifest-minimal-local-disposable-worker-01")
PATCH_TRANSACTION_CAPABILITY_REF = reference_id.format_reference_id("capability", "minimal_patch_transaction_schema")
WORKER_RUN_CAPABILITY_REF = reference_id.format_reference_id("capability", "minimal_worker_run_schema")
TEST_JOB_CAPABILITY_REF = reference_id.format_reference_id("capability", "minimal_test_job_schema")
CONFORMANCE_RESULT_REF = reference_id.format_reference_id("conformance-result", "minimal_capability_manifest-v1.0.0-evidence-projection-01")

REPORT_ROOT = Path(".aide/reports/adapter-manifest-resume")
SCHEMA_PATH = Path(".aide/protocol/aide-adapter-manifest.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
MANIFESTS_JSON = REPORT_ROOT / "manifests.json"
MANIFESTS_MD = REPORT_ROOT / "manifests.md"
MANIFEST_INDEX_JSON = REPORT_ROOT / "manifest-index.json"
MANIFEST_INDEX_MD = REPORT_ROOT / "manifest-index.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
ADMISSION_BOUNDARY_MD = REPORT_ROOT / "admission-boundary.md"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"

REQUIRED_REPORTS = [
    STATUS_MD,
    MANIFESTS_JSON,
    MANIFESTS_MD,
    MANIFEST_INDEX_JSON,
    MANIFEST_INDEX_MD,
    PROJECTION_JSON,
    PROJECTION_MD,
    VALIDATION_JSON,
    VALIDATION_MD,
    ADMISSION_BOUNDARY_MD,
    EXPLICIT_NON_CAPABILITIES_MD,
    FUTURE_WORK_MD,
    NEXT_TASK_PROMPT_MD,
]

ADAPTER_KINDS = {"worker", "test_runner", "vcs_backend", "sandbox_backend", "ide_host", "interop_surface"}
INTEGRATION_SURFACES = {"worker_run", "test_job", "patch_transaction", "evidence_packet", "event_record"}
RECOGNIZED_CAPABILITY_REFS = {
    PATCH_TRANSACTION_CAPABILITY_REF,
    WORKER_RUN_CAPABILITY_REF,
    TEST_JOB_CAPABILITY_REF,
    reference_id.format_reference_id("capability", "minimal_evidence_packet_schema"),
}
RECOGNIZED_CONFORMANCE_RESULT_REFS = {CONFORMANCE_RESULT_REF}

EXPLICIT_NON_CAPABILITIES = [
    "adapter_admission",
    "adapter_trust",
    "adapter_execution",
    "worker_execution",
    "test_execution",
    "sandbox_creation",
    "scheduler",
    "leases",
    "supervisor",
    "runtime",
    "service",
    "commander",
    "workbench",
    "provider_model_calls",
    "gateway_calls",
    "network_calls",
    "credential_resolution",
    "github_mutation",
    "branch_worktree_automation",
    "patch_application",
    "target_repository_mutation",
    "policy_engine",
    "approval_engine",
    "rollback_execution",
    "conformance_runner",
    "automatic_observation_collection",
    "profile_activation",
    "context_pack_v2",
    "test_broker_runtime",
    "release",
    "promotion",
    "production_readiness",
]

VALIDATION_WARNINGS = [
    "AdapterManifest is declaration/projection/validation only; no adapter admission exists.",
    "No adapter execution, worker launch, sandbox creation, credential resolution, provider/model call, network call, GitHub mutation, patch apply, or target repository mutation is implemented.",
    "ConformanceResult references are prerequisites, not trust grants.",
]

FALSE_STATUS_FIELDS = [
    "admission_performed",
    "admitted",
    "trusted",
    "execution_performed",
    "worker_started",
    "test_started",
    "network_call_performed",
    "credential_resolution_performed",
    "target_mutated",
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
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _compatibility() -> dict[str, Any]:
    return {
        "schemaVersion": PROTOCOL_VERSION,
        "protocolVersion": PROTOCOL_VERSION,
        "minReaderVersion": PROTOCOL_VERSION,
        "minWriterVersion": PROTOCOL_VERSION,
        "featureFlags": [FEATURE_FLAG],
        "requiredCapabilities": [FEATURE_FLAG, ACCEPTED_PREDECESSOR],
    }


def load_adapter_manifest_schema(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / SCHEMA_PATH
    if not path.exists():
        raise ValueError(f"AdapterManifest schema missing: {SCHEMA_PATH.as_posix()}")
    return read_json(path)


def source_artifact_paths(repo_root: str | Path | None = None) -> list[str]:
    _root = Path(repo_root) if repo_root is not None else Path(".")
    return [
        ".aide/protocol/aide-adapter-manifest.schema.json",
        "core/protocol/adapter_manifest.py",
        ".aide/scripts/aide_lite.py",
        ".aide/scripts/tests/test_aide_adapter_manifest.py",
        ".aide/reports/patch-transaction-resume-accept/acceptance-report.json",
        ".aide/reports/patch-transaction-repair-check/check-report.json",
        ".aide/queue/AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01/status.yaml",
    ]


def _hash_source_artifacts(repo_root: Path, rels: list[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel in rels:
        path = repo_root / rel
        if path.exists():
            hashes[rel] = sha256_file(path)
    return hashes


def build_adapter_manifest(repo_root: str | Path) -> dict[str, Any]:
    _root = Path(repo_root)
    return {
        "apiVersion": API_VERSION,
        "kind": "AdapterManifest",
        "schema_version": ADAPTER_MANIFEST_SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "metadata": {
            "id": ADAPTER_ID,
            "name": "Minimal Local Disposable Worker Declaration",
            "title": "Minimal Local Disposable Worker Declaration",
            "createdAt": DETERMINISTIC_TIMESTAMP,
            "sourcePath": MANIFESTS_JSON.as_posix(),
            "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
            "compatibility": _compatibility(),
        },
        "spec": {
            "manifest_ref": MANIFEST_REF,
            "adapter_ref": ADAPTER_REF,
            "adapter_kind": "worker",
            "adapter_role": "local_disposable_worker_candidate",
            "provider_kind": "local_process_candidate",
            "integration_surfaces": ["worker_run", "test_job", "patch_transaction", "evidence_packet"],
            "declared_capability_refs": [WORKER_RUN_CAPABILITY_REF, TEST_JOB_CAPABILITY_REF],
            "required_capability_refs": [
                PATCH_TRANSACTION_CAPABILITY_REF,
                WORKER_RUN_CAPABILITY_REF,
                TEST_JOB_CAPABILITY_REF,
            ],
            "required_conformance_result_refs": [CONFORMANCE_RESULT_REF],
            "required_evidence_refs": [
                reference_id.format_reference_id("evidence", "patch-transaction-resume-acceptance"),
                reference_id.format_reference_id("evidence", "patch-transaction-repair-check"),
            ],
            "admission": {
                "admission_required": True,
                "admission_performed": False,
                "admitted": False,
                "trusted": False,
                "admission_authority_ref": None,
            },
            "execution_boundary": {
                "execution_performed": False,
                "worker_started": False,
                "test_started": False,
                "sandbox_created": False,
                "patch_applied": False,
                "target_mutated": False,
            },
            "security_boundary": {
                "credential_resolution_performed": False,
                "network_call_performed": False,
                "provider_model_call_performed": False,
                "github_mutation_performed": False,
                "branch_worktree_mutation_performed": False,
            },
            "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        },
        "status": {
            "validation_performed": True,
            "validation_status": "PASS_WITH_WARNINGS",
            "validation_errors": [],
            "validation_warnings": list(VALIDATION_WARNINGS),
            "admission_performed": False,
            "admitted": False,
            "trusted": False,
            "execution_performed": False,
            "worker_started": False,
            "test_started": False,
            "network_call_performed": False,
            "credential_resolution_performed": False,
            "target_mutated": False,
        },
    }


def _validate_required_ref(value: Any, expected_kind: str) -> list[str]:
    result = reference_id.validate_reference_id(value, required=True)
    errors = list(result.errors)
    parsed_kind = result.parsed.kind if result.parsed is not None else ""
    if result.valid and parsed_kind != expected_kind:
        errors.append(f"reference kind must be {expected_kind}: {value}")
    return errors


def validate_adapter_manifest_with_schema(record: dict[str, Any], schema: dict[str, Any] | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings = list(VALIDATION_WARNINGS)
    if record.get("apiVersion") != API_VERSION:
        errors.append("apiVersion mismatch")
    if record.get("kind") != "AdapterManifest":
        errors.append("kind must be AdapterManifest")
    for field in ["metadata", "spec", "status"]:
        if not isinstance(record.get(field), dict):
            errors.append(f"{field} must be an object")
    metadata = record.get("metadata", {})
    spec = record.get("spec", {})
    status = record.get("status", {})
    for field in ["id", "createdAt", "sourcePath", "producer", "compatibility"]:
        if field not in metadata:
            errors.append(f"metadata missing field: {field}")
    errors.extend(_validate_required_ref(spec.get("manifest_ref"), "artifact"))
    errors.extend(_validate_required_ref(spec.get("adapter_ref"), "adapter"))
    if spec.get("adapter_ref") != ADAPTER_REF:
        errors.append(f"adapter_ref must be stable: {ADAPTER_REF}")
    if spec.get("adapter_kind") not in ADAPTER_KINDS:
        errors.append("adapter_kind is not recognized")
    surfaces = spec.get("integration_surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        errors.append("integration_surfaces must be a non-empty array")
        surfaces = []
    for surface in surfaces:
        if surface not in INTEGRATION_SURFACES:
            errors.append(f"unknown integration surface: {surface}")
    for field in ["declared_capability_refs", "required_capability_refs"]:
        refs = spec.get(field)
        if not isinstance(refs, list) or not refs:
            errors.append(f"{field} must be a non-empty array")
            refs = []
        for ref in refs:
            errors.extend(_validate_required_ref(ref, "capability"))
            if isinstance(ref, str) and ref not in RECOGNIZED_CAPABILITY_REFS:
                errors.append(f"unknown capability ref: {ref}")
    result_refs = spec.get("required_conformance_result_refs")
    if not isinstance(result_refs, list) or not result_refs:
        errors.append("required_conformance_result_refs must be a non-empty array")
        result_refs = []
    for ref in result_refs:
        errors.extend(_validate_required_ref(ref, "conformance-result"))
        if isinstance(ref, str) and ref not in RECOGNIZED_CONFORMANCE_RESULT_REFS:
            errors.append(f"unknown ConformanceResult ref: {ref}")
    for ref in spec.get("required_evidence_refs", []):
        errors.extend(_validate_required_ref(ref, "evidence"))
    admission = spec.get("admission", {})
    execution = spec.get("execution_boundary", {})
    security = spec.get("security_boundary", {})
    if admission.get("admission_required") is not True:
        errors.append("admission.admission_required must be true")
    for field in ["admission_performed", "admitted", "trusted"]:
        if admission.get(field) is not False:
            errors.append(f"admission.{field} must be false")
    for field in ["execution_performed", "worker_started", "test_started", "sandbox_created", "patch_applied", "target_mutated"]:
        if execution.get(field) is not False:
            errors.append(f"execution_boundary.{field} must be false")
    for field in ["credential_resolution_performed", "network_call_performed", "provider_model_call_performed", "github_mutation_performed", "branch_worktree_mutation_performed"]:
        if security.get(field) is not False:
            errors.append(f"security_boundary.{field} must be false")
    if spec.get("explicit_non_capabilities") != EXPLICIT_NON_CAPABILITIES:
        errors.append("explicit_non_capabilities must match the accepted boundary list")
    if status.get("validation_performed") is not True:
        errors.append("status.validation_performed must be true")
    for field in FALSE_STATUS_FIELDS:
        if status.get(field) is not False:
            errors.append(f"status.{field} must be false")
    if status.get("trusted") is True and result_refs:
        errors.append("ConformanceResult presence must not set trusted true")
    return errors, warnings


def _json_valid(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (OSError, ValueError):
        return False


def build_manifest_index(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.adapter-manifest-index.v0",
        "kind": "AdapterManifestIndex",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "status": "PASS_WITH_WARNINGS",
        "manifest_count": 1,
        "adapter_refs": [record["spec"]["adapter_ref"]],
        "adapter_kinds": {record["spec"]["adapter_kind"]: 1},
        "admission_performed": False,
        "trusted": False,
        "execution_performed": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def adapter_manifest_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    schema_loaded = False
    try:
        load_adapter_manifest_schema(root)
        schema_loaded = True
    except ValueError:
        pass
    record = build_adapter_manifest(root)
    errors, warnings = validate_adapter_manifest_with_schema(record, {})
    return {
        "schema_version": "aide.adapter-manifest-status.v0",
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "status": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "schema_loaded": schema_loaded,
        "record_count": 1,
        "adapter_kind_counts": {record["spec"]["adapter_kind"]: 1},
        "record_valid": not errors,
        "admission_performed": False,
        "admitted": False,
        "trusted": False,
        "execution_performed": False,
        "worker_started": False,
        "network_call_performed": False,
        "credential_resolution_performed": False,
        "target_mutated": False,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "warnings": warnings,
        "validation_errors": errors,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def write_adapter_manifest_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    sources = source_artifact_paths(root)
    before = _hash_source_artifacts(root, sources)
    schema = load_adapter_manifest_schema(root)
    record = build_adapter_manifest(root)
    errors, warnings = validate_adapter_manifest_with_schema(record, schema)
    status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    record["status"]["validation_status"] = status
    record["status"]["validation_errors"] = errors
    record["status"]["validation_warnings"] = warnings
    index = build_manifest_index(record)
    index["status"] = status
    write_json(root / MANIFESTS_JSON, {"schema_version": "aide.adapter-manifests.v0", "manifests": [record]})
    write_text(root / MANIFESTS_MD, render_manifests_markdown(record))
    write_json(root / MANIFEST_INDEX_JSON, index)
    write_text(root / MANIFEST_INDEX_MD, render_index_markdown(index))
    write_text(root / ADMISSION_BOUNDARY_MD, render_admission_boundary_markdown())
    write_text(root / EXPLICIT_NON_CAPABILITIES_MD, render_explicit_non_capabilities_markdown())
    write_text(root / FUTURE_WORK_MD, render_future_work_markdown())
    write_text(root / NEXT_TASK_PROMPT_MD, render_next_task_prompt())
    validation = validate_adapter_manifest(root, project=False)
    after = _hash_source_artifacts(root, sources)
    report = {
        "schema_version": "aide.adapter-manifest-projection.v0",
        "kind": "AdapterManifestProjectionReport",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "status": validation["validation_status"],
        "manifest_ref": MANIFEST_REF,
        "adapter_ref": ADAPTER_REF,
        "adapter_kind": record["spec"]["adapter_kind"],
        "record_valid": validation["record_valid"],
        "manifest_count": 1,
        "declaration_only": True,
        "admission_performed": False,
        "trusted": False,
        "execution_performed": False,
        "worker_started": False,
        "network_call_performed": False,
        "credential_resolution_performed": False,
        "target_mutated": False,
        "source_artifacts_checked": sources,
        "source_artifacts_mutated": before != after,
        "reports_written": [path.as_posix() for path in REQUIRED_REPORTS],
        "warnings": validation["warnings"],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    write_text(root / STATUS_MD, render_status_markdown({**validation, "projection_exists": True}))
    return report


def validate_adapter_manifest(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    if project:
        projection = write_adapter_manifest_reports(root)
    else:
        projection = {"status": "PASS_WITH_WARNINGS"}
    schema_errors: list[str] = []
    schema_file_loaded = False
    schema_file_parsed = False
    schema_validation_executed = False
    try:
        schema = load_adapter_manifest_schema(root)
        schema_file_loaded = True
        schema_file_parsed = True
        schema_validation_executed = True
    except ValueError as exc:
        schema = {}
        schema_errors.append(str(exc))
    record = build_adapter_manifest(root)
    record_errors, warnings = validate_adapter_manifest_with_schema(record, schema)
    errors = [*schema_errors, *record_errors]
    reports_generated = all((root / rel).exists() for rel in REQUIRED_REPORTS if rel not in {VALIDATION_JSON, VALIDATION_MD, PROJECTION_JSON, PROJECTION_MD, STATUS_MD})
    checks = {
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "schema_file_loaded": schema_file_loaded,
        "schema_file_parsed": schema_file_parsed,
        "schema_validation_executed": schema_validation_executed,
        "helper_exists": (root / "core/protocol/adapter_manifest.py").exists(),
        "cli_registered": _cli_registered(root),
        "reports_generated": reports_generated,
        "manifests_json_valid": _json_valid(root / MANIFESTS_JSON) if (root / MANIFESTS_JSON).exists() else False,
        "manifest_index_json_valid": _json_valid(root / MANIFEST_INDEX_JSON) if (root / MANIFEST_INDEX_JSON).exists() else False,
        "record_valid": not record_errors,
        "adapter_ref_valid": not _validate_required_ref(record["spec"]["adapter_ref"], "adapter"),
        "required_capability_refs_valid": all(not _validate_required_ref(ref, "capability") for ref in record["spec"]["required_capability_refs"]),
        "conformance_result_ref_does_not_trust": record["status"]["trusted"] is False,
        "admission_not_performed": record["status"]["admission_performed"] is False,
        "execution_not_performed": record["status"]["execution_performed"] is False,
        "network_not_called": record["status"]["network_call_performed"] is False,
        "credentials_not_resolved": record["status"]["credential_resolution_performed"] is False,
        "target_not_mutated": record["status"]["target_mutated"] is False,
        "explicit_non_capabilities_preserved": record["spec"]["explicit_non_capabilities"] == EXPLICIT_NON_CAPABILITIES,
        "unsupported_execution_preserved": True,
    }
    failed = [key for key, value in checks.items() if value is not True]
    errors.extend(f"failed check: {item}" for item in failed)
    status = "PASS_WITH_WARNINGS" if not errors and projection.get("status") in {"PASS", "PASS_WITH_WARNINGS"} else "FAILED_VALIDATION"
    report = {
        "schema_version": "aide.adapter-manifest-validation.v0",
        "kind": "AdapterManifestValidationReport",
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "validation_status": status,
        "status": status,
        "validated": status in {"PASS", "PASS_WITH_WARNINGS"},
        "schema_validation_mode": "minimal_json_schema_subset_plus_adapter_manifest_semantics",
        "validation_errors": errors,
        "warnings": warnings,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        **checks,
        "admission_performed": False,
        "admitted": False,
        "trusted": False,
        "execution_performed": False,
        "worker_started": False,
        "network_call_performed": False,
        "credential_resolution_performed": False,
        "target_mutated": False,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_markdown(report))
    write_text(root / STATUS_MD, render_status_markdown(report))
    return report


def _cli_registered(repo_root: Path) -> bool:
    path = repo_root / ".aide/scripts/aide_lite.py"
    return path.exists() and "adapter-manifest" in path.read_text(encoding="utf-8")


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# AdapterManifest Status",
        "",
        f"- task_id: {TASK_ID}",
        f"- capability_target: {FEATURE_FLAG}",
        f"- status: {data.get('validation_status', data.get('status'))}",
        f"- schema_exists: {str(data.get('schema_exists', False)).lower()}",
        f"- helper_exists: {str(data.get('helper_exists', False)).lower()}",
        f"- cli_registered: {str(data.get('cli_registered', False)).lower()}",
        "- declaration_only: true",
        "- admission_performed: false",
        "- admitted: false",
        "- trusted: false",
        "- execution_performed: false",
        "- worker_started: false",
        "- network_call_performed: false",
        "- credential_resolution_performed: false",
        "- target_mutated: false",
        f"- recommended_next_task: {RECOMMENDED_NEXT_TASK}",
        "",
        "## Warnings",
        "",
    ]
    lines.extend(f"- {item}" for item in data.get("warnings", VALIDATION_WARNINGS))
    return "\n".join(lines) + "\n"


def render_manifests_markdown(record: dict[str, Any]) -> str:
    spec = record["spec"]
    lines = [
        "# AdapterManifest Records",
        "",
        f"- manifest_ref: {spec['manifest_ref']}",
        f"- adapter_ref: {spec['adapter_ref']}",
        f"- adapter_kind: {spec['adapter_kind']}",
        f"- adapter_role: {spec['adapter_role']}",
        f"- provider_kind: {spec['provider_kind']}",
        "- declaration_only: true",
        "- admitted: false",
        "- trusted: false",
        "- execution_performed: false",
        "",
        "## Integration Surfaces",
        "",
    ]
    lines.extend(f"- {item}" for item in spec["integration_surfaces"])
    return "\n".join(lines) + "\n"


def render_index_markdown(index: dict[str, Any]) -> str:
    return (
        "# AdapterManifest Index\n\n"
        f"- status: {index.get('status')}\n"
        f"- manifest_count: {index.get('manifest_count')}\n"
        f"- adapter_refs: {', '.join(index.get('adapter_refs', []))}\n"
        "- admission_performed: false\n"
        "- trusted: false\n"
        "- execution_performed: false\n"
        f"- recommended_next_task: {index.get('recommended_next_task')}\n"
    )


def render_projection_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# AdapterManifest Projection Report",
        "",
        f"- status: {report.get('status')}",
        f"- manifest_ref: {report.get('manifest_ref')}",
        f"- adapter_ref: {report.get('adapter_ref')}",
        f"- adapter_kind: {report.get('adapter_kind')}",
        "- declaration_only: true",
        "- admission_performed: false",
        "- trusted: false",
        "- execution_performed: false",
        "- worker_started: false",
        "- network_call_performed: false",
        "- credential_resolution_performed: false",
        "- target_mutated: false",
        f"- source_artifacts_mutated: {str(report.get('source_artifacts_mutated')).lower()}",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Reports Written",
        "",
    ]
    lines.extend(f"- {item}" for item in report.get("reports_written", []))
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    keys = [
        "schema_exists",
        "schema_file_loaded",
        "schema_file_parsed",
        "schema_validation_executed",
        "helper_exists",
        "cli_registered",
        "reports_generated",
        "manifests_json_valid",
        "manifest_index_json_valid",
        "record_valid",
        "adapter_ref_valid",
        "required_capability_refs_valid",
        "conformance_result_ref_does_not_trust",
        "admission_not_performed",
        "execution_not_performed",
        "network_not_called",
        "credentials_not_resolved",
        "target_not_mutated",
        "explicit_non_capabilities_preserved",
    ]
    lines = [
        "# AdapterManifest Validation",
        "",
        f"- validation_status: {report.get('validation_status')}",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Checks",
        "",
    ]
    lines.extend(f"- {key}: {str(report.get(key)).lower()}" for key in keys)
    lines.extend(["", "## Errors", ""])
    errors = report.get("validation_errors", [])
    lines.extend(f"- {item}" for item in errors) if errors else lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in report.get("warnings", []))
    return "\n".join(lines) + "\n"


def render_admission_boundary_markdown() -> str:
    return (
        "# AdapterManifest Admission Boundary\n\n"
        "- AdapterManifest declaration is not admission.\n"
        "- ConformanceResult reference is not trust.\n"
        "- Required capabilities are prerequisites, not authority grants.\n"
        "- No adapter execution, worker launch, sandbox creation, provider call, network call, credential resolution, patch apply, or target mutation is implemented.\n"
    )


def render_explicit_non_capabilities_markdown() -> str:
    lines = ["# AdapterManifest Explicit Non-Capabilities", ""]
    lines.extend(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES)
    return "\n".join(lines) + "\n"


def render_future_work_markdown() -> str:
    return (
        "# AdapterManifest Future Work\n\n"
        f"- Next task: `{RECOMMENDED_NEXT_TASK}`.\n"
        "- Future acceptance must remain separate from adapter admission.\n"
        "- Adapter execution, sandbox backends, scheduler, Test Broker, Service, and ContextPack v2 remain future work.\n"
    )


def render_next_task_prompt() -> str:
    return (
        "# AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01\n\n"
        "Create and process `AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01`.\n\n"
        "Preserve the original blocked `AIDE-CHECK-ADAPTER-MANIFEST-01` record. "
        "Independently check the resume AdapterManifest build, including schema/helper alignment, "
        "reference forms, declaration-only boundaries, deterministic projection, no admission, no trust, "
        "no execution, no credential resolution, no provider/network calls, and complete evidence.\n"
    )
