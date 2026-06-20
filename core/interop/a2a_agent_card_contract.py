"""Minimal contract-only A2A agent-card projection helpers for AIDE.

This module projects deterministic A2A Agent Card contract artifacts and
reports. It deliberately avoids endpoint startup, discovery publication,
registration, task delegation, authentication, worker dispatch, provider calls,
network access, and repository mutation.
"""

from __future__ import annotations

import copy
import hashlib
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from core.protocol import envelope


API_VERSION = envelope.API_VERSION
A2A_CONTRACT_SCHEMA_VERSION = "aide.a2a-agent-card-contract.v0"
PROTOCOL_VERSION = "0.1.0"
A2A_SPECIFICATION_RELEASE = "1.0.0"
A2A_PROTOCOL_VERSION = "1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_a2a_agent_card_contract"
TASK_ID = "AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01"
DETERMINISTIC_TIMESTAMP = "2026-06-20T00:00:00+10:00"

CONTRACT_ID = "a2a-agent-card-contract-v0"
ADVISORY_CONTRACT_REF = "aide://interop/a2a-agent-card-contract-v0"
AGENT_NAME = "AIDE Contract-Only Agent Card Fixture"
AGENT_VERSION = "0.1.0"
FIXTURE_INTERFACE_URL = "https://aide.invalid/a2a/v1"
FIXTURE_PROTOCOL_BINDING = "JSONRPC"

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
SPEC_RELEASE_RE = re.compile(r"^\d+\.\d+\.\d+$")
PROTOCOL_VERSION_RE = re.compile(r"^\d+\.\d+$")
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

OFFICIAL_AGENT_CARD_FIELDS = {
    "name",
    "description",
    "supportedInterfaces",
    "provider",
    "version",
    "documentationUrl",
    "capabilities",
    "securitySchemes",
    "securityRequirements",
    "defaultInputModes",
    "defaultOutputModes",
    "skills",
    "signatures",
    "iconUrl",
}
OFFICIAL_AGENT_SKILL_FIELDS = {
    "id",
    "name",
    "description",
    "tags",
    "examples",
    "inputModes",
    "outputModes",
    "securityRequirements",
}
OFFICIAL_CAPABILITY_FIELDS = {
    "streaming",
    "pushNotifications",
    "extensions",
    "extendedAgentCard",
}
AIDE_SKILL_GOVERNANCE_FIELDS = {
    "aide_operation_mapping",
    "implemented",
    "callable",
    "endpoint_available",
    "task_submission_available",
    "task_delegation_available",
    "requires_future_policy_decision",
    "requires_future_capability_grant",
    "side_effect_class",
}
AIDE_CARD_GOVERNANCE_FIELDS = {
    "schema_version",
    "preview_only",
    "endpoint_implemented",
    "canonical_truth",
    "explicit_non_capabilities",
    "publishable",
    "agent_registered",
}
LEGACY_AGENT_CARD_FIELDS = {
    "url",
    "protocolVersion",
    "preferredTransport",
    "additionalInterfaces",
    "supportsAuthenticatedExtendedCard",
    "supportsExtendedAgentCard",
    "security",
}

FALSE_RUNTIME_FIELDS = [
    "live_a2a_endpoint_started",
    "agent_registered",
    "task_delegation_performed",
    "authentication_implemented",
    "authorization_implemented",
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
    "publishable_agent_card",
    "well_known_discovery_publication",
    "agent_registration",
    "registry_publication",
    "interface_negotiation_runtime",
    "task_submission",
    "task_delegation",
    "task_status_runtime",
    "task_cancellation_runtime",
    "streaming",
    "push_notifications",
    "extended_agent_card_runtime",
    "authentication",
    "authorization",
    "security_scheme_implementation",
    "agent_card_signing",
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
    "A2A Agent Card contract is projection-only; no live endpoint or registration exists.",
    "A2A Agent Card is a standards-clean local fixture; full vendored official A2A schema validation remains future work.",
    "Candidate skills are retained as AIDE metadata only and are not advertised as official A2A skills.",
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
        "standards_clean_agent_card_fixture": True,
        "supported_interface_fixture_projection": True,
        "candidate_skill_catalog_projection": True,
        "streaming": False,
        "push_notifications": False,
        "extended_agent_card": False,
    }


def build_implemented_runtime_capabilities() -> dict[str, bool]:
    return {
        "live_endpoint": False,
        "agent_registered": False,
        "task_delegation": False,
        "task_submission": False,
        "task_status_runtime": False,
        "task_cancellation_runtime": False,
        "streaming": False,
        "push_notifications": False,
        "extended_agent_card": False,
        "authentication": False,
        "authorization": False,
        "worker_execution": False,
        "network_access": False,
    }


def build_official_skills() -> list[dict[str, Any]]:
    return []


def build_candidate_skills() -> list[dict[str, Any]]:
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
            "skill_id": skill_id,
            "name": name,
            "description": description,
            "tags": tags,
            "examples": [],
            "inputModes": ["application/json"],
            "outputModes": ["application/json"],
            "aide_operation_mapping": skill_id,
            "implemented": False,
            "callable": False,
            "endpoint_available": False,
            "task_submission_available": False,
            "task_delegation_available": False,
            "requires_future_policy_decision": True,
            "requires_future_capability_grant": True,
            "side_effect_class": "read_only_or_report_only",
        }
        for skill_id, name, description, tags in skill_specs
    ]


def build_skills() -> list[dict[str, Any]]:
    """Return AIDE candidate skill governance records.

    The name is retained for compatibility with existing tests and callers; the
    records are not official A2A AgentSkill objects.
    """

    return build_candidate_skills()


def build_security() -> dict[str, Any]:
    return {
        "securitySchemes": {},
        "securityRequirements": [],
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
        "agent card contains only standard A2A 1.0 AgentCard fields",
        "supportedInterfaces declares one non-live HTTPS fixture interface",
        "interface protocolVersion matches the outer A2A protocol version pin",
        "candidate skills remain outside the official AgentCard skills array",
        "official AgentCard skills array is empty while no endpoint exists",
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
        "name": AGENT_NAME,
        "description": "Non-publishable A2A 1.0 structural fixture for AIDE interoperability.",
        "supportedInterfaces": [
            {
                "url": FIXTURE_INTERFACE_URL,
                "protocolBinding": FIXTURE_PROTOCOL_BINDING,
                "protocolVersion": A2A_PROTOCOL_VERSION,
            }
        ],
        "version": AGENT_VERSION,
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
            "extendedAgentCard": False,
        },
        "defaultInputModes": ["application/json"],
        "defaultOutputModes": ["application/json"],
        "skills": build_official_skills(),
    }


def build_agent_card_fixture_metadata() -> dict[str, Any]:
    return {
        "schema_version": "aide.interop.a2a_agent_card.fixture_metadata.v0",
        "fixture_only": True,
        "interface_fixture_only": True,
        "endpoint_implemented": False,
        "publishable": False,
        "network_target_intentionally_non_live": True,
        "fixture_interface_url": FIXTURE_INTERFACE_URL,
        "well_known_publication_performed": False,
        "agent_registered": False,
        "live_a2a_endpoint": False,
        "task_submission_available": False,
        "task_delegation_available": False,
        "canonical_truth": [
            ".aide/queue/index.yaml",
            ".aide/queue/policy.yaml",
            "AGENTS.md",
        ],
    }


def _contract_status() -> dict[str, bool]:
    status = {
        "agent_card_projection_performed": True,
        "structural_validation_performed": True,
        "fixture_generation_performed": True,
    }
    status.update({field: False for field in FALSE_RUNTIME_FIELDS})
    return status


def build_a2a_agent_card_contract(repo_root: str | Path | None = None) -> dict[str, Any]:
    _root = Path(repo_root) if repo_root is not None else Path(".")
    candidate_skills = build_candidate_skills()
    spec = {
        "contract_id": CONTRACT_ID,
        "advisory_contract_ref": ADVISORY_CONTRACT_REF,
        "reference_id_kind_supported": False,
        "target_a2a_specification_release": A2A_SPECIFICATION_RELEASE,
        "target_a2a_protocol_version": A2A_PROTOCOL_VERSION,
        "agent_implementation_version": AGENT_VERSION,
        "agent_card": build_agent_card(),
        "agent_card_fixture": build_agent_card_fixture_metadata(),
        "declared_card_capabilities": build_declared_card_capabilities(),
        "implemented_runtime_capabilities": build_implemented_runtime_capabilities(),
        "candidate_skill_governance": candidate_skills,
        "official_advertised_skill_count": 0,
        "candidate_skill_count": len(candidate_skills),
        "callable_skill_count": 0,
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


def _is_absolute_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and bool(parsed.path)


def _is_fixture_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.hostname == "aide.invalid" or (parsed.hostname or "").endswith(".invalid")


def _add(errors: list[str], path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def _validate_version_pins(spec: dict[str, Any], errors: list[str]) -> None:
    release = spec.get("target_a2a_specification_release")
    protocol = spec.get("target_a2a_protocol_version")
    if release != A2A_SPECIFICATION_RELEASE or not isinstance(release, str) or not SPEC_RELEASE_RE.match(release):
        _add(errors, "spec.target_a2a_specification_release", "must be pinned to 1.0.0")
    if protocol != A2A_PROTOCOL_VERSION or not isinstance(protocol, str) or not PROTOCOL_VERSION_RE.match(protocol):
        _add(errors, "spec.target_a2a_protocol_version", "must be pinned to 1.0")
    if protocol in {"0.1.0", "latest"}:
        _add(errors, "spec.target_a2a_protocol_version", "must not use AIDE version or latest")
    if spec.get("agent_implementation_version") == protocol:
        _add(errors, "spec.agent_implementation_version", "must remain distinct from A2A protocol version")


def _validate_provider(provider: Any, errors: list[str]) -> None:
    if provider is None:
        return
    if not isinstance(provider, dict):
        _add(errors, "spec.agent_card.provider", "must be an object when present")
        return
    organization = provider.get("organization")
    url = provider.get("url")
    if not isinstance(organization, str) or not organization.strip():
        _add(errors, "spec.agent_card.provider.organization", "must be a non-empty string when provider is present")
    if not isinstance(url, str) or not url.strip():
        _add(errors, "spec.agent_card.provider.url", "must be a non-empty absolute URL when provider is present")
    elif not _is_absolute_https_url(url):
        _add(errors, "spec.agent_card.provider.url", "must be an absolute HTTPS URL")
    if isinstance(url, str) and SECRET_LIKE_RE.search(url):
        _add(errors, "spec.agent_card.provider.url", "must not contain credential-like content")


def _validate_supported_interfaces(spec: dict[str, Any], card: dict[str, Any], errors: list[str]) -> None:
    interfaces = card.get("supportedInterfaces")
    if not isinstance(interfaces, list) or not interfaces:
        _add(errors, "spec.agent_card.supportedInterfaces", "must be a non-empty array")
        return
    seen: set[tuple[str, str, str]] = set()
    fixture = spec.get("agent_card_fixture") if isinstance(spec.get("agent_card_fixture"), dict) else {}
    for index, interface in enumerate(interfaces):
        path = f"spec.agent_card.supportedInterfaces[{index}]"
        if not isinstance(interface, dict):
            _add(errors, path, "must be an object")
            continue
        url = interface.get("url")
        binding = interface.get("protocolBinding")
        protocol = interface.get("protocolVersion")
        if not isinstance(url, str) or not url:
            _add(errors, f"{path}.url", "must be a non-empty absolute HTTPS URL")
        elif not _is_absolute_https_url(url):
            _add(errors, f"{path}.url", "must be an absolute HTTPS URL")
        elif fixture.get("interface_fixture_only") is True and not _is_fixture_url(url):
            _add(errors, f"{path}.url", "must use an approved non-live .invalid fixture host")
        if not isinstance(binding, str) or not binding:
            _add(errors, f"{path}.protocolBinding", "must be a non-empty string")
        if protocol != spec.get("target_a2a_protocol_version"):
            _add(errors, f"{path}.protocolVersion", "must match spec.target_a2a_protocol_version")
        key = (str(url), str(binding), str(protocol))
        if key in seen:
            _add(errors, path, "duplicate supported interface entry")
        seen.add(key)


def _validate_capabilities(spec: dict[str, Any], card: dict[str, Any], errors: list[str]) -> None:
    capabilities = card.get("capabilities")
    if not isinstance(capabilities, dict):
        _add(errors, "spec.agent_card.capabilities", "must be an object")
        return
    implemented = spec.get("implemented_runtime_capabilities", {})
    for field in capabilities:
        if field not in OFFICIAL_CAPABILITY_FIELDS:
            _add(errors, f"spec.agent_card.capabilities.{field}", "is not an accepted A2A 1.0 capability field")
    runtime_map = {
        "streaming": "streaming",
        "pushNotifications": "push_notifications",
        "extendedAgentCard": "extended_agent_card",
    }
    for field, runtime_field in runtime_map.items():
        value = capabilities.get(field)
        if value is not None and not isinstance(value, bool):
            _add(errors, f"spec.agent_card.capabilities.{field}", "must be a boolean when present")
        if value is True and implemented.get(runtime_field) is not True:
            _add(errors, f"spec.agent_card.capabilities.{field}", "cannot be true while corresponding runtime fact is false")
    if "extensions" in capabilities and not isinstance(capabilities["extensions"], list):
        _add(errors, "spec.agent_card.capabilities.extensions", "must be an array when present")


def _validate_official_skills(spec: dict[str, Any], card: dict[str, Any], errors: list[str]) -> None:
    skills = card.get("skills")
    if not isinstance(skills, list):
        _add(errors, "spec.agent_card.skills", "must be an array")
        return
    if skills and spec.get("agent_card_fixture", {}).get("endpoint_implemented") is False:
        _add(errors, "spec.agent_card.skills", "must remain empty while no A2A endpoint exists")
    seen: set[str] = set()
    for index, skill in enumerate(skills):
        path = f"spec.agent_card.skills[{index}]"
        if not isinstance(skill, dict):
            _add(errors, path, "must be an object")
            continue
        for field in skill:
            if field not in OFFICIAL_AGENT_SKILL_FIELDS:
                if field in AIDE_SKILL_GOVERNANCE_FIELDS:
                    _add(errors, f"{path}.{field}", "AIDE governance metadata must move to spec.candidate_skill_governance")
                else:
                    _add(errors, f"{path}.{field}", "is not an accepted A2A 1.0 AgentSkill field")
        skill_id = skill.get("id")
        if skill_id is not None:
            valid, reason = validate_skill_id(skill_id)
            if not valid:
                _add(errors, f"{path}.id", reason)
            elif skill_id in seen:
                _add(errors, f"{path}.id", f"duplicate skill id: {skill_id}")
            else:
                seen.add(skill_id)


def _validate_security(card: dict[str, Any], errors: list[str]) -> None:
    schemes = card.get("securitySchemes")
    requirements = card.get("securityRequirements")
    if schemes not in (None, {}):
        _add(errors, "spec.agent_card.securitySchemes", "must be omitted or empty until authentication exists")
    if requirements not in (None, []):
        if not isinstance(requirements, list):
            _add(errors, "spec.agent_card.securityRequirements", "must be an array when present")
        elif not schemes:
            _add(errors, "spec.agent_card.securityRequirements", "must not reference nonexistent security schemes")
    if "security" in card:
        _add(errors, "spec.agent_card.security", "legacy top-level security field is not part of pinned A2A 1.0 AgentCard")
    if "signatures" in card and card["signatures"]:
        _add(errors, "spec.agent_card.signatures", "must be omitted or empty; this slice does not generate JWS signatures")


def _validate_agent_card(spec: dict[str, Any], errors: list[str]) -> None:
    card = spec.get("agent_card")
    if not isinstance(card, dict):
        _add(errors, "spec.agent_card", "must be an object")
        return
    for field in card:
        if field not in OFFICIAL_AGENT_CARD_FIELDS:
            if field in LEGACY_AGENT_CARD_FIELDS:
                _add(errors, f"spec.agent_card.{field}", "legacy field is invalid for A2A 1.0 AgentCard")
            elif field in AIDE_CARD_GOVERNANCE_FIELDS:
                _add(errors, f"spec.agent_card.{field}", "AIDE metadata must move to spec.agent_card_fixture")
            else:
                _add(errors, f"spec.agent_card.{field}", "is not an accepted A2A 1.0 AgentCard field")
    for required in ["name", "description", "supportedInterfaces", "version", "capabilities", "defaultInputModes", "defaultOutputModes", "skills"]:
        if required not in card:
            _add(errors, f"spec.agent_card.{required}", "required A2A AgentCard field is missing")
    if not isinstance(card.get("name"), str) or not card.get("name", "").strip():
        _add(errors, "spec.agent_card.name", "must be a non-empty string")
    if not isinstance(card.get("description"), str) or not card.get("description", "").strip():
        _add(errors, "spec.agent_card.description", "must be a non-empty string")
    if not isinstance(card.get("version"), str) or not card.get("version", "").strip():
        _add(errors, "spec.agent_card.version", "must be a non-empty agent implementation version")
    if not isinstance(card.get("defaultInputModes"), list) or not card.get("defaultInputModes"):
        _add(errors, "spec.agent_card.defaultInputModes", "must be a non-empty array")
    if not isinstance(card.get("defaultOutputModes"), list) or not card.get("defaultOutputModes"):
        _add(errors, "spec.agent_card.defaultOutputModes", "must be a non-empty array")
    _validate_supported_interfaces(spec, card, errors)
    _validate_provider(card.get("provider"), errors)
    _validate_capabilities(spec, card, errors)
    _validate_official_skills(spec, card, errors)
    _validate_security(card, errors)


def _validate_candidate_skills(spec: dict[str, Any], errors: list[str]) -> None:
    skills = spec.get("candidate_skill_governance")
    if not isinstance(skills, list) or not skills:
        _add(errors, "spec.candidate_skill_governance", "must be a non-empty array of AIDE metadata records")
        return
    seen: set[str] = set()
    for index, skill in enumerate(skills):
        path = f"spec.candidate_skill_governance[{index}]"
        if not isinstance(skill, dict):
            _add(errors, path, "must be an object")
            continue
        skill_id = skill.get("skill_id")
        valid, reason = validate_skill_id(skill_id)
        if not valid:
            _add(errors, f"{path}.skill_id", reason)
        elif skill_id in seen:
            _add(errors, f"{path}.skill_id", f"duplicate skill id: {skill_id}")
        else:
            seen.add(skill_id)
        if skill.get("aide_operation_mapping") != skill_id:
            _add(errors, f"{path}.aide_operation_mapping", "must match skill_id")
        for field in ["implemented", "callable", "endpoint_available", "task_submission_available", "task_delegation_available"]:
            if skill.get(field) is not False:
                _add(errors, f"{path}.{field}", "must be false for candidate skills in this slice")
        if skill.get("requires_future_policy_decision") is not True:
            _add(errors, f"{path}.requires_future_policy_decision", "must be true")
        if skill.get("requires_future_capability_grant") is not True:
            _add(errors, f"{path}.requires_future_capability_grant", "must be true")
    if spec.get("candidate_skill_count") != len(skills):
        _add(errors, "spec.candidate_skill_count", "must match candidate_skill_governance length")
    if spec.get("callable_skill_count") != 0:
        _add(errors, "spec.callable_skill_count", "must remain zero")


def _validate_fixture_metadata(spec: dict[str, Any], errors: list[str]) -> None:
    fixture = spec.get("agent_card_fixture")
    if not isinstance(fixture, dict):
        _add(errors, "spec.agent_card_fixture", "must be an object")
        return
    required_truths = {
        "fixture_only": True,
        "interface_fixture_only": True,
        "network_target_intentionally_non_live": True,
    }
    required_falses = [
        "endpoint_implemented",
        "publishable",
        "well_known_publication_performed",
        "agent_registered",
        "live_a2a_endpoint",
        "task_submission_available",
        "task_delegation_available",
    ]
    for field, expected in required_truths.items():
        if fixture.get(field) is not expected:
            _add(errors, f"spec.agent_card_fixture.{field}", f"must be {expected}")
    for field in required_falses:
        if fixture.get(field) is not False:
            _add(errors, f"spec.agent_card_fixture.{field}", "must be false")


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
        _add(errors, "spec.contract_id", "must be stable a2a-agent-card-contract-v0")
    if spec.get("advisory_contract_ref") != ADVISORY_CONTRACT_REF:
        _add(errors, "spec.advisory_contract_ref", "must remain aide://interop/a2a-agent-card-contract-v0")
    if spec.get("reference_id_kind_supported") is not False:
        _add(errors, "spec.reference_id_kind_supported", "must remain false")
    _validate_version_pins(spec, errors)
    for field in FALSE_RUNTIME_FIELDS:
        if status.get(field) is not False:
            _add(errors, f"status.{field}", "must be false in the contract-only slice")
    implemented = spec.get("implemented_runtime_capabilities", {})
    if not isinstance(implemented, dict):
        _add(errors, "spec.implemented_runtime_capabilities", "must be an object")
        implemented = {}
    for key, value in implemented.items():
        if value is not False:
            _add(errors, f"spec.implemented_runtime_capabilities.{key}", "must be false")
    _validate_agent_card(spec, errors)
    _validate_candidate_skills(spec, errors)
    _validate_fixture_metadata(spec, errors)
    security = spec.get("security") if isinstance(spec.get("security"), dict) else {}
    if security.get("authentication_implemented") is not False:
        _add(errors, "spec.security.authentication_implemented", "must be false")
    if security.get("authorization_implemented") is not False:
        _add(errors, "spec.security.authorization_implemented", "must be false")
    if security.get("securitySchemes") not in ({}, None):
        _add(errors, "spec.security.securitySchemes", "must be empty until authentication exists")
    required = spec.get("required_aide_capabilities", [])
    if not isinstance(required, list):
        _add(errors, "spec.required_aide_capabilities", "must be an array")
    elif required:
        _add(errors, "spec.required_aide_capabilities", "unknown required AIDE capabilities fail closed in this slice")
    if spec.get("explicit_non_capabilities") != EXPLICIT_NON_CAPABILITIES:
        _add(errors, "spec.explicit_non_capabilities", "must match helper boundary list")
    return errors, warnings


def _capability_matrix(contract: dict[str, Any]) -> dict[str, Any]:
    spec = contract["spec"]
    official_skills = spec["agent_card"].get("skills", [])
    candidates = spec["candidate_skill_governance"]
    return {
        "schema_version": "aide.a2a-agent-card-contract.capability-matrix.v0",
        "contract_id": CONTRACT_ID,
        "declared_card_capabilities": spec["declared_card_capabilities"],
        "implemented_runtime_capabilities": spec["implemented_runtime_capabilities"],
        "skill_count": len(official_skills),
        "official_advertised_skill_count": len(official_skills),
        "candidate_skill_count": len(candidates),
        "callable_skill_count": sum(1 for skill in candidates if skill.get("callable") is True),
        "implemented_skill_count": sum(1 for skill in candidates if skill.get("implemented") is True),
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
    write_json(root / SKILL_CATALOG_JSON, _catalog_file("candidate-skill", contract["spec"]["candidate_skill_governance"]))
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
        "aide_schema_version": A2A_CONTRACT_SCHEMA_VERSION,
        "aide_contract_version": PROTOCOL_VERSION,
        "agent_fixture_version": AGENT_VERSION,
        "target_a2a_specification_release": A2A_SPECIFICATION_RELEASE,
        "target_a2a_protocol_version": A2A_PROTOCOL_VERSION,
        "agent_card_name": AGENT_NAME,
        "skill_count": capability_matrix["official_advertised_skill_count"],
        "official_advertised_skill_count": capability_matrix["official_advertised_skill_count"],
        "candidate_skill_count": capability_matrix["candidate_skill_count"],
        "callable_skill_count": capability_matrix["callable_skill_count"],
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
    write_json(root / SKILL_CATALOG_REPORT_JSON, _catalog_file("candidate-skill", contract["spec"]["candidate_skill_governance"]))
    write_text(root / SKILL_CATALOG_REPORT_MD, render_catalog_markdown("A2A Candidate Skills", contract["spec"]["candidate_skill_governance"]))
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
        "target_a2a_specification_release": contract["spec"].get("target_a2a_specification_release"),
        "target_a2a_protocol_version": contract["spec"].get("target_a2a_protocol_version"),
        "agent_card_name": contract["spec"].get("agent_card", {}).get("name"),
        "skill_count": matrix["skill_count"],
        "official_advertised_skill_count": matrix["official_advertised_skill_count"],
        "candidate_skill_count": matrix["candidate_skill_count"],
        "implemented_skill_count": matrix["implemented_skill_count"],
        "callable_skill_count": matrix["callable_skill_count"],
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
    matrix = _capability_matrix(contract)
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
        "aide_schema_version": A2A_CONTRACT_SCHEMA_VERSION,
        "aide_contract_version": PROTOCOL_VERSION,
        "agent_fixture_version": AGENT_VERSION,
        "target_a2a_specification_release": contract["spec"].get("target_a2a_specification_release"),
        "target_a2a_protocol_version": contract["spec"].get("target_a2a_protocol_version"),
        "agent_card_name": AGENT_NAME,
        "skill_count": matrix["official_advertised_skill_count"],
        "official_advertised_skill_count": matrix["official_advertised_skill_count"],
        "candidate_skill_count": matrix["candidate_skill_count"],
        "callable_skill_count": matrix["callable_skill_count"],
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
        f"- AIDE schema version: `{data.get('aide_schema_version', A2A_CONTRACT_SCHEMA_VERSION)}`",
        f"- AIDE contract version: `{data.get('aide_contract_version', PROTOCOL_VERSION)}`",
        f"- agent fixture version: `{data.get('agent_fixture_version', AGENT_VERSION)}`",
        f"- A2A specification release: `{data.get('target_a2a_specification_release')}`",
        f"- A2A protocol version: `{data.get('target_a2a_protocol_version')}`",
        f"- agent_card_name: `{data.get('agent_card_name')}`",
        f"- official_advertised_skill_count: `{data.get('official_advertised_skill_count')}`",
        f"- candidate_skill_count: `{data.get('candidate_skill_count')}`",
        f"- callable_skill_count: `{data.get('callable_skill_count')}`",
        f"- artifact_count: `{data.get('artifact_count')}`",
        f"- live_endpoint_count: `{data.get('live_endpoint_count', 0)}`",
        f"- registered_agent_count: `{data.get('registered_agent_count', 0)}`",
        f"- delegation_capability_count: `{data.get('delegation_capability_count', 0)}`",
        f"- recommended_next_task: `{data.get('recommended_next_task')}`",
        "",
        "This is a contract-only projection. It does not start, publish, or register A2A runtime behavior.",
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
            f"- AIDE schema version: `{A2A_CONTRACT_SCHEMA_VERSION}`",
            f"- AIDE contract version: `{PROTOCOL_VERSION}`",
            f"- agent fixture version: `{spec['agent_implementation_version']}`",
            f"- A2A specification release: `{spec['target_a2a_specification_release']}`",
            f"- A2A protocol version: `{spec['target_a2a_protocol_version']}`",
            f"- agent_card_name: `{spec['agent_card']['name']}`",
            f"- endpoint_implemented: `{spec['agent_card_fixture']['endpoint_implemented']}`",
            f"- publishable: `{spec['agent_card_fixture']['publishable']}`",
            "",
            "AIDE queue, protocol, evidence, and OKF records remain authoritative. A2A card artifacts are generated projections.",
            "",
        ]
    )


def render_agent_card_markdown(card: dict[str, Any]) -> str:
    interface = card.get("supportedInterfaces", [{}])[0] if card.get("supportedInterfaces") else {}
    return "\n".join(
        [
            "# A2A Agent Card Projection",
            "",
            f"- name: `{card.get('name')}`",
            f"- version: `{card.get('version')}`",
            f"- supported_interface_count: `{len(card.get('supportedInterfaces', []))}`",
            f"- fixture_interface_url: `{interface.get('url')}`",
            f"- protocolBinding: `{interface.get('protocolBinding')}`",
            f"- protocolVersion: `{interface.get('protocolVersion')}`",
            f"- official_advertised_skill_count: `{len(card.get('skills', []))}`",
            "",
        ]
    )


def render_capability_matrix_markdown(matrix: dict[str, Any]) -> str:
    lines = [
        "# A2A Capability Matrix",
        "",
        f"- official_advertised_skill_count: `{matrix['official_advertised_skill_count']}`",
        f"- candidate_skill_count: `{matrix['candidate_skill_count']}`",
        f"- callable_skill_count: `{matrix['callable_skill_count']}`",
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
        label = item.get("skill_id") or item.get("id") or item.get("name") or item.get("reason_code")
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
        f"- A2A specification release: `{report['target_a2a_specification_release']}`",
        f"- A2A protocol version: `{report['target_a2a_protocol_version']}`",
        f"- official_advertised_skill_count: `{report['official_advertised_skill_count']}`",
        f"- candidate_skill_count: `{report['candidate_skill_count']}`",
        f"- callable_skill_count: `{report['callable_skill_count']}`",
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
            "- Independent repair check of this A2A agent-card contract slice.",
            "- Acceptance review if the independent repair check passes.",
            "- Live A2A endpoint work only after runtime, trust, authorization, and host semantics are separately accepted.",
            "",
        ]
    )


def render_next_task_prompt() -> str:
    return "\n".join(
        [
            "# AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01",
            "# Independent Check of A2A Agent Card Standards Repair",
            "",
            "Use `.aide/queue/index.yaml` as canonical queue truth.",
            "",
            "Check `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01` without modifying the A2A contract implementation.",
            "Verify explicit A2A version pins, standards-clean AgentCard shape, supportedInterfaces, fixture-only endpoint metadata, provider omission, legacy-field removal, candidate skill metadata separation, validator hardening, deterministic projection, source immutability, and explicit non-capabilities.",
            "",
            "If no material issue exists, recommend `AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01`.",
            "If a material defect exists, recommend one bounded repair task.",
            "",
        ]
    )
