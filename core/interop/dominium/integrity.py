"""Digest and projection-index integrity helpers for SeamBundle artifacts."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from . import models
from .references import sha256_bytes


def stable_digest(value: Any) -> str:
    return sha256_bytes(models.stable_json(value).encode("utf-8"))


def snapshot_payload_for_digest(snapshot: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(snapshot)
    payload.pop("snapshot_digest", None)
    return payload


def bundle_payload_for_self_digest(bundle: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(bundle)
    digests = payload.get("content_digests")
    if isinstance(digests, dict):
        digests.pop("seam_bundle_without_self_digest", None)
    metadata = payload.get("metadata")
    if isinstance(metadata, dict):
        for key in [item for item in metadata if str(item).startswith("x_optional_")]:
            metadata.pop(key, None)
    return payload


def record_list(records: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for value in records.values():
        if isinstance(value, list):
            result.extend(item for item in value if isinstance(item, dict) and item.get("kind"))
        elif isinstance(value, dict) and value.get("kind"):
            result.append(value)
    return sorted(result, key=lambda item: (str(item.get("kind", "")), str(item.get("metadata", {}).get("id", ""))))


def projection_index_for_records(records: dict[str, Any]) -> dict[str, Any]:
    flat = record_list(records)
    return {
        "schema_version": "aide.dominium-readonly-seam.projection-index.v0",
        "record_count": len(flat),
        "records": [
            {
                "kind": item["kind"],
                "id": item["metadata"]["id"],
                "semantic_owner": item["metadata"].get("semantic_owner"),
                "authority_role": item["metadata"].get("authority_role"),
                "digest": stable_digest(item),
            }
            for item in flat
        ],
    }


def content_digests_for_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    records = bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {}
    source = bundle.get("source_snapshot", {}) if isinstance(bundle.get("source_snapshot"), dict) else {}
    projection_index = projection_index_for_records(records)
    return {
        "source_snapshot": stable_digest(snapshot_payload_for_digest(source)),
        "projection_index": stable_digest(projection_index),
        "records": {item["metadata"]["id"]: stable_digest(item) for item in record_list(records)},
    }


def finalize_source_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    snapshot["snapshot_digest"] = stable_digest(snapshot_payload_for_digest(snapshot))
    return snapshot


def finalize_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    source = bundle.get("source_snapshot")
    if isinstance(source, dict):
        finalize_source_snapshot(source)
    bundle["content_digests"] = content_digests_for_bundle(bundle)
    bundle["content_digests"]["seam_bundle_without_self_digest"] = stable_digest(bundle_payload_for_self_digest(bundle))
    return bundle
