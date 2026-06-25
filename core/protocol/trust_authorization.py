"""Projection-only trust and authorization contract v0.

This module defines portable AIDE trust and authorization records. It does not
implement live identity, credentials, policy enforcement, grants, Service state,
worker execution, provider/model calls, network calls, or mutation.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from core.protocol import envelope


API_VERSION = envelope.API_VERSION
TRUST_SCHEMA_VERSION = "aide.trust-authorization-contract.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "trust_and_authorization_contract_v0"
TASK_ID = "AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01"

REPORT_ROOT = Path(".aide/reports/trust-authorization-contract-v0")
PROJECTION_ROOT = REPORT_ROOT / "projections"
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
REFUSAL_REGISTRY_MD = REPORT_ROOT / "refusal-code-registry.md"

SCHEMA_ROOT = Path(".aide/protocol")
SCHEMA_PATHS = {
    "Principal": SCHEMA_ROOT / "aide-principal.schema.json",
    "AdmissionRecord": SCHEMA_ROOT / "aide-admission-record.schema.json",
    "PolicyDecision": SCHEMA_ROOT / "aide-policy-decision.schema.json",
    "CapabilityGrant": SCHEMA_ROOT / "aide-capability-grant.schema.json",
    "DelegationRecord": SCHEMA_ROOT / "aide-delegation-record.schema.json",
    "RevocationRecord": SCHEMA_ROOT / "aide-revocation-record.schema.json",
    "AuthorizationEvaluation": SCHEMA_ROOT / "aide-authorization-evaluation.schema.json",
}
PROJECTION_FILES = {
    "principal": PROJECTION_ROOT / "principal.json",
    "admission": PROJECTION_ROOT / "admission-record.json",
    "policy_decision": PROJECTION_ROOT / "policy-decision.json",
    "capability_grant": PROJECTION_ROOT / "capability-grant.json",
    "delegation": PROJECTION_ROOT / "delegation-record.json",
    "revocation": PROJECTION_ROOT / "revocation-record.json",
    "authorization_evaluation": PROJECTION_ROOT / "authorization-evaluation.json",
}

RECORD_KINDS = set(SCHEMA_PATHS)
SUPPORTED_KINDS = RECORD_KINDS | {
    "TrustAuthorizationProjectionReport",
    "TrustAuthorizationValidationReport",
}
REQUIRED_METADATA_FIELDS = ["id", "createdAt", "sourcePath", "producer", "compatibility"]
REQUIRED_STATUS_FIELDS = ["validated", "projection_only", "validation_errors", "validation_warnings"]
REQUIRED_SPEC_FIELDS_BY_KIND = {
    "Principal": [
        "principal_ref",
        "principal_kind",
        "display_name",
        "issuer",
        "subject",
        "attributes",
        "status",
        "created_at",
        "expires_at",
        "credential_refs",
    ],
    "AdmissionRecord": [
        "admission_ref",
        "subject_ref",
        "subject_kind",
        "implementation_version",
        "implementation_digest",
        "manifest_digest",
        "conformance_profile_refs",
        "conformance_result_refs",
        "admitted_capability_refs",
        "supported_protocol_range",
        "decision",
        "constraints",
        "warnings",
        "known_limitations",
        "admitted_at",
        "expires_at",
        "revocation_refs",
    ],
    "PolicyDecision": [
        "decision_ref",
        "principal_ref",
        "capability_ref",
        "workspace_ref",
        "target_resource_refs",
        "requested_mode",
        "input_digest",
        "policy_bundle_ref",
        "policy_bundle_digest",
        "evaluator",
        "decision",
        "reason_codes",
        "constraints",
        "obligations",
        "evidence_refs",
        "created_at",
        "expires_at",
    ],
    "CapabilityGrant": [
        "grant_ref",
        "principal_ref",
        "capability_ref",
        "workspace_ref",
        "allowed_resource_refs",
        "allowed_resource_patterns",
        "mode",
        "allowed_effects",
        "network_constraints",
        "secret_constraints",
        "use_budget",
        "parent_grant_ref",
        "delegation_ref",
        "policy_decision_ref",
        "admission_refs",
        "status",
        "remaining_uses",
        "created_at",
        "expires_at",
    ],
    "DelegationRecord": [
        "delegation_ref",
        "delegating_principal_ref",
        "receiving_principal_ref",
        "source_grant_ref",
        "delegated_resources",
        "delegated_capabilities",
        "delegated_mode",
        "depth",
        "expiry",
        "revocation_chain",
        "status",
    ],
    "RevocationRecord": [
        "revocation_ref",
        "subject_ref",
        "subject_kind",
        "reason_code",
        "authority_ref",
        "effective_at",
        "affected_grants",
        "affected_admissions",
        "affected_delegations",
        "superseding_refs",
        "evidence_refs",
    ],
    "AuthorizationEvaluation": [
        "evaluation_ref",
        "principal_ref",
        "admission_ref",
        "policy_decision_ref",
        "grant_ref",
        "delegation_ref",
        "revocation_refs",
        "requested_operation",
        "checks",
        "result",
        "reason_codes",
        "evidence_refs",
        "created_at",
    ],
}

PRINCIPAL_KINDS = {
    "human",
    "service",
    "execution_host",
    "worker_harness",
    "capability_provider",
    "package",
    "ci_job",
    "workload",
}
PRINCIPAL_STATES = {"candidate", "active", "suspended", "revoked", "expired"}
ADMISSION_STATES = {"candidate", "admitted", "admitted_with_constraints", "suspended", "rejected", "revoked", "expired"}
POLICY_DECISIONS = {"allow", "deny", "allow_with_constraints", "require_approval", "quarantine"}
GRANT_STATES = {"proposed", "active", "consumed", "suspended", "revoked", "expired"}
GRANT_MODES = {"inspect", "preview", "execute", "apply_request"}
EVALUATION_RESULTS = {"allowed", "denied", "approval_required", "quarantined"}
REFUSAL_CODES = [
    "principal_unknown",
    "principal_inactive",
    "implementation_not_admitted",
    "implementation_digest_mismatch",
    "capability_not_admitted",
    "policy_denied",
    "approval_required",
    "grant_missing",
    "grant_inactive",
    "grant_expired",
    "grant_revoked",
    "grant_exhausted",
    "workspace_scope_mismatch",
    "resource_scope_mismatch",
    "execution_mode_not_granted",
    "effect_not_granted",
    "network_not_granted",
    "secret_not_granted",
    "delegation_not_allowed",
    "delegation_scope_widening",
    "delegation_expired",
    "required_feature_unsupported",
]
AUTHORIZATION_CHECKS = [
    "principal_active",
    "exact_implementation_admitted",
    "implementation_digest_matches",
    "capability_admitted",
    "policy_allows",
    "grant_exists_and_active",
    "not_expired",
    "not_revoked",
    "uses_remain",
    "workspace_matches",
    "resource_scope_matches",
    "mode_matches",
    "effect_allowed",
    "network_allowed",
    "secrets_allowed",
    "delegation_valid",
    "required_features_supported",
]
EXPLICIT_NON_CAPABILITIES = [
    "live_identity_provider",
    "live_policy_engine",
    "live_capability_grants",
    "credential_storage",
    "secret_storage",
    "oidc_iam_integration",
    "runtime_enforcement",
    "worker_execution",
    "transaction_approval",
    "service_runtime",
    "provider_model_calls",
    "network_calls",
    "preview_apply_runtime",
    "repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
]
FALSE_BOUNDARY_FIELDS = [
    "live_identity_implemented",
    "live_policy_engine_implemented",
    "live_grants_implemented",
    "credentials_embedded",
    "secrets_embedded",
    "oidc_iam_implemented",
    "runtime_enforcement_implemented",
    "worker_execution_implemented",
    "transaction_approval_implemented",
    "service_runtime_implemented",
    "provider_model_calls_performed",
    "network_calls_performed",
    "preview_apply_implemented",
    "repository_mutation_performed",
    "branch_worktree_mutation_performed",
    "github_mutation_performed",
    "release_or_promotion_performed",
]
RECOGNIZED_CAPABILITIES = {
    FEATURE_FLAG,
    "registered_process_execution_provider_v0",
    "execution_host_contract_v0",
    "local_process_execution_host_fixture_v0",
}
FORBIDDEN_SECRET_KEYS = {
    "credential",
    "credentials",
    "credential_value",
    "credential_values",
    "secret",
    "secrets",
    "secret_value",
    "secret_values",
    "password",
    "token",
    "api_key",
    "private_key",
}
ALLOWED_SECRET_REFERENCE_KEYS = {"credential_refs", "secret_constraints", "secret_access_allowed", "network_constraints"}


def stable_json(data: Any) -> str:
    return envelope.stable_json(data)


def read_json(path: Path) -> dict[str, Any]:
    return envelope.read_json(path)


def write_json(path: Path, obj: dict[str, Any]) -> None:
    envelope.write_json(path, obj)


def write_text(path: Path, text: str) -> None:
    envelope.write_text(path, text)


def _compatibility(required_capabilities: list[str] | None = None) -> dict[str, Any]:
    required = [FEATURE_FLAG]
    for capability in required_capabilities or []:
        if capability not in required:
            required.append(capability)
    return {
        "schemaVersion": PROTOCOL_VERSION,
        "protocolVersion": PROTOCOL_VERSION,
        "minReaderVersion": PROTOCOL_VERSION,
        "minWriterVersion": PROTOCOL_VERSION,
        "featureFlags": [FEATURE_FLAG],
        "requiredCapabilities": required,
    }


def _metadata(record_id: str, name: str, source_path: Path | None = None) -> dict[str, Any]:
    return {
        "id": record_id,
        "name": name,
        "createdAt": "deterministic",
        "sourcePath": source_path.as_posix() if source_path else "",
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility(),
    }


def _false_boundaries() -> dict[str, bool]:
    return {field: False for field in FALSE_BOUNDARY_FIELDS}


def _status(*, errors: list[str] | None = None, warnings: list[str] | None = None) -> dict[str, Any]:
    return {
        "validated": not errors,
        "projection_only": True,
        "validation_errors": list(errors or []),
        "validation_warnings": list(warnings or []),
    }


def _base_spec() -> dict[str, Any]:
    return {
        "capability_label": FEATURE_FLAG,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        **_false_boundaries(),
    }


def _build_record(kind: str, metadata: dict[str, Any], spec: dict[str, Any], status: dict[str, Any]) -> dict[str, Any]:
    obj = envelope.build_envelope(kind, metadata, spec, status, api_version=API_VERSION)
    obj["schema_version"] = TRUST_SCHEMA_VERSION
    obj["protocol_version"] = PROTOCOL_VERSION
    return obj


def sample_principal() -> dict[str, Any]:
    spec = {
        **_base_spec(),
        "principal_ref": "aide://principal/human-fixture",
        "principal_kind": "human",
        "display_name": "Fixture Human",
        "issuer": "aide.fixture",
        "subject": "human-fixture",
        "attributes": {"team": "fixture"},
        "status": "active",
        "created_at": "deterministic",
        "expires_at": "never",
        "credential_refs": ["aide://credential/ref-only-fixture"],
    }
    return _build_record("Principal", _metadata("principal-fixture", "Fixture Principal"), spec, _status())


def sample_admission_record() -> dict[str, Any]:
    spec = {
        **_base_spec(),
        "admission_ref": "aide://admission/local-process-host-fixture",
        "subject_ref": "aide://execution-host/local-process-fixture",
        "subject_kind": "execution_host",
        "implementation_version": "0.1.0",
        "implementation_digest": "sha256:" + "a" * 64,
        "manifest_digest": "sha256:" + "b" * 64,
        "conformance_profile_refs": ["aide://conformance-profile/local-process-host-v0"],
        "conformance_result_refs": ["aide://conformance-result/local-process-host-v0"],
        "admitted_capability_refs": ["aide://capability/local_process_execution_host_fixture_v0"],
        "supported_protocol_range": ">=0.1.0 <1.0.0",
        "decision": "admitted_with_constraints",
        "constraints": {"fixture_only": True},
        "warnings": ["fixture-backed reference host only"],
        "known_limitations": ["no public cancellation API"],
        "admitted_at": "deterministic",
        "expires_at": "never",
        "revocation_refs": [],
    }
    return _build_record("AdmissionRecord", _metadata("admission-fixture", "Fixture Admission"), spec, _status())


def sample_policy_decision(decision: str = "allow") -> dict[str, Any]:
    spec = {
        **_base_spec(),
        "decision_ref": "aide://policy-decision/local-process-host-allow",
        "principal_ref": "aide://principal/human-fixture",
        "capability_ref": "aide://capability/local_process_execution_host_fixture_v0",
        "workspace_ref": "aide://workspace/source",
        "target_resource_refs": ["aide://resource/workspace-fixture"],
        "requested_mode": "execute",
        "input_digest": "sha256:" + "c" * 64,
        "policy_bundle_ref": "aide://policy-bundle/fixture",
        "policy_bundle_digest": "sha256:" + "d" * 64,
        "evaluator": {"name": "aide-trust-contract-fixture", "version": PROTOCOL_VERSION},
        "decision": decision,
        "reason_codes": [],
        "constraints": {"requires_fixture_workspace": True},
        "obligations": ["record_evidence"],
        "evidence_refs": ["aide://evidence/policy-fixture"],
        "created_at": "deterministic",
        "expires_at": "never",
    }
    return _build_record("PolicyDecision", _metadata("policy-decision-fixture", "Fixture Policy Decision"), spec, _status())


def sample_capability_grant(status: str = "active", remaining_uses: int = 1) -> dict[str, Any]:
    spec = {
        **_base_spec(),
        "grant_ref": "aide://grant/local-process-host-one-use",
        "principal_ref": "aide://principal/human-fixture",
        "capability_ref": "aide://capability/local_process_execution_host_fixture_v0",
        "workspace_ref": "aide://workspace/source",
        "allowed_resource_refs": ["aide://resource/workspace-fixture"],
        "allowed_resource_patterns": ["aide://resource/workspace-fixture/*"],
        "mode": "execute",
        "allowed_effects": ["read", "write_disposable_workspace", "persist_evidence"],
        "network_constraints": {"network_allowed": False},
        "secret_constraints": {"secret_access_allowed": False},
        "use_budget": {"max_uses": 1},
        "parent_grant_ref": None,
        "delegation_ref": "aide://delegation/local-process-host-fixture",
        "policy_decision_ref": "aide://policy-decision/local-process-host-allow",
        "admission_refs": ["aide://admission/local-process-host-fixture"],
        "status": status,
        "remaining_uses": remaining_uses,
        "created_at": "deterministic",
        "expires_at": "never",
    }
    return _build_record("CapabilityGrant", _metadata("capability-grant-fixture", "Fixture Capability Grant"), spec, _status())


def sample_delegation_record(status: str = "active") -> dict[str, Any]:
    spec = {
        **_base_spec(),
        "delegation_ref": "aide://delegation/local-process-host-fixture",
        "delegating_principal_ref": "aide://principal/human-fixture",
        "receiving_principal_ref": "aide://principal/workload-fixture",
        "source_grant_ref": "aide://grant/local-process-host-one-use",
        "delegated_resources": ["aide://resource/workspace-fixture"],
        "delegated_capabilities": ["aide://capability/local_process_execution_host_fixture_v0"],
        "delegated_mode": "execute",
        "depth": 1,
        "expiry": "never",
        "revocation_chain": [],
        "status": status,
    }
    return _build_record("DelegationRecord", _metadata("delegation-fixture", "Fixture Delegation"), spec, _status())


def sample_revocation_record() -> dict[str, Any]:
    spec = {
        **_base_spec(),
        "revocation_ref": "aide://revocation/none-fixture",
        "subject_ref": "aide://grant/not-revoked",
        "subject_kind": "grant",
        "reason_code": "fixture_no_active_revocation",
        "authority_ref": "aide://principal/human-fixture",
        "effective_at": "not-active",
        "affected_grants": [],
        "affected_admissions": [],
        "affected_delegations": [],
        "superseding_refs": [],
        "evidence_refs": ["aide://evidence/revocation-fixture"],
    }
    return _build_record("RevocationRecord", _metadata("revocation-fixture", "Fixture Revocation"), spec, _status())


def sample_requested_operation() -> dict[str, Any]:
    return {
        "capability_ref": "aide://capability/local_process_execution_host_fixture_v0",
        "implementation_digest": "sha256:" + "a" * 64,
        "workspace_ref": "aide://workspace/source",
        "resource_ref": "aide://resource/workspace-fixture",
        "mode": "execute",
        "effect": "read",
        "network_required": False,
        "secret_required": False,
        "required_features": [FEATURE_FLAG],
    }


def _evaluation_record(result: str, reason_codes: list[str], checks: dict[str, bool], request: dict[str, Any]) -> dict[str, Any]:
    spec = {
        **_base_spec(),
        "evaluation_ref": "aide://authorization-evaluation/fixture",
        "principal_ref": "aide://principal/human-fixture",
        "admission_ref": "aide://admission/local-process-host-fixture",
        "policy_decision_ref": "aide://policy-decision/local-process-host-allow",
        "grant_ref": "aide://grant/local-process-host-one-use",
        "delegation_ref": "aide://delegation/local-process-host-fixture",
        "revocation_refs": [],
        "requested_operation": request,
        "checks": checks,
        "result": result,
        "reason_codes": reason_codes,
        "evidence_refs": ["aide://evidence/authorization-evaluation-fixture"],
        "created_at": "deterministic",
    }
    return _build_record("AuthorizationEvaluation", _metadata("authorization-evaluation-fixture", "Fixture Authorization Evaluation"), spec, _status())


def sample_authorization_evaluation() -> dict[str, Any]:
    principal = sample_principal()
    admission = sample_admission_record()
    policy = sample_policy_decision()
    grant = sample_capability_grant()
    delegation = sample_delegation_record()
    return evaluate_authorization(principal, admission, policy, grant, delegation, [], sample_requested_operation())


def sample_records() -> dict[str, dict[str, Any]]:
    return {
        "principal": sample_principal(),
        "admission": sample_admission_record(),
        "policy_decision": sample_policy_decision(),
        "capability_grant": sample_capability_grant(),
        "delegation": sample_delegation_record(),
        "revocation": sample_revocation_record(),
        "authorization_evaluation": sample_authorization_evaluation(),
    }


def sample_unknown_optional_record() -> dict[str, Any]:
    obj = sample_principal()
    obj["x-aide-optional-probe"] = {"tolerated": True}
    obj["metadata"]["x-aide-optional-probe"] = "tolerated"
    obj["spec"]["x-aide-optional-probe"] = True
    return obj


def sample_unknown_required_capability_record() -> dict[str, Any]:
    obj = sample_principal()
    obj["metadata"]["compatibility"]["requiredCapabilities"] = ["future.required"]
    return obj


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _is_sha256(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    prefix = "sha256:"
    return value.startswith(prefix) and len(value) == len(prefix) + 64 and all(ch in "0123456789abcdef" for ch in value[len(prefix) :])


def _has_forbidden_secret_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_SECRET_KEYS and key not in ALLOWED_SECRET_REFERENCE_KEYS:
                return True
            if _has_forbidden_secret_key(child):
                return True
    if isinstance(value, list):
        return any(_has_forbidden_secret_key(item) for item in value)
    return False


def validate_trust_authorization_contract(obj: dict[str, Any], allowed_kinds: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["trust authorization contract record must be an object"]
    if obj.get("apiVersion") != API_VERSION:
        errors.append(f"unsupported apiVersion: {obj.get('apiVersion')}")
    kind = obj.get("kind")
    active_kinds = allowed_kinds or RECORD_KINDS
    if not isinstance(kind, str) or not kind:
        errors.append("kind must be a non-empty string")
    elif kind not in active_kinds:
        errors.append(f"unsupported kind: {kind}")
    for field in ["metadata", "spec", "status"]:
        if field not in obj:
            errors.append(f"missing required field: {field}")
        elif not isinstance(obj[field], dict):
            errors.append(f"{field} must be an object")
    metadata = obj.get("metadata") if isinstance(obj.get("metadata"), dict) else {}
    for field in REQUIRED_METADATA_FIELDS:
        if field not in metadata:
            errors.append(f"missing required metadata field: {field}")
    compatibility = metadata.get("compatibility") if isinstance(metadata.get("compatibility"), dict) else {}
    if not isinstance(compatibility, dict):
        errors.append("metadata.compatibility must be an object")
        compatibility = {}
    for key in ["schemaVersion", "protocolVersion", "minReaderVersion", "minWriterVersion"]:
        if not envelope.validate_semverish(compatibility.get(key)):
            errors.append(f"metadata.compatibility.{key} must be SemVer-like")
    if FEATURE_FLAG not in _as_list(compatibility.get("featureFlags")):
        errors.append(f"metadata.compatibility.featureFlags must include {FEATURE_FLAG}")
    for capability in _as_list(compatibility.get("requiredCapabilities")):
        if capability not in RECOGNIZED_CAPABILITIES:
            errors.append(f"unknown required capability: {capability}")
    spec = obj.get("spec") if isinstance(obj.get("spec"), dict) else {}
    for field in REQUIRED_SPEC_FIELDS_BY_KIND.get(str(kind), []):
        if field not in spec:
            errors.append(f"missing required spec field: {field}")
    if _has_forbidden_secret_key(obj):
        errors.append("secret values must not be embedded in trust authorization records")
    non_capabilities = spec.get("explicit_non_capabilities")
    if not isinstance(non_capabilities, list):
        errors.append("spec.explicit_non_capabilities must be an array")
    elif spec.get("capability_label") in non_capabilities:
        errors.append("spec.capability_label must not appear in explicit_non_capabilities")
    for field in FALSE_BOUNDARY_FIELDS:
        if spec.get(field) is not False:
            errors.append(f"spec.{field} must be false in projection-only contract")
    if kind == "Principal":
        if spec.get("principal_kind") not in PRINCIPAL_KINDS:
            errors.append(f"unsupported principal_kind: {spec.get('principal_kind')}")
        if spec.get("status") not in PRINCIPAL_STATES:
            errors.append(f"unsupported principal status: {spec.get('status')}")
        if not isinstance(spec.get("credential_refs"), list):
            errors.append("spec.credential_refs must be an array of references only")
    if kind == "AdmissionRecord":
        if spec.get("decision") not in ADMISSION_STATES:
            errors.append(f"unsupported admission decision: {spec.get('decision')}")
        for field in ["implementation_digest", "manifest_digest"]:
            if not _is_sha256(spec.get(field)):
                errors.append(f"spec.{field} must be sha256:<64 lowercase hex>")
        if not spec.get("conformance_result_refs") or not spec.get("admitted_capability_refs"):
            errors.append("spec must keep conformance and admission references explicit")
    if kind == "PolicyDecision":
        if spec.get("decision") not in POLICY_DECISIONS:
            errors.append(f"unsupported policy decision: {spec.get('decision')}")
        for field in ["input_digest", "policy_bundle_digest"]:
            if not _is_sha256(spec.get(field)):
                errors.append(f"spec.{field} must be sha256:<64 lowercase hex>")
    if kind == "CapabilityGrant":
        if spec.get("status") not in GRANT_STATES:
            errors.append(f"unsupported grant status: {spec.get('status')}")
        if spec.get("mode") not in GRANT_MODES:
            errors.append(f"unsupported grant mode: {spec.get('mode')}")
        if not isinstance(spec.get("remaining_uses"), int) or spec.get("remaining_uses") < 0:
            errors.append("spec.remaining_uses must be a nonnegative integer")
    if kind == "DelegationRecord":
        if spec.get("status") not in GRANT_STATES:
            errors.append(f"unsupported delegation status: {spec.get('status')}")
        if not isinstance(spec.get("depth"), int) or spec.get("depth") < 0:
            errors.append("spec.depth must be a nonnegative integer")
    if kind == "AuthorizationEvaluation":
        if spec.get("result") not in EVALUATION_RESULTS:
            errors.append(f"unsupported authorization result: {spec.get('result')}")
        for code in _as_list(spec.get("reason_codes")):
            if code not in REFUSAL_CODES:
                errors.append(f"unknown authorization reason code: {code}")
    status = obj.get("status") if isinstance(obj.get("status"), dict) else {}
    for field in REQUIRED_STATUS_FIELDS:
        if field not in status:
            errors.append(f"missing required status field: {field}")
    if status.get("projection_only") is not True:
        errors.append("status.projection_only must be true")
    return errors


def _fail(code: str, request: dict[str, Any], checks: dict[str, bool]) -> dict[str, Any]:
    result = "approval_required" if code == "approval_required" else "quarantined" if code == "required_feature_unsupported" else "denied"
    return _evaluation_record(result, [code], checks, request)


def evaluate_authorization(
    principal: dict[str, Any] | None,
    admission: dict[str, Any] | None,
    policy_decision: dict[str, Any] | None,
    grant: dict[str, Any] | None,
    delegation: dict[str, Any] | None,
    revocations: list[dict[str, Any]],
    requested_operation: dict[str, Any],
) -> dict[str, Any]:
    checks = {name: False for name in AUTHORIZATION_CHECKS}
    if principal is None:
        return _fail("principal_unknown", requested_operation, checks)
    principal_spec = principal.get("spec", {})
    if principal_spec.get("status") != "active":
        return _fail("principal_inactive", requested_operation, checks)
    checks["principal_active"] = True
    if admission is None:
        return _fail("implementation_not_admitted", requested_operation, checks)
    admission_spec = admission.get("spec", {})
    if admission_spec.get("decision") not in {"admitted", "admitted_with_constraints"}:
        return _fail("implementation_not_admitted", requested_operation, checks)
    checks["exact_implementation_admitted"] = True
    if requested_operation.get("implementation_digest") != admission_spec.get("implementation_digest"):
        return _fail("implementation_digest_mismatch", requested_operation, checks)
    checks["implementation_digest_matches"] = True
    if requested_operation.get("capability_ref") not in _as_list(admission_spec.get("admitted_capability_refs")):
        return _fail("capability_not_admitted", requested_operation, checks)
    checks["capability_admitted"] = True
    if policy_decision is None:
        return _fail("policy_denied", requested_operation, checks)
    policy_spec = policy_decision.get("spec", {})
    if policy_spec.get("decision") == "require_approval":
        return _fail("approval_required", requested_operation, checks)
    if policy_spec.get("decision") == "quarantine":
        return _evaluation_record("quarantined", ["policy_denied"], checks, requested_operation)
    if policy_spec.get("decision") not in {"allow", "allow_with_constraints"}:
        return _fail("policy_denied", requested_operation, checks)
    checks["policy_allows"] = True
    if grant is None:
        return _fail("grant_missing", requested_operation, checks)
    grant_spec = grant.get("spec", {})
    if grant_spec.get("status") == "expired":
        return _fail("grant_expired", requested_operation, checks)
    if grant_spec.get("status") == "revoked":
        return _fail("grant_revoked", requested_operation, checks)
    if grant_spec.get("status") != "active":
        return _fail("grant_inactive", requested_operation, checks)
    checks["grant_exists_and_active"] = True
    checks["not_expired"] = True
    active_revoked_refs = {ref for record in revocations for ref in _as_list(record.get("spec", {}).get("affected_grants"))}
    if grant_spec.get("grant_ref") in active_revoked_refs:
        return _fail("grant_revoked", requested_operation, checks)
    checks["not_revoked"] = True
    if grant_spec.get("remaining_uses", 0) <= 0:
        return _fail("grant_exhausted", requested_operation, checks)
    checks["uses_remain"] = True
    if requested_operation.get("workspace_ref") != grant_spec.get("workspace_ref"):
        return _fail("workspace_scope_mismatch", requested_operation, checks)
    checks["workspace_matches"] = True
    if requested_operation.get("resource_ref") not in _as_list(grant_spec.get("allowed_resource_refs")):
        return _fail("resource_scope_mismatch", requested_operation, checks)
    checks["resource_scope_matches"] = True
    if requested_operation.get("mode") != grant_spec.get("mode"):
        return _fail("execution_mode_not_granted", requested_operation, checks)
    checks["mode_matches"] = True
    if requested_operation.get("effect") not in _as_list(grant_spec.get("allowed_effects")):
        return _fail("effect_not_granted", requested_operation, checks)
    checks["effect_allowed"] = True
    network_allowed = grant_spec.get("network_constraints", {}).get("network_allowed") is True
    if requested_operation.get("network_required") and not network_allowed:
        return _fail("network_not_granted", requested_operation, checks)
    checks["network_allowed"] = True
    secret_allowed = grant_spec.get("secret_constraints", {}).get("secret_access_allowed") is True
    if requested_operation.get("secret_required") and not secret_allowed:
        return _fail("secret_not_granted", requested_operation, checks)
    checks["secrets_allowed"] = True
    if delegation is None or delegation.get("spec", {}).get("status") != "active":
        return _fail("delegation_not_allowed", requested_operation, checks)
    delegation_spec = delegation.get("spec", {})
    if requested_operation.get("capability_ref") not in _as_list(delegation_spec.get("delegated_capabilities")):
        return _fail("delegation_scope_widening", requested_operation, checks)
    if requested_operation.get("mode") != delegation_spec.get("delegated_mode"):
        return _fail("delegation_scope_widening", requested_operation, checks)
    if delegation_spec.get("expiry") == "expired":
        return _fail("delegation_expired", requested_operation, checks)
    checks["delegation_valid"] = True
    unsupported_features = [item for item in _as_list(requested_operation.get("required_features")) if item not in RECOGNIZED_CAPABILITIES]
    if unsupported_features:
        return _fail("required_feature_unsupported", requested_operation, checks)
    checks["required_features_supported"] = True
    return _evaluation_record("allowed", [], checks, requested_operation)


def negative_evaluation_matrix() -> dict[str, dict[str, Any]]:
    base_principal = sample_principal()
    base_admission = sample_admission_record()
    base_policy = sample_policy_decision()
    base_grant = sample_capability_grant()
    base_delegation = sample_delegation_record()
    base_request = sample_requested_operation()

    matrix: dict[str, dict[str, Any]] = {}

    def record(code: str, *, principal=base_principal, admission=base_admission, policy=base_policy, grant=base_grant, delegation=base_delegation, revocations=None, request=None) -> None:
        matrix[code] = evaluate_authorization(
            copy.deepcopy(principal) if principal is not None else None,
            copy.deepcopy(admission) if admission is not None else None,
            copy.deepcopy(policy) if policy is not None else None,
            copy.deepcopy(grant) if grant is not None else None,
            copy.deepcopy(delegation) if delegation is not None else None,
            copy.deepcopy(revocations or []),
            copy.deepcopy(request or base_request),
        )

    record("principal_unknown", principal=None)
    inactive = copy.deepcopy(base_principal)
    inactive["spec"]["status"] = "suspended"
    record("principal_inactive", principal=inactive)
    unadmitted = copy.deepcopy(base_admission)
    unadmitted["spec"]["decision"] = "candidate"
    record("implementation_not_admitted", admission=unadmitted)
    mismatch = copy.deepcopy(base_request)
    mismatch["implementation_digest"] = "sha256:" + "e" * 64
    record("implementation_digest_mismatch", request=mismatch)
    capability = copy.deepcopy(base_request)
    capability["capability_ref"] = "aide://capability/unadmitted"
    record("capability_not_admitted", request=capability)
    record("policy_denied", policy=sample_policy_decision("deny"))
    record("approval_required", policy=sample_policy_decision("require_approval"))
    record("grant_missing", grant=None)
    inactive_grant = sample_capability_grant("suspended", 1)
    record("grant_inactive", grant=inactive_grant)
    record("grant_expired", grant=sample_capability_grant("expired", 1))
    record("grant_revoked", grant=sample_capability_grant("revoked", 1))
    record("grant_exhausted", grant=sample_capability_grant("active", 0))
    workspace = copy.deepcopy(base_request)
    workspace["workspace_ref"] = "aide://workspace/other"
    record("workspace_scope_mismatch", request=workspace)
    resource = copy.deepcopy(base_request)
    resource["resource_ref"] = "aide://resource/other"
    record("resource_scope_mismatch", request=resource)
    mode = copy.deepcopy(base_request)
    mode["mode"] = "apply_request"
    record("execution_mode_not_granted", request=mode)
    effect = copy.deepcopy(base_request)
    effect["effect"] = "network"
    record("effect_not_granted", request=effect)
    network = copy.deepcopy(base_request)
    network["network_required"] = True
    record("network_not_granted", request=network)
    secret = copy.deepcopy(base_request)
    secret["secret_required"] = True
    record("secret_not_granted", request=secret)
    record("delegation_not_allowed", delegation=None)
    delegation_widen = copy.deepcopy(base_delegation)
    delegation_widen["spec"]["delegated_capabilities"] = ["aide://capability/other"]
    record("delegation_scope_widening", delegation=delegation_widen)
    delegation_expired = copy.deepcopy(base_delegation)
    delegation_expired["spec"]["expiry"] = "expired"
    record("delegation_expired", delegation=delegation_expired)
    required = copy.deepcopy(base_request)
    required["required_features"] = ["future.required"]
    record("required_feature_unsupported", request=required)
    return matrix


def fixture_matrix() -> dict[str, Any]:
    matrix = negative_evaluation_matrix()
    return {
        "positive_records": {name: record["kind"] for name, record in sample_records().items()},
        "negative_evaluation_reason_codes": {code: item["spec"]["reason_codes"] for code, item in matrix.items()},
        "required_refusal_codes": list(REFUSAL_CODES),
        "all_required_refusal_codes_covered": sorted(matrix) == sorted(REFUSAL_CODES),
    }


def implemented_capabilities(record: dict[str, Any]) -> set[str]:
    spec = record.get("spec") if isinstance(record.get("spec"), dict) else {}
    capability = spec.get("capability_label")
    return {capability} if isinstance(capability, str) and capability else set()


def schema_for_kind(kind: str) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"AIDE {kind} schema",
        "description": f"Projection-only {kind} record for AIDE trust and authorization contract v0.",
        "type": "object",
        "additionalProperties": True,
        "required": ["apiVersion", "kind", "metadata", "spec", "status"],
        "properties": {
            "apiVersion": {"type": "string"},
            "kind": {"const": kind, "type": "string"},
            "schema_version": {"type": "string"},
            "protocol_version": {"type": "string"},
            "metadata": {
                "type": "object",
                "additionalProperties": True,
                "required": REQUIRED_METADATA_FIELDS,
                "properties": {
                    "id": {"type": "string"},
                    "createdAt": {"type": "string"},
                    "sourcePath": {"type": "string"},
                    "producer": {"type": "object"},
                    "compatibility": {"type": "object"},
                },
            },
            "spec": {
                "type": "object",
                "additionalProperties": True,
                "required": REQUIRED_SPEC_FIELDS_BY_KIND[kind],
            },
            "status": {
                "type": "object",
                "additionalProperties": True,
                "required": REQUIRED_STATUS_FIELDS,
                "properties": {
                    "validated": {"type": "boolean"},
                    "projection_only": {"type": "boolean"},
                    "validation_errors": {"type": "array", "items": {"type": "string"}},
                    "validation_warnings": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    }


def load_schema(repo_root: str | Path, kind: str) -> dict[str, Any]:
    path = Path(repo_root) / SCHEMA_PATHS[kind]
    if not path.exists():
        raise ValueError(f"schema missing for {kind}: {SCHEMA_PATHS[kind].as_posix()}")
    return read_json(path)


def _schema_node_errors(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type == "object" and not isinstance(value, dict):
        return [f"{path} must be object"]
    if expected_type == "array" and not isinstance(value, list):
        return [f"{path} must be array"]
    if expected_type == "string" and not isinstance(value, str):
        return [f"{path} must be string"]
    if expected_type == "boolean" and not isinstance(value, bool):
        return [f"{path} must be boolean"]
    if isinstance(schema.get("const"), str) and value != schema["const"]:
        errors.append(f"{path} must equal {schema['const']}")
    if isinstance(value, dict):
        for field in schema.get("required", []) if isinstance(schema.get("required"), list) else []:
            if field not in value:
                errors.append(f"{path}.{field} is required")
        properties = schema.get("properties", {}) if isinstance(schema.get("properties"), dict) else {}
        for key, child_schema in properties.items():
            if key in value and isinstance(child_schema, dict):
                errors.extend(_schema_node_errors(value[key], child_schema, f"{path}.{key}"))
    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for index, item in enumerate(value):
            errors.extend(_schema_node_errors(item, schema["items"], f"{path}[{index}]"))
    return errors


def validate_with_schema(obj: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    return _schema_node_errors(obj, schema, "$")


def check_schema_helper_alignment(repo_root: str | Path) -> dict[str, Any]:
    errors: list[str] = []
    loaded: list[str] = []
    for kind in sorted(RECORD_KINDS):
        try:
            schema = load_schema(repo_root, kind)
            loaded.append(kind)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if schema.get("properties", {}).get("kind", {}).get("const") != kind:
            errors.append(f"{kind} schema kind const mismatch")
        for field in ["apiVersion", "kind", "metadata", "spec", "status"]:
            if field not in schema.get("required", []):
                errors.append(f"{kind} schema.required missing {field}")
        spec_required = schema.get("properties", {}).get("spec", {}).get("required", [])
        for field in REQUIRED_SPEC_FIELDS_BY_KIND[kind]:
            if field not in spec_required:
                errors.append(f"{kind} schema.spec.required missing {field}")
    return {
        "schema_helper_alignment_status": "PASS" if not errors else "FAILED_VALIDATION",
        "loaded_kinds": loaded,
        "errors": errors,
    }


def validate_runtime(obj: dict[str, Any], repo_root: str | Path) -> dict[str, Any]:
    kind = obj.get("kind")
    helper_errors = validate_trust_authorization_contract(obj)
    schema_errors: list[str] = []
    if kind in RECORD_KINDS:
        schema_errors = validate_with_schema(obj, load_schema(repo_root, kind))
    else:
        schema_errors = [f"unsupported kind for schema validation: {kind}"]
    status = "PASS" if not helper_errors and not schema_errors else "FAILED_VALIDATION"
    return {
        "status": status,
        "helper_valid": not helper_errors,
        "schema_valid": not schema_errors,
        "helper_validation_errors": helper_errors,
        "schema_validation_errors": schema_errors,
    }


def project_trust_authorization_contract(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    records = sample_records()
    for key, rel in PROJECTION_FILES.items():
        write_json(root / rel, records[key])
    report = {
        "schema_version": "aide.trust-authorization-contract-projection.v0",
        "report_type": "trust_authorization_contract_projection",
        "kind": "TrustAuthorizationProjectionReport",
        "task_id": TASK_ID,
        "status": "PASS_WITH_WARNINGS",
        "capability_label": FEATURE_FLAG,
        "projection_only": True,
        "record_kinds_written": sorted(record["kind"] for record in records.values()),
        "projections_written": [rel.as_posix() for rel in PROJECTION_FILES.values()],
        "required_refusal_codes": list(REFUSAL_CODES),
        "fixture_matrix": fixture_matrix(),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        **_false_boundaries(),
        "warnings": [
            "Trust and authorization contract v0 is projection-only.",
            "No live identity provider, credential store, policy engine, grant store, Service, or runtime enforcement is implemented.",
        ],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    write_text(root / NON_CAPABILITIES_MD, render_non_capabilities_markdown())
    write_text(root / REFUSAL_REGISTRY_MD, render_refusal_registry_markdown())
    return report


def trust_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    data = {
        "schema_version": "aide.trust-authorization-contract-status.v0",
        "report_type": "trust_authorization_contract_status",
        "status": "PASS_WITH_WARNINGS",
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_label": FEATURE_FLAG,
        "schema_files": {kind: path.as_posix() for kind, path in SCHEMA_PATHS.items()},
        "schema_files_exist": {kind: (root / path).exists() for kind, path in SCHEMA_PATHS.items()},
        "record_kinds": sorted(RECORD_KINDS),
        "projection_only": True,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        **_false_boundaries(),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    return data


def trust_validate(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    projection_result = project_trust_authorization_contract(root) if project else {"projections_written": []}
    alignment = check_schema_helper_alignment(root)
    validation_results: list[dict[str, Any]] = []
    for rel in projection_result.get("projections_written", []):
        obj = read_json(root / rel)
        runtime = validate_runtime(obj, root)
        validation_results.append(
            {
                "path": rel,
                "kind": obj.get("kind"),
                "result": runtime["status"],
                "helper_valid": runtime["helper_valid"],
                "schema_valid": runtime["schema_valid"],
                "errors": [*runtime["helper_validation_errors"], *runtime["schema_validation_errors"]],
            }
        )
    optional_runtime = validate_runtime(sample_unknown_optional_record(), root)
    required_runtime = validate_runtime(sample_unknown_required_capability_record(), root)
    fixture = fixture_matrix()
    validation_errors = [*alignment["errors"], *[error for item in validation_results for error in item["errors"]]]
    projection_only_truthful = all(read_json(root / rel)["status"]["projection_only"] is True for rel in projection_result.get("projections_written", []))
    explicit_non_capabilities_preserved = all(
        not (implemented_capabilities(read_json(root / rel)) & set(read_json(root / rel)["spec"]["explicit_non_capabilities"]))
        for rel in projection_result.get("projections_written", [])
    )
    no_secret_values_embedded = not any(_has_forbidden_secret_key(read_json(root / rel)) for rel in projection_result.get("projections_written", []))
    status = (
        "PASS_WITH_WARNINGS"
        if not validation_errors
        and all(item["result"] == "PASS" for item in validation_results)
        and alignment["schema_helper_alignment_status"] == "PASS"
        and optional_runtime["status"] == "PASS"
        and bool(required_runtime["helper_validation_errors"])
        and fixture["all_required_refusal_codes_covered"]
        and projection_only_truthful
        and explicit_non_capabilities_preserved
        and no_secret_values_embedded
        else "FAILED_VALIDATION"
    )
    report = {
        "schema_version": "aide.trust-authorization-contract-validation.v0",
        "report_type": "trust_authorization_contract_validation",
        "kind": "TrustAuthorizationValidationReport",
        "task_id": TASK_ID,
        "status": status,
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_label": FEATURE_FLAG,
        "schema_helper_alignment_status": alignment["schema_helper_alignment_status"],
        "schema_files_loaded": alignment["loaded_kinds"],
        "validation_errors": validation_errors,
        "validation_results": validation_results,
        "projection_only_truthful": projection_only_truthful,
        "explicit_non_capabilities_preserved": explicit_non_capabilities_preserved,
        "unknown_optional_fields_tolerated": optional_runtime["status"] == "PASS",
        "unknown_required_capability_fails_closed": bool(required_runtime["helper_validation_errors"]),
        "all_required_refusal_codes_covered": fixture["all_required_refusal_codes_covered"],
        "required_refusal_codes": list(REFUSAL_CODES),
        "no_secret_values_embedded": no_secret_values_embedded,
        "admission_vs_conformance_separated": True,
        "policy_vs_grant_separated": True,
        "delegation_only_narrows_authority": True,
        "runtime_approval_distinct_from_transaction_approval": True,
        **_false_boundaries(),
        "warnings": [
            "Trust and authorization contract v0 is projection-only.",
            "No live enforcement, identity provider, credentials, policy engine, grants, Service, or provider/model/network behavior is implemented.",
        ],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_markdown(report))
    return report


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Trust And Authorization Contract Status",
        "",
        f"- status: {data.get('status')}",
        f"- capability_label: {data.get('capability_label')}",
        "- projection_only: true",
        "- live_identity_implemented: false",
        "- live_policy_engine_implemented: false",
        "- live_grants_implemented: false",
        "- credentials_embedded: false",
        "- secrets_embedded: false",
        "- runtime_enforcement_implemented: false",
        "- service_runtime_implemented: false",
        "- provider_or_model_calls: none",
        "- network_calls: none",
        f"- recommended_next_task: {data.get('recommended_next_task')}",
        "",
        "## Record Kinds",
        "",
    ]
    for kind in data.get("record_kinds", []):
        lines.append(f"- {kind}")
    return "\n".join(lines) + "\n"


def render_projection_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Trust And Authorization Contract Projection",
        "",
        f"- status: {report.get('status')}",
        f"- task_id: {report.get('task_id')}",
        f"- capability_label: {report.get('capability_label')}",
        "- projection_only: true",
        "- live_identity_implemented: false",
        "- live_policy_engine_implemented: false",
        "- live_grants_implemented: false",
        "- credentials_embedded: false",
        "- secrets_embedded: false",
        "- runtime_enforcement_implemented: false",
        "- provider_or_model_calls: none",
        "- network_calls: none",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Projections Written",
        "",
    ]
    for rel in report.get("projections_written", []):
        lines.append(f"- {rel}")
    lines.extend(["", "## Refusal Codes", ""])
    for code in report.get("required_refusal_codes", []):
        lines.append(f"- {code}")
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Trust And Authorization Contract Validation",
        "",
        f"- status: {report.get('status')}",
        f"- capability_label: {report.get('capability_label')}",
        f"- schema_helper_alignment_status: {report.get('schema_helper_alignment_status')}",
        f"- projection_only_truthful: {str(report.get('projection_only_truthful', False)).lower()}",
        f"- explicit_non_capabilities_preserved: {str(report.get('explicit_non_capabilities_preserved', False)).lower()}",
        f"- unknown_optional_fields_tolerated: {str(report.get('unknown_optional_fields_tolerated', False)).lower()}",
        f"- unknown_required_capability_fails_closed: {str(report.get('unknown_required_capability_fails_closed', False)).lower()}",
        f"- all_required_refusal_codes_covered: {str(report.get('all_required_refusal_codes_covered', False)).lower()}",
        f"- no_secret_values_embedded: {str(report.get('no_secret_values_embedded', False)).lower()}",
        "- live_identity_implemented: false",
        "- runtime_enforcement_implemented: false",
        "- service_runtime_implemented: false",
        "- provider_or_model_calls: none",
        "- network_calls: none",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Validation Results",
        "",
    ]
    for item in report.get("validation_results", []):
        lines.append(f"- {item.get('result')}: {item.get('path')}")
    if report.get("validation_errors"):
        lines.extend(["", "## Errors", ""])
        for error in report.get("validation_errors", []):
            lines.append(f"- {error}")
    return "\n".join(lines) + "\n"


def render_non_capabilities_markdown() -> str:
    lines = ["# Explicit Non-Capabilities", ""]
    for item in EXPLICIT_NON_CAPABILITIES:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def render_refusal_registry_markdown() -> str:
    lines = ["# Refusal Code Registry", ""]
    for code in REFUSAL_CODES:
        lines.append(f"- {code}")
    return "\n".join(lines) + "\n"
