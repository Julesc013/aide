"""A separate durable broker ledger; unknown effects retain the target writer."""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sqlite3

from .common import Refused, canonical, digest, require_path


class Ledger:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        for name in ("broker.sqlite3", "broker.sqlite3-wal", "broker.sqlite3-shm"):
            require_path(str(self.root / name))
        self.db = sqlite3.connect(self.root / "broker.sqlite3", isolation_level=None, timeout=10)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        version = self.db.execute("PRAGMA user_version").fetchone()[0]
        if version not in (0, 1):
            self.db.close()
            raise Refused("unsupported broker ledger version")
        self.db.executescript("""
          CREATE TABLE IF NOT EXISTS requests(
            digest TEXT PRIMARY KEY, task TEXT UNIQUE NOT NULL,
            repository TEXT NOT NULL, target TEXT NOT NULL, authority TEXT NOT NULL,
            request TEXT NOT NULL, manifest TEXT NOT NULL, stage TEXT NOT NULL,
            receipt TEXT);
          CREATE UNIQUE INDEX IF NOT EXISTS target_writer ON requests(repository,target)
            WHERE stage != 'integrated';
          CREATE TABLE IF NOT EXISTS events(
            sequence INTEGER PRIMARY KEY, request TEXT NOT NULL, kind TEXT NOT NULL, body TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS preparations(
            request TEXT NOT NULL, generation TEXT UNIQUE NOT NULL,
            ordinal INTEGER NOT NULL, stage TEXT NOT NULL, identity TEXT,
            PRIMARY KEY(request,ordinal));
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

    def get(self, key):
        row = self.db.execute("SELECT * FROM requests WHERE digest=?", (key,)).fetchone()
        return dict(row) if row else None

    def event(self, key, kind, value):
        self.db.execute("INSERT INTO events(request,kind,body) VALUES(?,?,?)", (key, kind, canonical(value)))

    def reserve(self, request, manifest, authority):
        key = digest(request)
        with self.transaction():
            existing = self.get(key)
            if existing:
                if existing["authority"] != digest(authority) or existing["manifest"] != canonical(manifest):
                    raise Refused("reservation evidence drift")
                return False
            if self.db.execute("SELECT COUNT(*) FROM requests").fetchone()[0] >= authority["max_requests"]:
                raise Refused("broker transaction budget exhausted")
            try:
                self.db.execute("INSERT INTO requests VALUES(?,?,?,?,?,?,?,'reserved',NULL)",
                                (key, request["task"], authority["repository"], authority["target_ref"],
                                 digest(authority), canonical(request), canonical(manifest)))
            except sqlite3.IntegrityError as exc:
                raise Refused("task or target already reserved") from exc
            self.event(key, "reserved", {"authority": digest(authority), "candidate_tree": manifest["candidate_tree"]})
        return True

    def allocate_preparation(self, key, generation):
        with self.transaction():
            row = self.get(key)
            if not row or row["stage"] != "reserved":
                raise Refused("preparation requires a reserved request")
            count = self.db.execute("SELECT COUNT(*) FROM preparations WHERE request=?", (key,)).fetchone()[0]
            if count >= 3:
                raise Refused("preparation generation budget exhausted; retain for diagnosis")
            self.db.execute("INSERT INTO preparations VALUES(?,?,?,'intent',NULL)",
                            (key, generation, count + 1))
            self.event(key, "preparation_intent", {"generation": generation, "ordinal": count + 1})

    def preparation(self, key):
        row = self.db.execute("SELECT * FROM preparations WHERE request=? ORDER BY ordinal DESC LIMIT 1", (key,)).fetchone()
        return dict(row) if row else None

    def prepared(self, key, tree, *, generation=None, directory_identity=None):
        with self.transaction():
            row = self.get(key)
            if not row or row["stage"] != "reserved":
                raise Refused("invalid preparation transition")
            if generation is not None:
                current = self.preparation(key)
                if not current or current["generation"] != generation or current["stage"] != "intent":
                    raise Refused("preparation generation identity mismatch")
                self.db.execute("UPDATE preparations SET stage='prepared',identity=? WHERE generation=?",
                                (canonical(directory_identity), generation))
            self.db.execute("UPDATE requests SET stage='prepared' WHERE digest=?", (key,))
            self.event(key, "prepared", {"tree": tree})

    def intent(self, key):
        with self.transaction():
            row = self.get(key)
            if not row or row["stage"] != "prepared":
                return False
            self.db.execute("UPDATE requests SET stage='apply_intent' WHERE digest=?", (key,))
            self.event(key, "apply_intent", {"request_digest": key})
            return True

    def integrated(self, key, receipt):
        with self.transaction():
            row = self.get(key)
            if not row or row["stage"] not in ("apply_intent", "integrated"):
                raise Refused("integration has no durable intent")
            value = canonical(receipt)
            if row["stage"] == "integrated":
                if row["receipt"] != value:
                    raise Refused("conflicting integration receipt")
                return
            self.db.execute("UPDATE requests SET stage='integrated',receipt=? WHERE digest=?", (value, key))
            self.event(key, "integrated", receipt)
