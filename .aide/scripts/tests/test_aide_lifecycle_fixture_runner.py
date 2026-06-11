from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from core.apply import lifecycle_fixture_runner as runner


REPO_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = REPO_ROOT / ".aide/scripts/aide_lite.py"
SPEC = importlib.util.spec_from_file_location("aide_lite_lifecycle_fixture_runner", MODULE_PATH)
aide_lite = importlib.util.module_from_spec(SPEC)
sys.modules["aide_lite_lifecycle_fixture_runner"] = aide_lite
assert SPEC.loader is not None
SPEC.loader.exec_module(aide_lite)


COMMAND_VECTORS = [
    ["lifecycle-fixture", "status"],
    ["lifecycle-fixture", "run", "--scenario", "install-managed-section", "--mode", "apply-temp"],
    ["lifecycle-fixture", "verify"],
]

REQUIRED_FILES = [
    "core/apply/__init__.py",
    "core/apply/managed_sections.py",
    "core/apply/lifecycle_fixture_runner.py",
    ".aide/examples/apply/lifecycle-fixtures/scenarios.json",
    ".aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json",
    ".aide/examples/apply/lifecycle-fixtures/expected-reports/install-managed-section.report.json",
    ".aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json",
    ".aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/manual/with-managed-section.md",
    ".aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/manual/with-managed-section.md",
]


def copy_lifecycle_fixture_files(root: Path) -> None:
    for rel in REQUIRED_FILES:
        aide_lite.copy_pack_file(REPO_ROOT / rel, root / rel)


class AIDELifecycleFixtureRunnerTests(unittest.TestCase):
    def test_parser_accepts_lifecycle_fixture_commands(self) -> None:
        parser = aide_lite.build_parser(REPO_ROOT)
        for command in COMMAND_VECTORS:
            parsed = parser.parse_args(command)
            self.assertTrue(callable(getattr(parsed, "handler", None)), command)

    def test_run_mutates_temp_workspace_only_and_matches_expected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            copy_lifecycle_fixture_files(root)
            canonical = root / ".aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/manual/with-managed-section.md"
            expected = root / ".aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/manual/with-managed-section.md"
            before = canonical.read_text(encoding="utf-8")

            report = runner.run_lifecycle_fixture(root, workspace_name="test")

            after = canonical.read_text(encoding="utf-8")
            temp_target = root / str(report["temp_target_path"])
            self.assertEqual(before, after)
            self.assertEqual(temp_target.read_text(encoding="utf-8"), expected.read_text(encoding="utf-8"))
            self.assertEqual(report["capability_label"], "fixture_temp_apply_only")
            self.assertIn("active_repo_apply", report["not_capabilities"])
            self.assertFalse(report["canonical_fixture_mutated"])
            self.assertEqual(report["mutation_scope"], "temp_workspace_only")

    def test_verify_latest_completed_run_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            copy_lifecycle_fixture_files(root)
            runner.run_lifecycle_fixture(root, workspace_name="test")

            report = runner.verify_lifecycle_fixture(root)

            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["capability_label"], "fixture_temp_apply_only")
            failures = [check for check in report["checks"] if check["result"] == "FAIL"]
            self.assertEqual(failures, [])

    def test_verify_fails_closed_without_latest_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            copy_lifecycle_fixture_files(root)

            report = runner.verify_lifecycle_fixture(root)

            self.assertEqual(report["status"], "FAIL")
            self.assertTrue((root / ".aide/reports/lifecycle-fixture-runner/latest-verify.json").exists())

    def test_cli_status_run_and_verify_use_temp_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            copy_lifecycle_fixture_files(root)
            parser = aide_lite.build_parser(root)

            status_args = parser.parse_args(["lifecycle-fixture", "status"])
            run_args = parser.parse_args(["lifecycle-fixture", "run", "--scenario", "install-managed-section", "--mode", "apply-temp"])
            verify_args = parser.parse_args(["lifecycle-fixture", "verify"])

            self.assertEqual(status_args.handler(status_args), 0)
            self.assertEqual(run_args.handler(run_args), 0)
            self.assertEqual(verify_args.handler(verify_args), 0)

    def test_path_jail_rejects_absolute_and_parent_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            workspace.mkdir()
            with self.assertRaises(runner.PathJailError):
                runner.resolve_under_jail(workspace, "../outside.md")
            with self.assertRaises(runner.PathJailError):
                runner.resolve_under_jail(workspace, "C:/outside.md")

    def test_path_jail_rejects_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "workspace"
            outside = root / "outside"
            workspace.mkdir()
            outside.mkdir()
            outside_file = outside / "fixture.md"
            outside_file.write_text("outside\n", encoding="utf-8")
            link = workspace / "link.md"
            try:
                link.symlink_to(outside_file)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink unavailable: {exc}")
            with self.assertRaises(runner.PathJailError):
                runner.resolve_under_jail(workspace, "link.md")


if __name__ == "__main__":
    unittest.main()
