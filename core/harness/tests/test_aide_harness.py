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


if __name__ == "__main__":
    unittest.main()
