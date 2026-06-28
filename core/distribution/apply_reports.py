"""Report renderers for DistributionApplyEngine v0."""

from __future__ import annotations

from typing import Any


def status_md(data: dict[str, Any]) -> str:
    lines = [
        "# DistributionApplyEngine v0 Status",
        "",
        f"- result: `{data.get('status')}`",
        f"- proposed_capability: `{data.get('proposed_capability')}`",
        f"- fixture_only: `{str(data.get('fixture_only', False)).lower()}`",
        f"- temp_workspace_only: `{str(data.get('temp_workspace_only', False)).lower()}`",
        f"- scenario_count: `{data.get('scenario_count')}`",
        f"- recommended_next_task: `{data.get('recommended_next_task')}`",
        "",
        "## Boundary",
        "",
        "- real_target_apply: false",
        "- source_repo_apply: false",
        "- release_publication: false",
        "- provider_model_network_calls: false",
    ]
    return "\n".join(lines) + "\n"

def validation_md(report: dict[str, Any]) -> str:
    lines = [
        "# DistributionApplyEngine v0 Validation",
        "",
        f"- result: `{report.get('validation_status')}`",
        f"- material_finding_count: `{report.get('material_finding_count')}`",
        f"- missing_evidence: `{report.get('missing_evidence')}`",
        f"- recommended_next_task: `{report.get('recommended_next_task')}`",
        "",
        "## Scenario Results",
        "",
        "| Scenario | Expected | Observed | Code | Pass |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report.get("scenario_results", []):
        lines.append(
            f"| {item.get('scenario_id')} | {item.get('expected_result')} | {item.get('status')} | {item.get('refusal_code') or 'none'} | {str(item.get('passed')).lower()} |"
        )
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def refusal_summary_md(report: dict[str, Any]) -> str:
    lines = [
        "# DistributionApplyEngine v0 Refusal Summary",
        "",
        "| Scenario | Refusal Code | Expected |",
        "| --- | --- | --- |",
    ]
    for item in report.get("scenario_results", []):
        if item.get("refusal_code"):
            lines.append(f"| {item.get('scenario_id')} | {item.get('refusal_code')} | {str(item.get('passed')).lower()} |")
    return "\n".join(lines) + "\n"


def no_target_apply_boundary_md() -> str:
    return "\n".join(
        [
            "# DistributionApplyEngine v0 No-Target-Apply Boundary",
            "",
            "DistributionApplyEngine v0 may mutate only a copied temporary fixture workspace.",
            "",
            "It does not:",
            "",
            "- apply to real target repositories;",
            "- apply to the source repository;",
            "- mutate ScreenSave, Eureka, Dominium, or external repositories;",
            "- create release archives, tags, uploads, or GitHub Releases;",
            "- call provider, model, or network services;",
            "- authorize self-update or production update behavior.",
        ]
    ) + "\n"


def canonical_fixture_preservation_md(report: dict[str, Any]) -> str:
    lines = [
        "# DistributionApplyEngine v0 Canonical Fixture Preservation",
        "",
        f"- canonical_fixture_unchanged: `{str(report.get('canonical_fixture_unchanged', False)).lower()}`",
        f"- source_repo_apply_occurred: `{str(report.get('source_repo_apply_occurred', False)).lower()}`",
        f"- temp_workspace_retained: `{str(report.get('temp_workspace_retained', False)).lower()}`",
        "",
        "Canonical scenario files are hashed before and after each temp run. The engine does not edit canonical fixture directories during execution.",
    ]
    return "\n".join(lines) + "\n"
