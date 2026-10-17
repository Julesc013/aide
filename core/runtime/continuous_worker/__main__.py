"""Opt-in CLI. No scheduled service or live activation is installed implicitly."""
import argparse
import hashlib
import json
import sqlite3
import time
from pathlib import Path

from .coordinator import Coordinator
from .contract import read_activation
from .state import Refused, State


def dependency_command(args):
    from .requests import Requests, CONFIG_KEY, MAX_MESSAGE, configuration, decode
    from .state import digest

    from .request_access import checked_root, preflight, open_requests

    root = checked_root(args.state_root)
    payload = None
    if args.command != "request-status":
        with args.input.open("rb") as src:
            raw = src.read(MAX_MESSAGE + 1)
        payload = decode(raw)
    if args.command == "request-init":
        if hashlib.sha256(raw).hexdigest() != args.sha256:
            raise Refused("configuration input digest mismatch")
        configuration(payload, root)
        if time.time() >= payload["expires_at"]:
            raise Refused("configuration expired")
        database = root / "coordinator.sqlite3"
        if database.exists() and database.stat().st_size:
            preflight(root, digest(payload), initializing=True)
            existing = State(root, read_only=True)
            try:
                if existing.db.execute("SELECT 1 FROM meta WHERE key=?", (CONFIG_KEY,)).fetchone():
                    Requests(existing, digest(payload))
            finally:
                existing.close()
        state = State(root)
        try:
            return Requests.initialize(state, payload)
        finally:
            state.close()
    with open_requests(root, args.configuration_sha256,
                       write=args.command != "request-status") as requests:
        if args.command == "request-status":
            return requests.inspect(args.request_id)
        if args.command == "request-submit":
            return requests.submit(payload)
        return requests.observe(payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("request-init", "request-submit", "request-observe", "request-status"):
        p = sub.add_parser(name, help="cooperative local records; no worker dispatch")
        p.add_argument("--state-root", type=Path, required=True)
        if name == "request-init":
            p.add_argument("--sha256", required=True)
        else:
            p.add_argument("--configuration-sha256", required=True)
        if name == "request-status":
            p.add_argument("--request-id", required=True)
        else:
            p.add_argument("--input", type=Path, required=True)
    for name in ("preflight", "run"):
        p = sub.add_parser(name)
        p.add_argument("--activation", type=Path, required=True)
        p.add_argument("--approval-sha256", required=True)
    for name in ("status", "pause-dispatch", "drain", "resume", "emergency-stop", "cancel-task"):
        p = sub.add_parser(name)
        p.add_argument("--state-root", type=Path, required=True)
        if name == "cancel-task":
            p.add_argument("--task", required=True)
    args = parser.parse_args()
    try:
        if args.command.startswith("request-"):
            result = dependency_command(args)
        elif args.command == "preflight":
            read_activation(args.activation, args.approval_sha256)
            result = {"configuration": "valid", "dispatch": False,
                      "qualification": "external host and integration evidence still authoritative"}
        elif args.command == "run":
            runner = Coordinator(args.activation, args.approval_sha256)
            try:
                result = runner.run()
            finally:
                runner.state.close()
        else:
            if not (args.state_root / "coordinator.sqlite3").is_file():
                raise Refused("unknown state root; operator commands never initialize state")
            state = State(args.state_root)
            try:
                if args.command != "status":
                    state.control(args.command, getattr(args, "task", None))
                result = state.status()
            finally:
                state.close()
        print(json.dumps(result, indent=2))
        return 0
    except (Refused, OSError, ValueError, KeyError, sqlite3.Error) as exc:
        print(json.dumps({"result": "refused", "reason": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

