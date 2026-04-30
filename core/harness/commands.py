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
    ".aide/compat/migration-baseline.yaml",
]

SOURCE_OF_TRUTH_DOCS = [
    "docs/reference/profile-contract-v0.md",
    "docs/reference/source-of-truth.md",
    "docs/reference/generated-artifacts-v0.md",
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

QUEUE_IDS = [
    "Q00-bootstrap-audit",
    "Q01-documentation-split",
    "Q02-structural-skeleton",
    "Q03-profile-contract-v0",
    "Q04-harness-v0",
    "Q05-generated-artifacts-v0",
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

    diagnostics.extend(collect_generated_artifact_diagnostics(ctx))

    return diagnostics


def run_validate(args: Namespace, ctx: RepoContext) -> int:
    diagnostics = collect_validation_diagnostics(ctx)
    print(render_report("AIDE Harness v0 validate", diagnostics))
    print()
    print("validation_model: structural file, directory, anchor, and queue checks only")
    print("full_yaml_schema_validation: not implemented in Q04")
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
    print("- Q05 should stop at needs_review after implementation evidence is recorded.")
    print("- Compatibility baseline remains Q06; Dominium Bridge baseline remains Q07.")
    print()
    print("next_recommended_step: Q05 implementation or review according to .aide/queue/Q05-generated-artifacts-v0/status.yaml")
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
    diagnostics: list[Diagnostic] = []
    profile_text = _read_or_error(ctx, ".aide/profile.yaml", diagnostics, "MIGRATE-PROFILE")
    compat_text = _read_or_error(ctx, ".aide/compat/schema-version.yaml", diagnostics, "MIGRATE-COMPAT")
    baseline_text = _read_or_error(ctx, ".aide/compat/migration-baseline.yaml", diagnostics, "MIGRATE-BASELINE")

    profile_values = parse_top_level_scalars(profile_text) if profile_text else {}
    compat_values = parse_top_level_scalars(compat_text) if compat_text else {}
    baseline_values = parse_top_level_scalars(baseline_text) if baseline_text else {}

    print("AIDE Harness v0 migrate")
    print("mode: no-op baseline report")
    print(f"profile_contract_version: {profile_values.get('profile_contract_version', 'unknown')}")
    print(f"compat_schema_status: {compat_values.get('status', 'unknown')}")
    print(f"migration_baseline_status: {baseline_values.get('status', 'unknown')}")
    print("migration_engine: not implemented")
    print("automatic_migrations: none")
    print("q06_compatibility_baseline: deferred")
    if has_errors(diagnostics):
        print()
        print(render_report("migration diagnostics", diagnostics))
        return 1
    print("migration_needed: no executable migration is defined for Harness v0")
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
    print("q06_compatibility_smoke: deferred")
    if has_errors(diagnostics):
        print()
        print(render_report("bakeoff diagnostics", diagnostics))
        return 1
    return 0
