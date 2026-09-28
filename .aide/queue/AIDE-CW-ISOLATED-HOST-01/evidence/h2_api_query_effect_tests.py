"""Synthetic admission and durable-output checks; no native API calls."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest import mock
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import h2_api_query_effect as effect


class EffectTests(unittest.TestCase):
    def setUp(self):
        parent = os.environ["AIDE_JOB_TMP"]
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "output"
        self.output.mkdir()
        names = json.loads((effect.REPO / effect.INVENTORY).read_bytes())["api_names"]
        self.value = {
            "schema": "aide.host.api-set-native-effect.v1",
            "inventory_sha256": effect.INVENTORY_SHA256,
            "source_files": {
                relative: hashlib.sha256((effect.REPO / relative).read_bytes()).hexdigest()
                for relative in effect.SOURCE_FILES
            },
            "plan": {
                "schema": "aide.host.api-set-query.v1",
                "request_id": "0" * 32,
                "os_build": "10.0.19041",
                "api_names": names,
                "expires_at": time.time() + 300,
                "max_seconds": 30,
            },
            "effects": {
                "native_api_set_queries": 180,
                "api_query_library_loads": 1,
                "physical_host_reads": 0,
                "file_copies": 0,
                "grants": 0,
                "profiles": 0,
                "network_calls": 0,
                "operational_activation": False,
            },
        }

    def write_effect(self):
        path = self.root / "effect.json"
        raw = effect._canonical(self.value)
        path.write_bytes(raw)
        return path, effect.digest(raw)

    def test_exact_retained_inventory_and_source_admit_without_native_call(self):
        path, sha = self.write_effect()
        with mock.patch.object(effect, "NativeApiSetQueryApi", side_effect=AssertionError("native")):
            value, plan = effect.load_effect(path, sha)
        self.assertEqual(len(plan.api_names), 180)
        self.assertEqual(value["inventory_sha256"], effect.INVENTORY_SHA256)

    def test_changed_inventory_or_source_refused_before_native_constructor(self):
        self.value["plan"]["api_names"] = self.value["plan"]["api_names"][:-1]
        path, sha = self.write_effect()
        with self.assertRaisesRegex(ValueError, "180-name"):
            effect.load_effect(path, sha)
        self.value["plan"]["api_names"] = json.loads(
            (effect.REPO / effect.INVENTORY).read_bytes()
        )["api_names"]
        self.value["source_files"][effect.SOURCE_FILES[0]] = "0" * 64
        path, sha = self.write_effect()
        with self.assertRaisesRegex(ValueError, "source input changed"):
            effect.load_effect(path, sha)

    def test_journal_exclusive_and_durable_intent_order(self):
        journal = effect.Journal(self.output, "a" * 64, "b" * 32)
        try:
            self.assertEqual(journal.reserve("c" * 64), "c" * 64)
            row = {"schema": "test.intent.v1", "sequence": 0}
            self.assertEqual(journal.intent(row), effect.digest(effect._canonical(row)))
        finally:
            journal.close()
        entries = [json.loads(line) for line in journal.path.read_bytes().splitlines()]
        self.assertEqual([entry["schema"] for entry in entries],
                         ["aide.host.api-set-native-reservation.v1", "test.intent.v1"])
        self.assertFalse(entries[0]["replay_permitted"])
        with self.assertRaises(FileExistsError):
            effect.Journal(self.output, "a" * 64, "b" * 32)

    def test_native_library_construction_is_deferred_until_after_reservation(self):
        fake = mock.Mock()
        fake.os_build.return_value = "10.0.19041"
        with mock.patch.object(effect, "NativeApiSetQueryApi", return_value=fake) as ctor:
            api = effect.DeferredNativeApi()
            ctor.assert_not_called()
            journal = effect.Journal(self.output, "a" * 64, "b" * 32)
            try:
                journal.reserve("c" * 64)
                self.assertEqual(api.os_build(), "10.0.19041")
                api.api_set_host("api-ms-win-core-test-l1-1-0.dll")
                ctor.assert_called_once()
            finally:
                journal.close()

    def test_failure_retained_without_replay_or_success_output(self):
        path, sha = self.write_effect()
        class FailingSession:
            failure = {"native_calls": 1, "query_attempts": 1}

            def __init__(self, plan, api, journal, guard):
                self.journal = journal

            def run(self):
                self.journal.reserve("c" * 64)
                self.journal.intent({"schema": "test.intent.v1"})
                raise RuntimeError("synthetic native refusal")

        with mock.patch.object(effect, "NativeApiSetQueryApi", return_value=object()):
            with mock.patch.object(effect, "ApiSetQuerySession", FailingSession):
                self.assertEqual(effect.run(path, sha, self.output, "b" * 32), 2)
        failure = json.loads((self.output / "api-query-failure.json").read_bytes())
        self.assertFalse(failure["replay_permitted"])
        self.assertEqual(failure["session_failure"]["native_calls"], 1)
        self.assertFalse((self.output / "api-query-result.json").exists())
        with self.assertRaises(FileExistsError):
            effect.run(path, sha, self.output, "b" * 32)


if __name__ == "__main__":
    unittest.main()
