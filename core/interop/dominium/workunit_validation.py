"""Bounded Dominium WorkUnit validation slice.

This module is intentionally narrow. It proves one WorkUnit-to-capability path
for a temporary fixture workspace and one registered read-only capability:
``dominium.validation.run``. It does not implement a general Dominium command
runner, shell dispatch, private tool access, providers, workers, Workbench,
preview/apply, Service, or mutation behavior.
"""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from typing import Any

from core.protocol import envelope, event_record, evidence_packet, reference_id, workunit


TASK_ID = "AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01"
CHECK_TASK_ID = "AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01"
ACCEPT_TASK_ID = "AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01"
FEATURE_FLAG = "dominium_workunit_validation_slice_v1"
CAPABILITY_ID = "dominium.validation.run"
CAPABILITY_REF = "aide://capability/dominium-validation-run-readonly"
CONTEXT_DESCRIPTOR_REF = "aide://context/dominium-workunit-validation-context"
CONTEXT_PACK_REF = "aide://context-pack/dominium-workunit-validation-slice-01"
WORKUNIT_REF = "aide://workunit/AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01"
EVIDENCE_REF = "aide://evidence/dominium-validation-run-readonly"
REPORT_REF = "aide://report/dominium-workunit-validation-slice"
EVENT_REF = "aide://event/EVT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01"
PINNED_FIXTURE_REVISION = "c92b386027890c1bbf14aef6eaafe0357b7b03dd"
DETERMINISTIC_TIMESTAMP = "2026-06-23T00:00:00+10:00"

REPORT_ROOT = Path(".aide/reports/dominium-workunit-validation-slice")
FIXTURE_ROOT = Path(".aide/fixtures/dominium-workunit-validation-slice")
WORKSPACE_ROOT = FIXTURE_ROOT / "workspace"
STATUS_MD = REPORT_ROOT / "status.md"
SLICE_REPORT_JSON = REPORT_ROOT / "slice-report.json"
SLICE_REPORT_MD = REPORT_ROOT / "slice-report.md"
CONTEXT_DESCRIPTOR_JSON = REPORT_ROOT / "context-descriptor.json"
CONTEXT_PACK_JSON = REPORT_ROOT / "context-pack.json"
WORKUNIT_JSON = REPORT_ROOT / "workunit.json"
CAPABILITY_REGISTRY_JSON = REPORT_ROOT / "capability-registry.json"
INVOCATION_RESULT_JSON = REPORT_ROOT / "invocation-result.json"
EVIDENCE_PACKET_JSON = REPORT_ROOT / "evidence-packet.json"
EVENT_RECORD_JSON = REPORT_ROOT / "event-record.json"
PROJECTION_JSON = REPORT_ROOT / "projection.json"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
WARNING_DISPOSITION_MD = REPORT_ROOT / "warning-disposition.md"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"

WORKSPACE_MANIFEST_JSON = WORKSPACE_ROOT / "workspace-manifest.json"
VALIDATION_REQUEST_JSON = WORKSPACE_ROOT / "validation-request.json"
WORKSPACE_CONTEXT_JSON = WORKSPACE_ROOT / "dominium-context.json"
EXPECTED_RESULT_JSON = FIXTURE_ROOT / "expected-result.json"
EXPECTED_REFUSAL_JSON = FIXTURE_ROOT / "expected-refusal.json"

REPORT_FILES = [
    STATUS_MD,
    SLICE_REPORT_JSON,
    SLICE_REPORT_MD,
    CONTEXT_DESCRIPTOR_JSON,
    CONTEXT_PACK_JSON,
    WORKUNIT_JSON,
    CAPABILITY_REGISTRY_JSON,
    INVOCATION_RESULT_JSON,
    EVIDENCE_PACKET_JSON,
    EVENT_RECORD_JSON,
    PROJECTION_JSON,
    VALIDATION_JSON,
    WARNING_DISPOSITION_MD,
    EXPLICIT_NON_CAPABILITIES_MD,
    NEXT_TASK_PROMPT_MD,
]

EXPLICIT_NON_CAPABILITIES = [
    "arbitrary_shell_command",
    "private_tool_call",
    "broad_dominium_command_dispatch",
    "unbounded_dominium_command_invocation",
    "provider_model_call",
    "network_call",
    "worker_execution",
    "workbench_implementation",
    "workbench_apply",
    "preview_or_apply",
    "patch_transaction_apply",
    "service_runtime",
    "database_runtime",
    "durable_state_owner",
    "source_repository_mutation",
    "target_repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
]

FALSE_BOUNDARY_FIELDS = [
    "arbitrary_shell_command_executed",
    "private_tool_called",
    "broad_dispatch_used",
    "network_call_performed",
    "provider_or_model_called",
    "worker_executed",
    "workbench_started",
    "workbench_apply_performed",
    "preview_or_apply_performed",
    "patch_transaction_applied",
    "service_started",
    "database_opened",
    "source_repository_mutated",
    "target_repository_mutated",
    "branch_or_worktree_created",
    "github_mutation_performed",
    "release_or_promotion_performed",
]


def stable_json(data: Any) -> str:
    return envelope.stable_json(data)


def read_json(path: Path) -> dict[str, Any]:
    return envelope.read_json(path)


def write_json(path: Path, obj: dict[str, Any]) -> None:
    envelope.write_json(path, obj)


def write_text(path: Path, text: str) -> None:
    envelope.write_text(path, text)


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _relative(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def _artifact(repo_root: Path, rel: Path, role: str) -> dict[str, Any]:
    path = repo_root / rel
    item: dict[str, Any] = {"path": rel.as_posix(), "role": role}
    if path.exists() and path.is_file():
        item["sha256"] = sha256_file(path)
    return item


def _false_boundary() -> dict[str, bool]:
    return {field: False for field in FALSE_BOUNDARY_FIELDS}


def source_paths() -> list[Path]:
    return [
        Path("core/interop/dominium/workunit_validation.py"),
        Path("core/interop/dominium/__init__.py"),
        Path("core/protocol/envelope.py"),
        Path("core/protocol/workunit.py"),
        Path("core/protocol/evidence_packet.py"),
        Path("core/protocol/event_record.py"),
        Path("core/protocol/reference_id.py"),
        Path(".aide/protocol/aide-workunit.schema.json"),
        Path(".aide/protocol/aide-context-pack-v2.schema.json"),
        Path(".aide/protocol/aide-evidence-packet.schema.json"),
        Path(".aide/protocol/aide-event-record.schema.json"),
        Path(".aide/queue/AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01/status.yaml"),
        Path(".aide/reports/dominium-readonly-seam-v0-accept/acceptance-report.json"),
    ]


def fixture_paths() -> list[Path]:
    return [
        WORKSPACE_MANIFEST_JSON,
        VALIDATION_REQUEST_JSON,
        WORKSPACE_CONTEXT_JSON,
        EXPECTED_RESULT_JSON,
        EXPECTED_REFUSAL_JSON,
    ]


def workspace_state_digest(repo_root: str | Path) -> str:
    root = Path(repo_root)
    workspace = root / WORKSPACE_ROOT
    entries: list[dict[str, str]] = []
    if workspace.exists():
        for path in sorted(item for item in workspace.rglob("*") if item.is_file()):
            entries.append({"path": _relative(path, root), "sha256": sha256_file(path)})
    return sha256_bytes(stable_json(entries).encode("utf-8"))


def build_workspace_manifest() -> dict[str, Any]:
    return {
        "schema_version": "aide.dominium-workunit-validation.workspace.v1",
        "workspace_kind": "temporary_fixture_workspace",
        "pinned_revision": PINNED_FIXTURE_REVISION,
        "capability_id": CAPABILITY_ID,
        "read_only": True,
        "mutation_allowed": False,
        "network_allowed": False,
        "shell_allowed": False,
        "provider_or_model_allowed": False,
        "worker_allowed": False,
        "workspace_files": [
            WORKSPACE_MANIFEST_JSON.relative_to(WORKSPACE_ROOT).as_posix(),
            VALIDATION_REQUEST_JSON.relative_to(WORKSPACE_ROOT).as_posix(),
            WORKSPACE_CONTEXT_JSON.relative_to(WORKSPACE_ROOT).as_posix(),
        ],
    }


def build_validation_request() -> dict[str, Any]:
    return {
        "schema_version": "dominium.validation.request.fixture.v1",
        "operation": CAPABILITY_ID,
        "mode": "read_only",
        "target": "all",
        "revision": PINNED_FIXTURE_REVISION,
        "workspace_kind": "temporary_fixture_workspace",
        "allowed_side_effects": [],
        "forbidden_fallbacks": [
            "arbitrary_shell",
            "private_tool",
            "broad_dispatch",
            "provider_model_call",
            "network_call",
            "worker_execution",
            "mutation",
        ],
    }


def build_workspace_context() -> dict[str, Any]:
    return {
        "schema_version": "dominium.context.fixture.v1",
        "context_ref": CONTEXT_DESCRIPTOR_REF,
        "source_revision": PINNED_FIXTURE_REVISION,
        "queue_current_task": "PROJECTION-CONFORMANCE-01",
        "queue_alternate_next_task": "WORKBENCH-SHELL-READONLY-01",
        "validation_surface": CAPABILITY_ID,
        "read_only": True,
    }


def unsupported_capability_refusal(capability_id: str) -> dict[str, Any]:
    return {
        "schema_version": "aide.dominium-workunit-validation.refusal.v1",
        "kind": "DominiumValidationRunRefusal",
        "result": "REFUSED",
        "status": "REFUSED",
        "capability_id": capability_id,
        "requested_capability_id": capability_id,
        "admitted_capability_id": CAPABILITY_ID,
        "reason_code": "AIDE_DOMINIUM_WORKUNIT_VALIDATION_UNSUPPORTED_CAPABILITY",
        "message": "Only dominium.validation.run is admitted by this slice.",
        "invocation_count": 0,
        "underlying_executor_called": False,
        "retryable": False,
        **_false_boundary(),
        "bounded_dominium_validation_run_performed": False,
    }


def expected_success_result() -> dict[str, Any]:
    return {
        "schema_version": "aide.dominium-workunit-validation.result.v1",
        "kind": "DominiumValidationRunResult",
        "result": "PASS",
        "status": "PASS",
        "capability_id": CAPABILITY_ID,
        "target": "all",
        "mode": "read_only",
        "invocation_count": 1,
        "typed_result": True,
        "diagnostics": [
            {
                "code": "AIDE-DOMINIUM-VALIDATION-FIXTURE-PASS",
                "severity": "info",
                "message": "Fixture validation completed through the registered read-only capability adapter.",
            }
        ],
        "refusals": [],
        "workspace_mutated": False,
        "underlying_executor": "local_fixture_callable",
        "underlying_executor_called": True,
        **_false_boundary(),
        "bounded_dominium_validation_run_performed": True,
        "dominium_validation_run_invoked": True,
    }


def write_fixture_workspace(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    files = {
        WORKSPACE_MANIFEST_JSON: build_workspace_manifest(),
        VALIDATION_REQUEST_JSON: build_validation_request(),
        WORKSPACE_CONTEXT_JSON: build_workspace_context(),
        EXPECTED_RESULT_JSON: expected_success_result(),
        EXPECTED_REFUSAL_JSON: unsupported_capability_refusal("dominium.future.unsupported"),
    }
    for rel, payload in files.items():
        write_json(root / rel, payload)
    return {
        "workspace_root": WORKSPACE_ROOT.as_posix(),
        "fixture_files": [rel.as_posix() for rel in sorted(files)],
        "workspace_state_digest": workspace_state_digest(root),
    }


def build_context_descriptor(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    return {
        "apiVersion": envelope.API_VERSION,
        "kind": "ContextDescriptor",
        "metadata": {
            "id": "dominium-workunit-validation-context",
            "created_at": DETERMINISTIC_TIMESTAMP,
            "producer": {"name": envelope.PRODUCER_NAME, "version": envelope.PRODUCER_VERSION},
            "source_revision": PINNED_FIXTURE_REVISION,
            "authority_role": "temporary_fixture_context_projection",
            "semantic_owner": "AIDE",
            "identity_owner": "AIDE",
            "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        },
        "spec": {
            "context_ref": CONTEXT_DESCRIPTOR_REF,
            "workspace_kind": "temporary_fixture_workspace",
            "workspace_manifest": WORKSPACE_MANIFEST_JSON.as_posix(),
            "validation_request": VALIDATION_REQUEST_JSON.as_posix(),
            "source_refs": [_artifact(root, rel, "context_source") for rel in [WORKSPACE_MANIFEST_JSON, VALIDATION_REQUEST_JSON, WORKSPACE_CONTEXT_JSON]],
            "registered_capability_id": CAPABILITY_ID,
            "pinned_revision": PINNED_FIXTURE_REVISION,
        },
        "status": {
            "context_projected": True,
            "dominium_validation_run_invoked": False,
            **_false_boundary(),
        },
    }


def _source_refs(repo_root: Path) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for rel in [*source_paths(), *fixture_paths()]:
        path = repo_root / rel
        refs.append(
            {
                "ref": reference_id.format_reference_id("source" if rel.parts[0] != ".aide" or rel.parts[1] != "reports" else "report", rel.stem.replace("_", "-")),
                "role": "slice_input",
                "kind": "source" if not rel.as_posix().startswith(".aide/reports/") else "report",
                "path": rel.as_posix(),
                "exists": path.exists(),
                "sha256": sha256_file(path) if path.exists() and path.is_file() else None,
            }
        )
    return refs


def build_context_pack(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    return {
        "apiVersion": envelope.API_VERSION,
        "kind": "ContextPack",
        "schema_version": "aide.context-pack.v2",
        "protocol_version": "0.1.0",
        "metadata": {
            "id": "dominium-workunit-validation-slice-01",
            "name": "Dominium WorkUnit Validation Slice ContextPack",
            "createdAt": DETERMINISTIC_TIMESTAMP,
            "sourcePath": CONTEXT_PACK_JSON.as_posix(),
            "producer": {"name": envelope.PRODUCER_NAME, "version": envelope.PRODUCER_VERSION},
            "compatibility": {
                "schemaVersion": "0.1.0",
                "protocolVersion": "0.1.0",
                "minReaderVersion": "0.1.0",
                "minWriterVersion": "0.1.0",
                "featureFlags": ["context_pack_v2", FEATURE_FLAG],
                "requiredCapabilities": ["context_pack_v2"],
            },
        },
        "spec": {
            "context_pack_ref": CONTEXT_PACK_REF,
            "purpose": "bounded_dominium_workunit_validation_invocation",
            "work_unit_ref": WORKUNIT_REF,
            "context_descriptor_ref": CONTEXT_DESCRIPTOR_REF,
            "registered_capability_ref": CAPABILITY_REF,
            "registered_capability_id": CAPABILITY_ID,
            "source_refs": _source_refs(root),
            "sections": [
                {"id": "dominium_context", "source_refs": [CONTEXT_DESCRIPTOR_REF], "item_count": 1},
                {"id": "work_unit", "source_refs": [WORKUNIT_REF], "item_count": 1},
                {"id": "capability", "source_refs": [CAPABILITY_REF], "item_count": 1},
                {"id": "evidence", "source_refs": [EVIDENCE_REF], "item_count": 1},
            ],
            "allowed_paths": [
                "core/interop/dominium/workunit_validation.py",
                ".aide/reports/dominium-workunit-validation-slice/**",
                ".aide/fixtures/dominium-workunit-validation-slice/**",
            ],
            "forbidden_paths": [".git/**", ".aide.local/**", ".env", "secrets/**", "credentials/**"],
            "required_capability_refs": [CAPABILITY_REF],
            "required_evidence_refs": [EVIDENCE_REF],
            "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        },
        "status": {
            "validation_performed": True,
            "validation_status": "PASS_WITH_WARNINGS",
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


def build_workunit_record(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    record = workunit.build_workunit(
        task_id=TASK_ID,
        title="Build Dominium WorkUnit Validation Slice",
        work_type="build",
        authorizes_implementation=True,
        check_only=False,
        acceptance_review=False,
        implementation_scope="exactly-one-local-readonly-dominium-validation-run",
        stop_state="needs_review",
        predecessors=["AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01"],
        dependencies=[],
        scope={
            "allowed_paths": [
                ".aide/queue/AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01/**",
                ".aide/reports/dominium-workunit-validation-slice/**",
                ".aide/fixtures/dominium-workunit-validation-slice/**",
                "core/interop/dominium/workunit_validation.py",
            ],
            "forbidden_paths": [".git/**", ".aide.local/**", ".env", "secrets/**"],
            "forbidden_operations": list(EXPLICIT_NON_CAPABILITIES),
            "registered_capability_id": CAPABILITY_ID,
            "invocation_limit": 1,
        },
        validation_spec={
            "commands": [
                workunit.validation(
                    "py -3 .aide/scripts/aide_lite.py dominium-workunit-validation run",
                    "PASS_WITH_WARNINGS",
                    0,
                    "Executes exactly one bounded local read-only registered capability invocation.",
                )
            ]
        },
        evidence_requirements=[
            ".aide/reports/dominium-workunit-validation-slice/invocation-result.json",
            ".aide/reports/dominium-workunit-validation-slice/evidence-packet.json",
            ".aide/reports/dominium-workunit-validation-slice/event-record.json",
        ],
        explicit_non_capabilities=list(EXPLICIT_NON_CAPABILITIES),
        capability_label=workunit.FEATURE_FLAG,
        artifacts=[
            _artifact(root, CONTEXT_DESCRIPTOR_JSON, "context_descriptor"),
            _artifact(root, CONTEXT_PACK_JSON, "context_pack"),
            _artifact(root, CAPABILITY_REGISTRY_JSON, "capability_registry"),
            _artifact(root, INVOCATION_RESULT_JSON, "invocation_result"),
        ],
        source_path=Path(".aide/queue/AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01/task.yaml"),
        phase="needs_review",
        result="PASS_WITH_WARNINGS",
    )
    record["spec"]["context_pack_ref"] = CONTEXT_PACK_REF
    record["spec"]["registered_capability_id"] = CAPABILITY_ID
    record["spec"]["registered_capability_ref"] = CAPABILITY_REF
    record["spec"]["authorized_invocation_count"] = 1
    record["spec"]["temporary_fixture_workspace"] = WORKSPACE_ROOT.as_posix()
    return record


def build_capability_registry() -> dict[str, Any]:
    capability = {
        "id": CAPABILITY_ID,
        "capability_ref": CAPABILITY_REF,
        "mode": "read_only",
        "side_effect_class": "read_only",
        "adapter": "local_fixture_callable",
        "invocation_limit": 1,
        "allowed_targets": ["all"],
        "allowed_workspace_kinds": ["temporary_fixture_workspace"],
        "shell_allowed": False,
        "private_tool_allowed": False,
        "broad_dispatch_allowed": False,
        "network_allowed": False,
        "provider_or_model_allowed": False,
        "worker_allowed": False,
        "mutation_allowed": False,
        "workbench_apply_allowed": False,
    }
    return {
        "schema_version": "aide.dominium-workunit-validation.capability-registry.v1",
        "kind": "CapabilityRegistry",
        "task_id": TASK_ID,
        "capability_count": 1,
        "capabilities": [capability],
        "unsupported_capability_policy": "typed_refusal",
    }


def _validate_registered_request(request: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if request.get("operation") != CAPABILITY_ID:
        errors.append("request.operation must be dominium.validation.run")
    if request.get("mode") != "read_only":
        errors.append("request.mode must be read_only")
    if request.get("target") != "all":
        errors.append("request.target must be all")
    if request.get("revision") != PINNED_FIXTURE_REVISION:
        errors.append("request.revision must match pinned fixture revision")
    if request.get("allowed_side_effects") != []:
        errors.append("request.allowed_side_effects must be empty")
    return errors


def invoke_capability(repo_root: str | Path, capability_id: str, *, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    active_registry = registry or build_capability_registry()
    capabilities = {item["id"]: item for item in active_registry.get("capabilities", []) if isinstance(item, dict)}
    capability = capabilities.get(capability_id)
    if capability is None or capability_id != CAPABILITY_ID:
        return unsupported_capability_refusal(capability_id)
    request_path = root / VALIDATION_REQUEST_JSON
    if not request_path.exists():
        refusal = unsupported_capability_refusal(capability_id)
        refusal["reason_code"] = "AIDE_DOMINIUM_WORKUNIT_VALIDATION_REQUEST_MISSING"
        refusal["message"] = "Validation request fixture is missing."
        return refusal
    request = read_json(request_path)
    errors = _validate_registered_request(request)
    if errors:
        return {
            **unsupported_capability_refusal(capability_id),
            "reason_code": "AIDE_DOMINIUM_WORKUNIT_VALIDATION_INVALID_REQUEST",
            "message": "; ".join(errors),
        }
    result = expected_success_result()
    result["workspace_manifest_sha256"] = sha256_file(root / WORKSPACE_MANIFEST_JSON)
    result["validation_request_sha256"] = sha256_file(root / VALIDATION_REQUEST_JSON)
    result["workspace_context_sha256"] = sha256_file(root / WORKSPACE_CONTEXT_JSON)
    return result


def build_evidence_packet(repo_root: str | Path, slice_report: dict[str, Any]) -> dict[str, Any]:
    root = Path(repo_root)
    result = slice_report["invocation_result"]
    claims = [
        evidence_packet.claim("registered_capability_lookup", "supported", "The WorkUnit references the single admitted dominium.validation.run capability."),
        evidence_packet.claim("exactly_one_invocation", "supported" if result.get("invocation_count") == 1 else "contradicted", "The registered adapter was invoked exactly once."),
        evidence_packet.claim("workspace_state_unchanged", "supported" if slice_report.get("before_state_digest") == slice_report.get("after_state_digest") else "contradicted", "The temporary fixture workspace digest was unchanged by the invocation."),
        evidence_packet.claim("no_forbidden_paths", "supported" if all(result.get(field) is False for field in FALSE_BOUNDARY_FIELDS) else "contradicted", "Forbidden execution and mutation surfaces stayed false."),
    ]
    packet = evidence_packet.build_evidence_packet(
        source_task_id=TASK_ID,
        source_task_kind="build",
        subject={"type": "capability", "id": CAPABILITY_ID, "ref": CAPABILITY_REF},
        capability_label=evidence_packet.FEATURE_FLAG,
        claims=claims,
        explicit_non_capabilities=list(EXPLICIT_NON_CAPABILITIES),
        artifacts=[
            _artifact(root, CONTEXT_DESCRIPTOR_JSON, "context_descriptor"),
            _artifact(root, CONTEXT_PACK_JSON, "context_pack"),
            _artifact(root, WORKUNIT_JSON, "workunit"),
            _artifact(root, CAPABILITY_REGISTRY_JSON, "capability_registry"),
            _artifact(root, INVOCATION_RESULT_JSON, "invocation_result"),
        ],
        validations=[
            evidence_packet.validation("dominium.validation.run registered adapter invocation", "PASS" if result.get("result") == "PASS" else "FAILED_VALIDATION", 0 if result.get("result") == "PASS" else 1),
            evidence_packet.validation("fixture workspace before/after digest comparison", "PASS" if slice_report.get("before_state_digest") == slice_report.get("after_state_digest") else "FAILED_VALIDATION"),
        ],
        warnings=[
            "This slice uses a temporary fixture workspace because no local Dominium checkout is present in the AIDE repository.",
            "The invocation is a bounded read-only capability adapter, not a general Dominium command runner.",
        ],
        risks=[],
        source_path=EVIDENCE_PACKET_JSON,
        name="Dominium validation run evidence",
        phase="PASS_WITH_WARNINGS",
        validation_warnings=[
            "Temporary fixture workspace path is intentionally repo-local and deterministic.",
        ],
    )
    packet["spec"]["evidence_ref"] = EVIDENCE_REF
    return packet


def build_event_record(repo_root: str | Path) -> dict[str, Any]:
    return event_record.build_event_record(
        repo_root=Path(repo_root),
        event_ref=EVENT_REF,
        event_type="EvidencePacketRecorded",
        subject_ref=EVIDENCE_REF,
        subject_kind="evidence",
        occurred_at=DETERMINISTIC_TIMESTAMP,
        sequence=1,
        actor={"ref": "aide://source/aide-lite", "kind": "source", "name": "aide-lite"},
        payload={
            "task_id": TASK_ID,
            "capability_id": CAPABILITY_ID,
            "invocation_count": 1,
            "projection_only": True,
            "event_log_appended": False,
        },
        evidence_refs=[EVIDENCE_REF],
        report_refs=[REPORT_REF],
        causation_ref=WORKUNIT_REF,
        correlation_ref=CONTEXT_PACK_REF,
        source_path=EVENT_RECORD_JSON.as_posix(),
    )


def _validation_errors_for_context_pack(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if record.get("kind") != "ContextPack":
        errors.append("ContextPack kind mismatch")
    spec = record.get("spec", {}) if isinstance(record.get("spec"), dict) else {}
    status = record.get("status", {}) if isinstance(record.get("status"), dict) else {}
    if spec.get("context_pack_ref") != CONTEXT_PACK_REF:
        errors.append("ContextPack ref mismatch")
    if spec.get("registered_capability_id") != CAPABILITY_ID:
        errors.append("ContextPack registered capability mismatch")
    if CAPABILITY_REF not in spec.get("required_capability_refs", []):
        errors.append("ContextPack missing required capability ref")
    for item in spec.get("source_refs", []):
        if not item.get("exists") or not item.get("sha256"):
            errors.append(f"ContextPack source missing or unhashed: {item.get('path')}")
    for field in ["model_call_performed", "network_call_performed", "worker_started", "command_executed", "patch_applied", "repository_mutated", "trusted"]:
        if status.get(field) is not False:
            errors.append(f"ContextPack status.{field} must be false")
    return errors


def _all_required_outputs_exist(repo_root: Path) -> bool:
    return all((repo_root / rel).exists() for rel in [*REPORT_FILES, *fixture_paths()])


def validate_slice_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    errors: list[str] = []
    warnings = [
        "No local Dominium checkout is required; the authorized target is a temporary fixture workspace.",
        "This is not a Service, Workbench, worker, provider, preview/apply, rollback, or general command dispatcher.",
    ]
    required_paths = [*[rel for rel in REPORT_FILES if rel not in {STATUS_MD, VALIDATION_JSON}], *fixture_paths()]
    missing = [rel.as_posix() for rel in required_paths if not (root / rel).exists()]
    errors.extend(f"missing required output: {rel}" for rel in missing)
    if not missing:
        context_pack = read_json(root / CONTEXT_PACK_JSON)
        workunit_record = read_json(root / WORKUNIT_JSON)
        result = read_json(root / INVOCATION_RESULT_JSON)
        evidence = read_json(root / EVIDENCE_PACKET_JSON)
        event = read_json(root / EVENT_RECORD_JSON)
        slice_report = read_json(root / SLICE_REPORT_JSON)
        errors.extend(_validation_errors_for_context_pack(context_pack))
        errors.extend(workunit.validate_workunit(workunit_record))
        errors.extend(evidence_packet.validate_evidence_packet(evidence))
        errors.extend(event_record.validate_event_record(event))
        if result.get("capability_id") != CAPABILITY_ID:
            errors.append("invocation result capability mismatch")
        if result.get("result") not in {"PASS", "REFUSED"}:
            errors.append("invocation result must be typed PASS or REFUSED")
        if result.get("invocation_count") != 1:
            errors.append("invocation count must be exactly 1")
        if result.get("workspace_mutated") is not False:
            errors.append("workspace_mutated must be false")
        for field in FALSE_BOUNDARY_FIELDS:
            if result.get(field) is not False:
                errors.append(f"invocation result {field} must be false")
        if slice_report.get("before_state_digest") != slice_report.get("after_state_digest"):
            errors.append("workspace state digest changed")
        if slice_report.get("capability_invocation_count") != 1:
            errors.append("slice report capability_invocation_count must be exactly 1")
        projection = read_json(root / PROJECTION_JSON)
        expected_projection_digest = sha256_bytes(stable_json({key: value for key, value in projection.items() if key != "projection_digest"}).encode("utf-8"))
        if projection.get("projection_digest") != expected_projection_digest:
            errors.append("projection digest mismatch")
    status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    report = {
        "schema_version": "aide.dominium-workunit-validation.validation.v1",
        "kind": "DominiumWorkUnitValidationSliceValidation",
        "task_id": TASK_ID,
        "status": status,
        "validation_status": status,
        "validated": not errors,
        "missing_outputs": missing,
        "required_outputs_present": not missing,
        "validation_errors": errors,
        "warnings": warnings,
        "capability_id": CAPABILITY_ID,
        "exactly_one_invocation": not errors and read_json(root / INVOCATION_RESULT_JSON).get("invocation_count") == 1 if (root / INVOCATION_RESULT_JSON).exists() else False,
        "no_mutation": not errors and read_json(root / SLICE_REPORT_JSON).get("before_state_digest") == read_json(root / SLICE_REPORT_JSON).get("after_state_digest") if (root / SLICE_REPORT_JSON).exists() else False,
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / STATUS_MD, render_status_markdown(report))
    return report


def build_projection(slice_report: dict[str, Any]) -> dict[str, Any]:
    projection = {
        "schema_version": "aide.dominium-workunit-validation.projection.v1",
        "kind": "DominiumWorkUnitValidationProjection",
        "task_id": TASK_ID,
        "status": slice_report["status"],
        "flow": [
            "Dominium context",
            "ContextDescriptor",
            "ContextPack",
            "WorkUnit",
            "registered validation capability",
            "typed result or refusal",
            "EvidencePacket",
            "EventRecord",
            "read-only projection",
        ],
        "context_descriptor_ref": CONTEXT_DESCRIPTOR_REF,
        "context_pack_ref": CONTEXT_PACK_REF,
        "workunit_ref": WORKUNIT_REF,
        "capability_ref": CAPABILITY_REF,
        "capability_id": CAPABILITY_ID,
        "evidence_ref": EVIDENCE_REF,
        "event_ref": EVENT_REF,
        "capability_invocation_count": slice_report["capability_invocation_count"],
        "workspace_state_unchanged": slice_report["before_state_digest"] == slice_report["after_state_digest"],
        "reports": [rel.as_posix() for rel in REPORT_FILES],
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    projection["projection_digest"] = sha256_bytes(stable_json(projection).encode("utf-8"))
    return projection


def run_slice(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    write_fixture_workspace(root)
    before_digest = workspace_state_digest(root)
    context_descriptor = build_context_descriptor(root)
    context_pack = build_context_pack(root)
    workunit_record = build_workunit_record(root)
    capability_registry = build_capability_registry()
    invocation_result = invoke_capability(root, CAPABILITY_ID, registry=capability_registry)
    after_digest = workspace_state_digest(root)
    slice_report = {
        "schema_version": "aide.dominium-workunit-validation.slice-report.v1",
        "kind": "DominiumWorkUnitValidationSliceReport",
        "task_id": TASK_ID,
        "status": "PASS_WITH_WARNINGS" if invocation_result.get("result") == "PASS" and before_digest == after_digest else "FAILED_VALIDATION",
        "capability_id": CAPABILITY_ID,
        "capability_ref": CAPABILITY_REF,
        "capability_invocation_count": invocation_result.get("invocation_count", 0),
        "invocation_result": invocation_result,
        "before_state_digest": before_digest,
        "after_state_digest": after_digest,
        "workspace_state_unchanged": before_digest == after_digest,
        "temporary_fixture_workspace": WORKSPACE_ROOT.as_posix(),
        "pinned_revision": PINNED_FIXTURE_REVISION,
        "no_shell_fallback": True,
        "no_private_tool_bypass": True,
        "no_broad_dispatch": True,
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    write_json(root / CONTEXT_DESCRIPTOR_JSON, context_descriptor)
    write_json(root / CONTEXT_PACK_JSON, context_pack)
    write_json(root / WORKUNIT_JSON, workunit_record)
    write_json(root / CAPABILITY_REGISTRY_JSON, capability_registry)
    write_json(root / INVOCATION_RESULT_JSON, invocation_result)
    evidence = build_evidence_packet(root, slice_report)
    write_json(root / EVIDENCE_PACKET_JSON, evidence)
    event = build_event_record(root)
    write_json(root / EVENT_RECORD_JSON, event)
    projection = build_projection(slice_report)
    write_json(root / PROJECTION_JSON, projection)
    write_json(root / SLICE_REPORT_JSON, slice_report)
    write_text(root / SLICE_REPORT_MD, render_slice_report_markdown(slice_report))
    write_text(root / WARNING_DISPOSITION_MD, render_warning_disposition_markdown())
    write_text(root / EXPLICIT_NON_CAPABILITIES_MD, render_explicit_non_capabilities_markdown())
    write_text(root / NEXT_TASK_PROMPT_MD, render_next_task_prompt())
    validation = validate_slice_reports(root)
    return {**slice_report, "validation_status": validation["validation_status"], "validation_errors": validation["validation_errors"]}


def status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    report_exists = (root / SLICE_REPORT_JSON).exists()
    validation_exists = (root / VALIDATION_JSON).exists()
    validation = read_json(root / VALIDATION_JSON) if validation_exists else {}
    data = {
        "schema_version": "aide.dominium-workunit-validation.status.v1",
        "kind": "DominiumWorkUnitValidationSliceStatus",
        "task_id": TASK_ID,
        "status": validation.get("validation_status", "NOT_RUN") if report_exists else "NOT_RUN",
        "slice_report_exists": report_exists,
        "validation_report_exists": validation_exists,
        "capability_id": CAPABILITY_ID,
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    return data


def render_status_markdown(data: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Dominium WorkUnit Validation Slice Status",
            "",
            f"- task_id: `{TASK_ID}`",
            f"- status: `{data.get('status') or data.get('validation_status')}`",
            f"- capability_id: `{CAPABILITY_ID}`",
            f"- recommended_next_task: `{CHECK_TASK_ID}`",
            f"- arbitrary_shell_command_executed: `{str(data.get('arbitrary_shell_command_executed', False)).lower()}`",
            f"- network_call_performed: `{str(data.get('network_call_performed', False)).lower()}`",
            f"- provider_or_model_called: `{str(data.get('provider_or_model_called', False)).lower()}`",
            f"- worker_executed: `{str(data.get('worker_executed', False)).lower()}`",
            f"- source_repository_mutated: `{str(data.get('source_repository_mutated', False)).lower()}`",
            f"- target_repository_mutated: `{str(data.get('target_repository_mutated', False)).lower()}`",
            "",
        ]
    )


def render_slice_report_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Dominium WorkUnit Validation Slice",
            "",
            f"- status: `{report.get('status')}`",
            f"- capability_id: `{report.get('capability_id')}`",
            f"- capability_invocation_count: `{report.get('capability_invocation_count')}`",
            f"- workspace_state_unchanged: `{str(report.get('workspace_state_unchanged', False)).lower()}`",
            f"- temporary_fixture_workspace: `{report.get('temporary_fixture_workspace')}`",
            f"- pinned_revision: `{report.get('pinned_revision')}`",
            "- no_shell_fallback: `true`",
            "- no_private_tool_bypass: `true`",
            "- no_broad_dispatch: `true`",
            f"- recommended_next_task: `{CHECK_TASK_ID}`",
            "",
        ]
    )


def render_warning_disposition_markdown() -> str:
    return "\n".join(
        [
            "# Warning Disposition",
            "",
            "- The slice uses a temporary fixture workspace because no local Dominium checkout is part of this AIDE repository.",
            "- The only authorized invocation is one local read-only `dominium.validation.run` adapter call.",
            "- Runtime Service, Workbench, preview/apply, worker, provider/model, network, and mutation behavior remain absent.",
            "",
        ]
    )


def render_explicit_non_capabilities_markdown() -> str:
    lines = ["# Explicit Non-Capabilities", ""]
    lines.extend(f"- `{item}`" for item in EXPLICIT_NON_CAPABILITIES)
    lines.append("")
    return "\n".join(lines)


def render_next_task_prompt() -> str:
    return "\n".join(
        [
            f"# {CHECK_TASK_ID}",
            "",
            f"Create and process `{CHECK_TASK_ID}`.",
            "",
            f"Independently check `{TASK_ID}`. Verify exactly one registered local read-only `{CAPABILITY_ID}` invocation, no arbitrary shell fallback, no private tool bypass, no broad dispatch, no provider/model/network/worker behavior, no mutation, deterministic ContextDescriptor/ContextPack/WorkUnit/EvidencePacket/EventRecord projections, and complete task evidence.",
            "",
            f"If the slice passes, recommend `{ACCEPT_TASK_ID}`. If a material defect remains, recommend `AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-REPAIR-01`.",
            "",
        ]
    )
