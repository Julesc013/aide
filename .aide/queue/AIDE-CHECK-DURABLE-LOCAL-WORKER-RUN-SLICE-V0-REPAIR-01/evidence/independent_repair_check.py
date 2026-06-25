from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01"
SOURCE_CHECK_ID = "AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01"
REPAIR_ID = "AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01"
SOURCE_BUILD_ID = "AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01"
FINDING_ID = "event_record_result_consistency"
NEXT_ON_PASS = "AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01"
NEXT_ON_FAIL = "AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-02"

EVIDENCE_DIR = ROOT / ".aide/queue" / TASK_ID / "evidence"
REPORT_DIR = ROOT / ".aide/reports/durable-local-worker-run-slice-v0-repair-01-check"


def read_json(relative_path: str) -> Any:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def assertion(
    assertions: list[dict[str, Any]],
    *,
    assertion_id: str,
    category: str,
    description: str,
    condition: bool,
    expected: Any,
    observed: Any,
    evidence_refs: list[str],
    severity_on_fail: str = "material",
    source_finding_id: str | None = FINDING_ID,
) -> None:
    assertions.append(
        {
            "id": assertion_id,
            "category": category,
            "description": description,
            "outcome": "PASS" if condition else "FAIL",
            "severity": "none" if condition else severity_on_fail,
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs,
            "source_finding_id": source_finding_id,
        }
    )


def scan_for_leaks(relative_roots: list[str]) -> list[dict[str, Any]]:
    local_path_re = re.compile(r"[A-Za-z]:(?:\\|/(?!/))[^\s\"']+")
    credential_assignment_re = re.compile(r"(?i)\b(api[_-]?key|credential|password|token)\b\s*[:=]\s*\S+")
    hits: list[dict[str, Any]] = []
    for relative_root in relative_roots:
        root = ROOT / relative_root
        if not root.exists():
            continue
        paths = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
        for path in paths:
            if "__pycache__" in path.parts:
                continue
            rel = path.relative_to(ROOT).as_posix()
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for line_number, line in enumerate(text.splitlines(), start=1):
                if local_path_re.search(line) or credential_assignment_re.search(line):
                    hits.append({"path": rel, "line": line_number, "kind": "local_path_or_credential_assignment"})
    return hits


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    original_check = read_json(
        ".aide/queue/AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01/evidence/independent-check-output.json"
    )
    repair_status = read_json_like_yaml(".aide/queue/AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01/status.yaml")
    repair_report = read_json(".aide/reports/durable-local-worker-run-slice-v0-repair-01/repair-report.json")
    fixture_report = read_json(".aide/reports/durable-local-worker-run-slice-v0/fixture-report.json")
    event_record = read_json(".aide/reports/durable-local-worker-run-slice-v0/event-record.json")
    source_text = read_text("core/service/durable_worker_run.py")
    test_text = read_text(".aide/scripts/tests/test_aide_durable_worker_run_slice.py")

    source_hashes = {
        "core/service/durable_worker_run.py": sha256_text(source_text),
        ".aide/scripts/tests/test_aide_durable_worker_run_slice.py": sha256_text(test_text),
    }

    material_findings = original_check.get("material_findings", [])
    original_finding_ids = [item.get("id") for item in material_findings]
    event_payload = event_record.get("spec", {}).get("payload", {})
    event_status = event_record.get("status", {})

    leak_hits = scan_for_leaks(
        [
            ".aide/reports/durable-local-worker-run-slice-v0",
            ".aide/reports/durable-local-worker-run-slice-v0-repair-01",
            ".aide/queue/AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01/evidence",
        ]
    )

    assertions: list[dict[str, Any]] = []
    assertion(
        assertions,
        assertion_id="baseline_single_material_finding",
        category="source_chain",
        description="The source check recorded exactly one material finding and routed to Repair 01.",
        condition=original_check.get("material_finding_count") == 1
        and original_finding_ids == [FINDING_ID]
        and original_check.get("recommended_next_task") == REPAIR_ID,
        expected={"material_finding_count": 1, "material_findings": [FINDING_ID], "recommended_next_task": REPAIR_ID},
        observed={
            "material_finding_count": original_check.get("material_finding_count"),
            "material_findings": original_finding_ids,
            "recommended_next_task": original_check.get("recommended_next_task"),
        },
        evidence_refs=[
            ".aide/queue/AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01/evidence/independent-check-output.json"
        ],
        source_finding_id=None,
    )
    assertion(
        assertions,
        assertion_id="repair_task_complete",
        category="source_chain",
        description="Repair 01 reports PASS_WITH_WARNINGS, no material findings, no missing evidence, and this repair check as next.",
        condition=repair_status.get("result") == "PASS_WITH_WARNINGS"
        and repair_status.get("material_finding_count") == "0"
        and repair_status.get("missing_evidence") == "0"
        and repair_status.get("recommended_next_task") == TASK_ID,
        expected={
            "result": "PASS_WITH_WARNINGS",
            "material_finding_count": "0",
            "missing_evidence": "0",
            "recommended_next_task": TASK_ID,
        },
        observed={
            "result": repair_status.get("result"),
            "material_finding_count": repair_status.get("material_finding_count"),
            "missing_evidence": repair_status.get("missing_evidence"),
            "recommended_next_task": repair_status.get("recommended_next_task"),
        },
        evidence_refs=[".aide/queue/AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01/status.yaml"],
        source_finding_id=None,
    )
    assertion(
        assertions,
        assertion_id="repair_report_closes_exact_finding",
        category="finding_closure",
        description="Repair 01 disposition names exactly the source finding and reports no extra material findings.",
        condition=repair_report.get("repaired_findings") == [FINDING_ID]
        and repair_report.get("material_finding_count") == 0
        and repair_report.get("missing_evidence") == 0,
        expected={"repaired_findings": [FINDING_ID], "material_finding_count": 0, "missing_evidence": 0},
        observed={
            "repaired_findings": repair_report.get("repaired_findings"),
            "material_finding_count": repair_report.get("material_finding_count"),
            "missing_evidence": repair_report.get("missing_evidence"),
        },
        evidence_refs=[".aide/reports/durable-local-worker-run-slice-v0-repair-01/repair-report.json"],
    )
    assertion(
        assertions,
        assertion_id="event_record_result_consistency_closed",
        category="evidence_truthfulness",
        description="The EventRecord payload result now preserves the fixture host result.",
        condition=fixture_report.get("host_result") == "PASS"
        and event_payload.get("result") == fixture_report.get("host_result")
        and event_status.get("result") == fixture_report.get("host_result"),
        expected={"fixture_host_result": "PASS", "event_payload_result": "PASS", "event_status_result": "PASS"},
        observed={
            "fixture_host_result": fixture_report.get("host_result"),
            "event_payload_result": event_payload.get("result"),
            "event_status_result": event_status.get("result"),
        },
        evidence_refs=[
            ".aide/reports/durable-local-worker-run-slice-v0/fixture-report.json",
            ".aide/reports/durable-local-worker-run-slice-v0/event-record.json",
        ],
    )
    assertion(
        assertions,
        assertion_id="event_payload_semantics_preserved",
        category="event_semantics",
        description="The EventRecord payload still points at the expected WorkUnit and fixture host run with one process call.",
        condition=event_payload.get("workunit_ref") == "aide://workunit/AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01"
        and event_payload.get("host_ref") == "aide://execution-host/local-process/reference-v0"
        and event_payload.get("host_run_ref") == "aide://execution-host-run/local-process-reference-01"
        and event_payload.get("process_call_count") == 1
        and event_payload.get("durably_recorded") is True
        and event_payload.get("fixture_backed") is True,
        expected={
            "process_call_count": 1,
            "durably_recorded": True,
            "fixture_backed": True,
        },
        observed={
            "workunit_ref": event_payload.get("workunit_ref"),
            "host_ref": event_payload.get("host_ref"),
            "host_run_ref": event_payload.get("host_run_ref"),
            "process_call_count": event_payload.get("process_call_count"),
            "durably_recorded": event_payload.get("durably_recorded"),
            "fixture_backed": event_payload.get("fixture_backed"),
        },
        evidence_refs=[".aide/reports/durable-local-worker-run-slice-v0/event-record.json"],
        source_finding_id=None,
    )
    assertion(
        assertions,
        assertion_id="source_fallback_handles_normalized_report",
        category="implementation_inspection",
        description="Source now falls back from live result to normalized host_result when building EventRecord payloads.",
        condition='"result": host_result.get("result", host_result.get("host_result"))' in source_text,
        expected="result fallback from result to host_result",
        observed={"source_hash": source_hashes["core/service/durable_worker_run.py"]},
        evidence_refs=["core/service/durable_worker_run.py"],
    )
    assertion(
        assertions,
        assertion_id="focused_regression_present",
        category="test_coverage",
        description="Focused test coverage asserts build_event_record(report) preserves PASS in the payload.",
        condition="build_event_record(report)" in test_text
        and 'event_record["spec"]["payload"]["result"]' in test_text
        and '"PASS"' in test_text,
        expected="test asserts EventRecord payload result equals PASS",
        observed={"test_hash": source_hashes[".aide/scripts/tests/test_aide_durable_worker_run_slice.py"]},
        evidence_refs=[".aide/scripts/tests/test_aide_durable_worker_run_slice.py"],
    )

    false_boundary_keys = [
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
    false_boundary_observed = {key: fixture_report.get(key) for key in false_boundary_keys}
    assertion(
        assertions,
        assertion_id="false_boundaries_remain_false",
        category="non_capabilities",
        description="Repair 01 did not widen the durable WorkerRun false-boundary set.",
        condition=all(value is False for value in false_boundary_observed.values()),
        expected={key: False for key in false_boundary_keys},
        observed=false_boundary_observed,
        evidence_refs=[".aide/reports/durable-local-worker-run-slice-v0/fixture-report.json"],
        source_finding_id=None,
    )
    assertion(
        assertions,
        assertion_id="source_state_still_unchanged",
        category="read_only_safety",
        description="The durable WorkerRun fixture still reports unchanged source and workspace state.",
        condition=fixture_report.get("source_checkout_unchanged") is True
        and fixture_report.get("source_snapshot_unchanged") is True
        and fixture_report.get("workspace_state_unchanged") is True,
        expected={
            "source_checkout_unchanged": True,
            "source_snapshot_unchanged": True,
            "workspace_state_unchanged": True,
        },
        observed={
            "source_checkout_unchanged": fixture_report.get("source_checkout_unchanged"),
            "source_snapshot_unchanged": fixture_report.get("source_snapshot_unchanged"),
            "workspace_state_unchanged": fixture_report.get("workspace_state_unchanged"),
        },
        evidence_refs=[".aide/reports/durable-local-worker-run-slice-v0/fixture-report.json"],
        source_finding_id=None,
    )
    assertion(
        assertions,
        assertion_id="committed_reports_scrubbed",
        category="evidence",
        description="Committed durable WorkerRun reports and Repair 01 evidence contain no local absolute paths or credential assignments.",
        condition=leak_hits == [],
        expected=[],
        observed=leak_hits,
        evidence_refs=[(EVIDENCE_DIR / "leak-scan.json").relative_to(ROOT).as_posix()],
        source_finding_id=None,
    )

    material_findings_after = [
        item for item in assertions if item["outcome"] != "PASS" and item["severity"] == "material"
    ]
    result = "PASS_WITH_WARNINGS" if not material_findings_after else "REQUEST_CHANGES"
    next_task = NEXT_ON_PASS if not material_findings_after else NEXT_ON_FAIL

    output = {
        "schema_version": "aide.durable-local-worker-run.repair-01-check.v0",
        "task_id": TASK_ID,
        "source_build_task_id": SOURCE_BUILD_ID,
        "source_check_task_id": SOURCE_CHECK_ID,
        "repair_task_id": REPAIR_ID,
        "result": result,
        "material_finding_count": len(material_findings_after),
        "missing_evidence": 0,
        "closed_findings": [FINDING_ID] if not material_findings_after else [],
        "material_findings": material_findings_after,
        "assertions": assertions,
        "source_hashes": source_hashes,
        "recommended_next_task": next_task,
        "warnings": [
            "durable_local_worker_run_slice_v0 remains fixture-backed.",
            "This check does not accept the capability.",
            "No general worker harness, autonomous worker, scheduler, daemon, Workbench/MCP runtime, provider/model call, network call, preview, apply, rollback, repository mutation, branch/worktree automation, GitHub mutation, release, or promotion is accepted.",
        ],
    }

    leak_output = {
        "schema_version": "aide.leak-scan.summary.v0",
        "task_id": TASK_ID,
        "scanned_roots": [
            ".aide/reports/durable-local-worker-run-slice-v0",
            ".aide/reports/durable-local-worker-run-slice-v0-repair-01",
            ".aide/queue/AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01/evidence",
        ],
        "hit_count": len(leak_hits),
        "hits": leak_hits,
    }

    write_json(EVIDENCE_DIR / "leak-scan.json", leak_output)
    write_json(EVIDENCE_DIR / "independent-check-output.json", output)
    write_json(REPORT_DIR / "check-report.json", output)
    write_json(
        REPORT_DIR / "finding-disposition.json",
        {
            "schema_version": "aide.finding-disposition.v0",
            "task_id": TASK_ID,
            "source_finding_id": FINDING_ID,
            "disposition": "CLOSED" if not material_findings_after else "OPEN",
            "expected": "EventRecord payload result preserves fixture host_result.",
            "observed": {
                "fixture_host_result": fixture_report.get("host_result"),
                "event_payload_result": event_payload.get("result"),
                "event_status_result": event_status.get("result"),
            },
            "evidence_refs": [
                ".aide/queue/AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01/evidence/independent-check-output.json",
                ".aide/reports/durable-local-worker-run-slice-v0/fixture-report.json",
                ".aide/reports/durable-local-worker-run-slice-v0/event-record.json",
            ],
        },
    )
    return 0 if not material_findings_after else 1


def read_json_like_yaml(relative_path: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw_line in read_text(relative_path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("- ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("'\"")
    return result


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
