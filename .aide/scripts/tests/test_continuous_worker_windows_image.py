"""H2 source/ordinary synthetic tests; no real tools, package grants or lowbox launches."""
import copy
import ctypes as C
from ctypes import wintypes as W
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker import windows_image as image
from core.runtime.continuous_worker import windows_security_objects as native
from core.runtime.continuous_worker.state import Refused

USER = "S-1-5-21-11-22-33-1001"
PACKAGE = "S-1-15-2-11-22-33-44-55-66-77"
DATA = bytes(range(256)) * 513
DIGEST = hashlib.sha256(DATA).hexdigest()


def fixture():
    return {"schema": "aide.host.private-image.v1", "generation": "a" * 32,
            "input_root": r"C:\trusted", "input_identity": {"volume": 1, "file_id": "1" * 32},
            "output_root": "C:\\owned\\image-" + "a" * 32,
            "parent_identity": {"volume": 1, "file_id": "2" * 32},
            "user_sid": USER, "package_sid": PACKAGE, "entrypoint": "probe.exe",
            "limits": {"entries": 8, "file_bytes": 262144, "total_bytes": 524288, "seconds": 10},
            "files": [{"path": "probe.exe", "source": "probe.exe", "size": len(DATA), "sha256": DIGEST,
                       "source_identity": {"volume": 1, "file_id": "3" * 32}}]}


class ImageAdmissionTests(unittest.TestCase):
    def test_immutable_canonical_admission_survives_mutated_input_and_order(self):
        value = fixture(); other = dict(value["files"][0], path="_socket.pyd", source="_socket.pyd")
        value["files"].append(other)
        first = image.ImagePlan.read(value)
        value["files"].reverse()
        self.assertEqual(first, image.ImagePlan.read(value))
        value["files"][0]["size"] = 0
        self.assertEqual(first.files[0].size, len(DATA))
        self.assertEqual(first.validate(), first)
        with self.assertRaises(Exception): first.files[0].path = "foreign"

    def test_paths_reject_devices_streams_traversal_unicode_and_case_collisions(self):
        for name in ("CON", "con.txt", "AUX", "NUL", "COM1.dll", "lpt9", ".", "..", ".hidden", "abc.", "a ", "a:b", "a/b", "a\\b", "COM¹", "\x00"):
            with self.subTest(name=name), self.assertRaises(Refused): native.literal_component(name)
        self.assertEqual(native.literal_component("_socket.pyd"), "_socket.pyd")
        for failure in ("case_file", "case_dir", "file_dir", "source_alias", "source_case_dir", "source_file_dir", "depth", "directory_budget"):
            value = fixture(); row = value["files"][0]
            if failure == "case_file": value["files"].append(dict(row, path="PROBE.EXE", source="other.exe"))
            if failure == "case_dir":
                row.update(path="Lib/probe.exe"); value["entrypoint"] = row["path"]
                value["files"].append(dict(row, path="lib/other.exe", source="other.exe"))
            if failure == "file_dir": value["files"].append(dict(row, path="probe.exe/other.exe", source="other.exe"))
            if failure == "source_alias": value["files"].append(dict(row, path="other.exe", source="PROBE.EXE"))
            if failure == "source_case_dir":
                row["source"] = "Lib/probe.exe"
                value["files"].append(dict(row, path="other.exe", source="lib/other.exe"))
            if failure == "source_file_dir": value["files"].append(dict(row, path="other.exe", source="probe.exe/other.exe"))
            if failure == "depth": row["path"] = "a/" * 12 + "probe.exe"; value["entrypoint"] = row["path"]
            if failure == "directory_budget": row["path"] = "a/b/probe.exe"; value["entrypoint"] = row["path"]; value["limits"]["entries"] = 2
            with self.subTest(failure=failure), self.assertRaises(Refused): image.ImagePlan.read(value)

    def test_root_alias_devices_surrogates_and_utf16_length_refuse_before_effects(self):
        bad_parts = ["parent.", "parent ", "CON", "nul.txt", "CON .txt", "COM¹", "LPT³.dat", "CONIN$", "CONOUT$",
                     "bad<name", "bad?name", "bad|name", "bad\x1fname", "bad\ud800name", "x" + "\U0001f680" * 89]
        for part in bad_parts:
            for field in ("input_root", "output_root"):
                value = fixture()
                value[field] = "C:\\" + part + "\\" + ("trusted" if field == "input_root" else "image-" + value["generation"])
                with self.subTest(part=ascii(part), field=field), patch.object(image, "SourceDirectory") as source, patch("builtins.open") as opened:
                    with self.assertRaises(Refused): image.ImagePlan.read(value)
                    source.assert_not_called(); opened.assert_not_called()
        value = fixture(); value["input_root"] = "C:\\Program Files\\Python-é\\測試"
        value["output_root"] = "C:\\owned é\\image-" + value["generation"]
        self.assertEqual(image.ImagePlan.read(value).input_root, value["input_root"])

    def test_actual_name_overlap_and_case_sensitive_siblings_refuse_conservatively(self):
        def held(name, identity): return SimpleNamespace(canonical_name=name, expected=(1, identity))
        source = held(r"\Device\HarddiskVolume3\source", "source")
        for parent, output in [(held(r"\Device\HarddiskVolume3\source", "source"), r"C:\alias\image"),
                               (held(r"\Device\HarddiskVolume3\source\nested", "nested"), r"C:\alias\image"),
                               (held(r"\Device\HarddiskVolume3\SOURCE", "different-case-sensitive-id"), r"C:\alias\image")]:
            with self.subTest(parent=parent), self.assertRaises(Refused): image._separate_roots(source, parent, output)
        # A candidate ancestor of the held input also refuses.
        with self.assertRaises(Refused):
            image._separate_roots(held(r"\Device\HarddiskVolume3\image\source", "source"), held(r"\Device\HarddiskVolume3", "parent"), r"C:\image")
        image._separate_roots(source, held(r"\Device\HarddiskVolume4\owned", "parent"), r"D:\owned\image")

    def test_budget_and_root_refusals_happen_before_native_or_reservation_effects(self):
        cases = []
        for key, bad in (("entries", True), ("entries", 2049), ("file_bytes", 512 * 1024**2 + 1),
                         ("total_bytes", 768 * 1024**2 + 1), ("seconds", float("nan")), ("seconds", 301)):
            value = fixture(); value["limits"][key] = bad; cases.append(value)
        for key, bad in (("input_root", r"C:\trusted\..\secret"), ("output_root", r"\\host\share\image"),
                         ("package_sid", "S-1-15-2-1"), ("entrypoint", "absent.exe"), ("generation", True)):
            value = fixture(); value[key] = bad; cases.append(value)
        value = fixture(); value["input_root"] = r"C:\owned"; cases.append(value)
        value = fixture(); value["files"][0]["size"] = True; cases.append(value)
        value = fixture(); value["files"][0]["size"] = 300000; cases.append(value)
        cases += [None, [], True, {}]
        for value in cases:
            with self.subTest(value=value), patch.object(image, "SourceDirectory") as sources, patch("builtins.open") as opened:
                with self.assertRaises(Refused): image.ImagePlan.read(value)
                sources.assert_not_called(); opened.assert_not_called()
        plan = image.ImagePlan.read(fixture())
        for invalid in (replace(plan, files=()), replace(plan, fingerprint="0" * 64), replace(plan, output_root=r"C:\foreign")):
            with patch.object(image, "SourceDirectory") as sources, patch("builtins.open") as opened:
                with self.assertRaises(Refused): image.prepare_image(invalid, guard=lambda: None)
                sources.assert_not_called(); opened.assert_not_called()


@unittest.skipUnless(os.name == "nt", "actual Windows file handles required")
class NativeStreamTests(unittest.TestCase):
    def owned_file(self, folder):
        import msvcrt
        path = Path(folder) / "synthetic.bin"
        file = path.open("xb+")
        handle = msvcrt.get_osfhandle(file.fileno())
        obj = native.OwnedObject(handle, path.name, None, str(path), False, USER, native._identity(handle))
        return file, obj, path

    def test_actual_stream_copies_binary_chunks_and_preserves_old_write_ceiling(self):
        with tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
            file, obj, path = self.owned_file(folder)
            with file:
                chunks = (DATA[i:i + image.CHUNK] for i in range(0, len(DATA), image.CHUNK))
                self.assertEqual(obj.write_stream(chunks, size=len(DATA), sha256=DIGEST, limit=262144, deadline=10, clock=lambda: 0), DIGEST)
                self.assertEqual(obj.content_sha256, DIGEST)
                with self.assertRaises(Refused): obj.write_stream([], size=0, sha256=hashlib.sha256(b"").hexdigest(), limit=1, deadline=10, clock=lambda: 0)
            self.assertEqual(path.read_bytes(), DATA)
        obj = native.OwnedObject(123, "file", None, r"C:\owned\file", False, USER, {"file_id": "synthetic"})
        with patch.object(native, "_identity", return_value=obj.identity), patch.object(native, "write_file") as write:
            with self.assertRaises(Refused): obj.write(b"x" * (16 * 1024**2 + 1))
            write.assert_not_called()

    def test_actual_large_and_empty_streams_use_explicit_image_limits(self):
        block = bytes(range(256)) * 256
        for count in (0, 257):
            with self.subTest(chunks=count), tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
                digest = hashlib.sha256()
                for _ in range(count): digest.update(block)
                expected, size = digest.hexdigest(), count * len(block)
                file, obj, path = self.owned_file(folder)
                with file:
                    self.assertEqual(obj.write_stream((block for _ in range(count)), size=size, sha256=expected,
                                                     limit=17 * 1024**2, deadline=time.monotonic() + 15), expected)
                    self.assertTrue(obj.written)
                self.assertEqual(path.stat().st_size, size)
                with path.open("rb") as copied: self.assertEqual(hashlib.file_digest(copied, "sha256").hexdigest(), expected)

    def test_stream_admission_refuses_before_consuming_or_writing(self):
        for change in ({"size": True}, {"limit": 512 * 1024**2 + 1}, {"sha256": "bad"}, {"deadline": float("nan")}, {"deadline": -1}, {"deadline": 3601}):
            with self.subTest(change=change), tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
                file, obj, path = self.owned_file(folder)
                args = dict(size=1, sha256=hashlib.sha256(b"x").hexdigest(), limit=1, deadline=10, clock=lambda: 0); args.update(change)
                with file, patch.object(native, "write_file") as write:
                    with self.assertRaises(Refused): obj.write_stream([b"x"], **args)
                    write.assert_not_called(); self.assertFalse(obj.written)
                self.assertEqual(path.read_bytes(), b"")

    def test_bad_short_extra_or_fragmented_stream_is_retained_and_never_sealed(self):
        streams = [[DATA[:65536]], [DATA[:65536], DATA[65536:131072], DATA[131072:], b"extra"],
                   [b"x"] * 6, [b""], ["not bytes"], [b"x" * 65537]]
        for blocks in streams:
            with self.subTest(length=len(blocks)), tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
                file, obj, path = self.owned_file(folder)
                with file:
                    with self.assertRaises(Refused): obj.write_stream(iter(blocks), size=len(DATA), sha256=DIGEST, limit=262144, deadline=10, clock=lambda: 0)
                    self.assertTrue(obj.written); self.assertIsNone(obj.content_sha256)
                    with patch.object(native, "_open") as opened, patch.object(native, "set_security") as grant:
                        with self.assertRaises(Refused): obj.seal()
                        with self.assertRaises(Refused): obj.grant(PACKAGE, mode="read")
                        opened.assert_not_called(); grant.assert_not_called()
                    with self.assertRaises(Refused): obj.write(b"retry")
                self.assertTrue(path.exists())

    def test_source_exception_revocation_flush_and_deadline_uncertainty_retain_once(self):
        for failure in ("source", "guard", "digest", "flush", "deadline"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
                file, obj, path = self.owned_file(folder); expired = [False]
                def guard():
                    if failure == "guard" and expired[0]: raise Refused("revoked source")
                obj.guard = guard
                def chunks():
                    yield DATA[:65536]
                    if failure == "source": raise OSError("synthetic read failure")
                    if failure in ("guard", "deadline"): expired[0] = True
                    yield DATA[65536:131072]
                    yield DATA[131072:]
                original = native.flush_file
                with file, patch.object(native, "flush_file", side_effect=lambda handle: False if failure == "flush" else original(handle)):
                    with self.assertRaises((OSError, Refused)):
                        obj.write_stream(chunks(), size=len(DATA), sha256="0" * 64 if failure == "digest" else DIGEST,
                                         limit=262144, deadline=10, clock=lambda: 10 if failure == "deadline" and expired[0] else 0)
                    obj.guard = None
                    self.assertIsNone(obj.content_sha256)
                    with self.assertRaises(Refused): obj.seal()
                    with self.assertRaises(Refused): obj.write(b"retry")
                self.assertTrue(path.exists())
                self.assertGreater(path.stat().st_size, 0)

    def test_actual_source_read_lease_binds_bytes_and_denies_simultaneous_writer(self):
        with tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
            path = Path(folder) / "_socket.pyd"; path.write_bytes(DATA)
            handle = native._open(native.native_path(folder), None, directory=True, create=False, read_only_source=True)
            try: identity = tuple(native._identity(handle)[key] for key in ("volume", "file_id"))
            finally: native.close(handle)
            handle = native._open(native.native_path(str(path)), None, directory=False, create=False, read_only_source=True)
            try: file_id = tuple(native._identity(handle)[key] for key in ("volume", "file_id"))
            finally: native.close(handle)
            source = image.SourceDirectory(folder, identity, lambda: None)
            try:
                entry = image.ImageFile(path.name, path.name, len(DATA), DIGEST, file_id)
                stream = source.chunks(entry); first = next(stream)
                with self.assertRaises(OSError): path.write_bytes(b"foreign replacement")
                self.assertEqual(first + b"".join(stream), DATA)
                wrong = replace(entry, source_identity=(file_id[0], "f" * 32))
                with self.assertRaises(Refused): list(source.chunks(wrong))
            finally: source.close()
            self.assertEqual(path.read_bytes(), DATA)

    def test_actual_held_descendant_blocks_ancestor_path_substitution(self):
        with tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
            root = Path(folder).resolve(); ancestor = root / "ancestor"; child = ancestor / "held"
            child.mkdir(parents=True); replacement = root / "moved"
            self.assertEqual(ancestor.resolve().parent, root); self.assertEqual(replacement.parent.resolve(), root)
            handle = native._open(native.native_path(str(child)), None, directory=True, create=False, read_only_source=True)
            try:
                with self.assertRaises(OSError): ancestor.rename(replacement)
            finally: native.close(handle)
            self.assertTrue(child.is_dir()); self.assertFalse(replacement.exists())


class SyntheticOwnedObject:
    """Ordinary temp-file preparation model; grant/seal are recorded, never native ACL effects."""
    events = []
    created = []
    failure = None

    def __init__(self, path, directory, guard):
        self.path, self.directory, self.guard = str(path), directory, guard
        self.sealed, self.closed, self.content_sha256 = False, False, None
        if directory:
            Path(path).mkdir()
            self.file, self.writer = None, None
        else:
            import msvcrt
            self.file = Path(path).open("xb+")
            handle = msvcrt.get_osfhandle(self.file.fileno())
            self.writer = native.OwnedObject(handle, Path(path).name, None, self.path, False, USER, native._identity(handle), guard=guard)
        self.identity = Path(path).stat().st_ino
        type(self).created.append(self)
        type(self).events.append(("create", self.path))

    @classmethod
    def create_root(cls, path, user, *, guard, parent=None):
        guard()
        return cls(path, True, guard)

    def child(self, name, *, directory=False):
        self.guard()
        return type(self)(Path(self.path) / name, directory, self.guard)

    def write_stream(self, chunks, **kwargs):
        self.content_sha256 = self.writer.write_stream(chunks, **kwargs)
        type(self).events.append(("written", self.path))

    def seal(self):
        self.guard()
        if not self.directory and self.content_sha256 is None: raise Refused("incomplete synthetic copy")
        self.sealed = True
        type(self).events.append(("seal", self.path))

    def grant(self, package, *, mode):
        self.guard()
        if not self.sealed or package != PACKAGE or mode != "read": raise Refused("bad synthetic grant")
        type(self).events.append(("grant-model-only", self.path))
        if type(self).failure == "grant" and not self.directory: raise OSError("synthetic refused grant")
        return self.observe()

    def observe(self):
        self.guard()
        if self.closed: raise Refused("closed synthetic object")
        return {"path": self.path, "sealed": self.sealed, "identity": {"file_id": str(self.identity)},
                "sddl": "synthetic-no-ACL-effect", "content_sha256": self.content_sha256}

    def close(self):
        if self.file is not None: self.file.close()
        self.closed = True


def native_identity(path, directory):
    handle = native._open(native.native_path(str(path)), None, directory=directory, create=False, read_only_source=True)
    try: return native._identity(handle)
    finally: native.close(handle)


def preparation_fixture(folder):
    root = Path(folder).resolve(); trusted = root / "trusted"; trusted.mkdir()
    path = trusted / "probe.exe"; path.write_bytes(DATA)
    value = fixture(); value["input_root"] = str(trusted); value["input_identity"] = native_identity(trusted, True)
    value["output_root"] = str(root / ("image-" + value["generation"]))
    value["parent_identity"] = native_identity(root, True)
    value["files"][0]["source_identity"] = native_identity(path, False)
    return root, image.ImagePlan.read(value)


@unittest.skipUnless(os.name == "nt", "ordinary Windows preparation fixtures required")
class PreparationProtocolTests(unittest.TestCase):
    def setUp(self):
        SyntheticOwnedObject.events, SyntheticOwnedObject.created, SyntheticOwnedObject.failure = [], [], None

    def test_prepared_byte_receipt_follows_all_sealing_and_survives_lease_transfer(self):
        with tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
            root, plan = preparation_fixture(folder); revoked = [False]
            def guard():
                if revoked[0]: raise Refused("revoked fixture controller")
            fsync = image.os.fsync
            def verify_noninheritable_journal(fd):
                self.assertFalse(os.get_inheritable(fd))
                fsync(fd)
            with patch.object(image, "_create_image_root", SyntheticOwnedObject.create_root), patch.object(image.os, "fsync", verify_noninheritable_journal):
                result = image.prepare_image(plan, guard=guard)
                try:
                    self.assertEqual(Path(result.plan.output_root, "probe.exe").read_bytes(), DATA)
                    self.assertEqual(result.check(), result.observations)
                    # A prepared image retains its leases after prepare_image returns.
                    self.assertFalse(result.closed)
                    rows = [json.loads(line) for line in Path(plan.reservation).read_bytes().splitlines()]
                    self.assertEqual(rows[0]["plan_sha256"], plan.fingerprint)
                    self.assertEqual(rows[1]["phase"], "prepared_bytes")
                    self.assertIs(rows[1]["tool_runtime_qualified"], False)
                    events = [name for name, _ in SyntheticOwnedObject.events]
                    self.assertGreater(events.index("grant-model-only"), max(i for i, name in enumerate(events) if name == "seal"))
                    revoked[0] = True
                    with self.assertRaises(Refused): result.check()
                finally: result.close()
                self.assertTrue(all(obj.closed for obj in SyntheticOwnedObject.created))
                with self.assertRaises(Refused): result.check()
                revoked[0] = False
                with self.assertRaisesRegex(Refused, "reservation unavailable"):
                    image.prepare_image(plan, guard=guard)
            self.assertTrue(Path(plan.output_root).is_dir())
            self.assertEqual(Path(plan.output_root, "probe.exe").read_bytes(), DATA)

    def test_failed_initial_journal_durability_precedes_any_generation_effect(self):
        with tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
            root, plan = preparation_fixture(folder)
            with patch.object(image.os, "fsync", side_effect=OSError("synthetic fsync failure")), patch.object(image, "_create_image_root") as create:
                with self.assertRaises(OSError): image.prepare_image(plan, guard=lambda: None)
                create.assert_not_called()
            self.assertTrue(Path(plan.reservation).exists()); self.assertFalse(Path(plan.output_root).exists())
            with patch.object(image, "_create_image_root") as create:
                with self.assertRaises(Refused): image.prepare_image(plan, guard=lambda: None)
                create.assert_not_called()

    def test_corrupt_source_or_partial_grant_retains_without_destructive_rollback(self):
        for failure in ("source", "grant"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
                root, plan = preparation_fixture(folder)
                if failure == "source": Path(plan.input_root, "probe.exe").write_bytes(b"z" * len(DATA))
                SyntheticOwnedObject.events, SyntheticOwnedObject.created, SyntheticOwnedObject.failure = [], [], failure
                with patch.object(image, "_create_image_root", SyntheticOwnedObject.create_root):
                    with self.assertRaises((Refused, OSError)): image.prepare_image(plan, guard=lambda: None)
                self.assertTrue(all(obj.closed for obj in SyntheticOwnedObject.created))
                if failure == "source": self.assertFalse(any(name == "grant-model-only" for name, _ in SyntheticOwnedObject.events))
                self.assertTrue(Path(plan.output_root, "probe.exe").exists())
                retained = Path(plan.output_root, "probe.exe").read_bytes()
                rows = [json.loads(row) for row in Path(plan.reservation).read_bytes().splitlines()]
                self.assertEqual(rows[-1]["phase"], "failed_or_uncertain")
                with patch.object(image, "_create_image_root") as create:
                    with self.assertRaises(Refused): image.prepare_image(plan, guard=lambda: None)
                    create.assert_not_called()
                self.assertEqual(Path(plan.output_root, "probe.exe").read_bytes(), retained)

    def test_interrupted_write_closes_source_lease_even_with_retained_exception(self):
        with tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
            root, plan = preparation_fixture(folder); retained = None
            with patch.object(image, "_create_image_root", SyntheticOwnedObject.create_root), patch.object(native, "write_file", side_effect=OSError("synthetic write failure")):
                try: image.prepare_image(plan, guard=lambda: None)
                except OSError as error: retained = error
                else: self.fail("interrupted write unexpectedly prepared")
            self.assertIsNotNone(retained.__traceback__)
            self.assertTrue(all(obj.closed for obj in SyntheticOwnedObject.created))
            self.assertFalse(any(name == "grant-model-only" for name, _ in SyntheticOwnedObject.events))
            self.assertEqual(Path(plan.output_root, "probe.exe").read_bytes(), b"")
            # Retaining the exception must not retain the generator's read lock.
            with Path(plan.input_root, "probe.exe").open("r+b") as source: source.write(b"z")
            self.assertEqual(Path(plan.input_root, "probe.exe").read_bytes(), b"z" + DATA[1:])

    def test_expiry_during_final_journal_flush_cannot_return_prepared_image(self):
        with tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
            root, plan = preparation_fixture(folder); now, count = [100.0], [0]
            fsync = image.os.fsync
            def expire_on_prepared_flush(fd):
                fsync(fd); count[0] += 1
                if count[0] == 2: now[0] += plan.limits.seconds
            with patch.object(image.os, "fsync", expire_on_prepared_flush), patch.object(image, "_create_image_root", SyntheticOwnedObject.create_root):
                result = None
                try:
                    with self.assertRaisesRegex(Refused, "deadline"):
                        result = image.prepare_image(plan, guard=lambda: None, clock=lambda: now[0])
                finally:
                    if result is not None: result.close()
            self.assertTrue(all(obj.closed for obj in SyntheticOwnedObject.created))
            rows = [json.loads(row) for row in Path(plan.reservation).read_bytes().splitlines()]
            self.assertEqual(rows[-1]["phase"], "failed_or_uncertain")
            self.assertEqual(Path(plan.output_root, "probe.exe").read_bytes(), DATA)
            with patch.object(image, "_create_image_root") as create:
                with self.assertRaises(Refused): image.prepare_image(plan, guard=lambda: None)
                create.assert_not_called()

    def test_concurrent_generation_reservation_allows_only_one_preparation(self):
        with tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
            root, plan = preparation_fixture(folder)
            reserved, release = threading.Event(), threading.Event()
            results, errors = [], []
            def wait_after_intent(path, user, *, guard, parent):
                reserved.set()
                if not release.wait(3): raise RuntimeError("synthetic concurrent fixture timed out")
                return SyntheticOwnedObject.create_root(path, user, guard=guard)
            def first_writer():
                try: results.append(image.prepare_image(plan, guard=lambda: None))
                except BaseException as error: errors.append(error)
            with patch.object(image, "_create_image_root", wait_after_intent):
                thread = threading.Thread(target=first_writer); thread.start()
                try:
                    self.assertTrue(reserved.wait(3))
                    with self.assertRaisesRegex(Refused, "reservation unavailable"):
                        image.prepare_image(plan, guard=lambda: None)
                finally:
                    release.set(); thread.join(3)
                self.assertFalse(thread.is_alive())
                try:
                    self.assertEqual(errors, []); self.assertEqual(len(results), 1)
                    self.assertEqual(results[0].check(), results[0].observations)
                    self.assertEqual(len(Path(plan.reservation).read_bytes().splitlines()), 2)
                    self.assertEqual(Path(plan.output_root, "probe.exe").read_bytes(), DATA)
                finally:
                    for result in results: result.close()

    def test_actual_distinct_native_alias_parent_refuses_before_journal(self):
        with tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
            root, plan = preparation_fixture(folder)
            ordinary = root / "parent"; ordinary.mkdir()
            literal = root / "parent."
            extended = "\\\\?\\" + str(literal)
            os.mkdir(extended)
            try:
                self.assertNotEqual(native_identity(literal, True), native_identity(ordinary, True))
                value = plan.to_value(); value["output_root"] = str(literal / ("image-" + plan.generation))
                value["parent_identity"] = native_identity(literal, True)
                with patch.object(image, "SourceDirectory") as sources, patch("builtins.open") as opened, patch.object(image, "_create_image_root") as create:
                    with self.assertRaises(Refused): image.ImagePlan.read(value)
                    sources.assert_not_called(); opened.assert_not_called(); create.assert_not_called()
                self.assertEqual(os.listdir(ordinary), []); self.assertEqual(os.listdir(extended), [])
            finally:
                # Only remove our exact empty native spelling, never its DOS alias.
                self.assertEqual(literal.parent.resolve(), root)
                self.assertEqual(literal.name, "parent.")
                os.rmdir(extended)

    def test_real_short_name_equal_and_nested_input_aliases_refuse_before_intent(self):
        short_name = native.bind(native.K, "GetShortPathNameW", [W.LPCWSTR, W.LPWSTR, W.DWORD], W.DWORD)
        for nested in (False, True):
            with self.subTest(nested=nested), tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
                root, plan = preparation_fixture(folder)
                trusted = root / "Trusted input with spaces"
                self.assertEqual(trusted.parent.resolve(), root)
                Path(plan.input_root).rename(trusted)
                parent = trusted
                if nested: parent = trusted / "Nested output with spaces"; parent.mkdir()
                buffer = C.create_unicode_buffer(4096); count = short_name(str(parent), buffer, len(buffer))
                self.assertTrue(0 < count < len(buffer))
                if buffer.value.casefold() == str(parent).casefold(): self.skipTest("fixture volume did not supply an actual short-name alias")
                value = plan.to_value(); value["input_root"] = str(trusted)
                value["output_root"] = str(Path(buffer.value) / ("image-" + plan.generation))
                value["parent_identity"] = native_identity(parent, True)
                alias_plan = image.ImagePlan.read(value)
                with patch.object(image, "_reserve_journal") as reserve, patch.object(image, "_create_image_root") as create:
                    with self.assertRaisesRegex(Refused, "alias|overlap"): image.prepare_image(alias_plan, guard=lambda: None)
                    reserve.assert_not_called(); create.assert_not_called()
                self.assertFalse(Path(alias_plan.reservation).exists())
                self.assertEqual((trusted / "probe.exe").read_bytes(), DATA)

    def test_mapping_drift_at_relative_reservation_seam_keeps_exact_parent_and_refuses_image(self):
        with tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
            root, plan = preparation_fixture(folder)
            original_path, original_open = native.native_path, native._open
            changed, parent_handles = [False], []
            def mapping(path):
                actual = original_path(path)
                return actual.replace("HarddiskVolume", "HarddiskVolume9", 1) if changed[0] else actual
            def drift_after_guard(name, parent, **kwargs):
                if name.endswith(".intent.jsonl"):
                    self.assertIsNotNone(parent); parent_handles.append(parent.value)
                    self.assertFalse("\\" in name)
                    guard = kwargs["guard"]
                    def at_dispatch(): guard(); changed[0] = True
                    kwargs["guard"] = at_dispatch
                return original_open(name, parent, **kwargs)
            with patch.object(native, "native_path", mapping), patch.object(native, "_open", drift_after_guard), patch.object(image, "_create_image_root") as create:
                with self.assertRaisesRegex(Refused, "mapping"): image.prepare_image(plan, guard=lambda: None)
                create.assert_not_called()
            self.assertEqual(len(parent_handles), 1)
            rows = [json.loads(row) for row in Path(plan.reservation).read_bytes().splitlines()]
            self.assertEqual(rows[0]["plan_sha256"], plan.fingerprint)
            self.assertEqual(rows[-1]["phase"], "failed_or_uncertain")
            self.assertFalse(Path(plan.output_root).exists())
            with patch.object(image, "_create_image_root") as create:
                with self.assertRaisesRegex(Refused, "reservation unavailable"): image.prepare_image(plan, guard=lambda: None)
                create.assert_not_called()

    def test_journal_handle_adoption_failure_retains_empty_reservation_and_closes_handle(self):
        import msvcrt
        for phase in ("crt", "file_object"):
            with self.subTest(phase=phase), tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
                root, plan = preparation_fixture(folder)
                owner, name = (msvcrt, "open_osfhandle") if phase == "crt" else (image.os, "fdopen")
                with patch.object(owner, name, side_effect=OSError("synthetic journal adoption failure")), patch.object(image, "_create_image_root") as create:
                    with self.assertRaises(OSError): image.prepare_image(plan, guard=lambda: None)
                    create.assert_not_called()
                # This read would fail while the exclusive native handle leaked.
                self.assertEqual(Path(plan.reservation).read_bytes(), b"")
                with patch.object(image, "_create_image_root") as create:
                    with self.assertRaisesRegex(Refused, "reservation unavailable"): image.prepare_image(plan, guard=lambda: None)
                    create.assert_not_called()

    def test_image_root_create_and_seal_keep_the_exact_parent_handle(self):
        from unittest.mock import Mock
        parent = SimpleNamespace(path=r"C:\owned", handle=777, closed=False, check=Mock())
        identity = {"volume": 1, "file_id": "3" * 32}
        with patch.object(native, "_open", return_value=123) as opened, patch.object(native, "_identity", return_value=identity), patch.object(native, "close") as closed, patch.object(native, "set_security") as grant:
            obj = image._create_image_root(r"C:\owned\image", USER, guard=lambda: None, parent=parent)
            self.assertIs(obj.parent, parent); self.assertEqual(obj.name, "image")
            obj.seal(); obj.close()
            self.assertEqual(len(opened.call_args_list), 3)
            for call in opened.call_args_list: self.assertEqual(call.args, ("image", 777))
            self.assertTrue(opened.call_args_list[0].kwargs["create"])
            self.assertEqual([call.kwargs.get("share") for call in opened.call_args_list[1:]], [3, 1])
            grant.assert_not_called(); self.assertNotIn(777, [call.args[0] for call in closed.call_args_list])

    def test_unavailable_or_unbound_canonical_name_refuses_before_reservation(self):
        with tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
            root, plan = preparation_fixture(folder)
            for observed in (Refused("unavailable normalized name"), r"\Device\HarddiskVolume3\foreign"):
                with self.subTest(observed=observed), patch.object(image, "_normalized_nt_name", side_effect=observed if isinstance(observed, Exception) else None, return_value=observed), patch.object(image, "_reserve_journal") as reserve:
                    with self.assertRaises(Refused): image.prepare_image(plan, guard=lambda: None)
                    reserve.assert_not_called()
            self.assertFalse(Path(plan.reservation).exists())

    def test_changed_protected_root_or_parent_refuses_before_reservation(self):
        for field in ("input_identity", "parent_identity"):
            with self.subTest(field=field), tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
                root, plan = preparation_fixture(folder); value = plan.to_value(); value[field]["file_id"] = "f" * 32
                plan = image.ImagePlan.read(value)
                with patch.object(image, "_create_image_root") as create:
                    with self.assertRaises(Refused): image.prepare_image(plan, guard=lambda: None)
                    create.assert_not_called()
                self.assertFalse(Path(plan.reservation).exists())

    def test_actual_abrupt_process_exit_after_intent_or_partial_copy_cannot_replay(self):
        for phase in ("intent", "partial"):
            with self.subTest(phase=phase), tempfile.TemporaryDirectory(prefix="aide-h2-synthetic-") as folder:
                root, plan = preparation_fixture(folder); manifest = root / "synthetic-plan.json"
                manifest.write_text(json.dumps(plan.to_value()), encoding="utf-8")
                command = [sys.executable, "-B", str(Path(__file__).resolve()), "--crash-fixture", str(manifest), phase]
                run = subprocess.run(command, capture_output=True, timeout=10)
                self.assertEqual((run.returncode, run.stdout, run.stderr), (73, b"", b""))
                rows = Path(plan.reservation).read_bytes().splitlines()
                self.assertEqual(len(rows), 1); self.assertEqual(json.loads(rows[0])["schema"], "aide.host.image-intent.v1")
                output = Path(plan.output_root) / "probe.exe"
                retained = output.read_bytes() if phase == "partial" else None
                if phase == "partial": self.assertEqual(retained, DATA[:image.CHUNK])
                else: self.assertFalse(Path(plan.output_root).exists())
                with patch.object(image, "_create_image_root") as create:
                    with self.assertRaises(Refused): image.prepare_image(plan, guard=lambda: None)
                    create.assert_not_called()
                if phase == "partial": self.assertEqual(output.read_bytes(), retained)


def crash_fixture(manifest, phase):
    # Only an explicitly synthetic, contained test directory can use this entry.
    path = Path(manifest).resolve(); root = path.parent
    if not root.name.startswith("aide-h2-synthetic-") or root.parent != Path(tempfile.gettempdir()).resolve():
        raise RuntimeError("owned synthetic crash fixture required")
    plan = image.ImagePlan.read(json.loads(path.read_bytes()))
    if Path(plan.output_root).parent.resolve() != root or Path(plan.input_root).parent.resolve() != root:
        raise RuntimeError("synthetic fixture escaped its owned parent")
    original = image.SourceDirectory.chunks
    def interrupted_chunks(self, entry):
        stream = original(self, entry)
        yield next(stream)
        os._exit(73)
    if phase == "intent":
        with patch.object(image, "_create_image_root", side_effect=lambda *args, **kwargs: os._exit(73)):
            image.prepare_image(plan, guard=lambda: None)
    elif phase == "partial":
        with patch.object(image, "_create_image_root", SyntheticOwnedObject.create_root), patch.object(image.SourceDirectory, "chunks", interrupted_chunks):
            image.prepare_image(plan, guard=lambda: None)
    else: raise RuntimeError("unknown synthetic crash phase")


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--crash-fixture": crash_fixture(sys.argv[2], sys.argv[3])
    else: unittest.main()
