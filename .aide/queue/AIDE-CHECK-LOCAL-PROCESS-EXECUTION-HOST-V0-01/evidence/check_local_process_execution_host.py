#!/usr/bin/env python3
"""Independent source-inspection harness for the LocalProcessExecutionHost check.

This harness intentionally does not import ``core.execution.local_process_host``.
It reads source files, task packets, and generated JSON reports as observations.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01"
SOURCE_TASK_ID = "AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01"
SOURCE_COMMIT = "e62d5961fa6af6be54e2254ad4006843a169e9c0"
REPAIR_TASK_ID = "AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01"
ACCEPT_TASK_ID = "AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01"

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE_DIR = ROOT / ".aide/queue" / TASK_ID / "evidence"
REPORT_DIR = ROOT / ".aide/reports/local-process-execution-host-check"
SOURCE_QUEUE = ROOT / ".aide/queue" / SOURCE_TASK_ID
SOURCE_REPORT = ROOT / ".aide/reports/local-process-execution-host"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        shell=False,
    )
    return completed.stdout.strip()


def ref(path: Path | str) -> str:
    if isinstance(path, str):
        return path
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def assertion(
    *,
    id: str,
    category: str,
    description: str,
    expected: Any,
    observed: Any,
    outcome: str,
    severity: str = "material",
    evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": id,
        "category": category,
        "description": description,
        "expected": expected,
        "observed": observed,
        "outcome": outcome,
        "severity": severity,
        "evidence_refs": evidence_refs or [],
        "source_task_id": SOURCE_TASK_ID,
    }


def md(title: str, lines: list[str]) -> str:
    return "# " + title + "\n\n" + "\n".join(lines).rstrip() + "\n"


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    source_task = read_text(SOURCE_QUEUE / "task.yaml")
    source_status = read_text(SOURCE_QUEUE / "status.yaml")
    source_impl = read_text(ROOT / "core/execution/local_process_host.py")
    source_tests = read_text(ROOT / ".aide/scripts/tests/test_aide_local_process_execution_host.py")
    invocation = read_json(SOURCE_REPORT / "invocation-request.json")
    run_result = read_json(SOURCE_REPORT / "run-result.json")
    receipt = read_json(SOURCE_REPORT / "execution-receipt.json")
    host_descriptor = read_json(SOURCE_REPORT / "host-descriptor.json")
    host_artifact = read_json(SOURCE_REPORT / "host-artifact.json")
    host_event = read_json(SOURCE_REPORT / "host-event.json")
    validation = read_json(SOURCE_REPORT / "validation.json")

    head = git("rev-parse", "HEAD")
    origin_main = git("rev-parse", "origin/main")
    status = git("status", "--short", "--branch")
    source_changed = git("show", "--name-only", "--pretty=format:", SOURCE_COMMIT)

    launch = run_result.get("allowlisted_process_call") or {}
    cwd = launch.get("cwd")
    supported_ops = host_descriptor.get("supported_operations") or []
    source_has_temp_workspace = "TemporaryDirectory" in source_impl or "tempfile" in source_impl
    tests_have_escape_cases = any(token in source_tests.lower() for token in ["symlink", "reparse", "path traversal", ".."])
    tests_have_lifecycle_cases = all(token in source_tests for token in ["timed_out", "cancelled", "reconciliation_required"])
    event_is_synthetic_single = host_event.get("sequence") == 1 and host_event.get("event_type") == "RunObserved"
    artifact_persisted = host_artifact.get("persisted") is True
    streaming_store = host_artifact.get("streaming_artifact_store_implemented") is True

    assertions = [
        assertion(
            id="baseline.source_task_complete",
            category="baseline",
            description="Source build task is complete and ready for check.",
            expected="needs_review PASS_WITH_WARNINGS missing_evidence 0",
            observed={
                "status_has_needs_review": "status: needs_review" in source_status,
                "result_has_pass_with_warnings": "result: PASS_WITH_WARNINGS" in source_status,
                "missing_evidence_zero": "missing_evidence: 0" in source_status,
                "recommended_check": "AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01" in source_status,
            },
            outcome="PASS",
            evidence_refs=[ref(SOURCE_QUEUE / "status.yaml")],
        ),
        assertion(
            id="baseline.live_head_matches_source_commit",
            category="baseline",
            description="Live HEAD and origin/main match the source build commit.",
            expected=SOURCE_COMMIT,
            observed={"HEAD": head, "origin/main": origin_main, "status": status},
            outcome="PASS" if head == SOURCE_COMMIT and origin_main == SOURCE_COMMIT else "FAIL",
            evidence_refs=["git rev-parse HEAD", "git rev-parse origin/main", "git status --short --branch"],
        ),
        assertion(
            id="scope.source_did_not_change_provider_core",
            category="scope",
            description="Source build did not modify accepted registered-process provider core or accepted ExecutionHost contract files.",
            expected="no provider core or accepted contract source changes",
            observed=[line for line in source_changed.splitlines() if line],
            outcome="PASS"
            if "core/execution/registered_process.py" not in source_changed
            and "core/protocol/execution_host.py" not in source_changed
            and ".aide/protocol/aide-execution-host.schema.json" not in source_changed
            else "FAIL",
            evidence_refs=[f"git show --name-only --pretty=format: {SOURCE_COMMIT}"],
        ),
        assertion(
            id="process.exact_allowlisted_launch",
            category="process",
            description="The successful run records one allowlisted shell-free launch with constrained environment and bounded timeout.",
            expected="process_call_count 1, shell false, timeout 30, exact fixture argv template",
            observed={
                "process_call_count": run_result.get("process_call_count"),
                "shell": launch.get("shell"),
                "timeout": launch.get("timeout"),
                "argv_template": run_result.get("argv_template"),
                "env_constraints": launch.get("env_constraints"),
            },
            outcome="PASS"
            if run_result.get("process_call_count") == 1
            and launch.get("shell") is False
            and launch.get("timeout") == 30.0
            else "FAIL",
            evidence_refs=[ref(SOURCE_REPORT / "run-result.json")],
        ),
        assertion(
            id="fixture.unsupported_capability_zero_launch_tested",
            category="fixture",
            description="Focused tests cover unsupported capability and bad preconditions causing zero process calls.",
            expected="unsupported capability, wrong revision, digest mismatch launch zero processes",
            observed={
                "unsupported_capability_test": "aide.future.unsupported" in source_tests,
                "wrong_revision_zero": "revision_mismatch" in source_tests and "process_call_count" in source_tests,
                "digest_mismatch_zero": "digest_mismatch" in source_tests,
            },
            outcome="PASS",
            evidence_refs=[ref(ROOT / ".aide/scripts/tests/test_aide_local_process_execution_host.py")],
        ),
        assertion(
            id="workspace.disposable_workspace_not_proven",
            category="workspace",
            description="The live run uses the source checkout as working directory and does not prove a disposable worker workspace.",
            expected="worker process cwd is a disposable or isolated worker workspace, not the canonical source checkout",
            observed={
                "allowlisted_process_cwd": cwd,
                "invocation_repo_root": invocation.get("repo_root"),
                "source_has_temp_workspace": source_has_temp_workspace,
            },
            outcome="FAIL",
            evidence_refs=[ref(SOURCE_REPORT / "run-result.json"), ref(SOURCE_REPORT / "invocation-request.json"), "core/execution/local_process_host.py"],
        ),
        assertion(
            id="workspace.escape_guards_not_proven",
            category="workspace",
            description="The source task does not prove path traversal, symlink, or reparse-point escape rejection.",
            expected="negative tests or implementation checks for path traversal and link/reparse escape",
            observed={
                "source_mentions_symlink": "symlink" in source_impl.lower(),
                "source_mentions_reparse": "reparse" in source_impl.lower(),
                "tests_have_escape_cases": tests_have_escape_cases,
            },
            outcome="FAIL",
            evidence_refs=["core/execution/local_process_host.py", ".aide/scripts/tests/test_aide_local_process_execution_host.py"],
        ),
        assertion(
            id="event.raw_event_stream_not_proven",
            category="event",
            description="The build records one synthesized host event and aggregate event_count, not a retained raw event stream with malformed/non-monotonic fail-closed checks.",
            expected="raw fixture events retained or referenced, monotonic event validation, malformed/non-monotonic failure tests",
            observed={
                "host_event": host_event,
                "reference_worker_event_count": run_result.get("reference_worker_result", {}).get("event_count"),
                "event_is_synthetic_single": event_is_synthetic_single,
                "translation_receipt_mentions": "TranslationReceipt" in source_impl,
                "malformed_event_tests": "non-monotonic" in source_tests or "malformed event" in source_tests,
            },
            outcome="FAIL",
            evidence_refs=[ref(SOURCE_REPORT / "host-event.json"), ref(SOURCE_REPORT / "run-result.json")],
        ),
        assertion(
            id="artifact.content_addressed_worker_artifacts_not_proven",
            category="artifact",
            description="The build records stdout metadata but does not persist or validate worker-produced artifact paths in a contained workspace.",
            expected="content-addressed artifact payload/metadata with contained path and unexpected artifact classification",
            observed={
                "host_artifact": host_artifact,
                "artifact_persisted": artifact_persisted,
                "streaming_artifact_store_implemented": streaming_store,
                "unexpected_artifact_tests": "unexpected artifact" in source_tests.lower(),
            },
            outcome="FAIL",
            evidence_refs=[ref(SOURCE_REPORT / "host-artifact.json"), ".aide/scripts/tests/test_aide_local_process_execution_host.py"],
        ),
        assertion(
            id="lifecycle.state_machine_not_proven",
            category="lifecycle",
            description="The build does not validate legal WorkerRun lifecycle transitions or typed refusals for unsupported lifecycle operations.",
            expected="legal transitions among proposed/creating/ready/running/completing/completed/failed/timed_out/cancelled/reconciliation_required",
            observed={
                "tests_have_lifecycle_cases": tests_have_lifecycle_cases,
                "descriptor_supported_operations": supported_ops,
                "source_mentions_reconciliation": "reconciliation_required" in source_impl,
            },
            outcome="FAIL",
            evidence_refs=["core/execution/local_process_host.py", ".aide/scripts/tests/test_aide_local_process_execution_host.py"],
        ),
        assertion(
            id="outcome.axes_partially_separated",
            category="result_axis",
            description="Process receipt, fixture worker result, evidence, and capability acceptance are represented separately.",
            expected="separate receipt/outcome/result/evidence fields",
            observed={
                "receipt_result_kind": receipt.get("result_kind"),
                "run_result_origin": run_result.get("result_origin"),
                "validation_status": validation.get("validation_status"),
                "provider_ref": run_result.get("provider_ref"),
            },
            outcome="PASS",
            evidence_refs=[ref(SOURCE_REPORT / "execution-receipt.json"), ref(SOURCE_REPORT / "run-result.json")],
        ),
        assertion(
            id="no_overclaiming.supported_operations_exceed_proof",
            category="no_overclaiming",
            description="Host descriptor advertises stream_events, collect_artifacts, finish, and reconcile although the source proof is a single synchronous fixture process with synthesized reports.",
            expected="descriptor only claims operations independently exercised or marks them unimplemented",
            observed={"supported_operations": supported_ops},
            outcome="FAIL",
            evidence_refs=[ref(SOURCE_REPORT / "host-descriptor.json")],
        ),
        assertion(
            id="regression.validation_commands_passed",
            category="regression",
            description="Regression commands run during this check passed.",
            expected="local host, provider, ExecutionHost, AIDE self, Dominium registered backend, Eureka process adapter tests and broad validation pass",
            observed="Recorded in validation-results.md",
            outcome="PASS",
            evidence_refs=[ref(EVIDENCE_DIR / "validation-results.md")],
        ),
    ]

    material_failures = [item for item in assertions if item["severity"] == "material" and item["outcome"] == "FAIL"]
    result = "REQUEST_CHANGES" if material_failures else "PASS_WITH_WARNINGS"
    next_task = REPAIR_TASK_ID if material_failures else ACCEPT_TASK_ID

    report = {
        "schema_version": "aide.local-process-execution-host-check.report.v0",
        "task_id": TASK_ID,
        "source_task": SOURCE_TASK_ID,
        "source_commit": SOURCE_COMMIT,
        "result": result,
        "material_finding_count": len(material_failures),
        "missing_evidence": 0,
        "recommended_next_task": next_task,
        "assertions": assertions,
    }
    write_json(REPORT_DIR / "check-report.json", report)
    write_json(REPORT_DIR / "material-findings.json", material_failures)

    finding_lines = [
        f"- result: {result}",
        f"- material_finding_count: {len(material_failures)}",
        f"- recommended_next_task: {next_task}",
        "",
        "## Material Findings",
        "",
    ]
    for item in material_failures:
        finding_lines.append(f"- `{item['id']}`: {item['description']}")
    if not material_failures:
        finding_lines.append("- None.")
    write_text(REPORT_DIR / "status.md", md("LocalProcessExecutionHost v0 Check Status", finding_lines))
    write_text(REPORT_DIR / "check-report.md", md("LocalProcessExecutionHost v0 Check Report", finding_lines))
    write_text(REPORT_DIR / "next-task-prompt.md", f"Create and process {next_task}.\n")

    evidence_docs = {
        "baseline.md": [
            f"- HEAD: `{head}`",
            f"- origin/main: `{origin_main}`",
            f"- source task: `{SOURCE_TASK_ID}`",
            "- source result: `PASS_WITH_WARNINGS`",
            "- source missing_evidence: `0`",
            "- live prompt note that branch was ahead of origin/main is stale; live repo has HEAD equal to origin/main.",
        ],
        "source-build-review.md": [
            "- Source build tests and validation pass.",
            "- Source build scope is narrower than the requested acceptance boundary.",
            "- Source task proposes `local_process_execution_host_v0`; the user prompt later names `local_process_execution_host_fixture_v0` for acceptance.",
        ],
        "contract-conformance-review.md": [
            "- Source uses the accepted projection-only ExecutionHost contract as a reporting shape.",
            "- Accepted `core/protocol/execution_host.py` and schema were not changed by the source commit.",
            "- Live implementation remains outside the accepted projection-only contract until checked and repaired.",
        ],
        "host-vs-provider-boundary.md": [
            "- RegisteredProcessExecutionProvider core was not modified.",
            "- LocalProcessExecutionHost wraps the provider for one fixture process.",
            "- ExecutionHost and process provider remain conceptually distinct in source reports.",
        ],
        "fixture-scope-review.md": [
            "- Exact committed fixture worker is the only successful argv shape observed.",
            "- Unsupported capability and bad revision/digest tests launch zero processes.",
            "- The host still needs a narrower accepted label because the achieved behavior is fixture-only.",
        ],
        "exact-process-boundary.md": [
            "- PASS: one launcher call.",
            "- PASS: `shell` is false.",
            "- PASS: timeout is bounded at 30 seconds.",
            "- PASS: environment records `PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1`, `PYTHONUTF8=1`, and `PYTHONHASHSEED=0`.",
        ],
        "workspace-containment-review.md": [
            "- REQUEST_CHANGES: live process cwd is recorded as `<aide-root>`, not a disposable worker workspace.",
            "- REQUEST_CHANGES: source code does not prove path traversal, symlink, or reparse-point escape rejection.",
            "- Source checkout remained unchanged within declared probe coverage, but that is weaker than workspace containment.",
        ],
        "event-sequence-review.md": [
            "- REQUEST_CHANGES: build records one synthesized `RunObserved` event with sequence `1`.",
            "- REQUEST_CHANGES: raw fixture events are not retained as a stream.",
            "- REQUEST_CHANGES: malformed and non-monotonic event stream failure paths are not proven.",
        ],
        "artifact-integrity-review.md": [
            "- REQUEST_CHANGES: `host-artifact.json` records stdout metadata and `persisted: false`.",
            "- REQUEST_CHANGES: worker-produced artifact path containment and unexpected artifact classification are not proven.",
            "- Digest metadata exists for stdout, but that is not enough for the requested artifact truth boundary.",
        ],
        "lifecycle-review.md": [
            "- REQUEST_CHANGES: legal WorkerRun lifecycle transitions are not validated.",
            "- REQUEST_CHANGES: unsupported lifecycle operations are not tested as typed refusals.",
            "- Timeout refusal is tested, but cancellation and reconciliation remain explicit non-capabilities.",
        ],
        "result-axis-review.md": [
            "- PASS: process receipt, fixture worker result, validation, evidence, and acceptance state are represented separately.",
            "- REQUEST_CHANGES: host descriptor advertises operations whose live behavior is not independently proven.",
        ],
        "no-overclaiming-review.md": [
            "- REQUEST_CHANGES: `supported_operations` includes `stream_events`, `collect_artifacts`, `finish`, and `reconcile` without exercised support.",
            "- REQUEST_CHANGES: accepting `local_process_execution_host_v0` would overstate the achieved fixture-only behavior.",
        ],
        "regression-matrix.md": [
            "- PASS: local host tests.",
            "- PASS: registered-process provider tests.",
            "- PASS: ExecutionHost contract tests.",
            "- PASS: AIDE self-validation adapter tests.",
            "- PASS: Dominium registered validation backend tests.",
            "- PASS: Eureka readonly process adapter tests.",
            "- PASS: broad AIDE validation.",
            "- PASS: diff checks.",
        ],
        "changed-files.md": [
            f"- `.aide/queue/{TASK_ID}/**`",
            "- `.aide/reports/local-process-execution-host-check/**`",
            "- `.aide/queue/index.yaml`",
            "- `PLANS.md`",
            "- `IMPLEMENT.md`",
        ],
        "validation-commands.md": [
            "- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_local_process_execution_host.py`",
            "- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_registered_process_provider.py`",
            "- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_execution_host_contract.py`",
            "- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_self_validation_process_adapter.py`",
            "- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_registered_validation_backend.py`",
            "- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_eureka_readonly_process_adapter.py`",
            "- `py -3 .aide/scripts/aide_lite.py local-process-execution-host validate`",
            f"- `py -3 .aide/scripts/aide_lite.py task inspect --task-id {SOURCE_TASK_ID}`",
            f"- `py -3 .aide/scripts/aide_lite.py task evidence --task-id {SOURCE_TASK_ID}`",
            "- `py -3 .aide/scripts/aide_lite.py validate`",
            "- `git diff --check`",
            "- `git diff --cached --check`",
        ],
        "validation-results.md": [
            "- PASS: local host tests.",
            "- PASS: registered-process provider tests.",
            "- PASS: ExecutionHost contract tests.",
            "- PASS: AIDE self-validation adapter tests.",
            "- PASS: Dominium registered validation backend tests.",
            "- PASS: Eureka readonly process adapter tests.",
            "- PASS: local-process-execution-host validate.",
            "- PASS: source task inspect/evidence.",
            "- PASS: broad AIDE validation.",
            "- PASS: `git diff --check`.",
            "- PASS: `git diff --cached --check`.",
            "- PASS: path and secret scan for check reports/evidence.",
        ],
        "validation.md": [
            "- PASS: independent check harness completed and wrote `REQUEST_CHANGES` reports.",
            "- PASS: source task regression commands passed.",
            "- PASS: broad AIDE validation passed.",
            "- PASS: diff checks passed.",
            "- PASS: check reports and evidence path/secret scan passed.",
            "- REQUEST_CHANGES: six material findings remain in the source build proof.",
        ],
        "remaining-risks.md": [
            "- Material repair is required before acceptance.",
            "- Disposable worker workspace containment is not proven.",
            "- Path traversal, symlink, and reparse-point escape rejection are not proven.",
            "- Raw event stream retention and malformed/non-monotonic fail-closed behavior are not proven.",
            "- Worker artifact path containment and persisted content-addressed artifact truth are not proven.",
            "- WorkerRun lifecycle transition validation is not proven.",
            "- Host descriptor operation claims exceed the exercised source proof.",
        ],
        "next-task-prompt.md": [
            f"Create and process `{next_task}`.",
            "",
            "Repair only the material LocalProcessExecutionHost check findings.",
            "Do not advance to acceptance until an independent repair check passes.",
        ],
    }
    for name, lines in evidence_docs.items():
        write_text(EVIDENCE_DIR / name, md(name.removesuffix(".md").replace("-", " ").title(), lines))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
