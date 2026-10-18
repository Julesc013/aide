"""Opt-in MCP 2025-11-25 stdio tools over cooperative local dependency records.

No host wake-up, task execution, live initialization or authentication is implied.
Keep this bounded transport replaceable; Requests owns every lifecycle rule.
"""
import argparse
import json
from pathlib import Path
import sqlite3
import sys

from .request_access import open_requests
from .requests import CANCELLATION, DISPOSITIONS, MAX_MESSAGE, OBLIGATIONS, STAGES, decode, fields
from .state import Refused

VERSION = "2025-11-25"
MAX_RESPONSE = 1024 * 1024


def object_schema(properties, required=None):
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": False}


REFERENCE = object_schema({"ref": {"type": "string"}, "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}})
REFERENCES = {"type": "array", "minItems": 1, "maxItems": 32, "items": REFERENCE}
REQUEST = object_schema({
    "schema": {"const": "aide.dependency-request.v1"},
    **{key: {"type": "string"} for key in ("id", "sender", "recipient", "objective", "acceptance")},
    "sender_work": REFERENCE, "references": REFERENCES,
    "completion": {"type": "array", "minItems": 1, "uniqueItems": True,
                   "items": {"enum": sorted(OBLIGATIONS)}}})
DETAIL = {"oneOf": [object_schema({"receipt": REFERENCE}),
                    object_schema({"native_work": REFERENCE, "evidence": REFERENCES}),
                    object_schema({"subject": REFERENCE, "claims": {"type": "object",
                                   "additionalProperties": {"enum": ["PASS", "FAILED", "NOT_RUN", "UNKNOWN"]}},
                                   "evidence": REFERENCES}),
                    object_schema({"returned_sha256": {"type": "string"}, "verification": REFERENCES}),
                    object_schema({"expected_stage": {"enum": list(STAGES[:-1])},
                                   "reason": {"type": "string"}, "evidence": REFERENCES}),
                    object_schema({"cancellation_sha256": {"type": "string"},
                                   "disposition": {"enum": list(DISPOSITIONS)}, "evidence": REFERENCES})]}

TOOLS = [
    {"name": "dependency_inbox", "description": "List this participant's requests; reading does not acknowledge delivery.",
     "inputSchema": object_schema({"after": {"type": "string"},
                                   "limit": {"type": "integer", "minimum": 1, "maximum": 16}}, []),
     "annotations": {"readOnlyHint": True, "openWorldHint": False}},
    {"name": "dependency_status", "description": "Read one involved request, its reported evidence and next action.",
     "inputSchema": object_schema({"request_id": {"type": "string"}}),
     "annotations": {"readOnlyHint": True, "openWorldHint": False}},
    {"name": "dependency_submit", "description": "Record an immutable dependency request as the bound sender; no execution grant.",
     "inputSchema": object_schema({"request": REQUEST}),
     "annotations": {"readOnlyHint": False, "destructiveHint": False,
                     "idempotentHint": True, "openWorldHint": False}},
    {"name": "dependency_observe", "description": "Record a revision-bound lifecycle observation. Cancellation requires v2 configuration; acknowledgement does not stop processes or verify claims.",
     "inputSchema": object_schema({"request_id": {"type": "string"}, "request_sha256": {"type": "string"},
                                   "stage": {"enum": [*STAGES[1:], *CANCELLATION]},
                                   "detail": DETAIL}),
     "annotations": {"readOnlyHint": False, "destructiveHint": False,
                     "idempotentHint": True, "openWorldHint": False}},
]


class DependencyTools:
    def __init__(self, root, configuration_sha256, participant, binding_sha256):
        self.root, self.configuration_sha256 = root, configuration_sha256
        self.actor = {"participant": participant, "binding_sha256": binding_sha256}
        with self.open():
            pass

    def open(self, *, write=False):
        return open_requests(self.root, self.configuration_sha256, write=write, actor=self.actor)

    def call(self, name, arguments):
        if not isinstance(arguments, dict):
            raise Refused("tool arguments must be an object")
        with self.open(write=name in ("dependency_submit", "dependency_observe")) as requests:
            if name == "dependency_inbox":
                if set(arguments) - {"after", "limit"}:
                    raise Refused("unknown inbox argument")
                return requests.inbox(self.actor, **arguments)
            if name == "dependency_status":
                fields(arguments, "request_id")
                result = requests.inspect(arguments["request_id"])
                if self.actor["participant"] not in (result["request"]["sender"], result["request"]["recipient"]):
                    raise Refused("request is outside this participant binding")
                return result
            if name == "dependency_submit":
                fields(arguments, "request")
                return requests.submit({"actor": self.actor, "request": arguments["request"]})
            if name == "dependency_observe":
                fields(arguments, "request_id request_sha256 stage detail")
                return requests.observe({**arguments, "actor": self.actor})
            raise Refused("unknown dependency tool")


class ProtocolError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message


class Server:
    def __init__(self, tools):
        self.tools = tools
        self.initialized = self.ready = False

    def handle(self, message):
        valid_id = lambda x: type(x) is int or isinstance(x, str)
        if (not isinstance(message, dict) or message.get("jsonrpc") != "2.0"
                or not isinstance(message.get("method"), str)
                or set(message) - {"jsonrpc", "id", "method", "params"}
                or ("id" in message and not valid_id(message["id"]))):
            return self.error(None, -32600, "Invalid Request")
        method = message["method"]
        # Notifications never execute tools and never receive a response.
        if "id" not in message:
            if method == "notifications/initialized" and self.initialized:
                self.ready = True
            return None
        request_id = message["id"]
        try:
            params = message.get("params", {})
            if not isinstance(params, dict):
                raise ProtocolError(-32602, "params must be an object")
            if method == "ping":
                result = {}
            elif method == "initialize":
                if self.initialized:
                    raise ProtocolError(-32600, "Already initialized")
                info = params.get("clientInfo")
                if (not isinstance(params.get("protocolVersion"), str)
                        or not isinstance(params.get("capabilities"), dict)
                        or not isinstance(info, dict)
                        or not all(isinstance(info.get(key), str) for key in ("name", "version"))):
                    raise ProtocolError(-32602, "Invalid initialization parameters")
                self.initialized = True
                result = {"protocolVersion": VERSION, "capabilities": {"tools": {}},
                          "serverInfo": {"name": "aide-local-dependencies", "version": "0.1.0"},
                          "instructions": "Cooperative records only. Inbox reads do not acknowledge. Reported claims are not independently verified; requests grant no execution authority."}
            elif not self.ready:
                raise ProtocolError(-32000, "Initialize and send notifications/initialized first")
            elif method == "tools/list":
                if set(params) - {"_meta"}:
                    raise ProtocolError(-32602, "This bounded catalogue has no cursor")
                result = {"tools": TOOLS}
            elif method == "tools/call":
                if (set(params) - {"name", "arguments", "_meta"}
                        or params.get("name") not in [tool["name"] for tool in TOOLS]):
                    raise ProtocolError(-32602, "Unknown tool or call parameter")
                try:
                    value = self.tools.call(params["name"], params.get("arguments", {}))
                    result = {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}], "isError": False}
                except (Refused, OSError, ValueError, KeyError, TypeError, sqlite3.Error) as exc:
                    result = {"content": [{"type": "text", "text": str(exc)}], "isError": True}
            else:
                raise ProtocolError(-32601, "Method not found")
            return {"jsonrpc": "2.0", "id": request_id, "result": result}
        except ProtocolError as exc:
            return self.error(request_id, exc.code, exc.message)

    @staticmethod
    def error(request_id, code, message):
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}

    def run(self, source, destination):
        def emit(value):
            if value is not None:
                raw = json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8") + b"\n"
                if len(raw) > MAX_RESPONSE:
                    value = self.error(value.get("id"), -32603,
                                       "Response exceeds outgoing limit; mutation may already be recorded. Reconcile by request ID before retry.")
                    raw = json.dumps(value).encode("utf-8") + b"\n"
                destination.write(raw)
                destination.flush()
        while True:
            raw = source.readline(MAX_MESSAGE + 1)
            if not raw:
                return 0
            if len(raw) > MAX_MESSAGE or not raw.endswith(b"\n"):
                emit(self.error(None, -32700, "Oversized or unterminated frame; reconnect and inspect by ID"))
                return 2
            try:
                # JSON's permissive byte decoder also accepts UTF-16; MCP does not.
                message = decode(raw.decode("utf-8").encode("utf-8"))
            except (Refused, UnicodeError):
                emit(self.error(None, -32700, "Parse error"))
                continue
            emit(self.handle(message))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-root", type=Path, required=True)
    parser.add_argument("--configuration-sha256", required=True)
    parser.add_argument("--participant", required=True)
    parser.add_argument("--binding-sha256", required=True)
    args = parser.parse_args()
    try:
        tools = DependencyTools(args.state_root, args.configuration_sha256, args.participant, args.binding_sha256)
        return Server(tools).run(sys.stdin.buffer, sys.stdout.buffer)
    except (Refused, OSError, ValueError, KeyError, sqlite3.Error) as exc:
        print("Dependency adapter refused: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
