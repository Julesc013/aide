from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from core.apply import managed_sections, transaction_executor


SECTION = "aide-scoped-fixture-section"
VALID_TEXT = f"""# Fixture

Manual prefix.

<!-- AIDE-GENERATED:BEGIN section={SECTION} -->
Old generated content.
<!-- AIDE-GENERATED:END section={SECTION} -->

Manual suffix.
"""
REPLACEMENT = "New generated content.\n"


def postimage_for(text: str = VALID_TEXT, replacement: str = REPLACEMENT) -> str:
    patch = managed_sections.build_managed_section_patch(text, SECTION, replacement, path="workspace/fixture.md")
    assert patch["status"] == "planned"
    return str(patch["after_text"])


class ScopedTransactionExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "workspace").mkdir()
        (self.root / "reports").mkdir()
        (self.root / "workspace/fixture.md").write_text(VALID_TEXT, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def plan(self, **overrides: object) -> dict[str, object]:
        operation: dict[str, object] = {
            "operation_id": "op-fixture",
            "operation_type": "update_managed_section",
            "path": "workspace/fixture.md",
            "section_name": SECTION,
            "replacement_content": REPLACEMENT,
            "expected_preimage_hash": managed_sections.compute_text_hash(VALID_TEXT),
            "expected_postimage_hash": managed_sections.compute_text_hash(postimage_for()),
        }
        operation.update(overrides.pop("operation_overrides", {}))  # type: ignore[arg-type]
        plan: dict[str, object] = {
            "schema_version": transaction_executor.PLAN_SCHEMA_VERSION,
            "transaction_id": "scoped-fixture-transaction",
            "mode": "dry-run",
            "generated_at": "deterministic",
            "allowed_roots": ["workspace", "reports"],
            "protected_roots": [".git", ".github", ".aide.local", ".env", "secrets"],
            "allowed_operation_types": ["update_managed_section", "report", "validate", "noop"],
            "report_path": "reports/scoped-report.json",
            "rollback_record_path": "reports/scoped-rollback.json",
            "operations": [operation],
        }
        plan.update(overrides)
        return plan

    def execute(self, plan: dict[str, object] | None = None) -> dict[str, object]:
        return transaction_executor.execute_transaction_plan(plan or self.plan(), self.root)

    def test_dry_run_report_mode_produces_no_file_mutation(self) -> None:
        before = (self.root / "workspace/fixture.md").read_text(encoding="utf-8")
        report = self.execute()
        after = (self.root / "workspace/fixture.md").read_text(encoding="utf-8")
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(before, after)
        self.assertFalse(report["target_files_mutated"])

    def test_allowed_managed_section_replacement_succeeds_in_fixture_apply(self) -> None:
        report = self.execute(self.plan(mode="apply"))
        text = (self.root / "workspace/fixture.md").read_text(encoding="utf-8")
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["target_files_mutated"])
        self.assertIn(REPLACEMENT, text)

    def test_manual_content_outside_markers_is_preserved(self) -> None:
        self.execute(self.plan(mode="apply"))
        text = (self.root / "workspace/fixture.md").read_text(encoding="utf-8")
        self.assertIn("Manual prefix.", text)
        self.assertIn("Manual suffix.", text)
        self.assertNotIn("Old generated content.", text)

    def test_disallowed_path_is_blocked(self) -> None:
        (self.root / "outside.md").write_text(VALID_TEXT, encoding="utf-8")
        report = self.execute(self.plan(operation_overrides={"path": "outside.md"}))
        self.assertEqual(report["result"], "BLOCKED_ALLOWED_PATH")

    def test_protected_path_is_blocked(self) -> None:
        (self.root / ".git").mkdir()
        (self.root / ".git/config").write_text(VALID_TEXT, encoding="utf-8")
        plan = self.plan(allowed_roots=["workspace", "reports", ".git"], operation_overrides={"path": ".git/config"})
        report = self.execute(plan)
        self.assertEqual(report["result"], "BLOCKED_PROTECTED_PATH")

    def test_path_traversal_is_blocked(self) -> None:
        report = self.execute(self.plan(operation_overrides={"path": "workspace/../fixture.md"}))
        self.assertEqual(report["result"], "BLOCKED_ALLOWED_PATH")

    def test_unsupported_operation_is_blocked(self) -> None:
        report = self.execute(self.plan(operation_overrides={"operation_type": "delete"}))
        self.assertEqual(report["result"], "BLOCKED_PROHIBITED_OPERATION")

    def test_missing_operation_type_is_blocked(self) -> None:
        plan = self.plan()
        operation = dict(plan["operations"][0])  # type: ignore[index]
        operation.pop("operation_type")
        plan["operations"] = [operation]
        report = self.execute(plan)
        self.assertEqual(report["result"], "BLOCKED_PROHIBITED_OPERATION")

    def test_missing_marker_is_blocked(self) -> None:
        (self.root / "workspace/fixture.md").write_text("Manual only.\n", encoding="utf-8")
        plan = self.plan(operation_overrides={"expected_preimage_hash": managed_sections.compute_text_hash("Manual only.\n")})
        report = self.execute(plan)
        self.assertEqual(report["result"], "BLOCKED_MANAGED_SECTION")

    def test_duplicate_marker_is_blocked(self) -> None:
        text = VALID_TEXT + "\n" + VALID_TEXT
        (self.root / "workspace/fixture.md").write_text(text, encoding="utf-8")
        plan = self.plan(operation_overrides={"expected_preimage_hash": managed_sections.compute_text_hash(text)})
        report = self.execute(plan)
        self.assertEqual(report["result"], "BLOCKED_MANAGED_SECTION")
        self.assertIn("duplicate_start_marker", json.dumps(report))

    def test_malformed_marker_is_blocked(self) -> None:
        text = "<!-- AIDE-GENERATED:BEGIN -->\nBody.\n<!-- AIDE-GENERATED:END section=aide-scoped-fixture-section -->\n"
        (self.root / "workspace/fixture.md").write_text(text, encoding="utf-8")
        plan = self.plan(operation_overrides={"expected_preimage_hash": managed_sections.compute_text_hash(text)})
        report = self.execute(plan)
        self.assertEqual(report["result"], "BLOCKED_MANAGED_SECTION")
        self.assertIn("malformed_marker", json.dumps(report))

    def test_nested_marker_is_blocked(self) -> None:
        text = f"""<!-- AIDE-GENERATED:BEGIN section={SECTION} -->
<!-- AIDE-GENERATED:BEGIN section=inner -->
Inner.
<!-- AIDE-GENERATED:END section=inner -->
<!-- AIDE-GENERATED:END section={SECTION} -->
"""
        (self.root / "workspace/fixture.md").write_text(text, encoding="utf-8")
        plan = self.plan(operation_overrides={"expected_preimage_hash": managed_sections.compute_text_hash(text)})
        report = self.execute(plan)
        self.assertEqual(report["result"], "BLOCKED_MANAGED_SECTION")
        self.assertIn("nested_marker", json.dumps(report))

    def test_ambiguous_marker_ownership_is_blocked(self) -> None:
        report = self.execute(self.plan(operation_overrides={"marker_family": "OTHER-GENERATED"}))
        self.assertEqual(report["result"], "BLOCKED_MANAGED_SECTION")
        self.assertIn("ambiguous marker ownership", json.dumps(report))

    def test_preimage_hash_mismatch_is_blocked(self) -> None:
        report = self.execute(self.plan(operation_overrides={"expected_preimage_hash": "sha256:not-current"}))
        self.assertEqual(report["result"], "BLOCKED_PREIMAGE_HASH_MISMATCH")

    def test_postimage_mismatch_is_detected(self) -> None:
        report = self.execute(self.plan(operation_overrides={"expected_postimage_hash": "sha256:not-planned"}))
        self.assertEqual(report["result"], "FAILED_POSTIMAGE_VERIFICATION")

    def test_staged_change_record_is_generated(self) -> None:
        report = self.execute()
        self.assertEqual(report["staged_changes"][0]["schema_version"], transaction_executor.STAGED_CHANGE_SCHEMA_VERSION)
        self.assertEqual(report["staged_changes"][0]["operation_type"], "update_managed_section")

    def test_rollback_compatible_record_is_generated(self) -> None:
        report = self.execute()
        rollback = report["rollback_record"]
        self.assertEqual(rollback["schema_version"], transaction_executor.ROLLBACK_SCHEMA_VERSION)
        self.assertFalse(rollback["apply_allowed"])
        self.assertFalse(rollback["rollback_execution"])

    def test_final_report_and_evidence_outputs_are_generated(self) -> None:
        report = self.execute()
        self.assertEqual(report["status"], "PASS")
        self.assertTrue((self.root / "reports/scoped-report.json").exists())
        self.assertTrue((self.root / "reports/scoped-rollback.json").exists())

    def test_capability_label_is_not_overstated(self) -> None:
        report = self.execute()
        capability = report["capability_reality"]
        self.assertEqual(capability["state"], "implemented_tested_review_gated")
        self.assertFalse(capability["production_ready"])
        self.assertFalse(capability["release_ready"])
        self.assertFalse(capability["broad_active_repo_apply"])

    def test_forbidden_operation_types_are_rejected(self) -> None:
        for operation_type in ["install_apply", "upgrade_apply", "repair_apply", "rollback_apply", "network_call"]:
            with self.subTest(operation_type=operation_type):
                report = self.execute(self.plan(operation_overrides={"operation_type": operation_type}))
                self.assertEqual(report["result"], "BLOCKED_PROHIBITED_OPERATION")

    def test_malformed_plan_input_is_rejected(self) -> None:
        report = self.execute({"schema_version": "wrong", "transaction_id": "", "mode": "dry-run", "operations": []})
        self.assertEqual(report["result"], "BLOCKED_MALFORMED_PLAN")


if __name__ == "__main__":
    unittest.main()
