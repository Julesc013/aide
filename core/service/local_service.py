"""Small local, no-network AIDE Service foundation v0."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from core.service.artifact_store import ArtifactStore, ArtifactStoreError
from core.service.sqlite_store import LocalServiceError, SQLiteStore, digest_json


TASK_ID = "AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01"
ACCEPTED_TRUST_TASK_ID = "AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01"
PROPOSED_CAPABILITY_LABEL = "local_service_foundation_v0"
REPORT_ROOT = Path(".aide/reports/local-service-foundation-v0")
STATUS_MD = REPORT_ROOT / "status.md"
FIXTURE_REPORT_JSON = REPORT_ROOT / "fixture-report.json"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"

FALSE_BOUNDARY_FIELDS = [
    "network_listener_opened",
    "scheduler_implemented",
    "worker_execution_implemented",
    "capability_execution_implemented",
    "trust_enforcement_implemented",
    "mcp_implemented",
    "workbench_implemented",
    "distributed_locking_implemented",
    "provider_model_calls_performed",
    "preview_apply_implemented",
    "repository_mutation_performed",
    "branch_worktree_mutation_performed",
    "github_mutation_performed",
    "release_or_promotion_performed",
]

EXPLICIT_NON_CAPABILITIES = [
    "network_api",
    "http_server",
    "socket_listener",
    "scheduler",
    "worker_execution",
    "capability_execution",
    "trust_enforcement",
    "mcp_runtime",
    "workbench_runtime",
    "distributed_locking",
    "exactly_once_delivery",
    "provider_model_calls",
    "preview_apply_rollback",
    "repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def local_state_root(repo_root: Path) -> Path:
    return repo_root / ".aide.local" / "service"


def git_status(repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--short"],
            check=True,
            capture_output=True,
            text=True,
            shell=False,
        )
    except (OSError, subprocess.CalledProcessError):
        return "UNKNOWN"
    return result.stdout


def boundary_flags() -> dict[str, bool]:
    return {field: False for field in FALSE_BOUNDARY_FIELDS}


def init_fixture(repo_root: Path, *, state_root: Path | None = None) -> dict[str, Any]:
    root = state_root or Path(tempfile.mkdtemp(prefix="aide-local-service-init-"))
    store = SQLiteStore(root / "state.sqlite")
    try:
        schema_version = store.initialize()
        health = store.health()
    finally:
        store.close()
    report = {
        "status": "PASS_WITH_WARNINGS",
        "task_id": TASK_ID,
        "capability_label": PROPOSED_CAPABILITY_LABEL,
        "schema_version": schema_version,
        "health": health,
        "state_root_is_temp": state_root is None,
        "recommended_next_task": CHECK_TASK_ID,
        **boundary_flags(),
    }
    if state_root is None:
        shutil.rmtree(root, ignore_errors=True)
    return report


def _future_migration_refused(temp_root: Path) -> bool:
    store = SQLiteStore(temp_root / "future" / "state.sqlite")
    try:
        store.initialize()
        store.force_schema_version_for_test(999)
        try:
            store.initialize()
        except LocalServiceError as exc:
            return str(exc) == "future_migration"
        return False
    finally:
        store.close()


def _corruption_refused(temp_root: Path) -> bool:
    db_path = temp_root / "corrupt" / "state.sqlite"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.write_text("not sqlite", encoding="utf-8")
    try:
        store = SQLiteStore(db_path)
        try:
            store.health()
        finally:
            store.close()
    except LocalServiceError:
        return True
    return False


def fixture(repo_root: Path, *, state_root: Path | None = None, write_reports: bool = True) -> dict[str, Any]:
    before_status = git_status(repo_root)
    temp_owner: tempfile.TemporaryDirectory[str] | None = None
    if state_root is None:
        temp_owner = tempfile.TemporaryDirectory(prefix="aide-local-service-")
        root = Path(temp_owner.name)
    else:
        root = state_root
        root.mkdir(parents=True, exist_ok=True)

    store = SQLiteStore(root / "state.sqlite")
    artifacts = ArtifactStore(root)
    report: dict[str, Any]
    try:
        schema_version = store.initialize()
        migration_rerun_version = store.initialize()
        health = store.health()

        work_ref = "aide://workunit/local-service-fixture"
        work_body = {"kind": "WorkUnit", "id": "local-service-fixture", "status": "ready"}
        stored = store.put_object(work_ref, "WorkUnit", work_body)
        listed = store.list_objects(kind="WorkUnit")
        read_back = store.get_object(work_ref)
        version_conflict_refused = False
        try:
            store.put_object(work_ref, "WorkUnit", {"status": "stale"}, expected_version=99)
        except LocalServiceError as exc:
            version_conflict_refused = str(exc) == "resource_version_conflict"

        atomic_ref = "aide://object/local-service-atomic"
        atomic_object, atomic_sequence = store.put_object_with_event(
            atomic_ref,
            "ServiceObject",
            {"value": 1},
            event_ref="aide://event/local-service-atomic-1",
            event_type="object.updated",
        )
        rollback_on_error = False
        try:
            store.put_object_with_event(
                "aide://object/rollback",
                "ServiceObject",
                {"value": "should-not-persist"},
                event_ref="aide://event/rollback",
                event_type="object.updated",
                fail_after_object=True,
            )
        except LocalServiceError as exc:
            rollback_on_error = str(exc) == "injected_atomic_failure"
        rollback_absent = False
        try:
            store.get_object("aide://object/rollback")
        except LocalServiceError as exc:
            rollback_absent = str(exc) == "object_missing"

        second_sequence = store.append_event(
            "aide://event/local-service-event-2",
            "service.observed",
            work_ref,
            {"sequence": 2},
        )
        events_after_zero = store.read_events_after(0)
        cursor = store.ack_cursor("aide://cursor/local-service-fixture", second_sequence)

        payload = b'{"artifact":"fixture"}\n'
        artifact_write = artifacts.write(payload)
        duplicate_artifact = artifacts.write(payload)
        payload_readback = artifacts.read(artifact_write.digest)
        store.record_artifact_metadata(artifact_write.digest, artifact_write.size, "application/json", "fixture.json")
        artifact_metadata = store.get_artifact_metadata(artifact_write.digest)
        digest_mismatch_refused = False
        try:
            artifacts.write(payload, expected_digest="sha256:" + ("0" * 64))
        except ArtifactStoreError as exc:
            digest_mismatch_refused = str(exc) == "artifact_digest_mismatch"
        traversal_refused = False
        try:
            artifacts.read("sha256:../bad")
        except ArtifactStoreError as exc:
            traversal_refused = str(exc) == "artifact_digest_invalid"

        request_digest = digest_json({"request": "local-service-fixture"})
        idempotency_first = store.record_idempotency("fixture-key", request_digest, "aide://result/local-service-fixture")
        idempotency_duplicate = store.record_idempotency("fixture-key", request_digest, "aide://result/local-service-fixture")
        idempotency_conflict_refused = False
        try:
            store.record_idempotency("fixture-key", digest_json({"request": "conflict"}), "aide://result/local-service-fixture")
        except LocalServiceError as exc:
            idempotency_conflict_refused = str(exc) == "idempotency_conflict"

        store.close()
        reopened = SQLiteStore(root / "state.sqlite")
        try:
            reopened_health = reopened.health()
            reopened_object = reopened.get_object(work_ref)
            reopened_events = reopened.read_events_after(0)
            reopened_metadata = reopened.get_artifact_metadata(artifact_write.digest)
        finally:
            reopened.close()

        future_migration_refused = _future_migration_refused(root)
        corruption_refused = _corruption_refused(root)
        after_status = git_status(repo_root)
        report = {
            "status": "PASS_WITH_WARNINGS",
            "task_id": TASK_ID,
            "capability_label": PROPOSED_CAPABILITY_LABEL,
            "recommended_next_task": CHECK_TASK_ID,
            "schema_version": schema_version,
            "migration_idempotent": migration_rerun_version == schema_version,
            "future_migration_refused": future_migration_refused,
            "health": health,
            "object_put_get_list": bool(stored.version == 1 and read_back.body == work_body and len(listed) == 1),
            "resource_version_conflict_refused": version_conflict_refused,
            "atomic_object_event_sequence": atomic_sequence,
            "atomic_object_event_committed": atomic_object.version == 1 and atomic_sequence == 1,
            "rollback_on_error": rollback_on_error and rollback_absent,
            "event_sequences": [item["sequence"] for item in events_after_zero],
            "monotonic_events": [item["sequence"] for item in events_after_zero] == [1, 2],
            "event_delivery_semantics": "at_least_once",
            "cursor_acknowledgment": cursor,
            "artifact_write_read": payload_readback == payload,
            "artifact_digest": artifact_write.digest,
            "artifact_deduplicated": duplicate_artifact.deduplicated,
            "artifact_metadata": artifact_metadata,
            "artifact_digest_mismatch_refused": digest_mismatch_refused,
            "artifact_path_traversal_refused": traversal_refused,
            "idempotency_first": idempotency_first,
            "idempotency_duplicate": idempotency_duplicate,
            "idempotency_conflict_refused": idempotency_conflict_refused,
            "reopen_persistence": reopened_health["status"] == "PASS" and reopened_object.body == work_body and len(reopened_events) == 2 and reopened_metadata == artifact_metadata,
            "corruption_refused": corruption_refused,
            "source_checkout_unchanged": before_status == after_status,
            "local_state_committed": False,
            "runtime_state_root": "temporary" if state_root is None else "operator-provided",
            "fixture_state_removed": state_root is None,
            **boundary_flags(),
        }
    finally:
        try:
            store.close()
        except Exception:
            pass
        if temp_owner is not None:
            temp_owner.cleanup()

    if write_reports:
        write_reports_for_fixture(repo_root, report)
    return report


def status(repo_root: Path) -> dict[str, Any]:
    report_exists = (repo_root / VALIDATION_JSON).is_file()
    data = {
        "status": "PASS_WITH_WARNINGS" if report_exists else "NOT_RUN",
        "task_id": TASK_ID,
        "capability_label": PROPOSED_CAPABILITY_LABEL,
        "report_exists": report_exists,
        "local_state_path": ".aide.local/service",
        "local_state_committed": False,
        "recommended_next_task": CHECK_TASK_ID,
        **boundary_flags(),
    }
    if report_exists:
        try:
            validation = json.loads((repo_root / VALIDATION_JSON).read_text(encoding="utf-8"))
            data.update({"validation_status": validation.get("status"), "validated": validation.get("validated")})
        except json.JSONDecodeError:
            data.update({"status": "FAIL", "validated": False})
    return data


def write_reports_for_fixture(repo_root: Path, report: dict[str, Any]) -> None:
    validation = validate_fixture_report(report)
    write_json(repo_root / FIXTURE_REPORT_JSON, report)
    write_json(repo_root / VALIDATION_JSON, validation)
    lines = [
        "# Local Service Foundation v0",
        "",
        f"- status: {report.get('status')}",
        f"- capability_label: {PROPOSED_CAPABILITY_LABEL}",
        f"- recommended_next_task: {CHECK_TASK_ID}",
        f"- event_delivery_semantics: {report.get('event_delivery_semantics')}",
        f"- source_checkout_unchanged: {str(report.get('source_checkout_unchanged', False)).lower()}",
        f"- local_state_committed: {str(report.get('local_state_committed', True)).lower()}",
        "",
        "## Non-Capabilities",
        "",
    ]
    lines.extend(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES)
    (repo_root / STATUS_MD).parent.mkdir(parents=True, exist_ok=True)
    (repo_root / STATUS_MD).write_text("\n".join(lines) + "\n", encoding="utf-8")
    (repo_root / VALIDATION_MD).write_text(render_validation_markdown(validation), encoding="utf-8")
    (repo_root / EXPLICIT_NON_CAPABILITIES_MD).write_text("\n".join(["# Explicit Non-Capabilities", "", *[f"- {item}" for item in EXPLICIT_NON_CAPABILITIES]]) + "\n", encoding="utf-8")
    (repo_root / NEXT_TASK_PROMPT_MD).write_text(
        "\n".join(
            [
                "# Next Task Prompt",
                "",
                "```text",
                "Create and process AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01.",
                "Independently verify local_service_foundation_v0 without repairing implementation.",
                "If material findings remain, recommend AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-REPAIR-01.",
                "If pass, recommend AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01.",
                "```",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def validate_fixture_report(report: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "migration_idempotent": report.get("migration_idempotent") is True,
        "future_migration_refused": report.get("future_migration_refused") is True,
        "object_put_get_list": report.get("object_put_get_list") is True,
        "resource_version_conflict_refused": report.get("resource_version_conflict_refused") is True,
        "atomic_object_event_committed": report.get("atomic_object_event_committed") is True,
        "rollback_on_error": report.get("rollback_on_error") is True,
        "monotonic_events": report.get("monotonic_events") is True and report.get("event_sequences") == [1, 2],
        "at_least_once_only": report.get("event_delivery_semantics") == "at_least_once",
        "artifact_write_read": report.get("artifact_write_read") is True,
        "artifact_deduplicated": report.get("artifact_deduplicated") is True,
        "artifact_digest_mismatch_refused": report.get("artifact_digest_mismatch_refused") is True,
        "artifact_path_traversal_refused": report.get("artifact_path_traversal_refused") is True,
        "idempotency_duplicate": report.get("idempotency_duplicate", {}).get("status") == "duplicate",
        "idempotency_conflict_refused": report.get("idempotency_conflict_refused") is True,
        "reopen_persistence": report.get("reopen_persistence") is True,
        "corruption_refused": report.get("corruption_refused") is True,
        "source_checkout_unchanged": report.get("source_checkout_unchanged") is True,
        "false_boundaries": all(report.get(field) is False for field in FALSE_BOUNDARY_FIELDS),
    }
    errors = [name for name, passed in checks.items() if not passed]
    return {
        "status": "PASS_WITH_WARNINGS" if not errors else "FAIL",
        "validated": not errors,
        "task_id": TASK_ID,
        "capability_label": PROPOSED_CAPABILITY_LABEL,
        "recommended_next_task": CHECK_TASK_ID,
        "checks": checks,
        "validation_errors": errors,
        "warnings": [
            "Local Service foundation v0 is single-machine and no-network.",
            "Delivery semantics are at-least-once only, not exactly-once.",
        ],
        **boundary_flags(),
    }


def render_validation_markdown(validation: dict[str, Any]) -> str:
    lines = [
        "# Local Service Foundation Validation",
        "",
        f"- status: {validation.get('status')}",
        f"- validated: {str(validation.get('validated', False)).lower()}",
        f"- recommended_next_task: {validation.get('recommended_next_task')}",
        "",
        "## Checks",
        "",
    ]
    for name, passed in validation.get("checks", {}).items():
        lines.append(f"- {name}: {'PASS' if passed else 'FAIL'}")
    return "\n".join(lines) + "\n"


def validate_reports(repo_root: Path) -> dict[str, Any]:
    report_path = repo_root / FIXTURE_REPORT_JSON
    if not report_path.is_file():
        return {
            "status": "FAIL",
            "validated": False,
            "reason_code": "local_service_report_missing",
            "recommended_next_task": TASK_ID,
            **boundary_flags(),
        }
    report = json.loads(report_path.read_text(encoding="utf-8"))
    validation = validate_fixture_report(report)
    write_json(repo_root / VALIDATION_JSON, validation)
    (repo_root / VALIDATION_MD).write_text(render_validation_markdown(validation), encoding="utf-8")
    return validation


def reset_fixture(repo_root: Path) -> dict[str, Any]:
    report_dir = repo_root / REPORT_ROOT
    if report_dir.exists():
        shutil.rmtree(report_dir)
    return {
        "status": "PASS",
        "removed_report_dir": True,
        "local_state_removed": False,
        "recommended_next_task": TASK_ID,
        **boundary_flags(),
    }
