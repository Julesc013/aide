"""Deterministic Dominium-to-AIDE seam mappings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import models, snapshot
from .references import stable_id, stable_ref


def _command_inventory(dominium_root: Path, revision: str) -> dict[str, Any]:
    data = snapshot.git_object_toml(dominium_root, revision, "contracts/command/command_surface.contract.toml")
    commands = data.get("command", []) if isinstance(data.get("command"), list) else []
    command_ids = [str(item.get("id", "")) for item in commands if isinstance(item, dict) and item.get("id")]
    return {
        "command_count": len(command_ids),
        "command_ids": sorted(command_ids),
        "registered_validation_command_present": "dominium.validation.run" in command_ids,
        "aide_is_authority": bool(data.get("policy", {}).get("aide_is_authority")) if isinstance(data.get("policy"), dict) else None,
        "workbench_is_authority": bool(data.get("policy", {}).get("workbench_is_authority")) if isinstance(data.get("policy"), dict) else None,
    }


def host_manifest(source_snapshot: dict[str, Any], command_inventory: dict[str, Any]) -> dict[str, Any]:
    revision = str(source_snapshot["source_revision"])
    freshness = source_snapshot["freshness"]
    return models.seam_record(
        kind="HostManifest",
        record_id="dominium-host-manifest-v0",
        source_revision=revision,
        authority_role="aide_read_only_host_projection",
        freshness=freshness,
        spec={
            "host_id": "dominium.local.readonly",
            "host_kind": "local_git_repository_snapshot",
            "repository_identity": source_snapshot["repository_identity"],
            "selected_revision": revision,
            "supported_surfaces": [
                "read_only_snapshot",
                "selected_file_inventory",
                "contract_inventory_projection",
                "diagnostic_projection",
                "refusal_projection",
                "evidence_reference_projection",
            ],
            "registered_dominium_command_count": command_inventory["command_count"],
            "registered_validation_command_present": command_inventory["registered_validation_command_present"],
            "runtime_dispatch_available": False,
        },
        status={"host_manifest_projected": True},
    )


def host_capability_set(source_snapshot: dict[str, Any]) -> dict[str, Any]:
    revision = str(source_snapshot["source_revision"])
    freshness = source_snapshot["freshness"]
    capabilities = [
        "dominium.snapshot.read",
        "dominium.selected_files.hash",
        "dominium.contract_inventory.project",
        "dominium.diagnostic_registry.project",
        "dominium.refusal_registry.project",
        "dominium.evidence_refs.project",
        "dominium.event_envelopes.project",
    ]
    forbidden = [
        "dominium.command.invoke",
        "dominium.source.write",
        "dominium.service.start",
        "dominium.provider.call",
        "dominium.worker.execute",
        "dominium.patch.apply",
        "dominium.branch.create",
        "dominium.worktree.create",
        "dominium.release.publish",
    ]
    return models.seam_record(
        kind="HostCapabilitySet",
        record_id="dominium-host-capability-set-v0",
        source_revision=revision,
        authority_role="aide_read_only_capability_projection",
        freshness=freshness,
        spec={
            "capabilities": [
                {
                    "id": item,
                    "side_effect_class": "read_only",
                    "implemented_in_this_slice": True,
                    "requires_future_policy_decision": False,
                }
                for item in capabilities
            ],
            "forbidden_capabilities": [
                {
                    "id": item,
                    "implemented_in_this_slice": False,
                    "refusal_code": "AIDE_DOMINIUM_SEAM_READ_ONLY_BOUNDARY",
                }
                for item in forbidden
            ],
        },
        status={"read_only_capability_count": len(capabilities), "mutation_capability_count": 0},
    )


def workspace_descriptor(source_snapshot: dict[str, Any]) -> dict[str, Any]:
    revision = str(source_snapshot["source_revision"])
    freshness = source_snapshot["freshness"]
    workspace_id = f"dominium-workspace-{revision[:12]}"
    return models.seam_record(
        kind="WorkspaceDescriptor",
        record_id=workspace_id,
        source_revision=revision,
        authority_role="workspace_projection_not_product_truth",
        freshness=freshness,
        semantic_owner="Dominium",
        spec={
            "workspace_ref": stable_ref("workspace", workspace_id),
            "repository_remote_url_hash": stable_id("remote", str(source_snapshot["repository_identity"].get("remote_url", ""))),
            "selected_revision": revision,
            "branch": freshness.get("branch", ""),
            "identity_is_file_path": False,
            "local_path_is_locator_only": True,
            "queue_status": source_snapshot.get("queue_status", {}),
        },
        status={"workspace_projected": True},
    )


def artifact_references(source_snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    revision = str(source_snapshot["source_revision"])
    freshness = source_snapshot["freshness"]
    records = []
    for item in source_snapshot["selected_files"]:
        record_id = stable_id("dominium-artifact", str(item["path"]))
        records.append(
            models.seam_record(
                kind="ArtifactReference",
                record_id=record_id,
                source_revision=revision,
                authority_role="artifact_reference_to_dominium_source_bytes",
                freshness=freshness,
                semantic_owner="Dominium",
                spec={
                    "artifact_ref": stable_ref("artifact", record_id),
                    "source_path": item["path"],
                    "source_role": item["role"],
                    "authority": item["authority"],
                    "source_revision": revision,
                    "sha256": item["sha256"],
                    "size_bytes": item["size_bytes"],
                    "git_object": item["git_object"],
                    "identity_is_file_path": False,
                    "file_path_is_locator": True,
                },
                status={"artifact_hash_bound": True},
            )
        )
    return records


def context_descriptor(source_snapshot: dict[str, Any], artifact_records: list[dict[str, Any]]) -> dict[str, Any]:
    revision = str(source_snapshot["source_revision"])
    freshness = source_snapshot["freshness"]
    sections: dict[str, list[str]] = {}
    for artifact in artifact_records:
        role = str(artifact["spec"].get("source_role", "unknown"))
        sections.setdefault(role, []).append(artifact["metadata"]["id"])
    return models.seam_record(
        kind="ContextDescriptor",
        record_id=f"dominium-context-{revision[:12]}",
        source_revision=revision,
        authority_role="bounded_context_projection",
        freshness=freshness,
        spec={
            "context_ref": stable_ref("context", f"dominium-context-{revision[:12]}"),
            "artifact_refs": [item["spec"]["artifact_ref"] for item in artifact_records],
            "section_count": len(sections),
            "sections": [{"role": key, "artifact_ids": sorted(value)} for key, value in sorted(sections.items())],
            "source_revision_binding": revision,
            "projection_direction": "dominium_source_to_aide_context_descriptor",
        },
        status={"context_projected": True, "artifact_ref_count": len(artifact_records)},
    )


def evidence_reference_set(source_snapshot: dict[str, Any], artifact_records: list[dict[str, Any]]) -> dict[str, Any]:
    revision = str(source_snapshot["source_revision"])
    freshness = source_snapshot["freshness"]
    evidence_artifacts = [
        item
        for item in artifact_records
        if str(item["spec"].get("source_role", "")).endswith("evidence")
        or "evidence" in str(item["spec"].get("authority", ""))
    ]
    return models.seam_record(
        kind="EvidenceReferenceSet",
        record_id=f"dominium-evidence-refs-{revision[:12]}",
        source_revision=revision,
        authority_role="evidence_reference_aggregation",
        freshness=freshness,
        semantic_owner="AIDE",
        spec={
            "evidence_refs": [item["spec"]["artifact_ref"] for item in evidence_artifacts],
            "evidence_count": len(evidence_artifacts),
            "native_evidence_meaning_owned_by": "Dominium",
            "aide_behavior": "reference_and_aggregate_only",
        },
        status={"evidence_refs_projected": True},
    )


def event_envelopes(source_snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    revision = str(source_snapshot["source_revision"])
    freshness = source_snapshot["freshness"]
    specs = [
        ("snapshot.observed", "Dominium source snapshot observed"),
        ("contracts.indexed", "Selected Dominium contracts indexed"),
        ("bundle.projected", "AIDE read-only seam bundle projected"),
    ]
    records = []
    for sequence, (event_type, summary) in enumerate(specs, start=1):
        record_id = f"dominium-event-{sequence:02d}-{revision[:12]}"
        records.append(
            models.seam_record(
                kind="EventEnvelope",
                record_id=record_id,
                source_revision=revision,
                authority_role="event_projection_not_event_store",
                freshness=freshness,
                semantic_owner="AIDE",
                spec={
                    "event_ref": stable_ref("event", record_id),
                    "event_type": event_type,
                    "summary": summary,
                    "sequence": sequence,
                    "causation_ref": stable_ref("source", f"dominium-{revision[:12]}"),
                    "correlation_ref": stable_ref("seam-bundle", f"dominium-readonly-seam-{revision[:12]}"),
                    "universal_event_store_implemented": False,
                },
                status={"event_envelope_projected": True},
            )
        )
    return records


def bridge_manifest(source_snapshot: dict[str, Any], command_inventory: dict[str, Any]) -> dict[str, Any]:
    revision = str(source_snapshot["source_revision"])
    freshness = source_snapshot["freshness"]
    return models.seam_record(
        kind="DominiumBridgeManifest",
        record_id="dominium-bridge-manifest-readonly-v0",
        source_revision=revision,
        authority_role="mapping_version_law_projection",
        freshness=freshness,
        semantic_owner="AIDE",
        spec={
            "bridge_id": "aide-dominium-readonly-seam-v0",
            "bridge_runtime_implemented": False,
            "mapping_version": "0.1.0",
            "source_revision": revision,
            "source_of_truth": {
                "aide": "AIDE queue and accepted protocol/evidence objects",
                "dominium": "Dominium constitution, glossary, AGENTS.md, command/result/refusal/diagnostic law",
                "projection_only": ["reports", "OKF", "RepoGraph", "Workbench views", "interop projections"],
            },
            "ownership": {
                "AIDE": "generic governance, coordination, portable protocol envelopes",
                "Dominium": "product and domain meaning",
                "Domino": "deterministic execution, replay, apply, undo, simulation mechanics",
                "Workbench": "presentation, context capture, preview, approval interaction, apply requests",
            },
            "command_mapping": {
                "registered_validation_command_present": command_inventory["registered_validation_command_present"],
                "command_invocation_implemented": False,
                "future_chain": "AIDE WorkUnit -> registered Dominium command -> typed result/refusal -> evidence/event refs -> read-only projection",
            },
            "compatibility_policy": {
                "read_old_write_current": True,
                "unknown_optional_fields": "preserve_or_ignore",
                "unknown_required_fields": "refuse",
                "silent_migration": False,
            },
        },
        status={"bridge_manifest_projected": True, "bridge_runtime_started": False},
    )


def build_all_mappings(source_snapshot: dict[str, Any], dominium_root: Path) -> dict[str, Any]:
    revision = str(source_snapshot["source_revision"])
    command_inventory = _command_inventory(dominium_root, revision)
    artifacts = artifact_references(source_snapshot)
    return {
        "host_manifest": host_manifest(source_snapshot, command_inventory),
        "host_capability_set": host_capability_set(source_snapshot),
        "workspace_descriptor": workspace_descriptor(source_snapshot),
        "context_descriptor": context_descriptor(source_snapshot, artifacts),
        "artifact_references": artifacts,
        "evidence_reference_set": evidence_reference_set(source_snapshot, artifacts),
        "event_envelopes": event_envelopes(source_snapshot),
        "dominium_bridge_manifest": bridge_manifest(source_snapshot, command_inventory),
        "command_inventory": command_inventory,
    }
