"""No-op migration registry for the Q06 Compatibility baseline."""

from __future__ import annotations

from dataclasses import dataclass

from .version_registry import BASELINE_VERSION


@dataclass(frozen=True)
class MigrationEntry:
    id: str
    source_version: str
    target_version: str
    status: str
    mutates_repo: bool
    owner_queue_item: str
    review_required_for_apply: bool
    notes: str


def migration_entries() -> list[MigrationEntry]:
    return [
        MigrationEntry(
            id="baseline-current-noop",
            source_version="none",
            target_version=BASELINE_VERSION,
            status="current-noop",
            mutates_repo=False,
            owner_queue_item="Q06-compatibility-baseline",
            review_required_for_apply=True,
            notes="Q06 records the current baseline only; it applies no migrations.",
        )
    ]


def mutating_migrations_available() -> bool:
    return any(entry.mutates_repo for entry in migration_entries())

