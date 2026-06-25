from __future__ import annotations

import copy
import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.protocol import distribution_manifest

MODULE_PATH = REPO_ROOT / ".aide/scripts/aide_lite.py"
SPEC = importlib.util.spec_from_file_location("aide_lite_distribution_manifest", MODULE_PATH)
aide_lite = importlib.util.module_from_spec(SPEC)
sys.modules["aide_lite_distribution_manifest"] = aide_lite
assert SPEC.loader is not None
SPEC.loader.exec_module(aide_lite)


def copy_file(root: Path, rel: str) -> None:
    source = REPO_ROOT / rel
    target = root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())


def copy_tree(root: Path, rel: str) -> None:
    source_root = REPO_ROOT / rel
    for source in source_root.rglob("*"):
        if source.is_file():
            target = root / rel / source.relative_to(source_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())


def copy_distribution_inputs(root: Path) -> None:
    for rel in [
        ".aide/scripts/aide_lite.py",
        ".aide/protocol/aide-distribution-manifest-v1.schema.json",
        "core/protocol/__init__.py",
        "core/protocol/envelope.py",
        "core/protocol/distribution_manifest.py",
        ".aide/release/latest-release-bundle.json",
    ]:
        copy_file(root, rel)
    copy_tree(root, ".aide/release/dist")
    copy_tree(root, ".aide/export/aide-lite-pack-v0")


class AIDEDistributionManifestV1Tests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        copy_distribution_inputs(root)
        return root

    def test_schema_file_exists_and_parses(self) -> None:
        schema = distribution_manifest.load_schema(REPO_ROOT)
        self.assertEqual(schema["title"], "AIDE DistributionManifest v1")
        self.assertEqual(schema["properties"]["kind"]["const"], "DistributionManifest")
        self.assertIn("metadata", schema["required"])
        self.assertIn("spec", schema["required"])
        self.assertIn("status", schema["required"])

    def test_build_manifest_maps_q47_without_absolute_paths(self) -> None:
        manifest = distribution_manifest.build_distribution_manifest(REPO_ROOT)
        self.assertEqual(manifest["kind"], "DistributionManifest")
        self.assertEqual(manifest["status"]["proposed_capability"], "distribution_manifest_v1")
        self.assertGreaterEqual(len(manifest["spec"]["artifacts"]), 3)
        self.assertFalse(distribution_manifest.contains_absolute_local_path(manifest))
        self.assertFalse(manifest["spec"]["source"]["q48_publication_draft_is_distribution_truth"])
        self.assertTrue(manifest["spec"]["provenance"]["source_repo_local_path_suppressed"])
        self.assertFalse(manifest["status"]["install_apply_implemented"])
        self.assertFalse(manifest["status"]["release_publication_implemented"])

    def test_validation_rejects_duplicate_component_and_artifact(self) -> None:
        manifest = distribution_manifest.minimal_fixture_manifest()
        duplicate_component = copy.deepcopy(manifest)
        distribution_manifest.duplicate_first_component(duplicate_component)
        duplicate_component = distribution_manifest.finalize_manifest(duplicate_component)
        result = distribution_manifest.validate_distribution_manifest_object(duplicate_component)
        self.assertIn("distribution.duplicate_component", result["refusal_codes"])
        duplicate_artifact = copy.deepcopy(manifest)
        distribution_manifest.duplicate_first_artifact(duplicate_artifact)
        duplicate_artifact = distribution_manifest.finalize_manifest(duplicate_artifact)
        result = distribution_manifest.validate_distribution_manifest_object(duplicate_artifact)
        self.assertIn("distribution.duplicate_artifact", result["refusal_codes"])

    def test_validation_rejects_feature_protocol_source_and_path_boundaries(self) -> None:
        cases = [
            ("distribution.unknown_required_feature", distribution_manifest.add_unknown_required_feature),
            ("distribution.unsupported_protocol_range", distribution_manifest.unsupported_protocol),
            ("distribution.unsupported_source_kind", distribution_manifest.unsupported_source_kind),
            ("distribution.forbidden_member", lambda m: distribution_manifest.set_artifact_path(m, ".aide.local/state.sqlite")),
            ("distribution.forbidden_member", lambda m: distribution_manifest.set_artifact_path(m, "C:/tmp/aide.zip")),
            ("distribution.forbidden_member", lambda m: distribution_manifest.set_artifact_path(m, "../outside.zip")),
        ]
        for expected, mutator in cases:
            with self.subTest(expected=expected):
                manifest = distribution_manifest.minimal_fixture_manifest()
                mutator(manifest)
                manifest = distribution_manifest.finalize_manifest(manifest)
                result = distribution_manifest.validate_distribution_manifest_object(manifest)
                self.assertIn(expected, result["refusal_codes"])

    def test_validation_rejects_digest_signature_sbom_and_migration_claims(self) -> None:
        cases = [
            ("distribution.artifact_digest_mismatch", distribution_manifest.wrong_artifact_digest, True),
            ("distribution.manifest_digest_mismatch", distribution_manifest.wrong_manifest_digest, False),
            ("distribution.signature_unverified", distribution_manifest.false_verified_signature, True),
            ("distribution.sbom_unavailable", distribution_manifest.sbom_generated_claim, True),
            ("distribution.incompatible_migration", distribution_manifest.add_incompatible_migration, True),
            ("distribution.missing_checksum", distribution_manifest.missing_checksum, True),
        ]
        for expected, mutator, should_finalize in cases:
            with self.subTest(expected=expected):
                manifest = distribution_manifest.minimal_fixture_manifest()
                mutator(manifest)
                if should_finalize:
                    manifest = distribution_manifest.finalize_manifest(manifest)
                result = distribution_manifest.validate_distribution_manifest_object(manifest)
                self.assertIn(expected, result["refusal_codes"])

    def test_reordered_input_keeps_distribution_digest(self) -> None:
        manifest = distribution_manifest.build_distribution_manifest(REPO_ROOT)
        reordered = distribution_manifest.reordered_manifest(manifest)
        self.assertEqual(manifest["status"]["distribution_digest"], reordered["status"]["distribution_digest"])

    def test_project_and_validate_write_reports_and_fixture_corpus(self) -> None:
        root = self.make_repo()
        project_report = distribution_manifest.project(root)
        self.assertEqual(project_report["status"], "PASS_WITH_WARNINGS")
        validation = distribution_manifest.validate(root)
        self.assertEqual(validation["validation_status"], "PASS_WITH_WARNINGS")
        self.assertTrue(validation["checks"]["fixture_matrix_passed"])
        for rel in [
            ".aide/reports/distribution-manifest-v1/manifest.json",
            ".aide/reports/distribution-manifest-v1/validation.json",
            ".aide/reports/distribution-manifest-v1/q47-source-mapping.json",
            ".aide/fixtures/distribution-manifest-v1/valid/minimal-unsigned.json",
            ".aide/fixtures/distribution-manifest-v1/invalid/unknown-required-feature.json",
        ]:
            self.assertTrue((root / rel).exists(), rel)

    def test_cli_status_project_validate_and_no_apply_subcommands(self) -> None:
        root = self.make_repo()
        parser = aide_lite.build_parser(REPO_ROOT)
        for command in [
            ["--repo-root", str(root), "distribution-manifest", "status"],
            ["--repo-root", str(root), "distribution-manifest", "project"],
            ["--repo-root", str(root), "distribution-manifest", "validate"],
        ]:
            parsed = parser.parse_args(command)
            output = io.StringIO()
            with redirect_stdout(output):
                result = parsed.handler(parsed)
            self.assertEqual(result, 0, output.getvalue())
            self.assertIn("proposed_capability: distribution_manifest_v1", output.getvalue())
            self.assertIn("install_apply_implemented: false", output.getvalue())
            self.assertIn("release_publication_implemented: false", output.getvalue())
            self.assertIn("target_repository_mutation_implemented: false", output.getvalue())
        for subcommand in ["apply", "publish", "install", "update", "rollback", "uninstall"]:
            with self.subTest(subcommand=subcommand):
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    parser.parse_args(["distribution-manifest", subcommand])


if __name__ == "__main__":
    unittest.main()
