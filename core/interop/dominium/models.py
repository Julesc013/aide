"""Shared constants and record builders for the Dominium read-only seam."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from core.protocol import envelope


API_VERSION = envelope.API_VERSION
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
SCHEMA_VERSION = "aide.dominium-readonly-seam.v0"
PROTOCOL_VERSION = "0.1.0"
FEATURE_FLAG = "dominium_readonly_seam_v0"
TASK_ID = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01"
REPAIR_TASK_ID = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02"
DETERMINISTIC_TIMESTAMP = "2026-06-21T00:00:00+10:00"

SCHEMA_PATH = Path(".aide/protocol/aide-dominium-readonly-seam-v0.schema.json")
REPORT_ROOT = Path(".aide/reports/dominium-readonly-seam-v0")
INTEROP_ROOT = Path(".aide/interop/dominium")
FIXTURE_ROOT = Path(".aide/fixtures/dominium-readonly-seam")

STATUS_MD = REPORT_ROOT / "status.md"
SEAM_BUNDLE_JSON = REPORT_ROOT / "seam-bundle.json"
SOURCE_SNAPSHOT_JSON = REPORT_ROOT / "source-snapshot.json"
PROJECTION_INDEX_JSON = REPORT_ROOT / "projection-index.json"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
CONFORMANCE_RESULTS_JSON = REPORT_ROOT / "conformance-results.json"
CONFORMANCE_ASSERTIONS_JSON = REPORT_ROOT / "conformance-assertions.json"
COMPATIBILITY_JSON = REPORT_ROOT / "compatibility.json"
DEMO_RESULT_JSON = REPORT_ROOT / "demo-result.json"
PORTABILITY_RESULT_JSON = REPORT_ROOT / "portability-result.json"
RISKS_MD = REPORT_ROOT / "risks.md"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"
DIFF_JSON = REPORT_ROOT / "diff.json"
FIXTURE_MANIFEST_JSON = REPORT_ROOT / "fixture-manifest.json"
RUNTIME_DEPENDENCY_MANIFEST_JSON = INTEROP_ROOT / "runtime-dependency-manifest.json"

INTEROP_SEAM_BUNDLE_JSON = INTEROP_ROOT / "seam-bundle.json"
INTEROP_BRIDGE_MANIFEST_JSON = INTEROP_ROOT / "dominium-bridge-manifest.json"
INTEROP_CONFORMANCE_EXPECTATIONS_JSON = INTEROP_ROOT / "conformance-expectations.json"

REQUIRED_REPORTS = [
    STATUS_MD,
    SEAM_BUNDLE_JSON,
    SOURCE_SNAPSHOT_JSON,
    PROJECTION_INDEX_JSON,
    VALIDATION_JSON,
    CONFORMANCE_RESULTS_JSON,
    CONFORMANCE_ASSERTIONS_JSON,
    COMPATIBILITY_JSON,
    DEMO_RESULT_JSON,
    PORTABILITY_RESULT_JSON,
    RISKS_MD,
    EXPLICIT_NON_CAPABILITIES_MD,
    NEXT_TASK_PROMPT_MD,
]

AUTHORIZED_SEAM_KINDS = [
    "HostManifest",
    "HostCapabilitySet",
    "WorkspaceDescriptor",
    "ContextDescriptor",
    "ArtifactReference",
    "DiagnosticProjection",
    "RefusalProjection",
    "EvidenceReferenceSet",
    "EventEnvelope",
    "DominiumBridgeManifest",
]

SELECTED_DOMINIUM_INPUTS = [
    {"path": "AGENTS.md", "role": "operator_law", "authority": "dominium_product_law", "required": True},
    {"path": ".aide/queue/current.toml", "role": "queue_status", "authority": "dominium_queue_truth", "required": True},
    {"path": "docs/canon/constitution_v1.md", "role": "constitution", "authority": "dominium_canon", "required": True},
    {"path": "docs/canon/glossary_v1.md", "role": "glossary", "authority": "dominium_canon", "required": True},
    {"path": "contracts/command/command_surface.contract.toml", "role": "command_surface", "authority": "dominium_contract", "required": True},
    {"path": "contracts/service/service.contract.toml", "role": "service_surface", "authority": "dominium_contract", "required": True},
    {"path": "contracts/module/module_surface.contract.toml", "role": "module_surface", "authority": "dominium_contract", "required": True},
    {"path": "contracts/workbench/workbench_surface.contract.toml", "role": "workbench_surface", "authority": "dominium_contract", "required": True},
    {"path": "contracts/refusal/refusal_code.registry.json", "role": "refusal_registry", "authority": "dominium_contract", "required": True},
    {"path": "contracts/diagnostic/diagnostic_code.registry.json", "role": "diagnostic_registry", "authority": "dominium_contract", "required": True},
    {"path": "contracts/diagnostic/diagnostic_severity.registry.json", "role": "diagnostic_severity_registry", "authority": "dominium_contract", "required": True},
    {"path": "contracts/capability/capability.registry.json", "role": "capability_registry", "authority": "dominium_contract", "required": True},
    {"path": "contracts/project_graph/project_graph_model.contract.toml", "role": "project_graph_model", "authority": "dominium_contract", "required": True},
    {"path": "docs/repo/audits/PRESENTATION_CONTRACT_01.md", "role": "presentation_contract_evidence", "authority": "dominium_evidence", "required": True},
    {"path": "docs/repo/audits/WORKBENCH_VALIDATION_SLICE_01.md", "role": "workbench_validation_evidence", "authority": "dominium_evidence", "required": True},
    {"path": "docs/development/workbench_validation_slice.md", "role": "workbench_validation_plan", "authority": "dominium_documentation", "required": True},
    {"path": "docs/development/command_result_view_slice.md", "role": "command_result_view_plan", "authority": "dominium_documentation", "required": True},
]

EXPLICIT_NON_CAPABILITIES = [
    "dominium_command_invocation",
    "host_runtime",
    "host_sdk",
    "workbench_implementation",
    "bridge_runtime",
    "service",
    "database_runtime",
    "transport",
    "network_call",
    "provider_model_call",
    "worker_execution",
    "patch_transaction_apply",
    "preview_apply_rollback",
    "target_repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
]

FALSE_STATUS_FIELDS = [
    "dominium_command_invoked",
    "host_runtime_started",
    "workbench_started",
    "bridge_runtime_started",
    "service_started",
    "database_opened",
    "transport_started",
    "network_call_performed",
    "provider_or_model_called",
    "worker_executed",
    "patch_transaction_applied",
    "preview_or_apply_performed",
    "target_repository_mutated",
    "branch_or_worktree_created",
    "github_mutation_performed",
    "release_or_promotion_performed",
]

WARNING_MESSAGES = [
    "Dominium seam v0 is offline and read-only.",
    "SeamBundle is generated projection evidence, not canonical Dominium truth.",
    "Local Dominium checkout may remain behind remote main; freshness is recorded rather than hidden.",
    "No Host runtime, Workbench implementation, bridge runtime, command invocation, provider/model/network call, worker execution, preview, apply, rollback, or mutation behavior exists.",
]


def stable_json(data: Any) -> str:
    return envelope.stable_json(data)


def read_json(path: Path) -> dict[str, Any]:
    return envelope.read_json(path)


def write_json(path: Path, obj: dict[str, Any]) -> None:
    envelope.write_json(path, obj)


def write_text(path: Path, text: str) -> None:
    envelope.write_text(path, text)


def compatibility(
    *,
    feature_flags: list[str] | None = None,
    required_capabilities: list[str] | None = None,
    min_reader: str = PROTOCOL_VERSION,
    min_writer: str = PROTOCOL_VERSION,
) -> dict[str, Any]:
    return {
        "schemaVersion": PROTOCOL_VERSION,
        "protocolVersion": PROTOCOL_VERSION,
        "minReaderVersion": min_reader,
        "minWriterVersion": min_writer,
        "featureFlags": feature_flags or [FEATURE_FLAG],
        "requiredCapabilities": required_capabilities or [],
        "readOldWriteCurrent": True,
        "unknownOptionalFields": "preserve_or_ignore_by_owner_contract",
        "unknownRequiredFields": "refuse",
    }


def false_status(**overrides: Any) -> dict[str, Any]:
    status = {field: False for field in FALSE_STATUS_FIELDS}
    status.update(overrides)
    return status


def required_runtime_dependency_paths() -> list[str]:
    module_root = Path(__file__).resolve().parents[3]
    dominium_module_root = module_root / "core" / "interop" / "dominium"
    return [
        ".aide/scripts/aide_lite.py",
        ".aide/protocol/aide-dominium-readonly-seam-v0.schema.json",
        "core/interop/__init__.py",
        "core/protocol/__init__.py",
        "core/protocol/envelope.py",
        *[
            path.relative_to(module_root).as_posix()
            for path in sorted(dominium_module_root.glob("*.py"))
        ],
    ]


def common_metadata(
    *,
    record_id: str,
    source_revision: str,
    authority_role: str,
    freshness: dict[str, Any],
    identity_owner: str = "AIDE",
    semantic_owner: str = "AIDE",
    compatibility_metadata: dict[str, Any] | None = None,
    explicit_non_capabilities: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": record_id,
        "schema_version": SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "created_at": DETERMINISTIC_TIMESTAMP,
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "source_revision": source_revision,
        "identity_owner": identity_owner,
        "semantic_owner": semantic_owner,
        "authority_role": authority_role,
        "freshness": deepcopy(freshness),
        "compatibility": compatibility_metadata or compatibility(),
        "explicit_non_capabilities": explicit_non_capabilities or list(EXPLICIT_NON_CAPABILITIES),
    }


def seam_record(
    *,
    kind: str,
    record_id: str,
    source_revision: str,
    authority_role: str,
    freshness: dict[str, Any],
    spec: dict[str, Any],
    status: dict[str, Any] | None = None,
    identity_owner: str = "AIDE",
    semantic_owner: str = "AIDE",
    compatibility_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "apiVersion": API_VERSION,
        "kind": kind,
        "metadata": common_metadata(
            record_id=record_id,
            source_revision=source_revision,
            authority_role=authority_role,
            freshness=freshness,
            identity_owner=identity_owner,
            semantic_owner=semantic_owner,
            compatibility_metadata=compatibility_metadata,
        ),
        "spec": deepcopy(spec),
        "status": false_status(record_projected=True, **(status or {})),
    }
