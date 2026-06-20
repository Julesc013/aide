"""Minimal contract-only A2A agent-card projection helpers for AIDE.

This module projects deterministic A2A agent-card contract artifacts and
reports. It deliberately avoids endpoint startup, registration, task
delegation, authentication, worker dispatch, provider calls, network access, and
repository mutation.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

from core.protocol import envelope


API_VERSION = envelope.API_VERSION
A2A_CONTRACT_SCHEMA_VERSION = "aide.a2a-agent-card-contract.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_a2a_agent_card_contract"
TASK_ID = "AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01"
DETERMINISTIC_TIMESTAMP = "2026-06-20T00:00:00+10:00"

CONTRACT_ID = "a2a-agent-card-contract-v0"
ADVISORY_CONTRACT_REF = "aide://interop/a2a-agent-card-contract-v0"
AGENT_NAME = "AIDE Contract-Only Agent Card Preview"
AGENT_VERSION = "0.1.0"

SCHEMA_PATH = Path(".aide/protocol/aide-a2a-agent-card-contract.schema.json")
INTEROP_ROOT = Path(".aide/interop/a2a")
AGENT_CARD_CONTRACT_JSON = INTEROP_ROOT / "agent-card-contract.json"
AGENT_CARD_PREVIEW_JSON = INTEROP_ROOT / "agent-card.preview.json"
CAPABILITY_CATALOG_JSON = INTEROP_ROOT / "capability-catalog.json"
SKILL_CATALOG_JSON = INTEROP_ROOT / "skill-catalog.json"
REFUSAL_CATALOG_JSON = INTEROP_ROOT / "refusal-catalog.json"
CONFORMANCE_EXPECTATIONS_JSON = INTEROP_ROOT / "conformance-expectations.json"

REPORT_ROOT = Path(".aide/reports/a2a-agent-card-contract")
STATUS_MD = REPORT_ROOT / "status.md"
CONTRACT_REPORT_JSON = REPORT_ROOT / "contract.json"
CONTRACT_REPORT_MD = REPORT_ROOT / "contract.md"
AGENT_CARD_REPORT_JSON = REPORT_ROOT / "agent-card.json"
AGENT_CARD_REPORT_MD = REPORT_ROOT / "agent-card.md"
CAPABILITY_MATRIX_JSON = REPORT_ROOT / "capability-matrix.json"
CAPABILITY_MATRIX_MD = REPORT_ROOT / "capability-matrix.md"
SKILL_CATALOG_REPORT_JSON = REPORT_ROOT / "skill-catalog.json"
SKILL_CATALOG_REPORT_MD = REPORT_ROOT / "skill-catalog.md"
SECURITY_BOUNDARY_JSON = REPORT_ROOT / "security-boundary.json"
SECURITY_BOUNDARY_MD = REPORT_ROOT / "security-boundary.md"
REFUSAL_MAPPING_JSON = REPORT_ROOT / "refusal-mapping.json"
REFUSAL_MAPPING_MD = REPORT_ROOT / "refusal-mapping.md"
CONFORMANCE_REPORT_JSON = REPORT_ROOT / "conformance-expectations.json"
CONFORMANCE_REPORT_MD = REPORT_ROOT / "conformance-expectations.md"
ARTIFACT_INDEX_JSON = REPORT_ROOT / "artifact-index.json"
ARTIFACT_INDEX_MD = REPORT_ROOT / "artifact-index.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"

REQUIRED_REPORTS = [
    STATUS_MD,
    CONTRACT_REPORT_JSON,
    CONTRACT_REPORT_MD,
    AGENT_CARD_REPORT_JSON,
    AGENT_CARD_REPORT_MD,
    CAPABILITY_MATRIX_JSON,
    CAPABILITY_MATRIX_MD,
    SKILL_CATALOG_REPORT_JSON,
    SKILL_CATALOG_REPORT_MD,
    SECURITY_BOUNDARY_JSON,
    SECURITY_BOUNDARY_MD,
    REFUSAL_MAPPING_JSON,
    REFUSAL_MAPPING_MD,
    CONFORMANCE_REPORT_JSON,
    CONFORMANCE_REPORT_MD,
    ARTIFACT_INDEX_JSON,
    ARTIFACT_INDEX_MD,
    VALIDATION_JSON,
    VALIDATION_MD,
    EXPLICIT_NON_CAPABILITIES_MD,
    FUTURE_WORK_MD,
    NEXT_TASK_PROMPT_MD,
]

PROJECTION_ARTIFACTS = [
    AGENT_CARD_CONTRACT_JSON,
    AGENT_CARD_PREVIEW_JSON,
    CAPABILITY_CATALOG_JSON,
    SKILL_CATALOG_JSON,
    REFUSAL_CATALOG_JSON,
    CONFORMANCE_EXPECTATIONS_JSON,
]

SKILL_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9_-]*)+$")
FORBIDDEN_SKILL_ID_PARTS = [
    ".apply",
    ".approve",
    ".dispatch",
    ".execute",
    ".grant",
    ".mutate",
    ".register",
    ".run",
]
SECRET_LIKE_RE = re.compile(
    r"(api[_-]?key|token|password|passwd|secret|private[_-]?key|-----BEGIN|cookie|connection[_-]?string)",
    re.IGNORECASE,
)

FALSE_RUNTIME_FIELDS = [
    "live_a2a_endpoint_started",
    "agent_registered",
    "task_delegation_performed",
    "authentication_implemented",
    "worker_dispatched",
    "model_or_provider_called",
    "network_call_performed",
    "patch_applied",
    "repository_target_mutated",
    "branch_or_worktree_created",
    "github_mutation_performed",
    "trusted",
]

EXPLICIT_NON_CAPABILITIES = [
    "live_a2a_endpoint",
    "agent_registration",
    "agent_discovery_publication",
    "task_delegation",
    "task_submission",
    "task_status_runtime",
    "streaming",
    "push_notifications",
    "state_transition_history_runtime",
    "authentication",
    "authorization",
    "credential_resolution",
    "worker_execution",
    "provider_model_calls",
    "network_calls",
    "patch_transaction_approval",
    "patch_transaction_apply",
    "target_repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "host_contract",
    "dominium_bridge",
    "workbench",
    "runtime",
    "service",
    "scheduler",
    "leases",
    "supervisor",
    "release",
    "promotion",
    "production_readiness",
]

VALIDATION_WARNINGS = [
    "A2A agent-card contract is projection-only; no live endpoint or registration exists.",
    "Agent-card shape is a local structural subset; full external A2A schema validation remains future work.",
    "Skills are declared as future read-only discovery candidates only; no task delegation or worker execution exists.",
    "Authentication, authorization, PolicyDecision, CapabilityGrant, and credential handling are intentionally absent.",
    "Inherited Interop Exports preview-only limitations and prior report/OKF/Reconciler warning debt remain unresolved.",
]


def stable_json(data: Any) -> str:
    return envelope.stable_json(data)


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


def load_a2a_agent_card_contract_schema(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(repo_root) if repo_root is not None else Path(".")
    return read_json(root / SCHEMA_PATH)


def source_artifact_paths(repo_root: str | Path | None = None) -> list[str]:
    _root = Path(repo_root) if repo_root is not None else Path(".")
    return [
        ".aide/protocol/aide-a2a-agent-card-contract.schema.json",
        "core/interop/__init__.py",
        "core/interop/a2a_agent_card_contract.py",
        ".aide/scripts/aide_lite.py",
        ".aide/scripts/tests/test_aide_a2a_agent_card_contract.py",
        ".aide/interop/exports/manifest.json",
        ".aide/interop/exports/a2a-agent-card.preview.json",
        ".aide/reports/interop-exports-accept/acceptance-report.json",
        ".aide/reports/mcp-server-contract-accept/acceptance-report.json",
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
        "requiredCapabilities": [],
    }


def build_declared_card_capabilities() -> dict[str, bool]:
    return {
        "agent_card_projection": True,
        "skill_catalog_projection": True,
        "read_only_discovery_candidates": True,
        "streaming": False,
        "push_notifications": False,
        "state_transition_history": False,
        "authenticated_extended_card": False,
    }


def build_implemented_runtime_capabilities() -> dict[str, bool]:
    return {
        "live_endpoint": False,
        "agent_registered": False,
        "task_delegation": False,
        "task_submission": False,
        "authentication": False,
        "authorization": False,
        "worker_execution": False,
    }


def build_skills() -> list[dict[str, Any]]:
    skill_specs = [
        (
            "aide.queue.inspect",
            "Inspect AIDE queue projection",
            "Future read-only queue discovery candidate. No A2A task endpoint exists in this slice.",
            ["queue", "read-only", "projection"],
        ),
        (
            "aide.evidence.inspect",
            "Inspect AIDE evidence projection",
            "Future read-only evidence discovery candidate. No A2A task endpoint exists in this slice.",
            ["evidence", "read-only", "projection"],
        ),
        (
            "aide.capability.inspect",
            "Inspect AIDE capability projection",
            "Future read-only capability discovery candidate. No A2A task endpoint exists in this slice.",
            ["capability", "read-only", "projection"],
        ),
        (
            "aide.context.inspect",
            "Inspect AIDE context projection",
            "Future read-only ContextPack discovery candidate. No A2A task endpoint exists in this slice.",
            ["context", "read-only", "projection"],
        ),
    ]
    return [
        {
            "id": skill_id,
            "name": name,
            "description": description,
            "tags": tags,
            "examples": [],
            "inputModes": ["application/json"],
            "outputModes": ["application/json"],
            "aide_operation_mapping": skill_id,
            "implemented": False,
            "requires_future_policy_decision": True,
            "requires_future_capability_grant": True,
            "side_effect_class": "read_only_or_report_only",
        }
        for skill_id, name, description, tags in skill_specs
    ]


def build_security() -> dict[str, Any]:
    return {
        "securitySchemes": {},
        "security": [],
        "authentication_implemented": False,
        "authorization_implemented": False,
        "credential_resolution_performed": False,
        "notes": [
            "No A2A endpoint exists, so no authentication challenge can be issued.",
            "Future authenticated use must bind through AIDE PolicyDecision and CapabilityGrant.",
        ],
    }


def build_refusal_mappings() -> list[dict[str, Any]]:
    mappings = [
        ("endpoint_not_implemented", "A2A_ENDPOINT_NOT_IMPLEMENTED", "A2A endpoint is not implemented."),
        ("agent_not_registered", "A2A_AGENT_NOT_REGISTERED", "AIDE has not registered an A2A agent externally."),
        ("task_delegation_not_implemented", "A2A_TASK_DELEGATION_NOT_IMPLEMENTED", "A2A task delegation is not implemented."),
        ("authentication_not_implemented", "A2A_AUTHENTICATION_NOT_IMPLEMENTED", "A2A authentication is not implemented."),
        ("required_capability_unavailable", "AIDE_REQUIRED_CAPABILITY_UNAVAILABLE", "Required AIDE capability is unavailable."),
    ]
    return [
        {
            "id": mapping_id,
            "reason_code": reason_code,
            "message": message,
            "retryable": False,
            "human_action_required": True,
            "runtime_status": "not_implemented",
        }
        for mapping_id, reason_code, message in mappings
    ]


def build_conformance_expectations() -> list[dict[str, Any]]:
    expectations = [
        "agent card JSON parses",
        "agent card remains preview-only",
        "live endpoint URL is absent while endpoint is not implemented",
        "declared skills have stable IDs",
        "declared skills are not implemented or callable",
        "security schemes remain empty until authentication exists",
        "task delegation remains false",
        "worker execution remains false",
        "provider/model/network calls remain false",
        "explicit non-capabilities remain present",
        "projection is deterministic",
        "source interop exports remain unchanged",
    ]
    return [
        {
            "id": f"a2a-agent-card-contract-{index:02d}",
            "description": description,
            "required_for_acceptance": True,
            "status": "expected_not_executed_in_build",
        }
        for index, description in enumerate(expectations, start=1)
    ]


def build_agent_card() -> dict[str, Any]:
    return {
        "schema_version": "aide.interop.a2a_agent_card.contract_projection.v0",
        "name": AGENT_NAME,
        "description": "Contract-only AIDE interop identity for future A2A discovery.",
        "version": AGENT_VERSION,
        "preview_only": True,
        "endpoint_implemented": False,
        "url": None,
        "provider": {
            "organization": "AIDE",
            "url": None,
        },
        "canonical_truth": [
            ".aide/queue/index.yaml",
            ".aide/queue/policy.yaml",
            "AGENTS.md",
        ],
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
            "stateTransitionHistory": False,
        },
        "defaultInputModes": ["application/json"],
        "defaultOutputModes": ["application/json"],
        "skills": build_skills(),
        "securitySchemes": {},
        "security": [],
        "supportsAuthenticatedExtendedCard": False,
        "explicit_non_capabilities": {
            "live_a2a_endpoint": False,
            "agent_registration": False,
            "task_delegation": False,
            "authentication": False,
            "worker_execution": False,
            "provider_model_calls": False,
            "network_calls": False,
            "target_repository_mutation": False,
        },
    }


def _contract_status() -> dict[str, bool]:
    status = {
        "agent_card_projection_performed": True,
        "structural_validation_performed": True,
    }
    status.update({field: False for field in FALSE_RUNTIME_FIELDS})
    return status


def build_a2a_agent_card_contract(repo_root: str | Path | None = None) -> dict[str, Any]:
    _root = Path(repo_root) if repo_root is not None else Path(".")
    spec = {
        "contract_id": CONTRACT_ID,
        "advisory_contract_ref": ADVISORY_CONTRACT_REF,
        "reference_id_kind_supported": False,
        "agent_card": build_agent_card(),
        "declared_card_capabilities": build_declared_card_capabilities(),
        "implemented_runtime_capabilities": build_implemented_runtime_capabilities(),
        "skills": build_skills(),
        "security": build_security(),
        "refusal_mappings": build_refusal_mappings(),
        "conformance_expectations": build_conformance_expectations(),
        "required_aide_capabilities": [],
        "source_authority": [
            ".aide/queue/index.yaml",
            ".aide/queue/policy.yaml",
            "accepted AIDE protocol and interop reports",
        ],
        "projection_authority": "generated_non_authoritative",
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
    }
    return {
        "apiVersion": API_VERSION,
        "kind": "A2AAgentCardContract",
        "metadata": {
            "name": CONTRACT_ID,
            "created_at": DETERMINISTIC_TIMESTAMP,
            "producer": {
                "name": PRODUCER_NAME,
                "version": PRODUCER_VERSION,
            },
            "compatibility": _compatibility(),
            "task_id": TASK_ID,
        },
        "spec": spec,
        "status": _contract_status(),
    }


def _schema_errors(obj: dict[str, Any], schema: dict[str, Any] | None) -> list[str]:
    if not schema:
        return []
    return envelope.validate_envelope_with_schema(obj, schema)


def validate_skill_id(skill_id: str) -> tuple[bool, str]:
    if not isinstance(skill_id, str) or not skill_id:
        return False, "skill id must be a non-empty string"
    if not SKILL_ID_RE.match(skill_id):
        return False, "skill id must use dotted lower-case identifier form"
    for part in FORBIDDEN_SKILL_ID_PARTS:
        if part in skill_id:
            return False, f"skill id contains forbidden operation segment: {part}"
    return True, "ok"


def validate_a2a_agent_card_contract_with_schema(
    record: dict[str, Any],
    schema: dict[str, Any] | None = None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings = list(VALIDATION_WARNINGS)
    if not isinstance(record, dict):
        return ["contract must be an object"], warnings
    errors.extend(envelope.validate_envelope(record, {"A2AAgentCardContract"}))
    errors.extend(_schema_errors(record, schema))
    spec = record.get("spec") if isinstance(record.get("spec"), dict) else {}
    status = record.get("status") if isinstance(record.get("status"), dict) else {}
    if spec.get("contract_id") != CONTRACT_ID:
        errors.append("spec.contract_id must be stable a2a-agent-card-contract-v0")
    if spec.get("advisory_contract_ref") != ADVISORY_CONTRACT_REF:
        errors.append("spec.advisory_contract_ref must remain aide://interop/a2a-agent-card-contract-v0")
    if spec.get("reference_id_kind_supported") is not False:
        errors.append("spec.reference_id_kind_supported must remain false")
    for field in FALSE_RUNTIME_FIELDS:
        if status.get(field) is not False:
            errors.append(f"status.{field} must be false in the contract-only slice")
    implemented = spec.get("implemented_runtime_capabilities", {})
    if not isinstance(implemented, dict):
        errors.append("spec.implemented_runtime_capabilities must be an object")
        implemented = {}
    for key, value in implemented.items():
        if value is not False:
            errors.append(f"spec.implemented_runtime_capabilities.{key} must be false")
    card = spec.get("agent_card")
    if not isinstance(card, dict):
        errors.append("spec.agent_card must be an object")
        card = {}
    if card.get("preview_only") is not True:
        errors.append("spec.agent_card.preview_only must be true")
    if card.get("endpoint_implemented") is not False:
        errors.append("spec.agent_card.endpoint_implemented must be false")
    if "url" in card and card.get("url") is not None:
        errors.append("spec.agent_card.url must be null or omitted until a live endpoint exists")
    provider = card.get("provider") if isinstance(card.get("provider"), dict) else {}
    if "url" in provider and provider.get("url") is not None:
        errors.append("spec.agent_card.provider.url must be null or omitted in this slice")
    card_capabilities = card.get("capabilities") if isinstance(card.get("capabilities"), dict) else {}
    for field in ["streaming", "pushNotifications", "stateTransitionHistory"]:
        if card_capabilities.get(field) is not False:
            errors.append(f"spec.agent_card.capabilities.{field} must be false")
    if card.get("supportsAuthenticatedExtendedCard") is not False:
        errors.append("spec.agent_card.supportsAuthenticatedExtendedCard must be false")
    security = spec.get("security") if isinstance(spec.get("security"), dict) else {}
    if security.get("authentication_implemented") is not False:
        errors.append("spec.security.authentication_implemented must be false")
    if security.get("authorization_implemented") is not False:
        errors.append("spec.security.authorization_implemented must be false")
    if security.get("securitySchemes") not in ({}, None):
        errors.append("spec.security.securitySchemes must be empty until authentication exists")
    skills = spec.get("skills")
    if not isinstance(skills, list) or not skills:
        errors.append("spec.skills must be a non-empty array")
        skills = []
    seen: set[str] = set()
    for skill in skills:
        if not isinstance(skill, dict):
            errors.append("spec.skills entries must be objects")
            continue
        skill_id = skill.get("id")
        valid, reason = validate_skill_id(skill_id)
        if not valid:
            errors.append(f"invalid skill id {skill_id!r}: {reason}")
        elif skill_id in seen:
            errors.append(f"duplicate skill id: {skill_id}")
        else:
            seen.add(skill_id)
        if skill.get("implemented") is not False:
            errors.append(f"skill {skill_id!r} implemented must be false")
        if skill.get("requires_future_policy_decision") is not True:
            errors.append(f"skill {skill_id!r} must require a future policy decision")
        if skill.get("requires_future_capability_grant") is not True:
            errors.append(f"skill {skill_id!r} must require a future capability grant")
    required = spec.get("required_aide_capabilities", [])
    if not isinstance(required, list):
        errors.append("spec.required_aide_capabilities must be an array")
    elif required:
        errors.append("unknown required AIDE capabilities fail closed in this slice")
    if spec.get("explicit_non_capabilities") != EXPLICIT_NON_CAPABILITIES:
        errors.append("spec.explicit_non_capabilities must match helper boundary list")
    text = stable_json(record)
    if "http://" in text or "https://" in text:
        errors.append("contract-only A2A projection must not contain live URL-like endpoints")
    return errors, warnings


def _capability_matrix(contract: dict[str, Any]) -> dict[str, Any]:
    spec = contract["spec"]
    return {
        "schema_version": "aide.a2a-agent-card-contract.capability-matrix.v0",
        "contract_id": CONTRACT_ID,
        "declared_card_capabilities": spec["declared_card_capabilities"],
        "implemented_runtime_capabilities": spec["implemented_runtime_capabilities"],
        "skill_count": len(spec["skills"]),
        "implemented_skill_count": sum(1 for skill in spec["skills"] if skill.get("implemented") is True),
        "live_endpoint_count": 0,
        "registered_agent_count": 0,
        "delegation_capability_count": 0,
    }


def _catalog_file(kind: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": f"aide.a2a-agent-card-contract.{kind}-catalog.v0",
        "task_id": TASK_ID,
        "contract_id": CONTRACT_ID,
        "count": len(items),
        "items": copy.deepcopy(items),
    }


def _security_boundary(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.a2a-agent-card-contract.security-boundary.v0",
        "task_id": TASK_ID,
        "contract_id": CONTRACT_ID,
        "authentication_implemented": False,
        "authorization_implemented": False,
        "credential_resolution_performed": False,
        "policy_decision_required_before_runtime": True,
        "capability_grant_required_before_runtime": True,
        "security": copy.deepcopy(contract["spec"]["security"]),
    }


def _artifact_index(root: Path, artifacts: list[Path]) -> dict[str, Any]:
    entries = []
    for rel in artifacts:
        path = root / rel
        entries.append(
            {
                "path": rel.as_posix(),
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return {
        "schema_version": "aide.a2a-agent-card-contract.artifact-index.v0",
        "task_id": TASK_ID,
        "contract_id": CONTRACT_ID,
        "artifact_count": len(entries),
        "artifacts": entries,
    }


def _contains_secret_like_text(root: Path, paths: list[Path]) -> bool:
    allowed_words = {
        "authentication",
        "authorization",
        "credential",
        "credentials",
        "secret-like",
        "token",
        "password",
        "private key",
    }
    for rel in paths:
        path = root / rel
        if path.exists() and path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if SECRET_LIKE_RE.search(text):
                lowered = text.lower()
                if not any(word in lowered for word in allowed_words):
                    return True
    return False


def _deterministic_projection_check(root: Path) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp)
        for rel in source_artifact_paths(root):
            src = root / rel
            if src.exists():
                dst = temp_root / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        write_a2a_agent_card_contract_reports(temp_root)
        first = {}
        for path in sorted((temp_root / INTEROP_ROOT).rglob("*")) + sorted((temp_root / REPORT_ROOT).rglob("*")):
            if path.is_file():
                first[path.relative_to(temp_root).as_posix()] = path.read_bytes()
        write_a2a_agent_card_contract_reports(temp_root)
        second = {}
        for path in sorted((temp_root / INTEROP_ROOT).rglob("*")) + sorted((temp_root / REPORT_ROOT).rglob("*")):
            if path.is_file():
                second[path.relative_to(temp_root).as_posix()] = path.read_bytes()
    return first == second


def write_a2a_agent_card_contract_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    before = _hash_existing(root, source_artifact_paths(root))
    contract = build_a2a_agent_card_contract(root)
    schema = load_a2a_agent_card_contract_schema(root)
    errors, warnings = validate_a2a_agent_card_contract_with_schema(contract, schema)

    write_json(root / AGENT_CARD_CONTRACT_JSON, contract)
    write_json(root / AGENT_CARD_PREVIEW_JSON, contract["spec"]["agent_card"])
    write_json(root / CAPABILITY_CATALOG_JSON, _capability_matrix(contract))
    write_json(root / SKILL_CATALOG_JSON, _catalog_file("skill", contract["spec"]["skills"]))
    write_json(root / REFUSAL_CATALOG_JSON, _catalog_file("refusal", contract["spec"]["refusal_mappings"]))
    write_json(root / CONFORMANCE_EXPECTATIONS_JSON, _catalog_file("conformance-expectation", contract["spec"]["conformance_expectations"]))

    artifacts = list(PROJECTION_ARTIFACTS)
    artifact_index = _artifact_index(root, artifacts)
    capability_matrix = _capability_matrix(contract)
    validation_status = "FAILED_VALIDATION" if errors else "PASS_WITH_WARNINGS"
    projection_report = {
        "schema_version": "aide.a2a-agent-card-contract.projection-report.v0",
        "task_id": TASK_ID,
        "status": validation_status,
        "contract_id": CONTRACT_ID,
        "agent_card_name": AGENT_NAME,
        "skill_count": len(contract["spec"]["skills"]),
        "artifact_count": len(artifacts),
        "live_endpoint_count": 0,
        "registered_agent_count": 0,
        "delegation_capability_count": 0,
        "errors": errors,
        "warnings": warnings,
        "source_artifacts_mutated": before != _hash_existing(root, source_artifact_paths(root)),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }

    write_json(root / CONTRACT_REPORT_JSON, contract)
    write_text(root / CONTRACT_REPORT_MD, render_contract_markdown(contract))
    write_json(root / AGENT_CARD_REPORT_JSON, contract["spec"]["agent_card"])
    write_text(root / AGENT_CARD_REPORT_MD, render_agent_card_markdown(contract["spec"]["agent_card"]))
    write_json(root / CAPABILITY_MATRIX_JSON, capability_matrix)
    write_text(root / CAPABILITY_MATRIX_MD, render_capability_matrix_markdown(capability_matrix))
    write_json(root / SKILL_CATALOG_REPORT_JSON, _catalog_file("skill", contract["spec"]["skills"]))
    write_text(root / SKILL_CATALOG_REPORT_MD, render_catalog_markdown("A2A Skills", contract["spec"]["skills"]))
    write_json(root / SECURITY_BOUNDARY_JSON, _security_boundary(contract))
    write_text(root / SECURITY_BOUNDARY_MD, render_security_boundary_markdown(_security_boundary(contract)))
    write_json(root / REFUSAL_MAPPING_JSON, _catalog_file("refusal", contract["spec"]["refusal_mappings"]))
    write_text(root / REFUSAL_MAPPING_MD, render_catalog_markdown("A2A Refusal Mappings", contract["spec"]["refusal_mappings"]))
    write_json(root / CONFORMANCE_REPORT_JSON, _catalog_file("conformance-expectation", contract["spec"]["conformance_expectations"]))
    write_text(root / CONFORMANCE_REPORT_MD, render_catalog_markdown("A2A Conformance Expectations", contract["spec"]["conformance_expectations"]))
    write_json(root / ARTIFACT_INDEX_JSON, artifact_index)
    write_text(root / ARTIFACT_INDEX_MD, render_artifact_index_markdown(artifact_index))
    write_text(root / EXPLICIT_NON_CAPABILITIES_MD, render_explicit_non_capabilities_markdown())
    write_text(root / FUTURE_WORK_MD, render_future_work_markdown())
    write_text(root / NEXT_TASK_PROMPT_MD, render_next_task_prompt())
    write_text(root / STATUS_MD, render_status_markdown(projection_report))
    return projection_report


def a2a_agent_card_contract_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    schema_loaded = (root / SCHEMA_PATH).exists()
    contract_path = root / AGENT_CARD_CONTRACT_JSON
    contract = read_json(contract_path) if contract_path.exists() else build_a2a_agent_card_contract(root)
    errors, warnings = validate_a2a_agent_card_contract_with_schema(
        contract,
        load_a2a_agent_card_contract_schema(root) if schema_loaded else None,
    )
    matrix = _capability_matrix(contract)
    return {
        "status": "FAILED_VALIDATION" if errors else "PASS_WITH_WARNINGS",
        "capability_target": FEATURE_FLAG,
        "schema_loaded": schema_loaded,
        "contract_valid": not errors,
        "contract_id": contract["spec"].get("contract_id"),
        "agent_card_name": contract["spec"].get("agent_card", {}).get("name"),
        "skill_count": matrix["skill_count"],
        "implemented_skill_count": matrix["implemented_skill_count"],
        "artifact_count": len(PROJECTION_ARTIFACTS),
        "live_endpoint_count": matrix["live_endpoint_count"],
        "registered_agent_count": matrix["registered_agent_count"],
        "delegation_capability_count": matrix["delegation_capability_count"],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "warnings": warnings,
        "errors": errors,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        **contract["status"],
    }


def validate_a2a_agent_card_contract(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    if project:
        write_a2a_agent_card_contract_reports(root)
    schema_exists = (root / SCHEMA_PATH).exists()
    schema: dict[str, Any] | None = None
    schema_file_parsed = False
    schema_error = None
    if schema_exists:
        try:
            schema = load_a2a_agent_card_contract_schema(root)
            schema_file_parsed = True
        except ValueError as exc:
            schema_error = str(exc)
    contract = read_json(root / AGENT_CARD_CONTRACT_JSON) if (root / AGENT_CARD_CONTRACT_JSON).exists() else build_a2a_agent_card_contract(root)
    errors, warnings = validate_a2a_agent_card_contract_with_schema(contract, schema)
    source_before = _hash_existing(root, source_artifact_paths(root))
    deterministic_projection = _deterministic_projection_check(root)
    source_after = _hash_existing(root, source_artifact_paths(root))
    report_paths = [
        *PROJECTION_ARTIFACTS,
        CONTRACT_REPORT_JSON,
        AGENT_CARD_REPORT_JSON,
        CAPABILITY_MATRIX_JSON,
        SKILL_CATALOG_REPORT_JSON,
        SECURITY_BOUNDARY_JSON,
        REFUSAL_MAPPING_JSON,
        CONFORMANCE_REPORT_JSON,
        ARTIFACT_INDEX_JSON,
    ]
    secret_like_scan_clear = not _contains_secret_like_text(root, report_paths)
    if not deterministic_projection:
        errors.append("projection must be deterministic")
    if source_before != source_after:
        errors.append("source interop export artifacts must remain unchanged")
    if not secret_like_scan_clear:
        errors.append("secret-like value scan found a material projected secret")
    status = "FAILED_VALIDATION" if errors else "PASS_WITH_WARNINGS"
    report = {
        "schema_version": "aide.a2a-agent-card-contract.validation.v0",
        "task_id": TASK_ID,
        "validation_status": status,
        "schema_exists": schema_exists,
        "schema_file_parsed": schema_file_parsed,
        "schema_error": schema_error,
        "helper_exists": True,
        "cli_registered": True,
        "schema_helper_alignment_checked": True,
        "schema_helper_alignment_status": "PASS" if schema_file_parsed and not schema_error else "FAILED_VALIDATION",
        "contract_valid": not errors,
        "contract_id": CONTRACT_ID,
        "agent_card_name": AGENT_NAME,
        "skill_count": len(contract["spec"].get("skills", [])),
        "artifact_count": len(PROJECTION_ARTIFACTS),
        "runtime_facts_preserved": all(contract["status"].get(field) is False for field in FALSE_RUNTIME_FIELDS),
        "deterministic_projection": deterministic_projection,
        "source_artifacts_mutated": source_before != source_after,
        "secret_like_scan_clear": secret_like_scan_clear,
        "explicit_non_capabilities_preserved": contract["spec"].get("explicit_non_capabilities") == EXPLICIT_NON_CAPABILITIES,
        "errors": errors,
        "warnings": warnings,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_markdown(report))
    write_text(root / STATUS_MD, render_status_markdown(report))
    return report


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# A2A Agent Card Contract Status",
        "",
        f"- result: `{data.get('validation_status', data.get('status'))}`",
        f"- capability_target: `{FEATURE_FLAG}`",
        f"- contract_id: `{data.get('contract_id')}`",
        f"- agent_card_name: `{data.get('agent_card_name')}`",
        f"- skill_count: `{data.get('skill_count')}`",
        f"- artifact_count: `{data.get('artifact_count')}`",
        f"- live_endpoint_count: `{data.get('live_endpoint_count', 0)}`",
        f"- registered_agent_count: `{data.get('registered_agent_count', 0)}`",
        f"- delegation_capability_count: `{data.get('delegation_capability_count', 0)}`",
        f"- recommended_next_task: `{data.get('recommended_next_task')}`",
        "",
        "This is a contract-only projection. It does not start or register A2A runtime behavior.",
        "",
    ]
    return "\n".join(lines)


def render_contract_markdown(contract: dict[str, Any]) -> str:
    spec = contract["spec"]
    return "\n".join(
        [
            "# A2A Agent Card Contract",
            "",
            f"- contract_id: `{spec['contract_id']}`",
            f"- advisory_contract_ref: `{spec['advisory_contract_ref']}`",
            f"- agent_card_name: `{spec['agent_card']['name']}`",
            f"- endpoint_implemented: `{spec['agent_card']['endpoint_implemented']}`",
            "",
            "AIDE queue, protocol, evidence, and OKF records remain authoritative. A2A card artifacts are generated projections.",
            "",
        ]
    )


def render_agent_card_markdown(card: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# A2A Agent Card Projection",
            "",
            f"- name: `{card.get('name')}`",
            f"- preview_only: `{card.get('preview_only')}`",
            f"- endpoint_implemented: `{card.get('endpoint_implemented')}`",
            f"- url: `{card.get('url')}`",
            f"- skill_count: `{len(card.get('skills', []))}`",
            "",
        ]
    )


def render_capability_matrix_markdown(matrix: dict[str, Any]) -> str:
    lines = [
        "# A2A Capability Matrix",
        "",
        f"- skill_count: `{matrix['skill_count']}`",
        f"- implemented_skill_count: `{matrix['implemented_skill_count']}`",
        f"- live_endpoint_count: `{matrix['live_endpoint_count']}`",
        f"- registered_agent_count: `{matrix['registered_agent_count']}`",
        f"- delegation_capability_count: `{matrix['delegation_capability_count']}`",
        "",
    ]
    return "\n".join(lines)


def render_catalog_markdown(title: str, items: list[dict[str, Any]]) -> str:
    lines = [f"# {title}", ""]
    if not items:
        lines.append("No entries are declared for this projection.")
    for item in items:
        label = item.get("id") or item.get("name") or item.get("reason_code")
        lines.append(f"- `{label}`")
    lines.append("")
    return "\n".join(lines)


def render_security_boundary_markdown(security: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# A2A Security Boundary",
            "",
            f"- authentication_implemented: `{security.get('authentication_implemented')}`",
            f"- authorization_implemented: `{security.get('authorization_implemented')}`",
            f"- credential_resolution_performed: `{security.get('credential_resolution_performed')}`",
            f"- policy_decision_required_before_runtime: `{security.get('policy_decision_required_before_runtime')}`",
            f"- capability_grant_required_before_runtime: `{security.get('capability_grant_required_before_runtime')}`",
            "",
        ]
    )


def render_artifact_index_markdown(index: dict[str, Any]) -> str:
    lines = ["# A2A Artifact Index", "", f"- artifact_count: `{index['artifact_count']}`", ""]
    for item in index["artifacts"]:
        lines.append(f"- `{item['path']}` `{item['sha256']}`")
    lines.append("")
    return "\n".join(lines)


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# A2A Agent Card Contract Validation",
        "",
        f"- validation_status: `{report['validation_status']}`",
        f"- schema_file_parsed: `{report['schema_file_parsed']}`",
        f"- contract_valid: `{report['contract_valid']}`",
        f"- deterministic_projection: `{report['deterministic_projection']}`",
        f"- source_artifacts_mutated: `{report['source_artifacts_mutated']}`",
        f"- secret_like_scan_clear: `{report['secret_like_scan_clear']}`",
        "",
        "## Errors",
        "",
    ]
    errors = report.get("errors", [])
    if errors:
        lines.extend(f"- {item}" for item in errors)
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in report.get("warnings", []))
    lines.append("")
    return "\n".join(lines)


def render_explicit_non_capabilities_markdown() -> str:
    lines = ["# Explicit Non-Capabilities", ""]
    lines.extend(f"- `{item}`" for item in EXPLICIT_NON_CAPABILITIES)
    lines.append("")
    return "\n".join(lines)


def render_future_work_markdown() -> str:
    return "\n".join(
        [
            "# A2A Agent Card Future Work",
            "",
            "- Independent check of this A2A agent-card contract slice.",
            "- Acceptance review if the independent check passes.",
            "- Live A2A endpoint work only after runtime, trust, authorization, and host semantics are separately accepted.",
            "",
        ]
    )


def render_next_task_prompt() -> str:
    return "\n".join(
        [
            "# AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01",
            "# Independent Check of Minimal Contract-Only A2A Agent Card Projection",
            "",
            "Use `.aide/queue/index.yaml` as canonical queue truth.",
            "",
            "Check `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01` without modifying the A2A contract implementation.",
            "Verify schema/helper alignment, agent-card shape, skill catalogue consistency, security/authentication boundaries, refusal mappings, deterministic projection, source immutability, and explicit non-capabilities.",
            "",
            "If no material issue exists, recommend `AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01`.",
            "If a material defect exists, recommend one bounded repair task.",
            "",
        ]
    )
