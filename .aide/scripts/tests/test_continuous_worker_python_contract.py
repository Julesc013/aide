"""Synthetic named PE closure; no actual DLL load or system ownership assertion."""
import copy
from dataclasses import replace
import hashlib
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker import windows_python_contract as contract
from core.runtime.continuous_worker.state import Refused
from test_continuous_worker_windows_pe import fixture as pe_fixture


def digest(data): return hashlib.sha256(data).hexdigest()
def identity(number): return {"volume": 42, "file_id": f"{number:032x}"}
def dll(**kwargs): return bytes(pe_fixture(is_dll=True, **kwargs))
API = "api-ms-win-crt-runtime-l1-1-0.dll"


def fixture():
    private = {"python.exe": bytes(pe_fixture(imports=("python314.dll", "vcruntime140.dll"))),
               "python314.dll": dll(imports=(API,), delayed=("KERNEL32.dll",)),
               "vcruntime140.dll": dll(imports=("KERNEL32.dll",))}
    system = {"kernel32.dll": dll(imports=(), forwarders=("NTDLL.Example",)),
              "ntdll.dll": dll(imports=()), "ucrtbase.dll": dll(imports=("kernel32.dll",))}
    value = {"schema": "aide.host.python-system.v1", "os_build": "10.0.26100.100",
             "native_root": r"\Device\HarddiskVolume6\Windows\System32", "root_identity": identity(1),
             "modules": [{"name": name, "sha256": digest(data), "identity": identity(i + 2)} for i, (name, data) in enumerate(system.items())],
             "api_sets": [{"name": API, "hosts": ["ucrtbase.dll"]}]}
    return value, {name: digest(data) for name, data in private.items()}, private, system


def validate(value, pins, private, system):
    return contract.validate_python_recipe(contract.SystemContract.read(value), pins, private, system)


def update_system(value, system, name, data):
    system[name] = data
    next(row for row in value["modules"] if row["name"] == name)["sha256"] = digest(data)


class PythonContractTests(unittest.TestCase):
    def test_exact_recursive_api_delay_forwarded_closure_is_deterministic_unqualified_data(self):
        value, pins, private, system = fixture(); first = validate(value, pins, private, system)
        value["modules"].reverse(); value["api_sets"].reverse()
        second = validate(value, dict(reversed(list(pins.items()))), dict(reversed(list(private.items()))), system)
        self.assertEqual(first, second)
        self.assertEqual(set(first.bootstrap_modules), set(private) | set(system))
        self.assertEqual(first.inspected_bytes, sum(map(len, private.values())) + sum(map(len, system.values())))
        rows = {(row.importer, row.requested): row.hosts for row in first.edges}
        self.assertEqual(rows[("python314.dll", API)], ("ucrtbase.dll",))
        self.assertEqual(rows[("kernel32.dll", "ntdll.dll")], ("ntdll.dll",))
        self.assertEqual(rows[("python314.dll", "kernel32.dll")], ("kernel32.dll",))
        self.assertFalse(first.manifest()["loader_qualified"])
        self.assertFalse(first.manifest()["system_ownership_qualified"])

    def test_root_build_identity_and_schema_are_literal_bounded_data(self):
        for key, bad in (("native_root", r"C:\Windows\System32"), ("native_root", r"\Device\HarddiskVolume6\Windows\System32\.."),
                         ("native_root", r"\Device\HarddiskVolume6\Windows\System32."), ("native_root", None),
                         ("os_build", "current"), ("os_build", "10.0.26100"), ("os_build", True),
                         ("root_identity", identity(0)), ("root_identity", {"volume": True, "file_id": "1" * 32}),
                         ("schema", "aide.host.python-system.v2")):
            value, _, _, _ = fixture(); value[key] = bad
            with self.subTest(key=key, bad=bad), self.assertRaises(Refused): contract.SystemContract.read(value)
        value, _, _, _ = fixture(); value["ambient_exemption"] = "System32"
        with self.assertRaises(Refused): contract.SystemContract.read(value)
        for invalid in (None, [], "", True):
            with self.assertRaises(Refused): contract.SystemContract.read(invalid)

    def test_duplicate_alias_device_volume_and_unnamed_system_declarations_refuse(self):
        for case in ("duplicate", "case", "device", "escape", "private", "api_physical", "identity", "volume", "extra", "hash", "count"):
            value, _, _, _ = fixture(); row = value["modules"][0]
            if case == "duplicate": value["modules"].append(dict(row))
            if case == "case": row["name"] = row["name"].upper()
            if case == "device": row["name"] = "con.dll"
            if case == "escape": row["name"] = "../kernel32.dll"
            if case == "private": row["name"] = "python314.dll"
            if case == "api_physical": row["name"] = API
            if case == "identity": row["identity"] = value["root_identity"]
            if case == "volume": row["identity"]["volume"] = 43
            if case == "extra": row["path"] = "arbitrary"
            if case == "hash": row["sha256"] = "X" * 64
            if case == "count": value["modules"] *= 22
            with self.subTest(case=case), self.assertRaises(Refused): contract.SystemContract.read(value)

    def test_api_sets_require_exact_distinct_physical_hosts_without_wildcards_or_private_fallback(self):
        for case in ("wildcard", "ordinary", "missing", "private", "recursive", "duplicate_host", "case", "empty", "host_count", "duplicate", "count"):
            value, _, _, _ = fixture(); row = value["api_sets"][0]
            if case == "wildcard": row["name"] = "api-ms-win-*.dll"
            if case == "ordinary": row["name"] = "ordinary.dll"
            if case == "missing": row["hosts"] = ["unknown.dll"]
            if case == "private": row["hosts"] = ["python314.dll"]
            if case == "recursive": row["hosts"] = [API]
            if case == "duplicate_host": row["hosts"] *= 2
            if case == "case": row["hosts"] = ["UCRTBASE.dll"]
            if case == "empty": row["hosts"] = []
            if case == "host_count": row["hosts"] *= 9
            if case == "duplicate": value["api_sets"].append(dict(row))
            if case == "count": value["api_sets"] *= contract.MAX_API_SETS + 1
            with self.subTest(case=case), self.assertRaises(Refused): contract.SystemContract.read(value)

    def test_unknown_normal_delayed_and_forwarded_dependencies_refuse(self):
        for mode in ("imports", "delayed", "forwarders"):
            for module in ("python314.dll", "ntdll.dll"):
                value, pins, private, system = fixture()
                args = {"imports": (), mode: ("evil.Target" if mode == "forwarders" else "evil.dll",)}
                data = dll(**args)
                if module in private: private[module] = data; pins[module] = digest(data)
                else: update_system(value, system, module, data)
                with self.subTest(mode=mode, module=module), self.assertRaises(Refused): validate(value, pins, private, system)
        value, pins, private, system = fixture(); value["api_sets"] = []
        with self.assertRaises(Refused): validate(value, pins, private, system)

    def test_named_system_cannot_call_private_python_and_private_cannot_bypass_direct_policy(self):
        value, pins, private, system = fixture()
        update_system(value, system, "ntdll.dll", dll(imports=("python314.dll",)))
        with self.assertRaises(Refused): validate(value, pins, private, system)
        value, pins, private, system = fixture(); private["python314.dll"] = dll(imports=("ntdll.dll",)); pins["python314.dll"] = digest(private["python314.dll"])
        with self.assertRaises(Refused): validate(value, pins, private, system)

    def test_finite_physical_cycles_and_explicit_unreachable_system_inventory(self):
        value, pins, private, system = fixture()
        update_system(value, system, "ntdll.dll", dll(imports=("kernel32.dll",)))
        result = validate(value, pins, private, system)
        self.assertEqual(len(result.bootstrap_modules), 6)
        extra = dll(imports=()); system["extra.dll"] = extra
        value["modules"].append({"name": "extra.dll", "sha256": digest(extra), "identity": identity(20)})
        result = validate(value, pins, private, system)
        self.assertIn("extra.dll", dict(result.modules)); self.assertNotIn("extra.dll", result.bootstrap_modules)
        private["python.exe"] = bytes(pe_fixture(imports=("python314.dll",))); pins["python.exe"] = digest(private["python.exe"])
        with self.assertRaises(Refused): validate(value, pins, private, system)

    def test_input_sets_hashes_byte_types_and_total_bound_refuse_before_parser(self):
        for kind in ("private_missing", "private_extra", "pin_missing", "pin_invalid", "system_missing", "system_extra", "mutable", "digest", "small", "total"):
            value, pins, private, system = fixture()
            if kind == "private_missing": del private["python.exe"]
            if kind == "private_extra": private["python3.dll"] = dll()
            if kind == "pin_missing": del pins["python.exe"]
            if kind == "pin_invalid": pins["python.exe"] = True
            if kind == "system_missing": del system["ntdll.dll"]
            if kind == "system_extra": system["unknown.dll"] = dll()
            if kind == "mutable": private["python.exe"] = bytearray(private["python.exe"])
            if kind == "digest": system["ntdll.dll"] = b"x" * len(system["ntdll.dll"])
            if kind == "small": system["ntdll.dll"] = b"x"
            with self.subTest(kind=kind), patch.object(contract, "read_pe") as parser, patch.object(contract, "MAX_TOTAL_BYTES", 100 if kind == "total" else contract.MAX_TOTAL_BYTES):
                with self.assertRaises(Refused): validate(value, pins, private, system)
                parser.assert_not_called()

    def test_dll_characteristics_and_malformed_pe_refuse_despite_matching_hashes(self):
        for name in ("python.exe", "python314.dll", "ntdll.dll"):
            value, pins, private, system = fixture()
            data = bytes(pe_fixture(imports=(), is_dll=name == "python.exe"))
            if name in private: private[name] = data; pins[name] = digest(data)
            else: update_system(value, system, name, data)
            with self.subTest(name=name), self.assertRaises(Refused): validate(value, pins, private, system)
        value, pins, private, system = fixture(); update_system(value, system, "ntdll.dll", b"x" * 1024)
        with self.assertRaises(Refused): validate(value, pins, private, system)

    def test_frozen_contract_and_inputs_cannot_change_after_validation(self):
        value, pins, private, system = fixture(); admitted = contract.SystemContract.read(value)
        value["modules"][0]["sha256"] = "0" * 64
        for bad in (replace(admitted, modules=()), replace(admitted, fingerprint="0" * 64), replace(admitted, root_identity=())):
            with patch.object(contract, "read_pe") as parser:
                with self.assertRaises(Refused): contract.validate_python_recipe(bad, pins, private, system)
                parser.assert_not_called()
        expected = contract.validate_python_recipe(admitted, pins, private, system); original = contract.read_pe
        def mutate(data):
            private["python.exe"] = b"x"; system.clear(); pins.clear()
            return original(data)
        with patch.object(contract, "read_pe", mutate):
            actual = contract.validate_python_recipe(admitted, pins, private, system)
        self.assertEqual(actual, expected)

    def test_edge_limit_refuses_finite_metadata_without_unbounded_traversal(self):
        value, pins, private, system = fixture()
        with patch.object(contract, "MAX_EDGES", 1), self.assertRaises(Refused): validate(value, pins, private, system)


if __name__ == "__main__": unittest.main()
