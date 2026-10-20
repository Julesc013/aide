"""Run unchanged lifecycle behavior oracles through each implemented binding.

The original Windows-specific fixtures remain intact. This suite explicitly
reuses only their platform-neutral behavior checks, with smaller valid packs;
the delivered evaluator separately exercises the complete development pack.
"""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("aide_portable_lifecycle_oracles",
    ROOT / ".aide/scripts/tests/test_export_import.py")
original = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = original
spec.loader.exec_module(original)


class PortableLifecycleBindingTests(unittest.TestCase):
    copy_file = original.ExportImportTests.copy_file
    build_pack = original.ExportImportTests.build_pack
    freeze_pack = original.ExportImportTests.freeze_pack

    def make_source_repo(self, **_):
        source = original.ExportImportTests.make_source_repo(self, minimal_recovery=True)
        for relative in (".aide/scripts/posix_filesystem.py", ".aide.local.example/secrets/README.md"):
            self.copy_file(ROOT / relative, source / relative)
        return source

    def test_source_checkout_lifecycle_fixture_is_not_exported(self):
        source = self.make_source_repo()
        relative = ".aide/scripts/tests/test_posix_lifecycle.py"
        self.copy_file(Path(__file__), source / relative)
        pack = self.freeze_pack(source, "source-fixture-boundary")
        self.assertFalse((pack / "files" / relative).exists())
        self.assertTrue((pack / "files/.aide/scripts/posix_filesystem.py").is_file())

    @unittest.skipUnless(os.name == "posix", "POSIX rename-gap process termination")
    def test_process_exit_retains_unresolved_import_backup_and_original_bytes(self):
        module = original.aide_lite
        source = self.make_source_repo()
        old = self.freeze_pack(source, "crash-old")
        target = source.parent / "crash-target"
        self.assertEqual(module.apply_import_pack(old, target)["status"], "APPLIED")
        relative = ".aide/prompts/compact-task.md"
        before = (target / relative).read_bytes()
        (source / relative).write_bytes(b"# Incoming changed prompt\n")
        new = self.freeze_pack(source, "crash-new")
        script = """
import importlib.util, os, pathlib, sys
path = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('crash_delivered_lite', path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
binding = module.posix_filesystem_binding()
publish = binding._publish
def terminate(directory, stage, descriptor, destination, digest):
    if destination == 'compact-task.md':
        os._exit(87)
    return publish(directory, stage, descriptor, destination, digest)
binding._publish = terminate
module.apply_import_pack(pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), predecessor_pack=pathlib.Path(sys.argv[4]))
"""
        result = subprocess.run([sys.executable, "-I", "-B", "-c", script,
            str(new / "files/.aide/scripts/aide_lite.py"), str(new), str(target), str(old)],
            stdin=subprocess.DEVNULL, capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 87, result.stderr)
        self.assertFalse((target / relative).exists())
        intent = module.load_portable_import_intent(target)
        operation = next(item for item in intent["operations"] if item["target"] == relative)
        self.assertEqual((target / operation["backup_rel"]).read_bytes(), before)
        recovery = module.classify_portable_import_recovery(target, intent)
        self.assertEqual(recovery["classification"], "unknown")
        self.assertIn(operation["backup_rel"], recovery["outstanding_backups"])
        snapshot = {p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob("*") if p.is_file()}
        refused = module.apply_import_pack(new, target, predecessor_pack=old,
            expected_plan_digest=intent["plan_digest"], recover_partial=True)
        self.assertEqual(refused["status"], "RECOVERY_REQUIRED")
        self.assertEqual({p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob("*") if p.is_file()}, snapshot)

    @unittest.skipUnless(os.name == "posix", "POSIX installed helper dependency")
    def test_missing_installed_binding_refuses_before_removal_effect(self):
        module = original.aide_lite
        source = self.make_source_repo()
        pack = self.freeze_pack(source, "missing-binding-pack")
        target = source.parent / "missing-binding-target"
        self.assertEqual(module.apply_import_pack(pack, target)["status"], "APPLIED")
        (target / ".aide/scripts/posix_filesystem.py").unlink()
        plan = module.build_portable_removal_plan(target)
        before = {p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob("*") if p.is_file()}
        result = subprocess.run([sys.executable, "-I", "-B", str(target / ".aide/scripts/aide_lite.py"),
            "--repo-root", str(target), "apply-removal", "--target", str(target),
            "--expect-plan", plan["plan_digest"], "--json"],
            stdin=subprocess.DEVNULL, capture_output=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual({p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob("*") if p.is_file()}, before)


# No expected status, byte oracle, assertion or historical skip is edited.
# These methods contain no Windows API calls; they exercise shared behavior.
ORACLES = (
    "test_explicit_partial_recovery_finishes_fresh_and_predecessor_update",
    "test_exact_predecessor_rollback_restores_owned_bytes_and_receipt",
    "test_removal_detaches_brownfield_agents_section_preserving_authored_bytes",
    "test_removal_interruption_keeps_intent_and_reconciles_exact_bytes",
    "test_removal_recovers_after_receipt_retirement_before_intent_cleanup",
    "test_owned_repair_restores_missing_file_from_extracted_pack",
    "test_owned_repair_interruption_blocks_import_and_recovers_exact_postimage",
    "test_v2_optional_disable_persists_and_legacy_guards_refuse_skipped_path",
)
for name in ORACLES:
    method = getattr(original.ExportImportTests, name)
    setattr(PortableLifecycleBindingTests, name, getattr(method, "__wrapped__", method))


if __name__ == "__main__":
    unittest.main()
