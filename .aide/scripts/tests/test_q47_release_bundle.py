from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = REPO_ROOT / ".aide/scripts/aide_lite.py"
SPEC = importlib.util.spec_from_file_location("aide_lite_q47", MODULE_PATH)
aide_lite = importlib.util.module_from_spec(SPEC)
sys.modules["aide_lite_q47"] = aide_lite
assert SPEC.loader is not None
SPEC.loader.exec_module(aide_lite)


class Q47ReleaseBundleTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for rel in [*aide_lite.Q47_POLICY_FILES, *aide_lite.Q47_SCHEMA_FILES, aide_lite.RELEASE_README_PATH]:
            source = REPO_ROOT / rel
            self.write(root, rel, source.read_text(encoding="utf-8"))
        self.write(root, ".gitignore", ".aide.local/\n.aide.local/**\n.env\nsecrets/\n")
        self.write(root, aide_lite.CHANGELOG_PREVIEW_MD_PATH, "# AIDE Changelog Preview\n\nsource_head: fixture-commit\nrelease_publishing: false\n")
        self.write(root, aide_lite.RELEASE_NOTES_PREVIEW_MD_PATH, "# AIDE Release Notes Preview\n\nsource_head: fixture-commit\nrelease_publishing: false\n")
        self.write_pack(root)
        return root

    def write(self, root: Path, rel: str, text: str) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def write_pack(self, root: Path) -> None:
        pack_root = aide_lite.export_pack_root(root, aide_lite.EXPORT_PACK_ID)
        self.write(root, f"{aide_lite.EXPORT_PACK_PATH}/README.md", "# Pack\n")
        self.write(root, f"{aide_lite.EXPORT_PACK_PATH}/install.md", "# Install\n")
        self.write(root, f"{aide_lite.EXPORT_PACK_PATH}/import-policy.yaml", "schema_version: fixture.import.v0\n")
        self.write(root, f"{aide_lite.EXPORT_PACK_PATH}/export-report.md", "# Export Report\n")
        portable_script = root / aide_lite.EXPORT_PACK_FILES_ROOT / ".aide/scripts/aide_lite.py"
        portable_script.parent.mkdir(parents=True, exist_ok=True)
        portable_script.write_bytes(MODULE_PATH.read_bytes())
        self.write(root, f"{aide_lite.EXPORT_PACK_FILES_ROOT}/docs/reference/aide-lite.md", "# AIDE Lite\n")
        self.write(
            root,
            f"{aide_lite.EXPORT_PACK_FILES_ROOT}/.aide.local.example/secrets/README.md",
            "# Empty local secret directory placeholder\n",
        )
        included_files = [
            "files/.aide.local.example/secrets/README.md",
            "files/.aide/scripts/aide_lite.py",
            "files/docs/reference/aide-lite.md",
        ]
        self.write(
            root,
            f"{aide_lite.EXPORT_PACK_PATH}/manifest.yaml",
            aide_lite.render_manifest(included_files, "fixture-commit", True),
        )
        checksums = aide_lite.build_pack_checksums(pack_root)
        self.write(root, f"{aide_lite.EXPORT_PACK_PATH}/checksums.json", aide_lite.stable_json_text(checksums))

    def run_cmd(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(MODULE_PATH), "--repo-root", str(root), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def files_under_release(self, root: Path) -> dict[str, bytes]:
        release_root = root / ".aide/release"
        if not release_root.exists():
            return {}
        return {
            aide_lite.normalize_rel(path.relative_to(root)): path.read_bytes()
            for path in sorted(release_root.rglob("*"))
            if path.is_file()
        }

    def extract_archive(self, root: Path, archive_rel: str) -> Path:
        extracted = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, extracted, ignore_errors=True)
        shutil.unpack_archive(root / archive_rel, extracted)
        return extracted / aide_lite.RELEASE_ARCHIVE_ROOT

    def run_extracted_cli(self, pack_root: Path, target: Path, *args: str) -> subprocess.CompletedProcess[str]:
        script = pack_root / "files/.aide/scripts/aide_lite.py"
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        environment["PYTHONNOUSERSITE"] = "1"
        return subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                str(script),
                "--repo-root",
                str(target),
                *args,
            ],
            cwd=pack_root,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_release_policy_and_schema_validation(self) -> None:
        root = self.make_repo()
        checks = aide_lite.validate_release_files(root, require_outputs=False)
        self.assertEqual(aide_lite.result_from_checks(checks), "PASS")

    def test_release_bundle_fixture_generation_creates_required_artifacts(self) -> None:
        root = self.make_repo()
        bundle = aide_lite.build_release_bundle_outputs(root)
        self.assertEqual(bundle["validation"]["result"], "PASS")
        for rel in [
            aide_lite.RELEASE_ZIP_PATH,
            aide_lite.RELEASE_TAR_GZ_PATH,
            aide_lite.RELEASE_CHECKSUMS_JSON_PATH,
            aide_lite.RELEASE_SHA256SUMS_PATH,
            aide_lite.RELEASE_MANIFEST_PATH,
            aide_lite.RELEASE_INSTALL_NOTES_PATH,
            aide_lite.RELEASE_PROVENANCE_JSON_PATH,
            aide_lite.RELEASE_VALIDATION_JSON_PATH,
        ]:
            self.assertTrue((root / rel).exists(), rel)
            self.assertGreater((root / rel).stat().st_size, 0, rel)

    def test_archive_extraction_validation_and_forbidden_paths(self) -> None:
        root = self.make_repo()
        aide_lite.build_release_bundle_outputs(root)
        for rel in [aide_lite.RELEASE_ZIP_PATH, aide_lite.RELEASE_TAR_GZ_PATH]:
            fixture = aide_lite.validate_release_archive(root, rel)
            self.assertEqual(fixture["result"], "PASS", fixture)
            self.assertEqual(fixture["forbidden_paths"], [])
            names = aide_lite.archive_member_names(root / rel)
            self.assertIn("aide-lite-pack-v0/files/.aide/scripts/aide_lite.py", names)
            self.assertFalse(any(".aide.local" in name or name.endswith(".env") for name in names))

    def test_extracted_archives_import_without_source_checkout(self) -> None:
        root = self.make_repo()
        aide_lite.build_release_bundle_outputs(root)

        for archive_rel in [aide_lite.RELEASE_ZIP_PATH, aide_lite.RELEASE_TAR_GZ_PATH]:
            with self.subTest(archive=archive_rel):
                pack_root = self.extract_archive(root, archive_rel)
                target = Path(tempfile.mkdtemp())
                self.addCleanup(shutil.rmtree, target, ignore_errors=True)
                subprocess.run(
                    ["git", "init", "--quiet", str(target)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                )

                checksums = json.loads((pack_root / "checksums.json").read_text(encoding="utf-8"))
                manifest = (pack_root / "manifest.yaml").read_text(encoding="utf-8")
                forbidden = "files/.aide.local.example/secrets/README.md"
                self.assertNotIn(forbidden, checksums["checksums"])
                self.assertNotIn(forbidden, manifest)

                dry_run = self.run_extracted_cli(
                    pack_root,
                    target,
                    "import-pack",
                    "--pack",
                    str(pack_root),
                    "--target",
                    str(target),
                    "--dry-run",
                    "--mode",
                    "safe",
                )
                self.assertEqual(dry_run.returncode, 0, dry_run.stdout + dry_run.stderr)
                self.assertIn("dry_run: true", dry_run.stdout)
                plan_digest = next(
                    line.split(":", 1)[1].strip()
                    for line in dry_run.stdout.splitlines()
                    if line.startswith("plan_digest:")
                )

                apply = self.run_extracted_cli(
                    pack_root,
                    target,
                    "import-pack",
                    "--pack",
                    str(pack_root),
                    "--target",
                    str(target),
                    "--mode",
                    "safe",
                    "--expect-plan",
                    plan_digest,
                )
                self.assertEqual(apply.returncode, 0, apply.stdout + apply.stderr)
                self.assertIn("status: APPLIED", apply.stdout)
                self.assertTrue((target / ".aide/scripts/aide_lite.py").is_file())
                self.assertTrue((target / aide_lite.PORTABLE_IMPORT_RECEIPT_PATH).is_file())
                self.assertFalse((target / ".aide.local.example/secrets/README.md").exists())

                rerun = self.run_extracted_cli(
                    pack_root,
                    target,
                    "import-pack",
                    "--pack",
                    str(pack_root),
                    "--target",
                    str(target),
                    "--mode",
                    "safe",
                )
                self.assertEqual(rerun.returncode, 0, rerun.stdout + rerun.stderr)
                self.assertIn("status: NO_CHANGES", rerun.stdout)

    def test_release_archives_are_byte_deterministic(self) -> None:
        root = self.make_repo()
        aide_lite.build_release_bundle_outputs(root)
        first = {
            rel: (root / rel).read_bytes()
            for rel in [aide_lite.RELEASE_ZIP_PATH, aide_lite.RELEASE_TAR_GZ_PATH]
        }
        aide_lite.build_release_bundle_outputs(root)
        second = {rel: (root / rel).read_bytes() for rel in first}
        self.assertEqual(first, second)

    def test_release_records_clean_source_before_writing_bundle_outputs(self) -> None:
        root = self.make_repo()
        subprocess.run(["git", "init", "--quiet", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "AIDE Fixture"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "fixture@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "core.autocrlf", "false"], check=True)
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "--quiet", "-m", "fixture"], check=True)
        source_commit = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip()

        pack_root = aide_lite.export_pack_root(root, aide_lite.EXPORT_PACK_ID)
        included_files = aide_lite.pack_manifest_list(pack_root, "included_files")
        self.write(
            root,
            f"{aide_lite.EXPORT_PACK_PATH}/manifest.yaml",
            aide_lite.render_manifest(included_files, source_commit, False),
        )

        bundle = aide_lite.build_release_bundle_outputs(root)
        provenance = json.loads((root / aide_lite.RELEASE_PROVENANCE_JSON_PATH).read_text(encoding="utf-8"))
        self.assertEqual(provenance["source_commit"], source_commit)
        self.assertFalse(provenance["dirty_state"])
        self.assertEqual(bundle["source_commit"], source_commit)
        self.assertFalse(bundle["dirty_state"])

    def test_checksum_mismatch_detection_fails(self) -> None:
        root = self.make_repo()
        aide_lite.build_release_bundle_outputs(root)
        self.write(root, aide_lite.RELEASE_INSTALL_NOTES_PATH, "# tampered\n")
        ok, problems = aide_lite.validate_release_checksums(root)
        self.assertFalse(ok)
        self.assertTrue(any("checksum mismatch" in problem for problem in problems))

    def test_checksum_validation_rejects_stale_and_missing_entries(self) -> None:
        root = self.make_repo()
        aide_lite.build_release_bundle_outputs(root)
        checksums_path = root / aide_lite.RELEASE_CHECKSUMS_JSON_PATH
        checksums = json.loads(checksums_path.read_text(encoding="utf-8"))
        checksums["checksums"]["stale.bin"] = "0" * 64
        checksums["checksums"].pop("manifest.yaml")
        checksums_path.write_text(aide_lite.stable_json_text(checksums), encoding="utf-8")
        ok, problems = aide_lite.validate_release_checksums(root)
        self.assertFalse(ok)
        self.assertTrue(any("stale artifact" in problem for problem in problems))
        self.assertTrue(any("missing artifact" in problem for problem in problems))

    def test_release_asset_index_binds_exact_hashes_and_sizes(self) -> None:
        root = self.make_repo()
        aide_lite.build_release_bundle_outputs(root)
        index_path = root / aide_lite.RELEASE_ASSETS_JSON_PATH
        index = json.loads(index_path.read_text(encoding="utf-8"))
        for artifact in index["artifacts"]:
            path = root / artifact["path"]
            self.assertEqual(artifact["sha256"], aide_lite.sha256_file(path))
            self.assertEqual(artifact["size_bytes"], path.stat().st_size)
        index["artifacts"][0]["sha256"] = "0" * 64
        index["artifacts"][1]["size_bytes"] += 1
        index_path.write_text(aide_lite.stable_json_text(index), encoding="utf-8")
        ok, problems = aide_lite.validate_release_asset_index(root)
        self.assertFalse(ok)
        self.assertTrue(any("checksum mismatch" in problem for problem in problems))
        self.assertTrue(any("size mismatch" in problem for problem in problems))

    def test_release_metadata_is_checkout_path_independent(self) -> None:
        first = self.make_repo()
        second = self.make_repo()
        first_bundle = aide_lite.build_release_bundle_outputs(first)
        second_bundle = aide_lite.build_release_bundle_outputs(second)
        self.assertEqual(first_bundle["source_repo"], "julesc013/aide")
        self.assertEqual(first_bundle["source_branch"], "not-recorded-in-pack")
        self.assertEqual(first_bundle, second_bundle)
        first_provenance = (first / aide_lite.RELEASE_PROVENANCE_JSON_PATH).read_bytes()
        second_provenance = (second / aide_lite.RELEASE_PROVENANCE_JSON_PATH).read_bytes()
        self.assertEqual(first_provenance, second_provenance)
        self.assertNotIn(str(first).encode(), first_provenance)
        self.assertNotIn(str(second).encode(), second_provenance)

    def test_stale_preview_is_blocked_in_release_bundle(self) -> None:
        root = self.make_repo()
        self.write(root, aide_lite.CHANGELOG_PREVIEW_MD_PATH, "# AIDE Changelog Preview\n\nsource_head: stale-commit\n")
        bundle = aide_lite.build_release_bundle_outputs(root)
        copied = (root / aide_lite.RELEASE_CHANGELOG_PREVIEW_PATH).read_text(encoding="utf-8")
        self.assertIn("status: blocked_stale_source_preview", copied)
        self.assertIn("publish_candidate: false", copied)
        self.assertEqual(bundle["validation"]["result"], "FAIL")

    def test_release_validate_rejects_missing_required_file(self) -> None:
        root = self.make_repo()
        aide_lite.build_release_bundle_outputs(root)
        (root / aide_lite.RELEASE_MANIFEST_PATH).unlink()
        checks = aide_lite.validate_release_files(root, require_outputs=True)
        self.assertEqual(aide_lite.result_from_checks(checks), "FAIL")

    def test_release_clean_dry_run_deletes_nothing(self) -> None:
        root = self.make_repo()
        aide_lite.build_release_bundle_outputs(root)
        before = self.files_under_release(root)
        result = self.run_cmd(root, "release", "clean", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("deleted: 0", result.stdout)
        self.assertEqual(before, self.files_under_release(root))

    def test_release_commands_are_local_only_and_no_publish(self) -> None:
        root = self.make_repo()
        result = self.run_cmd(root, "release", "bundle")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("no_publish: true", result.stdout)
        for args in [
            ("release", "validate"),
            ("release", "status"),
            ("release", "assets"),
            ("release", "manifest"),
            ("release", "checksums"),
            ("release", "provenance"),
        ]:
            result = self.run_cmd(root, *args)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("no_publish: true", result.stdout)


if __name__ == "__main__":
    unittest.main()
