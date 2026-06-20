"""Validation for the offline Dominium read-only seam."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from . import models, projector, snapshot
from .references import is_commit_sha, is_sha256, normalize_repo_path, sha256_bytes


class ValidationFailure(ValueError):
    """Raised for validation defects that should fail closed."""


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _all_records(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    records = bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {}
    result: list[dict[str, Any]] = []
    for value in records.values():
        if isinstance(value, list):
            result.extend([item for item in value if isinstance(item, dict)])
        elif isinstance(value, dict):
            result.append(value)
    return result


def _check_common_record(record: dict[str, Any], errors: list[str]) -> None:
    kind = str(record.get("kind", ""))
    if kind not in models.AUTHORIZED_SEAM_KINDS:
        errors.append(f"unsupported record kind: {kind}")
    metadata = record.get("metadata", {}) if isinstance(record.get("metadata"), dict) else {}
    _check_common_metadata(kind or "record", metadata, errors)
    status = record.get("status", {}) if isinstance(record.get("status"), dict) else {}
    for field in models.FALSE_STATUS_FIELDS:
        if status.get(field) is not False:
            errors.append(f"{kind} status.{field} must be false")


def _check_common_metadata(label: str, metadata: dict[str, Any], errors: list[str]) -> None:
    for field in [
        "id",
        "schema_version",
        "protocol_version",
        "producer",
        "source_revision",
        "authority_role",
        "freshness",
        "compatibility",
        "explicit_non_capabilities",
    ]:
        if field not in metadata:
            errors.append(f"{label} missing metadata.{field}")
    if metadata.get("schema_version") != models.SCHEMA_VERSION:
        errors.append(f"{label} schema_version mismatch")
    if not is_commit_sha(metadata.get("source_revision")):
        errors.append(f"{label} source_revision must be commit sha")
    if metadata.get("explicit_non_capabilities") != models.EXPLICIT_NON_CAPABILITIES:
        errors.append(f"{label} explicit_non_capabilities mismatch")
    if metadata.get("semantic_owner") not in {"AIDE", "Dominium"}:
        errors.append(f"{label} semantic_owner must be AIDE or Dominium")
    compatibility = metadata.get("compatibility", {}) if isinstance(metadata.get("compatibility"), dict) else {}
    for capability in _as_list(compatibility.get("requiredCapabilities")):
        if capability not in {models.FEATURE_FLAG}:
            errors.append(f"unknown required capability: {capability}")


def validate_bundle(bundle: dict[str, Any], *, dominium_root: str | Path | None = None) -> dict[str, Any]:
    errors: list[str] = []
    warnings = list(models.WARNING_MESSAGES)
    if bundle.get("apiVersion") != models.API_VERSION:
        errors.append("apiVersion mismatch")
    if bundle.get("kind") != "DominiumReadonlySeamBundle":
        errors.append("kind must be DominiumReadonlySeamBundle")
    metadata = bundle.get("metadata", {}) if isinstance(bundle.get("metadata"), dict) else {}
    _check_common_metadata("bundle", metadata, errors)
    if metadata.get("authority_role") != "generated_projection_not_canonical_truth":
        errors.append("bundle must be generated projection, not canonical authority")
    if bundle.get("explicit_non_capabilities") != models.EXPLICIT_NON_CAPABILITIES:
        errors.append("bundle explicit_non_capabilities mismatch")
    for field in models.FALSE_STATUS_FIELDS:
        status = bundle.get("status", {}) if isinstance(bundle.get("status"), dict) else {}
        if status.get(field) is not False:
            errors.append(f"bundle status.{field} must be false")
    source = bundle.get("source_snapshot", {}) if isinstance(bundle.get("source_snapshot"), dict) else {}
    revision = str(source.get("source_revision", ""))
    if not is_commit_sha(revision):
        errors.append("source_snapshot.source_revision must be commit sha")
    selected = source.get("selected_files", []) if isinstance(source.get("selected_files"), list) else []
    if len(selected) != len(models.SELECTED_DOMINIUM_INPUTS):
        errors.append("selected file count mismatch")
    seen_paths: set[str] = set()
    for item in selected:
        if not isinstance(item, dict):
            errors.append("selected_files items must be objects")
            continue
        try:
            rel = normalize_repo_path(str(item.get("path", "")))
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if rel in seen_paths:
            errors.append(f"duplicate selected source path: {rel}")
        seen_paths.add(rel)
        if not is_sha256(item.get("sha256")):
            errors.append(f"invalid selected source digest: {rel}")
    records = _all_records(bundle)
    ids = [str(item.get("metadata", {}).get("id", "")) for item in records]
    if len(ids) != len(set(ids)):
        errors.append("duplicate identity in seam records")
    kinds = {str(item.get("kind", "")) for item in records}
    for kind in models.AUTHORIZED_SEAM_KINDS:
        if kind not in kinds:
            errors.append(f"missing seam kind: {kind}")
    for record in records:
        _check_common_record(record, errors)
    for diagnostic in [item for item in records if item.get("kind") == "DiagnosticProjection"]:
        if diagnostic.get("spec", {}).get("severity_valid") is not True:
            errors.append(f"invalid diagnostic severity: {diagnostic.get('metadata', {}).get('id')}")
    for refusal in [item for item in records if item.get("kind") == "RefusalProjection"]:
        spec = refusal.get("spec", {})
        if not spec.get("refusal_id") or not spec.get("reason"):
            errors.append(f"invalid refusal mapping: {refusal.get('metadata', {}).get('id')}")
    events = [item for item in records if item.get("kind") == "EventEnvelope"]
    event_sequences = [item.get("spec", {}).get("sequence") for item in events]
    if event_sequences != sorted(event_sequences):
        errors.append("event sequence must be deterministic")
    for event in events:
        spec = event.get("spec", {})
        if not spec.get("correlation_ref") or spec.get("universal_event_store_implemented") is not False:
            errors.append("event correlation mismatch")
    capability_sets = [item for item in records if item.get("kind") == "HostCapabilitySet"]
    if capability_sets:
        for capability in capability_sets[0].get("spec", {}).get("capabilities", []):
            if isinstance(capability, dict) and capability.get("side_effect_class") != "read_only":
                errors.append(f"read-only capability boundary violated: {capability.get('id')}")
        forbidden = capability_sets[0].get("spec", {}).get("forbidden_capabilities", [])
        if any(item.get("implemented_in_this_slice") is True for item in forbidden if isinstance(item, dict)):
            errors.append("mutation capability in read-only seam")
    bridge_records = [item for item in records if item.get("kind") == "DominiumBridgeManifest"]
    if bridge_records:
        bridge_spec = bridge_records[0].get("spec", {})
        if bridge_spec.get("bridge_runtime_implemented") is not False:
            errors.append("bridge runtime must not be implemented")
        if bridge_spec.get("command_mapping", {}).get("command_invocation_implemented") is not False:
            errors.append("command invocation must not be implemented")
    if bundle.get("status", {}).get("generated_projection_marked_canonical") is not False:
        errors.append("generated projection marked canonical")
    expected_index = projector.projection_index_for_bundle(bundle)
    expected_digest = sha256_bytes(models.stable_json(expected_index).encode("utf-8"))
    if bundle.get("content_digests", {}).get("projection_index") != expected_digest:
        errors.append("projection index digest mismatch")
    if dominium_root is not None and is_commit_sha(revision):
        root = Path(dominium_root)
        for item in selected:
            if not isinstance(item, dict):
                continue
            rel = str(item.get("path", ""))
            try:
                payload = snapshot.git_object_bytes(root, revision, rel)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"source digest recomputation failed: {rel}: {exc}")
                continue
            if sha256_bytes(payload) != item.get("sha256"):
                errors.append(f"source digest mismatch: {rel}")
    status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    return {
        "schema_version": "aide.dominium-readonly-seam.validation.v0",
        "task_id": models.TASK_ID,
        "validation_status": status,
        "status": status,
        "validated": not errors,
        "record_count": len(records),
        "selected_file_count": len(selected),
        "errors": errors,
        "warnings": warnings,
        "explicit_non_capabilities_preserved": bundle.get("explicit_non_capabilities") == models.EXPLICIT_NON_CAPABILITIES,
        "source_revision_bound": is_commit_sha(revision),
        "digest_validity_checked": True,
        "read_only_capability_boundary_preserved": not any("read-only capability boundary" in item for item in errors),
        "deterministic_ordering_checked": True,
        "dominium_command_invoked": False,
        "network_call_performed": False,
        "provider_or_model_called": False,
        "worker_executed": False,
        "mutation_performed": False,
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }


def negative_fixture_cases(valid_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []

    def add(name: str, expected: str, mutator) -> None:
        candidate = deepcopy(valid_bundle)
        mutator(candidate)
        cases.append({"name": name, "expected_error": expected, "mutation": name, "bundle": candidate})

    add("wrong_repository_identity", "selected file count", lambda b: b["source_snapshot"].update({"selected_files": []}))
    add("stale_revision", "source_revision must be commit sha", lambda b: b["source_snapshot"].update({"source_revision": "stale"}))
    add("missing_required_contract", "selected file count", lambda b: b["source_snapshot"]["selected_files"].pop())
    add("invalid_reference_id", "event correlation mismatch", lambda b: b["records"]["event_envelopes"][0]["spec"].update({"correlation_ref": ""}))
    add("duplicate_identity", "duplicate identity", lambda b: b["records"]["artifact_references"][1]["metadata"].update({"id": b["records"]["artifact_references"][0]["metadata"]["id"]}))
    add("wrong_authority_role", "generated projection", lambda b: b["metadata"].update({"authority_role": "canonical_truth"}))
    add("generated_projection_marked_canonical", "generated projection marked canonical", lambda b: b["status"].update({"generated_projection_marked_canonical": True}))
    add("path_traversal", "path traversal", lambda b: b["source_snapshot"]["selected_files"][0].update({"path": "../AGENTS.md"}))
    add("absolute_path_escape", "absolute path", lambda b: b["source_snapshot"]["selected_files"][0].update({"path": "/tmp/AGENTS.md"}))
    add("digest_mismatch", "source digest mismatch", lambda b: b["source_snapshot"]["selected_files"][0].update({"sha256": "sha256:" + "0" * 64}))
    add("unknown_required_capability", "unknown required capability", lambda b: b["metadata"]["compatibility"].update({"requiredCapabilities": ["future.required"]}))
    add("unsupported_version", "schema_version mismatch", lambda b: b["records"]["host_manifest"]["metadata"].update({"schema_version": "future"}))
    add("conflicting_ownership", "semantic_owner", lambda b: b["records"]["host_manifest"]["metadata"].update({"semantic_owner": "Workbench"}))
    add("workbench_authority_overclaim", "status.workbench_started", lambda b: b["records"]["workspace_descriptor"]["status"].update({"workbench_started": True}))
    add("private_tool_bypass_declaration", "command invocation", lambda b: b["records"]["dominium_bridge_manifest"]["spec"]["command_mapping"].update({"command_invocation_implemented": True}))
    add("mutation_capability_claim", "mutation capability", lambda b: b["records"]["host_capability_set"]["spec"]["forbidden_capabilities"][0].update({"implemented_in_this_slice": True}))
    add("provider_network_worker_claim", "status.network_call_performed", lambda b: b["status"].update({"network_call_performed": True}))
    add("invalid_refusal_mapping", "invalid refusal mapping", lambda b: b["records"]["refusal_projections"][0]["spec"].update({"reason": ""}))
    add("invalid_diagnostic_severity", "invalid diagnostic severity", lambda b: b["records"]["diagnostic_projections"][0]["spec"].update({"severity_valid": False}))
    add("broken_evidence_ref", "missing seam kind", lambda b: b["records"].pop("evidence_reference_set"))
    add("event_correlation_mismatch", "event correlation mismatch", lambda b: b["records"]["event_envelopes"][0]["spec"].update({"universal_event_store_implemented": True}))
    add("non_deterministic_ordering", "event sequence", lambda b: b["records"]["event_envelopes"][0]["spec"].update({"sequence": 99}))
    return cases
