"""Conformance expectations for the Dominium read-only seam."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from . import contracts, fixture_replay, integrity, models


EXPECTATION_SPECS = [
    ("contract parsing", "seam.contract.parses"),
    ("stable identity", "seam.identity.unique"),
    ("exact repository identity", "seam.repository.identity_exact"),
    ("read-only source access", "seam.source.read_only"),
    ("no cross-repo writes", "seam.source.no_writes"),
    ("deterministic snapshot", "seam.snapshot.digest"),
    ("deterministic projection", "seam.projection.digest"),
    ("source digest binding", "seam.source.digest_binding"),
    ("bundle self digest binding", "seam.bundle.self_digest"),
    ("bounded mapping completeness", "seam.mapping.complete_bounded"),
    ("authority preservation", "seam.authority.preserved"),
    ("Workbench non-authority", "seam.workbench.non_authority"),
    ("refusal typing", "seam.refusal.typed"),
    ("diagnostic typing", "seam.diagnostic.typed"),
    ("evidence linkage", "seam.evidence.closed"),
    ("event correlation", "seam.event.correlated"),
    ("version compatibility", "seam.compatibility.bounded"),
    ("unsupported-operation refusal", "seam.unsupported_operations.refused"),
    ("no provider/model/network activity", "seam.network.absent"),
    ("no worker execution", "seam.worker.absent"),
    ("no mutation", "seam.mutation.absent"),
    ("explicit non-capabilities", "seam.non_capabilities.preserved"),
    ("replayable negative fixtures", "seam.negative_fixtures.replay"),
]

EXPECTATIONS = [description for description, _assertion_id in EXPECTATION_SPECS]


def conformance_expectations() -> list[dict[str, Any]]:
    return [
        {
            "id": f"dominium-readonly-seam-{index:02d}",
            "description": description,
            "assertion_id": assertion_id,
            "required_for_build": True,
            "status": "declared",
        }
        for index, (description, assertion_id) in enumerate(EXPECTATION_SPECS, start=1)
    ]


def _records(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    records = bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {}
    return integrity.record_list(records)


def _error_codes(validation_report: dict[str, Any]) -> set[str]:
    return {str(item.get("code", "")) for item in validation_report.get("error_records", []) if isinstance(item, dict)}


def _expectation_checks(bundle: dict[str, Any], validation_report: dict[str, Any], *, dominium_root: str | Path | None = None) -> list[Callable[[], tuple[bool, Any, Any]]]:
    records = _records(bundle)
    record_kinds = {item.get("kind") for item in records}
    errors = _error_codes(validation_report)
    source = bundle.get("source_snapshot", {}) if isinstance(bundle.get("source_snapshot"), dict) else {}
    digests = bundle.get("content_digests", {}) if isinstance(bundle.get("content_digests"), dict) else {}
    caps = bundle.get("records", {}).get("host_capability_set", {}) if isinstance(bundle.get("records"), dict) else {}
    bridge = bundle.get("records", {}).get("dominium_bridge_manifest", {}) if isinstance(bundle.get("records"), dict) else {}
    summary = bundle.get("registry_projection_summary", {}) if isinstance(bundle.get("registry_projection_summary"), dict) else {}

    def no_error_prefix(prefix: str) -> tuple[bool, Any, Any]:
        observed = sorted(code for code in errors if code.startswith(prefix))
        return (not observed, "no matching validation errors", observed)

    def negative_replay() -> tuple[bool, Any, Any]:
        failed: list[dict[str, Any]] = []
        for case in fixture_replay.negative_fixture_cases(bundle):
            invalid = fixture_replay.materialize_fixture(case, bundle)
            observed_digest = integrity.stable_digest(invalid)
            if observed_digest != case["invalid_bundle_sha256"]:
                failed.append({"name": case["name"], "reason": "digest mismatch"})
                continue
            expected = set(case["expected_error_codes"])
            root_for_case = dominium_root if expected.intersection({"diagnostic.registry", "refusal.registry"}) else None
            observed = _error_codes(validation_report_for_negative(invalid, dominium_root=root_for_case))
            if not expected.issubset(observed):
                failed.append({"name": case["name"], "expected": sorted(expected), "observed": sorted(observed)})
        return (not failed, "all negative fixture expected codes observed", failed)

    return [
        lambda: (bundle.get("apiVersion") == models.API_VERSION and bundle.get("kind") == "DominiumReadonlySeamBundle", {"apiVersion": models.API_VERSION, "kind": "DominiumReadonlySeamBundle"}, {"apiVersion": bundle.get("apiVersion"), "kind": bundle.get("kind")}),
        lambda: (len({item.get("metadata", {}).get("id") for item in records}) == len(records), "unique record metadata ids", len(records)),
        lambda: (source.get("repository_identity", {}).get("canonical_identity") == "github.com/julesc013/dominium", "github.com/julesc013/dominium", source.get("repository_identity", {}).get("canonical_identity")),
        lambda: (source.get("read_only_operations", {}).get("git_fetch") is False and source.get("read_only_operations", {}).get("git_pull") is False, {"git_fetch": False, "git_pull": False}, source.get("read_only_operations", {})),
        lambda: (source.get("read_only_operations", {}).get("dominium_file_write") is False, False, source.get("read_only_operations", {}).get("dominium_file_write")),
        lambda: (source.get("snapshot_digest") == integrity.stable_digest(integrity.snapshot_payload_for_digest(source)), integrity.stable_digest(integrity.snapshot_payload_for_digest(source)), source.get("snapshot_digest")),
        lambda: (digests.get("projection_index") == integrity.stable_digest(integrity.projection_index_for_records(bundle.get("records", {}))), integrity.stable_digest(integrity.projection_index_for_records(bundle.get("records", {}))), digests.get("projection_index")),
        lambda: no_error_prefix("digest.source"),
        lambda: (digests.get("seam_bundle_without_self_digest") == integrity.stable_digest(integrity.bundle_payload_for_self_digest(bundle)), integrity.stable_digest(integrity.bundle_payload_for_self_digest(bundle)), digests.get("seam_bundle_without_self_digest")),
        lambda: (record_kinds == set(models.AUTHORIZED_SEAM_KINDS) and "diagnostics" in summary and "refusals" in summary, sorted(models.AUTHORIZED_SEAM_KINDS), sorted(record_kinds)),
        lambda: no_error_prefix("authority."),
        lambda: (bridge.get("spec", {}).get("ownership", {}).get("Workbench") == "presentation, context capture, preview, approval interaction, apply requests", "presentation, context capture, preview, approval interaction, apply requests", bridge.get("spec", {}).get("ownership", {}).get("Workbench")),
        lambda: no_error_prefix("refusal."),
        lambda: no_error_prefix("diagnostic."),
        lambda: no_error_prefix("reference.closure"),
        lambda: no_error_prefix("event."),
        lambda: (bundle.get("metadata", {}).get("compatibility", {}).get("readOldWriteCurrent") is True, True, bundle.get("metadata", {}).get("compatibility", {}).get("readOldWriteCurrent")),
        lambda: (models.RECOMMENDED_NEXT_TASK.endswith("REPAIR-02"), "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02", models.RECOMMENDED_NEXT_TASK),
        lambda: (bundle.get("status", {}).get("network_call_performed") is False and bundle.get("status", {}).get("provider_or_model_called") is False, {"network_call_performed": False, "provider_or_model_called": False}, bundle.get("status", {})),
        lambda: (bundle.get("status", {}).get("worker_executed") is False, False, bundle.get("status", {}).get("worker_executed")),
        lambda: (caps.get("spec", {}).get("forbidden_capabilities") and {item.get("id") for item in caps.get("spec", {}).get("forbidden_capabilities", [])} == contracts.FORBIDDEN_CAPABILITIES, sorted(contracts.FORBIDDEN_CAPABILITIES), sorted(item.get("id") for item in caps.get("spec", {}).get("forbidden_capabilities", []))),
        lambda: (bundle.get("explicit_non_capabilities") == models.EXPLICIT_NON_CAPABILITIES, models.EXPLICIT_NON_CAPABILITIES, bundle.get("explicit_non_capabilities")),
        negative_replay,
    ]


def validation_report_for_negative(bundle: dict[str, Any], *, dominium_root: str | Path | None = None) -> dict[str, Any]:
    from . import validation  # Local import avoids an import cycle.

    return validation.validate_bundle(bundle, dominium_root=dominium_root)


def conformance_assertions(bundle: dict[str, Any], validation_report: dict[str, Any], *, dominium_root: str | Path | None = None) -> dict[str, Any]:
    assertions: dict[str, dict[str, Any]] = {}
    for expectation, check in zip(conformance_expectations(), _expectation_checks(bundle, validation_report, dominium_root=dominium_root), strict=True):
        passed, expected, observed = check()
        assertion_id = expectation["assertion_id"]
        assertions[assertion_id] = {
            "assertion_id": assertion_id,
            "description": expectation["description"],
            "result": "PASS" if passed else "FAILED_VALIDATION",
            "expected": expected,
            "observed": observed,
        }
    return {
        "schema_version": "aide.dominium-readonly-seam.conformance-assertions.v0",
        "task_id": models.REPAIR_TASK_ID,
        "assertions": assertions,
    }


def _not_proven_results(validation_report: dict[str, Any] | None) -> dict[str, Any]:
    results = [
        {
            "id": item["id"],
            "description": item["description"],
            "assertion_id": item["assertion_id"],
            "result": "NOT_PROVEN",
            "expected": "bundle plus expectation-specific evidence",
            "observed": "aggregate validation report only",
            "evidence_refs": [],
            "failure_details": "aggregate-only conformance cannot prove expectation-specific PASS",
        }
        for item in conformance_expectations()
    ]
    return {
        "schema_version": "aide.dominium-readonly-seam.conformance-results.v2",
        "task_id": models.REPAIR_TASK_ID,
        "status": "FAILED_VALIDATION",
        "expectation_count": len(results),
        "passed_count": 0,
        "results": results,
        "aggregate_validation_status": (validation_report or {}).get("validation_status"),
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }


def conformance_results(bundle: dict[str, Any], validation_report: dict[str, Any] | None = None, *, dominium_root: str | Path | None = None) -> dict[str, Any]:
    if validation_report is None:
        return _not_proven_results(bundle)
    assertions = conformance_assertions(bundle, validation_report, dominium_root=dominium_root)
    results = []
    for expectation in conformance_expectations():
        assertion_id = expectation["assertion_id"]
        assertion = assertions["assertions"][assertion_id]
        result = {
            "id": expectation["id"],
            "description": expectation["description"],
            "assertion_id": assertion_id,
            "result": assertion["result"],
            "expected": assertion["expected"],
            "observed": assertion["observed"],
            "evidence_refs": [f"{models.CONFORMANCE_ASSERTIONS_JSON.as_posix()}#/assertions/{assertion_id}"],
        }
        if assertion["result"] != "PASS":
            result["failure_details"] = assertion["observed"]
        results.append(result)
    passed_count = sum(1 for item in results if item["result"] == "PASS")
    status = "PASS_WITH_WARNINGS" if passed_count == len(results) and validation_report.get("validation_status") in {"PASS", "PASS_WITH_WARNINGS"} else "FAILED_VALIDATION"
    return {
        "schema_version": "aide.dominium-readonly-seam.conformance-results.v2",
        "task_id": models.REPAIR_TASK_ID,
        "status": status,
        "expectation_count": len(results),
        "passed_count": passed_count,
        "results": results,
        "aggregate_validation_status": validation_report.get("validation_status"),
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }
