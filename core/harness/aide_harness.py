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

    compile_parser = subparsers.add_parser("compile", help="Print a deterministic compile plan without generated outputs.")
    compile_parser.set_defaults(handler=run_compile)

    validate_parser = subparsers.add_parser("validate", help="Validate local Profile/Contract and queue structure.")
    validate_parser.set_defaults(handler=run_validate)

    doctor_parser = subparsers.add_parser("doctor", help="Print actionable diagnostics and next repair steps.")
    doctor_parser.set_defaults(handler=run_doctor)

    migrate_parser = subparsers.add_parser("migrate", help="Report no-op migration baseline posture.")
    migrate_parser.set_defaults(handler=run_migrate)

    bakeoff_parser = subparsers.add_parser("bakeoff", help="Report bakeoff metadata readiness without external calls.")
    bakeoff_parser.set_defaults(handler=run_bakeoff)

    return parser


def main(default_repo_root: Path | None = None, argv: list[str] | None = None) -> int:
    root = default_repo_root or Path.cwd()
    parser = build_parser(root)
    args = parser.parse_args(argv)
    ctx = RepoContext(Path(args.repo_root).resolve())
    return int(args.handler(args, ctx))
