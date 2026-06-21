"""Validation for the offline Dominium read-only seam."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import contracts, diagnostics, fixture_replay, integrity, models, projector, refusals, snapshot
from .references import is_commit_sha, is_sha256, normalize_repo_path, parse_stable_ref, sha256_bytes


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


def _error(
    errors: list[str],
    error_records: list[dict[str, Any]],
    code: str,
    path: str,
    message: str,
    *,
    expected: Any = None,
    observed: Any = None,
) -> None:
    errors.append(f"{code}: {message}")
    error_records.append({"code": code, "path": path, "message": message, "expected": expected, "observed": observed})


def _check_common_metadata(
    label: str,
    metadata: dict[str, Any],
    errors: list[str],
    error_records: list[dict[str, Any]],
    *,
    expected_revision: str | None = None,
) -> None:
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
            _error(errors, error_records, "metadata.required", f"{label}.metadata.{field}", f"{label} missing metadata.{field}")
    if metadata.get("schema_version") != models.SCHEMA_VERSION:
        _error(errors, error_records, "schema.version", f"{label}.metadata.schema_version", f"{label} schema_version mismatch", expected=models.SCHEMA_VERSION, observed=metadata.get("schema_version"))
    producer = metadata.get("producer")
    if not isinstance(producer, dict) or not producer.get("name") or not producer.get("version"):
        _error(errors, error_records, "metadata.producer", f"{label}.metadata.producer", f"{label} metadata.producer must contain name and version", expected={"name": "string", "version": "string"}, observed=producer)
    if not is_commit_sha(metadata.get("source_revision")):
        _error(errors, error_records, "revision.syntax", f"{label}.metadata.source_revision", f"{label} source_revision must be commit sha", expected="40-char lowercase hex commit", observed=metadata.get("source_revision"))
    if expected_revision and metadata.get("source_revision") != expected_revision:
        _error(errors, error_records, "revision.binding", f"{label}.metadata.source_revision", f"{label} source_revision does not match bundle revision", expected=expected_revision, observed=metadata.get("source_revision"))
    if metadata.get("explicit_non_capabilities") != models.EXPLICIT_NON_CAPABILITIES:
        _error(errors, error_records, "noncapability.explicit", f"{label}.metadata.explicit_non_capabilities", f"{label} explicit_non_capabilities mismatch")
    compatibility = metadata.get("compatibility", {}) if isinstance(metadata.get("compatibility"), dict) else {}
    for capability in _as_list(compatibility.get("requiredCapabilities")):
        if capability not in {models.FEATURE_FLAG}:
            _error(errors, error_records, "compat.required_capability", f"{label}.metadata.compatibility.requiredCapabilities", f"unknown required capability: {capability}")


def _check_record(
    record: dict[str, Any],
    errors: list[str],
    error_records: list[dict[str, Any]],
    *,
    expected_revision: str,
) -> None:
    kind = str(record.get("kind", ""))
    if kind not in models.AUTHORIZED_SEAM_KINDS:
        _error(errors, error_records, "kind.unsupported", "records", f"unsupported record kind: {kind}")
        return
    metadata = record.get("metadata", {}) if isinstance(record.get("metadata"), dict) else {}
    _check_common_metadata(kind or "record", metadata, errors, error_records, expected_revision=expected_revision)
    rule = contracts.KIND_RULES.get(kind, {})
    if metadata.get("semantic_owner") != rule.get("semantic_owner"):
        _error(errors, error_records, "ownership.semantic", f"{kind}.metadata.semantic_owner", f"{kind} semantic_owner must be {rule.get('semantic_owner')}")
    if metadata.get("identity_owner") != rule.get("identity_owner"):
        _error(errors, error_records, "ownership.identity", f"{kind}.metadata.identity_owner", f"{kind} identity_owner must be {rule.get('identity_owner')}")
    if metadata.get("authority_role") != rule.get("authority_role"):
        _error(errors, error_records, "authority.role", f"{kind}.metadata.authority_role", f"{kind} authority_role mismatch")
    spec = record.get("spec", {}) if isinstance(record.get("spec"), dict) else {}
    for field in sorted(rule.get("required_spec", set())):
        if field not in spec:
            _error(errors, error_records, "schema.spec_required", f"{kind}.spec.{field}", f"{kind} missing spec.{field}", expected="field present", observed="missing")
            _error(errors, error_records, "spec.required", f"{kind}.spec.{field}", f"{kind} missing spec.{field}", expected="field present", observed="missing")
    status = record.get("status", {}) if isinstance(record.get("status"), dict) else {}
    for field in models.FALSE_STATUS_FIELDS:
        if field not in status:
            _error(errors, error_records, "schema.status_required", f"{kind}.status.{field}", f"{kind} missing status.{field}", expected=False, observed="missing")
        elif status.get(field) is not False:
            code = "workbench.authority" if field == "workbench_started" else "status.false_boundary"
            _error(errors, error_records, code, f"{kind}.status.{field}", f"{kind} status.{field} must be false", expected=False, observed=status.get(field))


def _check_selected_inputs(
    source: dict[str, Any],
    errors: list[str],
    error_records: list[dict[str, Any]],
) -> None:
    selected = source.get("selected_files", []) if isinstance(source.get("selected_files"), list) else []
    expected_paths = [str(item["path"]) for item in models.SELECTED_DOMINIUM_INPUTS]
    actual_paths: list[str] = []
    seen_paths: set[str] = set()
    for index, item in enumerate(selected):
        if not isinstance(item, dict):
            _error(errors, error_records, "selected_files.item", f"source_snapshot.selected_files.{index}", "selected_files items must be objects")
            continue
        try:
            rel = normalize_repo_path(str(item.get("path", "")))
        except ValueError as exc:
            code = "path.absolute" if "absolute path" in str(exc) or "drive-qualified" in str(exc) else "path.traversal"
            _error(errors, error_records, code, f"source_snapshot.selected_files.{index}.path", str(exc))
            continue
        actual_paths.append(rel)
        if rel in seen_paths:
            _error(errors, error_records, "selected_files.duplicate_path", f"source_snapshot.selected_files.{index}.path", f"duplicate selected source path: {rel}")
        seen_paths.add(rel)
        if not is_sha256(item.get("sha256")):
            _error(errors, error_records, "digest.source.syntax", f"source_snapshot.selected_files.{index}.sha256", f"invalid selected source digest: {rel}")
    if actual_paths != expected_paths:
        _error(errors, error_records, "selected_files.exact_set", "source_snapshot.selected_files", "selected file count or order mismatch")


def _check_cardinality(
    bundle: dict[str, Any],
    errors: list[str],
    error_records: list[dict[str, Any]],
) -> None:
    records = bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {}
    for container in sorted(contracts.SINGLETON_CONTAINERS):
        value = records.get(container)
        if not isinstance(value, dict):
            _error(errors, error_records, "cardinality.singleton", f"records.{container}", f"{container} must contain exactly one record object")
    for container in sorted(contracts.LIST_CONTAINERS):
        value = records.get(container)
        if not isinstance(value, list) or not value:
            _error(errors, error_records, "cardinality.list", f"records.{container}", f"{container} must contain one or more records")
    observed_kinds = {str(item.get("kind", "")) for item in _all_records(bundle)}
    for kind in models.AUTHORIZED_SEAM_KINDS:
        if kind not in observed_kinds:
            _error(errors, error_records, "kind.missing", "records", f"missing seam kind: {kind}")


def _check_references(bundle: dict[str, Any], errors: list[str], error_records: list[dict[str, Any]]) -> None:
    index = bundle.get("cross_reference_index", {}) if isinstance(bundle.get("cross_reference_index"), dict) else {}
    artifact_refs = set(index.get("artifact_refs", []) if isinstance(index.get("artifact_refs"), list) else [])
    event_refs = set(index.get("event_refs", []) if isinstance(index.get("event_refs"), list) else [])
    bundle_ref = str(index.get("bundle_ref", ""))
    context_ref = str(index.get("context_ref", ""))
    workspace_ref = str(index.get("workspace_ref", ""))
    refs_to_parse = [bundle_ref, context_ref, workspace_ref, *artifact_refs, *event_refs]
    for ref in refs_to_parse:
        try:
            parse_stable_ref(ref)
        except ValueError as exc:
            _error(errors, error_records, "reference.syntax", "cross_reference_index", str(exc))
    records = bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {}
    context_refs = records.get("context_descriptor", {}).get("spec", {}).get("artifact_refs", []) if isinstance(records.get("context_descriptor"), dict) else []
    for ref in context_refs:
        if ref not in artifact_refs:
            _error(errors, error_records, "reference.closure", "records.context_descriptor.spec.artifact_refs", f"context references unknown artifact: {ref}")
    evidence_refs = records.get("evidence_reference_set", {}).get("spec", {}).get("evidence_refs", []) if isinstance(records.get("evidence_reference_set"), dict) else []
    for ref in evidence_refs:
        if ref not in artifact_refs:
            _error(errors, error_records, "reference.closure", "records.evidence_reference_set.spec.evidence_refs", f"evidence references unknown artifact: {ref}")
    events = records.get("event_envelopes", []) if isinstance(records.get("event_envelopes"), list) else []
    for event in events:
        spec = event.get("spec", {}) if isinstance(event, dict) else {}
        for field in ["event_ref", "correlation_ref"]:
            try:
                parse_stable_ref(spec.get(field))
            except ValueError as exc:
                _error(errors, error_records, "reference.syntax", f"records.event_envelopes.spec.{field}", str(exc))
        if spec.get("event_ref") not in event_refs:
            _error(errors, error_records, "reference.closure", "records.event_envelopes.spec.event_ref", "event ref missing from cross-reference index")
        if spec.get("correlation_ref") != bundle_ref:
            _error(errors, error_records, "event.correlation", "records.event_envelopes.spec.correlation_ref", "event correlation mismatch")


def _check_digest_integrity(
    bundle: dict[str, Any],
    errors: list[str],
    error_records: list[dict[str, Any]],
) -> None:
    digests = bundle.get("content_digests", {}) if isinstance(bundle.get("content_digests"), dict) else {}
    source = bundle.get("source_snapshot", {}) if isinstance(bundle.get("source_snapshot"), dict) else {}
    expected_source = integrity.stable_digest(integrity.snapshot_payload_for_digest(source))
    if source.get("snapshot_digest") != expected_source:
        _error(errors, error_records, "digest.snapshot", "source_snapshot.snapshot_digest", "source snapshot digest mismatch")
    if digests.get("source_snapshot") != expected_source:
        _error(errors, error_records, "digest.source", "content_digests.source_snapshot", "source digest mismatch")
    expected_index = projector.projection_index_for_bundle(bundle)
    expected_index_digest = integrity.stable_digest(expected_index)
    if digests.get("projection_index") != expected_index_digest:
        _error(errors, error_records, "digest.projection_index", "content_digests.projection_index", "projection index digest mismatch")
    record_digests = digests.get("records", {}) if isinstance(digests.get("records"), dict) else {}
    for record in integrity.record_list(bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {}):
        record_id = str(record.get("metadata", {}).get("id", ""))
        if record_digests.get(record_id) != integrity.stable_digest(record):
            _error(errors, error_records, "digest.record", f"content_digests.records.{record_id}", f"record digest mismatch: {record_id}")
    expected_self = integrity.stable_digest(integrity.bundle_payload_for_self_digest(bundle))
    if digests.get("seam_bundle_without_self_digest") != expected_self:
        _error(errors, error_records, "digest.bundle_self", "content_digests.seam_bundle_without_self_digest", "bundle self digest mismatch")


def _check_revision_binding(bundle: dict[str, Any], errors: list[str], error_records: list[dict[str, Any]]) -> str:
    manifest = bundle.get("manifest", {}) if isinstance(bundle.get("manifest"), dict) else {}
    source = bundle.get("source_snapshot", {}) if isinstance(bundle.get("source_snapshot"), dict) else {}
    revision = str(source.get("source_revision", ""))
    if not is_commit_sha(revision):
        _error(errors, error_records, "revision.syntax", "source_snapshot.source_revision", "source_snapshot.source_revision must be commit sha")
    for path, value in [
        ("manifest.source_revision", manifest.get("source_revision")),
        ("metadata.source_revision", bundle.get("metadata", {}).get("source_revision") if isinstance(bundle.get("metadata"), dict) else None),
    ]:
        if value != revision:
            _error(errors, error_records, "revision.binding", path, f"{path} does not match source revision")
    records = _all_records(bundle)
    for record in records:
        metadata = record.get("metadata", {}) if isinstance(record.get("metadata"), dict) else {}
        if metadata.get("source_revision") != revision:
            _error(errors, error_records, "revision.binding", f"{record.get('kind')}.metadata.source_revision", "record revision does not match source revision")
        spec = record.get("spec", {}) if isinstance(record.get("spec"), dict) else {}
        for key in ["selected_revision", "source_revision", "source_revision_binding"]:
            if key in spec and spec[key] != revision:
                _error(errors, error_records, "revision.binding", f"{record.get('kind')}.spec.{key}", f"{key} does not match source revision")
    return revision


def _check_capabilities(bundle: dict[str, Any], errors: list[str], error_records: list[dict[str, Any]]) -> None:
    record = bundle.get("records", {}).get("host_capability_set") if isinstance(bundle.get("records"), dict) else None
    if not isinstance(record, dict):
        return
    spec = record.get("spec", {}) if isinstance(record.get("spec"), dict) else {}
    capabilities = [item for item in spec.get("capabilities", []) if isinstance(item, dict)]
    forbidden = [item for item in spec.get("forbidden_capabilities", []) if isinstance(item, dict)]
    capability_ids = {str(item.get("id", "")) for item in capabilities}
    forbidden_ids = {str(item.get("id", "")) for item in forbidden}
    if capability_ids != contracts.IMPLEMENTED_CAPABILITIES:
        _error(errors, error_records, "capability.implemented_set", "records.host_capability_set.spec.capabilities", "implemented read-only capability set mismatch")
    if forbidden_ids != contracts.FORBIDDEN_CAPABILITIES:
        _error(errors, error_records, "capability.forbidden_set", "records.host_capability_set.spec.forbidden_capabilities", "forbidden capability set mismatch")
    if capability_ids & contracts.FORBIDDEN_CAPABILITIES:
        _error(errors, error_records, "capability.mutation", "records.host_capability_set.spec.capabilities", "mutation capability in read-only seam")
    for item in capabilities:
        if item.get("side_effect_class") != "read_only" or item.get("implemented_in_this_slice") is not True:
            _error(errors, error_records, "capability.readonly", "records.host_capability_set.spec.capabilities", f"read-only capability boundary violated: {item.get('id')}")
    if any(item.get("implemented_in_this_slice") is True for item in forbidden):
        _error(errors, error_records, "capability.mutation", "records.host_capability_set.spec.forbidden_capabilities", "mutation capability in read-only seam")


def _check_events(bundle: dict[str, Any], errors: list[str], error_records: list[dict[str, Any]]) -> None:
    events = bundle.get("records", {}).get("event_envelopes", []) if isinstance(bundle.get("records"), dict) else []
    if not isinstance(events, list):
        return
    sequences = [item.get("spec", {}).get("sequence") for item in events if isinstance(item, dict)]
    if sequences != list(range(1, len(sequences) + 1)):
        _error(errors, error_records, "event.sequence", "records.event_envelopes.spec.sequence", "event sequence must be deterministic and contiguous")
    refs = [item.get("spec", {}).get("event_ref") for item in events if isinstance(item, dict)]
    if len(refs) != len(set(refs)):
        _error(errors, error_records, "event.identity", "records.event_envelopes.spec.event_ref", "duplicate event ref")
    for item in events:
        spec = item.get("spec", {}) if isinstance(item, dict) else {}
        if spec.get("universal_event_store_implemented") is not False:
            _error(errors, error_records, "event.correlation", "records.event_envelopes.spec.universal_event_store_implemented", "event correlation mismatch")
        try:
            parse_stable_ref(spec.get("causation_ref"))
        except ValueError as exc:
            _error(errors, error_records, "reference.syntax", "records.event_envelopes.spec.causation_ref", str(exc))


def _check_bridge(bundle: dict[str, Any], errors: list[str], error_records: list[dict[str, Any]]) -> None:
    bridge = bundle.get("records", {}).get("dominium_bridge_manifest") if isinstance(bundle.get("records"), dict) else None
    if not isinstance(bridge, dict):
        return
    spec = bridge.get("spec", {}) if isinstance(bridge.get("spec"), dict) else {}
    if spec.get("bridge_runtime_implemented") is not False:
        _error(errors, error_records, "bridge.runtime", "records.dominium_bridge_manifest.spec.bridge_runtime_implemented", "bridge runtime must not be implemented")
    command_mapping = spec.get("command_mapping", {}) if isinstance(spec.get("command_mapping"), dict) else {}
    if command_mapping.get("command_invocation_implemented") is not False:
        _error(errors, error_records, "command.invocation", "records.dominium_bridge_manifest.spec.command_mapping.command_invocation_implemented", "command invocation must not be implemented", expected=False, observed=command_mapping.get("command_invocation_implemented"))
    for field in ["private_tool_bypass", "direct_tool_invocation", "workbench_private_tool_access"]:
        if command_mapping.get(field) is True:
            _error(errors, error_records, "command.invocation", f"records.dominium_bridge_manifest.spec.command_mapping.{field}", f"{field} must not be enabled", expected=False, observed=True)
    ownership = spec.get("ownership", {}) if isinstance(spec.get("ownership"), dict) else {}
    if ownership.get("Workbench") != "presentation, context capture, preview, approval interaction, apply requests":
        _error(errors, error_records, "workbench.authority", "records.dominium_bridge_manifest.spec.ownership.Workbench", "Workbench ownership boundary mismatch", expected="presentation, context capture, preview, approval interaction, apply requests", observed=ownership.get("Workbench"))
    compatibility_policy = spec.get("compatibility_policy", {}) if isinstance(spec.get("compatibility_policy"), dict) else {}
    for capability in _as_list(compatibility_policy.get("requiredCapabilities")):
        if capability not in {models.FEATURE_FLAG}:
            _error(errors, error_records, "compat.required_capability", "records.dominium_bridge_manifest.spec.compatibility_policy.requiredCapabilities", f"unknown required capability: {capability}", expected=[models.FEATURE_FLAG], observed=capability)


def _check_registry_projection(
    bundle: dict[str, Any],
    errors: list[str],
    error_records: list[dict[str, Any]],
    *,
    dominium_root: str | Path | None,
    revision: str,
) -> None:
    if dominium_root is None or not is_commit_sha(revision):
        return
    root = Path(dominium_root)
    try:
        native_diagnostics = diagnostics.native_diagnostic_codes(root, revision)
        native_refusals = refusals.native_refusal_codes(root, revision)
        severities = diagnostics.severity_ids(root, revision)
    except Exception as exc:  # noqa: BLE001
        _error(errors, error_records, "registry.read", "records", f"registry projection read failed: {exc}")
        return
    records = bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {}
    diagnostic_records = records.get("diagnostic_projections", []) if isinstance(records.get("diagnostic_projections"), list) else []
    refusal_records = records.get("refusal_projections", []) if isinstance(records.get("refusal_projections"), list) else []
    expected_diagnostics = {str(item.get("id") or item.get("code")): item for item in native_diagnostics[: len(diagnostic_records)]}
    for record in diagnostic_records:
        spec = record.get("spec", {}) if isinstance(record, dict) else {}
        native = expected_diagnostics.get(str(spec.get("diagnostic_id", "")))
        if native is None or spec.get("code") != native.get("code") or spec.get("severity") != native.get("severity") or spec.get("severity") not in severities:
            _error(errors, error_records, "diagnostic.registry", "records.diagnostic_projections", f"invalid diagnostic severity: {record.get('metadata', {}).get('id')}")
        if spec.get("severity_valid") is not True:
            _error(errors, error_records, "diagnostic.registry", "records.diagnostic_projections.spec.severity_valid", "diagnostic severity_valid must be true")
    expected_refusals = {str(item.get("refusal_id") or item.get("code")): item for item in native_refusals[: len(refusal_records)]}
    for record in refusal_records:
        spec = record.get("spec", {}) if isinstance(record, dict) else {}
        native = expected_refusals.get(str(spec.get("refusal_id", "")))
        if native is None or spec.get("code") != native.get("code") or spec.get("reason") != native.get("reason"):
            _error(errors, error_records, "refusal.registry", "records.refusal_projections", f"invalid refusal mapping: {record.get('metadata', {}).get('id')}")
        if not spec.get("reason"):
            _error(errors, error_records, "refusal.registry", "records.refusal_projections.spec.reason", "invalid refusal mapping")
    summary = bundle.get("registry_projection_summary", {}) if isinstance(bundle.get("registry_projection_summary"), dict) else {}
    diag_summary = summary.get("diagnostics", {}) if isinstance(summary.get("diagnostics"), dict) else {}
    ref_summary = summary.get("refusals", {}) if isinstance(summary.get("refusals"), dict) else {}

    source_files = {
        str(item.get("path")): item
        for item in bundle.get("source_snapshot", {}).get("selected_files", [])
        if isinstance(item, dict)
    }

    def check_summary(
        label: str,
        summary_obj: dict[str, Any],
        *,
        expected_path: str,
        native_items: list[dict[str, Any]],
        projected_records: list[dict[str, Any]],
        native_key: str,
        projected_key: str,
    ) -> None:
        native_ids = [str(item.get(native_key) or item.get("code")) for item in native_items]
        projected_ids = [str(item.get("spec", {}).get(projected_key, "")) for item in projected_records]
        omitted_ids = native_ids[len(projected_ids) :]
        source_entry = source_files.get(expected_path, {})
        expected_digest = source_entry.get("sha256")
        expected_git_object = {
            "mode": source_entry.get("mode", ""),
            "object_type": source_entry.get("object_type", ""),
            "git_object": source_entry.get("git_object", ""),
        }
        expected_selected_digest = sha256_bytes(models.stable_json(projected_ids).encode("utf-8"))
        expected_omitted_digest = sha256_bytes(models.stable_json(omitted_ids).encode("utf-8"))
        checks = [
            ("registry.summary_missing", "", bool(summary_obj), True, bool(summary_obj)),
            ("registry.source_digest", "source_registry_path", summary_obj.get("source_registry_path") == expected_path, expected_path, summary_obj.get("source_registry_path")),
            ("registry.source_digest", "source_registry_sha256", summary_obj.get("source_registry_sha256") == expected_digest, expected_digest, summary_obj.get("source_registry_sha256")),
            ("registry.source_digest", "source_registry_git_object", summary_obj.get("source_registry_git_object") == expected_git_object, expected_git_object, summary_obj.get("source_registry_git_object")),
            ("registry.source_revision", "source_revision", summary_obj.get("source_revision") == revision, revision, summary_obj.get("source_revision")),
            ("registry.native_count", "native_count", summary_obj.get("native_count") == len(native_ids), len(native_ids), summary_obj.get("native_count")),
            ("registry.projected_count", "projected_count", summary_obj.get("projected_count") == len(projected_ids), len(projected_ids), summary_obj.get("projected_count")),
            ("registry.omitted_count", "omitted_count", summary_obj.get("omitted_count") == len(omitted_ids), len(omitted_ids), summary_obj.get("omitted_count")),
            ("registry.selection_policy", "selection_policy", summary_obj.get("selection_policy") == "source_order_first_n", "source_order_first_n", summary_obj.get("selection_policy")),
            ("registry.selection_limit", "selection_limit", summary_obj.get("selection_limit") == 8, 8, summary_obj.get("selection_limit")),
            ("registry.projected_ids", "projected_ids", summary_obj.get("projected_ids") == projected_ids, projected_ids, summary_obj.get("projected_ids")),
            ("registry.selected_ids_digest", "selected_ids_sha256", summary_obj.get("selected_ids_sha256") == expected_selected_digest, expected_selected_digest, summary_obj.get("selected_ids_sha256")),
            ("registry.omitted_ids_digest", "omitted_ids_sha256", summary_obj.get("omitted_ids_sha256") == expected_omitted_digest, expected_omitted_digest, summary_obj.get("omitted_ids_sha256")),
            ("registry.truncation_disclosure", "truncation_disclosed", summary_obj.get("truncation_disclosed") is (len(omitted_ids) > 0), len(omitted_ids) > 0, summary_obj.get("truncation_disclosed")),
        ]
        for code, field, passed, expected, observed in checks:
            if not passed:
                path = f"registry_projection_summary.{label}" + (f".{field}" if field else "")
                _error(errors, error_records, code, path, f"{label} registry projection summary failed {field or 'presence'}", expected=expected, observed=observed)

    check_summary(
        "diagnostics",
        diag_summary,
        expected_path=diagnostics.DIAGNOSTIC_REGISTRY,
        native_items=native_diagnostics,
        projected_records=diagnostic_records,
        native_key="id",
        projected_key="diagnostic_id",
    )
    check_summary(
        "refusals",
        ref_summary,
        expected_path=refusals.REFUSAL_REGISTRY,
        native_items=native_refusals,
        projected_records=refusal_records,
        native_key="refusal_id",
        projected_key="refusal_id",
    )


def validate_bundle(bundle: dict[str, Any], *, dominium_root: str | Path | None = None) -> dict[str, Any]:
    errors: list[str] = []
    error_records: list[dict[str, Any]] = []
    warnings = list(models.WARNING_MESSAGES)
    if bundle.get("apiVersion") != models.API_VERSION:
        _error(errors, error_records, "api.version", "apiVersion", "apiVersion mismatch")
    if bundle.get("kind") != "DominiumReadonlySeamBundle":
        _error(errors, error_records, "kind.bundle", "kind", "kind must be DominiumReadonlySeamBundle")
    metadata = bundle.get("metadata", {}) if isinstance(bundle.get("metadata"), dict) else {}
    source = bundle.get("source_snapshot", {}) if isinstance(bundle.get("source_snapshot"), dict) else {}
    repo_identity = source.get("repository_identity", {}) if isinstance(source.get("repository_identity"), dict) else {}
    if repo_identity.get("canonical_identity") != "github.com/julesc013/dominium":
        _error(errors, error_records, "repository.identity", "source_snapshot.repository_identity.canonical_identity", "unexpected repository identity")
    revision = _check_revision_binding(bundle, errors, error_records)
    _check_common_metadata("bundle", metadata, errors, error_records, expected_revision=revision if is_commit_sha(revision) else None)
    if metadata.get("authority_role") != "generated_projection_not_canonical_truth":
        _error(errors, error_records, "authority.role", "metadata.authority_role", "bundle must be generated projection, not canonical authority")
    if bundle.get("explicit_non_capabilities") != models.EXPLICIT_NON_CAPABILITIES:
        _error(errors, error_records, "noncapability.explicit", "explicit_non_capabilities", "bundle explicit_non_capabilities mismatch")
    bundle_status = bundle.get("status", {}) if isinstance(bundle.get("status"), dict) else {}
    if bundle_status.get("generated_projection_marked_canonical") is not False:
        _error(errors, error_records, "authority.canonical_overclaim", "status.generated_projection_marked_canonical", "generated projection marked canonical", expected=False, observed=bundle_status.get("generated_projection_marked_canonical"))
    for field in models.FALSE_STATUS_FIELDS:
        if field not in bundle_status:
            _error(errors, error_records, "schema.status_required", f"status.{field}", f"bundle missing status.{field}", expected=False, observed="missing")
        elif bundle_status.get(field) is not False:
            _error(errors, error_records, "status.false_boundary", f"status.{field}", f"bundle status.{field} must be false", expected=False, observed=bundle_status.get(field))
    _check_selected_inputs(source, errors, error_records)
    _check_cardinality(bundle, errors, error_records)
    records = _all_records(bundle)
    ids = [str(item.get("metadata", {}).get("id", "")) for item in records]
    if len(ids) != len(set(ids)):
        _error(errors, error_records, "identity.duplicate", "records", "duplicate identity in seam records")
    for record in records:
        _check_record(record, errors, error_records, expected_revision=revision)
    _check_references(bundle, errors, error_records)
    _check_capabilities(bundle, errors, error_records)
    _check_events(bundle, errors, error_records)
    _check_bridge(bundle, errors, error_records)
    _check_registry_projection(bundle, errors, error_records, dominium_root=dominium_root, revision=revision)
    _check_digest_integrity(bundle, errors, error_records)
    selected = source.get("selected_files", []) if isinstance(source.get("selected_files"), list) else []
    if dominium_root is not None and is_commit_sha(revision):
        root = Path(dominium_root)
        for item in selected:
            if not isinstance(item, dict):
                continue
            rel = str(item.get("path", ""))
            try:
                payload = snapshot.git_object_bytes(root, revision, rel)
            except Exception as exc:  # noqa: BLE001
                _error(errors, error_records, "digest.source.read", f"source_snapshot.selected_files.{rel}", f"source digest recomputation failed: {rel}: {exc}")
                continue
            if sha256_bytes(payload) != item.get("sha256"):
                _error(errors, error_records, "digest.source", f"source_snapshot.selected_files.{rel}", f"source digest mismatch: {rel}")
    status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    return {
        "schema_version": "aide.dominium-readonly-seam.validation.v1",
        "task_id": models.REPAIR_TASK_ID,
        "validation_status": status,
        "status": status,
        "validated": not errors,
        "record_count": len(records),
        "selected_file_count": len(selected),
        "errors": errors,
        "error_records": error_records,
        "warnings": warnings,
        "explicit_non_capabilities_preserved": bundle.get("explicit_non_capabilities") == models.EXPLICIT_NON_CAPABILITIES,
        "source_revision_bound": is_commit_sha(revision),
        "digest_validity_checked": True,
        "bundle_self_digest_checked": True,
        "read_only_capability_boundary_preserved": not any(item["code"].startswith("capability.") for item in error_records),
        "deterministic_ordering_checked": True,
        "dominium_command_invoked": False,
        "network_call_performed": False,
        "provider_or_model_called": False,
        "worker_executed": False,
        "mutation_performed": False,
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }


def negative_fixture_cases(valid_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    cases = []
    for fixture in fixture_replay.negative_fixture_cases(valid_bundle):
        invalid = fixture_replay.materialize_fixture(fixture, valid_bundle)
        expected = fixture["expected_error_codes"][0]
        cases.append(
            {
                "name": fixture["name"],
                "expected_error": expected,
                "expected_error_codes": fixture["expected_error_codes"],
                "operations": fixture["operations"],
                "fixture": fixture,
                "bundle": invalid,
            }
        )
    return cases
