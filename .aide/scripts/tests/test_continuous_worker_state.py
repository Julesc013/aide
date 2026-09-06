from __future__ import annotations

import concurrent.futures
import json
import sqlite3
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from core.runtime.continuous_worker.state import State, Refused, digest
from core.runtime.continuous_worker.locking import supervisor_lock
from core.runtime.continuous_worker import codex


def activation():
    return {"tasks": [{"id": "first", "depends_on": []}, {"id": "second", "depends_on": []}]}


class StateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aide-continuous-state-")
        self.root = Path(self.temp.name)
        self.state = State(self.root)
        self.state.bind(activation())

    def tearDown(self):
        self.state.close()
        self.temp.cleanup()

    def test_two_connections_claim_once(self):
        def claim(_):
            s = State(self.root)
            try:
                return s.claim(2)
            finally:
                s.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(claim, range(2)))
        self.assertEqual(sum(r is not None for r in results), 1)

    def test_effect_intent_survives_reopen(self):
        task = self.state.claim(2)
        effect = self.state.intent(task["id"], "coding", {"job_id": uuid.uuid4().hex})
        self.state.close()
        self.state = State(self.root)
        self.assertEqual(self.state.unresolved()[0]["id"], effect)
        self.assertIsNone(self.state.claim(2))

    def test_same_phase_cannot_dispatch_twice(self):
        task = self.state.claim(2)
        self.state.intent(task["id"], "coding", {})
        with self.assertRaises(sqlite3.IntegrityError):
            self.state.intent(task["id"], "coding", {})
        self.assertEqual(len(self.state.unresolved()), 1)

    def test_unresolved_effect_prevents_terminal_transition(self):
        task = self.state.claim(2)
        self.state.intent(task["id"], "coding", {})
        with self.assertRaisesRegex(Refused, "unreconciled"):
            self.state.transition(task["id"], "succeeded", {})
        self.assertEqual(self.state.active()["stage"], "claimed")

    def test_observation_idempotency_and_conflict(self):
        task = self.state.claim(2)
        effect = self.state.intent(task["id"], "coding", {})
        self.state.observed(effect, {"done": True})
        self.state.observed(effect, {"done": True})
        with self.assertRaisesRegex(Refused, "conflicting"):
            self.state.observed(effect, {"done": False})

    def test_automatic_next_task_and_attempt_budget(self):
        first = self.state.claim(2)
        self.state.transition(first["id"], "succeeded", {"receipt": "test-only"})
        second = self.state.claim(2)
        self.assertEqual(second["task"], "second")
        self.state.transition(second["id"], "blocked", {"reason": "fixture"})
        self.assertIsNone(self.state.claim(2))

    def test_changed_admission_refused(self):
        altered = activation()
        altered["tasks"][0]["depends_on"] = ["second"]
        with self.assertRaisesRegex(Refused, "activation changed"):
            self.state.bind(altered)

    def test_pause_and_resume_persist(self):
        self.state.control("pause-dispatch")
        self.assertIsNone(self.state.claim(2))
        other = State(self.root)
        try:
            self.assertEqual(other.mode(), "pause-dispatch")
        finally:
            other.close()
        self.state.control("resume")
        self.assertIsNotNone(self.state.claim(2))

    def test_drain_admits_no_new_task(self):
        task = self.state.claim(2)
        self.state.control("drain")
        self.assertFalse(self.state.cancelled(task["task"]))
        self.state.transition(task["id"], "succeeded", {})
        self.assertIsNone(self.state.claim(2))

    def test_cancel_one_task_keeps_other_ready(self):
        self.state.control("cancel-task", "first")
        self.assertEqual(self.state.claim(2)["task"], "second")

    def test_emergency_stop_cancels_active(self):
        task = self.state.claim(2)
        self.state.control("emergency-stop")
        self.assertTrue(self.state.cancelled(task["task"]))

    def test_exclusive_supervisor_lock(self):
        with supervisor_lock(self.root):
            with self.assertRaisesRegex(Refused, "another supervisor"):
                with supervisor_lock(self.root):
                    self.fail("second lock acquired")
        with supervisor_lock(self.root):
            pass

    def test_schema_downgrade_refused(self):
        self.state.db.execute("PRAGMA user_version=999")
        with self.assertRaisesRegex(Refused, "unsupported"):
            State(self.root)


class CodexTests(unittest.TestCase):
    def parse(self, records, expected="subject"):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "events.jsonl"
            path.write_text("\n".join(json.dumps(e) for e in records), encoding="utf-8")
            return codex.parse_events(path, expected)

    def events(self):
        return [{"type": "thread.started", "thread_id": str(uuid.uuid4())},
                {"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps({
                    "status": "pass", "summary": "fixture", "findings": [], "subject_identity": "subject"})}},
                {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 2}}]

    def test_valid_structured_completed_session(self):
        self.assertEqual(self.parse(self.events())["result"]["status"], "pass")

    def test_final_message_without_completed_turn_fails(self):
        with self.assertRaises(Refused):
            self.parse(self.events()[:-1])

    def test_error_overrides_success_message(self):
        with self.assertRaises(Refused):
            self.parse(self.events() + [{"type": "error", "message": "quota"}])

    def test_wrong_subject_fails(self):
        with self.assertRaisesRegex(Refused, "subject"):
            self.parse(self.events(), "different")

    def test_resume_never_uses_last(self):
        session = str(uuid.uuid4())
        args = codex.argv(["codex"], "workspace", "schema", session_id=session)
        self.assertIn(session, args)
        self.assertNotIn("--last", args)
        with self.assertRaises(ValueError):
            codex.argv(["codex"], "workspace", "schema", session_id="--last")

    def test_scalar_events_and_null_session_refused(self):
        for events in ([None], [7], [{"type": "thread.started", "thread_id": None}]):
            with self.subTest(events=events), self.assertRaises(Refused):
                self.parse(events)

    def test_scalar_final_refused(self):
        records = self.events()
        records[1]["item"]["text"] = "null"
        with self.assertRaises(Refused):
            self.parse(records)


if __name__ == "__main__":
    unittest.main()

