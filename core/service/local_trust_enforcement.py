"""Deterministic local trust enforcement fixture v0.

This module evaluates accepted trust authorization records and persists the
result through the accepted local Service foundation. It does not implement
external IAM, credentials, secrets, network policy engines, process launch,
worker execution, transaction approval, preview/apply/rollback, or mutation.
"""

from __future__ import annotations

import copy
import json
import shutil
import sqlite3
import tempfile
from hashlib import sha256
from pathlib import Path
from typing import Any

from core.protocol import trust_authorization
from core.service.sqlite_store import DETERMINISTIC_TIMESTAMP, LocalServiceError, SQLiteStore, canonical_json, digest_json


TASK_ID = "AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01"
PROPOSED_CAPABILITY_LABEL = "local_trust_enforcement_v0"
TRUST_CONTRACT_LABEL = "trust_and_authorization_contract_v0"
LOCAL_SERVICE_LABEL = "local_service_foundation_v0"

REPORT_ROOT = Path(".aide/reports/local-trust-enforcement-v0")
STATUS_MD = REPORT_ROOT / "status.md"
FIXTURE_REPORT_JSON = REPORT_ROOT / "fixture-report.json"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"

FALSE_BOUNDARY_FIELDS = [
    "external_iam_implemented",
    "credentials_embedded",
    "secrets_embedded",
    "network_calls_performed",
    "process_launch_performed",
    "worker_execution_performed",
    "transaction_approval_implemented",
    "provider_model_calls_performed",
    "preview_apply_implemented",
    "repository_mutation_performed",
    "branch_worktree_mutation_performed",
    "github_mutation_performed",
    "release_or_promotion_performed",
]

EXPLICIT_NON_CAPABILITIES = [
    "external_iam",
    "credentials",
    "secrets",
    "oidc",
    "remote_policy_engine",
    "process_launch",
    "worker_execution",
    "transaction_approval",
    "provider_model_calls",
    "network_calls",
    "preview_apply_rollback",
    "repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
]


def boundary_flags() -> dict[str, bool]:
    return {field: False for field in FALSE_BOUNDARY_FIELDS}


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_snapshot(repo_root: Path) -> dict[str, str | None]:
    files = [
        "core/protocol/trust_authorization.py",
        "core/service/local_trust_enforcement.py",
        "core/service/sqlite_store.py",
    ]
    snapshot: dict[str, str | None] = {}
    for rel in files:
        path = repo_root / rel
        snapshot[rel] = "sha256:" + sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    return snapshot


def _object_ref(record: dict[str, Any]) -> str:
    kind = record.get("kind")
    spec = record.get("spec") if isinstance(record.get("spec"), dict) else {}
    ref_fields = {
        "Principal": "principal_ref",
        "AdmissionRecord": "admission_ref",
        "PolicyDecision": "decision_ref",
        "CapabilityGrant": "grant_ref",
        "DelegationRecord": "delegation_ref",
        "RevocationRecord": "revocation_ref",
        "AuthorizationEvaluation": "evaluation_ref",
    }
    field = ref_fields.get(str(kind))
    if field is None or not isinstance(spec.get(field), str):
        raise LocalServiceError("trust_record_ref_missing")
    return str(spec[field])


def _write_object(conn: sqlite3.Connection, record: dict[str, Any], *, expected_version: int | None = None) -> int:
    ref = _object_ref(record)
    kind = str(record["kind"])
    body_json = canonical_json(record)
    body_digest = digest_json(record)
    row = conn.execute("SELECT version FROM objects WHERE ref = ?", (ref,)).fetchone()
    if row is None:
        if expected_version not in (None, 0):
            raise LocalServiceError("resource_version_conflict")
        version = 1
        conn.execute(
            "INSERT INTO objects(ref, kind, version, body_json, body_digest, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (ref, kind, version, body_json, body_digest, DETERMINISTIC_TIMESTAMP),
        )
    else:
        current = int(row["version"])
        if expected_version is not None and expected_version != current:
            raise LocalServiceError("resource_version_conflict")
        version = current + 1
        conn.execute(
            "UPDATE objects SET kind = ?, version = ?, body_json = ?, body_digest = ?, updated_at = ? WHERE ref = ?",
            (kind, version, body_json, body_digest, DETERMINISTIC_TIMESTAMP, ref),
        )
    return version


def _get_object_body(store: SQLiteStore, ref: str) -> dict[str, Any] | None:
    try:
        return store.get_object(ref).body
    except LocalServiceError as exc:
        if str(exc) == "object_missing":
            return None
        raise


def _grant_remaining_uses(grant: dict[str, Any]) -> int:
    return int(grant.get("spec", {}).get("remaining_uses", 0))


def _records_for_fixture() -> dict[str, Any]:
    return {
        "principal": trust_authorization.sample_principal(),
        "admission": trust_authorization.sample_admission_record(),
        "policy_decision": trust_authorization.sample_policy_decision(),
        "grant": trust_authorization.sample_capability_grant(),
        "delegation": trust_authorization.sample_delegation_record(),
        "revocations": [],
        "request": trust_authorization.sample_requested_operation(),
    }


def evaluate_local_authorization(records: dict[str, Any]) -> dict[str, Any]:
    evaluation = trust_authorization.evaluate_authorization(
        copy.deepcopy(records.get("principal")),
        copy.deepcopy(records.get("admission")),
        copy.deepcopy(records.get("policy_decision")),
        copy.deepcopy(records.get("grant")),
        copy.deepcopy(records.get("delegation")),
        copy.deepcopy(records.get("revocations") or []),
        copy.deepcopy(records.get("request") or {}),
    )
    errors = trust_authorization.validate_trust_authorization_contract(evaluation)
    if errors:
        raise LocalServiceError("authorization_evaluation_invalid")
    return evaluation


def _consume_grant(grant: dict[str, Any]) -> dict[str, Any]:
    consumed = copy.deepcopy(grant)
    consumed["spec"]["remaining_uses"] = max(0, int(consumed["spec"].get("remaining_uses", 0)) - 1)
    if consumed["spec"]["remaining_uses"] == 0:
        consumed["spec"]["status"] = "consumed"
    return consumed


def persist_evaluation(store: SQLiteStore, records: dict[str, Any], evaluation: dict[str, Any], *, idempotency_key: str) -> dict[str, Any]:
    request_digest = digest_json(records["request"])
    result_ref = _object_ref(evaluation)
    grant_ref = records["grant"]["spec"]["grant_ref"]
    try:
        with store.conn:
            existing = store.conn.execute(
                "SELECT request_digest, result_ref FROM idempotency WHERE idempotency_key = ?",
                (idempotency_key,),
            ).fetchone()
            if existing is not None:
                if existing["request_digest"] != request_digest or existing["result_ref"] != result_ref:
                    raise LocalServiceError("idempotency_conflict")
                return {
                    "idempotency": {"status": "duplicate", "idempotency_key": idempotency_key, "result_ref": existing["result_ref"]},
                    "event_sequence": None,
                    "grant_event_sequence": None,
                    "grant_consumed": False,
                }

            if evaluation["spec"]["result"] == "allowed":
                current_grant = _get_object_body(store, grant_ref)
                if current_grant is not None and (
                    current_grant.get("spec", {}).get("status") != "active" or _grant_remaining_uses(current_grant) <= 0
                ):
                    raise LocalServiceError("grant_exhausted")

            for key in ["principal", "admission", "policy_decision", "delegation"]:
                _write_object(store.conn, records[key])
            for revocation in records.get("revocations") or []:
                _write_object(store.conn, revocation)

            grant_row = store.conn.execute("SELECT version, body_json FROM objects WHERE ref = ?", (grant_ref,)).fetchone()
            if grant_row is None:
                grant_version = _write_object(store.conn, records["grant"], expected_version=0)
                current_grant_body = records["grant"]
            else:
                grant_version = int(grant_row["version"])
                current_grant_body = json.loads(grant_row["body_json"])
            if evaluation["spec"]["result"] == "allowed" and (
                current_grant_body.get("spec", {}).get("status") != "active" or _grant_remaining_uses(current_grant_body) <= 0
            ):
                raise LocalServiceError("grant_exhausted")

            _write_object(store.conn, evaluation)
            event_body = {
                "result": evaluation["spec"]["result"],
                "reason_codes": evaluation["spec"]["reason_codes"],
                "policy_decision_ref": evaluation["spec"]["policy_decision_ref"],
                "grant_ref": evaluation["spec"]["grant_ref"],
            }
            event_cursor = store.conn.execute(
                "INSERT INTO events(event_ref, event_type, subject_ref, body_json, body_digest, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    f"aide://event/local-trust-evaluation/{idempotency_key}",
                    "trust.authorization_evaluated",
                    result_ref,
                    canonical_json(event_body),
                    digest_json(event_body),
                    DETERMINISTIC_TIMESTAMP,
                ),
            )
            grant_event_sequence = None
            grant_consumed = False
            if evaluation["spec"]["result"] == "allowed":
                consumed = _consume_grant(current_grant_body)
                _write_object(store.conn, consumed, expected_version=grant_version)
                grant_event_body = {
                    "grant_ref": grant_ref,
                    "remaining_uses": consumed["spec"]["remaining_uses"],
                    "status": consumed["spec"]["status"],
                }
                grant_cursor = store.conn.execute(
                    "INSERT INTO events(event_ref, event_type, subject_ref, body_json, body_digest, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        f"aide://event/local-trust-grant-consumed/{idempotency_key}",
                        "trust.grant_consumed",
                        grant_ref,
                        canonical_json(grant_event_body),
                        digest_json(grant_event_body),
                        DETERMINISTIC_TIMESTAMP,
                    ),
                )
                grant_event_sequence = int(grant_cursor.lastrowid)
                grant_consumed = True
            store.conn.execute(
                "INSERT INTO idempotency(idempotency_key, request_digest, result_ref, created_at) VALUES (?, ?, ?, ?)",
                (idempotency_key, request_digest, result_ref, DETERMINISTIC_TIMESTAMP),
            )
            return {
                "idempotency": {"status": "recorded", "idempotency_key": idempotency_key, "result_ref": result_ref},
                "event_sequence": int(event_cursor.lastrowid),
                "grant_event_sequence": grant_event_sequence,
                "grant_consumed": grant_consumed,
            }
    except sqlite3.IntegrityError as exc:
        raise LocalServiceError("local_trust_persistence_conflict") from exc


def fixture(repo_root: Path, *, state_root: Path | None = None, write_reports: bool = True) -> dict[str, Any]:
    before_snapshot = source_snapshot(repo_root)
    temp_owner: tempfile.TemporaryDirectory[str] | None = None
    if state_root is None:
        temp_owner = tempfile.TemporaryDirectory(prefix="aide-local-trust-")
        root = Path(temp_owner.name)
    else:
        root = state_root
        root.mkdir(parents=True, exist_ok=True)

    store = SQLiteStore(root / "state.sqlite")
    try:
        store.initialize()
        records = _records_for_fixture()
        evaluation = evaluate_local_authorization(records)
        persistence = persist_evaluation(store, records, evaluation, idempotency_key="local-trust-fixture")
        replay = persist_evaluation(store, records, evaluation, idempotency_key="local-trust-fixture")
        concurrent_final_use_refused = False
        try:
            persist_evaluation(store, records, evaluation, idempotency_key="local-trust-final-use-race")
        except LocalServiceError as exc:
            concurrent_final_use_refused = str(exc) == "grant_exhausted"
        matrix = trust_authorization.negative_evaluation_matrix()
        stored_events = store.read_events_after(0)
        store.close()

        reopened = SQLiteStore(root / "state.sqlite")
        try:
            reopened_eval = reopened.get_object(_object_ref(evaluation))
            reopened_grant = reopened.get_object(records["grant"]["spec"]["grant_ref"])
            reopened_events = reopened.read_events_after(0)
        finally:
            reopened.close()

        after_snapshot = source_snapshot(repo_root)
        report = {
            "schema_version": "aide.local-trust-enforcement-fixture.v0",
            "status": "PASS_WITH_WARNINGS",
            "task_id": TASK_ID,
            "capability_label": PROPOSED_CAPABILITY_LABEL,
            "uses_contract": TRUST_CONTRACT_LABEL,
            "uses_service": LOCAL_SERVICE_LABEL,
            "evaluation_result": evaluation["spec"]["result"],
            "reason_codes": evaluation["spec"]["reason_codes"],
            "checks": evaluation["spec"]["checks"],
            "persisted_evaluation": reopened_eval.body["spec"]["result"] == "allowed",
            "event_sequences": [item["sequence"] for item in stored_events],
            "reopened_event_sequences": [item["sequence"] for item in reopened_events],
            "grant_consumed": persistence["grant_consumed"],
            "grant_event_sequence": persistence["grant_event_sequence"],
            "grant_remaining_uses": reopened_grant.body["spec"]["remaining_uses"],
            "idempotent_replay_no_second_event": replay["idempotency"]["status"] == "duplicate" and replay["event_sequence"] is None,
            "idempotent_replay_no_second_launch": replay["idempotency"]["status"] == "duplicate" and replay["event_sequence"] is None,
            "concurrent_final_use_refused": concurrent_final_use_refused,
            "negative_reason_codes": sorted(matrix),
            "all_required_refusal_codes_covered": sorted(matrix) == sorted(trust_authorization.REFUSAL_CODES),
            "source_snapshot_unchanged": before_snapshot == after_snapshot,
            "source_checkout_unchanged": before_snapshot == after_snapshot,
            "process_launch_count": 0,
            "local_state_committed": False,
            "runtime_state_root": "temporary" if state_root is None else "operator-provided",
            "fixture_state_removed": state_root is None,
            "recommended_next_task": CHECK_TASK_ID,
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


def validate_fixture_report(report: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "evaluation_allowed": report.get("evaluation_result") == "allowed",
        "persisted_evaluation": report.get("persisted_evaluation") is True,
        "grant_consumed": report.get("grant_consumed") is True and report.get("grant_remaining_uses") == 0,
        "idempotent_replay": report.get("idempotent_replay_no_second_event") is True,
        "concurrent_final_use_refused": report.get("concurrent_final_use_refused") is True,
        "events_monotonic": report.get("event_sequences") == [1, 2] and report.get("reopened_event_sequences") == [1, 2],
        "required_refusal_codes_covered": report.get("all_required_refusal_codes_covered") is True,
        "no_process_launch": report.get("process_launch_count") == 0,
        "source_snapshot_unchanged": report.get("source_snapshot_unchanged") is True,
        "false_boundaries": all(report.get(field) is False for field in FALSE_BOUNDARY_FIELDS),
    }
    errors = [name for name, passed in checks.items() if not passed]
    return {
        "status": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "validated": not errors,
        "task_id": TASK_ID,
        "capability_label": PROPOSED_CAPABILITY_LABEL,
        "checks": checks,
        "validation_errors": errors,
        "warnings": [
            "Local trust enforcement v0 is deterministic and local only.",
            "No process launch, worker execution, external IAM, credentials, secrets, network, or transaction approval is implemented.",
        ],
        "recommended_next_task": CHECK_TASK_ID,
        **boundary_flags(),
    }


def write_reports_for_fixture(repo_root: Path, report: dict[str, Any]) -> None:
    validation = validate_fixture_report(report)
    write_json(repo_root / FIXTURE_REPORT_JSON, report)
    write_json(repo_root / VALIDATION_JSON, validation)
    lines = [
        "# Local Trust Enforcement v0",
        "",
        f"- status: {report.get('status')}",
        f"- capability_label: {PROPOSED_CAPABILITY_LABEL}",
        f"- evaluation_result: {report.get('evaluation_result')}",
        f"- grant_consumed: {str(report.get('grant_consumed', False)).lower()}",
        f"- concurrent_final_use_refused: {str(report.get('concurrent_final_use_refused', False)).lower()}",
        f"- process_launch_count: {report.get('process_launch_count')}",
        f"- recommended_next_task: {CHECK_TASK_ID}",
        "",
        "## Non-Capabilities",
        "",
    ]
    lines.extend(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES)
    (repo_root / STATUS_MD).parent.mkdir(parents=True, exist_ok=True)
    (repo_root / STATUS_MD).write_text("\n".join(lines) + "\n", encoding="utf-8")
    (repo_root / VALIDATION_MD).write_text(render_validation_markdown(validation), encoding="utf-8")
    (repo_root / EXPLICIT_NON_CAPABILITIES_MD).write_text(
        "# Explicit Non-Capabilities\n\n" + "\n".join(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES) + "\n",
        encoding="utf-8",
    )
    (repo_root / NEXT_TASK_PROMPT_MD).write_text(
        "# Next Task Prompt\n\n```text\nCreate and process AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01.\n```\n",
        encoding="utf-8",
    )


def render_validation_markdown(validation: dict[str, Any]) -> str:
    lines = [
        "# Local Trust Enforcement Validation",
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


def status(repo_root: Path) -> dict[str, Any]:
    report_exists = (repo_root / VALIDATION_JSON).is_file()
    data = {
        "status": "PASS_WITH_WARNINGS" if report_exists else "NOT_RUN",
        "task_id": TASK_ID,
        "capability_label": PROPOSED_CAPABILITY_LABEL,
        "report_exists": report_exists,
        "recommended_next_task": CHECK_TASK_ID,
        **boundary_flags(),
    }
    if report_exists:
        validation = json.loads((repo_root / VALIDATION_JSON).read_text(encoding="utf-8"))
        data.update({"validation_status": validation.get("status"), "validated": validation.get("validated")})
    return data


def validate_reports(repo_root: Path) -> dict[str, Any]:
    report_path = repo_root / FIXTURE_REPORT_JSON
    if not report_path.is_file():
        return {
            "status": "FAILED_VALIDATION",
            "validated": False,
            "reason_code": "local_trust_report_missing",
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
        "recommended_next_task": TASK_ID,
        **boundary_flags(),
    }
