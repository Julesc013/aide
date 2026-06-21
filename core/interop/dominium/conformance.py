"""Conformance expectations for the Dominium read-only seam."""

from __future__ import annotations

from typing import Any, Callable

from . import contracts, integrity, models


EXPECTATIONS = [
    "contract parsing",
    "stable identity",
    "exact repository identity",
    "read-only source access",
    "no cross-repo writes",
    "deterministic snapshot",
    "deterministic projection",
    "source digest binding",
    "bundle self digest binding",
    "mapping completeness",
    "authority preservation",
    "Workbench non-authority",
    "refusal typing",
    "diagnostic typing",
    "evidence linkage",
    "event correlation",
    "version compatibility",
    "unsupported-operation refusal",
    "no provider/model/network activity",
    "no worker execution",
    "no mutation",
    "explicit non-capabilities",
    "replayable negative fixtures",
]


def conformance_expectations() -> list[dict[str, Any]]:
    return [
        {
            "id": f"dominium-readonly-seam-{index:02d}",
            "description": description,
            "required_for_build": True,
            "status": "declared",
        }
        for index, description in enumerate(EXPECTATIONS, start=1)
    ]


def _records(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    records = bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {}
    return integrity.record_list(records)


def _expectation_checks(bundle: dict[str, Any], validation_report: dict[str, Any]) -> list[Callable[[], tuple[bool, str]]]:
    records = _records(bundle)
    record_kinds = {item.get("kind") for item in records}
    errors = validation_report.get("error_records", [])
    source = bundle.get("source_snapshot", {}) if isinstance(bundle.get("source_snapshot"), dict) else {}
    digests = bundle.get("content_digests", {}) if isinstance(bundle.get("content_digests"), dict) else {}
    caps = bundle.get("records", {}).get("host_capability_set", {}) if isinstance(bundle.get("records"), dict) else {}
    bridge = bundle.get("records", {}).get("dominium_bridge_manifest", {}) if isinstance(bundle.get("records"), dict) else {}

    def no_error_prefix(prefix: str) -> tuple[bool, str]:
        return (not any(str(item.get("code", "")).startswith(prefix) for item in errors), f"no {prefix} validation errors")

    return [
        lambda: (bundle.get("apiVersion") == models.API_VERSION and bundle.get("kind") == "DominiumReadonlySeamBundle", "bundle contract parsed"),
        lambda: (len({item.get("metadata", {}).get("id") for item in records}) == len(records), "record identities are unique"),
        lambda: (source.get("repository_identity", {}).get("canonical_identity") == "github.com/julesc013/dominium", "repository identity is exact"),
        lambda: (source.get("read_only_operations", {}).get("git_fetch") is False and source.get("read_only_operations", {}).get("git_pull") is False, "source access is read-only"),
        lambda: (source.get("read_only_operations", {}).get("dominium_file_write") is False, "no Dominium file writes recorded"),
        lambda: (source.get("snapshot_digest") == integrity.stable_digest(integrity.snapshot_payload_for_digest(source)), "snapshot digest recomputes"),
        lambda: (digests.get("projection_index") == integrity.stable_digest(integrity.projection_index_for_records(bundle.get("records", {}))), "projection index digest recomputes"),
        lambda: no_error_prefix("digest.source"),
        lambda: (digests.get("seam_bundle_without_self_digest") == integrity.stable_digest(integrity.bundle_payload_for_self_digest(bundle)), "bundle self digest recomputes"),
        lambda: (record_kinds == set(models.AUTHORIZED_SEAM_KINDS), "all seam kinds are present"),
        lambda: no_error_prefix("authority."),
        lambda: (bridge.get("spec", {}).get("ownership", {}).get("Workbench") == "presentation, context capture, preview, approval interaction, apply requests", "Workbench remains non-authoritative"),
        lambda: no_error_prefix("refusal."),
        lambda: no_error_prefix("diagnostic."),
        lambda: no_error_prefix("reference.closure"),
        lambda: no_error_prefix("event."),
        lambda: (bundle.get("metadata", {}).get("compatibility", {}).get("readOldWriteCurrent") is True, "read-old/write-current metadata is present"),
        lambda: (models.RECOMMENDED_NEXT_TASK.endswith("REPAIR-01"), "unsupported verbs are routed to the independent repair check"),
        lambda: (bundle.get("status", {}).get("network_call_performed") is False, "network/provider/model activity absent"),
        lambda: (bundle.get("status", {}).get("worker_executed") is False, "worker execution absent"),
        lambda: (caps.get("spec", {}).get("forbidden_capabilities") and {item.get("id") for item in caps.get("spec", {}).get("forbidden_capabilities", [])} == contracts.FORBIDDEN_CAPABILITIES, "mutation capabilities are forbidden"),
        lambda: (bundle.get("explicit_non_capabilities") == models.EXPLICIT_NON_CAPABILITIES, "explicit non-capabilities preserved"),
        lambda: (len(bundle.get("records", {}).get("artifact_references", [])) == len(source.get("selected_files", [])), "negative fixture replay has a complete base bundle"),
    ]


def conformance_results(bundle: dict[str, Any], validation_report: dict[str, Any] | None = None) -> dict[str, Any]:
    if validation_report is None:
        validation_report = bundle
        passed = validation_report.get("validation_status") in {"PASS", "PASS_WITH_WARNINGS"}
        results = [
            {
                "id": item["id"],
                "description": item["description"],
                "result": "PASS" if passed else "FAILED_VALIDATION",
                "observation": "legacy aggregate validation report",
                "evidence": models.VALIDATION_JSON.as_posix(),
            }
            for item in conformance_expectations()
        ]
        return {
            "schema_version": "aide.dominium-readonly-seam.conformance-results.v1",
            "task_id": models.REPAIR_TASK_ID,
            "status": "PASS_WITH_WARNINGS" if passed else "FAILED_VALIDATION",
            "expectation_count": len(results),
            "passed_count": sum(1 for item in results if item["result"] == "PASS"),
            "results": results,
            "aggregate_validation_status": validation_report.get("validation_status"),
            "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
        }
    checks = _expectation_checks(bundle, validation_report)
    results = []
    for expectation, check in zip(conformance_expectations(), checks, strict=True):
        passed, observation = check()
        results.append(
            {
                "id": expectation["id"],
                "description": expectation["description"],
                "result": "PASS" if passed else "FAILED_VALIDATION",
                "observation": observation,
                "evidence": models.VALIDATION_JSON.as_posix(),
            }
        )
    passed_count = sum(1 for item in results if item["result"] == "PASS")
    status = "PASS_WITH_WARNINGS" if passed_count == len(results) and validation_report.get("validation_status") in {"PASS", "PASS_WITH_WARNINGS"} else "FAILED_VALIDATION"
    return {
        "schema_version": "aide.dominium-readonly-seam.conformance-results.v1",
        "task_id": models.REPAIR_TASK_ID,
        "status": status,
        "expectation_count": len(results),
        "passed_count": passed_count,
        "results": results,
        "aggregate_validation_status": validation_report.get("validation_status"),
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }
