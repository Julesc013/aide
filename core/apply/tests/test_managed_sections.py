from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from core.apply import managed_sections


VALID_TEXT = """# Fixture

Manual prefix.

<!-- AIDE-GENERATED:BEGIN section=aide-fixture-section -->
Old generated content.
<!-- AIDE-GENERATED:END section=aide-fixture-section -->

Manual suffix.
"""

REPLACEMENT = "New generated content.\n"


class ManagedSectionsCoreTests(unittest.TestCase):
    def test_valid_section_detection(self) -> None:
        sections = managed_sections.find_managed_sections(VALID_TEXT)
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0]["section_name"], "aide-fixture-section")
        self.assertEqual(sections[0]["marker_status"], "valid")

    def test_valid_section_patching_preserves_manual_content(self) -> None:
        patch = managed_sections.build_managed_section_patch(VALID_TEXT, "aide-fixture-section", REPLACEMENT)
        self.assertEqual(patch["status"], "planned")
        after = managed_sections.apply_managed_section_patch_to_text(VALID_TEXT, patch)
        operation = patch["operation"]
        self.assertTrue(managed_sections.verify_manual_content_preserved(VALID_TEXT, after, operation))
        self.assertIn("Manual prefix.", after)
        self.assertIn("Manual suffix.", after)
        self.assertIn(REPLACEMENT, after)
        self.assertNotIn("Old generated content.", after)

    def test_missing_start_marker_blocks(self) -> None:
        text = "<!-- AIDE-GENERATED:END section=aide-fixture-section -->\n"
        patch = managed_sections.build_managed_section_patch(text, "aide-fixture-section", REPLACEMENT)
        self.assertEqual(patch["status"], "blocked")
        self.assertEqual(patch["conflicts"][0]["conflict_class"], "missing_start_marker")

    def test_missing_end_marker_blocks(self) -> None:
        text = "<!-- AIDE-GENERATED:BEGIN section=aide-fixture-section -->\nBody.\n"
        patch = managed_sections.build_managed_section_patch(text, "aide-fixture-section", REPLACEMENT)
        self.assertEqual(patch["status"], "blocked")
        self.assertEqual(patch["conflicts"][0]["conflict_class"], "missing_end_marker")

    def test_duplicate_markers_block(self) -> None:
        text = VALID_TEXT + "\n" + VALID_TEXT
        patch = managed_sections.build_managed_section_patch(text, "aide-fixture-section", REPLACEMENT)
        self.assertEqual(patch["status"], "blocked")
        self.assertEqual(patch["conflicts"][0]["conflict_class"], "duplicate_start_marker")

    def test_nested_marker_blocks(self) -> None:
        text = """<!-- AIDE-GENERATED:BEGIN section=aide-fixture-section -->
<!-- AIDE-GENERATED:BEGIN section=inner -->
Inner.
<!-- AIDE-GENERATED:END section=inner -->
<!-- AIDE-GENERATED:END section=aide-fixture-section -->
"""
        patch = managed_sections.build_managed_section_patch(text, "aide-fixture-section", REPLACEMENT)
        self.assertEqual(patch["status"], "blocked")
        self.assertEqual(patch["conflicts"][0]["conflict_class"], "nested_marker")

    def test_malformed_marker_blocks(self) -> None:
        text = "<!-- AIDE-GENERATED:BEGIN -->\nBody.\n<!-- AIDE-GENERATED:END section=aide-fixture-section -->\n"
        patch = managed_sections.build_managed_section_patch(text, "aide-fixture-section", REPLACEMENT)
        self.assertEqual(patch["status"], "blocked")
        self.assertEqual(patch["conflicts"][0]["conflict_class"], "malformed_marker")

    def test_existing_hash_mismatch_blocks(self) -> None:
        patch = managed_sections.build_managed_section_patch(
            VALID_TEXT,
            "aide-fixture-section",
            REPLACEMENT,
            expected_existing_hash="sha256:not-the-current-section",
        )
        self.assertEqual(patch["status"], "blocked")
        self.assertEqual(patch["conflicts"][0]["conflict_class"], "existing_hash_mismatch")

    def test_fixture_file_patch_records_preimage_postimage_and_rollback(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "fixture.md").write_text(VALID_TEXT, encoding="utf-8")
            result = managed_sections.patch_file_in_fixture(root, "fixture.md", "aide-fixture-section", REPLACEMENT)
            self.assertEqual(result["status"], "patched_fixture")
            self.assertTrue(result["manual_content_preserved"])
            self.assertEqual(result["preimage"]["schema_version"], "aide.preimage.v0")
            self.assertEqual(result["postimage"]["schema_version"], "aide.postimage.v0")
            self.assertEqual(result["rollback"]["schema_version"], "aide.rollback-record.v0")
            self.assertFalse(result["rollback"]["apply_allowed"])

    def test_binary_file_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "binary.bin"
            path.write_bytes(b"abc\0def")
            self.assertTrue(managed_sections.is_binary_file(path))
            with self.assertRaises(managed_sections.ManagedSectionError):
                managed_sections.load_text_file_safely(path)


if __name__ == "__main__":
    unittest.main()
