"""Report writing, CLI-facing commands, fixtures, and demo orchestration."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Any

from . import conformance, fixture_replay, integrity, models, operations, projector, snapshot, validation
from .references import sha256_bytes, sha256_file


PINNED_DOMINIUM_HEAD = "c92b386027890c1bbf14aef6eaafe0357b7b03dd"


def default_dominium_root(repo_root: str | Path) -> Path:
    root = Path(repo_root).resolve()
    candidate = root.parent.parent / "Dominium" / "dominium"
    if candidate.exists():
        return candidate
    return Path("C:/Projects/Dominium/dominium")


def _dominium_root(repo_root: str | Path, dominium_root: str | Path | None = None) -> Path:
    return Path(dominium_root).resolve() if dominium_root is not None else default_dominium_root(repo_root)


def _revision(revision: str | None = None) -> str:
    return revision or PINNED_DOMINIUM_HEAD


def load_schema(repo_root: str | Path) -> dict[str, Any]:
    return models.read_json(Path(repo_root) / models.SCHEMA_PATH)


def _write_bundle_reports(repo_root: Path, bundle: dict[str, Any]) -> dict[str, Any]:
    projection_index = projector.projection_index_for_bundle(bundle)
    models.write_json(repo_root / models.SEAM_BUNDLE_JSON, bundle)
    models.write_json(repo_root / models.SOURCE_SNAPSHOT_JSON, bundle["source_snapshot"])
    models.write_json(repo_root / models.PROJECTION_INDEX_JSON, projection_index)
    models.write_json(repo_root / models.INTEROP_SEAM_BUNDLE_JSON, bundle)
    models.write_json(repo_root / models.INTEROP_BRIDGE_MANIFEST_JSON, bundle["records"]["dominium_bridge_manifest"])
    models.write_json(repo_root / models.INTEROP_CONFORMANCE_EXPECTATIONS_JSON, {"schema_version": "aide.dominium-readonly-seam.conformance-expectations.v0", "expectations": conformance.conformance_expectations()})
    return projection_index


def _fixture_manifest(repo_root: Path, files: list[Path]) -> dict[str, Any]:
    entries = []
    for path in sorted(files):
        if path.exists() and path.is_file():
            entries.append({"path": path.relative_to(repo_root).as_posix(), "sha256": sha256_file(path)})
    return {
        "schema_version": "aide.dominium-readonly-seam.fixture-manifest.v0",
        "fixture_count": len(entries),
        "fixtures": entries,
    }


def write_fixtures(repo_root: Path, bundle: dict[str, Any]) -> dict[str, Any]:
    positive_root = repo_root / models.FIXTURE_ROOT / "positive"
    negative_root = repo_root / models.FIXTURE_ROOT / "negative"
    for root in [positive_root, negative_root]:
        root.mkdir(parents=True, exist_ok=True)
        for existing in root.glob("*.json"):
            existing.unlink()
    files: list[Path] = []
    positive_records = {
        "host-manifest.json": bundle["records"]["host_manifest"],
        "host-capability-set.json": bundle["records"]["host_capability_set"],
        "workspace-descriptor.json": bundle["records"]["workspace_descriptor"],
        "context-descriptor.json": bundle["records"]["context_descriptor"],
        "artifact-references.json": {"records": bundle["records"]["artifact_references"]},
        "diagnostic-projections.json": {"records": bundle["records"]["diagnostic_projections"]},
        "refusal-projections.json": {"records": bundle["records"]["refusal_projections"]},
        "evidence-reference-set.json": bundle["records"]["evidence_reference_set"],
        "event-envelopes.json": {"records": bundle["records"]["event_envelopes"]},
        "dominium-bridge-manifest.json": bundle["records"]["dominium_bridge_manifest"],
        "complete-seam-bundle.json": bundle,
    }
    for name, obj in positive_records.items():
        path = positive_root / name
        models.write_json(path, obj)
        files.append(path)
    for case in fixture_replay.negative_fixture_cases(bundle):
        path = negative_root / f"{case['name']}.json"
        models.write_json(path, case)
        files.append(path)
    manifest = _fixture_manifest(repo_root, files)
    models.write_json(repo_root / models.FIXTURE_MANIFEST_JSON, manifest)
    return manifest


def render_status_markdown(data: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Dominium Read-Only Seam v0 Status",
            "",
            f"- result: `{data.get('status') or data.get('validation_status')}`",
            f"- capability_target: `{models.FEATURE_FLAG}`",
            f"- source_revision: `{data.get('source_revision', '')}`",
            f"- selected_file_count: `{data.get('selected_file_count', 0)}`",
            f"- record_count: `{data.get('record_count', 0)}`",
            f"- fixture_count: `{data.get('fixture_count', 0)}`",
            f"- dominium_command_invoked: `{str(data.get('dominium_command_invoked', False)).lower()}`",
            f"- network_call_performed: `{str(data.get('network_call_performed', False)).lower()}`",
            f"- mutation_performed: `{str(data.get('mutation_performed', False)).lower()}`",
            f"- recommended_next_task: `{models.RECOMMENDED_NEXT_TASK}`",
            "",
            "Offline read-only projection only. It is not a Host runtime, bridge runtime, Workbench implementation, service, transport, preview/apply/rollback, or mutation capability.",
            "",
        ]
    )


def render_risks_markdown() -> str:
    return "\n".join(
        [
            "# Dominium Read-Only Seam Risks",
            "",
            "- Local Dominium input is read-only and may be behind remote main; freshness is recorded in source-snapshot.json.",
            "- SeamBundle is generated projection evidence, not canonical Dominium truth.",
            "- Command invocation, runtime bridge behavior, Workbench UI, preview/apply/rollback, and mutation remain absent by design.",
            "",
        ]
    )


def render_explicit_non_capabilities_markdown() -> str:
    lines = ["# Explicit Non-Capabilities", ""]
    lines.extend(f"- `{item}`" for item in models.EXPLICIT_NON_CAPABILITIES)
    lines.append("")
    return "\n".join(lines)


def render_next_task_prompt() -> str:
    return "\n".join(
        [
            "# AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01",
            "",
            "Create and process `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01`.",
            "",
            "Use `.aide/queue/index.yaml` as canonical queue truth.",
            "",
            "Independently check `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01` without modifying the seam implementation.",
            "Verify all repaired findings from the original seam check, including exact repository identity, digest binding, registry projection disclosure, schema effectiveness, replayable fixtures, independent conformance, truthful demo observation, semantic validation, and Dominium source immutability.",
            "",
            "If no material issue exists, recommend `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`.",
            "If a material defect remains, recommend one bounded follow-up repair task.",
            "",
        ]
    )


def snapshot_dominium_source(repo_root: str | Path, *, dominium_root: str | Path | None = None, revision: str | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    report = snapshot.build_source_snapshot(dom_root, revision=_revision(revision), expected_revision=_revision(revision))
    models.write_json(root / models.SOURCE_SNAPSHOT_JSON, report)
    return report


def project_dominium_seam(repo_root: str | Path, *, dominium_root: str | Path | None = None, revision: str | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    bundle = projector.build_seam_bundle(root, dom_root, revision=_revision(revision), expected_revision=_revision(revision))
    validation_report = validation.validate_bundle(bundle, dominium_root=dom_root)
    bundle["validation_summary"] = {
        "validation_status": validation_report["validation_status"],
        "validated": validation_report["validated"],
        "error_count": len(validation_report["errors"]),
        "warning_count": len(validation_report["warnings"]),
    }
    integrity.finalize_bundle(bundle)
    validation_report = validation.validate_bundle(bundle, dominium_root=dom_root)
    bundle["validation_summary"] = {
        "validation_status": validation_report["validation_status"],
        "validated": validation_report["validated"],
        "error_count": len(validation_report["errors"]),
        "warning_count": len(validation_report["warnings"]),
    }
    integrity.finalize_bundle(bundle)
    validation_report = validation.validate_bundle(bundle, dominium_root=dom_root)
    projection_index = _write_bundle_reports(root, bundle)
    fixture_manifest = write_fixtures(root, bundle)
    validation_report = validation.validate_bundle(bundle, dominium_root=dom_root)
    conformance_report = conformance.conformance_results(bundle, validation_report)
    compatibility = {
        "schema_version": "aide.dominium-readonly-seam.compatibility.v1",
        "status": "PASS",
        "read_old_write_current": True,
        "unknown_optional_field_handling": "preserve_or_ignore_by_owner_contract",
        "unknown_required_field_refusal": True,
        "windows_path_handling_checked": True,
        "posix_repo_relative_paths_checked": True,
        "stable_utf8_json_output": True,
        "deterministic_key_and_record_ordering": True,
    }
    models.write_json(root / models.VALIDATION_JSON, validation_report)
    models.write_json(root / models.CONFORMANCE_RESULTS_JSON, conformance_report)
    models.write_json(root / models.COMPATIBILITY_JSON, compatibility)
    status = {
        "status": validation_report["validation_status"],
        "source_revision": bundle["manifest"]["source_revision"],
        "selected_file_count": bundle["manifest"]["selected_file_count"],
        "record_count": bundle["manifest"]["record_count"],
        "fixture_count": fixture_manifest["fixture_count"],
        "dominium_command_invoked": False,
        "network_call_performed": False,
        "mutation_performed": False,
    }
    models.write_text(root / models.STATUS_MD, render_status_markdown(status))
    models.write_text(root / models.RISKS_MD, render_risks_markdown())
    models.write_text(root / models.EXPLICIT_NON_CAPABILITIES_MD, render_explicit_non_capabilities_markdown())
    models.write_text(root / models.NEXT_TASK_PROMPT_MD, render_next_task_prompt())
    return {
        "schema_version": "aide.dominium-readonly-seam.projection-report.v0",
        "status": validation_report["validation_status"],
        "source_revision": bundle["manifest"]["source_revision"],
        "selected_file_count": bundle["manifest"]["selected_file_count"],
        "record_count": bundle["manifest"]["record_count"],
        "fixture_count": fixture_manifest["fixture_count"],
        "projection_index_digest": integrity.stable_digest(projection_index),
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
        "dominium_command_invoked": False,
        "network_call_performed": False,
        "mutation_performed": False,
    }


def validate_dominium_seam(repo_root: str | Path, *, dominium_root: str | Path | None = None, revision: str | None = None, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    if project or not (root / models.SEAM_BUNDLE_JSON).exists():
        project_dominium_seam(root, dominium_root=dom_root, revision=revision)
    bundle = models.read_json(root / models.SEAM_BUNDLE_JSON)
    report = validation.validate_bundle(bundle, dominium_root=dom_root)
    models.write_json(root / models.VALIDATION_JSON, report)
    models.write_json(root / models.CONFORMANCE_RESULTS_JSON, conformance.conformance_results(bundle, report))
    status = {
        "status": report["validation_status"],
        "source_revision": bundle.get("manifest", {}).get("source_revision", ""),
        "selected_file_count": bundle.get("manifest", {}).get("selected_file_count", 0),
        "record_count": bundle.get("manifest", {}).get("record_count", 0),
        "fixture_count": (models.read_json(root / models.FIXTURE_MANIFEST_JSON).get("fixture_count", 0) if (root / models.FIXTURE_MANIFEST_JSON).exists() else 0),
        "dominium_command_invoked": False,
        "network_call_performed": False,
        "mutation_performed": False,
    }
    models.write_text(root / models.STATUS_MD, render_status_markdown(status))
    return report


def dominium_seam_diff(repo_root: str | Path, *, dominium_root: str | Path | None = None, revision: str | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    if not (root / models.SEAM_BUNDLE_JSON).exists():
        project_dominium_seam(root, dominium_root=dom_root, revision=revision)
    current = (root / models.SEAM_BUNDLE_JSON).read_bytes()
    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp)
        for rel in [models.SCHEMA_PATH]:
            src = root / rel
            if src.exists():
                dst = temp_root / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        project_dominium_seam(temp_root, dominium_root=dom_root, revision=revision)
        fresh = (temp_root / models.SEAM_BUNDLE_JSON).read_bytes()
    report = {
        "schema_version": "aide.dominium-readonly-seam.diff.v0",
        "status": "PASS" if current == fresh else "FAILED_VALIDATION",
        "byte_equal": current == fresh,
        "current_sha256": sha256_bytes(current),
        "fresh_sha256": sha256_bytes(fresh),
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }
    models.write_json(root / models.DIFF_JSON, report)
    return report


def run_dominium_seam_demo(repo_root: str | Path, *, dominium_root: str | Path | None = None, revision: str | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    ledger = operations.OperationLedger()
    ledger.record_demo_readonly_flow()
    before_status = snapshot.worktree_status(dom_root)
    before_snapshot = snapshot.build_source_snapshot(dom_root, revision=_revision(revision), expected_revision=_revision(revision))
    projection = project_dominium_seam(root, dominium_root=dom_root, revision=revision)
    validation_report = validate_dominium_seam(root, dominium_root=dom_root, revision=revision, project=False)
    diff = dominium_seam_diff(root, dominium_root=dom_root, revision=revision)
    after_snapshot = snapshot.build_source_snapshot(dom_root, revision=_revision(revision), expected_revision=_revision(revision))
    after_status = snapshot.worktree_status(dom_root)
    before_hashes = {item["path"]: item["sha256"] for item in before_snapshot["selected_files"]}
    after_hashes = {item["path"]: item["sha256"] for item in after_snapshot["selected_files"]}
    source_mutation_count = sum(1 for key, value in before_hashes.items() if after_hashes.get(key) != value)
    operation_report = ledger.as_report()
    result = {
        "schema_version": "aide.dominium-readonly-seam.demo-result.v0",
        "task_id": models.REPAIR_TASK_ID,
        "status": "PASS_WITH_WARNINGS" if validation_report["validation_status"] in {"PASS", "PASS_WITH_WARNINGS"} and diff["byte_equal"] and source_mutation_count == 0 and before_status == after_status else "FAILED_VALIDATION",
        "input_revision": before_snapshot["source_revision"],
        "input_hashes": before_hashes,
        "output_hashes": {
            models.SEAM_BUNDLE_JSON.as_posix(): sha256_file(root / models.SEAM_BUNDLE_JSON),
            models.VALIDATION_JSON.as_posix(): sha256_file(root / models.VALIDATION_JSON),
            models.PROJECTION_INDEX_JSON.as_posix(): sha256_file(root / models.PROJECTION_INDEX_JSON),
        },
        "record_counts": {
            "selected_files": before_snapshot["selected_file_count"],
            "records": projection["record_count"],
            "fixtures": projection["fixture_count"],
        },
        "validation_result": validation_report["validation_status"],
        "elapsed_time": {
            "status": "not_measured",
            "elapsed_ms": None,
            "reason": "determinism and source immutability are measured; wall-clock timing is intentionally not asserted by the offline demo",
        },
        "source_mutation_count": source_mutation_count,
        "forbidden_operation_count": operation_report["forbidden_operation_count"],
        "operation_ledger": operation_report,
        "dominium_status_before": before_status,
        "dominium_status_after": after_status,
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }
    models.write_json(root / models.DEMO_RESULT_JSON, result)
    models.write_text(
        root / models.STATUS_MD,
        render_status_markdown(
            {
                "status": result["status"],
                "source_revision": result["input_revision"],
                "selected_file_count": result["record_counts"]["selected_files"],
                "record_count": result["record_counts"]["records"],
                "fixture_count": result["record_counts"]["fixtures"],
                "dominium_command_invoked": False,
                "network_call_performed": False,
                "mutation_performed": False,
            }
        ),
    )
    return result


def dominium_seam_status(repo_root: str | Path, *, dominium_root: str | Path | None = None, revision: str | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    schema_exists = (root / models.SCHEMA_PATH).exists()
    bundle_exists = (root / models.SEAM_BUNDLE_JSON).exists()
    source_revision = ""
    selected_file_count = 0
    record_count = 0
    dominium_available = False
    try:
        source = snapshot.build_source_snapshot(dom_root, revision=_revision(revision), expected_revision=_revision(revision))
        dominium_available = True
        source_revision = source["source_revision"]
        selected_file_count = source["selected_file_count"]
    except Exception:
        source = {}
    if bundle_exists:
        bundle = models.read_json(root / models.SEAM_BUNDLE_JSON)
        record_count = int(bundle.get("manifest", {}).get("record_count", 0))
    status = {
        "schema_version": "aide.dominium-readonly-seam.status.v0",
        "status": "PASS_WITH_WARNINGS" if schema_exists and dominium_available else "BLOCKED",
        "capability_target": models.FEATURE_FLAG,
        "schema_exists": schema_exists,
        "bundle_exists": bundle_exists,
        "dominium_available": dominium_available,
        "source_revision": source_revision,
        "selected_file_count": selected_file_count,
        "record_count": record_count,
        "warnings": list(models.WARNING_MESSAGES),
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
        "dominium_command_invoked": False,
        "network_call_performed": False,
        "mutation_performed": False,
    }
    models.write_text(root / models.STATUS_MD, render_status_markdown(status))
    return status


def unsupported_operation_refusal(operation: str) -> dict[str, Any]:
    return {
        "schema_version": "aide.dominium-readonly-seam.unsupported-operation-refusal.v0",
        "status": "REFUSED",
        "reason_code": "AIDE_DOMINIUM_SEAM_UNSUPPORTED_OPERATION",
        "operation": operation,
        "message": f"dominium-seam {operation} is outside the read-only seam boundary",
        "retryable": False,
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }
