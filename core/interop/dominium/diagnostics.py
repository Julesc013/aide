"""Diagnostic projection helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import models, snapshot
from .references import sha256_bytes, stable_id


DIAGNOSTIC_REGISTRY = "contracts/diagnostic/diagnostic_code.registry.json"
SEVERITY_REGISTRY = "contracts/diagnostic/diagnostic_severity.registry.json"


def severity_ids(dominium_root: Path, revision: str) -> set[str]:
    data = snapshot.git_object_json(dominium_root, revision, SEVERITY_REGISTRY)
    return {str(item.get("id")) for item in data.get("severities", []) if isinstance(item, dict)}


def native_diagnostic_codes(dominium_root: Path, revision: str) -> list[dict[str, Any]]:
    registry = snapshot.git_object_json(dominium_root, revision, DIAGNOSTIC_REGISTRY)
    return [item for item in registry.get("codes", []) if isinstance(item, dict)]


def diagnostic_projections(dominium_root: Path, revision: str, freshness: dict[str, Any], *, limit: int = 8) -> list[dict[str, Any]]:
    native_codes = native_diagnostic_codes(dominium_root, revision)
    valid_severities = severity_ids(dominium_root, revision)
    records: list[dict[str, Any]] = []
    for item in native_codes[:limit]:
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
                    "source_registry_path": DIAGNOSTIC_REGISTRY,
                    "native_meaning_owned_by": "Dominium",
                    "projection_direction": "dominium_to_aide_read_only",
                },
                status={"diagnostic_typed": bool(diagnostic_id), "severity_checked": True},
            )
        )
    return records


def diagnostic_projection_summary(dominium_root: Path, revision: str, projected: list[dict[str, Any]], *, limit: int = 8) -> dict[str, Any]:
    native_codes = native_diagnostic_codes(dominium_root, revision)
    native_ids = [str(item.get("id") or item.get("code")) for item in native_codes]
    projected_ids = [str(item.get("spec", {}).get("diagnostic_id", "")) for item in projected]
    omitted_ids = native_ids[len(projected_ids) :]
    return {
        "source_registry_path": DIAGNOSTIC_REGISTRY,
        "selection_policy": "source_order_first_n",
        "selection_limit": limit,
        "native_count": len(native_ids),
        "projected_count": len(projected_ids),
        "omitted_count": len(omitted_ids),
        "projected_ids": projected_ids,
        "omitted_ids_sha256": sha256_bytes(models.stable_json(omitted_ids).encode("utf-8")),
        "truncation_disclosed": len(omitted_ids) > 0,
    }
