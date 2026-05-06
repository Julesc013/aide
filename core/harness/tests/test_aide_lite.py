from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = REPO_ROOT / ".aide/scripts/aide_lite.py"
SPEC = importlib.util.spec_from_file_location("aide_lite", MODULE_PATH)
aide_lite = importlib.util.module_from_spec(SPEC)
sys.modules["aide_lite"] = aide_lite
assert SPEC.loader is not None
SPEC.loader.exec_module(aide_lite)


class AideLiteTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        aide_lite._write_minimal_repo(root)
        return root

    def test_estimate_math_uses_chars_divided_by_four(self) -> None:
        self.assertEqual(aide_lite.estimate_text("").approx_tokens, 0)
        self.assertEqual(aide_lite.estimate_text("a").approx_tokens, 1)
        self.assertEqual(aide_lite.estimate_text("abcd").approx_tokens, 1)
        self.assertEqual(aide_lite.estimate_text("abcde").approx_tokens, 2)

    def test_ignore_matching_handles_root_and_nested_paths(self) -> None:
        self.assertTrue(aide_lite.pattern_matches(".env", ".env"))
        self.assertTrue(aide_lite.pattern_matches("node_modules/pkg/index.js", "node_modules/**"))
        self.assertTrue(aide_lite.pattern_matches("core/harness/__pycache__/x.pyc", "__pycache__/**"))
        self.assertTrue(aide_lite.pattern_matches("dist/app.zip", "dist/**"))
        self.assertFalse(aide_lite.pattern_matches("docs/reference/readme.md", "dist/**"))

    def test_snapshot_excludes_ignored_paths_and_sorts(self) -> None:
        root = self.make_repo()
        snapshot_path = aide_lite.write_snapshot(root)
        snapshot = json.loads(aide_lite.read_text(snapshot_path))
        paths = [entry["path"] for entry in snapshot["files"]]
        self.assertEqual(paths, sorted(paths))
        self.assertNotIn(".env", paths)
        self.assertFalse(any(path.startswith("node_modules/") for path in paths))
        self.assertFalse(any(path == aide_lite.SNAPSHOT_PATH for path in paths))
        self.assertEqual(snapshot["contents_inline"], False)

    def test_pack_output_contains_required_sections_without_file_dump(self) -> None:
        root = self.make_repo()
        packet_path = aide_lite.write_task_packet(root, "Implement Q10 AIDE Lite hardening")
        packet = aide_lite.read_text(packet_path)
        for section in [
            "PHASE",
            "GOAL",
            "WHY",
            "CONTEXT_REFS",
            "ALLOWED_PATHS",
            "FORBIDDEN_PATHS",
            "IMPLEMENTATION",
            "VALIDATION",
            "EVIDENCE",
            "NON_GOALS",
            "ACCEPTANCE",
            "TOKEN_ESTIMATE",
        ]:
            self.assertIn(f"## {section}", packet)
        self.assertNotIn("print('hello')", packet)
        self.assertIn("chars:", packet)
        self.assertIn("approx_tokens:", packet)

    def test_adapt_is_deterministic(self) -> None:
        root = self.make_repo()
        aide_lite.adapt_agents(root)
        once = aide_lite.read_text(root / "AGENTS.md")
        aide_lite.adapt_agents(root)
        twice = aide_lite.read_text(root / "AGENTS.md")
        self.assertEqual(once, twice)
        self.assertIn(aide_lite.AGENTS_BEGIN, twice)
        self.assertIn(aide_lite.AGENTS_END, twice)

    def test_validate_catches_missing_required_sections(self) -> None:
        root = self.make_repo()
        aide_lite.write_text(root / ".aide/prompts/compact-task.md", "# Broken\n\n## PHASE\n")
        ok, messages = aide_lite.validate_repo(root)
        self.assertFalse(ok)
        self.assertTrue(any("compact task missing section: GOAL" in message for message in messages))

    def test_selftest_passes(self) -> None:
        ok, messages = aide_lite.run_selftest()
        self.assertTrue(ok)
        self.assertTrue(any(message.startswith("PASS internal") for message in messages))


if __name__ == "__main__":
    unittest.main()
