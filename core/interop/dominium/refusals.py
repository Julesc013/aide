"""Refusal projection helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import models, snapshot
from .references import sha256_bytes, stable_id


REFUSAL_REGISTRY = "contracts/refusal/refusal_code.registry.json"


def native_refusal_codes(dominium_root: Path, revision: str) -> list[dict[str, Any]]:
    registry = snapshot.git_object_json(dominium_root, revision, REFUSAL_REGISTRY)
    return [item for item in registry.get("codes", []) if isinstance(item, dict)]


def refusal_projections(dominium_root: Path, revision: str, freshness: dict[str, Any], *, limit: int = 8) -> list[dict[str, Any]]:
    native_codes = native_refusal_codes(dominium_root, revision)
    records: list[dict[str, Any]] = []
    for item in native_codes[:limit]:
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
                    "recovery": recovery,
                    "recovery_action": recovery.get("action", ""),
                    "diagnostic_codes": item.get("diagnostic_codes", []),
                    "related_commands": item.get("related_commands", []),
                    "source_registry": REFUSAL_REGISTRY,
                    "source_registry_path": REFUSAL_REGISTRY,
                    "native_meaning_owned_by": "Dominium",
                    "projection_direction": "dominium_to_aide_read_only",
                },
                status={"refusal_typed": bool(refusal_id), "recovery_mapped": bool(recovery)},
            )
        )
    return records


def refusal_projection_summary(dominium_root: Path, revision: str, projected: list[dict[str, Any]], *, limit: int = 8) -> dict[str, Any]:
    native_codes = native_refusal_codes(dominium_root, revision)
    native_ids = [str(item.get("refusal_id") or item.get("code")) for item in native_codes]
    projected_ids = [str(item.get("spec", {}).get("refusal_id", "")) for item in projected]
    omitted_ids = native_ids[len(projected_ids) :]
    source_bytes = snapshot.git_object_bytes(dominium_root, revision, REFUSAL_REGISTRY)
    source_meta = snapshot.git_object_metadata(dominium_root, revision, REFUSAL_REGISTRY)
    return {
        "path": REFUSAL_REGISTRY,
        "source_registry_path": REFUSAL_REGISTRY,
        "source_registry_sha256": sha256_bytes(source_bytes),
        "source_registry_git_object": source_meta,
        "source_revision": revision,
        "selection_policy": "source_order_first_n",
        "selection_limit": limit,
        "native_count": len(native_ids),
        "projected_count": len(projected_ids),
        "omitted_count": len(omitted_ids),
        "projected_ids": projected_ids,
        "selected_ids_sha256": sha256_bytes(models.stable_json(projected_ids).encode("utf-8")),
        "omitted_ids_sha256": sha256_bytes(models.stable_json(omitted_ids).encode("utf-8")),
        "truncation_disclosed": len(omitted_ids) > 0,
    }
