"""Synthetic dependency metadata fixtures; no inspected binary is loaded."""
from dataclasses import FrozenInstanceError
import hashlib
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker import windows_pe as pe
from core.runtime.continuous_worker.state import Refused

PE, OPTIONAL, SECTION = 0x80, 0x98, 0x188
HEADERS, RAW, RVA = 0x400, 0x3000, 0x1000


def write(data, offset, pattern, *values):
    struct.pack_into(pattern, data, offset, *values)


def put(data, rva, value):
    offset = HEADERS + rva - RVA
    data[offset:offset + len(value)] = value


def fixture(*, imports=("KERNEL32.dll",), delayed=(), forwarders=(), is_dll=False):
    data = bytearray(HEADERS + RAW); data[:2] = b"MZ"; write(data, 60, "<I", PE)
    data[PE:PE + 4] = b"PE\0\0"; write(data, PE + 4, "<HHIIIHH", 0x8664, 1, 0, 0, 0, 240, 2 | (0x2000 if is_dll else 0))
    write(data, OPTIONAL, "<H", 0x20b); write(data, OPTIONAL + 32, "<II", 0x1000, 0x200)
    write(data, OPTIONAL + 56, "<II", 0x5000, HEADERS); write(data, OPTIONAL + 108, "<I", 16)
    data[SECTION:SECTION + 8] = b".rdata\0\0"; write(data, SECTION + 8, "<IIII", RAW, RVA, RAW, HEADERS)
    if imports:
        write(data, OPTIONAL + 112 + 8, "<II", 0x1000, (len(imports) + 1) * 20)
        for i, name in enumerate(imports):
            put(data, 0x1000 + i * 20, struct.pack("<IIIII", 0x2900 + 16 * i, 0, 0, 0x2000 + 64 * i, 0x2800 + 16 * i))
            put(data, 0x2000 + 64 * i, name.encode("ascii") + b"\0")
    if delayed:
        write(data, OPTIONAL + 112 + 13 * 8, "<II", 0x1200, (len(delayed) + 1) * 32)
        for i, name in enumerate(delayed):
            put(data, 0x1200 + i * 32, struct.pack("<IIIIIIII", 1, 0x2400 + 64 * i, 0, 0x2a00 + 16 * i, 0x2b00 + 16 * i, 0, 0, 0))
            put(data, 0x2400 + 64 * i, name.encode("ascii") + b"\0")
    if forwarders:
        count = len(forwarders); write(data, OPTIONAL + 112, "<II", 0x1400, 0x400)
        put(data, 0x1400, struct.pack("<IIHHIIIIIII", 0, 0, 0, 0, 0x1f00, 1, count, count, 0x1440, 0x1480, 0x14c0))
        put(data, 0x1f00, b"fixture.dll\0")
        for i, target in enumerate(forwarders):
            put(data, 0x1440 + 4 * i, struct.pack("<I", 0x1500 + i * 64))
            put(data, 0x1480 + 4 * i, struct.pack("<I", 0x1a00 + i * 32))
            put(data, 0x14c0 + 2 * i, struct.pack("<H", i))
            put(data, 0x1500 + i * 64, target.encode("ascii") + b"\0")
            put(data, 0x1a00 + i * 32, ("Export" + str(i)).encode() + b"\0")
    return data


class PeMetadataTests(unittest.TestCase):
    def refuse(self, value):
        with self.assertRaises(Refused): pe.read_pe(bytes(value) if isinstance(value, bytearray) else value)

    def test_exact_immutable_dependency_union_and_forwarder_targets(self):
        data = fixture(imports=("python314.dll", "KERNEL32.dll"), delayed=("VERSION.dll",), forwarders=("NTDLL.RtlExample", "KERNELBASE.#27"), is_dll=True)
        immutable = bytes(data); result = pe.read_pe(immutable)
        self.assertEqual(result.sha256, hashlib.sha256(immutable).hexdigest()); self.assertEqual(result.machine, "amd64"); self.assertTrue(result.is_dll)
        self.assertEqual(result.imports, ("kernel32.dll", "python314.dll")); self.assertEqual(result.delay_imports, ("version.dll",))
        self.assertEqual(result.forwarders, (pe.Forwarder("kernelbase.dll", "#27"), pe.Forwarder("ntdll.dll", "RtlExample")))
        self.assertEqual(result.dependencies, ("kernel32.dll", "kernelbase.dll", "ntdll.dll", "python314.dll", "version.dll"))
        data[0] = 0; self.assertEqual(result.sha256, hashlib.sha256(immutable).hexdigest())
        with self.assertRaises(FrozenInstanceError): result.machine = "arm64"
        empty = pe.read_pe(bytes(fixture(imports=()))); self.assertEqual(empty.dependencies, ()); self.assertFalse(empty.is_dll)

    def test_immutable_byte_and_header_limits(self):
        for value in (None, "MZ", bytearray(fixture()), b"MZ", b"x" * 64, b"MZ" + b"\0" * pe.MAX_PE_BYTES):
            with self.subTest(kind=type(value).__name__), self.assertRaises(Refused): pe.read_pe(value)
        mutations = [(60, "<I", 0xffffffff), (PE + 4, "<H", 0x14c), (PE + 6, "<H", 0), (PE + 6, "<H", 97),
                     (PE + 20, "<H", 111), (PE + 20, "<H", 248), (PE + 22, "<H", 0), (OPTIONAL, "<H", 0x10b),
                     (OPTIONAL + 56, "<I", pe.MAX_IMAGE_BYTES + 1), (OPTIONAL + 60, "<I", 0x100), (OPTIONAL + 108, "<I", 17)]
        for offset, pattern, value in mutations:
            with self.subTest(offset=offset, value=value): data = fixture(); write(data, offset, pattern, value); self.refuse(data)
        data = fixture(); data[PE:PE + 4] = b"NONE"; self.refuse(data)

    def test_truncation_and_raw_virtual_overlap_refuse(self):
        original = fixture(forwarders=("NTDLL.Target",))
        for end in (63, PE + 3, OPTIONAL + 111, SECTION + 39, HEADERS, len(original) - 1):
            with self.subTest(end=end): self.refuse(original[:end])
        for field, value in ((SECTION + 12, 0x100), (SECTION + 12, 0xfffffff0), (SECTION + 16, 0xffffffff), (SECTION + 20, HEADERS - 1)):
            data = fixture(); write(data, field, "<I", value); self.refuse(data)
        for overlap in ("virtual", "raw"):
            data = fixture(); write(data, PE + 6, "<H", 2)
            write(data, SECTION + 40 + 8, "<IIII", 0x100, 0x1800 if overlap == "virtual" else 0x4000, 0x100, 0x500)
            self.refuse(data)

    def test_import_names_bounds_duplicates_and_tables(self):
        for names in (("KERNEL32.dll", "kernel32.DLL"), ("../foreign.dll",), ("C:foreign.dll",), ("CON.dll",)):
            with self.subTest(names=names): self.refuse(fixture(imports=names))
        for name in (b"", b"not-a-dll", b"foreign\x00.dll", b"bad\x80.dll", b"bad name.dll", b"x" * 260):
            data = fixture(); put(data, 0x2000, name + b"\0"); self.refuse(data)
        for field, value in ((HEADERS + 12, 0xffffffff), (HEADERS + 16, 0), (HEADERS + 16, 0x4ff0), (HEADERS + 4, 1),
                             (OPTIONAL + 112 + 8, 0), (OPTIONAL + 112 + 12, 0), (OPTIONAL + 112 + 12, 19),
                             (OPTIONAL + 112 + 12, 20), (OPTIONAL + 112 + 12, 20 * (pe.MAX_IMPORTS + 2))):
            with self.subTest(field=field, value=value): data = fixture(); write(data, field, "<I", value); self.refuse(data)
        data = fixture(); write(data, OPTIONAL + 112 + 11 * 8, "<II", 0x2d00, 8); self.refuse(data)

    def test_delay_imports_require_unbound_rva_descriptors(self):
        for field, value in ((0, 0), (0, 2), (4, 0x4ff0), (12, 0), (16, 0x4ff0), (20, 1)):
            data = fixture(delayed=("VERSION.dll",)); write(data, HEADERS + 0x200 + field, "<I", value); self.refuse(data)
        self.refuse(fixture(delayed=("VERSION.dll", "version.DLL")))
        data = fixture(delayed=("VERSION.dll",)); write(data, OPTIONAL + 112 + 13 * 8 + 4, "<I", 32); self.refuse(data)

    def test_forwarder_names_extents_and_export_counts(self):
        for target in ("NTDLL", "../foreign.Target", "NTDLL.dll.Target", "NTDLL.#0", "NTDLL.#", "NTDLL.Target/escape", "NTDLL.#99999999999"):
            with self.subTest(target=target): self.refuse(fixture(forwarders=(target,)))
        for offset, value in ((HEADERS + 0x400 + 20, pe.MAX_EXPORTS + 1), (HEADERS + 0x400 + 24, 2),
                              (HEADERS + 0x400 + 28, 0x4ff0), (HEADERS + 0x440, 0x5000), (HEADERS + 0x480, 0x4ff0),
                              (OPTIONAL + 112 + 4, 39)):
            data = fixture(forwarders=("NTDLL.Target",)); write(data, offset, "<I", value); self.refuse(data)
        data = fixture(forwarders=("NTDLL.Target",)); write(data, HEADERS + 0x4c0, "<H", 1); self.refuse(data)
        data = fixture(forwarders=("NTDLL.Target",)); write(data, HEADERS + 0x440, "<I", 0x17fb); put(data, 0x17fb, b"NTDLL.Target\0"); self.refuse(data)

    def test_zero_export_holes_and_nonforwarded_targets_add_no_dependencies(self):
        data = fixture(imports=(), forwarders=("NTDLL.Target", "KERNEL32.Other"))
        put(data, 0x1440, struct.pack("<II", 0, 0x3000))
        result = pe.read_pe(bytes(data)); self.assertEqual(result.forwarders, ()); self.assertEqual(result.dependencies, ())


def optional_delay_fixture(*, virtual_iat=False, unload=False):
    data = fixture(imports=(), delayed=("VERSION.dll",))
    iat = 0x4100 if virtual_iat else 0x2a00
    module = 0x4180 if virtual_iat else 0x2d80
    if virtual_iat: write(data, SECTION + 8, "<I", 0x4000)
    put(data, 0x1200, struct.pack("<8I", 1, 0x2400, module, iat, 0x2b00, 0x2c00, 0x2d00 if unload else 0, 0))
    put(data, 0x2b00, struct.pack("<3Q", 0x2e00, (1 << 63) | 7, 0))
    put(data, 0x2e00, b"\0\0ExampleImport\0")
    original_iat = struct.pack("<3Q", 0, 0, 0) if virtual_iat else struct.pack("<3Q", 0x180003000, 0x180003100, 0)
    if not virtual_iat: put(data, iat, original_iat)
    # Timestamp0 means these optional bound values are inert metadata; they are
    # neither loader targets nor file offsets and must never be dereferenced.
    put(data, 0x2c00, struct.pack("<3Q", 0x7ff000001000, 0x7ff000002000, 0))
    if unload: put(data, 0x2d00, original_iat)
    return data


class OptionalDelayMetadataTests(unittest.TestCase):
    def test_timestamp_zero_optional_table_and_unload_copy_are_supported_without_address_following(self):
        for unload in (False, True):
            with self.subTest(unload=unload):
                data = optional_delay_fixture(unload=unload); result = pe.read_pe(bytes(data))
                self.assertEqual(result.delay_imports, ("version.dll",)); self.assertEqual(result.dependencies, ("version.dll",))
                self.assertEqual(result.sha256, hashlib.sha256(data).hexdigest())

    def test_virtual_zero_filled_iat_and_handle_storage_are_mapped_metadata_only(self):
        data = optional_delay_fixture(virtual_iat=True, unload=True)
        self.assertEqual(pe.read_pe(bytes(data)).delay_imports, ("version.dll",))
        reader = pe._Reader(bytes(data))
        with self.assertRaises(Refused): reader.offset(0x4100, 24)
        self.assertEqual(reader.image_bytes(0x4100, 24), b"\0" * 24)
        # The initialized/zero-filled boundary may be crossed by an IAT span.
        put(data, 0x1200 + 12, struct.pack("<I", 0x3ff8)); put(data, 0x3ff8, struct.pack("<Q", 0))
        self.assertEqual(pe.read_pe(bytes(data)).delay_imports, ("version.dll",))

    def test_nonzero_timestamps_old_attributes_and_incomplete_optional_spans_refuse(self):
        for field, value in ((0, 0), (0, 2), (8, 0x5000), (12, 0), (12, 0x4ff0), (16, 0), (16, 0x4ff0),
                             (20, 0x3ff8), (20, 0x4100), (24, 0x3ff8), (28, 1), (28, 0xffffffff)):
            data = optional_delay_fixture(virtual_iat=True); put(data, 0x1200 + field, struct.pack("<I", value))
            with self.subTest(field=field, value=value), self.assertRaises(Refused): pe.read_pe(bytes(data))
        data = optional_delay_fixture(); put(data, 0x1200 + 20, struct.pack("<I", 0)); put(data, 0x1200 + 28, struct.pack("<I", 1))
        with self.assertRaises(Refused): pe.read_pe(bytes(data))

    def test_lookup_names_ordinals_terminators_and_optional_terminators_are_bounded(self):
        for kind in ("wide_name_rva", "name_extent", "name_unterminated", "ordinal_reserved", "lookup_terminator", "iat_terminator", "bound_terminator", "unload_terminator"):
            data = optional_delay_fixture(unload=True)
            if kind == "wide_name_rva": put(data, 0x2b00, struct.pack("<Q", 1 << 40))
            if kind == "name_extent": put(data, 0x2b00, struct.pack("<Q", 0x4fff))
            if kind == "name_unterminated": put(data, 0x2e00, b"\0\0" + b"x" * 512)
            if kind == "ordinal_reserved": put(data, 0x2b08, struct.pack("<Q", (1 << 63) | (1 << 20) | 7))
            if kind == "lookup_terminator":
                put(data, 0x1200 + 16, struct.pack("<I", 0x3ff8)); put(data, 0x3ff8, struct.pack("<Q", 0x2e00))
            if kind == "iat_terminator": put(data, 0x2a10, struct.pack("<Q", 1))
            if kind == "bound_terminator": put(data, 0x2c10, struct.pack("<Q", 1))
            if kind == "unload_terminator": put(data, 0x2d10, struct.pack("<Q", 1))
            with self.subTest(kind=kind), self.assertRaises(Refused): pe.read_pe(bytes(data))

    def test_unload_table_must_represent_the_same_original_iat_bytes(self):
        for virtual in (False, True):
            data = optional_delay_fixture(virtual_iat=virtual, unload=True); put(data, 0x2d00, struct.pack("<Q", 0x1234))
            with self.subTest(virtual=virtual), self.assertRaises(Refused): pe.read_pe(bytes(data))

    def test_delay_symbol_budget_is_aggregate_and_refuses_before_unbounded_traversal(self):
        data = optional_delay_fixture()
        with patch.object(pe, "MAX_DELAY_SYMBOLS", 1), self.assertRaises(Refused): pe.read_pe(bytes(data))
        # Two descriptors reusing a small lookup still consume separate work.
        write(data, OPTIONAL + 112 + 13 * 8, "<II", 0x1200, 96)
        put(data, 0x1220, struct.pack("<8I", 1, 0x2480, 0x2d80, 0x2a00, 0x2b00, 0, 0, 0))
        put(data, 0x2480, b"KERNEL32.dll\0")
        with patch.object(pe, "MAX_DELAY_SYMBOLS", 3), self.assertRaises(Refused): pe.read_pe(bytes(data))


if __name__ == "__main__": unittest.main()
