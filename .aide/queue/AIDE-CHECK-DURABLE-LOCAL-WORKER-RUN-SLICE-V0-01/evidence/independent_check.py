from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01"
SOURCE_TASK_ID = "AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01"
PASS_NEXT = "AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01"
REPAIR_NEXT = "AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01"

REPORT_DIR = Path(".aide/reports/durable-local-worker-run-slice-v0-check")
EVIDENCE_DIR = Path(".aide/queue") / TASK_ID / "evidence"
SOURCE_REPORT_DIR = Path(".aide/reports/durable-local-worker-run-slice-v0")
SOURCE_TASK_DIR = Path(".aide/queue") / SOURCE_TASK_ID

FALSE_BOUNDARY_FIELDS = [
    "arbitrary_command_executed",
    "general_worker_harness_implemented",
    "autonomous_ai_worker_started",
    "remote_execution_host_started",
    "scheduler_started",
    "lease_created",
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

EXPECTED_EVENTS = [
    "trust.authorization_evaluated",
    "trust.grant_consumed",
    "durable_worker_run.workunit_recorded",
    "durable_worker_run.started",
    "durable_worker_run.completed",
    "durable_worker_run.evidence_recorded",
]

EXPECTED_OBJECT_KINDS = {
    "AuthorizationEvaluation",
    "CapabilityGrant",
    "PolicyDecision",
    "Principal",
    "AdmissionRecord",
    "WorkUnit",
    "WorkerRun",
    "ExecutionHostOutcome",
    "EvidencePacket",
    "EventRecord",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return "<outside-repo>"


def assertion(
    assertions: list[dict[str, Any]],
    *,
    id: str,
    category: str,
    description: str,
    passed: bool,
    severity: str,
    expected: Any,
    observed: Any,
    evidence_refs: list[str],
    source_finding_id: str | None = None,
) -> None:
    assertions.append(
        {
            "id": id,
            "category": category,
            "description": description,
            "outcome": "PASS" if passed else "FAIL",
            "severity": "none" if passed else severity,
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs,
            "source_finding_id": source_finding_id,
        }
    )


def sqlite_summary(db_path: Path) -> dict[str, Any]:
    con = sqlite3.connect(db_path)
    try:
        tables = [row[0] for row in con.execute("select name from sqlite_master where type='table' order by name")]
        counts = {
            table: con.execute(f"select count(*) from {table}").fetchone()[0]
            for table in tables
            if table != "sqlite_sequence"
        }
        objects = [
            {"ref": row[0], "kind": row[1], "digest": row[2]}
            for row in con.execute("select ref, kind, body_digest from objects order by ref")
        ]
        events = [
            {"sequence": row[0], "event_ref": row[1], "event_type": row[2], "subject_ref": row[3], "digest": row[4]}
            for row in con.execute("select sequence, event_ref, event_type, subject_ref, body_digest from events order by sequence")
        ]
        idempotency = [
            {"key": row[0], "request_digest": row[1], "result_ref": row[2]}
            for row in con.execute("select idempotency_key, request_digest, result_ref from idempotency order by idempotency_key")
        ]
        artifacts = [
            {"digest": row[0], "size": row[1], "media_type": row[2], "relative_path": row[3]}
            for row in con.execute("select digest, size, media_type, relative_path from artifact_metadata order by digest")
        ]
        return {
            "tables": tables,
            "counts": counts,
            "objects": objects,
            "events": events,
            "idempotency": idempotency,
            "artifact_metadata": artifacts,
        }
    finally:
        con.close()


def run_fixture(repo_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    sys.path.insert(0, str(repo_root))
    from core.service import durable_worker_run  # system under test

    runtime_root = EVIDENCE_DIR / "runtime-state"
    if runtime_root.exists():
        shutil.rmtree(runtime_root)
    runtime_root.mkdir(parents=True)
    report = durable_worker_run.fixture(repo_root, state_root=runtime_root, write_reports=False)
    summary = sqlite_summary(runtime_root / "state.sqlite")
    shutil.rmtree(runtime_root)
    return report, summary


def scan_for_leaks(paths: list[Path]) -> list[str]:
    root = str(Path.cwd())
    root_fwd = root.replace("\\", "/")
    secret_pattern = re.compile(r"(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}")
    hits: list[str] = []
    for base in paths:
        if base.is_file():
            candidates = [base]
        else:
            candidates = [path for path in base.rglob("*") if path.is_file()]
        for path in candidates:
            text = path.read_text(encoding="utf-8", errors="replace")
            if root in text or root_fwd in text:
                hits.append(f"{rel(path)}:absolute-path")
            if secret_pattern.search(text):
                hits.append(f"{rel(path)}:secret-like")
    return sorted(set(hits))


def main() -> int:
    repo_root = Path.cwd()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    source_task = read_json(SOURCE_TASK_DIR / "task.yaml") if False else None
    del source_task
    source_fixture = read_json(SOURCE_REPORT_DIR / "fixture-report.json")
    source_projection = read_json(SOURCE_REPORT_DIR / "projection.json")
    source_evidence = read_json(SOURCE_REPORT_DIR / "evidence-packet.json")
    source_event = read_json(SOURCE_REPORT_DIR / "event-record.json")
    source_validation = read_json(SOURCE_REPORT_DIR / "validation.json")

    fresh_report, db_summary = run_fixture(repo_root)
    raw_artifact = fresh_report.get("raw_event_stream_artifact", {})
    worker_artifacts = fresh_report.get("worker_artifacts", [])
    raw_path = repo_root / raw_artifact.get("path", "")
    raw_lines = raw_path.read_text(encoding="utf-8").splitlines() if raw_path.is_file() else []
    parsed_raw_lines = [json.loads(line) for line in raw_lines if line.strip()]

    worker_integrity = []
    for artifact in worker_artifacts:
        path = repo_root / artifact.get("path", "")
        expected = artifact.get("sha256")
        observed = sha256_file(path) if path.is_file() else None
        worker_integrity.append({"path": artifact.get("path"), "expected": expected, "observed": observed, "matches": expected == observed})

    artifact_integrity = []
    for artifact in db_summary["artifact_metadata"]:
        path = EVIDENCE_DIR / "runtime-state" / artifact["relative_path"]
        artifact_integrity.append({"digest": artifact["digest"], "relative_path": artifact["relative_path"], "committed_runtime_copy": path.is_file()})

    object_kinds = {item["kind"] for item in db_summary["objects"]}
    event_types = [item["event_type"] for item in db_summary["events"]]
    event_sequences = [item["sequence"] for item in db_summary["events"]]
    false_boundary_values = {field: fresh_report.get(field) for field in FALSE_BOUNDARY_FIELDS}
    leak_hits = scan_for_leaks([SOURCE_REPORT_DIR, SOURCE_TASK_DIR])

    assertions: list[dict[str, Any]] = []
    assertion(
        assertions,
        id="source_task_complete",
        category="source_chain",
        description="Build task reports PASS_WITH_WARNINGS with no missing evidence.",
        passed=source_fixture.get("status") == "PASS_WITH_WARNINGS" and source_validation.get("validated") is True,
        severity="material",
        expected={"status": "PASS_WITH_WARNINGS", "validated": True},
        observed={"status": source_fixture.get("status"), "validated": source_validation.get("validated")},
        evidence_refs=[rel(SOURCE_REPORT_DIR / "fixture-report.json"), rel(SOURCE_REPORT_DIR / "validation.json")],
    )
    assertion(
        assertions,
        id="fresh_fixture_one_process",
        category="runtime_observation",
        description="Fresh task-local fixture run launches exactly one accepted local reference host process.",
        passed=fresh_report.get("process_call_count") == 1 and fresh_report.get("reference_worker_process_started") is True,
        severity="material",
        expected={"process_call_count": 1, "reference_worker_process_started": True},
        observed={"process_call_count": fresh_report.get("process_call_count"), "reference_worker_process_started": fresh_report.get("reference_worker_process_started")},
        evidence_refs=[rel(EVIDENCE_DIR / "independent-check-output.json")],
    )
    assertion(
        assertions,
        id="authorization_before_launch",
        category="authority",
        description="Fresh fixture records allowed local authorization and one-use grant consumption.",
        passed=fresh_report.get("authorization_result") == "allowed" and fresh_report.get("trust_grant_consumed") is True,
        severity="material",
        expected={"authorization_result": "allowed", "trust_grant_consumed": True},
        observed={"authorization_result": fresh_report.get("authorization_result"), "trust_grant_consumed": fresh_report.get("trust_grant_consumed")},
        evidence_refs=[rel(EVIDENCE_DIR / "independent-check-output.json")],
    )
    assertion(
        assertions,
        id="sqlite_persistence",
        category="persistence",
        description="Temporary local Service state contains expected objects, events, idempotency rows, and artifact metadata.",
        passed=EXPECTED_OBJECT_KINDS.issubset(object_kinds) and db_summary["counts"].get("events") == 6 and db_summary["counts"].get("idempotency", 0) >= 2 and db_summary["counts"].get("artifact_metadata") == 2,
        severity="material",
        expected={"object_kinds_subset": sorted(EXPECTED_OBJECT_KINDS), "events": 6, "idempotency_at_least": 2, "artifact_metadata": 2},
        observed={"object_kinds": sorted(object_kinds), "counts": db_summary["counts"]},
        evidence_refs=[rel(EVIDENCE_DIR / "sqlite-summary.json")],
    )
    assertion(
        assertions,
        id="event_sequence",
        category="events",
        description="Temporary local Service events are contiguous and semantically ordered.",
        passed=event_sequences == [1, 2, 3, 4, 5, 6] and event_types == EXPECTED_EVENTS,
        severity="material",
        expected={"sequences": [1, 2, 3, 4, 5, 6], "event_types": EXPECTED_EVENTS},
        observed={"sequences": event_sequences, "event_types": event_types},
        evidence_refs=[rel(EVIDENCE_DIR / "sqlite-summary.json")],
    )
    assertion(
        assertions,
        id="idempotent_replay",
        category="idempotency",
        description="Fresh fixture records idempotent replay without a second host launch.",
        passed=fresh_report.get("idempotent_replay_no_second_host_launch") is True and fresh_report.get("host_call_count_after_replay") == 1,
        severity="material",
        expected={"idempotent_replay_no_second_host_launch": True, "host_call_count_after_replay": 1},
        observed={"idempotent_replay_no_second_host_launch": fresh_report.get("idempotent_replay_no_second_host_launch"), "host_call_count_after_replay": fresh_report.get("host_call_count_after_replay")},
        evidence_refs=[rel(EVIDENCE_DIR / "independent-check-output.json")],
    )
    assertion(
        assertions,
        id="artifact_integrity",
        category="artifacts",
        description="Raw event stream and worker artifact paths exist and hashes match declared digests.",
        passed=raw_path.is_file() and sha256_file(raw_path) == raw_artifact.get("sha256") and all(item["matches"] for item in worker_integrity),
        severity="material",
        expected={"raw_event_exists": True, "hashes_match": True},
        observed={"raw_event_exists": raw_path.is_file(), "raw_event_sha_matches": sha256_file(raw_path) == raw_artifact.get("sha256") if raw_path.is_file() else False, "worker_integrity": worker_integrity},
        evidence_refs=[rel(EVIDENCE_DIR / "artifact-integrity.json")],
    )
    assertion(
        assertions,
        id="raw_event_stream_semantics",
        category="events",
        description="Raw event stream is parseable NDJSON and contains worker lifecycle events.",
        passed=bool(parsed_raw_lines) and any(item.get("event_kind") == "run_started" for item in parsed_raw_lines) and any(item.get("event_kind") == "run_completed" for item in parsed_raw_lines),
        severity="material",
        expected={"parseable": True, "run_started": True, "run_completed": True},
        observed={"line_count": len(raw_lines), "events": [item.get("event_kind") for item in parsed_raw_lines]},
        evidence_refs=[raw_artifact.get("path", "")],
    )
    assertion(
        assertions,
        id="false_boundaries",
        category="non_capabilities",
        description="Fresh fixture keeps all explicit false-boundary fields boolean false.",
        passed=all(value is False for value in false_boundary_values.values()),
        severity="material",
        expected={field: False for field in FALSE_BOUNDARY_FIELDS},
        observed=false_boundary_values,
        evidence_refs=[rel(EVIDENCE_DIR / "independent-check-output.json")],
    )
    assertion(
        assertions,
        id="source_state_unchanged",
        category="read_only_safety",
        description="Fresh fixture reports unchanged material source snapshot and checkout.",
        passed=fresh_report.get("source_snapshot_unchanged") is True and fresh_report.get("source_checkout_unchanged") is True,
        severity="material",
        expected={"source_snapshot_unchanged": True, "source_checkout_unchanged": True},
        observed={"source_snapshot_unchanged": fresh_report.get("source_snapshot_unchanged"), "source_checkout_unchanged": fresh_report.get("source_checkout_unchanged")},
        evidence_refs=[rel(EVIDENCE_DIR / "independent-check-output.json")],
    )
    assertion(
        assertions,
        id="evidence_packet_consistency",
        category="evidence",
        description="EvidencePacket claims and artifact references match source fixture report.",
        passed=source_evidence.get("status", {}).get("validated") is True and any(a.get("role") == "host_raw_event_stream" and a.get("sha256") == source_fixture.get("raw_event_stream_artifact", {}).get("sha256") for a in source_evidence.get("spec", {}).get("artifacts", [])),
        severity="material",
        expected={"validated": True, "host_raw_event_stream_sha_matches": True},
        observed={"validated": source_evidence.get("status", {}).get("validated"), "artifact_roles": [a.get("role") for a in source_evidence.get("spec", {}).get("artifacts", [])]},
        evidence_refs=[rel(SOURCE_REPORT_DIR / "evidence-packet.json"), rel(SOURCE_REPORT_DIR / "fixture-report.json")],
    )
    assertion(
        assertions,
        id="event_record_result_consistency",
        category="evidence_truthfulness",
        description="EventRecord payload should preserve the observed host result from the durable WorkerRun fixture report.",
        passed=source_event.get("spec", {}).get("payload", {}).get("result") == source_fixture.get("host_result"),
        severity="material",
        expected={"event_payload_result": source_fixture.get("host_result")},
        observed={"event_payload_result": source_event.get("spec", {}).get("payload", {}).get("result"), "fixture_host_result": source_fixture.get("host_result"), "event_status_result": source_event.get("status", {}).get("result")},
        evidence_refs=[rel(SOURCE_REPORT_DIR / "event-record.json"), rel(SOURCE_REPORT_DIR / "fixture-report.json")],
    )
    assertion(
        assertions,
        id="report_scrubbed",
        category="evidence",
        description="Committed durable reports and build task evidence contain no local absolute path or secret-like leak.",
        passed=not leak_hits,
        severity="material",
        expected=[],
        observed=leak_hits,
        evidence_refs=[rel(EVIDENCE_DIR / "leak-scan.json")],
    )

    material_findings = [item for item in assertions if item["outcome"] == "FAIL" and item["severity"] == "material"]
    result = "PASS_WITH_WARNINGS" if not material_findings else "REQUEST_CHANGES"
    next_task = PASS_NEXT if not material_findings else REPAIR_NEXT

    output = {
        "schema_version": "aide.durable-local-worker-run.check.v0",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "result": result,
        "material_finding_count": len(material_findings),
        "missing_evidence": 0,
        "recommended_next_task": next_task,
        "fresh_fixture_summary": {
            "status": fresh_report.get("status"),
            "host_result": fresh_report.get("host_result"),
            "process_call_count": fresh_report.get("process_call_count"),
            "reference_worker_process_started": fresh_report.get("reference_worker_process_started"),
            "authorization_result": fresh_report.get("authorization_result"),
            "trust_grant_consumed": fresh_report.get("trust_grant_consumed"),
            "service_event_sequences": fresh_report.get("service_event_sequences"),
            "service_event_types": fresh_report.get("service_event_types"),
            "service_objects_persisted": fresh_report.get("service_objects_persisted"),
            "idempotent_replay_no_second_host_launch": fresh_report.get("idempotent_replay_no_second_host_launch"),
            "source_snapshot_unchanged": fresh_report.get("source_snapshot_unchanged"),
        },
        "assertions": assertions,
        "material_findings": material_findings,
        "warnings": [
            "The checked capability remains fixture-backed.",
            "The check did not repair production implementation.",
            "No general worker harness, scheduler, persistent daemon, Workbench/MCP runtime, provider/model call, network call, preview, apply, rollback, or repository mutation is accepted.",
        ],
    }

    (EVIDENCE_DIR / "independent-check-output.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (EVIDENCE_DIR / "sqlite-summary.json").write_text(json.dumps(db_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (EVIDENCE_DIR / "artifact-integrity.json").write_text(json.dumps({"raw_event": raw_artifact, "raw_event_sha_observed": sha256_file(raw_path) if raw_path.is_file() else None, "worker_artifacts": worker_integrity}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (EVIDENCE_DIR / "leak-scan.json").write_text(json.dumps({"hits": leak_hits}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = {
        "schema_version": "aide.check-report.v0",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "result": result,
        "material_finding_count": len(material_findings),
        "missing_evidence": 0,
        "recommended_next_task": next_task,
        "assertions": assertions,
    }
    (REPORT_DIR / "check-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (REPORT_DIR / "status.md").write_text(render_status(output), encoding="utf-8")
    (REPORT_DIR / "material-findings.md").write_text(render_findings(material_findings), encoding="utf-8")
    (REPORT_DIR / "source-chain-review.md").write_text(render_section("Source Chain Review", assertions, "source_chain"), encoding="utf-8")
    (REPORT_DIR / "persistence-review.md").write_text(render_section("Persistence Review", assertions, "persistence"), encoding="utf-8")
    (REPORT_DIR / "event-evidence-review.md").write_text(render_categories("Event And Evidence Review", assertions, {"events", "evidence", "evidence_truthfulness"}), encoding="utf-8")
    (REPORT_DIR / "artifact-integrity-review.md").write_text(render_section("Artifact Integrity Review", assertions, "artifacts"), encoding="utf-8")
    (REPORT_DIR / "idempotency-review.md").write_text(render_section("Idempotency Review", assertions, "idempotency"), encoding="utf-8")
    (REPORT_DIR / "non-capabilities-review.md").write_text(render_section("Non-Capabilities Review", assertions, "non_capabilities"), encoding="utf-8")
    (REPORT_DIR / "report-consistency-review.md").write_text(render_categories("Report Consistency Review", assertions, {"evidence_truthfulness", "evidence"}), encoding="utf-8")
    (REPORT_DIR / "warning-disposition.md").write_text(render_warnings(output), encoding="utf-8")
    (REPORT_DIR / "next-task-prompt.md").write_text(render_next_task(next_task, result), encoding="utf-8")
    return 0 if result == "PASS_WITH_WARNINGS" else 2


def render_status(output: dict[str, Any]) -> str:
    return (
        "# Durable Local WorkerRun Slice v0 Check\n\n"
        f"- result: {output['result']}\n"
        f"- material_finding_count: {output['material_finding_count']}\n"
        f"- missing_evidence: {output['missing_evidence']}\n"
        f"- recommended_next_task: {output['recommended_next_task']}\n"
        f"- fresh_process_call_count: {output['fresh_fixture_summary']['process_call_count']}\n"
        f"- fresh_service_event_sequences: {output['fresh_fixture_summary']['service_event_sequences']}\n"
    )


def render_findings(findings: list[dict[str, Any]]) -> str:
    lines = ["# Material Findings", ""]
    if not findings:
        lines.append("No material findings remain.")
    else:
        for item in findings:
            lines.extend(
                [
                    f"## {item['id']}",
                    "",
                    f"- category: {item['category']}",
                    f"- severity: {item['severity']}",
                    f"- expected: `{json.dumps(item['expected'], sort_keys=True)}`",
                    f"- observed: `{json.dumps(item['observed'], sort_keys=True)}`",
                    f"- evidence_refs: {', '.join(item['evidence_refs'])}",
                    "",
                    item["description"],
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def render_section(title: str, assertions: list[dict[str, Any]], category: str) -> str:
    return render_categories(title, assertions, {category})


def render_categories(title: str, assertions: list[dict[str, Any]], categories: set[str]) -> str:
    lines = [f"# {title}", ""]
    selected = [item for item in assertions if item["category"] in categories]
    for item in selected:
        lines.append(f"- {item['id']}: {item['outcome']}")
    if not selected:
        lines.append("- no assertions in this category")
    return "\n".join(lines).rstrip() + "\n"


def render_warnings(output: dict[str, Any]) -> str:
    lines = ["# Warning Disposition", ""]
    for warning in output["warnings"]:
        lines.append(f"- {warning}")
    return "\n".join(lines).rstrip() + "\n"


def render_next_task(next_task: str, result: str) -> str:
    return (
        "# Next Task Prompt\n\n"
        "```text\n"
        f"Create and process {next_task}.\n"
        f"Prior result: {TASK_ID} returned {result}.\n"
        "Repo truth outranks this prompt. Preserve all prior evidence.\n"
        "```\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
