"""Opt-in CLI. No scheduled service or live activation is installed implicitly."""
import argparse
from contextlib import closing
import hashlib
import json
import sqlite3
import time
from pathlib import Path

from .coordinator import Coordinator
from .contract import read_activation, require_path
from .state import Refused, State


def dependency_command(args):
    from .requests import Requests, CONFIG_KEY, MAX_MESSAGE, configuration, decode
    from .state import digest

    root = require_path(str(args.state_root))
    if not root.is_dir():
        raise Refused("dependency state root must already exist and be explicitly owned")
    for suffix in ("", "-wal", "-shm"):
        path = require_path(str(root / ("coordinator.sqlite3" + suffix)))
        if path.exists() and (not path.is_file() or path.stat().st_nlink != 1):
            raise Refused("unsafe coordinator state file")
    database = root / "coordinator.sqlite3"
    wal = (root / "coordinator.sqlite3-wal").exists()
    shm = (root / "coordinator.sqlite3-shm").exists()
    if wal != shm or ((wal or shm) and (not database.exists() or not database.stat().st_size)):
        raise Refused("incomplete WAL state requires explicit reconciliation")

    def preflight(expected, *, initializing=False):
        database = root / "coordinator.sqlite3"
        if not (root / "coordinator.sqlite3-wal").exists() and not (root / "coordinator.sqlite3-shm").exists():
            # A normal read-only WAL open can create sidecars. This committed-
            # page snapshot is ONLY a refusal preflight, never operational truth.
            # Concurrent initialization may conservatively refuse; successful
            # operations revalidate the live DB below before any record change.
            with closing(sqlite3.connect(database.as_uri() + "?mode=ro&immutable=1", uri=True)) as db:
                if db.execute("PRAGMA user_version").fetchone()[0] != 1:
                    raise Refused("unsupported state schema")
                row = db.execute("SELECT value FROM meta WHERE key=?", (CONFIG_KEY,)).fetchone()
                if row is None and not initializing:
                    raise Refused("dependency interface is not initialized")
                if row:
                    config = decode(row[0].encode())
                    configuration(config, root)
                    if digest(config) != expected:
                        raise Refused("configuration digest mismatch")
        elif not ((root / "coordinator.sqlite3-wal").exists() and (root / "coordinator.sqlite3-shm").exists()):
            raise Refused("incomplete WAL state requires explicit reconciliation")

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
            preflight(digest(payload), initializing=True)
            existing = State(root, read_only=True)
            try:
                if existing.db.execute("SELECT 1 FROM meta WHERE key=?", (CONFIG_KEY,)).fetchone():
                    Requests(existing, digest(payload))
            finally:
                existing.close()
    elif not (root / "coordinator.sqlite3").is_file():
        raise Refused("unknown state root; initialize explicitly")
    if args.command != "request-init":
        # Refusal must not initialize schema or alter journaling. Validate the
        # existing database and configuration before constructing any writer.
        preflight(args.configuration_sha256)
        existing = State(root, read_only=True)
        try:
            requests = Requests(existing, args.configuration_sha256)
            if args.command == "request-status":
                return requests.inspect(args.request_id)
        finally:
            existing.close()
    state = State(root)
    try:
        if args.command == "request-init":
            return Requests.initialize(state, payload)
        requests = Requests(state, args.configuration_sha256)
        if args.command == "request-submit":
            return requests.submit(payload)
        return requests.observe(payload)
    finally:
        state.close()


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

