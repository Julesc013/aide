from __future__ import annotations

import copy
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.protocol import distribution_manifest, ownership_ledger, project_lock

MODULE_PATH = REPO_ROOT / ".aide/scripts/aide_lite.py"
SPEC = importlib.util.spec_from_file_location("aide_lite_ownership_ledger", MODULE_PATH)
aide_lite = importlib.util.module_from_spec(SPEC)
sys.modules["aide_lite_ownership_ledger"] = aide_lite
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


def copy_inputs(root: Path) -> None:
    for rel in [
        ".aide/scripts/aide_lite.py",
        ".aide/protocol/aide-distribution-manifest-v1.schema.json",
        ".aide/protocol/aide-project-lock-v0.schema.json",
        ".aide/protocol/aide-ownership-ledger-v1.schema.json",
        "core/protocol/__init__.py",
        "core/protocol/envelope.py",
        "core/protocol/distribution_manifest.py",
        "core/protocol/project_lock.py",
        "core/protocol/ownership_ledger.py",
        ".aide/release/latest-release-bundle.json",
        ".aide/reports/distribution-manifest-v1-accept/acceptance-report.json",
        ".aide/reports/project-lock-v0-accept/acceptance-report.json",
    ]:
        copy_file(root, rel)
    copy_tree(root, ".aide/release/dist")
    copy_tree(root, ".aide/export/aide-lite-pack-v0")


class AIDEOwnershipLedgerV1Tests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        copy_inputs(root)
        distribution_manifest.project(root)
        project_lock.project(root)
        return root

    def test_schema_file_exists_and_parses(self) -> None:
        schema = ownership_ledger.load_schema(REPO_ROOT)
        self.assertEqual(schema["title"], "AIDE OwnershipLedger v1")
        self.assertEqual(schema["properties"]["kind"]["const"], "OwnershipLedger")
        self.assertIn("metadata", schema["required"])
        self.assertIn("spec", schema["required"])
        self.assertIn("status", schema["required"])
        self.assertIn("extensions", schema["required"])

    def test_build_binds_accepted_project_lock(self) -> None:
        root = self.make_repo()
        lock = ownership_ledger.load_project_lock(root)
        ledger = ownership_ledger.build_ownership_ledger(root)
        self.assertEqual(ledger["kind"], "OwnershipLedger")
        self.assertEqual(ledger["metadata"]["project_lock_digest"], lock["status"]["project_lock_digest"])
        self.assertTrue(ownership_ledger.project_lock_is_accepted(root, lock))
        self.assertFalse(ledger["status"]["install_apply_implemented"])
        self.assertFalse(ledger["status"]["admission_implemented"])
        self.assertFalse(ledger["status"]["authorization_implemented"])
        self.assertFalse(ledger["status"]["target_repository_mutation_implemented"])

    def test_taxonomy_contains_exact_required_classes(self) -> None:
        ledger = ownership_ledger.minimal_fixture_ledger()
        classes = {entry["class_id"] for entry in ledger["spec"]["taxonomy"]}
        self.assertEqual(classes, set(ownership_ledger.OWNERSHIP_CLASSES))
        record_classes = {entry["ownership_class"] for entry in ledger["spec"]["records"]}
        self.assertTrue(set(ownership_ledger.OWNERSHIP_CLASSES).issubset(record_classes))

    def test_validation_rejects_material_ownership_defects(self) -> None:
        lock = project_lock.minimal_fixture_lock()
        cases = [
            ("ownership_ledger.project_lock_digest_mismatch", lambda d: d["metadata"].__setitem__("project_lock_digest", "sha256:" + "0" * 64)),
            ("ownership_ledger.missing_taxonomy_class", lambda d: d["spec"].__setitem__("taxonomy", d["spec"]["taxonomy"][:-1])),
            ("ownership_ledger.unknown_taxonomy_class", lambda d: d["spec"]["taxonomy"].append({"class_id": "mystery", "authority": "target_project", "automatic_apply_allowed": False, "overwrite_allowed": False, "delete_allowed": False, "blocks_automatic_apply": True, "description": "invalid", "extensions": {}})),
            ("ownership_ledger.duplicate_record", lambda d: d["spec"]["records"].append(copy.deepcopy(d["spec"]["records"][0]))),
            ("ownership_ledger.record_class_unknown", lambda d: d["spec"]["records"][0].__setitem__("ownership_class", "mystery")),
            ("ownership_ledger.vendor_digest_missing", lambda d: d["spec"]["records"][0].__setitem__("content_digest", None)),
            ("ownership_ledger.managed_section_identity_missing", lambda d: d["spec"]["records"][2].__setitem__("managed_section_identity", None)),
            ("ownership_ledger.automatic_apply_forbidden", lambda d: next(r for r in d["spec"]["records"] if r["ownership_class"] == "unknown").__setitem__("apply_allowed", True)),
            ("ownership_ledger.absolute_path_forbidden", lambda d: d["spec"]["records"][0].__setitem__("target_path", "C:/outside/file.txt")),
            ("ownership_ledger.path_traversal_forbidden", lambda d: d["spec"]["records"][0].__setitem__("target_path", "../outside/file.txt")),
            ("ownership_ledger.source_state_contamination", lambda d: d["spec"]["records"][0].__setitem__("target_path", ".aide/context/latest-task-packet.md")),
            ("ownership_ledger.unknown_required_feature", lambda d: d["spec"]["required_features"].append("future.required.ownership")),
            ("ownership_ledger.extension_required_unknown", lambda d: d["spec"]["extensions"].__setitem__("requires.future", {"enabled": True})),
        ]
        for expected, mutator in cases:
            with self.subTest(expected=expected):
                ledger = ownership_ledger.minimal_fixture_ledger()
                mutator(ledger)
                ledger = ownership_ledger.finalize_ownership_ledger(ledger)
                result = ownership_ledger.validate_ownership_ledger_object(ledger, lock=lock, require_project_lock_acceptance=False)
                self.assertIn(expected, result["refusal_codes"])

    def test_unknown_optional_features_and_extensions_are_preserved(self) -> None:
        ledger = ownership_ledger.minimal_fixture_ledger()
        ledger["spec"]["optional_features"].append("future.optional.ownership")
        ledger["extensions"] = {"future.optional": {"preserve": True}}
        ledger = ownership_ledger.finalize_ownership_ledger(ledger)
        result = ownership_ledger.validate_ownership_ledger_object(
            ledger,
            lock=project_lock.minimal_fixture_lock(),
            require_project_lock_acceptance=False,
        )
        self.assertTrue(result["valid"], result)
        self.assertIn("unknown optional feature tolerated: future.optional.ownership", result["warnings"])
        self.assertEqual(ledger["extensions"]["future.optional"]["preserve"], True)

    def test_fixture_corpus_contains_required_cases_and_validate_passes(self) -> None:
        root = self.make_repo()
        ownership_ledger.write_fixture_corpus(root)
        required_valid = {"minimal-valid-ledger", "extension-round-trip", "reordered-records-valid"}
        required_invalid = set(ownership_ledger.EXPECTED_INVALID_REFUSALS)
        valid_names = {path.stem for path in (root / ownership_ledger.FIXTURE_ROOT / "valid").glob("*.json")}
        invalid_names = {path.stem for path in (root / ownership_ledger.FIXTURE_ROOT / "invalid").glob("*.json")}
        self.assertTrue(required_valid.issubset(valid_names), required_valid - valid_names)
        self.assertTrue(required_invalid.issubset(invalid_names), required_invalid - invalid_names)
        validation = ownership_ledger.validate(root)
        self.assertEqual(validation["validation_status"], "PASS_WITH_WARNINGS", validation["errors"])
        self.assertTrue(validation["checks"]["fixture_matrix_passed"])

    def test_project_and_cli_status_project_validate(self) -> None:
        root = self.make_repo()
        report = ownership_ledger.project(root)
        self.assertEqual(report["status"], "PASS_WITH_WARNINGS")
        self.assertTrue((root / ".aide/reports/ownership-ledger-v1/ownership-ledger.json").exists())
        parser = aide_lite.build_parser(REPO_ROOT)
        for command in [
            ["--repo-root", str(root), "ownership-ledger", "status"],
            ["--repo-root", str(root), "ownership-ledger", "project"],
            ["--repo-root", str(root), "ownership-ledger", "validate"],
        ]:
            parsed = parser.parse_args(command)
            output = io.StringIO()
            with redirect_stdout(output):
                result = parsed.handler(parsed)
            self.assertEqual(result, 0, output.getvalue())
            self.assertIn("proposed_capability: ownership_ledger_v1", output.getvalue())
            self.assertIn("install_apply_implemented: false", output.getvalue())
            self.assertIn("admission_implemented: false", output.getvalue())
            self.assertIn("authorization_implemented: false", output.getvalue())
            self.assertIn("target_repository_mutation_implemented: false", output.getvalue())

    def test_cli_rejects_apply_or_runtime_subcommands(self) -> None:
        parser = aide_lite.build_parser(REPO_ROOT)
        for subcommand in ["apply", "install", "update", "admit", "authorize", "mutate", "publish"]:
            with self.subTest(subcommand=subcommand):
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    parser.parse_args(["ownership-ledger", subcommand])


if __name__ == "__main__":
    unittest.main()
