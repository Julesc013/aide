from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = REPO_ROOT / ".aide/scripts/aide_lite.py"
SPEC = importlib.util.spec_from_file_location("aide_lite_q27", MODULE_PATH)
aide_lite = importlib.util.module_from_spec(SPEC)
sys.modules["aide_lite_q27"] = aide_lite
assert SPEC.loader is not None
SPEC.loader.exec_module(aide_lite)


class Q27CommitRecoveryTests(unittest.TestCase):
    def result_for(self, message: str) -> str:
        return aide_lite.commit_message_result(aide_lite.validate_commit_message_text(message))

    def test_valid_commit_message_passes(self) -> None:
        self.assertEqual(self.result_for(aide_lite.COMMIT_GOOD_EXAMPLE), "PASS")

    def test_invalid_commit_type_fails(self) -> None:
        message = aide_lite.COMMIT_GOOD_EXAMPLE.replace("policy(aide):", "random(aide):")
        self.assertEqual(self.result_for(message), "FAIL")

    def test_vague_summary_fails(self) -> None:
        message = aide_lite.COMMIT_GOOD_EXAMPLE.replace(
            "policy(aide): define structured commit recovery",
            "policy(aide): update",
        )
        self.assertEqual(self.result_for(message), "FAIL")

    def test_too_long_subject_fails(self) -> None:
        message = aide_lite.COMMIT_GOOD_EXAMPLE.replace(
            "policy(aide): define structured commit recovery",
            "policy(aide): " + "x" * 80,
        )
        self.assertEqual(self.result_for(message), "FAIL")

    def test_missing_heading_fails(self) -> None:
        message = aide_lite.COMMIT_GOOD_EXAMPLE.replace("## Validation", "## Checks")
        self.assertEqual(self.result_for(message), "FAIL")

    def test_missing_changelog_category_fails(self) -> None:
        message = aide_lite.COMMIT_GOOD_EXAMPLE.replace("- Added:", "- Unknown:")
        self.assertEqual(self.result_for(message), "FAIL")

    def test_trailer_parsing(self) -> None:
        trailers = aide_lite.parse_commit_trailers(aide_lite.COMMIT_GOOD_EXAMPLE)
        self.assertEqual(trailers["AIDE-Task"], "Q27-commit-discipline-workunit-recovery-v0")
        self.assertEqual(trailers["AIDE-Phase"], "Q27")

    def test_commit_check_inline_command(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = aide_lite.main(["commit", "check", "--message", aide_lite.COMMIT_GOOD_EXAMPLE])
        self.assertEqual(code, 0)
        self.assertIn("result: PASS", buffer.getvalue())

    def test_changelog_preview_groups_and_reports_malformed(self) -> None:
        data = {
            "schema_version": "aide.changelog-preview.v0",
            "source_range": "fixture",
            "commit_count": 2,
            "categories": {
                "Added": [
                    {
                        "commit": "abc123",
                        "subject": "policy(aide): define structured commit recovery",
                        "entry": "commit-message enforcement.",
                    }
                ]
            },
            "malformed_commits": [{"commit": "bad", "subject": "update", "reason": "vague"}],
        }
        rendered = aide_lite.render_changelog_preview(data)
        self.assertIn("## Added", rendered)
        self.assertIn("Malformed Commits", rendered)
        self.assertIn("release_publishing: false", rendered)

    def test_task_complete_fixture_returns_noop(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            aide_lite.write_text(
                root / ".aide/queue/index.yaml",
                """items:
  - id: TASK-1
    status: passed
    task: .aide/queue/TASK-1/task.yaml
    evidence: .aide/queue/TASK-1/evidence
""",
            )
            aide_lite.write_text(root / ".aide/queue/TASK-1/task.yaml", "id: TASK-1\nacceptance:\n  - done\n")
            aide_lite.write_text(root / ".aide/queue/TASK-1/status.yaml", "status: passed\n")
            aide_lite.write_text(root / ".aide/queue/TASK-1/evidence/changed-files.md", "# Changed\n")
            aide_lite.write_text(root / ".aide/queue/TASK-1/evidence/validation.md", "# Validation\n- PASS\n")
            aide_lite.write_text(root / ".aide/queue/TASK-1/evidence/remaining-risks.md", "# Risks\n- None\n")
            inspection = aide_lite.inspect_task(root, "TASK-1")
        self.assertEqual(inspection["classification"], "complete")
        self.assertEqual(aide_lite.task_recovery_suggestion(inspection), "noop_already_complete")

    def test_task_partial_fixture_suggests_resume(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            aide_lite.write_text(root / ".aide/queue/TASK-2/task.yaml", "id: TASK-2\n")
            aide_lite.write_text(root / ".aide/queue/TASK-2/status.yaml", "status: running\n")
            aide_lite.write_text(root / ".aide/queue/TASK-2/evidence/changed-files.md", "# Changed\n")
            inspection = aide_lite.inspect_task(root, "TASK-2")
        self.assertEqual(inspection["classification"], "partial")
        self.assertEqual(aide_lite.task_recovery_suggestion(inspection), "continue_from_status_and_evidence")

    def test_task_short_id_resolves_from_queue_index(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            aide_lite.write_text(
                root / ".aide/queue/index.yaml",
                """items:
  - id: Q28-git-workflow-policy-v0
    status: superseded
    task: .aide/queue/Q28-git-workflow-policy-v0/task.yaml
    evidence: .aide/queue/Q28-git-workflow-policy-v0/evidence
""",
            )
            aide_lite.write_text(root / ".aide/queue/Q28-git-workflow-policy-v0/task.yaml", "id: Q28-git-workflow-policy-v0\n")
            aide_lite.write_text(root / ".aide/queue/Q28-git-workflow-policy-v0/status.yaml", "status: superseded\n")
            inspection = aide_lite.inspect_task(root, "Q28")
        self.assertEqual(inspection["requested_task_id"], "Q28")
        self.assertEqual(inspection["task_id"], "Q28-git-workflow-policy-v0")
        self.assertEqual(inspection["classification"], "partial")

    def test_hook_and_template_have_no_live_external_behavior(self) -> None:
        hook = aide_lite.read_text(REPO_ROOT / ".aide/hooks/commit-msg")
        template = aide_lite.read_text(REPO_ROOT / ".aide/git/commit-template.md")
        self.assertIn("commit check --message-file", hook)
        self.assertIn("provider", hook.lower())
        self.assertIn("network", hook.lower())
        self.assertIn("## Changelog", template)
        self.assertNotIn("OPENAI_API_KEY=", hook)
        self.assertNotIn("BEGIN PRIVATE KEY", template)

    def test_changelog_preview_json_shape_from_fixture(self) -> None:
        data = aide_lite.make_changelog_preview(REPO_ROOT, revision_range="HEAD~1..HEAD")
        self.assertEqual(data["schema_version"], "aide.changelog-preview.v0")
        self.assertIn("malformed_commits", data)
        json.dumps(data)

    def make_commit_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path, str, str, list[aide_lite.Check]]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        subprocess.run(["git", "init", "--quiet", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "AIDE Fixture"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "fixture@example.invalid"], check=True)
        (root / "fixture.txt").write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "fixture.txt"], check=True)
        subprocess.run(
            ["git", "-C", str(root), "commit", "--quiet", "-m", "fixture base"],
            check=True,
        )
        (root / "fixture.txt").write_text("historical\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "fixture.txt"], check=True)
        message = aide_lite.COMMIT_GOOD_EXAMPLE.replace(
            "- `py -3 .aide/scripts/aide_lite.py commit check --message-file fixture`: PASS.",
            "- Validation was recorded historically without a recognized outcome label.",
        )
        message_path = root / "message.txt"
        message_path.write_text(message, encoding="utf-8")
        subprocess.run(
            ["git", "-C", str(root), "commit", "--quiet", "-F", str(message_path)],
            check=True,
        )
        commit_hash = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip()
        committed_message = aide_lite.git_commit_messages_for_range(root, "HEAD^..HEAD")[0][2]
        checks = aide_lite.validate_commit_message_text(committed_message)
        self.assertEqual(aide_lite.commit_message_result(checks), "FAIL")
        return temp, root, commit_hash, committed_message, checks

    def accepted_disposition(
        self,
        root: Path,
        commit_hash: str,
        message: str,
        checks: list[aide_lite.Check],
    ) -> dict[str, object]:
        facts = aide_lite.git_commit_object_facts(root, commit_hash)
        decision_path = root / ".aide/queue/FIXTURE/evidence/decision.md"
        evidence_path = root / ".aide/queue/FIXTURE/evidence/validation.md"
        decision_path.parent.mkdir(parents=True, exist_ok=True)
        decision_path.write_text("# Decision\n\nFixture owner acceptance.\n", encoding="utf-8")
        evidence_path.write_text("# Validation\n\nFixture evidence.\n", encoding="utf-8")
        record: dict[str, object] = {
            "schema_version": "aide.commit-message-disposition.v1",
            "disposition_id": "fixture-historical-message",
            "status": "accepted",
            "commit": commit_hash,
            "tree": facts["tree"],
            "parents": facts["parents"],
            "message_sha256": aide_lite.canonical_commit_message_sha256(message),
            "failed_checks": [check.message for check in checks if check.severity == "FAIL"],
            "scope": "historical_commit_message_only",
            "decision": "accept_historical_nonconformance",
            "reviewed_by": "owner:fixture",
            "reviewed_at": "2026-09-22",
            "decision_ref": {
                "path": ".aide/queue/FIXTURE/evidence/decision.md",
                "sha256": aide_lite.sha256_file(decision_path),
            },
            "evidence": [
                {
                    "path": ".aide/queue/FIXTURE/evidence/validation.md",
                    "sha256": aide_lite.sha256_file(evidence_path),
                }
            ],
        }
        record["record_digest"] = aide_lite.historical_disposition_record_digest(record)
        return record

    def test_range_disposition_preserves_raw_failure_and_requires_acceptance(self) -> None:
        temp, root, commit_hash, message, checks = self.make_commit_fixture()
        self.addCleanup(temp.cleanup)
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = aide_lite.main(["--repo-root", str(root), "commit", "check", "--range", "HEAD^..HEAD"])
        self.assertEqual(code, 1)
        self.assertIn("result: FAIL", buffer.getvalue())

        record = self.accepted_disposition(root, commit_hash, message, checks)
        registry_path = root / aide_lite.COMMIT_MESSAGE_DISPOSITIONS_PATH
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_text(
            aide_lite.stable_json_text(
                {
                    "schema_version": "aide.commit-message-dispositions.v1",
                    "records": [record],
                }
            ),
            encoding="utf-8",
        )
        accepted = io.StringIO()
        with contextlib.redirect_stdout(accepted):
            code = aide_lite.main(["--repo-root", str(root), "commit", "check", "--range", "HEAD^..HEAD"])
        self.assertEqual(code, 0, accepted.getvalue())
        self.assertIn("result: PASS_WITH_DISPOSITIONS", accepted.getvalue())
        self.assertIn("DISPOSITIONED", accepted.getvalue())
        self.assertIn("original_failure:", accepted.getvalue())

        raw = io.StringIO()
        with contextlib.redirect_stdout(raw):
            code = aide_lite.main(
                ["--repo-root", str(root), "commit", "check", "--range", "HEAD^..HEAD", "--no-dispositions"]
            )
        self.assertEqual(code, 1)
        self.assertIn("result: FAIL", raw.getvalue())
        self.assertNotIn("DISPOSITIONED", raw.getvalue())

    def test_disposition_rejects_altered_exact_identity_and_decision_fields(self) -> None:
        temp, root, commit_hash, message, checks = self.make_commit_fixture()
        self.addCleanup(temp.cleanup)
        baseline = self.accepted_disposition(root, commit_hash, message, checks)
        mutations = {
            "commit": "*",
            "tree": "0" * 40,
            "parents": ["0" * 40],
            "message_sha256": "0" * 64,
            "failed_checks": ["different failure"],
            "scope": "all_commits",
            "decision": "ignore_failure",
            "reviewed_by": "",
            "reviewed_at": "not-a-date",
            "decision_ref": {"path": "../outside.md", "sha256": "0" * 64},
            "evidence": [],
            "record_digest": "0" * 64,
        }
        for key, value in mutations.items():
            with self.subTest(field=key):
                record = dict(baseline)
                record[key] = value
                if key != "record_digest":
                    record["record_digest"] = aide_lite.historical_disposition_record_digest(record)
                result = aide_lite.evaluate_historical_commit_disposition(
                    root,
                    commit_hash,
                    message,
                    checks,
                    {
                        "schema_version": "aide.commit-message-dispositions.v1",
                        "records": [record],
                    },
                )
                self.assertNotEqual(result["status"], "accepted", result)
                self.assertTrue(result["errors"], result)

    def test_disposition_rejects_tampered_evidence_duplicate_and_unknown_fields(self) -> None:
        temp, root, commit_hash, message, checks = self.make_commit_fixture()
        self.addCleanup(temp.cleanup)
        record = self.accepted_disposition(root, commit_hash, message, checks)

        evidence_path = root / str(record["evidence"][0]["path"])
        evidence_path.write_text("tampered\n", encoding="utf-8")
        tampered = aide_lite.evaluate_historical_commit_disposition(
            root,
            commit_hash,
            message,
            checks,
            {"schema_version": "aide.commit-message-dispositions.v1", "records": [record]},
        )
        self.assertEqual(tampered["status"], "invalid")
        self.assertTrue(any("sha256 does not match" in error for error in tampered["errors"]))

        duplicate = aide_lite.evaluate_historical_commit_disposition(
            root,
            commit_hash,
            message,
            checks,
            {"schema_version": "aide.commit-message-dispositions.v1", "records": [record, record]},
        )
        self.assertEqual(duplicate["status"], "missing")
        self.assertTrue(any("multiple disposition records" in error for error in duplicate["errors"]))

        evidence_path.write_text("# Validation\n\nFixture evidence.\n", encoding="utf-8")
        unknown = dict(record)
        unknown["wildcard"] = True
        unknown["record_digest"] = aide_lite.historical_disposition_record_digest(unknown)
        unsupported = aide_lite.evaluate_historical_commit_disposition(
            root,
            commit_hash,
            message,
            checks,
            {"schema_version": "aide.commit-message-dispositions.v1", "records": [unknown]},
        )
        self.assertEqual(unsupported["status"], "invalid")
        self.assertTrue(any("unsupported fields" in error for error in unsupported["errors"]))

    def test_proposed_disposition_is_visible_but_ineffective(self) -> None:
        temp, root, commit_hash, message, checks = self.make_commit_fixture()
        self.addCleanup(temp.cleanup)
        record = self.accepted_disposition(root, commit_hash, message, checks)
        record["status"] = "proposed"
        record["record_digest"] = aide_lite.historical_disposition_record_digest(record)
        result = aide_lite.evaluate_historical_commit_disposition(
            root,
            commit_hash,
            message,
            checks,
            {"schema_version": "aide.commit-message-dispositions.v1", "records": [record]},
        )
        self.assertEqual(result["status"], "proposed")
        self.assertFalse(result["effective"])

    def test_source_disposition_registry_is_not_exportable(self) -> None:
        self.assertTrue(aide_lite.is_forbidden_export_path(aide_lite.COMMIT_MESSAGE_DISPOSITIONS_PATH))


if __name__ == "__main__":
    unittest.main()
