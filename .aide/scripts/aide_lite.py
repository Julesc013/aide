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
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


GENERATOR_NAME = "aide-lite"
GENERATOR_VERSION = "q11.context-compiler.v0"
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
        "compact_task_packet_target_tokens": parse_int_value(text, "compact_task_packet_target_tokens", 1800),
    }


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
    for queue_id in ["Q11-context-compiler-v0", "Q10-aide-lite-hardening", "Q09-token-survival-core"]:
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
- formal ledger: deferred to Q14
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


def agents_body() -> str:
    return """## Q11 Token And Context Guidance

- Use `.aide/context/latest-task-packet.md` when present instead of pasting long chat history.
- Use `.aide/context/latest-context-packet.md`, repo-map refs, test-map refs, compact project memory, and evidence packets before broad context dumps.
- Do not paste full prior transcripts, whole repo dumps, repeated roadmap dumps, secrets, provider keys, local caches, or raw prompt logs.
- Emit deltas and compact final reports with status, changed files, validation, evidence, risks, and next step.
- Review evidence only by default; ask for more context only when the packet is insufficient.
- Run `py -3 .aide/scripts/aide_lite.py doctor`, `validate`, `snapshot`, `index`, `context`, `pack`, `estimate`, `adapt`, and `selftest` for token/context work.
- Prefer exact refs such as `path#Lstart-Lend`; do not inline whole files by default.
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
- `py -3 .aide/scripts/aide_lite.py selftest`
- `py -3 scripts/aide validate`
- `git diff --check`

## COMMITS

- Commit coherent subdeliverables with verbose bodies.
- Stop at review gates.

## EVIDENCE

- changed files
- validation commands and results
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

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- chars: {chars}
- approx_tokens: {tokens}
- budget_status: {budget_status}
- warnings:
{warning_lines}
- formal ledger: deferred to Q14
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

    ignore_patterns = load_ignore_patterns(repo_root)
    for pattern in REQUIRED_IGNORE_PATTERNS:
        if pattern not in ignore_patterns:
            checks.append(Check("FAIL", f"ignore policy missing exclusion: {pattern}"))

    for rel in CONTEXT_CONFIG_FILES:
        if (repo_root / rel).exists():
            checks.append(Check("PASS", f"context compiler config exists: {rel}"))
        elif (repo_root / ".aide/queue/Q11-context-compiler-v0").exists():
            checks.append(Check("FAIL", f"context compiler config missing: {rel}"))

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
        if review_stats.approx_tokens > budget["max_review_packet_tokens"]:
            checks.append(Check("WARN", f"review packet over hard limit: {review_stats.approx_tokens} > {budget['max_review_packet_tokens']}"))

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
            LATEST_PACKET_PATH,
            LATEST_CONTEXT_PACKET_PATH,
            REVIEW_PACKET_PATH,
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
    messages.append(f"INFO Q09 status: {q09}")
    messages.append(f"INFO Q10 status: {q10}")
    messages.append(f"INFO Q11 status: {q11}")
    snapshot_exists = (repo_root / SNAPSHOT_PATH).exists()
    packet_exists = (repo_root / LATEST_PACKET_PATH).exists()
    messages.append(f"{'PASS' if snapshot_exists else 'WARN'} snapshot exists: {SNAPSHOT_PATH}")
    messages.append(f"{'PASS' if packet_exists else 'WARN'} latest task packet exists: {LATEST_PACKET_PATH}")
    for rel in [REPO_MAP_JSON_PATH, REPO_MAP_MD_PATH, TEST_MAP_JSON_PATH, CONTEXT_INDEX_PATH, LATEST_CONTEXT_PACKET_PATH]:
        exists = (repo_root / rel).exists()
        messages.append(f"{'PASS' if exists else 'WARN'} context artifact exists: {rel}")
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
    print("AIDE Lite estimate")
    print(f"path: {stats.path}")
    print(f"chars: {stats.chars}")
    print(f"lines: {stats.lines}")
    print(f"approx_tokens: {stats.approx_tokens}")
    print("method: chars / 4, rounded up")
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
    print("AIDE Lite context")
    print(f"path: {LATEST_CONTEXT_PACKET_PATH}")
    print(f"action: {result['context_packet'].action}")
    print(f"chars: {packet.stats.chars}")
    print(f"approx_tokens: {packet.stats.approx_tokens}")
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
    print("ledger: deferred to Q14")
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
    write_text(root / ".aide/queue/Q08-self-hosting-automation/status.yaml", "status: passed\n")
    write_text(root / ".aide/queue/Q09-token-survival-core/status.yaml", "status: needs_review\n")
    write_text(root / ".aide/queue/Q10-aide-lite-hardening/status.yaml", "status: running\n")
    write_text(root / ".aide/queue/Q11-context-compiler-v0/status.yaml", "status: running\n")
    write_text(root / "AGENTS.md", "# AGENTS\n\nManual intro.\n")
    write_text(root / "README.md", "# README\n")
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
        ok, validate_messages = validate_repo(root)
        assert ok, "\n".join(validate_messages)
        messages.append("PASS internal estimate, ignore, snapshot, index, context, pack, adapt, drift, line-ref, and validate checks")
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
