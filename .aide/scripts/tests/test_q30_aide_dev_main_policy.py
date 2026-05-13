from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = REPO_ROOT / ".aide/scripts/aide_lite.py"
SPEC = importlib.util.spec_from_file_location("aide_lite_q30", MODULE_PATH)
aide_lite = importlib.util.module_from_spec(SPEC)
sys.modules["aide_lite_q30"] = aide_lite
assert SPEC.loader is not None
SPEC.loader.exec_module(aide_lite)


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def git_fixture(with_dev: bool = False):
    seen: list[tuple[str, ...]] = []

    def fake_git(_root: Path, args: list[str]) -> tuple[bool, str, str]:
        seen.append(tuple(args))
        local = "main\ndev" if with_dev else "main"
        remote = "origin/main\norigin/dev" if with_dev else "origin/main"
        outputs = {
            ("branch", "--show-current"): "main",
            ("rev-parse", "HEAD"): "abc123",
            ("branch", "--format=%(refname:short)"): local,
            ("branch", "--remotes", "--format=%(refname:short)"): remote,
            ("tag", "--list"): "",
            ("remote", "-v"): "origin https://github.com/Julesc013/aide.git (fetch)\norigin https://github.com/Julesc013/aide.git (push)",
            ("status", "--short"): "",
            ("rev-parse", "--show-toplevel"): "C:/fixture/aide",
            ("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"): "origin/main",
            ("rev-list", "--left-right", "--count", "HEAD...@{u}"): "0 0",
        }
        key = tuple(args)
        if key in outputs:
            return True, outputs[key], ""
        return False, "", f"unexpected git args: {' '.join(args)}"

    return seen, fake_git


def fake_status_code(_root: Path, args: list[str]) -> tuple[int, str, str]:
    if args[:2] == ["rev-list", "--left-right"]:
        return 0, "0 0", ""
    if args[:2] == ["merge-base", "--is-ancestor"]:
        return 1, "", ""
    return 0, "", ""


class Q30AideDevMainPolicyTests(unittest.TestCase):
    def test_aide_branch_policy_validates(self) -> None:
        checks = aide_lite.validate_aide_branch_policy_files(REPO_ROOT)
        failures = [check.message for check in checks if check.severity == "FAIL"]
        self.assertEqual(failures, [])

    def test_main_and_dev_roles_are_fixed(self) -> None:
        policy = aide_lite.read_text(REPO_ROOT / aide_lite.AIDE_BRANCH_POLICY_PATH)
        self.assertIn("main: canonical", policy)
        self.assertIn("dev: integration", policy)
        self.assertNotIn("dev: canonical", policy)

    def test_q30_live_mutation_flag_is_false(self) -> None:
        plan = json.loads(aide_lite.read_text(REPO_ROOT / aide_lite.AIDE_DEV_MAIN_PLAN_JSON_PATH))
        self.assertTrue(plan["non_mutating"])
        self.assertFalse(plan["live_mutation_performed"])
        self.assertFalse(plan["helper_dry_run_results"]["plan"]["remote_mutation"])

    def test_helper_plan_output_includes_current_branch_and_role(self) -> None:
        plan = aide_lite.make_git_helper_plan(REPO_ROOT, "plan", dry_run=True)
        self.assertIn("current_branch", plan["state"])
        self.assertIn("current_role", plan["state"])

    def test_missing_dev_produces_plan_not_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root, aide_lite.AIDE_BRANCH_POLICY_PATH, aide_lite.read_text(REPO_ROOT / aide_lite.AIDE_BRANCH_POLICY_PATH))
            seen, fake_git = git_fixture(with_dev=False)
            with mock.patch.object(aide_lite, "run_git_capture", side_effect=fake_git), mock.patch.object(aide_lite, "run_git_status_code", side_effect=fake_status_code):
                plan = aide_lite.make_aide_dev_main_plan(root)
        self.assertFalse(plan["local_dev_exists"])
        self.assertFalse(plan["remote_origin_dev_exists"])
        self.assertTrue(plan["future_explicit_operator_plan"]["required_if_dev_missing"])
        self.assertIn("git switch -c dev main", plan["future_explicit_operator_plan"]["commands_not_run"])
        self.assertFalse(plan["live_mutation_performed"])
        flattened = " ".join(" ".join(args) for args in seen)
        for forbidden in ["checkout -b", "switch -c", "push", "merge --no-ff", "branch -d", "branch -D"]:
            self.assertNotIn(forbidden, flattened)

    def test_existing_dev_branch_is_integration(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root, aide_lite.AIDE_BRANCH_POLICY_PATH, aide_lite.read_text(REPO_ROOT / aide_lite.AIDE_BRANCH_POLICY_PATH))
            _seen, fake_git = git_fixture(with_dev=True)
            with mock.patch.object(aide_lite, "run_git_capture", side_effect=fake_git), mock.patch.object(aide_lite, "run_git_status_code", side_effect=fake_status_code):
                plan = aide_lite.make_aide_dev_main_plan(root)
        self.assertTrue(plan["local_dev_exists"])
        self.assertTrue(plan["remote_origin_dev_exists"])
        self.assertEqual(plan["branch_roles"]["dev"], "integration")
        self.assertEqual(plan["branch_roles"]["origin/dev"], "integration")

    def test_policy_validation_fails_if_roles_are_swapped(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root, aide_lite.AIDE_BRANCH_POLICY_PATH, "schema_version: aide.repo-branch-policy.v0\nrepo_id: julesc013/aide\ncanonical_branch: dev\nintegration_branch: main\nbranch_roles:\n  main: integration\n  dev: canonical\n")
            write(root, aide_lite.AIDE_DEV_MAIN_PLAN_JSON_PATH, "{}\n")
            write(root, aide_lite.AIDE_DEV_MAIN_PLAN_MD_PATH, "# plan\n")
            failures = [check.message for check in aide_lite.validate_aide_branch_policy_files(root) if check.severity == "FAIL"]
        self.assertTrue(any("AIDE main is canonical" in failure for failure in failures))
        self.assertTrue(any("AIDE dev is integration" in failure for failure in failures))

    def test_promotion_gate_contains_required_commands(self) -> None:
        policy = aide_lite.read_text(REPO_ROOT / aide_lite.AIDE_BRANCH_POLICY_PATH)
        for marker in [
            "py -3 .aide/scripts/aide_lite.py validate",
            "py -3 .aide/scripts/aide_lite.py eval run",
            "py -3 .aide/scripts/aide_lite.py commit check --range",
            "py -3 .aide/scripts/aide_lite.py pack-status",
            "targeted secret scan",
            "review packet",
        ]:
            self.assertIn(marker, policy)

    def test_q30_golden_tasks_pass(self) -> None:
        for task_id in ["aide_dev_main_policy_golden", "aide_branch_plan_golden"]:
            with self.subTest(task_id=task_id):
                result = aide_lite.run_golden_task(REPO_ROOT, task_id)
                self.assertEqual(result.result, "PASS", result.errors)


if __name__ == "__main__":
    unittest.main()
