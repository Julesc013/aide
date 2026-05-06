#!/usr/bin/env python3
"""AIDE Lite token-survival helper.

Q09 keeps this helper standard-library only. It compiles compact task
packets from repo-local state, validates Q09 token-survival anchors, and
does not call providers, models, network services, or external tools.
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

SNAPSHOT_PATH = ".aide/context/repo-snapshot.json"
LATEST_PACKET_PATH = ".aide/context/latest-task-packet.md"
AGENTS_BEGIN = "<!-- AIDE-TOKEN-SURVIVAL:BEGIN section=q09-token-survival mode=managed -->"
AGENTS_END = "<!-- AIDE-TOKEN-SURVIVAL:END section=q09-token-survival -->"

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


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize_rel(path: str | Path) -> str:
    rel = Path(path).as_posix()
    while rel.startswith("./"):
        rel = rel[2:]
    return rel


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def approx_tokens_for_chars(chars: int) -> int:
    return int(math.ceil(chars / 4)) if chars else 0


def estimate_text(text: str, path: str = "<memory>") -> TextStats:
    return TextStats(
        path=path,
        chars=len(text),
        lines=0 if not text else text.count("\n") + (0 if text.endswith("\n") else 1),
        approx_tokens=approx_tokens_for_chars(len(text)),
    )


def estimate_file(repo_root: Path, requested: str) -> TextStats:
    target = safe_repo_path(repo_root, requested)
    text = read_text(target)
    return estimate_text(text, normalize_rel(target.relative_to(repo_root)))


def safe_repo_path(repo_root: Path, requested: str) -> Path:
    target = (repo_root / requested).resolve()
    root = repo_root.resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path must stay inside repo: {requested}") from exc
    return target


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
            parts = rel.split("/")
            return base in parts
        return rel == base or rel.startswith(base + "/")
    if "/" not in pattern:
        return any(fnmatch.fnmatch(part, pattern) for part in rel.split("/"))
    return fnmatch.fnmatch(rel, pattern)


def is_ignored(rel_path: str, patterns: Iterable[str]) -> bool:
    rel = normalize_rel(rel_path)
    if rel in {SNAPSHOT_PATH, LATEST_PACKET_PATH}:
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
            files.append(
                {
                    "path": rel,
                    "size": stat.st_size,
                    "mtime": int(stat.st_mtime),
                    "sha256": sha256_file(path),
                    "extension": path.suffix.lower(),
                    "type": coarse_type(path),
                }
            )
    files.sort(key=lambda item: str(item["path"]))
    return {
        "schema_version": "aide.repo-snapshot.v0",
        "generator": "aide_lite.py",
        "contents_inline": False,
        "ignored_patterns": patterns,
        "file_count": len(files),
        "files": files,
    }


def write_snapshot(repo_root: Path) -> Path:
    snapshot = build_snapshot(repo_root)
    target = repo_root / SNAPSHOT_PATH
    write_text(target, json.dumps(snapshot, indent=2, sort_keys=True))
    return target


def load_task_template(repo_root: Path) -> str:
    path = repo_root / ".aide/prompts/compact-task.md"
    if path.exists():
        return read_text(path)
    return "# AIDE Compact Task Packet Template\n"


def render_task_packet(repo_root: Path, task_text: str, chars: int = 0, tokens: int = 0) -> str:
    template_path = ".aide/prompts/compact-task.md"
    snapshot_path = SNAPSHOT_PATH
    snapshot_state = "present" if (repo_root / snapshot_path).exists() else "missing; run snapshot"
    return f"""# AIDE Latest Task Packet

## PHASE

Q10 - AIDE Lite hardening

## GOAL

{task_text}

## WHY

Continue Q09 token survival by hardening compact packet generation, validation, deterministic adapter updates, and selftests.

## CONTEXT_REFS

- `.aide/memory/project-state.md`
- `.aide/memory/decisions.md`
- `.aide/memory/open-risks.md`
- `{snapshot_path}` ({snapshot_state})
- `{template_path}`
- `.aide/queue/Q09-token-survival-core/evidence/`

## ALLOWED_PATHS

- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/**`
- `.aide/policies/**`
- `.aide/prompts/**`
- `.aide/context/**`
- `.aide/memory/**`
- `.aide/queue/Q10-*` or future reviewed Q10 queue path
- `AGENTS.md` managed token-survival section
- root docs only when behavior or documentation links change

## FORBIDDEN_PATHS

- `.git/**`
- `.env`
- `secrets/**`
- `.aide.local/**`
- raw provider credentials, API keys, local caches, raw prompt logs
- Gateway, provider, Runtime, Service, Commander, Mobile, MCP/A2A, host, or app-surface implementation paths

## IMPLEMENTATION

- Harden AIDE Lite command structure and deterministic writes.
- Add drift-aware adapter generation and stronger validation.
- Expand tests/selftests around ignore matching, packet budgets, and adapter determinism.
- Keep stdlib-only behavior and no provider/network calls.

## VALIDATION

- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py selftest`
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`
- `py -3 scripts/aide validate`
- `git diff --check`

## COMMITS

- CLI hardening
- tests/selftests
- generated adapter/context updates
- evidence/docs updates if needed

## EVIDENCE

- changed files
- validation commands and results
- compact packet size and budget status
- unresolved risks and deferrals

## NON_GOALS

- No Gateway
- No provider calls
- No model routing
- No local model setup
- No Runtime, Service, Commander, Mobile, MCP/A2A, or host implementation

## ACCEPTANCE

- AIDE Lite commands pass.
- Adapt can run twice without changing output.
- Pack emits a compact packet under the configured hard limit.
- Validation catches missing required files or sections.
- Evidence records token estimates and remaining risks.

## OUTPUT_SCHEMA

Return a compact final report with `STATUS`, `SUMMARY`, `COMMITS`, `CHANGED_FILES`, `VALIDATION`, `TOKEN_SURVIVAL_RESULT`, `RISKS`, and `NEXT`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- chars: {chars}
- approx_tokens: {tokens}
- formal ledger: deferred to Q14
"""


def write_task_packet(repo_root: Path, task_text: str) -> Path:
    if not (repo_root / SNAPSHOT_PATH).exists():
        write_snapshot(repo_root)
    body = render_task_packet(repo_root, task_text)
    for _ in range(3):
        stats = estimate_text(body, LATEST_PACKET_PATH)
        updated = render_task_packet(repo_root, task_text, stats.chars, stats.approx_tokens)
        if updated == body:
            break
        body = updated
    target = repo_root / LATEST_PACKET_PATH
    write_text(target, body)
    return target


def token_guidance_section() -> str:
    body = """## Q09 Token-Survival Guidance

- Use `.aide/context/latest-task-packet.md` when present instead of pasting long chat history.
- Use repo refs, compact project memory, and evidence packets before broad context dumps.
- Do not paste full prior transcripts, whole repo dumps, repeated roadmap dumps, secrets, provider keys, local caches, or raw prompt logs.
- Emit deltas and compact final reports with status, changed files, validation, evidence, risks, and next step.
- Review evidence only by default; ask for more context only when the packet is insufficient.
- Run proportionate validation and write task-local evidence before reporting substantial work complete.
- Commit coherent subdeliverables with verbose bodies when queue work changes repo state.
"""
    return f"{AGENTS_BEGIN}\n{body}{AGENTS_END}\n"


def adapt_agents(repo_root: Path) -> Path:
    target = repo_root / "AGENTS.md"
    existing = read_text(target) if target.exists() else ""
    section = token_guidance_section().rstrip()
    if AGENTS_BEGIN in existing:
        start = existing.index(AGENTS_BEGIN)
        end = existing.index(AGENTS_END, start) + len(AGENTS_END)
        updated = existing[:start] + section + existing[end:]
    else:
        updated = existing.rstrip() + "\n\n" + section if existing.strip() else section
    write_text(target, updated)
    return target


def has_token_guidance(repo_root: Path) -> bool:
    path = repo_root / "AGENTS.md"
    return path.exists() and AGENTS_BEGIN in read_text(path)


def contains_section(text: str, section: str) -> bool:
    return re.search(rf"^##\s+{re.escape(section)}\s*$", text, re.MULTILINE) is not None


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
                text = read_text(candidate)
            except UnicodeDecodeError:
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    findings.append(normalize_rel(candidate.relative_to(repo_root)))
                    break
    return sorted(set(findings))


def validate_repo(repo_root: Path) -> tuple[bool, list[str]]:
    messages: list[str] = []
    ok = True
    for rel in REQUIRED_FILES:
        if not (repo_root / rel).exists():
            ok = False
            messages.append(f"FAIL missing required file: {rel}")
        else:
            messages.append(f"PASS required file: {rel}")

    budget_path = repo_root / ".aide/policies/token-budget.yaml"
    if budget_path.exists():
        budget_text = read_text(budget_path)
        for anchor in TOKEN_BUDGET_ANCHORS:
            if anchor not in budget_text:
                ok = False
                messages.append(f"FAIL token budget missing anchor: {anchor}")
        max_project = parse_int_value(budget_text, "max_project_state_tokens", 1600)
    else:
        max_project = 1600

    prompt_path = repo_root / ".aide/prompts/compact-task.md"
    if prompt_path.exists():
        prompt_text = read_text(prompt_path)
        for section in COMPACT_TASK_SECTIONS:
            if not contains_section(prompt_text, section):
                ok = False
                messages.append(f"FAIL compact task missing section: {section}")

    review_path = repo_root / ".aide/prompts/evidence-review.md"
    if review_path.exists():
        review_text = read_text(review_path)
        for decision in ["PASS", "PASS_WITH_NOTES", "REQUEST_CHANGES", "BLOCKED"]:
            if decision not in review_text:
                ok = False
                messages.append(f"FAIL evidence review missing decision: {decision}")

    ignore_patterns = load_ignore_patterns(repo_root)
    for pattern in REQUIRED_IGNORE_PATTERNS:
        if pattern not in ignore_patterns:
            ok = False
            messages.append(f"FAIL ignore policy missing exclusion: {pattern}")

    project_state = repo_root / ".aide/memory/project-state.md"
    if project_state.exists():
        stats = estimate_file(repo_root, ".aide/memory/project-state.md")
        if stats.approx_tokens > max_project:
            messages.append(
                f"WARN project state over max_project_state_tokens: {stats.approx_tokens} > {max_project}"
            )
        else:
            messages.append(f"PASS project state tokens: {stats.approx_tokens} <= {max_project}")

    secret_findings = scan_for_secrets(
        repo_root,
        [
            ".aide/policies",
            ".aide/prompts",
            ".aide/memory",
            ".aide/context/latest-task-packet.md",
            "AGENTS.md",
        ],
    )
    if secret_findings:
        ok = False
        messages.append(f"FAIL possible secret material: {', '.join(secret_findings)}")
    else:
        messages.append("PASS no obvious secrets in Q09 token-survival files")

    return ok, messages


def doctor(repo_root: Path) -> tuple[bool, list[str]]:
    messages: list[str] = []
    all_ok = True
    for rel in REQUIRED_FILES:
        exists = (repo_root / rel).exists()
        all_ok = all_ok and exists
        messages.append(f"{'PASS' if exists else 'FAIL'} required: {rel}")

    q08_status = repo_root / ".aide/queue/Q08-self-hosting-automation/status.yaml"
    q08_visible = q08_status.exists() and "status: passed" in read_text(q08_status)
    all_ok = all_ok and q08_visible
    messages.append(f"{'PASS' if q08_visible else 'FAIL'} Q08 passed state visible")

    agents_guidance = has_token_guidance(repo_root)
    messages.append(f"{'PASS' if agents_guidance else 'WARN'} AGENTS.md token-survival guidance")

    latest_packet = (repo_root / LATEST_PACKET_PATH).exists()
    messages.append(f"{'PASS' if latest_packet else 'WARN'} latest task packet exists")

    ignore_configured = (repo_root / ".aide/context/ignore.yaml").exists()
    all_ok = all_ok and ignore_configured
    messages.append(f"{'PASS' if ignore_configured else 'FAIL'} context ignore configured")
    return all_ok, messages


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
    target = write_snapshot(args.repo_root)
    snapshot = json.loads(read_text(target))
    print("AIDE Lite snapshot")
    print(f"path: {normalize_rel(target.relative_to(args.repo_root))}")
    print(f"file_count: {snapshot['file_count']}")
    print("contents_inline: false")
    return 0


def command_pack(args: argparse.Namespace) -> int:
    target = write_task_packet(args.repo_root, args.task)
    stats = estimate_file(args.repo_root, LATEST_PACKET_PATH)
    print("AIDE Lite pack")
    print(f"path: {normalize_rel(target.relative_to(args.repo_root))}")
    print(f"chars: {stats.chars}")
    print(f"approx_tokens: {stats.approx_tokens}")
    print("ledger: deferred to Q14")
    return 0


def command_adapt(args: argparse.Namespace) -> int:
    before = read_text(args.repo_root / "AGENTS.md") if (args.repo_root / "AGENTS.md").exists() else ""
    target = adapt_agents(args.repo_root)
    after = read_text(target)
    action = "unchanged" if before == after else "updated"
    print("AIDE Lite adapt")
    print(f"path: {normalize_rel(target.relative_to(args.repo_root))}")
    print(f"action: {action}")
    print("managed_section: q09-token-survival")
    return 0


def _write_minimal_repo(root: Path) -> None:
    for rel in REQUIRED_FILES:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
    write_text(root / ".aide/policies/token-budget.yaml", read_text(repo_root_from_script() / ".aide/policies/token-budget.yaml"))
    write_text(root / ".aide/memory/project-state.md", "# Project\n\nCompact state.\n")
    write_text(root / ".aide/memory/decisions.md", "# Decisions\n")
    write_text(root / ".aide/memory/open-risks.md", "# Risks\n")
    write_text(root / ".aide/prompts/compact-task.md", read_text(repo_root_from_script() / ".aide/prompts/compact-task.md"))
    write_text(root / ".aide/prompts/evidence-review.md", read_text(repo_root_from_script() / ".aide/prompts/evidence-review.md"))
    write_text(root / ".aide/prompts/codex-token-mode.md", read_text(repo_root_from_script() / ".aide/prompts/codex-token-mode.md"))
    write_text(root / ".aide/context/ignore.yaml", read_text(repo_root_from_script() / ".aide/context/ignore.yaml"))
    write_text(root / ".aide/queue/Q08-self-hosting-automation/status.yaml", "status: passed\n")
    write_text(root / "AGENTS.md", "# AGENTS\n")
    write_text(root / "README.md", "# README\n")
    write_text(root / "src/example.py", "print('hello')\n")
    write_text(root / ".env", "SHOULD_NOT_APPEAR=1\n")
    write_text(root / "node_modules/pkg/index.js", "ignored\n")


def run_selftest() -> tuple[bool, list[str]]:
    messages: list[str] = []
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _write_minimal_repo(root)
        stats = estimate_text("abcd")
        assert stats.approx_tokens == 1
        assert pattern_matches("core/harness/__pycache__/x.pyc", "__pycache__/**")
        assert pattern_matches("node_modules/pkg/index.js", "node_modules/**")
        assert pattern_matches(".env", ".env")
        snapshot_path = write_snapshot(root)
        snapshot = json.loads(read_text(snapshot_path))
        paths = [entry["path"] for entry in snapshot["files"]]
        assert ".env" not in paths
        assert all(not path.startswith("node_modules/") for path in paths)
        assert paths == sorted(paths)
        packet_path = write_task_packet(root, "Implement Q10 AIDE Lite hardening")
        packet = read_text(packet_path)
        for section in ["PHASE", "GOAL", "CONTEXT_REFS", "ACCEPTANCE", "TOKEN_ESTIMATE"]:
            assert f"## {section}" in packet
        assert "print('hello')" not in packet
        before = read_text(root / "AGENTS.md")
        adapt_agents(root)
        once = read_text(root / "AGENTS.md")
        adapt_agents(root)
        twice = read_text(root / "AGENTS.md")
        assert before != once
        assert once == twice
        ok, validate_messages = validate_repo(root)
        assert ok, "\n".join(validate_messages)
        messages.append("PASS internal estimate, ignore, snapshot, pack, adapt, and validate checks")
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

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.set_defaults(handler=command_doctor)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.set_defaults(handler=command_validate)

    estimate_parser = subparsers.add_parser("estimate")
    estimate_parser.add_argument("--file", required=True)
    estimate_parser.set_defaults(handler=command_estimate)

    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.set_defaults(handler=command_snapshot)

    pack_parser = subparsers.add_parser("pack")
    pack_parser.add_argument("--task", required=True)
    pack_parser.set_defaults(handler=command_pack)

    adapt_parser = subparsers.add_parser("adapt")
    adapt_parser.set_defaults(handler=command_adapt)

    selftest_parser = subparsers.add_parser("selftest")
    selftest_parser.set_defaults(handler=command_selftest)
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
