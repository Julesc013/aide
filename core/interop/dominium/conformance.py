"""Conformance expectations for the Dominium read-only seam."""

from __future__ import annotations

from typing import Any

from . import models


EXPECTATIONS = [
    "contract parsing",
    "stable identity",
    "read-only source access",
    "no cross-repo writes",
    "deterministic snapshot",
    "deterministic projection",
    "source digest binding",
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


def conformance_results(validation_report: dict[str, Any]) -> dict[str, Any]:
    passed = validation_report.get("validation_status") in {"PASS", "PASS_WITH_WARNINGS"}
    results = [
        {
            "id": item["id"],
            "description": item["description"],
            "result": "PASS" if passed else "FAILED_VALIDATION",
            "evidence": models.VALIDATION_JSON.as_posix(),
        }
        for item in conformance_expectations()
    ]
    return {
        "schema_version": "aide.dominium-readonly-seam.conformance-results.v0",
        "task_id": models.TASK_ID,
        "status": "PASS_WITH_WARNINGS" if passed else "FAILED_VALIDATION",
        "expectation_count": len(results),
        "passed_count": sum(1 for item in results if item["result"] == "PASS"),
        "results": results,
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }
