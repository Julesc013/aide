"""SQLite store for the local AIDE Service foundation v0."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import migrations


DETERMINISTIC_TIMESTAMP = "2026-06-25T00:00:00+10:00"


class LocalServiceError(ValueError):
    """Raised for fail-closed local service refusals."""


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_json(data: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class StoredObject:
    ref: str
    kind: str
    version: int
    body: dict[str, Any]
    body_digest: str


class SQLiteStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path.resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.conn = sqlite3.connect(str(self.db_path))
        except sqlite3.Error as exc:
            raise LocalServiceError("database_open_failed") from exc
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys=ON")

    def close(self) -> None:
        self.conn.close()

    def initialize(self) -> int:
        try:
            return migrations.apply_migrations(self.conn, applied_at=DETERMINISTIC_TIMESTAMP)
        except ValueError as exc:
            raise LocalServiceError(str(exc)) from exc
        except sqlite3.Error as exc:
            raise LocalServiceError("migration_failed") from exc

    def force_schema_version_for_test(self, version: int) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO migrations(version, applied_at) VALUES (?, ?)",
                (version, DETERMINISTIC_TIMESTAMP),
            )

    def health(self) -> dict[str, Any]:
        try:
            version = migrations.installed_schema_version(self.conn)
            self.conn.execute("SELECT 1").fetchone()
        except sqlite3.Error as exc:
            raise LocalServiceError("health_check_failed") from exc
        if version > migrations.CURRENT_SCHEMA_VERSION:
            raise LocalServiceError("future_migration")
        return {
            "status": "PASS",
            "database_opened": True,
            "schema_version": version,
            "single_writer": True,
            "network_listener_opened": False,
        }

    def put_object(self, ref: str, kind: str, body: dict[str, Any], *, expected_version: int | None = None) -> StoredObject:
        body_json = canonical_json(body)
        body_digest = digest_json(body)
        with self.conn:
            row = self.conn.execute("SELECT version FROM objects WHERE ref = ?", (ref,)).fetchone()
            if row is None:
                if expected_version not in (None, 0):
                    raise LocalServiceError("resource_version_conflict")
                version = 1
                self.conn.execute(
                    "INSERT INTO objects(ref, kind, version, body_json, body_digest, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (ref, kind, version, body_json, body_digest, DETERMINISTIC_TIMESTAMP),
                )
            else:
                current = int(row["version"])
                if expected_version is not None and expected_version != current:
                    raise LocalServiceError("resource_version_conflict")
                version = current + 1
                self.conn.execute(
                    "UPDATE objects SET kind = ?, version = ?, body_json = ?, body_digest = ?, updated_at = ? WHERE ref = ?",
                    (kind, version, body_json, body_digest, DETERMINISTIC_TIMESTAMP, ref),
                )
        return StoredObject(ref, kind, version, body, body_digest)

    def get_object(self, ref: str) -> StoredObject:
        row = self.conn.execute("SELECT * FROM objects WHERE ref = ?", (ref,)).fetchone()
        if row is None:
            raise LocalServiceError("object_missing")
        body = json.loads(row["body_json"])
        return StoredObject(row["ref"], row["kind"], int(row["version"]), body, row["body_digest"])

    def list_objects(self, *, kind: str | None = None) -> list[StoredObject]:
        if kind is None:
            rows = self.conn.execute("SELECT * FROM objects ORDER BY ref").fetchall()
        else:
            rows = self.conn.execute("SELECT * FROM objects WHERE kind = ? ORDER BY ref", (kind,)).fetchall()
        return [
            StoredObject(row["ref"], row["kind"], int(row["version"]), json.loads(row["body_json"]), row["body_digest"])
            for row in rows
        ]

    def append_event(self, event_ref: str, event_type: str, subject_ref: str, body: dict[str, Any]) -> int:
        body_json = canonical_json(body)
        body_digest = digest_json(body)
        try:
            with self.conn:
                cur = self.conn.execute(
                    "INSERT INTO events(event_ref, event_type, subject_ref, body_json, body_digest, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (event_ref, event_type, subject_ref, body_json, body_digest, DETERMINISTIC_TIMESTAMP),
                )
            return int(cur.lastrowid)
        except sqlite3.IntegrityError as exc:
            raise LocalServiceError("event_duplicate") from exc

    def put_object_with_event(
        self,
        ref: str,
        kind: str,
        body: dict[str, Any],
        *,
        event_ref: str,
        event_type: str,
        expected_version: int | None = None,
        fail_after_object: bool = False,
    ) -> tuple[StoredObject, int]:
        body_json = canonical_json(body)
        body_digest = digest_json(body)
        try:
            with self.conn:
                row = self.conn.execute("SELECT version FROM objects WHERE ref = ?", (ref,)).fetchone()
                if row is None:
                    if expected_version not in (None, 0):
                        raise LocalServiceError("resource_version_conflict")
                    version = 1
                    self.conn.execute(
                        "INSERT INTO objects(ref, kind, version, body_json, body_digest, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (ref, kind, version, body_json, body_digest, DETERMINISTIC_TIMESTAMP),
                    )
                else:
                    current = int(row["version"])
                    if expected_version is not None and expected_version != current:
                        raise LocalServiceError("resource_version_conflict")
                    version = current + 1
                    self.conn.execute(
                        "UPDATE objects SET kind = ?, version = ?, body_json = ?, body_digest = ?, updated_at = ? WHERE ref = ?",
                        (kind, version, body_json, body_digest, DETERMINISTIC_TIMESTAMP, ref),
                    )
                if fail_after_object:
                    raise LocalServiceError("injected_atomic_failure")
                cur = self.conn.execute(
                    "INSERT INTO events(event_ref, event_type, subject_ref, body_json, body_digest, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (event_ref, event_type, ref, body_json, body_digest, DETERMINISTIC_TIMESTAMP),
                )
            return StoredObject(ref, kind, version, body, body_digest), int(cur.lastrowid)
        except sqlite3.IntegrityError as exc:
            raise LocalServiceError("event_duplicate") from exc

    def read_events_after(self, sequence: int, *, limit: int = 100) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT * FROM events WHERE sequence > ? ORDER BY sequence LIMIT ?",
            (sequence, limit),
        ).fetchall()
        return [
            {
                "sequence": int(row["sequence"]),
                "event_ref": row["event_ref"],
                "event_type": row["event_type"],
                "subject_ref": row["subject_ref"],
                "body": json.loads(row["body_json"]),
                "body_digest": row["body_digest"],
            }
            for row in rows
        ]

    def ack_cursor(self, cursor_ref: str, last_sequence: int) -> dict[str, Any]:
        with self.conn:
            self.conn.execute(
                "INSERT INTO cursors(cursor_ref, last_sequence, updated_at) VALUES (?, ?, ?) "
                "ON CONFLICT(cursor_ref) DO UPDATE SET last_sequence = excluded.last_sequence, updated_at = excluded.updated_at",
                (cursor_ref, last_sequence, DETERMINISTIC_TIMESTAMP),
            )
        return {"cursor_ref": cursor_ref, "last_sequence": last_sequence}

    def record_artifact_metadata(self, digest: str, size: int, media_type: str, relative_path: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO artifact_metadata(digest, size, media_type, relative_path, created_at) VALUES (?, ?, ?, ?, ?)",
                (digest, size, media_type, relative_path, DETERMINISTIC_TIMESTAMP),
            )

    def get_artifact_metadata(self, digest: str) -> dict[str, Any]:
        row = self.conn.execute("SELECT * FROM artifact_metadata WHERE digest = ?", (digest,)).fetchone()
        if row is None:
            raise LocalServiceError("artifact_metadata_missing")
        return {
            "digest": row["digest"],
            "size": int(row["size"]),
            "media_type": row["media_type"],
            "relative_path": row["relative_path"],
        }

    def record_idempotency(self, key: str, request_digest: str, result_ref: str) -> dict[str, Any]:
        with self.conn:
            row = self.conn.execute("SELECT * FROM idempotency WHERE idempotency_key = ?", (key,)).fetchone()
            if row is None:
                self.conn.execute(
                    "INSERT INTO idempotency(idempotency_key, request_digest, result_ref, created_at) VALUES (?, ?, ?, ?)",
                    (key, request_digest, result_ref, DETERMINISTIC_TIMESTAMP),
                )
                return {"status": "recorded", "idempotency_key": key, "result_ref": result_ref}
            if row["request_digest"] != request_digest or row["result_ref"] != result_ref:
                raise LocalServiceError("idempotency_conflict")
            return {"status": "duplicate", "idempotency_key": key, "result_ref": row["result_ref"]}
