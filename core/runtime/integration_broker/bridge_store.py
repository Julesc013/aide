"""Bounded registered bridge calls; uncertain Jobs and evidence are retained."""
from contextlib import contextmanager, closing
import json
import sqlite3

from .common import Refused, canonical, digest, require_path


class BridgeStore:
    def __init__(self, root):
        self.root = require_path(str(root))
        for name in ("provider-bridge.sqlite3", "provider-bridge.sqlite3-wal", "provider-bridge.sqlite3-shm"):
            require_path(str(self.root / name))
        self.db = sqlite3.connect(self.root / "provider-bridge.sqlite3", isolation_level=None, timeout=10)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        if self.db.execute("PRAGMA user_version").fetchone()[0] not in (0, 1):
            self.db.close()
            raise Refused("unknown bridge ledger schema")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS registrations(request TEXT PRIMARY KEY, registration TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS calls(id TEXT PRIMARY KEY, request TEXT NOT NULL,
                operation TEXT NOT NULL, attempt INTEGER UNIQUE, body_digest TEXT NOT NULL,
                reserved_bytes INTEGER NOT NULL, stage TEXT NOT NULL, identity TEXT, result TEXT);
            CREATE UNIQUE INDEX IF NOT EXISTS one_mutation ON calls(request,operation) WHERE operation != 'observe';
            PRAGMA user_version=1;
        """)

    def close(self):
        self.db.close()

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def authorized(self, plan, operation, attempt):
        path = require_path(str(self.root / "pr-observations.sqlite3"))
        if not path.is_file():
            raise Refused("provider call has no durable observation ledger")
        with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as db:
            row = db.execute("SELECT plan,stage,latest FROM plans WHERE request=?", (plan["request_digest"],)).fetchone()
            if row is None or row[0] != canonical(plan):
                raise Refused("provider call plan lacks exact durable reservation")
            if operation == "observe":
                if (type(attempt) is not int or attempt <= 0 or not db.execute(
                        "SELECT 1 FROM observation_attempts WHERE sequence=? AND request=?",
                        (attempt, plan["request_digest"])).fetchone()):
                    raise Refused("provider read requires its exact durable attempt token")
            else:
                if operation not in ("publish_objects", "create_branch", "create_pr", "merge") or attempt is not None:
                    raise Refused("unknown provider mutation")
                intent = db.execute("SELECT observation FROM intents WHERE request=? AND operation=?",
                                    (plan["request_digest"], operation)).fetchone()
                if (intent is None or row[1] != operation or row[2] is None or
                        digest(json.loads(row[2])) != intent[0]):
                    raise Refused("provider mutation does not bind current durable stage intent")

    def reserve(self, plan, registration, operation, attempt, call_id, body_digest, reserved_bytes, limits):
        self.authorized(plan, operation, attempt)
        key = plan["request_digest"]
        with self.transaction():
            row = self.db.execute("SELECT registration FROM registrations WHERE request=?", (key,)).fetchone()
            if row is None:
                if self.db.execute("SELECT COUNT(*) FROM registrations").fetchone()[0] >= 2:
                    raise Refused("finite bridge request budget exhausted")
                self.db.execute("INSERT INTO registrations VALUES(?,?)", (key, registration))
            elif row[0] != registration:
                raise Refused("bridge registration changed for a reserved request")
            count, used = self.db.execute("SELECT COUNT(*),COALESCE(SUM(reserved_bytes),0) FROM calls WHERE request=?", (key,)).fetchone()
            if count >= limits["max_calls"] or used + reserved_bytes > limits["max_io_bytes"]:
                raise Refused("finite bridge call or retained IO budget exhausted")
            try:
                self.db.execute("INSERT INTO calls VALUES(?,?,?,?,?,?,'intent',NULL,NULL)",
                                (call_id, key, operation, attempt, body_digest, reserved_bytes))
            except sqlite3.IntegrityError as error:
                raise Refused("provider attempt or mutation cannot be replayed") from error

    def unfinished(self):
        rows = self.db.execute("SELECT * FROM calls WHERE stage='intent' LIMIT 265").fetchall()
        if len(rows) > 264:
            raise Refused("bridge recovery record budget exceeded")
        return [dict(row) for row in rows]

    def owned_directory(self, call_id, identity):
        with self.transaction():
            row = self.db.execute("SELECT identity,stage FROM calls WHERE id=?", (call_id,)).fetchone()
            if row is None or row[1] != "intent" or row[0] is not None:
                raise Refused("bridge call directory binding is not fresh")
            self.db.execute("UPDATE calls SET identity=? WHERE id=?", (canonical(identity), call_id))

    def finish(self, call_id, stage, result):
        if stage not in ("returned", "uncertain"):
            raise Refused("invalid bridge completion state")
        with self.transaction():
            row = self.db.execute("SELECT stage FROM calls WHERE id=?", (call_id,)).fetchone()
            if row is None or row[0] != "intent":
                raise Refused("bridge call completion has no live intent")
            self.db.execute("UPDATE calls SET stage=?,result=? WHERE id=?", (stage, canonical(result), call_id))
