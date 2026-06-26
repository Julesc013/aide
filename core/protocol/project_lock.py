"""ProjectLock v0 helpers.

ProjectLock records a target-owned exact selection of one accepted
DistributionManifest and its selected components. It is not an install record,
install plan, admission record, authorization, or target mutation mechanism.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import distribution_manifest, envelope


API_VERSION = envelope.API_VERSION
KIND = "ProjectLock"
SCHEMA_VERSION = "aide.project-lock.v0"
PROTOCOL_VERSION = "0.1.0"
TASK_ID = "AIDE-BUILD-PROJECT-LOCK-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-PROJECT-LOCK-V0-01"
PROPOSED_CAPABILITY = "project_lock_v0"
DETERMINISTIC_TIMESTAMP = "fixture-timestamp:project-lock-v0"

REPORT_ROOT = Path(".aide/reports/project-lock-v0")
SCHEMA_PATH = Path(".aide/protocol/aide-project-lock-v0.schema.json")
FIXTURE_ROOT = Path(".aide/fixtures/project-lock-v0")

LOCK_JSON = REPORT_ROOT / "project-lock.json"
LOCK_MD = REPORT_ROOT / "project-lock.md"
STATUS_MD = REPORT_ROOT / "status.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
DIGEST_BINDING_JSON = REPORT_ROOT / "digest-binding.json"
COMPONENT_SELECTION_JSON = REPORT_ROOT / "component-selection.json"
DEPENDENCY_CLOSURE_JSON = REPORT_ROOT / "dependency-closure.json"
FIXTURE_MATRIX_JSON = REPORT_ROOT / "fixture-matrix.json"
FIXTURE_MATRIX_MD = REPORT_ROOT / "fixture-matrix.md"
NON_CAPABILITIES_MD = REPORT_ROOT / "non-capabilities.md"

DISTRIBUTION_MANIFEST_JSON = distribution_manifest.MANIFEST_JSON
DISTRIBUTION_ACCEPTANCE_JSON = Path(".aide/reports/distribution-manifest-v1-accept/acceptance-report.json")

SUPPORTED_REQUIRED_FEATURES = {
    "project_lock_v0",
    "distribution_manifest_v1",
    "portable_release_bundle_v0",
    "sha256_digest_canonical_json_v1",
}
SUPPORTED_OPTIONAL_FEATURES = {
    "project_overlay_refs_v0",
    "knowledge_overlay_refs_v0",
}
SUPPORTED_INSTALL_MODES = {"metadata_only_no_apply", "portable_pack_selection_only_no_apply"}
SUPPORTED_CHANNELS = distribution_manifest.SUPPORTED_CHANNELS

REFUSAL_CODES = [
    "project_lock.missing",
    "project_lock.invalid",
    "project_lock.manifest_not_accepted",
    "project_lock.digest_mismatch",
    "project_lock.payload_digest_mismatch",
    "project_lock.component_missing",
    "project_lock.component_digest_mismatch",
    "project_lock.required_component_omitted",
    "project_lock.optional_component_ambiguous",
    "project_lock.dependency_unsatisfied",
    "project_lock.dependency_cycle",
    "project_lock.protocol_incompatible",
    "project_lock.unknown_required_feature",
    "project_lock.absolute_path_forbidden",
    "project_lock.path_traversal_forbidden",
    "project_lock.secret_or_credential_forbidden",
    "project_lock.source_state_contamination",
    "project_lock.channel_digest_drift",
    "project_lock.target_overlay_invalid",
    "project_lock.extension_required_unknown",
]

EXPLICIT_NON_CAPABILITIES = [
    "install_truth",
    "install_plan",
    "install_apply",
    "update_apply",
    "repair_apply",
    "rollback_apply",
    "uninstall_apply",
    "admission",
    "authorization",
    "target_repository_mutation",
    "release_publication",
    "git_tag_creation",
    "github_release_creation",
    "upload",
    "network_call",
    "provider_model_call",
    "workbench_runtime",
    "mcp_runtime",
    "source_change_preview_apply_rollback",
    "promotion",
]

PATH_FIELDS = {
    "bridge_package_selections",
    "host_package_selections",
    "policy_overlay_refs",
    "knowledge_overlay_refs",
}
SECRET_LIKE_RE = re.compile(r"(^|[/_.-])(secret|secrets|credential|credentials|token|tokens|api[_-]?key|\\.env)([/_.-]|$)", re.IGNORECASE)


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def canonical_json_bytes(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_digest(data: bytes) -> str:
    return distribution_manifest.sha256_digest(data)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_json(path: Path, data: dict[str, Any]) -> None:
    write_text(path, stable_json(data))


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not load JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def load_distribution_manifest(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / DISTRIBUTION_MANIFEST_JSON
    if path.exists():
        return read_json(path)
    return distribution_manifest.build_distribution_manifest(repo_root)


def load_distribution_acceptance(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / DISTRIBUTION_ACCEPTANCE_JSON
    if not path.exists():
        return {}
    return read_json(path)


def distribution_is_accepted(repo_root: str | Path, manifest: dict[str, Any]) -> bool:
    acceptance = load_distribution_acceptance(repo_root)
    return (
        acceptance.get("result") == "ACCEPTED_WITH_WARNINGS"
        and acceptance.get("accepted_capability") == "distribution_manifest_v1"
        and acceptance.get("distribution_digest") == manifest.get("status", {}).get("distribution_digest")
        and acceptance.get("manifest_payload_digest") == manifest.get("status", {}).get("manifest_payload_digest")
    )


def selected_component_from_manifest(component: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "component_ref": component["component_ref"],
        "component_id": component["component_id"],
        "selected_digest": component["content_digest"],
        "required": bool(component.get("required", False)),
        "source_distribution_ref": manifest["metadata"]["distribution_ref"],
        "dependencies": sorted(str(item) for item in component.get("dependencies", [])),
        "protocol_requirements": sorted(str(item) for item in component.get("protocol_requirements", [])),
        "selected_artifact_refs": sorted(str(item) for item in component.get("artifact_refs", [])),
        "compatibility_constraints": copy.deepcopy(component.get("compatibility_constraints", {})),
        "extensions": {},
    }


def build_project_lock(repo_root: str | Path) -> dict[str, Any]:
    manifest = load_distribution_manifest(repo_root)
    required_components = [
        selected_component_from_manifest(component, manifest)
        for component in manifest.get("spec", {}).get("components", [])
        if isinstance(component, dict) and component.get("required") is True
    ]
    optional_components = [
        component
        for component in manifest.get("spec", {}).get("components", [])
        if isinstance(component, dict) and component.get("required") is not True
    ]
    lock = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "project_lock_ref": "aide://project-lock/aide-self-aide-lite-pack-v0",
            "project_ref": "aide://project/aide-self",
            "project_identity": "julesc013/aide",
            "project_profile": "aide-self-hosting",
            "lock_revision": "0",
            "selected_distribution_ref": manifest["metadata"]["distribution_ref"],
            "selected_distribution_digest": manifest["status"]["distribution_digest"],
            "manifest_payload_digest": manifest["status"]["manifest_payload_digest"],
            "selected_channel": manifest["metadata"]["channel"],
            "created_from": "accepted_distribution_manifest_v1",
            "created_at_classification": "deterministic_projection_not_wall_clock",
            "prior_lock_ref": None,
            "superseded_by_ref": None,
            "extensions": {},
        },
        "spec": {
            "selected_components": required_components,
            "omitted_optional_components": [
                {
                    "component_ref": component["component_ref"],
                    "component_id": component["component_id"],
                    "reason": "optional_component_not_selected",
                    "extensions": {},
                }
                for component in optional_components
            ],
            "required_component_closure": required_component_closure(required_components),
            "bridge_package_selections": [],
            "host_package_selections": [],
            "policy_overlay_refs": [],
            "knowledge_overlay_refs": [],
            "compatibility_range": copy.deepcopy(manifest["spec"]["protocol"]["protocol_range"]),
            "install_mode": "portable_pack_selection_only_no_apply",
            "target_platform_profile": "portable-local-no-apply",
            "warnings": [
                "ProjectLock selects an accepted DistributionManifest but does not install it.",
                "Channel is informational; digests are authoritative.",
            ],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "required_features": ["project_lock_v0", "distribution_manifest_v1", "sha256_digest_canonical_json_v1"],
            "optional_features": ["project_overlay_refs_v0", "knowledge_overlay_refs_v0"],
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "project_lock_digest": "",
            "validation_result": "PASS_WITH_WARNINGS",
            "recommended_next_task": CHECK_TASK_ID,
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "admission_implemented": False,
            "authorization_implemented": False,
            "extensions": {},
        },
        "extensions": {},
    }
    return finalize_project_lock(lock)


def required_component_closure(selected_components: list[dict[str, Any]]) -> list[str]:
    refs = {str(component.get("component_ref", "")) for component in selected_components}
    for component in selected_components:
        refs.update(str(item) for item in component.get("dependencies", []) if isinstance(item, str))
    return sorted(ref for ref in refs if ref)


def canonicalize_project_lock(lock: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(lock)
    spec = data.get("spec")
    if isinstance(spec, dict):
        if isinstance(spec.get("selected_components"), list):
            spec["selected_components"] = sorted(
                (canonicalize_selected_component(item) for item in spec["selected_components"] if isinstance(item, dict)),
                key=lambda item: str(item.get("component_ref", "")),
            )
        if isinstance(spec.get("omitted_optional_components"), list):
            spec["omitted_optional_components"] = sorted(
                (copy.deepcopy(item) for item in spec["omitted_optional_components"] if isinstance(item, dict)),
                key=lambda item: str(item.get("component_ref", "")),
            )
        for key in [
            "required_component_closure",
            "bridge_package_selections",
            "host_package_selections",
            "policy_overlay_refs",
            "knowledge_overlay_refs",
            "warnings",
            "explicit_non_capabilities",
            "required_features",
            "optional_features",
        ]:
            if isinstance(spec.get(key), list):
                spec[key] = sorted(spec[key], key=lambda item: json.dumps(item, sort_keys=True))
    return data


def canonicalize_selected_component(component: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(component)
    for key in ["dependencies", "protocol_requirements", "selected_artifact_refs"]:
        if isinstance(data.get(key), list):
            data[key] = sorted(str(item) for item in data[key])
    return data


def project_lock_payload_for_digest(lock: dict[str, Any]) -> dict[str, Any]:
    data = canonicalize_project_lock(lock)
    data.pop("status", None)
    metadata = data.get("metadata")
    if isinstance(metadata, dict):
        metadata.pop("selected_channel", None)
    return data


def project_lock_digest(lock: dict[str, Any]) -> str:
    return sha256_digest(canonical_json_bytes(project_lock_payload_for_digest(lock)))


def finalize_project_lock(lock: dict[str, Any]) -> dict[str, Any]:
    data = canonicalize_project_lock(lock)
    status = data.setdefault("status", {})
    status["project_lock_digest"] = project_lock_digest(data)
    return data


def _add_error(errors: list[dict[str, str]], code: str, message: str) -> None:
    errors.append({"code": code, "message": message})


def _validation_result(errors: list[dict[str, str]], warnings: list[str]) -> dict[str, Any]:
    codes = sorted({item["code"] for item in errors})
    return {
        "valid": not errors,
        "status": "PASS" if not errors else "FAILED_VALIDATION",
        "error_count": len(errors),
        "errors": errors,
        "refusal_codes": codes,
        "warnings": warnings,
    }


def _path_refusal_code(value: str) -> str | None:
    normalized = distribution_manifest.normalize_rel(value)
    if not normalized:
        return None
    if distribution_manifest.is_absolute_or_traversal(normalized):
        if ".." in [part for part in normalized.split("/") if part]:
            return "project_lock.path_traversal_forbidden"
        return "project_lock.absolute_path_forbidden"
    if SECRET_LIKE_RE.search(normalized):
        return "project_lock.secret_or_credential_forbidden"
    if distribution_manifest.forbidden_member_reason(normalized):
        return "project_lock.source_state_contamination"
    return None


def _iter_string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(_iter_string_values(item))
        return result
    if isinstance(value, dict):
        result = []
        for item in value.values():
            result.extend(_iter_string_values(item))
        return result
    return []


def validate_project_lock_object(
    lock: dict[str, Any] | None,
    *,
    distribution: dict[str, Any] | None = None,
    repo_root: str | Path | None = None,
    require_manifest_acceptance: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[str] = []
    if lock is None:
        _add_error(errors, "project_lock.missing", "ProjectLock is missing")
        return _validation_result(errors, warnings)
    if not isinstance(lock, dict):
        _add_error(errors, "project_lock.invalid", "ProjectLock root must be an object")
        return _validation_result(errors, warnings)
    for field in ["apiVersion", "kind", "schema_version", "metadata", "spec", "status"]:
        if field not in lock:
            _add_error(errors, "project_lock.invalid", f"missing required field: {field}")
    if lock.get("kind") != KIND:
        _add_error(errors, "project_lock.invalid", "kind must be ProjectLock")
    if lock.get("schema_version") != SCHEMA_VERSION:
        _add_error(errors, "project_lock.invalid", f"schema_version must be {SCHEMA_VERSION}")
    metadata = lock.get("metadata") if isinstance(lock.get("metadata"), dict) else {}
    spec = lock.get("spec") if isinstance(lock.get("spec"), dict) else {}
    status = lock.get("status") if isinstance(lock.get("status"), dict) else {}
    manifest = distribution if distribution is not None else load_distribution_manifest(repo_root or Path("."))
    manifest_validation = distribution_manifest.validate_distribution_manifest_object(manifest, repo_root=repo_root, require_artifact_files=False)
    if not manifest_validation["valid"]:
        _add_error(errors, "project_lock.manifest_not_accepted", "source DistributionManifest does not validate")
    if require_manifest_acceptance and (repo_root is None or not distribution_is_accepted(repo_root, manifest)):
        _add_error(errors, "project_lock.manifest_not_accepted", "source DistributionManifest is not accepted")
    manifest_status = manifest.get("status", {}) if isinstance(manifest.get("status"), dict) else {}
    manifest_metadata = manifest.get("metadata", {}) if isinstance(manifest.get("metadata"), dict) else {}
    manifest_spec = manifest.get("spec", {}) if isinstance(manifest.get("spec"), dict) else {}
    if metadata.get("selected_distribution_ref") != manifest_metadata.get("distribution_ref"):
        _add_error(errors, "project_lock.digest_mismatch", "selected_distribution_ref does not match manifest")
    if metadata.get("selected_distribution_digest") != manifest_status.get("distribution_digest"):
        _add_error(errors, "project_lock.digest_mismatch", "selected_distribution_digest does not match manifest")
    if metadata.get("manifest_payload_digest") != manifest_status.get("manifest_payload_digest"):
        _add_error(errors, "project_lock.payload_digest_mismatch", "manifest_payload_digest does not match manifest")
    if metadata.get("selected_channel") not in SUPPORTED_CHANNELS:
        _add_error(errors, "project_lock.invalid", "selected_channel is not supported")
    if metadata.get("selected_channel") != manifest_metadata.get("channel") and metadata.get("selected_distribution_digest") != manifest_status.get("distribution_digest"):
        _add_error(errors, "project_lock.channel_digest_drift", "channel and digest drift together")
    if spec.get("install_mode") not in SUPPORTED_INSTALL_MODES:
        _add_error(errors, "project_lock.invalid", "unsupported install_mode")
    protocol = {"protocol_range": spec.get("compatibility_range"), "min_reader_version": "1.0.0", "min_writer_version": "1.0.0"}
    if not distribution_manifest.protocol_range_includes_current(protocol):
        _add_error(errors, "project_lock.protocol_incompatible", "compatibility_range does not include supported v1 distribution protocol")
    for feature in spec.get("required_features", []) if isinstance(spec.get("required_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES:
            _add_error(errors, "project_lock.unknown_required_feature", f"unknown required feature: {feature}")
    for feature in spec.get("optional_features", []) if isinstance(spec.get("optional_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES and feature not in SUPPORTED_OPTIONAL_FEATURES:
            warnings.append(f"unknown optional feature tolerated: {feature}")
    _validate_extension_requirements(lock, errors)
    for field in PATH_FIELDS:
        for value in _iter_string_values(spec.get(field, [])):
            code = _path_refusal_code(value)
            if code:
                _add_error(errors, code, f"{field} contains forbidden path/reference: {value}")
            if field in {"policy_overlay_refs", "knowledge_overlay_refs"} and value.startswith("aide://source/"):
                _add_error(errors, "project_lock.target_overlay_invalid", f"{field} must remain target-owned: {value}")
    selected_components = spec.get("selected_components", [])
    omitted_optional = spec.get("omitted_optional_components", [])
    if not isinstance(selected_components, list):
        _add_error(errors, "project_lock.invalid", "selected_components must be an array")
        selected_components = []
    if not isinstance(omitted_optional, list):
        _add_error(errors, "project_lock.invalid", "omitted_optional_components must be an array")
        omitted_optional = []
    manifest_components = {
        str(component.get("component_ref")): component
        for component in manifest_spec.get("components", [])
        if isinstance(component, dict)
    }
    manifest_artifacts = {
        str(artifact.get("artifact_ref")): artifact
        for artifact in manifest_spec.get("artifacts", [])
        if isinstance(artifact, dict)
    }
    selected_refs: set[str] = set()
    dependency_graph: dict[str, list[str]] = {}
    for component in selected_components:
        if not isinstance(component, dict):
            _add_error(errors, "project_lock.invalid", "selected component entries must be objects")
            continue
        ref = str(component.get("component_ref", ""))
        if ref in selected_refs:
            _add_error(errors, "project_lock.invalid", f"duplicate selected component: {ref}")
        selected_refs.add(ref)
        source_component = manifest_components.get(ref)
        if source_component is None:
            _add_error(errors, "project_lock.component_missing", f"selected component not found in manifest: {ref}")
            continue
        if component.get("component_id") != source_component.get("component_id"):
            _add_error(errors, "project_lock.component_missing", f"component_id mismatch for {ref}")
        if component.get("selected_digest") != source_component.get("content_digest"):
            _add_error(errors, "project_lock.component_digest_mismatch", f"component digest mismatch for {ref}")
        if bool(component.get("required", False)) != bool(source_component.get("required", False)):
            _add_error(errors, "project_lock.component_digest_mismatch", f"component required flag mismatch for {ref}")
        dependencies = sorted(str(item) for item in component.get("dependencies", []) if isinstance(item, str)) if isinstance(component.get("dependencies"), list) else []
        expected_dependencies = sorted(str(item) for item in source_component.get("dependencies", []) if isinstance(item, str))
        if dependencies != expected_dependencies:
            _add_error(errors, "project_lock.dependency_unsatisfied", f"dependency list mismatch for {ref}")
        dependency_graph[ref] = dependencies
        expected_artifacts = set(str(item) for item in source_component.get("artifact_refs", []) if isinstance(item, str))
        selected_artifacts = set(str(item) for item in component.get("selected_artifact_refs", []) if isinstance(item, str))
        if not selected_artifacts:
            _add_error(errors, "project_lock.component_missing", f"selected component has no artifacts: {ref}")
        for artifact_ref in selected_artifacts:
            if artifact_ref not in manifest_artifacts or artifact_ref not in expected_artifacts:
                _add_error(errors, "project_lock.component_missing", f"selected artifact does not resolve for {ref}: {artifact_ref}")
        for requirement in component.get("protocol_requirements", []) if isinstance(component.get("protocol_requirements"), list) else []:
            if requirement not in SUPPORTED_REQUIRED_FEATURES and requirement not in SUPPORTED_OPTIONAL_FEATURES:
                _add_error(errors, "project_lock.unknown_required_feature", f"unknown component protocol requirement: {requirement}")
        if not distribution_manifest.compatibility_constraints_include_current(component.get("compatibility_constraints")):
            _add_error(errors, "project_lock.protocol_incompatible", f"component constraints incompatible: {ref}")
    omitted_refs = {
        str(component.get("component_ref"))
        for component in omitted_optional
        if isinstance(component, dict)
    }
    for ref, source_component in manifest_components.items():
        if source_component.get("required") is True and ref not in selected_refs:
            _add_error(errors, "project_lock.required_component_omitted", f"required component omitted: {ref}")
        if source_component.get("required") is not True:
            if (ref in selected_refs and ref in omitted_refs) or (ref not in selected_refs and ref not in omitted_refs):
                _add_error(errors, "project_lock.optional_component_ambiguous", f"optional component selection is ambiguous: {ref}")
    for ref, dependencies in dependency_graph.items():
        for dependency in dependencies:
            if dependency not in selected_refs:
                _add_error(errors, "project_lock.dependency_unsatisfied", f"dependency not selected for {ref}: {dependency}")
    closure = sorted(str(item) for item in spec.get("required_component_closure", []) if isinstance(item, str)) if isinstance(spec.get("required_component_closure"), list) else []
    expected_closure = required_component_closure([item for item in selected_components if isinstance(item, dict)])
    if closure != expected_closure:
        _add_error(errors, "project_lock.dependency_unsatisfied", "required_component_closure mismatch")
    for cycle in distribution_manifest.component_dependency_cycles(dependency_graph):
        _add_error(errors, "project_lock.dependency_cycle", f"component dependency cycle: {' -> '.join(cycle)}")
    for field in [
        "install_apply_implemented",
        "update_apply_implemented",
        "target_repository_mutation_implemented",
        "admission_implemented",
        "authorization_implemented",
    ]:
        if status.get(field) is not False:
            _add_error(errors, "project_lock.invalid", f"{field} must be false")
    expected_digest = project_lock_digest(lock)
    if status.get("project_lock_digest") != expected_digest:
        _add_error(errors, "project_lock.digest_mismatch", "project_lock_digest does not match canonical payload")
    return _validation_result(errors, warnings)


def _validate_extension_requirements(value: Any, errors: list[dict[str, str]]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).startswith("requires."):
                _add_error(errors, "project_lock.extension_required_unknown", f"unknown required extension: {key}")
            _validate_extension_requirements(child, errors)
    elif isinstance(value, list):
        for child in value:
            _validate_extension_requirements(child, errors)


def minimal_fixture_lock() -> dict[str, Any]:
    manifest = distribution_manifest.minimal_fixture_manifest()
    component = selected_component_from_manifest(manifest["spec"]["components"][0], manifest)
    lock = build_lock_from_manifest(manifest)
    lock["metadata"]["project_lock_ref"] = "aide://project-lock/fixture-minimal"
    lock["metadata"]["project_ref"] = "aide://project/fixture"
    lock["metadata"]["project_identity"] = "fixture/project"
    lock["metadata"]["project_profile"] = "fixture"
    lock["spec"]["selected_components"] = [component]
    lock["spec"]["required_component_closure"] = required_component_closure([component])
    return finalize_project_lock(lock)


def build_lock_from_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    required_components = [
        selected_component_from_manifest(component, manifest)
        for component in manifest.get("spec", {}).get("components", [])
        if isinstance(component, dict) and component.get("required") is True
    ]
    optional_components = [
        component
        for component in manifest.get("spec", {}).get("components", [])
        if isinstance(component, dict) and component.get("required") is not True
    ]
    lock = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "project_lock_ref": "aide://project-lock/fixture",
            "project_ref": "aide://project/fixture",
            "project_identity": "fixture/project",
            "project_profile": "fixture",
            "lock_revision": "0",
            "selected_distribution_ref": manifest["metadata"]["distribution_ref"],
            "selected_distribution_digest": manifest["status"]["distribution_digest"],
            "manifest_payload_digest": manifest["status"]["manifest_payload_digest"],
            "selected_channel": manifest["metadata"]["channel"],
            "created_from": "fixture",
            "created_at_classification": DETERMINISTIC_TIMESTAMP,
            "prior_lock_ref": None,
            "superseded_by_ref": None,
            "extensions": {},
        },
        "spec": {
            "selected_components": required_components,
            "omitted_optional_components": [
                {"component_ref": item["component_ref"], "component_id": item["component_id"], "reason": "optional_component_not_selected", "extensions": {}}
                for item in optional_components
            ],
            "required_component_closure": required_component_closure(required_components),
            "bridge_package_selections": [],
            "host_package_selections": [],
            "policy_overlay_refs": [],
            "knowledge_overlay_refs": [],
            "compatibility_range": copy.deepcopy(manifest["spec"]["protocol"]["protocol_range"]),
            "install_mode": "metadata_only_no_apply",
            "target_platform_profile": "fixture",
            "warnings": [],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "required_features": ["project_lock_v0", "distribution_manifest_v1", "sha256_digest_canonical_json_v1"],
            "optional_features": [],
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "project_lock_digest": "",
            "validation_result": "PASS_WITH_WARNINGS",
            "recommended_next_task": CHECK_TASK_ID,
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "admission_implemented": False,
            "authorization_implemented": False,
            "extensions": {},
        },
        "extensions": {},
    }
    return finalize_project_lock(lock)


def add_optional_component(manifest: dict[str, Any]) -> str:
    component = copy.deepcopy(manifest["spec"]["components"][0])
    component["component_ref"] = distribution_manifest.component_ref("optional-addon")
    component["component_id"] = "optional-addon"
    component["required"] = False
    artifact_by_ref = {
        str(artifact.get("artifact_ref")): artifact
        for artifact in manifest["spec"].get("artifacts", [])
        if isinstance(artifact, dict)
    }
    component["content_digest"] = distribution_manifest.component_digest(
        distribution_manifest.component_digest_payload(component, artifact_by_ref)
    )
    manifest["spec"]["components"].append(component)
    return component["component_ref"]


def write_fixture_corpus(repo_root: str | Path) -> None:
    root = Path(repo_root)
    valid_root = root / FIXTURE_ROOT / "valid"
    invalid_root = root / FIXTURE_ROOT / "invalid"
    valid_root.mkdir(parents=True, exist_ok=True)
    invalid_root.mkdir(parents=True, exist_ok=True)
    minimal = minimal_fixture_lock()
    write_json(valid_root / "minimal-valid-lock.json", minimal)
    full = build_project_lock(root)
    write_json(valid_root / "full-valid-lock.json", full)
    write_json(valid_root / "reordered-deterministic-lock.json", reordered_lock(full))
    optional_manifest = distribution_manifest.minimal_fixture_manifest()
    optional_ref = add_optional_component(optional_manifest)
    optional_selected = build_lock_from_manifest(distribution_manifest.finalize_manifest(optional_manifest))
    optional_component = selected_component_from_manifest(
        next(component for component in optional_manifest["spec"]["components"] if component["component_ref"] == optional_ref),
        optional_manifest,
    )
    optional_selected["spec"]["selected_components"].append(optional_component)
    optional_selected["spec"]["omitted_optional_components"] = []
    optional_selected["spec"]["required_component_closure"] = required_component_closure(optional_selected["spec"]["selected_components"])
    write_json(valid_root / "optional-component-selected.json", finalize_project_lock(optional_selected))
    optional_omitted = build_lock_from_manifest(distribution_manifest.finalize_manifest(optional_manifest))
    write_json(valid_root / "optional-component-omitted.json", optional_omitted)
    unknown_optional = copy.deepcopy(minimal)
    unknown_optional["spec"]["optional_features"].append("future.optional.project-lock")
    write_json(valid_root / "unknown-optional-feature-preserved.json", finalize_project_lock(unknown_optional))
    extension_round_trip = copy.deepcopy(minimal)
    extension_round_trip["metadata"]["extensions"] = {"operator.note": {"value": "preserve"}}
    extension_round_trip["spec"]["extensions"] = {"future.optional": {"enabled": True}}
    extension_round_trip["extensions"] = {"top.optional": True}
    write_json(valid_root / "extension-round-trip.json", finalize_project_lock(extension_round_trip))
    channel_change = copy.deepcopy(minimal)
    channel_change["metadata"]["selected_channel"] = "stable"
    write_json(valid_root / "channel-changed-digest-unchanged.json", finalize_project_lock(channel_change))

    invalid_cases = {
        "manifest-digest-mismatch": manifest_digest_mismatch,
        "manifest-payload-digest-mismatch": manifest_payload_digest_mismatch,
        "manifest-not-accepted": lambda lock: lock,
        "component-digest-mismatch": component_digest_mismatch,
        "missing-required-component": missing_required_component,
        "optional-component-ambiguous": optional_component_ambiguous,
        "unknown-component": unknown_component,
        "unsatisfied-dependency": unsatisfied_dependency,
        "dependency-cycle": dependency_cycle,
        "unsupported-protocol": unsupported_protocol,
        "unknown-required-feature": unknown_required_feature,
        "channel-changed-unapproved-digest": channel_digest_drift,
        "target-overlay-invalid": target_overlay_invalid,
        "secret-like-field": secret_like_field,
        "absolute-path": absolute_path,
        "traversal-path": traversal_path,
        "source-latest-reference": source_latest_reference,
        "source-report-reference": source_report_reference,
        "aide-local-reference": aide_local_reference,
        "extension-required-unknown": extension_required_unknown,
    }
    for name, mutator in invalid_cases.items():
        lock = copy.deepcopy(minimal)
        if name == "optional-component-ambiguous":
            manifest = distribution_manifest.minimal_fixture_manifest()
            add_optional_component(manifest)
            lock = build_lock_from_manifest(distribution_manifest.finalize_manifest(manifest))
            lock["spec"]["omitted_optional_components"] = []
        mutator(lock)
        write_json(invalid_root / f"{name}.json", finalize_project_lock(lock))


def reordered_lock(lock: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(lock)
    data["spec"]["selected_components"] = list(reversed(data["spec"]["selected_components"]))
    data["spec"]["required_features"] = list(reversed(data["spec"]["required_features"]))
    return finalize_project_lock(data)


def manifest_digest_mismatch(lock: dict[str, Any]) -> None:
    lock["metadata"]["selected_distribution_digest"] = "sha256:" + "1" * 64


def manifest_payload_digest_mismatch(lock: dict[str, Any]) -> None:
    lock["metadata"]["manifest_payload_digest"] = "sha256:" + "2" * 64


def component_digest_mismatch(lock: dict[str, Any]) -> None:
    lock["spec"]["selected_components"][0]["selected_digest"] = "sha256:" + "3" * 64


def missing_required_component(lock: dict[str, Any]) -> None:
    lock["spec"]["selected_components"] = []
    lock["spec"]["required_component_closure"] = []


def optional_component_ambiguous(lock: dict[str, Any]) -> None:
    del lock


def unknown_component(lock: dict[str, Any]) -> None:
    lock["spec"]["selected_components"][0]["component_ref"] = "aide://distribution/component/missing"


def unsatisfied_dependency(lock: dict[str, Any]) -> None:
    lock["spec"]["selected_components"][0]["dependencies"] = ["aide://distribution/component/missing"]


def dependency_cycle(lock: dict[str, Any]) -> None:
    ref = lock["spec"]["selected_components"][0]["component_ref"]
    lock["spec"]["selected_components"][0]["dependencies"] = [ref]
    lock["spec"]["required_component_closure"] = [ref]


def unsupported_protocol(lock: dict[str, Any]) -> None:
    lock["spec"]["compatibility_range"] = {"min": "2.0.0", "max": "2.x"}


def unknown_required_feature(lock: dict[str, Any]) -> None:
    lock["spec"]["required_features"].append("future.required.project-lock")


def channel_digest_drift(lock: dict[str, Any]) -> None:
    lock["metadata"]["selected_channel"] = "stable"
    lock["metadata"]["selected_distribution_digest"] = "sha256:" + "4" * 64


def target_overlay_invalid(lock: dict[str, Any]) -> None:
    lock["spec"]["policy_overlay_refs"] = ["aide://source/.aide/context/latest-task-packet.md"]


def secret_like_field(lock: dict[str, Any]) -> None:
    lock["spec"]["bridge_package_selections"] = ["config/secrets/token.txt"]


def absolute_path(lock: dict[str, Any]) -> None:
    lock["spec"]["host_package_selections"] = ["C:/tmp/aide"]


def traversal_path(lock: dict[str, Any]) -> None:
    lock["spec"]["host_package_selections"] = ["../outside"]


def source_latest_reference(lock: dict[str, Any]) -> None:
    lock["spec"]["knowledge_overlay_refs"] = [".aide/context/latest-task-packet.md"]


def source_report_reference(lock: dict[str, Any]) -> None:
    lock["spec"]["knowledge_overlay_refs"] = [".aide/reports/source-report.json"]


def aide_local_reference(lock: dict[str, Any]) -> None:
    lock["spec"]["knowledge_overlay_refs"] = [".aide.local/state.sqlite"]


def extension_required_unknown(lock: dict[str, Any]) -> None:
    lock["extensions"] = {"requires.future": {"enabled": True}}


INVALID_FIXTURE_EXPECTATIONS = {
    "absolute-path": ["project_lock.absolute_path_forbidden"],
    "aide-local-reference": ["project_lock.source_state_contamination"],
    "channel-changed-unapproved-digest": ["project_lock.digest_mismatch", "project_lock.channel_digest_drift"],
    "component-digest-mismatch": ["project_lock.component_digest_mismatch"],
    "dependency-cycle": ["project_lock.dependency_cycle", "project_lock.dependency_unsatisfied"],
    "extension-required-unknown": ["project_lock.extension_required_unknown"],
    "manifest-digest-mismatch": ["project_lock.digest_mismatch"],
    "manifest-not-accepted": ["project_lock.manifest_not_accepted"],
    "manifest-payload-digest-mismatch": ["project_lock.payload_digest_mismatch"],
    "missing-required-component": ["project_lock.required_component_omitted"],
    "optional-component-ambiguous": ["project_lock.optional_component_ambiguous"],
    "secret-like-field": ["project_lock.secret_or_credential_forbidden"],
    "source-latest-reference": ["project_lock.source_state_contamination"],
    "source-report-reference": ["project_lock.source_state_contamination"],
    "target-overlay-invalid": ["project_lock.target_overlay_invalid"],
    "traversal-path": ["project_lock.path_traversal_forbidden"],
    "unknown-component": ["project_lock.component_missing"],
    "unknown-required-feature": ["project_lock.unknown_required_feature"],
    "unsatisfied-dependency": ["project_lock.dependency_unsatisfied"],
    "unsupported-protocol": ["project_lock.protocol_incompatible"],
}


def fixture_matrix(repo_root: str | Path) -> list[dict[str, Any]]:
    root = Path(repo_root)
    fixtures: list[dict[str, Any]] = []
    for path in sorted((root / FIXTURE_ROOT / "valid").glob("*.json")):
        fixtures.append({"case_id": path.stem, "path": repo_rel(path, root), "expected_result": "PASS", "expected_refusal_codes": []})
    for path in sorted((root / FIXTURE_ROOT / "invalid").glob("*.json")):
        fixtures.append(
            {
                "case_id": path.stem,
                "path": repo_rel(path, root),
                "expected_result": "FAILED_VALIDATION",
                "expected_refusal_codes": INVALID_FIXTURE_EXPECTATIONS.get(path.stem, []),
            }
        )
    return fixtures


def load_schema(repo_root: str | Path) -> dict[str, Any]:
    return read_json(Path(repo_root) / SCHEMA_PATH)


def status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    report = {
        "schema_version": "aide.project-lock-status.v0",
        "status": "PASS_WITH_WARNINGS",
        "proposed_capability": PROPOSED_CAPABILITY,
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/project_lock.py").exists(),
        "distribution_manifest_report_exists": (root / DISTRIBUTION_MANIFEST_JSON).exists(),
        "distribution_acceptance_report_exists": (root / DISTRIBUTION_ACCEPTANCE_JSON).exists(),
        "project_lock_report_exists": (root / LOCK_JSON).exists(),
        "validation_report_exists": (root / VALIDATION_JSON).exists(),
        "refusal_codes": REFUSAL_CODES,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "recommended_next_task": CHECK_TASK_ID,
        "install_apply_implemented": False,
        "update_apply_implemented": False,
        "target_repository_mutation_implemented": False,
        "admission_implemented": False,
        "authorization_implemented": False,
        "warnings": ["ProjectLock v0 remains proposed until independent check and acceptance."],
    }
    write_text(root / STATUS_MD, render_status_md(report))
    return report


def project(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    lock = build_project_lock(root)
    write_json(root / LOCK_JSON, lock)
    write_text(root / LOCK_MD, render_lock_md(lock))
    write_fixture_corpus(root)
    digest_binding = {
        "schema_version": "aide.project-lock-digest-binding.v0",
        "selected_distribution_ref": lock["metadata"]["selected_distribution_ref"],
        "selected_distribution_digest": lock["metadata"]["selected_distribution_digest"],
        "manifest_payload_digest": lock["metadata"]["manifest_payload_digest"],
        "project_lock_digest": lock["status"]["project_lock_digest"],
        "channel_in_digest": False,
    }
    write_json(root / DIGEST_BINDING_JSON, digest_binding)
    component_selection = {
        "schema_version": "aide.project-lock-component-selection.v0",
        "selected_components": lock["spec"]["selected_components"],
        "omitted_optional_components": lock["spec"]["omitted_optional_components"],
    }
    write_json(root / COMPONENT_SELECTION_JSON, component_selection)
    dependency_closure = {
        "schema_version": "aide.project-lock-dependency-closure.v0",
        "required_component_closure": lock["spec"]["required_component_closure"],
    }
    write_json(root / DEPENDENCY_CLOSURE_JSON, dependency_closure)
    matrix = fixture_matrix(root)
    write_json(root / FIXTURE_MATRIX_JSON, {"schema_version": "aide.project-lock-fixture-matrix.v0", "fixtures": matrix})
    write_text(root / FIXTURE_MATRIX_MD, render_fixture_matrix_md(matrix))
    write_text(root / NON_CAPABILITIES_MD, render_non_capabilities_md())
    report = {
        "schema_version": "aide.project-lock-project-report.v0",
        "status": "PASS_WITH_WARNINGS",
        "proposed_capability": PROPOSED_CAPABILITY,
        "project_lock_path": LOCK_JSON.as_posix(),
        "project_lock_digest": lock["status"]["project_lock_digest"],
        "selected_distribution_digest": lock["metadata"]["selected_distribution_digest"],
        "manifest_payload_digest": lock["metadata"]["manifest_payload_digest"],
        "selected_component_count": len(lock["spec"]["selected_components"]),
        "source_artifacts_mutated": False,
        "recommended_next_task": CHECK_TASK_ID,
        "warnings": lock["spec"]["warnings"],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
    }
    status(root)
    return report


def validate(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    project_report = project(root)
    lock = read_json(root / LOCK_JSON)
    manifest = load_distribution_manifest(root)
    lock_validation = validate_project_lock_object(lock, distribution=manifest, repo_root=root)
    schema = load_schema(root)
    schema_alignment_errors = schema_alignment_errors_for(schema)
    fixture_results = []
    for fixture in fixture_matrix(root):
        data = read_json(root / fixture["path"])
        fixture_distribution = fixture_distribution_for_case(fixture["case_id"])
        result = validate_project_lock_object(data, distribution=fixture_distribution, repo_root=None, require_manifest_acceptance=False)
        if fixture["case_id"] in {"full-valid-lock", "reordered-deterministic-lock"}:
            result = validate_project_lock_object(data, distribution=manifest, repo_root=root, require_manifest_acceptance=True)
        if fixture["case_id"] == "manifest-not-accepted":
            result = validate_project_lock_object(data, distribution=fixture_distribution, repo_root=None, require_manifest_acceptance=True)
        expected_codes = set(fixture.get("expected_refusal_codes", []))
        observed_codes = set(result["refusal_codes"])
        expected_valid = fixture["expected_result"] == "PASS"
        fixture_results.append(
            {
                **fixture,
                "observed_result": "PASS" if result["valid"] else "FAILED_VALIDATION",
                "observed_refusal_codes": sorted(observed_codes),
                "passed": (result["valid"] is expected_valid) and expected_codes.issubset(observed_codes),
            }
        )
    fixture_pass = all(item["passed"] for item in fixture_results)
    checks = {
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/project_lock.py").exists(),
        "cli_registered": cli_registered(root),
        "lock_generated": (root / LOCK_JSON).exists(),
        "lock_valid": lock_validation["valid"],
        "schema_alignment": not schema_alignment_errors,
        "fixture_matrix_passed": fixture_pass,
        "distribution_manifest_accepted": distribution_is_accepted(root, manifest),
        "selected_distribution_digest_bound": lock["metadata"]["selected_distribution_digest"] == manifest["status"]["distribution_digest"],
        "manifest_payload_digest_bound": lock["metadata"]["manifest_payload_digest"] == manifest["status"]["manifest_payload_digest"],
        "component_selection_complete": not any(code in lock_validation["refusal_codes"] for code in ["project_lock.required_component_omitted", "project_lock.optional_component_ambiguous", "project_lock.dependency_unsatisfied"]),
        "channel_informational": project_lock_digest(channel_changed_copy(lock)) == lock["status"]["project_lock_digest"],
        "install_apply_not_implemented": lock["status"]["install_apply_implemented"] is False,
        "update_apply_not_implemented": lock["status"]["update_apply_implemented"] is False,
        "target_repository_mutation_not_implemented": lock["status"]["target_repository_mutation_implemented"] is False,
        "admission_not_implemented": lock["status"]["admission_implemented"] is False,
        "authorization_not_implemented": lock["status"]["authorization_implemented"] is False,
        "absolute_local_paths_suppressed": not contains_absolute_local_path(lock),
    }
    errors = [key for key, value in checks.items() if not value]
    status_value = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    report = {
        "schema_version": "aide.project-lock-validation.v0",
        "validation_status": status_value,
        "status": status_value,
        "proposed_capability": PROPOSED_CAPABILITY,
        "checks": checks,
        "errors": errors,
        "schema_alignment_errors": schema_alignment_errors,
        "lock_validation": lock_validation,
        "fixture_results": fixture_results,
        "project_report": project_report,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "warnings": [
            "ProjectLock v0 is proposed until independent check and acceptance.",
            "ProjectLock selects an accepted DistributionManifest but performs no install or target mutation.",
        ],
        "recommended_next_task": CHECK_TASK_ID,
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_md(report))
    return report


def fixture_distribution_for_case(case_id: str) -> dict[str, Any]:
    manifest = distribution_manifest.minimal_fixture_manifest()
    if case_id in {"optional-component-selected", "optional-component-omitted", "optional-component-ambiguous"}:
        add_optional_component(manifest)
        manifest = distribution_manifest.finalize_manifest(manifest)
    return manifest


def channel_changed_copy(lock: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(lock)
    data["metadata"]["selected_channel"] = "stable" if data["metadata"].get("selected_channel") != "stable" else "canary"
    return finalize_project_lock(data)


def schema_alignment_errors_for(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema must declare Draft 2020-12")
    if schema.get("title") != "AIDE ProjectLock v0":
        errors.append("schema title mismatch")
    for field in ["apiVersion", "kind", "schema_version", "metadata", "spec", "status", "extensions"]:
        if field not in schema.get("required", []):
            errors.append(f"schema missing required field: {field}")
    return errors


def cli_registered(repo_root: Path) -> bool:
    script = repo_root / ".aide/scripts/aide_lite.py"
    if not script.exists():
        return False
    text = script.read_text(encoding="utf-8")
    return "project-lock" in text and "command_project_lock_validate" in text


def contains_absolute_local_path(data: Any) -> bool:
    if isinstance(data, dict):
        return any(contains_absolute_local_path(value) for value in data.values())
    if isinstance(data, list):
        return any(contains_absolute_local_path(value) for value in data)
    if isinstance(data, str):
        return bool(re.match(r"^[A-Za-z]:[/\\]", data) or data.startswith("/Users/") or data.startswith("/home/"))
    return False


def render_status_md(data: dict[str, Any]) -> str:
    lines = [
        "# ProjectLock v0 Status",
        "",
        f"- status: {data.get('status')}",
        f"- proposed_capability: {data.get('proposed_capability')}",
        f"- schema_exists: {str(data.get('schema_exists')).lower()}",
        f"- helper_exists: {str(data.get('helper_exists')).lower()}",
        f"- distribution_manifest_report_exists: {str(data.get('distribution_manifest_report_exists')).lower()}",
        f"- distribution_acceptance_report_exists: {str(data.get('distribution_acceptance_report_exists')).lower()}",
        f"- recommended_next_task: {data.get('recommended_next_task')}",
        "",
        "## Explicit Non-Capabilities",
        "",
    ]
    for item in EXPLICIT_NON_CAPABILITIES:
        lines.append(f"- {item}: false")
    return "\n".join(lines) + "\n"


def render_lock_md(lock: dict[str, Any]) -> str:
    lines = [
        "# ProjectLock v0 Projection",
        "",
        f"- project_lock_ref: `{lock['metadata']['project_lock_ref']}`",
        f"- selected_distribution_ref: `{lock['metadata']['selected_distribution_ref']}`",
        f"- selected_distribution_digest: `{lock['metadata']['selected_distribution_digest']}`",
        f"- manifest_payload_digest: `{lock['metadata']['manifest_payload_digest']}`",
        f"- project_lock_digest: `{lock['status']['project_lock_digest']}`",
        f"- selected_component_count: {len(lock['spec']['selected_components'])}",
        "- channel_informational: true",
        "- install_apply_implemented: false",
        "- admission_implemented: false",
        "- authorization_implemented: false",
        "- target_repository_mutation_implemented: false",
        "",
        "## Selected Components",
        "",
    ]
    for component in lock["spec"]["selected_components"]:
        lines.append(f"- `{component['component_ref']}`: {component['selected_digest']}")
    return "\n".join(lines) + "\n"


def render_fixture_matrix_md(fixtures: list[dict[str, Any]]) -> str:
    lines = ["# ProjectLock Fixture Matrix", "", "| Case | Expected | Codes |", "| --- | --- | --- |"]
    for fixture in fixtures:
        codes = ", ".join(fixture.get("expected_refusal_codes", [])) or "none"
        lines.append(f"| {fixture['case_id']} | {fixture['expected_result']} | {codes} |")
    return "\n".join(lines) + "\n"


def render_non_capabilities_md() -> str:
    lines = ["# ProjectLock v0 Explicit Non-Capabilities", ""]
    for item in EXPLICIT_NON_CAPABILITIES:
        lines.append(f"- {item}: false")
    return "\n".join(lines) + "\n"


def render_validation_md(report: dict[str, Any]) -> str:
    lines = [
        "# ProjectLock v0 Validation",
        "",
        f"- result: {report.get('validation_status')}",
        f"- proposed_capability: {report.get('proposed_capability')}",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Checks",
        "",
    ]
    for key, value in report.get("checks", {}).items():
        lines.append(f"- {key}: {str(value).lower()}")
    lines.extend(["", "## Fixture Results", ""])
    for item in report.get("fixture_results", []):
        lines.append(f"- {item['case_id']}: {str(item['passed']).lower()} ({item['observed_result']})")
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"
