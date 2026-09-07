"""H1 source refusals. Actual profile/DACL probe requires a separate reviewed manifest."""
import ctypes as C
import copy
from ctypes import wintypes as W
import hashlib
import importlib.util
import json
import socket
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker.state import Refused
from core.runtime.continuous_worker import windows_security as security
from core.runtime.continuous_worker import windows_security_objects as objects

USER = "S-1-5-21-11-22-33-1001"
PACKAGE = "S-1-15-2-11-22-33-44-55-66-77"
MONIKER = "aide.cw.h1." + "a" * 32


def observed():
    return {"appcontainer": 1, "package_sid": PACKAGE, "capability_count": 0,
            "integrity_sid": "S-1-16-4096", "user_sid": USER, "elevated": 0,
            "ui_access": 0, "in_owned_job": True}


class WindowsSecuritySourceTests(unittest.TestCase):
    def test_exact_actual_child_identity_is_required_before_resume(self):
        self.assertEqual(security.verify_observation(observed(), PACKAGE, USER), observed())
        for field, bad in (("appcontainer", 0), ("appcontainer", True), ("package_sid", "S-1-15-2-999"),
                           ("capability_count", 1), ("capability_count", False),
                           ("integrity_sid", "S-1-16-8192"), ("user_sid", "S-1-5-18"),
                           ("elevated", 1), ("ui_access", 1), ("in_owned_job", False), ("in_owned_job", 1)):
            value = observed(); value[field] = bad
            with self.subTest(field=field, value=bad), self.assertRaises(Refused):
                security.verify_observation(value, PACKAGE, USER)
        for field in observed():
            value = observed(); del value[field]
            with self.subTest(missing=field), self.assertRaises(Refused):
                security.verify_observation(value, PACKAGE, USER)

    def test_descriptor_grants_only_specific_package_and_never_descriptor_control(self):
        private = objects.descriptor(USER, directory=True)
        self.assertNotIn(PACKAGE, private)
        self.assertTrue(private.startswith("D:P"))
        self.assertTrue(private.endswith("S:(ML;;NW;;;ME)"))
        for mode, rights in (("read", 0x1200a9), ("modify", 0x1301bf)):
            result = objects.descriptor(USER, PACKAGE, mode=mode, directory=True)
            self.assertIn(f"0x{rights:x};;;{PACKAGE}", result)
            self.assertFalse(rights & (0x40000 | 0x80000))  # WRITE_DAC / WRITE_OWNER.
            self.assertNotIn(";;;AC)", result)
            self.assertNotIn("S-1-15-2-1)", result)
        for bad in (None, "S-1-5-18)(A;;FA;;;WD", "S-1-", "S-1-15-2-1", "S-1-5-18", 7):
            with self.subTest(bad=bad), self.assertRaises(Refused):
                objects.descriptor(USER, bad, mode="modify")

    def test_spec_refuses_nonliteral_profile_or_unprotected_journal_shape(self):
        for moniker in ("existing-profile", "aide.cw.h1." + "A" * 32, None, MONIKER + "/x"):
            with self.subTest(moniker=moniker), self.assertRaises(Refused):
                security.ProfileSpec(moniker, r"C:\owned\profile-reservation.jsonl").validate()
        for path in ("profile-reservation.jsonl", r"C:\owned\other.json", None):
            with self.subTest(path=path), self.assertRaises(Refused):
                security.ProfileSpec(MONIKER, path).validate()

    def test_existing_reservation_preserves_foreign_bytes_without_profile_effect(self):
        with tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
            path = Path(folder) / "profile-reservation.jsonl"
            path.write_bytes(b"foreign reservation")
            spec = security.ProfileSpec(MONIKER, str(path))
            with patch.object(security, "expected_package_sid", return_value=PACKAGE), patch.object(security, "create_profile") as create:
                with self.assertRaises(FileExistsError):
                    security.PreparedProfile.create_once(spec, guard=lambda: None)
                create.assert_not_called()
            self.assertEqual(path.read_bytes(), b"foreign reservation")

    def test_failed_durable_intent_precedes_any_profile_call(self):
        with tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
            spec = security.ProfileSpec(MONIKER, str(Path(folder) / "profile-reservation.jsonl"))
            with patch.object(security, "expected_package_sid", return_value=PACKAGE), patch.object(security, "create_profile") as create, patch.object(security.os, "fsync", side_effect=OSError("synthetic disk refusal")):
                with self.assertRaises(OSError):
                    security.PreparedProfile.create_once(spec, guard=lambda: None)
                create.assert_not_called()
            self.assertTrue(Path(spec.reservation).exists())

    def test_ambiguous_profile_creation_retains_intent_and_cannot_replay(self):
        for response in (-2147024713, SystemExit("synthetic supervisor death")):
            with self.subTest(response=type(response).__name__), tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
                spec = security.ProfileSpec(MONIKER, str(Path(folder) / "profile-reservation.jsonl"))
                def create(*args):
                    rows = Path(spec.reservation).read_text(encoding="utf-8").splitlines()
                    self.assertEqual(json.loads(rows[0])["cleanup"], "retain_only")
                    if isinstance(response, BaseException):
                        raise response
                    return response
                with patch.object(security, "expected_package_sid", return_value=PACKAGE), patch.object(security, "create_profile", side_effect=create) as call:
                    with self.assertRaises((Refused, SystemExit)):
                        security.PreparedProfile.create_once(spec, guard=lambda: None)
                    with self.assertRaises(FileExistsError):
                        security.PreparedProfile.create_once(spec, guard=lambda: None)
                    self.assertEqual(call.call_count, 1)
                self.assertTrue(Path(spec.reservation).read_bytes().endswith(b"\n"))

    def test_expiry_after_durable_intent_never_calls_profile_creation(self):
        with tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
            spec = security.ProfileSpec(MONIKER, str(Path(folder) / "profile-reservation.jsonl"))
            calls = []
            def guard():
                calls.append(True)
                if len(calls) == 2:
                    raise Refused("synthetic deadline after durable intent")
            with patch.object(security, "expected_package_sid", return_value=PACKAGE), patch.object(security, "create_profile") as create:
                with self.assertRaises(Refused):
                    security.PreparedProfile.create_once(spec, guard=guard)
                create.assert_not_called()
            self.assertEqual(json.loads(Path(spec.reservation).read_bytes())["cleanup"], "retain_only")

    def test_expired_effect_guard_precedes_native_create_and_descriptor_mutation(self):
        def expired():
            raise Refused("synthetic expired effect")
        with patch.object(objects, "nt_create") as create:
            with self.assertRaises(Refused):
                objects._open("\\??\\C:\\unused", None, directory=True, create=True,
                              security=objects.descriptor(USER, directory=True), guard=expired)
            create.assert_not_called()
        calls = []
        def expires_after_observation():
            calls.append(True)
            if len(calls) == 2:
                raise Refused("synthetic expiry at grant boundary")
        obj = objects.OwnedObject(123, "owned", None, r"C:\owned", True, USER, {"file_id": "first"}, sealed=True, guard=expires_after_observation)
        with patch.object(objects, "_identity", return_value=obj.identity), patch.object(objects, "set_security") as grant:
            with self.assertRaises(Refused):
                obj.grant(PACKAGE, mode="read")
            grant.assert_not_called()

    def test_token_buffer_sid_pointer_and_extent_refuse_before_conversion(self):
        for kind in ("external", "overlong", "bad_revision"):
            value = C.create_string_buffer(32)
            start = C.addressof(value)
            sid = start + 16
            C.cast(value, C.POINTER(C.c_void_p)).contents.value = 1 if kind == "external" else sid
            if kind != "external":
                C.memmove(sid, bytes([2 if kind == "bad_revision" else 1, 15 if kind == "overlong" else 1]) + b"\0" * 10, 12)
            with self.subTest(kind=kind), patch.object(security, "_token_buffer", return_value=value), patch.object(security, "_sid") as convert:
                with self.assertRaises(Refused):
                    security._token_sid(123, 31)
                convert.assert_not_called()

    def test_owned_root_never_adopts_a_preexisting_name(self):
        with patch.object(objects, "local_volume", return_value=r"\Device\HarddiskVolume3"), patch.object(objects, "_open", side_effect=Refused("exclusive create collision")) as opened, patch.object(objects, "set_security") as grant:
            with self.assertRaises(Refused):
                objects.OwnedObject.create_root(r"C:\owned\probe", USER)
            grant.assert_not_called()
            self.assertTrue(opened.call_args.kwargs["create"])
            self.assertEqual(opened.call_args.args[0], r"\Device\HarddiskVolume3\owned\probe")

    def test_drive_mapping_refuses_subst_network_ambiguity_and_unbounded_results(self):
        good = "\\Device\\HarddiskVolume3\x00\x00"
        def query(text, count=None):
            def call(drive, buffer, size):
                self.assertEqual(drive, "C:")
                self.assertEqual(size, 4096)
                buffer[:len(text)] = text
                return len(text) if count is None else count
            return call
        with patch.object(objects, "query_device", side_effect=query(good)):
            self.assertEqual(objects.native_path(r"C:\owned\probe"), r"\Device\HarddiskVolume3\owned\probe")
        for bad, count in (("\\??\\D:\\other\x00\x00", None), ("\\Device\\Mup\\server\x00\x00", None),
                           (good[:-1], None), (good[:-1] + "\\Device\\HarddiskVolume4\x00\x00", None),
                           ("\\Device\\HarddiskVolume3\\other\x00\x00", None),
                           (good, 0), (good, 4096), (good, 9000)):
            with self.subTest(mapping=repr(bad), count=count), patch.object(objects, "query_device", side_effect=query(bad, count)), patch.object(objects, "nt_create") as create:
                with self.assertRaises(Refused):
                    objects.OwnedObject.create_root(r"C:\owned\probe", USER)
                create.assert_not_called()
        for bad in (None, r"\\server\share\file", r"C:\owned\..\other", "C:relative", "C:\\bad:stream"):
            with self.subTest(path=bad), patch.object(objects, "query_device") as query_call:
                with self.assertRaises(Refused):
                    objects.native_path(bad)
                query_call.assert_not_called()

    def test_native_volume_path_keeps_no_reparse_flag_at_actual_open(self):
        def create(handle, access, attrs, status, allocation, attributes, share, disposition, options, ea, ea_length):
            value = C.cast(attrs, C.POINTER(objects.ATTRIBUTES)).contents
            self.assertTrue(value.Attributes & 0x1000)  # OBJ_DONT_REPARSE.
            self.assertEqual(value.ObjectName.contents.Buffer, r"\Device\HarddiskVolume3\owned\probe")
            self.assertEqual(disposition, 2)  # FILE_CREATE, never adopt/open.
            return -1073741771  # STATUS_OBJECT_NAME_COLLISION.
        with patch.object(objects, "nt_create", side_effect=create):
            with self.assertRaises(Refused):
                objects._open(r"\Device\HarddiskVolume3\owned\probe", None, directory=True, create=True)

    def test_effect_driver_refuses_volume_drift_and_monotonic_expiry_before_profile(self):
        driver_path = ROOT / ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h1-native-effect-probe.py"
        spec = importlib.util.spec_from_file_location("h1_reviewed_probe_test", driver_path)
        driver = importlib.util.module_from_spec(spec); spec.loader.exec_module(driver)
        for failure in ("mapping", "monotonic"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
                owned = Path(folder)
                (owned / "owner.json").write_bytes(b"synthetic owned marker")
                (owned / "security-probe.exe").write_bytes(b"unexecuted synthetic image")
                info = owned.stat()
                value = {"schema": "aide.host.h1-effect.v1", "source_base": "0" * 40,
                         "repository": str(ROOT), "source_files": {p: driver.digest((ROOT / p).read_bytes()) for p in driver.SOURCES},
                         "owned_root": str(owned), "owner_sha256": driver.digest((owned / "owner.json").read_bytes()),
                         "parent_stat": {"dev": info.st_dev, "ino": info.st_ino}, "native_volume": r"\Device\HarddiskVolume3",
                         "moniker": MONIKER, "package_sid": PACKAGE, "user_sid": USER,
                         "probe_sha256": driver.digest((owned / "security-probe.exe").read_bytes()),
                         "expires_at": time.time() + 300, "activation": False,
                         "effects": {"profile_creations": 1, "package_capabilities": [], "root": str(owned / "probe-objects"),
                             "reservation": str(owned / "profile-reservation.jsonl"), "new_objects": ["probe.exe", "scratch", "protected-canary"],
                             "package_grants": {".": "read", "probe.exe": "read", "scratch": "modify"},
                             "loopback": "one owned 127.0.0.1 listener; no exemption", "cleanup": "retain_only"}}
                manifest = owned / "manifest.json"; manifest.write_bytes(json.dumps(value).encode())
                with patch.object(objects, "local_volume", return_value=r"\Device\HarddiskVolume4" if failure == "mapping" else value["native_volume"]), patch.object(security, "current_user_sid", return_value=USER), patch.object(security, "expected_package_sid", return_value=PACKAGE), patch.object(security, "create_profile") as create, patch.object(objects, "nt_create") as objects_create, patch.object(driver.time, "monotonic", side_effect=[0, 1000]):
                    with self.assertRaisesRegex(RuntimeError, "local volume changed" if failure == "mapping" else "authority expired"):
                        driver.run(manifest, driver.digest(manifest.read_bytes()))
                    create.assert_not_called(); objects_create.assert_not_called()
                self.assertFalse((owned / "profile-reservation.jsonl").exists())
                self.assertFalse((owned / "probe-objects").exists())

    def continuation_fixture(self, owned):
        path = ROOT / ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h1-owned-network-effect-probe.py"
        spec = importlib.util.spec_from_file_location("h1_owned_continuation_test", path)
        driver = importlib.util.module_from_spec(spec); spec.loader.exec_module(driver)
        rows = [{"schema": "aide.host.profile-intent.v1", "moniker": MONIKER,
                 "expected_package_sid": PACKAGE, "capability_count": 0, "cleanup": "retain_only"},
                {"phase": "created", "package_sid": PACKAGE, "folder": r"C:\synthetic-profile", "cleanup": "retain_only"}]
        receipt = {"schema": "aide.host.h1-native-probe.v1", "activation": False,
                   "profile": {"moniker": MONIKER, "package_sid": PACKAGE, "folder": rows[1]["folder"]},
                   "actual_child_token": observed(), "result": "FAIL"}
        (owned / "profile-reservation.jsonl").write_bytes(b"\n".join(json.dumps(row).encode() for row in rows) + b"\n")
        (owned / "native-probe-receipt.json").write_bytes(json.dumps(receipt).encode())
        proof = {name: driver.digest((owned / name).read_bytes()) for name in ("profile-reservation.jsonl", "native-probe-receipt.json")}
        return driver, rows, receipt, proof

    def endpoint_fixture(self, driver):
        raw = (ROOT / ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h1-local-interface-inventory.json").read_bytes()
        return {"address": "172.21.208.1", "interface_index": 50, "interface_alias": "vEthernet (WSL)",
                "prefix_length": 20, "inventory_sha256": driver.digest(raw)}

    def test_endpoint_refuses_unbound_nonliteral_or_stale_interface_before_effects(self):
        with tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
            driver, _, _, _ = self.continuation_fixture(Path(folder))
            endpoint = self.endpoint_fixture(driver)
            self.assertEqual(driver.pinned_endpoint(endpoint), endpoint)
            cases = [("address", address) for address in ("localhost", "0.0.0.0", "127.0.0.1", "8.8.8.8", "172.21.208.0", "172.21.223.255", "172.021.208.1")]
            cases += [("interface_index", True), ("interface_index", 51), ("interface_alias", "foreign"), ("prefix_length", 24), ("inventory_sha256", "0" * 64)]
            for key, value in cases:
                with self.subTest(key=key, value=value), patch.object(driver.subprocess, "run") as dispatch:
                    changed = dict(endpoint); changed[key] = value
                    with self.assertRaises(RuntimeError): driver.pinned_endpoint(changed)
                    dispatch.assert_not_called()

    def test_actual_interface_parser_refuses_missing_changed_ambiguous_and_unbounded_results(self):
        with tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
            owned = Path(folder); driver, _, _, _ = self.continuation_fixture(owned)
            endpoint = self.endpoint_fixture(driver)
            image = owned / "unexecuted-image"; image.write_bytes(b"synthetic native image")
            expected = driver.digest(image.read_bytes())
            observation = {"address_status": 0, "adapter_status": 0, "address_match": 1, "index_match": 1,
                           "alias_match": 1, "preferred": 1, "connected": 1, "prefix_length": 20, "skip_as_source": 0}
            result = type("Result", (), {"returncode": 0, "stderr": b"", "stdout": json.dumps(observation).encode()})()
            with patch.object(driver.subprocess, "run", return_value=result) as dispatch:
                self.assertEqual(driver.observe_endpoint(image, expected, endpoint), observation)
                self.assertEqual(dispatch.call_args.args[0], [str(image), "--local-interface", endpoint["address"], "50", endpoint["interface_alias"]])
                self.assertEqual(dispatch.call_args.kwargs["timeout"], 1)
            cases = []
            for key in observation:
                changed = dict(observation); changed[key] += 1
                cases.append(json.dumps(changed).encode())
            cases += [b"null", b"[]", b"true", b"{" , b" " * 513, json.dumps(dict(observation, preferred=True)).encode()]
            for raw in cases:
                result.stdout = raw
                with self.subTest(raw=raw[:60]), patch.object(driver.subprocess, "run", return_value=result):
                    with self.assertRaises((RuntimeError, ValueError)): driver.observe_endpoint(image, expected, endpoint)
            result.stdout = json.dumps(observation).encode()
            for code, errors in ((1, b""), (0, b"unexpected")):
                result.returncode, result.stderr = code, errors
                with patch.object(driver.subprocess, "run", return_value=result), self.assertRaises(RuntimeError):
                    driver.observe_endpoint(image, expected, endpoint)
            image.write_bytes(b"substitution")
            with patch.object(driver.subprocess, "run") as dispatch, self.assertRaises(RuntimeError):
                driver.observe_endpoint(image, expected, endpoint)
            dispatch.assert_not_called()

    def test_profile_continuation_requires_proved_creation_and_exact_original_token(self):
        for failure in (None, "intent_only", "uncertain", "boolean_count", "wrong_package", "token_capability", "changed_bytes"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
                owned = Path(folder); driver, rows, receipt, proof = self.continuation_fixture(owned)
                if failure == "intent_only": rows.pop()
                if failure == "uncertain": rows[1]["phase"] = "created_folder_unobserved"
                if failure == "boolean_count": rows[0]["capability_count"] = False
                if failure == "wrong_package": receipt["profile"]["package_sid"] = "S-1-15-2-999"
                if failure == "token_capability": receipt["actual_child_token"]["capability_count"] = 1
                (owned / "profile-reservation.jsonl").write_bytes(b"\n".join(json.dumps(row).encode() for row in rows) + b"\n")
                (owned / "native-probe-receipt.json").write_bytes(json.dumps(receipt).encode())
                if failure != "changed_bytes": proof = {name: driver.digest((owned / name).read_bytes()) for name in proof}
                else: (owned / "native-probe-receipt.json").write_bytes(b"changed foreign evidence")
                with patch.object(security, "create_profile") as create, patch.object(objects, "nt_create") as object_create:
                    if failure is None:
                        profile = driver.observed_created_profile(owned, MONIKER, PACKAGE, USER, proof)
                        self.assertEqual(profile.package_sid, PACKAGE)
                    else:
                        with self.assertRaises((RuntimeError, Refused)):
                            driver.observed_created_profile(owned, MONIKER, PACKAGE, USER, proof)
                    create.assert_not_called(); object_create.assert_not_called()

    def continuation_manifest_fixture(self, folder):
        owned = Path(folder); driver, _, _, proof = self.continuation_fixture(owned)
        (owned / "owner.json").write_bytes(b"synthetic owned marker")
        (owned / "security-probe-interface.exe").write_bytes(b"unexecuted synthetic image")
        endpoint = self.endpoint_fixture(driver)
        info = owned.stat()
        value = {"schema": "aide.host.h1-owned-interface-effect.v1", "source_base": "0" * 40,
                 "repository": str(ROOT), "source_files": {p: driver.digest((ROOT / p).read_bytes()) for p in driver.SOURCES},
                 "owned_root": str(owned), "owner_sha256": driver.digest((owned / "owner.json").read_bytes()),
                 "parent_stat": {"dev": info.st_dev, "ino": info.st_ino}, "native_volume": r"\Device\HarddiskVolume3",
                 "moniker": MONIKER, "package_sid": PACKAGE, "user_sid": USER,
                 "probe_sha256": driver.digest((owned / "security-probe-interface.exe").read_bytes()),
                 "endpoint": endpoint, "expires_at": time.time() + 300, "activation": False, "origin_proof": proof,
                 "effects": {"profile_creations": 0, "package_capabilities": [], "root": str(owned / "interface-probe-objects"),
                     "reservation": str(owned / "interface-probe-reservation.jsonl"), "new_objects": ["probe.exe", "scratch", "protected-canary"],
                     "package_grants": {".": "read", "probe.exe": "read", "scratch": "modify"},
                     "listener": {"address": endpoint["address"], "port": 0, "count": 1, "exclusive": True},
                     "ordinary_controls": 2, "read_only_interface_observations": {"max_calls": 256, "timeout_seconds": 1, "output_bytes": 512},
                     "network_settings_changes": 0, "cleanup": "retain_only"}}
        manifest = owned / "manifest.json"; manifest.write_bytes(json.dumps(value).encode())
        return owned, driver, proof, value, manifest

    def test_continuation_expiry_after_durable_intent_retains_and_cannot_replay(self):
        with tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
            owned, driver, proof, value, manifest = self.continuation_manifest_fixture(folder)
            with patch.object(driver, "observe_endpoint", return_value={}), patch.object(security, "loopback_configuration", return_value={"package_sid": PACKAGE, "configuration_count": 0, "loopback_exempt": False}), patch.object(objects, "local_volume", return_value=value["native_volume"]), patch.object(security, "current_user_sid", return_value=USER), patch.object(security, "expected_package_sid", return_value=PACKAGE), patch.object(security, "create_profile") as create, patch.object(objects.OwnedObject, "create_root") as object_create:
                with patch.object(driver.time, "monotonic", side_effect=lambda: 1000 if (owned / "interface-probe-reservation.jsonl").exists() else 0), self.assertRaisesRegex(RuntimeError, "authority expired"):
                    driver.run(manifest, driver.digest(manifest.read_bytes()))
                intent = (owned / "interface-probe-reservation.jsonl").read_bytes()
                self.assertEqual(json.loads(intent)["profile_creations"], 0)
                self.assertEqual(json.loads((owned / "interface-native-probe-receipt.json").read_bytes())["result"], "FAIL")
                with self.assertRaisesRegex(RuntimeError, "cannot replay"):
                    driver.run(manifest, driver.digest(manifest.read_bytes()))
                self.assertEqual((owned / "interface-probe-reservation.jsonl").read_bytes(), intent)
                self.assertEqual(proof, {name: driver.digest((owned / name).read_bytes()) for name in proof})
                create.assert_not_called(); object_create.assert_not_called()

    def test_interface_revocation_or_expiry_during_read_precedes_durable_effect_intent(self):
        for failure in ("drift", "expiry"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
                owned, driver, proof, value, manifest = self.continuation_manifest_fixture(folder)
                expired = [False]
                def observe(*args):
                    if failure == "drift": raise RuntimeError("actual interface drift")
                    expired[0] = True
                    return {}
                with patch.object(objects, "local_volume", return_value=value["native_volume"]), patch.object(driver, "observe_endpoint", side_effect=observe) as query, patch.object(driver.time, "time", side_effect=lambda: value["expires_at"] + (1 if expired[0] else -300)), patch.object(objects.OwnedObject, "create_root") as create, patch.object(security, "create_profile") as profile:
                    with self.assertRaisesRegex(RuntimeError, "actual interface drift|expired during read-only"):
                        driver.run(manifest, driver.digest(manifest.read_bytes()))
                    self.assertEqual(query.call_count, 1); create.assert_not_called(); profile.assert_not_called()
                self.assertFalse((owned / "interface-probe-reservation.jsonl").exists())
                self.assertFalse((owned / "interface-probe-objects").exists())

    def test_readonly_interface_observation_budget_stops_before_another_dispatch(self):
        with tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
            owned, driver, proof, value, manifest = self.continuation_manifest_fixture(folder)
            def demand_observations(*args, guard, **kwargs):
                for _ in range(257): guard()
                self.fail("observation bound was bypassed")
            with patch.object(driver, "observe_endpoint", return_value={}) as query, patch.object(security, "loopback_configuration", return_value={"package_sid": PACKAGE, "configuration_count": 0, "loopback_exempt": False}), patch.object(objects, "local_volume", return_value=value["native_volume"]), patch.object(security, "current_user_sid", return_value=USER), patch.object(security, "expected_package_sid", return_value=PACKAGE), patch.object(security, "create_profile") as profile, patch.object(objects.OwnedObject, "create_root", side_effect=demand_observations):
                with self.assertRaisesRegex(RuntimeError, "budget exhausted"):
                    driver.run(manifest, driver.digest(manifest.read_bytes()))
                self.assertEqual(query.call_count, 256); profile.assert_not_called()
            receipt = json.loads((owned / "interface-native-probe-receipt.json").read_bytes())
            self.assertEqual((receipt["result"], receipt["read_only_interface_observations"]), ("FAIL", 256))
            self.assertTrue((owned / "interface-probe-reservation.jsonl").exists())
            self.assertFalse((owned / "interface-probe-objects").exists())

    def test_exact_loopback_config_observation_refuses_missing_or_broad_results(self):
        for count, error, matches in ((0, 0, False), (2, 0, True), (0, 5, None), (4097, 0, None)):
            with self.subTest(count=count, error=error):
                rows = (security.SID_ATTRIBUTES * 2)(security.SID_ATTRIBUTES(111, 0), security.SID_ATTRIBUTES(222, 0))
                def query(count_out, rows_out):
                    C.cast(count_out, C.POINTER(W.DWORD)).contents.value = count
                    if count == 2:
                        C.cast(rows_out, C.POINTER(C.POINTER(security.SID_ATTRIBUTES)))[0] = C.cast(rows, C.POINTER(security.SID_ATTRIBUTES))
                    return error
                with patch.object(security, "get_loopback_config", side_effect=query), patch.object(security, "_sid", side_effect=lambda ptr: PACKAGE if ptr == 222 else "other-package"), patch.object(security, "get_heap", return_value=33), patch.object(security, "heap_free") as free:
                    if matches is None:
                        with self.assertRaises(Refused): security.loopback_configuration(PACKAGE)
                    else:
                        self.assertEqual(security.loopback_configuration(PACKAGE), {"package_sid": PACKAGE, "configuration_count": count, "loopback_exempt": matches})
                    self.assertEqual(free.call_count, 3 if count == 2 else 0)
        with patch.object(security, "get_loopback_config") as query:
            with self.assertRaises(Refused): security.loopback_configuration("S-1-15-2-1")
            query.assert_not_called()

    def test_timeout_never_qualifies_without_full_actual_network_diagnostic_controls(self):
        with tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
            driver, _, _, _ = self.continuation_fixture(Path(folder))
            endpoint = self.endpoint_fixture(driver)
            observation = {"network_error": 10060, "diagnostic_status": 0, "missing_capability": 1}
            config = {"package_sid": PACKAGE, "configuration_count": 0, "loopback_exempt": False}
            control = {"endpoint": [endpoint["address"], 23456], "client": [endpoint["address"], 34567], "accepted": [endpoint["address"], 34567]}
            receipt = {"endpoint_connection_observed": False, "loopback_configuration_before": config,
                       "loopback_configuration_after": copy.deepcopy(config),
                       "positive_control_before": control, "positive_control_after": copy.deepcopy(control)}
            driver.verify_network_evidence(observation, receipt, PACKAGE, endpoint)
            for failure in ("pending", "connected", "refused", "no_diagnostic", "unknown_kind", "boolean_kind", "child_connected", "no_config", "exempt", "config_drift", "no_control", "wrong_peer", "wrong_endpoint"):
                value, facts = copy.deepcopy(observation), copy.deepcopy(receipt)
                if failure == "pending": value["network_error"] = 10035
                if failure == "connected": value["network_error"] = 0
                if failure == "refused": value["network_error"] = 10061
                if failure == "no_diagnostic": value.pop("diagnostic_status")
                if failure == "unknown_kind": value["missing_capability"] = 0
                if failure == "boolean_kind": value["missing_capability"] = True
                if failure == "child_connected": facts["endpoint_connection_observed"] = True
                if failure == "no_config": facts.pop("loopback_configuration_before")
                if failure == "exempt": facts["loopback_configuration_before"]["loopback_exempt"] = True
                if failure == "config_drift": facts["loopback_configuration_after"]["configuration_count"] = 1
                if failure == "no_control": facts.pop("positive_control_after")
                if failure == "wrong_peer": facts["positive_control_after"]["accepted"][1] += 1
                if failure == "wrong_endpoint": facts["positive_control_after"]["endpoint"][1] += 1
                with self.subTest(failure=failure), self.assertRaises(RuntimeError):
                    driver.verify_network_evidence(value, facts, PACKAGE, endpoint)

    def test_actual_same_listener_controls_and_preconnect_revocation(self):
        with tempfile.TemporaryDirectory(prefix="aide-h1-source-") as folder:
            driver, _, _, _ = self.continuation_fixture(Path(folder))
            with socket.socket() as listener:
                listener.bind(("127.0.0.1", 0)); listener.listen(1); listener.settimeout(1)
                first = driver.positive_control(listener, lambda: None)
                second = driver.positive_control(listener, lambda: None)
                self.assertEqual(first["endpoint"], second["endpoint"])
                self.assertEqual(first["accepted"], first["client"])
                self.assertEqual(second["accepted"], second["client"])
                def expired(): raise Refused("synthetic revoked control")
                with patch.object(driver.socket, "socket") as create:
                    with self.assertRaises(Refused): driver.positive_control(listener, expired)
                    create.assert_not_called()

    def test_substituted_owned_object_refuses_before_any_grant(self):
        obj = objects.OwnedObject(123, "owned", None, r"C:\owned", True, USER, {"file_id": "first"}, sealed=True)
        with patch.object(objects, "_identity", return_value={"file_id": "foreign"}), patch.object(objects, "set_security") as grant:
            with self.assertRaises(Refused):
                obj.grant(PACKAGE, mode="read")
            grant.assert_not_called()
        with patch.object(objects, "close") as close:
            obj.close(); obj.close()
            close.assert_called_once_with(123)
        self.assertTrue(obj.closed)

    def test_unsealed_or_failed_write_cannot_be_reused_or_granted(self):
        obj = objects.OwnedObject(123, "file", None, r"C:\owned\file", False, USER, {"file_id": "first"})
        with patch.object(objects, "_identity", return_value=obj.identity), patch.object(objects, "set_security") as grant:
            with self.assertRaises(Refused):
                obj.grant(PACKAGE, mode="read")
            grant.assert_not_called()
            with patch.object(objects, "write_file", side_effect=OSError("synthetic partial write")) as write:
                with self.assertRaises(OSError):
                    obj.write(b"one")
                with self.assertRaises(Refused):
                    obj.write(b"retry")
                self.assertEqual(write.call_count, 1)

    def test_read_handle_preserves_original_identity_through_sealing(self):
        original = {"file_id": "original"}
        obj = objects.OwnedObject(1, "file", None, r"C:\owned\file", False, USER, original)
        events = []
        with patch.object(objects, "_identity", return_value=original), patch.object(objects, "_open", side_effect=lambda *args, **kwargs: events.append(("open", kwargs["share"])) or (2 if kwargs["share"] == 3 else 3)), patch.object(objects, "close", side_effect=lambda handle: events.append(("close", handle))):
            obj.seal()
        self.assertEqual(events, [("open", 3), ("close", 1), ("open", 1), ("close", 2)])
        self.assertEqual(obj.handle, 3)
        self.assertTrue(obj.sealed)

    def test_foreign_name_during_sealing_never_receives_grant_or_replaces_original(self):
        obj = objects.OwnedObject(1, "file", None, r"C:\owned\file", False, USER, {"file_id": "original"})
        with patch.object(objects, "_identity", side_effect=lambda handle: {"file_id": "original" if handle == 1 else "foreign"}), patch.object(objects, "_open", return_value=2), patch.object(objects, "close") as close, patch.object(objects, "set_security") as grant:
            with self.assertRaises(Refused):
                obj.seal()
            close.assert_called_once_with(2)
            grant.assert_not_called()
        self.assertEqual(obj.handle, 1)
        self.assertFalse(obj.sealed)

    def test_exact_native_probe_image_and_descriptor_must_stay_bound(self):
        profile = security.PreparedProfile(security.ProfileSpec(MONIKER, r"C:\state\profile-reservation.jsonl"), PACKAGE, r"C:\profile")
        digest = hashlib.sha256(b"native image fixture").hexdigest()
        image = objects.OwnedObject(1, "probe.exe", None, r"C:\owned\probe.exe", False, USER, {"file_id": "image"}, sealed=True, written=True, content_sha256=digest)
        folder = objects.OwnedObject(2, "scratch", None, r"C:\owned\scratch", True, USER, {"file_id": "scratch"}, sealed=True)
        def observation(obj):
            return {"path": obj.path, "identity": obj.identity, "sealed": obj.sealed, "sddl": "current"}
        with patch.object(objects.OwnedObject, "observe", observation):
            with self.assertRaises(Refused):
                security.SecurityLaunch(profile, user_sid=USER, argv=[image.path], cwd=folder.path, image_sha256="0" * 64, owned_objects=(image, folder))
            launch = security.SecurityLaunch(profile, user_sid=USER, argv=[image.path], cwd=folder.path, image_sha256=digest, owned_objects=(image, folder))
            launch.assert_launch([image.path], folder.path)
            with self.assertRaises(Refused):
                launch.assert_launch([image.path, "unexpected"], folder.path)
        with patch.object(objects.OwnedObject, "observe", return_value={"sddl": "changed"}):
            with self.assertRaises(Refused):
                launch.assert_launch([image.path], folder.path)


if __name__ == "__main__":
    unittest.main()
