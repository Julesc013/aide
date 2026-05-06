"""Generated artifact helpers for AIDE Harness v0.

This module intentionally uses deterministic text generation and small
line-oriented manifest parsing. It is not a general YAML parser.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from .contract_loader import ContractReadError, RepoContext
from .diagnostics import Diagnostic


GENERATOR_NAME = "aide-harness-generated-artifacts-v0"
GENERATOR_VERSION = "q05.generated-artifacts.v0"
MANIFEST_PATH = ".aide/generated/manifest.yaml"
PREVIEW_CLAUDE_PATH = ".aide/generated/preview/CLAUDE.md"

SOURCE_PATHS = [
    ".aide/profile.yaml",
    ".aide/toolchain.lock",
    ".aide/commands/catalog.yaml",
    ".aide/queue/policy.yaml",
    ".aide/queue/index.yaml",
    "docs/reference/source-of-truth.md",
    "docs/reference/harness-v0.md",
    "docs/reference/generated-artifacts-v0.md",
]


@dataclass(frozen=True)
class TargetSpec:
    path: str
    section: str
    mode: str
    status: str
    manual_policy: str
    description: str
    source_paths: tuple[str, ...] = tuple(SOURCE_PATHS)


@dataclass(frozen=True)
class TargetPlan:
    spec: TargetSpec
    body: str
    section_text: str
    content_fingerprint: str


@dataclass(frozen=True)
class GenerationPlan:
    source_fingerprint: str
    targets: list[TargetPlan]
    deferred_targets: list[TargetSpec]
    manifest_text: str


@dataclass(frozen=True)
class Operation:
    path: str
    action: str
    detail: str


@dataclass(frozen=True)
class MarkerBlock:
    start: str
    body: str
    end: str
    fingerprint: str | None


MANAGED_TARGETS = [
    TargetSpec(
        path="AGENTS.md",
        section="aide-self-hosting-summary",
        mode="managed-section",
        status="managed",
        manual_policy="outside-only",
        description="Root agent law receives a bounded generated summary; manual law remains outside markers.",
    ),
    TargetSpec(
        path=".agents/skills/aide-queue/SKILL.md",
        section="aide-queue-source-summary",
        mode="managed-section",
        status="managed",
        manual_policy="outside-only",
        description="Queue skill receives a generated source-of-truth summary.",
    ),
    TargetSpec(
        path=".agents/skills/aide-execplan/SKILL.md",
        section="aide-execplan-source-summary",
        mode="managed-section",
        status="managed",
        manual_policy="outside-only",
        description="ExecPlan skill receives a generated source-of-truth summary.",
    ),
    TargetSpec(
        path=".agents/skills/aide-review/SKILL.md",
        section="aide-review-source-summary",
        mode="managed-section",
        status="managed",
        manual_policy="outside-only",
        description="Review skill receives a generated review-gate summary.",
    ),
]

PREVIEW_TARGETS = [
    TargetSpec(
        path=PREVIEW_CLAUDE_PATH,
        section="claude-md-preview",
        mode="generated-preview",
        status="preview",
        manual_policy="preview-only",
        description="Claude guidance preview only; final root CLAUDE.md is deferred.",
    )
]

DEFERRED_TARGETS = [
    TargetSpec(
        path=".claude/settings.json",
        section="claude-settings",
        mode="deferred",
        status="deferred",
        manual_policy="deferred",
        description="Final Claude settings are deferred; Q05 adds no hooks or auto-execution.",
    ),
    TargetSpec(
        path=".claude/agents/*",
        section="claude-agents",
        mode="deferred",
        status="deferred",
        manual_policy="deferred",
        description="Final Claude subagents are deferred; Q05 defines no autonomous bypass agents.",
    ),
]


def normalize_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in normalized.splitlines()]
    return "\n".join(lines).strip() + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def _read_source(ctx: RepoContext, relative: str) -> str:
    try:
        return ctx.read_text(relative)
    except ContractReadError:
        return ""


def source_fingerprint(ctx: RepoContext, paths: tuple[str, ...] | list[str] = SOURCE_PATHS) -> str:
    chunks = []
    for path in paths:
        content = _read_source(ctx, path)
        chunks.append(f"path:{path}\n{normalize_text(content)}")
    return sha256_text("\n---\n".join(chunks))


def _sources_value(paths: tuple[str, ...]) -> str:
    return ",".join(paths)


def render_section(spec: TargetSpec, body: str) -> tuple[str, str]:
    body = normalize_text(body)
    fingerprint = sha256_text(body)
    start = (
        f"<!-- AIDE-GENERATED:BEGIN section={spec.section} "
        f"generator={GENERATOR_NAME} version={GENERATOR_VERSION} "
        f"mode={spec.mode} sources={_sources_value(spec.source_paths)} "
        f"fingerprint=sha256:{fingerprint} manual={spec.manual_policy} -->"
    )
    end = f"<!-- AIDE-GENERATED:END section={spec.section} -->"
    return f"{start}\n{body}{end}\n", fingerprint


def _root_agents_body() -> str:
    return """## Generated AIDE Contract Summary

- Canonical Profile/Contract source: `.aide/`.
- Canonical long-running work queue: `.aide/queue/`.
- Generated downstream artifacts are compiled or managed outputs, not canonical truth.
- Non-trivial work must route through AIDE intake or the filesystem queue and produce evidence.
- Current accepted foundation includes Contract/Profile v0, Harness v0, Compatibility baseline records, the AIDE-side Dominium Bridge baseline, and report-first self-hosting automation.
- Runtime, full Hosts, Gateway, providers, Commander, Mobile, app surfaces, and real Dominium Bridge implementation remain deferred until queue items authorize them.
"""


def _queue_skill_body() -> str:
    return """## Generated AIDE Source Summary

- Read `.aide/profile.yaml`, `.aide/queue/policy.yaml`, and the active queue packet before editing.
- `.aide/queue/` is canonical for long-running task state; extension task queues are not canonical.
- Generated downstream artifacts are not source of truth and must preserve provenance markers.
- Stop at review gates, write evidence, and keep changes inside the task allowlist.
"""


def _execplan_skill_body() -> str:
    return """## Generated AIDE Source Summary

- ExecPlans are the restartable control document for long-running AIDE queue work.
- Keep Progress, discoveries, decisions, validation, recovery, evidence, and retrospective current while work runs.
- Do not use an ExecPlan to widen scope beyond the queue task allowlist.
- Generated outputs must be treated as reviewable downstream artifacts, not canonical plans.
"""


def _review_skill_body() -> str:
    return """## Generated AIDE Source Summary

- Review outcomes are `PASS`, `PASS_WITH_NOTES`, or `REQUEST_CHANGES` unless a task defines a stricter blocker.
- Check scope, evidence, validation, source-of-truth boundaries, generated markers, and review-gate handling.
- Generated downstream artifacts must be deterministic, manifest-backed, and non-canonical.
- Q06 Compatibility, Q07 Dominium Bridge, Runtime, Hosts, and provider work remain out of Q05 review scope.
"""


def _claude_preview_body() -> str:
    return """# Claude Guidance Preview

This file is a Q05 generated preview. It is not canonical and is not the final root `CLAUDE.md`.

Use the canonical AIDE records instead:

- `.aide/profile.yaml` for the self-hosting Profile/Contract.
- `.aide/queue/` for long-running task execution state.
- `AGENTS.md` for root operating law.
- `docs/reference/source-of-truth.md` for source-of-truth boundaries.

Operational summary for Claude-style agents:

- Preserve bootstrap-era history.
- Route non-trivial work through the filesystem queue.
- Keep generated outputs deterministic, marked, and reviewable.
- Do not implement Runtime, Hosts, Dominium Bridge, Compatibility baseline, provider adapters, app surfaces, or Q06+ work without an explicit queue item.
"""


def body_for(spec: TargetSpec) -> str:
    if spec.section == "aide-self-hosting-summary":
        return _root_agents_body()
    if spec.section == "aide-queue-source-summary":
        return _queue_skill_body()
    if spec.section == "aide-execplan-source-summary":
        return _execplan_skill_body()
    if spec.section == "aide-review-source-summary":
        return _review_skill_body()
    if spec.section == "claude-md-preview":
        return _claude_preview_body()
    return ""


def build_generation_plan(ctx: RepoContext) -> GenerationPlan:
    current_source_fingerprint = source_fingerprint(ctx)
    targets: list[TargetPlan] = []
    for spec in [*MANAGED_TARGETS, *PREVIEW_TARGETS]:
        body = body_for(spec)
        section_text, content_fingerprint = render_section(spec, body)
        targets.append(TargetPlan(spec, normalize_text(body), section_text, content_fingerprint))
    manifest_text = render_manifest(current_source_fingerprint, targets, DEFERRED_TARGETS)
    return GenerationPlan(current_source_fingerprint, targets, DEFERRED_TARGETS, manifest_text)


def find_marker_block(text: str, section: str) -> MarkerBlock | None:
    start_pattern = re.compile(
        rf"<!-- AIDE-GENERATED:BEGIN section={re.escape(section)} (?P<meta>.*?) -->\n",
        re.DOTALL,
    )
    start_match = start_pattern.search(text)
    if not start_match:
        return None
    end_text = f"<!-- AIDE-GENERATED:END section={section} -->"
    end_index = text.find(end_text, start_match.end())
    if end_index == -1:
        return MarkerBlock(start_match.group(0), text[start_match.end() :], "", _fingerprint_from_start(start_match.group(0)))
    end_end = end_index + len(end_text)
    body = text[start_match.end() : end_index]
    return MarkerBlock(
        text[start_match.start() : start_match.end()].rstrip("\n"),
        body,
        text[end_index:end_end],
        _fingerprint_from_start(start_match.group(0)),
    )


def _fingerprint_from_start(start: str) -> str | None:
    match = re.search(r"fingerprint=sha256:([0-9a-f]{64})", start)
    return match.group(1) if match else None


def replace_managed_section(existing: str, spec: TargetSpec, rendered_section: str) -> tuple[str, str]:
    block = find_marker_block(existing, spec.section)
    if block is None:
        separator = "\n\n" if existing.strip() else ""
        return existing.rstrip() + separator + rendered_section, "append"
    if not block.end:
        raise ValueError(f"managed section {spec.section} is missing an end marker")

    start_pattern = re.compile(
        rf"<!-- AIDE-GENERATED:BEGIN section={re.escape(spec.section)} .*? -->\n",
        re.DOTALL,
    )
    start_match = start_pattern.search(existing)
    assert start_match is not None
    end_text = f"<!-- AIDE-GENERATED:END section={spec.section} -->"
    end_index = existing.find(end_text, start_match.end())
    end_end = end_index + len(end_text)
    old_section = existing[start_match.start() : end_end]
    new_section = rendered_section.rstrip("\n")
    if old_section == new_section:
        return existing, "unchanged"
    return existing[: start_match.start()] + new_section + existing[end_end:], "replace"


def preview_file_text(target: TargetPlan) -> str:
    return (
        "# AIDE Generated Preview\n\n"
        "This preview is non-canonical. Do not treat it as repository law until a future review promotes it.\n\n"
        f"{target.section_text}"
    )


def write_preview_targets(ctx: RepoContext, plan: GenerationPlan) -> list[Operation]:
    operations: list[Operation] = []
    for target in plan.targets:
        if target.spec.mode != "generated-preview":
            continue
        path = ctx.path(target.spec.path)
        text = preview_file_text(target)
        if path.exists():
            existing = path.read_text(encoding="utf-8")
            if "AIDE-GENERATED:BEGIN" not in existing:
                operations.append(Operation(target.spec.path, "blocked", "existing preview target lacks AIDE markers"))
                continue
            if normalize_text(existing) == normalize_text(text):
                operations.append(Operation(target.spec.path, "unchanged", "preview target already current"))
                continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        operations.append(Operation(target.spec.path, "write", "preview target written"))
    return operations


def write_managed_targets(ctx: RepoContext, plan: GenerationPlan) -> list[Operation]:
    operations: list[Operation] = []
    for target in plan.targets:
        if target.spec.mode != "managed-section":
            continue
        path = ctx.path(target.spec.path)
        if not path.exists():
            operations.append(Operation(target.spec.path, "blocked", "managed target is missing"))
            continue
        existing = path.read_text(encoding="utf-8")
        try:
            updated, action = replace_managed_section(existing, target.spec, target.section_text)
        except ValueError as exc:
            operations.append(Operation(target.spec.path, "blocked", str(exc)))
            continue
        if action != "unchanged":
            path.write_text(updated, encoding="utf-8", newline="\n")
        operations.append(Operation(target.spec.path, action, f"managed section {target.spec.section}"))
    return operations


def write_manifest(ctx: RepoContext, plan: GenerationPlan) -> Operation:
    path = ctx.path(MANIFEST_PATH)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if "schema_version: aide.generated-manifest.v0" not in existing:
            return Operation(MANIFEST_PATH, "blocked", "existing manifest does not look like AIDE generated manifest v0")
        if normalize_text(existing) == normalize_text(plan.manifest_text):
            return Operation(MANIFEST_PATH, "unchanged", "manifest already current")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(plan.manifest_text, encoding="utf-8", newline="\n")
    return Operation(MANIFEST_PATH, "write", "manifest written")


def render_manifest(source_fp: str, targets: list[TargetPlan], deferred: list[TargetSpec]) -> str:
    lines = [
        "schema_version: aide.generated-manifest.v0",
        f"generator: {GENERATOR_NAME}",
        f"generator_version: {GENERATOR_VERSION}",
        f"source_fingerprint: sha256:{source_fp}",
        "canonical_sources:",
    ]
    for source in SOURCE_PATHS:
        lines.append(f"  - {source}")
    lines.extend(["targets:"])
    for target in targets:
        lines.extend(
            [
                f"  - path: {target.spec.path}",
                f"    section: {target.spec.section}",
                f"    mode: {target.spec.mode}",
                f"    status: {target.spec.status}",
                f"    manual_edit_policy: {target.spec.manual_policy}",
                "    marker_style: markdown-comment",
                f"    source_fingerprint: sha256:{source_fp}",
                f"    content_fingerprint: sha256:{target.content_fingerprint}",
                "    sources:",
            ]
        )
        for source in target.spec.source_paths:
            lines.append(f"      - {source}")
    for spec in deferred:
        lines.extend(
            [
                f"  - path: {spec.path}",
                f"    section: {spec.section}",
                f"    mode: {spec.mode}",
                f"    status: {spec.status}",
                f"    manual_edit_policy: {spec.manual_policy}",
                "    marker_style: none",
                f"    source_fingerprint: sha256:{source_fp}",
                "    content_fingerprint: none",
                "    sources:",
            ]
        )
        for source in spec.source_paths:
            lines.append(f"      - {source}")
    lines.extend(
        [
            "validation_expectations:",
            "  - py -3 scripts/aide validate",
            "  - py -3 scripts/aide compile --dry-run",
            "  - py -3 scripts/aide compile --write",
            "",
        ]
    )
    return "\n".join(lines)


def planned_operations(ctx: RepoContext, plan: GenerationPlan) -> list[Operation]:
    operations: list[Operation] = []
    for target in plan.targets:
        path = ctx.path(target.spec.path)
        if target.spec.mode == "managed-section":
            if not path.exists():
                operations.append(Operation(target.spec.path, "would_block", "managed target is missing"))
                continue
            try:
                updated, action = replace_managed_section(path.read_text(encoding="utf-8"), target.spec, target.section_text)
            except ValueError as exc:
                operations.append(Operation(target.spec.path, "would_block", str(exc)))
                continue
            operations.append(
                Operation(
                    target.spec.path,
                    "would_" + ("keep" if action == "unchanged" else action),
                    "managed section current" if normalize_text(updated) == normalize_text(path.read_text(encoding="utf-8")) else "managed section would change",
                )
            )
        elif target.spec.mode == "generated-preview":
            if path.exists():
                existing = path.read_text(encoding="utf-8")
                if "AIDE-GENERATED:BEGIN" not in existing:
                    operations.append(Operation(target.spec.path, "would_block", "existing preview target lacks AIDE markers"))
                elif normalize_text(existing) == normalize_text(preview_file_text(target)):
                    operations.append(Operation(target.spec.path, "would_keep", "preview already current"))
                else:
                    operations.append(Operation(target.spec.path, "would_replace", "preview would be refreshed"))
            else:
                operations.append(Operation(target.spec.path, "would_write", "preview would be created"))
    if ctx.exists(MANIFEST_PATH):
        existing = ctx.read_text(MANIFEST_PATH)
        action = "would_keep" if normalize_text(existing) == normalize_text(plan.manifest_text) else "would_replace"
    else:
        action = "would_write"
    operations.append(Operation(MANIFEST_PATH, action, "manifest"))
    for spec in DEFERRED_TARGETS:
        operations.append(Operation(spec.path, "deferred", spec.description))
    return operations


def parse_manifest_targets(text: str) -> dict[str, dict[str, str]]:
    targets: dict[str, dict[str, str]] = {}
    current: dict[str, str] | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("- path:"):
            path = stripped.split(":", 1)[1].strip()
            current = {"path": path}
            targets[path] = current
            continue
        if current is None or not stripped or stripped.startswith("- "):
            continue
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip()
    return targets


def _validate_marker(ctx: RepoContext, target: TargetPlan, manifest_entry: dict[str, str] | None) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not ctx.exists(target.spec.path):
        diagnostics.append(
            Diagnostic(
                "GENERATED-MISSING",
                "error",
                "required generated target is missing",
                target.spec.path,
                "run py -3 scripts/aide compile --write from the repo root",
            )
        )
        return diagnostics
    text = ctx.read_text(target.spec.path)
    block = find_marker_block(text, target.spec.section)
    if block is None or not block.end:
        diagnostics.append(
            Diagnostic(
                "GENERATED-MARKER",
                "error",
                "generated target is missing required AIDE markers",
                target.spec.path,
                "restore the managed section by running py -3 scripts/aide compile --write",
            )
        )
        return diagnostics
    body_fingerprint = sha256_text(block.body)
    if block.fingerprint != body_fingerprint:
        diagnostics.append(
            Diagnostic(
                "GENERATED-MANUAL-EDIT",
                "error",
                "generated section fingerprint does not match its body",
                target.spec.path,
                "move manual edits outside the generated section or regenerate it",
            )
        )
    elif target.content_fingerprint != body_fingerprint:
        diagnostics.append(
            Diagnostic(
                "GENERATED-STALE-CONTENT",
                "warning",
                "generated section is stale relative to the current generator body",
                target.spec.path,
                "run py -3 scripts/aide compile --write and review the diff",
            )
        )
    else:
        diagnostics.append(Diagnostic("GENERATED-CURRENT", "info", "generated target is current", target.spec.path))

    if manifest_entry is None:
        diagnostics.append(
            Diagnostic(
                "GENERATED-MANIFEST-ENTRY",
                "error",
                "generated target has no manifest entry",
                target.spec.path,
                "regenerate the manifest with py -3 scripts/aide compile --write",
            )
        )
    else:
        manifest_fp = manifest_entry.get("content_fingerprint", "").removeprefix("sha256:")
        if manifest_fp != target.content_fingerprint:
            diagnostics.append(
                Diagnostic(
                    "GENERATED-MANIFEST-STALE",
                    "warning",
                    "manifest content fingerprint is stale",
                    target.spec.path,
                    "regenerate the manifest with py -3 scripts/aide compile --write",
                )
            )
    return diagnostics


def collect_generated_artifact_diagnostics(ctx: RepoContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    plan = build_generation_plan(ctx)

    if ctx.exists("CLAUDE.md"):
        diagnostics.append(
            Diagnostic(
                "GENERATED-FINAL-CLAUDE",
                "error",
                "final root CLAUDE.md exists but Q05 policy keeps Claude guidance preview-only",
                "CLAUDE.md",
                "remove the final target or replace it with an approved future generated artifact policy",
            )
        )
    if ctx.exists(".claude"):
        diagnostics.append(
            Diagnostic(
                "GENERATED-FINAL-CLAUDE-DIR",
                "error",
                "final .claude/ directory exists but Q05 policy defers final Claude targets",
                ".claude",
                "remove the final target or use the preview path under .aide/generated/preview/",
            )
        )

    if not ctx.exists(MANIFEST_PATH):
        diagnostics.append(
            Diagnostic(
                "GENERATED-MANIFEST",
                "warning",
                "generated artifact manifest is missing",
                MANIFEST_PATH,
                "run py -3 scripts/aide compile --write after Q05 implementation is authorized",
            )
        )
        return diagnostics

    manifest_text = ctx.read_text(MANIFEST_PATH)
    if "schema_version: aide.generated-manifest.v0" not in manifest_text:
        diagnostics.append(Diagnostic("GENERATED-MANIFEST-SCHEMA", "error", "manifest schema marker is missing", MANIFEST_PATH))
        return diagnostics

    expected_source_fp = f"sha256:{plan.source_fingerprint}"
    if f"source_fingerprint: {expected_source_fp}" not in manifest_text:
        diagnostics.append(
            Diagnostic(
                "GENERATED-SOURCE-STALE",
                "warning",
                "manifest source fingerprint is stale",
                MANIFEST_PATH,
                "run py -3 scripts/aide compile --write and review generated changes",
            )
        )
    else:
        diagnostics.append(Diagnostic("GENERATED-SOURCE-CURRENT", "info", "manifest source fingerprint is current", MANIFEST_PATH))

    manifest_targets = parse_manifest_targets(manifest_text)
    for target in plan.targets:
        diagnostics.extend(_validate_marker(ctx, target, manifest_targets.get(target.spec.path)))
    for spec in DEFERRED_TARGETS:
        entry = manifest_targets.get(spec.path)
        if entry is None:
            diagnostics.append(Diagnostic("GENERATED-DEFERRED-MISSING", "warning", "deferred target is missing from manifest", spec.path))
        else:
            diagnostics.append(Diagnostic("GENERATED-DEFERRED", "info", "target is intentionally deferred", spec.path))
    return diagnostics
