from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import importlib.util
import json
import shutil
import os
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = REPO_ROOT / ".aide/scripts/aide_lite.py"
SPEC = importlib.util.spec_from_file_location("aide_lite", MODULE_PATH)
aide_lite = importlib.util.module_from_spec(SPEC)
sys.modules["aide_lite"] = aide_lite
assert SPEC.loader is not None
SPEC.loader.exec_module(aide_lite)


class ExportImportTests(unittest.TestCase):
    def make_source_repo(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "source"
        root.mkdir()
        for rel in [*aide_lite.PORTABLE_SOURCE_FILES, *aide_lite.Q21_REQUIRED_FILES]:
            source = REPO_ROOT / rel
            if source.exists() and source.is_file():
                self.copy_file(source, root / rel)
        for directory in [*aide_lite.PORTABLE_SOURCE_DIRS, ".aide/import"]:
            source_root = REPO_ROOT / directory
            if not source_root.exists():
                continue
            for source in sorted(source_root.rglob("*")):
                if source.is_file():
                    self.copy_file(source, root / source.relative_to(REPO_ROOT))
        aide_lite.write_text(root / "README.md", "# Source Fixture\n")
        aide_lite.write_text(root / "AGENTS.md", "# Source Agents\n")
        aide_lite.write_text(root / ".gitignore", ".aide.local/\n.aide.local/**\n.env\n")
        return root

    def copy_file(self, source: Path, target: Path) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())

    def build_pack(self, source_root: Path) -> Path:
        pack_root, report = aide_lite.build_export_pack(source_root)
        self.assertGreater(len(report["included_files"]), 20)
        self.assertEqual(report["boundary_violations"], [])
        return pack_root

    def freeze_pack(self, source_root: Path, name: str) -> Path:
        pack_root = self.build_pack(source_root)
        frozen = source_root.parent / name
        shutil.copytree(pack_root, frozen)
        return frozen

    def set_manifest_scalars(self, pack_root: Path, updates: dict[str, str]) -> None:
        lines = []
        for line in aide_lite.read_text(pack_root / "manifest.yaml").splitlines():
            key = line.split(":", 1)[0] if ":" in line else ""
            if key in updates:
                lines.append(f"{key}: {updates[key]}")
            else:
                lines.append(line)
        aide_lite.write_text(pack_root / "manifest.yaml", "\n".join(lines) + "\n")

    def test_export_policy_has_required_anchors(self) -> None:
        policy = aide_lite.read_text(REPO_ROOT / aide_lite.EXPORT_IMPORT_POLICY_PATH)
        for anchor in [
            "portable_pack_only",
            "no_external_repo_mutation",
            "no_network",
            "no_provider_calls",
            "aide-lite-pack-v0",
            "never_copy_aide_self_hosting_queue: true",
            "never_copy_aide_generated_context: true",
            "never_copy_aide_local_state: true",
            "never_copy_provider_credentials: true",
        ]:
            self.assertIn(anchor, policy)

    def test_generated_install_guides_describe_bounded_removal_apply(self) -> None:
        pack_guide = aide_lite.pack_install_text()
        release_guide = aide_lite.release_install_notes_text(REPO_ROOT, "fixture", "PASS")
        for guide in [pack_guide, release_guide]:
            self.assertIn("plan-removal", guide)
            self.assertIn("apply-removal", guide)
            self.assertIn("--expect-plan", guide)
            self.assertIn("Windows", guide)
            self.assertIn("PARTIAL_REMOVAL", guide)
            self.assertIn("authored", guide.lower())
            self.assertIn("apply_allowed: false", guide)
            self.assertIn("RECOVERY_REQUIRED", guide)
            self.assertNotIn("uninstall are planning models only", guide)
        self.assertIn("apply_mode_available: true", release_guide)
        self.assertIn("Non-Windows apply", pack_guide)

    def test_export_includes_required_portable_files_and_manifest(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        self.assertTrue((pack_root / "manifest.yaml").exists())
        self.assertTrue((pack_root / "checksums.json").exists())
        for rel in [
            "files/.aide/scripts/aide_lite.py",
            "files/.aide/policies/token-budget.yaml",
            "files/.aide/policies/export-import.yaml",
            "files/.aide/prompts/compact-task.md",
            "files/.aide/profile.template.yaml",
            "files/.aide/memory/project-state.template.md",
            "files/AGENTS.md.template",
            "files/.aide.local.example/secrets/README.md",
        ]:
            self.assertTrue((pack_root / rel).exists(), rel)
        manifest = aide_lite.read_text(pack_root / "manifest.yaml")
        self.assertIn("included_files:", manifest)
        self.assertIn("excluded_classes:", manifest)
        self.assertIn("raw_prompt_storage: false", manifest)

    def test_export_excludes_source_state_and_generated_artifacts(self) -> None:
        source_root = self.make_source_repo()
        for rel in [
            ".aide/profile.yaml",
            ".aide/queue/index.yaml",
            ".aide/context/latest-task-packet.md",
            ".aide/reports/token-ledger.jsonl",
            ".aide/cache/latest-cache-keys.json",
            ".aide/routing/latest-route-decision.json",
            ".aide/gateway/latest-gateway-status.json",
            ".aide/providers/latest-provider-status.json",
            ".aide.local/state.json",
            ".env",
        ]:
            aide_lite.write_text(source_root / rel, "source-only\n")
        pack_root = self.build_pack(source_root)
        for rel in [
            "files/.aide/profile.yaml",
            "files/.aide/queue/index.yaml",
            "files/.aide/context/latest-task-packet.md",
            "files/.aide/reports/token-ledger.jsonl",
            "files/.aide/cache/latest-cache-keys.json",
            "files/.aide/routing/latest-route-decision.json",
            "files/.aide/gateway/latest-gateway-status.json",
            "files/.aide/providers/latest-provider-status.json",
            "files/.aide.local/state.json",
            "files/.env",
        ]:
            self.assertFalse((pack_root / rel).exists(), rel)

    def test_export_checksums_match_and_are_deterministic(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        ok, problems = aide_lite.validate_pack_checksums(pack_root)
        self.assertTrue(ok, problems)
        checksum_data = json.loads(aide_lite.read_text(pack_root / "checksums.json"))
        self.assertEqual(checksum_data["checksum_scope"], "payload-and-static-pack-docs")
        self.assertIn("manifest.yaml", checksum_data["excluded_from_checksums"])
        self.assertNotIn("manifest.yaml", checksum_data["checksums"])
        self.assertNotIn("checksums.json", checksum_data["checksums"])
        self.assertNotIn("export-report.md", checksum_data["checksums"])
        first = aide_lite.read_text(pack_root / "checksums.json")
        self.build_pack(source_root)
        second = aide_lite.read_text(pack_root / "checksums.json")
        self.assertEqual(first, second)

    def test_pack_status_fails_for_payload_mismatch_not_manifest_metadata(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        aide_lite.write_text(pack_root / "manifest.yaml", aide_lite.read_text(pack_root / "manifest.yaml") + "# metadata note\n")
        ok, problems = aide_lite.validate_pack_checksums(pack_root)
        self.assertTrue(ok, problems)
        aide_lite.write_text(pack_root / "files/.aide/scripts/aide_lite.py", "# tampered payload\n")
        ok, problems = aide_lite.validate_pack_checksums(pack_root)
        self.assertFalse(ok)
        self.assertTrue(any("checksum mismatch: files/.aide/scripts/aide_lite.py" in problem for problem in problems))

    def test_pack_status_fails_for_unchecksummed_payload_file(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        aide_lite.write_text(pack_root / "files/.aide/untracked-payload.txt", "untracked\n")
        ok, problems = aide_lite.validate_pack_checksums(pack_root)
        self.assertFalse(ok)
        self.assertIn("unchecksummed pack file: files/.aide/untracked-payload.txt", problems)

    def test_export_manifest_records_provenance_fields(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        manifest = aide_lite.read_text(pack_root / "manifest.yaml")
        self.assertIn("source_commit:", manifest)
        self.assertIn("source_dirty_state:", manifest)
        self.assertIn("checksum_scope:", manifest)
        status, problems = aide_lite.validate_pack_provenance(pack_root, source_root)
        self.assertFalse(problems)
        self.assertIn(status, {"PASS", "DIRTY_SOURCE_RECORDED", "UNKNOWN_GIT_UNAVAILABLE"})

    def test_export_records_clean_source_before_writing_generated_pack(self) -> None:
        source_root = self.make_source_repo()
        subprocess.run(["git", "init", "--quiet", str(source_root)], check=True)
        subprocess.run(["git", "-C", str(source_root), "config", "user.name", "AIDE Fixture"], check=True)
        subprocess.run(["git", "-C", str(source_root), "config", "user.email", "fixture@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(source_root), "config", "core.autocrlf", "false"], check=True)
        subprocess.run(["git", "-C", str(source_root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(source_root), "commit", "--quiet", "-m", "fixture"], check=True)
        source_commit = subprocess.run(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip()

        pack_root = self.build_pack(source_root)
        scalars = aide_lite.pack_manifest_scalars(pack_root)
        self.assertEqual(scalars["source_commit"], source_commit)
        self.assertEqual(scalars["source_dirty_state"], "false")
        status, problems = aide_lite.validate_pack_provenance(pack_root, source_root)
        self.assertEqual(status, "PASS", problems)
        self.assertFalse(problems)

    def test_pack_provenance_fails_stale_clean_manifest(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        self.set_manifest_scalars(
            pack_root,
            {
                "source_commit": "old-commit",
                "source_dirty_state": "false",
            },
        )
        status, problems = aide_lite.validate_pack_provenance(pack_root, source_root, current_commit="new-commit")
        self.assertEqual(status, "FAIL")
        self.assertTrue(any("does not match current HEAD" in problem for problem in problems))

    def test_pack_provenance_allows_explicit_dirty_manifest(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        self.set_manifest_scalars(
            pack_root,
            {
                "source_commit": "old-commit",
                "source_dirty_state": "true",
            },
        )
        status, problems = aide_lite.validate_pack_provenance(pack_root, source_root, current_commit="new-commit")
        self.assertEqual(status, "DIRTY_SOURCE_RECORDED")
        self.assertFalse(problems)

    def test_pack_provenance_allows_only_artifact_commit_changes(self) -> None:
        source_root = self.make_source_repo()
        subprocess.run(["git", "init", "--quiet", str(source_root)], check=True)
        subprocess.run(["git", "-C", str(source_root), "config", "user.name", "AIDE Fixture"], check=True)
        subprocess.run(["git", "-C", str(source_root), "config", "user.email", "fixture@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(source_root), "config", "core.autocrlf", "false"], check=True)
        subprocess.run(["git", "-C", str(source_root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(source_root), "commit", "--quiet", "-m", "source"], check=True)

        pack_root = self.build_pack(source_root)
        subprocess.run(["git", "-C", str(source_root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(source_root), "commit", "--quiet", "-m", "artifacts"], check=True)
        artifact_commit = subprocess.run(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip()
        status, problems = aide_lite.validate_pack_provenance(pack_root, source_root)
        self.assertEqual(status, "PASS_SOURCE_ANCESTOR", problems)
        self.assertFalse(problems)

        portable_script = source_root / ".aide/scripts/aide_lite.py"
        portable_script.write_text(portable_script.read_text(encoding="utf-8") + "\n# changed input\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(source_root), "add", ".aide/scripts/aide_lite.py"], check=True)
        subprocess.run(["git", "-C", str(source_root), "commit", "--quiet", "-m", "input changed"], check=True)
        input_commit = subprocess.run(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip()
        status, problems = aide_lite.validate_pack_provenance(pack_root, source_root)
        self.assertEqual(status, "FAIL")
        self.assertTrue(any("does not match current HEAD" in problem for problem in problems))

        subprocess.run(["git", "-C", str(source_root), "replace", input_commit, artifact_commit], check=True)
        self.addCleanup(
            subprocess.run,
            ["git", "-C", str(source_root), "replace", "-d", input_commit],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        status, problems = aide_lite.validate_pack_provenance(pack_root, source_root)
        self.assertEqual(status, "FAIL")
        self.assertTrue(any("does not match current HEAD" in problem for problem in problems))

    def test_import_dry_run_reports_without_writing(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        target = source_root.parent / "target-dry-run"
        aide_lite.write_text(target / "README.md", "# Target\n")
        result = aide_lite.apply_import_pack(pack_root, target, dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["mode"], "safe")
        self.assertGreater(result["operation_count"], 10)
        self.assertTrue(result["operations"])
        self.assertTrue(result["skipped"])
        self.assertFalse((target / ".aide").exists())

    def test_import_fixture_creates_templates_and_preserves_agents(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        target = source_root.parent / "target"
        aide_lite.write_text(target / "README.md", "# Target\n")
        aide_lite.write_text(target / "AGENTS.md", "# Target Agents\n\nManual guidance.\n")
        result = aide_lite.apply_import_pack(pack_root, target, dry_run=False)
        self.assertFalse(result["conflicts"])
        agents = aide_lite.read_text(target / "AGENTS.md")
        self.assertIn("Manual guidance.", agents)
        self.assertIn("AIDE-PORTABLE:BEGIN", agents)
        for rel in [
            ".aide/profile.template.yaml",
            ".aide/profile.yaml",
            ".aide/memory/project-state.template.md",
            ".aide/memory/project-state.md",
            ".aide/memory/decisions.template.md",
            ".aide/memory/open-risks.template.md",
        ]:
            self.assertTrue((target / rel).exists(), rel)
        self.assertTrue(aide_lite.gitignore_has_local_state_rules(target))
        self.assertFalse((target / ".aide.local").exists())
        self.assertFalse((target / ".aide/queue/index.yaml").exists())
        self.assertFalse((target / aide_lite.LATEST_PACKET_PATH).exists())
        self.assertFalse((target / "core").exists())
        self.assertTrue((target / "docs/reference/commit-discipline.md").exists())
        self.assertFalse((target / "docs/roadmap").exists())

    def test_import_preserves_authored_agents_bytes_outside_portable_section(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        target = source_root.parent / "target-agents-bytes"
        target.mkdir()
        authored = b"# Target Agents\r\n\r\nManual guidance with spaces  \r\n"
        (target / "AGENTS.md").write_bytes(authored)

        result = aide_lite.apply_import_pack(pack_root, target)
        self.assertEqual(result["status"], "APPLIED")
        installed = (target / "AGENTS.md").read_bytes()
        self.assertTrue(installed.startswith(authored), installed[: len(authored) + 20])
        self.assertIn(b"AIDE-PORTABLE:BEGIN", installed)
        rerun = aide_lite.apply_import_pack(pack_root, target)
        self.assertEqual(rerun["status"], "NO_CHANGES")
        self.assertEqual((target / "AGENTS.md").read_bytes(), installed)

    def test_import_safe_mode_skips_broad_source_roots(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        target = source_root.parent / "target-safe-scope"
        aide_lite.write_text(target / "README.md", "# Target\n")
        result = aide_lite.apply_import_pack(pack_root, target, dry_run=True)
        skipped_sources = {item["source"] for item in result["skipped"]}
        planned_targets = {item["target"] for item in result["operations"]}
        self.assertTrue(any(source.startswith("core/") for source in skipped_sources), skipped_sources)
        self.assertFalse(any(target.startswith("core/") for target in planned_targets), planned_targets)
        self.assertTrue(any(target.startswith("docs/reference/") for target in planned_targets), planned_targets)
        self.assertFalse(any(target.startswith("docs/roadmap/") for target in planned_targets), planned_targets)

    def test_import_full_mode_is_explicit_for_optional_broad_roots(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        target = source_root.parent / "target-full-scope"
        aide_lite.write_text(target / "README.md", "# Target\n")
        result = aide_lite.apply_import_pack(pack_root, target, dry_run=True, mode="full")
        planned_targets = {item["target"] for item in result["operations"]}
        self.assertFalse(result["skipped"])
        self.assertTrue(any(target.startswith("core/") for target in planned_targets), planned_targets)
        self.assertTrue(any(target.startswith("docs/reference/") for target in planned_targets), planned_targets)

    def test_imported_aide_lite_doctor_snapshot_and_pack_run(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.build_pack(source_root)
        target = source_root.parent / "target-smoke"
        aide_lite.write_text(target / "README.md", "# Target Smoke\n")
        aide_lite.apply_import_pack(pack_root, target, dry_run=False)
        script = target / ".aide/scripts/aide_lite.py"
        commands = [
            ["doctor"],
            ["snapshot"],
            ["index"],
            ["pack", "--task", "Fixture target smoke task"],
        ]
        for command in commands:
            result = subprocess.run(
                [sys.executable, str(script), "--repo-root", str(target), *command],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((target / aide_lite.SNAPSHOT_PATH).exists())
        self.assertTrue((target / aide_lite.LATEST_PACKET_PATH).exists())

    def test_import_records_baseline_and_updates_only_unchanged_owned_bytes(self) -> None:
        source_root = self.make_source_repo()
        managed_rel = ".aide/prompts/compact-task.md"
        pack_v1 = self.freeze_pack(source_root, "pack-v1")
        target = source_root.parent / "target-owned-update"
        first = aide_lite.apply_import_pack(pack_v1, target)
        self.assertEqual(first["status"], "APPLIED")
        self.assertTrue((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).is_file())

        aide_lite.write_text(source_root / managed_rel, "# Compact Task v2\n")
        pack_v2 = self.freeze_pack(source_root, "pack-v2")
        preview = aide_lite.apply_import_pack(pack_v2, target, dry_run=True)
        operation = next(item for item in preview["operations"] if item["target"] == managed_rel)
        self.assertEqual(operation["action"], "update_owned")
        self.assertEqual(operation["ownership_basis"], "installed_receipt")

        updated = aide_lite.apply_import_pack(
            pack_v2,
            target,
            expected_plan_digest=preview["plan_digest"],
        )
        self.assertEqual(updated["status"], "APPLIED")
        self.assertEqual(aide_lite.read_text(target / managed_rel), "# Compact Task v2\n")
        rerun = aide_lite.apply_import_pack(pack_v2, target)
        self.assertEqual(rerun["status"], "NO_CHANGES")
        self.assertFalse(rerun["written"])

    def test_validated_predecessor_pack_can_prove_an_unrecorded_baseline(self) -> None:
        source_root = self.make_source_repo()
        managed_rel = ".aide/prompts/compact-task.md"
        pack_v1 = self.freeze_pack(source_root, "predecessor-v1")
        target = source_root.parent / "target-predecessor-update"
        aide_lite.apply_import_pack(pack_v1, target)
        (target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).unlink()

        aide_lite.write_text(source_root / managed_rel, "# Proven predecessor v2\n")
        pack_v2 = self.freeze_pack(source_root, "predecessor-v2")
        preview = aide_lite.apply_import_pack(
            pack_v2,
            target,
            dry_run=True,
            predecessor_pack=pack_v1,
        )
        operation = next(item for item in preview["operations"] if item["target"] == managed_rel)
        self.assertEqual(operation["action"], "update_owned")
        self.assertEqual(operation["ownership_basis"], "validated_predecessor_pack")
        result = aide_lite.apply_import_pack(
            pack_v2,
            target,
            predecessor_pack=pack_v1,
            expected_plan_digest=preview["plan_digest"],
        )
        self.assertEqual(result["status"], "APPLIED")
        self.assertEqual(aide_lite.read_text(target / managed_rel), "# Proven predecessor v2\n")

    def test_tampered_predecessor_pack_is_rejected_before_target_writes(self) -> None:
        source_root = self.make_source_repo()
        managed_rel = ".aide/prompts/compact-task.md"
        pack_v1 = self.freeze_pack(source_root, "tampered-predecessor-v1")
        target = source_root.parent / "target-tampered-predecessor"
        aide_lite.apply_import_pack(pack_v1, target)
        (target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).unlink()
        target_before = (target / managed_rel).read_bytes()

        aide_lite.write_text(source_root / managed_rel, "# Tampered predecessor incoming\n")
        pack_v2 = self.freeze_pack(source_root, "tampered-predecessor-v2")
        aide_lite.write_text(pack_v1 / "files" / managed_rel, "# Invalid predecessor bytes\n")
        with self.assertRaisesRegex(ValueError, "invalid predecessor pack checksums"):
            aide_lite.apply_import_pack(pack_v2, target, predecessor_pack=pack_v1)
        self.assertEqual((target / managed_rel).read_bytes(), target_before)
        self.assertFalse((target / aide_lite.PORTABLE_IMPORT_INTENT_PATH).exists())

    def test_locally_edited_portable_agents_section_refuses_whole_apply(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "agents-section-v1")
        target = source_root.parent / "target-agents-section"
        aide_lite.write_text(target / "AGENTS.md", "# Target Agents\n\nManual guidance.\n")
        aide_lite.apply_import_pack(pack, target)
        agents = aide_lite.read_text(target / "AGENTS.md")
        aide_lite.write_text(target / "AGENTS.md", agents.replace("## AIDE Lite Portable Guidance", "## Locally edited portable guidance"))
        receipt_before = (target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes()

        result = aide_lite.apply_import_pack(pack, target)
        self.assertEqual(result["status"], "CONFLICT")
        self.assertEqual(result["written"], [])
        self.assertIn("AGENTS.md", result["conflicts"])
        self.assertIn("Manual guidance.", aide_lite.read_text(target / "AGENTS.md"))
        self.assertIn("Locally edited portable guidance", aide_lite.read_text(target / "AGENTS.md"))
        self.assertEqual((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes(), receipt_before)

    def test_local_edits_and_unknown_ownership_refuse_before_any_payload_write(self) -> None:
        source_root = self.make_source_repo()
        managed_rel = ".aide/prompts/compact-task.md"
        second_rel = ".aide/policies/token-budget.yaml"
        pack_v1 = self.freeze_pack(source_root, "conflict-v1")
        target = source_root.parent / "target-local-edit"
        aide_lite.apply_import_pack(pack_v1, target)
        receipt_before = (target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes()
        aide_lite.write_text(target / managed_rel, "# User-owned local edit\n")
        second_before = (target / second_rel).read_bytes()
        aide_lite.write_text(source_root / managed_rel, "# Incoming v2\n")
        aide_lite.write_text(source_root / second_rel, "version: incoming-v2\n")
        pack_v2 = self.freeze_pack(source_root, "conflict-v2")

        result = aide_lite.apply_import_pack(pack_v2, target)
        self.assertEqual(result["status"], "CONFLICT")
        self.assertEqual(result["written"], [])
        self.assertIn(managed_rel, result["conflicts"])
        self.assertEqual(aide_lite.read_text(target / managed_rel), "# User-owned local edit\n")
        self.assertEqual((target / second_rel).read_bytes(), second_before)
        self.assertEqual((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes(), receipt_before)

        unknown = source_root.parent / "target-unknown-ownership"
        aide_lite.write_text(unknown / managed_rel, "# Existing unknown bytes\n")
        unknown_result = aide_lite.apply_import_pack(pack_v2, unknown)
        self.assertEqual(unknown_result["status"], "CONFLICT")
        self.assertEqual(unknown_result["written"], [])
        self.assertFalse((unknown / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).exists())

    def test_customization_explains_project_owned_and_conflicting_direct_edits(self) -> None:
        source_root = self.make_source_repo()
        managed_rel = ".aide/prompts/compact-task.md"
        pack_v1 = self.freeze_pack(source_root, "customization-v1")
        target = source_root.parent / "target-customized"
        self.assertEqual(aide_lite.apply_import_pack(pack_v1, target)["status"], "APPLIED")
        profile = target / ".aide/profile.yaml"
        aide_lite.write_text(profile, aide_lite.read_text(profile) + "project_adapter: local\n")
        aide_lite.write_text(target / managed_rel, "# Direct project edit\n")
        profile_bytes = profile.read_bytes()
        managed_bytes = (target / managed_rel).read_bytes()
        receipt_bytes = (target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes()
        aide_lite.write_text(source_root / managed_rel, "# Conflicting upstream revision\n")
        pack_v2 = self.freeze_pack(source_root, "customization-v2")

        preview = aide_lite.apply_import_pack(pack_v2, target, dry_run=True)
        self.assertEqual(preview["status"], "PLANNED_CONFLICT")
        unknown = {item["target"]: item for item in aide_lite.explain_import_result(preview, target)}
        self.assertEqual(unknown[".aide/profile.yaml"]["action"], "preserve")
        self.assertEqual(unknown[".aide/profile.yaml"]["project_rationale"], "unknown")
        self.assertEqual(unknown[managed_rel]["action"], "conflict")
        self.assertEqual(unknown[managed_rel]["rationale_status"], "unknown")
        self.assertEqual(unknown[managed_rel]["observed_digest"], aide_lite.digest_bytes(managed_bytes))

        aide_lite.write_text(target / aide_lite.PROJECT_CUSTOMIZATIONS_PATH, json.dumps({
            "schema_version": aide_lite.PROJECT_CUSTOMIZATIONS_SCHEMA,
            "entries": {
                ".aide/profile.yaml": {"observed_digest": aide_lite.digest_bytes(profile_bytes), "rationale": "Keep the project adapter active."},
                managed_rel: {"observed_digest": aide_lite.digest_bytes(managed_bytes), "rationale": "Project command wording is intentional."},
            },
        }))
        known = {item["target"]: item for item in aide_lite.explain_import_result(preview, target)}
        self.assertEqual(known[".aide/profile.yaml"]["project_rationale"], "Keep the project adapter active.")
        self.assertEqual(known[managed_rel]["project_rationale"], "Project command wording is intentional.")
        aide_lite.write_text(profile, aide_lite.read_text(profile) + "intervening_edit: true\n")
        changed_after_preview = {item["target"]: item for item in aide_lite.explain_import_result(preview, target)}
        self.assertEqual(changed_after_preview[".aide/profile.yaml"]["project_rationale"], "unknown")
        profile.write_bytes(profile_bytes)
        self.assertEqual(aide_lite.apply_import_pack(pack_v2, target)["status"], "CONFLICT")
        self.assertEqual(profile.read_bytes(), profile_bytes)
        self.assertEqual((target / managed_rel).read_bytes(), managed_bytes)
        self.assertEqual((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes(), receipt_bytes)

        aide_lite.write_text(profile, aide_lite.read_text(profile) + "local_note: changed_again\n")
        stale_preview = aide_lite.apply_import_pack(pack_v2, target, dry_run=True)
        stale = {item["target"]: item for item in aide_lite.explain_import_result(stale_preview, target)}
        self.assertEqual(stale[".aide/profile.yaml"]["project_rationale"], "unknown")
        self.assertEqual(stale[".aide/profile.yaml"]["rationale_status"], "unknown")

    def test_feedback_is_explicit_local_and_malformed_rationale_refuses_explanation(self) -> None:
        source_root = self.make_source_repo()
        pack_root = self.freeze_pack(source_root, "feedback-pack")
        target = source_root.parent / "target-feedback"
        self.assertEqual(aide_lite.apply_import_pack(pack_root, target)["status"], "APPLIED")
        script = source_root / ".aide/scripts/aide_lite.py"
        feedback = source_root.parent / "feedback.json"
        command = [sys.executable, str(script), "--repo-root", str(source_root), "import-pack", "--pack", str(pack_root), "--target", str(target)]

        ordinary = subprocess.run([*command, "--dry-run"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(ordinary.returncode, 0, ordinary.stdout + ordinary.stderr)
        self.assertFalse(feedback.exists())
        requested = subprocess.run([*command, "--dry-run", "--explain", "--feedback-out", str(feedback)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(requested.returncode, 0, requested.stdout + requested.stderr)
        packet = json.loads(aide_lite.read_text(feedback))
        self.assertEqual(packet["sharing"], "manual_only")
        self.assertFalse(packet["network_calls"])
        self.assertTrue(all("observed_digest" in item and "incoming_digest" in item for item in packet["explanations"]))
        self.assertTrue(any(item["target"] == ".aide/profile.yaml" for item in packet["explanations"]))
        self.assertTrue(all(item["project_rationale"] == "unknown" for item in packet["explanations"]))
        self.assertFalse((target / "feedback.json").exists())
        self.assertEqual(aide_lite.apply_import_pack(pack_root, target)["status"], "NO_CHANGES")

        refused = subprocess.run([*command, "--feedback-out", str(source_root.parent / "forbidden.json")], capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(refused.returncode, 0)
        self.assertFalse((source_root.parent / "forbidden.json").exists())
        aide_lite.write_text(target / aide_lite.PROJECT_CUSTOMIZATIONS_PATH, '{"schema_version": "wrong", "entries": {}}')
        with self.assertRaisesRegex(ValueError, "invalid project customizations schema"):
            aide_lite.explain_import_result(aide_lite.apply_import_pack(pack_root, target, dry_run=True), target)
        self.assertEqual(aide_lite.apply_import_pack(pack_root, target)["status"], "NO_CHANGES")

    def test_changed_target_refuses_an_exact_preview_identity(self) -> None:
        source_root = self.make_source_repo()
        managed_rel = ".aide/prompts/compact-task.md"
        pack_v1 = self.freeze_pack(source_root, "stale-v1")
        target = source_root.parent / "target-stale-plan"
        aide_lite.apply_import_pack(pack_v1, target)
        aide_lite.write_text(source_root / managed_rel, "# Stale preview incoming\n")
        pack_v2 = self.freeze_pack(source_root, "stale-v2")
        preview = aide_lite.apply_import_pack(pack_v2, target, dry_run=True)
        receipt_before = (target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes()
        aide_lite.write_text(target / managed_rel, "# Changed after preview\n")

        result = aide_lite.apply_import_pack(
            pack_v2,
            target,
            expected_plan_digest=preview["plan_digest"],
        )
        self.assertEqual(result["status"], "STALE_PLAN")
        self.assertEqual(result["written"], [])
        self.assertEqual(aide_lite.read_text(target / managed_rel), "# Changed after preview\n")
        self.assertEqual((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes(), receipt_before)

    def test_interrupted_update_retains_exact_partial_state_and_refuses_replay(self) -> None:
        source_root = self.make_source_repo()
        first_rel = ".aide/prompts/compact-task.md"
        second_rel = ".aide/policies/token-budget.yaml"
        pack_v1 = self.freeze_pack(source_root, "interrupt-v1")
        target = source_root.parent / "target-interrupted-update"
        aide_lite.apply_import_pack(pack_v1, target)
        aide_lite.write_text(source_root / first_rel, "# Interrupted incoming one\n")
        aide_lite.write_text(source_root / second_rel, "version: interrupted-two\n")
        pack_v2 = self.freeze_pack(source_root, "interrupt-v2")

        interrupted = aide_lite.apply_import_pack(pack_v2, target, fail_after_writes=1)
        self.assertEqual(interrupted["status"], "INTERRUPTED")
        self.assertTrue((target / aide_lite.PORTABLE_IMPORT_INTENT_PATH).is_file())
        self.assertEqual(len(interrupted["written"]), 1)

        resumed = aide_lite.apply_import_pack(pack_v2, target)
        self.assertEqual(resumed["status"], "RECOVERY_REQUIRED")
        self.assertEqual(resumed["recovery"]["classification"], "partial")
        self.assertEqual(resumed["written"], [])
        self.assertTrue((target / aide_lite.PORTABLE_IMPORT_INTENT_PATH).is_file())

    @unittest.skipUnless(sys.platform == "win32", "Windows junction boundary")
    def test_rollback_pack_rejects_reparse_payload_and_pack_roots(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        pack = root / "pack"
        payload = root / "external-payload"
        pack.mkdir()
        payload.mkdir()
        (payload / "a.txt").write_bytes(b"fixture bytes")
        (pack / "manifest.yaml").write_text("included_files:\n  - files/a.txt\n", encoding="utf-8")
        files_root = pack / "files"
        pack_alias = root / "pack-alias"
        try:
            junction = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(files_root), str(payload)],
                capture_output=True, text=True, encoding="utf-8", check=False,
            )
            self.assertEqual(junction.returncode, 0, junction.stderr)
            aide_lite.write_text(pack / "checksums.json", aide_lite.stable_json_text(aide_lite.build_pack_checksums(pack)))
            self.assertEqual(aide_lite.validate_pack_checksums(pack), (True, []))
            with self.assertRaisesRegex(ValueError, "reparse"):
                aide_lite.portable_safe_pack_targets(pack)

            junction = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(pack_alias), str(pack)],
                capture_output=True, text=True, encoding="utf-8", check=False,
            )
            self.assertEqual(junction.returncode, 0, junction.stderr)
            with self.assertRaisesRegex(ValueError, "reparse"):
                aide_lite.portable_safe_pack_targets(pack_alias)
            target = root / "target"
            target.mkdir()
            with self.assertRaisesRegex(ValueError, "reparse"):
                aide_lite.build_portable_rollback_plan(pack_alias, pack, target)
        finally:
            if pack_alias.is_junction():
                pack_alias.rmdir()
            if files_root.is_junction():
                files_root.rmdir()

    @unittest.skipUnless(sys.platform == "win32", "anchored portable rollback apply is Windows only")
    def test_exact_predecessor_rollback_restores_owned_bytes_and_receipt(self) -> None:
        source_root = self.make_source_repo()
        managed_rel = ".aide/prompts/compact-task.md"
        pack_v1 = self.freeze_pack(source_root, "rollback-v1")
        target = source_root.parent / "target-rollback"
        aide_lite.write_text(target / "README.md", "# Project authored\n")
        self.assertEqual(aide_lite.apply_import_pack(pack_v1, target)["status"], "APPLIED")
        old_bytes = (target / managed_rel).read_bytes()
        aide_lite.write_text(source_root / managed_rel, "# Upstream v2\n")
        pack_v2 = self.freeze_pack(source_root, "rollback-v2")
        self.assertEqual(aide_lite.apply_import_pack(pack_v2, target, predecessor_pack=pack_v1)["status"], "APPLIED")
        self.assertNotEqual((target / managed_rel).read_bytes(), old_bytes)

        preview = aide_lite.build_portable_rollback_plan(pack_v2, pack_v1, target)
        self.assertEqual(preview["status"], "PLANNED")
        installed_cli = target / ".aide/scripts/aide_lite.py"
        command = [sys.executable, str(installed_cli), "--repo-root", str(target), "rollback-pack", "--current-pack", str(pack_v2), "--previous-pack", str(pack_v1), "--target", str(target), "--json"]
        cli_preview = subprocess.run([*command, "--dry-run"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(cli_preview.returncode, 0, cli_preview.stderr)
        self.assertEqual(json.loads(cli_preview.stdout)["plan_digest"], preview["plan_digest"])
        cli_apply = subprocess.run([*command, "--expect-plan", preview["plan_digest"]], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(cli_apply.returncode, 0, cli_apply.stderr)
        result = json.loads(cli_apply.stdout)
        self.assertEqual(result["status"], "ROLLED_BACK")
        self.assertEqual((target / managed_rel).read_bytes(), old_bytes)
        self.assertEqual(aide_lite.read_text(target / "README.md"), "# Project authored\n")
        self.assertEqual(aide_lite.load_portable_import_receipt(target)["pack"], aide_lite.import_pack_identity(pack_v1))

    @unittest.skipUnless(sys.platform == "win32", "anchored portable rollback apply is Windows only")
    def test_rollback_preserves_authored_edit_and_refuses_stale_or_wrong_lineage(self) -> None:
        source_root = self.make_source_repo()
        managed_rel = ".aide/prompts/compact-task.md"
        pack_v1 = self.freeze_pack(source_root, "rollback-edits-v1")
        target = source_root.parent / "target-rollback-edits"
        self.assertEqual(aide_lite.apply_import_pack(pack_v1, target)["status"], "APPLIED")
        aide_lite.write_text(source_root / managed_rel, "# Upstream changed bytes\n")
        pack_v2 = self.freeze_pack(source_root, "rollback-edits-v2")
        self.assertEqual(aide_lite.apply_import_pack(pack_v2, target, predecessor_pack=pack_v1)["status"], "APPLIED")
        preview = aide_lite.build_portable_rollback_plan(pack_v2, pack_v1, target)
        receipt_path = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        receipt_bytes = receipt_path.read_bytes()
        authored = b"# Project changed after v2\n"
        (target / managed_rel).write_bytes(authored)
        stale = aide_lite.apply_portable_rollback(pack_v2, pack_v1, target, preview["plan_digest"])
        self.assertEqual(stale["status"], "STALE_PLAN")
        conflicted = aide_lite.build_portable_rollback_plan(pack_v2, pack_v1, target)
        self.assertEqual(conflicted["status"], "CONFLICT")
        self.assertEqual(aide_lite.apply_portable_rollback(pack_v2, pack_v1, target, conflicted["plan_digest"])["status"], "CONFLICT")
        self.assertEqual((target / managed_rel).read_bytes(), authored)
        self.assertEqual(receipt_path.read_bytes(), receipt_bytes)
        wrong_previous = source_root.parent / "rollback-wrong-predecessor"
        shutil.copytree(pack_v1, wrong_previous)
        aide_lite.write_text(wrong_previous / "files" / managed_rel, "# Similar paths, different predecessor\n")
        aide_lite.write_text(wrong_previous / "checksums.json", aide_lite.stable_json_text(aide_lite.build_pack_checksums(wrong_previous)))
        self.assertEqual(aide_lite.validate_pack_checksums(wrong_previous), (True, []))
        with self.assertRaisesRegex(ValueError, "exact receipt lineage"):
            aide_lite.build_portable_rollback_plan(pack_v2, wrong_previous, target)
        with self.assertRaisesRegex(ValueError, "exact receipt lineage"):
            aide_lite.build_portable_rollback_plan(pack_v1, pack_v2, target)
        forged_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        forged_receipt["managed"][managed_rel]["installed_digest"] = aide_lite.digest_bytes(authored)
        forged_receipt["receipt_digest"] = aide_lite.portable_import_record_digest(forged_receipt, "receipt_digest")
        aide_lite.write_text(receipt_path, aide_lite.stable_json_text(forged_receipt))
        with self.assertRaisesRegex(ValueError, "baseline differs from current pack"):
            aide_lite.build_portable_rollback_plan(pack_v2, pack_v1, target)
        self.assertEqual((target / managed_rel).read_bytes(), authored)

    @unittest.skipUnless(sys.platform == "win32", "anchored portable rollback apply is Windows only")
    def test_rollback_refuses_changed_payload_path_set(self) -> None:
        source_root = self.make_source_repo()
        pack_v1 = self.freeze_pack(source_root, "rollback-paths-v1")
        added_rel = ".aide/prompts/compact-task.md"
        (pack_v1 / "files" / added_rel).unlink()
        manifest = aide_lite.read_text(pack_v1 / "manifest.yaml")
        aide_lite.write_text(pack_v1 / "manifest.yaml", manifest.replace(f"  - files/{added_rel}\n", ""))
        aide_lite.write_text(pack_v1 / "checksums.json", aide_lite.stable_json_text(aide_lite.build_pack_checksums(pack_v1)))
        self.assertEqual(aide_lite.validate_pack_checksums(pack_v1), (True, []))
        target = source_root.parent / "target-rollback-paths"
        self.assertEqual(aide_lite.apply_import_pack(pack_v1, target)["status"], "APPLIED")
        pack_v2 = self.freeze_pack(source_root, "rollback-paths-v2")
        self.assertEqual(aide_lite.apply_import_pack(pack_v2, target, predecessor_pack=pack_v1)["status"], "APPLIED")
        receipt_before = (target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes()
        with self.assertRaisesRegex(ValueError, "payload paths differ"):
            aide_lite.build_portable_rollback_plan(pack_v2, pack_v1, target)
        self.assertTrue((target / added_rel).is_file())
        self.assertEqual((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes(), receipt_before)

    @unittest.skipUnless(sys.platform == "win32", "anchored portable rollback apply is Windows only")
    def test_interrupted_rollback_retains_intent_and_requires_reconciliation(self) -> None:
        source_root = self.make_source_repo()
        first_rel = ".aide/prompts/compact-task.md"
        second_rel = ".aide/policies/token-budget.yaml"
        pack_v1 = self.freeze_pack(source_root, "rollback-interrupt-v1")
        target = source_root.parent / "target-rollback-interrupt"
        aide_lite.write_text(target / "README.md", "# Authored\n")
        self.assertEqual(aide_lite.apply_import_pack(pack_v1, target)["status"], "APPLIED")
        aide_lite.write_text(source_root / first_rel, "# Second release one\n")
        aide_lite.write_text(source_root / second_rel, "version: second-release\n")
        pack_v2 = self.freeze_pack(source_root, "rollback-interrupt-v2")
        self.assertEqual(aide_lite.apply_import_pack(pack_v2, target, predecessor_pack=pack_v1)["status"], "APPLIED")
        preview = aide_lite.build_portable_rollback_plan(pack_v2, pack_v1, target)
        interrupted = aide_lite.apply_portable_rollback(pack_v2, pack_v1, target, preview["plan_digest"], fail_after_writes=1)
        self.assertEqual(interrupted["status"], "INTERRUPTED")
        self.assertEqual(len(interrupted["written"]), 1)
        intent_path = target / aide_lite.PORTABLE_IMPORT_INTENT_PATH
        receipt_path = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        self.assertTrue(intent_path.is_file())
        self.assertEqual(aide_lite.load_portable_import_receipt(target)["pack"], aide_lite.import_pack_identity(pack_v2))
        intent_bytes, receipt_bytes = intent_path.read_bytes(), receipt_path.read_bytes()
        retry = aide_lite.apply_portable_rollback(pack_v2, pack_v1, target, preview["plan_digest"])
        self.assertEqual(retry["status"], "RECOVERY_REQUIRED")
        self.assertEqual(intent_path.read_bytes(), intent_bytes)
        self.assertEqual(receipt_path.read_bytes(), receipt_bytes)
        self.assertEqual(aide_lite.read_text(target / "README.md"), "# Authored\n")

    @unittest.skipUnless(sys.platform == "win32", "anchored portable rollback apply is Windows only")
    def test_rollback_refuses_pending_prior_update_without_touching_intent(self) -> None:
        source_root = self.make_source_repo()
        first_rel = ".aide/prompts/compact-task.md"
        second_rel = ".aide/policies/token-budget.yaml"
        pack_v1 = self.freeze_pack(source_root, "rollback-prior-intent-v1")
        target = source_root.parent / "target-rollback-prior-intent"
        self.assertEqual(aide_lite.apply_import_pack(pack_v1, target)["status"], "APPLIED")
        aide_lite.write_text(source_root / first_rel, "# Pending release one\n")
        aide_lite.write_text(source_root / second_rel, "version: pending-release\n")
        pack_v2 = self.freeze_pack(source_root, "rollback-prior-intent-v2")
        self.assertEqual(aide_lite.apply_import_pack(pack_v2, target, predecessor_pack=pack_v1, fail_after_writes=1)["status"], "INTERRUPTED")
        intent_path = target / aide_lite.PORTABLE_IMPORT_INTENT_PATH
        receipt_path = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        intent_bytes, receipt_bytes = intent_path.read_bytes(), receipt_path.read_bytes()
        preview = aide_lite.build_portable_rollback_plan(pack_v2, pack_v1, target)
        self.assertEqual(preview["status"], "RECOVERY_REQUIRED")
        with self.assertRaisesRegex(ValueError, "exact preview digest"):
            aide_lite.apply_portable_rollback(pack_v2, pack_v1, target, "")
        self.assertEqual(intent_path.read_bytes(), intent_bytes)
        self.assertEqual(receipt_path.read_bytes(), receipt_bytes)

    def test_dry_run_never_reconciles_a_pending_import_intent(self) -> None:
        source_root = self.make_source_repo()
        managed_rel = ".aide/prompts/compact-task.md"
        pack_v1 = self.freeze_pack(source_root, "recovery-dry-v1")
        target = source_root.parent / "target-recovery-dry"
        self.assertEqual(aide_lite.apply_import_pack(pack_v1, target)["status"], "APPLIED")
        receipt = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        intent = target / aide_lite.PORTABLE_IMPORT_INTENT_PATH

        aide_lite.write_text(source_root / managed_rel, "# Recovery candidate two\n")
        pack_v2 = self.freeze_pack(source_root, "recovery-dry-v2")
        interrupted = aide_lite.apply_import_pack(pack_v2, target, fail_after_writes=1)
        self.assertEqual(interrupted["status"], "INTERRUPTED")
        self.assertEqual(interrupted["recovery"]["classification"], "completed")
        intent_before = intent.read_bytes()
        receipt_before = receipt.read_bytes()
        target_before = (target / managed_rel).read_bytes()
        preview = aide_lite.apply_import_pack(pack_v2, target, dry_run=True)
        self.assertEqual(preview["status"], "RECOVERY_REQUIRED")
        self.assertTrue(preview["dry_run"])
        self.assertEqual(preview["recovery"]["classification"], "completed")
        self.assertEqual(intent.read_bytes(), intent_before)
        self.assertEqual(receipt.read_bytes(), receipt_before)

        self.assertEqual((target / managed_rel).read_bytes(), target_before)

        script = source_root / ".aide/scripts/aide_lite.py"
        feedback = source_root.parent / "recovery-feedback.json"
        command = [sys.executable, str(script), "--repo-root", str(source_root), "import-pack", "--pack", str(pack_v2), "--target", str(target), "--dry-run", "--feedback-out", str(feedback)]
        refused = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(refused.returncode, 0)
        self.assertFalse(feedback.exists())
        self.assertEqual(intent.read_bytes(), intent_before)
        self.assertEqual(receipt.read_bytes(), receipt_before)
        self.assertEqual(aide_lite.apply_import_pack(pack_v2, target)["status"], "RECOVERED")

        aide_lite.write_text(source_root / managed_rel, "# Recovery candidate three\n")
        pack_v3 = self.freeze_pack(source_root, "recovery-dry-v3")
        preimage = (target / managed_rel).read_bytes()
        interrupted = aide_lite.apply_import_pack(pack_v3, target, fail_after_writes=1)
        self.assertEqual(interrupted["status"], "INTERRUPTED")
        (target / managed_rel).write_bytes(preimage)
        intent_before = intent.read_bytes()
        receipt_before = receipt.read_bytes()
        preview = aide_lite.apply_import_pack(pack_v3, target, dry_run=True)
        self.assertEqual(preview["status"], "RECOVERY_REQUIRED")
        self.assertEqual(preview["recovery"]["classification"], "no_effect")
        self.assertEqual(intent.read_bytes(), intent_before)
        self.assertEqual(receipt.read_bytes(), receipt_before)

    def test_pack_cannot_supply_project_owned_customization_metadata(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "reserved-project-metadata")
        payload = pack / "files" / aide_lite.PROJECT_CUSTOMIZATIONS_PATH
        aide_lite.write_text(payload, '{"schema_version":"aide.project-customizations.v1","entries":{}}\n')
        checksums_path = pack / "checksums.json"
        checksums = json.loads(aide_lite.read_text(checksums_path))
        checksums["checksums"]["files/" + aide_lite.PROJECT_CUSTOMIZATIONS_PATH] = aide_lite.sha256_file(payload)
        aide_lite.write_text(checksums_path, json.dumps(checksums, sort_keys=True) + "\n")
        self.assertTrue(aide_lite.validate_pack_checksums(pack)[0])
        target = source_root.parent / "reserved-project-target"
        original = b'{"project":"owned"}\n'
        authored = target / aide_lite.PROJECT_CUSTOMIZATIONS_PATH
        authored.parent.mkdir(parents=True)
        authored.write_bytes(original)
        with self.assertRaisesRegex(ValueError, "reserved project/import state"):
            aide_lite.apply_import_pack(pack, target)
        self.assertEqual(authored.read_bytes(), original)
        self.assertFalse((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).exists())
        self.assertFalse((target / aide_lite.PORTABLE_IMPORT_INTENT_PATH).exists())
        payload.unlink()
        checksums["checksums"].pop("files/" + aide_lite.PROJECT_CUSTOMIZATIONS_PATH)
        alias_rel = ".aide/CUSTOMIZATIONS.JSON"
        alias_payload = pack / "files" / alias_rel
        aide_lite.write_text(alias_payload, '{"schema_version":"aide.project-customizations.v1","entries":{}}\n')
        checksums["checksums"]["files/" + alias_rel] = aide_lite.sha256_file(alias_payload)
        aide_lite.write_text(checksums_path, json.dumps(checksums, sort_keys=True) + "\n")
        self.assertTrue(aide_lite.validate_pack_checksums(pack)[0])
        with self.assertRaisesRegex(ValueError, "reserved project/import state"):
            aide_lite.apply_import_pack(pack, target)
        self.assertEqual(authored.read_bytes(), original)

    def test_import_payload_does_not_follow_a_swapped_parent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            target_root = root / "target"
            parent = target_root / ".aide" / "prompts"
            parent.mkdir(parents=True)
            parked = target_root / ".aide" / "prompts-parked"
            outside = root / "outside"
            outside.mkdir()
            self.assertEqual(parent.resolve().parent, (target_root / ".aide").resolve())
            self.assertEqual(parked.parent.resolve(), (target_root / ".aide").resolve())

            source_rel = ".aide/prompts/compact-task.md"
            payload = b"# Portable managed content\n"
            pack_root = root / "pack"
            source = pack_root / "files" / source_rel
            source.parent.mkdir(parents=True)
            source.write_bytes(payload)
            operation = {
                "action": "copy",
                "target": source_rel,
                "source": source_rel,
                "kind": "managed_file",
                "preimage_digest": "missing",
                "postimage_digest": aide_lite.digest_bytes(payload),
            }

            original_mkstemp = tempfile.mkstemp
            attempted = False

            def swap_before_staging(*args: object, **kwargs: object) -> tuple[int, str]:
                nonlocal attempted
                if Path(str(kwargs.get("dir"))) == parent and not attempted:
                    attempted = True
                    try:
                        parent.rename(parked)
                    except PermissionError:
                        # A pinned ancestor that denies deletion has already
                        # closed this interleaving; staging can continue.
                        pass
                    else:
                        if sys.platform == "win32":
                            junction = subprocess.run(
                                ["cmd", "/c", "mklink", "/J", str(parent), str(outside)],
                                capture_output=True,
                                text=True,
                                encoding="utf-8",
                            )
                            self.assertEqual(junction.returncode, 0, junction.stderr)
                        else:
                            parent.symlink_to(outside, target_is_directory=True)
                return original_mkstemp(*args, **kwargs)

            try:
                with mock.patch.object(aide_lite.tempfile, "mkstemp", side_effect=swap_before_staging):
                    try:
                        aide_lite.apply_import_operation(pack_root, target_root, operation)
                    except (OSError, RuntimeError, ValueError):
                        pass
                outside_entries = list(outside.iterdir())
            finally:
                if parent.is_symlink():
                    parent.unlink()
                elif getattr(parent, "is_junction", lambda: False)():
                    parent.rmdir()
                if parked.exists():
                    parked.rename(parent)

            self.assertTrue(attempted, "the importer must exercise the staging boundary")
            self.assertEqual(outside_entries, [], "import wrote through a swapped parent")

    def test_import_payload_does_not_clobber_a_racing_leaf(self) -> None:
        for initial in (None, b"# Previously managed content\n"):
            with self.subTest(initial=initial), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                target_root = root / "target"
                target = target_root / ".aide" / "prompts" / "compact-task.md"
                target.parent.mkdir(parents=True)
                if initial is not None:
                    target.write_bytes(initial)
                pack_root = root / "pack"
                source_rel = ".aide/prompts/compact-task.md"
                source = pack_root / "files" / source_rel
                source.parent.mkdir(parents=True)
                source.write_bytes(b"# Updated managed content\n")
                operation = {
                    "action": "copy" if initial is None else "update_owned",
                    "target": source_rel,
                    "source": source_rel,
                    "kind": "managed_file",
                    "preimage_digest": "missing" if initial is None else aide_lite.digest_bytes(initial),
                    "postimage_digest": aide_lite.digest_bytes(source.read_bytes()),
                }
                competing = b"# Concurrent project edit\n"
                original_mkstemp = tempfile.mkstemp
                attempted = False

                def change_leaf_after_preimage(*args: object, **kwargs: object) -> tuple[int, str]:
                    nonlocal attempted
                    descriptor, temporary_name = original_mkstemp(*args, **kwargs)
                    if Path(str(kwargs.get("dir"))) == target.parent and not attempted:
                        attempted = True
                        target.write_bytes(competing)
                    return descriptor, temporary_name

                with mock.patch.object(aide_lite.tempfile, "mkstemp", side_effect=change_leaf_after_preimage):
                    try:
                        aide_lite.apply_import_operation(pack_root, target_root, operation)
                    except (OSError, RuntimeError, ValueError):
                        pass
                self.assertTrue(attempted, "the importer must exercise the staging boundary")
                self.assertEqual(target.read_bytes(), competing, "import replaced a concurrent project edit")

    @unittest.skipUnless(sys.platform == "win32", "requires Windows guarded staging")
    def test_atomic_create_staged_bytes_deny_rival_writer(self) -> None:
        for relative in (".aide/install/aide-lite-pack-v0.repair-intent.json", ".aide/prompts/compact-task.md"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as raw:
                target = Path(raw) / relative
                target.parent.mkdir(parents=True)
                original_link = aide_lite.windows_link_from_handle
                attempted = False

                def rival_before_publication(descriptor: int, directory_handle: int, leaf_name: str) -> None:
                    nonlocal attempted
                    stage = list(target.parent.glob(f".{target.name}.*.tmp"))
                    self.assertEqual(len(stage), 1)
                    attempted = True
                    with self.assertRaises(OSError):
                        stage[0].write_bytes(b"rival bytes")
                    original_link(descriptor, directory_handle, leaf_name)

                with mock.patch.object(aide_lite, "windows_link_from_handle", side_effect=rival_before_publication):
                    aide_lite.atomic_create_bytes_no_clobber(target, b"expected bytes")
                self.assertTrue(attempted)
                self.assertEqual(target.read_bytes(), b"expected bytes")
                self.assertEqual(list(target.parent.iterdir()), [target])

    @unittest.skipUnless(sys.platform == "win32", "requires Windows guarded staging")
    def test_import_staged_bytes_refuse_rival_before_guard(self) -> None:
        for relative in (".aide/install/aide-lite-pack-v0.repair-intent.json", ".aide/prompts/compact-task.md"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as raw:
                target = Path(raw) / relative
                target.parent.mkdir(parents=True)
                original_verified = aide_lite.portable_import_verified_leaf
                attempted = False

                def rival_before_guard(path: Path, expected: str, *, writable: bool = False) -> tuple[object, object]:
                    nonlocal attempted
                    if writable and not attempted:
                        attempted = True
                        path.write_bytes(b"rival bytes")
                    return original_verified(path, expected, writable=writable)

                with mock.patch.object(aide_lite, "portable_import_verified_leaf", side_effect=rival_before_guard):
                    with self.assertRaises(RuntimeError):
                        aide_lite.portable_import_write_exact(Path(raw), relative, b"expected bytes", "missing")
                self.assertTrue(attempted)
                self.assertFalse(target.exists())
                stages = list(target.parent.glob(f".{target.name}.*.tmp"))
                self.assertEqual(len(stages), 1)
                self.assertEqual(stages[0].read_bytes(), b"rival bytes")

    @unittest.skipUnless(sys.platform == "win32", "requires Windows guarded staging")
    def test_import_staged_bytes_deny_rival_writer(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target_root = Path(raw) / "target"
            target_root.mkdir()
            target = target_root / "managed.txt"
            original_link = aide_lite.windows_link_from_handle
            attempted = False

            def rival_before_publication(descriptor: int, directory_handle: int, leaf_name: str) -> None:
                nonlocal attempted
                stage = list(target.parent.glob(f".{target.name}.*.tmp"))
                self.assertEqual(len(stage), 1)
                attempted = True
                with self.assertRaises(OSError):
                    stage[0].write_bytes(b"rival bytes")
                original_link(descriptor, directory_handle, leaf_name)

            with mock.patch.object(aide_lite, "windows_link_from_handle", side_effect=rival_before_publication):
                aide_lite.portable_import_write_exact(target_root, "managed.txt", b"expected bytes", "missing")
            self.assertTrue(attempted)
            self.assertEqual(target.read_bytes(), b"expected bytes")
            self.assertEqual(list(target.parent.iterdir()), [target])

    @unittest.skipUnless(sys.platform == "win32", "requires Windows no-replace publication")
    def test_import_update_preserves_preimage_backup_when_rival_wins_publish_gap(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            target_root = root / "target"
            target = target_root / ".aide" / "prompts" / "compact-task.md"
            target.parent.mkdir(parents=True)
            original = b"# Previously managed content\n"
            competing = b"# Concurrent project edit\n"
            target.write_bytes(original)
            backup_rel = ".aide/prompts/.compact-task.md.aide-import-backup-test"
            backup = target_root / backup_rel
            original_link = aide_lite.windows_link_from_handle
            attempted = False

            def rival_at_publication(descriptor: int, directory_handle: int, leaf_name: str) -> None:
                nonlocal attempted
                if leaf_name == target.name and not attempted:
                    attempted = True
                    self.assertFalse(target.exists(), "the verified old leaf must be held under its backup")
                    target.write_bytes(competing)
                original_link(descriptor, directory_handle, leaf_name)

            with mock.patch.object(aide_lite, "windows_link_from_handle", side_effect=rival_at_publication):
                with self.assertRaises((OSError, RuntimeError)):
                    aide_lite.portable_import_write_exact(
                        target_root,
                        ".aide/prompts/compact-task.md",
                        b"# Incoming managed content\n",
                        aide_lite.digest_bytes(original),
                        backup_rel,
                    )
            self.assertTrue(attempted)
            self.assertEqual(target.read_bytes(), competing)
            self.assertEqual(backup.read_bytes(), original)

    @unittest.skipUnless(sys.platform == "win32", "requires Windows no-replace publication")
    def test_import_recovery_reports_backup_and_refuses_rival_replay(self) -> None:
        source_root = self.make_source_repo()
        source_rel = ".aide/prompts/compact-task.md"
        pack_v1 = self.freeze_pack(source_root, "backup-gap-v1")
        target_root = source_root.parent / "backup-gap-target"
        self.assertEqual(aide_lite.apply_import_pack(pack_v1, target_root)["status"], "APPLIED")
        target = target_root / source_rel
        original = target.read_bytes()
        competing = b"# Concurrent project edit during publish\n"
        aide_lite.write_text(source_root / source_rel, "# Incoming managed content\n")
        pack_v2 = self.freeze_pack(source_root, "backup-gap-v2")
        original_link = aide_lite.windows_link_from_handle
        attempted = False

        def rival_at_publication(descriptor: int, directory_handle: int, leaf_name: str) -> None:
            nonlocal attempted
            if leaf_name == target.name and not attempted:
                attempted = True
                self.assertFalse(target.exists())
                target.write_bytes(competing)
            original_link(descriptor, directory_handle, leaf_name)

        with mock.patch.object(aide_lite, "windows_link_from_handle", side_effect=rival_at_publication):
            result = aide_lite.apply_import_pack(pack_v2, target_root)
        self.assertTrue(attempted)
        self.assertEqual(result["status"], "INTERRUPTED")
        self.assertEqual(result["recovery"]["classification"], "unknown")
        intent = aide_lite.load_portable_import_intent(target_root)
        self.assertIsNotNone(intent)
        item = next(item for item in intent["operations"] if item["target"] == source_rel)
        backup_rel = item["backup_rel"]
        self.assertIn(backup_rel, result["recovery"]["outstanding_backups"])
        self.assertEqual((target_root / backup_rel).read_bytes(), original)
        self.assertEqual(target.read_bytes(), competing)
        resumed = aide_lite.apply_import_pack(pack_v2, target_root)
        self.assertEqual(resumed["status"], "RECOVERY_REQUIRED")
        self.assertEqual(resumed["recovery"]["classification"], "unknown")
        self.assertEqual(target.read_bytes(), competing)
        self.assertEqual((target_root / backup_rel).read_bytes(), original)

    def test_import_receipt_only_transition_uses_an_intent(self) -> None:
        source_root = self.make_source_repo()
        pack_v1 = self.freeze_pack(source_root, "receipt-only-v1")
        target_root = source_root.parent / "receipt-only-target"
        self.assertEqual(aide_lite.apply_import_pack(pack_v1, target_root)["status"], "APPLIED")
        pack_v2 = self.freeze_pack(source_root, "receipt-only-v2")
        self.set_manifest_scalars(pack_v2, {"source_commit": "a" * 40})
        self.assertTrue(aide_lite.validate_pack_checksums(pack_v2)[0])
        preview = aide_lite.apply_import_pack(pack_v2, target_root, dry_run=True)
        self.assertFalse(any(item["preimage_digest"] != item["postimage_digest"] for item in preview["operations"] if item["action"] != "conflict"))
        original_write = aide_lite.portable_import_write_exact
        saw_intent = False

        def observe_receipt_write(root: Path, rel: str, data: bytes, expected: str, backup_rel: str | None = None) -> aide_lite.WriteResult:
            nonlocal saw_intent
            if rel == aide_lite.PORTABLE_IMPORT_RECEIPT_PATH:
                saw_intent = (target_root / aide_lite.PORTABLE_IMPORT_INTENT_PATH).is_file()
            return original_write(root, rel, data, expected, backup_rel)

        if sys.platform == "win32":
            with mock.patch.object(aide_lite, "portable_import_write_exact", side_effect=observe_receipt_write):
                result = aide_lite.apply_import_pack(pack_v2, target_root)
            self.assertTrue(saw_intent)
        else:
            result = aide_lite.apply_import_pack(pack_v2, target_root)
        self.assertEqual(result["status"], "APPLIED")
        self.assertTrue(result["receipt_written"])
        self.assertEqual(result["written"], [])
        self.assertFalse((target_root / aide_lite.PORTABLE_IMPORT_INTENT_PATH).exists())

    @unittest.skipUnless(sys.platform == "win32", "requires Windows anchored intent cleanup")
    def test_import_recovers_after_receipt_commit_before_intent_cleanup(self) -> None:
        source_root = self.make_source_repo()
        source_rel = ".aide/prompts/compact-task.md"
        pack_v1 = self.freeze_pack(source_root, "receipt-commit-v1")
        target_root = source_root.parent / "receipt-commit-target"
        self.assertEqual(aide_lite.apply_import_pack(pack_v1, target_root)["status"], "APPLIED")
        aide_lite.write_text(source_root / source_rel, "# Updated managed content\n")
        pack_v2 = self.freeze_pack(source_root, "receipt-commit-v2")
        with mock.patch.object(aide_lite, "portable_import_delete_exact", side_effect=OSError("simulated interruption after receipt")):
            with self.assertRaisesRegex(OSError, "simulated interruption"):
                aide_lite.apply_import_pack(pack_v2, target_root)
        intent_path = target_root / aide_lite.PORTABLE_IMPORT_INTENT_PATH
        self.assertTrue(intent_path.is_file())
        receipt_before = (target_root / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes()
        target_before = (target_root / source_rel).read_bytes()
        recovered = aide_lite.apply_import_pack(pack_v2, target_root)
        self.assertEqual(recovered["status"], "RECOVERED")
        self.assertFalse(intent_path.exists())
        self.assertEqual((target_root / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes(), receipt_before)
        self.assertEqual((target_root / source_rel).read_bytes(), target_before)

    @unittest.skipUnless(sys.platform == "win32", "requires Windows junction and pinned handles")
    def test_import_receipt_does_not_follow_a_swapped_parent(self) -> None:
        source_root = self.make_source_repo()
        pack_v1 = self.freeze_pack(source_root, "receipt-parent-v1")
        target_root = source_root.parent / "receipt-parent-target"
        self.assertEqual(aide_lite.apply_import_pack(pack_v1, target_root)["status"], "APPLIED")
        pack_v2 = self.freeze_pack(source_root, "receipt-parent-v2")
        self.set_manifest_scalars(pack_v2, {"source_commit": "b" * 40})
        parent = target_root / ".aide" / "install"
        parked = target_root / ".aide" / "install-parked"
        outside = source_root.parent / "receipt-parent-outside"
        outside.mkdir()
        original_mkstemp = tempfile.mkstemp
        attempted = False

        def swap_before_receipt_staging(*args: object, **kwargs: object) -> tuple[int, str]:
            nonlocal attempted
            if Path(str(kwargs.get("dir"))) == parent and str(kwargs.get("prefix", "")).startswith(".aide-lite-pack-v0.receipt.json.") and not attempted:
                attempted = True
                try:
                    parent.rename(parked)
                except PermissionError:
                    pass
                else:
                    junction = subprocess.run(["cmd", "/c", "mklink", "/J", str(parent), str(outside)], capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(junction.returncode, 0, junction.stderr)
            return original_mkstemp(*args, **kwargs)

        try:
            with mock.patch.object(aide_lite.tempfile, "mkstemp", side_effect=swap_before_receipt_staging):
                try:
                    aide_lite.apply_import_pack(pack_v2, target_root)
                except (OSError, RuntimeError, ValueError):
                    pass
            outside_entries = list(outside.iterdir())
        finally:
            if parent.is_symlink():
                parent.unlink()
            elif getattr(parent, "is_junction", lambda: False)():
                parent.rmdir()
            if parked.exists():
                parked.rename(parent)
        self.assertTrue(attempted)
        self.assertEqual(outside_entries, [], "import wrote a receipt through a swapped parent")

    def test_import_intent_does_not_follow_a_swapped_parent(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "intent-parent-pack")
        target_root = source_root.parent / "intent-parent-target"
        parent = target_root / ".aide" / "install"
        parent.mkdir(parents=True)
        parked = target_root / ".aide" / "install-parked"
        outside = source_root.parent / "intent-parent-outside"
        outside.mkdir()
        original_mkstemp = tempfile.mkstemp
        attempted = False

        def swap_before_intent_staging(*args: object, **kwargs: object) -> tuple[int, str]:
            nonlocal attempted
            if Path(str(kwargs.get("dir"))) == parent and not attempted:
                attempted = True
                try:
                    parent.rename(parked)
                except PermissionError:
                    pass
                else:
                    if sys.platform == "win32":
                        junction = subprocess.run(
                            ["cmd", "/c", "mklink", "/J", str(parent), str(outside)],
                            capture_output=True,
                            text=True,
                            encoding="utf-8",
                        )
                        self.assertEqual(junction.returncode, 0, junction.stderr)
                    else:
                        parent.symlink_to(outside, target_is_directory=True)
            return original_mkstemp(*args, **kwargs)

        try:
            with mock.patch.object(aide_lite.tempfile, "mkstemp", side_effect=swap_before_intent_staging):
                try:
                    aide_lite.apply_import_pack(pack, target_root)
                except (OSError, RuntimeError, ValueError):
                    pass
            outside_entries = list(outside.iterdir())
        finally:
            if parent.is_symlink():
                parent.unlink()
            elif getattr(parent, "is_junction", lambda: False)():
                parent.rmdir()
            if parked.exists():
                parked.rename(parent)

        self.assertTrue(attempted, "the importer must exercise the intent staging boundary")
        self.assertEqual(outside_entries, [], "import wrote an intent through a swapped parent")

    def test_removal_plan_requires_an_exact_valid_receipt(self) -> None:
        source_root = self.make_source_repo()
        target = source_root.parent / "target-removal-receipt"
        target.mkdir()

        with self.assertRaisesRegex(ValueError, "portable import receipt missing"):
            aide_lite.build_portable_removal_plan(target)

        aide_lite.write_text(target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH, "not json\n")
        with self.assertRaisesRegex(ValueError, "invalid portable import receipt"):
            aide_lite.build_portable_removal_plan(target)

        pack = self.freeze_pack(source_root, "removal-receipt-pack")
        shutil.rmtree(target)
        aide_lite.apply_import_pack(pack, target)
        receipt_path = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["plan_digest"] = "tampered"
        aide_lite.write_text(receipt_path, aide_lite.stable_json_text(receipt))
        with self.assertRaisesRegex(ValueError, "portable import receipt digest mismatch"):
            aide_lite.build_portable_removal_plan(target)

    def test_removal_plan_is_read_only_and_preserves_non_owned_bytes(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-plan-pack")
        target = source_root.parent / "target-removal-plan"
        aide_lite.write_text(target / "AGENTS.md", "# Target Agents\n\nAuthored guidance.\n")
        applied = aide_lite.apply_import_pack(pack, target)
        self.assertEqual(applied["status"], "APPLIED")
        aide_lite.write_text(target / "unknown.txt", "target owned\n")

        before = {
            aide_lite.normalize_rel(path.relative_to(target)): path.read_bytes()
            for path in sorted(target.rglob("*"))
            if path.is_file()
        }
        plan = aide_lite.build_portable_removal_plan(target)
        after = {
            aide_lite.normalize_rel(path.relative_to(target)): path.read_bytes()
            for path in sorted(target.rglob("*"))
            if path.is_file()
        }

        self.assertEqual(plan["status"], "PLANNED")
        self.assertTrue(plan["read_only"])
        self.assertFalse(plan["apply_allowed"])
        self.assertFalse(plan["delete_allowed"])
        self.assertEqual(before, after)
        self.assertEqual(plan["candidate_count"], len(plan["operations"]))
        self.assertNotIn("unknown.txt", {item["target"] for item in plan["operations"]})
        agents = next(item for item in plan["operations"] if item["target"] == "AGENTS.md")
        self.assertEqual(agents["action"], "remove_managed_section_future")
        self.assertTrue(agents["preserves_authored_content"])
        self.assertIn("Authored guidance.", aide_lite.read_text(target / "AGENTS.md"))
        for rel in [
            ".aide/profile.yaml",
            ".aide/memory/project-state.md",
            ".aide/memory/decisions.md",
            ".aide/memory/open-risks.md",
            ".gitignore",
            "unknown.txt",
        ]:
            self.assertNotIn(rel, plan["candidate_targets"])

        managed_rel = ".aide/prompts/compact-task.md"
        aide_lite.write_text(target / managed_rel, "# Local edit\n")
        edited = aide_lite.build_portable_removal_plan(target)
        operation = next(item for item in edited["operations"] if item["target"] == managed_rel)
        self.assertEqual(edited["status"], "PRESERVATION_REQUIRED")
        self.assertEqual(operation["action"], "preserve_local_or_unknown")
        self.assertFalse(operation["removal_candidate"])
        self.assertNotEqual(edited["plan_digest"], plan["plan_digest"])
        self.assertEqual(aide_lite.read_text(target / managed_rel), "# Local edit\n")

    def test_removal_plan_identity_changes_with_receipt_or_managed_state(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-identity-pack")
        target = source_root.parent / "target-removal-identity"
        aide_lite.apply_import_pack(pack, target)
        original = aide_lite.build_portable_removal_plan(target)

        receipt_path = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["plan_digest"] = "f" * 64
        receipt["receipt_digest"] = aide_lite.portable_import_record_digest(receipt, "receipt_digest")
        aide_lite.write_text(receipt_path, aide_lite.stable_json_text(receipt))
        changed_receipt = aide_lite.build_portable_removal_plan(target)
        self.assertNotEqual(changed_receipt["plan_digest"], original["plan_digest"])

        managed_rel = next(
            item["target"]
            for item in changed_receipt["operations"]
            if item["kind"] == "managed_file"
        )
        (target / managed_rel).unlink()
        missing = aide_lite.build_portable_removal_plan(target)
        operation = next(item for item in missing["operations"] if item["target"] == managed_rel)
        self.assertEqual(operation["action"], "preserve_already_absent")
        self.assertFalse(operation["removal_candidate"])
        self.assertNotEqual(missing["plan_digest"], changed_receipt["plan_digest"])

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_removal_apply_requires_exact_plan_and_preserves_authored_state(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-apply-pack")
        target = source_root.parent / "target-removal-apply"
        aide_lite.write_text(target / "AGENTS.md", "# Project guidance\n\nKeep my authored words.\n")
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "APPLIED")
        managed_rel = ".aide/prompts/compact-task.md"
        changed_rel = ".aide/policies/token-budget.yaml"
        aide_lite.write_text(target / changed_rel, "# Direct target edit\n")
        aide_lite.write_text(target / "unknown.txt", "target owned\n")
        receipt = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        receipt_bytes = receipt.read_bytes()
        agents_bytes = (target / "AGENTS.md").read_bytes()
        original_plan = aide_lite.build_portable_removal_plan(target)
        self.assertEqual(aide_lite.apply_portable_removal(target, "f" * 64)["status"], "STALE_PLAN")
        self.assertTrue((target / managed_rel).is_file())

        result = aide_lite.apply_portable_removal(target, original_plan["plan_digest"])
        self.assertEqual(result["status"], "PARTIAL_REMOVAL")
        self.assertIn(managed_rel, result["removed"])
        self.assertFalse((target / managed_rel).exists())
        self.assertEqual((target / changed_rel).read_text(encoding="utf-8"), "# Direct target edit\n")
        self.assertEqual((target / "unknown.txt").read_text(encoding="utf-8"), "target owned\n")
        self.assertEqual((target / "AGENTS.md").read_bytes(), agents_bytes)
        self.assertTrue((target / aide_lite.PORTABLE_REMOVAL_RUNNER_PATH).is_file())
        self.assertEqual(receipt.read_bytes(), receipt_bytes)
        self.assertFalse((target / aide_lite.PORTABLE_REMOVAL_INTENT_PATH).exists())
        self.assertEqual(aide_lite.apply_portable_removal(target, original_plan["plan_digest"])["status"], "STALE_PLAN")
        remaining = aide_lite.build_portable_removal_plan(target)
        self.assertGreater(remaining["preservation_count"], 0)
        self.assertEqual(aide_lite.apply_portable_removal(target, remaining["plan_digest"])["status"], "PRESERVATION_REQUIRED")
        installed_plan = subprocess.run(
            [sys.executable, str(target / aide_lite.PORTABLE_REMOVAL_RUNNER_PATH), "--repo-root", str(target),
             "plan-removal", "--target", str(target), "--json"],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertIn(installed_plan.returncode, (0, 2), installed_plan.stderr)
        self.assertEqual(json.loads(installed_plan.stdout)["plan_digest"], remaining["plan_digest"])
        self.assertEqual(receipt.read_bytes(), receipt_bytes)

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_removal_interruption_keeps_intent_and_reconciles_exact_bytes(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-recovery-pack")
        target = source_root.parent / "target-removal-recovery"
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "APPLIED")
        plan = aide_lite.build_portable_removal_plan(target)
        interrupted = aide_lite.apply_portable_removal(target, plan["plan_digest"], fail_after_removals=1)
        self.assertEqual(interrupted["status"], "INTERRUPTED")
        intent = target / aide_lite.PORTABLE_REMOVAL_INTENT_PATH
        self.assertTrue(intent.is_file())
        self.assertEqual(len(interrupted["removed"]), 1)
        with self.assertRaisesRegex(ValueError, "removal recovery"):
            aide_lite.build_portable_removal_plan(target)
        with self.assertRaisesRegex(ValueError, "removal recovery"):
            aide_lite.apply_import_pack(pack, target)
        resumed = aide_lite.apply_portable_removal(target, plan["plan_digest"])
        self.assertEqual(resumed["status"], "DETACHED")
        self.assertFalse(intent.exists())
        self.assertFalse((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).exists())
        self.assertFalse((target / aide_lite.PORTABLE_REMOVAL_RUNNER_PATH).exists())
        self.assertFalse((target / "AGENTS.md").exists())

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_removal_rejects_rechecksummed_intent_for_later_authored_managed_file(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-forged-managed-intent-pack")
        target = source_root.parent / "target-removal-forged-managed-intent"
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "APPLIED")
        plan = aide_lite.build_portable_removal_plan(target)
        self.assertEqual(aide_lite.apply_portable_removal(target, plan["plan_digest"], fail_after_removals=1)["status"], "INTERRUPTED")
        intent_path = target / aide_lite.PORTABLE_REMOVAL_INTENT_PATH
        receipt_path = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        intent = json.loads(intent_path.read_text(encoding="utf-8"))
        operation = next(item for item in intent["operations"] if item["kind"] == "managed_file" and (target / item["target"]).is_file())
        authored = b"project's later authored bytes\n"
        (target / operation["target"]).write_bytes(authored)
        operation["preimage_digest"] = aide_lite.digest_bytes(authored)
        intent["intent_digest"] = aide_lite.portable_import_record_digest(intent, "intent_digest")
        aide_lite.write_text(intent_path, aide_lite.stable_json_text(intent))
        receipt_bytes = receipt_path.read_bytes()
        with self.assertRaisesRegex(ValueError, "preimage differs from installed bytes"):
            aide_lite.apply_portable_removal(target, plan["plan_digest"])
        self.assertEqual((target / operation["target"]).read_bytes(), authored)
        self.assertEqual(receipt_path.read_bytes(), receipt_bytes)

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_removal_rejects_rechecksummed_intent_for_authored_agents_file(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-forged-agents-intent-pack")
        target = source_root.parent / "target-removal-forged-agents-intent"
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "APPLIED")
        plan = aide_lite.build_portable_removal_plan(target)
        self.assertEqual(aide_lite.apply_portable_removal(target, plan["plan_digest"], fail_after_removals=1)["status"], "INTERRUPTED")
        intent_path = target / aide_lite.PORTABLE_REMOVAL_INTENT_PATH
        receipt_path = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        intent = json.loads(intent_path.read_text(encoding="utf-8"))
        operation = next(item for item in intent["operations"] if item["kind"] == "standalone_managed_agents")
        agents_path = target / "AGENTS.md"
        authored = b"# Project authored preface\n" + agents_path.read_bytes()
        agents_path.write_bytes(authored)
        operation["preimage_digest"] = aide_lite.digest_bytes(authored)
        intent["intent_digest"] = aide_lite.portable_import_record_digest(intent, "intent_digest")
        aide_lite.write_text(intent_path, aide_lite.stable_json_text(intent))
        receipt_bytes = receipt_path.read_bytes()
        result = aide_lite.apply_portable_removal(target, plan["plan_digest"])
        self.assertEqual(result["status"], "RECOVERY_REQUIRED")
        self.assertEqual(agents_path.read_bytes(), authored)
        self.assertEqual(receipt_path.read_bytes(), receipt_bytes)

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_removal_recovers_after_receipt_retirement_before_intent_cleanup(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-retirement-pack")
        target = source_root.parent / "target-removal-retirement"
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "APPLIED")
        aide_lite.write_text(target / "unknown.txt", "keep target data\n")
        plan = aide_lite.build_portable_removal_plan(target)
        stopped = aide_lite.apply_portable_removal(target, plan["plan_digest"], fail_after_receipt=True)
        self.assertEqual(stopped["status"], "INTERRUPTED")
        self.assertFalse((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).exists())
        self.assertFalse((target / aide_lite.PORTABLE_REMOVAL_RUNNER_PATH).exists())
        self.assertTrue((target / aide_lite.PORTABLE_REMOVAL_INTENT_PATH).is_file())
        self.assertEqual(aide_lite.read_text(target / "unknown.txt"), "keep target data\n")
        recovered = aide_lite.apply_portable_removal(target, plan["plan_digest"])
        self.assertEqual(recovered["status"], "DETACHED_RECOVERED")
        self.assertFalse((target / aide_lite.PORTABLE_REMOVAL_INTENT_PATH).exists())
        self.assertEqual(aide_lite.read_text(target / "unknown.txt"), "keep target data\n")

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_removal_retains_receipt_when_one_owned_file_is_already_absent(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-already-absent-pack")
        target = source_root.parent / "target-removal-already-absent"
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "APPLIED")
        missing = target / ".aide/prompts/compact-task.md"
        missing.unlink()
        plan = aide_lite.build_portable_removal_plan(target)
        self.assertEqual(plan["status"], "PRESERVATION_REQUIRED")
        self.assertIn(".aide/prompts/compact-task.md", plan["preserved_recorded_targets"])
        result = aide_lite.apply_portable_removal(target, plan["plan_digest"])
        self.assertEqual(result["status"], "PARTIAL_REMOVAL")
        self.assertTrue((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).exists())
        self.assertTrue((target / aide_lite.PORTABLE_REMOVAL_RUNNER_PATH).exists())
        self.assertFalse((target / "AGENTS.md").exists())
        self.assertFalse(missing.exists())

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_removal_does_not_retire_receipt_at_absent_path_race_boundary(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-absent-race-pack")
        target = source_root.parent / "target-removal-absent-race"
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "APPLIED")
        missing = target / ".aide/prompts/compact-task.md"
        missing.unlink()
        plan = aide_lite.build_portable_removal_plan(target)
        receipt_path = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        original_unlink = aide_lite.windows_unlink_exact_portable_file
        receipt_attempts = []
        def intercept_receipt(path, expected_digest):
            if path == receipt_path:
                receipt_attempts.append(path)
                missing.write_bytes(b"project created this at retirement boundary\n")
            return original_unlink(path, expected_digest)
        with mock.patch.object(aide_lite, "windows_unlink_exact_portable_file", side_effect=intercept_receipt):
            result = aide_lite.apply_portable_removal(target, plan["plan_digest"], fail_after_receipt=True)
        self.assertEqual(result["status"], "PARTIAL_REMOVAL")
        self.assertEqual(receipt_attempts, [])
        self.assertTrue(receipt_path.is_file())
        new_bytes = b"project created this after partial removal\n"
        missing.write_bytes(new_bytes)
        self.assertEqual(aide_lite.apply_portable_removal(target, plan["plan_digest"])["status"], "STALE_PLAN")
        self.assertEqual(missing.read_bytes(), new_bytes)
        self.assertTrue(receipt_path.is_file())
        self.assertTrue((target / aide_lite.PORTABLE_REMOVAL_RUNNER_PATH).is_file())

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_removal_preview_refuses_changed_receipt_or_managed_bytes(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-stale-pack")
        target = source_root.parent / "target-removal-stale"
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "APPLIED")
        preview = aide_lite.build_portable_removal_plan(target)
        managed_rel = next(item["target"] for item in preview["operations"] if item["kind"] == "managed_file" and item["removal_candidate"])
        original = (target / managed_rel).read_bytes()
        changed = b"project's later edit\n"
        (target / managed_rel).write_bytes(changed)
        self.assertEqual(aide_lite.apply_portable_removal(target, preview["plan_digest"])["status"], "STALE_PLAN")
        self.assertEqual((target / managed_rel).read_bytes(), changed)
        (target / managed_rel).write_bytes(original)
        receipt_path = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["plan_digest"] = "a" * 64
        receipt["receipt_digest"] = aide_lite.portable_import_record_digest(receipt, "receipt_digest")
        aide_lite.write_text(receipt_path, aide_lite.stable_json_text(receipt))
        self.assertEqual(aide_lite.apply_portable_removal(target, preview["plan_digest"])["status"], "STALE_PLAN")
        self.assertEqual((target / managed_rel).read_bytes(), original)
        self.assertFalse((target / aide_lite.PORTABLE_REMOVAL_INTENT_PATH).exists())

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_removal_leaf_change_before_handle_open_is_preserved(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-leaf-race-pack")
        target = source_root.parent / "target-removal-leaf-race"
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "APPLIED")
        plan = aide_lite.build_portable_removal_plan(target)
        first = next(item for item in plan["operations"] if item["removal_candidate"] and item["kind"] == "managed_file")
        original = aide_lite.windows_unlink_exact_portable_file
        altered = b"project wrote during removal\n"
        def replace_leaf(path: Path, digest: str) -> None:
            if path == target / first["target"]:
                path.write_bytes(altered)
            original(path, digest)
        with mock.patch.object(aide_lite, "windows_unlink_exact_portable_file", side_effect=replace_leaf):
            result = aide_lite.apply_portable_removal(target, plan["plan_digest"])
        self.assertEqual(result["status"], "RECOVERY_REQUIRED")
        self.assertEqual((target / first["target"]).read_bytes(), altered)
        self.assertTrue((target / aide_lite.PORTABLE_REMOVAL_INTENT_PATH).is_file())
        self.assertTrue((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).is_file())

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_fresh_agents_edit_at_effect_time_is_preserved_with_receipt(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "removal-agents-race-pack")
        target = source_root.parent / "target-removal-agents-race"
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "APPLIED")
        plan = aide_lite.build_portable_removal_plan(target)
        agents = target / "AGENTS.md"
        original = aide_lite.windows_unlink_exact_portable_file
        authored = b"# Newly authored guidance\n\n" + agents.read_bytes()
        attempted = False
        def change_agents(path: Path, digest: str, before_disposition=None) -> None:
            nonlocal attempted
            if path == agents:
                attempted = True
                path.write_bytes(authored)
            original(path, digest, before_disposition=before_disposition)
        with mock.patch.object(aide_lite, "windows_unlink_exact_portable_file", side_effect=change_agents):
            result = aide_lite.apply_portable_removal(target, plan["plan_digest"])
        self.assertTrue(attempted)
        self.assertEqual(result["status"], "RECOVERY_REQUIRED")
        self.assertEqual(agents.read_bytes(), authored)
        self.assertTrue((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).is_file())
        self.assertTrue((target / aide_lite.PORTABLE_REMOVAL_INTENT_PATH).is_file())
        self.assertTrue((target / aide_lite.PORTABLE_REMOVAL_RUNNER_PATH).is_file())

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_removal_rejects_parent_junction_swapped_at_handle_open(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        parent = root / "target" / "owned"
        outside = root / "outside"
        parent.mkdir(parents=True)
        outside.mkdir()
        leaf = parent / "payload.txt"
        data = b"exact recorded bytes\n"
        leaf.write_bytes(data)
        (outside / leaf.name).write_bytes(data)
        parked = parent.with_name("parked-owned")
        original = aide_lite.windows_pinned_directory
        invoked = False
        def swap_then_pin(path: Path):
            nonlocal invoked
            if not invoked:
                invoked = True
                parent.rename(parked)
                linked = subprocess.run(["cmd", "/c", "mklink", "/J", str(parent), str(outside)], capture_output=True, text=True)
                if linked.returncode:
                    parked.rename(parent)
                    self.skipTest("junction creation unavailable: " + linked.stderr)
            return original(path)
        try:
            with mock.patch.object(aide_lite, "windows_pinned_directory", side_effect=swap_then_pin):
                with self.assertRaises((ValueError, OSError)):
                    aide_lite.windows_unlink_exact_portable_file(leaf, aide_lite.digest_bytes(data))
            self.assertTrue(invoked)
            self.assertEqual((outside / leaf.name).read_bytes(), data)
            self.assertEqual((parked / leaf.name).read_bytes(), data)
        finally:
            if parent.is_junction():
                os.rmdir(parent)

    @unittest.skipUnless(os.name == "nt", "anchored portable removal apply is Windows only")
    def test_removal_handle_refuses_a_competing_writer_or_hard_link(self) -> None:
        import ctypes
        from ctypes import wintypes

        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        leaf = root / "owned.txt"
        data = b"receipt-owned bytes\n"
        leaf.write_bytes(data)
        digest = aide_lite.digest_bytes(data)

        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        kernel.CreateFileW.restype = wintypes.HANDLE
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle.restype = wintypes.BOOL
        writer = kernel.CreateFileW(str(leaf), 0x40000000, 0x1 | 0x2 | 0x4, None, 3, 0, None)
        self.assertNotEqual(writer, ctypes.c_void_p(-1).value)
        try:
            with self.assertRaises(OSError):
                aide_lite.windows_unlink_exact_portable_file(leaf, digest)
        finally:
            kernel.CloseHandle(writer)
        self.assertEqual(leaf.read_bytes(), data)

        alias = root / "project-owned-alias.txt"
        os.link(leaf, alias)
        with self.assertRaisesRegex(ValueError, "multiple hard links"):
            aide_lite.windows_unlink_exact_portable_file(leaf, digest)
        self.assertEqual(leaf.read_bytes(), data)
        self.assertEqual(alias.read_bytes(), data)
        alias.unlink()

        attempted = []
        def competing_opens() -> None:
            for access in (0x40000000, 0x00010000):  # write, delete
                competing = kernel.CreateFileW(str(leaf), access, 0x1 | 0x2 | 0x4, None, 3, 0, None)
                attempted.append((access, competing))
                if competing != ctypes.c_void_p(-1).value:
                    kernel.CloseHandle(competing)
        aide_lite.windows_unlink_exact_portable_file(leaf, digest, before_disposition=competing_opens)
        self.assertEqual(len(attempted), 2)
        self.assertTrue(all(handle == ctypes.c_void_p(-1).value for _, handle in attempted))
        self.assertFalse(leaf.exists())

    def test_fake_secret_source_file_is_not_exported(self) -> None:
        source_root = self.make_source_repo()
        aide_lite.write_text(source_root / ".aide/prompts/compact-task.md", "api_key = \"abcdefghijklmnop\"\n")
        self.assertFalse(aide_lite.is_exportable_file(source_root, ".aide/prompts/compact-task.md"))
        pack_root = self.build_pack(source_root)
        self.assertFalse((pack_root / "files/.aide/prompts/compact-task.md").exists())

    def test_owned_repair_restores_missing_file_from_extracted_pack(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "repair-pack")
        target = source_root.parent / "repair-consumer"
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "APPLIED")
        rel = ".aide/prompts/compact-task.md"
        managed = target / rel
        expected = managed.read_bytes()
        managed.unlink()
        cli = pack / "files/.aide/scripts/aide_lite.py"
        command = [sys.executable, "-I", "-B", str(cli), "--repo-root", str(target), "repair-owned-file", "--pack", str(pack), "--target", str(target), "--path", rel]
        preview = subprocess.run([*command, "--dry-run"], text=True, capture_output=True)
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertIn("status: PLANNED", preview.stdout)
        plan_digest = next(line.partition(": ")[2] for line in preview.stdout.splitlines() if line.startswith("plan_digest: "))
        self.assertFalse((target / aide_lite.PORTABLE_REPAIR_INTENT_PATH).exists())
        applied = subprocess.run([*command, "--expect-plan", plan_digest], text=True, capture_output=True)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertIn("status: APPLIED", applied.stdout)
        self.assertEqual(managed.read_bytes(), expected)
        self.assertFalse((target / aide_lite.PORTABLE_REPAIR_INTENT_PATH).exists())
        self.assertEqual(aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)["status"], "CONFLICT")

    def test_owned_repair_rejects_edits_stale_plan_and_tampered_pack(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "repair-adversarial-pack")
        target = source_root.parent / "repair-adversarial-consumer"
        aide_lite.apply_import_pack(pack, target)
        rel = ".aide/prompts/compact-task.md"
        managed = target / rel
        managed.unlink()
        preview = aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)
        self.assertEqual(aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest="0" * 64)["status"], "STALE_PLAN")
        self.assertFalse(managed.exists())
        managed.write_bytes(b"project edit\n")
        self.assertEqual(aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])["status"], "CONFLICT")
        self.assertEqual(managed.read_bytes(), b"project edit\n")
        managed.unlink()
        with self.assertRaises(ValueError):
            aide_lite.apply_portable_owned_repair(pack, target, "../escape", dry_run=True)
        (pack / "files" / rel).write_bytes(b"tampered\n")
        with self.assertRaisesRegex(ValueError, "invalid pack checksums"):
            aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])

    def test_owned_repair_interruption_blocks_import_and_recovers_exact_postimage(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "repair-interruption-pack")
        target = source_root.parent / "repair-interruption-consumer"
        aide_lite.apply_import_pack(pack, target)
        rel = ".aide/prompts/compact-task.md"
        managed = target / rel
        managed.unlink()
        preview = aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)
        interrupted = aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"], fail_after_write=True)
        self.assertEqual(interrupted["status"], "INTERRUPTED")
        intent = target / aide_lite.PORTABLE_REPAIR_INTENT_PATH
        before = intent.read_bytes()
        self.assertEqual(aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)["status"], "RECOVERY_REQUIRED")
        self.assertEqual(intent.read_bytes(), before)
        with self.assertRaisesRegex(ValueError, "repair recovery"):
            aide_lite.apply_import_pack(pack, target)
        self.assertEqual(aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])["status"], "RECOVERED")
        self.assertFalse(intent.exists())

    def test_owned_repair_rejects_wrong_pack_receipt_and_unknown_interruption(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "repair-receipt-pack")
        target = source_root.parent / "repair-receipt-consumer"
        aide_lite.apply_import_pack(pack, target)
        rel = ".aide/prompts/compact-task.md"
        managed = target / rel
        managed.unlink()
        other_pack = source_root.parent / "repair-other-pack"
        shutil.copytree(pack, other_pack)
        aide_lite.write_text(other_pack / "README.md", aide_lite.read_text(other_pack / "README.md") + "different\n")
        checksums = json.loads(aide_lite.read_text(other_pack / "checksums.json"))
        checksums["checksums"]["README.md"] = aide_lite.sha256_file(other_pack / "README.md")
        aide_lite.write_text(other_pack / "checksums.json", json.dumps(checksums, sort_keys=True) + "\n")
        with self.assertRaisesRegex(ValueError, "exact pack"):
            aide_lite.apply_portable_owned_repair(other_pack, target, rel, dry_run=True)
        receipt_path = target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH
        saved_receipt = receipt_path.read_bytes()
        receipt = json.loads(saved_receipt)
        receipt["managed"][rel]["ownership"] = "unknown"
        aide_lite.write_text(receipt_path, json.dumps(receipt) + "\n")
        with self.assertRaisesRegex(ValueError, "receipt digest"):
            aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)
        receipt_path.write_bytes(saved_receipt)
        preview = aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)
        aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"], fail_after_write=True)
        managed.write_bytes(b"unexpected project edit\n")
        self.assertEqual(aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])["status"], "CONFLICT")
        self.assertEqual(managed.read_bytes(), b"unexpected project edit\n")
        self.assertTrue((target / aide_lite.PORTABLE_REPAIR_INTENT_PATH).exists())

    def test_owned_repair_atomic_creation_preserves_competing_file(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "repair-race-pack")
        target = source_root.parent / "repair-race-consumer"
        aide_lite.apply_import_pack(pack, target)
        rel = ".aide/prompts/compact-task.md"
        managed = target / rel
        managed.unlink()
        preview = aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)
        real_link = aide_lite.windows_link_from_handle

        def competing_creation(descriptor: int, directory_handle: int, leaf_name: str) -> None:
            managed.write_bytes(b"competing project bytes\n")
            real_link(descriptor, directory_handle, leaf_name)

        with mock.patch.object(aide_lite, "windows_link_from_handle", side_effect=competing_creation):
            result = aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])
        self.assertEqual(result["status"], "CONFLICT")
        self.assertEqual(managed.read_bytes(), b"competing project bytes\n")
        self.assertTrue((target / aide_lite.PORTABLE_REPAIR_INTENT_PATH).exists())
        self.assertEqual(aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])["status"], "CONFLICT")
        self.assertEqual(managed.read_bytes(), b"competing project bytes\n")

    @unittest.skipUnless(sys.platform == "win32", "requires Windows file sharing")
    def test_owned_repair_stage_denies_second_process_writer(self) -> None:
        for rel in (".aide/install/aide-lite-pack-v0.repair-intent.json", ".aide/prompts/compact-task.md"):
            with self.subTest(path=rel), tempfile.TemporaryDirectory() as raw:
                target = Path(raw) / rel
                target.parent.mkdir(parents=True)
                original_link = aide_lite.windows_link_from_handle
                attempted = []

                def rival_before_link(descriptor: int, directory_handle: int, leaf_name: str) -> None:
                    stages = list(target.parent.glob(f".{target.name}.*.tmp"))
                    self.assertEqual(len(stages), 1)
                    child = subprocess.run(
                        [
                            sys.executable, "-I", "-B", "-c",
                            "import sys\ntry:\n with open(sys.argv[1], 'r+b') as handle: handle.write(b'ATTACKED bytes')\nexcept PermissionError:\n sys.exit(23)\n",
                            str(stages[0]),
                        ],
                        capture_output=True, text=True, timeout=10,
                    )
                    attempted.append(child.returncode)
                    self.assertEqual(child.returncode, 23, child.stderr)
                    original_link(descriptor, directory_handle, leaf_name)

                with mock.patch.object(aide_lite, "windows_link_from_handle", side_effect=rival_before_link):
                    aide_lite.atomic_create_bytes_no_clobber(target, b"expected bytes")
                self.assertEqual(attempted, [23])
                self.assertEqual(target.read_bytes(), b"expected bytes")
                self.assertEqual(list(target.parent.iterdir()), [target])

    @unittest.skipUnless(sys.platform == "win32", "requires Windows file sharing")
    def test_owned_repair_stage_setup_failure_cleans_owned_link(self) -> None:
        for stage in ("descriptor", "file-object"):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as raw:
                target = Path(raw) / "victim.bin"
                if stage == "descriptor":
                    context = mock.patch("msvcrt.open_osfhandle", side_effect=OSError("descriptor setup failed"))
                else:
                    context = mock.patch.object(aide_lite.os, "fdopen", side_effect=OSError("file-object setup failed"))
                with context, self.assertRaisesRegex(OSError, "setup failed"):
                    aide_lite.atomic_create_bytes_no_clobber(target, b"expected bytes")
                self.assertFalse(target.exists())
                self.assertEqual(list(target.parent.iterdir()), [])

    def test_owned_repair_prepublication_failure_retries_from_missing(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "repair-prepublish-pack")
        target = source_root.parent / "repair-prepublish-consumer"
        aide_lite.apply_import_pack(pack, target)
        rel = ".aide/prompts/compact-task.md"
        managed = target / rel
        managed.unlink()
        preview = aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)
        real_link = aide_lite.windows_link_from_handle

        def fail_payload(descriptor: int, directory_handle: int, leaf_name: str) -> None:
            if leaf_name == managed.name:
                raise OSError("simulated prepublication failure")
            real_link(descriptor, directory_handle, leaf_name)

        with mock.patch.object(aide_lite, "windows_link_from_handle", side_effect=fail_payload):
            with self.assertRaisesRegex(OSError, "prepublication"):
                aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])
        self.assertFalse(managed.exists())
        intent = target / aide_lite.PORTABLE_REPAIR_INTENT_PATH
        self.assertTrue(intent.exists())
        self.assertEqual(aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)["status"], "RECOVERY_REQUIRED")
        self.assertEqual(aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])["status"], "APPLIED")
        self.assertFalse(intent.exists())

    def test_owned_repair_serializes_concurrent_repair_and_import(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "repair-concurrent-pack")
        target = source_root.parent / "repair-concurrent-consumer"
        aide_lite.apply_import_pack(pack, target)
        rel = ".aide/prompts/compact-task.md"
        (target / rel).unlink()
        preview = aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)
        real_link = aide_lite.windows_link_from_handle
        blocked = []

        def overlapping_publish(descriptor: int, directory_handle: int, leaf_name: str) -> None:
            if leaf_name != (target / rel).name:
                real_link(descriptor, directory_handle, leaf_name)
                return
            for operation in (
                lambda: aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"]),
                lambda: aide_lite.apply_import_pack(pack, target),
            ):
                with self.assertRaisesRegex(ValueError, "already in progress"):
                    operation()
                blocked.append(True)
            real_link(descriptor, directory_handle, leaf_name)

        with mock.patch.object(aide_lite, "windows_link_from_handle", side_effect=overlapping_publish):
            result = aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])
        self.assertEqual(result["status"], "APPLIED")
        self.assertEqual(blocked, [True, True])
        self.assertFalse((target / aide_lite.PORTABLE_REPAIR_INTENT_PATH).exists())

    def test_owned_repair_blocks_parent_substitution_at_publish(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "repair-junction-pack")
        target = source_root.parent / "repair-junction-consumer"
        aide_lite.apply_import_pack(pack, target)
        rel = ".aide/prompts/compact-task.md"
        managed = target / rel
        managed.unlink()
        preview = aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)
        parent = managed.parent
        moved = parent.with_name("prompts-moved")
        outside = source_root.parent / "outside-junction-target"
        outside.mkdir()
        sentinel = outside / "sentinel.txt"
        sentinel.write_bytes(b"outside unchanged\n")
        real_link = aide_lite.windows_link_from_handle
        blocked = []

        def attempt_swap(descriptor: int, directory_handle: int, leaf_name: str) -> None:
            if leaf_name == managed.name:
                with self.assertRaises(OSError):
                    parent.rename(moved)
                blocked.append(True)
            real_link(descriptor, directory_handle, leaf_name)

        with mock.patch.object(aide_lite, "windows_link_from_handle", side_effect=attempt_swap):
            result = aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])
        self.assertEqual(result["status"], "APPLIED")
        self.assertEqual(blocked, [True])
        self.assertFalse(moved.exists())
        self.assertEqual(sentinel.read_bytes(), b"outside unchanged\n")
        self.assertFalse((outside / managed.name).exists())

    def test_fresh_import_serializes_second_import_and_repair_without_lock_file(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "fresh-import-overlap-pack")
        target = source_root.parent / "fresh-import-overlap-consumer"
        self.assertEqual(aide_lite.apply_import_pack(pack, target, dry_run=True)["status"], "PLANNED")
        self.assertFalse(target.exists())
        real_operation = aide_lite.apply_import_operation
        checked = []

        def overlap(pack_root: Path, target_root: Path, operation: dict[str, str]) -> bool:
            if not checked:
                with self.assertRaisesRegex(ValueError, "already in progress"):
                    aide_lite.apply_import_pack(pack, target)
                with self.assertRaisesRegex(ValueError, "already in progress"):
                    aide_lite.apply_portable_owned_repair(pack, target, ".aide/prompts/compact-task.md")
                cli = pack / "files/.aide/scripts/aide_lite.py"
                other = subprocess.run([sys.executable, "-I", "-B", str(cli), "--repo-root", str(target), "import-pack", "--pack", str(pack), "--target", str(target)], text=True, capture_output=True, timeout=30)
                self.assertNotEqual(other.returncode, 0)
                self.assertIn("already in progress", other.stderr)
                self.assertFalse((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).exists())
                checked.append(True)
            return real_operation(pack_root, target_root, operation)

        with mock.patch.object(aide_lite, "apply_import_operation", side_effect=overlap):
            first = aide_lite.apply_import_pack(pack, target)
        self.assertEqual(first["status"], "APPLIED")
        self.assertEqual(checked, [True])
        self.assertTrue((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).exists())
        self.assertFalse((target / aide_lite.PORTABLE_IMPORT_INTENT_PATH).exists())
        self.assertFalse((target / aide_lite.PORTABLE_LIFECYCLE_LOCK_PATH).exists())
        self.assertEqual(aide_lite.apply_import_pack(pack, target)["status"], "NO_CHANGES")

    def test_owned_repair_cleanup_rejects_junction_swap_on_success_and_recovery(self) -> None:
        source_root = self.make_source_repo()
        pack = self.freeze_pack(source_root, "repair-cleanup-junction-pack")
        rel = ".aide/prompts/compact-task.md"
        for scenario in ("success", "recovery"):
            with self.subTest(scenario=scenario):
                target = source_root.parent / f"repair-cleanup-{scenario}-consumer"
                aide_lite.apply_import_pack(pack, target)
                managed = target / rel
                managed.unlink()
                preview = aide_lite.apply_portable_owned_repair(pack, target, rel, dry_run=True)
                if scenario == "recovery":
                    interrupted = aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"], fail_after_write=True)
                    self.assertEqual(interrupted["status"], "INTERRUPTED")
                install = (target / aide_lite.PORTABLE_REPAIR_INTENT_PATH).parent
                moved = install.with_name("install-before-junction-swap")
                outside = source_root.parent / f"repair-cleanup-{scenario}-outside"
                outside.mkdir()
                outside_same_name = outside / Path(aide_lite.PORTABLE_REPAIR_INTENT_PATH).name
                outside_same_name.write_bytes(b"outside project-owned intent name\n")
                observed_intent = []
                real_cleanup = aide_lite.delete_portable_repair_intent_anchored

                def swap_at_cleanup(root: Path, intent: dict[str, object]) -> None:
                    observed_intent.append((install / Path(aide_lite.PORTABLE_REPAIR_INTENT_PATH).name).read_bytes())
                    install.rename(moved)
                    junction = subprocess.run(["cmd", "/c", "mklink", "/J", str(install), str(outside)], text=True, capture_output=True, timeout=10)
                    self.assertEqual(junction.returncode, 0, junction.stderr)
                    self.assertTrue(install.is_junction())
                    real_cleanup(root, intent)

                try:
                    with mock.patch.object(aide_lite, "delete_portable_repair_intent_anchored", side_effect=swap_at_cleanup):
                        with self.assertRaisesRegex(ValueError, "reparse point"):
                            aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])
                    self.assertEqual(outside_same_name.read_bytes(), b"outside project-owned intent name\n")
                    self.assertEqual(len(observed_intent), 1)
                finally:
                    if install.is_junction():
                        install.rmdir()
                    if moved.exists():
                        moved.rename(install)
                intent_path = target / aide_lite.PORTABLE_REPAIR_INTENT_PATH
                self.assertEqual(intent_path.read_bytes(), observed_intent[0])
                if scenario == "success":
                    original_intent = observed_intent[0]
                    intent_record = json.loads(original_intent)
                    altered = bytearray(original_intent)
                    altered[0] ^= 1
                    intent_path.write_bytes(altered)
                    with self.assertRaisesRegex(ValueError, "bytes changed"):
                        aide_lite.delete_portable_repair_intent_anchored(target, intent_record)
                    self.assertEqual(intent_path.read_bytes(), altered)
                    intent_path.write_bytes(original_intent)
                    second_link = intent_path.with_name("intent-second-link")
                    aide_lite.os.link(intent_path, second_link)
                    try:
                        with self.assertRaisesRegex(ValueError, "single-link"):
                            aide_lite.delete_portable_repair_intent_anchored(target, intent_record)
                    finally:
                        second_link.unlink()
                    self.assertEqual(intent_path.read_bytes(), original_intent)
                self.assertEqual(aide_lite.apply_portable_owned_repair(pack, target, rel, expected_plan_digest=preview["plan_digest"])["status"], "RECOVERED")
                self.assertFalse(intent_path.exists())


if __name__ == "__main__":
    unittest.main()
