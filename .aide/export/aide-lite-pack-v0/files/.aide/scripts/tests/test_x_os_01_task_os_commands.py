from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = REPO_ROOT / ".aide/scripts/aide_lite.py"
SPEC = importlib.util.spec_from_file_location("aide_lite_x_os_01", MODULE_PATH)
aide_lite = importlib.util.module_from_spec(SPEC)
sys.modules["aide_lite_x_os_01"] = aide_lite
assert SPEC.loader is not None
SPEC.loader.exec_module(aide_lite)


COMMAND_VECTORS = [
    ["task", "status"],
    ["task", "classify"],
    ["task", "repair-plan"],
    ["task", "requeue-plan"],
    ["task", "resume-plan"],
    ["blocker", "status"],
    ["blocker", "classify"],
    ["wave", "status"],
    ["wave", "plan"],
    ["checkpoint", "status"],
    ["checkpoint", "plan"],
]


def write_fixture(root: Path) -> None:
    (root / ".aide/queue/FIXTURE-TASK/evidence").mkdir(parents=True)
    (root / ".aide/context").mkdir(parents=True)
    (root / ".aide/reports").mkdir(parents=True)
    (root / ".aide/queue/index.yaml").write_text(
        "\n".join(
            [
                "schema_version: aide.queue-index.v0",
                "items:",
                "  - id: FIXTURE-TASK",
                "    title: Fixture Task",
                "    status: running",
                "    planning_state: planned",
                "    path: .aide/queue/FIXTURE-TASK",
                "    evidence:",
                "      - .aide/queue/FIXTURE-TASK/evidence/validation.md",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / ".aide/queue/FIXTURE-TASK/task.yaml").write_text(
        "\n".join(
            [
                "schema_version: aide.task.v1",
                "id: FIXTURE-TASK",
                "title: Fixture Task",
                "status: running",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / ".aide/queue/FIXTURE-TASK/status.yaml").write_text(
        "\n".join(
            [
                "schema_version: aide.task-status.v1",
                "id: FIXTURE-TASK",
                "status: running",
                "result: pending",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / ".aide/queue/FIXTURE-TASK/evidence/validation.md").write_text("# Validation\n\n- pending\n", encoding="utf-8")
    (root / ".aide/context/latest-task-packet.md").write_text("# Task Packet\n\n- task_id: FIXTURE-TASK\n", encoding="utf-8")


class XOS01TaskOSCommandTests(unittest.TestCase):
    def test_parser_accepts_report_only_commands(self) -> None:
        parser = aide_lite.build_parser(REPO_ROOT)
        for command in COMMAND_VECTORS:
            parsed = parser.parse_args(command)
            self.assertTrue(callable(getattr(parsed, "handler", None)), command)

    def test_fixture_report_generation_is_no_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_fixture(root)
            aide_lite.write_all_task_os_reports(root)
            for rel in aide_lite.TASK_OS_COMMAND_REPORT_FILES:
                path = root / rel
                self.assertTrue(path.exists(), rel)
                if rel.endswith(".json"):
                    data = json.loads(path.read_text(encoding="utf-8"))
                    self.assertIn("schema_version", data)
                    boundary = data["no_apply_boundary"]
                    self.assertIs(boundary["task_execution"], False)
                    self.assertIs(boundary["repair_execution"], False)
                    self.assertIs(boundary["branch_mutation"], False)
                    self.assertIs(boundary["target_mutation"], False)
                    self.assertEqual(boundary["provider_or_model_calls"], "none")
                    self.assertEqual(boundary["network_calls"], "none")
                    continue
                text = path.read_text(encoding="utf-8")
                for marker in [
                    "report_only",
                    "task_execution: false",
                    "repair_execution: false",
                    "branch_mutation: false",
                    "target_mutation: false",
                    "provider_or_model_calls: none",
                    "network_calls: none",
                ]:
                    self.assertIn(marker, text, rel)
                for forbidden in ["apply_allowed: true", "target_mutation: true", "checkpoint_branch_created: true"]:
                    self.assertNotIn(forbidden, text, rel)

    def test_task_and_blocker_classification_json_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_fixture(root)
            aide_lite.write_task_os_task_classification(root)
            aide_lite.write_task_os_blocker_classification(root)
            task_data = json.loads((root / aide_lite.TASK_OS_TASK_CLASSIFICATION_JSON_PATH).read_text(encoding="utf-8"))
            blocker_data = json.loads((root / aide_lite.TASK_OS_BLOCKER_CLASSIFICATION_JSON_PATH).read_text(encoding="utf-8"))
            self.assertEqual(task_data["schema_version"], "aide.task-os-task-classification.v0")
            self.assertIn(task_data["lifecycle_state"], [*aide_lite.TASK_OS_LIFECYCLE_STATES, "unknown"])
            self.assertEqual(blocker_data["schema_version"], "aide.task-os-blocker-classification.v0")
            self.assertIsInstance(blocker_data["blockers"], list)

    def test_current_repo_validation_registration_passes(self) -> None:
        checks = aide_lite.validate_task_os_command_files(REPO_ROOT)
        failures = [check.message for check in checks if check.severity == "FAIL"]
        self.assertEqual(failures, [])

    def test_x_os_01_golden_runners_pass(self) -> None:
        definitions = {task.task_id for task in aide_lite.parse_golden_task_catalog(REPO_ROOT)}
        for task_id in aide_lite.XOS01_GOLDEN_TASK_IDS:
            self.assertIn(task_id, definitions)
            result = aide_lite.run_golden_task(REPO_ROOT, task_id)
            self.assertEqual(result.result, "PASS", result.errors)


if __name__ == "__main__":
    unittest.main()
