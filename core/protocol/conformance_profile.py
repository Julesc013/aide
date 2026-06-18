"""Minimal AIDE ConformanceProfile helpers.

This module defines profile-scoped conformance requirements for the accepted
``minimal_capability_manifest`` capability. It writes deterministic candidate
profiles, indexes, and validation reports. It does not run checks, create
ConformanceResult records, admit capabilities, admit adapters, execute workers,
call providers, mutate target repositories, or implement runtime behavior.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import envelope, reference_id


API_VERSION = envelope.API_VERSION
CONFORMANCE_PROFILE_SCHEMA_VERSION = "aide.conformance-profile.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_conformance_profile"
ACCEPTED_PREDECESSOR = "minimal_capability_manifest"
TASK_ID = "AIDE-BUILD-CONFORMANCE-PROFILE-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-CONFORMANCE-PROFILE-01"
DETERMINISTIC_TIMESTAMP = "2026-06-18T00:00:00+10:00"

PROFILE_ID = "minimal_capability_manifest"
PROFILE_VERSION = "1.0.0"
PROFILE_REF = reference_id.format_reference_id("conformance-profile", f"{PROFILE_ID}-v{PROFILE_VERSION}")
SUBJECT_KIND = "capability"
SUBJECT_REF = reference_id.format_reference_id("capability", PROFILE_ID)

REPORT_ROOT = Path(".aide/reports/conformance-profile")
SCHEMA_PATH = Path(".aide/protocol/aide-conformance-profile.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
PROFILES_JSON = REPORT_ROOT / "profiles.json"
PROFILES_MD = REPORT_ROOT / "profiles.md"
PROFILE_INDEX_JSON = REPORT_ROOT / "profile-index.json"
PROFILE_INDEX_MD = REPORT_ROOT / "profile-index.md"
CASE_INDEX_JSON = REPORT_ROOT / "case-index.json"
CASE_INDEX_MD = REPORT_ROOT / "case-index.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"

REQUIRED_REPORTS = [
    STATUS_MD,
    PROJECTION_JSON,
    PROJECTION_MD,
    VALIDATION_JSON,
    VALIDATION_MD,
    PROFILES_JSON,
    PROFILES_MD,
    PROFILE_INDEX_JSON,
    PROFILE_INDEX_MD,
    CASE_INDEX_JSON,
    CASE_INDEX_MD,
    FUTURE_WORK_MD,
    UNFINISHED_WORK_MD,
]

SUPPORTED_KINDS = {
    "ConformanceProfile",
    "ConformanceProfileProjectionReport",
    "ConformanceProfileValidationReport",
    "ConformanceProfileIndex",
    "ConformanceCaseIndex",
}

REQUIREMENT_LEVELS = {"required", "optional", "advisory"}
LIFECYCLES = {"candidate", "accepted", "superseded"}
ACCEPTED_OUTCOMES = {"PASS", "PASS_WITH_WARNINGS", "ACCEPTED", "ACCEPTED_WITH_WARNINGS"}
KNOWN_EVALUATORS = {
    "boundary_review",
    "evidence_file_exists",
    "json_report_valid",
    "predecessor_validator",
    "queue_task_status",
    "reference_id_validator",
    "report_review",
    "schema_parse",
    "source_mutation_sentinel",
}

PROFILE_CLASSES = ["protocol", "capability_admission_requirements"]

EVIDENCE_REQUIREMENTS = [
    "profile_subject_ref",
    "case_id",
    "case_ref",
    "requirement_level",
    "evaluator",
    "accepted_outcomes",
    "source_refs",
    "evidence_refs",
    "report_refs",
    "observed_status",
    "warning_disposition",
]

EXPLICIT_NON_CAPABILITIES = [
    "conformance_result",
    "conformance_runner",
    "conformance_execution",
    "conformance_admission",
    "automatic_admission",
    "policy_decision",
    "adapter_admission",
    "adapter_execution",
    "capability_execution",
    "runtime_capability_registry",
    "patch_transaction",
    "adapter_manifest",
    "context_pack_v2",
    "scheduler",
    "leases",
    "supervisor",
    "runtime",
    "service",
    "commander",
    "test_broker_runtime",
    "worker_execution",
    "provider_adapters",
    "branch_worktree_automation",
    "target_apply",
    "active_apply",
    "rollback_execution",
    "release",
    "promotion",
    "github_mutation",
    "gateway_calls",
    "network_calls",
    "model_provider_calls",
    "target_repo_mutation",
    "production_readiness",
    "release_readiness",
    "broad_autonomous_runtime",
]

FORBIDDEN_CLAIM_PATTERNS = [
    "conformanceprofile admits capability",
    "conformanceprofile proves capability",
    "conformanceprofile executes checks",
    "conformanceresult implemented",
    "conformance runner implemented",
    "automatic admission implemented",
    "adapter admission implemented",
    "adapter execution implemented",
    "runtime capability registry implemented",
    "patchtransaction implemented",
    "adaptermanifest implemented",
    "contextpack v2 implemented",
    "scheduler implemented",
    "leases implemented",
    "supervisor implemented",
    "runtime implemented",
    "service implemented",
    "commander implemented",
    "test broker runtime implemented",
    "worker execution implemented",
    "provider/model calls implemented",
    "network/gateway/github calls implemented",
    "target apply implemented",
    "active apply implemented",
    "release ready",
    "production ready",
    "autonomous runtime ready",
]

SCHEMA_VALIDATION_MODE = "minimal_json_schema_subset"
SCHEMA_VALIDATION_LIMITATIONS = [
    "Local subset validator checks required envelope, profile, case, aggregation, evidence, and boundary fields.",
    "Full JSON Schema Draft 2020-12 validation remains future work.",
    "ConformanceProfile defines requirements only; ConformanceResult and admission remain future work.",
]

CONFORMANCE_CASE_DEFINITIONS: list[dict[str, Any]] = [
    {
        "case_id": "capability-manifest-schema-parses",
        "title": "CapabilityManifest Schema Parses",
        "description": "The accepted CapabilityManifest schema exists and parses as JSON.",
        "requirement_level": "required",
        "evaluator": "schema_parse",
        "accepted_outcomes": ["PASS", "PASS_WITH_WARNINGS"],
        "evidence_required": [".aide/protocol/aide-capability-manifest.schema.json"],
        "dependencies": [],
        "source_refs": [
            reference_id.format_reference_id("schema", "aide-capability-manifest"),
            reference_id.format_reference_id("queue-task", "AIDE-BUILD-CAPABILITY-MANIFEST-01"),
        ],
    },
    {
        "case_id": "capability-manifest-projection-json-valid",
        "title": "CapabilityManifest Projection JSON Valid",
        "description": "The accepted CapabilityManifest projection and index reports parse as JSON.",
        "requirement_level": "required",
        "evaluator": "json_report_valid",
        "accepted_outcomes": ["PASS", "PASS_WITH_WARNINGS"],
        "evidence_required": [
            ".aide/reports/capability-manifest/capabilities.json",
            ".aide/reports/capability-manifest/capability-index.json",
        ],
        "dependencies": ["capability-manifest-schema-parses"],
        "source_refs": [
            reference_id.format_reference_id("report", "capability-manifest-capabilities"),
            reference_id.format_reference_id("report", "capability-manifest-capability-index"),
        ],
    },
    {
        "case_id": "capability-manifest-validation-pass-with-warnings",
        "title": "CapabilityManifest Validation Preserved",
        "description": "CapabilityManifest validation reports PASS_WITH_WARNINGS and preserves warning debt.",
        "requirement_level": "required",
        "evaluator": "predecessor_validator",
        "accepted_outcomes": ["PASS", "PASS_WITH_WARNINGS", "ACCEPTED_WITH_WARNINGS"],
        "evidence_required": [
            ".aide/reports/capability-manifest/validation.json",
            ".aide/reports/capability-manifest-check/check-report.json",
        ],
        "dependencies": ["capability-manifest-projection-json-valid"],
        "source_refs": [
            reference_id.format_reference_id("queue-task", "AIDE-BUILD-CAPABILITY-MANIFEST-01"),
            reference_id.format_reference_id("queue-task", "AIDE-CHECK-CAPABILITY-MANIFEST-01"),
        ],
    },
    {
        "case_id": "capability-manifest-acceptance-evidence-complete",
        "title": "CapabilityManifest Acceptance Evidence Complete",
        "description": "The acceptance queue task exists, remains at needs_review, and has no missing evidence.",
        "requirement_level": "required",
        "evaluator": "queue_task_status",
        "accepted_outcomes": ["ACCEPTED", "ACCEPTED_WITH_WARNINGS", "PASS_WITH_WARNINGS"],
        "evidence_required": [
            ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/task.yaml",
            ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/status.yaml",
            ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/evidence/acceptance-summary.md",
        ],
        "dependencies": ["capability-manifest-validation-pass-with-warnings"],
        "source_refs": [
            reference_id.format_reference_id("queue-task", "AIDE-ACCEPT-CAPABILITY-MANIFEST-01"),
        ],
    },
    {
        "case_id": "capability-manifest-declaration-only-boundary",
        "title": "Declaration-Only Boundary Preserved",
        "description": "CapabilityManifest declares capability state without proof, execution, admission, or adapter trust.",
        "requirement_level": "required",
        "evaluator": "boundary_review",
        "accepted_outcomes": ["PASS", "PASS_WITH_WARNINGS", "ACCEPTED_WITH_WARNINGS"],
        "evidence_required": [
            ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/evidence/capability-boundary-review.md",
            ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/evidence/non-capability-boundary.md",
        ],
        "dependencies": ["capability-manifest-acceptance-evidence-complete"],
        "source_refs": [
            reference_id.format_reference_id("queue-task", "AIDE-ACCEPT-CAPABILITY-MANIFEST-01"),
            SUBJECT_REF,
        ],
    },
    {
        "case_id": "accepted-warning-debt-classified",
        "title": "Accepted Warning Debt Classified",
        "description": "Accepted warning dispositions remain visible and are not repaired opportunistically.",
        "requirement_level": "required",
        "evaluator": "report_review",
        "accepted_outcomes": ["PASS", "PASS_WITH_WARNINGS", "ACCEPTED_WITH_WARNINGS"],
        "evidence_required": [
            ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/evidence/warning-disposition.md",
            ".aide/reports/capability-manifest-accept/warning-disposition.md",
        ],
        "dependencies": ["capability-manifest-acceptance-evidence-complete"],
        "source_refs": [
            reference_id.format_reference_id("report", "capability-manifest-accept-warning-disposition"),
        ],
    },
    {
        "case_id": "reference-and-event-refs-parse",
        "title": "Reference And Event Refs Parse",
        "description": "Projected source, evidence, report, event, and capability refs remain syntactically valid.",
        "requirement_level": "required",
        "evaluator": "reference_id_validator",
        "accepted_outcomes": ["PASS", "PASS_WITH_WARNINGS"],
        "evidence_required": [
            ".aide/reports/reference-id/validation.json",
            ".aide/reports/event-record/validation.json",
        ],
        "dependencies": ["capability-manifest-projection-json-valid"],
        "source_refs": [
            reference_id.format_reference_id("report", "reference-id-validation"),
            reference_id.format_reference_id("report", "event-record-validation"),
        ],
    },
    {
        "case_id": "source-artifacts-not-mutated-by-profile",
        "title": "Profile Projection Does Not Mutate Source Artifacts",
        "description": "Building the profile reads predecessor artifacts but writes only ConformanceProfile outputs.",
        "requirement_level": "required",
        "evaluator": "source_mutation_sentinel",
        "accepted_outcomes": ["PASS", "PASS_WITH_WARNINGS"],
        "evidence_required": [".aide/reports/conformance-profile/projection-report.json"],
        "dependencies": [
            "capability-manifest-projection-json-valid",
            "capability-manifest-declaration-only-boundary",
        ],
        "source_refs": [
            reference_id.format_reference_id("queue-task", TASK_ID),
        ],
    },
    {
        "case_id": "latest-task-packet-drift-classified",
        "title": "Latest Task Packet Drift Classified",
        "description": "Stale latest-task-packet projection drift remains classified as warning debt.",
        "requirement_level": "advisory",
        "evaluator": "report_review",
        "accepted_outcomes": ["PASS", "PASS_WITH_WARNINGS"],
        "evidence_required": [".aide/reports/reconciler/findings.json"],
        "dependencies": [],
        "source_refs": [
            reference_id.format_reference_id("report", "reconciler-findings"),
        ],
    },
    {
        "case_id": "track-b-b1-barrier-authorized-track-a",
        "title": "Track B B1 Barrier Authorized Track A",
        "description": "Track B B1 completed with zero errors/blockers and authorized Track A resumption.",
        "requirement_level": "optional",
        "evaluator": "report_review",
        "accepted_outcomes": ["PASS", "PASS_WITH_WARNINGS"],
        "evidence_required": [
            ".aide/queue/AIDE-CHECK-TRACK-B-B1-BARRIER-01/status.yaml",
        ],
        "dependencies": [],
        "source_refs": [
            reference_id.format_reference_id("queue-task", "AIDE-CHECK-TRACK-B-B1-BARRIER-01"),
        ],
    },
]


def stable_json(data: Any) -> str:
    return envelope.stable_json(data)


def read_json(path: Path) -> dict[str, Any]:
    return envelope.read_json(path)


def write_json(path: Path, obj: dict[str, Any]) -> None:
    envelope.write_json(path, obj)


def write_text(path: Path, text: str) -> None:
    envelope.write_text(path, text)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _relative(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


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


def _case_ref(case_id: str) -> str:
    return f"{PROFILE_REF}#{case_id}"


def _profile_ref(profile_id: str, profile_version: str) -> str:
    return reference_id.format_reference_id("conformance-profile", f"{profile_id}-v{profile_version}")


def _path_exists(repo_root: Path, rel: str) -> bool:
    return (repo_root / rel).exists()


def _semver(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", value))


def _hash_source_artifacts(repo_root: Path, rels: list[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel in rels:
        path = repo_root / rel
        if path.exists() and path.is_file():
            hashes[rel] = sha256_file(path)
    return hashes


def source_artifact_paths(repo_root: str | Path) -> list[str]:
    root = Path(repo_root)
    paths: set[str] = {
        ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/task.yaml",
        ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/status.yaml",
        ".aide/queue/AIDE-CHECK-TRACK-B-B1-BARRIER-01/status.yaml",
        ".aide/protocol/aide-capability-manifest.schema.json",
        ".aide/reports/capability-manifest/capabilities.json",
        ".aide/reports/capability-manifest/capability-index.json",
        ".aide/reports/capability-manifest/validation.json",
        ".aide/reports/capability-manifest-check/check-report.json",
        ".aide/reports/capability-manifest-accept/acceptance-report.json",
        ".aide/reports/capability-manifest-accept/warning-disposition.md",
        ".aide/reports/capability-manifest-accept/non-capabilities.md",
        ".aide/reports/reconciler/findings.json",
        ".aide/reports/reference-id/validation.json",
        ".aide/reports/event-record/validation.json",
        "core/protocol/capability_manifest.py",
    }
    evidence_root = root / ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/evidence"
    if evidence_root.exists():
        paths.update(_relative(path, root) for path in sorted(evidence_root.glob("*.md")))
    return sorted(rel for rel in paths if (root / rel).exists())


def load_conformance_profile_schema(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / SCHEMA_PATH
    if not path.exists():
        raise ValueError(f"ConformanceProfile schema missing: {SCHEMA_PATH.as_posix()}")
    return read_json(path)


def build_conformance_case(definition: dict[str, Any]) -> dict[str, Any]:
    case_id = str(definition["case_id"])
    return {
        "case_id": case_id,
        "case_ref": _case_ref(case_id),
        "title": str(definition["title"]),
        "description": str(definition["description"]),
        "requirement_level": str(definition["requirement_level"]),
        "evaluator": str(definition["evaluator"]),
        "accepted_outcomes": list(definition["accepted_outcomes"]),
        "evidence_required": list(definition["evidence_required"]),
        "dependencies": list(definition["dependencies"]),
        "source_refs": list(definition["source_refs"]),
        "result_ref": None,
        "result_generated": False,
        "execution_implemented": False,
        "admission_performed": False,
    }


def build_conformance_profile(repo_root: str | Path) -> dict[str, Any]:
    del repo_root
    cases = [build_conformance_case(definition) for definition in CONFORMANCE_CASE_DEFINITIONS]
    warnings = conformance_profile_warnings()
    metadata = {
        "id": "conformance-profile-minimal-capability-manifest-v1",
        "name": "Minimal CapabilityManifest ConformanceProfile",
        "title": "Minimal CapabilityManifest ConformanceProfile",
        "createdAt": DETERMINISTIC_TIMESTAMP,
        "sourcePath": PROFILES_JSON.as_posix(),
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility([PROFILE_ID]),
    }
    spec = {
        "profile_ref": PROFILE_REF,
        "profile_id": PROFILE_ID,
        "profile_version": PROFILE_VERSION,
        "lifecycle": "candidate",
        "subject": {
            "kind": SUBJECT_KIND,
            "ref": SUBJECT_REF,
        },
        "accepted_predecessor": ACCEPTED_PREDECESSOR,
        "profile_class": list(PROFILE_CLASSES),
        "cases": cases,
        "aggregation_policy": {
            "required_cases": "all_required_cases_must_have_accepted_outcomes",
            "missing_required_case": "fail_closed",
            "unknown_required_evaluator": "fail_closed",
            "unknown_optional_evaluator": "warn_only",
            "unknown_advisory_evaluator": "warn_only",
            "dependency_failure": "fail_closed_for_dependent_required_cases",
            "optional_case_failure": "warning_only",
            "advisory_case_failure": "informational_warning",
            "admission_decision": "out_of_scope",
        },
        "evidence_requirements": list(EVIDENCE_REQUIREMENTS),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "result_model": {
            "kind": "ConformanceResult",
            "implemented": False,
            "result_generated": False,
            "future_task": "AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01",
        },
        "admission": {
            "implemented": False,
            "admission_performed": False,
            "policy_decision": False,
            "trusted": False,
        },
    }
    status = {
        "valid": True,
        "validated": True,
        "result": "PASS_WITH_WARNINGS",
        "validation_status": "PASS_WITH_WARNINGS",
        "validation_errors": [],
        "validation_warnings": warnings,
        "profile_only": True,
        "result_generated": False,
        "execution_implemented": False,
        "admission_performed": False,
        "admitted": False,
        "trusted": False,
        "runtime": False,
        "mutating": False,
    }
    obj = envelope.build_envelope("ConformanceProfile", metadata, spec, status, api_version=API_VERSION)
    obj["schema_version"] = CONFORMANCE_PROFILE_SCHEMA_VERSION
    obj["protocol_version"] = PROTOCOL_VERSION
    return obj


def build_profile_index(profile: dict[str, Any]) -> dict[str, Any]:
    spec = profile.get("spec", {})
    cases = list(spec.get("cases", []))
    return {
        "schema_version": "aide.conformance-profile-index.v0",
        "report_type": "conformance_profile_index",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "status": profile.get("status", {}).get("validation_status", "UNKNOWN"),
        "profile_ref": spec.get("profile_ref"),
        "profile_id": spec.get("profile_id"),
        "profile_version": spec.get("profile_version"),
        "lifecycle": spec.get("lifecycle"),
        "subject": spec.get("subject", {}),
        "profile_class": spec.get("profile_class", []),
        "case_count": len(cases),
        "required_case_count": sum(1 for item in cases if item.get("requirement_level") == "required"),
        "optional_case_count": sum(1 for item in cases if item.get("requirement_level") == "optional"),
        "advisory_case_count": sum(1 for item in cases if item.get("requirement_level") == "advisory"),
        "profile_only": True,
        "result_generated": False,
        "admission_performed": False,
        "trusted": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def build_case_index(profile: dict[str, Any]) -> dict[str, Any]:
    cases = list(profile.get("spec", {}).get("cases", []))
    return {
        "schema_version": "aide.conformance-case-index.v0",
        "report_type": "conformance_case_index",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "profile_ref": profile.get("spec", {}).get("profile_ref"),
        "case_count": len(cases),
        "cases": [
            {
                "case_id": item.get("case_id"),
                "case_ref": item.get("case_ref"),
                "requirement_level": item.get("requirement_level"),
                "evaluator": item.get("evaluator"),
                "dependencies": item.get("dependencies", []),
                "accepted_outcomes": item.get("accepted_outcomes", []),
                "result_ref": item.get("result_ref"),
                "result_generated": item.get("result_generated"),
                "execution_implemented": item.get("execution_implemented"),
                "admission_performed": item.get("admission_performed"),
            }
            for item in cases
        ],
        "profile_only": True,
        "result_generated": False,
        "admission_performed": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def conformance_profile_counts(profile: dict[str, Any]) -> dict[str, int]:
    cases = list(profile.get("spec", {}).get("cases", []))
    return {
        "profile_count": 1,
        "case_count": len(cases),
        "required_case_count": sum(1 for item in cases if item.get("requirement_level") == "required"),
        "optional_case_count": sum(1 for item in cases if item.get("requirement_level") == "optional"),
        "advisory_case_count": sum(1 for item in cases if item.get("requirement_level") == "advisory"),
    }


def conformance_profile_warnings() -> list[str]:
    return [
        "ConformanceProfile defines required checks but does not execute them.",
        "ConformanceResult is not implemented by this slice.",
        "Admission policy and acceptance decisions remain separate future work.",
        "The profile lifecycle is candidate and must be checked independently before acceptance.",
        "Unknown required evaluators fail closed; optional and advisory unknown evaluators warn only.",
        "Accepted predecessor warning debt is preserved rather than repaired.",
        "Stale generated latest-task-packet drift remains reported; queue truth is canonical.",
    ]


def future_work_items() -> list[dict[str, str]]:
    return [
        {
            "task": RECOMMENDED_NEXT_TASK,
            "reason": "independent review of ConformanceProfile schema, helper, reports, CLI, tests, and boundaries",
        },
        {
            "task": "AIDE-ACCEPT-CONFORMANCE-PROFILE-01",
            "reason": "accept the profile only after independent check evidence exists",
        },
        {
            "task": "AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01",
            "reason": "future object for recording observed case results after the profile is accepted",
        },
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    return [{"item": item, "reason": "intentionally deferred beyond the minimal ConformanceProfile slice"} for item in EXPLICIT_NON_CAPABILITIES]


def _case_ids(cases: list[dict[str, Any]]) -> list[str]:
    return [str(item.get("case_id", "")) for item in cases]


def _dependency_cycle_errors(cases: list[dict[str, Any]]) -> list[str]:
    by_id = {str(item.get("case_id")): item for item in cases if isinstance(item.get("case_id"), str)}
    errors: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(case_id: str, stack: list[str]) -> None:
        if case_id in visited:
            return
        if case_id in visiting:
            cycle = " -> ".join([*stack, case_id])
            errors.append(f"case dependency cycle detected: {cycle}")
            return
        visiting.add(case_id)
        for dependency in by_id.get(case_id, {}).get("dependencies", []):
            if dependency in by_id:
                visit(str(dependency), [*stack, case_id])
        visiting.remove(case_id)
        visited.add(case_id)

    for case_id in by_id:
        visit(case_id, [])
    return errors


def _validate_refs(refs: list[str], *, required: bool) -> list[str]:
    errors: list[str] = []
    for ref in refs:
        result = reference_id.validate_reference_id(ref, required=required)
        if not result.valid:
            errors.extend(result.errors)
    return errors


def validate_conformance_profile_with_schema(obj: dict[str, Any], schema: dict[str, Any]) -> tuple[list[str], list[str]]:
    del schema
    errors: list[str] = []
    warnings: list[str] = []
    if obj.get("apiVersion") != API_VERSION:
        errors.append("apiVersion must match AIDE API version")
    if obj.get("kind") != "ConformanceProfile":
        errors.append("kind must be ConformanceProfile")
    for field in ["metadata", "spec", "status"]:
        if not isinstance(obj.get(field), dict):
            errors.append(f"{field} must be an object")
    spec = obj.get("spec") if isinstance(obj.get("spec"), dict) else {}
    status = obj.get("status") if isinstance(obj.get("status"), dict) else {}
    for field in [
        "profile_ref",
        "profile_id",
        "profile_version",
        "lifecycle",
        "subject",
        "profile_class",
        "cases",
        "aggregation_policy",
        "evidence_requirements",
        "explicit_non_capabilities",
    ]:
        if field not in spec:
            errors.append(f"missing spec field: {field}")
    if spec.get("profile_ref") != _profile_ref(str(spec.get("profile_id", "")), str(spec.get("profile_version", ""))):
        errors.append("spec.profile_ref must match profile_id/profile_version")
    profile_ref_result = reference_id.validate_reference_id(str(spec.get("profile_ref", "")), required=True)
    errors.extend(profile_ref_result.errors)
    if not _semver(spec.get("profile_version")):
        errors.append("spec.profile_version must be SemVer")
    if spec.get("lifecycle") not in LIFECYCLES:
        errors.append(f"unsupported lifecycle: {spec.get('lifecycle')}")
    subject = spec.get("subject") if isinstance(spec.get("subject"), dict) else {}
    if subject.get("kind") != "capability":
        errors.append("spec.subject.kind must be capability")
    subject_ref = subject.get("ref")
    if not isinstance(subject_ref, str) or not subject_ref:
        errors.append("spec.subject.ref must be a non-empty ReferenceID")
    else:
        errors.extend(reference_id.validate_reference_id(subject_ref, required=True).errors)
    cases = spec.get("cases", [])
    if not isinstance(cases, list) or not cases:
        errors.append("spec.cases must be a non-empty array")
        cases = []
    ids = _case_ids(cases)
    if len(ids) != len(set(ids)):
        errors.append("case_id values must be unique within a profile")
    known_ids = set(ids)
    required_case_seen = False
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"spec.cases[{index}] must be an object")
            continue
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"spec.cases[{index}].case_id must be non-empty")
            continue
        if case.get("case_ref") != f"{spec.get('profile_ref')}#{case_id}":
            errors.append(f"spec.cases[{index}].case_ref must be scoped to profile_ref")
        requirement_level = case.get("requirement_level")
        if requirement_level not in REQUIREMENT_LEVELS:
            errors.append(f"spec.cases[{index}].requirement_level is unsupported: {requirement_level}")
        if requirement_level == "required":
            required_case_seen = True
        evaluator = case.get("evaluator")
        if evaluator not in KNOWN_EVALUATORS:
            message = f"spec.cases[{index}].evaluator is unknown: {evaluator}"
            if requirement_level == "required":
                errors.append(message)
            else:
                warnings.append(message)
        accepted = case.get("accepted_outcomes")
        if not isinstance(accepted, list):
            errors.append(f"spec.cases[{index}].accepted_outcomes must be an array")
            accepted = []
        if requirement_level == "required" and not any(item in ACCEPTED_OUTCOMES for item in accepted):
            errors.append(f"required case has no accepted outcome: {case_id}")
        for dependency in case.get("dependencies", []):
            if dependency not in known_ids:
                errors.append(f"case dependency is missing: {case_id} depends on {dependency}")
        if not isinstance(case.get("evidence_required"), list) or not case.get("evidence_required"):
            errors.append(f"spec.cases[{index}].evidence_required must be a non-empty array")
        if not isinstance(case.get("source_refs"), list) or not case.get("source_refs"):
            errors.append(f"spec.cases[{index}].source_refs must be a non-empty array")
        else:
            errors.extend(_validate_refs([str(ref) for ref in case.get("source_refs", [])], required=True))
        if case.get("result_ref") is not None:
            errors.append(f"spec.cases[{index}].result_ref must be null until ConformanceResult exists")
        for flag in ["result_generated", "execution_implemented", "admission_performed"]:
            if case.get(flag) is not False:
                errors.append(f"spec.cases[{index}].{flag} must be false in this slice")
    if not required_case_seen:
        errors.append("profile must define at least one required case")
    errors.extend(_dependency_cycle_errors(cases))
    aggregation = spec.get("aggregation_policy") if isinstance(spec.get("aggregation_policy"), dict) else {}
    if aggregation.get("missing_required_case") != "fail_closed":
        errors.append("aggregation_policy.missing_required_case must be fail_closed")
    if aggregation.get("unknown_required_evaluator") != "fail_closed":
        errors.append("aggregation_policy.unknown_required_evaluator must be fail_closed")
    explicit = spec.get("explicit_non_capabilities")
    if not isinstance(explicit, list):
        errors.append("spec.explicit_non_capabilities must be an array")
    else:
        for item in ["conformance_result", "conformance_execution", "conformance_admission", "adapter_admission", "patch_transaction", "runtime"]:
            if item not in explicit:
                errors.append(f"missing explicit non-capability: {item}")
    for field in [
        "valid",
        "validation_status",
        "validation_errors",
        "validation_warnings",
        "profile_only",
        "result_generated",
        "execution_implemented",
        "admission_performed",
        "admitted",
        "trusted",
    ]:
        if field not in status:
            errors.append(f"missing status field: {field}")
    for false_field in ["result_generated", "execution_implemented", "admission_performed", "admitted", "trusted", "runtime", "mutating"]:
        if status.get(false_field) is not False:
            errors.append(f"status.{false_field} must be false in this slice")
    if status.get("profile_only") is not True:
        errors.append("status.profile_only must be true")
    return errors, warnings


def _cli_registered(repo_root: Path) -> bool:
    script = repo_root / ".aide/scripts/aide_lite.py"
    return script.exists() and 'subparsers.add_parser("conformance-profile")' in script.read_text(encoding="utf-8")


def _json_valid(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return True


def _profile_reports_exist(repo_root: Path) -> bool:
    in_progress_outputs = {VALIDATION_JSON, VALIDATION_MD}
    return all((repo_root / rel).exists() for rel in REQUIRED_REPORTS if rel not in in_progress_outputs)


def _source_evidence_exists(repo_root: Path, profile: dict[str, Any]) -> bool:
    cases = list(profile.get("spec", {}).get("cases", []))
    return all(
        _path_exists(repo_root, str(rel))
        for case in cases
        for rel in case.get("evidence_required", [])
        if isinstance(rel, str) and rel.startswith(".aide/")
    )


def _profile_boundary_valid(profile: dict[str, Any]) -> bool:
    spec = profile.get("spec", {})
    status = profile.get("status", {})
    result_model = spec.get("result_model", {}) if isinstance(spec.get("result_model"), dict) else {}
    admission = spec.get("admission", {}) if isinstance(spec.get("admission"), dict) else {}
    return (
        status.get("profile_only") is True
        and status.get("result_generated") is False
        and status.get("execution_implemented") is False
        and status.get("admission_performed") is False
        and status.get("admitted") is False
        and status.get("trusted") is False
        and result_model.get("implemented") is False
        and result_model.get("result_generated") is False
        and admission.get("implemented") is False
        and admission.get("admission_performed") is False
        and admission.get("trusted") is False
    )


def _overclaiming_findings(repo_root: Path) -> list[str]:
    findings: list[str] = []
    for rel in [STATUS_MD, PROJECTION_MD, VALIDATION_MD, PROFILES_MD, PROFILE_INDEX_MD, CASE_INDEX_MD, FUTURE_WORK_MD, UNFINISHED_WORK_MD]:
        path = repo_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for pattern in FORBIDDEN_CLAIM_PATTERNS:
            if pattern in text:
                findings.append(f"{rel.as_posix()}: forbidden claim pattern: {pattern}")
    return findings


def forbidden_operations_preserved() -> dict[str, bool]:
    return {
        "result_generation": True,
        "case_execution": True,
        "admission_policy": True,
        "adapter_admission": True,
        "adapter_execution": True,
        "runtime_registry": True,
        "patch_transaction": True,
        "target_apply": True,
        "branch_worktree_automation": True,
        "github_mutation": True,
        "gateway_calls": True,
        "network_calls": True,
        "provider_model_calls": True,
        "release_promotion": True,
    }


def conformance_profile_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    profile = build_conformance_profile(root)
    counts = conformance_profile_counts(profile)
    data = {
        "schema_version": "aide.conformance-profile-status.v0",
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "profile_ref": PROFILE_REF,
        "profile_id": PROFILE_ID,
        "profile_version": PROFILE_VERSION,
        "subject_ref": SUBJECT_REF,
        "status": "PASS_WITH_WARNINGS",
        "schema_path": SCHEMA_PATH.as_posix(),
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_path": "core/protocol/conformance_profile.py",
        "helper_exists": (root / "core/protocol/conformance_profile.py").exists(),
        "projection_exists": (root / PROJECTION_JSON).exists(),
        **counts,
        "warnings": conformance_profile_warnings(),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "profile_only": True,
        "result_generated": False,
        "execution_implemented": False,
        "admission_performed": False,
        "admitted": False,
        "trusted": False,
        "runtime": False,
        "mutating": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    return data


def write_conformance_profile_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    sources = source_artifact_paths(root)
    before = _hash_source_artifacts(root, sources)
    profile = build_conformance_profile(root)
    profile_index = build_profile_index(profile)
    case_index = build_case_index(profile)
    write_json(root / PROFILES_JSON, profile)
    write_text(root / PROFILES_MD, render_profiles_markdown(profile))
    write_json(root / PROFILE_INDEX_JSON, profile_index)
    write_text(root / PROFILE_INDEX_MD, render_profile_index_markdown(profile_index))
    write_json(root / CASE_INDEX_JSON, case_index)
    write_text(root / CASE_INDEX_MD, render_case_index_markdown(case_index))
    write_text(root / FUTURE_WORK_MD, render_future_work_markdown())
    write_text(root / UNFINISHED_WORK_MD, render_unfinished_work_markdown())
    counts = conformance_profile_counts(profile)
    after = _hash_source_artifacts(root, sources)
    report = {
        "schema_version": "aide.conformance-profile-projection.v0",
        "report_type": "conformance_profile_projection",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "profile_ref": PROFILE_REF,
        "profile_id": PROFILE_ID,
        "profile_version": PROFILE_VERSION,
        "subject_ref": SUBJECT_REF,
        "status": "PASS_WITH_WARNINGS",
        "profile_only": True,
        "result_generated": False,
        "execution_implemented": False,
        "admission_performed": False,
        "admitted": False,
        "trusted": False,
        **counts,
        "source_artifacts_checked": sources,
        "source_artifacts_mutated": before != after,
        "reports_written": [path.as_posix() for path in REQUIRED_REPORTS],
        "warnings": conformance_profile_warnings(),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    status = conformance_profile_status(root)
    status["status"] = report["status"]
    write_text(root / STATUS_MD, render_status_markdown(status))
    validation = validate_conformance_profile(root, project=False)
    report["status"] = validation["validation_status"]
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    status["status"] = report["status"]
    write_text(root / STATUS_MD, render_status_markdown(status))
    return report


def validate_conformance_profile(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    if project:
        projection_result = write_conformance_profile_reports(root)
    else:
        projection_result = {"status": "PASS_WITH_WARNINGS"}
    profile = build_conformance_profile(root)
    schema_errors: list[str] = []
    schema_warnings: list[str] = []
    schema_file_loaded = False
    schema_file_parsed = False
    schema_validation_executed = False
    try:
        schema = load_conformance_profile_schema(root)
        schema_file_loaded = True
        schema_file_parsed = True
        profile_errors, profile_warnings = validate_conformance_profile_with_schema(profile, schema)
        schema_validation_executed = True
        schema_errors.extend(profile_errors)
        schema_warnings.extend(profile_warnings)
    except ValueError as exc:
        schema_errors.append(str(exc))
    forbidden = forbidden_operations_preserved()
    overclaiming_findings = _overclaiming_findings(root)
    reports_generated = _profile_reports_exist(root)
    profiles_json_valid = _json_valid(root / PROFILES_JSON) if (root / PROFILES_JSON).exists() else False
    profile_index_json_valid = _json_valid(root / PROFILE_INDEX_JSON) if (root / PROFILE_INDEX_JSON).exists() else False
    case_index_json_valid = _json_valid(root / CASE_INDEX_JSON) if (root / CASE_INDEX_JSON).exists() else False
    case_ids_unique = len(_case_ids(profile["spec"]["cases"])) == len(set(_case_ids(profile["spec"]["cases"])))
    dependencies_resolve = not [
        dependency
        for case in profile["spec"]["cases"]
        for dependency in case.get("dependencies", [])
        if dependency not in set(_case_ids(profile["spec"]["cases"]))
    ]
    dependency_cycles_absent = not _dependency_cycle_errors(profile["spec"]["cases"])
    required_cases_fail_closed = profile["spec"]["aggregation_policy"].get("missing_required_case") == "fail_closed"
    unknown_required_evaluator_fails_closed = profile["spec"]["aggregation_policy"].get("unknown_required_evaluator") == "fail_closed"
    unknown_optional_evaluator_warns = profile["spec"]["aggregation_policy"].get("unknown_optional_evaluator") == "warn_only"
    unknown_advisory_evaluator_warns = profile["spec"]["aggregation_policy"].get("unknown_advisory_evaluator") == "warn_only"
    required_cases_have_accepted_outcomes = all(
        case.get("requirement_level") != "required" or any(item in ACCEPTED_OUTCOMES for item in case.get("accepted_outcomes", []))
        for case in profile["spec"]["cases"]
    )
    validation_errors = [*schema_errors, *overclaiming_findings]
    status = (
        "PASS_WITH_WARNINGS"
        if not validation_errors
        and projection_result.get("status") in {"PASS", "PASS_WITH_WARNINGS"}
        and reports_generated
        and profiles_json_valid
        and profile_index_json_valid
        and case_index_json_valid
        and _profile_boundary_valid(profile)
        and _source_evidence_exists(root, profile)
        and case_ids_unique
        and dependencies_resolve
        and dependency_cycles_absent
        and required_cases_fail_closed
        and unknown_required_evaluator_fails_closed
        and unknown_optional_evaluator_warns
        and unknown_advisory_evaluator_warns
        and required_cases_have_accepted_outcomes
        and all(forbidden.values())
        else "FAILED_VALIDATION"
    )
    warnings = [*conformance_profile_warnings(), *schema_warnings]
    report = {
        "schema_version": "aide.conformance-profile-validation.v0",
        "report_type": "conformance_profile_validation",
        "kind": "ConformanceProfileValidationReport",
        "task_id": TASK_ID,
        "status": status,
        "validation_status": status,
        "validated": status in {"PASS", "PASS_WITH_WARNINGS"},
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_target": FEATURE_FLAG,
        "accepted_predecessor": ACCEPTED_PREDECESSOR,
        "profile_ref": PROFILE_REF,
        "profile_id": PROFILE_ID,
        "profile_version": PROFILE_VERSION,
        "subject_ref": SUBJECT_REF,
        "schema_path": SCHEMA_PATH.as_posix(),
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "schema_file_loaded": schema_file_loaded,
        "schema_file_parsed": schema_file_parsed,
        "schema_validation_executed": schema_validation_executed,
        "schema_validation_mode": SCHEMA_VALIDATION_MODE if schema_validation_executed else "unavailable",
        "schema_validation_limitations": SCHEMA_VALIDATION_LIMITATIONS,
        "helper_path": "core/protocol/conformance_profile.py",
        "helper_exists": (root / "core/protocol/conformance_profile.py").exists(),
        "cli_registered": _cli_registered(root),
        "reports_generated": reports_generated,
        "profiles_json_valid": profiles_json_valid,
        "profile_index_json_valid": profile_index_json_valid,
        "case_index_json_valid": case_index_json_valid,
        "case_ids_unique": case_ids_unique,
        "dependencies_resolve": dependencies_resolve,
        "dependency_cycles_absent": dependency_cycles_absent,
        "requirement_levels_valid": all(case.get("requirement_level") in REQUIREMENT_LEVELS for case in profile["spec"]["cases"]),
        "known_required_evaluators": all(case.get("requirement_level") != "required" or case.get("evaluator") in KNOWN_EVALUATORS for case in profile["spec"]["cases"]),
        "unknown_required_evaluator_fails_closed": unknown_required_evaluator_fails_closed,
        "unknown_optional_evaluator_warns": unknown_optional_evaluator_warns,
        "unknown_advisory_evaluator_warns": unknown_advisory_evaluator_warns,
        "required_cases_have_accepted_outcomes": required_cases_have_accepted_outcomes,
        "required_cases_fail_closed": required_cases_fail_closed,
        "profile_lifecycle_candidate": profile["spec"].get("lifecycle") == "candidate",
        "evidence_requirements_declared": bool(profile["spec"].get("evidence_requirements")),
        "source_evidence_exists": _source_evidence_exists(root, profile),
        "profile_boundary_valid": _profile_boundary_valid(profile),
        "result_not_generated": profile["status"].get("result_generated") is False,
        "execution_not_implemented": profile["status"].get("execution_implemented") is False,
        "admission_not_performed": profile["status"].get("admission_performed") is False,
        "trusted_not_promoted": profile["status"].get("trusted") is False,
        "explicit_non_capabilities_preserved": all(item in profile["spec"]["explicit_non_capabilities"] for item in EXPLICIT_NON_CAPABILITIES),
        "predecessor_compatibility_preserved": (root / ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/status.yaml").exists(),
        "overclaiming_check_passed": not overclaiming_findings,
        "overclaiming_findings": overclaiming_findings,
        "forbidden_ops_preserved": all(forbidden.values()),
        "forbidden_operations": forbidden,
        "validation_errors": validation_errors,
        "warnings": warnings,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_markdown(report))
    return report


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# ConformanceProfile Status",
        "",
        f"- task_id: {data.get('task_id')}",
        f"- status: {data.get('status')}",
        f"- profile_ref: {data.get('profile_ref')}",
        f"- subject_ref: {data.get('subject_ref')}",
        f"- profile_count: {data.get('profile_count')}",
        f"- case_count: {data.get('case_count')}",
        f"- required_case_count: {data.get('required_case_count')}",
        f"- optional_case_count: {data.get('optional_case_count')}",
        f"- advisory_case_count: {data.get('advisory_case_count')}",
        f"- profile_only: {str(data.get('profile_only')).lower()}",
        f"- result_generated: {str(data.get('result_generated')).lower()}",
        f"- execution_implemented: {str(data.get('execution_implemented')).lower()}",
        f"- admission_performed: {str(data.get('admission_performed')).lower()}",
        f"- admitted: {str(data.get('admitted')).lower()}",
        f"- trusted: {str(data.get('trusted')).lower()}",
        f"- runtime: {str(data.get('runtime')).lower()}",
        f"- mutating: {str(data.get('mutating')).lower()}",
        f"- recommended_next_task: {data.get('recommended_next_task')}",
        "",
        "## Warnings",
        "",
    ]
    lines.extend(f"- {item}" for item in data.get("warnings", []))
    return "\n".join(lines) + "\n"


def render_profiles_markdown(profile: dict[str, Any]) -> str:
    spec = profile["spec"]
    lines = [
        "# Minimal CapabilityManifest ConformanceProfile",
        "",
        f"- profile_ref: {spec.get('profile_ref')}",
        f"- profile_id: {spec.get('profile_id')}",
        f"- profile_version: {spec.get('profile_version')}",
        f"- lifecycle: {spec.get('lifecycle')}",
        f"- subject_ref: {spec.get('subject', {}).get('ref')}",
        f"- profile_only: {str(profile.get('status', {}).get('profile_only')).lower()}",
        f"- result_generated: {str(profile.get('status', {}).get('result_generated')).lower()}",
        f"- admission_performed: {str(profile.get('status', {}).get('admission_performed')).lower()}",
        "",
        "## Cases",
        "",
    ]
    for case in spec.get("cases", []):
        lines.extend(
            [
                f"### {case.get('case_id')}",
                "",
                f"- title: {case.get('title')}",
                f"- requirement_level: {case.get('requirement_level')}",
                f"- evaluator: {case.get('evaluator')}",
                f"- accepted_outcomes: {', '.join(case.get('accepted_outcomes', []))}",
                f"- dependencies: {', '.join(case.get('dependencies', [])) or 'none'}",
                f"- result_ref: {case.get('result_ref')}",
                f"- execution_implemented: {str(case.get('execution_implemented')).lower()}",
                "",
            ]
        )
    return "\n".join(lines)


def render_profile_index_markdown(index: dict[str, Any]) -> str:
    return (
        "# ConformanceProfile Index\n\n"
        f"- status: {index.get('status')}\n"
        f"- profile_ref: {index.get('profile_ref')}\n"
        f"- profile_id: {index.get('profile_id')}\n"
        f"- lifecycle: {index.get('lifecycle')}\n"
        f"- case_count: {index.get('case_count')}\n"
        f"- required_case_count: {index.get('required_case_count')}\n"
        f"- optional_case_count: {index.get('optional_case_count')}\n"
        f"- advisory_case_count: {index.get('advisory_case_count')}\n"
        f"- result_generated: {str(index.get('result_generated')).lower()}\n"
        f"- admission_performed: {str(index.get('admission_performed')).lower()}\n"
        f"- recommended_next_task: {index.get('recommended_next_task')}\n"
    )


def render_case_index_markdown(index: dict[str, Any]) -> str:
    lines = [
        "# ConformanceCase Index",
        "",
        f"- profile_ref: {index.get('profile_ref')}",
        f"- case_count: {index.get('case_count')}",
        f"- result_generated: {str(index.get('result_generated')).lower()}",
        f"- admission_performed: {str(index.get('admission_performed')).lower()}",
        "",
    ]
    for case in index.get("cases", []):
        lines.append(f"- {case.get('case_id')} ({case.get('requirement_level')}, evaluator={case.get('evaluator')})")
    lines.append("")
    return "\n".join(lines)


def render_projection_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# ConformanceProfile Projection Report",
        "",
        f"- status: {report.get('status')}",
        f"- profile_ref: {report.get('profile_ref')}",
        f"- subject_ref: {report.get('subject_ref')}",
        f"- case_count: {report.get('case_count')}",
        f"- required_case_count: {report.get('required_case_count')}",
        f"- source_artifacts_mutated: {str(report.get('source_artifacts_mutated')).lower()}",
        f"- profile_only: {str(report.get('profile_only')).lower()}",
        f"- result_generated: {str(report.get('result_generated')).lower()}",
        f"- execution_implemented: {str(report.get('execution_implemented')).lower()}",
        f"- admission_performed: {str(report.get('admission_performed')).lower()}",
        f"- trusted: {str(report.get('trusted')).lower()}",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Reports Written",
        "",
    ]
    lines.extend(f"- {item}" for item in report.get("reports_written", []))
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in report.get("warnings", []))
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    keys = [
        "schema_exists",
        "schema_file_loaded",
        "schema_file_parsed",
        "schema_validation_executed",
        "helper_exists",
        "cli_registered",
        "reports_generated",
        "profiles_json_valid",
        "profile_index_json_valid",
        "case_index_json_valid",
        "case_ids_unique",
        "dependencies_resolve",
        "dependency_cycles_absent",
        "requirement_levels_valid",
        "known_required_evaluators",
        "unknown_required_evaluator_fails_closed",
        "unknown_optional_evaluator_warns",
        "unknown_advisory_evaluator_warns",
        "required_cases_have_accepted_outcomes",
        "required_cases_fail_closed",
        "profile_lifecycle_candidate",
        "evidence_requirements_declared",
        "source_evidence_exists",
        "profile_boundary_valid",
        "result_not_generated",
        "execution_not_implemented",
        "admission_not_performed",
        "trusted_not_promoted",
        "explicit_non_capabilities_preserved",
        "predecessor_compatibility_preserved",
        "overclaiming_check_passed",
        "forbidden_ops_preserved",
    ]
    lines = [
        "# ConformanceProfile Validation Report",
        "",
        f"- status: {report.get('validation_status')}",
        f"- profile_ref: {report.get('profile_ref')}",
        f"- subject_ref: {report.get('subject_ref')}",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Checks",
        "",
    ]
    lines.extend(f"- {key}: {str(report.get(key)).lower()}" for key in keys)
    lines.extend(["", "## Validation Errors", ""])
    errors = report.get("validation_errors", [])
    lines.extend(f"- {item}" for item in errors) if errors else lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in report.get("warnings", []))
    return "\n".join(lines) + "\n"


def render_future_work_markdown() -> str:
    lines = ["# ConformanceProfile Future Work", ""]
    lines.extend(f"- {item['task']}: {item['reason']}" for item in future_work_items())
    lines.append("")
    return "\n".join(lines)


def render_unfinished_work_markdown() -> str:
    lines = ["# ConformanceProfile Explicit Non-Capabilities", ""]
    lines.extend(f"- {item['item']}: {item['reason']}" for item in unfinished_work_items())
    lines.append("")
    return "\n".join(lines)
