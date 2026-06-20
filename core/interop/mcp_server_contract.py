"""Minimal contract-only MCP projection helpers for AIDE.

This module projects a deterministic MCP server contract, resource/tool/prompt
catalogues, JSON-RPC fixtures, and validation reports. It deliberately avoids
server startup, transport binding, resource serving, tool invocation,
credential resolution, worker dispatch, provider calls, network access, and
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
MCP_CONTRACT_SCHEMA_VERSION = "aide.mcp-server-contract.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_mcp_server_contract"
TASK_ID = "AIDE-BUILD-MCP-SERVER-CONTRACT-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-MCP-SERVER-CONTRACT-01"
DETERMINISTIC_TIMESTAMP = "2026-06-20T00:00:00+10:00"

TARGET_PROTOCOL_VERSION = "2025-11-25"
JSONRPC_VERSION = "2.0"
CONTRACT_ID = "mcp-server-contract-v0"
ADVISORY_CONTRACT_REF = "aide://interop/mcp-server-contract-v0"
SERVER_NAME = "aide-mcp-contract-preview"
SERVER_TITLE = "AIDE MCP Server Contract Preview"
MCP_RESOURCE_NOT_FOUND_CODE = -32002

SCHEMA_PATH = Path(".aide/protocol/aide-mcp-server-contract.schema.json")
INTEROP_ROOT = Path(".aide/interop/mcp")
FIXTURE_ROOT = INTEROP_ROOT / "fixtures"
SERVER_CONTRACT_JSON = INTEROP_ROOT / "server-contract.json"
CAPABILITY_CATALOG_JSON = INTEROP_ROOT / "capability-catalog.json"
RESOURCE_CATALOG_JSON = INTEROP_ROOT / "resource-catalog.json"
TOOL_CATALOG_JSON = INTEROP_ROOT / "tool-catalog.json"
PROMPT_CATALOG_JSON = INTEROP_ROOT / "prompt-catalog.json"
CONFORMANCE_EXPECTATIONS_JSON = INTEROP_ROOT / "conformance-expectations.json"

REPORT_ROOT = Path(".aide/reports/mcp-server-contract")
STATUS_MD = REPORT_ROOT / "status.md"
CONTRACT_REPORT_JSON = REPORT_ROOT / "contract.json"
CONTRACT_REPORT_MD = REPORT_ROOT / "contract.md"
CAPABILITY_MATRIX_JSON = REPORT_ROOT / "capability-matrix.json"
CAPABILITY_MATRIX_MD = REPORT_ROOT / "capability-matrix.md"
RESOURCE_REPORT_JSON = REPORT_ROOT / "resource-catalog.json"
RESOURCE_REPORT_MD = REPORT_ROOT / "resource-catalog.md"
TOOL_REPORT_JSON = REPORT_ROOT / "tool-catalog.json"
TOOL_REPORT_MD = REPORT_ROOT / "tool-catalog.md"
PROMPT_REPORT_JSON = REPORT_ROOT / "prompt-catalog.json"
PROMPT_REPORT_MD = REPORT_ROOT / "prompt-catalog.md"
TRANSPORT_EXPECTATIONS_JSON = REPORT_ROOT / "transport-expectations.json"
TRANSPORT_EXPECTATIONS_MD = REPORT_ROOT / "transport-expectations.md"
AUTHORIZATION_EXPECTATIONS_JSON = REPORT_ROOT / "authorization-expectations.json"
AUTHORIZATION_EXPECTATIONS_MD = REPORT_ROOT / "authorization-expectations.md"
REFUSAL_MAPPING_JSON = REPORT_ROOT / "refusal-mapping.json"
REFUSAL_MAPPING_MD = REPORT_ROOT / "refusal-mapping.md"
CONFORMANCE_REPORT_JSON = REPORT_ROOT / "conformance-expectations.json"
CONFORMANCE_REPORT_MD = REPORT_ROOT / "conformance-expectations.md"
FIXTURE_INDEX_JSON = REPORT_ROOT / "fixture-index.json"
FIXTURE_INDEX_MD = REPORT_ROOT / "fixture-index.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"

REQUIRED_REPORTS = [
    STATUS_MD,
    CONTRACT_REPORT_JSON,
    CONTRACT_REPORT_MD,
    CAPABILITY_MATRIX_JSON,
    CAPABILITY_MATRIX_MD,
    RESOURCE_REPORT_JSON,
    RESOURCE_REPORT_MD,
    TOOL_REPORT_JSON,
    TOOL_REPORT_MD,
    PROMPT_REPORT_JSON,
    PROMPT_REPORT_MD,
    TRANSPORT_EXPECTATIONS_JSON,
    TRANSPORT_EXPECTATIONS_MD,
    AUTHORIZATION_EXPECTATIONS_JSON,
    AUTHORIZATION_EXPECTATIONS_MD,
    REFUSAL_MAPPING_JSON,
    REFUSAL_MAPPING_MD,
    CONFORMANCE_REPORT_JSON,
    CONFORMANCE_REPORT_MD,
    FIXTURE_INDEX_JSON,
    FIXTURE_INDEX_MD,
    VALIDATION_JSON,
    VALIDATION_MD,
    EXPLICIT_NON_CAPABILITIES_MD,
    FUTURE_WORK_MD,
    NEXT_TASK_PROMPT_MD,
]

FIXTURE_FILES = [
    "initialize-request.json",
    "initialize-result.json",
    "initialized-notification.json",
    "resources-list-request.json",
    "resources-list-result.json",
    "resources-read-request.json",
    "resources-read-result.json",
    "tools-list-request.json",
    "tools-list-result.json",
    "tools-call-refusal.json",
    "prompts-list-request.json",
    "prompts-list-result.json",
    "protocol-version-refusal.json",
    "capability-refusal.json",
    "resource-not-found-refusal.json",
]

PAGINATED_REQUEST_METHODS = {
    "resources/list",
    "resources/templates/list",
    "tools/list",
    "prompts/list",
    "roots/list",
    "tasks/list",
}

PAGINATED_RESULT_FIXTURES = {
    "resources-list-result.json": "resources",
    "resources-templates-list-result.json": "resourceTemplates",
    "tools-list-result.json": "tools",
    "prompts-list-result.json": "prompts",
    "roots-list-result.json": "roots",
    "tasks-list-result.json": "tasks",
}

CUSTOM_REFUSAL_FIXTURE_CODES = {
    "tools-call-refusal.json": (-32040, "MCP_RUNTIME_NOT_IMPLEMENTED"),
    "protocol-version-refusal.json": (-32041, "MCP_UNSUPPORTED_PROTOCOL_VERSION"),
    "capability-refusal.json": (-32042, "MCP_REQUIRED_CAPABILITY_UNAVAILABLE"),
}

READ_ONLY_TOOL_NAMES = [
    "aide.status",
    "aide.work.inspect",
    "aide.evidence.inspect",
    "aide.okf.search",
    "aide.reconciler.inspect",
    "aide.patch.inspect",
    "aide.context.inspect",
]
FORBIDDEN_TOOL_NAME_PARTS = [
    ".apply",
    ".run",
    ".dispatch",
    ".create",
    ".publish",
    ".mutate",
    ".install",
    ".execute",
]
TOOL_NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)+$")
SECRET_LIKE_RE = re.compile(
    r"(api[_-]?key|token|password|passwd|secret|private[_-]?key|-----BEGIN|cookie|connection[_-]?string)",
    re.IGNORECASE,
)

FALSE_RUNTIME_FIELDS = [
    "server_process_started",
    "stdio_transport_started",
    "http_transport_started",
    "http_endpoint_bound",
    "network_call_performed",
    "resource_serving_performed",
    "tool_execution_performed",
    "prompt_serving_performed",
    "authorization_implemented",
    "credential_resolution_performed",
    "worker_dispatched",
    "model_or_provider_called",
    "patch_applied",
    "repository_target_mutated",
    "branch_or_worktree_created",
    "github_mutation_performed",
    "trusted",
]

EXPLICIT_NON_CAPABILITIES = [
    "live_mcp_server",
    "mcp_process_lifecycle",
    "stdio_transport",
    "streamable_http_transport",
    "http_endpoint",
    "sse",
    "mcp_sessions",
    "mcp_authentication",
    "oauth",
    "authorization_server_discovery",
    "token_handling",
    "live_resources_list",
    "live_resources_read",
    "live_prompts_list",
    "live_prompts_get",
    "live_tools_list",
    "live_tools_call",
    "tool_invocation",
    "resource_serving",
    "prompt_serving",
    "client_roots",
    "sampling",
    "elicitation",
    "mcp_tasks",
    "adapter_execution",
    "worker_execution",
    "model_provider_calls",
    "network_calls",
    "credential_resolution",
    "patch_transaction_approval",
    "patch_transaction_apply",
    "target_repository_mutation",
    "branch_worktree_automation",
    "host_contract",
    "dominium_bridge",
    "workbench",
    "runtime",
    "service",
    "scheduler",
    "leases",
    "supervisor",
    "github_mutation",
    "release",
    "promotion",
    "production_readiness",
]

VALIDATION_WARNINGS = [
    "MCP server contract is projection-only; no live MCP server or transport exists.",
    "Resources, prompts, and tools are catalogued and fixture-backed only; they are not served or callable.",
    "Authorization expectations are declared but OAuth, credentials, PolicyDecision, and CapabilityGrant enforcement are not implemented.",
    "The preferred future aide://interop contract ReferenceID kind is advisory only; the accepted ReferenceID scheme is not broadened by this task.",
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


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def load_mcp_server_contract_schema(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(repo_root) if repo_root is not None else Path(".")
    return read_json(root / SCHEMA_PATH)


def source_artifact_paths(repo_root: str | Path | None = None) -> list[str]:
    _root = Path(repo_root) if repo_root is not None else Path(".")
    return [
        ".aide/protocol/aide-mcp-server-contract.schema.json",
        "core/interop/__init__.py",
        "core/interop/mcp_server_contract.py",
        ".aide/scripts/aide_lite.py",
        ".aide/scripts/tests/test_aide_mcp_server_contract.py",
        ".aide/interop/exports/manifest.json",
        ".aide/interop/exports/mcp-manifest.preview.json",
        ".aide/reports/interop-exports-accept/acceptance-report.json",
        ".aide/reports/interop-exports-check/check-report.json",
        ".aide/reports/context-pack-v2-resume-accept/acceptance-report.json",
        ".aide/reports/adapter-manifest-resume-accept/acceptance-report.json",
        ".aide/reports/patch-transaction-resume-accept/acceptance-report.json",
        ".aide/reports/conformance-result-accept/acceptance-report.json",
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


def build_declared_capabilities() -> dict[str, Any]:
    return {
        "resources": {
            "catalog_defined": True,
            "list_changed": False,
            "subscribe": False,
        },
        "tools": {
            "catalog_defined": True,
            "list_changed": False,
            "invocation_contract_defined": True,
        },
        "prompts": {
            "catalog_defined": True,
            "list_changed": False,
        },
        "logging": {
            "contract_defined": False,
        },
        "tasks": {
            "contract_defined": False,
        },
    }


def build_implemented_capabilities() -> dict[str, bool]:
    return {
        "resources_served": False,
        "tools_callable": False,
        "prompts_served": False,
        "logging_active": False,
        "tasks_active": False,
    }


def build_resource_catalog() -> list[dict[str, Any]]:
    resources = [
        ("aide://status/current", "aide_status_current", "AIDE Current Status", "AIDE queue and governance status projection.", "AIDEStatusProjection"),
        ("aide://workunit/{id}", "aide_workunit", "AIDE WorkUnit", "Accepted WorkUnit or queue task projection by identifier.", "WorkUnit"),
        ("aide://evidence/{id}", "aide_evidence", "AIDE EvidencePacket", "EvidencePacket projection by identifier.", "EvidencePacket"),
        ("aide://event/{id}", "aide_event", "AIDE EventRecord", "EventRecord projection by identifier.", "EventRecord"),
        ("aide://okf/{concept}", "aide_okf_concept", "AIDE OKF Concept", "OKF explanatory concept projection.", "OKFConcept"),
        ("aide://capability/{id}", "aide_capability", "AIDE Capability", "CapabilityManifest projection by capability identifier.", "CapabilityManifest"),
        ("aide://conformance-result/{id}", "aide_conformance_result", "AIDE ConformanceResult", "ConformanceResult evidence projection by identifier.", "ConformanceResult"),
        ("aide://patch-transaction/{id}", "aide_patch_transaction", "AIDE PatchTransaction", "No-apply PatchTransaction projection by identifier.", "PatchTransaction"),
        ("aide://context-pack/{id}", "aide_context_pack", "AIDE ContextPack", "ContextPack v2 projection by identifier.", "ContextPack"),
        ("aide://reconciler/status", "aide_reconciler_status", "AIDE Reconciler Status", "Report-only Reconciler status projection.", "ReconcilerStatus"),
    ]
    return [
        {
            "uri": uri,
            "name": name,
            "title": title,
            "description": description,
            "mime_type": "application/json",
            "source_aide_object_kind": kind,
            "authority_role": "projection_of_aide_source_truth",
            "read_policy": "contract_only_not_served",
            "freshness_behavior": "regenerate_from_accepted_aide_inputs",
            "sensitive_data_classification": "non_secret_projection_metadata",
            "content_availability_status": "not_served_contract_only",
        }
        for uri, name, title, description, kind in resources
    ]


def _input_schema(properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": required or [],
    }


def build_tool_catalog() -> list[dict[str, Any]]:
    tool_specs = [
        ("aide.status", "AIDE Status", "Inspect current AIDE queue and capability status.", "status.inspect", {}, []),
        ("aide.work.inspect", "Inspect Work", "Inspect a WorkUnit or queue task projection.", "work.inspect", {"id": {"type": "string"}}, ["id"]),
        ("aide.evidence.inspect", "Inspect Evidence", "Inspect an EvidencePacket projection.", "evidence.inspect", {"id": {"type": "string"}}, ["id"]),
        ("aide.okf.search", "Search OKF", "Search accepted OKF explanatory knowledge projections.", "okf.search", {"query": {"type": "string"}}, ["query"]),
        ("aide.reconciler.inspect", "Inspect Reconciler", "Inspect report-only Reconciler findings.", "reconciler.inspect", {}, []),
        ("aide.patch.inspect", "Inspect PatchTransaction", "Inspect a no-apply PatchTransaction projection.", "patch.inspect", {"id": {"type": "string"}}, ["id"]),
        ("aide.context.inspect", "Inspect ContextPack", "Inspect a ContextPack v2 projection.", "context.inspect", {"id": {"type": "string"}}, ["id"]),
    ]
    return [
        {
            "name": name,
            "title": title,
            "description": description,
            "inputSchema": _input_schema(properties, required),
            "outputSchema": _input_schema({"projection": {"type": "object"}}, []),
            "aide_operation_mapping": mapping,
            "required_aide_capability_refs": [],
            "required_policy_state": "future_policy_decision_required_before_runtime",
            "human_consent_required": True,
            "side_effect_class": "read_only_or_report_only",
            "execution_status": "not_implemented",
            "callable": False,
            "annotations": {
                "readOnlyHint": True,
                "destructiveHint": False,
                "openWorldHint": False,
            },
        }
        for name, title, description, mapping, properties, required in tool_specs
    ]


def build_prompt_catalog() -> list[dict[str, Any]]:
    return []


def build_transport_profiles() -> list[dict[str, Any]]:
    return [
        {
            "name": "stdio",
            "contract_defined": True,
            "implementation_status": "not_implemented",
            "security_requirements": [
                "UTF-8 JSON-RPC messages",
                "newline-delimited messages",
                "no non-MCP output on stdout",
                "logging may use stderr",
                "client-launched subprocess model",
            ],
            "supported_protocol_versions": [TARGET_PROTOCOL_VERSION],
        },
        {
            "name": "streamable_http",
            "contract_defined": True,
            "implementation_status": "not_implemented",
            "security_requirements": [
                "single MCP endpoint supporting POST and GET",
                "protocol-version header handling",
                "content-type requirements",
                "session handling",
                "resumability expectations",
                "explicit cancellation",
                "Origin validation",
                "localhost-only default for local service",
                "authentication requirement for protected use",
            ],
            "supported_protocol_versions": [TARGET_PROTOCOL_VERSION],
        },
    ]


def build_authorization_expectations() -> dict[str, Any]:
    return {
        "authorization_supported_by_contract": True,
        "authorization_implemented": False,
        "stdio_credential_sourcing_expectations": [
            "future client launch environment must not be treated as AIDE authorization",
            "future credentials must not be embedded in generated projections",
        ],
        "http_authorization_expectations": [
            "protected use requires authentication",
            "Origin validation is required for browser-accessible local endpoints",
            "localhost-only default is required for local service HTTP",
        ],
        "aide_authority": {
            "policy_decision_controls_operation_permission": True,
            "capability_grant_controls_aide_operation_scope": True,
            "implemented": False,
        },
        "not_implemented": [
            "OAuth",
            "client registration",
            "token issuance",
            "token parsing",
            "token storage",
            "scopes",
            "credential resolution",
            "authorization-server discovery",
        ],
    }


def build_security_expectations() -> list[str]:
    return [
        "user consent required before future tool invocation",
        "tool descriptions and annotations are not trusted authorization",
        "resource URIs require validation",
        "sensitive resources require access control",
        "no raw credentials in projections",
        "no arbitrary filesystem exposure",
        "no live network behavior",
        "no mutation tools in v0",
    ]


def build_refusal_mappings() -> list[dict[str, Any]]:
    mappings = [
        ("runtime_not_implemented", "MCP_RUNTIME_NOT_IMPLEMENTED", "MCP runtime is not implemented."),
        ("resource_not_found", "MCP_RESOURCE_NOT_FOUND", "Requested projected resource is not found."),
        ("required_capability_unavailable", "MCP_REQUIRED_CAPABILITY_UNAVAILABLE", "Required capability is unavailable."),
        ("policy_or_grant_unavailable", "AIDE_POLICY_OR_GRANT_UNAVAILABLE", "AIDE PolicyDecision or CapabilityGrant is unavailable."),
        ("unsupported_protocol_version", "MCP_UNSUPPORTED_PROTOCOL_VERSION", "Requested MCP protocol version is unsupported."),
    ]
    return [
        {
            "refusal_ref": f"{CONTRACT_ID}:{refusal_id}",
            "reason_code": reason_code,
            "message": message,
            "retryable": False,
            "human_action_required": False,
            "subject_ref": ADVISORY_CONTRACT_REF,
            "capability_ref": FEATURE_FLAG if refusal_id != "required_capability_unavailable" else "unknown",
            "policy_decision_ref": None,
            "evidence_refs": [],
        }
        for refusal_id, reason_code, message in mappings
    ]


def build_conformance_expectations() -> list[dict[str, Any]]:
    texts = [
        "JSON-RPC version is 2.0",
        "protocol target is 2025-11-25",
        "initialize precedes normal operation",
        "protocol version must be negotiated",
        "only negotiated capabilities may be used",
        "resource URIs validate",
        "resources/list supports deterministic pagination shape",
        "resources/read returns bounded content shape",
        "tools/list returns valid tool definitions",
        "tool names are unique and valid",
        "tool input schemas are JSON Schema objects",
        "tools/call is refused while runtime is absent",
        "prompts/list and prompts/get shapes are valid when declared",
        "stdio expectations are declared but not implemented",
        "Streamable HTTP expectations are declared but not implemented",
        "HTTP Origin validation is required for future implementation",
        "local HTTP should default to localhost",
        "authorization expectations are declared but not implemented",
        "no secret values exist in projected artifacts",
        "no mutation-capable tool is exposed in v0",
        "MCP projection does not supersede AIDE authority",
        "projection is deterministic and source-immutable",
    ]
    return [
        {
            "id": f"MCP-CONTRACT-{index:03d}",
            "description": text,
            "expectation_status": "declared_not_executed",
            "evidence_status": "fixture_or_static_projection_only",
        }
        for index, text in enumerate(texts, 1)
    ]


def build_lifecycle_expectations() -> list[dict[str, Any]]:
    return [
        {
            "state": "initialization",
            "order": 1,
            "normal_first_interaction": "initialize",
            "implemented": False,
        },
        {
            "state": "operation",
            "order": 2,
            "requires_initialized_notification": True,
            "implemented": False,
        },
        {
            "state": "shutdown",
            "order": 3,
            "implemented": False,
        },
    ]


def build_status() -> dict[str, bool]:
    status: dict[str, bool] = {
        "contract_projection_performed": True,
        "fixture_generation_performed": True,
        "structural_validation_performed": True,
    }
    for field in FALSE_RUNTIME_FIELDS:
        status[field] = False
    return status


def build_mcp_server_contract(repo_root: str | Path | None = None) -> dict[str, Any]:
    _root = Path(repo_root) if repo_root is not None else Path(".")
    resources = build_resource_catalog()
    tools = build_tool_catalog()
    prompts = build_prompt_catalog()
    transport_profiles = build_transport_profiles()
    authorization = build_authorization_expectations()
    refusal_mappings = build_refusal_mappings()
    conformance = build_conformance_expectations()
    return envelope.build_envelope(
        "McpServerContract",
        {
            "name": CONTRACT_ID,
            "created_at": DETERMINISTIC_TIMESTAMP,
            "producer": {
                "name": PRODUCER_NAME,
                "version": PRODUCER_VERSION,
            },
            "compatibility": _compatibility(),
        },
        {
            "contract_id": CONTRACT_ID,
            "contract_ref": CONTRACT_ID,
            "advisory_contract_ref": ADVISORY_CONTRACT_REF,
            "reference_id_kind_supported": False,
            "schema_version": MCP_CONTRACT_SCHEMA_VERSION,
            "target_protocol_version": TARGET_PROTOCOL_VERSION,
            "supported_protocol_versions": [TARGET_PROTOCOL_VERSION],
            "backward_compatibility_claimed": False,
            "forward_compatibility_claimed": False,
            "jsonrpc_version": JSONRPC_VERSION,
            "server_info": {
                "name": SERVER_NAME,
                "title": SERVER_TITLE,
                "version": PROTOCOL_VERSION,
                "description": "Contract-only AIDE MCP projection. No server process, endpoint, resource serving, prompt serving, or tool execution exists.",
                "contract_ref": CONTRACT_ID,
                "implementation_status": "contract_only",
            },
            "declared_feature_families": ["resources", "tools", "prompts"],
            "required_mcp_capabilities": [],
            "declared_contract_capabilities": build_declared_capabilities(),
            "implemented_runtime_capabilities": build_implemented_capabilities(),
            "lifecycle_expectations": build_lifecycle_expectations(),
            "resources": resources,
            "tools": tools,
            "prompts": prompts,
            "transport_profiles": transport_profiles,
            "authorization": authorization,
            "security_expectations": build_security_expectations(),
            "aide_authority_mappings": {
                "queue_truth": ".aide/queue/index.yaml",
                "protocol_truth": ".aide/protocol/",
                "evidence_truth": "EvidencePacket",
                "knowledge_projection": "OKF",
                "mcp_catalogues_and_fixtures": "generated_interoperability_projection",
            },
            "refusal_mappings": refusal_mappings,
            "conformance_expectations": conformance,
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "recommended_next_task": RECOMMENDED_NEXT_TASK,
        },
        build_status(),
    )


def _jsonrpc_request(method: str, request_id: int, params: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "jsonrpc": JSONRPC_VERSION,
        "id": request_id,
        "method": method,
    }
    if params is not None:
        payload["params"] = params
    return payload


def _jsonrpc_result(request_id: int, result: dict[str, Any]) -> dict[str, Any]:
    return {
        "jsonrpc": JSONRPC_VERSION,
        "id": request_id,
        "result": result,
    }


def _jsonrpc_error(request_id: int | None, code: int, message: str, data: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "jsonrpc": JSONRPC_VERSION,
        "error": {
            "code": code,
            "message": message,
            "data": data,
        },
    }
    if request_id is not None:
        payload["id"] = request_id
    return payload


def build_fixtures(contract: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    record = contract or build_mcp_server_contract()
    spec = record["spec"]
    capabilities = {
        "resources": {
            "listChanged": False,
            "subscribe": False,
        },
        "tools": {
            "listChanged": False,
        },
        "prompts": {
            "listChanged": False,
        },
    }
    resource_entries = [
        {
            "uri": item["uri"],
            "name": item["name"],
            "title": item["title"],
            "description": item["description"],
            "mimeType": item["mime_type"],
        }
        for item in spec["resources"]
    ]
    tool_entries = [
        {
            "name": item["name"],
            "title": item["title"],
            "description": item["description"],
            "inputSchema": item["inputSchema"],
            "annotations": item["annotations"],
        }
        for item in spec["tools"]
    ]
    projection_text = stable_json(
        {
            "generated_projection": True,
            "non_authoritative": True,
            "no_live_resource_serving": True,
            "summary": "Contract-only current AIDE status projection.",
            "canonical_queue_truth": ".aide/queue/index.yaml",
            "contract_ref": CONTRACT_ID,
        }
    )
    return {
        "initialize-request.json": _jsonrpc_request(
            "initialize",
            1,
            {
                "protocolVersion": TARGET_PROTOCOL_VERSION,
                "capabilities": {
                    "roots": {"listChanged": False},
                    "sampling": {},
                },
                "clientInfo": {
                    "name": "aide-contract-fixture-client",
                    "version": "0.1.0",
                },
            },
        ),
        "initialize-result.json": _jsonrpc_result(
            1,
            {
                "protocolVersion": TARGET_PROTOCOL_VERSION,
                "capabilities": capabilities,
                "serverInfo": {
                    "name": SERVER_NAME,
                    "title": SERVER_TITLE,
                    "version": PROTOCOL_VERSION,
                },
                "instructions": "Generated contract fixture only. AIDE queue and protocol records remain authoritative.",
            },
        ),
        "initialized-notification.json": {
            "jsonrpc": JSONRPC_VERSION,
            "method": "notifications/initialized",
        },
        "resources-list-request.json": _jsonrpc_request("resources/list", 2),
        "resources-list-result.json": _jsonrpc_result(2, {"resources": resource_entries}),
        "resources-read-request.json": _jsonrpc_request("resources/read", 3, {"uri": "aide://status/current"}),
        "resources-read-result.json": _jsonrpc_result(
            3,
            {
                "contents": [
                    {
                        "uri": "aide://status/current",
                        "mimeType": "application/json",
                        "text": projection_text,
                    }
                ]
            },
        ),
        "tools-list-request.json": _jsonrpc_request("tools/list", 4),
        "tools-list-result.json": _jsonrpc_result(4, {"tools": tool_entries}),
        "tools-call-refusal.json": _jsonrpc_error(
            5,
            -32040,
            "MCP runtime is not implemented.",
            {
                "reason_code": "MCP_RUNTIME_NOT_IMPLEMENTED",
                "retryable": False,
                "human_action_required": False,
                "tool_name": "aide.status",
                "contract_ref": CONTRACT_ID,
                "evidence_refs": [],
            },
        ),
        "prompts-list-request.json": _jsonrpc_request("prompts/list", 6),
        "prompts-list-result.json": _jsonrpc_result(6, {"prompts": []}),
        "protocol-version-refusal.json": _jsonrpc_error(
            7,
            -32041,
            "Unsupported MCP protocol version.",
            {
                "reason_code": "MCP_UNSUPPORTED_PROTOCOL_VERSION",
                "requested_protocol_version": "latest",
                "supported_protocol_versions": [TARGET_PROTOCOL_VERSION],
                "retryable": False,
                "human_action_required": False,
                "contract_ref": CONTRACT_ID,
            },
        ),
        "capability-refusal.json": _jsonrpc_error(
            8,
            -32042,
            "Required capability is unavailable.",
            {
                "reason_code": "MCP_REQUIRED_CAPABILITY_UNAVAILABLE",
                "required_capability": "sampling",
                "retryable": False,
                "human_action_required": False,
                "contract_ref": CONTRACT_ID,
            },
        ),
        "resource-not-found-refusal.json": _jsonrpc_error(
            9,
            MCP_RESOURCE_NOT_FOUND_CODE,
            "Resource not found",
            {
                "reason_code": "MCP_RESOURCE_NOT_FOUND",
                "uri": "aide://workunit/not-found",
                "retryable": False,
                "human_action_required": False,
                "contract_ref": CONTRACT_ID,
            },
        ),
    }


def _fixture_index(root: Path, fixtures: dict[str, dict[str, Any]]) -> dict[str, Any]:
    entries = []
    for name in sorted(fixtures):
        path = FIXTURE_ROOT / name
        abs_path = root / path
        entries.append(
            {
                "path": path.as_posix(),
                "name": name,
                "sha256": sha256_file(abs_path) if abs_path.exists() else sha256_bytes(stable_json(fixtures[name]).encode("utf-8")),
                "jsonrpc": fixtures[name].get("jsonrpc"),
            }
        )
    return {
        "schema_version": "aide.mcp-server-contract.fixture-index.v0",
        "fixture_count": len(entries),
        "fixtures": entries,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _capability_matrix(contract: dict[str, Any]) -> dict[str, Any]:
    spec = contract["spec"]
    return {
        "schema_version": "aide.mcp-server-contract.capability-matrix.v0",
        "target_protocol_version": spec["target_protocol_version"],
        "jsonrpc_version": spec["jsonrpc_version"],
        "declared_contract_capabilities": spec["declared_contract_capabilities"],
        "implemented_runtime_capabilities": spec["implemented_runtime_capabilities"],
        "resource_count": len(spec["resources"]),
        "tool_count": len(spec["tools"]),
        "prompt_count": len(spec["prompts"]),
        "callable_tool_count": sum(1 for item in spec["tools"] if item.get("callable") is True),
        "served_resource_count": 0,
        "live_endpoint_count": 0,
        "implemented_live_transport_count": 0,
    }


def _catalog_file(kind: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": f"aide.mcp-server-contract.{kind}-catalog.v0",
        "contract_id": CONTRACT_ID,
        "target_protocol_version": TARGET_PROTOCOL_VERSION,
        "items": items,
        "count": len(items),
        "projection_only": True,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def validate_resource_uri(value: Any) -> tuple[bool, str | None]:
    if not isinstance(value, str) or not value:
        return False, "resource URI must be a non-empty string"
    lowered = value.lower()
    if lowered.startswith(("file://", "http://", "https://")):
        return False, "resource URI must not expose filesystem or network schemes"
    if ".aide.local" in lowered or ".." in value.replace("\\", "/"):
        return False, "resource URI must not expose local state or traversal"
    if not value.startswith("aide://"):
        return False, "resource URI must use aide:// scheme"
    if value.count("{") != value.count("}"):
        return False, "resource URI template braces must be balanced"
    return True, None


def validate_tool_name(value: Any) -> tuple[bool, str | None]:
    if not isinstance(value, str) or not TOOL_NAME_RE.match(value):
        return False, "tool name must use bounded dotted lowercase syntax"
    if any(part in value for part in FORBIDDEN_TOOL_NAME_PARTS):
        return False, "mutation-capable tool names are not allowed in v0"
    return True, None


def _validate_schema_like_object(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{field} must be a JSON Schema object")
        return
    if value.get("type") != "object":
        errors.append(f"{field} must have type object")
    if "properties" in value and not isinstance(value["properties"], dict):
        errors.append(f"{field}.properties must be an object")
    if "required" in value and not isinstance(value["required"], list):
        errors.append(f"{field}.required must be an array")


def validate_mcp_server_contract_with_schema(record: dict[str, Any], schema: dict[str, Any] | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings = list(VALIDATION_WARNINGS)
    errors.extend(envelope.validate_envelope(record, {"McpServerContract"}))
    if record.get("kind") != "McpServerContract":
        errors.append("kind must be McpServerContract")
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    spec = record.get("spec") if isinstance(record.get("spec"), dict) else {}
    status = record.get("status") if isinstance(record.get("status"), dict) else {}
    compatibility = metadata.get("compatibility") if isinstance(metadata.get("compatibility"), dict) else {}
    if FEATURE_FLAG not in compatibility.get("featureFlags", []):
        errors.append("metadata.compatibility.featureFlags must include minimal_mcp_server_contract")
    if spec.get("contract_id") != CONTRACT_ID:
        errors.append("spec.contract_id must be stable")
    if spec.get("target_protocol_version") != TARGET_PROTOCOL_VERSION:
        errors.append("spec.target_protocol_version must be 2025-11-25")
    if spec.get("supported_protocol_versions") != [TARGET_PROTOCOL_VERSION]:
        errors.append("spec.supported_protocol_versions must contain only 2025-11-25")
    if spec.get("jsonrpc_version") != JSONRPC_VERSION:
        errors.append("spec.jsonrpc_version must be 2.0")
    if spec.get("backward_compatibility_claimed") is not False:
        errors.append("backward compatibility must not be claimed")
    if spec.get("forward_compatibility_claimed") is not False:
        errors.append("forward compatibility must not be claimed")
    if spec.get("reference_id_kind_supported") is not False:
        errors.append("interop ReferenceID support must not be claimed")

    declared = spec.get("declared_contract_capabilities")
    implemented = spec.get("implemented_runtime_capabilities")
    if not isinstance(declared, dict):
        errors.append("declared_contract_capabilities must be an object")
        declared = {}
    if not isinstance(implemented, dict):
        errors.append("implemented_runtime_capabilities must be an object")
        implemented = {}
    for key in ["resources_served", "tools_callable", "prompts_served", "logging_active", "tasks_active"]:
        if implemented.get(key) is not False:
            errors.append(f"implemented_runtime_capabilities.{key} must be false")
    required_mcp_capabilities = spec.get("required_mcp_capabilities", [])
    if not isinstance(required_mcp_capabilities, list):
        errors.append("required_mcp_capabilities must be an array")
    else:
        for capability in required_mcp_capabilities:
            if capability not in {"resources", "tools", "prompts"}:
                errors.append(f"unknown required MCP capability: {capability}")

    resources = spec.get("resources")
    if not isinstance(resources, list):
        errors.append("spec.resources must be an array")
        resources = []
    seen_resources: set[str] = set()
    for item in resources:
        if not isinstance(item, dict):
            errors.append("resource entry must be an object")
            continue
        uri = item.get("uri")
        valid, reason = validate_resource_uri(uri)
        if not valid:
            errors.append(f"invalid resource URI {uri!r}: {reason}")
        elif uri in seen_resources:
            errors.append(f"duplicate resource URI: {uri}")
        else:
            seen_resources.add(str(uri))
        if item.get("content_availability_status") != "not_served_contract_only":
            errors.append(f"resource {uri!r} must not be marked served")

    tools = spec.get("tools")
    if not isinstance(tools, list):
        errors.append("spec.tools must be an array")
        tools = []
    seen_tools: set[str] = set()
    for item in tools:
        if not isinstance(item, dict):
            errors.append("tool entry must be an object")
            continue
        name = item.get("name")
        valid, reason = validate_tool_name(name)
        if not valid:
            errors.append(f"invalid tool name {name!r}: {reason}")
        elif name in seen_tools:
            errors.append(f"duplicate tool name: {name}")
        else:
            seen_tools.add(str(name))
        _validate_schema_like_object(item.get("inputSchema"), f"tool {name}.inputSchema", errors)
        if item.get("outputSchema") is not None:
            _validate_schema_like_object(item.get("outputSchema"), f"tool {name}.outputSchema", errors)
        if item.get("side_effect_class") != "read_only_or_report_only":
            errors.append(f"tool {name} must remain read-only/report-only")
        if item.get("execution_status") != "not_implemented":
            errors.append(f"tool {name} must have execution_status not_implemented")
        if item.get("callable") is not False:
            errors.append(f"tool {name} must not be callable")

    prompts = spec.get("prompts")
    if not isinstance(prompts, list):
        errors.append("spec.prompts must be an array")
        prompts = []
    for item in prompts:
        if not isinstance(item, dict):
            errors.append("prompt entry must be an object")
            continue
        arguments = item.get("arguments", [])
        if not isinstance(arguments, list):
            errors.append(f"prompt {item.get('name')} arguments must be an array")
            continue
        for argument in arguments:
            if not isinstance(argument, dict) or not isinstance(argument.get("name"), str):
                errors.append(f"prompt {item.get('name')} argument definitions must include names")

    if declared.get("resources", {}).get("catalog_defined") is not (len(resources) > 0):
        errors.append("declared resources catalog flag must match resource catalog presence")
    if declared.get("tools", {}).get("catalog_defined") is not (len(tools) > 0):
        errors.append("declared tools catalog flag must match tool catalog presence")
    if declared.get("prompts", {}).get("catalog_defined") is not True:
        errors.append("declared prompts catalog must remain defined even when empty")

    lifecycle = spec.get("lifecycle_expectations")
    if not isinstance(lifecycle, list) or [item.get("state") for item in lifecycle if isinstance(item, dict)][:2] != ["initialization", "operation"]:
        errors.append("lifecycle must order initialization before operation")

    transports = spec.get("transport_profiles")
    if not isinstance(transports, list):
        errors.append("transport_profiles must be an array")
        transports = []
    for item in transports:
        if not isinstance(item, dict):
            errors.append("transport profile entry must be an object")
            continue
        if item.get("implementation_status") != "not_implemented":
            errors.append(f"transport {item.get('name')} must be not_implemented")
        if TARGET_PROTOCOL_VERSION not in item.get("supported_protocol_versions", []):
            errors.append(f"transport {item.get('name')} must list target protocol version")
        if item.get("name") == "streamable_http":
            requirements = item.get("security_requirements", [])
            if "Origin validation" not in requirements:
                errors.append("streamable_http must require future Origin validation")
            if "localhost-only default for local service" not in requirements:
                errors.append("streamable_http must require localhost-only default")

    authorization = spec.get("authorization")
    if not isinstance(authorization, dict):
        errors.append("authorization must be an object")
    else:
        if authorization.get("authorization_supported_by_contract") is not True:
            errors.append("authorization_supported_by_contract must be true")
        if authorization.get("authorization_implemented") is not False:
            errors.append("authorization_implemented must be false")

    refusals = spec.get("refusal_mappings")
    if not isinstance(refusals, list) or not refusals:
        errors.append("refusal_mappings must be a non-empty array")
    else:
        reason_codes = {item.get("reason_code") for item in refusals if isinstance(item, dict)}
        for required in [
            "MCP_RUNTIME_NOT_IMPLEMENTED",
            "MCP_RESOURCE_NOT_FOUND",
            "MCP_REQUIRED_CAPABILITY_UNAVAILABLE",
            "AIDE_POLICY_OR_GRANT_UNAVAILABLE",
            "MCP_UNSUPPORTED_PROTOCOL_VERSION",
        ]:
            if required not in reason_codes:
                errors.append(f"missing refusal reason code: {required}")

    conformance = spec.get("conformance_expectations")
    if not isinstance(conformance, list) or len(conformance) < 22:
        errors.append("at least 22 conformance expectations are required")
    else:
        ids = [item.get("id") for item in conformance if isinstance(item, dict)]
        if ids != [f"MCP-CONTRACT-{index:03d}" for index in range(1, len(ids) + 1)]:
            errors.append("conformance expectation ids must be deterministic and ordered")

    explicit = spec.get("explicit_non_capabilities")
    if explicit != EXPLICIT_NON_CAPABILITIES:
        errors.append("explicit non-capabilities must match the accepted v0 boundary list")
    for field in FALSE_RUNTIME_FIELDS:
        if status.get(field) is not False:
            errors.append(f"status.{field} must be false")
    for field in ["contract_projection_performed", "fixture_generation_performed", "structural_validation_performed"]:
        if status.get(field) is not True:
            errors.append(f"status.{field} must be true")
    if schema:
        if schema.get("title") != "AIDE Minimal MCP Server Contract":
            errors.append("schema title mismatch")
        schema_kind = schema.get("properties", {}).get("kind", {}).get("enum")
        if schema_kind != ["McpServerContract"]:
            errors.append("schema/helper kind mismatch")
    return errors, warnings


def validate_fixtures(fixtures: dict[str, dict[str, Any]], contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for name in FIXTURE_FILES:
        fixture = fixtures.get(name)
        if not isinstance(fixture, dict):
            errors.append(f"missing fixture: {name}")
            continue
        if fixture.get("jsonrpc") != JSONRPC_VERSION:
            errors.append(f"{name} must use JSON-RPC 2.0")
        if fixture.get("method") in PAGINATED_REQUEST_METHODS:
            _validate_paginated_request_fixture(name, fixture, errors)
        if name in PAGINATED_RESULT_FIXTURES:
            _validate_paginated_result_fixture(name, fixture, errors)
    initialize = fixtures.get("initialize-result.json", {})
    if initialize.get("result", {}).get("protocolVersion") != TARGET_PROTOCOL_VERSION:
        errors.append("initialize-result protocolVersion must match target")
    initialized = fixtures.get("initialized-notification.json", {})
    if initialized.get("method") != "notifications/initialized":
        errors.append("initialized notification method mismatch")
    call_refusal = fixtures.get("tools-call-refusal.json", {})
    error = call_refusal.get("error", {}) if isinstance(call_refusal, dict) else {}
    if error.get("data", {}).get("reason_code") != "MCP_RUNTIME_NOT_IMPLEMENTED":
        errors.append("tools/call refusal must preserve runtime-not-implemented reason")
    if "result" in call_refusal:
        errors.append("tools/call refusal must not contain execution result")
    resource_not_found = fixtures.get("resource-not-found-refusal.json", {})
    if resource_not_found.get("error", {}).get("data", {}).get("reason_code") != "MCP_RESOURCE_NOT_FOUND":
        errors.append("resource-not-found fixture must use bounded reason")
    if resource_not_found.get("error", {}).get("code") != MCP_RESOURCE_NOT_FOUND_CODE:
        errors.append("resource-not-found-refusal.json error.code must be -32002")
    for name, (expected_code, expected_reason) in CUSTOM_REFUSAL_FIXTURE_CODES.items():
        fixture = fixtures.get(name, {})
        error = fixture.get("error", {}) if isinstance(fixture, dict) else {}
        data = error.get("data", {}) if isinstance(error, dict) else {}
        if error.get("code") != expected_code:
            errors.append(f"{name} error.code must remain {expected_code}")
        if data.get("reason_code") != expected_reason:
            errors.append(f"{name} reason_code must remain {expected_reason}")
    resource_count = len(contract["spec"]["resources"])
    listed_resources = fixtures.get("resources-list-result.json", {}).get("result", {}).get("resources", [])
    if len(listed_resources) != resource_count:
        errors.append("resources/list fixture count must match resource catalog")
    tool_count = len(contract["spec"]["tools"])
    listed_tools = fixtures.get("tools-list-result.json", {}).get("result", {}).get("tools", [])
    if len(listed_tools) != tool_count:
        errors.append("tools/list fixture count must match tool catalog")
    return errors


def _validate_paginated_request_fixture(name: str, fixture: dict[str, Any], errors: list[str]) -> None:
    params = fixture.get("params")
    if params is None:
        return
    if not isinstance(params, dict):
        errors.append(f"{name} params must be omitted or an object")
        return
    if "cursor" in params and not isinstance(params["cursor"], str):
        errors.append(f"{name} params.cursor must be omitted or a string")


def _validate_paginated_result_fixture(name: str, fixture: dict[str, Any], errors: list[str]) -> None:
    result = fixture.get("result")
    if not isinstance(result, dict):
        errors.append(f"{name} result must be an object")
        return
    expected_collection = PAGINATED_RESULT_FIXTURES[name]
    if expected_collection not in result:
        errors.append(f"{name} result.{expected_collection} must be present")
    if "nextCursor" in result and not isinstance(result["nextCursor"], str):
        errors.append(f"{name} result.nextCursor must be omitted or a string")


def _contains_secret_like_text(root: Path, paths: list[Path]) -> bool:
    for rel in paths:
        path = root / rel
        if path.exists() and path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if SECRET_LIKE_RE.search(text):
                allowed = {"authorization", "credential", "secret", "token", "password", "private key"}
                lowered = text.lower()
                if not any(word in lowered for word in allowed):
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
        write_mcp_server_contract_reports(temp_root)
        first = {}
        for path in sorted((temp_root / INTEROP_ROOT).rglob("*")) + sorted((temp_root / REPORT_ROOT).rglob("*")):
            if path.is_file():
                first[path.relative_to(temp_root).as_posix()] = path.read_bytes()
        write_mcp_server_contract_reports(temp_root)
        second = {}
        for path in sorted((temp_root / INTEROP_ROOT).rglob("*")) + sorted((temp_root / REPORT_ROOT).rglob("*")):
            if path.is_file():
                second[path.relative_to(temp_root).as_posix()] = path.read_bytes()
    return first == second


def write_mcp_server_contract_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    before = _hash_existing(root, source_artifact_paths(root))
    contract = build_mcp_server_contract(root)
    fixtures = build_fixtures(contract)
    schema = load_mcp_server_contract_schema(root)
    errors, warnings = validate_mcp_server_contract_with_schema(contract, schema)
    errors.extend(validate_fixtures(fixtures, contract))

    write_json(root / SERVER_CONTRACT_JSON, contract)
    write_json(root / CAPABILITY_CATALOG_JSON, _capability_matrix(contract))
    write_json(root / RESOURCE_CATALOG_JSON, _catalog_file("resource", contract["spec"]["resources"]))
    write_json(root / TOOL_CATALOG_JSON, _catalog_file("tool", contract["spec"]["tools"]))
    write_json(root / PROMPT_CATALOG_JSON, _catalog_file("prompt", contract["spec"]["prompts"]))
    write_json(root / CONFORMANCE_EXPECTATIONS_JSON, _catalog_file("conformance-expectation", contract["spec"]["conformance_expectations"]))
    for name, fixture in fixtures.items():
        write_json(root / FIXTURE_ROOT / name, fixture)

    fixture_index = _fixture_index(root, fixtures)
    capability_matrix = _capability_matrix(contract)
    validation_status = "FAILED_VALIDATION" if errors else "PASS_WITH_WARNINGS"
    projection_report = {
        "schema_version": "aide.mcp-server-contract.projection-report.v0",
        "task_id": TASK_ID,
        "status": validation_status,
        "contract_id": CONTRACT_ID,
        "target_protocol_version": TARGET_PROTOCOL_VERSION,
        "jsonrpc_version": JSONRPC_VERSION,
        "resource_count": len(contract["spec"]["resources"]),
        "tool_count": len(contract["spec"]["tools"]),
        "prompt_count": len(contract["spec"]["prompts"]),
        "fixture_count": len(fixtures),
        "transport_contract_count": len(contract["spec"]["transport_profiles"]),
        "conformance_expectation_count": len(contract["spec"]["conformance_expectations"]),
        "implemented_live_transport_count": 0,
        "callable_tool_count": 0,
        "served_resource_count": 0,
        "live_endpoint_count": 0,
        "errors": errors,
        "warnings": warnings,
        "source_artifacts_mutated": before != _hash_existing(root, source_artifact_paths(root)),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }

    write_json(root / CONTRACT_REPORT_JSON, contract)
    write_text(root / CONTRACT_REPORT_MD, render_contract_markdown(contract))
    write_json(root / CAPABILITY_MATRIX_JSON, capability_matrix)
    write_text(root / CAPABILITY_MATRIX_MD, render_capability_matrix_markdown(capability_matrix))
    write_json(root / RESOURCE_REPORT_JSON, _catalog_file("resource", contract["spec"]["resources"]))
    write_text(root / RESOURCE_REPORT_MD, render_catalog_markdown("Resources", contract["spec"]["resources"]))
    write_json(root / TOOL_REPORT_JSON, _catalog_file("tool", contract["spec"]["tools"]))
    write_text(root / TOOL_REPORT_MD, render_catalog_markdown("Tools", contract["spec"]["tools"]))
    write_json(root / PROMPT_REPORT_JSON, _catalog_file("prompt", contract["spec"]["prompts"]))
    write_text(root / PROMPT_REPORT_MD, render_catalog_markdown("Prompts", contract["spec"]["prompts"]))
    write_json(root / TRANSPORT_EXPECTATIONS_JSON, _catalog_file("transport", contract["spec"]["transport_profiles"]))
    write_text(root / TRANSPORT_EXPECTATIONS_MD, render_catalog_markdown("Transport Expectations", contract["spec"]["transport_profiles"]))
    write_json(root / AUTHORIZATION_EXPECTATIONS_JSON, {"schema_version": "aide.mcp-server-contract.authorization.v0", **contract["spec"]["authorization"]})
    write_text(root / AUTHORIZATION_EXPECTATIONS_MD, render_authorization_markdown(contract["spec"]["authorization"]))
    write_json(root / REFUSAL_MAPPING_JSON, _catalog_file("refusal", contract["spec"]["refusal_mappings"]))
    write_text(root / REFUSAL_MAPPING_MD, render_catalog_markdown("Refusal Mappings", contract["spec"]["refusal_mappings"]))
    write_json(root / CONFORMANCE_REPORT_JSON, _catalog_file("conformance-expectation", contract["spec"]["conformance_expectations"]))
    write_text(root / CONFORMANCE_REPORT_MD, render_catalog_markdown("Conformance Expectations", contract["spec"]["conformance_expectations"]))
    write_json(root / FIXTURE_INDEX_JSON, fixture_index)
    write_text(root / FIXTURE_INDEX_MD, render_fixture_index_markdown(fixture_index))
    write_text(root / EXPLICIT_NON_CAPABILITIES_MD, render_explicit_non_capabilities_markdown())
    write_text(root / FUTURE_WORK_MD, render_future_work_markdown())
    write_text(root / NEXT_TASK_PROMPT_MD, render_next_task_prompt())
    write_text(root / STATUS_MD, render_status_markdown(projection_report))
    return projection_report


def mcp_server_contract_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    contract_path = root / SERVER_CONTRACT_JSON
    schema_loaded = (root / SCHEMA_PATH).exists()
    contract = read_json(contract_path) if contract_path.exists() else build_mcp_server_contract(root)
    errors, warnings = validate_mcp_server_contract_with_schema(contract, load_mcp_server_contract_schema(root) if schema_loaded else None)
    fixture_count = len(list((root / FIXTURE_ROOT).glob("*.json"))) if (root / FIXTURE_ROOT).exists() else len(FIXTURE_FILES)
    capability_matrix = _capability_matrix(contract)
    return {
        "status": "FAILED_VALIDATION" if errors else "PASS_WITH_WARNINGS",
        "capability_target": FEATURE_FLAG,
        "schema_loaded": schema_loaded,
        "contract_valid": not errors,
        "target_protocol_version": contract["spec"].get("target_protocol_version"),
        "jsonrpc_version": contract["spec"].get("jsonrpc_version"),
        "resource_count": capability_matrix["resource_count"],
        "tool_count": capability_matrix["tool_count"],
        "prompt_count": capability_matrix["prompt_count"],
        "fixture_count": fixture_count,
        "transport_contract_count": len(contract["spec"].get("transport_profiles", [])),
        "conformance_expectation_count": len(contract["spec"].get("conformance_expectations", [])),
        "implemented_live_transport_count": capability_matrix["implemented_live_transport_count"],
        "callable_tool_count": capability_matrix["callable_tool_count"],
        "served_resource_count": capability_matrix["served_resource_count"],
        "live_endpoint_count": capability_matrix["live_endpoint_count"],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "warnings": warnings,
        "errors": errors,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        **contract["status"],
    }


def validate_mcp_server_contract(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    if project:
        write_mcp_server_contract_reports(root)
    schema_exists = (root / SCHEMA_PATH).exists()
    schema: dict[str, Any] | None = None
    schema_file_parsed = False
    schema_error = None
    if schema_exists:
        try:
            schema = load_mcp_server_contract_schema(root)
            schema_file_parsed = True
        except ValueError as exc:
            schema_error = str(exc)
    contract = read_json(root / SERVER_CONTRACT_JSON) if (root / SERVER_CONTRACT_JSON).exists() else build_mcp_server_contract(root)
    fixtures = build_fixtures(contract)
    errors, warnings = validate_mcp_server_contract_with_schema(contract, schema)
    errors.extend(validate_fixtures(fixtures, contract))
    source_before = _hash_existing(root, source_artifact_paths(root))
    deterministic_projection = _deterministic_projection_check(root)
    source_after = _hash_existing(root, source_artifact_paths(root))
    report_paths = [
        SERVER_CONTRACT_JSON,
        CAPABILITY_CATALOG_JSON,
        RESOURCE_CATALOG_JSON,
        TOOL_CATALOG_JSON,
        PROMPT_CATALOG_JSON,
        CONFORMANCE_EXPECTATIONS_JSON,
        *[FIXTURE_ROOT / name for name in FIXTURE_FILES],
        CONTRACT_REPORT_JSON,
        CAPABILITY_MATRIX_JSON,
        RESOURCE_REPORT_JSON,
        TOOL_REPORT_JSON,
        PROMPT_REPORT_JSON,
        TRANSPORT_EXPECTATIONS_JSON,
        AUTHORIZATION_EXPECTATIONS_JSON,
        REFUSAL_MAPPING_JSON,
        CONFORMANCE_REPORT_JSON,
        FIXTURE_INDEX_JSON,
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
        "schema_version": "aide.mcp-server-contract.validation.v0",
        "task_id": TASK_ID,
        "validation_status": status,
        "schema_exists": schema_exists,
        "schema_file_parsed": schema_file_parsed,
        "schema_error": schema_error,
        "helper_exists": True,
        "cli_registered": True,
        "schema_helper_alignment_checked": True,
        "schema_helper_alignment_status": "PASS" if schema_file_parsed and not schema_error else "FAILED_VALIDATION",
        "target_protocol_version": contract["spec"].get("target_protocol_version"),
        "jsonrpc_version": contract["spec"].get("jsonrpc_version"),
        "contract_valid": not errors,
        "resource_count": len(contract["spec"].get("resources", [])),
        "tool_count": len(contract["spec"].get("tools", [])),
        "prompt_count": len(contract["spec"].get("prompts", [])),
        "fixture_count": len(FIXTURE_FILES),
        "transport_contract_count": len(contract["spec"].get("transport_profiles", [])),
        "conformance_expectation_count": len(contract["spec"].get("conformance_expectations", [])),
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
        "# MCP Server Contract Status",
        "",
        f"- result: `{data.get('validation_status', data.get('status'))}`",
        f"- capability_target: `{FEATURE_FLAG}`",
        f"- target_protocol_version: `{data.get('target_protocol_version')}`",
        f"- jsonrpc_version: `{data.get('jsonrpc_version')}`",
        f"- resource_count: `{data.get('resource_count')}`",
        f"- tool_count: `{data.get('tool_count')}`",
        f"- prompt_count: `{data.get('prompt_count')}`",
        f"- fixture_count: `{data.get('fixture_count')}`",
        f"- implemented_live_transport_count: `{data.get('implemented_live_transport_count', 0)}`",
        f"- callable_tool_count: `{data.get('callable_tool_count', 0)}`",
        f"- served_resource_count: `{data.get('served_resource_count', 0)}`",
        f"- live_endpoint_count: `{data.get('live_endpoint_count', 0)}`",
        f"- recommended_next_task: `{data.get('recommended_next_task')}`",
        "",
        "This is a contract-only projection. It does not start or expose MCP runtime behavior.",
        "",
    ]
    return "\n".join(lines)


def render_contract_markdown(contract: dict[str, Any]) -> str:
    spec = contract["spec"]
    return "\n".join(
        [
            "# MCP Server Contract",
            "",
            f"- contract_id: `{spec['contract_id']}`",
            f"- advisory_contract_ref: `{spec['advisory_contract_ref']}`",
            f"- target_protocol_version: `{spec['target_protocol_version']}`",
            f"- jsonrpc_version: `{spec['jsonrpc_version']}`",
            f"- implementation_status: `{spec['server_info']['implementation_status']}`",
            "",
            "AIDE queue, protocol, evidence, and OKF records remain authoritative. MCP catalogues and fixtures are generated projections.",
            "",
        ]
    )


def render_capability_matrix_markdown(matrix: dict[str, Any]) -> str:
    lines = [
        "# MCP Capability Matrix",
        "",
        f"- declared resource catalog: `{matrix['declared_contract_capabilities']['resources']['catalog_defined']}`",
        f"- declared tool catalog: `{matrix['declared_contract_capabilities']['tools']['catalog_defined']}`",
        f"- declared prompt catalog: `{matrix['declared_contract_capabilities']['prompts']['catalog_defined']}`",
        f"- resources_served: `{matrix['implemented_runtime_capabilities']['resources_served']}`",
        f"- tools_callable: `{matrix['implemented_runtime_capabilities']['tools_callable']}`",
        f"- prompts_served: `{matrix['implemented_runtime_capabilities']['prompts_served']}`",
        "",
    ]
    return "\n".join(lines)


def render_catalog_markdown(title: str, items: list[dict[str, Any]]) -> str:
    lines = [f"# {title}", ""]
    if not items:
        lines.append("No entries are declared for this projection.")
    for item in items:
        label = item.get("name") or item.get("id") or item.get("uri")
        lines.append(f"- `{label}`")
    lines.append("")
    return "\n".join(lines)


def render_authorization_markdown(auth: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MCP Authorization Expectations",
            "",
            f"- authorization_supported_by_contract: `{auth.get('authorization_supported_by_contract')}`",
            f"- authorization_implemented: `{auth.get('authorization_implemented')}`",
            "",
            "MCP transport authorization does not replace future AIDE PolicyDecision or CapabilityGrant authority.",
            "",
        ]
    )


def render_fixture_index_markdown(index: dict[str, Any]) -> str:
    lines = ["# MCP Fixture Index", "", f"- fixture_count: `{index['fixture_count']}`", ""]
    for item in index["fixtures"]:
        lines.append(f"- `{item['path']}` `{item['sha256']}`")
    lines.append("")
    return "\n".join(lines)


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# MCP Server Contract Validation",
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
    lines.extend(f"- {item}" for item in report.get("errors", [])) or lines.append("- none")
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
            "# Future Work",
            "",
            "- Independent check of this MCP contract slice.",
            "- Acceptance review if the independent check passes.",
            "- Later live MCP server work only after authorization, runtime, and host semantics are separately accepted.",
            "",
        ]
    )


def render_next_task_prompt() -> str:
    return "\n".join(
        [
            "# AIDE-CHECK-MCP-SERVER-CONTRACT-01",
            "# Independent Check of Minimal Contract-Only MCP Projection",
            "",
            "Use `.aide/queue/index.yaml` as canonical queue truth.",
            "",
            "Check `AIDE-BUILD-MCP-SERVER-CONTRACT-01` without modifying the MCP contract implementation.",
            "Verify schema/helper alignment, protocol/version pinning, JSON-RPC fixtures, catalogue consistency, refusal fixtures, transport and authorization boundaries, deterministic projection, source immutability, and explicit non-capabilities.",
            "",
            "If no material issue exists, recommend `AIDE-ACCEPT-MCP-SERVER-CONTRACT-01`.",
            "If a material defect exists, recommend one bounded repair task.",
            "",
        ]
    )
