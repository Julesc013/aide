"""Synthetic Python recipe data only; no real library copying or imports."""
import copy
from dataclasses import replace
import hashlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker import windows_python_image as recipe
from core.runtime.continuous_worker.state import Refused


def fixture():
    inputs = {name: ("# synthetic inert member " + name + "\n").encode() for name in sorted(recipe.BOOTSTRAP_MEMBERS)}
    value = {"schema": "aide.host.python-library.v1", "source_bytes": 65536, "archive_bytes": 131072,
             "members": [{"path": name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()} for name, data in inputs.items()]}
    return value, inputs


class PythonLibraryTests(unittest.TestCase):
    def test_deterministic_stored_archive_and_fixed_path_bytes(self):
        value, inputs = fixture(); spec = recipe.LibrarySpec.read(value); first = recipe.build_stdlib(spec, inputs)
        value["members"].reverse(); second = recipe.build_stdlib(recipe.LibrarySpec.read(value), dict(reversed(list(inputs.items()))))
        self.assertEqual(first, second); self.assertEqual(len(first.files), 2)
        self.assertEqual(first.files[1].contents, b"python314.zip\n.\n")
        self.assertIs(first.manifest()["tool_runtime_qualified"], False)
        self.assertEqual(first.files[0].declaration()["kind"], "generated_bytes")
        self.assertNotIn("source_identity", first.files[0].declaration())
        with zipfile.ZipFile(io.BytesIO(first.files[0].contents)) as archive:
            self.assertEqual(archive.namelist(), sorted(inputs)); self.assertEqual(archive.comment, b"")
            for info in archive.infolist():
                self.assertEqual(archive.read(info.filename), inputs[info.filename])
                self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0)); self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                self.assertEqual((info.create_system, info.create_version, info.extract_version), (0, 20, 20))
                self.assertEqual((info.extra, info.comment, info.flag_bits), (b"", b"", 0))
                self.assertEqual(info.external_attr, 0o100444 << 16); self.assertFalse(info.is_dir())

    def test_admission_is_frozen_and_tampered_typed_specs_refuse(self):
        value, inputs = fixture(); spec = recipe.LibrarySpec.read(value)
        value["members"][0]["sha256"] = "0" * 64
        self.assertNotEqual(spec.members[0].sha256, "0" * 64)
        for invalid in (replace(spec, members=()), replace(spec, fingerprint="0" * 64), replace(spec, archive_bytes=1)):
            with patch.object(recipe.zipfile, "ZipFile") as writer:
                with self.assertRaises(Refused): recipe.build_stdlib(invalid, inputs)
                writer.assert_not_called()

    def test_device_alias_traversal_and_site_injection_refuse(self):
        for path in ("../escape.py", "C:/escape.py", "a\\escape.py", "a:stream.py", "CON.py", "lpt1.py", "bad./x.py", "sitecustomize.py", "usercustomize.py", "site-packages/x.py", "__pycache__/x.py", "evil.pth", "foo.pyc", "café.py"):
            value, inputs = fixture(); value["members"].append(dict(value["members"][0], path=path))
            with self.subTest(path=path), self.assertRaises(Refused): recipe.LibrarySpec.read(value)
        for case in ("file", "directory", "file_directory"):
            value, inputs = fixture()
            if case == "file": value["members"].append(dict(value["members"][0], path=value["members"][0]["path"].upper().replace(".PY", ".py")))
            if case == "directory": value["members"].append(dict(value["members"][0], path="Encodings/other.py"))
            if case == "file_directory": value["members"].append(dict(value["members"][0], path="codecs.py/other.py"))
            with self.subTest(case=case), self.assertRaises(Refused): recipe.LibrarySpec.read(value)

    def test_missing_bootstrap_and_input_mutation_refuse_before_archive(self):
        value, inputs = fixture(); value["members"] = [row for row in value["members"] if row["path"] != "encodings/__init__.py"]
        with self.assertRaises(Refused): recipe.LibrarySpec.read(value)
        value, original = fixture(); spec = recipe.LibrarySpec.read(value)
        for case in ("missing", "extra", "length", "digest", "mutable"):
            inputs = dict(original); key = next(iter(inputs))
            if case == "missing": del inputs[key]
            if case == "extra": inputs["unknown.py"] = b"extra"
            if case == "length": inputs[key] += b"x"
            if case == "digest": inputs[key] = b"x" * len(inputs[key])
            if case == "mutable": inputs[key] = bytearray(inputs[key])
            with self.subTest(case=case), patch.object(recipe.zipfile, "ZipFile") as writer:
                with self.assertRaises(Refused): recipe.build_stdlib(spec, inputs)
                writer.assert_not_called()

    def test_limits_and_predicted_zip_overhead_refuse_before_writer(self):
        for key, bad in (("source_bytes", True), ("source_bytes", recipe.MAX_SOURCE_BYTES + 1), ("archive_bytes", recipe.MAX_ARCHIVE_BYTES + 1), ("archive_bytes", float("nan"))):
            value, inputs = fixture(); value[key] = bad
            with self.subTest(key=key, bad=bad), self.assertRaises(Refused): recipe.LibrarySpec.read(value)
        for kind in ("member", "total", "archive", "count"):
            value, inputs = fixture()
            if kind == "member": value["members"][0]["size"] = recipe.MAX_MEMBER_BYTES + 1
            if kind == "total": value["source_bytes"] = 1
            if kind == "archive": value["source_bytes"] = sum(len(data) for data in inputs.values()); value["archive_bytes"] = value["source_bytes"]
            if kind == "count": value["members"] = value["members"] * (recipe.MAX_MEMBERS // len(value["members"]) + 1)
            with self.subTest(kind=kind), self.assertRaises(Refused): recipe.LibrarySpec.read(value)

    def test_source_dictionary_change_after_validation_cannot_change_derived_members(self):
        value, inputs = fixture(); expected = dict(inputs); spec = recipe.LibrarySpec.read(value)
        original = recipe.zipfile.ZipFile
        class ConcurrentMutation(original):
            def writestr(self, info, data, *args, **kwargs):
                inputs["encodings/aliases.py"] = b"x" * len(inputs["encodings/aliases.py"])
                return super().writestr(info, data, *args, **kwargs)
        with patch.object(recipe.zipfile, "ZipFile", ConcurrentMutation): bundle = recipe.build_stdlib(spec, inputs)
        with original(io.BytesIO(bundle.files[0].contents)) as archive:
            for path, data in expected.items(): self.assertEqual(archive.read(path), data)

    def test_derived_kind_never_accepts_ambient_path_payload_or_mutable_bytes(self):
        for path, contents, producer in (("unknown.zip", b"x", "1" * 64), ("python314._pth", b"C:/ambient\nimport site\n", "1" * 64),
                                          ("python314.zip", bytearray(b"x"), "1" * 64), ("python314.zip", b"x", "not-a-hash"),
                                          ("python314.zip", b"", "1" * 64)):
            with self.subTest(path=path, kind=type(contents).__name__), self.assertRaises(Refused): recipe.DerivedFile(path, contents, producer)


if __name__ == "__main__": unittest.main()
