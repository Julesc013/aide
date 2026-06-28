"""Accepted context checks for the fixture-only distribution apply engine.

The apply engine is executable, even though it is fixture-only. This module
keeps the trust boundary explicit: no temp workspace execution can begin until
the selected scenario is bound to accepted predecessor reports and mutually
consistent UpdatePlan/RollbackBundle refs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ACCEPTED_STATUSES = {"accepted", "accepted_with_warnings", "ACCEPTED", "ACCEPTED_WITH_WARNINGS"}

EXPECTED_CONTEXT_REFS = {
    "distribution_manifest_ref": "aide://distribution/aide-lite-pack-v0",
    "source_distribution_ref": "aide://distribution/aide-lite-pack-v0",
    "candidate_distribution_ref": "aide://distribution/aide-lite-pack-v0",
    "target_project_ref": "aide://project/aide-self",
    "current_project_lock_ref": "aide://project-lock/aide-self-aide-lite-pack-v0",
    "candidate_project_lock_ref": "aide://project-lock/aide-self-aide-lite-pack-v0",
    "ownership_ledger_ref": "aide://ownership-ledger/aide-self-project-lock-v0",
    "update_plan_ref": "aide://update-plan/aide-self-no-apply-update-plan-v1",
    "rollback_bundle_ref": "aide://rollback-bundle/aide-self-no-apply-rollback-bundle-v0",
}

EXPECTED_INSTALL_RECORD_REFS = ["aide://install-record/aide-self-install-record-v0"]
EXPECTED_MIGRATION_RECORD_REFS = ["aide://migration-record/install-record-v0/no-op-compatibility"]

ACCEPTANCE_REPORTS = [
    {
        "path": ".aide/reports/distribution-manifest-v1-accept/acceptance-report.json",
        "capability": "distribution_manifest_v1",
    },
    {
        "path": ".aide/reports/project-lock-v0-accept/acceptance-report.json",
        "capability": "project_lock_v0",
    },
    {
        "path": ".aide/reports/ownership-ledger-v1-acceptance/acceptance-report.json",
        "capability": "ownership_ledger_v1",
    },
    {
        "path": ".aide/reports/install-record-v0-acceptance/acceptance-report.json",
        "capability": "install_record_v0",
    },
    {
        "path": ".aide/reports/migration-record-v0-acceptance/acceptance-report.json",
        "capability": "migration_record_v0",
    },
    {
        "path": ".aide/reports/update-plan-v1-acceptance/validation-summary.json",
        "capability": "update_plan_v1",
    },
    {
        "path": ".aide/reports/rollback-bundle-v0-acceptance/validation-summary.json",
        "capability": "rollback_bundle_v0",
    },
    {
        "path": ".aide/reports/update-receipt-v0-acceptance/validation-summary.json",
        "capability": "update_receipt_v0",
    },
]


@dataclass(frozen=True)
class ContextValidation:
    accepted: bool
    refusal_code: str | None = None
    message: str | None = None
    context: dict[str, Any] | None = None

    def as_report(self) -> dict[str, Any]:
        return {
            "accepted": self.accepted,
            "refusal_code": self.refusal_code,
            "message": self.message,
            "context": self.context or {},
        }


def accepted_context_template(operations: list[dict[str, Any]]) -> dict[str, Any]:
    operation_refs = [str(operation.get("operation_ref")) for operation in operations if operation.get("operation_ref")]
    return {
        "required": True,
        "status": "accepted_with_warnings",
        **EXPECTED_CONTEXT_REFS,
        "install_record_refs": list(EXPECTED_INSTALL_RECORD_REFS),
        "migration_record_refs": list(EXPECTED_MIGRATION_RECORD_REFS),
        "rollback_bundle_update_plan_ref": EXPECTED_CONTEXT_REFS["update_plan_ref"],
        "required_bindings": {
            "update_plan": True,
            "rollback_bundle": True,
            "predecessors": True,
        },
        "update_plan_operation_refs": operation_refs,
        "rollback_operation_refs": operation_refs,
    }


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _report_count(report: dict[str, Any], primary: str, fallback: str) -> int:
    value = report.get(primary, report.get(fallback, 1))
    try:
        return int(value)
    except Exception:
        return 1


def acceptance_reports_are_valid(repo_root: str | Path) -> tuple[bool, str | None]:
    root = Path(repo_root)
    for spec in ACCEPTANCE_REPORTS:
        path = root / str(spec["path"])
        report = _read_json(path)
        if report is None:
            return False, f"missing or invalid acceptance report: {spec['path']}"
        status = str(report.get("result", ""))
        if status not in {"ACCEPTED", "ACCEPTED_WITH_WARNINGS"}:
            return False, f"acceptance report is not accepted: {spec['path']}"
        if report.get("accepted_capability") != spec["capability"]:
            return False, f"unexpected accepted capability in {spec['path']}"
        material = _report_count(report, "material_finding_count", "source_material_finding_count")
        missing = _report_count(report, "missing_evidence", "source_missing_evidence")
        if material != 0 or missing != 0:
            return False, f"acceptance report still has material findings or missing evidence: {spec['path']}"
    return True, None


def _refuse(code: str, message: str, context: dict[str, Any] | None = None) -> ContextValidation:
    return ContextValidation(False, code, message, context)


def _list_matches(actual: Any, expected: list[str]) -> bool:
    return list(actual or []) == expected


def _scenario_ref(scenario: dict[str, Any], key: str) -> Any:
    if key == "current_project_lock_ref":
        return scenario.get("current_project_lock_ref", scenario.get("project_lock_ref"))
    if key == "candidate_project_lock_ref":
        return scenario.get("candidate_project_lock_ref", scenario.get("project_lock_ref"))
    if key == "candidate_distribution_ref":
        return scenario.get("candidate_distribution_ref", scenario.get("source_distribution_ref"))
    return scenario.get(key)


def validate_accepted_context(repo_root: str | Path, scenario: dict[str, Any]) -> ContextValidation:
    context = scenario.get("accepted_context")
    if not isinstance(context, dict) or not context.get("required"):
        return _refuse(
            "distribution_apply_engine.accepted_context_missing",
            "accepted context is required before fixture execution",
            context if isinstance(context, dict) else None,
        )

    if str(context.get("status", "")) not in ACCEPTED_STATUSES:
        return _refuse(
            "distribution_apply_engine.accepted_context_not_accepted",
            "accepted context status is not accepted",
            context,
        )

    reports_ok, report_message = acceptance_reports_are_valid(repo_root)
    if not reports_ok:
        return _refuse(
            "distribution_apply_engine.accepted_context_missing",
            report_message or "accepted predecessor reports are missing",
            context,
        )

    update_plan_ref = scenario.get("update_plan_ref") or context.get("update_plan_ref")
    if not update_plan_ref:
        return _refuse(
            "distribution_apply_engine.update_plan_binding_missing",
            "scenario is missing update_plan_ref",
            context,
        )
    if not context.get("update_plan_ref"):
        return _refuse(
            "distribution_apply_engine.update_plan_binding_missing",
            "accepted context is missing update_plan_ref",
            context,
        )

    rollback_bundle_ref = scenario.get("rollback_bundle_ref") or context.get("rollback_bundle_ref")
    if not rollback_bundle_ref:
        return _refuse(
            "distribution_apply_engine.rollback_bundle_binding_missing",
            "scenario is missing rollback_bundle_ref",
            context,
        )
    if not context.get("rollback_bundle_ref"):
        return _refuse(
            "distribution_apply_engine.rollback_bundle_binding_missing",
            "accepted context is missing rollback_bundle_ref",
            context,
        )

    if context.get("rollback_bundle_update_plan_ref") != update_plan_ref:
        return _refuse(
            "distribution_apply_engine.update_plan_rollback_bundle_mismatch",
            "rollback bundle is not bound to the selected update plan",
            context,
        )

    for key, expected in EXPECTED_CONTEXT_REFS.items():
        scenario_value = _scenario_ref(scenario, key)
        context_value = context.get(key)
        if key in {"update_plan_ref", "rollback_bundle_ref"}:
            if scenario_value != context_value:
                code = (
                    "distribution_apply_engine.update_plan_binding_missing"
                    if key == "update_plan_ref"
                    else "distribution_apply_engine.rollback_bundle_binding_missing"
                )
                return _refuse(code, f"scenario and context disagree for {key}", context)
        elif scenario_value is not None and scenario_value != context_value:
            return _refuse("distribution_apply_engine.predecessor_mismatch", f"scenario and context disagree for {key}", context)
        if context_value != expected:
            return _refuse("distribution_apply_engine.predecessor_mismatch", f"accepted context has unexpected {key}", context)

    if not _list_matches(context.get("install_record_refs"), EXPECTED_INSTALL_RECORD_REFS):
        return _refuse("distribution_apply_engine.predecessor_mismatch", "accepted context install_record_refs mismatch", context)
    if not _list_matches(context.get("migration_record_refs"), EXPECTED_MIGRATION_RECORD_REFS):
        return _refuse("distribution_apply_engine.predecessor_mismatch", "accepted context migration_record_refs mismatch", context)
    if scenario.get("install_record_refs") and not _list_matches(scenario.get("install_record_refs"), EXPECTED_INSTALL_RECORD_REFS):
        return _refuse("distribution_apply_engine.predecessor_mismatch", "scenario install_record_refs mismatch", context)
    if scenario.get("migration_record_refs") and not _list_matches(scenario.get("migration_record_refs"), EXPECTED_MIGRATION_RECORD_REFS):
        return _refuse("distribution_apply_engine.predecessor_mismatch", "scenario migration_record_refs mismatch", context)

    update_plan_operations = set(context.get("update_plan_operation_refs") or [])
    rollback_operations = set(context.get("rollback_operation_refs") or [])
    for operation in scenario.get("operations", []):
        operation_ref = operation.get("operation_ref")
        if operation_ref not in update_plan_operations:
            return _refuse(
                "distribution_apply_engine.operation_not_in_update_plan",
                f"operation is not in bound update plan: {operation_ref}",
                context,
            )
        if operation_ref not in rollback_operations:
            return _refuse(
                "distribution_apply_engine.operation_lacks_rollback_coverage",
                f"operation lacks rollback coverage: {operation_ref}",
                context,
            )

    return ContextValidation(True, context=context)
