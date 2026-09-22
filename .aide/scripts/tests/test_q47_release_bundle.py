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
        self.write(root, aide_lite.CHANGELOG_PREVIEW_MD_PATH, "# AIDE Changelog Preview\n\nrelease_publishing: false\n")
        self.write(root, aide_lite.RELEASE_NOTES_PREVIEW_MD_PATH, "# AIDE Release Notes Preview\n\nrelease_publishing: false\n")
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
                )
                self.assertEqual(apply.returncode, 0, apply.stdout + apply.stderr)
                self.assertTrue((target / ".aide/scripts/aide_lite.py").is_file())
                self.assertFalse((target / ".aide.local.example/secrets/README.md").exists())

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

    def test_checksum_mismatch_detection_fails(self) -> None:
        root = self.make_repo()
        aide_lite.build_release_bundle_outputs(root)
        self.write(root, aide_lite.RELEASE_INSTALL_NOTES_PATH, "# tampered\n")
        ok, problems = aide_lite.validate_release_checksums(root)
        self.assertFalse(ok)
        self.assertTrue(any("checksum mismatch" in problem for problem in problems))

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
