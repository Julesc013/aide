from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import sys
import tempfile
from hashlib import sha256
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01"
SOURCE_TASK_ID = "AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01"
CHECKED_CAPABILITY = "local_trust_enforcement_v0"
NEXT_TASK = "AIDE-ACCEPT-LOCAL-TRUST-ENFORCEMENT-V0-01"
REPAIR_TASK = "AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-REPAIR-01"

REPO_ROOT = Path(__file__).resolve().parents[4]
EVIDENCE_ROOT = REPO_ROOT / ".aide/queue" / TASK_ID / "evidence"
REPORT_ROOT = REPO_ROOT / ".aide/reports/local-trust-enforcement-v0-check"
SOURCE_REPORT_ROOT = REPO_ROOT / ".aide/reports/local-trust-enforcement-v0"

EXPECTED_REFUSAL_CODES = [
    "approval_required",
    "capability_not_admitted",
    "delegation_expired",
    "delegation_not_allowed",
    "delegation_scope_widening",
    "effect_not_granted",
    "execution_mode_not_granted",
    "grant_exhausted",
    "grant_expired",
    "grant_inactive",
    "grant_missing",
    "grant_revoked",
    "implementation_digest_mismatch",
    "implementation_not_admitted",
    "network_not_granted",
    "policy_denied",
    "principal_inactive",
    "principal_unknown",
    "required_feature_unsupported",
    "resource_scope_mismatch",
    "secret_not_granted",
    "workspace_scope_mismatch",
]

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
    "implementation_repair",
    "capability_acceptance",
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
    "github_mutation",
    "release_or_promotion",
]


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith(" ") or line.startswith("-") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value == "null":
            data[key] = None
        elif value in {"true", "false"}:
            data[key] = value == "true"
        elif value.isdigit():
            data[key] = int(value)
        else:
            data[key] = value
    return data


def git_status() -> str:
    result = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
        shell=False,
    )
    return result.stdout


def run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )


def assertion(
    assertions: list[dict[str, Any]],
    *,
    id: str,
    category: str,
    description: str,
    expected: Any,
    observed: Any,
    passed: bool,
    evidence_refs: list[str],
) -> None:
    assertions.append(
        {
            "id": id,
            "category": category,
            "description": description,
            "outcome": "PASS" if passed else "FAIL",
            "severity": "material",
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs,
            "source_finding_id": None,
        }
    )


def load_sut_modules() -> tuple[Any, Any]:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    from core.protocol import trust_authorization
    from core.service import local_trust_enforcement

    return local_trust_enforcement, trust_authorization


def inspect_sqlite(db_path: Path) -> dict[str, Any]:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        tables = [
            row["name"]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            ).fetchall()
        ]
        objects = conn.execute("SELECT ref, kind, version, body_json FROM objects ORDER BY ref").fetchall()
        events = conn.execute("SELECT sequence, event_type, subject_ref, body_json FROM events ORDER BY sequence").fetchall()
        idempotency = conn.execute("SELECT * FROM idempotency ORDER BY idempotency_key").fetchall()
        grant_rows = [
            row
            for row in objects
            if row["kind"] == "CapabilityGrant" and row["ref"] == "aide://grant/local-process-host-one-use"
        ]
        eval_rows = [row for row in objects if row["kind"] == "AuthorizationEvaluation"]
        grant_body = json.loads(grant_rows[0]["body_json"]) if grant_rows else {}
        eval_body = json.loads(eval_rows[0]["body_json"]) if eval_rows else {}
        return {
            "tables": tables,
            "object_kinds": sorted(row["kind"] for row in objects),
            "object_count": len(objects),
            "event_sequences": [int(row["sequence"]) for row in events],
            "event_types": [row["event_type"] for row in events],
            "event_subjects": [row["subject_ref"] for row in events],
            "idempotency_count": len(idempotency),
            "idempotency_keys": [row["idempotency_key"] for row in idempotency],
            "grant_status": grant_body.get("spec", {}).get("status"),
            "grant_remaining_uses": grant_body.get("spec", {}).get("remaining_uses"),
            "grant_version": int(grant_rows[0]["version"]) if grant_rows else None,
            "evaluation_result": eval_body.get("spec", {}).get("result"),
            "evaluation_reason_codes": eval_body.get("spec", {}).get("reason_codes"),
        }
    finally:
        conn.close()


def report_scrubbed(paths: list[Path]) -> dict[str, Any]:
    root_native = str(REPO_ROOT)
    root_posix = REPO_ROOT.as_posix()
    secret_patterns = [
        r"(?i)api[_-]?key\s*[:=]",
        r"(?i)token\s*[:=]\s*[A-Za-z0-9_\-]{12,}",
        r"(?i)password\s*[:=]",
        r"(?i)secret\s*[:=]",
        r"(?i)private[_-]?key\s*[:=]",
    ]
    leaks: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if root_native in text or root_posix in text:
            leaks.append(path.relative_to(REPO_ROOT).as_posix() + ":absolute_path")
        for pattern in secret_patterns:
            if re.search(pattern, text):
                leaks.append(path.relative_to(REPO_ROOT).as_posix() + ":secret_pattern")
    return {"leaks": leaks, "scrubbed": not leaks}


def scan_no_external_execution() -> dict[str, Any]:
    source = (REPO_ROOT / "core/service/local_trust_enforcement.py").read_text(encoding="utf-8")
    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "Popen(",
        "import socket",
        "socket.",
        "requests.",
        "urllib.request",
        "http.client",
        "shell=True",
    ]
    hits = [pattern for pattern in forbidden_patterns if pattern in source]
    return {"forbidden_hits": hits, "passed": not hits}


def main() -> int:
    assertions: list[dict[str, Any]] = []
    source_status = simple_yaml(REPO_ROOT / ".aide/queue" / SOURCE_TASK_ID / "status.yaml")
    source_task = simple_yaml(REPO_ROOT / ".aide/queue" / SOURCE_TASK_ID / "task.yaml")
    source_validation = read_json(SOURCE_REPORT_ROOT / "validation.json")
    source_fixture = read_json(SOURCE_REPORT_ROOT / "fixture-report.json")

    source_observed = {
        "task_status": source_task.get("status"),
        "task_result": source_task.get("result"),
        "status_result": source_status.get("result"),
        "missing_evidence": source_status.get("missing_evidence"),
        "recommended_next_task": source_status.get("recommended_next_task"),
        "validation_status": source_validation.get("status"),
        "validation_validated": source_validation.get("validated"),
        "fixture_status": source_fixture.get("status"),
    }
    assertion(
        assertions,
        id="source.task_chain",
        category="source-chain",
        description="Source build task reports the expected capability, result, evidence, and route.",
        expected={
            "result": "PASS_WITH_WARNINGS",
            "missing_evidence": 0,
            "next": TASK_ID,
            "validated": True,
        },
        observed=source_observed,
        passed=(
            source_observed["task_result"] == "PASS_WITH_WARNINGS"
            and source_observed["status_result"] == "PASS_WITH_WARNINGS"
            and source_observed["missing_evidence"] == 0
            and source_observed["recommended_next_task"] == TASK_ID
            and source_observed["validation_validated"] is True
        ),
        evidence_refs=[
            f".aide/queue/{SOURCE_TASK_ID}/task.yaml",
            f".aide/queue/{SOURCE_TASK_ID}/status.yaml",
            ".aide/reports/local-trust-enforcement-v0/validation.json",
            ".aide/reports/local-trust-enforcement-v0/fixture-report.json",
        ],
    )

    local_trust, trust_authorization = load_sut_modules()
    before_status = git_status()
    with tempfile.TemporaryDirectory(prefix="aide-local-trust-check-") as tmp1, tempfile.TemporaryDirectory(
        prefix="aide-local-trust-check-"
    ) as tmp2:
        report1 = local_trust.fixture(REPO_ROOT, state_root=Path(tmp1), write_reports=False)
        report2 = local_trust.fixture(REPO_ROOT, state_root=Path(tmp2), write_reports=False)
        sqlite_state = inspect_sqlite(Path(tmp1) / "state.sqlite")
    after_fixture_status = git_status()

    assertion(
        assertions,
        id="enforcement.allowed_consumes_grant",
        category="enforcement",
        description="Allowed authorization evaluation persists and consumes the one-use grant.",
        expected={"evaluation_result": "allowed", "grant_status": "consumed", "remaining_uses": 0},
        observed={
            "evaluation_result": report1.get("evaluation_result"),
            "grant_consumed": report1.get("grant_consumed"),
            "grant_remaining_uses": report1.get("grant_remaining_uses"),
            "sqlite_grant_status": sqlite_state["grant_status"],
            "sqlite_grant_remaining_uses": sqlite_state["grant_remaining_uses"],
        },
        passed=(
            report1.get("evaluation_result") == "allowed"
            and report1.get("grant_consumed") is True
            and report1.get("grant_remaining_uses") == 0
            and sqlite_state["grant_status"] == "consumed"
            and sqlite_state["grant_remaining_uses"] == 0
        ),
        evidence_refs=[f".aide/queue/{TASK_ID}/evidence/independent_local_trust_check.py"],
    )

    assertion(
        assertions,
        id="enforcement.final_use_and_idempotency",
        category="enforcement",
        description="Idempotent replay adds no second event and a second final-use attempt fails closed.",
        expected={"idempotency_count": 1, "event_sequences": [1, 2], "second_final_use_refused": True},
        observed={
            "idempotent_replay_no_second_event": report1.get("idempotent_replay_no_second_event"),
            "concurrent_final_use_refused": report1.get("concurrent_final_use_refused"),
            "sqlite_idempotency_count": sqlite_state["idempotency_count"],
            "sqlite_event_sequences": sqlite_state["event_sequences"],
        },
        passed=(
            report1.get("idempotent_replay_no_second_event") is True
            and report1.get("concurrent_final_use_refused") is True
            and sqlite_state["idempotency_count"] == 1
            and sqlite_state["event_sequences"] == [1, 2]
        ),
        evidence_refs=[f".aide/queue/{TASK_ID}/evidence/independent_local_trust_check.py"],
    )

    expected_kinds = [
        "AdmissionRecord",
        "AuthorizationEvaluation",
        "CapabilityGrant",
        "DelegationRecord",
        "PolicyDecision",
        "Principal",
    ]
    assertion(
        assertions,
        id="persistence.sqlite_objects_events",
        category="persistence",
        description="SQLite persistence contains the expected trust objects, monotonic events, and grant-consumption event.",
        expected={
            "object_kinds": expected_kinds,
            "event_types": ["trust.authorization_evaluated", "trust.grant_consumed"],
        },
        observed=sqlite_state,
        passed=(
            sqlite_state["object_kinds"] == expected_kinds
            and sqlite_state["event_sequences"] == [1, 2]
            and sqlite_state["event_types"] == ["trust.authorization_evaluated", "trust.grant_consumed"]
            and sqlite_state["evaluation_result"] == "allowed"
            and sqlite_state["grant_version"] == 2
        ),
        evidence_refs=[f".aide/queue/{TASK_ID}/evidence/independent_local_trust_check.py"],
    )

    matrix = trust_authorization.negative_evaluation_matrix()
    matrix_codes = sorted(matrix)
    matrix_reason_self_refs = {
        code: code in matrix[code].get("spec", {}).get("reason_codes", [])
        for code in matrix_codes
    }
    assertion(
        assertions,
        id="refusal.matrix_complete",
        category="refusal-matrix",
        description="Negative authorization matrix covers every expected refusal code and each fixture carries its own code.",
        expected=EXPECTED_REFUSAL_CODES,
        observed={"codes": matrix_codes, "self_refs": matrix_reason_self_refs},
        passed=matrix_codes == EXPECTED_REFUSAL_CODES and all(matrix_reason_self_refs.values()),
        evidence_refs=[
            "core/protocol/trust_authorization.py",
            f".aide/queue/{TASK_ID}/evidence/independent_local_trust_check.py",
        ],
    )

    boundary_values = {field: report1.get(field) for field in FALSE_BOUNDARY_FIELDS}
    no_external = scan_no_external_execution()
    assertion(
        assertions,
        id="boundary.false_no_external_execution",
        category="authority-boundary",
        description="False-boundary fields remain false and local-trust implementation does not launch processes or use network clients.",
        expected={"all_false": True, "forbidden_source_hits": []},
        observed={"boundary_values": boundary_values, "source_scan": no_external},
        passed=all(value is False for value in boundary_values.values()) and no_external["passed"],
        evidence_refs=[
            "core/service/local_trust_enforcement.py",
            f".aide/queue/{TASK_ID}/evidence/independent_local_trust_check.py",
        ],
    )

    semantic_report1 = json.loads(stable_json(report1))
    semantic_report2 = json.loads(stable_json(report2))
    assertion(
        assertions,
        id="determinism.fixture_semantics",
        category="determinism",
        description="Two clean fixture runs produce identical semantic reports.",
        expected=True,
        observed={
            "digest_1": "sha256:" + sha256(stable_json(semantic_report1).encode("utf-8")).hexdigest(),
            "digest_2": "sha256:" + sha256(stable_json(semantic_report2).encode("utf-8")).hexdigest(),
        },
        passed=semantic_report1 == semantic_report2,
        evidence_refs=[f".aide/queue/{TASK_ID}/evidence/independent_local_trust_check.py"],
    )

    cli_result = run_cli([".aide/scripts/aide_lite.py", "local-trust", "fixture"])
    after_cli_status = git_status()
    cli_observed = {
        "returncode": cli_result.returncode,
        "stderr": cli_result.stderr,
        "stdout_contains": {
            "result": "result: PASS_WITH_WARNINGS" in cli_result.stdout,
            "capability": "capability_label: local_trust_enforcement_v0" in cli_result.stdout,
            "process_false": "process_launch_performed: false" in cli_result.stdout,
            "network_false": "network_calls_performed: false" in cli_result.stdout,
            "worker_false": "worker_execution_performed: false" in cli_result.stdout,
        },
    }
    assertion(
        assertions,
        id="cli.fixture_boundary",
        category="cli",
        description="Public local-trust fixture command succeeds and reports the same false boundaries.",
        expected={"returncode": 0, "stdout_contains": "all true", "stderr": ""},
        observed=cli_observed,
        passed=cli_result.returncode == 0 and not cli_result.stderr and all(cli_observed["stdout_contains"].values()),
        evidence_refs=[f".aide/queue/{TASK_ID}/evidence/independent_local_trust_check.py"],
    )

    assertion(
        assertions,
        id="cleanliness.git_status_unchanged",
        category="cleanliness",
        description="Check harness and public fixture do not create unexpected checkout churn beyond the check task outputs.",
        expected={"status_after_sut_fixture": before_status, "status_after_cli": "same or only check outputs"},
        observed={
            "before": before_status,
            "after_sut_fixture": after_fixture_status,
            "after_cli": after_cli_status,
        },
        passed=before_status == after_fixture_status and "core/service" not in after_cli_status and ".aide.local" not in after_cli_status,
        evidence_refs=[f".aide/queue/{TASK_ID}/evidence/independent_local_trust_check.py"],
    )

    scrub = report_scrubbed(
        [
            SOURCE_REPORT_ROOT / "fixture-report.json",
            SOURCE_REPORT_ROOT / "validation.json",
            SOURCE_REPORT_ROOT / "status.md",
            SOURCE_REPORT_ROOT / "explicit-non-capabilities.md",
        ]
    )
    assertion(
        assertions,
        id="reports.source_reports_scrubbed",
        category="report-integrity",
        description="Committed source reports contain no local absolute checkout paths or secret-like assignments.",
        expected={"scrubbed": True, "leaks": []},
        observed=scrub,
        passed=scrub["scrubbed"],
        evidence_refs=[".aide/reports/local-trust-enforcement-v0/**"],
    )

    failures = [item for item in assertions if item["outcome"] != "PASS"]
    result = "PASS_WITH_WARNINGS" if not failures else "REQUEST_CHANGES"
    recommended = NEXT_TASK if not failures else REPAIR_TASK
    check_report = {
        "task_id": TASK_ID,
        "checked_task": SOURCE_TASK_ID,
        "checked_capability": CHECKED_CAPABILITY,
        "result": result,
        "status": result,
        "material_finding_count": len(failures),
        "missing_evidence": 0,
        "assertions": assertions,
        "warnings": [
            "Check uses production local-trust modules as the system under test but does not repair them.",
            "Local trust enforcement remains local, deterministic, fixture-backed, and not an external IAM or transaction approval system.",
        ],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "recommended_next_task": recommended,
    }

    write_json(EVIDENCE_ROOT / "assertions.json", assertions)
    write_json(EVIDENCE_ROOT / "check-report.json", check_report)
    write_json(REPORT_ROOT / "assertions.json", assertions)
    write_json(REPORT_ROOT / "check-report.json", check_report)
    write_text(
        REPORT_ROOT / "status.md",
        "\n".join(
            [
                "# Local Trust Enforcement v0 Check",
                "",
                f"- status: {result}",
                f"- checked_task: {SOURCE_TASK_ID}",
                f"- checked_capability: {CHECKED_CAPABILITY}",
                f"- material_finding_count: {len(failures)}",
                "- missing_evidence: 0",
                f"- recommended_next_task: {recommended}",
                "",
                "## Warnings",
                "",
                "- Check uses production local-trust modules as the system under test but does not repair them.",
                "- Local trust enforcement remains local, deterministic, fixture-backed, and not an external IAM or transaction approval system.",
            ]
        )
        + "\n",
    )
    write_text(
        REPORT_ROOT / "validation.md",
        "\n".join(
            [
                "# Local Trust Enforcement Check Validation",
                "",
                f"- status: {result}",
                f"- assertions: {len(assertions)}",
                f"- failed_assertions: {len(failures)}",
                f"- recommended_next_task: {recommended}",
            ]
        )
        + "\n",
    )
    write_text(
        REPORT_ROOT / "explicit-non-capabilities.md",
        "# Explicit Non-Capabilities\n\n" + "\n".join(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES) + "\n",
    )
    write_text(
        REPORT_ROOT / "next-task-prompt.md",
        f"# Next Task Prompt\n\n```text\nCreate and process {recommended}.\n```\n",
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
