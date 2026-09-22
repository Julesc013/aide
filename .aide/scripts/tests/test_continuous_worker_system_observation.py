"""Injected observation tests: no actual DLL mappings, images or grants."""
import copy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker import windows_system_observation as obs
from core.runtime.continuous_worker.state import Refused

NATIVE = r"\Device\HarddiskVolume9\Windows\System32"
API_NAME = "api-ms-win-core-test-l1-1-0.dll"
DATA = b"MZ" + bytes(range(126))
SHA = hashlib.sha256(DATA).hexdigest()


def value():
    return {"schema": "aide.host.system-observation.v1", "request_id": "a" * 32,
            "root": {"path": NATIVE, "identity": {"volume": 5, "file_id": "1" * 32},
                     "owner_sid": "S-1-5-18", "security_sha256": "2" * 64},
            "files": [{"name": "kernelbase.dll", "identity": {"volume": 5, "file_id": "3" * 32},
                       "owner_sid": "S-1-5-18", "security_sha256": "4" * 64,
                       "size": len(DATA), "sha256": SHA, "links": 3}],
            "api_names": [API_NAME], "expires_at": 2000, "max_seconds": 10}


class NativeFake:
    def __init__(self):
        self.events, self.hooks, self.positions = [], {}, {}
        self.root_facts = obs.ObjectFacts(NATIVE, (5, "1" * 32), True, False, 0, 1, "S-1-5-18", "2" * 64)
        self.file_facts = obs.ObjectFacts(NATIVE + r"\kernelbase.dll", (5, "3" * 32), False, False, len(DATA), 3, "S-1-5-18", "4" * 64)
        self.data, self.mapped, self.handle = DATA, self.file_facts.path, 0x10002
        self.bases = (0x20000,)

    def event(self, name, *args):
        self.events.append((name, *args))
        if name in self.hooks: self.hooks[name](*args)

    def open_root(self, path):
        self.event("open_root", path)
        return 16

    def open_file(self, parent, name):
        self.event("open_file", parent, name)
        return 20

    def facts(self, handle):
        self.event("facts", handle)
        return self.root_facts if handle == 16 else self.file_facts

    def read_file(self, handle, count):
        self.event("read_file", handle, count)
        offset = self.positions.get(handle, 0)
        block = self.data[offset:offset + count]
        self.positions[handle] = offset + len(block)
        return block

    def executable_bases(self):
        self.event("bases")
        return self.bases

    def map_resource(self, name):
        self.event("map", name)
        return self.handle

    def mapped_name(self, address):
        self.event("mapped_name", address)
        return self.mapped

    def free_resource(self, handle):
        self.event("free", handle)
        return True

    def close_file(self, handle):
        self.event("close", handle)
        return True


class Journal:
    def __init__(self, api):
        self.api = api
        self.reservation, self.ack = "auto", "auto"
        self.on_reserve, self.on_intent = None, None

    def reserve(self, fingerprint):
        self.api.event("reserve", fingerprint)
        if self.on_reserve: self.on_reserve()
        return fingerprint if self.reservation == "auto" else self.reservation

    def intent(self, intent):
        self.api.event("intent", dict(intent))
        if self.on_intent: self.on_intent()
        return hashlib.sha256(obs._canonical(intent)).hexdigest() if self.ack == "auto" else self.ack


class ObservationTests(unittest.TestCase):
    def setUp(self):
        self.api = NativeFake(); self.journal = Journal(self.api)
        self.now, self.wall = 10.0, 1000.0
        self.guard = lambda: None

    def session(self, plan=None):
        return obs.ObservationSession(obs.ObservationPlan.read(plan or value()), self.api, self.journal,
                                      lambda: self.guard(), clock=lambda: self.now, wall_clock=lambda: self.wall)

    def names(self): return [row[0] for row in self.api.events]

    def test_success_exact_pins_intent_order_and_reverse_release(self):
        session = self.session(); raw = session.run(); result = json.loads(raw)
        self.assertTrue(result["all_owned_handles_released"])
        self.assertFalse(result["loader_qualified"])
        self.assertFalse(result["api_context_qualified"])
        self.assertFalse(result["system_ownership_qualified"])
        self.assertEqual(result["files"][0]["links"], 3)
        self.assertEqual(result["mappings"][0]["physical_name"], "kernelbase.dll")
        self.assertEqual(result["mapping_attempts"], 1)
        self.assertLess(self.names().index("reserve"), self.names().index("open_root"))
        self.assertLess(self.names().index("intent"), self.names().index("map"))
        self.assertEqual([x for x in self.api.events if x[0] in ("free", "close")],
                         [("free", 0x10002), ("close", 20), ("close", 16)])
        intent = next(row[1] for row in self.api.events if row[0] == "intent")
        self.assertEqual(intent["plan_sha256"], session.plan.fingerprint)
        self.assertEqual(intent["flags"], 0x860)
        self.assertEqual(session.resources, [])

    def test_already_loaded_executable_is_distinguished(self):
        self.api.handle = 0x20000
        result = json.loads(self.session().run())
        self.assertEqual(result["mappings"][0]["mapping_kind"], "prior_executable")
        self.assertIn(("free", 0x20000), self.api.events)

    def test_no_replay_after_success_or_uncertain_mapping(self):
        for failure in (False, True):
            with self.subTest(failure=failure):
                self.setUp(); session = self.session()
                if failure:
                    self.api.hooks["map"] = lambda name: (_ for _ in ()).throw(OSError("ambiguous mapping"))
                    with self.assertRaises(Refused): session.run()
                else: session.run()
                before = list(self.api.events)
                with self.assertRaises(Refused): session.run()
                self.assertEqual(self.api.events, before)
                self.assertEqual(self.names().count("map"), 1)
                self.assertEqual(len(session.attempts), 1)

    def test_missing_or_refused_journal_has_no_native_call(self):
        with self.assertRaises(Refused): obs.ObservationSession(obs.ObservationPlan.read(value()), self.api, None, lambda: None)
        for ack in (None, {}, "invalid", 7, "5" * 64):
            with self.subTest(ack=ack):
                self.setUp(); self.journal.reservation = ack
                with self.assertRaises(Refused): self.session().run()
                self.assertEqual(self.names(), ["reserve"])

    def test_intent_failure_never_dispatches_and_closes_leases(self):
        self.journal.ack = None
        session = self.session()
        with self.assertRaises(Refused): session.run()
        self.assertNotIn("map", self.names())
        self.assertEqual(self.names().count("intent"), 1)
        self.assertEqual(self.api.events[-2:], [("close", 20), ("close", 16)])

    def test_well_formed_acknowledgement_for_wrong_intent_refuses(self):
        self.journal.ack = "6" * 64
        with self.assertRaises(Refused): self.session().run()
        self.assertIn("intent", self.names()); self.assertNotIn("map", self.names())

    def test_explicit_guard_refusal_has_no_journal_or_native_calls(self):
        self.guard = lambda: False
        with self.assertRaises(Refused): self.session().run()
        self.assertEqual(self.api.events, [])

    def test_expired_before_reservation_refuses_every_effect(self):
        self.wall = 2000
        with self.assertRaises(Refused): self.session().run()
        self.assertEqual(self.api.events, [])

    def test_expiry_after_intent_never_maps(self):
        self.journal.on_intent = lambda: setattr(self, "wall", 2000)
        with self.assertRaises(Refused): self.session().run()
        self.assertIn("intent", self.names()); self.assertNotIn("map", self.names())
        self.assertEqual(self.api.events[-2:], [("close", 20), ("close", 16)])

    def test_elapsed_and_backward_clock_refuse_after_acquisition(self):
        for name, changed in (("now", 20), ("now", 9), ("wall", 999), ("now", float("nan"))):
            with self.subTest(name=name, changed=changed):
                self.setUp(); self.api.hooks["open_root"] = lambda path: setattr(self, name, changed)
                with self.assertRaises(Refused): self.session().run()
                self.assertEqual(self.api.events[-1], ("close", 16))
                self.assertNotIn("open_file", self.names())

    def test_post_mapping_guard_failure_still_releases_exact_handle(self):
        def changed(name):
            self.guard = lambda: (_ for _ in ()).throw(Refused("admission drift"))
        self.api.hooks["map"] = changed
        with self.assertRaises(Refused): self.session().run()
        self.assertEqual(self.api.events[-3:], [("free", 0x10002), ("close", 20), ("close", 16)])
        self.assertNotIn("mapped_name", self.names())

    def test_operation_budget_is_consumed_before_call(self):
        with patch.object(obs, "MAX_NATIVE_CALLS", 1):
            session = self.session()
            with self.assertRaises(Refused): session.run()
        self.assertEqual(session.calls, 1)
        self.assertEqual(self.names(), ["reserve", "open_root", "close"])

    def test_root_drift_refuses_before_any_file_read_or_map(self):
        for update in ({"identity": (5, "9" * 32)}, {"owner_sid": "S-1-5-19"},
                       {"security_sha256": "9" * 64}, {"path": NATIVE + "."}, {"directory": False}):
            with self.subTest(update=update):
                self.setUp(); self.api.root_facts = replace(self.api.root_facts, **update)
                with self.assertRaises(Refused): self.session().run()
                self.assertNotIn("open_file", self.names()); self.assertNotIn("map", self.names())

    def test_untyped_object_facts_refuse_before_mapping(self):
        for update in ({"identity": [5, "3" * 32]}, {"identity": (True, "3" * 32)},
                       {"owner_sid": None}, {"security_sha256": None}):
            with self.subTest(update=update):
                self.setUp(); self.api.file_facts = replace(self.api.file_facts, **update)
                with self.assertRaises(Refused): self.session().run()
                self.assertNotIn("map", self.names())

    def test_file_kind_identity_descriptor_link_and_extent_drift_refuse(self):
        cases = [{"identity": (5, "9" * 32)}, {"directory": True}, {"delete_pending": True},
                 {"size": len(DATA) + 1}, {"links": 1}, {"owner_sid": "S-1-5-19"},
                 {"security_sha256": "8" * 64}, {"path": NATIVE + r"\elsewhere.dll"}]
        for update in cases:
            with self.subTest(update=update):
                self.setUp(); self.api.file_facts = replace(self.api.file_facts, **update)
                with self.assertRaises(Refused): self.session().run()
                self.assertNotIn("map", self.names())
                self.assertEqual(self.api.events[-2:], [("close", 20), ("close", 16)])

    def test_byte_substitution_and_incomplete_or_overlong_stream_refuse(self):
        for data in (b"x" * len(DATA), DATA[:-1], DATA + b"x"):
            with self.subTest(length=len(data)):
                self.setUp(); self.api.data = data
                with self.assertRaises(Refused): self.session().run()
                self.assertNotIn("map", self.names())

    def test_partial_native_reads_are_bounded_and_accumulate(self):
        original = self.api.read_file
        self.api.read_file = lambda handle, count: original(handle, min(count, 7))
        result = json.loads(self.session().run())
        self.assertEqual(result["files"][0]["sha256"], SHA)
        self.assertGreater(self.names().count("read_file"), 10)

    def test_unadmitted_or_incomplete_mapped_name_refuses(self):
        for path in (r"\Device\HarddiskVolume9\Temp\kernelbase.dll", NATIVE + r"\unknown.dll", "x" * 1024, None):
            with self.subTest(path=path):
                self.setUp(); self.api.mapped = path
                with self.assertRaises(Refused): self.session().run()
                self.assertEqual(self.names().count("free"), 1)

    def test_tags_prior_origin_and_new_executable_inventory_refuse(self):
        for handle in (0x10003, 0x10000, 0x10006):
            with self.subTest(handle=handle):
                self.setUp(); self.api.handle = handle
                with self.assertRaises(Refused): self.session().run()
                self.assertIn(("free", handle), self.api.events)
        self.setUp(); self.api.hooks["map"] = lambda name: setattr(self.api, "bases", (0x10000, 0x20000))
        with self.assertRaises(Refused): self.session().run()
        self.assertEqual(self.names().count("free"), 1)

    def test_mapping_host_is_reobserved_after_resource_call(self):
        self.api.hooks["mapped_name"] = lambda address: setattr(self.api, "file_facts", replace(self.api.file_facts, identity=(5, "9" * 32)))
        with self.assertRaises(Refused): self.session().run()
        self.assertEqual(self.names().count("free"), 1)

    def test_invalid_acquisition_and_duplicate_file_handle_are_not_closed_twice(self):
        self.api.open_file = lambda parent, name: 16
        with self.assertRaises(Refused): self.session().run()
        self.assertEqual([row for row in self.api.events if row[0] == "close"], [("close", 16)])
        self.setUp(); self.api.handle = None
        with self.assertRaises(Refused): self.session().run()
        self.assertNotIn("free", self.names())
        self.assertEqual(self.api.events[-2:], [("close", 20), ("close", 16)])

    def test_release_failure_is_retained_once_and_other_handles_close(self):
        self.api.hooks["free"] = lambda handle: (_ for _ in ()).throw(OSError("release uncertain"))
        session = self.session()
        with self.assertRaises(Refused): session.run()
        self.assertEqual(session.release_failures, [{"kind": "mapping", "handle": 0x10002, "error_type": "OSError"}])
        self.assertEqual(self.names().count("free"), 1)
        self.assertEqual(self.api.events[-2:], [("close", 20), ("close", 16)])
        with self.assertRaises(Refused): session.run()
        self.assertEqual(self.names().count("free"), 1)

    def test_read_handle_close_failure_never_returns_success(self):
        self.api.hooks["close"] = lambda handle: (_ for _ in ()).throw(OSError("close uncertain")) if handle == 20 else None
        session = self.session()
        with self.assertRaises(Refused): session.run()
        self.assertEqual(session.release_failures[0]["handle"], 20)
        self.assertEqual(self.api.events[-1], ("close", 16))

    def test_final_cleanup_expiry_guard_or_clock_drift_refuses_success(self):
        for name, changed in (("now", 20), ("wall", 2000), ("guard", lambda: False),
                              ("now", 9), ("now", float("nan"))):
            with self.subTest(name=name, changed=changed):
                self.setUp()
                self.api.hooks["close"] = lambda handle: setattr(self, name, changed) if handle == 16 else None
                session = self.session()
                with self.assertRaises(Refused): session.run()
                self.assertIsNotNone(session.failure)
                self.assertEqual(session.resources, [])
                self.assertEqual(self.api.events[-2:], [("close", 20), ("close", 16)])
                count = len(self.api.events)
                with self.assertRaises(Refused): session.run()
                self.assertEqual(len(self.api.events), count)

    def test_final_serialization_staleness_size_and_failure_are_retained(self):
        original = obs._canonical
        for mode in ("expiry", "error", "oversize"):
            with self.subTest(mode=mode):
                self.setUp(); session = self.session()
                def serialize(row):
                    if ("close", 16) in self.api.events:
                        if mode == "expiry": self.wall = 2000
                        elif mode == "error": raise ValueError("serialization refused")
                        else: return b"x" * (obs.MAX_RESULT_BYTES + 1)
                    return original(row)
                with patch.object(obs, "_canonical", serialize), self.assertRaises(Refused): session.run()
                self.assertIsNotNone(session.failure)
                self.assertEqual(session.resources, [])
                self.assertEqual(self.names().count("close"), 2)

    def test_final_precall_guard_cannot_dispatch_after_consuming_expiry(self):
        for name, changed in (("wall", 2000), ("now", 20), ("now", 9), ("now", float("nan"))):
            with self.subTest(name=name, changed=changed):
                self.setUp(); count = [0]
                def guard():
                    count[0] += 1
                    if count[0] == 2: setattr(self, name, changed)
                self.journal.on_intent = lambda: setattr(self, "guard", guard)
                with self.assertRaises(Refused): self.session().run()
                self.assertIn("intent", self.names()); self.assertNotIn("map", self.names())
                self.assertEqual(self.api.events[-2:], [("close", 20), ("close", 16)])

    def test_mapping_exact_spelling_binds_the_held_object_observation(self):
        self.api.mapped = NATIVE + r"\KERNELBASE.DLL"
        with self.assertRaises(Refused): self.session().run()
        self.setUp()
        self.api.file_facts = replace(self.api.file_facts, path=NATIVE + r"\KERNELBASE.DLL")
        self.api.mapped = self.api.file_facts.path
        self.assertEqual(json.loads(self.session().run())["mappings"][0]["mapped_path"], self.api.mapped)

    def test_arbitrary_precision_temporal_fields_refuse_typed(self):
        for field in ("expires_at", "max_seconds"):
            with self.subTest(field=field), self.assertRaises(Refused):
                obs.ObservationPlan.read({**value(), field: 10**1000})
        self.now = 10**1000
        with self.assertRaises(Refused): self.session().run()
        self.assertEqual(self.api.events, [])

    def test_result_bound_refuses_and_releases_all_handles(self):
        with patch.object(obs, "MAX_RESULT_BYTES", 16):
            with self.assertRaises(Refused): self.session().run()
        self.assertEqual(self.api.events[-2:], [("close", 20), ("close", 16)])

    def test_plan_copies_caller_data_and_revalidates_typed_values(self):
        original = value(); plan = obs.ObservationPlan.read(original)
        original["files"][0]["sha256"] = "9" * 64
        self.assertEqual(plan.files[0].sha256, SHA)
        forged = replace(plan, max_seconds=121)
        with self.assertRaises(Refused): forged.validate()
        self.assertEqual(obs.ObservationPlan.read(plan.value()), plan)

    def test_plan_scalar_fields_names_and_aliases_refuse(self):
        for v in (None, [], 1, "x", {**value(), "extra": 1}):
            with self.subTest(value=v), self.assertRaises(Refused): obs.ObservationPlan.read(v)
        updates = [{"expires_at": float("inf")}, {"max_seconds": True}, {"max_seconds": 121},
                   {"request_id": "../../x"}, {"api_names": [API_NAME, API_NAME]},
                   {"api_names": [r"..\api-ms-win-x-l1-1-0.dll"]}, {"api_names": ["kernel32.dll"]}]
        for update in updates:
            with self.subTest(update=update), self.assertRaises(Refused): obs.ObservationPlan.read({**value(), **update})
        for name in ("KERNELBASE.DLL", "api-ms-win-x-l1-1-0.dll", "python314.dll", "vcruntime140.dll", "con.dll", "../x.dll"):
            v = value(); v["files"][0]["name"] = name
            with self.subTest(name=name), self.assertRaises(Refused): obs.ObservationPlan.read(v)

    def test_plan_identity_link_byte_and_api_capacity_bounds(self):
        for key, bad in (("size", True), ("size", obs.MAX_PE_BYTES + 1), ("links", 0), ("links", 1025)):
            v = value(); v["files"][0][key] = bad
            with self.subTest(key=key, bad=bad), self.assertRaises(Refused): obs.ObservationPlan.read(v)
        v = value(); v["files"][0]["identity"]["volume"] = 6
        with self.assertRaises(Refused): obs.ObservationPlan.read(v)
        v = value(); v["files"].append(copy.deepcopy(v["files"][0]))
        with self.assertRaises(Refused): obs.ObservationPlan.read(v)
        v = value(); v["api_names"] = [f"api-ms-win-test-{i}-l1-1-0.dll" for i in range(128)]
        self.assertEqual(len(obs.ObservationPlan.read(v).api_names), 128)
        v["api_names"].append("api-ms-win-extra-l1-1-0.dll")
        with self.assertRaises(Refused): obs.ObservationPlan.read(v)
        v = value(); v["files"] = [dict(v["files"][0], name=f"m{i}.dll", size=obs.MAX_PE_BYTES,
                                       identity={"volume": 5, "file_id": f"{100+i:032x}"}) for i in range(17)]
        with self.assertRaises(Refused): obs.ObservationPlan.read(v)

    def test_empty_api_inventory_is_an_explicit_file_only_observation(self):
        v = value(); v["api_names"] = []
        result = json.loads(self.session(v).run())
        self.assertEqual(result["mappings"], []); self.assertNotIn("map", self.names())

    def test_malformed_executable_inventory_refuses_typed(self):
        for bases in ([], (), (True,), (0x20000, 0x20000), (0x20001,), ([],)):
            with self.subTest(bases=bases), self.assertRaises(Refused): obs.ObservationSession._bases(bases)


class NativeAdapterInjectedTests(unittest.TestCase):
    def test_only_fixed_resource_flags_and_exact_owned_release(self):
        api = obs.NativeSystemApi.__new__(obs.NativeSystemApi)
        api._load = Mock(return_value=0x10002); api._free = Mock(return_value=True)
        self.assertEqual(api.map_resource(API_NAME), 0x10002)
        api._load.assert_called_once_with(API_NAME, None, 0x860)
        self.assertTrue(api.free_resource(0x10002)); api._free.assert_called_once_with(0x10002)
        api._load.reset_mock(); api._load.return_value = None
        with self.assertRaises(Refused): api.map_resource(API_NAME)
        self.assertEqual(api._load.call_count, 1)
        self.assertEqual(api._free.call_count, 1)

    def test_truncated_or_missing_native_mapped_path_refuses(self):
        api = obs.NativeSystemApi.__new__(obs.NativeSystemApi); api._process = lambda: 1
        for count in (0, 1024, 1025):
            api._mapped = Mock(return_value=count)
            with self.subTest(count=count), self.assertRaises(Refused): api.mapped_name(0x10000)
        def good(process, address, buffer, capacity):
            buffer.value = NATIVE + r"\kernelbase.dll"
            return len(buffer.value)
        api._mapped = good
        self.assertEqual(api.mapped_name(0x10000), NATIVE + r"\kernelbase.dll")

    def test_invalid_api_name_cannot_reach_loader(self):
        api = obs.NativeSystemApi.__new__(obs.NativeSystemApi); api._load = Mock()
        for name in ("kernel32.dll", r"C:\bad.dll", API_NAME.upper()):
            with self.subTest(name=name), self.assertRaises(Refused): api.map_resource(name)
        api._load.assert_not_called()


if __name__ == "__main__":
    unittest.main()
