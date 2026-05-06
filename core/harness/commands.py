"""Command handlers for AIDE Harness v0."""

from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from .contract_loader import (
    ContractReadError,
    RepoContext,
    list_item_ids,
    parse_queue_index,
    parse_status_file,
    parse_top_level_scalars,
)
from .diagnostics import Diagnostic, has_errors, render_report, status_label
from .generated_artifacts import (
    build_generation_plan,
    collect_generated_artifact_diagnostics,
    planned_operations,
    write_managed_targets,
    write_manifest,
    write_preview_targets,
)
from core.compat.migration_registry import migration_entries, mutating_migrations_available
from core.compat.version_registry import BASELINE_VERSION, collect_version_findings, known_surfaces


REQUIRED_AIDE_DIRS = [
    ".aide/components",
    ".aide/commands",
    ".aide/policies",
    ".aide/tasks",
    ".aide/evals",
    ".aide/adapters",
    ".aide/compat",
    ".aide/queue",
]

REQUIRED_AIDE_FILES = [
    ".aide/profile.yaml",
    ".aide/toolchain.lock",
    ".aide/components/catalog.yaml",
    ".aide/commands/catalog.yaml",
    ".aide/tasks/catalog.yaml",
    ".aide/evals/catalog.yaml",
    ".aide/adapters/catalog.yaml",
    ".aide/policies/autonomy.yaml",
    ".aide/policies/bypass.yaml",
    ".aide/policies/review-gates.yaml",
    ".aide/policies/ownership.yaml",
    ".aide/policies/generated-artifacts.yaml",
    ".aide/policies/compatibility.yaml",
    ".aide/policies/validation-severity.yaml",
    ".aide/compat/schema-version.yaml",
    ".aide/compat/schema-versions.yaml",
    ".aide/compat/migration-baseline.yaml",
    ".aide/compat/replay-corpus.yaml",
    ".aide/compat/upgrade-gates.yaml",
    ".aide/compat/deprecations.yaml",
]

SOURCE_OF_TRUTH_DOCS = [
    "docs/reference/profile-contract-v0.md",
    "docs/reference/source-of-truth.md",
    "docs/reference/generated-artifacts-v0.md",
    "docs/reference/compatibility-baseline.md",
    "docs/reference/self-hosting-automation.md",
]

HARNESS_FILES = [
    "scripts/aide",
    "core/harness/README.md",
    "core/harness/aide_harness.py",
    "core/harness/commands.py",
    "core/harness/contract_loader.py",
    "core/harness/diagnostics.py",
    "core/harness/generated_artifacts.py",
]

COMPAT_FILES = [
    "core/compat/README.md",
    "core/compat/__init__.py",
    "core/compat/version_registry.py",
    "core/compat/migration_registry.py",
    "core/compat/replay_manifest.py",
]

DOMINIUM_BRIDGE_FILES = [
    "docs/reference/dominium-bridge.md",
    "bridges/dominium/README.md",
    "bridges/dominium/bridge.yaml",
    "bridges/dominium/adoption.md",
    "bridges/dominium/validation.md",
    "bridges/dominium/compatibility.yaml",
    "bridges/dominium/xstack/README.md",
    "bridges/dominium/xstack/scope.md",
    "bridges/dominium/xstack/portable-mapping.yaml",
    "bridges/dominium/profiles/README.md",
    "bridges/dominium/profiles/dominium-xstack.profile.yaml",
    "bridges/dominium/policies/README.md",
    "bridges/dominium/policies/review-gates.yaml",
    "bridges/dominium/policies/proof-gates.yaml",
    "bridges/dominium/policies/generated-artifacts.yaml",
    "bridges/dominium/generators/README.md",
    "bridges/dominium/generators/targets.yaml",
]

DOMINIUM_BRIDGE_ANCHORS = [
    ("bridges/dominium/bridge.yaml", "schema_version: aide.dominium-bridge.v0", "DOMINIUM-BRIDGE-VERSION"),
    ("bridges/dominium/bridge.yaml", "external_dominium_repo_mutation: prohibited", "DOMINIUM-BRIDGE-NO-EXTERNAL"),
    ("bridges/dominium/xstack/scope.md", "XStack is Dominium-local and strict", "DOMINIUM-XSTACK-LOCAL"),
    ("bridges/dominium/xstack/portable-mapping.yaml", "generic_aide_product_layer: false", "DOMINIUM-XSTACK-NOT-GENERIC"),
    ("bridges/dominium/profiles/dominium-xstack.profile.yaml", "replaces_aide_profile: false", "DOMINIUM-PROFILE-OVERLAY"),
    ("bridges/dominium/policies/review-gates.yaml", "base_policy_relation: stricter-than-aide", "DOMINIUM-REVIEW-STRICT"),
    ("bridges/dominium/policies/proof-gates.yaml", "base_policy_relation: stricter-than-aide", "DOMINIUM-PROOF-STRICT"),
    ("bridges/dominium/policies/generated-artifacts.yaml", "emits_outputs: false", "DOMINIUM-GENERATED-NO-OUTPUT"),
    ("bridges/dominium/generators/targets.yaml", "emits_outputs: false", "DOMINIUM-TARGETS-NO-OUTPUT"),
    ("bridges/dominium/compatibility.yaml", "compatibility_baseline_version: aide.compat-baseline.v0", "DOMINIUM-COMPAT-Q06"),
    ("docs/reference/dominium-bridge.md", "Q07 implements only AIDE-side bridge metadata", "DOMINIUM-REFERENCE-BOUNDARY"),
]

DOMINIUM_BRIDGE_TARGET_CLASSES = [
    ("dominium-agents-md", "AGENTS.md managed sections", "deferred metadata only"),
    ("dominium-agent-skills", ".agents/skills/*", "deferred metadata only"),
    ("claude-guidance", "CLAUDE.md or .claude/**", "deferred metadata only"),
    ("codex-guidance", "future Codex target files", "deferred metadata only"),
    ("openhands-guidance", "future OpenHands target files", "deferred metadata only"),
    ("bridge-adoption-report", "future bridge adoption report", "deferred metadata only"),
]

QUEUE_IDS = [
    "Q00-bootstrap-audit",
    "Q01-documentation-split",
    "Q02-structural-skeleton",
    "Q03-profile-contract-v0",
    "Q04-harness-v0",
    "Q05-generated-artifacts-v0",
    "Q06-compatibility-baseline",
    "Q07-dominium-bridge-baseline",
    "Q08-self-hosting-automation",
]

QUEUE_PACKET_FILES = [
    "task.yaml",
    "ExecPlan.md",
    "prompt.md",
    "status.yaml",
]

Q04_EVIDENCE_FILES = [
    "changed-files.md",
    "validation.md",
    "command-smoke.md",
    "remaining-risks.md",
]

PROFILE_ANCHORS = [
    "schema_version:",
    "profile_contract_version:",
    "profile_id:",
    "profile_mode:",
    "repo_identity:",
    "lifecycle:",
    "public_model:",
    "internal_core_split:",
    "first_shipped_stack:",
    "source_of_truth:",
    "implemented_reality:",
]

TOOLCHAIN_ANCHORS = [
    "schema_version:",
    "profile_contract_version:",
    "profile_schema_version:",
    "queue_policy_version:",
    "harness:",
    "generated_artifacts:",
]

COMMAND_IDS = [
    "queue-status",
    "queue-next",
    "queue-run-skeleton",
    "aide-init",
    "aide-import",
    "aide-compile",
    "aide-validate",
    "aide-doctor",
    "aide-migrate",
    "aide-bakeoff",
    "aide-self-check",
]

SELF_CHECK_REPORT_DIR = ".aide/runs/self-check"
SELF_CHECK_DEFAULT_REPORT = f"{SELF_CHECK_REPORT_DIR}/latest.md"
ACCEPTED_REVIEW_OUTCOMES = {"PASS", "PASS_WITH_NOTES"}
REVIEW_OUTCOME_MARKERS = [
    "BLOCK_Q08",
    "BLOCK_Q07",
    "BLOCK_Q06",
    "BLOCK_Q05",
    "REQUEST_CHANGES",
    "PASS_WITH_NOTES",
    "PASS",
]


def _check_file(ctx: RepoContext, relative: str, diagnostics: list[Diagnostic], code: str) -> None:
    if ctx.exists(relative):
        diagnostics.append(Diagnostic(code, "info", "required file exists", relative))
    else:
        diagnostics.append(
            Diagnostic(
                code,
                "error",
                "required file is missing",
                relative,
                "restore this file or rerun the queue item that owns it",
            )
        )


def _check_dir(ctx: RepoContext, relative: str, diagnostics: list[Diagnostic], code: str) -> None:
    if ctx.is_dir(relative):
        diagnostics.append(Diagnostic(code, "info", "required directory exists", relative))
    else:
        diagnostics.append(
            Diagnostic(
                code,
                "error",
                "required directory is missing",
                relative,
                "restore this directory or rerun the queue item that owns it",
            )
        )


def _read_or_error(ctx: RepoContext, relative: str, diagnostics: list[Diagnostic], code: str) -> str:
    try:
        return ctx.read_text(relative)
    except ContractReadError as exc:
        diagnostics.append(Diagnostic(code, "error", str(exc), relative))
        return ""


def _collect_compatibility_diagnostics(ctx: RepoContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for finding in collect_version_findings(ctx.root):
        diagnostics.append(Diagnostic(finding.code, finding.severity, finding.message, finding.path, finding.hint))
    return diagnostics


def _collect_dominium_bridge_diagnostics(ctx: RepoContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for index, relative in enumerate(DOMINIUM_BRIDGE_FILES, start=1):
        if ctx.exists(relative):
            diagnostics.append(Diagnostic(f"DOMINIUM-FILE-{index:02d}", "info", "Dominium Bridge file exists", relative))
        else:
            diagnostics.append(
                Diagnostic(
                    f"DOMINIUM-FILE-{index:02d}",
                    "error",
                    "Dominium Bridge required file is missing",
                    relative,
                    "restore the Q07 bridge baseline file or rerun the Q07 implementation task",
                )
            )

    for relative, anchor, code in DOMINIUM_BRIDGE_ANCHORS:
        text = _read_or_error(ctx, relative, diagnostics, f"{code}-READ")
        if text and anchor in text:
            diagnostics.append(Diagnostic(code, "info", "Dominium Bridge boundary anchor is present", relative))
        elif text:
            diagnostics.append(
                Diagnostic(
                    code,
                    "error",
                    f"Dominium Bridge boundary anchor is missing: {anchor}",
                    relative,
                    "restore the strict Q07 bridge boundary before relying on the bridge",
                )
            )
    return diagnostics


def _queue_items(ctx: RepoContext) -> list[dict[str, str]]:
    try:
        return parse_queue_index(ctx.read_text(".aide/queue/index.yaml"))
    except ContractReadError:
        return []


def _status_values(ctx: RepoContext, queue_id: str) -> dict[str, str]:
    path = f".aide/queue/{queue_id}/status.yaml"
    if not ctx.exists(path):
        return {}
    try:
        return parse_status_file(ctx.read_text(path))
    except ContractReadError:
        return {}


def _review_outcome(ctx: RepoContext, queue_id: str) -> str:
    path = f".aide/queue/{queue_id}/evidence/review.md"
    if not ctx.exists(path):
        return "none"
    try:
        text = ctx.read_text(path)
    except ContractReadError:
        return "unreadable"
    for marker in REVIEW_OUTCOME_MARKERS:
        if marker in text:
            return marker
    return "present"


def _accepted_for_dependency(ctx: RepoContext, queue_id: str, status: str) -> str:
    if status == "passed":
        return "yes"
    outcome = _review_outcome(ctx, queue_id)
    if outcome in ACCEPTED_REVIEW_OUTCOMES:
        return "yes-by-review-evidence"
    return "no"


def _next_recommended_step(ctx: RepoContext, diagnostics: list[Diagnostic]) -> str:
    if has_errors(diagnostics):
        return "fix hard validation errors before running automation or continuing the queue"

    q08_status = _status_values(ctx, "Q08-self-hosting-automation").get("status")
    if q08_status in {"running", "claimed"}:
        return "finish Q08 implementation evidence and move Q08 to review"
    if q08_status == "needs_review":
        return "Q08 review according to .aide/queue/Q08-self-hosting-automation/status.yaml"
    if q08_status == "passed":
        later_step = _next_later_queue_step(ctx, after=8)
        if later_step:
            return later_step
        return "post-Q08 foundation review, then plan the next reviewed queue item"
    if q08_status == "pending":
        return "Q08 implementation according to .aide/queue/Q08-self-hosting-automation/prompt.md"

    for item in _queue_items(ctx):
        status = item.get("status", "")
        queue_id = item.get("id", "unknown")
        if status == "pending":
            return f"{queue_id} implementation according to {item.get('prompt', 'its prompt.md')}"
        if status == "needs_review" and _accepted_for_dependency(ctx, queue_id, status) == "no":
            return f"{queue_id} review according to .aide/queue/{queue_id}/status.yaml"
    return "no pending queue item found; run a foundation review before adding new work"


def _queue_number(queue_id: str) -> int | None:
    if not queue_id.startswith("Q") or len(queue_id) < 3:
        return None
    digits = queue_id[1:3]
    if not digits.isdigit():
        return None
    return int(digits)


def _next_later_queue_step(ctx: RepoContext, after: int) -> str:
    for item in _queue_items(ctx):
        queue_id = item.get("id", "unknown")
        queue_number = _queue_number(queue_id)
        if queue_number is None or queue_number <= after:
            continue
        status = _status_values(ctx, queue_id).get("status", item.get("status", "unknown"))
        if status in {"claimed", "planning", "running"}:
            return f"{queue_id} implementation according to {item.get('prompt', 'its prompt.md')}"
        if status == "needs_review" and _accepted_for_dependency(ctx, queue_id, status) == "no":
            return f"{queue_id} review according to .aide/queue/{queue_id}/status.yaml"
        if status == "pending":
            return f"{queue_id} implementation according to {item.get('prompt', 'its prompt.md')}"
    return ""


def _queue_health_lines(ctx: RepoContext) -> list[str]:
    lines: list[str] = []
    for item in _queue_items(ctx):
        queue_id = item.get("id", "unknown")
        status = _status_values(ctx, queue_id).get("status", item.get("status", "unknown"))
        planning_state = item.get("planning_state", "unknown")
        review_outcome = _review_outcome(ctx, queue_id)
        accepted = _accepted_for_dependency(ctx, queue_id, status)
        lines.append(
            f"- {queue_id}: status={status}; planning_state={planning_state}; "
            f"review_outcome={review_outcome}; accepted_for_dependency={accepted}"
        )
    if not lines:
        lines.append("- queue index could not be read")
    return lines


def _generated_drift_lines(ctx: RepoContext, diagnostics: list[Diagnostic]) -> list[str]:
    plan = build_generation_plan(ctx)
    operations = planned_operations(ctx, plan)
    lines = [f"- source_fingerprint: sha256:{plan.source_fingerprint}"]
    stale_diagnostics = [diagnostic for diagnostic in diagnostics if diagnostic.code == "GENERATED-SOURCE-STALE"]
    manifest_operations = [operation for operation in operations if operation.path == ".aide/generated/manifest.yaml"]
    if stale_diagnostics:
        lines.append("- manifest_source_fingerprint: stale")
        lines.append("- handling: report-only; Q08 does not refresh generated artifacts")
    else:
        lines.append("- manifest_source_fingerprint: current")
    for operation in manifest_operations:
        lines.append(f"- manifest_operation_if_compile_write: {operation.action} ({operation.detail})")
    lines.append("- generated_artifacts_refreshed: false")
    return lines


def _compatibility_smoke_lines() -> list[str]:
    lines = [f"- baseline_version: {BASELINE_VERSION}"]
    for surface in known_surfaces():
        lines.append(f"- {surface.id}: {surface.current_version} ({surface.status})")
    lines.append(f"- mutating_migrations_available: {str(mutating_migrations_available()).lower()}")
    return lines


def _dominium_bridge_status_lines(ctx: RepoContext) -> list[str]:
    diagnostics = _collect_dominium_bridge_diagnostics(ctx)
    dominium_errors = [diagnostic for diagnostic in diagnostics if diagnostic.severity == "error"]
    if dominium_errors:
        return [f"- status: error ({len(dominium_errors)} missing bridge checks)"]
    return [
        "- status: structural baseline present",
        "- external_dominium_repo_mutation: prohibited",
        "- real_dominium_outputs_written: false",
    ]


def build_self_check_report(ctx: RepoContext) -> str:
    diagnostics = collect_validation_diagnostics(ctx)
    info_count = sum(1 for diagnostic in diagnostics if diagnostic.severity == "info")
    warning_count = sum(1 for diagnostic in diagnostics if diagnostic.severity == "warning")
    error_count = sum(1 for diagnostic in diagnostics if diagnostic.severity == "error")

    lines = [
        "AIDE self-check",
        "mode: report-only",
        "mutation: none",
        "canonical: false",
        "external_calls: none",
        "provider_or_model_calls: none",
        "network_calls: none",
        "automatic_worker_invocation: false",
        "queue_auto_merge: false",
        "",
        "validation:",
        f"- status: {status_label(diagnostics)}",
        f"- info: {info_count}",
        f"- warning: {warning_count}",
        f"- error: {error_count}",
        "",
        "queue_health:",
        *_queue_health_lines(ctx),
        "",
        "review_gate_nuance:",
        "- Q00-Q03 raw statuses remain needs_review; foundation review evidence allowed later work to proceed with notes.",
        "- Q05 and Q06 raw statuses remain needs_review even though review evidence records PASS_WITH_NOTES.",
        "- Q07 is passed; doctor guidance should no longer point to Q07 review.",
        "",
        "generated_artifact_drift:",
        *_generated_drift_lines(ctx, diagnostics),
        "",
        "compatibility_smoke:",
        *_compatibility_smoke_lines(),
        "",
        "dominium_bridge_status:",
        *_dominium_bridge_status_lines(ctx),
        "",
        "proposed_followups:",
        "- Q09 token-survival review after this implementation stops at needs_review.",
        "- Reviewed generated-artifact refresh if .aide/generated/manifest.yaml source fingerprint drift remains.",
        "- Queue/status reconciliation QFIX if future automation needs raw statuses to match accepted review evidence.",
        "- Continue to keep Runtime, Service, Commander, Hosts, providers, Gateway, mobile, MCP/A2A, and autonomous loops deferred until reviewed queue items authorize them.",
        "",
        f"next_recommended_step: {_next_recommended_step(ctx, diagnostics)}",
    ]
    return "\n".join(lines)


def _safe_self_check_report_path(ctx: RepoContext, requested: str) -> Path:
    base = (ctx.root / SELF_CHECK_REPORT_DIR).resolve()
    target = (ctx.root / requested).resolve()
    try:
        target.relative_to(base)
    except ValueError as exc:
        raise ValueError(f"self-check reports must stay under {SELF_CHECK_REPORT_DIR}") from exc
    return target


def collect_validation_diagnostics(ctx: RepoContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for index, relative in enumerate(REQUIRED_AIDE_DIRS, start=1):
        _check_dir(ctx, relative, diagnostics, f"AIDE-DIR-{index:02d}")
    for index, relative in enumerate(REQUIRED_AIDE_FILES, start=1):
        _check_file(ctx, relative, diagnostics, f"AIDE-FILE-{index:02d}")
    for index, relative in enumerate(SOURCE_OF_TRUTH_DOCS, start=1):
        _check_file(ctx, relative, diagnostics, f"DOC-SOT-{index:02d}")
    for index, relative in enumerate(HARNESS_FILES, start=1):
        _check_file(ctx, relative, diagnostics, f"HARNESS-FILE-{index:02d}")
    for index, relative in enumerate(COMPAT_FILES, start=1):
        _check_file(ctx, relative, diagnostics, f"COMPAT-FILE-{index:02d}")

    profile_text = _read_or_error(ctx, ".aide/profile.yaml", diagnostics, "PROFILE-READ")
    if profile_text:
        for anchor in PROFILE_ANCHORS:
            if anchor not in profile_text:
                diagnostics.append(
                    Diagnostic(
                        "PROFILE-ANCHOR",
                        "error",
                        f"profile anchor is missing: {anchor}",
                        ".aide/profile.yaml",
                    )
                )
        profile_values = parse_top_level_scalars(profile_text)
        if profile_values.get("profile_mode") != "self-hosting":
            diagnostics.append(
                Diagnostic(
                    "PROFILE-MODE",
                    "error",
                    "profile_mode must be self-hosting for this repo",
                    ".aide/profile.yaml",
                )
            )
        if "harness_v0: not_implemented" in profile_text:
            diagnostics.append(
                Diagnostic(
                    "PROFILE-HARNESS-STALE",
                    "warning",
                    "profile still records harness_v0 as not_implemented",
                    ".aide/profile.yaml",
                    "refresh this through the bounded Q05 metadata update before generation",
                )
            )

    toolchain_text = _read_or_error(ctx, ".aide/toolchain.lock", diagnostics, "TOOLCHAIN-READ")
    if toolchain_text:
        for anchor in TOOLCHAIN_ANCHORS:
            if anchor not in toolchain_text:
                diagnostics.append(
                    Diagnostic(
                        "TOOLCHAIN-ANCHOR",
                        "error",
                        f"toolchain lock anchor is missing: {anchor}",
                        ".aide/toolchain.lock",
                    )
                )
        if "executable_harness_commands: not_implemented" in toolchain_text:
            diagnostics.append(
                Diagnostic(
                    "TOOLCHAIN-HARNESS-STALE",
                    "warning",
                    "toolchain lock still records executable Harness commands as not_implemented",
                    ".aide/toolchain.lock",
                    "refresh this through the bounded Q05 metadata update before generation",
                )
            )

    command_catalog = _read_or_error(ctx, ".aide/commands/catalog.yaml", diagnostics, "COMMANDS-READ")
    if command_catalog:
        command_ids = set(list_item_ids(command_catalog))
        for command_id in COMMAND_IDS:
            if command_id not in command_ids:
                diagnostics.append(
                    Diagnostic(
                        "COMMAND-ID",
                        "error",
                        f"command catalog is missing id {command_id}",
                        ".aide/commands/catalog.yaml",
                    )
                )
        if "future-harness-command" in command_catalog and "status: planned" in command_catalog:
            diagnostics.append(
                Diagnostic(
                    "COMMAND-CATALOG-PLANNED",
                    "warning",
                    "command catalog still marks Harness commands as planned",
                    ".aide/commands/catalog.yaml",
                    "refresh this through the bounded Q05 metadata update before generation",
                )
            )

    queue_index_text = _read_or_error(ctx, ".aide/queue/index.yaml", diagnostics, "QUEUE-INDEX-READ")
    queue_items: list[dict[str, str]] = []
    if queue_index_text:
        queue_items = parse_queue_index(queue_index_text)
        if not queue_items:
            diagnostics.append(Diagnostic("QUEUE-INDEX-EMPTY", "error", "queue index has no items", ".aide/queue/index.yaml"))
        item_by_id = {item.get("id", ""): item for item in queue_items}
        for queue_id in QUEUE_IDS:
            if queue_id not in item_by_id:
                diagnostics.append(
                    Diagnostic("QUEUE-ID", "error", f"queue index is missing {queue_id}", ".aide/queue/index.yaml")
                )

        for queue_id in QUEUE_IDS:
            base = f".aide/queue/{queue_id}"
            for filename in QUEUE_PACKET_FILES:
                _check_file(ctx, f"{base}/{filename}", diagnostics, f"QUEUE-PACKET-{queue_id}")
            _check_dir(ctx, f"{base}/evidence", diagnostics, f"QUEUE-EVIDENCE-{queue_id}")

            status_path = f"{base}/status.yaml"
            if ctx.exists(status_path):
                status_values = parse_status_file(_read_or_error(ctx, status_path, diagnostics, f"STATUS-READ-{queue_id}"))
                status_file_status = status_values.get("status")
                index_status = item_by_id.get(queue_id, {}).get("status")
                if status_file_status and index_status and status_file_status != index_status:
                    diagnostics.append(
                        Diagnostic(
                            "QUEUE-STATUS-MISMATCH",
                            "warning",
                            f"{queue_id} status file says {status_file_status} but index says {index_status}",
                            status_path,
                            "keep index.yaml and task status.yaml aligned when queue status changes",
                        )
                    )
                if status_file_status == "needs_review":
                    diagnostics.append(
                        Diagnostic(
                            "QUEUE-REVIEW-GATE",
                            "warning",
                            f"{queue_id} is waiting at a review gate",
                            status_path,
                            "do not treat this queue item as accepted until a review records the outcome",
                        )
                    )

        for evidence_file in Q04_EVIDENCE_FILES:
            _check_file(
                ctx,
                f".aide/queue/Q04-harness-v0/evidence/{evidence_file}",
                diagnostics,
                "Q04-EVIDENCE",
            )

        q04_status = item_by_id.get("Q04-harness-v0", {}).get("status")
        q05_status = item_by_id.get("Q05-generated-artifacts-v0", {}).get("status")
        if q04_status == "needs_review" and q05_status == "pending":
            diagnostics.append(
                Diagnostic(
                    "QUEUE-NEXT-RISK",
                    "warning",
                    "Q05 is pending while Q04 is still needs_review",
                    ".aide/queue/index.yaml",
                    "run Q04 review before starting Q05; the queue helper is order-based and not dependency-aware",
                )
            )

    diagnostics.extend(_collect_compatibility_diagnostics(ctx))
    diagnostics.extend(_collect_dominium_bridge_diagnostics(ctx))
    diagnostics.extend(collect_generated_artifact_diagnostics(ctx))

    return diagnostics


def run_validate(args: Namespace, ctx: RepoContext) -> int:
    diagnostics = collect_validation_diagnostics(ctx)
    print(render_report("AIDE Harness v0 validate", diagnostics))
    print()
    print("validation_model: structural file, directory, anchor, and queue checks only")
    print("full_yaml_schema_validation: not implemented in Harness v0")
    return 1 if has_errors(diagnostics) else 0


def run_doctor(args: Namespace, ctx: RepoContext) -> int:
    diagnostics = collect_validation_diagnostics(ctx)
    print(render_report("AIDE Harness v0 doctor", diagnostics))
    print()
    print("diagnosis:")
    if has_errors(diagnostics):
        print("- Fix error diagnostics first; they indicate missing required setup or unreadable contract records.")
    else:
        print("- No hard structural errors were found.")
    print("- Q00-Q03 still require review before their outputs are formally accepted.")
    print("- Q04 has passed review; Q05 owns generated artifact markers, previews, and drift checks.")
    print("- Q05 review evidence records PASS_WITH_NOTES; raw status remains needs_review to avoid hidden generated drift.")
    print("- Q06 compatibility baseline records known v0 versions and no-op migration posture.")
    print("- Q07 Dominium Bridge baseline is AIDE-side only; Harness checks required bridge records and boundary anchors.")
    print("- Dominium repo mutation and real Dominium generated outputs remain out of scope.")
    if any(diagnostic.code == "GENERATED-SOURCE-STALE" for diagnostic in diagnostics):
        print("- Generated artifact manifest source fingerprint is stale; Harness reports it and does not refresh artifacts without a reviewed write path.")
    print("- Q08 self-check is report-first and does not invoke external agents, providers, models, or network calls.")
    print()
    print(f"next_recommended_step: {_next_recommended_step(ctx, diagnostics)}")
    return 1 if has_errors(diagnostics) else 0


def run_self_check(args: Namespace, ctx: RepoContext) -> int:
    diagnostics = collect_validation_diagnostics(ctx)
    report = build_self_check_report(ctx)
    print(report)
    if args.write_report:
        try:
            report_path = _safe_self_check_report_path(ctx, args.output)
        except ValueError as exc:
            print()
            print(f"report_write: false")
            print(f"error: {exc}")
            return 1
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report + "\n", encoding="utf-8")
        print()
        print("report_write: true")
        print(f"report_path: {report_path.relative_to(ctx.root).as_posix()}")
        print("report_canonical: false")
    return 1 if has_errors(diagnostics) else 0


def run_init(args: Namespace, ctx: RepoContext) -> int:
    print("AIDE Harness v0 init")
    print(f"repo_root: {ctx.root}")
    print("mode: non-destructive")
    if args.dry_run:
        print("dry_run: true")
    if ctx.exists(".aide/profile.yaml"):
        print("status: already_initialized")
        print("detail: .aide/profile.yaml exists; Harness v0 will not overwrite existing contract records.")
        return 0
    print("status: not_initialized")
    print("detail: Harness v0 init reports only; future scaffold creation requires reviewed policy.")
    return 0


def run_import(args: Namespace, ctx: RepoContext) -> int:
    surfaces = [
        ("AGENTS.md", "root agent law"),
        (".agents/skills", "repo-local skills"),
        (".aide", "AIDE Profile/Contract and queue"),
        ("CLAUDE.md", "future generated Claude guidance"),
        (".claude", "future generated Claude directory"),
    ]
    print("AIDE Harness v0 import")
    print("mode: report-only")
    for path, description in surfaces:
        state = "present" if ctx.exists(path) else "absent"
        print(f"- {path}: {state} ({description})")
    print("mutation: none")
    print("canonical_contract_rewrite: false")
    return 0


def run_compile(args: Namespace, ctx: RepoContext) -> int:
    diagnostics = collect_validation_diagnostics(ctx)
    plan = build_generation_plan(ctx)
    operations = planned_operations(ctx, plan)
    mode = "write" if args.write else "preview" if args.preview else "dry-run"
    print("AIDE Harness v0 compile")
    print(f"validation_status: {status_label(diagnostics)}")
    print(f"mode: {mode}")
    if args.write:
        print("mutation: approved managed sections, preview files, and manifest")
    elif args.preview:
        print("mutation: preview files under .aide/generated/preview only")
    else:
        print("mutation: none")
    print("generated_artifacts_are_canonical: false")
    print(f"generator: {plan.manifest_text.splitlines()[1].split(': ', 1)[1]}")
    print(f"source_fingerprint: sha256:{plan.source_fingerprint}")
    print()
    print("source_inputs:")
    for path in plan.targets[0].spec.source_paths:
        print(f"- {path}")
    print()
    print("target_operations:")
    for operation in operations:
        print(f"- {operation.path}: {operation.action} ({operation.detail})")
    print()
    print("target_policy:")
    print("- AGENTS.md and existing AIDE skills: managed sections")
    print("- CLAUDE.md: preview only under .aide/generated/preview/CLAUDE.md")
    print("- .claude/settings.json and final .claude/agents/**: deferred")
    print("- Dominium Bridge targets: plan only; no real Dominium outputs are emitted")
    print()
    print("dominium_bridge_target_plan:")
    for target_id, target, posture in DOMINIUM_BRIDGE_TARGET_CLASSES:
        print(f"- {target_id}: {target} ({posture})")
    print("dominium_bridge_outputs_written: false")
    print()
    if has_errors(diagnostics):
        print("write_allowed: false")
        print("reason: validation has hard errors")
        return 1

    if args.preview:
        executed = write_preview_targets(ctx, plan)
        print("preview_results:")
        for operation in executed:
            print(f"- {operation.path}: {operation.action} ({operation.detail})")
        return 1 if any(operation.action == "blocked" for operation in executed) else 0

    if args.write:
        executed = [*write_managed_targets(ctx, plan), *write_preview_targets(ctx, plan)]
        manifest_operation = write_manifest(ctx, plan)
        executed.append(manifest_operation)
        print("write_results:")
        for operation in executed:
            print(f"- {operation.path}: {operation.action} ({operation.detail})")
        print()
        print("generated_artifacts_written: true")
        return 1 if any(operation.action == "blocked" for operation in executed) else 0

    print("generated_artifacts_written: false")
    return 0


def run_migrate(args: Namespace, ctx: RepoContext) -> int:
    diagnostics = _collect_compatibility_diagnostics(ctx)
    entries = migration_entries()
    print("AIDE Harness v0 migrate")
    print("mode: compatibility baseline report")
    print(f"compatibility_baseline_version: {BASELINE_VERSION}")
    print("mutation: none")
    print("migration_engine: no-op-current-baseline")
    print("automatic_migrations: none")
    print(f"mutating_migrations_available: {str(mutating_migrations_available()).lower()}")
    print()
    print("current_versions:")
    for surface in known_surfaces():
        print(f"- {surface.id}: {surface.current_version} ({surface.status}; source={surface.source_path})")
    print()
    print("available_migrations:")
    for entry in entries:
        print(f"- {entry.id}: {entry.source_version} -> {entry.target_version} ({entry.status}; mutates_repo={str(entry.mutates_repo).lower()})")
    print()
    print("unknown_future_versions: error")
    print("q06_compatibility_baseline: implemented-v0")
    if has_errors(diagnostics):
        print()
        print(render_report("migration diagnostics", diagnostics))
        return 1
    print("migration_needed: false")
    return 0


def run_bakeoff(args: Namespace, ctx: RepoContext) -> int:
    diagnostics: list[Diagnostic] = []
    eval_text = _read_or_error(ctx, ".aide/evals/catalog.yaml", diagnostics, "BAKEOFF-EVALS")
    eval_ids = list_item_ids(eval_text) if eval_text else []

    print("AIDE Harness v0 bakeoff")
    print("mode: metadata/readiness only")
    print("external_calls: none")
    print("provider_or_model_calls: none")
    print("native_host_calls: none")
    print("network_calls: none")
    print()
    print("declared_eval_ids:")
    if eval_ids:
        for eval_id in eval_ids:
            print(f"- {eval_id}")
    else:
        print("- none")
    print()
    print("executable_bakeoff_scenarios: none in Harness v0")
    print("q06_compatibility_smoke: structural replay baseline available")
    if has_errors(diagnostics):
        print()
        print(render_report("bakeoff diagnostics", diagnostics))
        return 1
    return 0
