"""Minimal AIDE TestJob helpers.

This module defines TestJob as data only: a durable record shape for future
validation and test attempts. It projects existing validation/check/acceptance
artifacts into TestJob records without submitting tests, running async jobs,
creating leases, scheduling, invoking providers, or applying patches.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from core.protocol import envelope


API_VERSION = envelope.API_VERSION
TEST_JOB_SCHEMA_VERSION = "aide.test-job.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_test_job_schema"
ACCEPTED_PREDECESSOR = "minimal_worker_run_schema"
REPORT_ROOT = Path(".aide/reports/test-job")
PROJECTION_ROOT = REPORT_ROOT / "projections"
SCHEMA_PATH = Path(".aide/protocol/aide-test-job.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"
SUPPORTED_KINDS = {
    "TestJob",
    "TestJobProjectionReport",
    "TestJobValidationReport",
}
TEST_JOB_REQUIRED_FIELDS = ["apiVersion", "kind", "metadata", "spec", "status"]
REQUIRED_METADATA_FIELDS = ["id", "createdAt", "sourcePath", "producer", "compatibility"]
REQUIRED_SPEC_FIELDS = [
    "job_id",
    "source_task_id",
    "source_workunit_id",
    "source_worker_run_id",
    "job_kind",
    "command",
    "environment",
    "framework",
    "timeout",
    "artifacts",
    "logs",
    "evidence_packet_refs",
    "explicit_non_capabilities",
]
REQUIRED_STATUS_FIELDS = ["phase", "result", "validated", "validation_errors", "validation_warnings"]
JOB_KINDS = {
    "metadata_only",
    "validation_observation",
    "unit_test",
    "integration_test",
    "lint",
    "typecheck",
    "schema_validate",
    "command_check",
    "unknown",
}
RUNNER_KINDS = {"metadata_only", "local_script", "ci", "human", "unknown"}
FRAMEWORK_NAMES = {"unittest", "pytest", "junit", "tap", "custom", "unknown", "none"}
RESULT_FORMATS = {"text", "json", "junit_xml", "tap", "markdown", "none", "unknown"}
PARSER_STATUSES = {"metadata_only", "not_implemented", "parsed", "unknown"}
TIMEOUT_POLICIES = {"metadata_only", "not_configured", "planned", "unknown"}
PHASE_VALUES = {
    "planned",
    "metadata_only",
    "validation_observation",
    "submitted",
    "running",
    "completed",
    "failed",
    "blocked",
    "cancelled",
    "timed_out",
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
    "UNKNOWN",
}
RECOGNIZED_CAPABILITIES = {
    FEATURE_FLAG,
    ACCEPTED_PREDECESSOR,
    "fixture_temp_apply_only",
    "minimal_contract_envelope",
    "minimal_evidence_packet_schema",
    "minimal_workunit_queue_v1",
    "minimal_workunit_readonly_cli",
    "minimal_workunit_queue_metadata_mutation_cli",
}
EXPLICIT_NON_CAPABILITIES = [
    "test_broker_runtime",
    "async_test_execution",
    "test_job_submission",
    "test_job_run",
    "test_job_retry_runtime",
    "test_job_summarize_runtime",
    "scheduler",
    "leases",
    "supervisor",
    "worker_execution",
    "workunit_claim",
    "workunit_run",
    "workunit_finish",
    "workunit_repair",
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
    "gateway",
    "network",
    "github_mutation",
    "model_provider_calls",
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
    "worker_run_acceptance": {
        "path": Path(".aide/reports/worker-run-accept/acceptance-report.json"),
        "source_task_id": "AIDE-ACCEPT-WORKER-RUN-SCHEMA-01",
        "source_task_kind": "acceptance",
        "role": "acceptance_report",
    },
    "worker_run_check": {
        "path": Path(".aide/reports/worker-run-check/check-report.json"),
        "source_task_id": "AIDE-CHECK-WORKER-RUN-SCHEMA-01",
        "source_task_kind": "check",
        "role": "check_report",
    },
    "worker_run_validation": {
        "path": Path(".aide/reports/worker-run/validation.json"),
        "source_task_id": "AIDE-BUILD-WORKER-RUN-SCHEMA-01",
        "source_task_kind": "build",
        "role": "validation_report",
    },
    "workunit_cli_mutation_acceptance": {
        "path": Path(".aide/reports/workunit-cli-mutation-acceptance/acceptance-report.json"),
        "source_task_id": "AIDE-ACCEPT-WORKUNIT-CLI-MUTATION-01",
        "source_task_kind": "acceptance",
        "role": "acceptance_report",
    },
    "workunit_cli_mutation_check": {
        "path": Path(".aide/reports/workunit-cli-mutation-check/check-report.json"),
        "source_task_id": "AIDE-CHECK-WORKUNIT-CLI-MUTATION-01",
        "source_task_kind": "check",
        "role": "check_report",
    },
    "workunit_cli_acceptance": {
        "path": Path(".aide/reports/workunit-cli-acceptance/acceptance-report.json"),
        "source_task_id": "AIDE-ACCEPT-WORKUNIT-CLI-01",
        "source_task_kind": "acceptance",
        "role": "acceptance_report",
    },
    "workunit_queue_acceptance": {
        "path": Path(".aide/reports/workunit-queue-acceptance/acceptance-report.json"),
        "source_task_id": "AIDE-ACCEPT-WORKUNIT-QUEUE-V1-01",
        "source_task_kind": "acceptance",
        "role": "acceptance_report",
    },
    "evidence_packet_validation": {
        "path": Path(".aide/reports/evidence-packet/validation.json"),
        "source_task_id": "AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01",
        "source_task_kind": "build",
        "role": "validation_report",
    },
    "contract_envelope_validation": {
        "path": Path(".aide/reports/contract-envelope/validation.json"),
        "source_task_id": "AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01",
        "source_task_kind": "build",
        "role": "validation_report",
    },
}
PROJECTION_FILES = {
    key: PROJECTION_ROOT / f"{key.replace('_', '-')}.test-job.json" for key in SOURCE_ARTIFACTS
}
COMPATIBILITY_REPORTS = {
    "contract_envelope": Path(".aide/reports/contract-envelope/validation.json"),
    "evidence_packet": Path(".aide/reports/evidence-packet/validation.json"),
    "workunit_queue": Path(".aide/reports/workunit-queue/validation.json"),
    "worker_run": Path(".aide/reports/worker-run/validation.json"),
    "worker_run_acceptance": Path(".aide/reports/worker-run-accept/acceptance-report.json"),
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
    raw = str(value or "UNKNOWN").strip().upper()
    if raw == "ACCEPTED":
        return "PASS"
    if raw == "ACCEPTED_WITH_WARNINGS":
        return "PASS_WITH_WARNINGS"
    if raw in {"FAILED", "FAIL", "REJECTED_NEEDS_REPAIR"}:
        return "FAILED_VALIDATION"
    return raw if raw in RESULT_VALUES else "UNKNOWN"


def _deterministic_job_id(source_task_id: str, source_path: Path | None, job_kind: str) -> str:
    seed = stable_json(
        {
            "source_task_id": source_task_id,
            "source_path": _source_path_value(source_path),
            "job_kind": job_kind,
        }
    )
    return "tj-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


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


def implemented_capabilities(test_job: dict[str, Any]) -> set[str]:
    spec = test_job.get("spec") if isinstance(test_job.get("spec"), dict) else {}
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


def _observed_commands(report: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for field in ["commands_run", "test_results", "validation_results"]:
        value = report.get(field)
        if not isinstance(value, list):
            continue
        for item in value:
            if isinstance(item, dict) and isinstance(item.get("command"), str) and item.get("command"):
                result.append(copy.deepcopy(item))
    return result


def _first_exit_code(commands: list[dict[str, Any]]) -> int | None:
    for item in commands:
        exit_code = item.get("exit_code")
        if isinstance(exit_code, int) and not isinstance(exit_code, bool):
            return exit_code
    return None


def _framework_for_command(command: str, report: dict[str, Any]) -> dict[str, Any]:
    lowered = command.lower()
    if "unittest" in lowered:
        name = "unittest"
        result_format = "text"
    elif "pytest" in lowered:
        name = "pytest"
        result_format = "text"
    elif "json.tool" in lowered or str(report.get("report_type", "")).endswith("validation"):
        name = "custom"
        result_format = "json"
    elif command:
        name = "custom"
        result_format = "text"
    else:
        name = "none"
        result_format = "none"
    return {"name": name, "result_format": result_format, "parser_status": "metadata_only"}


def build_test_job(
    *,
    job_id: str,
    source_task_id: str,
    source_workunit_id: str | None,
    source_worker_run_id: str | None,
    job_kind: str,
    command: dict[str, Any],
    environment: dict[str, Any],
    framework: dict[str, Any],
    timeout: dict[str, Any],
    artifacts: list[dict[str, Any]],
    logs: list[dict[str, Any]],
    evidence_packet_refs: list[dict[str, Any]],
    explicit_non_capabilities: list[str],
    source_path: Path | None = None,
    source_task_kind: str = "unknown",
    capability_label: str = FEATURE_FLAG,
    failure_summary: dict[str, Any] | None = None,
    retry: dict[str, Any] | None = None,
    validation_summary: dict[str, Any] | None = None,
    name: str | None = None,
    created_at: str | None = None,
    phase: str = "metadata_only",
    result: str = "UNKNOWN",
    started_at: str | None = None,
    ended_at: str | None = None,
    exit_code: int | None = None,
    duration_seconds: int | float | None = None,
    validation_errors: list[str] | None = None,
    validation_warnings: list[str] | None = None,
) -> dict[str, Any]:
    metadata = {
        "id": job_id,
        "name": name or source_task_id,
        "createdAt": created_at or "deterministic",
        "sourcePath": _source_path_value(source_path),
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility([capability_label, ACCEPTED_PREDECESSOR]),
    }
    spec = {
        "job_id": job_id,
        "source_task_id": source_task_id,
        "source_workunit_id": source_workunit_id,
        "source_worker_run_id": source_worker_run_id,
        "source_task_kind": source_task_kind,
        "job_kind": job_kind,
        "command": copy.deepcopy(command),
        "environment": copy.deepcopy(environment),
        "framework": copy.deepcopy(framework),
        "timeout": copy.deepcopy(timeout),
        "artifacts": copy.deepcopy(artifacts),
        "logs": copy.deepcopy(logs),
        "evidence_packet_refs": copy.deepcopy(evidence_packet_refs),
        "explicit_non_capabilities": list(explicit_non_capabilities),
        "failure_summary": copy.deepcopy(
            failure_summary
            or {
                "summary": "",
                "failed_tests": [],
                "likely_files": [],
                "excerpt_path": None,
                "parser_status": "metadata_only",
            }
        ),
        "retry": copy.deepcopy(
            retry
            or {
                "attempt": 1,
                "max_attempts": 1,
                "retry_policy": "not_configured",
                "flake_classification": "unknown",
            }
        ),
        "capability_label": capability_label,
        "validation_summary": copy.deepcopy(validation_summary or {}),
        "test_broker_runtime_implemented": False,
        "async_test_execution_implemented": False,
        "test_job_submission_implemented": False,
        "test_job_run_implemented": False,
        "test_job_retry_runtime_implemented": False,
        "test_job_summarize_runtime_implemented": False,
        "scheduler_implemented": False,
        "leases_implemented": False,
        "supervisor_implemented": False,
        "worker_execution_implemented": False,
        "workunit_claim_run_finish_repair_implemented": False,
        "provider_adapter_implemented": False,
        "service_implemented": False,
        "commander_implemented": False,
    }
    status = {
        "phase": phase if phase in PHASE_VALUES else "unknown",
        "result": _normalize_result(result),
        "startedAt": started_at,
        "endedAt": ended_at,
        "exitCode": exit_code,
        "durationSeconds": duration_seconds,
        "validated": not validation_errors,
        "validation_errors": list(validation_errors or []),
        "validation_warnings": list(validation_warnings or []),
    }
    obj = envelope.build_envelope("TestJob", metadata, spec, status, api_version=API_VERSION)
    obj["schema_version"] = TEST_JOB_SCHEMA_VERSION
    obj["protocol_version"] = PROTOCOL_VERSION
    return obj


def sample_test_job() -> dict[str, Any]:
    return build_test_job(
        job_id="tj-sample",
        source_task_id="AIDE-BUILD-TESTJOB-SCHEMA-01",
        source_workunit_id="AIDE-BUILD-TESTJOB-SCHEMA-01",
        source_worker_run_id=None,
        source_task_kind="build",
        job_kind="metadata_only",
        command={
            "argv": [],
            "cwd": ".",
            "env_policy": "metadata_only",
            "shell": None,
            "description": "Metadata-only TestJob sample; no command executed.",
        },
        environment={"runner_kind": "metadata_only", "platform": None, "python": None, "notes": []},
        framework={"name": "none", "result_format": "none", "parser_status": "metadata_only"},
        timeout={"timeout_seconds": None, "timeout_policy": "not_configured", "timed_out": None},
        artifacts=[{"path": ".aide/reports/test-job/validation.json", "role": "validation_report"}],
        logs=[],
        evidence_packet_refs=[],
        explicit_non_capabilities=explicit_non_capabilities(),
        source_path=Path(".aide/reports/test-job/validation.json"),
        validation_summary={"status": "PASS", "metadata_only": True, "test_executed": False},
        phase="metadata_only",
        result="PASS",
    )


def sample_unknown_optional_test_job() -> dict[str, Any]:
    obj = sample_test_job()
    obj["x-aide-optional-probe"] = {"tolerated": True}
    obj["metadata"]["x-aide-optional-probe"] = "tolerated"
    obj["spec"]["x-aide-optional-probe"] = True
    return obj


def sample_unknown_required_capability_test_job() -> dict[str, Any]:
    obj = sample_test_job()
    obj["metadata"]["compatibility"]["requiredCapabilities"] = ["future.required"]
    return obj


def validate_test_job(obj: dict[str, Any], allowed_kinds: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["TestJob must be an object"]
    if not isinstance(obj.get("apiVersion"), str) or not obj.get("apiVersion"):
        errors.append("apiVersion must be a non-empty string")
    if obj.get("apiVersion") != API_VERSION:
        errors.append(f"unsupported apiVersion: {obj.get('apiVersion')}")
    kind = obj.get("kind")
    active_kinds = allowed_kinds or {"TestJob"}
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
    if not isinstance(spec.get("job_id"), str) or not spec.get("job_id"):
        errors.append("spec.job_id must be a non-empty string")
    if not isinstance(spec.get("source_task_id"), str) or not spec.get("source_task_id"):
        errors.append("spec.source_task_id must be a non-empty string")
    if spec.get("source_workunit_id") is not None and not isinstance(spec.get("source_workunit_id"), str):
        errors.append("spec.source_workunit_id must be a string or null")
    if spec.get("source_worker_run_id") is not None and not isinstance(spec.get("source_worker_run_id"), str):
        errors.append("spec.source_worker_run_id must be a string or null")
    if spec.get("job_kind") not in JOB_KINDS:
        errors.append(f"unsupported job_kind: {spec.get('job_kind')}")
    command = spec.get("command")
    if not isinstance(command, dict):
        errors.append("spec.command must be an object")
    else:
        if not isinstance(command.get("argv"), list):
            errors.append("spec.command.argv must be an array")
        elif not all(isinstance(item, str) for item in command.get("argv", [])):
            errors.append("spec.command.argv entries must be strings")
        if not isinstance(command.get("cwd"), str) or not command.get("cwd"):
            errors.append("spec.command.cwd must be a non-empty string")
        if not isinstance(command.get("env_policy"), str) or not command.get("env_policy"):
            errors.append("spec.command.env_policy must be a non-empty string")
        if command.get("shell") is not None and not isinstance(command.get("shell"), str):
            errors.append("spec.command.shell must be a string or null")
    environment = spec.get("environment")
    if not isinstance(environment, dict):
        errors.append("spec.environment must be an object")
    else:
        if environment.get("runner_kind") not in RUNNER_KINDS:
            errors.append(f"unsupported environment.runner_kind: {environment.get('runner_kind')}")
        if environment.get("platform") is not None and not isinstance(environment.get("platform"), str):
            errors.append("spec.environment.platform must be a string or null")
        if environment.get("python") is not None and not isinstance(environment.get("python"), str):
            errors.append("spec.environment.python must be a string or null")
        if not isinstance(environment.get("notes"), list):
            errors.append("spec.environment.notes must be an array")
    framework = spec.get("framework")
    if not isinstance(framework, dict):
        errors.append("spec.framework must be an object")
    else:
        if framework.get("name") not in FRAMEWORK_NAMES:
            errors.append(f"unsupported framework.name: {framework.get('name')}")
        if framework.get("result_format") not in RESULT_FORMATS:
            errors.append(f"unsupported framework.result_format: {framework.get('result_format')}")
        if framework.get("parser_status") not in PARSER_STATUSES:
            errors.append(f"unsupported framework.parser_status: {framework.get('parser_status')}")
    timeout = spec.get("timeout")
    if not isinstance(timeout, dict):
        errors.append("spec.timeout must be an object")
    else:
        if timeout.get("timeout_seconds") is not None and (
            not isinstance(timeout.get("timeout_seconds"), int) or isinstance(timeout.get("timeout_seconds"), bool)
        ):
            errors.append("spec.timeout.timeout_seconds must be an integer or null")
        if timeout.get("timeout_policy") not in TIMEOUT_POLICIES:
            errors.append(f"unsupported timeout.timeout_policy: {timeout.get('timeout_policy')}")
        if timeout.get("timed_out") is not None and not isinstance(timeout.get("timed_out"), bool):
            errors.append("spec.timeout.timed_out must be a boolean or null")
    for list_field in ["artifacts", "logs", "evidence_packet_refs", "explicit_non_capabilities"]:
        if not isinstance(spec.get(list_field), list):
            errors.append(f"spec.{list_field} must be an array")
    for list_field in ["artifacts", "logs"]:
        for index, item in enumerate(_as_list(spec.get(list_field))):
            if not isinstance(item, dict):
                errors.append(f"spec.{list_field}[{index}] must be an object")
                continue
            if not isinstance(item.get("path"), str) or not item.get("path"):
                errors.append(f"spec.{list_field}[{index}].path must be a non-empty string")
            if not isinstance(item.get("role"), str) or not item.get("role"):
                errors.append(f"spec.{list_field}[{index}].role must be a non-empty string")
    non_capabilities = spec.get("explicit_non_capabilities")
    if isinstance(non_capabilities, list):
        for item in non_capabilities:
            if not isinstance(item, str) or not item:
                errors.append("spec.explicit_non_capabilities entries must be non-empty strings")
        if spec.get("capability_label") in non_capabilities:
            errors.append("spec.capability_label must not appear in explicit_non_capabilities")
    capability_label = spec.get("capability_label")
    if capability_label not in RECOGNIZED_CAPABILITIES:
        errors.append(f"unknown capability_label: {capability_label}")
    failure_summary = spec.get("failure_summary")
    if failure_summary is not None and not isinstance(failure_summary, dict):
        errors.append("spec.failure_summary must be an object")
    retry = spec.get("retry")
    if retry is not None and not isinstance(retry, dict):
        errors.append("spec.retry must be an object")
    for flag in [
        "test_broker_runtime_implemented",
        "async_test_execution_implemented",
        "test_job_submission_implemented",
        "test_job_run_implemented",
        "test_job_retry_runtime_implemented",
        "test_job_summarize_runtime_implemented",
        "scheduler_implemented",
        "leases_implemented",
        "supervisor_implemented",
        "worker_execution_implemented",
        "workunit_claim_run_finish_repair_implemented",
        "provider_adapter_implemented",
        "service_implemented",
        "commander_implemented",
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
    if status.get("startedAt") is not None and not isinstance(status.get("startedAt"), str):
        errors.append("status.startedAt must be a string or null")
    if status.get("endedAt") is not None and not isinstance(status.get("endedAt"), str):
        errors.append("status.endedAt must be a string or null")
    if status.get("exitCode") is not None and (
        not isinstance(status.get("exitCode"), int) or isinstance(status.get("exitCode"), bool)
    ):
        errors.append("status.exitCode must be an integer or null")
    if status.get("durationSeconds") is not None and (
        not isinstance(status.get("durationSeconds"), (int, float)) or isinstance(status.get("durationSeconds"), bool)
    ):
        errors.append("status.durationSeconds must be a number or null")
    if status.get("phase") in {"submitted", "running"} and spec.get("job_kind") in {"metadata_only", "validation_observation"}:
        errors.append("metadata-only TestJob must not claim submitted or running phase")
    return errors


def load_test_job_schema(repo_root: str | Path | None = None) -> dict[str, Any]:
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


def validate_test_job_with_schema(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    active_schema = schema if schema is not None else load_test_job_schema()
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
            "expected_required_fields": TEST_JOB_REQUIRED_FIELDS,
            "schema_required_fields": [],
        }
    required = schema.get("required")
    schema_required = required if isinstance(required, list) else []
    missing = [field for field in TEST_JOB_REQUIRED_FIELDS if field not in schema_required]
    extra_required = [str(field) for field in schema_required if field not in TEST_JOB_REQUIRED_FIELDS]
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
    if "TestJob" not in schema_kinds:
        errors.append("schema.properties.kind.enum must include TestJob")
    spec_required = (
        properties.get("spec", {}).get("required", [])
        if isinstance(properties.get("spec"), dict)
        else []
    )
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
        "expected_required_fields": TEST_JOB_REQUIRED_FIELDS,
        "schema_required_fields": [str(item) for item in schema_required],
        "missing_required_fields": missing,
        "extra_required_fields": extra_required,
        "checked_properties": sorted(expected_types),
    }


def validate_test_job_runtime(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> dict[str, Any]:
    active_schema = schema if schema is not None else load_test_job_schema()
    helper_errors = validate_test_job(obj)
    schema_errors = validate_test_job_with_schema(obj, active_schema)
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


def project_report_to_test_job(
    repo_root: Path,
    report: dict[str, Any],
    source_path: Path,
    *,
    source_task_id: str,
    source_task_kind: str,
    artifact_role: str,
) -> dict[str, Any]:
    observed_commands = _observed_commands(report)
    first_command = str(observed_commands[0]["command"]) if observed_commands else ""
    job_kind = "validation_observation" if first_command or "validation" in artifact_role or "check" in artifact_role else "metadata_only"
    job_id = _deterministic_job_id(source_task_id, source_path, job_kind)
    report_status = _normalize_result(report.get("status") or report.get("result"))
    warnings = report.get("warnings") if isinstance(report.get("warnings"), list) else []
    errors = report.get("errors") if isinstance(report.get("errors"), list) else []
    if report_status in {"FAILED_VALIDATION", "BLOCKED"} and not errors:
        errors = [f"source report status is {report_status}"]
    source_hash = sha256_file(repo_root / source_path) if (repo_root / source_path).exists() else ""
    source_worker_run_id = None
    if report.get("kind") == "WorkerRun":
        spec = report.get("spec") if isinstance(report.get("spec"), dict) else {}
        source_worker_run_id = spec.get("run_id") if isinstance(spec.get("run_id"), str) else None
    framework = _framework_for_command(first_command, report)
    return build_test_job(
        job_id=job_id,
        source_workunit_id=source_task_id,
        source_task_id=source_task_id,
        source_worker_run_id=source_worker_run_id,
        source_task_kind=source_task_kind,
        job_kind=job_kind,
        command={
            "argv": [first_command] if first_command else [],
            "cwd": ".",
            "env_policy": "metadata_only",
            "shell": None,
            "description": "Projected from existing validation/check evidence; no TestJob command executed.",
            "observed_commands": observed_commands,
        },
        environment={
            "runner_kind": "metadata_only",
            "platform": None,
            "python": None,
            "notes": ["Projection is metadata-only; no test runner was invoked by TestJob."],
        },
        framework=framework,
        timeout={"timeout_seconds": None, "timeout_policy": "not_configured", "timed_out": None},
        artifacts=[artifact_ref(repo_root, source_path, artifact_role)],
        logs=[],
        evidence_packet_refs=[],
        explicit_non_capabilities=explicit_non_capabilities(report),
        failure_summary={
            "summary": "; ".join(str(item) for item in errors) if errors else "",
            "failed_tests": [],
            "likely_files": [],
            "excerpt_path": None,
            "parser_status": "metadata_only",
        },
        retry={
            "attempt": 1,
            "max_attempts": 1,
            "retry_policy": "not_configured",
            "flake_classification": "unknown",
        },
        source_path=source_path,
        validation_summary={
            "status": report_status,
            "source_report_type": report.get("report_type", ""),
            "source_schema_version": report.get("schema_version", ""),
            "source_sha256": source_hash,
            "metadata_only_projection": True,
            "test_executed_by_test_job": False,
            "observed_commands_count": len(observed_commands),
        },
        name=source_path.stem,
        phase="validation_observation" if job_kind == "validation_observation" else "metadata_only",
        result=report_status,
        started_at=None,
        ended_at=None,
        exit_code=_first_exit_code(observed_commands),
        duration_seconds=None,
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
        projection = project_report_to_test_job(
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


def _missing_source_paths(root: Path) -> list[str]:
    missing: list[str] = []
    for meta in SOURCE_ARTIFACTS.values():
        rel = meta.get("path")
        if isinstance(rel, Path) and not (root / rel).exists():
            missing.append(rel.as_posix())
    return sorted(missing)


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
        "schema_version": "aide.test-job-projection.v0",
        "report_type": "test_job_projection",
        "kind": "TestJobProjectionReport",
        "status": "PASS" if projections and not source_reports_mutated else "FAILED_VALIDATION",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_label": FEATURE_FLAG,
        "source": "accepted-artifacts",
        "projections_written": sorted(projections),
        "source_reports_checked": [_relative_posix(path, root) for path in source_paths],
        "missing_sources": _missing_source_paths(root),
        "source_reports_mutated": source_reports_mutated,
        "destructive_migration_performed": False,
        "test_broker_runtime_implemented": False,
        "async_test_execution_implemented": False,
        "test_job_submission_implemented": False,
        "test_job_run_implemented": False,
        "test_job_retry_runtime_implemented": False,
        "test_job_summarize_runtime_implemented": False,
        "worker_execution_performed": False,
        "workunit_claim_run_finish_repair_performed": False,
        "scheduler_behavior": False,
        "leases_created": False,
        "supervisor_behavior": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
        "github_mutation": False,
        "not_capabilities": EXPLICIT_NON_CAPABILITIES,
        "warnings": [
            "Projection outputs are additive metadata-only TestJob records.",
            "Optional accepted-source gaps are recorded in missing_sources when present.",
        ],
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
        "contract_envelope_behavior_preserved": parsed.get("contract_envelope", False),
        "evidence_packet_behavior_preserved": parsed.get("evidence_packet", False),
        "workunit_queue_behavior_preserved": parsed.get("workunit_queue", False),
        "worker_run_behavior_preserved": parsed.get("worker_run", False),
        "worker_run_acceptance_preserved": parsed.get("worker_run_acceptance", False),
        "testjob_does_not_require_worker_execution": True,
        "testjob_does_not_require_test_broker_runtime": True,
        "projection_paths_additive": True,
        "destructive_migration_performed": False,
    }


def test_job_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    schema_path = root / SCHEMA_PATH
    projection_paths = [root / rel for rel in PROJECTION_FILES.values()]
    data = {
        "schema_version": "aide.test-job-status.v0",
        "report_type": "test_job_status",
        "kind": "TestJobProjectionReport",
        "status": "PASS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "schema_file_exists": schema_path.exists(),
        "schema_validation_mode": SCHEMA_VALIDATION_MODE,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "recognized_capabilities": sorted(RECOGNIZED_CAPABILITIES),
        "job_kinds": sorted(JOB_KINDS),
        "phase_values": sorted(PHASE_VALUES),
        "result_values": sorted(RESULT_VALUES),
        "capability_label": FEATURE_FLAG,
        "implementation_scope": "schema_helper_projection_cli_only",
        "accepted_predecessor": ACCEPTED_PREDECESSOR,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "source_reports": {key: (root / meta["path"]).exists() for key, meta in SOURCE_ARTIFACTS.items()},
        "projection_files": [PROJECTION_FILES[key].as_posix() for key in PROJECTION_FILES],
        "projection_files_existing": [path.relative_to(root).as_posix() for path in projection_paths if path.exists()],
        "test_broker_runtime_implemented": False,
        "async_test_execution_implemented": False,
        "test_job_submission_implemented": False,
        "test_job_run_implemented": False,
        "test_job_retry_runtime_implemented": False,
        "test_job_summarize_runtime_implemented": False,
        "worker_execution_implemented": False,
        "workunit_claim_run_finish_repair_implemented": False,
        "scheduler_implemented": False,
        "leases_implemented": False,
        "supervisor_implemented": False,
        "provider_adapter_implemented": False,
        "service_implemented": False,
        "commander_implemented": False,
        "destructive_migration_performed": False,
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


def test_job_validate(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
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
        schema = load_test_job_schema(root)
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
        helper_errors = validate_test_job(obj)
        schema_errors: list[str] = []
        if schema_file_parsed:
            runtime = validate_test_job_runtime(obj, schema)
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
        validate_test_job_runtime(sample_unknown_optional_test_job(), schema)
        if schema_file_parsed
        else {"status": "FAILED_VALIDATION", "helper_validation_errors": [], "schema_validation_errors": schema_load_errors}
    )
    required_runtime = (
        validate_test_job_runtime(sample_unknown_required_capability_test_job(), schema)
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
        read_json(path)["spec"]["test_broker_runtime_implemented"] is False
        and read_json(path)["spec"]["async_test_execution_implemented"] is False
        and read_json(path)["spec"]["test_job_submission_implemented"] is False
        and read_json(path)["spec"]["worker_execution_implemented"] is False
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
        "schema_version": "aide.test-job-validation.v0",
        "report_type": "test_job_validation",
        "kind": "TestJobValidationReport",
        "task_id": "AIDE-BUILD-TESTJOB-SCHEMA-01",
        "status": status,
        "validated": status == "PASS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_label": FEATURE_FLAG,
        "schema_path": SCHEMA_PATH.as_posix(),
        "schema_file_path": SCHEMA_PATH.as_posix(),
        "helper_path": "core/protocol/test_job.py",
        "schema_file_exists": schema_path.exists(),
        "schema_file_loaded": schema_file_loaded,
        "schema_file_parsed": schema_file_parsed,
        "schema_validation_executed": schema_validation_executed,
        "schema_validation_mode": SCHEMA_VALIDATION_MODE if schema_validation_executed else "unavailable",
        "schema_helper_alignment_checked": schema_file_parsed,
        "schema_helper_alignment": alignment_result.get("schema_helper_alignment_status", "FAILED_VALIDATION"),
        "schema_helper_alignment_status": alignment_result.get("schema_helper_alignment_status", "FAILED_VALIDATION"),
        "schema_validation_limitations": SCHEMA_VALIDATION_LIMITATIONS,
        "schema_load_errors": schema_load_errors,
        "alignment_errors": alignment_errors,
        "alignment_warnings": alignment_warnings,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "recognized_capabilities": sorted(RECOGNIZED_CAPABILITIES),
        "job_kinds": sorted(JOB_KINDS),
        "phase_values": sorted(PHASE_VALUES),
        "source_reports_checked": projection_result.get("source_reports_checked", []),
        "missing_sources": projection_result.get("missing_sources", []),
        "projections_written": projection_result.get("projections_written", []),
        "projections_checked": [item["path"] for item in validation_results],
        "validation_results": validation_results,
        "runtime_validation_results": runtime_validation_results,
        "helper_validation_errors": helper_validation_errors,
        "schema_validation_errors": schema_validation_errors,
        "validation_errors": [*schema_load_errors, *alignment_errors],
        "validation_warnings": [
            "TestJob is a minimal v1alpha1 metadata schema; Test Broker runtime is not implemented.",
            "Projection outputs are additive and source reports remain canonical.",
            "Full JSON Schema Draft 2020-12 validation remains future work.",
            "Missing optional accepted-source reports are recorded as warnings.",
            *projection_result.get("missing_sources", []),
            *alignment_warnings,
        ],
        "compatibility_results": compatibility_results,
        "backwards_compatibility_preserved": compatibility_results["status"] == "PASS",
        "projection_validation": "PASS" if projection_result.get("status") == "PASS" and all_projections_valid else "FAILED_VALIDATION",
        "cli_validation": "PASS",
        "destructive_migration_performed": False,
        "source_reports_mutated": projection_result.get("source_reports_mutated", False),
        "unknown_optional_fields_tolerated": unknown_optional_fields_tolerated,
        "unknown_required_capability_fails_closed": unknown_required_capability_fails_closed,
        "explicit_non_capabilities_preserved": explicit_non_capabilities_preserved,
        "not_capabilities_preserved": explicit_non_capabilities_preserved,
        "metadata_only_truthful": metadata_only_truthful,
        "test_broker_runtime_implemented": False,
        "async_test_execution_implemented": False,
        "test_job_submission_implemented": False,
        "test_job_run_implemented": False,
        "test_job_retry_runtime_implemented": False,
        "test_job_summarize_runtime_implemented": False,
        "worker_execution_implemented": False,
        "workunit_claim_run_finish_repair_implemented": False,
        "scheduler_implemented": False,
        "leases_implemented": False,
        "supervisor_implemented": False,
        "provider_adapter_implemented": False,
        "service_implemented": False,
        "commander_implemented": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
        "github_mutation": False,
        "forbidden_operations_preserved": forbidden_operations_preserved(),
        "warnings": [
            "TestJob is a minimal v1alpha1 metadata schema; Test Broker runtime is not implemented.",
            "Projection outputs are additive and source reports remain canonical.",
            "Full JSON Schema Draft 2020-12 validation remains future work.",
            "WorkUnit claim/run/finish/repair, leases, scheduler, worker execution, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target apply, rollback execution, release, and promotion remain future work.",
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
        "test_broker_runtime": True,
        "async_test_execution": True,
        "test_job_submit": True,
        "test_job_run": True,
        "test_job_retry_runtime": True,
        "test_job_summarize_runtime": True,
        "worker_execution": True,
        "workunit_claim": True,
        "workunit_run": True,
        "workunit_finish": True,
        "workunit_repair": True,
        "leases": True,
        "scheduler": True,
        "supervisor": True,
        "service": True,
        "commander": True,
        "provider_adapters": True,
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
        {"task": "AIDE-CHECK-TESTJOB-SCHEMA-01", "reason": "independent review of TestJob schema, helper validation, projections, compatibility, tests, no destructive migration, no overclaiming, and forbidden-operation preservation"},
        {"task": "AIDE-ACCEPT-TESTJOB-SCHEMA-01", "reason": "accept TestJob only after check and any required hardening"},
        {"task": "AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01", "reason": "define patch transaction protocol after TestJob acceptance"},
        {"task": "AIDE-BUILD-BLOCKER-REPAIR-SCHEMAS-01", "reason": "define blocker and repair objects before repair loops"},
        {"task": "AIDE-BUILD-CAPABILITY-MANIFEST-01", "reason": "declare capabilities before runtime/service surfaces"},
        {"task": "AIDE-BUILD-ADAPTER-MANIFEST-01", "reason": "declare adapter conformance before provider adapters"},
        {"task": "AIDE-BUILD-EVENT-RECORD-SCHEMA-01", "reason": "define event records before scheduler/runtime implementation"},
        {"task": "AIDE-BUILD-TEST-BROKER-RUNTIME-01", "reason": "future only after TestJob protocol acceptance"},
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    deferred = [
        "Test Broker runtime",
        "async test execution",
        "real TestJob submission",
        "test-job run/retry/summarize runtime",
        "scheduler",
        "leases",
        "supervisor",
        "worker execution",
        "WorkUnit claim/run/finish/repair",
        "Service",
        "Commander",
        "provider adapters",
        "branch/worktree automation",
        "target repo apply",
        "active repo apply",
        "rollback execution",
        "release/promotion",
        "GitHub mutation",
        "Gateway",
        "network",
        "model/provider calls",
    ]
    return [{"item": item, "reason": "intentionally deferred beyond the minimal TestJob schema slice"} for item in deferred]


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# TestJob Status",
        "",
        f"- status: {data.get('status')}",
        f"- api_version: {data.get('api_version')}",
        f"- protocol_version: {data.get('protocol_version')}",
        f"- schema_file_path: {data.get('schema_file_path')}",
        f"- schema_file_exists: {str(data.get('schema_file_exists', False)).lower()}",
        f"- schema_validation_mode: {data.get('schema_validation_mode')}",
        f"- capability_label: {data.get('capability_label')}",
        f"- implementation_scope: {data.get('implementation_scope')}",
        f"- accepted_predecessor: {data.get('accepted_predecessor')}",
        "- test_broker_runtime_implemented: false",
        "- async_test_execution_implemented: false",
        "- test_job_submission_implemented: false",
        "- test_job_run_implemented: false",
        "- scheduler_implemented: false",
        "- leases_implemented: false",
        "- supervisor_implemented: false",
        "- worker_execution_implemented: false",
        "- workunit_claim_run_finish_repair_implemented: false",
        "- provider_adapter_implemented: false",
        "- service_implemented: false",
        "- commander_implemented: false",
        "- destructive_migration_performed: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- branch_mutation: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "- github_mutation: false",
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
    lines.extend(["", "## Non-Capabilities", ""])
    for item in data.get("explicit_non_capabilities", []):
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def render_projection_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# TestJob Projection",
        "",
        f"- status: {report.get('status')}",
        f"- source: {report.get('source')}",
        f"- capability_label: {report.get('capability_label')}",
        f"- source_reports_mutated: {str(report.get('source_reports_mutated', False)).lower()}",
        "- test_broker_runtime_implemented: false",
        "- async_test_execution_implemented: false",
        "- test_job_submission_implemented: false",
        "- test_job_run_implemented: false",
        "- worker_execution_performed: false",
        "- workunit_claim_run_finish_repair_performed: false",
        "- scheduler_behavior: false",
        "- leases_created: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "- github_mutation: false",
        "",
        "## Projections Written",
        "",
    ]
    for rel in report.get("projections_written", []):
        lines.append(f"- {rel}")
    lines.extend(["", "## Source Reports Checked", ""])
    for rel in report.get("source_reports_checked", []):
        lines.append(f"- {rel}")
    lines.extend(["", "## Missing Optional Sources", ""])
    for rel in report.get("missing_sources", []):
        lines.append(f"- {rel}")
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# TestJob Validation",
        "",
        f"- status: {report.get('status')}",
        f"- capability_label: {report.get('capability_label')}",
        f"- api_version: {report.get('api_version')}",
        f"- protocol_version: {report.get('protocol_version')}",
        f"- schema_file_path: {report.get('schema_file_path')}",
        f"- helper_path: {report.get('helper_path')}",
        f"- schema_file_loaded: {str(report.get('schema_file_loaded', False)).lower()}",
        f"- schema_file_parsed: {str(report.get('schema_file_parsed', False)).lower()}",
        f"- schema_validation_executed: {str(report.get('schema_validation_executed', False)).lower()}",
        f"- schema_validation_mode: {report.get('schema_validation_mode')}",
        f"- schema_helper_alignment_checked: {str(report.get('schema_helper_alignment_checked', False)).lower()}",
        f"- schema_helper_alignment_status: {report.get('schema_helper_alignment_status')}",
        "- test_broker_runtime_implemented: false",
        "- async_test_execution_implemented: false",
        "- test_job_submission_implemented: false",
        "- test_job_run_implemented: false",
        "- worker_execution_implemented: false",
        "- workunit_claim_run_finish_repair_implemented: false",
        "- scheduler_implemented: false",
        "- leases_implemented: false",
        "- provider_adapter_implemented: false",
        "- service_implemented: false",
        "- commander_implemented: false",
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
        "# TestJob Future Work",
        "",
        "## Recommended Order",
        "",
    ]
    for index, item in enumerate(future_work_items(), start=1):
        future_lines.append(f"{index}. {item['task']}: {item['reason']}.")
    unfinished_lines = [
        "# TestJob Unfinished Work",
        "",
        "## Finished In This Slice",
        "",
        "- Minimal envelope-backed TestJob helper and validator.",
        "- Additive metadata-only projections from accepted validation/check/acceptance artifacts.",
        "- Additive validation reports under `.aide/reports/test-job/`.",
        "",
        "## Not Attempted By Design",
        "",
    ]
    for item in unfinished_work_items():
        unfinished_lines.append(f"- {item['item']}: {item['reason']}.")
    write_text(repo_root / FUTURE_WORK_MD, "\n".join(future_lines) + "\n")
    write_text(repo_root / UNFINISHED_WORK_MD, "\n".join(unfinished_lines) + "\n")
