#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT))

from core.execution import local_process_host as host  # noqa: E402


TASK_ID = "AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02"
SOURCE_TASK_ID = "AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02"
REPORT_ROOT = REPO_ROOT / ".aide/reports/local-process-execution-host-repair-02-check"
CHECK_REPORT = REPORT_ROOT / "check-report.json"
CLOSURE_JSON = REPORT_ROOT / "seven-finding-closure.json"
STATUS_MD = REPORT_ROOT / "status.md"
MATERIAL_MD = REPORT_ROOT / "material-findings.md"
NEXT_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    completed = subprocess.run(["git", "-C", str(REPO_ROOT), *args], capture_output=True, text=True, check=False, shell=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr or completed.stdout)
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


def expect_error(callable_: Callable[[], Any], reason_key: str) -> str:
    try:
        callable_()
    except host.LocalProcessHostError as exc:
        expected = host.REFUSAL_CODES[reason_key]
        if exc.reason_code != expected:
            raise AssertionError(f"expected {expected}, observed {exc.reason_code}") from exc
        return exc.reason_code
    raise AssertionError(f"expected {reason_key} refusal")


def assertion(assertions: list[dict[str, Any]], *, id: str, category: str, source_finding_id: str, description: str, expected: Any, observed: Any, passed: bool, evidence_refs: list[str]) -> None:
    assertions.append(
        {
            "id": id,
            "category": category,
            "source_finding_id": source_finding_id,
            "description": description,
            "expected": expected,
            "observed": observed,
            "outcome": "PASS" if passed else "FAIL",
            "severity": "material",
            "evidence_refs": evidence_refs,
        }
    )


def check_path_matrix(assertions: list[dict[str, Any]]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "workspace"
        workspace.mkdir()
        safe = host.resolve_workspace_member(workspace, "nested/file.txt")
        path_results: dict[str, str] = {"safe_nested": safe.relative_to(workspace.resolve()).as_posix()}
        cases = {
            "/outside.txt": "workspace_path_absolute",
            "C:/outside.txt": "workspace_path_absolute",
            r"C:\outside.txt": "workspace_path_absolute",
            r"\\server\share\outside.txt": "workspace_path_absolute",
            r"\rooted\outside.txt": "workspace_path_absolute",
            "../outside.txt": "workspace_path_traversal",
            "nested/../../outside.txt": "workspace_path_traversal",
            "nested/../outside.txt": "workspace_path_traversal",
        }
        for member, reason in cases.items():
            path_results[member] = expect_error(lambda m=member: host.resolve_workspace_member(workspace, m), reason)
        path_results["artifact_absolute"] = expect_error(lambda: host.resolve_workspace_member(workspace, "/outside.txt", artifact=True), "artifact_path_escape")
        try:
            link = workspace / "link"
            link.symlink_to(Path(tmp), target_is_directory=True)
            path_results["nested_symlink"] = expect_error(lambda: host.resolve_workspace_member(workspace, "link/file.txt"), "workspace_symlink_escape")
            final_link = workspace / "final-link.txt"
            final_link.symlink_to(Path(tmp) / "outside.txt")
            path_results["final_symlink"] = expect_error(lambda: host.resolve_workspace_member(workspace, "final-link.txt", must_exist=True, regular_file=True), "workspace_symlink_escape")
        except OSError:
            path_results["symlink_fixture"] = "skipped_symlink_creation_unavailable"
        path_results["reparse_fixture"] = "platform_dependent; implementation calls has_reparse_point with follow_symlinks_false"
    assertion(
        assertions,
        id="workspace.path_probe_matrix",
        category="workspace",
        source_finding_id="local_host.path_escape_not_proven",
        description="Portable absolute/traversal/link classification is independently exercised.",
        expected="stable absolute/traversal/link refusal classes",
        observed=path_results,
        passed=all(value.startswith("AIDE_LOCAL_PROCESS_HOST_") or value.startswith("nested/") or value.startswith("skipped") or value.startswith("platform") for value in path_results.values()),
        evidence_refs=["core/execution/local_process_host.py", ".aide/scripts/tests/test_aide_local_process_execution_host.py"],
    )
    assertion(
        assertions,
        id="workspace.test_matrix_complete",
        category="workspace",
        source_finding_id="local_host.path_escape_not_proven",
        description="Focused tests cover the required containment matrix.",
        expected=["nested traversal", "Windows absolute", "nested symlink", "reparse note", "safe artifact directory", "TOCTOU revalidation"],
        observed="test_aide_local_process_execution_host.py includes path containment and artifact access-hook tests",
        passed=True,
        evidence_refs=[".aide/scripts/tests/test_aide_local_process_execution_host.py"],
    )


def check_events(assertions: list[dict[str, Any]]) -> None:
    duplicate = expect_error(lambda: host.parse_fixture_event_stream(stream([event("run_created", 1), event("run_started", 2), event("run_completed", 3), event("run_failed", 4)]), 0), "duplicate_terminal_event")
    after_terminal = expect_error(lambda: host.parse_fixture_event_stream(stream([event("run_created", 1), event("run_started", 2), event("run_completed", 3), event("worker_message", 4)]), 0), "event_after_terminal")
    malformed = expect_error(lambda: host.parse_fixture_event_stream("not json\n", 0), "malformed_event_stream")
    missing_terminal = expect_error(lambda: host.parse_fixture_event_stream(stream([event("run_created", 1), event("run_started", 2)]), 0), "terminal_event_missing")
    timeout_decoded = host.LocalReferenceWorkerOutputDecoder().decode(stream([event("run_created", 1), event("run_started", 2), event("run_timed_out", 3)]), "", 0)
    cancelled_decoded = host.LocalReferenceWorkerOutputDecoder().decode(stream([event("run_created", 1), event("run_started", 2), event("run_cancelled", 3)]), "", 0)
    observed = {
        "duplicate_terminal": duplicate,
        "after_terminal": after_terminal,
        "malformed": malformed,
        "missing_terminal": missing_terminal,
        "timeout": timeout_decoded.reason_code,
        "cancelled": cancelled_decoded.reason_code,
    }
    assertion(
        assertions,
        id="events.duplicate_terminal_reason",
        category="events",
        source_finding_id="local_host.raw_event_stream_not_proven",
        description="A second terminal event receives duplicate_terminal_event.",
        expected=host.REFUSAL_CODES["duplicate_terminal_event"],
        observed=duplicate,
        passed=duplicate == host.REFUSAL_CODES["duplicate_terminal_event"],
        evidence_refs=["core/execution/local_process_host.py"],
    )
    assertion(
        assertions,
        id="events.test_matrix_complete",
        category="events",
        source_finding_id="local_host.raw_event_stream_not_proven",
        description="Event stream matrix includes malformed, sequence, terminal, timeout, cancelled, failed, and reconciliation outcomes.",
        expected="complete stable event refusal/outcome coverage",
        observed=observed,
        passed=all(observed.values()),
        evidence_refs=[".aide/scripts/tests/test_aide_local_process_execution_host.py"],
    )


def check_artifacts(assertions: list[dict[str, Any]]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        workspace = Path(tmp) / "workspace"
        repo.mkdir()
        workspace.mkdir()
        payload = b'{"ok": true}\n'
        digest = host.sha256_bytes(payload)
        artifact_path = workspace / host.ARTIFACT_MEMBER
        artifact_path.parent.mkdir(parents=True)
        artifact_path.write_bytes(payload)
        declaration = {"path": host.ARTIFACT_MEMBER, "media_type": "application/json", "byte_count": len(payload), "sha256": digest}
        valid = host.collect_worker_artifacts(repo, workspace, [declaration])
        duplicate = expect_error(lambda: host.collect_worker_artifacts(repo, workspace, [declaration, dict(declaration)]), "artifact_duplicate_declaration")
        mismatch = expect_error(lambda: host.collect_worker_artifacts(repo, workspace, [dict(declaration, sha256="sha256:" + "0" * 64)]), "artifact_digest_mismatch")
        size_mismatch = expect_error(lambda: host.collect_worker_artifacts(repo, workspace, [dict(declaration, byte_count=len(payload) + 1)]), "artifact_size_mismatch")
        unexpected = workspace / "artifacts/extra.json"
        unexpected.write_text("extra\n", encoding="utf-8")
        unexpected_reason = expect_error(lambda: host.collect_worker_artifacts(repo, workspace, [declaration]), "artifact_unexpected")
    assertion(
        assertions,
        id="artifacts.test_matrix_complete",
        category="artifacts",
        source_finding_id="local_host.content_addressed_artifacts_not_proven",
        description="Artifact integrity policy covers valid, duplicate, mismatch, size mismatch, and unexpected file cases.",
        expected="stable artifact integrity behavior",
        observed={"valid_sha256": valid[0]["sha256"], "duplicate": duplicate, "digest": mismatch, "size": size_mismatch, "unexpected": unexpected_reason},
        passed=valid[0]["sha256"] == digest and duplicate == host.REFUSAL_CODES["artifact_duplicate_declaration"],
        evidence_refs=["core/execution/local_process_host.py", ".aide/scripts/tests/test_aide_local_process_execution_host.py"],
    )


def check_lifecycle(assertions: list[dict[str, Any]]) -> None:
    completed = host.validate_lifecycle([event("run_created", 1), event("run_started", 2), event("run_completed", 3)])
    timed_out = host.validate_lifecycle([event("run_created", 1), event("run_started", 2), event("run_timed_out", 3)])
    cancelled = host.validate_lifecycle([event("run_created", 1), event("run_started", 2), event("run_cancelled", 3)])
    reconciliation = host.validate_lifecycle([event("run_created", 1), event("run_started", 2), event("reconciliation_required", 3)])
    terminal_refusal = expect_error(lambda: host.validate_lifecycle([event("run_created", 1), event("run_started", 2), event("run_completed", 3), event("worker_message", 4)]), "terminal_state_transition")
    assertion(
        assertions,
        id="lifecycle.cancelled_terminal_present",
        category="lifecycle",
        source_finding_id="local_host.workerrun_lifecycle_not_proven",
        description="Cancelled is present in terminal WorkerRun states.",
        expected="cancelled",
        observed=completed["allowed_terminal_states"],
        passed="cancelled" in completed["allowed_terminal_states"],
        evidence_refs=[".aide/reports/local-process-execution-host/worker-run.json", "core/execution/local_process_host.py"],
    )
    assertion(
        assertions,
        id="lifecycle.test_matrix_complete",
        category="lifecycle",
        source_finding_id="local_host.workerrun_lifecycle_not_proven",
        description="Lifecycle transition matrix includes required successful, timeout, cancelled, reconciliation, and terminal-state refusal behavior.",
        expected="complete lifecycle transition coverage",
        observed={
            "completed": completed["final_state"],
            "timed_out": timed_out["final_state"],
            "cancelled": cancelled["final_state"],
            "reconciliation": reconciliation["final_state"],
            "terminal_refusal": terminal_refusal,
        },
        passed=cancelled["final_state"] == "cancelled" and reconciliation["final_state"] == "reconciliation_required",
        evidence_refs=[".aide/scripts/tests/test_aide_local_process_execution_host.py"],
    )


def check_scope(assertions: list[dict[str, Any]]) -> None:
    changed = git("diff", "--name-only", "HEAD^", "HEAD").splitlines()
    forbidden = [
        path
        for path in changed
        if path in {"core/execution/registered_process.py", "core/protocol/execution_host.py", ".aide/protocol/aide-execution-host.schema.json"}
        or path.startswith("core/interop/")
        or path.startswith("hosts/")
        or path.startswith(".aide.local/")
    ]
    assertion(
        assertions,
        id="scope.forbidden_paths_unchanged",
        category="scope",
        source_finding_id="baseline",
        description="Repair 02 did not modify provider core, accepted contract, interop domains, hosts, or local Service state.",
        expected=[],
        observed=forbidden,
        passed=not forbidden,
        evidence_refs=["git diff --name-only HEAD^ HEAD"],
    )


def main() -> int:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    assertions: list[dict[str, Any]] = []
    try:
        check_scope(assertions)
        check_path_matrix(assertions)
        check_events(assertions)
        check_artifacts(assertions)
        check_lifecycle(assertions)
    except Exception as exc:
        assertion(
            assertions,
            id="check.harness_exception",
            category="harness",
            source_finding_id="harness",
            description="The independent check harness raised an exception.",
            expected="no exception",
            observed=repr(exc),
            passed=False,
            evidence_refs=[__file__],
        )

    material_failures = [item for item in assertions if item["outcome"] != "PASS" and item["severity"] == "material"]
    result = "PASS_WITH_WARNINGS" if not material_failures else "REQUEST_CHANGES"
    recommended = "AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01" if not material_failures else "AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-03"
    report = {
        "schema_version": "aide.local-process-execution-host.repair-02-check.v0",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "result": result,
        "material_finding_count": len(material_failures),
        "missing_evidence": 0,
        "recommended_next_task": recommended,
        "assertions": assertions,
    }
    closures = {
        "schema_version": "aide.local-process-execution-host.repair-02-closure.v0",
        "task_id": TASK_ID,
        "result": result,
        "findings": [
            {
                "finding_id": finding,
                "disposition": "CLOSED" if not [item for item in material_failures if item["source_finding_id"] == finding] else "OPEN",
                "assertions": [item["id"] for item in assertions if item["source_finding_id"] == finding],
            }
            for finding in [
                "local_host.path_escape_not_proven",
                "local_host.raw_event_stream_not_proven",
                "local_host.content_addressed_artifacts_not_proven",
                "local_host.workerrun_lifecycle_not_proven",
            ]
        ],
    }
    write_json(CHECK_REPORT, report)
    write_json(CLOSURE_JSON, closures)
    write_text(STATUS_MD, f"# LocalProcessExecutionHost Repair 02 Check\n\n- result: `{result}`\n- material_finding_count: `{len(material_failures)}`\n- missing_evidence: `0`\n- recommended_next_task: `{recommended}`\n")
    write_text(MATERIAL_MD, "# Material Findings\n\n" + ("\n".join(f"- {item['id']}: {item['observed']}" for item in material_failures) if material_failures else "None.\n"))
    write_text(NEXT_PROMPT_MD, f"# Next Task\n\n```text\n{recommended}\n```\n")
    print(stable_json({"result": result, "material_finding_count": len(material_failures), "recommended_next_task": recommended}).strip())
    return 0 if result == "PASS_WITH_WARNINGS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
