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
        self.assertTrue(aide_lite.pattern_matches(".git/config", ".git/**"))
        self.assertTrue(aide_lite.pattern_matches(".aide.local/state.json", ".aide.local/**"))
        self.assertTrue(aide_lite.pattern_matches("node_modules/pkg/index.js", "node_modules/**"))
        self.assertTrue(aide_lite.pattern_matches("core/harness/__pycache__/x.pyc", "__pycache__/**"))
        self.assertTrue(aide_lite.pattern_matches("dist/app.zip", "dist/**"))
        self.assertTrue(aide_lite.pattern_matches("build/output.txt", "build/**"))
        self.assertFalse(aide_lite.pattern_matches("docs/reference/readme.md", "dist/**"))

    def test_snapshot_excludes_ignored_paths_and_sorts(self) -> None:
        root = self.make_repo()
        result = aide_lite.write_snapshot(root)
        snapshot = json.loads(aide_lite.read_text(result.path))
        paths = [entry["path"] for entry in snapshot["files"]]
        self.assertEqual(paths, sorted(paths))
        self.assertNotIn(".env", paths)
        self.assertFalse(any(path.startswith(".git/") for path in paths))
        self.assertFalse(any(path.startswith(".aide.local/") for path in paths))
        self.assertFalse(any(path.startswith("node_modules/") for path in paths))
        self.assertFalse(any(path.startswith("build/") for path in paths))
        self.assertFalse(any(path == aide_lite.SNAPSHOT_PATH for path in paths))
        self.assertEqual(snapshot["contents_inline"], False)
        self.assertIn("summary", snapshot)
        self.assertIn("aggregate_approx_tokens", snapshot["summary"])
        self.assertNotIn("contents", snapshot["files"][0])

    def test_pack_output_contains_required_sections_without_file_dump(self) -> None:
        root = self.make_repo()
        result, rendered = aide_lite.write_task_packet(root, "Implement Q10 AIDE Lite hardening")
        packet = aide_lite.read_text(result.path)
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
        self.assertEqual(rendered.budget_status, "PASS")

    def test_pack_marks_budget_overflow(self) -> None:
        root = self.make_repo()
        budget_path = root / ".aide/policies/token-budget.yaml"
        text = aide_lite.read_text(budget_path)
        text = text.replace("max_compact_task_packet_tokens: 3200", "max_compact_task_packet_tokens: 10")
        aide_lite.write_text(budget_path, text)
        _result, rendered = aide_lite.write_task_packet(root, "Implement Q10 AIDE Lite hardening")
        self.assertEqual(rendered.budget_status, "WARN")
        self.assertTrue(any("over hard limit" in warning for warning in rendered.warnings))

    def test_adapt_is_deterministic(self) -> None:
        root = self.make_repo()
        result, before, after = aide_lite.adapt_agents(root)
        once = aide_lite.read_text(root / "AGENTS.md")
        second, _second_before, _second_after = aide_lite.adapt_agents(root)
        twice = aide_lite.read_text(root / "AGENTS.md")
        self.assertEqual(once, twice)
        self.assertEqual(result.action, "appended")
        self.assertEqual(second.action, "unchanged")
        self.assertEqual(before.status, "missing")
        self.assertEqual(after.status, "current")
        self.assertIn("Manual intro.", twice)
        self.assertIn(aide_lite.AGENTS_BEGIN, twice)
        self.assertIn(aide_lite.AGENTS_END, twice)

    def test_adapt_replaces_managed_drift(self) -> None:
        root = self.make_repo()
        aide_lite.adapt_agents(root)
        agents = root / "AGENTS.md"
        drifted = aide_lite.read_text(agents).replace("Use repo refs", "Use every file")
        aide_lite.write_text(agents, drifted)
        self.assertEqual(aide_lite.adapter_status(root).status, "drift")
        result, before, after = aide_lite.adapt_agents(root)
        self.assertEqual(result.action, "replaced")
        self.assertEqual(before.status, "drift")
        self.assertEqual(after.status, "current")

    def test_estimate_missing_or_binary_file_fails(self) -> None:
        root = self.make_repo()
        with self.assertRaises(ValueError):
            aide_lite.estimate_file(root, "missing.txt")
        binary = root / "artifact.bin"
        binary.write_bytes(b"\x00\x01\x02")
        with self.assertRaises(ValueError):
            aide_lite.estimate_file(root, "artifact.bin")

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
