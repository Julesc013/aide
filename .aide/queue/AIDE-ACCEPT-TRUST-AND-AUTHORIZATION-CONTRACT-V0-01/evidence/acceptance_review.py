from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01"
BUILD_TASK_ID = "AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01"
ACCEPTED_CAPABILITY = "trust_and_authorization_contract_v0"
NEXT_TASK = "AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01"

FALSE_FIELDS = [
    "live_identity_implemented",
    "live_policy_engine_implemented",
    "live_grants_implemented",
    "credentials_embedded",
    "secrets_embedded",
    "oidc_iam_implemented",
    "runtime_enforcement_implemented",
    "worker_execution_implemented",
    "transaction_approval_implemented",
    "service_runtime_implemented",
    "provider_model_calls_performed",
    "network_calls_performed",
    "preview_apply_implemented",
    "repository_mutation_performed",
    "branch_worktree_mutation_performed",
    "github_mutation_performed",
    "release_or_promotion_performed",
]

SECRET_VALUE_RE = re.compile(
    r"AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_\-]{35}|gh[pousr]_[0-9A-Za-z_]{36,}|"
    r"xox[baprs]-[0-9A-Za-z-]+|BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY"
)


def find_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "AGENTS.md").is_file() and (parent / ".aide").is_dir():
            return parent
    raise RuntimeError("repository root not found")


ROOT = find_root()
EVIDENCE_DIR = ROOT / ".aide/queue" / TASK_ID / "evidence"
REPORT_DIR = ROOT / ".aide/reports/trust-authorization-contract-v0-accept"


def load_json(path: str) -> Any:
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assertion(id_: str, ok: bool, expected: Any, observed: Any, evidence_refs: list[str]) -> dict[str, Any]:
    return {
        "id": id_,
        "outcome": "PASS" if ok else "FAIL",
        "severity": "none" if ok else "material",
        "expected": expected,
        "observed": observed,
        "evidence_refs": evidence_refs,
    }


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    build_status = read_text(f".aide/queue/{BUILD_TASK_ID}/status.yaml")
    check_status = read_text(f".aide/queue/{CHECK_TASK_ID}/status.yaml")
    check_report = load_json(".aide/reports/trust-authorization-contract-v0-check/check-report.json")
    validation = load_json(".aide/reports/trust-authorization-contract-v0/validation.json")

    build_ok = all(
        marker in build_status
        for marker in [
            "result: PASS_WITH_WARNINGS",
            "proposed_capability: trust_and_authorization_contract_v0",
            "missing_evidence: 0",
            f"recommended_next_task: {CHECK_TASK_ID}",
        ]
    )
    check_ok = all(
        marker in check_status
        for marker in [
            "result: PASS_WITH_WARNINGS",
            "checked_capability: trust_and_authorization_contract_v0",
            "material_finding_count: 0",
            "missing_evidence: 0",
            f"recommended_next_task: {TASK_ID}",
        ]
    )
    report_ok = (
        check_report.get("result") == "PASS_WITH_WARNINGS"
        and check_report.get("checked_capability") == ACCEPTED_CAPABILITY
        and check_report.get("material_finding_count") == 0
        and check_report.get("missing_evidence") == 0
    )
    false_boundaries_ok = all(validation.get(field) is False for field in FALSE_FIELDS)
    projection_only_ok = validation.get("projection_only_truthful") is True

    scan_paths = [
        ".aide/reports/trust-authorization-contract-v0/validation.json",
        ".aide/reports/trust-authorization-contract-v0/projection-report.json",
        ".aide/reports/trust-authorization-contract-v0-check/check-report.json",
    ]
    secret_hits = [path for path in scan_paths if SECRET_VALUE_RE.search(read_text(path))]

    assertions = [
        assertion(
            "acceptance.source_build_passed",
            build_ok,
            "source build PASS_WITH_WARNINGS, proposed capability exact, missing_evidence 0",
            {"ok": build_ok},
            [f".aide/queue/{BUILD_TASK_ID}/status.yaml"],
        ),
        assertion(
            "acceptance.independent_check_passed",
            check_ok and report_ok,
            "check PASS_WITH_WARNINGS, material_finding_count 0, missing_evidence 0",
            {"status_ok": check_ok, "report_ok": report_ok},
            [f".aide/queue/{CHECK_TASK_ID}/status.yaml", ".aide/reports/trust-authorization-contract-v0-check/check-report.json"],
        ),
        assertion(
            "acceptance.boundary_exactness",
            false_boundaries_ok and projection_only_ok,
            "projection-only truthful and all live capability boundary fields false",
            {"false_boundaries_ok": false_boundaries_ok, "projection_only_truthful": projection_only_ok},
            [".aide/reports/trust-authorization-contract-v0/validation.json"],
        ),
        assertion(
            "acceptance.no_secret_like_values",
            not secret_hits,
            "no secret-like values in acceptance source reports",
            {"secret_hits": secret_hits},
            scan_paths,
        ),
    ]

    material_failures = [item for item in assertions if item["outcome"] != "PASS"]
    result = "ACCEPTED_WITH_WARNINGS" if not material_failures else "BLOCKED"
    recommended_next = NEXT_TASK if not material_failures else "AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-REPAIR-01"
    report = {
        "schema_version": "aide.trust-authorization-contract-acceptance.v0",
        "task_id": TASK_ID,
        "source_build_task_id": BUILD_TASK_ID,
        "source_check_task_id": CHECK_TASK_ID,
        "result": result,
        "accepted_capability": ACCEPTED_CAPABILITY if not material_failures else None,
        "material_finding_count": len(material_failures),
        "missing_evidence": 0,
        "recommended_next_task": recommended_next,
        "assertions": assertions,
        "accepted_meaning": "projection_only_trust_and_authorization_contract_v0",
        "warnings": [
            "Accepted capability is projection-only.",
            "Runtime enforcement and live trust infrastructure remain future work.",
        ],
    }
    (EVIDENCE_DIR / "acceptance-review.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (REPORT_DIR / "acceptance-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Trust And Authorization Contract v0 Acceptance Review",
        "",
        f"- result: {result}",
        f"- accepted_capability: {report['accepted_capability']}",
        f"- material_finding_count: {len(material_failures)}",
        "- missing_evidence: 0",
        f"- recommended_next_task: {recommended_next}",
        "",
        "## Assertions",
        "",
    ]
    lines.extend(f"- {item['id']}: {item['outcome']}" for item in assertions)
    (EVIDENCE_DIR / "acceptance-review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (REPORT_DIR / "status.md").write_text(
        "\n".join(
            [
                "# Trust And Authorization Contract v0 Acceptance",
                "",
                f"- result: {result}",
                f"- accepted_capability: {report['accepted_capability']}",
                "- accepted_meaning: projection-only trust and authorization contracts",
                f"- recommended_next_task: {recommended_next}",
                "",
                "## Non-Capabilities",
                "",
                "- no live identity",
                "- no credentials or secrets",
                "- no OIDC/IAM",
                "- no live policy engine or live grants",
                "- no runtime enforcement",
                "- no Service/runtime behavior",
                "- no provider/model/network calls",
                "- no transaction approval",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return 0 if not material_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
