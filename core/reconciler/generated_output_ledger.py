"""Report-only generated-output classification ledger.

This module observes tracked AIDE files that are likely generated,
projected, exported, or report outputs. It emits a deterministic ledger and
reports. It does not regenerate, delete, repair, move, rename, or rewrite any
classified artifact.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01"
ACCEPTED_PREDECESSOR = "AIDE-ACCEPT-DOC-KNOWLEDGE-TRUTH-RECONCILER-01"
RECOMMENDED_NEXT_TASK = "AIDE-BUILD-REPORT-INDEX-01"
INDEPENDENT_CHECK_TASK = "AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01"
DETERMINISTIC_TIMESTAMP = "2026-06-18T00:00:00+10:00"

LEDGER_PATH = Path(".aide/ledgers/generated-output.yaml")
REPORT_ROOT = Path(".aide/reports/self-management")
REPORT_JSON = REPORT_ROOT / "generated-output-ledger.json"
REPORT_MD = REPORT_ROOT / "generated-output-ledger.md"
FINDINGS_JSON = REPORT_ROOT / "generated-output-ledger.findings.json"

SCAN_ROOTS = (
    ".aide/generated/",
    ".aide/context/",
    ".aide/export/",
    ".aide/reports/",
    ".aide/knowledge/okf/",
    ".agents/",
    ".codex/",
)

EXCLUDED_PREFIXES = (
    ".git/",
    ".aide.local/",
    ".aide/queue/AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01/",
)

SELF_OUTPUTS = {
    ".aide/ledgers/generated-output.yaml",
    ".aide/reports/self-management/generated-output-ledger.json",
    ".aide/reports/self-management/generated-output-ledger.md",
    ".aide/reports/self-management/generated-output-ledger.findings.json",
}

EXPLICIT_NON_CAPABILITIES = [
    "automatic_regeneration",
    "automatic_deletion",
    "automatic_cleanup",
    "source_rewrite",
    "okf_regeneration",
    "report_migration",
    "reference_rewrite",
    "file_move",
    "file_rename",
    "migration_apply",
    "runtime",
    "provider_calls",
    "network_calls",
    "github_mutation",
    "branch_worktree_automation",
    "release_behavior",
    "target_repo_mutation",
]


@dataclass(frozen=True)
class LedgerEntry:
    id: str
    path: str
    kind: str
    authority: str
    canonical: str
    classification: str
    generator: str
    generator_status: str
    source_refs: list[str]
    source_hashes: dict[str, str]
    generated_timestamp: str
    generator_version: str
    generation_command: str
    baseline_ref: str
    committed_intentionally: str
    freshness: str
    safe_to_regenerate: str
    safe_to_delete: str
    consumer_refs: list[str]
    evidence_refs: list[str]
    classification_confidence: str
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


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def normalize_path(value: str | Path) -> str:
    text = str(value).replace("\\", "/")
    if text.startswith("./"):
        return text[2:]
    return text


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


def tracked_files(repo_root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []
    return sorted(
        normalize_path(line)
        for line in result.stdout.splitlines()
        if line.strip()
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def read_text_optional(path: Path, limit: int = 512_000) -> str:
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def load_manifest_targets(repo_root: Path) -> dict[str, dict[str, Any]]:
    """Parse the current generated manifest enough for target classification.

    The repo does not require a YAML parser for this slice, so this scans the
    simple manifest shape generated by Q05.
    """

    manifest = repo_root / ".aide/generated/manifest.yaml"
    text = read_text_optional(manifest)
    targets: dict[str, dict[str, Any]] = {}
    current: dict[str, Any] | None = None
    source_list: list[str] | None = None
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("- path:"):
            if current and current.get("path"):
                targets[current["path"]] = current
            current = {"path": stripped.split(":", 1)[1].strip()}
            source_list = None
            continue
        if current is None:
            continue
        if stripped.startswith("section:"):
            current["section"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("mode:"):
            current["mode"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("status:"):
            current["status"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("source_fingerprint:"):
            current["source_fingerprint"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("content_fingerprint:"):
            current["content_fingerprint"] = stripped.split(":", 1)[1].strip()
        elif stripped == "sources:":
            source_list = []
            current["sources"] = source_list
        elif source_list is not None and stripped.startswith("- "):
            source_list.append(stripped[2:].strip())
    if current and current.get("path"):
        targets[current["path"]] = current
    return targets


def candidate_files(files: list[str]) -> tuple[list[str], list[str]]:
    candidates: list[str] = []
    excluded: list[str] = []
    for rel in files:
        if any(rel.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
            excluded.append(rel)
            continue
        if rel in SELF_OUTPUTS:
            excluded.append(rel)
            continue
        if any(rel.startswith(prefix) for prefix in SCAN_ROOTS):
            candidates.append(rel)
    return sorted(candidates), sorted(excluded)


def infer_task_ids(text: str, limit: int = 5) -> list[str]:
    values = sorted(set(re.findall(r"AIDE-[A-Z0-9][A-Z0-9-]+-01", text)))
    return values[:limit]


def authority_for_path(rel: str) -> str:
    if rel.startswith(".aide/reports/"):
        return "generated evidence, advisory report, or index"
    if rel.startswith(".aide/generated/"):
        return "generated preview or manifest"
    if rel.startswith(".aide/context/"):
        return "generated context projection"
    if rel.startswith(".aide/knowledge/okf/"):
        return "OKF knowledge projection"
    if rel.startswith(".aide/export/"):
        return "exported portable pack copy"
    if rel.startswith(".agents/") or rel.startswith(".codex/"):
        return "tool-specific interop projection"
    return "unknown generated-output candidate"


def classify_path(repo_root: Path, rel: str, manifest_targets: dict[str, dict[str, Any]]) -> LedgerEntry:
    path = repo_root / rel
    text = read_text_optional(path)
    task_ids = infer_task_ids(text)
    source_refs: list[str] = []
    evidence_refs: list[str] = []
    generator = "generator_unknown"
    generator_status = "unknown"
    generator_version = "unknown"
    generation_command = "unknown"
    generated_timestamp = "unknown"
    classification = "unknown_candidate"
    kind = "unknown_candidate"
    canonical = "unknown"
    confidence = "low"
    freshness = "unknown"
    warnings: list[str] = []

    manifest = manifest_targets.get(rel)
    if manifest:
        mode = manifest.get("mode", "generated")
        classification = "generated_context" if rel.startswith(".aide/context/") else "projection"
        if mode == "generated-preview":
            classification = "projection"
        if mode == "managed-section":
            classification = "projection"
        kind = classification
        generator = "aide-harness-generated-artifacts-v0"
        generator_status = "known"
        generator_version = "q05.generated-artifacts.v0"
        generation_command = "py -3 scripts/aide compile --write"
        source_refs = list(manifest.get("sources", []))
        freshness = "unknown"
        canonical = "false"
        confidence = "high"
    elif "AIDE-GENERATED:BEGIN" in text:
        classification = "projection"
        kind = "managed_section"
        generator_match = re.search(r"generator=([^\s]+)", text)
        version_match = re.search(r"version=([^\s]+)", text)
        sources_match = re.search(r"sources=([^\s]+)", text)
        generator = generator_match.group(1) if generator_match else "generator_unknown"
        generator_status = "known" if generator_match else "unknown"
        generator_version = version_match.group(1) if version_match else "unknown"
        source_refs = sources_match.group(1).split(",") if sources_match else []
        generation_command = "unknown"
        canonical = "false"
        confidence = "high"
    elif rel.startswith(".aide/reports/"):
        classification = "generated_report"
        kind = "generated_report"
        generator = "report_producer_inferred"
        generator_status = "inferred"
        source_refs = [f".aide/queue/{task_id}/status.yaml" for task_id in task_ids]
        evidence_refs = [f".aide/queue/{task_id}/evidence" for task_id in task_ids]
        canonical = "false"
        confidence = "medium"
    elif rel.startswith(".aide/knowledge/okf/"):
        classification = "projection"
        kind = "okf_projection"
        generator = "okf_projection_generator_unknown"
        generator_status = "unknown"
        canonical = "false"
        confidence = "medium"
    elif rel.startswith(".aide/context/"):
        classification = "generated_context"
        kind = "context_projection"
        generator = "context_compiler_inferred"
        generator_status = "inferred"
        canonical = "false"
        confidence = "medium"
    elif rel.startswith(".aide/export/"):
        classification = "exported_copy"
        kind = "export_pack_artifact"
        generator = "aide_export_pack_inferred"
        generator_status = "inferred"
        canonical = "false"
        confidence = "medium"
    elif rel.startswith(".agents/") or rel.startswith(".codex/"):
        classification = "tool_specific_projection"
        kind = "interop_projection"
        generator = "tool_projection_generator_unknown"
        generator_status = "unknown"
        canonical = "false"
        confidence = "medium"

    source_hashes: dict[str, str] = {}
    for source in source_refs[:10]:
        source_path = repo_root / source
        if source_path.exists() and source_path.is_file():
            source_hashes[source] = sha256_file(source_path)

    if generator_status == "unknown":
        warnings.append("generator_unknown")
    if freshness == "unknown":
        warnings.append("freshness_unknown")
    if not source_refs:
        warnings.append("source_refs_unknown")
    warnings.append("consumer_unknown")
    if canonical != "false":
        warnings.append("canonical_status_ambiguous")
    if rel.startswith(".aide/reports/") or rel.startswith(".aide/knowledge/okf/") or rel.startswith(".aide/context/"):
        warnings.append("generated_truth_risk")

    return LedgerEntry(
        id="generated-output-" + hashlib.sha1(rel.encode("utf-8")).hexdigest()[:12],
        path=rel,
        kind=kind,
        authority=authority_for_path(rel),
        canonical=canonical,
        classification=classification,
        generator=generator,
        generator_status=generator_status,
        source_refs=source_refs,
        source_hashes=source_hashes,
        generated_timestamp=generated_timestamp,
        generator_version=generator_version,
        generation_command=generation_command,
        baseline_ref=ACCEPTED_PREDECESSOR,
        committed_intentionally="true",
        freshness=freshness,
        safe_to_regenerate="unknown",
        safe_to_delete="unknown",
        consumer_refs=[],
        evidence_refs=evidence_refs,
        classification_confidence=confidence,
        warnings=sorted(set(warnings)),
        explicit_non_capabilities=EXPLICIT_NON_CAPABILITIES,
    )


def build_entries(repo_root: Path) -> tuple[list[LedgerEntry], list[str], list[str]]:
    files = tracked_files(repo_root)
    candidates, excluded = candidate_files(files)
    manifest_targets = load_manifest_targets(repo_root)
    entries = [classify_path(repo_root, rel, manifest_targets) for rel in candidates]
    entries.sort(key=lambda entry: entry.path)
    return entries, candidates, excluded


def counts(entries: list[LedgerEntry], attr: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for entry in entries:
        key = str(getattr(entry, attr))
        result[key] = result.get(key, 0) + 1
    return dict(sorted(result.items()))


def build_findings(entries: list[LedgerEntry]) -> list[GovernanceFinding]:
    paths_by_warning: dict[str, list[str]] = {}
    for entry in entries:
        for warning in entry.warnings:
            paths_by_warning.setdefault(warning, []).append(entry.path)

    def sample(name: str) -> list[str]:
        return sorted(paths_by_warning.get(name, []))[:20]

    findings = [
        GovernanceFinding(
            id="GOL-001",
            severity="info",
            surface="generated_outputs",
            taxonomy="truth_alignment_confirmed",
            claim="Generated-output candidates were classified without applying repairs.",
            expected="The ledger should observe and classify candidates without regenerating, deleting, or rewriting artifacts.",
            observed=f"Classified {len(entries)} candidate generated/projection/export/report artifacts.",
            evidence_refs=[normalize_path(LEDGER_PATH), normalize_path(REPORT_JSON)],
            affected_paths=[],
            recommendation="Proceed to the independent generated-output ledger check.",
            next_task=INDEPENDENT_CHECK_TASK,
        ),
        GovernanceFinding(
            id="GOL-002",
            severity="warning" if sample("generator_unknown") else "info",
            surface="generated_outputs",
            taxonomy="generator_unknown",
            claim="Some generated-output candidates have unknown generators.",
            expected="Every generated or projected artifact should eventually have a known or explicitly inferred generator.",
            observed=f"{len(paths_by_warning.get('generator_unknown', []))} candidates have unknown generator status.",
            evidence_refs=[normalize_path(LEDGER_PATH)],
            affected_paths=sample("generator_unknown"),
            recommendation="Keep unknown generator classifications as evidence-backed debt for future check/accept gates.",
            next_task=INDEPENDENT_CHECK_TASK,
        ),
        GovernanceFinding(
            id="GOL-003",
            severity="warning" if sample("freshness_unknown") else "info",
            surface="generated_outputs",
            taxonomy="freshness_unknown",
            claim="Freshness is unknown for many generated-output candidates.",
            expected="Freshness should remain unknown unless source fingerprints and generation rules prove otherwise.",
            observed=f"{len(paths_by_warning.get('freshness_unknown', []))} candidates have unknown freshness.",
            evidence_refs=[normalize_path(LEDGER_PATH)],
            affected_paths=sample("freshness_unknown"),
            recommendation="Do not refresh outputs in this task; let the independent check validate the conservative classification.",
            next_task=INDEPENDENT_CHECK_TASK,
        ),
        GovernanceFinding(
            id="GOL-004",
            severity="warning",
            surface="generated_outputs",
            taxonomy="consumer_unknown",
            claim="Consumer references are not fully known for generated-output candidates.",
            expected="Consumer discovery should be deterministic and explicit before delete or regeneration claims are made.",
            observed=f"{len(paths_by_warning.get('consumer_unknown', []))} candidates retain consumer_unknown.",
            evidence_refs=[normalize_path(LEDGER_PATH)],
            affected_paths=sample("consumer_unknown"),
            recommendation="Treat safe_to_delete and safe_to_regenerate as unknown until future consumer analysis is accepted.",
            next_task=INDEPENDENT_CHECK_TASK,
        ),
        GovernanceFinding(
            id="GOL-005",
            severity="warning" if sample("generated_truth_risk") else "info",
            surface="generated_report",
            taxonomy="generated_truth_risk",
            claim="Reports and projections can be mistaken for canonical truth if not explicitly bounded.",
            expected="Generated reports, OKF projections, and context projections should default to non-canonical unless reviewed policy proves otherwise.",
            observed=f"{len(paths_by_warning.get('generated_truth_risk', []))} candidates carry generated_truth_risk.",
            evidence_refs=[normalize_path(LEDGER_PATH), ".aide/policies/root-authority.yaml"],
            affected_paths=sample("generated_truth_risk"),
            recommendation="Preserve non-canonical defaults and route to the ledger check.",
            next_task=INDEPENDENT_CHECK_TASK,
        ),
        GovernanceFinding(
            id="GOL-006",
            severity="warning",
            surface="okf_knowledge",
            taxonomy="missing_evidence",
            claim="Some projection candidates lack source references.",
            expected="Generated and projected artifacts should eventually identify source refs and source hashes where cheap and deterministic.",
            observed=f"{len(paths_by_warning.get('source_refs_unknown', []))} candidates have unknown source refs.",
            evidence_refs=[normalize_path(LEDGER_PATH)],
            affected_paths=sample("source_refs_unknown"),
            recommendation="Keep unknown source refs as ledger debt; do not infer beyond available evidence.",
            next_task=INDEPENDENT_CHECK_TASK,
        ),
        GovernanceFinding(
            id="GOL-007",
            severity="info",
            surface="context_projection",
            taxonomy="truth_alignment_confirmed",
            claim="Context projections are classified as non-canonical generated context.",
            expected="Context packets and maps should remain projections, not queue or protocol truth.",
            observed=f"{counts(entries, 'classification').get('generated_context', 0)} context projection candidates were classified.",
            evidence_refs=[normalize_path(LEDGER_PATH), "docs/reference/source-of-truth.md"],
            affected_paths=[entry.path for entry in entries if entry.classification == "generated_context"][:20],
            recommendation="Keep context projection entries in the generated-output ledger.",
            next_task=INDEPENDENT_CHECK_TASK,
        ),
        GovernanceFinding(
            id="GOL-008",
            severity="info",
            surface="interop_projection",
            taxonomy="truth_alignment_confirmed",
            claim="Tool-specific projection roots are classified without making them canonical.",
            expected=".agents and .codex surfaces should not become hidden AIDE queue or protocol truth.",
            observed=f"{counts(entries, 'classification').get('tool_specific_projection', 0)} tool-specific projection candidates were classified.",
            evidence_refs=[normalize_path(LEDGER_PATH), ".aide/policies/root-authority.yaml"],
            affected_paths=[entry.path for entry in entries if entry.classification == "tool_specific_projection"][:20],
            recommendation="Keep tool-specific projections bounded until a future interop policy task changes them.",
            next_task=INDEPENDENT_CHECK_TASK,
        ),
        GovernanceFinding(
            id="GOL-009",
            severity="info",
            surface="export_projection",
            taxonomy="truth_alignment_confirmed",
            claim="Export pack artifacts are classified as exported copies.",
            expected="Export pack copies should not become source-generated target truth for the live AIDE repo.",
            observed=f"{counts(entries, 'classification').get('exported_copy', 0)} export artifacts were classified.",
            evidence_refs=[normalize_path(LEDGER_PATH), "docs/reference/source-of-truth.md"],
            affected_paths=[entry.path for entry in entries if entry.classification == "exported_copy"][:20],
            recommendation="Keep export artifacts non-canonical and proceed to independent check.",
            next_task=INDEPENDENT_CHECK_TASK,
        ),
    ]
    return findings


def build_payloads(repo_root: str | Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    root = Path(repo_root)
    entries, candidates, excluded = build_entries(root)
    entry_dicts = [asdict(entry) for entry in entries]
    findings = build_findings(entries)
    finding_dicts = [asdict(finding) for finding in findings]
    severity_counts: dict[str, int] = {}
    surface_counts: dict[str, int] = {}
    taxonomy_counts: dict[str, int] = {}
    for finding in finding_dicts:
        severity_counts[finding["severity"]] = severity_counts.get(finding["severity"], 0) + 1
        surface_counts[finding["surface"]] = surface_counts.get(finding["surface"], 0) + 1
        taxonomy_counts[finding["taxonomy"]] = taxonomy_counts.get(finding["taxonomy"], 0) + 1

    result = "PASS_WITH_WARNINGS" if any(f["severity"] == "warning" for f in finding_dicts) else "PASS"
    ledger = {
        "format_version": "aide.generated-output-ledger.v0",
        "task_id": TASK_ID,
        "repository_ref": git_ref(root),
        "baseline_ref": ACCEPTED_PREDECESSOR,
        "profile": "AIDE_SELF_PROFILE",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "scan_mode": "full",
        "scanned_path_count": len(candidates),
        "candidate_count": len(candidates),
        "classified_count": len(entries),
        "unknown_count": sum(1 for entry in entries if entry.generator_status == "unknown"),
        "excluded_paths": excluded,
        "source_hash_algorithm": "sha256",
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "entries": entry_dicts,
    }
    report = {
        "task_id": TASK_ID,
        "result": result,
        "repository_ref": ledger["repository_ref"],
        "baseline_ref": ACCEPTED_PREDECESSOR,
        "scan_mode": "full",
        "ledger_path": normalize_path(LEDGER_PATH),
        "scanned_path_count": len(candidates),
        "candidate_count": len(candidates),
        "classified_count": len(entries),
        "unknown_count": ledger["unknown_count"],
        "counts_by_classification": counts(entries, "classification"),
        "counts_by_generator_status": counts(entries, "generator_status"),
        "counts_by_canonical": counts(entries, "canonical"),
        "counts_by_confidence": counts(entries, "classification_confidence"),
        "finding_count": len(finding_dicts),
        "counts_by_severity": dict(sorted(severity_counts.items())),
        "counts_by_surface": dict(sorted(surface_counts.items())),
        "counts_by_taxonomy": dict(sorted(taxonomy_counts.items())),
        "excluded_paths": excluded,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "independent_check_task": INDEPENDENT_CHECK_TASK,
    }
    findings_payload = {
        "task_id": TASK_ID,
        "result": result,
        "report_convention": "GovernanceFinding",
        "report_convention_only": True,
        "findings": finding_dicts,
    }
    return ledger, report, findings_payload


def render_markdown(report: dict[str, Any], findings_payload: dict[str, Any]) -> str:
    lines = [
        "# Generated Output Ledger",
        "",
        f"- task_id: {report['task_id']}",
        f"- result: {report['result']}",
        f"- repository_ref: {report['repository_ref']}",
        f"- baseline_ref: {report['baseline_ref']}",
        f"- ledger_path: {report['ledger_path']}",
        f"- scanned_path_count: {report['scanned_path_count']}",
        f"- classified_count: {report['classified_count']}",
        f"- unknown_count: {report['unknown_count']}",
        f"- finding_count: {report['finding_count']}",
        f"- recommended_next_task: {report['recommended_next_task']}",
        f"- independent_check_task: {report['independent_check_task']}",
        "",
        "## Counts By Classification",
        "",
    ]
    for key, value in report["counts_by_classification"].items():
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


def write_generated_output_ledger_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    ledger, report, findings = build_payloads(root)
    # JSON is valid YAML 1.2 and keeps this deterministic without an added
    # dependency.
    write_json(root / LEDGER_PATH, ledger)
    write_json(root / REPORT_JSON, report)
    write_json(root / FINDINGS_JSON, findings)
    write_text(root / REPORT_MD, render_markdown(report, findings))
    return report


def validate_generated_output_ledger_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    errors: list[str] = []
    warnings: list[str] = []
    required_report = {
        "task_id",
        "result",
        "repository_ref",
        "baseline_ref",
        "ledger_path",
        "classified_count",
        "finding_count",
        "counts_by_severity",
        "recommended_next_task",
        "independent_check_task",
    }
    required_entry = {
        "id",
        "path",
        "kind",
        "authority",
        "canonical",
        "classification",
        "generator",
        "generator_status",
        "source_refs",
        "source_hashes",
        "generated_timestamp",
        "generator_version",
        "generation_command",
        "baseline_ref",
        "committed_intentionally",
        "freshness",
        "safe_to_regenerate",
        "safe_to_delete",
        "consumer_refs",
        "evidence_refs",
        "classification_confidence",
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
        ledger = json.loads((root / LEDGER_PATH).read_text(encoding="utf-8"))
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

    if not required_report <= set(report):
        errors.append("report missing required fields")
    if report.get("classified_count") != len(ledger.get("entries", [])):
        errors.append("classified_count does not match ledger entries")
    for entry in ledger.get("entries", []):
        if not required_entry <= set(entry):
            errors.append(f"entry missing required fields: {entry.get('path')}")
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
    if any(entry.get("safe_to_delete") != "unknown" for entry in ledger.get("entries", [])):
        errors.append("safe_to_delete was overclaimed")
    if any(entry.get("canonical") == "true" for entry in ledger.get("entries", [])):
        errors.append("canonical true requires future reviewed policy")
    if report.get("result") == "PASS_WITH_WARNINGS":
        warnings.append("Generated-output ledger intentionally preserves unknown provenance and freshness debt.")

    return {
        "task_id": TASK_ID,
        "validation_status": "PASS_WITH_WARNINGS" if warnings and not errors else ("PASS" if not errors else "FAILED_VALIDATION"),
        "validated": not errors,
        "ledger_present": True,
        "reports_present": True,
        "entry_fields_valid": not errors,
        "finding_fields_valid": not errors,
        "markdown_json_agree": not errors,
        "errors": errors,
        "warnings": warnings,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "independent_check_task": INDEPENDENT_CHECK_TASK,
    }


if __name__ == "__main__":
    summary = write_generated_output_ledger_reports(Path("."))
    print(stable_json(summary), end="")
