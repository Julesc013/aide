"""Tiny managed fixtures for the one-use API-set query controller."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).with_name("h2_api_query_effect.py")
spec = importlib.util.spec_from_file_location("h2_api_query_effect", SOURCE)
effect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(effect)


class FakeApi:
    def __init__(self, *, build="10.0.19045", fail_at=None):
        self.build, self.fail_at, self.calls = build, fail_at, []

    def os_build(self):
        return self.build

    def api_set_host(self, name):
        self.calls.append(name)
        if len(self.calls) == self.fail_at:
            raise effect.Refused("injected native query refusal")
        return "kernelbase.dll"


class EffectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(
            prefix="h2-query-", dir=Path(os.environ["AIDE_JOB_TMP"])
        )
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        self.root.mkdir()
        self.control = Path(self.temp.name) / "control"
        self.output = Path(self.temp.name) / "output"
        self.control.mkdir(); self.output.mkdir()
        source = self.root / effect.SOURCE_REL
        source.parent.mkdir(parents=True)
        source.write_bytes(b"bounded source fixture")
        inventory = self.root / effect.INVENTORY_REL
        inventory.parent.mkdir(parents=True)
        self.names = [f"api-ms-win-core-test{i}-l1-1-0.dll" for i in range(180)]
        inventory.write_bytes(json.dumps({"api_names": self.names}).encode())
        self.manifest = {
            "schema": "aide.host.api-query-effect.v1", "request_id": "a" * 32,
            "os_build": "10.0.19045", "api_names": self.names,
            "inventory_sha256": hashlib.sha256(inventory.read_bytes()).hexdigest(),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "expires_at": time.time() + 300, "max_seconds": 120,
        }

    def journal(self):
        path = self.control / ("api-query-" + self.manifest["request_id"] + ".jsonl")
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    def test_exact_180_queries_have_durable_intents_result_and_no_replay(self):
        api = FakeApi()
        result = effect.run_effect(self.manifest, self.root, self.control, self.output, lambda: api)
        self.assertEqual(result["query_attempts"], 180)
        self.assertEqual(result["native_calls"], 181)
        self.assertEqual(api.calls, sorted(self.names))
        rows = self.journal()
        self.assertEqual(len(rows), 183)
        self.assertEqual([row["kind"] for row in rows[:3]],
                         ["exclusive_request", "session_reservation", "pre_call_intent"])
        self.assertEqual(rows[-1]["status"], "PASS")
        self.assertEqual(json.loads((self.output / effect.RESULT_NAME).read_bytes()), result)
        replay = FakeApi()
        with self.assertRaises(FileExistsError):
            effect.run_effect(self.manifest, self.root, self.control, self.output, lambda: replay)
        self.assertEqual(replay.calls, [])

    def test_changed_inventory_or_stale_expiry_refuses_before_reservation(self):
        for edit in ({"inventory_sha256": "0" * 64},
                     {"source_sha256": "0" * 64},
                     {"expires_at": time.time() - 1},
                     {"unexpected": "field"}):
            with self.subTest(edit=edit), self.assertRaises(effect.Refused):
                effect.run_effect({**self.manifest, **edit}, self.root,
                                  self.control, self.output, FakeApi)
        self.assertEqual(list(self.control.iterdir()), [])

    def test_unflushed_exclusive_reservation_refuses_before_backend(self):
        called = []
        with patch.object(effect.os, "fsync", side_effect=OSError("injected flush failure")):
            with self.assertRaises(OSError):
                effect.run_effect(self.manifest, self.root, self.control,
                                  self.output, lambda: called.append(True))
        self.assertEqual(called, [])
        self.assertEqual(len(list(self.control.iterdir())), 1)
        with self.assertRaises(FileExistsError):
            effect.run_effect(self.manifest, self.root, self.control,
                              self.output, lambda: called.append(True))
        self.assertEqual(called, [])

    def test_unusable_retained_output_refuses_before_reservation(self):
        with self.assertRaises(effect.Refused):
            effect.run_effect(self.manifest, self.root, self.control,
                              self.root / effect.SOURCE_REL, FakeApi)
        self.assertEqual(list(self.control.iterdir()), [])

    def test_wrong_running_build_records_consumed_failure_without_query(self):
        api = FakeApi(build="10.0.19041")
        with self.assertRaises(effect.Refused):
            effect.run_effect(self.manifest, self.root, self.control, self.output, lambda: api)
        self.assertEqual(api.calls, [])
        self.assertEqual([row["kind"] for row in self.journal()],
                         ["exclusive_request", "session_reservation", "terminal"])
        self.assertEqual(self.journal()[-1]["status"], "REFUSED")
        self.assertFalse((self.output / effect.RESULT_NAME).exists())

    def test_mid_query_failure_retains_pre_call_intents_and_refuses_replay(self):
        api = FakeApi(fail_at=4)
        with self.assertRaises(effect.Refused):
            effect.run_effect(self.manifest, self.root, self.control, self.output, lambda: api)
        self.assertEqual(len(api.calls), 4)
        self.assertEqual(sum(row["kind"] == "pre_call_intent" for row in self.journal()), 4)
        self.assertEqual(self.journal()[-1]["status"], "REFUSED")
        self.assertFalse((self.output / effect.RESULT_NAME).exists())
        with self.assertRaises(FileExistsError):
            effect.run_effect(self.manifest, self.root, self.control, self.output, FakeApi)

    def test_existing_result_never_becomes_terminal_success(self):
        path = self.output / effect.RESULT_NAME
        path.write_bytes(b"valuable prior result")
        with self.assertRaises(FileExistsError):
            effect.run_effect(self.manifest, self.root, self.control, self.output, FakeApi)
        self.assertEqual(path.read_bytes(), b"valuable prior result")
        self.assertEqual(self.journal()[-1]["status"], "REFUSED")


if __name__ == "__main__":
    unittest.main()
