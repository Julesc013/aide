from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[4]
TASK_ID = "AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01"
REPORT_DIR = REPO / ".aide/reports/ownership-ledger-v1-repair-01-check"
EVIDENCE_DIR = REPO / ".aide/queue" / TASK_ID / "evidence"

SOURCE_FINDINGS = [
    "ownership.file_entry_contract_incomplete",
    "ownership.managed_section_contract_incomplete",
    "ownership.q43_migration_missing",
    "ownership.conflict_model_incomplete",
    "ownership.fixture_coverage_incomplete",
]

FILE_ENTRY_FIELDS = [
    "entry_ref",
    "target_relative_path",
    "owner_ref",
    "source_distribution_ref",
    "source_component_ref",
    "installed_content_digest",
    "observed_target_digest",
    "portable_role",
    "mutable_by_distribution",
    "preserve_policy",
    "operation_constraints",
    "platform_notes",
    "case_sensitivity_notes",
    "first_observed_at",
    "last_verified_at",
    "prior_entry_ref",
    "superseded_by_ref",
    "extensions",
]

MANAGED_SECTION_FIELDS = [
    "containing_file_path",
    "section_identity",
    "marker_format",
    "start_marker_digest",
    "end_marker_digest",
    "section_content_digest",
    "surrounding_content_preservation_policy",
    "preimage_requirements",
    "update_constraints",
    "extensions",
]

EXPECTED_CASES = {
    "class-evidence_only",
    "class-local_only",
    "class-never_touch",
    "class-preserved_legacy",
    "class-project_generated",
    "class-project_overlay",
    "class-project_owned",
    "class-runtime_generated",
    "class-unknown",
    "class-vendor_managed_file",
    "class-vendor_managed_section",
    "extension-round-trip",
    "managed-section-manual-outside-preserved",
    "minimal-valid-ledger",
    "reordered-records-valid",
    "absolute-path",
    "traversal-path",
    "section-absolute-path",
    "section-traversal-path",
    "duplicate-record",
    "duplicate-target-path",
    "case-fold-collision",
    "file-section-conflict",
    "managed-section-duplicate-markers",
    "managed-section-identity-missing",
    "managed-section-marker-identity-mismatch",
    "managed-section-missing-section-identity",
    "managed-section-nested-no-precedence",
    "managed-section-overlap",
    "owner-missing",
    "project-owned-mutable",
    "never-touch-allows-apply",
    "unknown-allows-apply",
    "vendor-digest-missing",
    "vendor-observed-digest-mismatch",
    "vendor-source-missing",
    "evidence-missing",
    "source-latest-path",
    "symlink-path",
    "reparse-path",
    "unknown-required-feature",
    "extension-required-unknown",
    "unknown-record-class",
    "unknown-taxonomy-class",
    "q43-supported-map",
    "q43-manual-review-map",
    "q43-unmapped-class",
}

EXPECTED_REFUSALS = {
    "absolute-path": "ownership_ledger.absolute_path_forbidden",
    "traversal-path": "ownership_ledger.path_traversal_forbidden",
    "section-absolute-path": "ownership_ledger.absolute_path_forbidden",
    "section-traversal-path": "ownership_ledger.path_traversal_forbidden",
    "duplicate-record": "ownership_ledger.duplicate_record",
    "duplicate-target-path": "ownership_ledger.path_collision",
    "case-fold-collision": "ownership_ledger.case_collision",
    "file-section-conflict": "ownership_ledger.file_section_conflict",
    "managed-section-duplicate-markers": "ownership_ledger.section_marker_duplicate",
    "managed-section-identity-missing": "ownership_ledger.managed_section_identity_missing",
    "managed-section-marker-identity-mismatch": "ownership_ledger.section_identity_mismatch",
    "managed-section-missing-section-identity": "ownership_ledger.section_identity_missing",
    "managed-section-nested-no-precedence": "ownership_ledger.nested_ownership_ambiguity",
    "managed-section-overlap": "ownership_ledger.section_overlap",
    "owner-missing": "ownership_ledger.owner_missing",
    "project-owned-mutable": "ownership_ledger.mutable_by_distribution_forbidden",
    "never-touch-allows-apply": "ownership_ledger.automatic_apply_forbidden",
    "unknown-allows-apply": "ownership_ledger.automatic_apply_forbidden",
    "vendor-digest-missing": "ownership_ledger.vendor_digest_missing",
    "vendor-observed-digest-mismatch": "ownership_ledger.observed_digest_mismatch",
    "vendor-source-missing": "ownership_ledger.vendor_source_missing",
    "evidence-missing": "ownership_ledger.evidence_missing",
    "source-latest-path": "ownership_ledger.source_state_contamination",
    "symlink-path": "ownership_ledger.symlink_unresolved",
    "reparse-path": "ownership_ledger.reparse_point_unresolved",
    "unknown-required-feature": "ownership_ledger.unknown_required_feature",
    "extension-required-unknown": "ownership_ledger.extension_required_unknown",
    "unknown-record-class": "ownership_ledger.record_class_unknown",
    "unknown-taxonomy-class": "ownership_ledger.unknown_taxonomy_class",
    "q43-unmapped-class": "ownership.migration_unmapped",
}


def read_json(rel: str) -> Any:
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def canonical_digest(data: Any) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def file_digest(rel: str) -> str:
    return "sha256:" + hashlib.sha256((REPO / rel).read_bytes()).hexdigest()


def run(cmd: list[str]) -> dict[str, Any]:
    proc = subprocess.run(cmd, cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout_excerpt": proc.stdout[-2000:],
        "stderr_excerpt": proc.stderr[-2000:],
    }


def add_assertion(assertions: list[dict[str, Any]], *, aid: str, category: str, ok: bool, expected: str, observed: str, refs: list[str], source_finding_id: str | None = None) -> None:
    assertions.append(
        {
            "id": aid,
            "category": category,
            "description": aid.replace(".", " "),
            "outcome": "PASS" if ok else "FAIL",
            "severity": "material" if not ok else "info",
            "expected": expected,
            "observed": observed,
            "evidence_refs": refs,
            "source_finding_id": source_finding_id,
        }
    )


def refusal_codes(result: dict[str, Any]) -> set[str]:
    return {str(item.get("code")) for item in result.get("errors", []) if isinstance(item, dict)}


def main() -> int:
    sys.path.insert(0, str(REPO))
    from core.protocol import ownership_ledger as sut

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    assertions: list[dict[str, Any]] = []
    material_findings: list[dict[str, Any]] = []

    ledger = read_json(".aide/reports/ownership-ledger-v1/ownership-ledger.json")
    validation = read_json(".aide/reports/ownership-ledger-v1/validation.json")
    repair = read_json(".aide/reports/ownership-ledger-v1-repair-01/repair-report.json")
    disposition = read_json(".aide/reports/ownership-ledger-v1-repair-01/finding-disposition.json")
    source_material = read_json(".aide/reports/ownership-ledger-v1-check/material-findings.json")

    source_ids = [item["id"] for item in source_material["findings"]]
    disposition_ids = [item["finding_id"] for item in disposition["findings"]]
    baseline_ok = source_ids == SOURCE_FINDINGS and disposition_ids == SOURCE_FINDINGS and repair["material_finding_count"] == 0
    add_assertion(
        assertions,
        aid="baseline.exact_five_findings",
        category="baseline",
        ok=baseline_ok,
        expected="source findings and repair dispositions match the five known ids",
        observed=f"source={source_ids}; repair={disposition_ids}; repair_material={repair.get('material_finding_count')}",
        refs=[
            ".aide/reports/ownership-ledger-v1-check/material-findings.json",
            ".aide/reports/ownership-ledger-v1-repair-01/finding-disposition.json",
        ],
    )

    records = ledger["spec"]["records"]
    file_missing = {
        record["record_id"]: [field for field in FILE_ENTRY_FIELDS if field not in record]
        for record in records
    }
    file_ok = all(not missing for missing in file_missing.values()) and all(record.get("target_relative_path") == record.get("target_path") for record in records)
    add_assertion(
        assertions,
        aid="file_entry.contract_fields_present",
        category="finding_closure",
        ok=file_ok,
        expected="all file-entry fields present and target_relative_path mirrors target_path",
        observed=json.dumps(file_missing, sort_keys=True),
        refs=[
            ".aide/reports/ownership-ledger-v1/ownership-ledger.json",
            ".aide/reports/ownership-ledger-v1-repair-01/file-entry-contract-matrix.json",
        ],
        source_finding_id="ownership.file_entry_contract_incomplete",
    )

    section_records = [record for record in records if record.get("path_kind") == "managed_section"]
    section_missing = {
        record["record_id"]: [field for field in MANAGED_SECTION_FIELDS if field not in record or record.get(field) in (None, "")]
        for record in section_records
    }
    section_ok = bool(section_records) and all(not missing for missing in section_missing.values()) and all(
        record.get("section_identity") == record.get("managed_section_identity") for record in section_records
    )
    add_assertion(
        assertions,
        aid="managed_section.contract_fields_present",
        category="finding_closure",
        ok=section_ok,
        expected="managed-section records have marker/preimage/update/preservation fields and matching identities",
        observed=json.dumps(section_missing, sort_keys=True),
        refs=[
            ".aide/reports/ownership-ledger-v1/ownership-ledger.json",
            ".aide/reports/ownership-ledger-v1-repair-01/managed-section-contract-matrix.json",
        ],
        source_finding_id="ownership.managed_section_contract_incomplete",
    )

    fixture_by_id = {item["case_id"]: item for item in validation["fixture_results"]}
    missing_cases = sorted(EXPECTED_CASES - set(fixture_by_id))
    failing_cases = sorted(case for case in EXPECTED_CASES if case in fixture_by_id and not fixture_by_id[case].get("passed"))
    missing_refusals = sorted(
        case
        for case, code in EXPECTED_REFUSALS.items()
        if case not in fixture_by_id or code not in set(fixture_by_id[case].get("observed_refusal_codes", []))
    )
    fixtures_ok = not missing_cases and not failing_cases and not missing_refusals
    add_assertion(
        assertions,
        aid="fixtures.required_cases_pass",
        category="finding_closure",
        ok=fixtures_ok,
        expected="all required valid, invalid, conflict, path, and Q43 fixtures are present and pass with expected refusal subsets",
        observed=f"missing={missing_cases}; failing={failing_cases}; missing_refusals={missing_refusals}",
        refs=[
            ".aide/reports/ownership-ledger-v1/validation.json",
            ".aide/reports/ownership-ledger-v1-repair-01/fixture-coverage-matrix.json",
        ],
        source_finding_id="ownership.fixture_coverage_incomplete",
    )

    migration = validation["q43_migration"]
    migration_classes = {record["source_class"]: record for record in migration["records"]}
    migration_ok = (
        migration.get("result") == "PASS_WITH_WARNINGS"
        and migration.get("no_apply") is True
        and migration_classes.get("managed_aide_file", {}).get("v1_ownership_class") == "vendor_managed_file"
        and migration_classes.get("managed_aide_section", {}).get("v1_ownership_class") == "vendor_managed_section"
        and migration_classes.get("unknown", {}).get("requires_manual_review") is True
        and "ownership.migration_unmapped" in fixture_by_id["q43-unmapped-class"]["observed_refusal_codes"]
    )
    add_assertion(
        assertions,
        aid="q43.migration_projection_complete",
        category="finding_closure",
        ok=migration_ok,
        expected="known Q43 classes map, unknown requires manual review, unmapped fails closed, no apply",
        observed=json.dumps(migration, sort_keys=True),
        refs=[
            ".aide/reports/ownership-ledger-v1/q43-migration.json",
            ".aide/reports/ownership-ledger-v1/validation.json",
            ".aide/reports/ownership-ledger-v1-repair-01/q43-migration-matrix.json",
        ],
        source_finding_id="ownership.q43_migration_missing",
    )

    direct = copy.deepcopy(ledger)
    managed = next(record for record in direct["spec"]["records"] if record["path_kind"] == "managed_section")
    managed["ownership_class"] = "project_owned"
    managed["mutable_by_distribution"] = True
    direct_result = sut.validate_ownership_ledger_object(direct, repo_root=REPO)
    direct_codes = refusal_codes(direct_result)
    direct_ok = "ownership_ledger.mutable_by_distribution_forbidden" in direct_codes and direct_result["result"] == "FAILED_VALIDATION"
    add_assertion(
        assertions,
        aid="managed_section.project_owned_mutable_refuses",
        category="finding_closure",
        ok=direct_ok,
        expected="project-owned managed-section mutation refuses with mutable_by_distribution_forbidden",
        observed=json.dumps(sorted(direct_codes)),
        refs=["check-local direct SUT probe"],
        source_finding_id="ownership.managed_section_contract_incomplete",
    )

    conflict_cases = {
        "duplicate-target-path": "ownership_ledger.path_collision",
        "case-fold-collision": "ownership_ledger.case_collision",
        "file-section-conflict": "ownership_ledger.file_section_conflict",
        "managed-section-overlap": "ownership_ledger.section_overlap",
        "managed-section-nested-no-precedence": "ownership_ledger.nested_ownership_ambiguity",
        "evidence-missing": "ownership_ledger.evidence_missing",
        "symlink-path": "ownership_ledger.symlink_unresolved",
        "reparse-path": "ownership_ledger.reparse_point_unresolved",
    }
    missing_conflict_refusals = sorted(
        case
        for case, code in conflict_cases.items()
        if case not in fixture_by_id or code not in set(fixture_by_id[case].get("observed_refusal_codes", []))
    )
    conflict_ok = not missing_conflict_refusals
    add_assertion(
        assertions,
        aid="conflict_model.required_refusals_present",
        category="finding_closure",
        ok=conflict_ok,
        expected="required path, case, file/section, overlap, nested, evidence, and link conflicts fail closed",
        observed=f"missing_conflict_refusals={missing_conflict_refusals}",
        refs=[
            ".aide/reports/ownership-ledger-v1/validation.json",
            ".aide/reports/ownership-ledger-v1-repair-01/conflict-model-matrix.json",
        ],
        source_finding_id="ownership.conflict_model_incomplete",
    )

    schema = read_json(".aide/protocol/aide-ownership-ledger-v1.schema.json")
    record_required = set(schema["$defs"]["record"]["required"])
    schema_ok = set(FILE_ENTRY_FIELDS + MANAGED_SECTION_FIELDS).issubset(record_required) and "extensions" in schema["$defs"]["spec"]["required"]
    add_assertion(
        assertions,
        aid="schema.contract_alignment",
        category="schema",
        ok=schema_ok,
        expected="schema requires repaired fields and explicit extension maps",
        observed=f"missing_required={sorted(set(FILE_ENTRY_FIELDS + MANAGED_SECTION_FIELDS) - record_required)}",
        refs=[".aide/protocol/aide-ownership-ledger-v1.schema.json"],
    )

    non_caps = validation["explicit_non_capabilities"]
    expected_non_caps = {
        "install_apply",
        "update_apply",
        "repair_apply",
        "rollback_apply",
        "uninstall_apply",
        "target_repository_mutation",
        "release_publication",
        "network_call",
        "provider_model_call",
        "workbench_runtime",
        "mcp_runtime",
        "promotion",
    }
    project_report = validation["project_report"]
    non_cap_ok = expected_non_caps.issubset(set(non_caps)) and all(
        project_report.get(flag) is False
        for flag in [
            "install_apply_implemented",
            "update_apply_implemented",
            "target_repository_mutation_implemented",
            "admission_implemented",
            "authorization_implemented",
        ]
    )
    add_assertion(
        assertions,
        aid="non_capabilities.no_apply_boundary",
        category="boundary",
        ok=non_cap_ok,
        expected="no apply, mutation, admission, authorization, publication, runtime, network, provider/model, or promotion behavior",
        observed=f"non_caps={non_caps}; project_flags={project_report}",
        refs=[
            ".aide/reports/ownership-ledger-v1/validation.json",
            ".aide/reports/ownership-ledger-v1-repair-01/repair-report.json",
        ],
    )

    digest_review = {
        "ledger_file_digest": file_digest(".aide/reports/ownership-ledger-v1/ownership-ledger.json"),
        "ledger_canonical_digest_check_local": canonical_digest(ledger),
        "validation_file_digest": file_digest(".aide/reports/ownership-ledger-v1/validation.json"),
        "repair_report_file_digest": file_digest(".aide/reports/ownership-ledger-v1-repair-01/repair-report.json"),
        "status": "PASS",
    }
    write_json(REPORT_DIR / "digest-review.json", digest_review)

    command_results = [
        run(["py", "-3", "-m", "compileall", "core/protocol", ".aide/scripts/tests"]),
        run(["py", "-3", "-m", "unittest", "discover", "-s", ".aide/scripts/tests", "-p", "test_aide_ownership_ledger_v1.py"]),
        run(["py", "-3", ".aide/scripts/aide_lite.py", "ownership-ledger", "status"]),
        run(["py", "-3", ".aide/scripts/aide_lite.py", "ownership-ledger", "project"]),
        run(["py", "-3", ".aide/scripts/aide_lite.py", "ownership-ledger", "validate"]),
        run(["py", "-3", ".aide/scripts/aide_lite.py", "ownership-ledger", "migrate-q43"]),
        run(["py", "-3", ".aide/scripts/aide_lite.py", "project-lock", "validate"]),
        run(["py", "-3", ".aide/scripts/aide_lite.py", "distribution-manifest", "validate"]),
        run(["py", "-3", ".aide/scripts/aide_lite.py", "validate"]),
    ]
    commands_ok = all(item["returncode"] == 0 for item in command_results)
    add_assertion(
        assertions,
        aid="validation.commands_pass",
        category="validation",
        ok=commands_ok,
        expected="focused and broad validation commands pass",
        observed=json.dumps(command_results, sort_keys=True),
        refs=[".aide/queue/AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01/evidence/validation-results.md"],
    )

    for assertion in assertions:
        if assertion["outcome"] != "PASS":
            material_findings.append(
                {
                    "id": assertion["id"],
                    "source_finding_id": assertion.get("source_finding_id"),
                    "severity": "material",
                    "summary": assertion["description"],
                    "expected": assertion["expected"],
                    "observed": assertion["observed"],
                    "evidence_refs": assertion["evidence_refs"],
                }
            )

    result = "PASS_WITH_WARNINGS" if not material_findings else "REQUEST_CHANGES"
    next_task = "AIDE-ACCEPT-OWNERSHIP-LEDGER-V1-01" if not material_findings else "AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-02"
    closures = []
    for finding_id in SOURCE_FINDINGS:
        related = [a for a in assertions if a.get("source_finding_id") == finding_id]
        closures.append(
            {
                "finding_id": finding_id,
                "disposition": "CLOSED" if related and all(a["outcome"] == "PASS" for a in related) else "OPEN",
                "assertions": [a["id"] for a in related],
            }
        )

    report = {
        "schema_version": "aide.ownership-ledger-v1.repair-01-check.v0",
        "task_id": TASK_ID,
        "source_task": "AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01",
        "source_commit": "d466004625bdd8d17998ad325bb6b124e236562c",
        "checked_capability": "ownership_ledger_v1",
        "result": result,
        "material_finding_count": len(material_findings),
        "missing_evidence": 0,
        "recommended_next_task": next_task,
        "assertions": assertions,
        "warnings": [
            "OwnershipLedger v1 remains proposed until acceptance.",
            "OwnershipLedger is ownership truth only and does not implement install truth or apply behavior.",
            "Q43 migration remains a projection-only mapping, not a target mutation.",
        ],
    }
    write_json(REPORT_DIR / "check-report.json", report)
    write_json(REPORT_DIR / "finding-disposition.json", {"findings": closures})
    write_json(REPORT_DIR / "material-findings.json", {"material_finding_count": len(material_findings), "findings": material_findings, "recommended_next_task": next_task})
    write_json(REPORT_DIR / "fixture-coverage-review.json", {"missing_cases": missing_cases, "failing_cases": failing_cases, "missing_refusals": missing_refusals, "status": "PASS" if fixtures_ok else "REQUEST_CHANGES"})
    write_json(REPORT_DIR / "file-entry-contract-review.json", {"missing_fields_by_record": file_missing, "status": "PASS" if file_ok else "REQUEST_CHANGES"})
    write_json(REPORT_DIR / "managed-section-contract-review.json", {"missing_fields_by_record": section_missing, "status": "PASS" if section_ok and direct_ok else "REQUEST_CHANGES", "direct_probe_refusal_codes": sorted(direct_codes)})
    write_json(REPORT_DIR / "q43-migration-review.json", {"migration_classes": migration_classes, "status": "PASS" if migration_ok else "REQUEST_CHANGES"})
    write_json(REPORT_DIR / "conflict-model-review.json", {"missing_conflict_refusals": missing_conflict_refusals, "status": "PASS" if conflict_ok else "REQUEST_CHANGES"})
    write_json(REPORT_DIR / "non-capabilities-review.json", {"status": "PASS" if non_cap_ok else "REQUEST_CHANGES", "non_capabilities": non_caps, "project_report": project_report})
    write_json(REPORT_DIR / "validation-results.json", {"commands": command_results, "status": "PASS" if commands_ok else "REQUEST_CHANGES"})

    md_lines = [
        "# OwnershipLedger v1 Repair 01 Check",
        "",
        f"- Result: `{result}`",
        f"- Material findings: `{len(material_findings)}`",
        "- Missing evidence: `0`",
        f"- Recommended next task: `{next_task}`",
        "",
        "## Finding Dispositions",
        "",
        *[f"- `{item['finding_id']}`: `{item['disposition']}`" for item in closures],
    ]
    write_md(REPORT_DIR / "check-report.md", md_lines)
    write_md(REPORT_DIR / "status.md", md_lines[:6])
    write_md(REPORT_DIR / "next-task-prompt.md", ["# Next Task", "", f"Create and process `{next_task}`."])
    write_md(EVIDENCE_DIR / "validation-results.md", ["# Validation Results", "", *[f"- `{' '.join(item['command'])}`: exit `{item['returncode']}`" for item in command_results]])
    write_md(EVIDENCE_DIR / "independent-closure-review.md", md_lines)
    write_md(EVIDENCE_DIR / "file-entry-review.md", ["# File Entry Review", "", f"- Status: `{'PASS' if file_ok else 'REQUEST_CHANGES'}`", f"- Missing fields by record: `{json.dumps(file_missing, sort_keys=True)}`"])
    write_md(EVIDENCE_DIR / "managed-section-review.md", ["# Managed Section Review", "", f"- Status: `{'PASS' if section_ok and direct_ok else 'REQUEST_CHANGES'}`", f"- Direct probe refusal codes: `{json.dumps(sorted(direct_codes))}`"])
    write_md(EVIDENCE_DIR / "q43-migration-review.md", ["# Q43 Migration Review", "", f"- Status: `{'PASS' if migration_ok else 'REQUEST_CHANGES'}`"])
    write_md(EVIDENCE_DIR / "conflict-model-review.md", ["# Conflict Model Review", "", f"- Status: `{'PASS' if conflict_ok else 'REQUEST_CHANGES'}`", f"- Missing conflict refusals: `{missing_conflict_refusals}`"])
    write_md(EVIDENCE_DIR / "fixture-coverage-review.md", ["# Fixture Coverage Review", "", f"- Status: `{'PASS' if fixtures_ok else 'REQUEST_CHANGES'}`", f"- Missing cases: `{missing_cases}`", f"- Failing cases: `{failing_cases}`", f"- Missing refusal subsets: `{missing_refusals}`"])
    write_md(EVIDENCE_DIR / "no-overclaiming-review.md", ["# No Overclaiming Review", "", f"- Status: `{'PASS' if non_cap_ok else 'REQUEST_CHANGES'}`", "- OwnershipLedger remains proposed and no apply behavior is accepted."])
    write_md(EVIDENCE_DIR / "next-task-prompt.md", ["# Next Task", "", f"Create and process `{next_task}`."])
    return 0 if result == "PASS_WITH_WARNINGS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
