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
    data = {
        "schema_version": "aide.contract-envelope-status.v0",
        "report_type": "contract_envelope_status",
        "status": "PASS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
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
    for projection_path in projections:
        obj = read_json(projection_path)
        errors = validate_envelope(obj, SUPPORTED_KINDS)
        validation_results.append(
            {
                "path": projection_path.relative_to(root).as_posix(),
                "result": "PASS" if not errors else "FAIL",
                "errors": errors,
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
    compatibility_pass = all(
        value is True
        for key, value in compatibility_results.items()
        if key != "source_reports_destructively_migrated"
    ) and compatibility_results["source_reports_destructively_migrated"] is False
    status = "PASS" if all(item["result"] == "PASS" for item in validation_results) and compatibility_pass else "FAIL"
    report = {
        "schema_version": "aide.contract-envelope-validation.v0",
        "report_type": "contract_envelope_validation",
        "task_id": "AIDE-BUILD-CONTRACT-ENVELOPE-01",
        "status": status,
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "supported_kinds": sorted(SUPPORTED_KINDS),
        "recognized_capabilities": sorted(RECOGNIZED_CAPABILITIES),
        "source_reports_checked": projection_result.get("source_reports_checked", []),
        "projections_written": projection_result.get("projections_written", []),
        "validation_results": validation_results,
        "compatibility_results": compatibility_results,
        "backwards_compatibility_preserved": status == "PASS",
        "destructive_migration_performed": False,
        "forbidden_operations_preserved": forbidden_operations_preserved(),
        "warnings": [
            "Minimal envelope helper is v1alpha1 and is not a full protocol stability claim.",
            "WorkUnit, EvidencePacket, TestJob, Checkpoint, ProviderAdapter, Service, and Commander schemas remain future work.",
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
        "workunit_cli": True,
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
        {"task": "AIDE-CHECK-CONTRACT-ENVELOPE-01", "reason": "independent review of helper, projections, validation, compatibility, and no-overclaiming"},
        {"task": "AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01", "reason": "extract minimal EvidencePacket shape after envelope is checked"},
        {"task": "AIDE-BUILD-WORKUNIT-QUEUE-V1-01", "reason": "define minimal queue WorkUnit object after envelope and evidence shapes are accepted"},
        {"task": "AIDE-BUILD-WORKUNIT-CLI-01", "reason": "add WorkUnit CLI after queue object is stable"},
        {"task": "AIDE-BUILD-TEST-BROKER-01", "reason": "add async test broker after WorkUnit primitives exist"},
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
        "- destructive_migration_performed: false",
        f"- backwards_compatibility_preserved: {str(report.get('backwards_compatibility_preserved', False)).lower()}",
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
