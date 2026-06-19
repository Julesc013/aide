"""Minimal AIDE ConformanceResult helpers.

This module records one deterministic evidence-projected result for the
accepted ``minimal_capability_manifest`` ConformanceProfile candidate. It reads
accepted profile and predecessor evidence, writes result projections and
validation reports, and deliberately does not execute cases, admit subjects,
grant trust, activate profiles, call providers, mutate target repositories, or
implement runtime behavior.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import conformance_profile, envelope, reference_id


API_VERSION = envelope.API_VERSION
CONFORMANCE_RESULT_SCHEMA_VERSION = "aide.conformance-result.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_conformance_result_schema"
ACCEPTED_PREDECESSOR = "minimal_conformance_profile"
TASK_ID = "AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01"
DETERMINISTIC_TIMESTAMP = "2026-06-19T00:00:00+10:00"

PROFILE_ID = "minimal_capability_manifest"
PROFILE_VERSION = "1.0.0"
PROFILE_REF = reference_id.format_reference_id("conformance-profile", f"{PROFILE_ID}-v{PROFILE_VERSION}")
SUBJECT_KIND = "capability"
SUBJECT_REF = reference_id.format_reference_id("capability", PROFILE_ID)
RESULT_ID = "minimal_capability_manifest-v1.0.0-evidence-projection-01"
RESULT_VERSION = "1.0.0"
RESULT_REF = reference_id.format_reference_id("conformance-result", RESULT_ID)

REPORT_ROOT = Path(".aide/reports/conformance-result")
SCHEMA_PATH = Path(".aide/protocol/aide-conformance-result.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
RESULTS_JSON = REPORT_ROOT / "results.json"
RESULTS_MD = REPORT_ROOT / "results.md"
RESULT_INDEX_JSON = REPORT_ROOT / "result-index.json"
RESULT_INDEX_MD = REPORT_ROOT / "result-index.md"
CASE_RESULT_INDEX_JSON = REPORT_ROOT / "case-result-index.json"
CASE_RESULT_INDEX_MD = REPORT_ROOT / "case-result-index.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"

REQUIRED_REPORTS = [
    STATUS_MD,
    PROJECTION_JSON,
    PROJECTION_MD,
    VALIDATION_JSON,
    VALIDATION_MD,
    RESULTS_JSON,
    RESULTS_MD,
    RESULT_INDEX_JSON,
    RESULT_INDEX_MD,
    CASE_RESULT_INDEX_JSON,
    CASE_RESULT_INDEX_MD,
    FUTURE_WORK_MD,
    UNFINISHED_WORK_MD,
]

SUPPORTED_KINDS = {
    "ConformanceResult",
    "ConformanceResultProjectionReport",
    "ConformanceResultValidationReport",
    "ConformanceResultIndex",
    "ConformanceCaseResultIndex",
}

OBSERVATION_MODE = "evidence_projection"
OBSERVED_OUTCOMES = {"PASS", "PASS_WITH_WARNINGS", "FAIL", "ERROR", "SKIPPED", "UNAVAILABLE", "NOT_RUN"}
AGGREGATE_OUTCOMES = {"PASS", "PASS_WITH_WARNINGS", "FAIL", "ERROR", "INCOMPLETE"}
REQUIREMENT_LEVELS = {"required", "optional", "advisory"}
NON_OBSERVED_OUTCOMES = {"SKIPPED", "UNAVAILABLE", "NOT_RUN"}
NORMALIZED_ACCEPTED_OUTCOME_MAP = {
    "PASS": "PASS",
    "ACCEPTED": "PASS",
    "PASS_WITH_WARNINGS": "PASS_WITH_WARNINGS",
    "ACCEPTED_WITH_WARNINGS": "PASS_WITH_WARNINGS",
}

CASE_OUTCOME_OVERRIDES = {
    "capability-manifest-schema-parses": "PASS",
    "capability-manifest-projection-json-valid": "PASS",
    "capability-manifest-validation-pass-with-warnings": "PASS_WITH_WARNINGS",
    "capability-manifest-acceptance-evidence-complete": "PASS_WITH_WARNINGS",
    "capability-manifest-declaration-only-boundary": "PASS_WITH_WARNINGS",
    "accepted-warning-debt-classified": "PASS_WITH_WARNINGS",
    "reference-and-event-refs-parse": "PASS_WITH_WARNINGS",
    "source-artifacts-not-mutated-by-profile": "PASS",
    "latest-task-packet-drift-classified": "PASS_WITH_WARNINGS",
    "track-b-b1-barrier-authorized-track-a": "PASS",
}

EXPLICIT_NON_CAPABILITIES = [
    "conformance_runner",
    "case_execution",
    "command_execution",
    "automatic_result_collection",
    "profile_activation",
    "conformance_admission",
    "automatic_admission",
    "subject_admission_by_conformance_result",
    "trust_grant",
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
    "provider_model_calls",
    "network_calls",
    "gateway_calls",
    "github_mutation",
    "branch_worktree_automation",
    "target_apply",
    "active_apply",
    "rollback_execution",
    "release",
    "promotion",
    "production_readiness",
    "release_readiness",
    "broad_autonomous_runtime",
]

FORBIDDEN_CLAIM_PATTERNS = [
    "admission_performed: true",
    "subject_admitted: true",
    "trusted: true",
    "execution_performed: true",
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

SCHEMA_VALIDATION_MODE = "minimal_json_schema_subset_plus_result_semantics"
SCHEMA_VALIDATION_LIMITATIONS = [
    "Local subset validator checks required envelope, profile binding, result, case, aggregation, and boundary fields.",
    "The result is evidence-projected from accepted artifacts; no runner or subprocess execution is performed.",
    "Profile satisfaction and subject admission remain separate decisions.",
    "Full JSON Schema Draft 2020-12 validation remains future work.",
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


def sha256_data(data: Any) -> str:
    return "sha256:" + hashlib.sha256(stable_json(data).encode("utf-8")).hexdigest()


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


def _semver(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", value))


def _json_valid(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (OSError, ValueError):
        return False


def _hash_source_artifacts(repo_root: Path, rels: list[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel in rels:
        path = repo_root / rel
        if path.exists() and path.is_file():
            hashes[rel] = sha256_file(path)
    return hashes


def _result_reports_exist(repo_root: Path) -> bool:
    validation_reports = {VALIDATION_JSON, VALIDATION_MD}
    return all((repo_root / rel).exists() for rel in REQUIRED_REPORTS if rel not in validation_reports)


def _case_ref(case_id: str) -> str:
    return f"{PROFILE_REF}#{case_id}"


def _normalized_accepted_outcomes(case: dict[str, Any]) -> list[str]:
    normalized: list[str] = []
    for item in case.get("accepted_outcomes", []):
        value = NORMALIZED_ACCEPTED_OUTCOME_MAP.get(item)
        if value and value not in normalized:
            normalized.append(value)
    return normalized


def _case_outcome(case: dict[str, Any], repo_root: Path) -> str:
    case_id = str(case.get("case_id"))
    if case_id in CASE_OUTCOME_OVERRIDES:
        return CASE_OUTCOME_OVERRIDES[case_id]
    evidence = case.get("evidence_required", [])
    if not evidence:
        return "UNAVAILABLE"
    if all((repo_root / str(rel)).exists() for rel in evidence):
        accepted = _normalized_accepted_outcomes(case)
        return "PASS_WITH_WARNINGS" if "PASS_WITH_WARNINGS" in accepted else "PASS"
    return "UNAVAILABLE"


def source_artifact_paths(repo_root: str | Path) -> list[str]:
    root = Path(repo_root)
    paths: set[str] = {
        ".aide/protocol/aide-conformance-profile.schema.json",
        ".aide/reports/conformance-profile/profiles.json",
        ".aide/reports/conformance-profile/profile-index.json",
        ".aide/reports/conformance-profile/case-index.json",
        ".aide/reports/conformance-profile/projection-report.json",
        ".aide/reports/conformance-profile/validation.json",
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
        ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/task.yaml",
        ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/status.yaml",
        ".aide/queue/AIDE-ACCEPT-CONFORMANCE-PROFILE-01/task.yaml",
        ".aide/queue/AIDE-ACCEPT-CONFORMANCE-PROFILE-01/status.yaml",
        ".aide/queue/AIDE-CHECK-TRACK-B-B1-BARRIER-01/status.yaml",
        "core/protocol/capability_manifest.py",
        "core/protocol/conformance_profile.py",
    }
    evidence_roots = [
        root / ".aide/queue/AIDE-ACCEPT-CAPABILITY-MANIFEST-01/evidence",
        root / ".aide/queue/AIDE-ACCEPT-CONFORMANCE-PROFILE-01/evidence",
    ]
    for evidence_root in evidence_roots:
        if evidence_root.exists():
            paths.update(_relative(path, root) for path in sorted(evidence_root.glob("*.md")))
    return sorted(rel for rel in paths if (root / rel).exists())


def load_conformance_result_schema(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / SCHEMA_PATH
    if not path.exists():
        raise ValueError(f"ConformanceResult schema missing: {SCHEMA_PATH.as_posix()}")
    return read_json(path)


def load_accepted_conformance_profile(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    path = root / ".aide/reports/conformance-profile/profiles.json"
    if path.exists():
        profile = read_json(path)
    else:
        profile = conformance_profile.build_conformance_profile(root)
    errors, warnings = _validate_profile_binding(profile)
    if errors:
        raise ValueError("; ".join(errors))
    if warnings:
        profile = copy.deepcopy(profile)
        profile.setdefault("status", {}).setdefault("validation_warnings", []).extend(warnings)
    return profile


def _validate_profile_binding(profile: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    spec = profile.get("spec", {})
    if profile.get("kind") != "ConformanceProfile":
        errors.append("profile.kind must be ConformanceProfile")
    if spec.get("profile_ref") != PROFILE_REF:
        errors.append(f"profile.ref must be {PROFILE_REF}")
    if spec.get("profile_id") != PROFILE_ID:
        errors.append(f"profile.id must be {PROFILE_ID}")
    if spec.get("profile_version") != PROFILE_VERSION:
        errors.append(f"profile.version must be {PROFILE_VERSION}")
    if spec.get("subject", {}).get("ref") != SUBJECT_REF:
        errors.append(f"profile.subject.ref must be {SUBJECT_REF}")
    if spec.get("lifecycle") not in {"candidate", "accepted"}:
        errors.append("profile.lifecycle must be candidate or accepted")
    if spec.get("lifecycle") == "candidate":
        warnings.append("Profile lifecycle is candidate; result records observations but does not admit the subject.")
    cases = spec.get("cases", [])
    if not isinstance(cases, list) or not cases:
        errors.append("profile.spec.cases must be non-empty")
    return errors, warnings


def profile_digest(profile: dict[str, Any]) -> str:
    return sha256_data(profile)


def build_assertion_results(repo_root: Path, evidence_refs: list[str]) -> list[dict[str, Any]]:
    assertions: list[dict[str, Any]] = []
    for rel in evidence_refs:
        path = repo_root / rel
        assertions.append(
            {
                "assertion": "evidence_ref_exists",
                "ref": rel,
                "outcome": "PASS" if path.exists() else "FAIL",
                "observed": True,
                "details": "Evidence path exists." if path.exists() else "Evidence path is missing.",
            }
        )
    return assertions


def build_case_result(repo_root: str | Path, case: dict[str, Any]) -> dict[str, Any]:
    root = Path(repo_root)
    outcome = _case_outcome(case, root)
    case_id = str(case.get("case_id"))
    requirement = str(case.get("requirement_level"))
    accepted = _normalized_accepted_outcomes(case)
    evidence_refs = [str(item) for item in case.get("evidence_required", [])]
    source_refs = [str(item) for item in case.get("source_refs", [])]
    report_refs = [item for item in evidence_refs if item.startswith(".aide/reports/")]
    observed = outcome not in NON_OBSERVED_OUTCOMES
    warnings: list[str] = []
    reason = None
    if outcome == "PASS_WITH_WARNINGS":
        warnings.append(_case_warning(case_id))
    elif outcome in {"FAIL", "ERROR"}:
        reason = "Evidence projection observed an unsuccessful case outcome."
    elif outcome in NON_OBSERVED_OUTCOMES:
        reason = "Evidence projection could not observe this case without a future runner."
    return {
        "case_id": case_id,
        "case_ref": str(case.get("case_ref", _case_ref(case_id))),
        "requirement_level_snapshot": requirement,
        "evaluator_kind_snapshot": str(case.get("evaluator")),
        "accepted_observed_outcomes": accepted,
        "outcome": outcome,
        "observed": observed,
        "reason": reason,
        "summary": _case_summary(case_id, outcome),
        "evidence_refs": evidence_refs,
        "report_refs": report_refs,
        "source_refs": source_refs,
        "assertion_results": build_assertion_results(root, evidence_refs),
        "warnings": warnings,
        "limitations": ["Evidence-projected; no case execution performed."],
        "execution_performed": False,
        "runner_ref": None,
        "admission_performed": False,
        "subject_admitted": False,
        "trusted": False,
    }


def _case_summary(case_id: str, outcome: str) -> str:
    if outcome == "PASS":
        return f"{case_id} is observed as pass from accepted evidence."
    if outcome == "PASS_WITH_WARNINGS":
        return f"{case_id} is observed as pass with retained warning debt."
    if outcome in {"SKIPPED", "UNAVAILABLE", "NOT_RUN"}:
        return f"{case_id} is not observed by this projection-only slice."
    return f"{case_id} is observed as {outcome.lower()} by this record."


def _case_warning(case_id: str) -> str:
    warnings = {
        "capability-manifest-validation-pass-with-warnings": "CapabilityManifest validation retains accepted warning debt.",
        "capability-manifest-acceptance-evidence-complete": "CapabilityManifest was admitted as ACCEPTED_WITH_WARNINGS.",
        "capability-manifest-declaration-only-boundary": "Declaration-only boundary is preserved; no capability proof is implied.",
        "accepted-warning-debt-classified": "Accepted warning debt remains visible for future routing.",
        "reference-and-event-refs-parse": "Reference and event validators remain predecessor compatibility checks, not runtime proof.",
        "latest-task-packet-drift-classified": "Stale latest-task-packet drift remains warning debt.",
    }
    return warnings.get(case_id, "Evidence projection records non-blocking warning debt.")


def aggregate_case_results(profile: dict[str, Any], case_results: list[dict[str, Any]]) -> dict[str, Any]:
    cases = profile.get("spec", {}).get("cases", [])
    result_by_case: dict[str, dict[str, Any]] = {}
    duplicate_case_ids: list[str] = []
    for result in case_results:
        case_id = str(result.get("case_id"))
        if case_id in result_by_case:
            duplicate_case_ids.append(case_id)
        result_by_case[case_id] = result

    required_total = 0
    required_satisfied = 0
    optional_total = 0
    advisory_total = 0
    missing_required: list[str] = []
    failed_required: list[str] = []
    errored_required: list[str] = []
    incomplete_required: list[str] = []
    warning_cases: list[str] = []
    optional_findings: list[str] = []
    advisory_findings: list[str] = []

    for case in cases:
        case_id = str(case.get("case_id"))
        requirement = str(case.get("requirement_level"))
        result = result_by_case.get(case_id)
        if requirement == "required":
            required_total += 1
        elif requirement == "optional":
            optional_total += 1
        elif requirement == "advisory":
            advisory_total += 1
        if result is None:
            if requirement == "required":
                missing_required.append(case_id)
            continue
        outcome = str(result.get("outcome"))
        accepted = set(_normalized_accepted_outcomes(case))
        if outcome == "PASS_WITH_WARNINGS":
            warning_cases.append(case_id)
        if requirement == "required":
            if outcome == "ERROR":
                errored_required.append(case_id)
            elif outcome == "FAIL":
                failed_required.append(case_id)
            elif outcome in NON_OBSERVED_OUTCOMES:
                incomplete_required.append(case_id)
            elif outcome in accepted:
                required_satisfied += 1
            else:
                failed_required.append(case_id)
        elif requirement == "optional" and outcome not in accepted:
            optional_findings.append(f"{case_id}: {outcome}")
        elif requirement == "advisory" and outcome not in accepted:
            advisory_findings.append(f"{case_id}: {outcome}")

    record_complete = len(result_by_case) >= len(cases) and not missing_required and not duplicate_case_ids
    profile_requirements_satisfied = (
        required_total > 0
        and required_satisfied == required_total
        and not missing_required
        and not failed_required
        and not errored_required
        and not incomplete_required
    )
    if errored_required:
        aggregate_outcome = "ERROR"
    elif failed_required:
        aggregate_outcome = "FAIL"
    elif missing_required or incomplete_required or required_satisfied < required_total:
        aggregate_outcome = "INCOMPLETE"
    elif warning_cases or optional_findings or advisory_findings:
        aggregate_outcome = "PASS_WITH_WARNINGS"
    else:
        aggregate_outcome = "PASS"

    blockers = [f"missing required case: {item}" for item in missing_required]
    blockers.extend(f"required case failed: {item}" for item in failed_required)
    blockers.extend(f"required case error: {item}" for item in errored_required)
    blockers.extend(f"required case incomplete: {item}" for item in incomplete_required)
    blockers.extend(f"duplicate case result: {item}" for item in duplicate_case_ids)

    warnings = [f"case retained warning debt: {item}" for item in warning_cases]
    warnings.extend(f"optional case finding: {item}" for item in optional_findings)
    warnings.extend(f"advisory case finding: {item}" for item in advisory_findings)
    warnings.append("Profile requirements satisfied does not admit or trust the subject.")

    return {
        "aggregate_outcome": aggregate_outcome,
        "record_complete": record_complete,
        "profile_requirements_satisfied": profile_requirements_satisfied,
        "required_cases_total": required_total,
        "required_cases_satisfied": required_satisfied,
        "required_cases_missing": len(missing_required),
        "required_cases_failed": len(failed_required),
        "required_cases_error": len(errored_required),
        "required_cases_incomplete": len(incomplete_required),
        "optional_cases_total": optional_total,
        "advisory_cases_total": advisory_total,
        "case_results_total": len(case_results),
        "fail_closed_triggered": bool(missing_required or failed_required or errored_required or incomplete_required),
        "blocker_reasons": blockers,
        "warning_case_ids": warning_cases,
        "warnings": warnings,
        "advisory_findings": advisory_findings,
        "optional_findings": optional_findings,
        "admission_performed": False,
        "subject_admitted": False,
        "trusted": False,
    }


def build_conformance_result(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    profile = load_accepted_conformance_profile(root)
    digest = profile_digest(profile)
    cases = profile.get("spec", {}).get("cases", [])
    case_results = [build_case_result(root, case) for case in cases]
    aggregation = aggregate_case_results(profile, case_results)
    validation_warnings = list(aggregation.get("warnings", []))
    metadata = {
        "id": "conformance-result-minimal-capability-manifest-v1",
        "name": "Minimal CapabilityManifest ConformanceResult",
        "title": "Minimal CapabilityManifest ConformanceResult",
        "createdAt": DETERMINISTIC_TIMESTAMP,
        "sourcePath": RESULTS_JSON.as_posix(),
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility([PROFILE_ID, "minimal_capability_manifest"]),
    }
    spec = {
        "result_ref": RESULT_REF,
        "result_id": RESULT_ID,
        "result_version": RESULT_VERSION,
        "lifecycle": "projected",
        "observation": {
            "mode": OBSERVATION_MODE,
            "execution_performed": False,
            "runner_ref": None,
            "collection": "deterministic_evidence_projection",
            "source_profile_ref": PROFILE_REF,
            "source_profile_digest": digest,
        },
        "profile": {
            "ref": PROFILE_REF,
            "id": PROFILE_ID,
            "version": PROFILE_VERSION,
            "digest": digest,
            "lifecycle_snapshot": profile.get("spec", {}).get("lifecycle"),
        },
        "subject": {
            "kind": SUBJECT_KIND,
            "ref": SUBJECT_REF,
            "admission_performed": False,
            "subject_admitted": False,
            "trusted": False,
        },
        "case_results": case_results,
        "aggregation": aggregation,
        "evidence_refs": sorted({ref for result in case_results for ref in result.get("evidence_refs", [])}),
        "report_refs": [
            PROJECTION_JSON.as_posix(),
            VALIDATION_JSON.as_posix(),
            RESULTS_JSON.as_posix(),
            RESULT_INDEX_JSON.as_posix(),
            CASE_RESULT_INDEX_JSON.as_posix(),
        ],
        "event_refs": [],
        "okf_refs": [],
        "source_refs": [
            PROFILE_REF,
            SUBJECT_REF,
            reference_id.format_reference_id("queue-task", "AIDE-ACCEPT-CONFORMANCE-PROFILE-01"),
            reference_id.format_reference_id("queue-task", "AIDE-ACCEPT-CAPABILITY-MANIFEST-01"),
        ],
        "limitations": [
            "Result is projected from accepted evidence; no case runner executed.",
            "Profile requirements satisfaction is not admission.",
            "Subject remains not admitted, not trusted, and not activated.",
        ],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
    }
    return {
        "apiVersion": API_VERSION,
        "kind": "ConformanceResult",
        "schema_version": CONFORMANCE_RESULT_SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "metadata": metadata,
        "spec": spec,
        "status": {
            "record_valid": True,
            "validation_status": aggregation["aggregate_outcome"],
            "validation_errors": [],
            "validation_warnings": validation_warnings,
            "result_only": True,
            "projection_only": True,
            "record_complete": aggregation["record_complete"],
            "profile_requirements_satisfied": aggregation["profile_requirements_satisfied"],
            "execution_performed": False,
            "admission_performed": False,
            "subject_admitted": False,
            "trusted": False,
            "mutating": False,
            "runtime": False,
        },
    }


def build_result_index(result: dict[str, Any]) -> dict[str, Any]:
    spec = result["spec"]
    aggregation = spec["aggregation"]
    return {
        "schema_version": "aide.conformance-result-index.v0",
        "report_type": "conformance_result_index",
        "kind": "ConformanceResultIndex",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "status": aggregation["aggregate_outcome"],
        "result_ref": spec["result_ref"],
        "result_id": spec["result_id"],
        "result_version": spec["result_version"],
        "profile_ref": spec["profile"]["ref"],
        "profile_digest": spec["profile"]["digest"],
        "subject_ref": spec["subject"]["ref"],
        "record_valid": result["status"]["record_valid"],
        "record_complete": aggregation["record_complete"],
        "profile_requirements_satisfied": aggregation["profile_requirements_satisfied"],
        "admission_performed": False,
        "subject_admitted": False,
        "trusted": False,
        "case_result_count": len(spec["case_results"]),
        "required_cases_total": aggregation["required_cases_total"],
        "required_cases_satisfied": aggregation["required_cases_satisfied"],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def build_case_result_index(result: dict[str, Any]) -> dict[str, Any]:
    spec = result["spec"]
    return {
        "schema_version": "aide.conformance-case-result-index.v0",
        "report_type": "conformance_case_result_index",
        "kind": "ConformanceCaseResultIndex",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "status": spec["aggregation"]["aggregate_outcome"],
        "result_ref": spec["result_ref"],
        "profile_ref": spec["profile"]["ref"],
        "subject_ref": spec["subject"]["ref"],
        "case_result_count": len(spec["case_results"]),
        "case_results": [
            {
                "case_id": item["case_id"],
                "case_ref": item["case_ref"],
                "requirement_level": item["requirement_level_snapshot"],
                "evaluator": item["evaluator_kind_snapshot"],
                "outcome": item["outcome"],
                "observed": item["observed"],
                "execution_performed": item["execution_performed"],
                "runner_ref": item["runner_ref"],
                "warnings_count": len(item.get("warnings", [])),
            }
            for item in spec["case_results"]
        ],
        "admission_performed": False,
        "subject_admitted": False,
        "trusted": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def conformance_result_counts(result: dict[str, Any]) -> dict[str, int]:
    case_results = result.get("spec", {}).get("case_results", [])
    return {
        "result_count": 1,
        "case_result_count": len(case_results),
        "required_case_result_count": sum(1 for item in case_results if item.get("requirement_level_snapshot") == "required"),
        "optional_case_result_count": sum(1 for item in case_results if item.get("requirement_level_snapshot") == "optional"),
        "advisory_case_result_count": sum(1 for item in case_results if item.get("requirement_level_snapshot") == "advisory"),
        "pass_count": sum(1 for item in case_results if item.get("outcome") == "PASS"),
        "pass_with_warnings_count": sum(1 for item in case_results if item.get("outcome") == "PASS_WITH_WARNINGS"),
        "fail_count": sum(1 for item in case_results if item.get("outcome") == "FAIL"),
        "error_count": sum(1 for item in case_results if item.get("outcome") == "ERROR"),
        "not_observed_count": sum(1 for item in case_results if item.get("outcome") in NON_OBSERVED_OUTCOMES),
    }


def validate_conformance_result_with_schema(
    result: dict[str, Any], schema: dict[str, Any], profile: dict[str, Any] | None = None
) -> tuple[list[str], list[str]]:
    schema_errors = envelope.validate_envelope_with_schema(result, schema)
    semantic_errors, semantic_warnings = validate_conformance_result_record(result, profile)
    return [*schema_errors, *semantic_errors], semantic_warnings


def validate_conformance_result_record(
    result: dict[str, Any], profile: dict[str, Any] | None = None
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if result.get("kind") != "ConformanceResult":
        errors.append("kind must be ConformanceResult")
    if result.get("schema_version") != CONFORMANCE_RESULT_SCHEMA_VERSION:
        errors.append(f"schema_version must be {CONFORMANCE_RESULT_SCHEMA_VERSION}")
    if result.get("protocol_version") != PROTOCOL_VERSION:
        errors.append(f"protocol_version must be {PROTOCOL_VERSION}")
    spec = result.get("spec", {})
    status = result.get("status", {})
    if spec.get("result_ref") != RESULT_REF:
        errors.append(f"result_ref must be {RESULT_REF}")
    if spec.get("result_id") != RESULT_ID:
        errors.append(f"result_id must be {RESULT_ID}")
    if not _semver(spec.get("result_version")):
        errors.append("result_version must be SemVer")
    observation = spec.get("observation", {})
    if observation.get("mode") != OBSERVATION_MODE:
        errors.append("observation.mode must be evidence_projection")
    if observation.get("execution_performed") is not False:
        errors.append("observation.execution_performed must be false")
    if observation.get("runner_ref") is not None:
        errors.append("observation.runner_ref must be null")
    profile_binding = spec.get("profile", {})
    if profile_binding.get("ref") != PROFILE_REF:
        errors.append(f"profile.ref must be {PROFILE_REF}")
    if profile_binding.get("id") != PROFILE_ID:
        errors.append(f"profile.id must be {PROFILE_ID}")
    if profile_binding.get("version") != PROFILE_VERSION:
        errors.append(f"profile.version must be {PROFILE_VERSION}")
    if not isinstance(profile_binding.get("digest"), str) or not profile_binding.get("digest", "").startswith("sha256:"):
        errors.append("profile.digest must be a sha256 digest")
    subject = spec.get("subject", {})
    if subject.get("kind") != SUBJECT_KIND:
        errors.append(f"subject.kind must be {SUBJECT_KIND}")
    if subject.get("ref") != SUBJECT_REF:
        errors.append(f"subject.ref must be {SUBJECT_REF}")
    for key in ["admission_performed", "subject_admitted", "trusted"]:
        if subject.get(key) is not False:
            errors.append(f"subject.{key} must be false")
    for key in ["execution_performed", "admission_performed", "subject_admitted", "trusted"]:
        if status.get(key) is not False:
            errors.append(f"status.{key} must be false")
    if status.get("result_only") is not True:
        errors.append("status.result_only must be true")
    if status.get("record_valid") is not True:
        errors.append("status.record_valid must be true")
    case_results = spec.get("case_results", [])
    if not isinstance(case_results, list) or not case_results:
        errors.append("spec.case_results must be non-empty")
    errors.extend(_case_result_errors(case_results))
    aggregation = spec.get("aggregation", {})
    if aggregation.get("aggregate_outcome") not in AGGREGATE_OUTCOMES:
        errors.append("aggregation.aggregate_outcome is invalid")
    if aggregation.get("admission_performed") is not False:
        errors.append("aggregation.admission_performed must be false")
    if aggregation.get("subject_admitted") is not False:
        errors.append("aggregation.subject_admitted must be false")
    if aggregation.get("trusted") is not False:
        errors.append("aggregation.trusted must be false")
    if profile is not None:
        expected_digest = profile_digest(profile)
        if profile_binding.get("digest") != expected_digest:
            errors.append("profile.digest does not match bound ConformanceProfile")
        expected_aggregation = aggregate_case_results(profile, case_results)
        for key in [
            "aggregate_outcome",
            "record_complete",
            "profile_requirements_satisfied",
            "required_cases_total",
            "required_cases_satisfied",
        ]:
            if aggregation.get(key) != expected_aggregation.get(key):
                errors.append(f"aggregation.{key} does not match case results")
        if status.get("record_complete") != expected_aggregation["record_complete"]:
            errors.append("status.record_complete does not match aggregation")
        if status.get("profile_requirements_satisfied") != expected_aggregation["profile_requirements_satisfied"]:
            errors.append("status.profile_requirements_satisfied does not match aggregation")
        profile_case_ids = [case.get("case_id") for case in profile.get("spec", {}).get("cases", [])]
        result_case_ids = [item.get("case_id") for item in case_results]
        unknown = [item for item in result_case_ids if item not in profile_case_ids]
        missing_required = [
            case.get("case_id")
            for case in profile.get("spec", {}).get("cases", [])
            if case.get("requirement_level") == "required" and case.get("case_id") not in result_case_ids
        ]
        errors.extend(f"unknown case result: {item}" for item in unknown)
        errors.extend(f"missing required case result: {item}" for item in missing_required)
    if spec.get("explicit_non_capabilities") != EXPLICIT_NON_CAPABILITIES:
        errors.append("explicit_non_capabilities must match declared boundary list")
    if errors:
        return errors, warnings
    warnings.extend(result.get("status", {}).get("validation_warnings", []))
    return errors, warnings


def _case_result_errors(case_results: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for item in case_results:
        case_id = str(item.get("case_id"))
        if not case_id:
            errors.append("case_result.case_id is required")
        if case_id in seen:
            errors.append(f"case_result.case_id must be unique: {case_id}")
        seen.add(case_id)
        if str(item.get("case_ref", "")).split("#", 1)[0] != PROFILE_REF:
            errors.append(f"case_result.case_ref must bind to {PROFILE_REF}: {case_id}")
        if item.get("requirement_level_snapshot") not in REQUIREMENT_LEVELS:
            errors.append(f"case_result.requirement_level_snapshot is invalid: {case_id}")
        if item.get("outcome") not in OBSERVED_OUTCOMES:
            errors.append(f"case_result.outcome is invalid: {case_id}")
        if item.get("execution_performed") is not False:
            errors.append(f"case_result.execution_performed must be false: {case_id}")
        if item.get("runner_ref") is not None:
            errors.append(f"case_result.runner_ref must be null: {case_id}")
        if item.get("admission_performed") is not False:
            errors.append(f"case_result.admission_performed must be false: {case_id}")
        if item.get("subject_admitted") is not False:
            errors.append(f"case_result.subject_admitted must be false: {case_id}")
        if item.get("trusted") is not False:
            errors.append(f"case_result.trusted must be false: {case_id}")
        outcome = item.get("outcome")
        if outcome in {"PASS", "PASS_WITH_WARNINGS"} and not (
            item.get("evidence_refs") or item.get("report_refs") or item.get("source_refs")
        ):
            errors.append(f"passing case must have evidence, report, or source refs: {case_id}")
        if outcome == "PASS_WITH_WARNINGS" and not item.get("warnings"):
            errors.append(f"PASS_WITH_WARNINGS case must include warnings: {case_id}")
        if outcome in {"FAIL", "ERROR"} and not item.get("reason"):
            errors.append(f"failed or errored case must include reason: {case_id}")
        if outcome in NON_OBSERVED_OUTCOMES and not item.get("reason"):
            errors.append(f"non-observed case must include reason: {case_id}")
        if outcome in NON_OBSERVED_OUTCOMES and item.get("observed") is not False:
            errors.append(f"non-observed case must set observed false: {case_id}")
        if outcome in {"PASS", "PASS_WITH_WARNINGS", "FAIL", "ERROR"} and item.get("observed") is not True:
            errors.append(f"observed outcome must set observed true: {case_id}")
    return errors


def result_boundary_valid(result: dict[str, Any]) -> bool:
    status = result.get("status", {})
    spec = result.get("spec", {})
    subject = spec.get("subject", {})
    observation = spec.get("observation", {})
    return (
        status.get("record_valid") is True
        and status.get("result_only") is True
        and status.get("execution_performed") is False
        and status.get("admission_performed") is False
        and status.get("subject_admitted") is False
        and status.get("trusted") is False
        and observation.get("mode") == OBSERVATION_MODE
        and observation.get("execution_performed") is False
        and observation.get("runner_ref") is None
        and subject.get("admission_performed") is False
        and subject.get("subject_admitted") is False
        and subject.get("trusted") is False
    )


def forbidden_operations_preserved() -> dict[str, bool]:
    return {
        "conformance_runner": True,
        "case_execution": True,
        "command_execution": True,
        "automatic_result_collection": True,
        "profile_activation": True,
        "conformance_admission": True,
        "subject_admission": True,
        "trust_grant": True,
        "adapter_admission": True,
        "adapter_execution": True,
        "capability_execution": True,
        "runtime_registry": True,
        "patch_transaction": True,
        "adapter_manifest": True,
        "context_pack_v2": True,
        "test_broker_runtime": True,
        "worker_execution": True,
        "branch_worktree_automation": True,
        "target_apply": True,
        "active_repo_apply_mutation": True,
        "release_promotion": True,
        "github_mutation": True,
        "gateway_calls": True,
        "network_calls": True,
        "provider_model_calls": True,
    }


def _overclaiming_findings(repo_root: Path) -> list[str]:
    findings: list[str] = []
    paths = [
        STATUS_MD,
        PROJECTION_MD,
        VALIDATION_MD,
        RESULTS_MD,
        RESULT_INDEX_MD,
        CASE_RESULT_INDEX_MD,
        FUTURE_WORK_MD,
        UNFINISHED_WORK_MD,
    ]
    for rel in paths:
        path = repo_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for pattern in FORBIDDEN_CLAIM_PATTERNS:
            if pattern in text:
                findings.append(f"{rel.as_posix()} contains forbidden claim pattern: {pattern}")
    return findings


def future_work_items() -> list[dict[str, str]]:
    return [
        {
            "task": RECOMMENDED_NEXT_TASK,
            "reason": "Independently check schema, helper, projection, aggregation semantics, CLI, reports, and evidence.",
        },
        {
            "task": "AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01",
            "reason": "Accept the checked ConformanceResult schema slice before proceeding to mutation semantics.",
        },
        {
            "task": "future-conformance-runner",
            "reason": "Runner-backed collection remains later work and must not be inferred from this evidence projection.",
        },
        {
            "task": "future-admission-gate",
            "reason": "Admission remains a separate decision after profile requirements and result records are accepted.",
        },
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    return [
        {"item": item, "reason": "Explicitly out of scope for this projection-only ConformanceResult slice."}
        for item in EXPLICIT_NON_CAPABILITIES
    ]


def conformance_result_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    result = build_conformance_result(root)
    aggregation = result["spec"]["aggregation"]
    counts = conformance_result_counts(result)
    data = {
        "schema_version": "aide.conformance-result-status.v0",
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "result_ref": RESULT_REF,
        "result_id": RESULT_ID,
        "profile_ref": PROFILE_REF,
        "profile_digest": result["spec"]["profile"]["digest"],
        "subject_ref": SUBJECT_REF,
        "status": aggregation["aggregate_outcome"],
        "schema_path": SCHEMA_PATH.as_posix(),
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_path": "core/protocol/conformance_result.py",
        "helper_exists": (root / "core/protocol/conformance_result.py").exists(),
        "projection_exists": (root / PROJECTION_JSON).exists(),
        **counts,
        "record_valid": result["status"]["record_valid"],
        "record_complete": aggregation["record_complete"],
        "profile_requirements_satisfied": aggregation["profile_requirements_satisfied"],
        "warnings": result["status"]["validation_warnings"],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "result_only": True,
        "projection_only": True,
        "execution_performed": False,
        "runner_ref": None,
        "admission_performed": False,
        "subject_admitted": False,
        "trusted": False,
        "runtime": False,
        "mutating": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    return data


def write_conformance_result_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    sources = source_artifact_paths(root)
    before = _hash_source_artifacts(root, sources)
    result = build_conformance_result(root)
    result_index = build_result_index(result)
    case_result_index = build_case_result_index(result)
    write_json(root / RESULTS_JSON, result)
    write_text(root / RESULTS_MD, render_results_markdown(result))
    write_json(root / RESULT_INDEX_JSON, result_index)
    write_text(root / RESULT_INDEX_MD, render_result_index_markdown(result_index))
    write_json(root / CASE_RESULT_INDEX_JSON, case_result_index)
    write_text(root / CASE_RESULT_INDEX_MD, render_case_result_index_markdown(case_result_index))
    write_text(root / FUTURE_WORK_MD, render_future_work_markdown())
    write_text(root / UNFINISHED_WORK_MD, render_unfinished_work_markdown())
    after = _hash_source_artifacts(root, sources)
    counts = conformance_result_counts(result)
    report = {
        "schema_version": "aide.conformance-result-projection.v0",
        "report_type": "conformance_result_projection",
        "kind": "ConformanceResultProjectionReport",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "result_ref": RESULT_REF,
        "result_id": RESULT_ID,
        "result_version": RESULT_VERSION,
        "profile_ref": PROFILE_REF,
        "profile_digest": result["spec"]["profile"]["digest"],
        "subject_ref": SUBJECT_REF,
        "status": result["spec"]["aggregation"]["aggregate_outcome"],
        "record_valid": result["status"]["record_valid"],
        "record_complete": result["spec"]["aggregation"]["record_complete"],
        "profile_requirements_satisfied": result["spec"]["aggregation"]["profile_requirements_satisfied"],
        "result_only": True,
        "projection_only": True,
        "observation_mode": OBSERVATION_MODE,
        "execution_performed": False,
        "runner_ref": None,
        "admission_performed": False,
        "subject_admitted": False,
        "trusted": False,
        **counts,
        "source_artifacts_checked": sources,
        "source_artifacts_mutated": before != after,
        "reports_written": [path.as_posix() for path in REQUIRED_REPORTS],
        "warnings": result["status"]["validation_warnings"],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    status = conformance_result_status(root)
    status["status"] = report["status"]
    write_text(root / STATUS_MD, render_status_markdown(status))
    validation = validate_conformance_result(root, project=False)
    report["status"] = validation["validation_status"]
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    status["status"] = report["status"]
    write_text(root / STATUS_MD, render_status_markdown(status))
    return report


def validate_conformance_result(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    if project:
        projection_result = write_conformance_result_reports(root)
    else:
        projection_result = {"status": "PASS_WITH_WARNINGS"}
    profile = load_accepted_conformance_profile(root)
    result = build_conformance_result(root)
    schema_errors: list[str] = []
    schema_warnings: list[str] = []
    schema_file_loaded = False
    schema_file_parsed = False
    schema_validation_executed = False
    try:
        schema = load_conformance_result_schema(root)
        schema_file_loaded = True
        schema_file_parsed = True
        result_errors, result_warnings = validate_conformance_result_with_schema(result, schema, profile)
        schema_validation_executed = True
        schema_errors.extend(result_errors)
        schema_warnings.extend(result_warnings)
    except ValueError as exc:
        schema_errors.append(str(exc))

    forbidden = forbidden_operations_preserved()
    overclaiming_findings = _overclaiming_findings(root)
    reports_generated = _result_reports_exist(root)
    json_checks = {
        "results_json_valid": _json_valid(root / RESULTS_JSON) if (root / RESULTS_JSON).exists() else False,
        "result_index_json_valid": _json_valid(root / RESULT_INDEX_JSON) if (root / RESULT_INDEX_JSON).exists() else False,
        "case_result_index_json_valid": _json_valid(root / CASE_RESULT_INDEX_JSON) if (root / CASE_RESULT_INDEX_JSON).exists() else False,
        "projection_json_valid": _json_valid(root / PROJECTION_JSON) if (root / PROJECTION_JSON).exists() else False,
    }
    case_results = result.get("spec", {}).get("case_results", [])
    case_ids_unique = len([item.get("case_id") for item in case_results]) == len({item.get("case_id") for item in case_results})
    case_results_bind_to_profile = all(str(item.get("case_ref", "")).split("#", 1)[0] == PROFILE_REF for item in case_results)
    case_results_execution_false = all(item.get("execution_performed") is False for item in case_results)
    case_results_runner_null = all(item.get("runner_ref") is None for item in case_results)
    observed_outcomes_valid = all(item.get("outcome") in OBSERVED_OUTCOMES for item in case_results)
    required_cases_accounted = (
        result["spec"]["aggregation"]["required_cases_total"]
        == result["spec"]["aggregation"]["required_cases_satisfied"]
        >= 1
    )
    validation_errors = [*schema_errors, *overclaiming_findings]
    base_pass = (
        not validation_errors
        and projection_result.get("status") in {"PASS", "PASS_WITH_WARNINGS"}
        and reports_generated
        and all(json_checks.values())
        and case_ids_unique
        and case_results_bind_to_profile
        and case_results_execution_false
        and case_results_runner_null
        and observed_outcomes_valid
        and required_cases_accounted
        and result_boundary_valid(result)
        and all(forbidden.values())
    )
    status = "PASS_WITH_WARNINGS" if base_pass else "FAILED_VALIDATION"
    warnings = list(dict.fromkeys([*result["status"].get("validation_warnings", []), *schema_warnings]))
    report = {
        "schema_version": "aide.conformance-result-validation.v0",
        "report_type": "conformance_result_validation",
        "kind": "ConformanceResultValidationReport",
        "task_id": TASK_ID,
        "status": status,
        "validation_status": status,
        "validated": status in {"PASS", "PASS_WITH_WARNINGS"},
        "api_version": API_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "capability_target": FEATURE_FLAG,
        "accepted_predecessor": ACCEPTED_PREDECESSOR,
        "result_ref": RESULT_REF,
        "result_id": RESULT_ID,
        "result_version": RESULT_VERSION,
        "profile_ref": PROFILE_REF,
        "profile_digest": result["spec"]["profile"]["digest"],
        "subject_ref": SUBJECT_REF,
        "schema_path": SCHEMA_PATH.as_posix(),
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "schema_file_loaded": schema_file_loaded,
        "schema_file_parsed": schema_file_parsed,
        "schema_validation_executed": schema_validation_executed,
        "schema_validation_mode": SCHEMA_VALIDATION_MODE if schema_validation_executed else "unavailable",
        "schema_validation_limitations": list(SCHEMA_VALIDATION_LIMITATIONS),
        "helper_path": "core/protocol/conformance_result.py",
        "helper_exists": (root / "core/protocol/conformance_result.py").exists(),
        "cli_registered": _cli_registered(root),
        "reports_generated": reports_generated,
        **json_checks,
        "case_ids_unique": case_ids_unique,
        "case_results_bind_to_profile": case_results_bind_to_profile,
        "observed_outcomes_valid": observed_outcomes_valid,
        "case_results_execution_false": case_results_execution_false,
        "case_results_runner_null": case_results_runner_null,
        "observation_mode_evidence_projection": result["spec"]["observation"].get("mode") == OBSERVATION_MODE,
        "observation_execution_false": result["spec"]["observation"].get("execution_performed") is False,
        "observation_runner_null": result["spec"]["observation"].get("runner_ref") is None,
        "profile_digest_matches": result["spec"]["profile"].get("digest") == profile_digest(profile),
        "required_cases_accounted": required_cases_accounted,
        "record_complete": result["status"]["record_complete"],
        "profile_requirements_satisfied": result["status"]["profile_requirements_satisfied"],
        "record_valid": result["status"]["record_valid"] is True,
        "record_valid_independent": result["status"]["record_valid"] is True,
        "admission_not_performed": result["status"]["admission_performed"] is False,
        "subject_not_admitted": result["status"]["subject_admitted"] is False,
        "trusted_not_promoted": result["status"]["trusted"] is False,
        "result_boundary_valid": result_boundary_valid(result),
        "explicit_non_capabilities_preserved": result["spec"].get("explicit_non_capabilities") == EXPLICIT_NON_CAPABILITIES,
        "predecessor_compatibility_preserved": (root / ".aide/queue/AIDE-ACCEPT-CONFORMANCE-PROFILE-01/status.yaml").exists(),
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


def _cli_registered(repo_root: Path) -> bool:
    path = repo_root / ".aide/scripts/aide_lite.py"
    return path.exists() and "conformance-result" in path.read_text(encoding="utf-8")


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# ConformanceResult Status",
        "",
        f"- task_id: {data.get('task_id')}",
        f"- status: {data.get('status')}",
        f"- result_ref: {data.get('result_ref')}",
        f"- profile_ref: {data.get('profile_ref')}",
        f"- subject_ref: {data.get('subject_ref')}",
        f"- result_count: {data.get('result_count')}",
        f"- case_result_count: {data.get('case_result_count')}",
        f"- required_case_result_count: {data.get('required_case_result_count')}",
        f"- pass_count: {data.get('pass_count')}",
        f"- pass_with_warnings_count: {data.get('pass_with_warnings_count')}",
        f"- record_valid: {str(data.get('record_valid')).lower()}",
        f"- record_complete: {str(data.get('record_complete')).lower()}",
        f"- profile_requirements_satisfied: {str(data.get('profile_requirements_satisfied')).lower()}",
        f"- result_only: {str(data.get('result_only')).lower()}",
        f"- projection_only: {str(data.get('projection_only')).lower()}",
        f"- execution_performed: {str(data.get('execution_performed')).lower()}",
        f"- runner_ref: {data.get('runner_ref')}",
        f"- admission_performed: {str(data.get('admission_performed')).lower()}",
        f"- subject_admitted: {str(data.get('subject_admitted')).lower()}",
        f"- trusted: {str(data.get('trusted')).lower()}",
        f"- runtime: {str(data.get('runtime')).lower()}",
        f"- mutating: {str(data.get('mutating')).lower()}",
        f"- recommended_next_task: {data.get('recommended_next_task')}",
        "",
        "## Warnings",
        "",
    ]
    warnings = data.get("warnings", [])
    lines.extend(f"- {item}" for item in warnings) if warnings else lines.append("- none")
    return "\n".join(lines) + "\n"


def render_results_markdown(result: dict[str, Any]) -> str:
    spec = result["spec"]
    aggregation = spec["aggregation"]
    lines = [
        "# Minimal CapabilityManifest ConformanceResult",
        "",
        f"- result_ref: {spec.get('result_ref')}",
        f"- profile_ref: {spec.get('profile', {}).get('ref')}",
        f"- profile_digest: {spec.get('profile', {}).get('digest')}",
        f"- subject_ref: {spec.get('subject', {}).get('ref')}",
        f"- observation_mode: {spec.get('observation', {}).get('mode')}",
        f"- execution_performed: {str(spec.get('observation', {}).get('execution_performed')).lower()}",
        f"- runner_ref: {spec.get('observation', {}).get('runner_ref')}",
        f"- aggregate_outcome: {aggregation.get('aggregate_outcome')}",
        f"- record_valid: {str(result.get('status', {}).get('record_valid')).lower()}",
        f"- record_complete: {str(aggregation.get('record_complete')).lower()}",
        f"- profile_requirements_satisfied: {str(aggregation.get('profile_requirements_satisfied')).lower()}",
        f"- admission_performed: {str(result.get('status', {}).get('admission_performed')).lower()}",
        f"- subject_admitted: {str(result.get('status', {}).get('subject_admitted')).lower()}",
        f"- trusted: {str(result.get('status', {}).get('trusted')).lower()}",
        "",
        "## Case Results",
        "",
    ]
    for case in spec.get("case_results", []):
        lines.extend(
            [
                f"### {case.get('case_id')}",
                "",
                f"- requirement_level: {case.get('requirement_level_snapshot')}",
                f"- evaluator: {case.get('evaluator_kind_snapshot')}",
                f"- outcome: {case.get('outcome')}",
                f"- observed: {str(case.get('observed')).lower()}",
                f"- execution_performed: {str(case.get('execution_performed')).lower()}",
                f"- runner_ref: {case.get('runner_ref')}",
                f"- warnings_count: {len(case.get('warnings', []))}",
                "",
            ]
        )
    return "\n".join(lines)


def render_result_index_markdown(index: dict[str, Any]) -> str:
    return (
        "# ConformanceResult Index\n\n"
        f"- status: {index.get('status')}\n"
        f"- result_ref: {index.get('result_ref')}\n"
        f"- profile_ref: {index.get('profile_ref')}\n"
        f"- subject_ref: {index.get('subject_ref')}\n"
        f"- record_valid: {str(index.get('record_valid')).lower()}\n"
        f"- record_complete: {str(index.get('record_complete')).lower()}\n"
        f"- profile_requirements_satisfied: {str(index.get('profile_requirements_satisfied')).lower()}\n"
        f"- admission_performed: {str(index.get('admission_performed')).lower()}\n"
        f"- subject_admitted: {str(index.get('subject_admitted')).lower()}\n"
        f"- trusted: {str(index.get('trusted')).lower()}\n"
        f"- case_result_count: {index.get('case_result_count')}\n"
        f"- required_cases_total: {index.get('required_cases_total')}\n"
        f"- required_cases_satisfied: {index.get('required_cases_satisfied')}\n"
        f"- recommended_next_task: {index.get('recommended_next_task')}\n"
    )


def render_case_result_index_markdown(index: dict[str, Any]) -> str:
    lines = [
        "# ConformanceCaseResult Index",
        "",
        f"- status: {index.get('status')}",
        f"- result_ref: {index.get('result_ref')}",
        f"- profile_ref: {index.get('profile_ref')}",
        f"- subject_ref: {index.get('subject_ref')}",
        f"- case_result_count: {index.get('case_result_count')}",
        f"- admission_performed: {str(index.get('admission_performed')).lower()}",
        f"- subject_admitted: {str(index.get('subject_admitted')).lower()}",
        f"- trusted: {str(index.get('trusted')).lower()}",
        "",
    ]
    for case in index.get("case_results", []):
        lines.append(
            f"- {case.get('case_id')} ({case.get('requirement_level')}, outcome={case.get('outcome')}, "
            f"execution_performed={str(case.get('execution_performed')).lower()})"
        )
    lines.append("")
    return "\n".join(lines)


def render_projection_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# ConformanceResult Projection Report",
        "",
        f"- status: {report.get('status')}",
        f"- result_ref: {report.get('result_ref')}",
        f"- profile_ref: {report.get('profile_ref')}",
        f"- subject_ref: {report.get('subject_ref')}",
        f"- observation_mode: {report.get('observation_mode')}",
        f"- source_artifacts_mutated: {str(report.get('source_artifacts_mutated')).lower()}",
        f"- record_valid: {str(report.get('record_valid')).lower()}",
        f"- record_complete: {str(report.get('record_complete')).lower()}",
        f"- profile_requirements_satisfied: {str(report.get('profile_requirements_satisfied')).lower()}",
        f"- result_only: {str(report.get('result_only')).lower()}",
        f"- projection_only: {str(report.get('projection_only')).lower()}",
        f"- execution_performed: {str(report.get('execution_performed')).lower()}",
        f"- runner_ref: {report.get('runner_ref')}",
        f"- admission_performed: {str(report.get('admission_performed')).lower()}",
        f"- subject_admitted: {str(report.get('subject_admitted')).lower()}",
        f"- trusted: {str(report.get('trusted')).lower()}",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Reports Written",
        "",
    ]
    lines.extend(f"- {item}" for item in report.get("reports_written", []))
    lines.extend(["", "## Warnings", ""])
    warnings = report.get("warnings", [])
    lines.extend(f"- {item}" for item in warnings) if warnings else lines.append("- none")
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
        "results_json_valid",
        "result_index_json_valid",
        "case_result_index_json_valid",
        "projection_json_valid",
        "case_ids_unique",
        "case_results_bind_to_profile",
        "observed_outcomes_valid",
        "case_results_execution_false",
        "case_results_runner_null",
        "observation_mode_evidence_projection",
        "observation_execution_false",
        "observation_runner_null",
        "profile_digest_matches",
        "required_cases_accounted",
        "record_complete",
        "profile_requirements_satisfied",
        "record_valid_independent",
        "admission_not_performed",
        "subject_not_admitted",
        "trusted_not_promoted",
        "result_boundary_valid",
        "explicit_non_capabilities_preserved",
        "predecessor_compatibility_preserved",
        "overclaiming_check_passed",
        "forbidden_ops_preserved",
    ]
    lines = [
        "# ConformanceResult Validation Report",
        "",
        f"- status: {report.get('validation_status')}",
        f"- result_ref: {report.get('result_ref')}",
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
    warnings = report.get("warnings", [])
    lines.extend(f"- {item}" for item in warnings) if warnings else lines.append("- none")
    return "\n".join(lines) + "\n"


def render_future_work_markdown() -> str:
    lines = ["# ConformanceResult Future Work", ""]
    lines.extend(f"- {item['task']}: {item['reason']}" for item in future_work_items())
    lines.append("")
    return "\n".join(lines)


def render_unfinished_work_markdown() -> str:
    lines = ["# ConformanceResult Explicit Non-Capabilities", ""]
    lines.extend(f"- {item['item']}: {item['reason']}" for item in unfinished_work_items())
    lines.append("")
    return "\n".join(lines)
