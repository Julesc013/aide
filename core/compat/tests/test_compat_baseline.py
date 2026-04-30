"""Lightweight tests for Q06 Compatibility baseline helpers."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from core.compat.migration_registry import migration_entries, mutating_migrations_available
from core.compat.replay_manifest import replay_expectations
from core.compat.version_registry import (
    BASELINE_VERSION,
    classify_version,
    collect_version_findings,
    known_version_map,
)


class CompatibilityBaselineTests(unittest.TestCase):
    def test_known_versions_include_required_baselines(self) -> None:
        versions = known_version_map()
        self.assertEqual(versions["profile"], "aide.profile.v0")
        self.assertEqual(versions["generated_manifest"], "aide.generated-manifest.v0")
        self.assertEqual(versions["compatibility_baseline"], BASELINE_VERSION)

    def test_unknown_future_versions_are_errors(self) -> None:
        classification, severity = classify_version("profile", "aide.profile.v99")
        self.assertEqual(classification, "unknown_or_future")
        self.assertEqual(severity, "error")

    def test_current_migration_registry_is_noop(self) -> None:
        entries = migration_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].id, "baseline-current-noop")
        self.assertFalse(entries[0].mutates_repo)
        self.assertFalse(mutating_migrations_available())

    def test_replay_manifest_is_structural(self) -> None:
        commands = {expectation.command for expectation in replay_expectations()}
        self.assertIn("py -3 scripts/aide validate", commands)
        self.assertIn("py -3 scripts/aide migrate", commands)

    def test_current_repo_compatibility_records_have_no_errors(self) -> None:
        findings = collect_version_findings(ROOT)
        errors = [finding for finding in findings if finding.severity == "error"]
        self.assertEqual([], errors, "\n".join(f"{finding.code}: {finding.message}" for finding in errors))


if __name__ == "__main__":
    unittest.main()
