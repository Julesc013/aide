"""Refusal projection helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import models, snapshot
from .references import stable_id


REFUSAL_REGISTRY = "contracts/refusal/refusal_code.registry.json"


def refusal_projections(dominium_root: Path, revision: str, freshness: dict[str, Any], *, limit: int = 8) -> list[dict[str, Any]]:
    registry = snapshot.git_object_json(dominium_root, revision, REFUSAL_REGISTRY)
    records: list[dict[str, Any]] = []
    for item in registry.get("codes", [])[:limit]:
        if not isinstance(item, dict):
            continue
        refusal_id = str(item.get("refusal_id") or item.get("code"))
        record_id = stable_id("dominium-refusal", refusal_id)
        recovery = item.get("recovery", {}) if isinstance(item.get("recovery"), dict) else {}
        records.append(
            models.seam_record(
                kind="RefusalProjection",
                record_id=record_id,
                source_revision=revision,
                authority_role="read_only_projection_of_dominium_refusal_contract",
                freshness=freshness,
                semantic_owner="Dominium",
                identity_owner="AIDE",
                spec={
                    "refusal_id": refusal_id,
                    "code": item.get("code", ""),
                    "owner": item.get("owner", ""),
                    "category": item.get("category", ""),
                    "summary": item.get("summary", ""),
                    "reason": item.get("reason", ""),
                    "recovery_action": recovery.get("action", ""),
                    "diagnostic_codes": item.get("diagnostic_codes", []),
                    "related_commands": item.get("related_commands", []),
                    "source_registry": REFUSAL_REGISTRY,
                    "native_meaning_owned_by": "Dominium",
                    "projection_direction": "dominium_to_aide_read_only",
                },
                status={"refusal_typed": bool(refusal_id), "recovery_mapped": bool(recovery)},
            )
        )
    return records
