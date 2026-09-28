"""One supported worker interface: Codex exec JSONL plus a strict final schema."""
from __future__ import annotations

import json
from pathlib import Path
import uuid

from .state import Refused

SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["pass", "blocked", "fail"]},
        "summary": {"type": "string"},
        "subject_identity": {"type": "string"},
        "findings": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["status", "summary", "subject_identity", "findings"],
    "additionalProperties": False,
}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Refused("duplicate JSON object key in worker result")
        result[key] = value
    return result


def argv(command, workspace, schema, *, assurance=False, session_id=None, model=None):
    # Never --last, --full-auto, approval bypass, shell interpolation or API key injection.
    args = [*command, "exec"]
    if session_id is not None:
        if str(uuid.UUID(session_id)) != session_id:
            raise Refused("resume requires an explicit canonical session UUID")
        args += ["resume", session_id]
    else:
        args += ["--cd", str(workspace), "--sandbox", "read-only" if assurance else "workspace-write"]
    if model is not None:
        args += ["--model", model]
    args += ["--ignore-user-config", "--json", "--output-schema", str(schema),
             "-c", 'approval_policy="never"', "-c", 'forced_login_method="chatgpt"',
             "-c", 'shell_environment_policy.inherit="core"',
             "-c", 'shell_environment_policy.ignore_default_excludes=false',
             "-c", 'agents.enabled=false', "-c", 'features.multi_agent=false',
             "-c", 'features.apps=false', "-c", 'features.hooks=false',
             "-c", 'features.remote_plugin=false', "-c", 'web_search="disabled"', "-"]
    return args


def parse_events(path, expected_identity):
    session = None
    started = False
    completed = False
    failed = False
    last_message = None
    usage = {}
    with Path(path).open(encoding="utf-8") as source:
        for line in source:
            if not line.strip():
                continue
            try:
                event = json.loads(line, object_pairs_hook=_unique_object)
            except (ValueError, TypeError) as exc:
                raise Refused("malformed Codex event stream") from exc
            if not isinstance(event, dict) or not isinstance(event.get("item", {}), dict):
                raise Refused("Codex events must be objects")
            kind = event.get("type")
            if kind == "thread.started":
                if session is not None or started:
                    raise Refused("multiple worker sessions in one invocation")
                if not isinstance(event.get("thread_id"), str):
                    raise Refused("worker session identity must be a UUID string")
                try:
                    session = str(uuid.UUID(event["thread_id"]))
                except ValueError as exc:
                    raise Refused("worker session identity is not a UUID") from exc
                if session != event["thread_id"]:
                    raise Refused("worker session identity is not canonical")
            elif kind == "turn.started":
                if session is None or started or completed:
                    raise Refused("worker turn start is missing or duplicated")
                started = True
            elif kind == "turn.completed":
                if session is None or not started or completed:
                    raise Refused("worker turn completion is missing or duplicated")
                if not isinstance(event.get("usage", {}), dict):
                    raise Refused("worker turn usage is not an object")
                completed = True
                usage = event.get("usage", {})
            elif kind in ("turn.failed", "error"):
                failed = True
            elif isinstance(kind, str) and kind.startswith("item."):
                if not started or completed:
                    raise Refused("worker item is outside the active turn")
                last_message = None
                if kind == "item.completed" and event["item"].get("type") == "agent_message":
                    last_message = event["item"].get("text")
    if not session or not started or not completed or failed or last_message is None:
        raise Refused("worker did not produce a completed session")
    try:
        result = json.loads(last_message, object_pairs_hook=_unique_object)
    except (ValueError, TypeError) as exc:
        raise Refused("worker final message violates result schema") from exc
    if (not isinstance(result, dict) or set(result) != set(SCHEMA["required"]) or result["status"] not in ("pass", "blocked", "fail")
            or not isinstance(result["summary"], str) or not isinstance(result["findings"], list)
            or any(not isinstance(f, str) for f in result["findings"])):
        raise Refused("worker result schema mismatch")
    if result["subject_identity"] != expected_identity:
        raise Refused("worker verdict is not bound to the observed subject")
    return {"session_id": session, "result": result, "usage": usage}
