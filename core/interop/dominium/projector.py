"""SeamBundle projection builder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import diagnostics, integrity, mappings, models, refusals, snapshot
from .references import stable_ref


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
    flat_records = integrity.record_list(records)
    projection_index = integrity.projection_index_for_records(records)
    diagnostic_summary = diagnostics.diagnostic_projection_summary(dom_root, source_revision, diagnostic_records)
    refusal_summary = refusals.refusal_projection_summary(dom_root, source_revision, refusal_records)
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
        "content_digests": {},
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
            "diagnostic_registry": diagnostic_summary,
            "refusal_registry": refusal_summary,
        },
        "registry_projection_summary": {
            "diagnostics": diagnostic_summary,
            "refusals": refusal_summary,
        },
        "explicit_non_capabilities": list(models.EXPLICIT_NON_CAPABILITIES),
        "status": models.false_status(
            bundle_projected=True,
            generated_projection_marked_canonical=False,
            source_repository_mutated=False,
        ),
    }
    integrity.finalize_bundle(bundle)
    return bundle


def projection_index_for_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    return integrity.projection_index_for_records(bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {})
