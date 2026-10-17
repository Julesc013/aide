"""Shared conservative access to an explicitly initialized local request ledger."""
from contextlib import closing, contextmanager
import sqlite3

from .contract import require_path
from .requests import CONFIG_KEY, Requests, configuration, decode
from .state import Refused, State, digest


def checked_root(value):
    root = require_path(str(value))
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
    return root


def preflight(root, expected, *, initializing=False):
    database = root / "coordinator.sqlite3"
    if not database.is_file():
        raise Refused("unknown state root; initialize explicitly")
    if not (root / "coordinator.sqlite3-wal").exists() and not (root / "coordinator.sqlite3-shm").exists():
        # Committed pages are ONLY a refusal preflight. A live open below must
        # revalidate before any operational result or writer is made available.
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


@contextmanager
def open_requests(value, expected, *, write=False, actor=None):
    root = checked_root(value)
    preflight(root, expected)
    state = State(root, read_only=True)
    try:
        requests = Requests(state, expected)
        if actor is not None:
            requests.actor(actor, actor["participant"])
        if not write:
            yield requests
            return
    finally:
        state.close()
    # Repeat path/config/binding checks for each call; never keep a stale live
    # connection or infer a new binding from an expired heartbeat.
    checked_root(root)
    state = State(root)
    try:
        requests = Requests(state, expected)
        if actor is not None:
            requests.actor(actor, actor["participant"])
        yield requests
    finally:
        state.close()
