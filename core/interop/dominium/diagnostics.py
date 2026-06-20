"""Diagnostic projection helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import models, snapshot
from .references import stable_id


DIAGNOSTIC_REGISTRY = "contracts/diagnostic/diagnostic_code.registry.json"
SEVERITY_REGISTRY = "contracts/diagnostic/diagnostic_severity.registry.json"


def severity_ids(dominium_root: Path, revision: str) -> set[str]:
    data = snapshot.git_object_json(dominium_root, revision, SEVERITY_REGISTRY)
    return {str(item.get("id")) for item in data.get("severities", []) if isinstance(item, dict)}


def diagnostic_projections(dominium_root: Path, revision: str, freshness: dict[str, Any], *, limit: int = 8) -> list[dict[str, Any]]:
    registry = snapshot.git_object_json(dominium_root, revision, DIAGNOSTIC_REGISTRY)
    valid_severities = severity_ids(dominium_root, revision)
    records: list[dict[str, Any]] = []
    for item in registry.get("codes", [])[:limit]:
        if not isinstance(item, dict):
            continue
        diagnostic_id = str(item.get("id") or item.get("code"))
        record_id = stable_id("dominium-diagnostic", diagnostic_id)
        severity = str(item.get("severity", ""))
        records.append(
            models.seam_record(
                kind="DiagnosticProjection",
                record_id=record_id,
                source_revision=revision,
                authority_role="read_only_projection_of_dominium_diagnostic_contract",
                freshness=freshness,
                semantic_owner="Dominium",
                identity_owner="AIDE",
                spec={
                    "diagnostic_id": diagnostic_id,
                    "code": item.get("code", ""),
                    "owner": item.get("owner", ""),
                    "severity": severity,
                    "severity_valid": severity in valid_severities,
                    "category": item.get("category", ""),
                    "summary": item.get("summary", ""),
                    "source_registry": DIAGNOSTIC_REGISTRY,
                    "native_meaning_owned_by": "Dominium",
                    "projection_direction": "dominium_to_aide_read_only",
                },
                status={"diagnostic_typed": bool(diagnostic_id), "severity_checked": True},
            )
        )
    return records
