from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01"
SOURCE_TASK_ID = "AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01"
REPORT_ROOT = Path(".aide/reports/local-process-execution-host-repair-01-check")


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.execution import local_process_host as host  # noqa: E402


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def read_json(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: Path, data: Any) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8", newline="\n")


def write_text(rel: Path, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def run_git(*args: str) -> str:
    completed = subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, shell=False)
    return completed.stdout.strip()


def event(kind: str, sequence: int, payload: dict[str, Any] | None = None, *, run_ref: str = host.RUN_REF) -> dict[str, Any]:
    return {
        "schema_version": host.FIXTURE_EVENT_SCHEMA,
        "run_ref": run_ref,
        "sequence": sequence,
        "event_kind": kind,
        "timestamp": host.DETERMINISTIC_TIMESTAMP,
        "payload": payload or {},
    }


def stream(events: list[dict[str, Any]]) -> str:
    return "\n".join(json.dumps(item, sort_keys=True) for item in events) + "\n"


def reason_for_event_stream(text: str, returncode: int = 0) -> str:
    try:
        host.parse_fixture_event_stream(text, returncode)
    except host.LocalProcessHostError as exc:
        return exc.reason_code
    return ""


def assertion(
    assertions: list[dict[str, Any]],
    *,
    id: str,
    category: str,
    description: str,
    outcome: str,
    severity: str,
    expected: Any,
    observed: Any,
    evidence_refs: list[str],
    source_finding_id: str,
) -> None:
    assertions.append(
        {
            "id": id,
            "category": category,
            "description": description,
            "outcome": outcome,
            "severity": severity,
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs,
            "source_finding_id": source_finding_id,
        }
    )


def material_count(assertions: list[dict[str, Any]]) -> int:
    return sum(1 for item in assertions if item["outcome"] == "FAIL" and item["severity"] == "material")


def main() -> int:
    assertions: list[dict[str, Any]] = []
    source = read_json(".aide/reports/local-process-execution-host-repair-01/repair-report.json")
    dispositions = read_json(".aide/reports/local-process-execution-host-repair-01/finding-disposition.json")
    validation = read_json(".aide/reports/local-process-execution-host/validation.json")
    descriptor = read_json(".aide/reports/local-process-execution-host/host-descriptor.json")
    run_result = read_json(".aide/reports/local-process-execution-host/run-result.json")
    host_source = (ROOT / "core/execution/local_process_host.py").read_text(encoding="utf-8")
    test_source = (ROOT / ".aide/scripts/tests/test_aide_local_process_execution_host.py").read_text(encoding="utf-8")
    latest_commit = run_git("rev-parse", "HEAD")
    latest_files = run_git("diff", "--name-only", "HEAD^", "HEAD").splitlines()

    expected_ids = [
        "local_host.disposable_workspace_not_proven",
        "local_host.path_escape_not_proven",
        "local_host.raw_event_stream_not_proven",
        "local_host.content_addressed_artifacts_not_proven",
        "local_host.workerrun_lifecycle_not_proven",
        "local_host.descriptor_overclaims_operations",
    ]
    observed_ids = [item.get("finding_id") for item in dispositions.get("findings", [])]
    assertion(
        assertions,
        id="baseline.source_result",
        category="baseline",
        description="Repair 01 reports PASS_WITH_WARNINGS, zero material findings, and recommends this check.",
        outcome="PASS" if source.get("result") == "PASS_WITH_WARNINGS" and source.get("material_finding_count") == 0 and source.get("recommended_next_task") == TASK_ID else "FAIL",
        severity="material",
        expected={"result": "PASS_WITH_WARNINGS", "material_finding_count": 0, "recommended_next_task": TASK_ID},
        observed={"result": source.get("result"), "material_finding_count": source.get("material_finding_count"), "recommended_next_task": source.get("recommended_next_task")},
        evidence_refs=[".aide/reports/local-process-execution-host-repair-01/repair-report.json"],
        source_finding_id="baseline",
    )
    assertion(
        assertions,
        id="baseline.six_dispositions",
        category="baseline",
        description="Repair 01 provides exactly six source-finding dispositions.",
        outcome="PASS" if observed_ids == expected_ids and all(item.get("disposition") == "CLOSED" for item in dispositions.get("findings", [])) else "FAIL",
        severity="material",
        expected=expected_ids,
        observed=observed_ids,
        evidence_refs=[".aide/reports/local-process-execution-host-repair-01/finding-disposition.json"],
        source_finding_id="baseline",
    )
    forbidden_changed = [item for item in latest_files if item in {"core/execution/registered_process.py", "core/protocol/execution_host.py", ".aide/protocol/aide-execution-host.schema.json"} or item.startswith("core/interop/") or item.startswith("hosts/") or item.startswith(".aide.local/")]
    assertion(
        assertions,
        id="baseline.forbidden_paths_unchanged",
        category="baseline",
        description="Repair commit does not modify provider core, accepted ExecutionHost contract, interop domains, hosts, or .aide.local.",
        outcome="PASS" if not forbidden_changed else "FAIL",
        severity="material",
        expected=[],
        observed=forbidden_changed,
        evidence_refs=["git diff --name-only HEAD^ HEAD"],
        source_finding_id="baseline",
    )

    assertion(
        assertions,
        id="workspace.disposable_workspace_report",
        category="workspace",
        description="Generated evidence shows a staged worker in a disposable workspace outside the source checkout and cleanup removed.",
        outcome="PASS" if run_result.get("workspace_stage", {}).get("workspace_root_inside_source") is False and run_result.get("workspace_cleanup", {}).get("removed") is True else "FAIL",
        severity="material",
        expected={"workspace_root_inside_source": False, "cleanup_removed": True},
        observed={"workspace_stage": run_result.get("workspace_stage", {}), "workspace_cleanup": run_result.get("workspace_cleanup", {})},
        evidence_refs=[".aide/reports/local-process-execution-host/run-result.json"],
        source_finding_id="local_host.disposable_workspace_not_proven",
    )

    path_probe_observed: dict[str, str] = {}
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "workspace"
        workspace.mkdir()
        path_cases = {
            "../outside": host.REFUSAL_CODES["workspace_path_traversal"],
            "nested/../../outside": host.REFUSAL_CODES["workspace_path_traversal"],
            "C:\\outside.txt": host.REFUSAL_CODES["workspace_path_absolute"],
            "/outside.txt": host.REFUSAL_CODES["workspace_path_absolute"],
        }
        for member, expected in path_cases.items():
            try:
                host.resolve_workspace_member(workspace, member)
                path_probe_observed[member] = "ACCEPTED"
            except host.LocalProcessHostError as exc:
                path_probe_observed[member] = exc.reason_code
        link = workspace / "link"
        nested_link = workspace / "nested-link"
        try:
            link.symlink_to(Path(tmp))
            nested_link.mkdir()
            (nested_link / "link").symlink_to(Path(tmp))
            for member in ("link/file.txt", "nested-link/link/file.txt"):
                try:
                    host.resolve_workspace_member(workspace, member)
                    path_probe_observed[member] = "ACCEPTED"
                except host.LocalProcessHostError as exc:
                    path_probe_observed[member] = exc.reason_code
        except OSError:
            path_probe_observed["symlink-fixture"] = "SKIPPED_UNAVAILABLE"
    path_probe_pass = all(path_probe_observed.get(member) == expected for member, expected in {
        "../outside": host.REFUSAL_CODES["workspace_path_traversal"],
        "nested/../../outside": host.REFUSAL_CODES["workspace_path_traversal"],
        "C:\\outside.txt": host.REFUSAL_CODES["workspace_path_absolute"],
        "/outside.txt": host.REFUSAL_CODES["workspace_path_absolute"],
    }.items()) and path_probe_observed.get("link/file.txt") in {host.REFUSAL_CODES["workspace_symlink_escape"], "SKIPPED_UNAVAILABLE"} and path_probe_observed.get("nested-link/link/file.txt") in {host.REFUSAL_CODES["workspace_symlink_escape"], None, "SKIPPED_UNAVAILABLE"}
    assertion(
        assertions,
        id="workspace.path_probe_matrix",
        category="workspace",
        description="Containment helper rejects traversal, absolute paths, and symlink escape when exercised directly.",
        outcome="PASS" if path_probe_pass else "FAIL",
        severity="material",
        expected="all probed unsafe members refused",
        observed=path_probe_observed,
        evidence_refs=["core/execution/local_process_host.py"],
        source_finding_id="local_host.path_escape_not_proven",
    )
    required_path_test_tokens = ["nested/../../", "C:\\\\", "nested symlink", "reparse", "TOCTOU", "safe artifact"]
    missing_path_tokens = [token for token in required_path_test_tokens if token not in test_source]
    assertion(
        assertions,
        id="workspace.test_matrix_incomplete",
        category="workspace",
        description="Focused tests do not cover the full required path containment matrix.",
        outcome="FAIL" if missing_path_tokens else "PASS",
        severity="material",
        expected="nested traversal, Windows absolute path, nested symlink, reparse practical note, safe artifact directory, and TOCTOU revalidation evidence",
        observed={"missing_test_tokens": missing_path_tokens},
        evidence_refs=[".aide/scripts/tests/test_aide_local_process_execution_host.py"],
        source_finding_id="local_host.path_escape_not_proven",
    )

    duplicate_terminal_stream = stream(
        [
            event("run_created", 1),
            event("run_started", 2),
            event("run_completed", 3),
            event("run_failed", 4),
        ]
    )
    duplicate_terminal_reason = reason_for_event_stream(duplicate_terminal_stream)
    assertion(
        assertions,
        id="events.duplicate_terminal_reason",
        category="events",
        description="A second terminal event must produce the typed duplicate_terminal_event refusal rather than a generic post-terminal refusal.",
        outcome="PASS" if duplicate_terminal_reason == host.REFUSAL_CODES["duplicate_terminal_event"] else "FAIL",
        severity="material",
        expected=host.REFUSAL_CODES["duplicate_terminal_event"],
        observed=duplicate_terminal_reason,
        evidence_refs=["core/execution/local_process_host.py"],
        source_finding_id="local_host.raw_event_stream_not_proven",
    )
    raw_artifact = run_result.get("raw_event_stream_artifact", {})
    raw_path = ROOT / str(raw_artifact.get("path", ""))
    raw_digest_ok = raw_path.is_file() and host.sha256_file(raw_path) == raw_artifact.get("sha256")
    assertion(
        assertions,
        id="events.raw_stream_persisted",
        category="events",
        description="Raw NDJSON event stream is persisted and digest-addressed.",
        outcome="PASS" if raw_artifact.get("persisted") and raw_digest_ok else "FAIL",
        severity="material",
        expected={"persisted": True, "digest_matches": True},
        observed={"artifact": raw_artifact, "digest_matches": raw_digest_ok},
        evidence_refs=[".aide/reports/local-process-execution-host/run-result.json", str(raw_artifact.get("path", ""))],
        source_finding_id="local_host.raw_event_stream_not_proven",
    )
    required_event_test_tokens = ["duplicate terminal", "missing sequence", "truncated", "invalid artifact", "timeout before terminal", "multiple terminal"]
    missing_event_tokens = [token for token in required_event_test_tokens if token not in test_source]
    assertion(
        assertions,
        id="events.test_matrix_incomplete",
        category="events",
        description="Focused tests do not cover the full required fail-closed event stream matrix.",
        outcome="FAIL" if missing_event_tokens else "PASS",
        severity="material",
        expected="all required event failure fixtures covered",
        observed={"missing_test_tokens": missing_event_tokens},
        evidence_refs=[".aide/scripts/tests/test_aide_local_process_execution_host.py"],
        source_finding_id="local_host.raw_event_stream_not_proven",
    )

    artifacts = run_result.get("worker_artifacts", [])
    artifact_ok = bool(artifacts)
    if artifact_ok:
        artifact_path = ROOT / artifacts[0]["path"]
        artifact_ok = artifact_path.is_file() and host.sha256_file(artifact_path) == artifacts[0].get("sha256") and artifacts[0].get("content_addressed") is True
    assertion(
        assertions,
        id="artifacts.persisted_content_addressed",
        category="artifacts",
        description="Declared worker artifact is persisted under a sha256-addressed path with matching digest.",
        outcome="PASS" if artifact_ok else "FAIL",
        severity="material",
        expected={"content_addressed": True, "digest_matches": True},
        observed=artifacts,
        evidence_refs=[".aide/reports/local-process-execution-host/host-artifacts.json"],
        source_finding_id="local_host.content_addressed_artifacts_not_proven",
    )
    required_artifact_tokens = ["artifact_size_mismatch", "directory instead", "link/reparse", "duplicate identical", "same path with different content", "partial artifact", "oversized"]
    missing_artifact_tokens = [token for token in required_artifact_tokens if token not in test_source]
    assertion(
        assertions,
        id="artifacts.test_matrix_incomplete",
        category="artifacts",
        description="Focused tests do not cover the full required artifact integrity matrix.",
        outcome="FAIL" if missing_artifact_tokens else "PASS",
        severity="material",
        expected="all required artifact integrity fixtures covered",
        observed={"missing_test_tokens": missing_artifact_tokens},
        evidence_refs=[".aide/scripts/tests/test_aide_local_process_execution_host.py"],
        source_finding_id="local_host.content_addressed_artifacts_not_proven",
    )

    worker_run = read_json(".aide/reports/local-process-execution-host/worker-run.json")
    lifecycle_report = run_result.get("worker_run_lifecycle", {})
    assertion(
        assertions,
        id="lifecycle.completed_projection",
        category="lifecycle",
        description="Successful live run projects a completed WorkerRun from validated events.",
        outcome="PASS" if worker_run.get("state") == "completed" and lifecycle_report.get("final_state") == "completed" else "FAIL",
        severity="material",
        expected={"worker_run.state": "completed", "final_state": "completed"},
        observed={"worker_run": worker_run, "lifecycle": lifecycle_report},
        evidence_refs=[".aide/reports/local-process-execution-host/worker-run.json"],
        source_finding_id="local_host.workerrun_lifecycle_not_proven",
    )
    lifecycle_terminal_states = lifecycle_report.get("allowed_terminal_states", [])
    assertion(
        assertions,
        id="lifecycle.cancelled_terminal_missing",
        category="lifecycle",
        description="The required compact lifecycle names cancelled as a terminal state, but the repair projection omits it.",
        outcome="PASS" if "cancelled" in lifecycle_terminal_states else "FAIL",
        severity="material",
        expected=["completed", "failed", "timed_out", "cancelled"],
        observed=lifecycle_terminal_states,
        evidence_refs=[".aide/reports/local-process-execution-host/run-result.json", "core/execution/local_process_host.py"],
        source_finding_id="local_host.workerrun_lifecycle_not_proven",
    )
    required_lifecycle_tokens = ["creating -> ready", "ready -> running", "running -> timed_out", "running -> reconciliation_required", "terminal_state_transition", "cancelled"]
    missing_lifecycle_tokens = [token for token in required_lifecycle_tokens if token not in test_source]
    assertion(
        assertions,
        id="lifecycle.test_matrix_incomplete",
        category="lifecycle",
        description="Focused tests do not cover every required allowed transition and representative invalid terminal/reconciliation cases.",
        outcome="FAIL" if missing_lifecycle_tokens else "PASS",
        severity="material",
        expected="all required lifecycle transition tests covered",
        observed={"missing_test_tokens": missing_lifecycle_tokens},
        evidence_refs=[".aide/scripts/tests/test_aide_local_process_execution_host.py"],
        source_finding_id="local_host.workerrun_lifecycle_not_proven",
    )

    descriptor_pass = descriptor.get("supported_operations") == ["probe", "create_run"] and all(op in descriptor.get("unsupported_operations", []) for op in ["stream_events", "collect_artifacts", "finish", "reconcile"])
    assertion(
        assertions,
        id="descriptor.operation_scope",
        category="descriptor",
        description="Host descriptor advertises only proven public operations and marks previously overclaimed operations unsupported.",
        outcome="PASS" if descriptor_pass else "FAIL",
        severity="material",
        expected={"supported_operations": ["probe", "create_run"], "unsupported_contains": ["stream_events", "collect_artifacts", "finish", "reconcile"]},
        observed={"supported_operations": descriptor.get("supported_operations"), "unsupported_operations": descriptor.get("unsupported_operations")},
        evidence_refs=[".aide/reports/local-process-execution-host/host-descriptor.json"],
        source_finding_id="local_host.descriptor_overclaims_operations",
    )

    open_by_source: dict[str, list[str]] = {}
    for item in assertions:
        if item["outcome"] == "FAIL" and item["severity"] == "material":
            open_by_source.setdefault(item["source_finding_id"], []).append(item["id"])
    result = "REQUEST_CHANGES" if material_count(assertions) else "PASS_WITH_WARNINGS"
    recommended_next_task = "AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02" if result == "REQUEST_CHANGES" else "AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01"
    report = {
        "schema_version": "aide.local-process-execution-host.repair-01-check.v0",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_commit": latest_commit,
        "result": result,
        "material_finding_count": material_count(assertions),
        "missing_evidence": 0,
        "recommended_next_task": recommended_next_task,
        "assertions": assertions,
        "open_source_findings": open_by_source,
        "warnings": [
            "The check invokes production helper functions as the system under test but does not modify implementation.",
            "Windows reparse-point fixture execution is only practical when the platform exposes such a fixture.",
        ],
    }
    closure_rows = []
    for finding_id in expected_ids:
        fails = open_by_source.get(finding_id, [])
        closure_rows.append(
            {
                "finding_id": finding_id,
                "disposition": "OPEN" if fails else "CLOSED",
                "check_assertions": [item["id"] for item in assertions if item["source_finding_id"] == finding_id],
                "open_assertions": fails,
            }
        )
    write_json(REPORT_ROOT / "check-report.json", report)
    write_json(REPORT_ROOT / "six-finding-closure.json", {"schema_version": "aide.local-process-execution-host.repair-01-closure.v0", "task_id": TASK_ID, "result": result, "findings": closure_rows})
    write_text(
        REPORT_ROOT / "status.md",
        "\n".join(
            [
                "# LocalProcessExecutionHost Repair 01 Check Status",
                "",
                f"- result: {result}",
                f"- material_finding_count: {material_count(assertions)}",
                "- missing_evidence: 0",
                f"- recommended_next_task: {recommended_next_task}",
                "",
            ]
        ),
    )
    write_text(
        REPORT_ROOT / "six-finding-closure.md",
        "# Six Finding Closure\n\n" + "\n".join(f"- {item['finding_id']}: {item['disposition']}" for item in closure_rows) + "\n",
    )
    write_text(
        REPORT_ROOT / "material-findings.md",
        "# Material Findings\n\n" + "\n".join(f"- {item['id']}: {item['description']}" for item in assertions if item["outcome"] == "FAIL" and item["severity"] == "material") + "\n",
    )
    write_text(
        REPORT_ROOT / "source-chain-review.md",
        f"# Source Chain Review\n\n- HEAD: {latest_commit}\n- source task: {SOURCE_TASK_ID}\n- latest repair files checked: {len(latest_files)}\n- forbidden changed files: {forbidden_changed}\n",
    )
    for category in ["workspace", "events", "artifacts", "lifecycle", "descriptor"]:
        rows = [item for item in assertions if item["category"] == category]
        write_text(
            REPORT_ROOT / f"{category}-review.md",
            f"# {category.title()} Review\n\n" + "\n".join(f"- {item['id']}: {item['outcome']}" for item in rows) + "\n",
        )
    write_text(
        REPORT_ROOT / "warning-disposition.md",
        "# Warning Disposition\n\n- Fixture-scoped local host remains acceptable only after material closure.\n- Reparse-point probing remains platform-dependent and should be documented narrowly.\n",
    )
    write_text(
        REPORT_ROOT / "explicit-non-capabilities.md",
        "# Explicit Non-Capabilities\n\n- no generic worker harness\n- no Service/runtime\n- no provider/model/network calls\n- no Workbench/Commander/Mobile\n- no preview/apply/rollback\n- no branch/worktree/GitHub/release mutation\n",
    )
    write_text(
        REPORT_ROOT / "next-task-prompt.md",
        "# AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02\n\nRepair only the material findings from AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01. Do not broaden beyond the fixture-backed LocalProcessExecutionHost. Stop at needs_review and recommend AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02.\n",
    )
    print(json.dumps({"result": result, "material_finding_count": material_count(assertions), "recommended_next_task": recommended_next_task}, sort_keys=True))
    return 0 if result in {"PASS_WITH_WARNINGS", "REQUEST_CHANGES"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
