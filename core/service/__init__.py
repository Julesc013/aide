"""Local AIDE Service foundation v0."""

from .artifact_store import ArtifactStore
from .local_service import (
    PROPOSED_CAPABILITY_LABEL,
    fixture,
    init_fixture,
    reset_fixture,
    status,
    validate_reports,
)
from .sqlite_store import LocalServiceError, SQLiteStore

__all__ = [
    "ArtifactStore",
    "LocalServiceError",
    "PROPOSED_CAPABILITY_LABEL",
    "SQLiteStore",
    "fixture",
    "init_fixture",
    "reset_fixture",
    "status",
    "validate_reports",
]
