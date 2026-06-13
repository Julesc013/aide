"""Read-only CLI helpers for accepted AIDE WorkUnit queue objects.

This module exposes existing filesystem queue tasks through the accepted
WorkUnit Queue V1 helper. It intentionally does not implement queue mutation,
claim/run semantics, leases, scheduling, service behavior, or runtime behavior.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from core.protocol import workunit


API_VERSION = workunit.API_VERSION
PROTOCOL_VERSION = "0.1.0"
FEATURE_FLAG = "minimal_workunit_readonly_cli"
REPORT_ROOT = Path(".aide/reports/workunit-cli")
STATUS_MD = REPORT_ROOT / "status.md"
LIST_JSON = REPORT_ROOT / "list.json"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"
INSPECT_ROOT = REPORT_ROOT / "inspect"
SUPPORTED_COMMANDS = ["status", "list", "inspect", "validate"]
UNSUPPORTED_COMMANDS = ["create", "claim", "run", "block", "finish", "repair"]
SAFE_TASK_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def write_json(path: Path, obj: dict[str, Any]) -> None:
    workunit.write_json(path, obj)


def write_text(path: Path, text: str) -> None:
    workunit.write_text(path, text)


def read_json(path: Path) -> dict[str, Any]:
    return workunit.read_json(path)


def queue_root(repo_root: str | Path) -> Path:
    return Path(repo_root) / ".aide/queue"


def _relative_posix(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def _is_under(child: Path, parent: Path) -> bool:
    child_resolved = child.resolve(strict=False)
    parent_resolved = parent.resolve(strict=False)
    return child_resolved == parent_resolved or parent_resolved in child_resolved.parents


def task_id_errors(repo_root: str | Path, task_id: str | None, *, require_exists: bool = True) -> list[str]:
    root = Path(repo_root)
    errors: list[str] = []
    if task_id is None or not str(task_id):
        return ["task_id is required"]
    raw = str(task_id)
    if raw != raw.strip():
        errors.append("task_id must not include surrounding whitespace")
    if Path(raw).is_absolute():
        errors.append("task_id must not be an absolute path")
    if raw.startswith("."):
        errors.append("task_id must not be a hidden path")
    if "/" in raw or "\\" in raw:
        errors.append("task_id must not include path separators")
    if ".." in raw:
        errors.append("task_id must not include parent traversal")
    if any(char in raw for char in "*?[]{}"):
        errors.append("task_id must not include wildcard or glob characters")
    if not SAFE_TASK_ID.fullmatch(raw):
        errors.append("task_id must match safe queue id characters")
    task_dir = queue_root(root) / raw
    if not _is_under(task_dir, queue_root(root)):
        errors.append("task_id resolves outside .aide/queue")
    if require_exists and not task_dir.is_dir():
        errors.append(f"queue task not found: {raw}")
    elif require_exists and not _is_under(task_dir.resolve(strict=False), queue_root(root)):
        errors.append("task directory resolves outside .aide/queue")
    return errors


def safe_task_dir(repo_root: str | Path, task_id: str) -> Path:
    errors = task_id_errors(repo_root, task_id, require_exists=True)
    if errors:
        raise ValueError("; ".join(errors))
    return queue_root(repo_root) / task_id


def queue_task_dirs(repo_root: str | Path) -> list[Path]:
    root = queue_root(repo_root)
    if not root.exists():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir() and (path / "task.yaml").exists())


def _source_artifact_paths(repo_root: Path, task_dirs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for task_dir in task_dirs:
        for name in ["task.yaml", "status.yaml"]:
            path = task_dir / name
            if path.exists():
                paths.append(path)
        evidence_dir = task_dir / "evidence"
        if evidence_dir.exists():
            paths.extend(sorted(path for path in evidence_dir.glob("*.md") if path.is_file()))
    return paths


def _hashes(paths: list[Path]) -> dict[str, str]:
    return {path.as_posix(): workunit.sha256_file(path) for path in paths if path.exists()}


def _task_summary(repo_root: Path, task_dir: Path) -> dict[str, Any]:
    task_id = task_dir.name
    task_path = task_dir / "task.yaml"
    status_path = task_dir / "status.yaml"
    evidence_dir = task_dir / "evidence"
    task_data = workunit.read_simple_yaml(task_path)
    status_data = workunit.read_simple_yaml(status_path)
    projection_valid = False
    validation_errors: list[str] = []
    work_type = "unknown"
    phase = str(status_data.get("status") or task_data.get("status") or "unknown")
    try:
        projected = workunit.project_queue_task(repo_root, task_id)
        validation_errors = workunit.validate_workunit(projected)
        projection_valid = not validation_errors
        work_type = str(projected.get("spec", {}).get("work_type", "unknown"))
        phase = str(projected.get("status", {}).get("phase", phase))
    except Exception as exc:  # noqa: BLE001 - list reports should not stop at first historical task.
        validation_errors = [str(exc)]
    return {
        "task_id": task_id,
        "title": str(task_data.get("title") or task_id),
        "source_path": _relative_posix(task_path, repo_root),
        "status_path": _relative_posix(status_path, repo_root) if status_path.exists() else "",
        "evidence_dir": _relative_posix(evidence_dir, repo_root) if evidence_dir.exists() else "",
        "task_yaml_exists": task_path.exists(),
        "status_yaml_exists": status_path.exists(),
        "evidence_dir_exists": evidence_dir.exists(),
        "evidence_file_count": len(list(evidence_dir.glob("*.md"))) if evidence_dir.exists() else 0,
        "phase": phase,
        "status": str(status_data.get("status") or task_data.get("status") or "unknown"),
        "planning_state": str(status_data.get("planning_state") or task_data.get("planning_state") or ""),
        "result": str(status_data.get("result") or task_data.get("result") or "UNKNOWN"),
        "work_type": work_type,
        "projectable": projection_valid,
        "validation_status": "PASS" if projection_valid else "FAILED_VALIDATION",
        "validation_errors": validation_errors,
    }


def discover_queue_tasks(repo_root: str | Path) -> list[dict[str, Any]]:
    root = Path(repo_root)
    return [_task_summary(root, path) for path in queue_task_dirs(root)]


def _latest_workunit_queue_validation(repo_root: Path) -> dict[str, Any]:
    path = repo_root / workunit.VALIDATION_JSON
    if not path.exists():
        return {"status": "UNAVAILABLE", "path": workunit.VALIDATION_JSON.as_posix()}
    try:
        data = read_json(path)
    except Exception as exc:  # noqa: BLE001 - status should report parse failures.
        return {"status": "FAILED_VALIDATION", "path": workunit.VALIDATION_JSON.as_posix(), "error": str(exc)}
    return {"status": data.get("status", "UNKNOWN"), "path": workunit.VALIDATION_JSON.as_posix()}


def mutation_command_flags(value: bool = False) -> dict[str, bool]:
    return {
        "workunit_create_implemented": value,
        "workunit_claim_implemented": value,
        "workunit_run_implemented": value,
        "workunit_block_implemented": value,
        "workunit_finish_implemented": value,
        "workunit_repair_implemented": value,
    }


def workunit_cli_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    tasks = discover_queue_tasks(root)
    schema_loaded = False
    schema_parsed = False
    schema_error = ""
    try:
        workunit.load_workunit_schema(root)
        schema_loaded = True
        schema_parsed = True
    except ValueError as exc:
        schema_error = str(exc)
    latest_validation = _latest_workunit_queue_validation(root)
    report = {
        "schema_version": "aide.workunit-cli-status.v1",
        "report_type": "workunit_cli_status",
        "task_id": "AIDE-BUILD-WORKUNIT-CLI-01",
        "status": "PASS" if queue_root(root).exists() and schema_loaded and schema_parsed else "FAILED_VALIDATION",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_label": FEATURE_FLAG,
        "accepted_workunit_queue_capability": workunit.FEATURE_FLAG,
        "workunit_cli_mode": "readonly",
        "supported_commands": SUPPORTED_COMMANDS,
        "unsupported_commands": UNSUPPORTED_COMMANDS,
        "queue_root": _relative_posix(queue_root(root), root),
        "queue_root_exists": queue_root(root).exists(),
        "task_directories_discovered": len(tasks),
        "projectable_workunits": sum(1 for item in tasks if item["projectable"]),
        "schema_file_loaded": schema_loaded,
        "schema_file_parsed": schema_parsed,
        "schema_error": schema_error,
        "latest_workunit_queue_validation": latest_validation,
        "read_only": True,
        "mutation_commands_implemented": False,
        **mutation_command_flags(False),
        "destructive_migration_performed": False,
        "source_queue_tasks_mutated": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "network_calls": False,
    }
    write_text(root / STATUS_MD, render_status_markdown(report))
    return report


def workunit_cli_list(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    tasks = discover_queue_tasks(root)
    report = {
        "schema_version": "aide.workunit-cli-list.v1",
        "report_type": "workunit_cli_list",
        "task_id": "AIDE-BUILD-WORKUNIT-CLI-01",
        "status": "PASS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_label": FEATURE_FLAG,
        "workunit_cli_mode": "readonly",
        "task_count": len(tasks),
        "tasks": tasks,
        "source_queue_tasks_mutated": False,
        "destructive_migration_performed": False,
        **mutation_command_flags(False),
    }
    write_json(root / LIST_JSON, report)
    return report


def workunit_cli_inspect(repo_root: str | Path, task_id: str) -> dict[str, Any]:
    root = Path(repo_root)
    task_dir = safe_task_dir(root, task_id)
    task_path = task_dir / "task.yaml"
    status_path = task_dir / "status.yaml"
    evidence_dir = task_dir / "evidence"
    projected = workunit.project_queue_task(root, task_id)
    runtime = workunit.validate_workunit_runtime(projected, workunit.load_workunit_schema(root))
    evidence_files = sorted(path for path in evidence_dir.glob("*.md") if path.is_file()) if evidence_dir.exists() else []
    report = {
        "schema_version": "aide.workunit-cli-inspect.v1",
        "report_type": "workunit_cli_inspect",
        "task_id": "AIDE-BUILD-WORKUNIT-CLI-01",
        "inspected_task_id": task_id,
        "status": runtime["status"],
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_label": FEATURE_FLAG,
        "workunit_cli_mode": "readonly",
        "source_paths": {
            "task_yaml": _relative_posix(task_path, root),
            "status_yaml": _relative_posix(status_path, root) if status_path.exists() else "",
            "evidence_dir": _relative_posix(evidence_dir, root) if evidence_dir.exists() else "",
        },
        "source_presence": {
            "task_yaml_exists": task_path.exists(),
            "status_yaml_exists": status_path.exists(),
            "evidence_dir_exists": evidence_dir.exists(),
            "evidence_file_count": len(evidence_files),
        },
        "source_hashes": {
            "task_yaml": workunit.sha256_file(task_path) if task_path.exists() else "",
            "status_yaml": workunit.sha256_file(status_path) if status_path.exists() else "",
            "evidence_files": {path.name: workunit.sha256_file(path) for path in evidence_files},
        },
        "workunit": projected,
        "validation": runtime,
        "source_queue_tasks_mutated": False,
        "destructive_migration_performed": False,
        **mutation_command_flags(False),
    }
    write_json(root / INSPECT_ROOT / f"{task_id}.json", report)
    return report


def _projection_report_status(repo_root: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"projection_files_checked": 0, "projection_files_valid": 0, "errors": []}
    schema = workunit.load_workunit_schema(repo_root)
    for path in sorted((repo_root / workunit.PROJECTION_ROOT).glob("*.json")):
        result["projection_files_checked"] += 1
        try:
            obj = read_json(path)
            runtime = workunit.validate_workunit_runtime(obj, schema)
        except Exception as exc:  # noqa: BLE001 - validation report records parse failures.
            result["errors"].append(f"{_relative_posix(path, repo_root)}: {exc}")
            continue
        if runtime["status"] == "PASS":
            result["projection_files_valid"] += 1
        else:
            result["errors"].append(f"{_relative_posix(path, repo_root)}: {runtime['status']}")
    result["status"] = "PASS" if not result["errors"] else "FAILED_VALIDATION"
    return result


def _compatibility_results(repo_root: Path) -> dict[str, Any]:
    paths = {
        "workunit_queue_validation": workunit.VALIDATION_JSON,
        "evidence_packet_validation": Path(".aide/reports/evidence-packet/validation.json"),
        "evidence_packet_acceptance": Path(".aide/reports/evidence-packet-acceptance/acceptance-report.json"),
        "contract_envelope_validation": Path(".aide/reports/contract-envelope/validation.json"),
        "lifecycle_fixture_latest_run": Path(".aide/reports/lifecycle-fixture-runner/latest-run.json"),
        "lifecycle_fixture_verify": Path(".aide/reports/lifecycle-fixture-runner/verify.json"),
    }
    parsed: dict[str, bool] = {}
    statuses: dict[str, str] = {}
    errors: list[str] = []
    for key, rel in paths.items():
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
        "legacy_queue_fields_preserved": True,
        "destructive_migration_performed": False,
        "lifecycle_fixture_behavior_preserved": parsed.get("lifecycle_fixture_verify", False),
        "contract_envelope_behavior_preserved": parsed.get("contract_envelope_validation", False),
        "evidence_packet_behavior_preserved": parsed.get("evidence_packet_validation", False),
        "workunit_queue_behavior_preserved": parsed.get("workunit_queue_validation", False),
        "projections_additive": True,
    }


def _path_safety_results(repo_root: Path) -> dict[str, bool]:
    samples = {
        "path_traversal_rejected": "../outside",
        "absolute_path_rejected": str((repo_root / ".aide/queue").resolve()),
        "separator_injection_rejected": "AIDE-BUILD-WORKUNIT-QUEUE-V1-01/extra",
        "wildcard_rejected": "AIDE-*",
        "hidden_path_rejected": ".git",
    }
    return {key: bool(task_id_errors(repo_root, value, require_exists=False)) for key, value in samples.items()}


def workunit_cli_validate(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    task_dirs = queue_task_dirs(root)
    source_paths = _source_artifact_paths(root, task_dirs)
    hashes_before = _hashes(source_paths)
    tasks = discover_queue_tasks(root)
    schema = workunit.load_workunit_schema(root)
    validation_results: list[dict[str, Any]] = []
    workunit_objects_validated = 0
    for item in tasks:
        if item["projectable"]:
            workunit_objects_validated += 1
        validation_results.append(
            {
                "task_id": item["task_id"],
                "result": item["validation_status"],
                "work_type": item["work_type"],
                "source_path": item["source_path"],
                "errors": item["validation_errors"],
            }
        )
    optional_runtime = workunit.validate_workunit_runtime(workunit.sample_unknown_optional_workunit(), schema)
    required_runtime = workunit.validate_workunit_runtime(workunit.sample_unknown_required_capability_workunit(), schema)
    projection_status = _projection_report_status(root)
    compatibility = _compatibility_results(root)
    path_safety = _path_safety_results(root)
    hashes_after = _hashes(source_paths)
    source_queue_tasks_mutated = hashes_before != hashes_after
    explicit_non_capabilities_preserved = True
    for task_dir in task_dirs:
        obj = workunit.project_queue_task(root, task_dir.name)
        if workunit.implemented_capabilities(obj) & set(obj["spec"]["explicit_non_capabilities"]):
            explicit_non_capabilities_preserved = False
            break
    status = (
        "PASS"
        if queue_root(root).exists()
        and tasks
        and all(item["result"] == "PASS" for item in validation_results)
        and projection_status["status"] == "PASS"
        and compatibility["status"] == "PASS"
        and all(path_safety.values())
        and optional_runtime["status"] == "PASS"
        and bool(required_runtime.get("helper_validation_errors"))
        and explicit_non_capabilities_preserved
        and not source_queue_tasks_mutated
        else "FAILED_VALIDATION"
    )
    report = {
        "schema_version": "aide.workunit-cli-validation.v1",
        "report_type": "workunit_cli_validation",
        "task_id": "AIDE-BUILD-WORKUNIT-CLI-01",
        "status": status,
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_label": FEATURE_FLAG,
        "supported_commands": SUPPORTED_COMMANDS,
        "unsupported_commands": UNSUPPORTED_COMMANDS,
        "recognized_capabilities": sorted({*workunit.RECOGNIZED_CAPABILITIES, FEATURE_FLAG}),
        "source_queue_tasks_checked": [item["task_id"] for item in tasks],
        "workunit_objects_validated": workunit_objects_validated,
        "workunit_cli_mode": "readonly",
        **mutation_command_flags(False),
        "queue_root": _relative_posix(queue_root(root), root),
        "queue_root_exists": queue_root(root).exists(),
        "task_discovery_status": "PASS" if tasks else "FAILED_VALIDATION",
        "task_id_safety_checked": True,
        **path_safety,
        "source_queue_tasks_mutated": source_queue_tasks_mutated,
        "destructive_migration_performed": False,
        "backwards_compatibility_preserved": compatibility["status"] == "PASS",
        "unknown_optional_fields_tolerated": optional_runtime["status"] == "PASS",
        "unknown_required_capability_fails_closed": bool(required_runtime.get("helper_validation_errors")),
        "explicit_non_capabilities_preserved": explicit_non_capabilities_preserved,
        "validation_results": validation_results,
        "projection_validation_results": projection_status,
        "compatibility_results": compatibility,
        "forbidden_operations_preserved": forbidden_operations_preserved(),
        "warnings": [
            "This is a read-only CLI surface only; mutation, claim, run, finish, block, and repair remain unimplemented.",
            "Full JSON Schema Draft 2020-12 validation remains deferred to future conformance work.",
        ],
        "limitations": [
            "Inspect accepts safe queue task ids only, not arbitrary paths.",
            "Validate observes queue tasks and writes additive workunit-cli reports only.",
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
        "workunit_mutation_cli": True,
        "workunit_create": True,
        "workunit_claim": True,
        "workunit_run": True,
        "workunit_block": True,
        "workunit_finish": True,
        "workunit_repair": True,
        "full_workunit_runtime": True,
        "scheduler": True,
        "supervisor": True,
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
        {"task": "AIDE-CHECK-WORKUNIT-CLI-01", "reason": "independent review of read-only WorkUnit CLI commands, path safety, compatibility, no destructive mutation, no overclaiming, and tests"},
        {"task": "AIDE-BUILD-WORKUNIT-CLI-HARDEN-01", "reason": "harden only if the check finds command, path, report, or compatibility gaps"},
        {"task": "AIDE-ACCEPT-WORKUNIT-CLI-01", "reason": "accept the read-only CLI after check and any required hardening"},
        {"task": "AIDE-BUILD-WORKUNIT-CLI-MUTATION-01", "reason": "add create/block-style mutation only after read-only CLI acceptance"},
        {"task": "AIDE-BUILD-WORKER-RUN-SCHEMA-01", "reason": "define WorkerRun before agent adapters"},
        {"task": "AIDE-BUILD-TESTJOB-SCHEMA-01", "reason": "define TestJob after the read-only WorkUnit CLI is accepted"},
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    deferred = [
        "WorkUnit mutation CLI",
        "workunit create",
        "workunit claim",
        "workunit run",
        "workunit block",
        "workunit finish",
        "workunit repair",
        "full WorkUnit runtime",
        "scheduler",
        "supervisor",
        "WorkerRun schema",
        "TestJob schema",
        "Test Broker",
        "Checkpoint schema",
        "PromotionPolicy schema",
        "branch/worktree allocator",
        "Service",
        "Commander",
        "provider adapters",
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
    return [{"item": item, "reason": "intentionally deferred beyond the read-only WorkUnit CLI slice"} for item in deferred]


def render_status_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# WorkUnit CLI Status",
        "",
        f"- status: {report.get('status')}",
        f"- capability_label: {report.get('capability_label')}",
        f"- workunit_cli_mode: {report.get('workunit_cli_mode')}",
        f"- accepted_workunit_queue_capability: {report.get('accepted_workunit_queue_capability')}",
        f"- queue_root_exists: {str(report.get('queue_root_exists', False)).lower()}",
        f"- task_directories_discovered: {report.get('task_directories_discovered')}",
        f"- projectable_workunits: {report.get('projectable_workunits')}",
        f"- latest_workunit_queue_validation: {report.get('latest_workunit_queue_validation', {}).get('status')}",
        "- mutation_commands_implemented: false",
        "- destructive_migration_performed: false",
        "- source_queue_tasks_mutated: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- branch_mutation: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        "",
        "## Supported Commands",
        "",
    ]
    for command in report.get("supported_commands", []):
        lines.append(f"- workunit {command}")
    lines.extend(["", "## Unsupported Commands", ""])
    for command in report.get("unsupported_commands", []):
        lines.append(f"- workunit {command}: not implemented")
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# WorkUnit CLI Validation",
        "",
        f"- status: {report.get('status')}",
        f"- capability_label: {report.get('capability_label')}",
        f"- workunit_cli_mode: {report.get('workunit_cli_mode')}",
        f"- source_queue_tasks_checked: {len(report.get('source_queue_tasks_checked', []))}",
        f"- workunit_objects_validated: {report.get('workunit_objects_validated')}",
        "- workunit_create_implemented: false",
        "- workunit_claim_implemented: false",
        "- workunit_run_implemented: false",
        "- workunit_block_implemented: false",
        "- workunit_finish_implemented: false",
        "- workunit_repair_implemented: false",
        f"- source_queue_tasks_mutated: {str(report.get('source_queue_tasks_mutated', False)).lower()}",
        "- destructive_migration_performed: false",
        f"- backwards_compatibility_preserved: {str(report.get('backwards_compatibility_preserved', False)).lower()}",
        f"- unknown_optional_fields_tolerated: {str(report.get('unknown_optional_fields_tolerated', False)).lower()}",
        f"- unknown_required_capability_fails_closed: {str(report.get('unknown_required_capability_fails_closed', False)).lower()}",
        f"- explicit_non_capabilities_preserved: {str(report.get('explicit_non_capabilities_preserved', False)).lower()}",
        "",
        "## Path Safety",
        "",
    ]
    for key in [
        "path_traversal_rejected",
        "absolute_path_rejected",
        "separator_injection_rejected",
        "wildcard_rejected",
        "hidden_path_rejected",
    ]:
        lines.append(f"- {key}: {str(report.get(key, False)).lower()}")
    lines.extend(["", "## Compatibility", ""])
    compatibility = report.get("compatibility_results", {})
    for key, value in compatibility.items():
        if key not in {"parsed_reports", "report_statuses", "errors"}:
            lines.append(f"- {key}: {str(value).lower()}")
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    lines.extend(["", "## Future Work", ""])
    for item in report.get("future_work", []):
        lines.append(f"- {item.get('task')}: {item.get('reason')}")
    return "\n".join(lines) + "\n"


def write_future_and_unfinished_reports(repo_root: Path) -> None:
    future_lines = [
        "# WorkUnit CLI Future Work",
        "",
        "## Recommended Order",
        "",
    ]
    for index, item in enumerate(future_work_items(), start=1):
        future_lines.append(f"{index}. {item['task']}: {item['reason']}.")
    unfinished_lines = [
        "# WorkUnit CLI Unfinished Work",
        "",
        "## Finished In This Slice",
        "",
        "- Read-only `workunit status`.",
        "- Read-only `workunit list`.",
        "- Read-only `workunit inspect --task-id <TASK_ID>`.",
        "- Read-only `workunit validate` with additive reports.",
        "",
        "## Intentionally Deferred",
        "",
    ]
    for item in unfinished_work_items():
        unfinished_lines.append(f"- {item['item']}: {item['reason']}.")
    write_text(repo_root / FUTURE_WORK_MD, "\n".join(future_lines) + "\n")
    write_text(repo_root / UNFINISHED_WORK_MD, "\n".join(unfinished_lines) + "\n")
