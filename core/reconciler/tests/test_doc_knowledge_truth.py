from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from core.reconciler import doc_knowledge_truth as dkt


class DocKnowledgeTruthTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / ".aide/queue").mkdir(parents=True)
        (root / ".aide/reports/self-management").mkdir(parents=True)
        (root / ".aide/policies").mkdir(parents=True)
        (root / ".aide/context").mkdir(parents=True)
        (root / ".aide/knowledge/okf/current-state").mkdir(parents=True)
        (root / ".aide/queue/AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01/evidence").mkdir(parents=True)
        (root / ".aide/queue/AIDE-CHECK-CAPABILITY-MANIFEST-01/evidence").mkdir(parents=True)
        (root / ".aide/queue/AIDE-ACCEPT-RECONCILER-REPORTS-01").mkdir(parents=True)

        (root / ".aide/queue/index.yaml").write_text(
            "\n".join(
                [
                    "schema_version: aide.queue-index.v0",
                    "items:",
                    "  - id: AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01",
                    "    status: needs_review",
                    "    result: ACCEPTED_WITH_WARNINGS",
                    "  - id: AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01",
                    "    status: needs_review",
                    "    result: PASS_WITH_WARNINGS",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (root / ".aide/reports/self-management/accept-self-management-charter.json").write_text(
            json.dumps(
                {
                    "task_id": "AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01",
                    "result": "ACCEPTED_WITH_WARNINGS",
                    "recommended_next_task": dkt.TASK_ID,
                }
            ),
            encoding="utf-8",
        )
        (root / ".aide/policies/self-management.yaml").write_text(
            "\n".join(
                [
                    "required_sequence:",
                    "  - AIDE-BUILD-ROOT-AUTHORITY-MANIFEST-01",
                    "  - AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (root / "docs/reference").mkdir(parents=True)
        (root / "docs/reference/aide-self-management.md").write_text(
            "1. `AIDE-BUILD-ROOT-AUTHORITY-MANIFEST-01`\n"
            "2. `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`\n",
            encoding="utf-8",
        )
        (root / ".aide/context/latest-task-packet.md").write_text(
            "# AIDE Latest Task Packet\n\n## PHASE\n\nAIDE-CHECK-SELF-MANAGEMENT-CHARTER-01\n",
            encoding="utf-8",
        )
        (root / ".aide/knowledge/okf/current-state/next-work.md").write_text(
            "The only next task recommended by this build slice is `AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01`.\n",
            encoding="utf-8",
        )
        (root / ".aide/knowledge/okf/current-state/queue.md").write_text(
            "source_hashes:\n"
            "  - path: \".aide/queue/index.yaml\"\n"
            "    sha256: \"sha256:not-current\"\n"
            "# Queue\n\n- Current build task: `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01`\n",
            encoding="utf-8",
        )
        (root / "README.md").write_text("| Reconciler reports | Planned |\n", encoding="utf-8")
        (root / "DOCUMENTATION.md").write_text(
            "Reconciler, CapabilityManifest, ConformanceProfile remain future phases.\n",
            encoding="utf-8",
        )
        (root / ".aide/queue/AIDE-ACCEPT-RECONCILER-REPORTS-01/status.yaml").write_text(
            "result: ACCEPTED_WITH_WARNINGS\n", encoding="utf-8"
        )
        (root / ".aide/queue/AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01/status.yaml").write_text(
            "evidence:\n"
            "  - .aide/queue/AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01/evidence/validation.md\n",
            encoding="utf-8",
        )
        (root / ".aide/queue/AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01/evidence/validation.md").write_text(
            "ok\n", encoding="utf-8"
        )
        (root / ".aide/queue/AIDE-CHECK-CAPABILITY-MANIFEST-01/status.yaml").write_text(
            "evidence:\n"
            "  - .aide/queue/AIDE-CHECK-CAPABILITY-MANIFEST-01/evidence/validation.md\n",
            encoding="utf-8",
        )
        (root / ".aide/queue/AIDE-CHECK-CAPABILITY-MANIFEST-01/evidence/validation.md").write_text(
            "ok\n", encoding="utf-8"
        )
        return root

    def test_collect_findings_uses_report_convention_shape(self) -> None:
        root = self.make_repo()
        findings = dkt.collect_findings(root)
        self.assertGreaterEqual(len(findings), 6)
        for finding in findings:
            data = finding.__dict__
            for field in [
                "id",
                "severity",
                "surface",
                "taxonomy",
                "claim",
                "expected",
                "observed",
                "evidence_refs",
                "affected_paths",
                "recommendation",
                "next_task",
            ]:
                self.assertIn(field, data)
            self.assertIn(finding.severity, dkt.ALLOWED_SEVERITIES)

    def test_write_reports_and_validate(self) -> None:
        root = self.make_repo()
        report = dkt.write_doc_knowledge_truth_reports(root)
        self.assertEqual(report["task_id"], dkt.TASK_ID)
        self.assertEqual(report["result"], "PASS_WITH_WARNINGS")
        validation = dkt.validate_doc_knowledge_truth_reports(root)
        self.assertEqual(validation["validation_status"], "PASS_WITH_WARNINGS", validation)
        self.assertTrue(validation["markdown_json_agree"])

    def test_non_capability_flags_remain_false(self) -> None:
        root = self.make_repo()
        report = dkt.write_doc_knowledge_truth_reports(root)
        for key in dkt.EXPLICIT_NON_CAPABILITIES:
            self.assertIs(report[key], False)


if __name__ == "__main__":
    unittest.main()
