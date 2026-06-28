"""Rollback verification for DistributionApplyEngine v0 temp workspaces."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.distribution.temp_workspace import restore_snapshot, snapshot_tree


def verify_rollback(
    workspace_root: Path,
    before_snapshot: dict[str, str],
    before_contents: dict[str, str],
    scenario: dict[str, Any],
) -> dict[str, Any]:
    if scenario.get("rollback_digest_mismatch"):
        return {
            "status": "FAILED_VALIDATION",
            "refusal_code": "distribution_apply_engine.rollback_digest_mismatch_refused",
            "rollback_verified": False,
        }
    restore_snapshot(workspace_root, before_snapshot, before_contents)
    after = snapshot_tree(workspace_root)
    verified = after == before_snapshot
    return {
        "status": "PASS_WITH_WARNINGS" if verified else "FAILED_VALIDATION",
        "refusal_code": None if verified else "distribution_apply_engine.rollback_verification_failed",
        "rollback_verified": verified,
    }
