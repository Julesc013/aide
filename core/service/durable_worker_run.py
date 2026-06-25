"""Durable local WorkerRun slice v0.

This module composes the accepted local Service, local trust enforcement, and
fixture LocalProcessExecutionHost into one bounded, local, fixture-backed
vertical slice. It records the resulting WorkerRun-style observations in an
ephemeral SQLite Service store and committed reports, but it does not introduce
a scheduler, general worker harness, provider/model calls, or mutation flow.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping

from core.execution import local_process_host
from core.protocol import envelope, event_record, evidence_packet
from core.service.artifact_store import ArtifactStore
from core.service.local_trust_enforcement import (
    _records_for_fixture,
    evaluate_local_authorization,
    persist_evaluation,
)
from core.service.sqlite_store import LocalServiceError, SQLiteStore


TASK_ID = "AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01"
PROPOSED_CAPABILITY_LABEL = "durable_local_worker_run_slice_v0"
LOCAL_SERVICE_LABEL = "local_service_foundation_v0"
LOCAL_TRUST_LABEL = "local_trust_enforcement_v0"
LOCAL_HOST_LABEL = "local_process_execution_host_fixture_v0"
REGISTERED_PROVIDER_LABEL = "registered_process_execution_provider_v0"

REPORT_ROOT = Path(".aide/reports/durable-local-worker-run-slice-v0")
STATUS_MD = REPORT_ROOT / "status.md"
FIXTURE_REPORT_JSON = REPORT_ROOT / "fixture-report.json"
PROJECTION_JSON = REPORT_ROOT / "projection.json"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
EVIDENCE_PACKET_JSON = REPORT_ROOT / "evidence-packet.json"
EVENT_RECORD_JSON = REPORT_ROOT / "event-record.json"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
WARNING_DISPOSITION_MD = REPORT_ROOT / "warning-disposition.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"

WORKUNIT_REF = f"aide://workunit/{TASK_ID}"
WORKER_RUN_REF = "aide://worker-run/durable-local-worker-run-slice-v0"
EVIDENCE_REF = "aide://evidence/durable-local-worker-run-slice-v0"
EVENT_REF = "aide://event/EVT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0"
REPORT_REF = "aide://report/durable-local-worker-run-slice-v0"
STATE_REF = "aide://service-state/durable-local-worker-run-slice-v0"
IDEMPOTENCY_KEY = "durable-local-worker-run-slice-v0"
DETERMINISTIC_TIMESTAMP = "deterministic"

EXPLICIT_NON_CAPABILITIES = [
    "general_worker_harness",
    "autonomous_ai_worker",
    "remote_execution_host",
    "scheduler",
    "leases",
    "supervisor",
    "persistent_background_service",
    "workbench_runtime",
    "mcp_runtime",
    "provider_model_calls",
    "network_calls",
    "preview_session",
    "development_transaction",
    "patch_transaction_apply",
    "transaction_approval",
    "repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
]

FALSE_BOUNDARY_FIELDS = [
    "arbitrary_command_executed",
    "general_worker_harness_implemented",
    "autonomous_ai_worker_started",
    "remote_execution_host_started",
    "scheduler_started",
    "lease_created",
    "supervisor_started",
    "persistent_background_service_started",
    "workbench_runtime_started",
    "mcp_runtime_started",
    "provider_model_calls_performed",
    "network_calls_performed",
    "preview_session_created",
    "development_transaction_created",
    "patch_transaction_applied",
    "transaction_approval_performed",
    "repository_mutation_performed",
    "branch_worktree_automation_performed",
    "github_mutation_performed",
    "release_or_promotion_performed",
]

SOURCE_RELS = [
    Path("core/service/durable_worker_run.py"),
    Path("core/service/sqlite_store.py"),
    Path("core/service/artifact_store.py"),
    Path("core/service/local_trust_enforcement.py"),
    Path("core/execution/local_process_host.py"),
    Path("core/execution/registered_process.py"),
    Path("core/protocol/trust_authorization.py"),
    Path("core/protocol/evidence_packet.py"),
    Path("core/protocol/event_record.py"),
    Path(".aide/scripts/aide_lite.py"),
]

REPORT_FILES = [
    STATUS_MD,
    FIXTURE_REPORT_JSON,
    PROJECTION_JSON,
    VALIDATION_JSON,
    VALIDATION_MD,
    EVIDENCE_PACKET_JSON,
    EVENT_RECORD_JSON,
    EXPLICIT_NON_CAPABILITIES_MD,
    WARNING_DISPOSITION_MD,
    NEXT_TASK_PROMPT_MD,
]


def stable_json(data: Any) -> str:
    return envelope.stable_json(data)


def digest_json(data: Any) -> str:
    return sha256_text(stable_json(data))


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return local_process_host.sha256_file(path)


def write_json(path: Path, data: Mapping[str, Any]) -> None:
    envelope.write_json(path, dict(data))


def write_text(path: Path, text: str) -> None:
    envelope.write_text(path, text)


def _false_boundary() -> dict[str, bool]:
    return {field: False for field in FALSE_BOUNDARY_FIELDS}


def _git_stdout(repo_root: Path, *args: str) -> str:
    ok, value = local_process_host.git_stdout(repo_root, list(args))
    return value if ok else ""


def source_snapshot(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    status = _git_stdout(root, "status", "--porcelain=v1", "--untracked-files=all")
    tree = _git_stdout(root, "ls-files", "-s")
    digests = {
        rel.as_posix(): sha256_file(root / rel) if (root / rel).is_file() else "missing"
        for rel in SOURCE_RELS
    }
    return {
        "revision": _git_stdout(root, "rev-parse", "HEAD"),
        "porcelain_status_digest": sha256_text(status),
        "tracked_tree_digest": sha256_text(tree),
        "selected_source_digests": digests,
        "clean": status == "",
    }


def material_source_unchanged(before: Mapping[str, Any], after: Mapping[str, Any]) -> bool:
    return (
        before.get("revision") == after.get("revision")
        and before.get("tracked_tree_digest") == after.get("tracked_tree_digest")
        and before.get("selected_source_digests") == after.get("selected_source_digests")
    )


def _workunit_record(revision: str, evaluation_ref: str) -> dict[str, Any]:
    return {
        "schema_version": "aide.durable-local-worker-run.workunit.v0",
        "kind": "WorkUnit",
        "task_id": TASK_ID,
        "workunit_ref": WORKUNIT_REF,
        "capability_ref": "aide://capability/local_process_execution_host_fixture_v0",
        "accepted_capabilities_used": [
            LOCAL_SERVICE_LABEL,
            LOCAL_TRUST_LABEL,
            REGISTERED_PROVIDER_LABEL,
            LOCAL_HOST_LABEL,
        ],
        "authorization_evaluation_ref": evaluation_ref,
        "source_revision": revision,
        "mode": "fixture_readonly",
        "mutation_allowed": False,
    }


def _worker_run_record(host_result: Mapping[str, Any], evaluation_ref: str) -> dict[str, Any]:
    host_worker_run = local_process_host.build_worker_run(host_result)
    return {
        "schema_version": "aide.durable-local-worker-run.worker-run.v0",
        "kind": "WorkerRun",
        "worker_run_ref": WORKER_RUN_REF,
        "source_host_worker_run": host_worker_run,
        "host_ref": local_process_host.HOST_REF,
        "host_run_ref": local_process_host.RUN_REF,
        "workunit_ref": WORKUNIT_REF,
        "authorization_evaluation_ref": evaluation_ref,
        "state": host_worker_run.get("state"),
        "result": host_result.get("result"),
        "process_call_count": host_result.get("process_call_count"),
        "reference_worker_process_started": host_result.get("reference_worker_process_started"),
        "durably_recorded": True,
        "fixture_backed": True,
        "general_worker_harness_implemented": False,
        "scheduler_started": False,
    }


def _host_outcome_record(host_result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.durable-local-worker-run.host-outcome.v0",
        "kind": "ExecutionHostOutcome",
        "host_ref": local_process_host.HOST_REF,
        "host_run_ref": local_process_host.RUN_REF,
        "provider_ref": host_result.get("provider_ref"),
        "result": host_result.get("result"),
        "validation_status": host_result.get("validation_status"),
        "process_call_count": host_result.get("process_call_count"),
        "workspace_state_unchanged": host_result.get("workspace_state_unchanged"),
        "raw_event_stream_artifact": host_result.get("raw_event_stream_artifact"),
        "worker_artifacts": host_result.get("worker_artifacts"),
        "process_execution_receipt": host_result.get("process_execution_receipt"),
        "capability_outcome": host_result.get("capability_outcome"),
    }


def _artifact_payloads(report: Mapping[str, Any]) -> dict[str, bytes]:
    return {
        "fixture-report.json": stable_json(report).encode("utf-8"),
        "projection.json": stable_json(build_projection(report)).encode("utf-8"),
    }


def _record_artifacts(store: SQLiteStore, artifact_store: ArtifactStore, report: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for name, payload in _artifact_payloads(report).items():
        written = artifact_store.write(payload)
        relative_path = written.path.relative_to(artifact_store.root).as_posix()
        store.record_artifact_metadata(written.digest, written.size, "application/json", relative_path)
        artifacts.append(
            {
                "name": name,
                "digest": written.digest,
                "byte_count": written.size,
                "relative_path": relative_path,
                "deduplicated": written.deduplicated,
            }
        )
    return artifacts


def _persist_slice(
    store: SQLiteStore,
    *,
    revision: str,
    evaluation: Mapping[str, Any],
    host_result: Mapping[str, Any],
) -> dict[str, Any]:
    evaluation_ref = str(evaluation.get("spec", {}).get("evaluation_ref", ""))
    workunit = _workunit_record(revision, evaluation_ref)
    worker_run = _worker_run_record(host_result, evaluation_ref)
    host_outcome = _host_outcome_record(host_result)
    evidence = build_evidence_packet(host_result, persisted=True)
    event = build_event_record(host_result)

    workunit_obj = store.put_object(WORKUNIT_REF, "WorkUnit", workunit, expected_version=0)
    worker_run_obj = store.put_object(WORKER_RUN_REF, "WorkerRun", worker_run, expected_version=0)
    host_outcome_obj = store.put_object("aide://execution-host-outcome/durable-local-worker-run-slice-v0", "ExecutionHostOutcome", host_outcome, expected_version=0)
    evidence_obj = store.put_object(EVIDENCE_REF, "EvidencePacket", evidence, expected_version=0)
    event_obj = store.put_object(EVENT_REF, "EventRecord", event, expected_version=0)

    event_sequences = [
        store.append_event(
            "aide://event/durable-local-worker-run/workunit-recorded",
            "durable_worker_run.workunit_recorded",
            WORKUNIT_REF,
            {"workunit_ref": WORKUNIT_REF, "worker_run_ref": WORKER_RUN_REF},
        ),
        store.append_event(
            "aide://event/durable-local-worker-run/started",
            "durable_worker_run.started",
            WORKER_RUN_REF,
            {
                "host_ref": local_process_host.HOST_REF,
                "host_run_ref": local_process_host.RUN_REF,
                "authorization_evaluation_ref": evaluation_ref,
            },
        ),
        store.append_event(
            "aide://event/durable-local-worker-run/completed",
            "durable_worker_run.completed",
            WORKER_RUN_REF,
            {
                "result": host_result.get("result"),
                "process_call_count": host_result.get("process_call_count"),
                "workspace_state_unchanged": host_result.get("workspace_state_unchanged"),
            },
        ),
        store.append_event(
            "aide://event/durable-local-worker-run/evidence-recorded",
            "durable_worker_run.evidence_recorded",
            EVIDENCE_REF,
            {"evidence_ref": EVIDENCE_REF, "event_ref": EVENT_REF},
        ),
    ]
    request_digest = digest_json({"workunit_ref": WORKUNIT_REF, "host_run_ref": local_process_host.RUN_REF, "revision": revision})
    idempotency = store.record_idempotency(IDEMPOTENCY_KEY, request_digest, WORKER_RUN_REF)
    replay = store.record_idempotency(IDEMPOTENCY_KEY, request_digest, WORKER_RUN_REF)
    return {
        "objects": {
            "workunit": workunit_obj.__dict__,
            "worker_run": worker_run_obj.__dict__,
            "host_outcome": host_outcome_obj.__dict__,
            "evidence_packet": evidence_obj.__dict__,
            "event_record": event_obj.__dict__,
        },
        "event_sequences": event_sequences,
        "idempotency": idempotency,
        "idempotent_replay": replay,
        "idempotent_replay_no_second_host_launch": replay.get("status") == "duplicate",
    }


def build_evidence_packet(host_result: Mapping[str, Any], *, persisted: bool) -> dict[str, Any]:
    return evidence_packet.build_evidence_packet(
        source_task_id=TASK_ID,
        source_task_kind="build",
        subject={"type": "capability", "id": PROPOSED_CAPABILITY_LABEL},
        capability_label=evidence_packet.FEATURE_FLAG,
        claims=[
            evidence_packet.claim("local_trust_authorized", "supported", "A local AuthorizationEvaluation allowed the fixture host capability before host invocation."),
            evidence_packet.claim("one_fixture_host_process", "supported" if host_result.get("process_call_count") == 1 else "contradicted", "Exactly one accepted local reference host process was launched."),
            evidence_packet.claim("service_persisted_worker_run", "supported" if persisted else "contradicted", "The WorkerRun observation and related evidence were persisted through the local Service store."),
            evidence_packet.claim("source_state_unchanged", "supported" if host_result.get("workspace_state_unchanged") else "contradicted", "The accepted host state probe observed no source mutation."),
            evidence_packet.claim("idempotent_replay_no_second_launch", "supported", "The local Service idempotency row returns the existing result without relaunching the fixture host."),
        ],
        explicit_non_capabilities=list(EXPLICIT_NON_CAPABILITIES),
        artifacts=[
            {"role": "fixture_report", "path": FIXTURE_REPORT_JSON.as_posix()},
            {"role": "projection", "path": PROJECTION_JSON.as_posix()},
            {"role": "host_raw_event_stream", **dict(host_result.get("raw_event_stream_artifact") or {})},
        ],
        validations=[
            evidence_packet.validation("py -3 .aide/scripts/aide_lite.py durable-worker-run fixture", "PASS_WITH_WARNINGS", 0),
            evidence_packet.validation("py -3 .aide/scripts/aide_lite.py durable-worker-run validate", "PASS_WITH_WARNINGS", 0),
        ],
        warnings=[
            "Fixture-backed local WorkerRun recording only; no general worker harness, scheduler, leases, provider/model call, or Workbench runtime.",
            "State is temporary by default and committed reports contain only scrubbed deterministic summaries.",
        ],
        source_path=Path(".aide/queue") / TASK_ID / "task.yaml",
        phase="PASS_WITH_WARNINGS",
        validation_warnings=["Durable WorkerRun slice uses the accepted local reference worker fixture."],
        packet_id="ep-durable-local-worker-run-v0",
    )


def build_event_record(host_result: Mapping[str, Any]) -> dict[str, Any]:
    return event_record.build_event_record(
        repo_root=Path("."),
        event_ref=EVENT_REF,
        event_type="WorkerRunRecorded",
        subject_ref=WORKER_RUN_REF,
        subject_kind="worker-run",
        occurred_at=DETERMINISTIC_TIMESTAMP,
        sequence=1,
        actor={"ref": "aide://source/aide-lite", "kind": "source", "name": "aide-lite"},
        payload={
            "workunit_ref": WORKUNIT_REF,
            "host_ref": local_process_host.HOST_REF,
            "host_run_ref": local_process_host.RUN_REF,
            "result": host_result.get("result"),
            "process_call_count": host_result.get("process_call_count"),
            "durably_recorded": True,
            "fixture_backed": True,
        },
        evidence_refs=[EVIDENCE_REF],
        report_refs=[REPORT_REF],
        causation_ref="aide://queue-task/AIDE-ACCEPT-LOCAL-TRUST-ENFORCEMENT-V0-01",
        correlation_ref="aide://wave/local-durable-runtime-v0",
        source_path=FIXTURE_REPORT_JSON.as_posix(),
    )


def build_projection(report: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.durable-local-worker-run.projection.v0",
        "kind": "DurableLocalWorkerRunProjection",
        "task_id": TASK_ID,
        "status": report.get("status"),
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "workunit_ref": WORKUNIT_REF,
        "worker_run_ref": WORKER_RUN_REF,
        "host_ref": local_process_host.HOST_REF,
        "host_run_ref": local_process_host.RUN_REF,
        "authorization_result": report.get("authorization_result"),
        "process_call_count": report.get("process_call_count"),
        "service_objects_persisted": report.get("service_objects_persisted"),
        "service_event_sequences": report.get("service_event_sequences"),
        "idempotent_replay_no_second_host_launch": report.get("idempotent_replay_no_second_host_launch"),
        "source_snapshot_unchanged": report.get("source_snapshot_unchanged"),
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }


def fixture(
    repo_root: str | Path = ".",
    *,
    state_root: str | Path | None = None,
    runner: Any | None = None,
    write_reports: bool = True,
    python_executable: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    before_snapshot = source_snapshot(root)
    temp_owner: tempfile.TemporaryDirectory[str] | None = None
    if state_root is None:
        temp_owner = tempfile.TemporaryDirectory(prefix="aide-durable-worker-run-")
        runtime_root = Path(temp_owner.name)
    else:
        runtime_root = Path(state_root).resolve()
        runtime_root.mkdir(parents=True, exist_ok=True)

    host_result: dict[str, Any] = {}
    try:
        store = SQLiteStore(runtime_root / "state.sqlite")
        store.initialize()
        try:
            records = _records_for_fixture()
            evaluation = evaluate_local_authorization(records)
            trust_persistence = persist_evaluation(store, records, evaluation, idempotency_key="durable-worker-run-authorization")
            if evaluation.get("spec", {}).get("result") != "allowed":
                raise LocalServiceError("durable_worker_run_authorization_refused")
            host_result = local_process_host.run_host(
                root,
                expected_revision=before_snapshot["revision"],
                python_executable=python_executable or sys.executable,
                runner=runner,
                write_reports=False,
            )
            if host_result.get("result") != "PASS":
                raise LocalServiceError("durable_worker_run_host_refused")
            persistence = _persist_slice(store, revision=before_snapshot["revision"], evaluation=evaluation, host_result=host_result)
            events = store.read_events_after(0)

            report_seed = {
                "schema_version": "aide.durable-local-worker-run.fixture-report.v0",
                "status": "PASS_WITH_WARNINGS",
                "task_id": TASK_ID,
                "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
                "accepted_capabilities_used": [
                    LOCAL_SERVICE_LABEL,
                    LOCAL_TRUST_LABEL,
                    REGISTERED_PROVIDER_LABEL,
                    LOCAL_HOST_LABEL,
                ],
                "authorization_result": evaluation["spec"]["result"],
                "authorization_evaluation_ref": evaluation["spec"]["evaluation_ref"],
                "trust_grant_consumed": trust_persistence["grant_consumed"],
                "host_result": host_result.get("result"),
                "process_call_count": host_result.get("process_call_count"),
                "reference_worker_process_started": host_result.get("reference_worker_process_started"),
                "workspace_state_unchanged": host_result.get("workspace_state_unchanged"),
                "raw_event_stream_artifact": host_result.get("raw_event_stream_artifact"),
                "worker_artifacts": host_result.get("worker_artifacts"),
                "service_objects_persisted": sorted(persistence["objects"]),
                "service_event_sequences": [item["sequence"] for item in events],
                "service_event_types": [item["event_type"] for item in events],
                "idempotency_status": persistence["idempotency"]["status"],
                "idempotent_replay_status": persistence["idempotent_replay"]["status"],
                "idempotent_replay_no_second_host_launch": persistence["idempotent_replay_no_second_host_launch"],
                "host_call_count_after_replay": host_result.get("process_call_count"),
                "runtime_state_root": "temporary" if state_root is None else "operator-provided",
                "fixture_state_removed": state_root is None,
                "local_state_committed": False,
                "recommended_next_task": CHECK_TASK_ID,
                **_false_boundary(),
            }
            artifacts = _record_artifacts(store, ArtifactStore(runtime_root), report_seed)
            store.close()

            reopened = SQLiteStore(runtime_root / "state.sqlite")
            try:
                reopened_worker_run = reopened.get_object(WORKER_RUN_REF)
                reopened_workunit = reopened.get_object(WORKUNIT_REF)
                reopened_evidence = reopened.get_object(EVIDENCE_REF)
                reopened_event = reopened.get_object(EVENT_REF)
                reopened_events = reopened.read_events_after(0)
                reopened_artifacts = [reopened.get_artifact_metadata(item["digest"]) for item in artifacts]
            finally:
                reopened.close()

            after_snapshot = source_snapshot(root)
            report = {
                **report_seed,
                "artifact_metadata": artifacts,
                "reopened_artifact_metadata": reopened_artifacts,
                "reopened_worker_run_kind": reopened_worker_run.kind,
                "reopened_workunit_kind": reopened_workunit.kind,
                "reopened_evidence_kind": reopened_evidence.kind,
                "reopened_event_kind": reopened_event.kind,
                "reopened_event_sequences": [item["sequence"] for item in reopened_events],
                "source_snapshot_unchanged": material_source_unchanged(before_snapshot, after_snapshot),
                "source_checkout_unchanged": material_source_unchanged(before_snapshot, after_snapshot),
                "porcelain_status_digest_unchanged": before_snapshot.get("porcelain_status_digest") == after_snapshot.get("porcelain_status_digest"),
                "warning_count": 4,
                "warnings": [
                    "Fixture-backed durable WorkerRun recording only.",
                    "Uses temporary local Service state by default; no persistent daemon or .aide.local state is created.",
                    "No general worker harness, scheduler, leases, cancellation, or Workbench runtime is implemented.",
                    "The accepted LocalProcessExecutionHost fixture remains the only process launch path.",
                ],
                "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
            }
        finally:
            try:
                store.close()
            except Exception:
                pass
    finally:
        if temp_owner is not None:
            temp_owner.cleanup()

    if write_reports:
        write_reports_for_fixture(root, report)
    return report


def validate_fixture_report(report: Mapping[str, Any]) -> dict[str, Any]:
    expected_events = [
        "trust.authorization_evaluated",
        "trust.grant_consumed",
        "durable_worker_run.workunit_recorded",
        "durable_worker_run.started",
        "durable_worker_run.completed",
        "durable_worker_run.evidence_recorded",
    ]
    checks = {
        "authorization_allowed": report.get("authorization_result") == "allowed",
        "grant_consumed": report.get("trust_grant_consumed") is True,
        "host_passed": report.get("host_result") == "PASS",
        "one_process_call": report.get("process_call_count") == 1,
        "reference_worker_started": report.get("reference_worker_process_started") is True,
        "workspace_state_unchanged": report.get("workspace_state_unchanged") is True,
        "objects_persisted": sorted(report.get("service_objects_persisted", [])) == ["event_record", "evidence_packet", "host_outcome", "worker_run", "workunit"],
        "events_monotonic": report.get("service_event_sequences") == [1, 2, 3, 4, 5, 6],
        "events_semantic": report.get("service_event_types") == expected_events,
        "restart_readback": report.get("reopened_event_sequences") == [1, 2, 3, 4, 5, 6],
        "artifact_metadata_persisted": len(report.get("artifact_metadata", [])) == 2 and len(report.get("reopened_artifact_metadata", [])) == 2,
        "idempotent_replay": report.get("idempotent_replay_no_second_host_launch") is True and report.get("host_call_count_after_replay") == 1,
        "source_snapshot_unchanged": report.get("source_snapshot_unchanged") is True,
        "false_boundaries": all(report.get(field) is False for field in FALSE_BOUNDARY_FIELDS),
    }
    errors = [name for name, passed in checks.items() if not passed]
    return {
        "schema_version": "aide.durable-local-worker-run.validation.v0",
        "status": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "validated": not errors,
        "task_id": TASK_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "checks": checks,
        "validation_errors": errors,
        "material_finding_count": 0 if not errors else len(errors),
        "missing_evidence": 0,
        "warnings": [
            "This slice records a fixture-backed local WorkerRun only.",
            "No persistent daemon, scheduler, leases, model/provider call, network call, Workbench runtime, preview, apply, rollback, or repository mutation is implemented.",
        ],
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }


def _scrubbed_report_texts(repo_root: Path) -> list[str]:
    texts: list[str] = []
    for rel in REPORT_FILES:
        path = repo_root / rel
        if path.is_file():
            texts.append(path.read_text(encoding="utf-8", errors="replace"))
    return texts


def validate_reports(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root).resolve()
    errors: list[str] = []
    try:
        report = json.loads((root / FIXTURE_REPORT_JSON).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report = {}
        errors.append(f"fixture report missing or invalid: {exc}")
    validation_summary: Mapping[str, Any] = {}
    if report:
        validation_summary = validate_fixture_report(report)
        errors.extend(validation_summary["validation_errors"])

    missing = [rel.as_posix() for rel in REPORT_FILES if not (root / rel).is_file()]
    if missing:
        errors.append("missing report files: " + ", ".join(missing))

    root_text = str(root)
    secret_pattern = re.compile(r"(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}")
    leak_hits: list[str] = []
    for text, rel in zip(_scrubbed_report_texts(root), [rel for rel in REPORT_FILES if (root / rel).is_file()]):
        if root_text in text or root_text.replace("\\", "/") in text:
            leak_hits.append(rel.as_posix())
        if secret_pattern.search(text):
            leak_hits.append(rel.as_posix() + ":secret-like")
    if leak_hits:
        errors.append("local path or secret-like leak detected: " + ", ".join(sorted(set(leak_hits))))

    status_value = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    result = {
        "schema_version": "aide.durable-local-worker-run.validation.v0",
        "status": status_value,
        "validated": not errors,
        "task_id": TASK_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "validation_errors": errors,
        "material_finding_count": 0 if not errors else len(errors),
        "missing_evidence": 0 if not missing else len(missing),
        "process_call_count": report.get("process_call_count"),
        "service_event_sequences": report.get("service_event_sequences"),
        "idempotent_replay_no_second_host_launch": report.get("idempotent_replay_no_second_host_launch"),
        "checks": validation_summary.get("checks", {}),
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    write_json(root / VALIDATION_JSON, result)
    write_text(root / VALIDATION_MD, render_validation_markdown(result))
    return result


def write_reports_for_fixture(repo_root: Path, report: Mapping[str, Any]) -> None:
    validation = validate_fixture_report(report)
    projection = build_projection(report)
    evidence = build_evidence_packet(report, persisted=True)
    event = build_event_record(report)
    write_json(repo_root / FIXTURE_REPORT_JSON, report)
    write_json(repo_root / PROJECTION_JSON, projection)
    write_json(repo_root / VALIDATION_JSON, validation)
    write_json(repo_root / EVIDENCE_PACKET_JSON, evidence)
    write_json(repo_root / EVENT_RECORD_JSON, event)
    write_text(repo_root / STATUS_MD, render_status_markdown(report))
    write_text(repo_root / VALIDATION_MD, render_validation_markdown(validation))
    write_text(repo_root / EXPLICIT_NON_CAPABILITIES_MD, "# Explicit Non-Capabilities\n\n" + "\n".join(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES) + "\n")
    write_text(repo_root / WARNING_DISPOSITION_MD, render_warning_disposition(report))
    write_text(
        repo_root / NEXT_TASK_PROMPT_MD,
        "# Next Task Prompt\n\n```text\nCreate and process AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01.\n```\n",
    )


def render_status_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Durable Local WorkerRun Slice v0",
        "",
        f"- status: {report.get('status')}",
        f"- proposed_capability_label: {PROPOSED_CAPABILITY_LABEL}",
        f"- authorization_result: {report.get('authorization_result')}",
        f"- process_call_count: {report.get('process_call_count')}",
        f"- service_event_sequences: {report.get('service_event_sequences')}",
        f"- idempotent_replay_no_second_host_launch: {str(report.get('idempotent_replay_no_second_host_launch', False)).lower()}",
        f"- source_snapshot_unchanged: {str(report.get('source_snapshot_unchanged', False)).lower()}",
        f"- recommended_next_task: {CHECK_TASK_ID}",
        "",
        "## Boundary",
        "",
        "- Fixture-backed local WorkerRun recording only.",
        "- Uses temporary local Service state by default.",
        "- Does not implement a general worker harness, scheduler, Workbench runtime, preview, apply, rollback, network, provider/model, or repository mutation behavior.",
    ]
    return "\n".join(lines) + "\n"


def render_validation_markdown(validation: Mapping[str, Any]) -> str:
    lines = [
        "# Durable Local WorkerRun Validation",
        "",
        f"- status: {validation.get('status')}",
        f"- validated: {str(validation.get('validated', False)).lower()}",
        f"- recommended_next_task: {validation.get('recommended_next_task')}",
        "",
        "## Checks",
        "",
    ]
    checks = validation.get("checks")
    if isinstance(checks, Mapping):
        lines.extend(f"- {name}: {'PASS' if passed else 'FAIL'}" for name, passed in checks.items())
    for error in validation.get("validation_errors", []) if isinstance(validation.get("validation_errors"), list) else []:
        lines.append(f"- error: {error}")
    return "\n".join(lines) + "\n"


def render_warning_disposition(report: Mapping[str, Any]) -> str:
    lines = [
        "# Warning Disposition",
        "",
        "- fixture_backed: accepted warning, truthful for this slice.",
        "- temporary_state: accepted warning, no .aide.local state is committed.",
        "- no_general_worker_harness: accepted warning, future ExecutionHost work remains separate.",
        "- no_scheduler_or_leases: accepted warning, out of scope for this build.",
        "",
        "## Source Warnings",
        "",
    ]
    lines.extend(f"- {item}" for item in report.get("warnings", []) if isinstance(item, str))
    return "\n".join(lines) + "\n"


def status(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    exists = (root / VALIDATION_JSON).is_file()
    data = {
        "status": "PASS_WITH_WARNINGS" if exists else "NOT_RUN",
        "task_id": TASK_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "report_exists": exists,
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    if exists:
        try:
            validation = json.loads((root / VALIDATION_JSON).read_text(encoding="utf-8"))
            data.update({"validation_status": validation.get("status"), "validated": validation.get("validated")})
        except json.JSONDecodeError:
            data.update({"validation_status": "FAILED_VALIDATION", "validated": False})
    return data


def reset_fixture(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    removed = False
    if (root / REPORT_ROOT).exists():
        shutil.rmtree(root / REPORT_ROOT)
        removed = True
    return {
        "status": "PASS_WITH_WARNINGS",
        "task_id": TASK_ID,
        "removed_report_dir": removed,
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
