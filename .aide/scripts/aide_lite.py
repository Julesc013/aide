#!/usr/bin/env python3
"""AIDE Lite token-survival helper.

This file is intentionally standard-library only. It compiles compact
task packets from repo-local state, validates Q09/Q10 token-survival
anchors, and never calls providers, models, network services, or
external tools.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


GENERATOR_NAME = "aide-lite"
GENERATOR_VERSION = "q14.token-ledger.v0"
SNAPSHOT_PATH = ".aide/context/repo-snapshot.json"
LATEST_PACKET_PATH = ".aide/context/latest-task-packet.md"
REVIEW_PACKET_PATH = ".aide/context/latest-review-packet.md"
REPO_MAP_JSON_PATH = ".aide/context/repo-map.json"
REPO_MAP_MD_PATH = ".aide/context/repo-map.md"
TEST_MAP_JSON_PATH = ".aide/context/test-map.json"
CONTEXT_INDEX_PATH = ".aide/context/context-index.json"
LATEST_CONTEXT_PACKET_PATH = ".aide/context/latest-context-packet.md"
CONTEXT_COMPILER_CONFIG_PATH = ".aide/context/compiler.yaml"
CONTEXT_PRIORITY_PATH = ".aide/context/priority.yaml"
EXCERPT_POLICY_PATH = ".aide/context/excerpt-policy.yaml"
VERIFICATION_POLICY_PATH = ".aide/policies/verification.yaml"
EVIDENCE_TEMPLATE_PATH = ".aide/verification/evidence-packet.template.md"
REVIEW_TEMPLATE_PATH = ".aide/verification/review-packet.template.md"
REVIEW_DECISION_POLICY_PATH = ".aide/verification/review-decision-policy.yaml"
DIFF_SCOPE_POLICY_PATH = ".aide/verification/diff-scope-policy.yaml"
FILE_REFERENCE_POLICY_PATH = ".aide/verification/file-reference-policy.yaml"
SECRET_SCAN_POLICY_PATH = ".aide/verification/secret-scan-policy.yaml"
LATEST_VERIFICATION_REPORT_PATH = ".aide/verification/latest-verification-report.md"
TOKEN_LEDGER_POLICY_PATH = ".aide/policies/token-ledger.yaml"
TOKEN_LEDGER_PATH = ".aide/reports/token-ledger.jsonl"
TOKEN_BASELINES_PATH = ".aide/reports/token-baselines.yaml"
TOKEN_SUMMARY_PATH = ".aide/reports/token-savings-summary.md"
AGENTS_SECTION = "token-survival-core"
AGENTS_BEGIN = f"<!-- AIDE-GENERATED:BEGIN section={AGENTS_SECTION}"
AGENTS_END = f"<!-- AIDE-GENERATED:END section={AGENTS_SECTION} -->"
LEGACY_AGENTS_BEGIN = "<!-- AIDE-TOKEN-SURVIVAL:BEGIN section=q09-token-survival mode=managed -->"
LEGACY_AGENTS_END = "<!-- AIDE-TOKEN-SURVIVAL:END section=q09-token-survival -->"

REQUIRED_FILES = [
    ".aide/policies/token-budget.yaml",
    ".aide/memory/project-state.md",
    ".aide/memory/decisions.md",
    ".aide/memory/open-risks.md",
    ".aide/prompts/compact-task.md",
    ".aide/prompts/evidence-review.md",
    ".aide/prompts/codex-token-mode.md",
    ".aide/context/ignore.yaml",
]

CONTEXT_CONFIG_FILES = [
    CONTEXT_COMPILER_CONFIG_PATH,
    CONTEXT_PRIORITY_PATH,
    EXCERPT_POLICY_PATH,
]

CONTEXT_OUTPUT_PATHS = [
    REPO_MAP_JSON_PATH,
    REPO_MAP_MD_PATH,
    TEST_MAP_JSON_PATH,
    CONTEXT_INDEX_PATH,
    LATEST_CONTEXT_PACKET_PATH,
]

VERIFICATION_CONFIG_FILES = [
    VERIFICATION_POLICY_PATH,
    EVIDENCE_TEMPLATE_PATH,
    REVIEW_TEMPLATE_PATH,
    REVIEW_DECISION_POLICY_PATH,
    DIFF_SCOPE_POLICY_PATH,
    FILE_REFERENCE_POLICY_PATH,
    SECRET_SCAN_POLICY_PATH,
]

GENERATED_CONTEXT_PATHS = {
    SNAPSHOT_PATH,
    LATEST_PACKET_PATH,
    REVIEW_PACKET_PATH,
    *CONTEXT_OUTPUT_PATHS,
}

COMPACT_TASK_SECTIONS = [
    "PHASE",
    "GOAL",
    "WHY",
    "CONTEXT_REFS",
    "ALLOWED_PATHS",
    "FORBIDDEN_PATHS",
    "IMPLEMENTATION",
    "VALIDATION",
    "EVIDENCE",
    "NON_GOALS",
    "ACCEPTANCE",
]

PACKET_REQUIRED_SECTIONS = [*COMPACT_TASK_SECTIONS, "OUTPUT_SCHEMA", "TOKEN_ESTIMATE"]

CONTEXT_PACKET_REQUIRED_SECTIONS = [
    "CONTEXT_COMPILER",
    "SOURCE_REFS",
    "REPO_MAP",
    "TEST_MAP",
    "CURRENT_QUEUE",
    "EXACT_REFS",
    "TOKEN_ESTIMATE",
]

EVIDENCE_PACKET_REQUIRED_SECTIONS = [
    "Task",
    "Objective",
    "Scope",
    "Changed Files",
    "Validation Commands",
    "Validation Results",
    "Generated Artifacts",
    "Token Estimates",
    "Risks",
    "Deferrals",
    "Next Recommended Phase",
]

REVIEW_PACKET_REQUIRED_SECTIONS = [
    "Review Objective",
    "Decision Requested",
    "Task Packet Reference",
    "Context Packet Reference",
    "Verification Report Reference",
    "Evidence Packet References",
    "Changed Files Summary",
    "Validation Summary",
    "Token Summary",
    "Risk Summary",
    "Non-Goals / Scope Guard",
    "Reviewer Instructions",
]

VERIFICATION_REPORT_REQUIRED_SECTIONS = [
    "VERIFIER_RESULT",
    "CHECK_COUNTS",
    "WARNINGS",
    "ERRORS",
    "EVIDENCE_REFS",
]

Q12_REQUIRED_FILES = [
    VERIFICATION_POLICY_PATH,
    EVIDENCE_TEMPLATE_PATH,
    REVIEW_TEMPLATE_PATH,
    REVIEW_DECISION_POLICY_PATH,
    DIFF_SCOPE_POLICY_PATH,
    FILE_REFERENCE_POLICY_PATH,
    SECRET_SCAN_POLICY_PATH,
]

Q14_REQUIRED_FILES = [
    TOKEN_LEDGER_POLICY_PATH,
    TOKEN_BASELINES_PATH,
    TOKEN_LEDGER_PATH,
    TOKEN_SUMMARY_PATH,
]

LEDGER_SURFACES = [
    "task_packet",
    "context_packet",
    "review_packet",
    "verification_report",
    "evidence_packet",
    "baseline_surface",
    "generated_adapter",
]

TOKEN_LEDGER_ANCHORS = [
    "schema_version",
    "policy_id",
    "approximation_method",
    "storage_policy",
    "raw_prompt_storage_default",
    "raw_response_storage_default",
    "committed_ledger_allowed",
    "record_surfaces",
    "required_record_fields",
    "comparison_policy",
    "regression_policy",
    "limitations",
]

TOKEN_BUDGET_ANCHORS = [
    "schema_version",
    "policy_id",
    "status",
    "purpose",
    "approx_token_method",
    "targets",
    "project_state_target_tokens",
    "compact_task_packet_target_tokens",
    "review_packet_target_tokens",
    "codex_prompt_target_tokens",
    "gpt_review_prompt_target_tokens",
    "hard_limits",
    "max_compact_task_packet_tokens",
    "max_review_packet_tokens",
    "max_project_state_tokens",
    "forbidden_prompt_patterns",
    "required_prompt_sections",
    "output_discipline",
    "review_policy",
    "non_degradation_rule",
]

REQUIRED_IGNORE_PATTERNS = [
    ".git/**",
    ".env",
    "secrets/**",
    ".aide.local/**",
    "__pycache__/**",
    ".pytest_cache/**",
    ".mypy_cache/**",
    ".ruff_cache/**",
    "node_modules/**",
    "dist/**",
    "build/**",
]

FORBIDDEN_PACKET_PHRASES = [
    "full prior transcript",
    "whole repo dump",
    "repeated roadmap dump",
    "model/provider keys",
]

CONTEXT_FORBIDDEN_INLINE_MARKERS = [
    "print('hello')",
    "SHOULD_NOT_APPEAR",
]

ROLE_ORDER = [
    "aide_contract",
    "aide_policy",
    "aide_prompt",
    "aide_context",
    "aide_queue",
    "aide_evidence",
    "harness_code",
    "compat_code",
    "shared_code",
    "test",
    "docs",
    "governance",
    "inventory",
    "matrix",
    "research",
    "host",
    "bridge",
    "script",
    "config",
    "generated",
    "binary_or_asset",
    "unknown",
]

BINARY_EXTENSIONS = {
    ".7z",
    ".bin",
    ".bmp",
    ".dll",
    ".dmg",
    ".dylib",
    ".exe",
    ".gif",
    ".ico",
    ".iso",
    ".jpeg",
    ".jpg",
    ".msi",
    ".nupkg",
    ".pdf",
    ".pkg",
    ".png",
    ".pyo",
    ".pyc",
    ".rar",
    ".so",
    ".tar",
    ".tgz",
    ".whl",
    ".zip",
}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"sk-ant-[A-Za-z0-9_-]{16,}"),
    re.compile(r"(?i)\b(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
]

SECRET_POLICY_TERM_PATTERN = re.compile(r"(?i)\b(api[_-]?key|secret|password|token)\b")


@dataclass(frozen=True)
class TextStats:
    path: str
    chars: int
    lines: int
    approx_tokens: int


@dataclass(frozen=True)
class Check:
    severity: str
    message: str


@dataclass(frozen=True)
class AdapterStatus:
    status: str
    action_hint: str
    body_matches: bool
    fingerprint_matches: bool


@dataclass(frozen=True)
class WriteResult:
    path: Path
    action: str


@dataclass(frozen=True)
class PacketRender:
    text: str
    stats: TextStats
    budget_status: str
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class VerificationFinding:
    severity: str
    check: str
    message: str
    path: str = ""


@dataclass(frozen=True)
class DiffScopeResult:
    status: str
    path: str
    classification: str
    reason: str


@dataclass(frozen=True)
class VerificationReport:
    result: str
    findings: tuple[VerificationFinding, ...]
    checked_files: tuple[str, ...]
    changed_files: tuple[DiffScopeResult, ...]


@dataclass(frozen=True)
class LedgerRecord:
    run_id: str
    phase: str
    surface: str
    path: str
    chars: int
    lines: int
    approx_tokens: int
    method: str
    budget: str
    budget_status: str
    notes: str


@dataclass(frozen=True)
class BaselineDefinition:
    name: str
    purpose: str
    paths: tuple[str, ...]


@dataclass(frozen=True)
class BaselineResult:
    name: str
    chars: int
    lines: int
    approx_tokens: int
    method: str
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class LedgerComparison:
    compact: LedgerRecord
    baseline: BaselineResult
    reduction_percent: float | None
    warnings: tuple[str, ...]


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize_rel(path: str | Path) -> str:
    rel = Path(path).as_posix()
    while rel.startswith("./"):
        rel = rel[2:]
    return rel


def normalize_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in normalized.splitlines()).strip() + "\n"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text_if_changed(path: Path, text: str) -> WriteResult:
    normalized = normalize_text(text)
    if path.exists() and normalize_text(read_text(path)) == normalized:
        return WriteResult(path, "unchanged")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(normalized, encoding="utf-8", newline="\n")
    return WriteResult(path, "written")


def write_text(path: Path, text: str) -> None:
    write_text_if_changed(path, text)


def sha256_text(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def approx_tokens_for_chars(chars: int) -> int:
    return int(math.ceil(chars / 4)) if chars else 0


def estimate_text(text: str, path: str = "<memory>") -> TextStats:
    return TextStats(
        path=path,
        chars=len(text),
        lines=0 if not text else text.count("\n") + (0 if text.endswith("\n") else 1),
        approx_tokens=approx_tokens_for_chars(len(text)),
    )


def safe_repo_path(repo_root: Path, requested: str) -> Path:
    target = (repo_root / requested).resolve()
    root = repo_root.resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path must stay inside repo: {requested}") from exc
    return target


def looks_binary(path: Path) -> bool:
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True
    sample = path.read_bytes()[:4096]
    if b"\x00" in sample:
        return True
    try:
        sample.decode("utf-8")
    except UnicodeDecodeError:
        return True
    return False


def estimate_file(repo_root: Path, requested: str) -> TextStats:
    target = safe_repo_path(repo_root, requested)
    if not target.exists():
        raise ValueError(f"file does not exist: {requested}")
    if not target.is_file():
        raise ValueError(f"path is not a file: {requested}")
    if looks_binary(target):
        raise ValueError(f"refusing to estimate binary-like file: {requested}")
    text = read_text(target)
    return estimate_text(text, normalize_rel(target.relative_to(repo_root)))


def ledger_record_for_file(
    repo_root: Path,
    requested: str,
    surface: str | None = None,
    phase: str = "Q14-token-ledger-savings-report",
    run_id: str = "q14.scan.current",
    notes: str = "",
) -> LedgerRecord:
    rel = normalize_rel(requested)
    stats = estimate_file(repo_root, rel)
    surface_value = surface or detect_surface(stats.path)
    if surface_value not in LEDGER_SURFACES:
        raise ValueError(f"unknown ledger surface: {surface_value}")
    budget, budget_status = ledger_budget_status(repo_root, surface_value, stats.approx_tokens)
    return LedgerRecord(
        run_id=run_id,
        phase=phase,
        surface=surface_value,
        path=stats.path,
        chars=stats.chars,
        lines=stats.lines,
        approx_tokens=stats.approx_tokens,
        method="chars/4",
        budget=budget,
        budget_status=budget_status,
        notes=notes or "estimated metadata only; raw content not stored",
    )


def ledger_record_to_dict(record: LedgerRecord) -> dict[str, object]:
    return {
        "run_id": record.run_id,
        "phase": record.phase,
        "surface": record.surface,
        "path": record.path,
        "chars": record.chars,
        "lines": record.lines,
        "approx_tokens": record.approx_tokens,
        "method": record.method,
        "budget": record.budget,
        "budget_status": record.budget_status,
        "notes": record.notes,
    }


def ledger_record_from_dict(data: dict[str, object]) -> LedgerRecord:
    return LedgerRecord(
        run_id=str(data.get("run_id", "")),
        phase=str(data.get("phase", "")),
        surface=str(data.get("surface", "")),
        path=normalize_rel(str(data.get("path", ""))),
        chars=int(data.get("chars", 0) or 0),
        lines=int(data.get("lines", 0) or 0),
        approx_tokens=int(data.get("approx_tokens", 0) or 0),
        method=str(data.get("method", "chars/4")),
        budget=str(data.get("budget", "unknown")),
        budget_status=str(data.get("budget_status", "unknown_budget")),
        notes=str(data.get("notes", "")),
    )


def read_ledger_records(repo_root: Path) -> list[LedgerRecord]:
    path = repo_root / TOKEN_LEDGER_PATH
    if not path.exists():
        return []
    records: list[LedgerRecord] = []
    for line in read_text(path).splitlines():
        if not line.strip():
            continue
        try:
            records.append(ledger_record_from_dict(json.loads(line)))
        except (json.JSONDecodeError, TypeError, ValueError):
            continue
    return records


def write_ledger_records(repo_root: Path, records: Iterable[LedgerRecord]) -> WriteResult:
    sorted_records = sorted(records, key=lambda item: (item.run_id, item.phase, item.surface, item.path))
    lines = [
        json.dumps(ledger_record_to_dict(record), sort_keys=True, separators=(",", ":"))
        for record in sorted_records
    ]
    return write_text_if_changed(repo_root / TOKEN_LEDGER_PATH, "\n".join(lines) + ("\n" if lines else ""))


def merge_ledger_records(repo_root: Path, new_records: Iterable[LedgerRecord], run_id: str) -> tuple[WriteResult, list[LedgerRecord], list[LedgerRecord]]:
    existing = read_ledger_records(repo_root)
    new_list = list(new_records)
    retained = [record for record in existing if record.run_id != run_id]
    merged = [*retained, *new_list]
    return write_ledger_records(repo_root, merged), merged, existing


def assert_ledger_safe_path(repo_root: Path, requested: str) -> str:
    rel = normalize_rel(requested)
    target = safe_repo_path(repo_root, rel)
    if not target.exists():
        raise ValueError(f"file does not exist: {rel}")
    if not target.is_file():
        raise ValueError(f"path is not a file: {rel}")
    if rel not in GENERATED_CONTEXT_PATHS and is_ignored(rel, load_ignore_patterns(repo_root)):
        raise ValueError(f"refusing ignored/local/secret path for ledger: {rel}")
    if looks_binary(target):
        raise ValueError(f"refusing binary-like file for ledger: {rel}")
    return rel


def ledger_scan_paths(repo_root: Path) -> list[tuple[str, str, str]]:
    candidates: list[tuple[str, str, str]] = [
        (LATEST_PACKET_PATH, "task_packet", "latest compact task packet"),
        (LATEST_CONTEXT_PACKET_PATH, "context_packet", "latest compact context packet"),
        (REVIEW_PACKET_PATH, "review_packet", "latest compact review packet"),
        (LATEST_VERIFICATION_REPORT_PATH, "verification_report", "latest compact verification report"),
        (".aide/prompts/compact-task.md", "baseline_surface", "compact task prompt template"),
        (".aide/prompts/evidence-review.md", "baseline_surface", "evidence review prompt template"),
        (".aide/prompts/codex-token-mode.md", "baseline_surface", "Codex token-mode guidance"),
        ("AGENTS.md", "generated_adapter", "managed agent guidance"),
    ]
    for queue_id in ["Q09-token-survival-core", "Q10-aide-lite-hardening", "Q11-context-compiler-v0", "Q12-verifier-v0", "Q13-evidence-review-workflow", "Q14-token-ledger-savings-report"]:
        evidence_dir = repo_root / f".aide/queue/{queue_id}/evidence"
        if evidence_dir.exists():
            for path in sorted(evidence_dir.glob("*.md")):
                rel = normalize_rel(path.relative_to(repo_root))
                candidates.append((rel, "evidence_packet", f"{queue_id} evidence"))
    seen: set[str] = set()
    result: list[tuple[str, str, str]] = []
    for rel, surface, notes in candidates:
        if rel in seen or not (repo_root / rel).exists():
            continue
        if rel not in GENERATED_CONTEXT_PATHS and is_ignored(rel, load_ignore_patterns(repo_root)):
            continue
        seen.add(rel)
        result.append((rel, surface, notes))
    return sorted(result, key=lambda item: item[0])


def build_ledger_scan_records(repo_root: Path, run_id: str = "q14.scan.current") -> list[LedgerRecord]:
    records: list[LedgerRecord] = []
    for rel, surface, notes in ledger_scan_paths(repo_root):
        records.append(ledger_record_for_file(repo_root, rel, surface, run_id=run_id, notes=notes))
    return records


def parse_token_baselines(repo_root: Path) -> list[BaselineDefinition]:
    path = repo_root / TOKEN_BASELINES_PATH
    if not path.exists():
        return []
    baselines: list[BaselineDefinition] = []
    name = ""
    purpose = ""
    paths: list[str] = []
    in_paths = False
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if stripped.startswith("- name:"):
            if name:
                baselines.append(BaselineDefinition(name, purpose, tuple(paths)))
            name = stripped.split(":", 1)[1].strip()
            purpose = ""
            paths = []
            in_paths = False
            continue
        if not name:
            continue
        if stripped.startswith("purpose:"):
            purpose = stripped.split(":", 1)[1].strip()
            in_paths = False
            continue
        if stripped == "paths:":
            in_paths = True
            continue
        if in_paths and stripped.startswith("- "):
            paths.append(normalize_rel(stripped[2:].strip().strip('"').strip("'")))
            continue
        if stripped and not stripped.startswith("#"):
            in_paths = False
    if name:
        baselines.append(BaselineDefinition(name, purpose, tuple(paths)))
    return baselines


def baseline_by_name(repo_root: Path, name: str) -> BaselineDefinition:
    for baseline in parse_token_baselines(repo_root):
        if baseline.name == name:
            return baseline
    raise ValueError(f"unknown baseline: {name}")


def calculate_baseline(repo_root: Path, baseline: BaselineDefinition) -> BaselineResult:
    chars = 0
    lines = 0
    warnings: list[str] = []
    for rel in baseline.paths:
        try:
            if rel not in GENERATED_CONTEXT_PATHS and is_ignored(rel, load_ignore_patterns(repo_root)):
                warnings.append(f"ignored baseline path skipped: {rel}")
                continue
            stats = estimate_file(repo_root, rel)
            chars += stats.chars
            lines += stats.lines
        except ValueError as exc:
            warnings.append(str(exc))
    return BaselineResult(
        name=baseline.name,
        chars=chars,
        lines=lines,
        approx_tokens=approx_tokens_for_chars(chars),
        method="chars/4",
        warnings=tuple(warnings),
    )


def compare_to_baseline(repo_root: Path, compact_path: str, baseline_name: str, surface: str | None = None) -> LedgerComparison:
    rel = assert_ledger_safe_path(repo_root, compact_path)
    compact = ledger_record_for_file(
        repo_root,
        rel,
        surface=surface or detect_surface(rel),
        run_id="q14.compare",
        notes=f"comparison against {baseline_name}",
    )
    baseline = calculate_baseline(repo_root, baseline_by_name(repo_root, baseline_name))
    reduction = None
    warnings = list(baseline.warnings)
    if baseline.approx_tokens > 0:
        reduction = ((baseline.approx_tokens - compact.approx_tokens) / baseline.approx_tokens) * 100
    else:
        warnings.append(f"baseline unavailable or empty: {baseline_name}")
    return LedgerComparison(compact, baseline, reduction, tuple(warnings))


def previous_records_by_path(records: Iterable[LedgerRecord], run_id: str) -> dict[tuple[str, str], LedgerRecord]:
    previous: dict[tuple[str, str], LedgerRecord] = {}
    for record in sorted(records, key=lambda item: (item.run_id, item.phase, item.surface, item.path)):
        if record.run_id == run_id:
            continue
        previous[(record.surface, record.path)] = record
    return previous


def regression_warnings(existing_records: Iterable[LedgerRecord], current_records: Iterable[LedgerRecord], threshold_percent: int) -> list[str]:
    previous = previous_records_by_path(existing_records, "q14.scan.current")
    warnings: list[str] = []
    for record in current_records:
        prior = previous.get((record.surface, record.path))
        if not prior or prior.approx_tokens <= 0:
            continue
        increase = ((record.approx_tokens - prior.approx_tokens) / prior.approx_tokens) * 100
        if increase > threshold_percent:
            warnings.append(
                f"{record.surface} `{record.path}` increased {increase:.1f}% ({prior.approx_tokens} -> {record.approx_tokens} approx tokens)"
            )
    return warnings


def ledger_budget_warnings(records: Iterable[LedgerRecord]) -> list[str]:
    warnings: list[str] = []
    for record in records:
        if record.budget_status == "near_budget":
            warnings.append(f"near budget: {record.surface} `{record.path}` {record.approx_tokens}/{record.budget}")
        elif record.budget_status == "over_budget":
            warnings.append(f"over budget: {record.surface} `{record.path}` {record.approx_tokens}/{record.budget}")
    return warnings


def render_token_savings_summary(repo_root: Path, records: list[LedgerRecord], regression: list[str]) -> str:
    latest = {record.path: record for record in records if record.run_id == "q14.scan.current"}
    latest_lines = []
    for rel in [LATEST_PACKET_PATH, LATEST_CONTEXT_PACKET_PATH, REVIEW_PACKET_PATH, LATEST_VERIFICATION_REPORT_PATH]:
        record = latest.get(rel)
        if record:
            latest_lines.append(f"- `{rel}`: {record.chars} chars / {record.approx_tokens} approx tokens / {record.budget_status}")
        else:
            latest_lines.append(f"- `{rel}`: missing from latest ledger scan")

    baseline_lines = []
    for baseline in parse_token_baselines(repo_root):
        result = calculate_baseline(repo_root, baseline)
        warning_note = f" ({len(result.warnings)} warning(s))" if result.warnings else ""
        baseline_lines.append(f"- `{baseline.name}`: {result.chars} chars / {result.approx_tokens} approx tokens{warning_note}")

    comparison_lines = []
    for compact_path, baseline_name in [
        (LATEST_PACKET_PATH, "root_history_baseline"),
        (REVIEW_PACKET_PATH, "review_baseline"),
        (LATEST_CONTEXT_PACKET_PATH, "repo_context_baseline"),
    ]:
        if not (repo_root / compact_path).exists():
            continue
        comparison = compare_to_baseline(repo_root, compact_path, baseline_name)
        if comparison.reduction_percent is None:
            comparison_lines.append(f"- `{compact_path}` vs `{baseline_name}`: unavailable")
        else:
            comparison_lines.append(
                f"- `{compact_path}` vs `{baseline_name}`: {comparison.reduction_percent:.1f}% estimated reduction "
                f"({comparison.compact.approx_tokens} vs {comparison.baseline.approx_tokens} approx tokens)"
            )

    budget_warnings = ledger_budget_warnings(records)
    budget_lines = [f"- {warning}" for warning in budget_warnings] or ["- none"]
    regression_lines = [f"- {warning}" for warning in regression] or ["- none"]
    largest = sorted(records, key=lambda item: item.approx_tokens, reverse=True)[:10]
    largest_lines = [
        f"- `{record.path}` ({record.surface}): {record.approx_tokens} approx tokens"
        for record in largest
    ] or ["- no records"]

    return f"""# AIDE Token Savings Summary

## Method

- approximation: chars / 4, rounded up
- exact_provider_billing: false
- exact_tokenizer: false
- raw_prompt_storage: false
- raw_response_storage: false

## Latest Compact Surfaces

{chr(10).join(latest_lines)}

## Named Baselines

{chr(10).join(baseline_lines)}

## Compact-To-Baseline Comparisons

{chr(10).join(comparison_lines)}

## Largest Ledger Surfaces

{chr(10).join(largest_lines)}

## Budget Warnings

{chr(10).join(budget_lines)}

## Regression Warnings

{chr(10).join(regression_lines)}

## Uncertainty

These are estimated metadata records only. They do not measure provider billing, exact tokenizer behavior, hidden reasoning tokens, cached-token discounts, or quality outcomes. Q15 must add golden tasks so token reductions can be checked against deterministic quality gates.
"""


def write_token_savings_summary(repo_root: Path, records: list[LedgerRecord], regression: list[str]) -> WriteResult:
    return write_text_if_changed(repo_root / TOKEN_SUMMARY_PATH, render_token_savings_summary(repo_root, records, regression))


def parse_simple_list(text: str, key: str) -> list[str]:
    lines = text.splitlines()
    values: list[str] = []
    in_list = False
    base_indent = 0
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == f"{key}:":
            in_list = True
            base_indent = len(line) - len(line.lstrip())
            continue
        if in_list:
            indent = len(line) - len(line.lstrip())
            if indent <= base_indent and not stripped.startswith("- "):
                break
            if stripped.startswith("- "):
                values.append(stripped[2:].strip().strip('"').strip("'"))
    return values


def parse_int_value(text: str, key: str, default: int) -> int:
    match = re.search(rf"^\s*{re.escape(key)}:\s*(\d+)\s*$", text, re.MULTILINE)
    return int(match.group(1)) if match else default


def load_token_budget(repo_root: Path) -> dict[str, int]:
    path = repo_root / ".aide/policies/token-budget.yaml"
    text = read_text(path) if path.exists() else ""
    return {
        "max_compact_task_packet_tokens": parse_int_value(text, "max_compact_task_packet_tokens", 3200),
        "max_review_packet_tokens": parse_int_value(text, "max_review_packet_tokens", 2400),
        "max_project_state_tokens": parse_int_value(text, "max_project_state_tokens", 1600),
        "max_context_packet_tokens": parse_int_value(text, "max_context_packet_tokens", 2400),
        "max_verification_report_tokens": parse_int_value(text, "max_verification_report_tokens", 2400),
        "max_evidence_packet_tokens": parse_int_value(text, "max_evidence_packet_tokens", 2400),
        "compact_task_packet_target_tokens": parse_int_value(text, "compact_task_packet_target_tokens", 1800),
    }


def load_regression_threshold(repo_root: Path) -> int:
    path = repo_root / TOKEN_LEDGER_POLICY_PATH
    text = read_text(path) if path.exists() else ""
    return parse_int_value(text, "default_warning_threshold_percent", 20)


def detect_surface(path: str) -> str:
    rel = normalize_rel(path)
    if rel == LATEST_PACKET_PATH:
        return "task_packet"
    if rel == LATEST_CONTEXT_PACKET_PATH:
        return "context_packet"
    if rel == REVIEW_PACKET_PATH:
        return "review_packet"
    if rel == LATEST_VERIFICATION_REPORT_PATH:
        return "verification_report"
    if "/evidence/" in rel:
        return "evidence_packet"
    if rel == "AGENTS.md" or rel.startswith(".aide/generated/"):
        return "generated_adapter"
    return "baseline_surface"


def budget_for_surface(repo_root: Path, surface: str) -> int | None:
    budget = load_token_budget(repo_root)
    mapping = {
        "task_packet": budget["max_compact_task_packet_tokens"],
        "context_packet": budget["max_context_packet_tokens"],
        "review_packet": budget["max_review_packet_tokens"],
        "verification_report": budget["max_verification_report_tokens"],
        "evidence_packet": budget["max_evidence_packet_tokens"],
    }
    return mapping.get(surface)


def classify_budget_status(approx_tokens: int, budget: int | None) -> str:
    if not budget or budget <= 0:
        return "unknown_budget"
    if approx_tokens > budget:
        return "over_budget"
    if approx_tokens > int(math.floor(budget * 0.8)):
        return "near_budget"
    return "within_budget"


def ledger_budget_status(repo_root: Path, surface: str, approx_tokens: int) -> tuple[str, str]:
    budget = budget_for_surface(repo_root, surface)
    if budget is None:
        return "unknown", "unknown_budget"
    return str(budget), classify_budget_status(approx_tokens, budget)


def load_ignore_patterns(repo_root: Path) -> list[str]:
    path = repo_root / ".aide/context/ignore.yaml"
    if not path.exists():
        return []
    return parse_simple_list(read_text(path), "exclude")


def pattern_matches(rel_path: str, pattern: str) -> bool:
    rel = normalize_rel(rel_path)
    pattern = pattern.strip()
    if not pattern:
        return False
    if pattern.endswith("/**"):
        base = pattern[:-3].rstrip("/")
        if "/" not in base and not base.startswith("."):
            return base in rel.split("/")
        return rel == base or rel.startswith(base + "/")
    if "/" not in pattern:
        return any(fnmatch.fnmatch(part, pattern) for part in rel.split("/"))
    return fnmatch.fnmatch(rel, pattern)


def is_ignored(rel_path: str, patterns: Iterable[str]) -> bool:
    rel = normalize_rel(rel_path)
    if rel in GENERATED_CONTEXT_PATHS:
        return True
    return any(pattern_matches(rel, pattern) for pattern in patterns)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def coarse_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".py", ".ps1", ".sh", ".bat", ".cmd", ".js", ".ts", ".json", ".yaml", ".yml", ".toml"}:
        return "source-or-config"
    if suffix in {".md", ".txt", ".rst"}:
        return "document"
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".pdf"}:
        return "binary-media"
    if suffix in {".zip", ".tar", ".gz", ".tgz", ".7z", ".rar", ".whl", ".nupkg"}:
        return "archive"
    if suffix in {".exe", ".dll", ".so", ".dylib", ".bin", ".iso", ".dmg", ".msi", ".pkg"}:
        return "binary"
    return "unknown"


def build_snapshot(repo_root: Path) -> dict[str, object]:
    patterns = load_ignore_patterns(repo_root)
    files: list[dict[str, object]] = []
    type_counts: dict[str, int] = {}
    total_size = 0
    for current_root, dirs, filenames in os.walk(repo_root):
        current = Path(current_root)
        rel_dir = normalize_rel(current.relative_to(repo_root)) if current != repo_root else ""
        dirs[:] = sorted(
            dirname
            for dirname in dirs
            if not is_ignored(f"{rel_dir}/{dirname}" if rel_dir else dirname, patterns)
        )
        for filename in sorted(filenames):
            path = current / filename
            rel = normalize_rel(path.relative_to(repo_root))
            if is_ignored(rel, patterns):
                continue
            stat = path.stat()
            kind = coarse_type(path)
            total_size += stat.st_size
            type_counts[kind] = type_counts.get(kind, 0) + 1
            files.append(
                {
                    "path": rel,
                    "size": stat.st_size,
                    "mtime": int(stat.st_mtime),
                    "sha256": sha256_file(path),
                    "extension": path.suffix.lower(),
                    "type": kind,
                }
            )
    files.sort(key=lambda item: str(item["path"]))
    return {
        "schema_version": "aide.repo-snapshot.v0",
        "generator": GENERATOR_NAME,
        "generator_version": GENERATOR_VERSION,
        "contents_inline": False,
        "ignored_patterns": patterns,
        "summary": {
            "file_count": len(files),
            "total_size": total_size,
            "aggregate_approx_tokens": approx_tokens_for_chars(total_size),
            "type_counts": dict(sorted(type_counts.items())),
        },
        "file_count": len(files),
        "files": files,
    }


def write_snapshot(repo_root: Path) -> WriteResult:
    snapshot = build_snapshot(repo_root)
    target = repo_root / SNAPSHOT_PATH
    return write_text_if_changed(target, json.dumps(snapshot, indent=2, sort_keys=True))


def load_snapshot(repo_root: Path) -> dict[str, object]:
    path = repo_root / SNAPSHOT_PATH
    if not path.exists():
        write_snapshot(repo_root)
    return json.loads(read_text(path))


def snapshot_fingerprint(snapshot: dict[str, object]) -> str:
    payload = json.dumps(snapshot, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def classify_role(rel_path: str, coarse: str = "unknown") -> tuple[str, str]:
    rel = normalize_rel(rel_path)
    name = Path(rel).name
    suffix = Path(rel).suffix.lower()
    if rel in {".aide/profile.yaml", ".aide/toolchain.lock"} or rel.startswith(".aide/components/") or rel.startswith(".aide/tasks/") or rel.startswith(".aide/evals/") or rel.startswith(".aide/adapters/") or rel.startswith(".aide/compat/"):
        return "aide_contract", "aide contract/profile path"
    if rel.startswith(".aide/policies/"):
        return "aide_policy", "aide policy path"
    if rel.startswith(".aide/prompts/"):
        return "aide_prompt", "aide prompt path"
    if rel.startswith(".aide/context/"):
        return "aide_context", "aide context path"
    if rel.startswith(".aide/queue/") and "/evidence/" in rel:
        return "aide_evidence", "aide queue evidence path"
    if rel.startswith(".aide/queue/"):
        return "aide_queue", "aide queue path"
    if rel.startswith(".aide/generated/") or rel in GENERATED_CONTEXT_PATHS:
        return "generated", "generated output path"
    if rel.startswith(".aide/scripts/tests/") or "/tests/" in rel or name.startswith("test_") or name.endswith("_test.py"):
        return "test", "test path/name heuristic"
    if rel.startswith("core/harness/"):
        return "harness_code", "core harness path"
    if rel.startswith("core/compat/"):
        return "compat_code", "core compatibility path"
    if rel.startswith("shared/"):
        return "shared_code", "shared implementation path"
    if rel.startswith("docs/") or suffix in {".md", ".rst"}:
        return "docs", "documentation path or extension"
    if rel.startswith("governance/"):
        return "governance", "governance path"
    if rel.startswith("inventory/"):
        return "inventory", "inventory path"
    if rel.startswith("matrices/"):
        return "matrix", "matrix path"
    if rel.startswith("research/"):
        return "research", "research path"
    if rel.startswith("hosts/"):
        return "host", "host path"
    if rel.startswith("bridges/"):
        return "bridge", "bridge path"
    if rel.startswith("scripts/") or rel.startswith(".aide/scripts/"):
        return "script", "script path"
    if coarse == "binary-media" or coarse == "archive" or coarse == "binary":
        return "binary_or_asset", "binary/archive/media type"
    if suffix in {".json", ".yaml", ".yml", ".toml", ".lock", ".ini", ".cfg"}:
        return "config", "configuration extension"
    return "unknown", "no deterministic role heuristic matched"


def generated_classification(rel_path: str) -> str:
    rel = normalize_rel(rel_path)
    if rel in GENERATED_CONTEXT_PATHS or rel.startswith(".aide/generated/"):
        return "generated"
    return "manual"


def priority_for_path(rel_path: str) -> int:
    rel = normalize_rel(rel_path)
    rules = [
        (100, [".aide/profile.yaml"]),
        (95, [".aide/policies/**"]),
        (92, [".aide/prompts/**"]),
        (90, [".aide/context/**"]),
        (88, [".aide/memory/**"]),
        (86, [".aide/queue/index.yaml"]),
        (85, [".aide/queue/Q11-context-compiler-v0/**"]),
        (84, ["AGENTS.md"]),
        (80, ["README.md", "ROADMAP.md", "PLANS.md", "IMPLEMENT.md", "DOCUMENTATION.md"]),
        (76, ["core/harness/**"]),
        (74, ["core/compat/**"]),
        (70, ["shared/**"]),
        (68, ["docs/reference/**"]),
        (64, ["docs/roadmap/**"]),
    ]
    for priority, patterns in rules:
        if any(pattern_matches(rel, pattern) for pattern in patterns):
            return priority
    return 10


def build_repo_map(repo_root: Path) -> dict[str, object]:
    snapshot = load_snapshot(repo_root)
    records: list[dict[str, object]] = []
    role_counts: dict[str, int] = {}
    priority_counts: dict[str, int] = {}
    for entry in snapshot.get("files", []):
        rel = str(entry["path"])
        role, reason = classify_role(rel, str(entry.get("type", "unknown")))
        priority = priority_for_path(rel)
        priority_band = "high" if priority >= 80 else "medium" if priority >= 60 else "normal"
        role_counts[role] = role_counts.get(role, 0) + 1
        priority_counts[priority_band] = priority_counts.get(priority_band, 0) + 1
        records.append(
            {
                "path": rel,
                "hash": entry.get("sha256", ""),
                "size": entry.get("size", 0),
                "extension": entry.get("extension", ""),
                "coarse_type": entry.get("type", "unknown"),
                "role": role,
                "role_reason": reason,
                "priority": priority,
                "priority_band": priority_band,
                "classification": generated_classification(rel),
            }
        )
    records.sort(key=lambda item: (str(item["role"]), str(item["path"])))
    return {
        "schema_version": "aide.repo-map.v0",
        "generator": GENERATOR_NAME,
        "generator_version": GENERATOR_VERSION,
        "contents_inline": False,
        "source_snapshot": SNAPSHOT_PATH,
        "source_snapshot_hash": snapshot_fingerprint(snapshot),
        "summary": {
            "file_count": len(records),
            "role_counts": dict(sorted(role_counts.items())),
            "priority_counts": dict(sorted(priority_counts.items())),
        },
        "files": records,
    }


def render_repo_map_md(repo_map: dict[str, object]) -> str:
    files = list(repo_map.get("files", []))
    summary = repo_map.get("summary", {})
    role_counts = dict(summary.get("role_counts", {})) if isinstance(summary, dict) else {}
    lines = [
        "# AIDE Repo Map",
        "",
        "Generated by AIDE Lite Context Compiler v0. This map contains repo-relative refs and metadata only; it does not inline file contents.",
        "",
        "## Summary",
        "",
        f"- file_count: {summary.get('file_count', len(files)) if isinstance(summary, dict) else len(files)}",
        f"- source_snapshot: `{repo_map.get('source_snapshot', SNAPSHOT_PATH)}`",
        f"- source_snapshot_hash: `{repo_map.get('source_snapshot_hash', '')}`",
        "- contents_inline: false",
        "",
        "## Role Counts",
        "",
    ]
    for role in ROLE_ORDER:
        if role in role_counts:
            lines.append(f"- {role}: {role_counts[role]}")
    lines.extend(["", "## Important Paths", ""])
    for role in ROLE_ORDER:
        role_files = [entry for entry in files if entry.get("role") == role]
        if not role_files:
            continue
        role_files.sort(key=lambda item: (-int(item.get("priority", 0)), str(item.get("path", ""))))
        lines.append(f"### {role}")
        lines.append("")
        for entry in role_files[:12]:
            lines.append(
                f"- `{entry['path']}` (priority {entry['priority']}, {entry['coarse_type']}, {entry['classification']})"
            )
        if len(role_files) > 12:
            lines.append(f"- ... {len(role_files) - 12} more")
        lines.append("")
    return "\n".join(lines)


def write_repo_map(repo_root: Path) -> tuple[WriteResult, WriteResult, dict[str, object]]:
    repo_map = build_repo_map(repo_root)
    json_result = write_text_if_changed(repo_root / REPO_MAP_JSON_PATH, json.dumps(repo_map, indent=2, sort_keys=True))
    md_result = write_text_if_changed(repo_root / REPO_MAP_MD_PATH, render_repo_map_md(repo_map))
    return json_result, md_result, repo_map


def test_record(path: str, exists: bool, kind: str = "file") -> dict[str, object]:
    return {"path": path, "exists": exists, "kind": kind}


def likely_test_candidates(repo_root: Path, source_path: str) -> tuple[list[dict[str, object]], str, str]:
    rel = normalize_rel(source_path)
    stem = Path(rel).stem
    candidates: list[str] = []
    confidence = "low"
    reason = "no direct test heuristic; use structural validation"
    if rel == ".aide/scripts/aide_lite.py":
        candidates = [".aide/scripts/tests/test_aide_lite.py", "core/harness/tests/test_aide_lite.py"]
        confidence = "high"
        reason = "AIDE Lite has direct and Harness-side tests"
    elif rel.startswith("core/harness/") and rel.endswith(".py") and "/tests/" not in rel:
        candidates = [f"core/harness/tests/test_{stem}.py", "core/harness/tests/test_aide_harness.py"]
        confidence = "medium"
        reason = "core/harness module mapped by test_<module> and Harness smoke tests"
    elif rel.startswith("core/compat/") and rel.endswith(".py") and "/tests/" not in rel:
        candidates = [f"core/compat/tests/test_{stem}.py", "core/compat/tests/test_compat_baseline.py"]
        confidence = "medium"
        reason = "core/compat module mapped by test_<module> and compatibility baseline tests"
    elif rel.startswith("shared/") and rel.endswith(".py") and "/tests/" not in rel:
        candidates = [f"shared/tests/test_{stem}.py"]
        confidence = "medium"
        reason = "shared module mapped by shared/tests naming convention"
    elif rel.startswith("scripts/") or rel.endswith(".md") or rel.endswith(".yaml"):
        candidates = ["scripts/aide"]
        confidence = "low"
        reason = "structural Harness validation is the likely check"
    records = [test_record(candidate, (repo_root / candidate).exists()) for candidate in dict.fromkeys(candidates)]
    return records, confidence, reason


def build_test_map(repo_root: Path, repo_map: dict[str, object] | None = None) -> dict[str, object]:
    repo_map = repo_map or build_repo_map(repo_root)
    mappings: list[dict[str, object]] = []
    for entry in repo_map.get("files", []):
        rel = str(entry["path"])
        role = str(entry.get("role", "unknown"))
        if role in {"test", "binary_or_asset", "generated"}:
            continue
        candidates, confidence, reason = likely_test_candidates(repo_root, rel)
        if not candidates and role not in {"harness_code", "compat_code", "shared_code", "script", "docs", "aide_context"}:
            continue
        mappings.append(
            {
                "source": rel,
                "source_role": role,
                "candidate_tests": candidates,
                "confidence": confidence,
                "reason": reason,
                "has_existing_candidate": any(bool(candidate["exists"]) for candidate in candidates),
            }
        )
    mappings.sort(key=lambda item: str(item["source"]))
    return {
        "schema_version": "aide.test-map.v0",
        "generator": GENERATOR_NAME,
        "generator_version": GENERATOR_VERSION,
        "complete_coverage_claimed": False,
        "summary": {
            "mapping_count": len(mappings),
            "with_existing_candidate": sum(1 for item in mappings if item["has_existing_candidate"]),
            "without_existing_candidate": sum(1 for item in mappings if not item["has_existing_candidate"]),
        },
        "mappings": mappings,
    }


def write_test_map(repo_root: Path, repo_map: dict[str, object] | None = None) -> tuple[WriteResult, dict[str, object]]:
    test_map = build_test_map(repo_root, repo_map)
    result = write_text_if_changed(repo_root / TEST_MAP_JSON_PATH, json.dumps(test_map, indent=2, sort_keys=True))
    return result, test_map


def build_context_index(repo_root: Path, repo_map: dict[str, object], test_map: dict[str, object]) -> dict[str, object]:
    return {
        "schema_version": "aide.context-index.v0",
        "generator": GENERATOR_NAME,
        "generator_version": GENERATOR_VERSION,
        "creation_mode": "deterministic-local",
        "contents_inline": False,
        "source_snapshot": SNAPSHOT_PATH,
        "source_snapshot_hash": repo_map.get("source_snapshot_hash", ""),
        "generated_outputs": {
            "repo_map_json": REPO_MAP_JSON_PATH,
            "repo_map_md": REPO_MAP_MD_PATH,
            "test_map_json": TEST_MAP_JSON_PATH,
            "latest_context_packet": LATEST_CONTEXT_PACKET_PATH,
        },
        "counts": {
            "repo_files": repo_map.get("summary", {}).get("file_count", 0),
            "test_mappings": test_map.get("summary", {}).get("mapping_count", 0),
            "test_mappings_with_existing_candidate": test_map.get("summary", {}).get("with_existing_candidate", 0),
        },
        "role_counts": repo_map.get("summary", {}).get("role_counts", {}),
    }


def write_context_index(repo_root: Path, repo_map: dict[str, object], test_map: dict[str, object]) -> tuple[WriteResult, dict[str, object]]:
    context_index = build_context_index(repo_root, repo_map, test_map)
    result = write_text_if_changed(repo_root / CONTEXT_INDEX_PATH, json.dumps(context_index, indent=2, sort_keys=True))
    return result, context_index


def current_queue_ref(repo_root: Path) -> str:
    for queue_id in [
        "Q14-token-ledger-savings-report",
        "Q13-evidence-review-workflow",
        "Q12-verifier-v0",
        "Q11-context-compiler-v0",
        "Q10-aide-lite-hardening",
        "Q09-token-survival-core",
    ]:
        if (repo_root / f".aide/queue/{queue_id}/status.yaml").exists():
            return f".aide/queue/{queue_id}/"
    return ".aide/queue/index.yaml"


def render_context_packet(repo_root: Path, repo_map: dict[str, object], test_map: dict[str, object], context_index: dict[str, object], chars: int = 0, tokens: int = 0) -> str:
    role_counts = context_index.get("role_counts", {})
    role_lines = []
    for role in ROLE_ORDER:
        if role in role_counts:
            role_lines.append(f"- {role}: {role_counts[role]}")
    if not role_lines:
        role_lines.append("- none")
    return f"""# AIDE Latest Context Packet

## CONTEXT_COMPILER

- compiler: q11-context-compiler-v0
- generator: {GENERATOR_NAME}
- generator_version: {GENERATOR_VERSION}
- contents_inline: false
- method: deterministic repo-local metadata, roles, priorities, and test heuristics

## SOURCE_REFS

- `{CONTEXT_COMPILER_CONFIG_PATH}`
- `{CONTEXT_PRIORITY_PATH}`
- `{EXCERPT_POLICY_PATH}`
- `.aide/context/ignore.yaml`
- `{SNAPSHOT_PATH}`
- `.aide/memory/project-state.md`
- `.aide/memory/decisions.md`
- `.aide/memory/open-risks.md`

## REPO_MAP

- json: `{REPO_MAP_JSON_PATH}`
- markdown: `{REPO_MAP_MD_PATH}`
- file_count: {context_index.get('counts', {}).get('repo_files', 0)}
- source_snapshot_hash: `{context_index.get('source_snapshot_hash', '')}`

## ROLE_COUNTS

{chr(10).join(role_lines)}

## TEST_MAP

- path: `{TEST_MAP_JSON_PATH}`
- mapping_count: {test_map.get('summary', {}).get('mapping_count', 0)}
- mappings_with_existing_candidate: {test_map.get('summary', {}).get('with_existing_candidate', 0)}
- complete_coverage_claimed: false

## CURRENT_QUEUE

- current_queue_ref: `{current_queue_ref(repo_root)}`
- queue_index: `.aide/queue/index.yaml`

## EXACT_REFS

- Preferred syntax: `path#Lstart-Lend`
- Validate refs before use.
- Do not inline whole files by default.
- Never inline ignored files, secrets, local state, caches, or binary artifacts.

## PACKET_GUIDANCE

- Use repo-map and test-map refs before broad documentation dumps.
- Include exact line refs only when required for correctness.
- Ask for additional context only when the compact packet is insufficient.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- chars: {chars}
- approx_tokens: {tokens}
- formal ledger: `.aide/reports/token-ledger.jsonl`
"""


def build_context_packet(repo_root: Path, repo_map: dict[str, object], test_map: dict[str, object], context_index: dict[str, object]) -> PacketRender:
    body = render_context_packet(repo_root, repo_map, test_map, context_index)
    for _ in range(5):
        stats = estimate_text(body, LATEST_CONTEXT_PACKET_PATH)
        updated = render_context_packet(repo_root, repo_map, test_map, context_index, stats.chars, stats.approx_tokens)
        if updated == body:
            break
        body = updated
    stats = estimate_text(body, LATEST_CONTEXT_PACKET_PATH)
    return PacketRender(body, stats, "PASS", ())


def write_context_packet(repo_root: Path, repo_map: dict[str, object], test_map: dict[str, object], context_index: dict[str, object]) -> tuple[WriteResult, PacketRender]:
    packet = build_context_packet(repo_root, repo_map, test_map, context_index)
    result = write_text_if_changed(repo_root / LATEST_CONTEXT_PACKET_PATH, packet.text)
    return result, packet


def run_index(repo_root: Path) -> dict[str, object]:
    snapshot_result = write_snapshot(repo_root)
    repo_map_json, repo_map_md, repo_map = write_repo_map(repo_root)
    test_map_result, test_map = write_test_map(repo_root, repo_map)
    context_index_result, context_index = write_context_index(repo_root, repo_map, test_map)
    return {
        "snapshot": snapshot_result,
        "repo_map_json": repo_map_json,
        "repo_map_md": repo_map_md,
        "test_map": test_map_result,
        "context_index": context_index_result,
        "repo_map": repo_map,
        "test_map_data": test_map,
        "context_index_data": context_index,
    }


def run_context(repo_root: Path) -> dict[str, object]:
    index_result = run_index(repo_root)
    context_packet_result, context_packet = write_context_packet(
        repo_root,
        index_result["repo_map"],
        index_result["test_map_data"],
        index_result["context_index_data"],
    )
    index_result["context_packet"] = context_packet_result
    index_result["context_packet_data"] = context_packet
    return index_result


def validate_line_ref(repo_root: Path, ref: str) -> tuple[bool, str]:
    match = re.match(r"^(?P<path>.+)#L(?P<start>\d+)-L(?P<end>\d+)$", ref)
    if not match:
        return False, "line ref must use path#Lstart-Lend"
    rel = normalize_rel(match.group("path"))
    start = int(match.group("start"))
    end = int(match.group("end"))
    if start < 1 or end < start:
        return False, "line range must be positive and ordered"
    try:
        target = safe_repo_path(repo_root, rel)
    except ValueError as exc:
        return False, str(exc)
    if not target.exists() or not target.is_file():
        return False, "line ref target does not exist as a file"
    if is_ignored(rel, load_ignore_patterns(repo_root)):
        return False, "line ref target is ignored"
    if looks_binary(target):
        return False, "line ref target is binary-like"
    line_count = read_text(target).count("\n") + 1
    if end > line_count:
        return False, f"line range exceeds file length: {line_count}"
    return True, "line ref is valid"


def contains_section(text: str, section: str) -> bool:
    return re.search(rf"^##\s+{re.escape(section)}\s*$", text, re.MULTILINE) is not None


def missing_sections(text: str, sections: Iterable[str]) -> list[str]:
    return [section for section in sections if not contains_section(text, section)]


def add_finding(findings: list[VerificationFinding], severity: str, check: str, message: str, path: str = "") -> None:
    findings.append(VerificationFinding(severity.upper(), check, message, normalize_rel(path) if path else ""))


def verification_result(findings: Iterable[VerificationFinding]) -> str:
    severities = {finding.severity.upper() for finding in findings}
    if "ERROR" in severities or "FAIL" in severities:
        return "FAIL"
    if "WARN" in severities or "WARNING" in severities:
        return "WARN"
    return "PASS"


def line_ref_match(ref: str) -> re.Match[str] | None:
    return re.match(r"^(?P<path>.+)#L(?P<start>\d+)-L(?P<end>\d+)$", ref)


def is_external_url(ref: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", ref))


def is_absolute_machine_path(ref: str) -> bool:
    return bool(re.match(r"^[A-Za-z]:[\\/]", ref)) or ref.startswith("/") or ref.startswith("\\\\")


def is_reference_candidate(ref: str) -> bool:
    candidate = ref.strip().strip(".,;:)")
    if not candidate or any(marker in candidate for marker in ["<", ">", "|", "*"]):
        return False
    if " " in candidate or "\t" in candidate:
        return False
    if candidate.startswith(("-", "--")):
        return False
    if line_ref_match(candidate) or is_external_url(candidate) or is_absolute_machine_path(candidate):
        return True
    if "/" in candidate or "\\" in candidate or candidate.startswith("."):
        return True
    suffix = Path(candidate).suffix.lower()
    return suffix in {".md", ".yaml", ".yml", ".json", ".py", ".toml", ".txt", ".ps1", ".sh"}


def clean_reference(ref: str) -> str:
    return ref.strip().strip("`").strip().rstrip(".,;:)")


def extract_file_refs(text: str) -> list[str]:
    refs: list[str] = []
    seen: set[str] = set()
    markdown_targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    backtick_targets = re.findall(r"`([^`\n]+)`", text)
    for raw in [*markdown_targets, *backtick_targets]:
        candidate = clean_reference(raw)
        if "#" in candidate and not line_ref_match(candidate):
            # Markdown anchor refs are not file refs unless they use the exact line syntax.
            continue
        if not is_reference_candidate(candidate):
            continue
        if candidate not in seen:
            refs.append(candidate)
            seen.add(candidate)
    return refs


def validate_file_reference(repo_root: Path, ref: str) -> VerificationFinding:
    clean = clean_reference(ref)
    if is_external_url(clean):
        return VerificationFinding("ERROR", "file_references", "external URL refs are not allowed in Q12 packets", clean)
    if is_absolute_machine_path(clean):
        return VerificationFinding("ERROR", "file_references", "absolute machine path refs are not allowed", clean)
    if line_ref_match(clean):
        ok, message = validate_line_ref(repo_root, clean)
        severity = "INFO" if ok else "ERROR"
        return VerificationFinding(severity, "file_references", message, clean)
    rel = normalize_rel(clean)
    try:
        target = safe_repo_path(repo_root, rel)
    except ValueError as exc:
        return VerificationFinding("ERROR", "file_references", str(exc), rel)
    if rel not in GENERATED_CONTEXT_PATHS and is_ignored(rel, load_ignore_patterns(repo_root)):
        return VerificationFinding("ERROR", "file_references", "ref points at ignored path", rel)
    if not target.exists():
        return VerificationFinding("WARN", "file_references", "referenced path does not exist", rel)
    return VerificationFinding("INFO", "file_references", "referenced path exists", rel)


def verify_refs_in_text(repo_root: Path, text: str, source_path: str) -> list[VerificationFinding]:
    findings: list[VerificationFinding] = []
    for ref in extract_file_refs(text):
        finding = validate_file_reference(repo_root, ref)
        findings.append(
            VerificationFinding(
                finding.severity,
                finding.check,
                f"{finding.message} (from {source_path})",
                finding.path,
            )
        )
    if not findings:
        findings.append(VerificationFinding("INFO", "file_references", f"no conservative file refs found in {source_path}", source_path))
    return findings


def scan_secret_text(text: str, rel_path: str) -> list[VerificationFinding]:
    findings: list[VerificationFinding] = []
    for pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            snippet = match.group(0)
            keyish = snippet.split("=", 1)[0].split(":", 1)[0].strip()
            findings.append(VerificationFinding("ERROR", "secret_scan", f"secret-like value detected near `{keyish}`", rel_path))
    if not findings and SECRET_POLICY_TERM_PATTERN.search(text):
        findings.append(VerificationFinding("INFO", "secret_scan", "policy/token/security terms present without secret-like values", rel_path))
    return findings


def verification_scan_paths(repo_root: Path) -> list[str]:
    candidates = [
        *REQUIRED_FILES,
        *CONTEXT_CONFIG_FILES,
        *CONTEXT_OUTPUT_PATHS,
        *Q12_REQUIRED_FILES,
        LATEST_PACKET_PATH,
        LATEST_CONTEXT_PACKET_PATH,
        "AGENTS.md",
        "README.md",
        "ROADMAP.md",
        "PLANS.md",
        "IMPLEMENT.md",
        "DOCUMENTATION.md",
        ".aide/scripts/aide_lite.py",
    ]
    seen: set[str] = set()
    existing: list[str] = []
    for rel in candidates:
        if rel in seen:
            continue
        seen.add(rel)
        if (repo_root / rel).exists():
            existing.append(rel)
    return existing


def scan_for_secret_findings(repo_root: Path, paths: Iterable[str]) -> list[VerificationFinding]:
    findings: list[VerificationFinding] = []
    for rel in paths:
        path = repo_root / rel
        if not path.exists() or not path.is_file():
            continue
        try:
            if looks_binary(path):
                continue
            findings.extend(scan_secret_text(read_text(path), rel))
        except (OSError, UnicodeDecodeError):
            findings.append(VerificationFinding("WARN", "secret_scan", "could not read file for secret scan", rel))
    return findings


def active_scope_task_path(repo_root: Path) -> Path | None:
    for queue_id in ["Q14-token-ledger-savings-report", "Q13-evidence-review-workflow", "Q12-verifier-v0"]:
        preferred = repo_root / f".aide/queue/{queue_id}/task.yaml"
        if preferred.exists():
            return preferred
    index = repo_root / ".aide/queue/index.yaml"
    if not index.exists():
        return None
    text = read_text(index)
    blocks = re.split(r"\n\s*-\s+id:\s+", "\n" + text)
    for block in reversed(blocks):
        if "status: active" in block:
            match = re.search(r"task:\s*(\S+)", block)
            if match:
                candidate = repo_root / match.group(1)
                if candidate.exists():
                    return candidate
    return None


def load_scope_patterns(repo_root: Path) -> tuple[list[str], list[str]]:
    task_path = active_scope_task_path(repo_root)
    if task_path and task_path.exists():
        text = read_text(task_path)
        allowed = parse_simple_list(text, "allowed_paths")
        forbidden = parse_simple_list(text, "forbidden_paths")
    else:
        allowed = []
        forbidden = []
    if not allowed:
        allowed = [
            ".aide/queue/Q14-token-ledger-savings-report/**",
            ".aide/queue/Q13-evidence-review-workflow/**",
            ".aide/queue/Q12-verifier-v0/**",
            ".aide/scripts/**",
            ".aide/reports/**",
            ".aide/policies/token-ledger.yaml",
            ".aide/verification/**",
            ".aide/policies/verification.yaml",
            ".aide/context/**",
            "AGENTS.md",
            "README.md",
            "ROADMAP.md",
            "PLANS.md",
            "IMPLEMENT.md",
            "DOCUMENTATION.md",
            "docs/reference/**",
            "docs/roadmap/**",
            "core/harness/**",
        ]
    if not forbidden:
        forbidden = [".git/**", ".env", "secrets/**", ".aide.local/**"]
    return allowed, forbidden


def classify_scope_path(rel_path: str, status: str, allowed: Iterable[str], forbidden: Iterable[str]) -> DiffScopeResult:
    rel = normalize_rel(rel_path)
    if any(pattern_matches(rel, pattern) for pattern in forbidden):
        return DiffScopeResult(status, rel, "forbidden", "matches forbidden path policy")
    if status.strip().startswith("D"):
        return DiffScopeResult(status, rel, "warning", "deleted path requires review")
    if any(pattern_matches(rel, pattern) for pattern in allowed):
        return DiffScopeResult(status, rel, "allowed", "matches active task allowed path")
    return DiffScopeResult(status, rel, "unknown", "does not match active task allowed paths")


def git_status_short(repo_root: Path) -> tuple[bool, list[tuple[str, str]], str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--short"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except OSError as exc:
        return False, [], str(exc)
    if result.returncode != 0:
        return False, [], result.stderr.strip() or "git status failed"
    entries: list[tuple[str, str]] = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        status = line[:2]
        path_part = line[3:] if len(line) > 3 else ""
        if " -> " in path_part:
            old, new = path_part.split(" -> ", 1)
            entries.append((status, old.strip().strip('"')))
            entries.append((status, new.strip().strip('"')))
        else:
            entries.append((status, path_part.strip().strip('"')))
    return True, entries, ""


def classify_changed_files(repo_root: Path) -> tuple[list[DiffScopeResult], list[VerificationFinding]]:
    ok, entries, error = git_status_short(repo_root)
    findings: list[VerificationFinding] = []
    if not ok:
        return [], [VerificationFinding("WARN", "diff_scope", f"git status unavailable: {error}")]
    allowed, forbidden = load_scope_patterns(repo_root)
    results = [classify_scope_path(path, status, allowed, forbidden) for status, path in entries]
    for result in results:
        if result.classification == "forbidden":
            findings.append(VerificationFinding("ERROR", "diff_scope", result.reason, result.path))
        elif result.classification in {"warning", "unknown"}:
            findings.append(VerificationFinding("WARN", "diff_scope", result.reason, result.path))
        else:
            findings.append(VerificationFinding("INFO", "diff_scope", result.reason, result.path))
    if not results:
        findings.append(VerificationFinding("INFO", "diff_scope", "no changed files reported by git status"))
    return results, findings


def verify_markdown_sections(text: str, sections: Iterable[str], source_path: str, check: str) -> list[VerificationFinding]:
    findings: list[VerificationFinding] = []
    for section in missing_sections(text, sections):
        findings.append(VerificationFinding("ERROR", check, f"missing required section: {section}", source_path))
    if not findings:
        findings.append(VerificationFinding("INFO", check, "required sections present", source_path))
    return findings


def verify_task_packet(repo_root: Path, rel_path: str) -> list[VerificationFinding]:
    findings: list[VerificationFinding] = []
    path = safe_repo_path(repo_root, rel_path)
    if not path.exists():
        return [VerificationFinding("ERROR", "task_packet", "task packet does not exist", rel_path)]
    text = read_text(path)
    findings.extend(verify_markdown_sections(text, PACKET_REQUIRED_SECTIONS, rel_path, "task_packet"))
    for phrase in FORBIDDEN_PACKET_PHRASES:
        if phrase.lower() in text.lower():
            findings.append(VerificationFinding("WARN", "task_packet", f"forbidden prompt pattern mentioned: {phrase}", rel_path))
    for required_ref in [REPO_MAP_JSON_PATH, TEST_MAP_JSON_PATH, CONTEXT_INDEX_PATH, LATEST_CONTEXT_PACKET_PATH]:
        if required_ref not in text:
            findings.append(VerificationFinding("WARN", "task_packet", f"context ref missing: {required_ref}", rel_path))
    budget = load_token_budget(repo_root)
    stats = estimate_text(text, rel_path)
    if stats.approx_tokens > budget["max_compact_task_packet_tokens"]:
        findings.append(VerificationFinding("WARN", "task_packet", f"task packet over hard limit: {stats.approx_tokens}", rel_path))
    else:
        findings.append(VerificationFinding("INFO", "task_packet", f"task packet tokens: {stats.approx_tokens}", rel_path))
    findings.extend(verify_refs_in_text(repo_root, text, rel_path))
    return findings


def verify_evidence_packet(repo_root: Path, rel_path: str) -> list[VerificationFinding]:
    findings: list[VerificationFinding] = []
    path = safe_repo_path(repo_root, rel_path)
    if not path.exists():
        return [VerificationFinding("ERROR", "evidence_packet", "evidence packet does not exist", rel_path)]
    text = read_text(path)
    findings.extend(verify_markdown_sections(text, EVIDENCE_PACKET_REQUIRED_SECTIONS, rel_path, "evidence_packet"))
    if "Validation Commands" in text and not re.search(r"py -3|python|git\s+|rg\s+", text):
        findings.append(VerificationFinding("WARN", "evidence_packet", "validation commands section may not record commands", rel_path))
    if "Changed Files" in text and not re.search(r"`[^`]+\.(md|yaml|yml|json|py|toml|txt)`", text):
        findings.append(VerificationFinding("WARN", "evidence_packet", "changed files section may not list repo-relative files", rel_path))
    findings.extend(verify_refs_in_text(repo_root, text, rel_path))
    return findings


def verify_context_shape(repo_root: Path) -> list[VerificationFinding]:
    findings: list[VerificationFinding] = []
    for rel in CONTEXT_OUTPUT_PATHS:
        if not (repo_root / rel).exists():
            findings.append(VerificationFinding("WARN", "context_packet_shape", "context artifact missing", rel))
    packet_path = repo_root / LATEST_CONTEXT_PACKET_PATH
    if packet_path.exists():
        text = read_text(packet_path)
        missing = missing_sections(text, CONTEXT_PACKET_REQUIRED_SECTIONS)
        for section in missing:
            findings.append(VerificationFinding("WARN", "context_packet_shape", f"latest context packet missing section: {section}", LATEST_CONTEXT_PACKET_PATH))
        if any(marker in text for marker in CONTEXT_FORBIDDEN_INLINE_MARKERS):
            findings.append(VerificationFinding("ERROR", "context_packet_shape", "latest context packet appears to inline raw source marker", LATEST_CONTEXT_PACKET_PATH))
        findings.append(VerificationFinding("INFO", "context_packet_shape", f"latest context packet tokens: {estimate_text(text).approx_tokens}", LATEST_CONTEXT_PACKET_PATH))
    return findings


def collect_verification_findings(
    repo_root: Path,
    evidence_path: str | None = None,
    task_packet_path: str | None = None,
    review_packet_path: str | None = None,
    changed_files_only: bool = False,
) -> tuple[list[VerificationFinding], list[DiffScopeResult], list[str]]:
    findings: list[VerificationFinding] = []
    checked_files: list[str] = []

    if not changed_files_only:
        for rel in [*REQUIRED_FILES, *CONTEXT_CONFIG_FILES, *Q12_REQUIRED_FILES]:
            checked_files.append(rel)
            if (repo_root / rel).exists():
                findings.append(VerificationFinding("INFO", "required_files", "required file exists", rel))
            else:
                findings.append(VerificationFinding("ERROR", "required_files", "required file missing", rel))
        task_rel = task_packet_path or LATEST_PACKET_PATH
        checked_files.append(task_rel)
        findings.extend(verify_task_packet(repo_root, task_rel))
        if evidence_path:
            checked_files.append(evidence_path)
            findings.extend(verify_evidence_packet(repo_root, evidence_path))
        review_rel = review_packet_path
        if review_rel is None and (repo_root / REVIEW_PACKET_PATH).exists():
            review_rel = REVIEW_PACKET_PATH
        if review_rel:
            checked_files.append(review_rel)
            findings.extend(verify_review_packet(repo_root, review_rel))
        findings.extend(verify_context_shape(repo_root))
        adapter = adapter_status(repo_root)
        if adapter.status == "current":
            findings.append(VerificationFinding("INFO", "adapter_drift", "AGENTS managed section is current", "AGENTS.md"))
        elif adapter.status in {"missing", "legacy", "drift"}:
            findings.append(VerificationFinding("WARN", "adapter_drift", f"AGENTS managed section status: {adapter.status}; {adapter.action_hint}", "AGENTS.md"))
        else:
            findings.append(VerificationFinding("ERROR", "adapter_drift", f"AGENTS managed section status: {adapter.status}; {adapter.action_hint}", "AGENTS.md"))
        scan_paths = verification_scan_paths(repo_root)
        checked_files.extend(scan_paths)
        findings.extend(scan_for_secret_findings(repo_root, scan_paths))

    changed_files, diff_findings = classify_changed_files(repo_root)
    findings.extend(diff_findings)
    return findings, changed_files, sorted(set(checked_files))


def render_verification_report(report: VerificationReport) -> str:
    counts = {
        "info": sum(1 for finding in report.findings if finding.severity == "INFO"),
        "warning": sum(1 for finding in report.findings if finding.severity in {"WARN", "WARNING"}),
        "error": sum(1 for finding in report.findings if finding.severity in {"ERROR", "FAIL"}),
    }
    warnings = [finding for finding in report.findings if finding.severity in {"WARN", "WARNING"}]
    errors = [finding for finding in report.findings if finding.severity in {"ERROR", "FAIL"}]
    lines = [
        "# AIDE Verification Report",
        "",
        "## VERIFIER_RESULT",
        "",
        f"- result: {report.result}",
        "- method: deterministic repo-local checks",
        "- contents_inline: false",
        "- provider_or_model_calls: none",
        "",
        "## CHECK_COUNTS",
        "",
        f"- info: {counts['info']}",
        f"- warnings: {counts['warning']}",
        f"- errors: {counts['error']}",
        f"- checked_files: {len(report.checked_files)}",
        f"- changed_files: {len(report.changed_files)}",
        "",
        "## CHANGED_FILES",
        "",
    ]
    if report.changed_files:
        for item in report.changed_files:
            lines.append(f"- {item.classification}: `{item.path}` ({item.status.strip() or 'clean'}; {item.reason})")
    else:
        lines.append("- none")
    lines.extend(["", "## WARNINGS", ""])
    if warnings:
        for finding in warnings:
            suffix = f" `{finding.path}`" if finding.path else ""
            lines.append(f"- {finding.check}: {finding.message}{suffix}")
    else:
        lines.append("- none")
    lines.extend(["", "## ERRORS", ""])
    if errors:
        for finding in errors:
            suffix = f" `{finding.path}`" if finding.path else ""
            lines.append(f"- {finding.check}: {finding.message}{suffix}")
    else:
        lines.append("- none")
    lines.extend(["", "## EVIDENCE_REFS", ""])
    for rel in report.checked_files[:80]:
        lines.append(f"- `{rel}`")
    if len(report.checked_files) > 80:
        lines.append(f"- omitted_refs: {len(report.checked_files) - 80}")
    lines.extend([
        "",
        "## LIMITS",
        "",
        "- Structural verifier only; no LLM judging.",
        "- Diff scope is path-based only.",
        "- Secret scan is heuristic only.",
        "- Token counts use chars / 4 approximation.",
        "",
    ])
    return "\n".join(lines)


def build_verification_report(
    repo_root: Path,
    evidence_path: str | None = None,
    task_packet_path: str | None = None,
    review_packet_path: str | None = None,
    changed_files_only: bool = False,
) -> VerificationReport:
    findings, changed_files, checked_files = collect_verification_findings(
        repo_root,
        evidence_path=evidence_path,
        task_packet_path=task_packet_path,
        review_packet_path=review_packet_path,
        changed_files_only=changed_files_only,
    )
    return VerificationReport(
        verification_result(findings),
        tuple(findings),
        tuple(checked_files),
        tuple(changed_files),
    )


def write_verification_report(repo_root: Path, requested: str, report: VerificationReport) -> WriteResult:
    target = safe_repo_path(repo_root, requested)
    rel = normalize_rel(target.relative_to(repo_root))
    allowed_report_path = rel.startswith(".aide/verification/") or rel.startswith(".aide/queue/")
    forbidden_report_path = any(pattern_matches(rel, pattern) for pattern in [".git/**", ".aide.local/**", "secrets/**", ".env"])
    if not allowed_report_path or forbidden_report_path:
        raise ValueError(f"verification report path is not allowed: {requested}")
    return write_text_if_changed(target, render_verification_report(report))


def current_queue_id(repo_root: Path) -> str:
    for queue_id in [
        "Q14-token-ledger-savings-report",
        "Q13-evidence-review-workflow",
        "Q12-verifier-v0",
        "Q11-context-compiler-v0",
        "Q10-aide-lite-hardening",
        "Q09-token-survival-core",
    ]:
        if (repo_root / f".aide/queue/{queue_id}/status.yaml").exists():
            return queue_id
    return ""


def default_evidence_dir(repo_root: Path) -> str:
    queue_id = current_queue_id(repo_root)
    return f".aide/queue/{queue_id}/evidence" if queue_id else ".aide/queue"


def default_review_task_packet(repo_root: Path) -> str:
    queue_id = current_queue_id(repo_root)
    candidate = f".aide/queue/{queue_id}/task.yaml" if queue_id else ""
    if candidate and (repo_root / candidate).exists():
        return candidate
    return LATEST_PACKET_PATH


def list_evidence_refs(repo_root: Path, evidence_dir: str) -> list[str]:
    directory = safe_repo_path(repo_root, evidence_dir)
    if not directory.exists() or not directory.is_dir():
        return []
    refs = [
        normalize_rel(path.relative_to(repo_root))
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".json"}
    ]
    return sorted(refs)


def compact_bullet_lines(text: str, limit: int = 20) -> list[str]:
    bullets: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped)
        if len(bullets) >= limit:
            break
    return bullets


def summarize_validation(repo_root: Path, evidence_dir: str) -> list[str]:
    path = safe_repo_path(repo_root, f"{evidence_dir.rstrip('/')}/validation.md")
    if not path.exists():
        return ["- validation evidence not found"]
    text = read_text(path)
    if "## Final Validation" in text:
        text = text.split("## Final Validation", 1)[1]
    bullets = compact_bullet_lines(text, limit=14)
    return bullets or ["- validation evidence contains no compact command bullets"]


def summarize_risks(repo_root: Path, evidence_dir: str) -> list[str]:
    risk_path = safe_repo_path(repo_root, f"{evidence_dir.rstrip('/')}/remaining-risks.md")
    if risk_path.exists():
        bullets = compact_bullet_lines(read_text(risk_path), limit=18)
        if bullets:
            return bullets
    open_risks = repo_root / ".aide/memory/open-risks.md"
    if open_risks.exists():
        bullets = compact_bullet_lines(read_text(open_risks), limit=18)
        if bullets:
            return bullets
    return ["- no compact risk bullets found; reviewer should inspect evidence refs"]


def extract_verification_result(repo_root: Path, verification_path: str) -> str:
    path = safe_repo_path(repo_root, verification_path)
    if not path.exists():
        return "MISSING"
    text = read_text(path)
    match = re.search(r"^-\s*result:\s*(PASS|WARN|FAIL)\s*$", text, re.MULTILINE)
    return match.group(1) if match else "UNKNOWN"


def changed_file_summary(repo_root: Path) -> list[str]:
    changed_files, _findings = classify_changed_files(repo_root)
    if not changed_files:
        return ["- none"]
    lines = []
    sorted_files = sorted(changed_files, key=lambda entry: entry.path)
    limit = 24
    for item in sorted_files[:limit]:
        lines.append(f"- {item.classification}: `{item.path}` ({item.status.strip() or 'clean'}; {item.reason})")
    remaining = len(sorted_files) - limit
    if remaining > 0:
        lines.append(f"- additional changed paths omitted from compact packet: {remaining}; see task evidence changed-files report")
    return lines


def non_goal_lines(repo_root: Path) -> list[str]:
    queue_id = current_queue_id(repo_root)
    task_path = repo_root / f".aide/queue/{queue_id}/task.yaml" if queue_id else repo_root / ".aide/queue/index.yaml"
    if task_path.exists():
        items = parse_simple_list(read_text(task_path), "non_goals")
        if items:
            return [f"- {item}" for item in items[:24]]
    return [
        "- Gateway",
        "- provider calls",
        "- model routing",
        "- Runtime/Service/Commander/UI/Mobile",
        "- MCP/A2A",
        "- automatic model calls or repair",
    ]


def review_packet_budget_warnings(text: str, repo_root: Path, max_token_warning: int | None = None) -> tuple[str, tuple[str, ...]]:
    stats = estimate_text(text, REVIEW_PACKET_PATH)
    budget = load_token_budget(repo_root)
    limit = max_token_warning or budget["max_review_packet_tokens"]
    warnings: list[str] = []
    if stats.approx_tokens > limit:
        warnings.append(f"review packet over warning limit: {stats.approx_tokens} > {limit}")
    lowered = text.lower()
    for phrase in FORBIDDEN_PACKET_PHRASES:
        if phrase.lower() in lowered:
            warnings.append(f"forbidden prompt phrase appears in review packet: {phrase}")
    return ("WARN" if warnings else "PASS", tuple(warnings))


def render_review_packet(
    repo_root: Path,
    task_packet_path: str | None = None,
    verification_path: str = LATEST_VERIFICATION_REPORT_PATH,
    evidence_dir: str | None = None,
    output_path: str = REVIEW_PACKET_PATH,
    chars: int = 0,
    tokens: int = 0,
    budget_status: str = "PENDING",
    warnings: Iterable[str] = (),
    max_token_warning: int | None = None,
) -> str:
    task_packet_path = task_packet_path or default_review_task_packet(repo_root)
    evidence_dir = evidence_dir or default_evidence_dir(repo_root)
    evidence_refs = list_evidence_refs(repo_root, evidence_dir)
    evidence_lines = [f"- `{ref}`" for ref in evidence_refs] or [f"- `{evidence_dir}` (missing or empty)"]
    validation_lines = summarize_validation(repo_root, evidence_dir)
    risk_lines = summarize_risks(repo_root, evidence_dir)
    changed_lines = changed_file_summary(repo_root)
    verifier_result = extract_verification_result(repo_root, verification_path)
    task_stats = estimate_file(repo_root, task_packet_path) if (repo_root / task_packet_path).exists() else TextStats(task_packet_path, 0, 0, 0)
    context_stats = estimate_file(repo_root, LATEST_CONTEXT_PACKET_PATH) if (repo_root / LATEST_CONTEXT_PACKET_PATH).exists() else TextStats(LATEST_CONTEXT_PACKET_PATH, 0, 0, 0)
    verification_stats = estimate_file(repo_root, verification_path) if (repo_root / verification_path).exists() else TextStats(verification_path, 0, 0, 0)
    warning_lines = "\n".join(f"- {warning}" for warning in warnings) or "- none"
    non_goals = "\n".join(non_goal_lines(repo_root))
    return f"""# AIDE Latest Review Packet

## Review Objective

Review the current AIDE queue phase from compact evidence only and decide whether it is ready to pass its review gate.

## Decision Requested

Return exactly one of `PASS`, `PASS_WITH_NOTES`, `REQUEST_CHANGES`, or `BLOCKED`.

## Task Packet Reference

- `{task_packet_path}` ({task_stats.chars} chars, {task_stats.approx_tokens} approximate tokens)

## Context Packet Reference

- `{LATEST_CONTEXT_PACKET_PATH}` ({context_stats.chars} chars, {context_stats.approx_tokens} approximate tokens)
- `{REPO_MAP_JSON_PATH}`
- `{TEST_MAP_JSON_PATH}`
- `{CONTEXT_INDEX_PATH}`

## Verification Report Reference

- `{verification_path}`
- verifier_result: {verifier_result}
- report_chars: {verification_stats.chars}
- report_approx_tokens: {verification_stats.approx_tokens}

## Evidence Packet References

{chr(10).join(evidence_lines)}

## Changed Files Summary

{chr(10).join(changed_lines)}

## Validation Summary

{chr(10).join(validation_lines)}

## Token Summary

- packet_path: `{output_path}`
- method: chars / 4, rounded up
- chars: {chars}
- approx_tokens: {tokens}
- budget_status: {budget_status}
- max_token_warning: {max_token_warning or load_token_budget(repo_root)['max_review_packet_tokens']}
- warnings:
{warning_lines}
- formal ledger: `.aide/reports/token-ledger.jsonl`

## Risk Summary

{chr(10).join(risk_lines)}

## Non-Goals / Scope Guard

{non_goals}

## Reviewer Instructions

- Review only this packet and the referenced evidence when needed.
- Do not request full chat history unless the packet is insufficient to judge correctness.
- Do not re-summarize the whole project.
- Do not reward scope creep.
- Do not approve missing validation as a pass.
- Required output sections: `DECISION`, `REASONS`, `REQUIRED_FIXES`, `OPTIONAL_NOTES`, `NEXT_PHASE`.
- Decision policy: `.aide/verification/review-decision-policy.yaml`.
"""


def build_review_packet(
    repo_root: Path,
    task_packet_path: str | None = None,
    verification_path: str = LATEST_VERIFICATION_REPORT_PATH,
    evidence_dir: str | None = None,
    output_path: str = REVIEW_PACKET_PATH,
    max_token_warning: int | None = None,
) -> PacketRender:
    body = render_review_packet(
        repo_root,
        task_packet_path=task_packet_path,
        verification_path=verification_path,
        evidence_dir=evidence_dir,
        output_path=output_path,
        max_token_warning=max_token_warning,
    )
    for _ in range(5):
        stats = estimate_text(body, output_path)
        budget_status, warnings = review_packet_budget_warnings(body, repo_root, max_token_warning=max_token_warning)
        updated = render_review_packet(
            repo_root,
            task_packet_path=task_packet_path,
            verification_path=verification_path,
            evidence_dir=evidence_dir,
            output_path=output_path,
            chars=stats.chars,
            tokens=stats.approx_tokens,
            budget_status=budget_status,
            warnings=warnings,
            max_token_warning=max_token_warning,
        )
        if updated == body:
            break
        body = updated
    stats = estimate_text(body, output_path)
    budget_status, warnings = review_packet_budget_warnings(body, repo_root, max_token_warning=max_token_warning)
    return PacketRender(body, stats, budget_status, warnings)


def write_review_packet(
    repo_root: Path,
    task_packet_path: str | None = None,
    verification_path: str = LATEST_VERIFICATION_REPORT_PATH,
    evidence_dir: str | None = None,
    output_path: str = REVIEW_PACKET_PATH,
    max_token_warning: int | None = None,
) -> tuple[WriteResult, PacketRender]:
    target = safe_repo_path(repo_root, output_path)
    rel = normalize_rel(target.relative_to(repo_root))
    allowed = rel.startswith(".aide/context/") or rel.startswith(".aide/queue/")
    forbidden = any(pattern_matches(rel, pattern) for pattern in [".git/**", ".aide.local/**", "secrets/**", ".env"])
    if not allowed or forbidden:
        raise ValueError(f"review packet output path is not allowed: {output_path}")
    packet = build_review_packet(
        repo_root,
        task_packet_path=task_packet_path,
        verification_path=verification_path,
        evidence_dir=evidence_dir,
        output_path=rel,
        max_token_warning=max_token_warning,
    )
    return write_text_if_changed(target, packet.text), packet


def verify_review_packet(repo_root: Path, rel_path: str) -> list[VerificationFinding]:
    findings: list[VerificationFinding] = []
    path = safe_repo_path(repo_root, rel_path)
    if not path.exists():
        return [VerificationFinding("ERROR", "review_packet", "review packet does not exist", rel_path)]
    text = read_text(path)
    findings.extend(verify_markdown_sections(text, REVIEW_PACKET_REQUIRED_SECTIONS, rel_path, "review_packet"))
    if len(re.findall(r"^##\s+Decision Requested\s*$", text, re.MULTILINE)) != 1:
        findings.append(VerificationFinding("ERROR", "review_packet", "must contain exactly one Decision Requested section", rel_path))
    if not all(decision in text for decision in ["PASS", "PASS_WITH_NOTES", "REQUEST_CHANGES", "BLOCKED"]):
        findings.append(VerificationFinding("ERROR", "review_packet", "decision request does not list all allowed decisions", rel_path))
    lowered = text.lower()
    for phrase in FORBIDDEN_PACKET_PHRASES:
        if phrase.lower() in lowered:
            findings.append(VerificationFinding("WARN", "review_packet", f"forbidden prompt pattern mentioned: {phrase}", rel_path))
    for marker in CONTEXT_FORBIDDEN_INLINE_MARKERS:
        if marker in text:
            findings.append(VerificationFinding("ERROR", "review_packet", "review packet appears to inline raw source marker", rel_path))
    budget = load_token_budget(repo_root)
    stats = estimate_text(text, rel_path)
    if stats.approx_tokens > budget["max_review_packet_tokens"]:
        findings.append(VerificationFinding("WARN", "review_packet", f"review packet over hard limit: {stats.approx_tokens}", rel_path))
    else:
        findings.append(VerificationFinding("INFO", "review_packet", f"review packet tokens: {stats.approx_tokens}", rel_path))
    for required_ref in [LATEST_CONTEXT_PACKET_PATH, LATEST_VERIFICATION_REPORT_PATH, REVIEW_DECISION_POLICY_PATH]:
        if required_ref not in text:
            findings.append(VerificationFinding("WARN", "review_packet", f"review ref missing: {required_ref}", rel_path))
    findings.extend(verify_refs_in_text(repo_root, text, rel_path))
    return findings


def agents_body() -> str:
    return """## Q14 Token, Context, Verifier, Review, And Ledger Guidance

- Use `.aide/context/latest-task-packet.md` when present instead of pasting long chat history.
- Use `.aide/context/latest-context-packet.md`, repo-map refs, test-map refs, compact project memory, and evidence packets before broad context dumps.
- Do not paste full prior transcripts, whole repo dumps, repeated roadmap dumps, secrets, provider keys, local caches, or raw prompt logs.
- Emit deltas and compact final reports with status, changed files, validation, evidence, risks, and next step.
- Generate `.aide/context/latest-review-packet.md` with `review-pack` before premium-model review.
- Run `ledger scan`, `ledger report`, and `ledger compare` for token-ledger work, and do not store raw prompts or raw responses in committed ledger records.
- Review compact review packets and verifier output only by default; ask for more context only when the packet is insufficient.
- Run `py -3 .aide/scripts/aide_lite.py doctor`, `validate`, `snapshot`, `index`, `context`, `pack`, `estimate`, `verify`, `review-pack`, `ledger`, `adapt`, and `selftest` for token/context/verifier/review/ledger work.
- Prefer exact refs such as `path#Lstart-Lend`; do not inline whole files by default.
- Treat token savings as invalid when validation, quality evidence, provenance, or review gates are weakened.
- Commit coherent subdeliverables with verbose bodies when queue work changes repo state.
"""


def render_agents_section() -> str:
    body = normalize_text(agents_body())
    fingerprint = sha256_text(body)
    start = (
        f"{AGENTS_BEGIN} generator={GENERATOR_NAME} version={GENERATOR_VERSION} "
        f"mode=managed-section fingerprint=sha256:{fingerprint} manual=outside-only -->"
    )
    return f"{start}\n{body}{AGENTS_END}\n"


def _managed_match(text: str) -> re.Match[str] | None:
    pattern = re.compile(
        rf"<!-- AIDE-GENERATED:BEGIN section={re.escape(AGENTS_SECTION)} (?P<meta>.*?) -->\n(?P<body>.*?)"
        rf"<!-- AIDE-GENERATED:END section={re.escape(AGENTS_SECTION)} -->",
        re.DOTALL,
    )
    return pattern.search(text)


def _legacy_bounds(text: str) -> tuple[int, int] | None:
    if LEGACY_AGENTS_BEGIN not in text:
        return None
    start = text.index(LEGACY_AGENTS_BEGIN)
    try:
        end = text.index(LEGACY_AGENTS_END, start) + len(LEGACY_AGENTS_END)
    except ValueError:
        return (start, len(text))
    return (start, end)


def adapter_status(repo_root: Path) -> AdapterStatus:
    target = repo_root / "AGENTS.md"
    if not target.exists():
        return AdapterStatus("missing-target", "restore AGENTS.md before adapting", False, False)
    text = read_text(target)
    expected_body = normalize_text(agents_body())
    match = _managed_match(text)
    if match:
        body = normalize_text(match.group("body"))
        body_matches = body == expected_body
        fingerprint = re.search(r"fingerprint=sha256:([0-9a-f]{64})", match.group("meta"))
        fingerprint_matches = bool(fingerprint and fingerprint.group(1) == sha256_text(body))
        if body_matches and fingerprint_matches:
            return AdapterStatus("current", "no action needed", True, True)
        return AdapterStatus("drift", "run adapt to replace managed section", body_matches, fingerprint_matches)
    if _legacy_bounds(text):
        return AdapterStatus("legacy", "run adapt to replace legacy Q09 marker", False, False)
    return AdapterStatus("missing", "run adapt to append managed section", False, False)


def adapt_agents(repo_root: Path) -> tuple[WriteResult, AdapterStatus, AdapterStatus]:
    target = repo_root / "AGENTS.md"
    existing = read_text(target) if target.exists() else ""
    before = adapter_status(repo_root) if target.exists() else AdapterStatus("missing-target", "restore AGENTS.md", False, False)
    section = render_agents_section().rstrip()
    match = _managed_match(existing)
    if match:
        updated = existing[: match.start()] + section + existing[match.end() :]
    else:
        legacy = _legacy_bounds(existing)
        if legacy:
            start, end = legacy
            updated = existing[:start] + section + existing[end:]
        else:
            updated = existing.rstrip() + "\n\n" + section if existing.strip() else section
    result = write_text_if_changed(target, updated)
    after = adapter_status(repo_root)
    if before.status == "missing" and result.action == "written":
        result = WriteResult(target, "appended")
    elif before.status in {"legacy", "drift"} and result.action == "written":
        result = WriteResult(target, "replaced")
    return result, before, after


def has_token_guidance(repo_root: Path) -> bool:
    return adapter_status(repo_root).status == "current"


def infer_phase(task_text: str) -> tuple[str, str]:
    cleaned = task_text.strip()
    match = re.search(r"\b(Q\d{2})\b\s*[-:—]?\s*(.*)", cleaned)
    if not match:
        return "UNSPECIFIED", cleaned or "Compact task"
    phase = match.group(1)
    title = match.group(2).strip()
    title = re.sub(r"^(Implement|Review|Plan)\s+", "", title, flags=re.IGNORECASE).strip()
    return phase, title or "Compact task"


def packet_budget_warnings(text: str, repo_root: Path) -> tuple[str, tuple[str, ...]]:
    stats = estimate_text(text, LATEST_PACKET_PATH)
    budget = load_token_budget(repo_root)
    warnings: list[str] = []
    if stats.approx_tokens > budget["max_compact_task_packet_tokens"]:
        warnings.append(
            f"compact task packet over hard limit: {stats.approx_tokens} > {budget['max_compact_task_packet_tokens']}"
        )
    elif stats.approx_tokens > budget["compact_task_packet_target_tokens"]:
        warnings.append(
            f"compact task packet over target: {stats.approx_tokens} > {budget['compact_task_packet_target_tokens']}"
        )
    lowered = text.lower()
    for phrase in FORBIDDEN_PACKET_PHRASES:
        if phrase.lower() in lowered:
            warnings.append(f"forbidden prompt phrase appears in generated packet: {phrase}")
    return ("WARN" if warnings else "PASS", tuple(warnings))


def render_task_packet(repo_root: Path, task_text: str, chars: int = 0, tokens: int = 0, budget_status: str = "PENDING", warnings: Iterable[str] = ()) -> str:
    phase, title = infer_phase(task_text)
    snapshot_state = "present" if (repo_root / SNAPSHOT_PATH).exists() else "missing; run snapshot"
    repo_map_state = "present" if (repo_root / REPO_MAP_JSON_PATH).exists() else "missing; run index"
    test_map_state = "present" if (repo_root / TEST_MAP_JSON_PATH).exists() else "missing; run index"
    context_packet_state = "present" if (repo_root / LATEST_CONTEXT_PACKET_PATH).exists() else "missing; run context"
    warning_lines = "\n".join(f"  - {warning}" for warning in warnings) or "  - none"
    return f"""# AIDE Latest Task Packet

## PHASE

{phase} - {title}

## GOAL

{task_text.strip()}

## WHY

Continue AIDE token survival by using repo-local context refs, compact objectives, deterministic validation, and evidence packets instead of long chat history.

## CONTEXT_REFS

- `.aide/memory/project-state.md`
- `.aide/memory/decisions.md`
- `.aide/memory/open-risks.md`
- `{SNAPSHOT_PATH}` ({snapshot_state})
- `{REPO_MAP_JSON_PATH}` ({repo_map_state})
- `{REPO_MAP_MD_PATH}` ({repo_map_state})
- `{TEST_MAP_JSON_PATH}` ({test_map_state})
- `{CONTEXT_INDEX_PATH}` ({'present' if (repo_root / CONTEXT_INDEX_PATH).exists() else 'missing; run index'})
- `{LATEST_CONTEXT_PACKET_PATH}` ({context_packet_state})
- `.aide/prompts/compact-task.md`
- `.aide/policies/token-budget.yaml`

## ALLOWED_PATHS

- `<fill from the next reviewed queue packet>`
- `.aide/context/**`
- `.aide/queue/{phase.lower()}-*` if this task becomes a queue item
- root docs only when behavior or documentation links change

## FORBIDDEN_PATHS

- `.git/**`
- `.env`
- `secrets/**`
- `.aide.local/**`
- raw provider credentials, API keys, local caches, raw prompt logs
- Gateway, provider, Runtime, Service, Commander, Mobile, MCP/A2A, host, or app-surface implementation paths unless the queue packet explicitly authorizes them

## IMPLEMENTATION

- Read the queue packet and relevant repo refs first.
- Keep changes inside the allowed paths.
- Make the smallest coherent diff that satisfies acceptance.
- Preserve generated/manual boundaries.
- Do not inline whole source files unless exact contents are required.
- Use exact refs such as `path#Lstart-Lend` when file details are load-bearing.

## VALIDATION

- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py index`
- `py -3 .aide/scripts/aide_lite.py context`
- `py -3 .aide/scripts/aide_lite.py verify`
- `py -3 .aide/scripts/aide_lite.py review-pack`
- `py -3 .aide/scripts/aide_lite.py selftest`
- `py -3 scripts/aide validate`
- `git diff --check`

## COMMITS

- Commit coherent subdeliverables with verbose bodies.
- Stop at review gates.

## EVIDENCE

- changed files
- validation commands and results
- verifier result
- review packet path and result when review-pack is available
- compact packet size and budget status
- unresolved risks and deferrals

## NON_GOALS

- No Gateway, provider calls, live model routing, local model setup, exact tokenizer, provider billing ledger, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app implementation, or autonomous loop unless this packet is superseded by a reviewed queue item that explicitly authorizes it.

## ACCEPTANCE

- Task-specific acceptance criteria are met.
- Validation is run and recorded.
- Evidence is written.
- No secrets, raw prompt logs, local caches, or `.aide.local` contents are committed.

## OUTPUT_SCHEMA

Return a compact final report with `STATUS`, `SUMMARY`, `COMMITS`, `CHANGED_FILES`, `VALIDATION`, `TOKEN_RESULT`, `RISKS`, and `NEXT`.
Include the verifier result when Q12 verifier behavior is available.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- chars: {chars}
- approx_tokens: {tokens}
- budget_status: {budget_status}
- warnings:
{warning_lines}
- formal ledger: `.aide/reports/token-ledger.jsonl`
"""


def build_task_packet(repo_root: Path, task_text: str) -> PacketRender:
    body = render_task_packet(repo_root, task_text)
    for _ in range(5):
        stats = estimate_text(body, LATEST_PACKET_PATH)
        budget_status, warnings = packet_budget_warnings(body, repo_root)
        updated = render_task_packet(repo_root, task_text, stats.chars, stats.approx_tokens, budget_status, warnings)
        if updated == body:
            break
        body = updated
    stats = estimate_text(body, LATEST_PACKET_PATH)
    budget_status, warnings = packet_budget_warnings(body, repo_root)
    return PacketRender(body, stats, budget_status, warnings)


def write_task_packet(repo_root: Path, task_text: str) -> tuple[WriteResult, PacketRender]:
    if not (repo_root / SNAPSHOT_PATH).exists():
        write_snapshot(repo_root)
    packet = build_task_packet(repo_root, task_text)
    result = write_text_if_changed(repo_root / LATEST_PACKET_PATH, packet.text)
    return result, packet


def scan_for_secrets(repo_root: Path, paths: Iterable[str]) -> list[str]:
    findings: list[str] = []
    for rel in paths:
        path = repo_root / rel
        if path.is_dir():
            candidates = [candidate for candidate in path.rglob("*") if candidate.is_file()]
        elif path.exists():
            candidates = [path]
        else:
            continue
        for candidate in candidates:
            try:
                if looks_binary(candidate):
                    continue
                text = read_text(candidate)
            except (OSError, UnicodeDecodeError):
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    findings.append(normalize_rel(candidate.relative_to(repo_root)))
                    break
    return sorted(set(findings))


def validate_repo(repo_root: Path) -> tuple[bool, list[str]]:
    checks = collect_validation_checks(repo_root)
    return not any(check.severity == "FAIL" for check in checks), [f"{check.severity} {check.message}" for check in checks]


def collect_validation_checks(repo_root: Path) -> list[Check]:
    checks: list[Check] = []
    for rel in REQUIRED_FILES:
        if not (repo_root / rel).exists():
            checks.append(Check("FAIL", f"missing required file: {rel}"))
        else:
            checks.append(Check("PASS", f"required file: {rel}"))

    budget_path = repo_root / ".aide/policies/token-budget.yaml"
    budget_text = read_text(budget_path) if budget_path.exists() else ""
    for anchor in TOKEN_BUDGET_ANCHORS:
        if anchor not in budget_text:
            checks.append(Check("FAIL", f"token budget missing anchor: {anchor}"))
    budget = load_token_budget(repo_root)

    prompt_path = repo_root / ".aide/prompts/compact-task.md"
    if prompt_path.exists():
        for section in missing_sections(read_text(prompt_path), COMPACT_TASK_SECTIONS):
            checks.append(Check("FAIL", f"compact task missing section: {section}"))

    review_path = repo_root / ".aide/prompts/evidence-review.md"
    if review_path.exists():
        review_text = read_text(review_path)
        for decision in ["PASS", "PASS_WITH_NOTES", "REQUEST_CHANGES", "BLOCKED"]:
            if decision not in review_text:
                checks.append(Check("FAIL", f"evidence review missing decision: {decision}"))
        for section in ["DECISION:", "REASONS:", "REQUIRED_FIXES:", "OPTIONAL_NOTES:", "NEXT_PHASE:"]:
            if section not in review_text:
                checks.append(Check("FAIL", f"evidence review missing output section: {section}"))

    ignore_patterns = load_ignore_patterns(repo_root)
    for pattern in REQUIRED_IGNORE_PATTERNS:
        if pattern not in ignore_patterns:
            checks.append(Check("FAIL", f"ignore policy missing exclusion: {pattern}"))

    for rel in CONTEXT_CONFIG_FILES:
        if (repo_root / rel).exists():
            checks.append(Check("PASS", f"context compiler config exists: {rel}"))
        elif (repo_root / ".aide/queue/Q11-context-compiler-v0").exists():
            checks.append(Check("FAIL", f"context compiler config missing: {rel}"))

    for rel in Q12_REQUIRED_FILES:
        if (repo_root / rel).exists():
            checks.append(Check("PASS", f"verifier config exists: {rel}"))
        elif (repo_root / ".aide/queue/Q12-verifier-v0").exists():
            checks.append(Check("FAIL", f"verifier config missing: {rel}"))

    if (repo_root / ".aide/queue/Q14-token-ledger-savings-report").exists():
        for rel in Q14_REQUIRED_FILES:
            if (repo_root / rel).exists():
                checks.append(Check("PASS", f"token ledger artifact exists: {rel}"))
            else:
                checks.append(Check("FAIL", f"token ledger artifact missing: {rel}"))
        ledger_policy = repo_root / TOKEN_LEDGER_POLICY_PATH
        if ledger_policy.exists():
            ledger_policy_text = read_text(ledger_policy)
            for anchor in TOKEN_LEDGER_ANCHORS:
                if anchor not in ledger_policy_text:
                    checks.append(Check("FAIL", f"token ledger policy missing anchor: {anchor}"))
            if "raw_prompt_storage_default: false" not in ledger_policy_text:
                checks.append(Check("FAIL", "token ledger policy must disable raw prompt storage by default"))
            if "raw_response_storage_default: false" not in ledger_policy_text:
                checks.append(Check("FAIL", "token ledger policy must disable raw response storage by default"))
        ledger_records = read_ledger_records(repo_root)
        if ledger_records:
            checks.append(Check("PASS", f"token ledger records: {len(ledger_records)}"))
            raw_terms = [
                record
                for record in ledger_records
                if "raw prompt" in record.notes.lower()
                and "not stored" not in record.notes.lower()
                and "no raw" not in record.notes.lower()
            ]
            if raw_terms:
                checks.append(Check("FAIL", "token ledger record appears to describe raw prompt storage"))
            for warning in ledger_budget_warnings(ledger_records):
                checks.append(Check("WARN", f"token ledger budget warning: {warning}"))
        else:
            checks.append(Check("WARN", "token ledger has no records yet; run ledger scan"))

    evidence_template = repo_root / EVIDENCE_TEMPLATE_PATH
    if evidence_template.exists():
        for section in missing_sections(read_text(evidence_template), EVIDENCE_PACKET_REQUIRED_SECTIONS):
            checks.append(Check("FAIL", f"evidence template missing section: {section}"))

    review_template = repo_root / REVIEW_TEMPLATE_PATH
    if review_template.exists():
        for section in missing_sections(read_text(review_template), REVIEW_PACKET_REQUIRED_SECTIONS):
            checks.append(Check("FAIL", f"review template missing section: {section}"))

    project_state = repo_root / ".aide/memory/project-state.md"
    if project_state.exists():
        stats = estimate_file(repo_root, ".aide/memory/project-state.md")
        if stats.approx_tokens > budget["max_project_state_tokens"]:
            checks.append(Check("WARN", f"project state over hard limit: {stats.approx_tokens} > {budget['max_project_state_tokens']}"))
        else:
            checks.append(Check("PASS", f"project state tokens: {stats.approx_tokens} <= {budget['max_project_state_tokens']}"))

    packet_path = repo_root / LATEST_PACKET_PATH
    if packet_path.exists():
        packet_text = read_text(packet_path)
        packet_stats = estimate_text(packet_text, LATEST_PACKET_PATH)
        for section in missing_sections(packet_text, PACKET_REQUIRED_SECTIONS):
            checks.append(Check("FAIL", f"latest task packet missing section: {section}"))
        if packet_stats.approx_tokens > budget["max_compact_task_packet_tokens"]:
            checks.append(Check("WARN", f"latest task packet over hard limit: {packet_stats.approx_tokens} > {budget['max_compact_task_packet_tokens']}"))
        for warning in packet_budget_warnings(packet_text, repo_root)[1]:
            checks.append(Check("WARN", warning))
        checks.append(Check("PASS", f"latest task packet tokens: {packet_stats.approx_tokens}"))
    else:
        checks.append(Check("WARN", f"latest task packet missing: {LATEST_PACKET_PATH}"))

    review_packet = repo_root / REVIEW_PACKET_PATH
    if review_packet.exists():
        review_stats = estimate_file(repo_root, REVIEW_PACKET_PATH)
        for finding in verify_review_packet(repo_root, REVIEW_PACKET_PATH):
            if finding.severity == "ERROR":
                checks.append(Check("FAIL", f"review packet {finding.message}"))
            elif finding.severity in {"WARN", "WARNING"}:
                checks.append(Check("WARN", f"review packet {finding.message}"))
        if review_stats.approx_tokens > budget["max_review_packet_tokens"]:
            checks.append(Check("WARN", f"review packet over hard limit: {review_stats.approx_tokens} > {budget['max_review_packet_tokens']}"))
        checks.append(Check("PASS", f"review packet tokens: {review_stats.approx_tokens}"))

    context_expected = (repo_root / ".aide/queue/Q11-context-compiler-v0").exists()
    for rel in CONTEXT_OUTPUT_PATHS:
        if not (repo_root / rel).exists():
            checks.append(Check("WARN" if context_expected else "PASS", f"context artifact missing: {rel}"))

    repo_map_path = repo_root / REPO_MAP_JSON_PATH
    if repo_map_path.exists():
        try:
            repo_map = json.loads(read_text(repo_map_path))
            files = repo_map.get("files", [])
            if repo_map.get("contents_inline") is not False:
                checks.append(Check("FAIL", "repo map must declare contents_inline: false"))
            ignored_records = [
                str(entry.get("path", ""))
                for entry in files
                if is_ignored(str(entry.get("path", "")), ignore_patterns)
            ]
            if ignored_records:
                checks.append(Check("FAIL", f"repo map contains ignored records: {', '.join(ignored_records[:5])}"))
            raw_markers = [
                marker
                for marker in CONTEXT_FORBIDDEN_INLINE_MARKERS
                if marker in read_text(repo_map_path)
            ]
            if raw_markers:
                checks.append(Check("FAIL", f"repo map appears to inline raw contents: {', '.join(raw_markers)}"))
            if files != sorted(files, key=lambda item: (str(item.get("role", "")), str(item.get("path", "")))):
                checks.append(Check("FAIL", "repo map records are not deterministically sorted"))
            checks.append(Check("PASS", f"repo map records: {len(files)}"))
            snapshot_path = repo_root / SNAPSHOT_PATH
            if snapshot_path.exists():
                snapshot = json.loads(read_text(snapshot_path))
                current_hash = snapshot_fingerprint(snapshot)
                if repo_map.get("source_snapshot_hash") != current_hash:
                    checks.append(Check("WARN", "repo map source snapshot hash is stale"))
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
            checks.append(Check("FAIL", f"repo map is malformed: {exc}"))

    test_map_path = repo_root / TEST_MAP_JSON_PATH
    if test_map_path.exists():
        try:
            test_map = json.loads(read_text(test_map_path))
            if test_map.get("complete_coverage_claimed") is not False:
                checks.append(Check("FAIL", "test map must not claim complete coverage"))
            checks.append(Check("PASS", f"test map mappings: {test_map.get('summary', {}).get('mapping_count', 0)}"))
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            checks.append(Check("FAIL", f"test map is malformed: {exc}"))

    context_index_path = repo_root / CONTEXT_INDEX_PATH
    if context_index_path.exists():
        try:
            context_index = json.loads(read_text(context_index_path))
            if context_index.get("contents_inline") is not False:
                checks.append(Check("FAIL", "context index must declare contents_inline: false"))
            checks.append(Check("PASS", "context index is readable"))
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            checks.append(Check("FAIL", f"context index is malformed: {exc}"))

    context_packet_path = repo_root / LATEST_CONTEXT_PACKET_PATH
    if context_packet_path.exists():
        context_text = read_text(context_packet_path)
        for section in missing_sections(context_text, CONTEXT_PACKET_REQUIRED_SECTIONS):
            checks.append(Check("FAIL", f"latest context packet missing section: {section}"))
        raw_markers = [marker for marker in CONTEXT_FORBIDDEN_INLINE_MARKERS if marker in context_text]
        if raw_markers:
            checks.append(Check("FAIL", f"context packet appears to inline raw contents: {', '.join(raw_markers)}"))
        checks.append(Check("PASS", f"latest context packet tokens: {estimate_text(context_text, LATEST_CONTEXT_PACKET_PATH).approx_tokens}"))

    adapter = adapter_status(repo_root)
    if adapter.status == "current":
        checks.append(Check("PASS", "AGENTS token-survival managed section is current"))
    elif adapter.status in {"missing", "legacy", "drift"}:
        checks.append(Check("WARN", f"AGENTS token-survival managed section status: {adapter.status}; {adapter.action_hint}"))
    else:
        checks.append(Check("FAIL", f"AGENTS token-survival managed section status: {adapter.status}; {adapter.action_hint}"))

    secret_findings = scan_for_secrets(
        repo_root,
        [
            ".aide/policies/token-budget.yaml",
            ".aide/prompts",
            ".aide/memory",
            ".aide/context/compiler.yaml",
            ".aide/context/priority.yaml",
            ".aide/context/excerpt-policy.yaml",
            VERIFICATION_POLICY_PATH,
            TOKEN_LEDGER_POLICY_PATH,
            TOKEN_LEDGER_PATH,
            TOKEN_BASELINES_PATH,
            TOKEN_SUMMARY_PATH,
            ".aide/verification",
            ".aide/reports",
            LATEST_PACKET_PATH,
            LATEST_CONTEXT_PACKET_PATH,
            REVIEW_PACKET_PATH,
            LATEST_VERIFICATION_REPORT_PATH,
            "AGENTS.md",
        ],
    )
    if secret_findings:
        checks.append(Check("FAIL", f"possible secret material: {', '.join(secret_findings)}"))
    else:
        checks.append(Check("PASS", "no obvious secrets in token-survival files"))

    return checks


def q_status(repo_root: Path, queue_id: str) -> str:
    path = repo_root / f".aide/queue/{queue_id}/status.yaml"
    if not path.exists():
        return "missing"
    match = re.search(r"^status:\s*(\S+)", read_text(path), re.MULTILINE)
    return match.group(1) if match else "unknown"


def doctor(repo_root: Path) -> tuple[bool, list[str]]:
    messages: list[str] = [f"repo_root: {normalize_rel(repo_root)}"]
    hard_ok = True
    for rel in REQUIRED_FILES:
        exists = (repo_root / rel).exists()
        hard_ok = hard_ok and exists
        messages.append(f"{'PASS' if exists else 'FAIL'} required: {rel}")
    q09 = q_status(repo_root, "Q09-token-survival-core")
    q10 = q_status(repo_root, "Q10-aide-lite-hardening")
    q11 = q_status(repo_root, "Q11-context-compiler-v0")
    q12 = q_status(repo_root, "Q12-verifier-v0")
    q13 = q_status(repo_root, "Q13-evidence-review-workflow")
    q14 = q_status(repo_root, "Q14-token-ledger-savings-report")
    messages.append(f"INFO Q09 status: {q09}")
    messages.append(f"INFO Q10 status: {q10}")
    messages.append(f"INFO Q11 status: {q11}")
    messages.append(f"INFO Q12 status: {q12}")
    messages.append(f"INFO Q13 status: {q13}")
    messages.append(f"INFO Q14 status: {q14}")
    snapshot_exists = (repo_root / SNAPSHOT_PATH).exists()
    packet_exists = (repo_root / LATEST_PACKET_PATH).exists()
    messages.append(f"{'PASS' if snapshot_exists else 'WARN'} snapshot exists: {SNAPSHOT_PATH}")
    messages.append(f"{'PASS' if packet_exists else 'WARN'} latest task packet exists: {LATEST_PACKET_PATH}")
    for rel in [REPO_MAP_JSON_PATH, REPO_MAP_MD_PATH, TEST_MAP_JSON_PATH, CONTEXT_INDEX_PATH, LATEST_CONTEXT_PACKET_PATH]:
        exists = (repo_root / rel).exists()
        messages.append(f"{'PASS' if exists else 'WARN'} context artifact exists: {rel}")
    for rel in [VERIFICATION_POLICY_PATH, LATEST_VERIFICATION_REPORT_PATH]:
        exists = (repo_root / rel).exists()
        messages.append(f"{'PASS' if exists else 'WARN'} verifier artifact exists: {rel}")
    for rel in [REVIEW_DECISION_POLICY_PATH, REVIEW_PACKET_PATH]:
        exists = (repo_root / rel).exists()
        messages.append(f"{'PASS' if exists else 'WARN'} review artifact exists: {rel}")
    for rel in Q14_REQUIRED_FILES:
        exists = (repo_root / rel).exists()
        messages.append(f"{'PASS' if exists else 'WARN'} token ledger artifact exists: {rel}")
    ledger_count = len(read_ledger_records(repo_root))
    messages.append(f"{'PASS' if ledger_count else 'WARN'} token ledger records: {ledger_count}")
    adapter = adapter_status(repo_root)
    messages.append(f"{'PASS' if adapter.status == 'current' else 'WARN'} adapter status: {adapter.status}; {adapter.action_hint}")
    validation_ok, _ = validate_repo(repo_root)
    messages.append(f"{'PASS' if validation_ok else 'FAIL'} validation should be run: {'no hard validation failures detected' if validation_ok else 'run validate and fix failures'}")
    hard_ok = hard_ok and validation_ok
    return hard_ok, messages


def print_messages(title: str, ok: bool, messages: Iterable[str]) -> int:
    print(title)
    print(f"status: {'PASS' if ok else 'FAIL'}")
    for message in messages:
        print(f"- {message}")
    return 0 if ok else 1


def command_doctor(args: argparse.Namespace) -> int:
    ok, messages = doctor(args.repo_root)
    return print_messages("AIDE Lite doctor", ok, messages)


def command_validate(args: argparse.Namespace) -> int:
    ok, messages = validate_repo(args.repo_root)
    return print_messages("AIDE Lite validate", ok, messages)


def command_estimate(args: argparse.Namespace) -> int:
    stats = estimate_file(args.repo_root, args.file)
    surface = detect_surface(stats.path)
    budget, budget_status = ledger_budget_status(args.repo_root, surface, stats.approx_tokens)
    print("AIDE Lite estimate")
    print(f"path: {stats.path}")
    print(f"chars: {stats.chars}")
    print(f"lines: {stats.lines}")
    print(f"approx_tokens: {stats.approx_tokens}")
    print("method: chars / 4, rounded up")
    print(f"surface: {surface}")
    print(f"budget: {budget}")
    print(f"budget_status: {budget_status}")
    return 0


def command_snapshot(args: argparse.Namespace) -> int:
    result = write_snapshot(args.repo_root)
    snapshot = json.loads(read_text(result.path))
    summary = snapshot["summary"]
    print("AIDE Lite snapshot")
    print(f"path: {normalize_rel(result.path.relative_to(args.repo_root))}")
    print(f"action: {result.action}")
    print(f"file_count: {summary['file_count']}")
    print(f"total_size: {summary['total_size']}")
    print(f"aggregate_approx_tokens: {summary['aggregate_approx_tokens']}")
    print("contents_inline: false")
    return 0


def command_index(args: argparse.Namespace) -> int:
    result = run_index(args.repo_root)
    repo_map = result["repo_map"]
    test_map = result["test_map_data"]
    context_index = result["context_index_data"]
    print("AIDE Lite index")
    print(f"snapshot: {result['snapshot'].action} {SNAPSHOT_PATH}")
    print(f"repo_map_json: {result['repo_map_json'].action} {REPO_MAP_JSON_PATH}")
    print(f"repo_map_md: {result['repo_map_md'].action} {REPO_MAP_MD_PATH}")
    print(f"test_map: {result['test_map'].action} {TEST_MAP_JSON_PATH}")
    print(f"context_index: {result['context_index'].action} {CONTEXT_INDEX_PATH}")
    print(f"file_count: {repo_map.get('summary', {}).get('file_count', 0)}")
    print(f"test_mappings: {test_map.get('summary', {}).get('mapping_count', 0)}")
    print(f"source_snapshot_hash: {context_index.get('source_snapshot_hash', '')}")
    print("contents_inline: false")
    return 0


def command_context(args: argparse.Namespace) -> int:
    result = run_context(args.repo_root)
    packet: PacketRender = result["context_packet_data"]
    _budget, budget_status = ledger_budget_status(args.repo_root, "context_packet", packet.stats.approx_tokens)
    print("AIDE Lite context")
    print(f"path: {LATEST_CONTEXT_PACKET_PATH}")
    print(f"action: {result['context_packet'].action}")
    print(f"chars: {packet.stats.chars}")
    print(f"approx_tokens: {packet.stats.approx_tokens}")
    print(f"budget_status: {budget_status}")
    print(f"repo_map_json: {REPO_MAP_JSON_PATH}")
    print(f"test_map: {TEST_MAP_JSON_PATH}")
    print("contents_inline: false")
    return 0


def command_map(args: argparse.Namespace) -> int:
    repo_map = build_repo_map(args.repo_root)
    summary = repo_map.get("summary", {})
    print("AIDE Lite map")
    print(f"file_count: {summary.get('file_count', 0)}")
    print("role_counts:")
    for role, count in sorted(summary.get("role_counts", {}).items()):
        print(f"- {role}: {count}")
    print("contents_inline: false")
    return 0


def command_pack(args: argparse.Namespace) -> int:
    result, packet = write_task_packet(args.repo_root, args.task)
    print("AIDE Lite pack")
    print(f"path: {normalize_rel(result.path.relative_to(args.repo_root))}")
    print(f"action: {result.action}")
    print(f"chars: {packet.stats.chars}")
    print(f"approx_tokens: {packet.stats.approx_tokens}")
    print(f"budget_status: {packet.budget_status}")
    for warning in packet.warnings:
        print(f"warning: {warning}")
    print("ledger: run `ledger scan` to refresh metadata records")
    return 0


def command_verify(args: argparse.Namespace) -> int:
    report = build_verification_report(
        args.repo_root,
        evidence_path=args.evidence,
        task_packet_path=args.task_packet,
        review_packet_path=args.review_packet,
        changed_files_only=args.changed_files,
    )
    write_result: WriteResult | None = None
    if args.write_report:
        write_result = write_verification_report(args.repo_root, args.write_report, report)
    counts = {
        "info": sum(1 for finding in report.findings if finding.severity == "INFO"),
        "warnings": sum(1 for finding in report.findings if finding.severity in {"WARN", "WARNING"}),
        "errors": sum(1 for finding in report.findings if finding.severity in {"ERROR", "FAIL"}),
    }
    print("AIDE Lite verify")
    print(f"result: {report.result}")
    print(f"checked_files: {len(report.checked_files)}")
    print(f"changed_files: {len(report.changed_files)}")
    print(f"info: {counts['info']}")
    print(f"warnings: {counts['warnings']}")
    print(f"errors: {counts['errors']}")
    if write_result:
        print(f"report: {normalize_rel(write_result.path.relative_to(args.repo_root))}")
        print(f"report_action: {write_result.action}")
    for finding in report.findings:
        if finding.severity == "INFO":
            continue
        suffix = f" path={finding.path}" if finding.path else ""
        print(f"- {finding.severity} {finding.check}: {finding.message}{suffix}")
    return 1 if report.result == "FAIL" else 0


def command_review_pack(args: argparse.Namespace) -> int:
    result, packet = write_review_packet(
        args.repo_root,
        task_packet_path=args.task_packet,
        verification_path=args.verification,
        evidence_dir=args.evidence_dir,
        output_path=args.output,
        max_token_warning=args.max_token_warning,
    )
    verification_result_value = extract_verification_result(args.repo_root, args.verification)
    print("AIDE Lite review-pack")
    print(f"path: {normalize_rel(result.path.relative_to(args.repo_root))}")
    print(f"action: {result.action}")
    print(f"chars: {packet.stats.chars}")
    print(f"approx_tokens: {packet.stats.approx_tokens}")
    print(f"budget_status: {packet.budget_status}")
    print(f"verifier_result: {verification_result_value}")
    print("contents_inline: false")
    for warning in packet.warnings:
        print(f"warning: {warning}")
    return 0


def command_ledger_scan(args: argparse.Namespace) -> int:
    records = build_ledger_scan_records(args.repo_root, run_id=args.run_id)
    write_result, merged, existing = merge_ledger_records(args.repo_root, records, args.run_id)
    regression = regression_warnings(existing, records, load_regression_threshold(args.repo_root))
    summary_result = write_token_savings_summary(args.repo_root, merged, regression)
    budget_warnings = ledger_budget_warnings(records)
    print("AIDE Lite ledger scan")
    print(f"ledger: {TOKEN_LEDGER_PATH}")
    print(f"ledger_action: {write_result.action}")
    print(f"records_written: {len(records)}")
    print(f"records_total: {len(merged)}")
    print(f"summary: {TOKEN_SUMMARY_PATH}")
    print(f"summary_action: {summary_result.action}")
    print(f"budget_warnings: {len(budget_warnings)}")
    print(f"regression_warnings: {len(regression)}")
    print("raw_prompt_storage: false")
    print("raw_response_storage: false")
    for warning in budget_warnings[:10]:
        print(f"budget_warning: {warning}")
    for warning in regression[:10]:
        print(f"regression_warning: {warning}")
    return 0


def command_ledger_add(args: argparse.Namespace) -> int:
    rel = assert_ledger_safe_path(args.repo_root, args.file)
    surface = args.surface or detect_surface(rel)
    record = ledger_record_for_file(
        args.repo_root,
        rel,
        surface=surface,
        phase=args.phase,
        run_id=args.run_id,
        notes=args.notes or "manual estimated metadata record; raw content not stored",
    )
    existing = read_ledger_records(args.repo_root)
    retained = [
        item
        for item in existing
        if not (item.run_id == record.run_id and item.surface == record.surface and item.path == record.path)
    ]
    result = write_ledger_records(args.repo_root, [*retained, record])
    print("AIDE Lite ledger add")
    print(f"ledger: {TOKEN_LEDGER_PATH}")
    print(f"action: {result.action}")
    print(f"path: {record.path}")
    print(f"surface: {record.surface}")
    print(f"chars: {record.chars}")
    print(f"approx_tokens: {record.approx_tokens}")
    print(f"budget_status: {record.budget_status}")
    print("raw_content_stored: false")
    return 0


def command_ledger_report(args: argparse.Namespace) -> int:
    records = read_ledger_records(args.repo_root)
    regression = regression_warnings(records, [record for record in records if record.run_id == args.run_id], load_regression_threshold(args.repo_root))
    summary_result = write_token_savings_summary(args.repo_root, records, regression)
    by_surface: dict[str, int] = {}
    for record in records:
        by_surface[record.surface] = by_surface.get(record.surface, 0) + record.approx_tokens
    largest = sorted(records, key=lambda item: item.approx_tokens, reverse=True)[:5]
    budget_warnings = ledger_budget_warnings(records)
    print("AIDE Lite ledger report")
    print(f"records: {len(records)}")
    print(f"summary: {TOKEN_SUMMARY_PATH}")
    print(f"summary_action: {summary_result.action}")
    print(f"budget_warnings: {len(budget_warnings)}")
    print(f"regression_warnings: {len(regression)}")
    print("totals_by_surface:")
    for surface in sorted(by_surface):
        print(f"- {surface}: {by_surface[surface]}")
    print("largest_surfaces:")
    for record in largest:
        print(f"- {record.surface} {record.path}: {record.approx_tokens}")
    return 0


def command_ledger_compare(args: argparse.Namespace) -> int:
    comparison = compare_to_baseline(args.repo_root, args.file, args.baseline, surface=args.surface)
    print("AIDE Lite ledger compare")
    print(f"file: {comparison.compact.path}")
    print(f"surface: {comparison.compact.surface}")
    print(f"compact_chars: {comparison.compact.chars}")
    print(f"compact_approx_tokens: {comparison.compact.approx_tokens}")
    print(f"baseline: {comparison.baseline.name}")
    print(f"baseline_chars: {comparison.baseline.chars}")
    print(f"baseline_approx_tokens: {comparison.baseline.approx_tokens}")
    if comparison.reduction_percent is None:
        print("estimated_reduction_percent: unavailable")
    else:
        print(f"estimated_reduction_percent: {comparison.reduction_percent:.1f}")
    print("method: chars / 4, rounded up")
    print("exact_provider_billing: false")
    for warning in comparison.warnings:
        print(f"warning: {warning}")
    return 0


def command_adapt(args: argparse.Namespace) -> int:
    result, before, after = adapt_agents(args.repo_root)
    print("AIDE Lite adapt")
    print(f"path: {normalize_rel(result.path.relative_to(args.repo_root))}")
    print(f"action: {result.action}")
    print(f"before_status: {before.status}")
    print(f"after_status: {after.status}")
    print(f"managed_section: {AGENTS_SECTION}")
    return 0 if after.status == "current" else 1


def command_version(args: argparse.Namespace) -> int:
    print(f"{GENERATOR_NAME} {GENERATOR_VERSION}")
    return 0


def command_show_config(args: argparse.Namespace) -> int:
    print("AIDE Lite config")
    print(f"repo_root: {normalize_rel(args.repo_root)}")
    print(f"generator: {GENERATOR_NAME}")
    print(f"generator_version: {GENERATOR_VERSION}")
    print("token_budget:")
    for key, value in load_token_budget(args.repo_root).items():
        print(f"- {key}: {value}")
    return 0


def _write_minimal_repo(root: Path) -> None:
    for rel in REQUIRED_FILES:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
    source_root = repo_root_from_script()
    write_text(root / ".aide/policies/token-budget.yaml", read_text(source_root / ".aide/policies/token-budget.yaml"))
    write_text(root / ".aide/memory/project-state.md", "# Project\n\nCompact state.\n")
    write_text(root / ".aide/memory/decisions.md", "# Decisions\n")
    write_text(root / ".aide/memory/open-risks.md", "# Risks\n")
    write_text(root / ".aide/prompts/compact-task.md", read_text(source_root / ".aide/prompts/compact-task.md"))
    write_text(root / ".aide/prompts/evidence-review.md", read_text(source_root / ".aide/prompts/evidence-review.md"))
    write_text(root / ".aide/prompts/codex-token-mode.md", read_text(source_root / ".aide/prompts/codex-token-mode.md"))
    write_text(root / ".aide/context/ignore.yaml", read_text(source_root / ".aide/context/ignore.yaml"))
    for rel in CONTEXT_CONFIG_FILES:
        source = source_root / rel
        write_text(root / rel, read_text(source) if source.exists() else f"schema_version: {rel}\n")
    for rel in Q12_REQUIRED_FILES:
        source = source_root / rel
        write_text(root / rel, read_text(source) if source.exists() else f"schema_version: {rel}\n")
    for rel in Q14_REQUIRED_FILES:
        source = source_root / rel
        if source.exists():
            write_text(root / rel, read_text(source))
        elif rel.endswith(".jsonl"):
            write_text(root / rel, "")
        else:
            write_text(root / rel, f"schema_version: {rel}\n")
    write_text(root / ".aide/queue/Q08-self-hosting-automation/status.yaml", "status: passed\n")
    write_text(root / ".aide/queue/Q09-token-survival-core/status.yaml", "status: needs_review\n")
    write_text(root / ".aide/queue/Q10-aide-lite-hardening/status.yaml", "status: running\n")
    write_text(root / ".aide/queue/Q11-context-compiler-v0/status.yaml", "status: running\n")
    write_text(root / ".aide/queue/Q12-verifier-v0/status.yaml", "status: running\n")
    write_text(root / ".aide/queue/Q13-evidence-review-workflow/status.yaml", "status: running\n")
    write_text(root / ".aide/queue/Q14-token-ledger-savings-report/status.yaml", "status: running\n")
    write_text(
        root / ".aide/queue/Q12-verifier-v0/task.yaml",
        """scope:
  allowed_paths:
    - .aide/**
    - AGENTS.md
    - README.md
    - core/harness/**
  forbidden_paths:
    - .git/**
    - .env
    - secrets/**
    - .aide.local/**
""",
    )
    write_text(root / "AGENTS.md", "# AGENTS\n\nManual intro.\n")
    write_text(root / "README.md", "# README\n")
    write_text(
        root / ".aide/queue/Q13-evidence-review-workflow/task.yaml",
        """non_goals:
  - Gateway
  - provider calls
  - automatic model calls
""",
    )
    write_text(
        root / ".aide/queue/Q14-token-ledger-savings-report/task.yaml",
        """scope:
  allowed_paths:
    - .aide/**
    - AGENTS.md
    - README.md
  forbidden_paths:
    - .git/**
    - .env
    - secrets/**
    - .aide.local/**
non_goals:
  - Gateway
  - provider calls
  - exact tokenizer
  - provider billing
""",
    )
    write_text(
        root / ".aide/queue/Q13-evidence-review-workflow/evidence/validation.md",
        """# Validation

- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS
- `py -3 .aide/scripts/aide_lite.py verify --review-packet .aide/context/latest-review-packet.md`: PASS
""",
    )
    write_text(
        root / ".aide/queue/Q13-evidence-review-workflow/evidence/remaining-risks.md",
        """# Risks

- structural review packet only
- no automatic model call
""",
    )
    write_text(
        root / ".aide/queue/Q14-token-ledger-savings-report/evidence/validation.md",
        """# Validation

- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS
""",
    )
    write_text(
        root / ".aide/queue/Q14-token-ledger-savings-report/evidence/remaining-risks.md",
        """# Risks

- estimated token accounting only
- no exact provider billing
""",
    )
    write_text(root / ".aide/scripts/aide_lite.py", "print('helper placeholder')\n")
    write_text(root / ".aide/scripts/tests/test_aide_lite.py", "def test_placeholder():\n    assert True\n")
    write_text(root / "core/harness/commands.py", "COMMANDS = []\n")
    write_text(root / "core/harness/tests/test_aide_harness.py", "def test_harness():\n    assert True\n")
    write_text(root / "core/compat/version_registry.py", "VERSION = 'x'\n")
    write_text(root / "core/compat/tests/test_compat_baseline.py", "def test_compat():\n    assert True\n")
    write_text(root / "src/example.py", "print('hello')\n")
    write_text(root / ".env", "SHOULD_NOT_APPEAR=1\n")
    write_text(root / ".git/config", "ignored\n")
    write_text(root / ".aide.local/state.json", "{}\n")
    write_text(root / "node_modules/pkg/index.js", "ignored\n")
    write_text(root / "build/output.txt", "ignored\n")


def run_selftest() -> tuple[bool, list[str]]:
    messages: list[str] = []
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _write_minimal_repo(root)
        assert estimate_text("abcd").approx_tokens == 1
        assert pattern_matches("core/harness/__pycache__/x.pyc", "__pycache__/**")
        assert pattern_matches("node_modules/pkg/index.js", "node_modules/**")
        assert pattern_matches(".env", ".env")
        assert pattern_matches(".aide.local/state.json", ".aide.local/**")
        snapshot_result = write_snapshot(root)
        snapshot = json.loads(read_text(snapshot_result.path))
        paths = [entry["path"] for entry in snapshot["files"]]
        assert ".env" not in paths
        assert all(not path.startswith(".git/") for path in paths)
        assert all(not path.startswith(".aide.local/") for path in paths)
        assert all(not path.startswith("node_modules/") for path in paths)
        assert all(not path.startswith("build/") for path in paths)
        assert paths == sorted(paths)
        assert snapshot["contents_inline"] is False
        assert "summary" in snapshot
        role, reason = classify_role(".aide/scripts/aide_lite.py")
        assert role == "script", reason
        role, reason = classify_role("core/harness/commands.py")
        assert role == "harness_code", reason
        index_result = run_index(root)
        repo_map = index_result["repo_map"]
        mapped_paths = [entry["path"] for entry in repo_map["files"]]
        assert ".env" not in mapped_paths
        assert mapped_paths == sorted(mapped_paths, key=lambda path: (classify_role(path)[0], path))
        assert all("contents" not in entry for entry in repo_map["files"])
        test_map = index_result["test_map_data"]
        aide_mapping = next(item for item in test_map["mappings"] if item["source"] == ".aide/scripts/aide_lite.py")
        assert aide_mapping["has_existing_candidate"] is True
        context_result = run_context(root)
        context_text = read_text(context_result["context_packet"].path)
        for section in CONTEXT_PACKET_REQUIRED_SECTIONS:
            assert f"## {section}" in context_text
        assert "print('hello')" not in context_text
        valid_ref, _message = validate_line_ref(root, "README.md#L1-L1")
        assert valid_ref
        packet_result, packet = write_task_packet(root, "Implement Q11 Context Compiler v0")
        packet_text = read_text(packet_result.path)
        for section in ["PHASE", "GOAL", "CONTEXT_REFS", "ACCEPTANCE", "TOKEN_ESTIMATE"]:
            assert f"## {section}" in packet_text
        assert REPO_MAP_JSON_PATH in packet_text
        assert LATEST_CONTEXT_PACKET_PATH in packet_text
        assert "print('hello')" not in packet_text
        assert packet.budget_status == "PASS"
        before_manual = read_text(root / "AGENTS.md")
        adapt_result, before, after = adapt_agents(root)
        once = read_text(root / "AGENTS.md")
        adapt_agents(root)
        twice = read_text(root / "AGENTS.md")
        assert "Manual intro." in twice
        assert before_manual != once
        assert once == twice
        assert adapt_result.action in {"appended", "written"}
        assert before.status == "missing"
        assert after.status == "current"
        ref_finding = validate_file_reference(root, "README.md#L1-L1")
        assert ref_finding.severity == "INFO", ref_finding
        missing_ref = validate_file_reference(root, "missing.md")
        assert missing_ref.severity == "WARN", missing_ref
        fake_secret_value = "1234567890abcdef" * 2
        secret_findings = scan_secret_text("api_key = '" + fake_secret_value + "'\n", ".aide/test.md")
        assert any(finding.severity == "ERROR" for finding in secret_findings)
        policy_findings = scan_secret_text("Mention api_key as policy text only.\n", ".aide/test.md")
        assert not any(finding.severity == "ERROR" for finding in policy_findings)
        verification = build_verification_report(root, task_packet_path=LATEST_PACKET_PATH)
        assert verification.result in {"PASS", "WARN"}, verification.result
        rendered_report = render_verification_report(verification)
        assert "## VERIFIER_RESULT" in rendered_report
        assert "print('hello')" not in rendered_report
        write_verification_report(root, LATEST_VERIFICATION_REPORT_PATH, verification)
        review_result, review_packet = write_review_packet(root)
        review_text = read_text(review_result.path)
        for section in REVIEW_PACKET_REQUIRED_SECTIONS:
            assert f"## {section}" in review_text
        assert default_review_task_packet(root) in review_text
        assert LATEST_CONTEXT_PACKET_PATH in review_text
        assert LATEST_VERIFICATION_REPORT_PATH in review_text
        assert "print('hello')" not in review_text
        assert review_packet.budget_status == "PASS"
        review_findings = verify_review_packet(root, REVIEW_PACKET_PATH)
        assert not any(finding.severity == "ERROR" for finding in review_findings), review_findings
        selftest_record = ledger_record_for_file(root, LATEST_PACKET_PATH, surface="task_packet", run_id="selftest")
        assert selftest_record.approx_tokens > 0
        assert selftest_record.budget_status in {"within_budget", "near_budget", "over_budget"}
        ledger_result, merged_records, old_records = merge_ledger_records(root, [selftest_record], "selftest")
        assert ledger_result.action in {"written", "unchanged"}
        assert not old_records or all("raw" not in record.path.lower() for record in old_records)
        read_records = read_ledger_records(root)
        assert any(record.run_id == "selftest" and record.path == LATEST_PACKET_PATH for record in read_records)
        baseline = calculate_baseline(root, baseline_by_name(root, "root_history_baseline"))
        assert baseline.approx_tokens > 0
        comparison = compare_to_baseline(root, LATEST_PACKET_PATH, "root_history_baseline")
        assert comparison.reduction_percent is not None
        prior = LedgerRecord("prior", "Q", "task_packet", LATEST_PACKET_PATH, 4, 1, 1, "chars/4", "3200", "within_budget", "old")
        current = LedgerRecord("q14.scan.current", "Q", "task_packet", LATEST_PACKET_PATH, 400, 1, 100, "chars/4", "3200", "within_budget", "new")
        assert regression_warnings([prior], [current], 20)
        summary_result = write_token_savings_summary(root, read_records, [])
        assert summary_result.action in {"written", "unchanged"}
        summary_text = read_text(root / TOKEN_SUMMARY_PATH)
        assert "raw_prompt_storage: false" in summary_text
        assert "print('hello')" not in read_text(root / TOKEN_LEDGER_PATH)
        ok, validate_messages = validate_repo(root)
        assert ok, "\n".join(validate_messages)
        messages.append("PASS internal estimate, ignore, snapshot, index, context, pack, adapt, drift, line-ref, verifier, review-pack, ledger, and validate checks")
    return True, messages


def command_selftest(args: argparse.Namespace) -> int:
    try:
        ok, messages = run_selftest()
    except AssertionError as exc:
        print("AIDE Lite selftest")
        print("status: FAIL")
        print(f"- {exc}")
        return 1
    return print_messages("AIDE Lite selftest", ok, messages)


def build_parser(default_repo_root: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AIDE Lite token-survival helper.")
    parser.add_argument("--repo-root", default=str(default_repo_root), help="Repository root. Defaults to the AIDE repo root.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor").set_defaults(handler=command_doctor)
    subparsers.add_parser("validate").set_defaults(handler=command_validate)

    estimate_parser = subparsers.add_parser("estimate")
    estimate_parser.add_argument("--file", required=True)
    estimate_parser.set_defaults(handler=command_estimate)

    subparsers.add_parser("snapshot").set_defaults(handler=command_snapshot)
    subparsers.add_parser("index").set_defaults(handler=command_index)
    subparsers.add_parser("context").set_defaults(handler=command_context)
    subparsers.add_parser("map").set_defaults(handler=command_map)

    pack_parser = subparsers.add_parser("pack")
    pack_parser.add_argument("--task", required=True)
    pack_parser.set_defaults(handler=command_pack)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--evidence", help="Evidence packet path to validate.")
    verify_parser.add_argument("--task-packet", help="Task packet path to validate. Defaults to latest task packet.")
    verify_parser.add_argument("--review-packet", help="Review packet path to validate. Defaults to latest review packet when present.")
    verify_parser.add_argument("--changed-files", action="store_true", help="Only classify git changed files against scope.")
    verify_parser.add_argument("--write-report", help="Write compact verification report under .aide/verification/ or .aide/queue/.")
    verify_parser.set_defaults(handler=command_verify)

    review_parser = subparsers.add_parser("review-pack")
    review_parser.add_argument("--task-packet", help="Task packet path to reference. Defaults to the current queue task when present.")
    review_parser.add_argument("--verification", default=LATEST_VERIFICATION_REPORT_PATH, help="Verification report path to reference.")
    review_parser.add_argument("--evidence-dir", help="Evidence directory to reference. Defaults to the current queue evidence directory.")
    review_parser.add_argument("--output", default=REVIEW_PACKET_PATH, help="Review packet output path.")
    review_parser.add_argument("--changed-files", action="store_true", help="Include git changed-file summary; current default already includes it.")
    review_parser.add_argument("--max-token-warning", type=int, help="Warn when review packet exceeds this approximate-token threshold.")
    review_parser.set_defaults(handler=command_review_pack)

    ledger_parser = subparsers.add_parser("ledger")
    ledger_subparsers = ledger_parser.add_subparsers(dest="ledger_command", required=True)

    ledger_scan_parser = ledger_subparsers.add_parser("scan")
    ledger_scan_parser.add_argument("--run-id", default="q14.scan.current", help="Stable run id for replacing current scan records.")
    ledger_scan_parser.set_defaults(handler=command_ledger_scan)

    ledger_add_parser = ledger_subparsers.add_parser("add")
    ledger_add_parser.add_argument("--file", required=True, help="File to add as estimated metadata.")
    ledger_add_parser.add_argument("--surface", choices=LEDGER_SURFACES, help="Record surface. Defaults to detection from path.")
    ledger_add_parser.add_argument("--phase", default="Q14-token-ledger-savings-report")
    ledger_add_parser.add_argument("--run-id", default="q14.manual")
    ledger_add_parser.add_argument("--notes", default="")
    ledger_add_parser.set_defaults(handler=command_ledger_add)

    ledger_report_parser = ledger_subparsers.add_parser("report")
    ledger_report_parser.add_argument("--run-id", default="q14.scan.current", help="Run id to use as current records for regression checks.")
    ledger_report_parser.set_defaults(handler=command_ledger_report)

    ledger_compare_parser = ledger_subparsers.add_parser("compare")
    ledger_compare_parser.add_argument("--baseline", required=True)
    ledger_compare_parser.add_argument("--file", required=True)
    ledger_compare_parser.add_argument("--surface", choices=LEDGER_SURFACES)
    ledger_compare_parser.set_defaults(handler=command_ledger_compare)

    subparsers.add_parser("adapt").set_defaults(handler=command_adapt)
    subparsers.add_parser("selftest").set_defaults(handler=command_selftest)
    subparsers.add_parser("version").set_defaults(handler=command_version)
    subparsers.add_parser("show-config").set_defaults(handler=command_show_config)
    return parser


def main(argv: list[str] | None = None) -> int:
    default_root = repo_root_from_script()
    parser = build_parser(default_root)
    args = parser.parse_args(argv)
    args.repo_root = Path(args.repo_root).resolve()
    try:
        return int(args.handler(args))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
