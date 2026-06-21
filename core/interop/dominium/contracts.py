"""Semantic contract rules for the Dominium read-only seam validator."""

from __future__ import annotations

from . import models


KIND_TO_CONTAINER = {
    "HostManifest": "host_manifest",
    "HostCapabilitySet": "host_capability_set",
    "WorkspaceDescriptor": "workspace_descriptor",
    "ContextDescriptor": "context_descriptor",
    "ArtifactReference": "artifact_references",
    "DiagnosticProjection": "diagnostic_projections",
    "RefusalProjection": "refusal_projections",
    "EvidenceReferenceSet": "evidence_reference_set",
    "EventEnvelope": "event_envelopes",
    "DominiumBridgeManifest": "dominium_bridge_manifest",
}


SINGLETON_CONTAINERS = {
    "host_manifest",
    "host_capability_set",
    "workspace_descriptor",
    "context_descriptor",
    "evidence_reference_set",
    "dominium_bridge_manifest",
}


LIST_CONTAINERS = {
    "artifact_references",
    "diagnostic_projections",
    "refusal_projections",
    "event_envelopes",
}


KIND_RULES = {
    "HostManifest": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "aide_read_only_host_projection",
        "required_spec": {"host_id", "host_kind", "repository_identity", "selected_revision", "supported_surfaces", "registered_dominium_command_count", "registered_validation_command_present", "runtime_dispatch_available"},
    },
    "HostCapabilitySet": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "aide_read_only_capability_projection",
        "required_spec": {"capabilities", "forbidden_capabilities"},
    },
    "WorkspaceDescriptor": {
        "semantic_owner": "Dominium",
        "identity_owner": "AIDE",
        "authority_role": "workspace_projection_not_product_truth",
        "required_spec": {"workspace_ref", "repository_remote_url_hash", "selected_revision", "branch", "identity_is_file_path", "local_path_is_locator_only", "queue_status"},
    },
    "ContextDescriptor": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "bounded_context_projection",
        "required_spec": {"context_ref", "artifact_refs", "section_count", "sections", "source_revision_binding", "projection_direction"},
    },
    "ArtifactReference": {
        "semantic_owner": "Dominium",
        "identity_owner": "AIDE",
        "authority_role": "artifact_reference_to_dominium_source_bytes",
        "required_spec": {"artifact_ref", "source_path", "source_role", "authority", "sha256", "size_bytes", "git_object", "source_revision", "identity_is_file_path", "file_path_is_locator"},
    },
    "DiagnosticProjection": {
        "semantic_owner": "Dominium",
        "identity_owner": "AIDE",
        "authority_role": "read_only_projection_of_dominium_diagnostic_contract",
        "required_spec": {"diagnostic_id", "code", "owner", "severity", "category", "summary", "source_registry", "native_meaning_owned_by", "projection_direction"},
    },
    "RefusalProjection": {
        "semantic_owner": "Dominium",
        "identity_owner": "AIDE",
        "authority_role": "read_only_projection_of_dominium_refusal_contract",
        "required_spec": {"refusal_id", "code", "owner", "category", "summary", "reason", "recovery_action", "diagnostic_codes", "related_commands", "source_registry", "native_meaning_owned_by", "projection_direction"},
    },
    "EvidenceReferenceSet": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "evidence_reference_aggregation",
        "required_spec": {"evidence_refs", "evidence_count", "native_evidence_meaning_owned_by", "aide_behavior"},
    },
    "EventEnvelope": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "event_projection_not_event_store",
        "required_spec": {"event_ref", "event_type", "summary", "sequence", "causation_ref", "correlation_ref", "universal_event_store_implemented"},
    },
    "DominiumBridgeManifest": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "mapping_version_law_projection",
        "required_spec": {"bridge_id", "bridge_runtime_implemented", "mapping_version", "source_of_truth", "ownership", "command_mapping", "compatibility_policy"},
    },
}


IMPLEMENTED_CAPABILITIES = {
    "dominium.snapshot.read",
    "dominium.selected_files.hash",
    "dominium.contract_inventory.project",
    "dominium.diagnostic_registry.project",
    "dominium.refusal_registry.project",
    "dominium.evidence_refs.project",
    "dominium.event_envelopes.project",
}


FORBIDDEN_CAPABILITIES = {
    "dominium.command.invoke",
    "dominium.source.write",
    "dominium.service.start",
    "dominium.provider.call",
    "dominium.worker.execute",
    "dominium.patch.apply",
    "dominium.branch.create",
    "dominium.worktree.create",
    "dominium.release.publish",
}


ALLOWED_SCHEMA_VERSIONS = {models.SCHEMA_VERSION}
