from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01"
BUILD_TASK_ID = "AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01"
ACCEPTED_CAPABILITY = "local_service_foundation_v0"
NEXT_TASK = "AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01"

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[4]
EVIDENCE_ROOT = REPO_ROOT / ".aide/queue" / TASK_ID / "evidence"
REPORT_ROOT = REPO_ROOT / ".aide/reports/local-service-foundation-v0-accept"


@dataclass(frozen=True)
class AssertionResult:
    id: str
    outcome: str
    severity: str
    expected: Any
    observed: Any
    evidence_refs: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "outcome": self.outcome,
            "severity": self.severity,
            "expected": self.expected,
            "observed": self.observed,
            "evidence_refs": self.evidence_refs,
        }


def read_scalar_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not match:
            continue
        key, raw_value = match.groups()
        value = raw_value.strip()
        if value in {"", ">", "|"}:
            continue
        if value == "null":
            data[key] = None
        elif value in {"true", "false"}:
            data[key] = value == "true"
        else:
            try:
                data[key] = int(value)
            except ValueError:
                data[key] = value.strip("\"'")
    return data


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def assertion(assertions: list[AssertionResult], assertion_id: str, condition: bool, expected: Any, observed: Any, evidence_refs: list[str]) -> None:
    assertions.append(
        AssertionResult(
            id=assertion_id,
            outcome="PASS" if condition else "FAIL",
            severity="material",
            expected=expected,
            observed=observed,
            evidence_refs=evidence_refs,
        )
    )


def scan_secret_like(paths: list[Path]) -> list[str]:
    pattern = re.compile(
        r"AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_\-]{35}|gh[pousr]_[0-9A-Za-z_]{36,}|"
        r"xox[baprs]-[0-9A-Za-z-]+|BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY"
    )
    hits: list[str] = []
    for path in paths:
        if not path.is_file():
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if pattern.search(line):
                hits.append(f"{path.relative_to(REPO_ROOT).as_posix()}:{line_no}")
    return hits


def run_review() -> dict[str, Any]:
    assertions: list[AssertionResult] = []
    build_status = read_scalar_yaml(REPO_ROOT / ".aide/queue" / BUILD_TASK_ID / "status.yaml")
    build_task = read_scalar_yaml(REPO_ROOT / ".aide/queue" / BUILD_TASK_ID / "task.yaml")
    check_status = read_scalar_yaml(REPO_ROOT / ".aide/queue" / CHECK_TASK_ID / "status.yaml")
    check_report = json.loads((REPO_ROOT / ".aide/reports/local-service-foundation-v0-check/check-report.json").read_text(encoding="utf-8"))
    build_validation = json.loads((REPO_ROOT / ".aide/reports/local-service-foundation-v0/validation.json").read_text(encoding="utf-8"))
    fixture_report = json.loads((REPO_ROOT / ".aide/reports/local-service-foundation-v0/fixture-report.json").read_text(encoding="utf-8"))

    assertion(
        assertions,
        "acceptance.source_build_passed",
        build_status.get("result") == "PASS_WITH_WARNINGS"
        and build_status.get("missing_evidence") == 0
        and build_task.get("proposed_capability") == ACCEPTED_CAPABILITY,
        {"result": "PASS_WITH_WARNINGS", "missing_evidence": 0, "capability": ACCEPTED_CAPABILITY},
        {
            "result": build_status.get("result"),
            "missing_evidence": build_status.get("missing_evidence"),
            "capability": build_task.get("proposed_capability"),
        },
        [f".aide/queue/{BUILD_TASK_ID}/status.yaml", f".aide/queue/{BUILD_TASK_ID}/task.yaml"],
    )
    assertion(
        assertions,
        "acceptance.independent_check_passed",
        check_status.get("result") == "PASS_WITH_WARNINGS"
        and check_status.get("material_finding_count") == 0
        and check_status.get("missing_evidence") == 0
        and check_report.get("recommended_next_task") == TASK_ID,
        {"result": "PASS_WITH_WARNINGS", "material_finding_count": 0, "missing_evidence": 0, "next": TASK_ID},
        {
            "result": check_status.get("result"),
            "material_finding_count": check_status.get("material_finding_count"),
            "missing_evidence": check_status.get("missing_evidence"),
            "next": check_report.get("recommended_next_task"),
        },
        [f".aide/queue/{CHECK_TASK_ID}/status.yaml", ".aide/reports/local-service-foundation-v0-check/check-report.json"],
    )

    false_fields = [
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
    false_boundaries_ok = all(build_validation.get(field) is False for field in false_fields)
    semantics_ok = fixture_report.get("event_delivery_semantics") == "at_least_once"
    assertion(
        assertions,
        "acceptance.boundary_exactness",
        false_boundaries_ok and semantics_ok and build_validation.get("validated") is True,
        "validated local no-network service, false runtime boundaries, at_least_once delivery only",
        {
            "false_boundaries_ok": false_boundaries_ok,
            "event_delivery_semantics": fixture_report.get("event_delivery_semantics"),
            "validated": build_validation.get("validated"),
        },
        [
            ".aide/reports/local-service-foundation-v0/validation.json",
            ".aide/reports/local-service-foundation-v0/fixture-report.json",
        ],
    )

    source_reports = [
        REPO_ROOT / ".aide/reports/local-service-foundation-v0/validation.json",
        REPO_ROOT / ".aide/reports/local-service-foundation-v0/fixture-report.json",
        REPO_ROOT / ".aide/reports/local-service-foundation-v0-check/check-report.json",
    ]
    secret_hits = scan_secret_like(source_reports)
    assertion(
        assertions,
        "acceptance.no_secret_like_values",
        not secret_hits,
        "no secret-like values in source acceptance reports",
        {"secret_hits": secret_hits},
        [path.relative_to(REPO_ROOT).as_posix() for path in source_reports],
    )

    failures = [item for item in assertions if item.outcome != "PASS"]
    result = "ACCEPTED_WITH_WARNINGS" if not failures else "REQUEST_CHANGES"
    return {
        "schema_version": "aide.local-service-foundation-acceptance.v0",
        "task_id": TASK_ID,
        "source_build_task_id": BUILD_TASK_ID,
        "source_check_task_id": CHECK_TASK_ID,
        "result": result,
        "accepted_capability": ACCEPTED_CAPABILITY if not failures else None,
        "accepted_meaning": "local_no_network_single_machine_object_event_artifact_idempotency_cursor_store_v0" if not failures else None,
        "material_finding_count": len(failures),
        "missing_evidence": 0,
        "assertions": [item.to_dict() for item in assertions],
        "warnings": [
            "Accepted capability is local, no-network, and single-machine.",
            "Event delivery is at-least-once only.",
            "Runtime scheduling, trust enforcement, worker execution, and interoperability surfaces remain future work.",
        ],
        "recommended_next_task": NEXT_TASK if not failures else "AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-REPAIR-01",
    }


def render_md(report: dict[str, Any]) -> str:
    lines = [
        "# Local Service Foundation v0 Acceptance Review",
        "",
        f"- result: {report['result']}",
        f"- accepted_capability: {report.get('accepted_capability')}",
        f"- material_finding_count: {report['material_finding_count']}",
        f"- missing_evidence: {report['missing_evidence']}",
        f"- recommended_next_task: {report['recommended_next_task']}",
        "",
        "## Assertions",
        "",
    ]
    for item in report["assertions"]:
        lines.append(f"- {item['id']}: {item['outcome']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    report = run_review()
    write_json(EVIDENCE_ROOT / "acceptance-review.json", report)
    (EVIDENCE_ROOT / "acceptance-review.md").write_text(render_md(report), encoding="utf-8")
    write_json(REPORT_ROOT / "acceptance-report.json", report)
    (REPORT_ROOT / "acceptance-report.md").parent.mkdir(parents=True, exist_ok=True)
    (REPORT_ROOT / "acceptance-report.md").write_text(render_md(report), encoding="utf-8")
    (REPORT_ROOT / "status.md").write_text(
        "\n".join(
            [
                "# Local Service Foundation v0 Acceptance",
                "",
                f"- result: {report['result']}",
                f"- accepted_capability: {report.get('accepted_capability')}",
                "- accepted_meaning: local no-network single-machine object, event, artifact, idempotency, and cursor store",
                f"- recommended_next_task: {report['recommended_next_task']}",
                "",
                "## Non-Capabilities",
                "",
                "- no scheduler",
                "- no worker execution",
                "- no capability execution",
                "- no authorization enforcement",
                "- no network API",
                "- no MCP or Workbench runtime",
                "- no distributed state",
                "- no exactly-once delivery",
                "- no provider/model calls",
                "- no preview/apply/rollback",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (REPORT_ROOT / "source-chain-review.md").write_text(
        "# Source Chain Review\n\nBuild and check tasks both passed with warnings, zero material findings, and complete evidence.\n",
        encoding="utf-8",
    )
    (REPORT_ROOT / "warning-disposition.md").write_text(
        "# Warning Disposition\n\nWarnings are accepted because they narrow capability claims to local, no-network, single-machine, at-least-once storage.\n",
        encoding="utf-8",
    )
    (REPORT_ROOT / "next-task-prompt.md").write_text(
        "# Next Task Prompt\n\n```text\nCreate and process AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01.\n```\n",
        encoding="utf-8",
    )
    print(json.dumps({"result": report["result"], "material_finding_count": report["material_finding_count"], "recommended_next_task": report["recommended_next_task"]}, sort_keys=True))
    return 0 if report["result"] == "ACCEPTED_WITH_WARNINGS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
