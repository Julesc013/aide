"""SQLite migrations for the local AIDE Service foundation v0."""

from __future__ import annotations

import sqlite3


CURRENT_SCHEMA_VERSION = 1


SCHEMA_SQL = [
    """
    CREATE TABLE IF NOT EXISTS migrations (
        version INTEGER PRIMARY KEY,
        applied_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS objects (
        ref TEXT PRIMARY KEY,
        kind TEXT NOT NULL,
        version INTEGER NOT NULL,
        body_json TEXT NOT NULL,
        body_digest TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS events (
        sequence INTEGER PRIMARY KEY AUTOINCREMENT,
        event_ref TEXT NOT NULL UNIQUE,
        event_type TEXT NOT NULL,
        subject_ref TEXT NOT NULL,
        body_json TEXT NOT NULL,
        body_digest TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS artifact_metadata (
        digest TEXT PRIMARY KEY,
        size INTEGER NOT NULL,
        media_type TEXT NOT NULL,
        relative_path TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS idempotency (
        idempotency_key TEXT PRIMARY KEY,
        request_digest TEXT NOT NULL,
        result_ref TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS cursors (
        cursor_ref TEXT PRIMARY KEY,
        last_sequence INTEGER NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
]


def installed_schema_version(conn: sqlite3.Connection) -> int:
    try:
        row = conn.execute("SELECT MAX(version) FROM migrations").fetchone()
    except sqlite3.OperationalError:
        return 0
    return int(row[0] or 0)


def apply_migrations(conn: sqlite3.Connection, *, applied_at: str) -> int:
    version = installed_schema_version(conn)
    if version > CURRENT_SCHEMA_VERSION:
        raise ValueError("future_migration")
    with conn:
        for statement in SCHEMA_SQL:
            conn.execute(statement)
        conn.execute(
            "INSERT OR IGNORE INTO migrations(version, applied_at) VALUES (?, ?)",
            (CURRENT_SCHEMA_VERSION, applied_at),
        )
    return CURRENT_SCHEMA_VERSION
