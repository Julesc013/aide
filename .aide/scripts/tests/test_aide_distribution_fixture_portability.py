"""Reusable regressions for fixture-only distribution helpers.

These tests are not native Windows qualification or a hostile-writer sandbox.
"""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from core.distribution import temp_workspace as tw
from core.distribution import operation_executor as oe


class FixturePortabilityRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "workspace"
        self.root.mkdir()

    def test_drive_relative_name_is_unsafe(self):
        self.assertTrue(tw.is_unsafe_relative_path("C:escape.txt"))

    def test_stream_name_is_unsafe(self):
        self.assertTrue(tw.is_unsafe_relative_path("file.txt:payload"))

    def test_device_name_is_unsafe(self):
        self.assertTrue(tw.is_unsafe_relative_path("nested/NUL.txt"))

    def test_root_alias_is_unsafe(self):
        self.assertTrue(tw.is_unsafe_relative_path("."))

    def test_windows_separators_have_same_identity(self):
        self.assertEqual(tw.safe_join(self.root, "docs\\guide.md"), self.root / "docs" / "guide.md")

    def test_snapshot_does_not_follow_file_symlink(self):
        outside = self.root.parent / "outside.txt"
        outside.write_text("synthetic canary", encoding="utf-8")
        try:
            (self.root / "link").symlink_to(outside)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(str(exc))
        with self.assertRaises(ValueError):
            tw.snapshot_tree(self.root)
        self.assertEqual(outside.read_text(encoding="utf-8"), "synthetic canary")

    def test_invalid_initial_map_writes_nothing(self):
        with self.assertRaises(ValueError):
            tw.write_initial_files(self.root, {"a.txt": "first", "z/../escape": "bad"})
        self.assertEqual(list(self.root.iterdir()), [])

    def test_invalid_restore_keeps_current_tree(self):
        (self.root / "current.txt").write_text("keep", encoding="utf-8")
        before = tw.snapshot_tree(self.root)
        with self.assertRaises(ValueError):
            tw.restore_snapshot(self.root, {"../escape": "sha256:bad"}, {"../escape": "bad"})
        self.assertEqual(tw.snapshot_tree(self.root), before)

    def test_add_cannot_overwrite_existing_file(self):
        p = self.root / "owned.txt"
        p.write_text("keep", encoding="utf-8")
        outcome = oe.execute_operation(self.root, {
            "operation_class": "add_managed_file", "target_relative_path": "owned.txt",
            "ownership_class": "vendor_managed_file", "rollback_covered": True,
            "postimage": "replace"})
        self.assertEqual(outcome["status"], "FAILED_VALIDATION")
        self.assertEqual(p.read_text(encoding="utf-8"), "keep")


class PortablePathTableTests(unittest.TestCase):
    """Explicit independent expected examples, not generated from implementation."""


_INVALID = [
    "", ".", "..", "./x", "x/.", "x/..", "x/../y", "../x", "x//y", "x/", "x\\",
    "/absolute", "\\rooted", "//host/share", "\\\\host\\share", "C:", "C:x", "C:/x", "C:\\x",
    "//?/C:/x", "//./pipe/x", "x:y", "x/file:stream", "x/file::$DATA", "x/space ", "x/dot.",
    "CON", "con.txt", "NUL.tar.gz", "aux", "prn.txt", "com1.txt", "LPT9", "COM¹", "lpt².txt",
    "CONIN$", "CONOUT$", "CLOCK$", "x/CON .txt", "x<y", "x>y", "x\"y", "x|y", "x?y", "x*y",
    "x\x00y", "x\ny", "x\ty", "x\x7fy", "bad\ud800", None, 12, [], {}, True,
]
_VALID = ["x", "x.txt", ".gitignore", ".aide/config.json", "docs/read-me.md", "v1.0/file_1.py",
          "with space/file.md", "café/日本語.txt", "a/b/c", "a\\b\\c", "COM10.txt", "conductor.txt"]


def _reject_case(value):
    def test(self):
        self.assertTrue(tw.is_unsafe_relative_path(value), repr(value))
        self.assertIsInstance(tw.relative_path_refusal(value), str)
    return test


def _accept_case(value):
    def test(self):
        self.assertFalse(tw.is_unsafe_relative_path(value), repr(value))
        self.assertIsNone(tw.relative_path_refusal(value))
    return test


for _i, _value in enumerate(_INVALID):
    setattr(PortablePathTableTests, f"test_reject_{_i:02d}", _reject_case(_value))
for _i, _value in enumerate(_VALID):
    setattr(PortablePathTableTests, f"test_accept_{_i:02d}", _accept_case(_value))


class FixtureCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "root"
        self.root.mkdir()

    def symlink(self, path, target, directory=False):
        try:
            path.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")

    def windows_short_leaf(self, path):
        if os.name != "nt":
            self.skipTest("Windows 8.3 aliases are Windows-specific")
        get_short_path_name = ctypes.WinDLL("kernel32", use_last_error=True).GetShortPathNameW
        get_short_path_name.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32]
        get_short_path_name.restype = ctypes.c_uint32
        buffer = ctypes.create_unicode_buffer(32768)
        length = get_short_path_name(str(path), buffer, len(buffer))
        if length == 0:
            self.skipTest(f"GetShortPathNameW unavailable: {ctypes.get_last_error()}")
        if length >= len(buffer):
            self.fail("GetShortPathNameW exceeded the fixed test buffer")
        short_leaf = Path(buffer.value).name
        if short_leaf.casefold() == path.name.casefold():
            self.skipTest("test volume did not generate a distinct 8.3 alias")
        return short_leaf


class FixtureFilesystemTests(FixtureCase):
    def test_empty_snapshot_and_hash_compatibility(self):
        self.assertEqual(tw.snapshot_tree(self.root), {})
        expected = "sha256:" + hashlib.sha256(b"{}").hexdigest()
        self.assertEqual(tw.tree_digest(self.root), expected)
        self.assertEqual(tw.directory_digest(self.root), expected)

    def test_snapshot_exact_raw_bytes_and_order(self):
        (self.root / "z.bin").write_bytes(b"\x00\xff\r\n")
        (self.root / "a.txt").write_bytes(b"text\r\n")
        result = tw.snapshot_tree(self.root)
        expected = {"a.txt": "sha256:" + hashlib.sha256(b"text\r\n").hexdigest(),
                    "z.bin": "sha256:" + hashlib.sha256(b"\x00\xff\r\n").hexdigest()}
        self.assertEqual(result, expected)
        self.assertEqual(list(result), ["a.txt", "z.bin"])
        self.assertEqual(tw.directory_digest(self.root), tw.tree_digest(self.root))

    def test_missing_snapshot_is_empty(self):
        self.assertEqual(tw.snapshot_tree(self.root / "missing"), {})

    def test_snapshot_chunked_file(self):
        data = b"x" * (1024 * 1024 + 7)
        (self.root / "large").write_bytes(data)
        self.assertEqual(tw.snapshot_tree(self.root)["large"], tw.sha256_bytes(data))

    def test_internal_symlink_is_not_silently_resolved(self):
        (self.root / "real").write_text("keep")
        self.symlink(self.root / "alias", self.root / "real")
        with self.assertRaises(ValueError):
            tw.safe_join(self.root, "alias")

    def test_directory_symlink_is_refused(self):
        outside = self.root.parent / "outside"
        outside.mkdir()
        self.symlink(self.root / "alias", outside, True)
        with self.assertRaises(ValueError):
            tw.safe_join(self.root, "alias/new")
        with self.assertRaises(ValueError):
            tw.snapshot_tree(self.root)
        self.assertEqual(list(outside.iterdir()), [])

    def test_dangling_symlink_is_refused(self):
        self.symlink(self.root / "alias", self.root.parent / "missing")
        with self.assertRaises(ValueError):
            tw.safe_join(self.root, "alias")
        with self.assertRaises(ValueError):
            tw.snapshot_tree(self.root)

    def test_symlink_root_is_refused(self):
        alias = self.root.parent / "root-alias"
        self.symlink(alias, self.root, True)
        with self.assertRaises(ValueError):
            tw.snapshot_tree(alias)
        with self.assertRaises(ValueError):
            tw.safe_join(alias, "x")

    def test_file_root_is_refused(self):
        file = self.root / "file"
        file.write_text("keep")
        with self.assertRaises(ValueError):
            tw.safe_join(file, "x")
        with self.assertRaises(ValueError):
            tw.snapshot_tree(file)

    def test_file_parent_is_refused(self):
        (self.root / "file").write_text("keep")
        with self.assertRaises(ValueError):
            tw.safe_join(self.root, "file/child")

    def test_hardlinked_file_is_refused(self):
        outside = self.root.parent / "outside"
        outside.write_text("keep")
        try:
            os.link(outside, self.root / "alias")
        except OSError as exc:
            self.skipTest(str(exc))
        with self.assertRaises(ValueError):
            tw.safe_join(self.root, "alias")
        with self.assertRaises(ValueError):
            tw.snapshot_tree(self.root)
        self.assertEqual(outside.read_text(), "keep")

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO not supported")
    def test_special_file_refused_without_blocking_read(self):
        os.mkfifo(self.root / "pipe")
        with self.assertRaises(ValueError):
            tw.snapshot_tree(self.root)

    def test_windows_reparse_attribute_is_refused(self):
        from types import SimpleNamespace
        fake = SimpleNamespace(st_mode=0o100644, st_file_attributes=0x400, st_nlink=1)
        with mock.patch.object(Path, "lstat", return_value=fake):
            with self.assertRaisesRegex(ValueError, "symlink_reparse_refused"):
                tw.safe_join(self.root, "x")

    def test_existing_parent_case_alias_is_refused(self):
        (self.root / "Data").mkdir()
        with self.assertRaisesRegex(ValueError, "path_collision_refused"):
            tw.safe_join(self.root, "data/new")

    def test_existing_file_case_alias_is_refused(self):
        (self.root / "Current.txt").write_text("keep")
        with self.assertRaisesRegex(ValueError, "path_collision_refused"):
            tw.safe_join(self.root, "current.txt")

    def test_windows_short_name_alias_is_typed_zero_write(self):
        target = self.root / "LongFixtureNameForAlias.txt"
        target.write_text("keep", encoding="utf-8")
        short_leaf = self.windows_short_leaf(target)
        with self.assertRaisesRegex(ValueError, "path_collision_refused"):
            tw.safe_join(self.root, short_leaf)
        operation = {
            "operation_class": "update_managed_file",
            "target_relative_path": short_leaf,
            "ownership_class": "vendor_managed_file",
            "rollback_covered": True,
            "preimage_digest": tw.sha256_text("keep"),
            "postimage": "changed",
        }
        outcome = oe.execute_operation(self.root, operation)
        self.assertEqual(outcome["status"], "FAILED_VALIDATION")
        self.assertEqual(
            outcome["refusal_code"],
            "distribution_apply_engine.path_collision_refused",
        )
        self.assertEqual(target.read_text(encoding="utf-8"), "keep")

    def test_initial_case_aliases_refused_before_write(self):
        with self.assertRaises(ValueError):
            tw.write_initial_files(self.root, {"a.txt": "one", "A.txt": "two"})
        self.assertEqual(list(self.root.iterdir()), [])

    def test_initial_parent_case_aliases_refused_before_write(self):
        with self.assertRaises(ValueError):
            tw.write_initial_files(self.root, {"Data/one": "one", "data/two": "two"})
        self.assertEqual(list(self.root.iterdir()), [])

    def test_initial_separator_aliases_refused_before_write(self):
        with self.assertRaises(ValueError):
            tw.write_initial_files(self.root, {"a/b": "one", "a\\b": "two"})
        self.assertEqual(list(self.root.iterdir()), [])

    def test_initial_unicode_aliases_refused_before_write(self):
        with self.assertRaises(ValueError):
            tw.write_initial_files(self.root, {"é.txt": "one", "e\u0301.txt": "two"})
        self.assertEqual(list(self.root.iterdir()), [])

    def test_file_parent_overlap_refused_before_write(self):
        with self.assertRaises(ValueError):
            tw.write_initial_files(self.root, {"a": "one", "a/b": "two"})
        self.assertEqual(list(self.root.iterdir()), [])

    def test_initial_content_type_error_preserves_root(self):
        with self.assertRaises(ValueError):
            tw.write_initial_files(self.root, {"a": "one", "b": 12})
        self.assertEqual(list(self.root.iterdir()), [])

    def test_initial_unencodable_text_preserves_root(self):
        with self.assertRaises(UnicodeEncodeError):
            tw.write_initial_files(self.root, {"a": "one", "b": "\ud800"})
        self.assertEqual(list(self.root.iterdir()), [])

    def test_initial_existing_file_preserved_before_other_writes(self):
        (self.root / "z").write_text("keep")
        with self.assertRaises(ValueError):
            tw.write_initial_files(self.root, {"a": "one", "z": "two"})
        self.assertEqual(tw.snapshot_tree(self.root), {"z": tw.sha256_text("keep")})

    def test_valid_initial_map_normalizes_separators(self):
        tw.write_initial_files(self.root, {"nested\\file": "x\r\n", "plain": "y"})
        self.assertEqual((self.root / "nested/file").read_bytes(), b"x\r\n")
        self.assertEqual(tw.snapshot_tree(self.root), {"nested/file": tw.sha256_text("x\r\n"), "plain": tw.sha256_text("y")})

    def test_restore_valid_preimage(self):
        (self.root / "new").write_text("new")
        contents = {"old/x": "old\r\n"}
        snapshot = {key: tw.sha256_text(value) for key, value in contents.items()}
        tw.restore_snapshot(self.root, snapshot, contents)
        self.assertEqual(tw.snapshot_tree(self.root), snapshot)
        self.assertEqual((self.root / "old/x").read_bytes(), b"old\r\n")

    def test_restore_can_replace_file_with_directory(self):
        (self.root / "nested").write_text("replace old fixture file")
        contents = {"nested/new": "restored"}
        snapshot = {key: tw.sha256_text(value) for key, value in contents.items()}
        tw.restore_snapshot(self.root, snapshot, contents)
        self.assertEqual(tw.snapshot_tree(self.root), snapshot)

    def test_restore_digest_mismatch_preserves_tree(self):
        (self.root / "current").write_text("keep")
        before = tw.snapshot_tree(self.root)
        with self.assertRaises(ValueError):
            tw.restore_snapshot(self.root, {"new": tw.sha256_text("different")}, {"new": "bad"})
        self.assertEqual(tw.snapshot_tree(self.root), before)

    def test_restore_missing_contents_preserves_tree(self):
        (self.root / "current").write_text("keep")
        before = tw.snapshot_tree(self.root)
        with self.assertRaises(ValueError):
            tw.restore_snapshot(self.root, {"new": tw.sha256_text("new")}, {})
        self.assertEqual(tw.snapshot_tree(self.root), before)

    def test_restore_extra_contents_preserves_tree(self):
        (self.root / "current").write_text("keep")
        before = tw.snapshot_tree(self.root)
        with self.assertRaises(ValueError):
            tw.restore_snapshot(self.root, {}, {"extra": "x"})
        self.assertEqual(tw.snapshot_tree(self.root), before)

    def test_restore_noncanonical_locator_preserves_tree(self):
        with self.assertRaises(ValueError):
            tw.restore_snapshot(self.root, {"x\\y": tw.sha256_text("v")}, {"x\\y": "v"})
        self.assertEqual(list(self.root.iterdir()), [])

    def test_restore_symlink_tree_preserved(self):
        outside = self.root.parent / "outside"
        outside.write_text("canary")
        self.symlink(self.root / "alias", outside)
        with self.assertRaises(ValueError):
            tw.restore_snapshot(self.root, {}, {})
        self.assertTrue((self.root / "alias").is_symlink())
        self.assertEqual(outside.read_text(), "canary")

    def test_restore_root_volume_is_refused(self):
        with self.assertRaises(ValueError):
            tw.restore_snapshot(Path(self.root.anchor), {}, {})

    def test_temporary_root_cleanup_and_valid_id(self):
        with tw.temporary_fixture_workspace("portable_case-01") as root:
            self.assertTrue(root.is_dir())
            tw.write_initial_files(root, {"a": "b"})
        self.assertFalse(root.exists())

    def test_bad_scenario_id_never_calls_tempfile(self):
        for scenario in ("../escape", "a/b", "\\a", "", None, "a" * 81):
            with self.subTest(scenario=scenario), mock.patch.object(tw.tempfile, "TemporaryDirectory") as constructor:
                with self.assertRaises(ValueError):
                    with tw.temporary_fixture_workspace(scenario):
                        self.fail("must not yield")
                constructor.assert_not_called()

    def test_snapshot_short_read_is_refused_and_fd_closed(self):
        (self.root / "x").write_bytes(b"data")
        original_close = os.close
        with mock.patch.object(tw.os, "read", return_value=b""), mock.patch.object(tw.os, "close", wraps=original_close) as close:
            with self.assertRaisesRegex(ValueError, "snapshot_changed"):
                tw.snapshot_tree(self.root)
            self.assertEqual(close.call_count, 1)

    def test_snapshot_content_changed_during_read_is_refused(self):
        path = self.root / "x"
        path.write_bytes(b"data")
        original_read = os.read
        first = True
        def changing_read(fd, size):
            nonlocal first
            result = original_read(fd, size)
            if first:
                first = False
                path.write_bytes(b"changed")
            return result
        with mock.patch.object(tw.os, "read", side_effect=changing_read):
            with self.assertRaisesRegex(ValueError, "snapshot_changed"):
                tw.snapshot_tree(self.root)

    def test_source_inspection_permission_error_propagates(self):
        with mock.patch.object(Path, "lstat", side_effect=PermissionError("denied")):
            with self.assertRaises(PermissionError):
                tw.snapshot_tree(self.root)

    def test_json_helpers_keep_existing_format(self):
        value = {"z": 1, "a": [True, None]}
        path = self.root / "nested/report.json"
        tw.write_json(path, value)
        self.assertEqual(tw.read_json(path), value)
        self.assertEqual(path.read_bytes(), tw.canonical_json(value).encode("utf-8"))


class OperationCompatibilityTests(FixtureCase):
    """Operation-level assertions reuse fixtures, not the semantic oracle."""
    def operation(self, kind="add_managed_file", path="new.txt", **extra):
        value = {"operation_class": kind, "target_relative_path": path,
                 "ownership_class": "vendor_managed_file", "rollback_covered": True,
                 "postimage": "new"}
        value.update(extra)
        return value

    def test_operation_invalid_paths_are_typed_zero_write(self):
        for path in ("C:bad", "NUL.txt", "x:stream", ".", None, 12, "../x", "/tmp/x"):
            with self.subTest(path=path):
                outcome = oe.execute_operation(self.root, self.operation(path=path))
                self.assertEqual(outcome["status"], "FAILED_VALIDATION")
                self.assertEqual(list(self.root.iterdir()), [])

    def test_original_absolute_and_traversal_codes_preserved(self):
        for path, code in (("C:/bad", "absolute_path_refused"), ("/bad", "absolute_path_refused"), ("../bad", "path_traversal_refused")):
            outcome = oe.execute_operation(self.root, self.operation(path=path))
            self.assertEqual(outcome["refusal_code"], "distribution_apply_engine." + code)

    def test_new_source_latest_output_guard_preserved(self):
        outcome = oe.execute_operation(self.root, self.operation(path=".aide/context/latest-context.md"))
        self.assertEqual(outcome["refusal_code"], "distribution_apply_engine.source_latest_output_refused")

    def test_operation_link_refusal_is_typed(self):
        outside = self.root.parent / "outside"
        outside.write_text("keep")
        self.symlink(self.root / "alias", outside)
        outcome = oe.execute_operation(self.root, self.operation(path="alias"))
        self.assertEqual(outcome["refusal_code"], "distribution_apply_engine.symlink_reparse_refused")
        self.assertEqual(outside.read_text(), "keep")

    def test_operation_directory_refusal_is_typed(self):
        (self.root / "directory").mkdir()
        outcome = oe.execute_operation(self.root, self.operation(path="directory"))
        self.assertEqual(outcome["refusal_code"], "distribution_apply_engine.non_regular_path_refused")

    def test_operation_path_inspection_failure_is_typed(self):
        with mock.patch.object(oe, "safe_join", side_effect=PermissionError("denied")):
            outcome = oe.execute_operation(self.root, self.operation())
        self.assertEqual(outcome["refusal_code"], "distribution_apply_engine.path_inspection_failed")

    def test_add_update_remove_roundtrip(self):
        self.assertEqual(oe.execute_operation(self.root, self.operation())["status"], "APPLIED_TEMP")
        update = self.operation("update_managed_file", preimage_digest=tw.sha256_text("new"), postimage="updated")
        self.assertEqual(oe.execute_operation(self.root, update)["status"], "APPLIED_TEMP")
        remove = self.operation("remove_managed_file", preimage_digest=tw.sha256_text("updated"))
        self.assertEqual(oe.execute_operation(self.root, remove)["status"], "APPLIED_TEMP")
        self.assertFalse((self.root / "new.txt").exists())

    def test_managed_section_roundtrip_preserves_manual_text(self):
        path = self.root / "guide.md"
        path.write_text("manual before\n", encoding="utf-8")
        add = self.operation("add_managed_section", "guide.md", section_identity="test", section_content="old")
        self.assertEqual(oe.execute_operation(self.root, add)["status"], "APPLIED_TEMP")
        update = self.operation("update_managed_section", "guide.md", section_identity="test", section_content="new")
        self.assertEqual(oe.execute_operation(self.root, update)["status"], "APPLIED_TEMP")
        self.assertTrue(path.read_text().startswith("manual before\n"))
        remove = self.operation("remove_managed_section", "guide.md", section_identity="test")
        self.assertEqual(oe.execute_operation(self.root, remove)["status"], "APPLIED_TEMP")
        self.assertEqual(path.read_text(), "manual before\n")

    def test_protected_ownership_stays_refused(self):
        for ownership in ("project_owned", "project_overlay", "local_only", "runtime_generated", "evidence_only", "never_touch", "unknown"):
            outcome = oe.execute_operation(self.root, self.operation(ownership_class=ownership))
            self.assertEqual(outcome["status"], "FAILED_VALIDATION")
        self.assertEqual(list(self.root.iterdir()), [])

    def test_uncovered_rollback_stays_refused(self):
        outcome = oe.execute_operation(self.root, self.operation(rollback_covered=False))
        self.assertEqual(outcome["refusal_code"], "distribution_apply_engine.operation_lacking_rollback_coverage_refused")

    def test_case_collision_helper_existing_behavior(self):
        self.assertEqual(oe.detect_case_collisions(["A/b", "a/b"]), ["a/b"])
        self.assertEqual(oe.detect_case_collisions(["a/b", "a/b"]), [])


if __name__ == "__main__":
    unittest.main()
