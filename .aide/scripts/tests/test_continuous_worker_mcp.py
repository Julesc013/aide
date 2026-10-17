"""Actual stdio subprocess exchanges; fixture success is not live host delivery."""
import copy
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker.state import State, digest
from core.runtime.continuous_worker.requests import Requests


def reference(name):
    return {"ref": name, "sha256": hashlib.sha256(name.encode()).hexdigest()}


def rpc(number, method, **params):
    return {"jsonrpc": "2.0", "id": number, "method": method, "params": params}


def handshake(version="2025-11-25"):
    return [rpc(1, "initialize", protocolVersion=version, capabilities={},
                clientInfo={"name": "independent-fixture", "version": "1"}),
            {"jsonrpc": "2.0", "method": "notifications/initialized"}]


def call(name, arguments, number=2):
    return rpc(number, "tools/call", name=name, arguments=arguments)


class DependencyMcpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dependency-mcp-")
        self.root = Path(self.temp.name).resolve()
        self.config = {"schema": "aide.dependency-configuration.v1", "state_root": str(self.root),
                       "participants": {name: {"repository": name + "/repo", "owner": name,
                                               "workspace": "fixture/" + name, "host": "fixture",
                                               "session": name, "generation": 1}
                                        for name in ("requester", "receiver", "other", "fourth")},
                       "expires_at": 4102444800, "max_requests": 8, "message_bytes": 65536}
        self.state = State(self.root)
        self.state.bind({"tasks": [{"id": "native", "depends_on": []}]})
        Requests.initialize(self.state, self.config)
        self.request = {"schema": "aide.dependency-request.v1", "id": "change-1", "sender": "requester",
                        "recipient": "receiver", "sender_work": reference("FM-1"),
                        "objective": "Return one verified change", "acceptance": "Consumer checks pass",
                        "references": [reference("base")], "completion": ["validated"]}

    def tearDown(self):
        self.state.close()
        self.temp.cleanup()

    def argv(self, participant="requester", **overrides):
        flags = {"state-root": str(self.root), "configuration-sha256": digest(self.config),
                 "participant": participant,
                 "binding-sha256": digest(self.config["participants"][participant]), **overrides}
        return [sys.executable, "-B", "-m", "core.runtime.continuous_worker.dependency_mcp",
                *[value for key, val in flags.items() for value in ("--" + key, val)]]

    def exchange(self, messages, participant="requester", *, raw=None, exit_code=0, **overrides):
        payload = raw if raw is not None else b"".join(json.dumps(x).encode() + b"\n" for x in messages)
        proc = subprocess.run(self.argv(participant, **overrides), input=payload,
                              capture_output=True, timeout=15, cwd=ROOT)
        self.assertEqual(proc.returncode, exit_code, proc.stderr.decode())
        if not exit_code:
            self.assertEqual(proc.stderr, b"")
        return [json.loads(line) for line in proc.stdout.decode("utf-8").splitlines()]

    def tool(self, name, arguments, participant="requester", *, error=False):
        response = self.exchange(handshake() + [call(name, arguments)], participant)[-1]["result"]
        self.assertEqual(response["isError"], error, response)
        return response["content"][0]["text"] if error else json.loads(response["content"][0]["text"])

    def test_complete_fresh_process_exchange_and_separate_adoption(self):
        native = [tuple(row) for row in self.state.db.execute("SELECT * FROM tasks")]
        self.assertEqual(self.tool("dependency_submit", {"request": self.request})["stage"], "recorded")
        inbox = self.tool("dependency_inbox", {}, "receiver")
        self.assertEqual([x["id"] for x in inbox["requests"]], ["change-1"])
        self.assertEqual(inbox["requests"][0]["stage"], "recorded")
        details = [("delivered", {"receipt": reference("host-observed")}),
                   ("accepted", {"native_work": reference("SETUP-1"), "evidence": [reference("admitted")]}),
                   ("returned", {"subject": reference("commit"), "claims": {"validated": "PASS"},
                                 "evidence": [reference("checks")]})]
        for stage, detail in details:
            returned = self.tool("dependency_observe", {"request_id": "change-1",
                                 "request_sha256": digest(self.request), "stage": stage, "detail": detail}, "receiver")
            self.assertEqual(returned["stage"], stage)
            self.assertFalse(returned["claims_independently_verified"])
            self.assertFalse(returned["execution_authorized"])
        self.assertEqual(returned["next_owner"], "requester")
        final = self.tool("dependency_observe", {"request_id": "change-1", "request_sha256": digest(self.request),
                          "stage": "adopted", "detail": {"returned_sha256": digest(returned["observations"]["returned"]),
                                                         "verification": [reference("consumer")]}})
        self.assertEqual(final["stage"], "adopted")
        self.assertEqual(native, [tuple(row) for row in self.state.db.execute("SELECT * FROM tasks")])
        for table in ("attempts", "effects"):
            self.assertEqual(self.state.db.execute("SELECT COUNT(*) FROM " + table).fetchone()[0], 0)

    def test_lost_reply_and_duplicate_on_fresh_connection_preserve_events(self):
        payload = b"".join(json.dumps(x).encode() + b"\n" for x in handshake() + [call("dependency_submit", {"request": self.request})])
        # Host discards output: durable effect must be discovered, not inferred.
        proc = subprocess.run(self.argv(), input=payload, stdout=subprocess.DEVNULL,
                              stderr=subprocess.PIPE, timeout=15, cwd=ROOT)
        self.assertEqual(proc.returncode, 0)
        count = self.state.db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        self.assertEqual(self.tool("dependency_status", {"request_id": "change-1"})["stage"], "recorded")
        self.tool("dependency_submit", {"request": self.request})
        self.assertEqual(count, self.state.db.execute("SELECT COUNT(*) FROM events").fetchone()[0])
        changed = copy.deepcopy(self.request); changed["objective"] = "Different work"
        self.tool("dependency_submit", {"request": changed}, error=True)

    def test_inbox_pages_filter_uninvolved_requests_without_acknowledging(self):
        for number in range(3):
            request = {**self.request, "id": "change-" + str(number)}
            self.tool("dependency_submit", {"request": request})
        unrelated = {**self.request, "id": "a-other", "sender": "other", "recipient": "fourth"}
        self.tool("dependency_submit", {"request": unrelated}, "other")
        first = self.tool("dependency_inbox", {"limit": 2}, "receiver")
        self.assertEqual([x["id"] for x in first["requests"]], ["change-0", "change-1"])
        self.assertEqual(first["next_cursor"], "change-1")
        second = self.tool("dependency_inbox", {"limit": 2, "after": first["next_cursor"]}, "receiver")
        self.assertEqual([x["id"] for x in second["requests"]], ["change-2"])
        self.assertIsNone(second["next_cursor"])
        self.tool("dependency_status", {"request_id": "a-other"}, "receiver", error=True)
        self.assertEqual({r[0] for r in self.state.db.execute("SELECT stage FROM dependency_requests")}, {"recorded"})

    def test_actor_spoof_and_changed_binding_refused(self):
        self.tool("dependency_submit", {"request": self.request}, "receiver", error=True)
        self.tool("dependency_submit", {"request": self.request, "actor": {"participant": "requester"}}, "receiver", error=True)
        self.assertEqual(self.exchange([], **{"binding-sha256": "0" * 64}, exit_code=2), [])
        self.assertEqual(self.state.db.execute("SELECT COUNT(*) FROM dependency_requests").fetchone()[0], 0)

    def test_pause_and_expiry_allow_reads_but_refuse_changes(self):
        self.tool("dependency_submit", {"request": self.request})
        self.state.control("pause-dispatch")
        self.tool("dependency_submit", {"request": {**self.request, "id": "new"}}, error=True)
        self.assertEqual(self.tool("dependency_inbox", {})["coordinator_mode"], "pause-dispatch")
        # Fixture-only controlled alteration: production configuration is immutable.
        self.config["expires_at"] = 1
        from core.runtime.continuous_worker.state import canonical
        self.state.db.execute("UPDATE meta SET value=? WHERE key='dependency_configuration_v1'", (canonical(self.config),))
        self.assertTrue(self.tool("dependency_status", {"request_id": "change-1"})["configuration_expired"])
        self.tool("dependency_submit", {"request": self.request}, error=True)

    def test_lifecycle_negotiation_methods_and_tool_catalogue(self):
        replies = self.exchange([rpc(0, "tools/list"), *handshake("older-unsupported-version"),
                                 rpc(2, "tools/list"), rpc(3, "ping"), rpc(4, "resources/list"),
                                 rpc(5, "initialize")])
        self.assertIn("error", replies[0])
        self.assertEqual(replies[1]["result"]["protocolVersion"], "2025-11-25")
        self.assertEqual(replies[1]["result"]["capabilities"], {"tools": {}})
        self.assertEqual({t["name"] for t in replies[2]["result"]["tools"]},
                         {"dependency_inbox", "dependency_status", "dependency_submit", "dependency_observe"})
        self.assertEqual(replies[3]["result"], {})
        self.assertEqual(replies[4]["error"]["code"], -32601)
        self.assertIn("error", replies[5])

    def test_notifications_do_not_execute_tools(self):
        notification = call("dependency_submit", {"request": self.request}); notification.pop("id")
        replies = self.exchange(handshake() + [notification, rpc(3, "ping")])
        self.assertEqual([r["id"] for r in replies], [1, 3])
        self.assertEqual(self.state.db.execute("SELECT COUNT(*) FROM dependency_requests").fetchone()[0], 0)

    def test_malformed_utf8_duplicate_keys_and_nonrequest_frames(self):
        raw = b'{"jsonrpc":"2.0","id":1,"id":2,"method":"ping"}\n' + b'\xff\n' + b'[]\n'
        replies = self.exchange([], raw=raw)
        self.assertEqual([x["error"]["code"] for x in replies], [-32700, -32700, -32600])
        invalid = [rpc(True, "ping"), rpc(None, "ping"), {**rpc(1, "ping"), "params": []}]
        self.assertTrue(all("error" in x for x in self.exchange(invalid)))

    def test_oversized_unterminated_frames_terminate_before_effect(self):
        for raw in (b" " * 65537 + b"\n", b'{"jsonrpc":"2.0","id":1,"method":"ping"}'):
            replies = self.exchange([], raw=raw, exit_code=2)
            self.assertEqual(replies[0]["error"]["code"], -32700)

    def test_tool_refusal_is_distinct_from_unknown_method(self):
        self.tool("dependency_status", {"request_id": "unknown"}, error=True)
        self.tool("dependency_inbox", {"limit": 0}, error=True)
        self.tool("dependency_inbox", {"limit": True}, error=True)
        response = self.exchange(handshake() + [call("launch_worker", {})])[-1]
        self.assertEqual(response["error"]["code"], -32602)

    def test_wrong_configuration_and_unknown_database_preserve_bytes(self):
        self.state.close()
        snapshot = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.exchange([], **{"configuration-sha256": "0" * 64}, exit_code=2)
        self.assertEqual(snapshot, {p.name: p.read_bytes() for p in self.root.iterdir()})
        with tempfile.TemporaryDirectory(dir=self.root) as unknown:
            db = Path(unknown) / "coordinator.sqlite3"
            db.write_bytes(b"unrecognized bytes")
            before = {p.name: p.read_bytes() for p in Path(unknown).iterdir()}
            self.exchange([], **{"state-root": unknown}, exit_code=2)
            self.assertEqual(before, {p.name: p.read_bytes() for p in Path(unknown).iterdir()})

    def test_large_valid_history_returns_complete_bounded_subprocess_response(self):
        references = [reference(str(n) + "x" * 1000) for n in range(32)]
        request = {**self.request, "references": references, "objective": "o" * 8192,
                   "acceptance": "a" * 8192}
        self.tool("dependency_submit", {"request": request})
        for stage, detail in [("delivered", {"receipt": reference("delivery")}),
                              ("accepted", {"native_work": reference("native"), "evidence": references}),
                              ("returned", {"subject": reference("commit"), "claims": {"validated": "PASS"},
                                            "evidence": references})]:
            self.tool("dependency_observe", {"request_id": request["id"], "request_sha256": digest(request),
                                            "stage": stage, "detail": detail}, "receiver")
        payload = b"".join(json.dumps(x).encode() + b"\n" for x in handshake() + [call("dependency_status", {"request_id": request["id"]})])
        proc = subprocess.run(self.argv(), input=payload, capture_output=True, timeout=15, cwd=ROOT)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        raw = proc.stdout.splitlines(keepends=True)[-1]
        self.assertGreater(len(raw), 65536)
        self.assertLessEqual(len(raw), 1024 * 1024)
        record = json.loads(json.loads(raw)["result"]["content"][0]["text"])
        self.assertEqual(record["request"], request)
        self.assertEqual(record["observations"]["returned"]["detail"]["evidence"], references)

    def test_oversized_response_reports_uncertain_effect_without_truncation(self):
        from core.runtime.continuous_worker.dependency_mcp import Server
        class OversizedResult:
            def call(self, name, arguments):
                return {"unrepresentable": "x" * (1024 * 1024)}
        source = io.BytesIO(b"".join(json.dumps(x).encode() + b"\n" for x in handshake() + [call("dependency_inbox", {})]))
        output = io.BytesIO()
        self.assertEqual(Server(OversizedResult()).run(source, output), 0)
        response = json.loads(output.getvalue().splitlines()[-1])
        self.assertEqual(response["error"]["code"], -32603)
        self.assertIn("mutation may already be recorded", response["error"]["message"])
        self.assertIn("Reconcile by request ID", response["error"]["message"])
        self.assertNotIn("result", response)


if __name__ == "__main__":
    unittest.main()
