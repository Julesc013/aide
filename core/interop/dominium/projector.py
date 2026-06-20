"""SeamBundle projection builder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import diagnostics, mappings, models, refusals, snapshot
from .references import sha256_bytes, stable_id, stable_ref


def _record_digest(record: dict[str, Any]) -> str:
    return sha256_bytes(models.stable_json(record).encode("utf-8"))


def _record_list(records: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for value in records.values():
        if isinstance(value, list):
            result.extend(value)
        elif isinstance(value, dict) and value.get("kind"):
            result.append(value)
    return sorted(result, key=lambda item: (str(item.get("kind", "")), str(item.get("metadata", {}).get("id", ""))))


def _projection_index(records: dict[str, Any]) -> dict[str, Any]:
    flat = _record_list(records)
    return {
        "schema_version": "aide.dominium-readonly-seam.projection-index.v0",
        "record_count": len(flat),
        "records": [
            {
                "kind": item["kind"],
                "id": item["metadata"]["id"],
                "semantic_owner": item["metadata"].get("semantic_owner"),
                "authority_role": item["metadata"].get("authority_role"),
                "digest": _record_digest(item),
            }
            for item in flat
        ],
    }


def build_seam_bundle(
    repo_root: str | Path,
    dominium_root: str | Path,
    *,
    revision: str | None = None,
    expected_revision: str | None = None,
) -> dict[str, Any]:
    _repo_root = Path(repo_root)
    dom_root = Path(dominium_root)
    source = snapshot.build_source_snapshot(
        dom_root,
        revision=revision,
        expected_revision=expected_revision,
        require_clean=True,
    )
    source_revision = str(source["source_revision"])
    freshness = source["freshness"]
    mapped = mappings.build_all_mappings(source, dom_root)
    diagnostic_records = diagnostics.diagnostic_projections(dom_root, source_revision, freshness)
    refusal_records = refusals.refusal_projections(dom_root, source_revision, freshness)
    records = {
        "host_manifest": mapped["host_manifest"],
        "host_capability_set": mapped["host_capability_set"],
        "workspace_descriptor": mapped["workspace_descriptor"],
        "context_descriptor": mapped["context_descriptor"],
        "artifact_references": mapped["artifact_references"],
        "diagnostic_projections": diagnostic_records,
        "refusal_projections": refusal_records,
        "evidence_reference_set": mapped["evidence_reference_set"],
        "event_envelopes": mapped["event_envelopes"],
        "dominium_bridge_manifest": mapped["dominium_bridge_manifest"],
    }
    flat_records = _record_list(records)
    projection_index = _projection_index(records)
    bundle_id = f"dominium-readonly-seam-{source_revision[:12]}"
    manifest = {
        "bundle_id": bundle_id,
        "bundle_ref": stable_ref("seam-bundle", bundle_id),
        "task_id": models.TASK_ID,
        "capability_target": models.FEATURE_FLAG,
        "source_revision": source_revision,
        "schema_version": models.SCHEMA_VERSION,
        "protocol_version": models.PROTOCOL_VERSION,
        "record_count": projection_index["record_count"],
        "selected_file_count": source["selected_file_count"],
        "projection_authority": "generated_non_authoritative",
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }
    bundle = {
        "apiVersion": models.API_VERSION,
        "kind": "DominiumReadonlySeamBundle",
        "metadata": models.common_metadata(
            record_id=bundle_id,
            source_revision=source_revision,
            authority_role="generated_projection_not_canonical_truth",
            freshness=freshness,
            identity_owner="AIDE",
            semantic_owner="AIDE",
        ),
        "manifest": manifest,
        "source_snapshot": source,
        "records": records,
        "cross_reference_index": {
            "schema_version": "aide.dominium-readonly-seam.cross-reference-index.v0",
            "bundle_ref": manifest["bundle_ref"],
            "workspace_ref": records["workspace_descriptor"]["spec"]["workspace_ref"],
            "context_ref": records["context_descriptor"]["spec"]["context_ref"],
            "artifact_refs": [item["spec"]["artifact_ref"] for item in records["artifact_references"]],
            "event_refs": [item["spec"]["event_ref"] for item in records["event_envelopes"]],
            "diagnostic_ids": [item["spec"]["diagnostic_id"] for item in records["diagnostic_projections"]],
            "refusal_ids": [item["spec"]["refusal_id"] for item in records["refusal_projections"]],
        },
        "content_digests": {
            "source_snapshot": source["snapshot_digest"],
            "projection_index": sha256_bytes(models.stable_json(projection_index).encode("utf-8")),
            "records": {item["metadata"]["id"]: _record_digest(item) for item in flat_records},
        },
        "authority_classification": {
            "canonical_authority": ["Dominium source files at pinned Git revision", "AIDE accepted charter and queue task"],
            "projection_only": ["SeamBundle", "reports", "fixtures", "CLI output"],
            "conflict_policy": "fail_closed",
        },
        "freshness": freshness,
        "validation_summary": {
            "validation_status": "PENDING",
            "validated": False,
            "error_count": 0,
            "warning_count": len(models.WARNING_MESSAGES),
        },
        "omission_summary": {
            "omitted_source_files": "all Dominium files outside the selected seam authority inputs",
            "reason": "bounded read-only seam v0 context",
        },
        "explicit_non_capabilities": list(models.EXPLICIT_NON_CAPABILITIES),
        "status": models.false_status(
            bundle_projected=True,
            generated_projection_marked_canonical=False,
            source_repository_mutated=False,
        ),
    }
    bundle["content_digests"]["seam_bundle_without_self_digest"] = sha256_bytes(models.stable_json(bundle).encode("utf-8"))
    return bundle


def projection_index_for_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    return _projection_index(bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {})
