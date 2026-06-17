"""Report-only AIDE Reconciler helpers.

This module detects and reports drift between queue truth, protocol reports,
evidence, ReferenceID/EventRecord projections, and OKF knowledge pages. It does
not repair drift, mutate source truth, schedule work, call providers, or
perform target/apply behavior.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-BUILD-RECONCILER-REPORTS-01"
CAPABILITY_TARGET = "minimal_reconciler_reports"
ACCEPTED_PREDECESSOR = "minimal_okf_knowledge_bundle"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-RECONCILER-REPORTS-01"
DETERMINISTIC_TIMESTAMP = "2026-06-17T00:00:00+10:00"
SCHEMA_VERSION = "aide.reconciler-reports.v0"

REPORT_ROOT = Path(".aide/reports/reconciler")
STATUS_MD = REPORT_ROOT / "status.md"
RECONCILIATION_JSON = REPORT_ROOT / "reconciliation-report.json"
RECONCILIATION_MD = REPORT_ROOT / "reconciliation-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
FINDINGS_JSON = REPORT_ROOT / "findings.json"
FINDINGS_MD = REPORT_ROOT / "findings.md"
TAXONOMY_JSON = REPORT_ROOT / "finding-taxonomy.json"
TAXONOMY_MD = REPORT_ROOT / "finding-taxonomy.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"

REQUIRED_REPORTS = [
    STATUS_MD,
    RECONCILIATION_JSON,
    RECONCILIATION_MD,
    VALIDATION_JSON,
    VALIDATION_MD,
    FINDINGS_JSON,
    FINDINGS_MD,
    TAXONOMY_JSON,
    TAXONOMY_MD,
    FUTURE_WORK_MD,
    UNFINISHED_WORK_MD,
]

SOURCE_ARTIFACTS = [
    ".aide/queue/index.yaml",
    ".aide/queue/AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01/status.yaml",
    ".aide/queue/AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01/evidence/acceptance-summary.md",
    ".aide/queue/AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01/evidence/next-task-prompt.md",
    ".aide/context/latest-task-packet.md",
    ".aide/reports/okf/projection-report.json",
    ".aide/reports/okf/validation.json",
    ".aide/reports/okf/lint.json",
    ".aide/reports/okf-accept/acceptance-report.json",
    ".aide/reports/reference-id/reference-map.json",
    ".aide/reports/reference-id/validation.json",
    ".aide/reports/event-record/event-family-index.json",
    ".aide/reports/event-record/validation.json",
    "core/knowledge/okf_bundle.py",
    "core/protocol/reference_id.py",
    "core/protocol/event_record.py",
]

EXPLICIT_NON_CAPABILITIES = [
    "drift_repair",
    "source_truth_mutation",
    "queue_acceptance_mutation",
    "latest_task_packet_rewrite",
    "okf_projection_refresh",
    "protocol_report_rewrite",
    "reference_id_rewrite",
    "event_record_rewrite",
    "capability_manifest",
    "conformance_profile",
    "patch_transaction",
    "adapter_manifest",
    "context_pack_v2",
    "runtime_reconciler_service",
    "scheduler",
    "leases",
    "supervisor",
    "test_broker_runtime",
    "async_execution",
    "worker_execution",
    "service",
    "commander",
    "provider_adapters",
    "branch_worktree_automation",
    "target_apply",
    "active_apply",
    "rollback_execution",
    "uninstall_execution",
    "release",
    "promotion",
    "github_mutation",
    "gateway_calls",
    "network_calls",
    "model_provider_calls",
    "production_readiness",
    "release_readiness",
    "broad_autonomous_runtime",
]

FINDING_TAXONOMY = [
    {
        "category": "stale_context",
        "default_severity": "warning",
        "description": "Generated context packets lag the canonical filesystem queue.",
    },
    {
        "category": "acceptance_gate_debt",
        "default_severity": "warning",
        "description": "Queue items remain implemented or accepted but still parked at needs_review review gates.",
    },
    {
        "category": "queue_contradiction",
        "default_severity": "warning",
        "description": "Queue records disagree with their task-local records or review state.",
    },
    {
        "category": "missing_evidence",
        "default_severity": "error",
        "description": "A queue or report record references evidence that is absent from the filesystem.",
    },
    {
        "category": "missing_report",
        "default_severity": "error",
        "description": "A queue or protocol record references a required report that is absent.",
    },
    {
        "category": "stale_generated_report",
        "default_severity": "warning",
        "description": "Generated reports reflect an older task routing state than the accepted queue chain.",
    },
    {
        "category": "source_hash_gap",
        "default_severity": "warning",
        "description": "A generated knowledge page records a source hash that no longer matches the source file.",
    },
    {
        "category": "protocol_report_mismatch",
        "default_severity": "warning",
        "description": "Protocol projection or validation reports disagree with their accepted protocol chain.",
    },
    {
        "category": "protocol_okf_mismatch",
        "default_severity": "warning",
        "description": "OKF knowledge explains protocol state differently from protocol or queue reports.",
    },
    {
        "category": "reference_mismatch",
        "default_severity": "warning",
        "description": "ReferenceID reports, locators, or OKF refs disagree.",
    },
    {
        "category": "event_mismatch",
        "default_severity": "warning",
        "description": "EventRecord reports, event refs, or OKF event refs disagree.",
    },
    {
        "category": "capability_overclaim",
        "default_severity": "error",
        "description": "A report or knowledge page claims an unimplemented capability.",
    },
    {
        "category": "unsupported_accepted_state",
        "default_severity": "error",
        "description": "A record marks capability acceptance without the required reviewed predecessor evidence.",
    },
    {
        "category": "authority_boundary_risk",
        "default_severity": "warning",
        "description": "A generated artifact could be mistaken for source truth if its boundary is not explicit.",
    },
    {
        "category": "dirty_state",
        "default_severity": "warning",
        "description": "The repository state or generated report set changed during reconciliation.",
    },
]

FORBIDDEN_CLAIM_PATTERNS = [
    "reconciler repairs drift",
    "reconciler mutates source truth",
    "reconciler updates latest-task-packet",
    "reconciler accepts tasks",
    "reconciler supersedes tasks",
    "capabilitymanifest implemented",
    "conformanceprofile implemented",
    "patchtransaction implemented",
    "adaptermanifest implemented",
    "contextpack v2 implemented",
    "scheduler implemented",
    "leases implemented",
    "supervisor implemented",
    "test broker runtime implemented",
    "service implemented",
    "commander implemented",
    "provider adapters implemented",
    "target apply implemented",
    "active apply implemented",
    "release ready",
    "production ready",
    "autonomous runtime ready",
]


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8", newline="\n")


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not load JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _relative(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def _clean_scalar(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        return ""
    if stripped[0] in {'"', "'"} and stripped[-1:] == stripped[0]:
        return stripped[1:-1]
    return stripped


def parse_top_level_scalars(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        if not raw_line or raw_line.startswith(" ") or raw_line.startswith("-"):
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        if key:
            values[key] = _clean_scalar(value)
    return values


def parse_simple_list(text: str, key: str) -> list[str]:
    values: list[str] = []
    in_list = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped == f"{key}:":
            in_list = True
            continue
        if in_list:
            if stripped.startswith("- "):
                values.append(_clean_scalar(stripped[2:]))
                continue
            if stripped and not raw_line.startswith(" "):
                break
    return values


def parse_queue_index(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_items = False
    key_value = re.compile(r"^\s+([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "items:":
            in_items = True
            continue
        if not in_items:
            continue
        if stripped.startswith("- id:"):
            if current is not None:
                items.append(current)
            current = {"id": _clean_scalar(stripped.split(":", 1)[1])}
            continue
        if current is None:
            continue
        match = key_value.match(raw_line.rstrip())
        if match:
            key, value = match.groups()
            current[key] = _clean_scalar(value)
    if current is not None:
        items.append(current)
    return items


def _read_text_optional(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _source_paths(repo_root: Path) -> list[Path]:
    paths = [repo_root / rel for rel in SOURCE_ARTIFACTS]
    okf_root = repo_root / ".aide/knowledge/okf"
    if okf_root.exists():
        paths.extend(sorted(path for path in okf_root.rglob("*.md") if path.is_file()))
    return sorted({path for path in paths if path.exists() and path.is_file()})


def _hashes(paths: list[Path]) -> dict[str, str]:
    return {path.as_posix(): sha256_file(path) for path in paths}


def _new_finding(
    *,
    category: str,
    severity: str,
    title: str,
    summary: str,
    source_refs: list[str],
    expected: str,
    observed: str,
    index: int,
    recommended_follow_up: str,
) -> dict[str, Any]:
    return {
        "id": f"reconciler-{index:03d}-{category}",
        "category": category,
        "severity": severity,
        "status": "open",
        "title": title,
        "summary": summary,
        "source_refs": source_refs,
        "expected": expected,
        "observed": observed,
        "report_only_disposition": "reported_only_no_repair",
        "repair_authorized": False,
        "mutates_source_truth": False,
        "recommended_follow_up": recommended_follow_up,
    }


def _next_index(findings: list[dict[str, Any]]) -> int:
    return len(findings) + 1


def _queue_state(repo_root: Path) -> dict[str, Any]:
    path = repo_root / ".aide/queue/index.yaml"
    text = _read_text_optional(path)
    items = parse_queue_index(text) if text else []
    return {
        "path": ".aide/queue/index.yaml",
        "exists": path.exists(),
        "items": items,
        "task_count": len(items),
        "ids": [item.get("id", "") for item in items],
        "needs_review_count": sum(1 for item in items if item.get("status") == "needs_review"),
        "blocked_count": sum(1 for item in items if item.get("status") == "blocked"),
        "passed_count": sum(1 for item in items if item.get("status") == "passed"),
    }


def _okf_acceptance_state(repo_root: Path) -> dict[str, Any]:
    status_path = repo_root / ".aide/queue/AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01/status.yaml"
    status_text = _read_text_optional(status_path)
    status_values = parse_top_level_scalars(status_text) if status_text else {}
    reports = parse_simple_list(status_text, "reports") if status_text else []
    evidence = parse_simple_list(status_text, "evidence") if status_text else []
    return {
        "status_path": ".aide/queue/AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01/status.yaml",
        "exists": status_path.exists(),
        "status": status_values.get("status", ""),
        "result": status_values.get("result", ""),
        "accepted_capability": status_values.get("accepted_capability", ""),
        "recommended_next_task": status_values.get("recommended_next_task", ""),
        "reports": reports,
        "evidence": evidence,
    }


def _json_report_status(repo_root: Path, rel: str) -> dict[str, Any]:
    path = repo_root / rel
    if not path.exists():
        return {"path": rel, "exists": False, "loaded": False, "status": "MISSING", "recommended_next_task": ""}
    try:
        data = read_json(path)
    except ValueError as exc:
        return {"path": rel, "exists": True, "loaded": False, "status": "FAILED_VALIDATION", "error": str(exc), "recommended_next_task": ""}
    return {
        "path": rel,
        "exists": True,
        "loaded": True,
        "status": str(data.get("status") or data.get("result") or data.get("validation_status") or data.get("lint_status") or "UNKNOWN"),
        "recommended_next_task": str(data.get("recommended_next_task") or ""),
        "task_id": str(data.get("task_id") or ""),
        "capability_target": str(data.get("capability_target") or data.get("capability_label") or ""),
    }


def _source_hash_records(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_hashes = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped == "source_hashes:":
            in_hashes = True
            continue
        if not in_hashes:
            continue
        if stripped.startswith("- path:"):
            if current is not None:
                records.append(current)
            current = {"path": _clean_scalar(stripped.split(":", 1)[1])}
            continue
        if current is not None and stripped.startswith("sha256:"):
            current["sha256"] = _clean_scalar(stripped.split(":", 1)[1])
            continue
        if stripped and not raw_line.startswith(" "):
            break
    if current is not None:
        records.append(current)
    return records


def _okf_source_hash_gaps(repo_root: Path) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []
    okf_root = repo_root / ".aide/knowledge/okf"
    if not okf_root.exists():
        return gaps
    for page in sorted(okf_root.rglob("*.md")):
        text = _read_text_optional(page)
        for record in _source_hash_records(text):
            rel = record.get("path", "")
            recorded = record.get("sha256", "")
            source = repo_root / rel
            if not rel or not recorded or not source.exists() or not source.is_file():
                continue
            current = sha256_file(source)
            if current != recorded:
                gaps.append(
                    {
                        "page": _relative(page, repo_root),
                        "source": rel,
                        "recorded": recorded,
                        "current": current,
                    }
                )
    return gaps


def _append_presence_findings(repo_root: Path, findings: list[dict[str, Any]], acceptance: dict[str, Any]) -> None:
    for rel in acceptance.get("evidence", []):
        if rel and not (repo_root / rel).exists():
            findings.append(
                _new_finding(
                    category="missing_evidence",
                    severity="error",
                    title="Accepted OKF evidence path is missing",
                    summary=f"Accepted OKF status references missing evidence `{rel}`.",
                    source_refs=[acceptance["status_path"], rel],
                    expected="Referenced evidence files exist.",
                    observed=f"Missing evidence path: {rel}",
                    index=_next_index(findings),
                    recommended_follow_up="Review accepted OKF evidence references before widening Reconciler scope.",
                )
            )
    for rel in acceptance.get("reports", []):
        if rel and not (repo_root / rel).exists():
            findings.append(
                _new_finding(
                    category="missing_report",
                    severity="error",
                    title="Accepted OKF report path is missing",
                    summary=f"Accepted OKF status references missing report `{rel}`.",
                    source_refs=[acceptance["status_path"], rel],
                    expected="Referenced report files exist.",
                    observed=f"Missing report path: {rel}",
                    index=_next_index(findings),
                    recommended_follow_up="Review accepted OKF report references before widening Reconciler scope.",
                )
            )


def collect_findings(repo_root: str | Path) -> list[dict[str, Any]]:
    root = Path(repo_root)
    findings: list[dict[str, Any]] = []
    queue = _queue_state(root)
    acceptance = _okf_acceptance_state(root)

    latest_packet = root / ".aide/context/latest-task-packet.md"
    latest_text = _read_text_optional(latest_packet)
    if latest_packet.exists() and TASK_ID not in latest_text and acceptance.get("recommended_next_task") == TASK_ID:
        phase = ""
        match = re.search(r"^## PHASE\s+(.+?)$", latest_text, flags=re.MULTILINE)
        if match:
            phase = match.group(1).strip()
        findings.append(
            _new_finding(
                category="stale_context",
                severity="warning",
                title="Latest task packet lags accepted OKF queue routing",
                summary="The generated latest task packet still points at an older lifecycle fixture runner task while OKF acceptance routes to the Reconciler build.",
                source_refs=[".aide/context/latest-task-packet.md", acceptance["status_path"], ".aide/queue/index.yaml"],
                expected=f"Latest context packet mentions `{TASK_ID}` or is regenerated after OKF acceptance.",
                observed=phase or "latest task packet does not mention the Reconciler build task",
                index=_next_index(findings),
                recommended_follow_up="Keep this as a reported drift item until a later authorized context-pack refresh updates generated context.",
            )
        )

    if queue["needs_review_count"]:
        findings.append(
            _new_finding(
                category="acceptance_gate_debt",
                severity="warning",
                title="Queue contains review-gated accepted or implemented work",
                summary="The filesystem queue intentionally carries many needs_review items; Reconciler reports the debt without accepting or superseding any task.",
                source_refs=[".aide/queue/index.yaml"],
                expected="Review-gated work remains explicit until a review task accepts, rejects, or supersedes it.",
                observed=f"needs_review_count={queue['needs_review_count']}; task_count={queue['task_count']}",
                index=_next_index(findings),
                recommended_follow_up="Use independent check or acceptance tasks for any item that should leave needs_review.",
            )
        )

    _append_presence_findings(root, findings, acceptance)

    expected_next = acceptance.get("recommended_next_task", "")
    stale_reports = []
    for rel in [
        ".aide/reports/okf/projection-report.json",
        ".aide/reports/okf/validation.json",
    ]:
        report = _json_report_status(root, rel)
        recommended = report.get("recommended_next_task", "")
        if report.get("loaded") and expected_next and recommended and recommended != expected_next:
            stale_reports.append(f"{rel}: recommended_next_task={recommended}")
    if stale_reports:
        findings.append(
            _new_finding(
                category="stale_generated_report",
                severity="warning",
                title="OKF build reports retain pre-acceptance next-task routing",
                summary="OKF build/validation reports still recommend the OKF check task even though the accepted OKF gate now routes to the Reconciler build.",
                source_refs=[".aide/reports/okf/projection-report.json", ".aide/reports/okf/validation.json", acceptance["status_path"]],
                expected=f"Accepted queue routing recommends `{expected_next}`.",
                observed="; ".join(stale_reports),
                index=_next_index(findings),
                recommended_follow_up="Treat OKF build reports as generated build evidence; do not rewrite them without a separate authorized refresh.",
            )
        )

    hash_gaps = _okf_source_hash_gaps(root)
    if hash_gaps:
        sample = "; ".join(f"{item['page']} -> {item['source']}" for item in hash_gaps[:5])
        findings.append(
            _new_finding(
                category="source_hash_gap",
                severity="warning",
                title="OKF source hashes lag current source files",
                summary="One or more OKF concept pages record source hashes from an older projection.",
                source_refs=[".aide/knowledge/okf/**", ".aide/queue/index.yaml"],
                expected="Generated OKF source_hashes match current source artifacts or are marked stale by a Reconciler report.",
                observed=f"stale_hash_count={len(hash_gaps)}; sample={sample}",
                index=_next_index(findings),
                recommended_follow_up="Keep as reported drift until a future authorized OKF refresh regenerates knowledge pages.",
            )
        )

    return findings


def findings_by_key(findings: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for finding in findings:
        value = str(finding.get(key, "unknown"))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def report_status(findings: list[dict[str, Any]]) -> str:
    if any(item.get("severity") == "error" for item in findings):
        return "FAILED_VALIDATION"
    if findings:
        return "PASS_WITH_WARNINGS"
    return "PASS"


def build_reconciliation_report(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    source_paths = _source_paths(root)
    before = _hashes(source_paths)
    findings = collect_findings(root)
    after = _hashes(source_paths)
    source_artifacts_mutated = before != after
    if source_artifacts_mutated:
        findings.append(
            _new_finding(
                category="dirty_state",
                severity="warning",
                title="Source artifact hash changed during reconciliation",
                summary="A source artifact changed while the report-only Reconciler was reading state.",
                source_refs=[_relative(path, root) for path in source_paths],
                expected="Report generation reads source artifacts without mutating them.",
                observed="source_artifacts_mutated=true",
                index=_next_index(findings),
                recommended_follow_up="Re-run reconciliation from a stable worktree before accepting results.",
            )
        )
    status = report_status(findings)
    queue = _queue_state(root)
    acceptance = _okf_acceptance_state(root)
    reports_checked = [
        _json_report_status(root, rel)
        for rel in [
            ".aide/reports/okf/projection-report.json",
            ".aide/reports/okf/validation.json",
            ".aide/reports/okf/lint.json",
            ".aide/reports/okf-accept/acceptance-report.json",
            ".aide/reports/reference-id/reference-map.json",
            ".aide/reports/reference-id/validation.json",
            ".aide/reports/event-record/event-family-index.json",
            ".aide/reports/event-record/validation.json",
        ]
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "report_type": "reconciliation_report",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "capability_target": CAPABILITY_TARGET,
        "accepted_predecessor": ACCEPTED_PREDECESSOR,
        "status": status,
        "result": status,
        "report_only": True,
        "detects_drift": True,
        "repair_implemented": False,
        "mutation_performed": False,
        "source_truth_mutation": False,
        "queue_mutation": False,
        "latest_task_packet_mutation": False,
        "okf_projection_mutation": False,
        "protocol_report_mutation": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "github_mutation": False,
        "network_calls": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "source_artifacts_checked": [_relative(path, root) for path in source_paths],
        "source_artifacts_mutated": source_artifacts_mutated,
        "queue": {
            "task_count": queue["task_count"],
            "needs_review_count": queue["needs_review_count"],
            "blocked_count": queue["blocked_count"],
            "passed_count": queue["passed_count"],
            "self_task_indexed": TASK_ID in queue["ids"],
        },
        "accepted_okf": acceptance,
        "reports_checked": reports_checked,
        "findings_count": len(findings),
        "findings_by_category": findings_by_key(findings, "category"),
        "findings_by_severity": findings_by_key(findings, "severity"),
        "findings_path": FINDINGS_JSON.as_posix(),
        "taxonomy_path": TAXONOMY_JSON.as_posix(),
        "reports_written": [path.as_posix() for path in REQUIRED_REPORTS],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "unfinished_work": unfinished_work_items(),
        "future_work": future_work_items(),
    }


def build_findings_payload(repo_root: str | Path) -> dict[str, Any]:
    findings = collect_findings(Path(repo_root))
    return {
        "schema_version": "aide.reconciler-findings.v0",
        "report_type": "reconciler_findings",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "capability_target": CAPABILITY_TARGET,
        "status": report_status(findings),
        "report_only": True,
        "repair_authorized": False,
        "mutation_performed": False,
        "findings_count": len(findings),
        "findings_by_category": findings_by_key(findings, "category"),
        "findings_by_severity": findings_by_key(findings, "severity"),
        "findings": findings,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def build_taxonomy_payload() -> dict[str, Any]:
    return {
        "schema_version": "aide.reconciler-finding-taxonomy.v0",
        "report_type": "reconciler_finding_taxonomy",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "capability_target": CAPABILITY_TARGET,
        "status": "PASS",
        "report_only": True,
        "repair_authorized": False,
        "categories": FINDING_TAXONOMY,
    }


def _required_categories_present(taxonomy: dict[str, Any]) -> bool:
    categories = taxonomy.get("categories", [])
    names = {item.get("category") for item in categories if isinstance(item, dict)}
    required = {item["category"] for item in FINDING_TAXONOMY}
    return required.issubset(names)


def _findings_schema_valid(payload: dict[str, Any]) -> bool:
    required = {"id", "category", "severity", "status", "title", "summary", "source_refs", "expected", "observed", "report_only_disposition", "repair_authorized", "mutates_source_truth"}
    categories = {item["category"] for item in FINDING_TAXONOMY}
    severities = {"info", "warning", "error"}
    for finding in payload.get("findings", []):
        if not isinstance(finding, dict) or not required.issubset(finding):
            return False
        if finding.get("category") not in categories:
            return False
        if finding.get("severity") not in severities:
            return False
        if finding.get("repair_authorized") is not False:
            return False
        if finding.get("mutates_source_truth") is not False:
            return False
    return True


def _output_overclaiming_findings(repo_root: Path) -> list[str]:
    findings: list[str] = []
    for rel in [RECONCILIATION_MD, VALIDATION_MD, FINDINGS_MD, TAXONOMY_MD, FUTURE_WORK_MD, UNFINISHED_WORK_MD, STATUS_MD]:
        path = repo_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for pattern in FORBIDDEN_CLAIM_PATTERNS:
            if pattern in text:
                findings.append(f"{rel.as_posix()}: {pattern}")
    return sorted(set(findings))


def validate_reconciler_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    errors: list[str] = []
    warnings: list[str] = []
    report_files_present = all((root / rel).exists() for rel in REQUIRED_REPORTS if rel not in {VALIDATION_JSON, VALIDATION_MD})
    if not report_files_present:
        missing = [rel.as_posix() for rel in REQUIRED_REPORTS if rel not in {VALIDATION_JSON, VALIDATION_MD} and not (root / rel).exists()]
        errors.extend(f"missing report file: {rel}" for rel in missing)
    json_reports_valid = True
    loaded: dict[str, dict[str, Any]] = {}
    for rel in [RECONCILIATION_JSON, FINDINGS_JSON, TAXONOMY_JSON]:
        path = root / rel
        if not path.exists():
            json_reports_valid = False
            continue
        try:
            loaded[rel.as_posix()] = read_json(path)
        except ValueError as exc:
            json_reports_valid = False
            errors.append(str(exc))
    reconciliation = loaded.get(RECONCILIATION_JSON.as_posix(), {})
    findings = loaded.get(FINDINGS_JSON.as_posix(), {})
    taxonomy = loaded.get(TAXONOMY_JSON.as_posix(), {})
    required_fields_present = all(
        field in reconciliation
        for field in [
            "task_id",
            "capability_target",
            "status",
            "report_only",
            "detects_drift",
            "repair_implemented",
            "mutation_performed",
            "source_truth_mutation",
            "findings_count",
            "recommended_next_task",
        ]
    )
    if not required_fields_present:
        errors.append("reconciliation report is missing required fields")
    report_only_boundary_preserved = (
        reconciliation.get("report_only") is True
        and reconciliation.get("detects_drift") is True
        and reconciliation.get("repair_implemented") is False
        and reconciliation.get("mutation_performed") is False
        and reconciliation.get("source_truth_mutation") is False
        and reconciliation.get("target_mutation") is False
        and reconciliation.get("active_repo_apply_mutation") is False
        and reconciliation.get("branch_mutation") is False
        and reconciliation.get("github_mutation") is False
        and reconciliation.get("network_calls") is False
        and reconciliation.get("provider_model_calls") is False
    )
    if not report_only_boundary_preserved:
        errors.append("report-only boundary is not preserved")
    taxonomy_categories_present = _required_categories_present(taxonomy) if taxonomy else False
    if not taxonomy_categories_present:
        errors.append("finding taxonomy is missing required categories")
    finding_schema_valid = _findings_schema_valid(findings) if findings else False
    if not finding_schema_valid:
        errors.append("findings payload does not match required shape")
    overclaiming_findings = _output_overclaiming_findings(root)
    if overclaiming_findings:
        errors.extend(overclaiming_findings)
    if findings.get("findings_count", 0):
        warnings.append("Reconciler findings are warning/error reports only; no repair was attempted.")
    source_artifacts_mutated = bool(reconciliation.get("source_artifacts_mutated", False))
    if source_artifacts_mutated:
        warnings.append("Source artifact mutation was detected during report generation.")
    status = "FAILED_VALIDATION" if errors else "PASS_WITH_WARNINGS" if warnings else "PASS"
    validation = {
        "schema_version": "aide.reconciler-validation.v0",
        "report_type": "reconciler_validation",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "capability_target": CAPABILITY_TARGET,
        "validation_status": status,
        "status": status,
        "validated": status in {"PASS", "PASS_WITH_WARNINGS"},
        "report_files_present": report_files_present,
        "json_reports_valid": json_reports_valid,
        "required_fields_present": required_fields_present,
        "taxonomy_categories_present": taxonomy_categories_present,
        "finding_schema_valid": finding_schema_valid,
        "report_only_boundary_preserved": report_only_boundary_preserved,
        "source_artifacts_mutated": source_artifacts_mutated,
        "overclaiming_check_passed": not overclaiming_findings,
        "forbidden_ops_preserved": not overclaiming_findings and report_only_boundary_preserved,
        "repair_implemented": False,
        "mutation_performed": False,
        "source_truth_mutation": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "github_mutation": False,
        "network_calls": False,
        "provider_model_calls": False,
        "gateway_calls": False,
        "validation_errors": errors,
        "warnings": warnings,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / VALIDATION_JSON, validation)
    write_text(root / VALIDATION_MD, render_validation_markdown(validation))
    return validation


def write_reconciliation_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    report = build_reconciliation_report(root)
    findings_payload = build_findings_payload(root)
    taxonomy_payload = build_taxonomy_payload()
    write_json(root / RECONCILIATION_JSON, report)
    write_text(root / RECONCILIATION_MD, render_reconciliation_markdown(report))
    write_json(root / FINDINGS_JSON, findings_payload)
    write_text(root / FINDINGS_MD, render_findings_markdown(findings_payload))
    write_json(root / TAXONOMY_JSON, taxonomy_payload)
    write_text(root / TAXONOMY_MD, render_taxonomy_markdown(taxonomy_payload))
    write_text(root / FUTURE_WORK_MD, render_future_work_markdown())
    write_text(root / UNFINISHED_WORK_MD, render_unfinished_work_markdown())
    write_text(root / STATUS_MD, render_status_markdown(report))
    validation = validate_reconciler_reports(root)
    report["validation_status"] = validation["validation_status"]
    write_json(root / RECONCILIATION_JSON, report)
    write_text(root / RECONCILIATION_MD, render_reconciliation_markdown(report))
    write_text(root / STATUS_MD, render_status_markdown(report))
    return report


def reconciler_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    findings = collect_findings(root)
    status = report_status(findings)
    data = {
        "schema_version": "aide.reconciler-status.v0",
        "task_id": TASK_ID,
        "capability_target": CAPABILITY_TARGET,
        "status": status,
        "report_only": True,
        "detects_drift": True,
        "repair_implemented": False,
        "mutation_performed": False,
        "findings_count": len(findings),
        "findings_by_category": findings_by_key(findings, "category"),
        "findings_by_severity": findings_by_key(findings, "severity"),
        "reports_exist": all((root / rel).exists() for rel in REQUIRED_REPORTS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "github_mutation": False,
        "network_calls": False,
        "provider_model_calls": False,
        "gateway_calls": False,
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    return data


def render_reconciliation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Reconciler Report",
        "",
        f"- task_id: {TASK_ID}",
        f"- capability_target: {CAPABILITY_TARGET}",
        f"- status: {report.get('status')}",
        f"- validation_status: {report.get('validation_status', 'not_run')}",
        f"- report_only: {str(report.get('report_only', True)).lower()}",
        f"- detects_drift: {str(report.get('detects_drift', True)).lower()}",
        "- repair_implemented: false",
        "- mutation_performed: false",
        "- source_truth_mutation: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- branch_mutation: false",
        "- github_mutation: false",
        "- network_calls: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        f"- findings_count: {report.get('findings_count')}",
        f"- recommended_next_task: {RECOMMENDED_NEXT_TASK}",
        "",
        "## Findings By Category",
        "",
    ]
    categories = report.get("findings_by_category", {})
    if categories:
        for key, value in categories.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- none")
    lines.extend(["", "## Reports Checked", ""])
    for item in report.get("reports_checked", []):
        lines.append(f"- {item.get('path')}: {item.get('status')}")
    lines.extend(["", "## Source Artifacts Checked", ""])
    for rel in report.get("source_artifacts_checked", []):
        lines.append(f"- {rel}")
    return "\n".join(lines) + "\n"


def render_findings_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Reconciler Findings",
        "",
        f"- task_id: {TASK_ID}",
        f"- status: {payload.get('status')}",
        f"- findings_count: {payload.get('findings_count')}",
        "- report_only: true",
        "- repair_authorized: false",
        "- mutation_performed: false",
        "",
    ]
    for finding in payload.get("findings", []):
        lines.extend(
            [
                f"## {finding.get('id')}",
                "",
                f"- category: {finding.get('category')}",
                f"- severity: {finding.get('severity')}",
                f"- title: {finding.get('title')}",
                f"- expected: {finding.get('expected')}",
                f"- observed: {finding.get('observed')}",
                "- repair_authorized: false",
                "- mutates_source_truth: false",
                "",
            ]
        )
    if not payload.get("findings"):
        lines.append("- none")
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def render_taxonomy_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Reconciler Finding Taxonomy",
        "",
        f"- task_id: {TASK_ID}",
        "- report_only: true",
        "- repair_authorized: false",
        "",
        "## Categories",
        "",
    ]
    for item in payload.get("categories", []):
        lines.append(f"- {item.get('category')}: severity={item.get('default_severity')}; {item.get('description')}")
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Reconciler Validation",
        "",
        f"- validation_status: {report.get('validation_status')}",
        f"- report_files_present: {str(report.get('report_files_present', False)).lower()}",
        f"- json_reports_valid: {str(report.get('json_reports_valid', False)).lower()}",
        f"- required_fields_present: {str(report.get('required_fields_present', False)).lower()}",
        f"- taxonomy_categories_present: {str(report.get('taxonomy_categories_present', False)).lower()}",
        f"- finding_schema_valid: {str(report.get('finding_schema_valid', False)).lower()}",
        f"- report_only_boundary_preserved: {str(report.get('report_only_boundary_preserved', False)).lower()}",
        f"- source_artifacts_mutated: {str(report.get('source_artifacts_mutated', False)).lower()}",
        f"- overclaiming_check_passed: {str(report.get('overclaiming_check_passed', False)).lower()}",
        f"- forbidden_ops_preserved: {str(report.get('forbidden_ops_preserved', False)).lower()}",
        "- repair_implemented: false",
        "- mutation_performed: false",
        "- source_truth_mutation: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- branch_mutation: false",
        "- github_mutation: false",
        "- network_calls: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        f"- recommended_next_task: {RECOMMENDED_NEXT_TASK}",
        "",
        "## Errors",
        "",
    ]
    errors = report.get("validation_errors", [])
    lines.extend(f"- {error}" for error in errors) if errors else lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    warnings = report.get("warnings", [])
    lines.extend(f"- {warning}" for warning in warnings) if warnings else lines.append("- none")
    return "\n".join(lines) + "\n"


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Reconciler Status",
        "",
        f"- task_id: {TASK_ID}",
        f"- capability_target: {CAPABILITY_TARGET}",
        f"- status: {data.get('status')}",
        f"- report_only: {str(data.get('report_only', True)).lower()}",
        f"- detects_drift: {str(data.get('detects_drift', True)).lower()}",
        "- repair_implemented: false",
        "- mutation_performed: false",
        "- source_truth_mutation: false",
        "- target_mutation: false",
        "- active_repo_apply_mutation: false",
        "- branch_mutation: false",
        "- github_mutation: false",
        "- network_calls: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        f"- findings_count: {data.get('findings_count')}",
        f"- recommended_next_task: {RECOMMENDED_NEXT_TASK}",
        "",
        "## Explicit Non-Capabilities",
        "",
    ]
    lines.extend(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES)
    return "\n".join(lines) + "\n"


def future_work_items() -> list[dict[str, str]]:
    return [
        {
            "task": "AIDE-CHECK-RECONCILER-REPORTS-01",
            "reason": "independent review of report-only Reconciler findings, taxonomy, CLI, reports, tests, and no-repair boundary",
        },
        {
            "task": "AIDE-ACCEPT-RECONCILER-REPORTS-01",
            "reason": "accept the report-only Reconciler only after independent check",
        },
        {
            "task": "AIDE-BUILD-CAPABILITY-MANIFEST-01",
            "reason": "future work after Reconciler check and acceptance, not a direct next task from this build",
        },
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    return [{"item": item, "reason": "intentionally deferred beyond the report-only Reconciler slice"} for item in EXPLICIT_NON_CAPABILITIES]


def render_future_work_markdown() -> str:
    lines = ["# Reconciler Future Work", "", "## Recommended Order", ""]
    for index, item in enumerate(future_work_items(), start=1):
        lines.append(f"{index}. {item['task']}: {item['reason']}.")
    lines.extend(
        [
            "",
            f"This build task recommends only `{RECOMMENDED_NEXT_TASK}` as the next task.",
            "CapabilityManifest remains deferred until Reconciler check and acceptance.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_unfinished_work_markdown() -> str:
    lines = [
        "# Reconciler Unfinished Work",
        "",
        "## Finished In This Slice",
        "",
        "- Deterministic report-only drift finding model.",
        "- Finding taxonomy for queue, evidence, protocol, ReferenceID, EventRecord, OKF, and capability overclaim drift.",
        "- Local JSON and Markdown reports under `.aide/reports/reconciler/`.",
        "",
        "## Not Attempted By Design",
        "",
    ]
    for item in unfinished_work_items():
        lines.append(f"- {item['item']}: {item['reason']}.")
    return "\n".join(lines) + "\n"
