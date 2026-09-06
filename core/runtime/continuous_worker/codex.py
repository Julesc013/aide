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
    completed = False
    failed = False
    last_message = None
    usage = {}
    with Path(path).open(encoding="utf-8") as source:
        for line in source:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except (ValueError, TypeError) as exc:
                raise Refused("malformed Codex event stream") from exc
            if not isinstance(event, dict) or not isinstance(event.get("item", {}), dict):
                raise Refused("Codex events must be objects")
            kind = event.get("type")
            if kind == "thread.started":
                if session is not None:
                    raise Refused("multiple worker sessions in one invocation")
                if not isinstance(event.get("thread_id"), str):
                    raise Refused("worker session identity must be a UUID string")
                session = str(uuid.UUID(event["thread_id"]))
            elif kind == "turn.completed":
                completed = True
                usage = event.get("usage", {})
            elif kind in ("turn.failed", "error"):
                failed = True
            elif kind == "item.completed" and event.get("item", {}).get("type") == "agent_message":
                last_message = event["item"].get("text")
    if not session or not completed or failed or last_message is None:
        raise Refused("worker did not produce a completed session")
    try:
        result = json.loads(last_message)
    except (ValueError, TypeError) as exc:
        raise Refused("worker final message violates result schema") from exc
    if (not isinstance(result, dict) or set(result) != set(SCHEMA["required"]) or result["status"] not in ("pass", "blocked", "fail")
            or not isinstance(result["summary"], str) or not isinstance(result["findings"], list)
            or any(not isinstance(f, str) for f in result["findings"])):
        raise Refused("worker result schema mismatch")
    if result["subject_identity"] != expected_identity:
        raise Refused("worker verdict is not bound to the observed subject")
    return {"session_id": session, "result": result, "usage": usage}

