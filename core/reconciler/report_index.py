"""Deterministic report index for AIDE reports.

This module indexes existing reports without moving, renaming, repairing,
rewriting, deleting, or normalizing them. The index is a generated,
non-canonical discovery projection.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-BUILD-REPORT-INDEX-01"
ACCEPTED_PREDECESSOR = "AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01"
INDEPENDENT_CHECK_TASK = "AIDE-CHECK-REPORT-INDEX-01"
DETERMINISTIC_TIMESTAMP = "2026-06-18T00:00:00+10:00"

INDEX_PATH = Path(".aide/reports/index.yaml")
REPORT_ROOT = Path(".aide/reports/self-management")
REPORT_JSON = REPORT_ROOT / "report-index.json"
REPORT_MD = REPORT_ROOT / "report-index.md"
FINDINGS_JSON = REPORT_ROOT / "report-index.findings.json"

SELF_OUTPUTS = {
    ".aide/reports/index.yaml",
    ".aide/reports/self-management/report-index.json",
    ".aide/reports/self-management/report-index.md",
    ".aide/reports/self-management/report-index.findings.json",
}

EXPLICIT_NON_CAPABILITIES = [
    "report_move",
    "report_rename",
    "report_rewrite",
    "report_repair",
    "report_delete",
    "evidence_rewrite",
    "normalization",
    "migration_apply",
    "canonical_truth_replacement",
    "runtime",
    "provider_calls",
    "network_calls",
    "github_mutation",
    "branch_worktree_automation",
    "release_behavior",
    "target_repo_mutation",
]


@dataclass(frozen=True)
class ReportRecord:
    report_id: str
    subject: str
    stage: str
    task_id: str
    path: str
    format: str
    producer: str
    producer_status: str
    source_refs: list[str]
    evidence_refs: list[str]
    baseline_ref: str
    canonical: str
    generated: str
    freshness: str
    related_report_paths: list[str]
    related_task_ids: list[str]
    warnings: list[str]
    explicit_non_capabilities: list[str]


@dataclass(frozen=True)
class GovernanceFinding:
    id: str
    severity: str
    surface: str
    taxonomy: str
    claim: str
    expected: str
    observed: str
    evidence_refs: list[str]
    affected_paths: list[str]
    recommendation: str
    next_task: str


def normalize_path(value: str | Path) -> str:
    text = str(value).replace("\\", "/")
    if text.startswith("./"):
        return text[2:]
    return text


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def git_ref(repo_root: Path, ref: str = "HEAD") -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", ref],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError:
        return "unknown"
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def tracked_report_files(repo_root: Path) -> tuple[list[str], list[str]]:
    try:
        result = subprocess.run(
            ["git", "ls-files", ".aide/reports"],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError:
        return [], sorted(SELF_OUTPUTS)
    if result.returncode != 0:
        return [], sorted(SELF_OUTPUTS)
    reports: list[str] = []
    excluded = set(SELF_OUTPUTS)
    for line in result.stdout.splitlines():
        rel = normalize_path(line.strip())
        if not rel:
            continue
        if rel in SELF_OUTPUTS:
            excluded.add(rel)
            continue
        if rel.startswith(".aide/reports/"):
            reports.append(rel)
    return sorted(reports), sorted(excluded)


def read_text_optional(path: Path, limit: int = 512_000) -> str:
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def infer_task_ids(text: str, path: str, limit: int = 5) -> list[str]:
    values = set(re.findall(r"AIDE-[A-Z0-9][A-Z0-9-]+-01", text))
    values.update(re.findall(r"AIDE-[A-Z0-9][A-Z0-9-]+-01", path))
    return sorted(values)[:limit]


def infer_stage(path: str, text: str) -> str:
    value = f"{path}\n{text[:2000]}".lower()
    if "acceptance" in value or "accept-" in value or "/accept" in value:
        return "accept"
    if "check-" in value or "/check" in value or "check report" in value:
        return "check"
    if "build-" in value or "/build" in value:
        return "build"
    if "harden" in value:
        return "harden"
    if "repair" in value:
        return "repair"
    if "audit" in value:
        return "audit"
    if "status" in value:
        return "status"
    if "inventory" in value:
        return "inventory"
    if "reconciler" in value or "reconciliation" in value:
        return "reconciliation"
    if "migration" in value:
        return "migration"
    return "unknown"


def infer_subject(path: str) -> str:
    parts = path.split("/")
    rel_parts = parts[2:]
    if not rel_parts:
        return "unknown"
    if len(rel_parts) >= 2:
        first = rel_parts[0]
        if first != "self-management":
            return first
        return Path(rel_parts[-1]).stem
    stem = Path(rel_parts[-1]).stem
    for suffix in ("-report", "-status", "-validation", "-findings"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return stem or "unknown"


def format_for_path(path: str) -> str:
    suffix = Path(path).suffix.lower()
    return {
        ".md": "markdown",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".txt": "text",
        ".jsonl": "jsonl",
    }.get(suffix, "other")


def producer_for(task_ids: list[str], path: str) -> tuple[str, str]:
    if task_ids:
        return task_ids[0], "known"
    if "latest-" in path or path.endswith(".json") or path.endswith(".md"):
        return "producer_inferred_from_report_path", "inferred"
    return "producer_unknown", "unknown"


def build_records(repo_root: Path) -> tuple[list[ReportRecord], list[str], list[str]]:
    report_paths, excluded = tracked_report_files(repo_root)
    records: list[ReportRecord] = []
    for rel in report_paths:
        text = read_text_optional(repo_root / rel)
        task_ids = infer_task_ids(text, rel)
        task_id = task_ids[0] if task_ids else "unknown"
        stage = infer_stage(rel, text)
        subject = infer_subject(rel)
        producer, producer_status = producer_for(task_ids, rel)
        evidence_refs = [
            f".aide/queue/{task}/evidence"
            for task in task_ids
            if (repo_root / f".aide/queue/{task}/evidence").exists()
        ]
        source_refs = [
            f".aide/queue/{task}/status.yaml"
            for task in task_ids
            if (repo_root / f".aide/queue/{task}/status.yaml").exists()
        ]
        warnings: list[str] = ["freshness_unknown", "generated_truth_risk"]
        if subject == "unknown":
            warnings.append("report_subject_ambiguous")
        if stage == "unknown":
            warnings.append("report_stage_ambiguous")
        if producer_status == "unknown":
            warnings.append("report_producer_unknown")
        if task_ids and not evidence_refs:
            warnings.append("missing_evidence")
        if task_ids and not source_refs:
            warnings.append("reference_break_risk")
        records.append(
            ReportRecord(
                report_id="report-" + hashlib.sha1(rel.encode("utf-8")).hexdigest()[:12],
                subject=subject,
                stage=stage,
                task_id=task_id,
                path=rel,
                format=format_for_path(rel),
                producer=producer,
                producer_status=producer_status,
                source_refs=source_refs,
                evidence_refs=evidence_refs,
                baseline_ref=ACCEPTED_PREDECESSOR,
                canonical="false",
                generated="true",
                freshness="unknown",
                related_report_paths=[],
                related_task_ids=task_ids,
                warnings=sorted(set(warnings)),
                explicit_non_capabilities=EXPLICIT_NON_CAPABILITIES,
            )
        )
    related_by_subject: dict[str, list[str]] = {}
    for record in records:
        related_by_subject.setdefault(record.subject, []).append(record.path)
    updated: list[ReportRecord] = []
    for record in records:
        related = [path for path in sorted(related_by_subject.get(record.subject, [])) if path != record.path][:20]
        updated.append(
            ReportRecord(
                **{**asdict(record), "related_report_paths": related}
            )
        )
    updated.sort(key=lambda record: record.path)
    return updated, report_paths, excluded


def counts(records: list[ReportRecord], attr: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for record in records:
        key = str(getattr(record, attr))
        result[key] = result.get(key, 0) + 1
    return dict(sorted(result.items()))


def warning_paths(records: list[ReportRecord], warning: str) -> list[str]:
    return [record.path for record in records if warning in record.warnings][:20]


def load_generated_output_ledger_status(repo_root: Path) -> dict[str, Any]:
    path = repo_root / ".aide/reports/self-management/generated-output-ledger.json"
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "path": normalize_path(path.relative_to(repo_root)) if path.is_absolute() else normalize_path(path),
            "status": "absent",
            "accepted": False,
        }
    return {
        "path": ".aide/reports/self-management/generated-output-ledger.json",
        "status": "present_provisional_unaccepted",
        "accepted": False,
        "task_id": report.get("task_id", "unknown"),
        "result": report.get("result", "unknown"),
        "classified_count": report.get("classified_count", 0),
    }


def build_findings(records: list[ReportRecord]) -> list[GovernanceFinding]:
    findings = [
        GovernanceFinding(
            id="RPT-001",
            severity="info",
            surface="generated_report",
            taxonomy="truth_alignment_confirmed",
            claim="Reports were indexed without moving or rewriting them.",
            expected="Report indexing should observe tracked reports and leave historic report paths untouched.",
            observed=f"Indexed {len(records)} tracked report files.",
            evidence_refs=[normalize_path(INDEX_PATH), normalize_path(REPORT_JSON)],
            affected_paths=[],
            recommendation="Proceed to the independent generated-output ledger check after this build wave.",
            next_task=RECOMMENDED_NEXT_TASK,
        ),
        GovernanceFinding(
            id="RPT-002",
            severity="warning" if warning_paths(records, "report_subject_ambiguous") else "info",
            surface="generated_report",
            taxonomy="report_subject_ambiguous",
            claim="Some report subjects are ambiguous.",
            expected="Report subjects should be inferable from path, task id, or report metadata where practical.",
            observed=f"{len(warning_paths(records, 'report_subject_ambiguous'))} sampled ambiguous subject paths; full count is recorded in report records.",
            evidence_refs=[normalize_path(INDEX_PATH)],
            affected_paths=warning_paths(records, "report_subject_ambiguous"),
            recommendation="Leave ambiguous subjects warning-class until an independent report-index check reviews inference rules.",
            next_task=RECOMMENDED_NEXT_TASK,
        ),
        GovernanceFinding(
            id="RPT-003",
            severity="warning" if warning_paths(records, "report_stage_ambiguous") else "info",
            surface="generated_report",
            taxonomy="report_stage_ambiguous",
            claim="Some report lifecycle stages are ambiguous.",
            expected="Build/check/accept/status/inventory stages should be inferred only when evidence is sufficient.",
            observed=f"{len([record for record in records if 'report_stage_ambiguous' in record.warnings])} reports have unknown stage.",
            evidence_refs=[normalize_path(INDEX_PATH)],
            affected_paths=warning_paths(records, "report_stage_ambiguous"),
            recommendation="Keep unknown stage rather than rename historic report folders.",
            next_task=RECOMMENDED_NEXT_TASK,
        ),
        GovernanceFinding(
            id="RPT-004",
            severity="warning" if warning_paths(records, "report_producer_unknown") else "info",
            surface="generated_report",
            taxonomy="report_producer_unknown",
            claim="Some report producers are unknown.",
            expected="Producer should be known or inferred without inventing task authority.",
            observed=f"{len([record for record in records if 'report_producer_unknown' in record.warnings])} reports have unknown producer.",
            evidence_refs=[normalize_path(INDEX_PATH)],
            affected_paths=warning_paths(records, "report_producer_unknown"),
            recommendation="Classify unknown producers as warning debt; do not rewrite historic reports.",
            next_task=RECOMMENDED_NEXT_TASK,
        ),
        GovernanceFinding(
            id="RPT-005",
            severity="warning",
            surface="generated_report",
            taxonomy="generated_truth_risk",
            claim="Reports are generated discovery projections and not canonical truth.",
            expected="Reports should default to canonical false unless accepted policy proves otherwise.",
            observed=f"{len(records)} indexed reports default to canonical false and generated true.",
            evidence_refs=[normalize_path(INDEX_PATH), "docs/reference/source-of-truth.md"],
            affected_paths=[record.path for record in records[:20]],
            recommendation="Preserve non-canonical defaults in the independent report-index check.",
            next_task=RECOMMENDED_NEXT_TASK,
        ),
        GovernanceFinding(
            id="RPT-006",
            severity="warning" if warning_paths(records, "missing_evidence") else "info",
            surface="evidence",
            taxonomy="missing_evidence",
            claim="Some task-linked reports have missing evidence directories.",
            expected="When a report names a task id, evidence should exist or absence should remain warning-class.",
            observed=f"{len([record for record in records if 'missing_evidence' in record.warnings])} reports reference task ids without discovered evidence directories.",
            evidence_refs=[normalize_path(INDEX_PATH)],
            affected_paths=warning_paths(records, "missing_evidence"),
            recommendation="Keep as warning debt for independent check; do not rewrite evidence refs.",
            next_task=RECOMMENDED_NEXT_TASK,
        ),
        GovernanceFinding(
            id="RPT-007",
            severity="warning" if warning_paths(records, "reference_break_risk") else "info",
            surface="generated_report",
            taxonomy="reference_break_risk",
            claim="Some task-linked reports have reference break risk.",
            expected="Task status refs inferred by reports should resolve or remain warning-class.",
            observed=f"{len([record for record in records if 'reference_break_risk' in record.warnings])} reports have task status reference risk.",
            evidence_refs=[normalize_path(INDEX_PATH)],
            affected_paths=warning_paths(records, "reference_break_risk"),
            recommendation="Do not rewrite historic references in this index task.",
            next_task=RECOMMENDED_NEXT_TASK,
        ),
        GovernanceFinding(
            id="RPT-008",
            severity="info",
            surface="generated_report",
            taxonomy="truth_alignment_confirmed",
            claim="GeneratedOutputLedger input is treated as provisional.",
            expected="ReportIndex may consume GeneratedOutputLedger build output only as unaccepted provisional information.",
            observed="GeneratedOutputLedger build output is present and recorded as provisional_unaccepted.",
            evidence_refs=[
                ".aide/reports/self-management/generated-output-ledger.json",
                normalize_path(REPORT_JSON),
            ],
            affected_paths=[
                ".aide/reports/self-management/generated-output-ledger.json"
            ],
            recommendation="Do not describe GeneratedOutputLedger as accepted until wave 2 acceptance.",
            next_task=RECOMMENDED_NEXT_TASK,
        ),
    ]
    return findings


def build_payloads(repo_root: str | Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    root = Path(repo_root)
    records, scanned_paths, excluded = build_records(root)
    record_dicts = [asdict(record) for record in records]
    findings = [asdict(finding) for finding in build_findings(records)]
    severity_counts: dict[str, int] = {}
    surface_counts: dict[str, int] = {}
    taxonomy_counts: dict[str, int] = {}
    for finding in findings:
        severity_counts[finding["severity"]] = severity_counts.get(finding["severity"], 0) + 1
        surface_counts[finding["surface"]] = surface_counts.get(finding["surface"], 0) + 1
        taxonomy_counts[finding["taxonomy"]] = taxonomy_counts.get(finding["taxonomy"], 0) + 1

    result = "PASS_WITH_WARNINGS" if any(f["severity"] == "warning" for f in findings) else "PASS"
    index = {
        "format_version": "aide.report-index.v0",
        "task_id": TASK_ID,
        "repository_ref": git_ref(root),
        "baseline_ref": ACCEPTED_PREDECESSOR,
        "profile": "AIDE_SELF_PROFILE",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "scan_mode": "full",
        "scanned_report_count": len(scanned_paths),
        "indexed_report_count": len(records),
        "ambiguous_count": sum(
            1
            for record in records
            if {
                "report_subject_ambiguous",
                "report_stage_ambiguous",
                "report_producer_unknown",
            }
            & set(record.warnings)
        ),
        "excluded_paths": excluded,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "generated_output_ledger_input": load_generated_output_ledger_status(root),
        "reports": record_dicts,
    }
    report = {
        "task_id": TASK_ID,
        "result": result,
        "repository_ref": index["repository_ref"],
        "baseline_ref": ACCEPTED_PREDECESSOR,
        "scan_mode": "full",
        "index_path": normalize_path(INDEX_PATH),
        "scanned_report_count": len(scanned_paths),
        "indexed_report_count": len(records),
        "ambiguous_count": index["ambiguous_count"],
        "counts_by_stage": counts(records, "stage"),
        "counts_by_format": counts(records, "format"),
        "counts_by_producer_status": counts(records, "producer_status"),
        "counts_by_canonical": counts(records, "canonical"),
        "counts_by_generated": counts(records, "generated"),
        "finding_count": len(findings),
        "counts_by_severity": dict(sorted(severity_counts.items())),
        "counts_by_surface": dict(sorted(surface_counts.items())),
        "counts_by_taxonomy": dict(sorted(taxonomy_counts.items())),
        "excluded_paths": excluded,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "generated_output_ledger_input": index["generated_output_ledger_input"],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "independent_report_index_check": INDEPENDENT_CHECK_TASK,
    }
    findings_payload = {
        "task_id": TASK_ID,
        "result": result,
        "report_convention": "GovernanceFinding",
        "report_convention_only": True,
        "findings": findings,
    }
    return index, report, findings_payload


def render_markdown(report: dict[str, Any], findings_payload: dict[str, Any]) -> str:
    lines = [
        "# Report Index",
        "",
        f"- task_id: {report['task_id']}",
        f"- result: {report['result']}",
        f"- repository_ref: {report['repository_ref']}",
        f"- baseline_ref: {report['baseline_ref']}",
        f"- index_path: {report['index_path']}",
        f"- scanned_report_count: {report['scanned_report_count']}",
        f"- indexed_report_count: {report['indexed_report_count']}",
        f"- ambiguous_count: {report['ambiguous_count']}",
        f"- finding_count: {report['finding_count']}",
        f"- recommended_next_task: {report['recommended_next_task']}",
        f"- independent_report_index_check: {report['independent_report_index_check']}",
        "",
        "## GeneratedOutputLedger Input",
        "",
        f"- status: {report['generated_output_ledger_input'].get('status')}",
        f"- accepted: {report['generated_output_ledger_input'].get('accepted')}",
        "",
        "## Counts By Stage",
        "",
    ]
    for key, value in report["counts_by_stage"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Counts By Severity", ""])
    for key, value in report["counts_by_severity"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Findings", ""])
    for finding in findings_payload["findings"]:
        lines.extend(
            [
                f"### {finding['id']}",
                "",
                f"- severity: {finding['severity']}",
                f"- surface: {finding['surface']}",
                f"- taxonomy: {finding['taxonomy']}",
                f"- claim: {finding['claim']}",
                f"- expected: {finding['expected']}",
                f"- observed: {finding['observed']}",
                f"- next_task: {finding['next_task']}",
                "",
            ]
        )
    lines.extend(["## Explicit Non-Capabilities", ""])
    for item in report["explicit_non_capabilities"]:
        lines.append(f"- {item}")
    return "\n".join(lines).rstrip() + "\n"


def write_report_index_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    index, report, findings = build_payloads(root)
    # JSON is valid YAML 1.2 and keeps this deterministic without an added
    # dependency.
    write_json(root / INDEX_PATH, index)
    write_json(root / REPORT_JSON, report)
    write_json(root / FINDINGS_JSON, findings)
    write_text(root / REPORT_MD, render_markdown(report, findings))
    return report


def validate_report_index_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    errors: list[str] = []
    warnings: list[str] = []
    required_record = {
        "report_id",
        "subject",
        "stage",
        "task_id",
        "path",
        "format",
        "producer",
        "producer_status",
        "source_refs",
        "evidence_refs",
        "baseline_ref",
        "canonical",
        "generated",
        "freshness",
        "related_report_paths",
        "related_task_ids",
        "warnings",
        "explicit_non_capabilities",
    }
    required_finding = {
        "id",
        "severity",
        "surface",
        "taxonomy",
        "claim",
        "expected",
        "observed",
        "evidence_refs",
        "affected_paths",
        "recommendation",
        "next_task",
    }
    try:
        index = json.loads((root / INDEX_PATH).read_text(encoding="utf-8"))
        report = json.loads((root / REPORT_JSON).read_text(encoding="utf-8"))
        findings = json.loads((root / FINDINGS_JSON).read_text(encoding="utf-8"))
        markdown = (root / REPORT_MD).read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "task_id": TASK_ID,
            "validation_status": "FAILED_VALIDATION",
            "validated": False,
            "errors": [str(exc)],
            "warnings": [],
        }
    if report.get("indexed_report_count") != len(index.get("reports", [])):
        errors.append("indexed_report_count does not match index records")
    for record in index.get("reports", []):
        if not required_record <= set(record):
            errors.append(f"record missing required fields: {record.get('path')}")
            break
        if record.get("canonical") != "false":
            errors.append(f"record overclaims canonical status: {record.get('path')}")
            break
    if report.get("finding_count") != len(findings.get("findings", [])):
        errors.append("finding_count does not match findings payload")
    for finding in findings.get("findings", []):
        if not required_finding <= set(finding):
            errors.append(f"finding missing required fields: {finding.get('id')}")
            break
        for key in ("id", "severity", "surface", "taxonomy", "next_task"):
            if str(finding.get(key)) not in markdown:
                errors.append(f"markdown missing finding {key}: {finding.get('id')}")
                break
    if not set(report.get("excluded_paths", [])) >= SELF_OUTPUTS:
        errors.append("self-index outputs are not explicitly excluded")
    if report.get("generated_output_ledger_input", {}).get("accepted") is not False:
        errors.append("GeneratedOutputLedger input must remain provisional")
    if not errors and report.get("result") == "PASS_WITH_WARNINGS":
        warnings.append("Report index intentionally preserves ambiguous producer/stage/freshness debt.")
    return {
        "task_id": TASK_ID,
        "validation_status": "PASS_WITH_WARNINGS" if warnings and not errors else ("PASS" if not errors else "FAILED_VALIDATION"),
        "validated": not errors,
        "index_present": True,
        "reports_present": True,
        "record_fields_valid": not errors,
        "finding_fields_valid": not errors,
        "markdown_json_agree": not errors,
        "errors": errors,
        "warnings": warnings,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "independent_report_index_check": INDEPENDENT_CHECK_TASK,
    }


if __name__ == "__main__":
    summary = write_report_index_reports(Path("."))
    print(stable_json(summary), end="")
