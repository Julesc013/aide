from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01"
SOURCE_TASK_ID = "AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01"
CHECKED_CAPABILITY = "trust_and_authorization_contract_v0"
PASS_OUTCOMES = {"PASS", "PASS_WITH_WARNINGS"}

EXPECTED_KINDS = {
    "Principal": ".aide/protocol/aide-principal.schema.json",
    "AdmissionRecord": ".aide/protocol/aide-admission-record.schema.json",
    "PolicyDecision": ".aide/protocol/aide-policy-decision.schema.json",
    "CapabilityGrant": ".aide/protocol/aide-capability-grant.schema.json",
    "DelegationRecord": ".aide/protocol/aide-delegation-record.schema.json",
    "RevocationRecord": ".aide/protocol/aide-revocation-record.schema.json",
    "AuthorizationEvaluation": ".aide/protocol/aide-authorization-evaluation.schema.json",
}

PROJECTION_FILES = {
    "Principal": ".aide/reports/trust-authorization-contract-v0/projections/principal.json",
    "AdmissionRecord": ".aide/reports/trust-authorization-contract-v0/projections/admission-record.json",
    "PolicyDecision": ".aide/reports/trust-authorization-contract-v0/projections/policy-decision.json",
    "CapabilityGrant": ".aide/reports/trust-authorization-contract-v0/projections/capability-grant.json",
    "DelegationRecord": ".aide/reports/trust-authorization-contract-v0/projections/delegation-record.json",
    "RevocationRecord": ".aide/reports/trust-authorization-contract-v0/projections/revocation-record.json",
    "AuthorizationEvaluation": ".aide/reports/trust-authorization-contract-v0/projections/authorization-evaluation.json",
}

REQUIRED_REFUSAL_CODES = [
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

SECRET_VALUE_RE = re.compile(
    r"AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_\-]{35}|gh[pousr]_[0-9A-Za-z_]{36,}|"
    r"xox[baprs]-[0-9A-Za-z-]+|BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY"
)
DRIVE_SEPARATOR = chr(58)
ABSOLUTE_PATH_RE = re.compile(r"\b[A-Za-z]" + DRIVE_SEPARATOR + r"[\\/]|/" + "Users/|/" + "home/")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
AIDE_REF_RE = re.compile(r"^aide://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+$")


def find_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "AGENTS.md").is_file() and (parent / ".aide").is_dir():
            return parent
    raise RuntimeError("repository root not found")


ROOT = find_root()
EVIDENCE_DIR = ROOT / ".aide/queue" / TASK_ID / "evidence"
REPORT_DIR = ROOT / ".aide/reports/trust-authorization-contract-v0-check"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: str) -> Any:
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def collect_refs(value: Any, refs: list[str]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key.endswith("_ref") and item is not None:
                refs.append(item)
            elif key.endswith("_refs") and isinstance(item, list):
                refs.extend(item)
            collect_refs(item, refs)
    elif isinstance(value, list):
        for item in value:
            collect_refs(item, refs)


def outcome(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def assertion(
    assertions: list[dict[str, Any]],
    id_: str,
    category: str,
    description: str,
    ok: bool,
    expected: Any,
    observed: Any,
    evidence_refs: list[str],
) -> None:
    assertions.append(
        {
            "id": id_,
            "category": category,
            "description": description,
            "outcome": outcome(ok),
            "severity": "material" if not ok else "none",
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs,
            "source_finding_id": None,
        }
    )


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    assertions: list[dict[str, Any]] = []
    schemas = {kind: load_json(path) for kind, path in EXPECTED_KINDS.items()}
    projections = {kind: load_json(path) for kind, path in PROJECTION_FILES.items()}
    validation = load_json(".aide/reports/trust-authorization-contract-v0/validation.json")
    projection_report = load_json(".aide/reports/trust-authorization-contract-v0/projection-report.json")

    source_status = (ROOT / ".aide/queue" / SOURCE_TASK_ID / "status.yaml").read_text(encoding="utf-8")
    assertion(
        assertions,
        "baseline.source_task_passed",
        "baseline",
        "Source build task reports PASS_WITH_WARNINGS, missing_evidence 0, and the expected next task.",
        all(
            marker in source_status
            for marker in [
                "result: PASS_WITH_WARNINGS",
                "missing_evidence: 0",
                f"recommended_next_task: {TASK_ID}",
            ]
        ),
        "source status contains PASS_WITH_WARNINGS, missing_evidence 0, and this check as next task",
        "markers present" if "result: PASS_WITH_WARNINGS" in source_status else "markers missing",
        [f".aide/queue/{SOURCE_TASK_ID}/status.yaml"],
    )

    kind_alignment: dict[str, bool] = {}
    for kind, schema in schemas.items():
        projection = projections[kind]
        kind_alignment[kind] = (
            schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
            and schema.get("type") == "object"
            and schema.get("properties", {}).get("kind", {}).get("const") == kind
            and projection.get("kind") == kind
            and projection.get("spec", {}).get("capability_label") == CHECKED_CAPABILITY
            and projection.get("status", {}).get("projection_only") is True
        )
    assertion(
        assertions,
        "schema.projection_alignment",
        "schema",
        "Every schema and projection has matching kind, Draft 2020-12 schema metadata, capability label, and projection-only status.",
        all(kind_alignment.values()),
        {kind: True for kind in EXPECTED_KINDS},
        kind_alignment,
        list(EXPECTED_KINDS.values()) + list(PROJECTION_FILES.values()),
    )

    all_refs: list[str] = []
    for projection in projections.values():
        collect_refs(projection, all_refs)
    bad_refs = sorted({ref for ref in all_refs if not isinstance(ref, str) or not AIDE_REF_RE.match(ref)})
    assertion(
        assertions,
        "refs.stable_aide_refs",
        "references",
        "All projected reference fields use stable aide:// references.",
        not bad_refs and len(all_refs) >= 20,
        "all refs match aide:// and at least 20 refs are observed",
        {"ref_count": len(all_refs), "bad_refs": bad_refs},
        list(PROJECTION_FILES.values()),
    )

    scan_paths = [
        *[ROOT / p for p in EXPECTED_KINDS.values()],
        *[ROOT / p for p in PROJECTION_FILES.values()],
        ROOT / ".aide/reports/trust-authorization-contract-v0/projection-report.json",
        ROOT / ".aide/reports/trust-authorization-contract-v0/validation.json",
        ROOT / "core/protocol/trust_authorization.py",
        ROOT / ".aide/scripts/tests/test_aide_trust_authorization_contract.py",
    ]
    secret_hits: list[str] = []
    absolute_path_hits: list[str] = []
    disallowed_key_hits: list[str] = []
    disallowed_keys = {"password", "token", "api_key", "private_key", "credential_value", "secret_value"}
    for path in scan_paths:
        text = path.read_text(encoding="utf-8")
        if SECRET_VALUE_RE.search(text):
            secret_hits.append(rel(path))
        if ABSOLUTE_PATH_RE.search(text):
            absolute_path_hits.append(rel(path))
        if path.suffix == ".json":
            data = json.loads(text)
            stack = [data]
            while stack:
                item = stack.pop()
                if isinstance(item, dict):
                    for key, value in item.items():
                        if key in disallowed_keys:
                            disallowed_key_hits.append(f"{rel(path)}:{key}")
                        stack.append(value)
                elif isinstance(item, list):
                    stack.extend(item)
    assertion(
        assertions,
        "security.no_embedded_credentials_or_secrets",
        "security",
        "Committed schemas, projections, reports, helper source, and focused tests contain no secret-like values or credential payload keys.",
        not secret_hits and not disallowed_key_hits,
        "no secret-like values and no credential payload keys",
        {"secret_hits": secret_hits, "disallowed_key_hits": disallowed_key_hits},
        [rel(path) for path in scan_paths],
    )
    assertion(
        assertions,
        "security.no_local_absolute_paths",
        "security",
        "Committed trust artifacts contain no local absolute path leakage.",
        not absolute_path_hits,
        "no local absolute path matches",
        {"absolute_path_hits": absolute_path_hits},
        [rel(path) for path in scan_paths],
    )

    admission = projections["AdmissionRecord"]["spec"]
    evaluation = projections["AuthorizationEvaluation"]["spec"]
    required_op = evaluation["requested_operation"]
    digest_ok = (
        SHA256_RE.match(admission.get("implementation_digest", "")) is not None
        and SHA256_RE.match(admission.get("manifest_digest", "")) is not None
        and required_op.get("implementation_digest") == admission.get("implementation_digest")
        and "implementation_digest_mismatch" in validation.get("required_refusal_codes", [])
    )
    assertion(
        assertions,
        "admission.exact_digest_binding",
        "admission",
        "Admission and authorization evaluation bind the same exact implementation digest and include mismatch refusal coverage.",
        digest_ok,
        "sha256 digests present, evaluation digest matches admission digest, mismatch refusal exists",
        {
            "implementation_digest": admission.get("implementation_digest"),
            "manifest_digest": admission.get("manifest_digest"),
            "evaluation_digest": required_op.get("implementation_digest"),
            "mismatch_refusal_present": "implementation_digest_mismatch" in validation.get("required_refusal_codes", []),
        },
        [
            PROJECTION_FILES["AdmissionRecord"],
            PROJECTION_FILES["AuthorizationEvaluation"],
            ".aide/reports/trust-authorization-contract-v0/validation.json",
        ],
    )

    policy = projections["PolicyDecision"]["spec"]
    grant = projections["CapabilityGrant"]["spec"]
    separation_ok = (
        "conformance_profile_refs" in admission
        and "conformance_result_refs" in admission
        and "policy_decision_ref" not in admission
        and "grant_ref" not in policy
        and grant.get("policy_decision_ref") == policy.get("decision_ref")
        and grant.get("admission_refs") == [admission.get("admission_ref")]
    )
    assertion(
        assertions,
        "authority.declaration_conformance_admission_policy_grant_separation",
        "authority",
        "Admission, conformance, policy, and grant records remain separate records linked by refs.",
        separation_ok,
        "admission carries conformance refs; grant links policy and admission by refs; policy does not embed grant",
        {
            "admission_has_conformance_profile_refs": "conformance_profile_refs" in admission,
            "admission_has_conformance_result_refs": "conformance_result_refs" in admission,
            "grant_policy_decision_ref": grant.get("policy_decision_ref"),
            "policy_decision_ref": policy.get("decision_ref"),
            "grant_admission_refs": grant.get("admission_refs"),
        },
        [
            PROJECTION_FILES["AdmissionRecord"],
            PROJECTION_FILES["PolicyDecision"],
            PROJECTION_FILES["CapabilityGrant"],
        ],
    )

    required_codes = validation.get("required_refusal_codes", [])
    missing_codes = [code for code in REQUIRED_REFUSAL_CODES if code not in required_codes]
    extra_codes = [code for code in required_codes if code not in REQUIRED_REFUSAL_CODES]
    assertion(
        assertions,
        "fixtures.complete_negative_refusal_matrix",
        "fixtures",
        "The validation report covers the complete required negative refusal matrix.",
        not missing_codes and not extra_codes,
        REQUIRED_REFUSAL_CODES,
        {"missing": missing_codes, "extra": extra_codes, "observed": required_codes},
        [".aide/reports/trust-authorization-contract-v0/validation.json"],
    )

    scope_codes = {
        "workspace_scope_mismatch",
        "resource_scope_mismatch",
        "execution_mode_not_granted",
        "effect_not_granted",
        "network_not_granted",
        "secret_not_granted",
    }
    delegation_codes = {"delegation_not_allowed", "delegation_scope_widening", "delegation_expired"}
    budget_codes = {"grant_expired", "grant_revoked", "grant_exhausted"}
    assertion(
        assertions,
        "authority.scope_delegation_revocation_expiry_budget_fail_closed",
        "authority",
        "Scope, delegation, revocation, expiry, and use-budget failures have stable fail-closed reason coverage.",
        scope_codes.issubset(required_codes) and delegation_codes.issubset(required_codes) and budget_codes.issubset(required_codes),
        sorted(scope_codes | delegation_codes | budget_codes),
        {
            "scope_codes_present": sorted(scope_codes.intersection(required_codes)),
            "delegation_codes_present": sorted(delegation_codes.intersection(required_codes)),
            "budget_codes_present": sorted(budget_codes.intersection(required_codes)),
        },
        [".aide/reports/trust-authorization-contract-v0/validation.json"],
    )

    runtime_distinction_ok = (
        validation.get("runtime_approval_distinct_from_transaction_approval") is True
        and validation.get("unknown_required_capability_fails_closed") is True
        and "approval_required" in required_codes
        and "required_feature_unsupported" in required_codes
    )
    assertion(
        assertions,
        "authority.runtime_transaction_and_required_feature_boundaries",
        "authority",
        "Runtime approval remains distinct from transaction approval and unknown required features fail closed.",
        runtime_distinction_ok,
        "runtime/transaction approval distinction true; required_feature_unsupported and approval_required covered",
        {
            "runtime_approval_distinct_from_transaction_approval": validation.get("runtime_approval_distinct_from_transaction_approval"),
            "unknown_required_capability_fails_closed": validation.get("unknown_required_capability_fails_closed"),
            "approval_required_present": "approval_required" in required_codes,
            "required_feature_unsupported_present": "required_feature_unsupported" in required_codes,
        },
        [".aide/reports/trust-authorization-contract-v0/validation.json"],
    )

    false_boundary_failures: dict[str, Any] = {}
    for field in FALSE_BOUNDARY_FIELDS:
        if validation.get(field) is not False or projection_report.get(field) is not False:
            false_boundary_failures[field] = {
                "validation": validation.get(field),
                "projection_report": projection_report.get(field),
            }
    for kind, projection in projections.items():
        spec = projection.get("spec", {})
        for field in FALSE_BOUNDARY_FIELDS:
            if spec.get(field) is not False:
                false_boundary_failures[f"{kind}.{field}"] = spec.get(field)
    assertion(
        assertions,
        "boundary.no_runtime_or_capability_overclaim",
        "boundary",
        "All live identity, grants, policy engine, enforcement, runtime, worker, provider, network, mutation, release, and approval flags remain false.",
        not false_boundary_failures and validation.get("projection_only_truthful") is True,
        "all boundary booleans false and projection_only_truthful true",
        {"false_boundary_failures": false_boundary_failures, "projection_only_truthful": validation.get("projection_only_truthful")},
        [".aide/reports/trust-authorization-contract-v0/validation.json", ".aide/reports/trust-authorization-contract-v0/projection-report.json"]
        + list(PROJECTION_FILES.values()),
    )

    validation_rows = validation.get("validation_results", [])
    validation_ok = (
        validation.get("schema_helper_alignment_status") == "PASS"
        and len(validation_rows) == len(EXPECTED_KINDS)
        and all(row.get("schema_valid") and row.get("helper_valid") and row.get("result") == "PASS" for row in validation_rows)
    )
    assertion(
        assertions,
        "validation.schema_helper_projection_alignment",
        "validation",
        "Build validation report says every schema, helper, and projection row passed.",
        validation_ok,
        "schema_helper_alignment_status PASS and seven PASS rows",
        {
            "schema_helper_alignment_status": validation.get("schema_helper_alignment_status"),
            "row_count": len(validation_rows),
            "rows": validation_rows,
        },
        [".aide/reports/trust-authorization-contract-v0/validation.json"],
    )

    artifact_hashes = {
        rel(path): sha256_file(path)
        for path in scan_paths
        if path.is_file()
    }
    material_failures = [item for item in assertions if item["outcome"] != "PASS"]
    result = "PASS_WITH_WARNINGS" if not material_failures else "REQUEST_CHANGES"
    recommended_next_task = (
        "AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01"
        if not material_failures
        else "AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-REPAIR-01"
    )
    report = {
        "schema_version": "aide.trust-authorization-contract-check.v0",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "checked_capability": CHECKED_CAPABILITY,
        "result": result,
        "material_finding_count": len(material_failures),
        "missing_evidence": 0,
        "recommended_next_task": recommended_next_task,
        "assertions": assertions,
        "artifact_hashes": artifact_hashes,
        "warnings": [
            "Trust and authorization contract v0 remains projection-only.",
            "No live identity, credential, policy, grant, Service, or enforcement runtime is accepted by this check.",
        ],
    }
    (EVIDENCE_DIR / "independent-check-results.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    markdown_lines = [
        "# Independent Trust Check Results",
        "",
        f"- result: {result}",
        f"- material_finding_count: {len(material_failures)}",
        f"- missing_evidence: 0",
        f"- recommended_next_task: {recommended_next_task}",
        "",
        "## Assertions",
        "",
    ]
    for item in assertions:
        markdown_lines.append(f"- {item['id']}: {item['outcome']}")
    (EVIDENCE_DIR / "independent-check-results.md").write_text(
        "\n".join(markdown_lines) + "\n", encoding="utf-8"
    )
    (REPORT_DIR / "check-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (REPORT_DIR / "status.md").write_text(
        "\n".join(
            [
                "# Trust And Authorization Contract v0 Check",
                "",
                f"- result: {result}",
                f"- checked_capability: {CHECKED_CAPABILITY}",
                f"- material_finding_count: {len(material_failures)}",
                "- missing_evidence: 0",
                f"- recommended_next_task: {recommended_next_task}",
                "",
                "## Warnings",
                "",
                "- Trust and authorization contract v0 remains projection-only.",
                "- Live identity, credentials, policy engine, grants, Service, and enforcement runtime remain non-capabilities.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return 0 if not material_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
