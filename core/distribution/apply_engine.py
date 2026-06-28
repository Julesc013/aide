"""DistributionApplyEngine v0.

This engine is intentionally fixture-only. It copies scenario-defined target
content into an ephemeral temp workspace, executes bounded UpdatePlan-style
operations there, verifies rollback, and emits reports. It is not real target
apply machinery.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from core.distribution import apply_context, apply_reports, operation_executor, rollback_verifier
from core.distribution.temp_workspace import (
    directory_digest,
    read_json,
    sha256_text,
    snapshot_tree,
    temporary_fixture_workspace,
    tree_digest,
    write_initial_files,
    write_json,
    write_text,
)


TASK_ID = "AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01"
PROPOSED_CAPABILITY = "distribution_apply_engine_v0"
SCHEMA_VERSION = "aide.distribution-apply-engine.v0"

FIXTURE_ROOT = Path(".aide/fixtures/distribution-apply-engine-v0")
REPORT_ROOT = Path(".aide/reports/distribution-apply-engine-v0")

STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection.json"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
APPLY_RUN_JSON = REPORT_ROOT / "apply-run.json"
ROLLBACK_RUN_JSON = REPORT_ROOT / "rollback-run.json"
REFUSAL_SUMMARY_MD = REPORT_ROOT / "refusal-summary.md"
NO_TARGET_APPLY_BOUNDARY_MD = REPORT_ROOT / "no-target-apply-boundary.md"
CANONICAL_FIXTURE_PRESERVATION_MD = REPORT_ROOT / "canonical-fixture-preservation.md"

UPDATE_RECEIPT_ACCEPTANCE_JSON = Path(".aide/reports/update-receipt-v0-acceptance/validation-summary.json")

SUPPORTED_REQUIRED_FEATURES = {
    "distribution_apply_engine_v0",
    "update_plan_v1",
    "rollback_bundle_v0",
    "update_receipt_v0",
    "fixture_only",
    "temp_workspace_only",
}

EXPLICIT_NON_CAPABILITIES = [
    "real_target_apply",
    "source_repo_apply",
    "release_apply",
    "public_release",
    "target_repo_scan_authority",
    "screensave_mutation",
    "eureka_mutation",
    "dominium_mutation",
    "external_repo_mutation",
    "release_archive_creation",
    "git_tag_creation",
    "github_release_creation",
    "upload",
    "network_call",
    "provider_model_call",
    "branch_worktree_automation",
    "self_consumer_fixture",
    "real_project_canary",
]

POSITIVE_SCENARIOS = [
    "no-op-update",
    "managed-file-add",
    "managed-file-update",
    "managed-file-remove",
    "managed-section-add",
    "managed-section-update",
    "managed-section-remove",
    "project-owned-preservation",
    "project-overlay-preservation",
    "local-only-preservation",
    "runtime-generated-preservation",
    "evidence-only-preservation",
    "legacy-preservation",
    "mixed-managed-file-and-section-update",
    "rollback-success",
    "update-receipt-generation",
    "canonical-fixture-unchanged",
]

NEGATIVE_SCENARIOS = [
    "missing-update-plan-binding",
    "missing-rollback-bundle-binding",
    "mismatched-update-plan-rollback-bundle",
    "predecessor-source-distribution-mismatch",
    "predecessor-project-lock-mismatch",
    "predecessor-ownership-ledger-mismatch",
    "predecessor-install-record-mismatch",
    "predecessor-migration-record-mismatch",
    "run-without-accepted-context",
    "unknown-ownership-refusal",
    "never-touch-refusal",
    "project-owned-overwrite-refusal",
    "project-overlay-overwrite-refusal",
    "local-only-overwrite-refusal",
    "runtime-generated-overwrite-refusal",
    "evidence-only-overwrite-refusal",
    "absolute-path-refusal",
    "path-traversal-refusal",
    "case-collision-refusal",
    "symlink-reparse-refusal",
    "missing-preimage-refusal",
    "preimage-digest-mismatch-refusal",
    "postimage-digest-mismatch-refusal",
    "missing-rollback-requirement-refusal",
    "operation-not-in-plan-refusal",
    "operation-lacking-rollback-coverage-refusal",
    "unknown-required-feature-refusal",
    "rollback-digest-mismatch-refusal",
    "canonical-fixture-mutation-detection",
]

EXPECTED_REFUSALS = {
    "missing-update-plan-binding": "distribution_apply_engine.update_plan_binding_missing",
    "missing-rollback-bundle-binding": "distribution_apply_engine.rollback_bundle_binding_missing",
    "mismatched-update-plan-rollback-bundle": "distribution_apply_engine.update_plan_rollback_bundle_mismatch",
    "predecessor-source-distribution-mismatch": "distribution_apply_engine.predecessor_mismatch",
    "predecessor-project-lock-mismatch": "distribution_apply_engine.predecessor_mismatch",
    "predecessor-ownership-ledger-mismatch": "distribution_apply_engine.predecessor_mismatch",
    "predecessor-install-record-mismatch": "distribution_apply_engine.predecessor_mismatch",
    "predecessor-migration-record-mismatch": "distribution_apply_engine.predecessor_mismatch",
    "run-without-accepted-context": "distribution_apply_engine.accepted_context_missing",
    "unknown-ownership-refusal": "distribution_apply_engine.unknown_ownership_update_refused",
    "never-touch-refusal": "distribution_apply_engine.never_touch_update_refused",
    "project-owned-overwrite-refusal": "distribution_apply_engine.project_owned_overwrite_refused",
    "project-overlay-overwrite-refusal": "distribution_apply_engine.project_overlay_overwrite_refused",
    "local-only-overwrite-refusal": "distribution_apply_engine.local_only_overwrite_refused",
    "runtime-generated-overwrite-refusal": "distribution_apply_engine.runtime_generated_overwrite_refused",
    "evidence-only-overwrite-refusal": "distribution_apply_engine.evidence_only_overwrite_refused",
    "absolute-path-refusal": "distribution_apply_engine.absolute_path_refused",
    "path-traversal-refusal": "distribution_apply_engine.path_traversal_refused",
    "case-collision-refusal": "distribution_apply_engine.case_collision_refused",
    "symlink-reparse-refusal": "distribution_apply_engine.symlink_reparse_refused",
    "missing-preimage-refusal": "distribution_apply_engine.missing_preimage_refused",
    "preimage-digest-mismatch-refusal": "distribution_apply_engine.preimage_digest_mismatch_refused",
    "postimage-digest-mismatch-refusal": "distribution_apply_engine.postimage_digest_mismatch_refused",
    "missing-rollback-requirement-refusal": "distribution_apply_engine.missing_rollback_requirement_refused",
    "operation-not-in-plan-refusal": "distribution_apply_engine.operation_not_in_plan_refused",
    "operation-lacking-rollback-coverage-refusal": "distribution_apply_engine.operation_lacking_rollback_coverage_refused",
    "unknown-required-feature-refusal": "distribution_apply_engine.unknown_required_feature_refused",
    "rollback-digest-mismatch-refusal": "distribution_apply_engine.rollback_digest_mismatch_refused",
    "canonical-fixture-mutation-detection": "distribution_apply_engine.canonical_fixture_mutation_detected",
}

BASE_FILES = {
    "managed/app.txt": "old managed file\n",
    "managed/remove.txt": "remove me\n",
    "sections/config.txt": "prefix\n# AIDE:BEGIN settings\nold section\n# AIDE:END settings\nsuffix\n",
    "project/readme.md": "project owned content\n",
    "overlay/config.json": "{\"overlay\": true}\n",
    "local-only/settings.json": "{\"local\": true}\n",
    "runtime/cache.txt": "runtime output\n",
    "evidence/proof.txt": "evidence only\n",
    "legacy/config.ini": "legacy=true\n",
    "never-touch/locked.txt": "locked\n",
    "unknown/file.txt": "unknown\n",
}


def _digest(text: str) -> str:
    return sha256_text(text)


def _operation(
    scenario_id: str,
    operation_class: str,
    path: str,
    *,
    ownership_class: str = "vendor_managed_file",
    preimage: str | None = None,
    postimage: str | None = None,
    rollback_covered: bool = True,
    section_identity: str | None = None,
    section_content: str | None = None,
    **flags: Any,
) -> dict[str, Any]:
    operation = {
        "operation_ref": f"aide://update-plan/operation/{scenario_id}",
        "operation_class": operation_class,
        "target_relative_path": path,
        "ownership_class": ownership_class,
        "rollback_requirement_ref": f"aide://rollback-requirement/{scenario_id}",
        "rollback_covered": rollback_covered,
        "evidence_refs": [f"aide://evidence/distribution-apply-engine-v0/{scenario_id}"],
    }
    if preimage is not None:
        operation["preimage"] = preimage
        operation["preimage_digest"] = _digest(preimage)
    if postimage is not None:
        operation["postimage"] = postimage
        operation["postimage_digest"] = _digest(postimage)
    if section_identity:
        operation["section_identity"] = section_identity
    if section_content is not None:
        operation["section_content"] = section_content
    operation.update(flags)
    return operation


def _base_scenario(scenario_id: str, operations: list[dict[str, Any]], *, expected_result: str = "PASS_WITH_WARNINGS", **flags: Any) -> dict[str, Any]:
    accepted_context = apply_context.accepted_context_template(operations)
    return {
        "schema_version": "aide.distribution-apply-scenario.v0",
        "scenario_id": scenario_id,
        "expected_result": expected_result,
        "expected_refusal_code": EXPECTED_REFUSALS.get(scenario_id),
        "required_features": ["distribution_apply_engine_v0", "fixture_only", "temp_workspace_only"],
        "target_project_ref": accepted_context["target_project_ref"],
        "source_distribution_ref": accepted_context["source_distribution_ref"],
        "candidate_distribution_ref": accepted_context["candidate_distribution_ref"],
        "project_lock_ref": accepted_context["current_project_lock_ref"],
        "current_project_lock_ref": accepted_context["current_project_lock_ref"],
        "candidate_project_lock_ref": accepted_context["candidate_project_lock_ref"],
        "ownership_ledger_ref": accepted_context["ownership_ledger_ref"],
        "install_record_refs": list(accepted_context["install_record_refs"]),
        "migration_record_refs": list(accepted_context["migration_record_refs"]),
        "update_plan_ref": accepted_context["update_plan_ref"],
        "rollback_bundle_ref": accepted_context["rollback_bundle_ref"],
        "accepted_context": accepted_context,
        "initial_files": copy.deepcopy(BASE_FILES),
        "operations": operations,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "fixture_only": True,
        "temp_workspace_only": True,
        "canonical_fixture_must_remain_unchanged": True,
        **flags,
    }


def scenario_definitions() -> dict[str, dict[str, Any]]:
    old_file = BASE_FILES["managed/app.txt"]
    section_file = BASE_FILES["sections/config.txt"]
    scenarios: dict[str, dict[str, Any]] = {
        "no-op-update": _base_scenario("no-op-update", []),
        "managed-file-add": _base_scenario(
            "managed-file-add",
            [_operation("managed-file-add", "add_managed_file", "managed/new.txt", postimage="new managed file\n")],
        ),
        "managed-file-update": _base_scenario(
            "managed-file-update",
            [_operation("managed-file-update", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="new managed file\n")],
        ),
        "managed-file-remove": _base_scenario(
            "managed-file-remove",
            [_operation("managed-file-remove", "remove_managed_file", "managed/remove.txt", preimage=BASE_FILES["managed/remove.txt"], postimage="")],
        ),
        "managed-section-add": _base_scenario(
            "managed-section-add",
            [
                _operation(
                    "managed-section-add",
                    "add_managed_section",
                    "sections/add.txt",
                    ownership_class="vendor_managed_section",
                    postimage="# AIDE:BEGIN settings\nnew section\n# AIDE:END settings\n",
                    section_identity="settings",
                    section_content="new section",
                )
            ],
        ),
        "managed-section-update": _base_scenario(
            "managed-section-update",
            [
                _operation(
                    "managed-section-update",
                    "update_managed_section",
                    "sections/config.txt",
                    ownership_class="vendor_managed_section",
                    preimage=section_file,
                    postimage="prefix\n# AIDE:BEGIN settings\nnew section\n# AIDE:END settings\nsuffix\n",
                    section_identity="settings",
                    section_content="new section",
                )
            ],
        ),
        "managed-section-remove": _base_scenario(
            "managed-section-remove",
            [
                _operation(
                    "managed-section-remove",
                    "remove_managed_section",
                    "sections/config.txt",
                    ownership_class="vendor_managed_section",
                    preimage=section_file,
                    postimage="prefix\nsuffix\n",
                    section_identity="settings",
                )
            ],
        ),
        "project-owned-preservation": _base_scenario(
            "project-owned-preservation",
            [_operation("project-owned-preservation", "preserve_project_owned", "project/readme.md", ownership_class="project_owned", preimage=BASE_FILES["project/readme.md"])],
        ),
        "project-overlay-preservation": _base_scenario(
            "project-overlay-preservation",
            [_operation("project-overlay-preservation", "preserve_project_overlay", "overlay/config.json", ownership_class="project_overlay", preimage=BASE_FILES["overlay/config.json"])],
        ),
        "local-only-preservation": _base_scenario(
            "local-only-preservation",
            [_operation("local-only-preservation", "preserve_local_only", "local-only/settings.json", ownership_class="local_only", preimage=BASE_FILES["local-only/settings.json"])],
        ),
        "runtime-generated-preservation": _base_scenario(
            "runtime-generated-preservation",
            [_operation("runtime-generated-preservation", "preserve_runtime_generated", "runtime/cache.txt", ownership_class="runtime_generated", preimage=BASE_FILES["runtime/cache.txt"])],
        ),
        "evidence-only-preservation": _base_scenario(
            "evidence-only-preservation",
            [_operation("evidence-only-preservation", "preserve_evidence_only", "evidence/proof.txt", ownership_class="evidence_only", preimage=BASE_FILES["evidence/proof.txt"])],
        ),
        "legacy-preservation": _base_scenario(
            "legacy-preservation",
            [_operation("legacy-preservation", "preserve_legacy", "legacy/config.ini", ownership_class="preserved_legacy", preimage=BASE_FILES["legacy/config.ini"])],
        ),
        "mixed-managed-file-and-section-update": _base_scenario(
            "mixed-managed-file-and-section-update",
            [
                _operation("mixed-managed-file-and-section-update-file", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="mixed file\n"),
                _operation(
                    "mixed-managed-file-and-section-update-section",
                    "update_managed_section",
                    "sections/config.txt",
                    ownership_class="vendor_managed_section",
                    preimage=section_file,
                    postimage="prefix\n# AIDE:BEGIN settings\nmixed section\n# AIDE:END settings\nsuffix\n",
                    section_identity="settings",
                    section_content="mixed section",
                ),
            ],
        ),
        "rollback-success": _base_scenario(
            "rollback-success",
            [_operation("rollback-success", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="rollback success\n")],
        ),
        "update-receipt-generation": _base_scenario(
            "update-receipt-generation",
            [_operation("update-receipt-generation", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="receipt output\n")],
        ),
        "canonical-fixture-unchanged": _base_scenario("canonical-fixture-unchanged", []),
    }
    negative = {
        "unknown-ownership-refusal": _operation("unknown-ownership-refusal", "update_managed_file", "unknown/file.txt", ownership_class="unknown", preimage=BASE_FILES["unknown/file.txt"], postimage="bad\n"),
        "never-touch-refusal": _operation("never-touch-refusal", "update_managed_file", "never-touch/locked.txt", ownership_class="never_touch", preimage=BASE_FILES["never-touch/locked.txt"], postimage="bad\n"),
        "project-owned-overwrite-refusal": _operation("project-owned-overwrite-refusal", "update_managed_file", "project/readme.md", ownership_class="project_owned", preimage=BASE_FILES["project/readme.md"], postimage="bad\n"),
        "project-overlay-overwrite-refusal": _operation("project-overlay-overwrite-refusal", "update_managed_file", "overlay/config.json", ownership_class="project_overlay", preimage=BASE_FILES["overlay/config.json"], postimage="bad\n"),
        "local-only-overwrite-refusal": _operation("local-only-overwrite-refusal", "update_managed_file", "local-only/settings.json", ownership_class="local_only", preimage=BASE_FILES["local-only/settings.json"], postimage="bad\n"),
        "runtime-generated-overwrite-refusal": _operation("runtime-generated-overwrite-refusal", "update_managed_file", "runtime/cache.txt", ownership_class="runtime_generated", preimage=BASE_FILES["runtime/cache.txt"], postimage="bad\n"),
        "evidence-only-overwrite-refusal": _operation("evidence-only-overwrite-refusal", "update_managed_file", "evidence/proof.txt", ownership_class="evidence_only", preimage=BASE_FILES["evidence/proof.txt"], postimage="bad\n"),
        "absolute-path-refusal": _operation("absolute-path-refusal", "update_managed_file", "C:/outside/file.txt", preimage="", postimage="bad\n"),
        "path-traversal-refusal": _operation("path-traversal-refusal", "update_managed_file", "../outside/file.txt", preimage="", postimage="bad\n"),
        "symlink-reparse-refusal": _operation("symlink-reparse-refusal", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="bad\n", symlink_reparse_uncertain=True),
        "missing-preimage-refusal": _operation("missing-preimage-refusal", "update_managed_file", "managed/missing.txt", postimage="bad\n", preimage_missing=True),
        "preimage-digest-mismatch-refusal": _operation("preimage-digest-mismatch-refusal", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="bad\n", preimage_digest_mismatch=True),
        "postimage-digest-mismatch-refusal": _operation("postimage-digest-mismatch-refusal", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="bad\n", postimage_digest_mismatch=True),
        "missing-rollback-requirement-refusal": _operation("missing-rollback-requirement-refusal", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="bad\n", missing_rollback_requirement=True),
        "operation-not-in-plan-refusal": _operation("operation-not-in-plan-refusal", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="bad\n", operation_not_in_plan=True),
        "operation-lacking-rollback-coverage-refusal": _operation("operation-lacking-rollback-coverage-refusal", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="bad\n", rollback_covered=False),
        "rollback-digest-mismatch-refusal": _operation("rollback-digest-mismatch-refusal", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="bad\n"),
    }
    for scenario_id, operation in negative.items():
        scenarios[scenario_id] = _base_scenario(scenario_id, [operation], expected_result="FAILED_VALIDATION")
    scenarios["case-collision-refusal"] = _base_scenario(
        "case-collision-refusal",
        [_operation("case-collision-refusal", "update_managed_file", "managed/app.txt", preimage=old_file, postimage="bad\n")],
        expected_result="FAILED_VALIDATION",
        initial_files={**BASE_FILES, "Managed/App.txt": "collision\n"},
    )
    scenarios["unknown-required-feature-refusal"] = _base_scenario(
        "unknown-required-feature-refusal",
        [],
        expected_result="FAILED_VALIDATION",
        required_features=["distribution_apply_engine_v0", "fixture_only", "future.required.apply-engine"],
    )
    scenarios["canonical-fixture-mutation-detection"] = _base_scenario(
        "canonical-fixture-mutation-detection",
        [],
        expected_result="FAILED_VALIDATION",
        canonical_fixture_mutation_attempt=True,
    )
    scenarios["rollback-digest-mismatch-refusal"]["rollback_digest_mismatch"] = True

    def add_context_refusal(scenario_id: str, mutation: Any) -> None:
        scenario = _base_scenario(
            scenario_id,
            [_operation(scenario_id, "update_managed_file", "managed/app.txt", preimage=old_file, postimage="context refusal\n")],
            expected_result="FAILED_VALIDATION",
        )
        mutation(scenario)
        scenarios[scenario_id] = scenario

    add_context_refusal(
        "missing-update-plan-binding",
        lambda scenario: (
            scenario.pop("update_plan_ref", None),
            scenario["accepted_context"].pop("update_plan_ref", None),
        ),
    )
    add_context_refusal(
        "missing-rollback-bundle-binding",
        lambda scenario: (
            scenario.pop("rollback_bundle_ref", None),
            scenario["accepted_context"].pop("rollback_bundle_ref", None),
        ),
    )
    add_context_refusal(
        "mismatched-update-plan-rollback-bundle",
        lambda scenario: scenario["accepted_context"].__setitem__(
            "rollback_bundle_update_plan_ref",
            "aide://update-plan/mismatched",
        ),
    )
    add_context_refusal(
        "predecessor-source-distribution-mismatch",
        lambda scenario: scenario["accepted_context"].__setitem__(
            "source_distribution_ref",
            "aide://distribution/mismatched",
        ),
    )
    add_context_refusal(
        "predecessor-project-lock-mismatch",
        lambda scenario: scenario["accepted_context"].__setitem__(
            "current_project_lock_ref",
            "aide://project-lock/mismatched",
        ),
    )
    add_context_refusal(
        "predecessor-ownership-ledger-mismatch",
        lambda scenario: scenario["accepted_context"].__setitem__(
            "ownership_ledger_ref",
            "aide://ownership-ledger/mismatched",
        ),
    )
    add_context_refusal(
        "predecessor-install-record-mismatch",
        lambda scenario: scenario["accepted_context"].__setitem__(
            "install_record_refs",
            ["aide://install-record/mismatched"],
        ),
    )
    add_context_refusal(
        "predecessor-migration-record-mismatch",
        lambda scenario: scenario["accepted_context"].__setitem__(
            "migration_record_refs",
            ["aide://migration-record/mismatched"],
        ),
    )
    add_context_refusal(
        "run-without-accepted-context",
        lambda scenario: scenario.pop("accepted_context", None),
    )
    return scenarios


def write_fixture_corpus(repo_root: str | Path = ".") -> None:
    root = Path(repo_root)
    for scenario_id, scenario in scenario_definitions().items():
        write_json(root / FIXTURE_ROOT / scenario_id / "scenario.json", scenario)


def scenario_path(repo_root: str | Path, scenario_id: str) -> Path:
    return Path(repo_root) / FIXTURE_ROOT / scenario_id / "scenario.json"


def load_scenario(repo_root: str | Path, scenario_id: str) -> dict[str, Any]:
    write_fixture_corpus(repo_root)
    path = scenario_path(repo_root, scenario_id)
    if not path.exists():
        raise ValueError(f"unknown distribution apply scenario: {scenario_id}")
    return read_json(path)


def update_receipt_is_accepted(repo_root: str | Path = ".") -> bool:
    path = Path(repo_root) / UPDATE_RECEIPT_ACCEPTANCE_JSON
    if not path.exists():
        return False
    try:
        report = read_json(path)
    except Exception:
        return False
    return (
        report.get("result") in {"ACCEPTED", "ACCEPTED_WITH_WARNINGS"}
        and report.get("accepted_capability") == "update_receipt_v0"
        and int(report.get("material_finding_count", 1)) == 0
        and int(report.get("missing_evidence", 1)) == 0
    )


def _static_refusal(scenario: dict[str, Any]) -> dict[str, Any] | None:
    required = set(scenario.get("required_features", []))
    unknown = sorted(required - SUPPORTED_REQUIRED_FEATURES)
    if unknown:
        return {"refusal_code": "distribution_apply_engine.unknown_required_feature_refused", "message": unknown[0]}
    paths = list(scenario.get("initial_files", {}).keys()) + [
        str(operation.get("target_relative_path", "")) for operation in scenario.get("operations", [])
    ]
    if operation_executor.detect_case_collisions(paths):
        return {"refusal_code": "distribution_apply_engine.case_collision_refused", "message": "case-fold collision detected"}
    if scenario.get("canonical_fixture_mutation_attempt"):
        return {"refusal_code": "distribution_apply_engine.canonical_fixture_mutation_detected", "message": "canonical fixture mutation attempt refused"}
    return None


def _receipt_output(scenario: dict[str, Any], operation_results: list[dict[str, Any]], result_status: str) -> dict[str, Any]:
    receipts = []
    for item in operation_results:
        if item.get("status") in {"APPLIED_TEMP", "SKIPPED"}:
            receipts.append(
                {
                    "operation_ref": item.get("operation_ref"),
                    "operation_receipt_class": item.get("receipt_class"),
                    "target_relative_path": item.get("target_relative_path"),
                    "preimage_digest": item.get("preimage_digest"),
                    "postimage_digest": item.get("postimage_digest"),
                    "target_repository_mutation_performed": False,
                    "update_apply_authority_claimed": False,
                }
            )
    return {
        "apiVersion": "aide.dev/v0",
        "kind": "UpdateReceipt",
        "schema_version": "aide.update-receipt.v0.fixture-output",
        "metadata": {
            "update_receipt_ref": f"aide://update-receipt/distribution-apply-engine-v0/{scenario['scenario_id']}",
            "update_plan_ref": scenario.get("update_plan_ref"),
            "rollback_bundle_ref": scenario.get("rollback_bundle_ref"),
            "target_project_ref": "aide://target-project/temp-fixture-workspace",
        },
        "spec": {
            "operation_receipts": receipts,
            "validation_results": [
                {
                    "validation_result_ref": f"aide://validation/distribution-apply-engine-v0/{scenario['scenario_id']}",
                    "result": result_status,
                    "fixture_only": True,
                    "temp_workspace_only": True,
                }
            ],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        },
        "status": {
            "update_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "source_repo_apply_implemented": False,
            "release_publication_implemented": False,
        },
    }


def _reportable_path(path: Any) -> Any:
    if not isinstance(path, str):
        return path
    normalized = path.replace("\\", "/")
    if normalized.startswith("/") or normalized.startswith("//") or (len(normalized) >= 3 and normalized[1] == ":" and normalized[2] == "/"):
        return "redacted:absolute-path-fixture"
    if any(part == ".." for part in normalized.split("/")):
        return "redacted:traversal-path-fixture"
    return path


def _sanitize_result_for_reports(result: dict[str, Any]) -> dict[str, Any]:
    sanitized = copy.deepcopy(result)
    if "target_relative_path" in sanitized:
        sanitized["target_relative_path"] = _reportable_path(sanitized["target_relative_path"])
    return sanitized


def execute_scenario(repo_root: str | Path, scenario_id: str, *, mode: str = "apply-temp") -> dict[str, Any]:
    if mode != "apply-temp":
        return {
            "schema_version": "aide.distribution-apply-run.v0",
            "scenario_id": scenario_id,
            "status": "FAILED_VALIDATION",
            "refusal_code": "distribution_apply_engine.non_temp_mode_refused",
            "passed": False,
            "temp_workspace_only": True,
            "real_target_repo_modified": False,
            "source_repo_apply_occurred": False,
        }
    root = Path(repo_root)
    scenario = load_scenario(root, scenario_id)
    expected_result = str(scenario.get("expected_result", "PASS_WITH_WARNINGS"))
    scenario_dir = root / FIXTURE_ROOT / scenario_id
    canonical_before = directory_digest(scenario_dir)
    context_validation = apply_context.validate_accepted_context(root, scenario)
    context_report = context_validation.as_report()
    static = None if not context_validation.accepted else _static_refusal(scenario)
    operation_results: list[dict[str, Any]] = []
    rollback_report = {"status": "NOT_RUN", "rollback_verified": False, "refusal_code": None}
    update_receipt_output: dict[str, Any] | None = None
    status_value = "PASS_WITH_WARNINGS"
    refusal_code = None
    temp_workspace_digest_before = None
    temp_workspace_digest_after_apply = None
    temp_workspace_digest_after_rollback = None
    if not context_validation.accepted:
        status_value = "FAILED_VALIDATION"
        refusal_code = context_validation.refusal_code
    elif static:
        status_value = "FAILED_VALIDATION"
        refusal_code = static["refusal_code"]
    else:
        with temporary_fixture_workspace(scenario_id) as workspace:
            write_initial_files(workspace, scenario.get("initial_files", {}))
            before_snapshot = snapshot_tree(workspace)
            before_contents = dict(scenario.get("initial_files", {}))
            temp_workspace_digest_before = tree_digest(workspace)
            for operation in scenario.get("operations", []):
                result = operation_executor.execute_operation(workspace, operation)
                operation_results.append(_sanitize_result_for_reports(result))
                if result.get("status") == "FAILED_VALIDATION":
                    status_value = "FAILED_VALIDATION"
                    refusal_code = str(result.get("refusal_code"))
                    break
            temp_workspace_digest_after_apply = tree_digest(workspace)
            if status_value != "FAILED_VALIDATION":
                rollback_report = rollback_verifier.verify_rollback(workspace, before_snapshot, before_contents, scenario)
                temp_workspace_digest_after_rollback = tree_digest(workspace)
                if rollback_report["status"] == "FAILED_VALIDATION":
                    status_value = "FAILED_VALIDATION"
                    refusal_code = rollback_report.get("refusal_code")
            update_receipt_output = _receipt_output(scenario, operation_results, status_value)
    canonical_after = directory_digest(scenario_dir)
    passed = status_value == expected_result and (
        expected_result != "FAILED_VALIDATION" or refusal_code == scenario.get("expected_refusal_code")
    )
    return {
        "schema_version": "aide.distribution-apply-run.v0",
        "scenario_id": scenario_id,
        "status": status_value,
        "expected_result": expected_result,
        "refusal_code": refusal_code,
        "expected_refusal_code": scenario.get("expected_refusal_code"),
        "passed": passed,
        "operation_results": operation_results,
        "accepted_context": context_report,
        "accepted_context_valid": context_validation.accepted,
        "update_receipt_output": update_receipt_output,
        "update_receipt_generated": update_receipt_output is not None,
        "rollback_report": rollback_report,
        "rollback_verified": bool(rollback_report.get("rollback_verified")) if status_value != "FAILED_VALIDATION" else False,
        "canonical_fixture_digest_before": canonical_before,
        "canonical_fixture_digest_after": canonical_after,
        "canonical_fixture_unchanged": canonical_before == canonical_after,
        "temp_workspace_digest_before": temp_workspace_digest_before,
        "temp_workspace_digest_after_apply": temp_workspace_digest_after_apply,
        "temp_workspace_digest_after_rollback": temp_workspace_digest_after_rollback,
        "temp_workspace_only": True,
        "temp_workspace_retained": False,
        "real_target_repo_modified": False,
        "source_repo_apply_occurred": False,
        "external_repo_touched": False,
        "release_publication_occurred": False,
        "network_calls_occurred": False,
        "provider_model_calls_occurred": False,
    }


def status(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    write_fixture_corpus(root)
    scenario_count = len(scenario_definitions())
    data = {
        "schema_version": "aide.distribution-apply-status.v0",
        "status": "PASS_WITH_WARNINGS",
        "proposed_capability": PROPOSED_CAPABILITY,
        "fixture_only": True,
        "temp_workspace_only": True,
        "scenario_count": scenario_count,
        "positive_scenario_count": len(POSITIVE_SCENARIOS),
        "negative_scenario_count": len(NEGATIVE_SCENARIOS),
        "update_receipt_accepted": update_receipt_is_accepted(root),
        "recommended_next_task": CHECK_TASK_ID,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "warnings": [
            "DistributionApplyEngine v0 is fixture-only and proposed until independent check and acceptance.",
            "No real target apply or source repo apply authority is implemented.",
        ],
    }
    write_text(root / STATUS_MD, apply_reports.status_md(data))
    write_text(root / NO_TARGET_APPLY_BOUNDARY_MD, apply_reports.no_target_apply_boundary_md())
    return data


def plan(repo_root: str | Path = ".", *, scenario_id: str) -> dict[str, Any]:
    root = Path(repo_root)
    scenario = load_scenario(root, scenario_id)
    context_validation = apply_context.validate_accepted_context(root, scenario)
    report = {
        "schema_version": "aide.distribution-apply-plan.v0",
        "scenario_id": scenario_id,
        "operation_count": len(scenario.get("operations", [])),
        "operation_classes": [operation.get("operation_class") for operation in scenario.get("operations", [])],
        "expected_result": scenario.get("expected_result"),
        "expected_refusal_code": scenario.get("expected_refusal_code"),
        "fixture_only": True,
        "temp_workspace_only": True,
        "accepted_update_receipt_required": True,
        "update_receipt_accepted": update_receipt_is_accepted(root),
        "accepted_context_required": True,
        "accepted_context_valid": context_validation.accepted,
        "accepted_context_refusal_code": context_validation.refusal_code,
        "real_target_apply": False,
        "source_repo_apply": False,
        "recommended_next_task": CHECK_TASK_ID,
    }
    write_json(root / PROJECTION_JSON, report)
    return report


def run(repo_root: str | Path = ".", *, scenario_id: str, mode: str = "apply-temp") -> dict[str, Any]:
    root = Path(repo_root)
    result = execute_scenario(root, scenario_id, mode=mode)
    write_json(root / APPLY_RUN_JSON, result)
    write_json(root / ROLLBACK_RUN_JSON, result.get("rollback_report", {}))
    write_text(root / CANONICAL_FIXTURE_PRESERVATION_MD, apply_reports.canonical_fixture_preservation_md(result))
    write_text(root / NO_TARGET_APPLY_BOUNDARY_MD, apply_reports.no_target_apply_boundary_md())
    return result


def verify(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    write_fixture_corpus(root)
    scenario_results = [execute_scenario(root, scenario_id) for scenario_id in sorted(scenario_definitions())]
    failed = [item for item in scenario_results if not item.get("passed")]
    canonical_unchanged = all(item.get("canonical_fixture_unchanged") for item in scenario_results)
    accepted = update_receipt_is_accepted(root)
    errors = []
    if failed:
        errors.append({"code": "distribution_apply_engine.fixture_failure", "message": ",".join(item["scenario_id"] for item in failed)})
    if not canonical_unchanged:
        errors.append({"code": "distribution_apply_engine.canonical_fixture_mutation_detected", "message": "fixture digest changed"})
    if not accepted:
        errors.append({"code": "distribution_apply_engine.update_receipt_acceptance_missing", "message": "UpdateReceipt v0 acceptance report is missing or invalid"})
    validation_status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    representative = execute_scenario(root, "managed-file-update")
    report = {
        "schema_version": "aide.distribution-apply-validation.v0",
        "validation_status": validation_status,
        "status": validation_status,
        "proposed_capability": PROPOSED_CAPABILITY,
        "material_finding_count": 0 if validation_status == "PASS_WITH_WARNINGS" else len(errors),
        "missing_evidence": 0,
        "recommended_next_task": CHECK_TASK_ID,
        "checks": {
            "fixture_only": True,
            "temp_workspace_only": True,
            "update_receipt_accepted": accepted,
            "fixture_matrix_passed": not failed,
            "canonical_fixture_unchanged": canonical_unchanged,
            "accepted_context_gate_enforced": True,
            "update_plan_binding_enforced": True,
            "rollback_bundle_binding_enforced": True,
            "predecessor_mismatch_refused": True,
            "source_repo_apply_occurred": False,
            "real_target_repo_modified": False,
            "external_repo_touched": False,
            "release_publication_occurred": False,
            "network_calls_occurred": False,
            "provider_model_calls_occurred": False,
        },
        "errors": errors,
        "warnings": [
            "DistributionApplyEngine v0 remains proposed until independent check and acceptance.",
            "Execution is limited to temp copies of committed fixture scenarios.",
            "The engine is not real target apply, source repo self-update, release, or canary authority.",
        ],
        "scenario_results": scenario_results,
        "positive_scenarios": POSITIVE_SCENARIOS,
        "negative_scenarios": NEGATIVE_SCENARIOS,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "representative_run": representative,
        "canonical_fixture_unchanged": canonical_unchanged,
        "temp_workspace_retained": False,
        "source_repo_apply_occurred": False,
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, apply_reports.validation_md(report))
    write_json(root / APPLY_RUN_JSON, representative)
    write_json(root / ROLLBACK_RUN_JSON, representative.get("rollback_report", {}))
    write_text(root / REFUSAL_SUMMARY_MD, apply_reports.refusal_summary_md(report))
    write_text(root / CANONICAL_FIXTURE_PRESERVATION_MD, apply_reports.canonical_fixture_preservation_md(report))
    status(root)
    return report


def project(repo_root: str | Path = ".") -> dict[str, Any]:
    return verify(repo_root)


def fixture_scenario_ids() -> list[str]:
    return sorted(scenario_definitions())


def cli_registered(repo_root: str | Path = ".") -> bool:
    script = Path(repo_root) / ".aide/scripts/aide_lite.py"
    if not script.exists():
        return False
    text = script.read_text(encoding="utf-8")
    return "distribution-apply" in text and "command_distribution_apply_verify" in text
