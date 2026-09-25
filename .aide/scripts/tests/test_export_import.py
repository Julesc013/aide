from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import importlib.util
import json
import shutil
from pathlib import Path


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
    def test_atomic_create_staged_bytes_refuse_rival_before_guard(self) -> None:
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
                        aide_lite.atomic_create_bytes_no_clobber(target, b"expected bytes")
                self.assertTrue(attempted)
                self.assertFalse(target.exists())

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

    def test_fake_secret_source_file_is_not_exported(self) -> None:
        source_root = self.make_source_repo()
        aide_lite.write_text(source_root / ".aide/prompts/compact-task.md", "api_key = \"abcdefghijklmnop\"\n")
        self.assertFalse(aide_lite.is_exportable_file(source_root, ".aide/prompts/compact-task.md"))
        pack_root = self.build_pack(source_root)
        self.assertFalse((pack_root / "files/.aide/prompts/compact-task.md").exists())


if __name__ == "__main__":
    unittest.main()
