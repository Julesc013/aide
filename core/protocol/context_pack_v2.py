"""Minimal AIDE ContextPack v2 helpers.

This module projects one deterministic, evidence-bound ContextPack record. The
record references accepted queue, protocol, evidence, OKF, Reconciler,
capability, conformance, and non-capability surfaces. It does not execute
workers, call models, fetch network data, admit adapters, grant trust, apply
patches, or mutate repositories.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from core.protocol import envelope, reference_id


API_VERSION = envelope.API_VERSION
CONTEXT_PACK_SCHEMA_VERSION = "aide.context-pack.v2"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "context_pack_v2"
TASK_ID = "AIDE-RESUME-BUILD-CONTEXTPACK-V2-01"
RECOMMENDED_NEXT_TASK = "AIDE-RESUME-CHECK-CONTEXTPACK-V2-01"
DETERMINISTIC_TIMESTAMP = "2026-06-20T00:00:00+10:00"

CONTEXT_PACK_ID = "minimal-context-pack-v2-01"
CONTEXT_PACK_REF = reference_id.format_reference_id("context-pack", CONTEXT_PACK_ID)
PATCH_TRANSACTION_CAPABILITY_REF = reference_id.format_reference_id("capability", "minimal_patch_transaction_schema")
ADAPTER_MANIFEST_CAPABILITY_REF = reference_id.format_reference_id("capability", "minimal_adapter_manifest_schema")
CONFORMANCE_RESULT_REF = reference_id.format_reference_id("conformance-result", "minimal_capability_manifest-v1.0.0-evidence-projection-01")

REPORT_ROOT = Path(".aide/reports/context-pack-v2-resume")
SCHEMA_PATH = Path(".aide/protocol/aide-context-pack-v2.schema.json")
PACK_JSON = REPORT_ROOT / "context-pack.json"
PACK_MD = REPORT_ROOT / "context-pack.md"
PACK_INDEX_JSON = REPORT_ROOT / "context-pack-index.json"
PACK_INDEX_MD = REPORT_ROOT / "context-pack-index.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
STATUS_MD = REPORT_ROOT / "status.md"
SOURCE_REVIEW_MD = REPORT_ROOT / "source-review.md"
BOUNDARY_MD = REPORT_ROOT / "execution-boundary.md"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"

REQUIRED_REPORTS = [
    STATUS_MD,
    PACK_JSON,
    PACK_MD,
    PACK_INDEX_JSON,
    PACK_INDEX_MD,
    PROJECTION_JSON,
    PROJECTION_MD,
    VALIDATION_JSON,
    VALIDATION_MD,
    SOURCE_REVIEW_MD,
    BOUNDARY_MD,
    EXPLICIT_NON_CAPABILITIES_MD,
    FUTURE_WORK_MD,
    NEXT_TASK_PROMPT_MD,
]

RECOGNIZED_CAPABILITY_REFS = {
    PATCH_TRANSACTION_CAPABILITY_REF,
    ADAPTER_MANIFEST_CAPABILITY_REF,
    reference_id.format_reference_id("capability", "minimal_evidence_packet_schema"),
    reference_id.format_reference_id("capability", "minimal_workunit_queue_v1"),
    reference_id.format_reference_id("capability", "minimal_worker_run_schema"),
    reference_id.format_reference_id("capability", "minimal_test_job_schema"),
}

REQUIRED_SECTION_IDS = {
    "work_unit",
    "scope",
    "protocol_baseline",
    "evidence",
    "okf",
    "reconciler",
    "capability_conformance",
    "explicit_non_capabilities",
}

EXPLICIT_NON_CAPABILITIES = [
    "model_calls",
    "provider_calls",
    "gateway_calls",
    "network_calls",
    "embedding_generation",
    "agent_execution",
    "worker_execution",
    "test_execution",
    "command_execution",
    "adapter_admission",
    "adapter_trust",
    "patch_application",
    "target_repository_mutation",
    "branch_worktree_automation",
    "runtime",
    "service",
    "scheduler",
    "leases",
    "supervisor",
    "test_broker_runtime",
    "commander",
    "workbench",
    "release",
    "promotion",
    "production_readiness",
]

VALIDATION_WARNINGS = [
    "ContextPack v2 is a deterministic projection only; it does not execute agents or commands.",
    "No model/provider/Gateway/network calls, embeddings, admission, trust, patch apply, target mutation, runtime, Service, Commander, or Workbench behavior exists.",
    "Pack sources are referenced by path and hash; no live resolver or event store exists.",
]

FALSE_STATUS_FIELDS = [
    "model_call_performed",
    "network_call_performed",
    "embedding_performed",
    "agent_started",
    "worker_started",
    "command_executed",
    "patch_applied",
    "repository_mutated",
    "trusted",
]


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


def load_context_pack_schema(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / SCHEMA_PATH
    if not path.exists():
        raise ValueError(f"ContextPack v2 schema missing: {SCHEMA_PATH.as_posix()}")
    return read_json(path)


def source_artifact_paths(repo_root: str | Path | None = None) -> list[str]:
    _root = Path(repo_root) if repo_root is not None else Path(".")
    return [
        ".aide/protocol/aide-context-pack-v2.schema.json",
        "core/protocol/context_pack_v2.py",
        ".aide/scripts/aide_lite.py",
        ".aide/scripts/tests/test_aide_context_pack_v2.py",
        ".aide/queue/AIDE-BUILD-CONTEXTPACK-V2-01/status.yaml",
        ".aide/queue/AIDE-RESUME-BUILD-CONTEXTPACK-V2-01/status.yaml",
        ".aide/reports/adapter-manifest-resume-accept/acceptance-report.json",
        ".aide/reports/adapter-manifest-resume-check/check-report.json",
        ".aide/reports/patch-transaction-resume-accept/acceptance-report.json",
        ".aide/reports/conformance-result-accept/acceptance-report.json",
        ".aide/reports/capability-manifest/validation.json",
        ".aide/reports/conformance-result/validation.json",
        ".aide/reports/reconciler/validation.json",
        ".aide/knowledge/okf/index.md",
    ]


def _hash_existing(root: Path, rels: list[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel in rels:
        path = root / rel
        if path.exists():
            hashes[rel] = sha256_file(path)
    return hashes


def _compatibility() -> dict[str, Any]:
    return {
        "schemaVersion": PROTOCOL_VERSION,
        "protocolVersion": PROTOCOL_VERSION,
        "minReaderVersion": PROTOCOL_VERSION,
        "minWriterVersion": PROTOCOL_VERSION,
        "featureFlags": [FEATURE_FLAG],
        "requiredCapabilities": [FEATURE_FLAG, "minimal_patch_transaction_schema", "minimal_adapter_manifest_schema"],
    }


def _source(root: Path, rel: str, role: str, kind: str) -> dict[str, Any]:
    path = root / rel
    exists = path.exists()
    return {
        "ref": reference_id.format_reference_id("source" if kind == "source" else "report", role),
        "role": role,
        "kind": kind,
        "path": rel,
        "exists": exists,
        "sha256": sha256_file(path) if exists and path.is_file() else None,
    }


def _source_refs(root: Path) -> list[dict[str, Any]]:
    sources = [
        (".aide/queue/AIDE-RESUME-ACCEPT-ADAPTER-MANIFEST-01/status.yaml", "adapter_manifest_resume_acceptance_status", "source"),
        (".aide/queue/AIDE-BUILD-CONTEXTPACK-V2-01/status.yaml", "original_blocked_contextpack_status", "source"),
        (".aide/queue/AIDE-RESUME-BUILD-CONTEXTPACK-V2-01/status.yaml", "contextpack_resume_build_status", "source"),
        (".aide/reports/adapter-manifest-resume-accept/acceptance-report.json", "adapter_manifest_resume_acceptance", "report"),
        (".aide/reports/adapter-manifest-resume-check/check-report.json", "adapter_manifest_resume_check", "report"),
        (".aide/reports/patch-transaction-resume-accept/acceptance-report.json", "patch_transaction_resume_acceptance", "report"),
        (".aide/reports/conformance-result-accept/acceptance-report.json", "conformance_result_acceptance", "report"),
        (".aide/reports/capability-manifest/validation.json", "capability_manifest_validation", "report"),
        (".aide/reports/conformance-result/validation.json", "conformance_result_validation", "report"),
        (".aide/reports/reconciler/validation.json", "reconciler_validation", "report"),
        (".aide/knowledge/okf/index.md", "okf_index", "source"),
        ("PLANS.md", "plans_index", "source"),
        ("IMPLEMENT.md", "implementation_log", "source"),
    ]
    return [_source(root, rel, role, kind) for rel, role, kind in sources]


def _sections(source_refs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    roles_by_section = {
        "work_unit": ["original_blocked_contextpack_status", "contextpack_resume_build_status"],
        "scope": ["adapter_manifest_resume_acceptance_status"],
        "protocol_baseline": ["patch_transaction_resume_acceptance", "adapter_manifest_resume_acceptance"],
        "evidence": ["adapter_manifest_resume_check", "conformance_result_acceptance"],
        "okf": ["okf_index"],
        "reconciler": ["reconciler_validation"],
        "capability_conformance": ["capability_manifest_validation", "conformance_result_validation"],
        "explicit_non_capabilities": ["adapter_manifest_resume_acceptance", "plans_index", "implementation_log"],
    }
    role_map = {item["role"]: item for item in source_refs}
    sections: list[dict[str, Any]] = []
    for section_id in sorted(roles_by_section):
        refs = [role_map[role]["ref"] for role in roles_by_section[section_id] if role in role_map]
        sections.append({"id": section_id, "source_refs": refs, "item_count": len(refs)})
    return sections


def build_context_pack(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    sources = _source_refs(root)
    return {
        "apiVersion": API_VERSION,
        "kind": "ContextPack",
        "schema_version": CONTEXT_PACK_SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "metadata": {
            "id": CONTEXT_PACK_ID,
            "name": "Minimal ContextPack v2",
            "createdAt": DETERMINISTIC_TIMESTAMP,
            "sourcePath": PACK_JSON.as_posix(),
            "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
            "compatibility": _compatibility(),
        },
        "spec": {
            "context_pack_ref": CONTEXT_PACK_REF,
            "purpose": "bounded_agent_context_projection",
            "work_unit_ref": reference_id.format_reference_id("queue-task", TASK_ID),
            "source_refs": sources,
            "sections": _sections(sources),
            "allowed_paths": [
                ".aide/queue/AIDE-RESUME-BUILD-CONTEXTPACK-V2-01/**",
                ".aide/reports/context-pack-v2-resume/**",
                ".aide/protocol/aide-context-pack-v2.schema.json",
                "core/protocol/context_pack_v2.py",
                ".aide/scripts/tests/test_aide_context_pack_v2.py",
            ],
            "forbidden_paths": [
                ".git/**",
                ".github/**",
                ".aide.local/**",
                ".env",
                "secrets/**",
                "credentials/**",
                "target repositories",
                "runtime/provider/host/VCS mutation",
            ],
            "required_capability_refs": [
                PATCH_TRANSACTION_CAPABILITY_REF,
                ADAPTER_MANIFEST_CAPABILITY_REF,
                reference_id.format_reference_id("capability", "minimal_evidence_packet_schema"),
                reference_id.format_reference_id("capability", "minimal_workunit_queue_v1"),
                reference_id.format_reference_id("capability", "minimal_worker_run_schema"),
                reference_id.format_reference_id("capability", "minimal_test_job_schema"),
            ],
            "required_conformance_result_refs": [CONFORMANCE_RESULT_REF],
            "required_evidence_refs": [
                reference_id.format_reference_id("evidence", "adapter-manifest-resume-acceptance"),
                reference_id.format_reference_id("evidence", "patch-transaction-resume-acceptance"),
            ],
            "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        },
        "status": {
            "validation_performed": True,
            "validation_status": "PASS_WITH_WARNINGS",
            "validation_errors": [],
            "validation_warnings": list(VALIDATION_WARNINGS),
            "model_call_performed": False,
            "network_call_performed": False,
            "embedding_performed": False,
            "agent_started": False,
            "worker_started": False,
            "command_executed": False,
            "patch_applied": False,
            "repository_mutated": False,
            "trusted": False,
        },
    }


def _validate_ref(value: Any, expected_kind: str) -> list[str]:
    result = reference_id.validate_reference_id(value, required=True)
    errors = list(result.errors)
    kind = result.parsed.kind if result.parsed is not None else ""
    if result.valid and kind != expected_kind:
        errors.append(f"reference kind must be {expected_kind}: {value}")
    return errors


def _validate_repo_rel_path(value: Any) -> list[str]:
    if not isinstance(value, str) or not value:
        return ["path must be a non-empty string"]
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or ".." in normalized.split("/") or normalized in {".", ""}:
        return [f"path is not safe repo-relative: {value}"]
    return []


def validate_context_pack_with_schema(record: dict[str, Any], schema: dict[str, Any] | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings = list(VALIDATION_WARNINGS)
    if record.get("apiVersion") != API_VERSION:
        errors.append("apiVersion mismatch")
    if record.get("kind") != "ContextPack":
        errors.append("kind must be ContextPack")
    for field in ["metadata", "spec", "status"]:
        if not isinstance(record.get(field), dict):
            errors.append(f"{field} must be an object")
    spec = record.get("spec", {})
    status = record.get("status", {})
    errors.extend(_validate_ref(spec.get("context_pack_ref"), "context-pack"))
    if spec.get("context_pack_ref") != CONTEXT_PACK_REF:
        errors.append(f"context_pack_ref must be stable: {CONTEXT_PACK_REF}")
    sources = spec.get("source_refs", [])
    if not isinstance(sources, list) or not sources:
        errors.append("source_refs must be a non-empty array")
        sources = []
    for item in sources:
        if not isinstance(item, dict):
            errors.append("source_refs items must be objects")
            continue
        errors.extend(_validate_repo_rel_path(item.get("path")))
        if item.get("exists") is not True:
            errors.append(f"source path must exist: {item.get('path')}")
        sha = item.get("sha256")
        if (
            not isinstance(sha, str)
            or not sha.startswith("sha256:")
            or len(sha) != 71
            or any(ch not in "0123456789abcdef" for ch in sha[7:])
        ):
            errors.append(f"source sha256 must be sha256:<64-hex>: {item.get('path')}")
    sections = spec.get("sections", [])
    section_ids = {item.get("id") for item in sections if isinstance(item, dict)}
    missing = sorted(REQUIRED_SECTION_IDS - section_ids)
    if missing:
        errors.append(f"missing required sections: {', '.join(missing)}")
    for ref in spec.get("required_capability_refs", []):
        errors.extend(_validate_ref(ref, "capability"))
        if isinstance(ref, str) and ref not in RECOGNIZED_CAPABILITY_REFS:
            errors.append(f"unknown capability ref: {ref}")
    for ref in spec.get("required_conformance_result_refs", []):
        errors.extend(_validate_ref(ref, "conformance-result"))
    for ref in spec.get("required_evidence_refs", []):
        errors.extend(_validate_ref(ref, "evidence"))
    if spec.get("explicit_non_capabilities") != EXPLICIT_NON_CAPABILITIES:
        errors.append("explicit_non_capabilities mismatch")
    for field in FALSE_STATUS_FIELDS:
        if status.get(field) is not False:
            errors.append(f"status.{field} must be false")
    if schema:
        required = schema.get("required", [])
        for field in required:
            if field not in record:
                errors.append(f"schema required field missing: {field}")
    return errors, warnings


def build_context_pack_index(record: dict[str, Any]) -> dict[str, Any]:
    spec = record["spec"]
    return {
        "schema_version": "aide.context-pack-index.v2",
        "kind": "ContextPackIndex",
        "task_id": TASK_ID,
        "context_pack_ref": spec["context_pack_ref"],
        "section_count": len(spec["sections"]),
        "source_ref_count": len(spec["source_refs"]),
        "required_capability_refs": spec["required_capability_refs"],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def context_pack_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    schema_loaded = False
    try:
        load_context_pack_schema(root)
        schema_loaded = True
    except ValueError:
        pass
    record = build_context_pack(root)
    errors, warnings = validate_context_pack_with_schema(record, {})
    return {
        "schema_version": "aide.context-pack-status.v2",
        "task_id": TASK_ID,
        "status": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "capability_target": FEATURE_FLAG,
        "schema_loaded": schema_loaded,
        "record_count": 1,
        "section_count": len(record["spec"]["sections"]),
        "source_ref_count": len(record["spec"]["source_refs"]),
        "record_valid": not errors,
        "validation_errors": errors,
        "warnings": warnings,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        **_false_status(),
    }


def _false_status() -> dict[str, bool]:
    return {
        "model_call_performed": False,
        "network_call_performed": False,
        "embedding_performed": False,
        "agent_started": False,
        "worker_started": False,
        "command_executed": False,
        "patch_applied": False,
        "repository_mutated": False,
        "trusted": False,
    }


def write_context_pack_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    sources = source_artifact_paths(root)
    before = _hash_existing(root, sources)
    schema = load_context_pack_schema(root)
    record = build_context_pack(root)
    errors, warnings = validate_context_pack_with_schema(record, schema)
    status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    record["status"]["validation_status"] = status
    record["status"]["validation_errors"] = errors
    record["status"]["validation_warnings"] = warnings
    index = build_context_pack_index(record)
    index["status"] = status
    write_json(root / PACK_JSON, {"schema_version": "aide.context-pack-records.v2", "context_packs": [record]})
    write_text(root / PACK_MD, render_pack_markdown(record))
    write_json(root / PACK_INDEX_JSON, index)
    write_text(root / PACK_INDEX_MD, render_index_markdown(index))
    write_text(root / SOURCE_REVIEW_MD, render_source_review_markdown(record))
    write_text(root / BOUNDARY_MD, render_boundary_markdown())
    write_text(root / EXPLICIT_NON_CAPABILITIES_MD, render_explicit_non_capabilities_markdown())
    write_text(root / FUTURE_WORK_MD, render_future_work_markdown())
    write_text(root / NEXT_TASK_PROMPT_MD, render_next_task_prompt())
    validation = validate_context_pack(root, project=False)
    after = _hash_existing(root, sources)
    report = {
        "schema_version": "aide.context-pack-projection.v2",
        "kind": "ContextPackProjectionReport",
        "task_id": TASK_ID,
        "status": validation["validation_status"],
        "context_pack_ref": CONTEXT_PACK_REF,
        "record_valid": validation["record_valid"],
        "source_artifacts_mutated": before != after,
        "source_ref_count": len(record["spec"]["source_refs"]),
        "section_count": len(record["spec"]["sections"]),
        "reports_written": [path.as_posix() for path in REQUIRED_REPORTS],
        "warnings": validation["warnings"],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        **_false_status(),
    }
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    write_text(root / STATUS_MD, render_status_markdown({**validation, "projection_exists": True}))
    return report


def validate_context_pack(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    projection = write_context_pack_reports(root) if project else {"status": "PASS_WITH_WARNINGS"}
    schema_errors: list[str] = []
    try:
        schema = load_context_pack_schema(root)
        schema_loaded = True
    except ValueError as exc:
        schema = {}
        schema_loaded = False
        schema_errors.append(str(exc))
    record = build_context_pack(root)
    record_errors, warnings = validate_context_pack_with_schema(record, schema)
    errors = [*schema_errors, *record_errors]
    checks = {
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "schema_file_parsed": schema_loaded,
        "helper_exists": (root / "core/protocol/context_pack_v2.py").exists(),
        "cli_registered": _cli_registered(root),
        "reports_generated": all((root / rel).exists() for rel in REQUIRED_REPORTS if rel not in {VALIDATION_JSON, VALIDATION_MD, PROJECTION_JSON, PROJECTION_MD, STATUS_MD}),
        "record_valid": not record_errors,
        "context_pack_ref_valid": not _validate_ref(record["spec"]["context_pack_ref"], "context-pack"),
        "required_sections_present": REQUIRED_SECTION_IDS <= {item.get("id") for item in record["spec"]["sections"]},
        "source_refs_exist": all(item.get("exists") is True for item in record["spec"]["source_refs"]),
        "explicit_non_capabilities_preserved": record["spec"]["explicit_non_capabilities"] == EXPLICIT_NON_CAPABILITIES,
        "no_execution_facts_preserved": all(record["status"].get(field) is False for field in FALSE_STATUS_FIELDS),
    }
    failed = [key for key, value in checks.items() if value is not True]
    errors.extend(f"failed check: {item}" for item in failed)
    status = "PASS_WITH_WARNINGS" if not errors and projection.get("status") in {"PASS", "PASS_WITH_WARNINGS"} else "FAILED_VALIDATION"
    report = {
        "schema_version": "aide.context-pack-validation.v2",
        "kind": "ContextPackValidationReport",
        "task_id": TASK_ID,
        "validation_status": status,
        "status": status,
        "capability_target": FEATURE_FLAG,
        "validation_errors": errors,
        "warnings": warnings,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        **checks,
        **_false_status(),
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_markdown(report))
    write_text(root / STATUS_MD, render_status_markdown(report))
    return report


def _cli_registered(root: Path) -> bool:
    path = root / ".aide/scripts/aide_lite.py"
    return path.exists() and "context-pack-v2" in path.read_text(encoding="utf-8")


def render_status_markdown(data: dict[str, Any]) -> str:
    return "\n".join([
        "# ContextPack v2 Status",
        "",
        f"- task_id: {TASK_ID}",
        f"- capability_target: {FEATURE_FLAG}",
        f"- status: {data.get('validation_status', data.get('status'))}",
        f"- record_valid: {str(data.get('record_valid', False)).lower()}",
        f"- section_count: {data.get('section_count', '')}",
        f"- source_ref_count: {data.get('source_ref_count', '')}",
        f"- recommended_next_task: {RECOMMENDED_NEXT_TASK}",
        "",
    ])


def render_pack_markdown(record: dict[str, Any]) -> str:
    lines = ["# ContextPack v2 Record", "", f"- context_pack_ref: `{record['spec']['context_pack_ref']}`", ""]
    lines.append("## Sections")
    for section in record["spec"]["sections"]:
        lines.append(f"- {section['id']}: {section['item_count']} refs")
    lines.append("")
    lines.append("## Sources")
    for source in record["spec"]["source_refs"]:
        lines.append(f"- `{source['path']}` exists={str(source['exists']).lower()} sha256={source['sha256']}")
    lines.append("")
    return "\n".join(lines)


def render_index_markdown(index: dict[str, Any]) -> str:
    return (
        "# ContextPack v2 Index\n\n"
        f"- context_pack_ref: `{index['context_pack_ref']}`\n"
        f"- source_ref_count: {index['source_ref_count']}\n"
        f"- section_count: {index['section_count']}\n"
        f"- status: {index.get('status')}\n"
    )


def render_projection_markdown(report: dict[str, Any]) -> str:
    return (
        "# ContextPack v2 Projection Report\n\n"
        f"- status: {report.get('status')}\n"
        f"- context_pack_ref: `{report.get('context_pack_ref')}`\n"
        f"- source_artifacts_mutated: {str(report.get('source_artifacts_mutated', False)).lower()}\n"
        f"- recommended_next_task: {report.get('recommended_next_task')}\n"
    )


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = ["# ContextPack v2 Validation", "", f"- validation_status: {report.get('validation_status')}", ""]
    if report.get("validation_errors"):
        lines.append("## Errors")
        for error in report["validation_errors"]:
            lines.append(f"- {error}")
    lines.append("## Warnings")
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    lines.append("")
    return "\n".join(lines)


def render_source_review_markdown(record: dict[str, Any]) -> str:
    return (
        "# ContextPack v2 Source Review\n\n"
        "The pack references source and report files by repo-relative path and sha256. "
        "It does not embed raw repository dumps or resolve external resources.\n"
    )


def render_boundary_markdown() -> str:
    return (
        "# ContextPack v2 Execution Boundary\n\n"
        "- model_call_performed: false\n"
        "- network_call_performed: false\n"
        "- embedding_performed: false\n"
        "- agent_started: false\n"
        "- worker_started: false\n"
        "- command_executed: false\n"
        "- patch_applied: false\n"
        "- repository_mutated: false\n"
        "- trusted: false\n"
    )


def render_explicit_non_capabilities_markdown() -> str:
    lines = ["# ContextPack v2 Explicit Non-Capabilities", ""]
    lines.extend(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES)
    lines.append("")
    return "\n".join(lines)


def render_future_work_markdown() -> str:
    return (
        "# ContextPack v2 Future Work\n\n"
        "- independent check and acceptance\n"
        "- richer source selection policy\n"
        "- evidence normalization integration\n"
        "- eventual worker/runtime consumption after separate gates\n"
    )


def render_next_task_prompt() -> str:
    return (
        "# AIDE-RESUME-CHECK-CONTEXTPACK-V2-01\n\n"
        "Create and process `AIDE-RESUME-CHECK-CONTEXTPACK-V2-01`.\n\n"
        "Preserve the original blocked `AIDE-CHECK-CONTEXTPACK-V2-01` record. "
        "Independently check the resume ContextPack v2 build for schema/helper "
        "alignment, source hash integrity, deterministic projection, evidence "
        "linkage, no execution, no model/network calls, no admission, no trust, "
        "no patch apply, and complete evidence.\n"
    )
