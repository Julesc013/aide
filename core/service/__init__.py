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
from .local_trust_enforcement import (
    PROPOSED_CAPABILITY_LABEL as LOCAL_TRUST_PROPOSED_CAPABILITY_LABEL,
    evaluate_local_authorization,
    persist_evaluation,
)
from .sqlite_store import LocalServiceError, SQLiteStore

__all__ = [
    "ArtifactStore",
    "LOCAL_TRUST_PROPOSED_CAPABILITY_LABEL",
    "LocalServiceError",
    "PROPOSED_CAPABILITY_LABEL",
    "SQLiteStore",
    "evaluate_local_authorization",
    "fixture",
    "init_fixture",
    "persist_evaluation",
    "reset_fixture",
    "status",
    "validate_reports",
]
