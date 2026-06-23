from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


TASK_ID = "AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01"
SOURCE_TASK = "AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01"
EXPECTED_LABEL = "dominium_registered_validation_command_boundary_invocation_v0"
OLD_LABEL = "live_dominium_validation_command_readonly_v0"
REPORT_ROOT = Path(".aide/reports/dominium-registered-validation-backend")
CHECK_REPORT_ROOT = Path(".aide/reports/dominium-registered-validation-backend-relabel-check")
CHECK_REPORT = CHECK_REPORT_ROOT / "check-report.json"
HISTORICAL_DIRS = [
    Path(".aide/queue/AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01"),
    Path(".aide/queue/AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01"),
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], check=False, capture_output=True, text=True)


def add_assertion(assertions: list[dict], *, item: str, ok: bool, observed: object, expected: object, severity: str = "material") -> None:
    assertions.append(
        {
            "item": item,
            "outcome": "PASS" if ok else "FAIL",
            "severity": severity,
            "observed": observed,
            "expected": expected,
        }
    )


def active_old_label_violations() -> list[str]:
    violations: list[str] = []
    for path in sorted(REPORT_ROOT.rglob("*")):
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if OLD_LABEL in line and "supersed" not in line.lower() and "prior label" not in line.lower():
                violations.append(f"{path.as_posix()}:{number}:{line.strip()}")
    return violations


def historical_dirs_changed() -> list[str]:
    changed: list[str] = []
    for path in HISTORICAL_DIRS:
        result = run_git(["diff", "--name-only", "HEAD~1", "--", path.as_posix()])
        if result.returncode != 0:
            changed.append(f"{path.as_posix()}: git diff failed: {result.stderr.strip()}")
        elif result.stdout.strip():
            changed.extend(result.stdout.strip().splitlines())
    return changed


def leakage_findings(paths: list[Path]) -> list[str]:
    drive_path = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")
    secret = re.compile(r"(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}")
    findings: list[str] = []
    for root in paths:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if drive_path.search(text):
                findings.append(f"{path.as_posix()}: local_absolute_path")
            if secret.search(text):
                findings.append(f"{path.as_posix()}: secret_like")
    return findings


def main() -> int:
    CHECK_REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    invocation = read_json(REPORT_ROOT / "invocation-result.json")
    validation = read_json(REPORT_ROOT / "validation.json")
    descriptor = read_json(REPORT_ROOT / "capability-descriptor.json")
    projection = read_json(REPORT_ROOT / "projection.json")
    assertions: list[dict] = []

    for name, data in {
        "invocation-result": invocation,
        "validation": validation,
        "capability-descriptor": descriptor,
        "projection": projection,
    }.items():
        add_assertion(
            assertions,
            item=f"{name}.active_label",
            ok=data.get("proposed_capability_label") == EXPECTED_LABEL,
            observed=data.get("proposed_capability_label"),
            expected=EXPECTED_LABEL,
        )

    violations = active_old_label_violations()
    add_assertion(
        assertions,
        item="active.old_label_not_misused",
        ok=not violations,
        observed=violations,
        expected=[],
    )

    historical_changed = historical_dirs_changed()
    add_assertion(
        assertions,
        item="historical.predecessor_evidence_unchanged",
        ok=not historical_changed,
        observed=historical_changed,
        expected=[],
    )

    boundary_expectations = {
        "process_started": True,
        "launcher_call_count": 1,
        "structured_output_parsed": True,
        "registered_command_boundary_reached": "proven",
        "service_adapter_boundary_reached": "unproven",
        "domain_outcome": "typed_refusal",
        "aggregate_validation_executed": False,
        "aggregate_validation_succeeded": False,
        "mutation_observation": "none_detected_within_probe_coverage",
    }
    for key, expected in boundary_expectations.items():
        add_assertion(
            assertions,
            item=f"boundary.{key}",
            ok=invocation.get(key) == expected and validation.get(key) == expected,
            observed={"invocation": invocation.get(key), "validation": validation.get(key)},
            expected=expected,
        )

    command_result = invocation.get("dominium_command_result", {})
    refusal = command_result.get("payload", {}).get("refusal", {}) if isinstance(command_result, dict) else {}
    add_assertion(
        assertions,
        item="domain.typed_refusal_preserved",
        ok=command_result.get("status") == "refused" and refusal.get("code") == "dominium.refusal.validation.tool_unavailable",
        observed={"status": command_result.get("status"), "refusal_code": refusal.get("code")},
        expected={"status": "refused", "refusal_code": "dominium.refusal.validation.tool_unavailable"},
    )

    leak_findings = leakage_findings(
        [
            REPORT_ROOT,
            CHECK_REPORT_ROOT,
            Path(".aide/queue/AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01"),
        ]
    )
    add_assertion(
        assertions,
        item="scrub.no_local_paths_or_secret_like_tokens",
        ok=not leak_findings,
        observed=leak_findings,
        expected=[],
    )

    material_failures = [item for item in assertions if item["outcome"] != "PASS" and item["severity"] == "material"]
    report = {
        "schema_version": "aide.dominium-registered-validation-relabel-check.v1",
        "task_id": TASK_ID,
        "source_task": SOURCE_TASK,
        "result": "PASS_WITH_WARNINGS" if not material_failures else "REQUEST_CHANGES",
        "material_finding_count": len(material_failures),
        "missing_evidence": 0,
        "checked_capability_label": EXPECTED_LABEL,
        "recommended_next_task": "AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01"
        if not material_failures
        else "AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-02",
        "assertions": assertions,
        "warnings": [
            "Historical predecessor evidence intentionally retains the old label.",
            "This check does not accept the capability.",
        ],
    }
    CHECK_REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if not material_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
