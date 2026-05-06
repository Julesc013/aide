from __future__ import annotations

import importlib.util
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


class AideLiteVerifierHarnessMirrorTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        aide_lite._write_minimal_repo(root)
        aide_lite.run_context(root)
        aide_lite.write_task_packet(root, "Implement Q12 Verifier v0")
        aide_lite.adapt_agents(root)
        return root

    def test_verifier_report_and_secret_scan_helpers(self) -> None:
        root = self.make_repo()
        report = aide_lite.build_verification_report(root, task_packet_path=aide_lite.LATEST_PACKET_PATH)
        rendered = aide_lite.render_verification_report(report)
        self.assertIn("## VERIFIER_RESULT", rendered)
        self.assertNotIn("print('hello')", rendered)

        fake_value = "abcdef0123456789" * 2
        findings = aide_lite.scan_secret_text("api_key = '" + fake_value + "'\n", ".aide/test.md")
        self.assertTrue(any(finding.severity == "ERROR" for finding in findings))
        policy_findings = aide_lite.scan_secret_text("api_key as policy term.\n", ".aide/test.md")
        self.assertFalse(any(finding.severity == "ERROR" for finding in policy_findings))

    def test_file_refs_and_diff_scope_helpers(self) -> None:
        root = self.make_repo()
        self.assertEqual(aide_lite.validate_file_reference(root, "README.md").severity, "INFO")
        self.assertEqual(aide_lite.validate_file_reference(root, "missing.md").severity, "WARN")
        self.assertEqual(aide_lite.validate_file_reference(root, "README.md#L99-L100").severity, "ERROR")
        allowed = [".aide/verification/**"]
        forbidden = [".env"]
        self.assertEqual(aide_lite.classify_scope_path(".aide/verification/report.md", " M", allowed, forbidden).classification, "allowed")
        self.assertEqual(aide_lite.classify_scope_path(".env", "??", allowed, forbidden).classification, "forbidden")


if __name__ == "__main__":
    unittest.main()
