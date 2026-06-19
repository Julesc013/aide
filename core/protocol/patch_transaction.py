"""Minimal AIDE PatchTransaction helpers.

This module projects one deterministic, synthetic PatchTransaction record. The
record represents a proposed bounded mutation and its requirements, but it does
not generate repository diffs, approve, apply, roll back, trust, or mutate any
target repository.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from core.protocol import envelope, reference_id


API_VERSION = envelope.API_VERSION
PATCH_TRANSACTION_SCHEMA_VERSION = "aide.patch-transaction.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_patch_transaction_schema"
ACCEPTED_PREDECESSOR = "minimal_conformance_result_schema"
TASK_ID = "AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01"
DETERMINISTIC_TIMESTAMP = "2026-06-19T00:00:00+10:00"
BASELINE_COMMIT = "ef89d1840dd26480be777b612e4bd443e5a92392"

TRANSACTION_ID = "synthetic-managed-section-review-candidate-01"
TRANSACTION_REF = reference_id.format_reference_id("patch-transaction", TRANSACTION_ID)
REPOSITORY_REF = reference_id.format_reference_id("source", "aide-self-hosting-repo")
TARGET_REF = reference_id.format_reference_id("queue-task", RECOMMENDED_NEXT_TASK)
WORK_UNIT_REF = reference_id.format_reference_id("queue-task", TASK_ID)
PATCH_ARTIFACT_ID = "synthetic-managed-section-unified-diff-01"
PATCH_ARTIFACT_REF = reference_id.format_reference_id("artifact", PATCH_ARTIFACT_ID)

REPORT_ROOT = Path(".aide/reports/patch-transaction")
SCHEMA_PATH = Path(".aide/protocol/aide-patch-transaction.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
TRANSACTION_INDEX_JSON = REPORT_ROOT / "transaction-index.json"
TRANSACTION_INDEX_MD = REPORT_ROOT / "transaction-index.md"
TRANSACTIONS_JSON = REPORT_ROOT / "transactions.json"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
SCOPE_REPORT_JSON = REPORT_ROOT / "scope-report.json"
SCOPE_REPORT_MD = REPORT_ROOT / "scope-report.md"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"
SAMPLE_PATCH_PATH = REPORT_ROOT / "sample-unified.diff"

REQUIRED_REPORTS = [
    STATUS_MD,
    TRANSACTION_INDEX_JSON,
    TRANSACTION_INDEX_MD,
    TRANSACTIONS_JSON,
    PROJECTION_JSON,
    PROJECTION_MD,
    VALIDATION_JSON,
    VALIDATION_MD,
    SCOPE_REPORT_JSON,
    SCOPE_REPORT_MD,
    EXPLICIT_NON_CAPABILITIES_MD,
    FUTURE_WORK_MD,
    NEXT_TASK_PROMPT_MD,
]

SUPPORTED_KINDS = {
    "PatchTransaction",
    "PatchTransactionIndex",
    "PatchTransactionProjectionReport",
    "PatchTransactionValidationReport",
    "PatchTransactionScopeReport",
}
LIFECYCLE_STATES = {
    "projected",
    "validated",
    "review_candidate",
    "approved",
    "rejected",
    "quarantined",
    "applied",
    "rolled_back",
    "superseded",
}
NO_APPLY_STATUS_FIELDS = {
    "policy_evaluation_performed": False,
    "approval_granted": False,
    "apply_performed": False,
    "target_mutated": False,
    "rollback_performed": False,
    "quarantined": False,
    "trusted": False,
}
RECOGNIZED_REQUIRED_CAPABILITY_REFS = {
    reference_id.format_reference_id("capability", "minimal_reference_id_scheme"),
    reference_id.format_reference_id("capability", "minimal_evidence_packet_schema"),
    reference_id.format_reference_id("capability", "minimal_conformance_result_schema"),
}
RECOGNIZED_REQUIRED_CONFORMANCE_RESULT_REFS = {
    reference_id.format_reference_id("conformance-result", "minimal_capability_manifest-v1.0.0-evidence-projection-01"),
}
ALLOWED_REQUIRED_REF_KINDS = {
    "capability",
    "conformance-result",
    "test-job",
    "evidence",
}
EXPLICIT_NON_CAPABILITIES = [
    "patch_application",
    "active_repository_mutation",
    "target_repository_mutation",
    "general_diff_generation",
    "general_diff_parsing",
    "three_way_merge",
    "conflict_resolution",
    "rollback_execution",
    "approval_engine",
    "policy_engine",
    "conformance_runner",
    "case_execution",
    "automatic_observation_collection",
    "profile_activation",
    "admission",
    "trust_grant",
    "adapter_manifest",
    "context_pack_v2",
    "test_broker_runtime",
    "worker_execution",
    "scheduler",
    "leases",
    "supervisor",
    "runtime",
    "service",
    "commander",
    "workbench",
    "mcp_server",
    "a2a_server",
    "provider_model_calls",
    "gateway_calls",
    "network_calls",
    "github_mutation",
    "branch_worktree_automation",
    "release",
    "promotion",
    "production_readiness",
    "release_readiness",
    "broad_autonomous_runtime",
]
VALIDATION_WARNINGS = [
    "PatchTransaction is schema/projection/validation only; no apply engine exists.",
    "Policy evaluation, approval, admission, trust, artifact resolution, VCS reachability, and runtime behavior remain absent.",
    "Inherited operational-health warning debt is retained: report volume, report ambiguity, generated-output provenance, one stale-context OKF finding, four Reconciler warnings, and queue readability debt.",
]
SCHEMA_VALIDATION_MODE = "minimal_json_schema_subset_plus_patch_transaction_semantics"
SCHEMA_VALIDATION_LIMITATIONS = [
    "Local subset validator checks required envelope, reference, digest, lifecycle, scope, and no-apply fields.",
    "Full JSON Schema Draft 2020-12 validation remains future work.",
    "Patch parsing, artifact resolution, VCS target reachability, policy evaluation, approval, apply, rollback, admission, and trust are not implemented.",
]
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def stable_json(data: Any) -> str:
    return envelope.stable_json(data)


def read_json(path: Path) -> dict[str, Any]:
    return envelope.read_json(path)


def write_json(path: Path, obj: dict[str, Any]) -> None:
    envelope.write_json(path, obj)


def write_text(path: Path, text: str) -> None:
    envelope.write_text(path, text)


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def sample_unified_diff_text() -> str:
    return (
        "diff --git a/fixtures/patch-transaction/synthetic-example.txt b/fixtures/patch-transaction/synthetic-example.txt\n"
        "new file mode 100644\n"
        "index 0000000..1111111\n"
        "--- /dev/null\n"
        "+++ b/fixtures/patch-transaction/synthetic-example.txt\n"
        "@@ -0,0 +1,2 @@\n"
        "+AIDE PatchTransaction synthetic sample.\n"
        "+No apply, approval, trust, branch mutation, or target mutation occurred.\n"
    )


def patch_artifact_digest(payload: bytes | str) -> str:
    if isinstance(payload, str):
        payload = payload.encode("utf-8")
    return sha256_bytes(payload)


def _compatibility(required_capabilities: list[str] | None = None) -> dict[str, Any]:
    required = [FEATURE_FLAG, ACCEPTED_PREDECESSOR]
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


def load_patch_transaction_schema(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(repo_root) if repo_root is not None else Path(".")
    return read_json(root / SCHEMA_PATH)


def _json_valid(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (OSError, ValueError):
        return False


def _is_absolute_repo_path(value: str) -> bool:
    return PurePosixPath(value).is_absolute() or PureWindowsPath(value).is_absolute() or bool(re.match(r"^[A-Za-z]:[\\/]", value))


def _has_windows_drive_prefix(value: str) -> bool:
    return bool(re.match(r"^[A-Za-z]:", value))


def normalize_repo_path(path_value: Any) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    if not isinstance(path_value, str):
        return None, ["path must be a string"]
    raw = path_value.strip().replace("\\", "/")
    if not raw:
        return None, ["path must not be empty"]
    if _has_windows_drive_prefix(raw):
        errors.append(f"path must not use a Windows drive prefix: {path_value}")
    if _is_absolute_repo_path(raw):
        errors.append(f"path must be repo-relative: {path_value}")
    if "\x00" in raw or any(ord(char) < 32 for char in raw):
        errors.append(f"path contains control characters: {path_value}")
    normalized = PurePosixPath(raw).as_posix()
    if normalized in {"", "."}:
        errors.append(f"path normalizes to empty: {path_value}")
    parts = PurePosixPath(normalized).parts
    if ".." in parts:
        errors.append(f"path traversal is forbidden: {path_value}")
    if any(part in {"", "."} for part in parts):
        errors.append(f"path contains empty or current-directory segments: {path_value}")
    if errors:
        return None, errors
    return normalized, []


def normalize_scope_path(path_value: Any) -> tuple[str | None, list[str]]:
    if isinstance(path_value, str) and path_value.strip().replace("\\", "/").endswith("/**"):
        base, errors = normalize_repo_path(path_value.strip().replace("\\", "/")[:-3])
        return (f"{base}/**" if base else None), errors
    return normalize_repo_path(path_value)


def _scope_contains(scope: str, path_or_scope: str) -> bool:
    scope_base = scope[:-3] if scope.endswith("/**") else scope
    other = path_or_scope[:-3] if path_or_scope.endswith("/**") else path_or_scope
    if scope.endswith("/**"):
        return other == scope_base or other.startswith(f"{scope_base}/")
    return other == scope_base


def _scopes_overlap(left: str, right: str) -> bool:
    return _scope_contains(left, right) or _scope_contains(right, left)


def _append_unique_normalized(
    target: list[str],
    seen_originals: dict[str, str],
    value: str,
    original_value: Any,
    field_name: str,
    errors: list[str],
) -> None:
    if value in target:
        errors.append(
            f"{field_name}: duplicate normalized path: {value} "
            f"from {seen_originals[value]!r} and {str(original_value)!r}"
        )
    else:
        target.append(value)
        seen_originals[value] = str(original_value)


def validate_scope(
    allowed_paths: list[Any],
    forbidden_paths: list[Any],
    declared_changed_paths: list[Any],
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    normalized_allowed: list[str] = []
    normalized_forbidden: list[str] = []
    normalized_declared: list[str] = []
    allowed_originals: dict[str, str] = {}
    forbidden_originals: dict[str, str] = {}
    declared_originals: dict[str, str] = {}

    for value in allowed_paths:
        normalized, path_errors = normalize_scope_path(value)
        errors.extend(f"allowed_paths: {item}" for item in path_errors)
        if normalized is not None:
            _append_unique_normalized(normalized_allowed, allowed_originals, normalized, value, "allowed_paths", errors)
    for value in forbidden_paths:
        normalized, path_errors = normalize_scope_path(value)
        errors.extend(f"forbidden_paths: {item}" for item in path_errors)
        if normalized is not None:
            _append_unique_normalized(normalized_forbidden, forbidden_originals, normalized, value, "forbidden_paths", errors)
    for value in declared_changed_paths:
        normalized, path_errors = normalize_repo_path(value)
        errors.extend(f"declared_changed_paths: {item}" for item in path_errors)
        if normalized is not None:
            _append_unique_normalized(normalized_declared, declared_originals, normalized, value, "declared_changed_paths", errors)

    if not normalized_allowed:
        errors.append("allowed_paths must contain at least one valid scope")
    if not normalized_declared:
        errors.append("declared_changed_paths must contain at least one valid path")

    for allowed in normalized_allowed:
        for forbidden in normalized_forbidden:
            if _scopes_overlap(allowed, forbidden):
                errors.append(f"allowed and forbidden scopes overlap: {allowed} :: {forbidden}")

    for declared in normalized_declared:
        if not any(_scope_contains(scope, declared) for scope in normalized_allowed):
            errors.append(f"declared path is outside allowed scope: {declared}")
        for forbidden in normalized_forbidden:
            if _scope_contains(forbidden, declared):
                errors.append(f"declared path matches forbidden scope: {declared} :: {forbidden}")

    return {
        "schema_version": "aide.patch-transaction-scope-report.v0",
        "report_type": "patch_transaction_scope",
        "kind": "PatchTransactionScopeReport",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "status": "PASS" if not errors else "FAILED_VALIDATION",
        "scope_valid": not errors,
        "allowed_paths": normalized_allowed,
        "forbidden_paths": normalized_forbidden,
        "declared_changed_paths": normalized_declared,
        "errors": errors,
        "warnings": warnings,
    }


def build_patch_transaction(repo_root: str | Path) -> dict[str, Any]:
    _root = Path(repo_root)
    declared_paths = ["fixtures/patch-transaction/synthetic-example.txt"]
    allowed_paths = ["fixtures/patch-transaction/**"]
    forbidden_paths = [
        ".git/**",
        ".aide.local/**",
        ".env",
        "secrets/**",
    ]
    patch_digest = patch_artifact_digest(sample_unified_diff_text())
    base_digest = sha256_text(BASELINE_COMMIT)
    metadata = {
        "id": TRANSACTION_ID,
        "name": "Synthetic Managed Section PatchTransaction",
        "title": "Synthetic Managed Section PatchTransaction",
        "createdAt": DETERMINISTIC_TIMESTAMP,
        "sourcePath": TRANSACTIONS_JSON.as_posix(),
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility(["minimal_reference_id_scheme", "minimal_evidence_packet_schema"]),
    }
    spec = {
        "provenance": {
            "transaction_ref": TRANSACTION_REF,
            "schema_version": PATCH_TRANSACTION_SCHEMA_VERSION,
            "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
            "created_at": DETERMINISTIC_TIMESTAMP,
            "work_unit_ref": WORK_UNIT_REF,
            "worker_run_ref": None,
            "source_event_refs": [],
        },
        "base": {
            "repository_ref": REPOSITORY_REF,
            "base_revision_ref": f"git:{BASELINE_COMMIT}",
            "target_ref": TARGET_REF,
            "base_digest": base_digest,
            "base_digest_algorithm": "sha256-static-ref-v1",
            "target_reachability_checked": False,
        },
        "patch_artifact": {
            "format": "unified_diff",
            "artifact_ref": PATCH_ARTIFACT_REF,
            "locator": SAMPLE_PATCH_PATH.as_posix(),
            "sha256": patch_digest,
            "media_type": "text/x-diff",
            "declared_changed_paths": declared_paths,
        },
        "scope": {
            "allowed_paths": allowed_paths,
            "forbidden_paths": forbidden_paths,
            "declared_changed_paths": declared_paths,
        },
        "requirements": {
            "required_capability_refs": [
                reference_id.format_reference_id("capability", "minimal_reference_id_scheme"),
                reference_id.format_reference_id("capability", "minimal_evidence_packet_schema"),
                reference_id.format_reference_id("capability", "minimal_conformance_result_schema"),
            ],
            "required_conformance_result_refs": [
                reference_id.format_reference_id("conformance-result", "minimal_capability_manifest-v1.0.0-evidence-projection-01"),
            ],
            "required_test_job_refs": [
                reference_id.format_reference_id("test-job", "patch-transaction-build-focused-unit-tests"),
            ],
            "required_evidence_refs": [
                reference_id.format_reference_id("evidence", "AIDE-OPERATIONAL-HEALTH-PAUSE-01-readiness"),
                reference_id.format_reference_id("evidence", "AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01-validation"),
            ],
            "approval_required": True,
        },
        "lifecycle": "validated",
        "rollback_compatible_record_refs": [],
        "status_event_refs": [],
        "limitations": [
            "Synthetic protocol example only; it is not a repository apply record.",
            "Target reachability, policy evaluation, approval, apply, rollback, admission, and trust were not performed.",
            "The lifecycle fixture runner remains temp-workspace evidence only and is not generalized by this record.",
        ],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
    }
    return {
        "apiVersion": API_VERSION,
        "kind": "PatchTransaction",
        "schema_version": PATCH_TRANSACTION_SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "metadata": metadata,
        "spec": spec,
        "status": {
            "validation_performed": True,
            "scope_validation_performed": True,
            "policy_evaluation_performed": False,
            "approval_granted": False,
            "apply_performed": False,
            "target_mutated": False,
            "rollback_performed": False,
            "quarantined": False,
            "trusted": False,
            "validation_status": "PASS_WITH_WARNINGS",
            "validation_errors": [],
            "validation_warnings": list(VALIDATION_WARNINGS),
        },
    }


def _validate_required_ref(ref: Any, *, expected_kind: str | None = None) -> list[str]:
    if not isinstance(ref, str) or not ref:
        return ["required reference must be a non-empty string"]
    validation = reference_id.validate_reference_id(ref, required=True)
    errors = list(validation.errors)
    parsed = validation.parsed
    if parsed is not None:
        if expected_kind is not None and parsed.kind != expected_kind:
            errors.append(f"reference kind must be {expected_kind}: {ref}")
        elif expected_kind is None and parsed.kind not in ALLOWED_REQUIRED_REF_KINDS:
            errors.append(f"unsupported required reference kind: {parsed.kind}")
    return errors


def validate_patch_transaction_record(record: dict[str, Any], schema: dict[str, Any] | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if schema is not None:
        errors.extend(envelope.validate_envelope_with_schema(record, schema))
    else:
        if not isinstance(record, dict):
            return ["record must be an object"], warnings
        for field in ["apiVersion", "kind", "metadata", "spec", "status"]:
            if field not in record:
                errors.append(f"missing required field: {field}")
        if not isinstance(record.get("metadata"), dict):
            errors.append("metadata must be an object")
        if not isinstance(record.get("spec"), dict):
            errors.append("spec must be an object")
        if not isinstance(record.get("status"), dict):
            errors.append("status must be an object")
    if record.get("kind") != "PatchTransaction":
        errors.append("kind must be PatchTransaction")
    if record.get("schema_version") != PATCH_TRANSACTION_SCHEMA_VERSION:
        errors.append(f"schema_version must be {PATCH_TRANSACTION_SCHEMA_VERSION}")
    if record.get("protocol_version") != PROTOCOL_VERSION:
        errors.append(f"protocol_version must be {PROTOCOL_VERSION}")

    spec = record.get("spec") if isinstance(record.get("spec"), dict) else {}
    status = record.get("status") if isinstance(record.get("status"), dict) else {}
    provenance = spec.get("provenance") if isinstance(spec.get("provenance"), dict) else {}
    base = spec.get("base") if isinstance(spec.get("base"), dict) else {}
    artifact = spec.get("patch_artifact") if isinstance(spec.get("patch_artifact"), dict) else {}
    scope = spec.get("scope") if isinstance(spec.get("scope"), dict) else {}
    requirements = spec.get("requirements") if isinstance(spec.get("requirements"), dict) else {}

    if provenance.get("transaction_ref") != TRANSACTION_REF:
        errors.append(f"transaction_ref must be {TRANSACTION_REF}")
    errors.extend(_validate_required_ref(provenance.get("transaction_ref"), expected_kind="patch-transaction"))
    if provenance.get("schema_version") != PATCH_TRANSACTION_SCHEMA_VERSION:
        errors.append(f"provenance.schema_version must be {PATCH_TRANSACTION_SCHEMA_VERSION}")
    if provenance.get("created_at") != DETERMINISTIC_TIMESTAMP:
        errors.append("provenance.created_at must be deterministic")
    producer = provenance.get("producer")
    if not isinstance(producer, dict) or producer.get("name") != PRODUCER_NAME or producer.get("version") != PRODUCER_VERSION:
        errors.append("provenance.producer must match aide-lite producer metadata")
    errors.extend(_validate_required_ref(provenance.get("work_unit_ref"), expected_kind="queue-task"))
    worker_ref = provenance.get("worker_run_ref")
    if worker_ref is not None:
        errors.extend(_validate_required_ref(worker_ref, expected_kind="worker-run"))
    source_event_refs = provenance.get("source_event_refs")
    if not isinstance(source_event_refs, list):
        errors.append("source_event_refs must be an array")
    else:
        for ref in source_event_refs:
            errors.extend(_validate_required_ref(ref, expected_kind="event"))

    errors.extend(_validate_required_ref(base.get("repository_ref"), expected_kind="source"))
    if base.get("base_revision_ref") != f"git:{BASELINE_COMMIT}":
        errors.append(f"base_revision_ref must bind to git:{BASELINE_COMMIT}")
    if not isinstance(base.get("base_digest"), str) or not SHA256_RE.fullmatch(base.get("base_digest", "")):
        errors.append("base_digest must be sha256:<64 lowercase hex>")
    elif base.get("base_digest") != sha256_text(BASELINE_COMMIT):
        errors.append("base_digest does not match baseline commit binding")
    if base.get("base_digest_algorithm") != "sha256-static-ref-v1":
        errors.append("base_digest_algorithm must be sha256-static-ref-v1")
    errors.extend(_validate_required_ref(base.get("target_ref"), expected_kind="queue-task"))
    if base.get("target_reachability_checked") is not False:
        errors.append("target_reachability_checked must be false")

    if artifact.get("format") != "unified_diff":
        errors.append("patch_artifact.format must be unified_diff")
    errors.extend(_validate_required_ref(artifact.get("artifact_ref"), expected_kind="artifact"))
    if not isinstance(artifact.get("sha256"), str) or not SHA256_RE.fullmatch(artifact.get("sha256", "")):
        errors.append("patch_artifact.sha256 must be sha256:<64 lowercase hex>")
    elif artifact.get("sha256") != patch_artifact_digest(sample_unified_diff_text()):
        errors.append("patch_artifact.sha256 does not match deterministic sample patch bytes")
    if artifact.get("media_type") != "text/x-diff":
        errors.append("patch_artifact.media_type must be text/x-diff")
    if artifact.get("declared_changed_paths") != scope.get("declared_changed_paths"):
        errors.append("patch_artifact.declared_changed_paths must match scope.declared_changed_paths")

    scope_report = validate_scope(
        scope.get("allowed_paths") if isinstance(scope.get("allowed_paths"), list) else [],
        scope.get("forbidden_paths") if isinstance(scope.get("forbidden_paths"), list) else [],
        scope.get("declared_changed_paths") if isinstance(scope.get("declared_changed_paths"), list) else [],
    )
    errors.extend(scope_report["errors"])

    required_capabilities = requirements.get("required_capability_refs")
    if not isinstance(required_capabilities, list):
        errors.append("required_capability_refs must be an array")
        required_capabilities = []
    for ref in required_capabilities:
        errors.extend(_validate_required_ref(ref, expected_kind="capability"))
        if isinstance(ref, str) and ref not in RECOGNIZED_REQUIRED_CAPABILITY_REFS:
            errors.append(f"unknown required capability ref: {ref}")

    required_results = requirements.get("required_conformance_result_refs")
    if not isinstance(required_results, list):
        errors.append("required_conformance_result_refs must be an array")
        required_results = []
    for ref in required_results:
        errors.extend(_validate_required_ref(ref, expected_kind="conformance-result"))
        if isinstance(ref, str) and ref not in RECOGNIZED_REQUIRED_CONFORMANCE_RESULT_REFS:
            errors.append(f"unknown required ConformanceResult ref: {ref}")

    for field, expected_kind in [
        ("required_test_job_refs", "test-job"),
        ("required_evidence_refs", "evidence"),
    ]:
        value = requirements.get(field)
        if not isinstance(value, list):
            errors.append(f"{field} must be an array")
            value = []
        for ref in value:
            errors.extend(_validate_required_ref(ref, expected_kind=expected_kind))
    if requirements.get("approval_required") is not True:
        errors.append("approval_required must be true for future apply")

    lifecycle = spec.get("lifecycle")
    if lifecycle not in LIFECYCLE_STATES:
        errors.append("lifecycle is invalid")
    if lifecycle in {"approved", "applied", "rolled_back"}:
        errors.append(f"projection lifecycle must not be {lifecycle}")
    if lifecycle == "applied" and status.get("apply_performed") is not True:
        errors.append("applied lifecycle requires apply_performed true")
    if lifecycle == "rolled_back" and status.get("rollback_performed") is not True:
        errors.append("rolled_back lifecycle requires rollback_performed true")

    rollback_refs = spec.get("rollback_compatible_record_refs")
    if not isinstance(rollback_refs, list):
        errors.append("rollback_compatible_record_refs must be an array")
        rollback_refs = []
    for ref in rollback_refs:
        errors.extend(_validate_required_ref(ref, expected_kind="artifact"))
    event_refs = spec.get("status_event_refs")
    if not isinstance(event_refs, list):
        errors.append("status_event_refs must be an array")
        event_refs = []
    for ref in event_refs:
        errors.extend(_validate_required_ref(ref, expected_kind="event"))

    if spec.get("explicit_non_capabilities") != EXPLICIT_NON_CAPABILITIES:
        errors.append("explicit_non_capabilities must match declared PatchTransaction boundary list")
    for key, expected in NO_APPLY_STATUS_FIELDS.items():
        if status.get(key) is not expected:
            errors.append(f"status.{key} must be {str(expected).lower()}")
    if status.get("validation_performed") is not True:
        errors.append("status.validation_performed must be true")
    if status.get("scope_validation_performed") is not True:
        errors.append("status.scope_validation_performed must be true")
    if status.get("validation_status") not in {"PASS", "PASS_WITH_WARNINGS"}:
        errors.append("status.validation_status must be PASS or PASS_WITH_WARNINGS for the projected record")
    if status.get("approval_granted") is True:
        errors.append("approval_granted true requires accepted approval authority, which this slice does not implement")
    if status.get("trusted") is True:
        errors.append("trusted true is forbidden; ConformanceResult references do not grant trust")

    if not errors:
        warnings.extend(status.get("validation_warnings", []))
        if required_results:
            warnings.append("ConformanceResult refs are evidence links only and do not grant admission or trust.")
    return errors, warnings


def validate_patch_transaction_with_schema(record: dict[str, Any], schema: dict[str, Any]) -> tuple[list[str], list[str]]:
    return validate_patch_transaction_record(record, schema)


def source_artifact_paths(repo_root: str | Path | None = None) -> list[str]:
    paths = [
        ".aide/protocol/aide-patch-transaction.schema.json",
        ".aide/scripts/aide_lite.py",
        "core/protocol/__init__.py",
        "core/protocol/envelope.py",
        "core/protocol/reference_id.py",
        "core/protocol/patch_transaction.py",
        ".aide/queue/AIDE-OPERATIONAL-HEALTH-PAUSE-01/status.yaml",
        ".aide/reports/operational-health-pause/health-report.json",
        ".aide/reports/conformance-result/results.json",
        ".aide/reports/conformance-result-accept/acceptance-report.json",
    ]
    root = Path(repo_root) if repo_root is not None else Path(".")
    return [path for path in paths if (root / path).exists()]


def _hash_source_artifacts(repo_root: Path, paths: list[str]) -> dict[str, str]:
    return {path: sha256_file(repo_root / path) for path in paths if (repo_root / path).exists()}


def build_transactions_payload(transaction: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.patch-transaction-records.v0",
        "report_type": "patch_transaction_records",
        "kind": "PatchTransactionRecords",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "record_count": 1,
        "transactions": [transaction],
    }


def build_transaction_index(transaction: dict[str, Any], scope_report: dict[str, Any]) -> dict[str, Any]:
    errors, _warnings = validate_patch_transaction_record(transaction)
    status = transaction["status"]
    lifecycle = transaction["spec"]["lifecycle"]
    return {
        "schema_version": "aide.patch-transaction-index.v0",
        "report_type": "patch_transaction_index",
        "kind": "PatchTransactionIndex",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "status": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "record_count": 1,
        "lifecycle_state_counts": {lifecycle: 1},
        "transactions": [
            {
                "transaction_ref": transaction["spec"]["provenance"]["transaction_ref"],
                "lifecycle": lifecycle,
                "record_valid": not errors,
                "scope_valid": scope_report["scope_valid"],
                "approval_required": transaction["spec"]["requirements"]["approval_required"],
                "approval_granted": status["approval_granted"],
                "apply_performed": status["apply_performed"],
                "target_mutated": status["target_mutated"],
                "trusted": status["trusted"],
            }
        ],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def build_status_data(repo_root: str | Path, transaction: dict[str, Any] | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    active_transaction = transaction or build_patch_transaction(root)
    schema_exists = (root / SCHEMA_PATH).exists()
    schema_loaded = False
    errors: list[str] = []
    warnings: list[str] = []
    if schema_exists:
        try:
            schema = load_patch_transaction_schema(root)
            schema_loaded = True
            errors, warnings = validate_patch_transaction_with_schema(active_transaction, schema)
        except ValueError as exc:
            errors.append(str(exc))
    else:
        errors.append(f"schema missing: {SCHEMA_PATH.as_posix()}")
    scope_report = validate_scope(
        active_transaction["spec"]["scope"]["allowed_paths"],
        active_transaction["spec"]["scope"]["forbidden_paths"],
        active_transaction["spec"]["scope"]["declared_changed_paths"],
    )
    lifecycle = active_transaction["spec"]["lifecycle"]
    status = active_transaction["status"]
    return {
        "schema_version": "aide.patch-transaction-status.v0",
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "status": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "schema_path": SCHEMA_PATH.as_posix(),
        "schema_exists": schema_exists,
        "schema_loaded": schema_loaded,
        "record_count": 1,
        "lifecycle_state_counts": {lifecycle: 1},
        "record_valid": not errors,
        "scope_valid": scope_report["scope_valid"],
        "record_errors": errors,
        "record_warnings": warnings,
        "apply_performed": status["apply_performed"],
        "target_mutated": status["target_mutated"],
        "approval_granted": status["approval_granted"],
        "trusted": status["trusted"],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def build_projection_report(
    repo_root: Path,
    transaction: dict[str, Any],
    source_artifacts_before: dict[str, str],
    source_artifacts_after: dict[str, str],
) -> dict[str, Any]:
    errors, warnings = validate_patch_transaction_record(transaction)
    return {
        "schema_version": "aide.patch-transaction-projection.v0",
        "report_type": "patch_transaction_projection",
        "kind": "PatchTransactionProjectionReport",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "status": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "transaction_ref": transaction["spec"]["provenance"]["transaction_ref"],
        "record_valid": not errors,
        "record_errors": errors,
        "record_warnings": warnings,
        "schema_path": SCHEMA_PATH.as_posix(),
        "patch_artifact_path": SAMPLE_PATCH_PATH.as_posix(),
        "patch_artifact_sha256": transaction["spec"]["patch_artifact"]["sha256"],
        "source_artifacts_checked": sorted(source_artifacts_before),
        "source_artifacts_mutated": source_artifacts_before != source_artifacts_after,
        "reports_written": [path.as_posix() for path in REQUIRED_REPORTS] + [SAMPLE_PATCH_PATH.as_posix()],
        "policy_evaluation_performed": False,
        "approval_granted": False,
        "apply_performed": False,
        "target_mutated": False,
        "rollback_performed": False,
        "trusted": False,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def build_validation_report(
    repo_root: Path,
    transaction: dict[str, Any],
    source_artifacts_before: dict[str, str],
    source_artifacts_after: dict[str, str],
    deterministic_projection: bool,
) -> dict[str, Any]:
    schema_loaded = False
    schema_parsed = False
    schema_errors: list[str] = []
    helper_errors: list[str] = []
    warnings: list[str] = []
    try:
        schema = load_patch_transaction_schema(repo_root)
        schema_loaded = True
        schema_parsed = True
        schema_errors, schema_warnings = validate_patch_transaction_with_schema(transaction, schema)
        warnings.extend(schema_warnings)
    except ValueError as exc:
        schema_errors.append(str(exc))
    helper_errors, helper_warnings = validate_patch_transaction_record(transaction)
    warnings.extend(helper_warnings)
    all_errors = [*schema_errors, *helper_errors]
    all_errors = list(dict.fromkeys(all_errors))
    warnings = list(dict.fromkeys(warnings))
    scope_report = validate_scope(
        transaction["spec"]["scope"]["allowed_paths"],
        transaction["spec"]["scope"]["forbidden_paths"],
        transaction["spec"]["scope"]["declared_changed_paths"],
    )
    if not deterministic_projection:
        all_errors.append("projection is not deterministic")
    if source_artifacts_before != source_artifacts_after:
        all_errors.append("source artifacts mutated during projection")
    current_report_outputs = {VALIDATION_JSON, VALIDATION_MD}
    required_existing_reports = [path for path in REQUIRED_REPORTS if path not in current_report_outputs]
    if not all((repo_root / path).exists() for path in required_existing_reports):
        all_errors.append("one or more required PatchTransaction reports are missing")
    return {
        "schema_version": "aide.patch-transaction-validation.v0",
        "report_type": "patch_transaction_validation",
        "kind": "PatchTransactionValidationReport",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "validation_status": "PASS_WITH_WARNINGS" if not all_errors else "FAILED_VALIDATION",
        "schema_loaded": schema_loaded,
        "schema_parsed": schema_parsed,
        "schema_validation_mode": SCHEMA_VALIDATION_MODE,
        "schema_validation_limitations": list(SCHEMA_VALIDATION_LIMITATIONS),
        "schema_helper_alignment_checked": True,
        "schema_helper_alignment_status": "PASS" if schema_loaded and not schema_errors else "FAILED_VALIDATION",
        "record_valid": not all_errors,
        "scope_valid": scope_report["scope_valid"],
        "reference_id_syntax_valid": not any("reference" in item.lower() or "ref" in item.lower() for item in all_errors),
        "transaction_identity_stable": transaction["spec"]["provenance"]["transaction_ref"] == TRANSACTION_REF,
        "digest_shape_valid": SHA256_RE.fullmatch(transaction["spec"]["patch_artifact"]["sha256"]) is not None,
        "digest_binding_valid": transaction["spec"]["patch_artifact"]["sha256"] == patch_artifact_digest(sample_unified_diff_text()),
        "deterministic_projection": deterministic_projection,
        "source_artifacts_mutated": source_artifacts_before != source_artifacts_after,
        "policy_evaluation_performed": False,
        "approval_granted": False,
        "apply_performed": False,
        "target_mutated": False,
        "rollback_performed": False,
        "trusted": False,
        "explicit_non_capabilities_preserved": transaction["spec"].get("explicit_non_capabilities") == EXPLICIT_NON_CAPABILITIES,
        "unknown_required_capability_fails_closed": True,
        "conformance_result_ref_does_not_trust": transaction["status"]["trusted"] is False,
        "errors": all_errors,
        "warnings": warnings or list(VALIDATION_WARNINGS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def patch_transaction_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    data = build_status_data(root)
    write_text(root / STATUS_MD, render_status_markdown(data))
    return data


def write_patch_transaction_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    sources = source_artifact_paths(root)
    before = _hash_source_artifacts(root, sources)
    transaction = build_patch_transaction(root)
    write_text(root / SAMPLE_PATCH_PATH, sample_unified_diff_text())
    scope_report = validate_scope(
        transaction["spec"]["scope"]["allowed_paths"],
        transaction["spec"]["scope"]["forbidden_paths"],
        transaction["spec"]["scope"]["declared_changed_paths"],
    )
    index = build_transaction_index(transaction, scope_report)
    transactions_payload = build_transactions_payload(transaction)
    write_json(root / TRANSACTIONS_JSON, transactions_payload)
    write_json(root / TRANSACTION_INDEX_JSON, index)
    write_text(root / TRANSACTION_INDEX_MD, render_transaction_index_markdown(index))
    write_json(root / SCOPE_REPORT_JSON, scope_report)
    write_text(root / SCOPE_REPORT_MD, render_scope_report_markdown(scope_report))
    write_text(root / EXPLICIT_NON_CAPABILITIES_MD, render_explicit_non_capabilities_markdown())
    write_text(root / FUTURE_WORK_MD, render_future_work_markdown())
    write_text(root / NEXT_TASK_PROMPT_MD, render_next_task_prompt_markdown())
    after = _hash_source_artifacts(root, sources)
    projection = build_projection_report(root, transaction, before, after)
    write_json(root / PROJECTION_JSON, projection)
    write_text(root / PROJECTION_MD, render_projection_markdown(projection))
    status_data = build_status_data(root, transaction)
    write_text(root / STATUS_MD, render_status_markdown(status_data))
    validation = build_validation_report(root, transaction, before, after, deterministic_projection=True)
    write_json(root / VALIDATION_JSON, validation)
    write_text(root / VALIDATION_MD, render_validation_markdown(validation))
    return projection


def patch_transaction_validate(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    sources = source_artifact_paths(root)
    before = _hash_source_artifacts(root, sources)
    write_patch_transaction_reports(root)
    first = (root / TRANSACTIONS_JSON).read_bytes()
    write_patch_transaction_reports(root)
    second = (root / TRANSACTIONS_JSON).read_bytes()
    after = _hash_source_artifacts(root, sources)
    transaction = build_patch_transaction(root)
    validation = build_validation_report(root, transaction, before, after, first == second)
    write_json(root / VALIDATION_JSON, validation)
    write_text(root / VALIDATION_MD, render_validation_markdown(validation))
    return validation


def _bool_text(value: Any) -> str:
    return "true" if value is True else "false"


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# PatchTransaction Status",
        "",
        f"- task_id: `{data['task_id']}`",
        f"- result: `{data['status']}`",
        f"- schema_loaded: `{_bool_text(data['schema_loaded'])}`",
        f"- record_count: `{data['record_count']}`",
        f"- lifecycle_state_counts: `{json.dumps(data['lifecycle_state_counts'], sort_keys=True)}`",
        f"- record_valid: `{_bool_text(data['record_valid'])}`",
        f"- scope_valid: `{_bool_text(data['scope_valid'])}`",
        f"- apply_performed: `{_bool_text(data['apply_performed'])}`",
        f"- target_mutated: `{_bool_text(data['target_mutated'])}`",
        f"- approval_granted: `{_bool_text(data['approval_granted'])}`",
        f"- trusted: `{_bool_text(data['trusted'])}`",
        f"- recommended_next_task: `{data['recommended_next_task']}`",
        "",
        "## Explicit Non-Capabilities",
        "",
    ]
    lines.extend(f"- `{item}`" for item in data["explicit_non_capabilities"])
    lines.append("")
    return "\n".join(lines)


def render_transaction_index_markdown(index: dict[str, Any]) -> str:
    item = index["transactions"][0]
    return (
        "# PatchTransaction Index\n\n"
        f"- result: `{index['status']}`\n"
        f"- record_count: `{index['record_count']}`\n"
        f"- transaction_ref: `{item['transaction_ref']}`\n"
        f"- lifecycle: `{item['lifecycle']}`\n"
        f"- record_valid: `{_bool_text(item['record_valid'])}`\n"
        f"- scope_valid: `{_bool_text(item['scope_valid'])}`\n"
        f"- apply_performed: `{_bool_text(item['apply_performed'])}`\n"
        f"- target_mutated: `{_bool_text(item['target_mutated'])}`\n"
        f"- trusted: `{_bool_text(item['trusted'])}`\n"
        f"- recommended_next_task: `{index['recommended_next_task']}`\n"
    )


def render_scope_report_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# PatchTransaction Scope Report",
        "",
        f"- result: `{report['status']}`",
        f"- scope_valid: `{_bool_text(report['scope_valid'])}`",
        "",
        "## Allowed Paths",
        "",
    ]
    lines.extend(f"- `{item}`" for item in report["allowed_paths"])
    lines.extend(["", "## Forbidden Paths", ""])
    lines.extend(f"- `{item}`" for item in report["forbidden_paths"])
    lines.extend(["", "## Declared Changed Paths", ""])
    lines.extend(f"- `{item}`" for item in report["declared_changed_paths"])
    if report["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    lines.append("")
    return "\n".join(lines)


def render_projection_markdown(report: dict[str, Any]) -> str:
    return (
        "# PatchTransaction Projection Report\n\n"
        f"- result: `{report['status']}`\n"
        f"- transaction_ref: `{report['transaction_ref']}`\n"
        f"- record_valid: `{_bool_text(report['record_valid'])}`\n"
        f"- patch_artifact_path: `{report['patch_artifact_path']}`\n"
        f"- patch_artifact_sha256: `{report['patch_artifact_sha256']}`\n"
        f"- source_artifacts_mutated: `{_bool_text(report['source_artifacts_mutated'])}`\n"
        f"- policy_evaluation_performed: `{_bool_text(report['policy_evaluation_performed'])}`\n"
        f"- approval_granted: `{_bool_text(report['approval_granted'])}`\n"
        f"- apply_performed: `{_bool_text(report['apply_performed'])}`\n"
        f"- target_mutated: `{_bool_text(report['target_mutated'])}`\n"
        f"- rollback_performed: `{_bool_text(report['rollback_performed'])}`\n"
        f"- trusted: `{_bool_text(report['trusted'])}`\n"
        f"- recommended_next_task: `{report['recommended_next_task']}`\n"
    )


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# PatchTransaction Validation Report",
        "",
        f"- result: `{report['validation_status']}`",
        f"- schema_loaded: `{_bool_text(report['schema_loaded'])}`",
        f"- schema_helper_alignment_status: `{report['schema_helper_alignment_status']}`",
        f"- record_valid: `{_bool_text(report['record_valid'])}`",
        f"- scope_valid: `{_bool_text(report['scope_valid'])}`",
        f"- deterministic_projection: `{_bool_text(report['deterministic_projection'])}`",
        f"- source_artifacts_mutated: `{_bool_text(report['source_artifacts_mutated'])}`",
        f"- apply_performed: `{_bool_text(report['apply_performed'])}`",
        f"- target_mutated: `{_bool_text(report['target_mutated'])}`",
        f"- approval_granted: `{_bool_text(report['approval_granted'])}`",
        f"- trusted: `{_bool_text(report['trusted'])}`",
        f"- recommended_next_task: `{report['recommended_next_task']}`",
        "",
        "## Warnings",
        "",
    ]
    lines.extend(f"- {item}" for item in report["warnings"])
    if report["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    lines.append("")
    return "\n".join(lines)


def render_explicit_non_capabilities_markdown() -> str:
    lines = [
        "# PatchTransaction Explicit Non-Capabilities",
        "",
        "This build records a schema-only PatchTransaction proposal. It does not authorize or implement the following capabilities:",
        "",
    ]
    lines.extend(f"- `{item}`" for item in EXPLICIT_NON_CAPABILITIES)
    lines.append("")
    return "\n".join(lines)


def render_future_work_markdown() -> str:
    return (
        "# PatchTransaction Future Work\n\n"
        f"- `{RECOMMENDED_NEXT_TASK}`: independently check schema, helper, CLI, reports, scope validation, deterministic projection, source immutability, evidence, and no-apply boundaries.\n"
        "- `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01`: accept only after independent check passes.\n"
        "- Future apply engine work remains blocked until PatchTransaction is checked and accepted.\n"
    )


def render_next_task_prompt_markdown() -> str:
    return (
        "# AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01\n\n"
        "Independently check the minimal PatchTransaction schema slice created by "
        "`AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`. Re-read live repository truth, "
        "verify the schema/helper/CLI/report/test/evidence chain, recompute the "
        "sample unified-diff artifact digest, test fail-closed scope validation, "
        "confirm no approval, apply, target mutation, admission, or trust occurred, "
        "preserve inherited operational-health warning debt, and stop at "
        "`needs_review`. Do not accept the capability or begin apply-engine work.\n"
    )


def _cli_registered(repo_root: Path) -> bool:
    path = repo_root / ".aide/scripts/aide_lite.py"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "patch-transaction" in text and "command_patch_transaction_validate" in text


def patch_transaction_runtime_summary(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    validation = patch_transaction_validate(root)
    return {
        **validation,
        "cli_registered": _cli_registered(root),
        "reports_json_valid": all(_json_valid(root / path) for path in [TRANSACTION_INDEX_JSON, TRANSACTIONS_JSON, PROJECTION_JSON, VALIDATION_JSON, SCOPE_REPORT_JSON]),
    }
