import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from core.reconciler.generated_output_ledger import (
    build_payloads,
    classify_path,
    normalize_path,
    validate_generated_output_ledger_reports,
    write_generated_output_ledger_reports,
)


class GeneratedOutputLedgerTests(unittest.TestCase):
    def make_repo(self) -> tempfile.TemporaryDirectory:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        (root / ".aide/generated").mkdir(parents=True)
        (root / ".aide/reports/self-management").mkdir(parents=True)
        (root / ".aide/knowledge/okf/current-state").mkdir(parents=True)
        (root / ".aide/context").mkdir(parents=True)
        (root / ".agents/skills/aide-queue").mkdir(parents=True)
        (root / ".aide/queue/AIDE-BUILD-SAMPLE-01/evidence").mkdir(parents=True)
        (root / ".aide/generated/manifest.yaml").write_text(
            """schema_version: aide.generated-manifest.v0
targets:
  - path: .agents/skills/aide-queue/SKILL.md
    section: aide-queue-source-summary
    mode: managed-section
    status: managed
    source_fingerprint: sha256:abc
    content_fingerprint: sha256:def
    sources:
      - .aide/profile.yaml
""",
            encoding="utf-8",
        )
        (root / ".aide/profile.yaml").write_text("schema_version: test\n", encoding="utf-8")
        (root / ".agents/skills/aide-queue/SKILL.md").write_text(
            "<!-- AIDE-GENERATED:BEGIN section=aide-queue-source-summary generator=aide-harness-generated-artifacts-v0 version=q05.generated-artifacts.v0 mode=managed-section sources=.aide/profile.yaml fingerprint=sha256:def manual=outside-only -->\nGenerated\n<!-- AIDE-GENERATED:END section=aide-queue-source-summary -->\n",
            encoding="utf-8",
        )
        (root / ".aide/reports/self-management/sample-report.md").write_text(
            "task_id: AIDE-BUILD-SAMPLE-01\n", encoding="utf-8"
        )
        (root / ".aide/knowledge/okf/current-state/queue.md").write_text(
            "projection\n", encoding="utf-8"
        )
        (root / ".aide/context/latest-task-packet.md").write_text(
            "context packet\n", encoding="utf-8"
        )
        (root / ".aide/queue/AIDE-BUILD-SAMPLE-01/status.yaml").write_text(
            "status: needs_review\n", encoding="utf-8"
        )
        (root / ".aide/queue/AIDE-BUILD-SAMPLE-01/evidence/validation.md").write_text(
            "PASS\n", encoding="utf-8"
        )
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "test"], cwd=root, check=True, stdout=subprocess.PIPE)
        return tmp

    def test_path_normalization_is_portable(self):
        self.assertEqual(normalize_path(Path(".aide") / "reports" / "x.md"), ".aide/reports/x.md")

    def test_known_generated_marker_and_manifest_are_noncanonical(self):
        with self.make_repo() as tmp:
            root = Path(tmp)
            entry = classify_path(
                root,
                ".agents/skills/aide-queue/SKILL.md",
                {
                    ".agents/skills/aide-queue/SKILL.md": {
                        "mode": "managed-section",
                        "sources": [".aide/profile.yaml"],
                    }
                },
            )
            self.assertEqual(entry.generator_status, "known")
            self.assertEqual(entry.canonical, "false")
            self.assertEqual(entry.safe_to_delete, "unknown")
            self.assertIn(".aide/profile.yaml", entry.source_hashes)

    def test_report_and_okf_unknowns_are_conservative(self):
        with self.make_repo() as tmp:
            root = Path(tmp)
            ledger, report, findings = build_payloads(root)
            entries = {entry["path"]: entry for entry in ledger["entries"]}
            self.assertEqual(entries[".aide/reports/self-management/sample-report.md"]["classification"], "generated_report")
            self.assertEqual(entries[".aide/knowledge/okf/current-state/queue.md"]["canonical"], "false")
            self.assertEqual(entries[".aide/reports/self-management/sample-report.md"]["safe_to_regenerate"], "unknown")
            self.assertEqual(report["result"], "PASS_WITH_WARNINGS")
            self.assertTrue(any(f["taxonomy"] == "generator_unknown" for f in findings["findings"]))

    def test_write_validate_and_no_source_mutation(self):
        with self.make_repo() as tmp:
            root = Path(tmp)
            source = root / ".aide/knowledge/okf/current-state/queue.md"
            before = source.read_text(encoding="utf-8")
            write_generated_output_ledger_reports(root)
            validation = validate_generated_output_ledger_reports(root)
            after = source.read_text(encoding="utf-8")
            self.assertTrue(validation["validated"], validation)
            self.assertEqual(before, after)
            ledger = json.loads((root / ".aide/ledgers/generated-output.yaml").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(ledger["entries"]), 4)
            self.assertTrue((root / ".aide/reports/self-management/generated-output-ledger.json").exists())


if __name__ == "__main__":
    unittest.main()
