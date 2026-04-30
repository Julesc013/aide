"""AIDE Harness v0 command-line dispatcher."""

from __future__ import annotations

import argparse
from pathlib import Path

from .commands import (
    run_bakeoff,
    run_compile,
    run_doctor,
    run_import,
    run_init,
    run_migrate,
    run_self_check,
    run_validate,
)
from .contract_loader import RepoContext


def build_parser(default_repo_root: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aide",
        description="AIDE Harness v0: local structural checks for the self-hosting Profile/Contract.",
    )
    parser.add_argument(
        "--repo-root",
        default=str(default_repo_root),
        help="Repository root to inspect. Defaults to the root containing scripts/aide.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Report initialization posture without overwriting .aide/.")
    init_parser.add_argument("--dry-run", action="store_true", help="Report planned init behavior without writing files.")
    init_parser.set_defaults(handler=run_init)

    import_parser = subparsers.add_parser("import", help="Report importable guidance surfaces without rewriting contract files.")
    import_parser.set_defaults(handler=run_import)

    compile_parser = subparsers.add_parser("compile", help="Compile or preview deterministic generated artifacts.")
    compile_mode = compile_parser.add_mutually_exclusive_group()
    compile_mode.add_argument("--dry-run", action="store_true", help="Print the deterministic generation plan without writing files.")
    compile_mode.add_argument("--preview", action="store_true", help="Write preview-only generated artifacts under .aide/generated/preview/.")
    compile_mode.add_argument("--write", action="store_true", help="Write approved managed sections, previews, and manifest records.")
    compile_parser.set_defaults(handler=run_compile)

    validate_parser = subparsers.add_parser("validate", help="Validate local Profile/Contract and queue structure.")
    validate_parser.set_defaults(handler=run_validate)

    doctor_parser = subparsers.add_parser("doctor", help="Print actionable diagnostics and next repair steps.")
    doctor_parser.set_defaults(handler=run_doctor)

    migrate_parser = subparsers.add_parser("migrate", help="Report no-op migration baseline posture.")
    migrate_parser.set_defaults(handler=run_migrate)

    bakeoff_parser = subparsers.add_parser("bakeoff", help="Report bakeoff metadata readiness without external calls.")
    bakeoff_parser.set_defaults(handler=run_bakeoff)

    self_check_parser = subparsers.add_parser("self-check", help="Run report-first self-hosting checks without external calls.")
    self_check_parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write the deterministic report under .aide/runs/self-check/.",
    )
    self_check_parser.add_argument(
        "--output",
        default=".aide/runs/self-check/latest.md",
        help="Report path to use with --write-report. Must stay under .aide/runs/self-check/.",
    )
    self_check_parser.set_defaults(handler=run_self_check)

    return parser


def main(default_repo_root: Path | None = None, argv: list[str] | None = None) -> int:
    root = default_repo_root or Path.cwd()
    parser = build_parser(root)
    args = parser.parse_args(argv)
    ctx = RepoContext(Path(args.repo_root).resolve())
    return int(args.handler(args, ctx))
