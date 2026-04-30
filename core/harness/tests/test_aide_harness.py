"""Lightweight standard-library tests for AIDE Harness v0."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from core.harness.commands import collect_validation_diagnostics
from core.harness.contract_loader import RepoContext, parse_top_level_scalars
from core.harness.diagnostics import has_errors
from core.harness.generated_artifacts import MANAGED_TARGETS, find_marker_block, render_section, replace_managed_section, sha256_text


class HarnessSmokeTests(unittest.TestCase):
    def test_help_smoke(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "aide"), "--help"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("AIDE Harness v0", result.stdout)

    def test_current_repo_validation_has_no_errors(self) -> None:
        diagnostics = collect_validation_diagnostics(RepoContext(ROOT))
        self.assertFalse(has_errors(diagnostics), "\n".join(f"{d.code}: {d.message}" for d in diagnostics))

    def test_missing_profile_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            diagnostics = collect_validation_diagnostics(RepoContext(Path(tmp)))
        self.assertTrue(has_errors(diagnostics))

    def test_top_level_scalar_reader(self) -> None:
        values = parse_top_level_scalars("schema_version: aide.test.v0\nnested:\n  status: planned\n")
        self.assertEqual(values["schema_version"], "aide.test.v0")
        self.assertEqual(values["nested"], "")
        self.assertNotIn("status", values)

    def test_generated_section_append_and_replace(self) -> None:
        spec = MANAGED_TARGETS[0]
        first_section, _ = render_section(spec, "first body\n")
        updated, action = replace_managed_section("manual law\n", spec, first_section)
        self.assertEqual(action, "append")
        self.assertIn("AIDE-GENERATED:BEGIN", updated)

        second_section, _ = render_section(spec, "second body\n")
        replaced, action = replace_managed_section(updated, spec, second_section)
        self.assertEqual(action, "replace")
        self.assertIn("second body", replaced)
        self.assertIn("manual law", replaced)

    def test_compile_dry_run_smoke(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "aide"), "compile", "--dry-run"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("generated_artifacts_are_canonical: false", result.stdout)

    def test_generated_marker_detects_body_drift(self) -> None:
        spec = MANAGED_TARGETS[0]
        section, _ = render_section(spec, "first body\n")
        drifted = section.replace("first body", "manual body")
        block = find_marker_block(drifted, spec.section)
        self.assertIsNotNone(block)
        assert block is not None
        self.assertNotEqual(block.fingerprint, sha256_text(block.body))


if __name__ == "__main__":
    unittest.main()
