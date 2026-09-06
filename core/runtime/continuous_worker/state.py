"""Durable operational state. Admissions remain external, immutable source references."""
from __future__ import annotations

import contextlib
import hashlib
import json
import sqlite3
import time
import uuid
from pathlib import Path


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


class Refused(RuntimeError):
    pass


class State:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.root / "coordinator.sqlite3", timeout=10, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute("PRAGMA foreign_keys=ON")
        version = self.db.execute("PRAGMA user_version").fetchone()[0]
        if version not in (0, 1):
            self.db.close()
            raise Refused("unsupported state schema")
        self.db.executescript("""
          CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY, spec TEXT NOT NULL,
            digest TEXT NOT NULL, status TEXT NOT NULL, reason TEXT NOT NULL DEFAULT '');
          CREATE TABLE IF NOT EXISTS attempts(id TEXT PRIMARY KEY, task TEXT NOT NULL REFERENCES tasks(id),
            stage TEXT NOT NULL, started REAL NOT NULL, updated REAL NOT NULL,
            evidence TEXT NOT NULL, fingerprint TEXT NOT NULL DEFAULT '');
          CREATE UNIQUE INDEX IF NOT EXISTS one_unresolved_attempt ON attempts((1))
            WHERE stage NOT IN ('succeeded','blocked','cancelled');
          CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY, at REAL NOT NULL,
            attempt TEXT, kind TEXT NOT NULL, body TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS effects(id TEXT PRIMARY KEY, attempt TEXT NOT NULL REFERENCES attempts(id),
            kind TEXT NOT NULL, status TEXT NOT NULL, request TEXT NOT NULL, response TEXT);
          CREATE UNIQUE INDEX IF NOT EXISTS one_effect_per_phase ON effects(attempt,kind);
          CREATE TABLE IF NOT EXISTS controls(seq INTEGER PRIMARY KEY, at REAL NOT NULL,
            kind TEXT NOT NULL, task TEXT);
          PRAGMA user_version=1;
        """)

    def close(self):
        self.db.close()

    @contextlib.contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def event(self, attempt, kind, body):
        self.db.execute("INSERT INTO events(at,attempt,kind,body) VALUES(?,?,?,?)",
                        (time.time(), attempt, kind, canonical(body)))

    def bind(self, activation):
        pin = digest(activation)
        with self.transaction():
            old = self.db.execute("SELECT value FROM meta WHERE key='activation'").fetchone()
            if old and old[0] != pin:
                raise Refused("activation changed; existing ledger is bound to its original authority")
            self.db.execute("INSERT OR IGNORE INTO meta VALUES('activation',?)", (pin,))
            for spec in activation["tasks"]:
                value = canonical(spec)
                old = self.db.execute("SELECT digest FROM tasks WHERE id=?", (spec["id"],)).fetchone()
                if old and old[0] != digest(spec):
                    raise Refused("admission changed")
                self.db.execute("INSERT OR IGNORE INTO tasks(id,spec,digest,status) VALUES(?,?,?,'ready')",
                                (spec["id"], value, digest(spec)))

    def control(self, kind, task=None):
        if kind not in ("resume", "pause-dispatch", "drain", "cancel-task", "emergency-stop"):
            raise Refused("unknown operator control")
        if (kind == "cancel-task") != bool(task):
            raise Refused("only cancel-task requires a task id")
        with self.transaction():
            if task and not self.db.execute("SELECT 1 FROM tasks WHERE id=?", (task,)).fetchone():
                raise Refused("unknown task")
            self.db.execute("INSERT INTO controls(at,kind,task) VALUES(?,?,?)", (time.time(), kind, task))
            if kind == "cancel-task":
                self.db.execute("UPDATE tasks SET status='cancelled',reason='operator cancellation' WHERE id=? AND status='ready'", (task,))
            self.event(None, "operator_control", {"kind": kind, "task": task})

    def mode(self):
        row = self.db.execute("SELECT kind FROM controls WHERE task IS NULL ORDER BY seq DESC LIMIT 1").fetchone()
        return row[0] if row else "resume"

    def cancelled(self, task):
        return self.mode() == "emergency-stop" or bool(self.db.execute(
            "SELECT 1 FROM controls WHERE kind='cancel-task' AND task=?", (task,)).fetchone())

    def claim(self, max_attempts):
        with self.transaction():
            if self.mode() != "resume":
                return None
            if self.db.execute("SELECT 1 FROM attempts WHERE stage NOT IN ('succeeded','blocked','cancelled')").fetchone():
                return None
            if self.db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0] >= max_attempts:
                return None
            for row in self.db.execute("SELECT * FROM tasks WHERE status='ready' ORDER BY rowid").fetchall():
                spec = json.loads(row["spec"])
                deps = [self.db.execute("SELECT status FROM tasks WHERE id=?", (d,)).fetchone() for d in spec["depends_on"]]
                if any(d is None or d[0] != "succeeded" for d in deps):
                    continue
                attempt = uuid.uuid4().hex
                now = time.time()
                self.db.execute("INSERT INTO attempts VALUES(?,?,?,?,?,?,?)",
                                (attempt, row["id"], "claimed", now, now, "{}", ""))
                self.db.execute("UPDATE tasks SET status='running' WHERE id=? AND status='ready'", (row["id"],))
                self.event(attempt, "claimed", {"admission": row["digest"]})
                return {"id": attempt, "task": row["id"], "spec": spec}
        return None

    def active(self):
        row = self.db.execute("SELECT * FROM attempts WHERE stage NOT IN ('succeeded','blocked','cancelled')").fetchone()
        return dict(row) if row else None

    def transition(self, attempt, stage, evidence):
        with self.transaction():
            row = self.db.execute("SELECT stage,evidence FROM attempts WHERE id=?", (attempt,)).fetchone()
            if row is None or row["stage"] in ("succeeded", "blocked", "cancelled"):
                raise Refused("attempt is not active")
            merged = json.loads(row["evidence"]) | evidence
            self.db.execute("UPDATE attempts SET stage=?,updated=?,evidence=? WHERE id=?",
                            (stage, time.time(), canonical(merged), attempt))
            self.event(attempt, stage, evidence)
            if stage in ("succeeded", "blocked", "cancelled"):
                unresolved = self.db.execute("SELECT 1 FROM effects WHERE attempt=? AND status='intent'", (attempt,)).fetchone()
                if unresolved:
                    raise Refused("unreconciled effect cannot release the writer")
                self.db.execute("UPDATE tasks SET status=?,reason=? WHERE id=(SELECT task FROM attempts WHERE id=?)",
                                (stage, evidence.get("reason", ""), attempt))

    def intent(self, attempt, kind, request):
        effect = uuid.uuid4().hex
        with self.transaction():
            self.db.execute("INSERT INTO effects VALUES(?,?,?,'intent',?,NULL)",
                            (effect, attempt, kind, canonical(request)))
            self.event(attempt, "effect_intent", {"id": effect, "kind": kind, "request": request})
        return effect

    def observed(self, effect, response):
        with self.transaction():
            row = self.db.execute("SELECT attempt,status,response FROM effects WHERE id=?", (effect,)).fetchone()
            if not row:
                raise Refused("unknown effect")
            if row["status"] == "observed":
                if row["response"] != canonical(response):
                    raise Refused("conflicting observation")
                return
            self.db.execute("UPDATE effects SET status='observed',response=? WHERE id=?",
                            (canonical(response), effect))
            self.event(row["attempt"], "effect_observed", {"id": effect, "response": response})

    def unresolved(self):
        return [dict(r) for r in self.db.execute("SELECT * FROM effects WHERE status='intent' ORDER BY rowid")]

    def status(self):
        return {"mode": self.mode(), "active": self.active(),
                "tasks": [dict(r) for r in self.db.execute("SELECT id,status,reason FROM tasks")],
                "unresolved_effects": self.unresolved(),
                "events": self.db.execute("SELECT COUNT(*) FROM events").fetchone()[0]}

