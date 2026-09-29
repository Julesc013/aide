"""Tiny injected tests for the ordinary-loader effect; no native load occurs."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).with_name("h2_api_loader_effect.py")
spec = importlib.util.spec_from_file_location("h2_api_loader_effect", SOURCE)
effect = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = effect
spec.loader.exec_module(effect)

API_NAME = "api-ms-win-core-file-l1-1-0.dll"


class FakeLoader:
    def __init__(self, *, build="10.0.19045", fail=False, observed=None):
        self.build, self.fail, self.observed = build, fail, observed
        self.calls = []

    def os_build(self):
        self.calls.append("build")
        return self.build

    def load_and_identify(self, name):
        self.calls.append(("load", name))
        if self.fail:
            raise effect.Refused("injected native loader refusal")
        return self.observed or {
            "api_name": name, "physical_name": "kernelbase.dll",
            "module_path": r"C:\Windows\System32\kernelbase.dll",
            "loader_flags": effect.observation.LOADER_SEARCH_SYSTEM32,
            "host_bytes_qualified": False,
            "restricted_loader_qualified": False,
        }


class LoaderEffectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="h2-loader-",
                                                dir=Path(os.environ["AIDE_JOB_TMP"]))
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.root = base / "source"
        self.control = base / "control"
        self.output = base / "output"
        self.root.mkdir(); self.control.mkdir(); self.output.mkdir()
        for relative in (effect.SOURCE_REL, effect.CONTROLLER_REL, effect.DRIVER_REL):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((relative + "\n").encode())
        inventory = self.root / effect.INVENTORY_REL
        inventory.parent.mkdir(parents=True, exist_ok=True)
        names = [API_NAME] + [f"api-ms-win-core-fixture{i}-l1-1-0.dll" for i in range(179)]
        inventory.write_text(json.dumps({"api_names": names}), encoding="utf-8")
        self.manifest = {
            "schema": "aide.host.api-set-loader-effect.v1",
            "request_id": "c" * 32,
            "os_build": "10.0.19045", "api_name": API_NAME,
            "inventory_sha256": self._sha(inventory),
            "source_sha256": self._sha(self.root / effect.SOURCE_REL),
            "controller_sha256": self._sha(self.root / effect.CONTROLLER_REL),
            "driver_sha256": self._sha(self.root / effect.DRIVER_REL),
            "expires_at": time.time() + 300, "max_seconds": 30,
        }

    @staticmethod
    def _sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def journal_path(self):
        return self.control / ("api-loader-" + self.manifest["request_id"] + ".jsonl")

    def journal(self):
        return [json.loads(line) for line in self.journal_path().read_text().splitlines()]

    def test_native_backend_reads_build_without_unavailable_l2_query(self):
        names = []

        def bind(unused, name, args, result):
            names.append(name)
            def running_build(pointer):
                value = pointer._obj
                value.dwMajorVersion, value.dwMinorVersion = 10, 0
                value.dwBuildNumber, value.dwPlatformId = 19045, 2
                return 0
            return running_build

        loader = FakeLoader()
        with patch.object(effect.observation, "NativeApiSetLoaderApi", return_value=loader), \
                patch.object(effect.observation.objects, "bind", side_effect=bind):
            backend = effect.NativeLoaderBackend()
        self.assertEqual(names, ["RtlGetVersion"])
        self.assertEqual(backend.os_build(), "10.0.19045")
        self.assertEqual(backend.load_and_identify(API_NAME)["physical_name"], "kernelbase.dll")

    def test_one_loader_intent_result_and_no_replay(self):
        api = FakeLoader()
        result = effect.run_effect(self.manifest, self.root, self.control, self.output,
                                   lambda: api)
        self.assertEqual(api.calls, ["build", ("load", API_NAME)])
        self.assertEqual(result["native_loads"], 1)
        self.assertFalse(result["host_bytes_qualified"])
        self.assertFalse(result["worker_activated"])
        self.assertEqual([row["kind"] for row in self.journal()],
                         ["exclusive_request", "session_reservation", "pre_call_intent", "terminal"])
        self.assertEqual(self.journal()[-1]["status"], "PASS")
        self.assertEqual(effect.reconcile_result(self.output, self.journal_path(),
                         effect.load_plan(self.manifest, self.root)), result)
        replay = FakeLoader()
        with self.assertRaises(FileExistsError):
            effect.run_effect(self.manifest, self.root, self.control, self.output,
                              lambda: replay)
        self.assertEqual(replay.calls, [])

    def test_changed_or_duplicate_inputs_refuse_before_reservation(self):
        cases = ({"source_sha256": "0" * 64}, {"controller_sha256": "0" * 64},
                 {"driver_sha256": "0" * 64}, {"inventory_sha256": "0" * 64},
                 {"api_name": "kernelbase.dll"}, {"max_seconds": 0},
                 {"expires_at": time.time() - 1}, {"unexpected": True})
        for edit in cases:
            with self.subTest(edit=edit), self.assertRaises(effect.Refused):
                effect.run_effect({**self.manifest, **edit}, self.root,
                                  self.control, self.output, FakeLoader)
        with self.assertRaises(effect.Refused):
            effect.strict_json(b'{"api_name":"x","api_name":"y"}')
        self.assertEqual(list(self.control.iterdir()), [])

    def test_wrong_build_consumes_request_without_load(self):
        api = FakeLoader(build="10.0.19041")
        with self.assertRaises(effect.Refused):
            effect.run_effect(self.manifest, self.root, self.control, self.output,
                              lambda: api)
        self.assertEqual(api.calls, ["build"])
        self.assertEqual(self.journal()[-1]["status"], "REFUSED")
        self.assertEqual((self.output / effect.RESULT_NAME).read_bytes(), effect.PENDING_MARKER)

    def test_loader_failure_retains_intent_and_blocks_replay(self):
        api = FakeLoader(fail=True)
        with self.assertRaises(effect.Refused):
            effect.run_effect(self.manifest, self.root, self.control, self.output,
                              lambda: api)
        self.assertEqual(api.calls, ["build", ("load", API_NAME)])
        self.assertEqual(self.journal()[-2]["kind"], "pre_call_intent")
        self.assertEqual(self.journal()[-1]["status"], "REFUSED")
        with self.assertRaises(FileExistsError):
            effect.run_effect(self.manifest, self.root, self.control, self.output,
                              FakeLoader)

    def test_existing_result_refuses_before_backend(self):
        path = self.output / effect.RESULT_NAME
        path.write_bytes(b"valuable existing result")
        api = FakeLoader()
        with self.assertRaises(FileExistsError):
            effect.run_effect(self.manifest, self.root, self.control, self.output,
                              lambda: api)
        self.assertEqual(api.calls, [])
        self.assertEqual(path.read_bytes(), b"valuable existing result")

    def test_pass_publication_failure_reconciles_without_second_load(self):
        api = FakeLoader()
        with patch.object(effect.control.os, "replace", side_effect=OSError("publication failed")):
            with self.assertRaises(OSError):
                effect.run_effect(self.manifest, self.root, self.control, self.output,
                                  lambda: api)
        self.assertEqual(self.journal()[-1]["status"], "PASS")
        self.assertEqual((self.output / effect.RESULT_NAME).read_bytes(), effect.PENDING_MARKER)
        plan = effect.load_plan(self.manifest, self.root)
        result = effect.reconcile_result(self.output, self.journal_path(), plan)
        self.assertEqual(result["native_loads"], 1)
        self.assertEqual(api.calls.count(("load", API_NAME)), 1)

    def test_short_result_write_never_publishes_success(self):
        actual_write = os.write

        def short_write(fd, value):
            if b'aide.host.api-set-loader-result.v1' in value:
                return len(value) - 1
            return actual_write(fd, value)

        with patch.object(effect.control.os, "write", side_effect=short_write):
            with self.assertRaises(effect.Refused):
                effect.run_effect(self.manifest, self.root, self.control, self.output,
                                  FakeLoader)
        self.assertEqual(self.journal()[-1]["status"], "REFUSED")
        self.assertEqual((self.output / effect.RESULT_NAME).read_bytes(), effect.PENDING_MARKER)

    def test_elapsed_deadline_after_load_refuses_result(self):
        ticks = iter([1.0, 1.0, 1.0, 1.0, 40.0])
        with self.assertRaises(effect.Refused):
            effect.run_effect(self.manifest, self.root, self.control, self.output,
                              FakeLoader, clock=lambda: next(ticks))
        self.assertEqual(self.journal()[-1]["status"], "REFUSED")


if __name__ == "__main__":
    unittest.main()
