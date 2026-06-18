import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from core.reconciler.report_index import (
    build_payloads,
    infer_stage,
    infer_subject,
    normalize_path,
    validate_report_index_reports,
    write_report_index_reports,
)


class ReportIndexTests(unittest.TestCase):
    def make_repo(self) -> tempfile.TemporaryDirectory:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        (root / ".aide/reports/sample-check").mkdir(parents=True)
        (root / ".aide/reports/self-management").mkdir(parents=True)
        (root / ".aide/queue/AIDE-BUILD-SAMPLE-01/evidence").mkdir(parents=True)
        (root / ".aide/reports/sample-check/check-report.md").write_text(
            "AIDE-BUILD-SAMPLE-01 check report\n", encoding="utf-8"
        )
        (root / ".aide/reports/sample-status.md").write_text(
            "status report\n", encoding="utf-8"
        )
        (root / ".aide/queue/AIDE-BUILD-SAMPLE-01/status.yaml").write_text(
            "status: needs_review\n", encoding="utf-8"
        )
        (root / ".aide/queue/AIDE-BUILD-SAMPLE-01/evidence/validation.md").write_text(
            "PASS\n", encoding="utf-8"
        )
        (root / ".aide/reports/self-management/generated-output-ledger.json").write_text(
            json.dumps(
                {
                    "task_id": "AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01",
                    "result": "PASS_WITH_WARNINGS",
                    "classified_count": 2,
                }
            ),
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "test"], cwd=root, check=True, stdout=subprocess.PIPE)
        return tmp

    def test_inference_helpers(self):
        self.assertEqual(normalize_path(Path(".aide") / "reports" / "x.md"), ".aide/reports/x.md")
        self.assertEqual(infer_stage(".aide/reports/sample-check/check-report.md", ""), "check")
        self.assertEqual(infer_stage(".aide/reports/sample-status.md", ""), "status")
        self.assertEqual(infer_subject(".aide/reports/sample-check/check-report.md"), "sample-check")

    def test_index_records_are_noncanonical(self):
        with self.make_repo() as tmp:
            root = Path(tmp)
            index, report, findings = build_payloads(root)
            self.assertEqual(report["result"], "PASS_WITH_WARNINGS")
            self.assertFalse(index["generated_output_ledger_input"]["accepted"])
            self.assertEqual(index["generated_output_ledger_input"]["status"], "present_provisional_unaccepted")
            self.assertTrue(set(report["excluded_paths"]) >= {
                ".aide/reports/index.yaml",
                ".aide/reports/self-management/report-index.json",
                ".aide/reports/self-management/report-index.md",
                ".aide/reports/self-management/report-index.findings.json",
            })
            self.assertTrue(all(record["canonical"] == "false" for record in index["reports"]))
            self.assertTrue(any(f["taxonomy"] == "generated_truth_risk" for f in findings["findings"]))

    def test_write_validate_and_no_report_mutation(self):
        with self.make_repo() as tmp:
            root = Path(tmp)
            report_path = root / ".aide/reports/sample-check/check-report.md"
            before = report_path.read_text(encoding="utf-8")
            write_report_index_reports(root)
            validation = validate_report_index_reports(root)
            after = report_path.read_text(encoding="utf-8")
            self.assertTrue(validation["validated"], validation)
            self.assertEqual(before, after)
            index = json.loads((root / ".aide/reports/index.yaml").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(index["reports"]), 2)


if __name__ == "__main__":
    unittest.main()
