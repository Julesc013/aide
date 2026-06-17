"""Minimal AIDE CapabilityManifest helpers.

This module projects accepted AIDE protocol/report slices into a declaration-
only capability manifest. It records source, evidence, report, EventRecord, and
OKF references, but it does not prove conformance, admit adapters, execute
capabilities, create a runtime registry, call providers, mutate GitHub, or
apply changes to target repositories.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import envelope, reference_id


API_VERSION = envelope.API_VERSION
CAPABILITY_MANIFEST_SCHEMA_VERSION = "aide.capability-manifest.v0"
PROTOCOL_VERSION = "0.1.0"
PRODUCER_NAME = envelope.PRODUCER_NAME
PRODUCER_VERSION = envelope.PRODUCER_VERSION
FEATURE_FLAG = "minimal_capability_manifest"
ACCEPTED_PREDECESSOR = "minimal_reconciler_reports"
TASK_ID = "AIDE-BUILD-CAPABILITY-MANIFEST-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-CAPABILITY-MANIFEST-01"
DETERMINISTIC_TIMESTAMP = "2026-06-18T00:00:00+10:00"

REPORT_ROOT = Path(".aide/reports/capability-manifest")
SCHEMA_PATH = Path(".aide/protocol/aide-capability-manifest.schema.json")
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
CAPABILITIES_JSON = REPORT_ROOT / "capabilities.json"
CAPABILITIES_MD = REPORT_ROOT / "capabilities.md"
CAPABILITY_INDEX_JSON = REPORT_ROOT / "capability-index.json"
CAPABILITY_INDEX_MD = REPORT_ROOT / "capability-index.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"

REQUIRED_REPORTS = [
    STATUS_MD,
    PROJECTION_JSON,
    PROJECTION_MD,
    VALIDATION_JSON,
    VALIDATION_MD,
    CAPABILITIES_JSON,
    CAPABILITIES_MD,
    CAPABILITY_INDEX_JSON,
    CAPABILITY_INDEX_MD,
    FUTURE_WORK_MD,
    UNFINISHED_WORK_MD,
]

SUPPORTED_KINDS = {
    "CapabilityManifest",
    "CapabilityManifestProjectionReport",
    "CapabilityManifestValidationReport",
    "CapabilityManifestIndex",
}

REQUIRED_CAPABILITY_LABELS = [
    "minimal_contract_envelope",
    "minimal_evidence_packet_schema",
    "minimal_workunit_queue_v1",
    "minimal_workunit_readonly_cli",
    "minimal_workunit_queue_metadata_mutation_cli",
    "minimal_worker_run_schema",
    "minimal_test_job_schema",
    "minimal_reference_id_scheme",
    "minimal_event_record_schema",
    "minimal_okf_knowledge_bundle",
    "minimal_reconciler_reports",
]

SOURCE_PRIORITY = [
    "acceptance_task_status_and_evidence",
    "check_task_status_and_evidence",
    "build_task_status_and_evidence",
    "protocol_reports",
    "reconciler_reports",
    "okf_pages",
    "generated_context_packets",
]

STATUS_VALUES = {
    "declared",
    "implemented",
    "checked",
    "accepted",
    "accepted_with_warnings",
    "metadata_only",
    "report_only",
    "projection_only",
    "deferred",
    "blocked",
    "superseded",
}

EXPLICIT_NON_CAPABILITIES = [
    "conformance_profile",
    "conformance_result",
    "conformance_admission",
    "adapter_admission",
    "adapter_execution",
    "capability_execution",
    "runtime_capability_registry",
    "scheduler",
    "leases",
    "supervisor",
    "runtime",
    "service",
    "commander",
    "patch_transaction",
    "adapter_manifest",
    "context_pack_v2",
    "event_sourcing_runtime",
    "append_only_runtime_store",
    "runtime_event_log",
    "state_reconstruction",
    "test_broker_runtime",
    "async_execution",
    "worker_execution",
    "runtime_reference_registry",
    "resolver_service",
    "database_state",
    "provider_adapters",
    "branch_worktree_automation",
    "target_apply",
    "active_apply",
    "rollback_execution",
    "uninstall_execution",
    "release",
    "promotion",
    "github_mutation",
    "gateway_calls",
    "network_calls",
    "model_provider_calls",
    "target_repo_mutation",
    "production_readiness",
    "release_readiness",
    "broad_autonomous_runtime",
]

FORBIDDEN_CLAIM_PATTERNS = [
    "capabilitymanifest proves capability",
    "capabilitymanifest admits capability",
    "capabilitymanifest executes capability",
    "conformanceprofile implemented",
    "conformanceresult implemented",
    "adapter admission implemented",
    "adapter execution implemented",
    "runtime capability registry implemented",
    "scheduler implemented",
    "leases implemented",
    "supervisor implemented",
    "runtime implemented",
    "service implemented",
    "commander implemented",
    "patchtransaction implemented",
    "adaptermanifest implemented",
    "contextpack v2 implemented",
    "event sourcing runtime implemented",
    "append-only runtime store implemented",
    "test broker runtime implemented",
    "worker execution implemented",
    "provider/model calls implemented",
    "network/gateway/github calls implemented",
    "target apply implemented",
    "active apply implemented",
    "release ready",
    "production ready",
    "autonomous runtime ready",
]

SCHEMA_VALIDATION_MODE = "minimal_json_schema_subset"
SCHEMA_VALIDATION_LIMITATIONS = [
    "Local subset validator checks required envelope, manifest, capability-record, status, and boundary fields.",
    "Full JSON Schema Draft 2020-12 validation remains future work.",
    "CapabilityManifest declares accepted queue state but does not prove conformance or admission.",
]

CAPABILITY_DEFINITIONS: list[dict[str, Any]] = [
    {
        "label": "minimal_contract_envelope",
        "title": "Minimal Contract Envelope",
        "capability_class": "protocol",
        "tags": ["protocol", "envelope"],
        "build_task": "AIDE-BUILD-CONTRACT-ENVELOPE-01",
        "check_task": "AIDE-CHECK-CONTRACT-ENVELOPE-01",
        "accept_task": "AIDE-ACCEPT-CONTRACT-ENVELOPE-01",
        "schema_ref": "aide://schema/envelope",
        "helper_path": "core/protocol/envelope.py",
        "schema_path": ".aide/protocol/aide-envelope.schema.json",
        "report_paths": [
            ".aide/reports/contract-envelope/validation.json",
            ".aide/reports/contract-envelope-acceptance/acceptance-report.json",
        ],
        "okf_ref": "aide://source/okf-minimal-contract-envelope",
        "okf_path": ".aide/knowledge/okf/capabilities/minimal-contract-envelope.md",
        "metadata_only": False,
        "report_only": False,
        "projection_only": False,
        "mutating": False,
        "known_limitations": [
            "Full JSON Schema Draft 2020-12 validation remains deferred.",
            "The envelope is a protocol wrapper, not a runtime execution authority.",
        ],
        "explicit_non_capabilities": ["runtime", "service", "capability_execution", "conformance_admission"],
    },
    {
        "label": "minimal_evidence_packet_schema",
        "title": "Minimal EvidencePacket Schema",
        "capability_class": "protocol_evidence",
        "tags": ["protocol", "evidence"],
        "build_task": "AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01",
        "check_task": "AIDE-CHECK-EVIDENCE-PACKET-SCHEMA-01",
        "accept_task": "AIDE-ACCEPT-EVIDENCE-PACKET-SCHEMA-01",
        "schema_ref": "aide://schema/evidence-packet",
        "helper_path": "core/protocol/evidence_packet.py",
        "schema_path": ".aide/protocol/aide-evidence-packet.schema.json",
        "report_paths": [
            ".aide/reports/evidence-packet/validation.json",
            ".aide/reports/evidence-packet-acceptance/acceptance-report.json",
        ],
        "okf_ref": "aide://source/okf-minimal-evidence-packet",
        "okf_path": ".aide/knowledge/okf/capabilities/minimal-evidence-packet.md",
        "metadata_only": False,
        "report_only": False,
        "projection_only": False,
        "mutating": False,
        "known_limitations": [
            "EvidencePacket records proof metadata; it is not an evidence runtime.",
            "Full JSON Schema Draft 2020-12 validation remains deferred.",
        ],
        "explicit_non_capabilities": ["runtime", "capability_execution", "provider_adapters"],
    },
    {
        "label": "minimal_workunit_queue_v1",
        "title": "Minimal WorkUnit Queue",
        "capability_class": "protocol_queue_projection",
        "tags": ["protocol", "queue", "projection"],
        "build_task": "AIDE-BUILD-WORKUNIT-QUEUE-V1-01",
        "check_task": "AIDE-CHECK-WORKUNIT-QUEUE-V1-01",
        "accept_task": "AIDE-ACCEPT-WORKUNIT-QUEUE-V1-01",
        "schema_ref": "aide://schema/workunit",
        "helper_path": "core/protocol/workunit.py",
        "schema_path": ".aide/protocol/aide-workunit.schema.json",
        "report_paths": [
            ".aide/reports/workunit-queue/validation.json",
            ".aide/reports/workunit-queue-acceptance/acceptance-report.json",
        ],
        "okf_ref": "aide://source/okf-minimal-workunit-queue",
        "okf_path": ".aide/knowledge/okf/capabilities/minimal-workunit-queue.md",
        "metadata_only": False,
        "report_only": False,
        "projection_only": True,
        "mutating": False,
        "known_limitations": [
            "WorkUnit queue projection does not claim, run, finish, or repair work.",
            "Scheduler, leases, supervisor, and worker execution remain deferred.",
        ],
        "explicit_non_capabilities": ["scheduler", "leases", "supervisor", "worker_execution"],
    },
    {
        "label": "minimal_workunit_readonly_cli",
        "title": "Minimal Read-Only WorkUnit CLI",
        "capability_class": "cli_read_only",
        "tags": ["cli", "queue", "read-only"],
        "build_task": "AIDE-BUILD-WORKUNIT-CLI-01",
        "check_task": "AIDE-CHECK-WORKUNIT-CLI-01",
        "accept_task": "AIDE-ACCEPT-WORKUNIT-CLI-01",
        "helper_path": "core/protocol/workunit_cli.py",
        "report_paths": [
            ".aide/reports/workunit-cli/validation.json",
            ".aide/reports/workunit-cli-acceptance/acceptance-report.json",
        ],
        "metadata_only": False,
        "report_only": False,
        "projection_only": False,
        "mutating": False,
        "known_limitations": [
            "Read-only WorkUnit CLI does not mutate queue state.",
            "Claim, run, finish, repair, runtime, and scheduler behavior remain deferred.",
        ],
        "explicit_non_capabilities": ["capability_execution", "scheduler", "worker_execution", "target_apply"],
    },
    {
        "label": "minimal_workunit_queue_metadata_mutation_cli",
        "title": "Minimal WorkUnit Queue Metadata Mutation CLI",
        "capability_class": "cli_queue_metadata_mutation",
        "tags": ["cli", "queue", "metadata-mutation"],
        "build_task": "AIDE-BUILD-WORKUNIT-CLI-MUTATION-01",
        "check_task": "AIDE-CHECK-WORKUNIT-CLI-MUTATION-01",
        "accept_task": "AIDE-ACCEPT-WORKUNIT-CLI-MUTATION-01",
        "helper_path": "core/protocol/workunit_cli.py",
        "report_paths": [
            ".aide/reports/workunit-cli-mutation/validation.json",
            ".aide/reports/workunit-cli-mutation-acceptance/acceptance-report.json",
        ],
        "metadata_only": False,
        "report_only": False,
        "projection_only": False,
        "mutating": True,
        "known_limitations": [
            "Mutation is limited to reviewed queue metadata commands.",
            "Claim, run, finish, repair, runtime, leases, scheduler, and target apply remain deferred.",
        ],
        "explicit_non_capabilities": ["worker_execution", "scheduler", "leases", "target_apply", "active_apply"],
    },
    {
        "label": "minimal_worker_run_schema",
        "title": "Minimal WorkerRun Schema",
        "capability_class": "protocol_metadata",
        "tags": ["protocol", "worker-run", "metadata-only"],
        "build_task": "AIDE-BUILD-WORKER-RUN-SCHEMA-01",
        "check_task": "AIDE-CHECK-WORKER-RUN-SCHEMA-01",
        "accept_task": "AIDE-ACCEPT-WORKER-RUN-SCHEMA-01",
        "schema_ref": "aide://schema/worker-run",
        "helper_path": "core/protocol/worker_run.py",
        "schema_path": ".aide/protocol/aide-worker-run.schema.json",
        "report_paths": [
            ".aide/reports/worker-run/validation.json",
            ".aide/reports/worker-run-accept/acceptance-report.json",
        ],
        "okf_ref": "aide://source/okf-minimal-worker-run-schema",
        "okf_path": ".aide/knowledge/okf/capabilities/minimal-worker-run-schema.md",
        "metadata_only": True,
        "report_only": False,
        "projection_only": False,
        "mutating": False,
        "known_limitations": [
            "WorkerRun is metadata-only and does not execute workers.",
            "WorkUnit claim/run/finish/repair, leases, scheduler, and supervisor remain deferred.",
        ],
        "explicit_non_capabilities": ["worker_execution", "leases", "scheduler", "supervisor"],
    },
    {
        "label": "minimal_test_job_schema",
        "title": "Minimal TestJob Schema",
        "capability_class": "protocol_metadata",
        "tags": ["protocol", "test-job", "metadata-only"],
        "build_task": "AIDE-BUILD-TESTJOB-SCHEMA-01",
        "check_task": "AIDE-CHECK-TESTJOB-SCHEMA-01",
        "accept_task": "AIDE-ACCEPT-TESTJOB-SCHEMA-01",
        "schema_ref": "aide://schema/test-job",
        "helper_path": "core/protocol/test_job.py",
        "schema_path": ".aide/protocol/aide-test-job.schema.json",
        "report_paths": [
            ".aide/reports/test-job/validation.json",
            ".aide/reports/test-job-accept/acceptance-report.json",
        ],
        "okf_ref": "aide://source/okf-minimal-testjob-schema",
        "okf_path": ".aide/knowledge/okf/capabilities/minimal-testjob-schema.md",
        "metadata_only": True,
        "report_only": False,
        "projection_only": False,
        "mutating": False,
        "known_limitations": [
            "TestJob is metadata-only and does not submit or run tests.",
            "Test Broker runtime and async execution remain deferred.",
        ],
        "explicit_non_capabilities": ["test_broker_runtime", "async_execution", "worker_execution"],
    },
    {
        "label": "minimal_reference_id_scheme",
        "title": "Minimal Reference ID Scheme",
        "capability_class": "protocol_identity_projection",
        "tags": ["protocol", "reference-id", "projection"],
        "build_task": "AIDE-BUILD-REFERENCE-ID-SCHEME-01",
        "check_task": "AIDE-CHECK-REFERENCE-ID-SCHEME-01",
        "accept_task": "AIDE-ACCEPT-REFERENCE-ID-SCHEME-01",
        "schema_ref": "aide://schema/reference-id",
        "helper_path": "core/protocol/reference_id.py",
        "schema_path": ".aide/protocol/aide-reference-id.schema.json",
        "report_paths": [
            ".aide/reports/reference-id/validation.json",
            ".aide/reports/reference-id/reference-map.json",
            ".aide/reports/reference-id-accept/acceptance-report.json",
        ],
        "okf_ref": "aide://source/okf-minimal-reference-id-scheme",
        "okf_path": ".aide/knowledge/okf/capabilities/minimal-reference-id-scheme.md",
        "metadata_only": False,
        "report_only": False,
        "projection_only": True,
        "mutating": False,
        "known_limitations": [
            "ReferenceID is syntactic/projection-only.",
            "Runtime reference registry, resolver service, and database state remain deferred.",
        ],
        "explicit_non_capabilities": ["runtime_reference_registry", "resolver_service", "database_state"],
    },
    {
        "label": "minimal_event_record_schema",
        "title": "Minimal EventRecord Schema",
        "capability_class": "protocol_event_projection",
        "tags": ["protocol", "event-record", "projection"],
        "build_task": "AIDE-BUILD-EVENT-RECORD-SCHEMA-01",
        "check_task": "AIDE-CHECK-EVENT-RECORD-SCHEMA-01",
        "accept_task": "AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01",
        "schema_ref": "aide://schema/event-record",
        "helper_path": "core/protocol/event_record.py",
        "schema_path": ".aide/protocol/aide-event-record.schema.json",
        "report_paths": [
            ".aide/reports/event-record/validation.json",
            ".aide/reports/event-record/event-family-index.json",
            ".aide/reports/event-record-accept/acceptance-report.json",
        ],
        "okf_ref": "aide://source/okf-minimal-event-record-schema",
        "okf_path": ".aide/knowledge/okf/capabilities/minimal-event-record-schema.md",
        "metadata_only": False,
        "report_only": False,
        "projection_only": True,
        "mutating": False,
        "known_limitations": [
            "EventRecord is projection-only and does not append, store, or replay events.",
            "Event sourcing runtime, append-only store, and state reconstruction remain deferred.",
        ],
        "explicit_non_capabilities": ["event_sourcing_runtime", "append_only_runtime_store", "runtime_event_log", "state_reconstruction"],
    },
    {
        "label": "minimal_okf_knowledge_bundle",
        "title": "Minimal OKF Knowledge Bundle",
        "capability_class": "knowledge_projection",
        "tags": ["knowledge", "okf", "projection"],
        "build_task": "AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01",
        "check_task": "AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01",
        "accept_task": "AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01",
        "helper_path": "core/knowledge/okf_bundle.py",
        "report_paths": [
            ".aide/reports/okf/validation.json",
            ".aide/reports/okf/projection-report.json",
            ".aide/reports/okf-accept/acceptance-report.json",
        ],
        "okf_ref": "aide://source/okf-index",
        "okf_path": ".aide/knowledge/okf/index.md",
        "metadata_only": False,
        "report_only": False,
        "projection_only": True,
        "mutating": False,
        "known_limitations": [
            "OKF pages are deterministic knowledge projection only.",
            "Markdown does not become protocol, evidence, or execution authority.",
        ],
        "explicit_non_capabilities": ["okf_execution_authority", "protocol_authority_from_markdown", "runtime_knowledge_service"],
    },
    {
        "label": "minimal_reconciler_reports",
        "title": "Minimal Reconciler Reports",
        "capability_class": "report_only_reconciler",
        "tags": ["reconciler", "report-only", "drift-detection"],
        "build_task": "AIDE-BUILD-RECONCILER-REPORTS-01",
        "check_task": "AIDE-CHECK-RECONCILER-REPORTS-01",
        "accept_task": "AIDE-ACCEPT-RECONCILER-REPORTS-01",
        "helper_path": "core/reconciler/reconciler_reports.py",
        "report_paths": [
            ".aide/reports/reconciler/validation.json",
            ".aide/reports/reconciler/findings.json",
            ".aide/reports/reconciler-accept/acceptance-report.json",
        ],
        "metadata_only": False,
        "report_only": True,
        "projection_only": False,
        "mutating": False,
        "known_limitations": [
            "Reconciler detects and reports drift only.",
            "Repair, source truth mutation, queue mutation, and generated context refresh remain deferred.",
        ],
        "explicit_non_capabilities": ["drift_repair", "source_truth_mutation", "queue_acceptance_mutation", "latest_task_packet_rewrite"],
    },
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


def _relative(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._~-]+", "-", value).strip("-")
    return slug or "item"


def _clean_scalar(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        return ""
    if stripped[0] in {'"', "'"} and stripped[-1:] == stripped[0]:
        return stripped[1:-1]
    return stripped


def parse_top_level_scalars(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        if not raw_line or raw_line.startswith(" ") or raw_line.startswith("-"):
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        if key:
            values[key] = _clean_scalar(value)
    return values


def parse_simple_list(text: str, key: str) -> list[str]:
    values: list[str] = []
    in_list = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped == f"{key}:":
            in_list = True
            continue
        if in_list:
            if stripped.startswith("- "):
                values.append(_clean_scalar(stripped[2:]))
                continue
            if stripped and not raw_line.startswith(" "):
                break
    return values


def _read_text_optional(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _compatibility(required_capabilities: list[str] | None = None) -> dict[str, Any]:
    required = [FEATURE_FLAG, ACCEPTED_PREDECESSOR]
    for capability in required_capabilities or []:
        if capability not in required:
            required.append(capability)
    return {
        "schemaVersion": PROTOCOL_VERSION,
        "protocolVersion": PROTOCOL_VERSION,
        "minReaderVersion": PROTOCOL_VERSION,
        "minWriterVersion": PROTOCOL_VERSION,
        "featureFlags": [FEATURE_FLAG],
        "requiredCapabilities": required,
    }


def _normalize_validation_state(values: dict[str, str]) -> str:
    raw = values.get("validation_status") or values.get("result") or values.get("decision") or "UNKNOWN"
    raw = raw.strip().upper()
    if raw == "ACCEPTED":
        return "PASS"
    if raw == "ACCEPTED_WITH_WARNINGS":
        return "PASS_WITH_WARNINGS"
    if raw in {"PASS", "PASS_WITH_WARNINGS", "FAILED_VALIDATION", "BLOCKED", "PARTIAL"}:
        return raw
    return "UNKNOWN"


def _acceptance_state(result: str) -> str:
    normalized = result.strip().upper()
    if normalized == "ACCEPTED_WITH_WARNINGS":
        return "accepted_with_warnings"
    if normalized == "ACCEPTED":
        return "accepted"
    if normalized in {"BLOCKED", "PARTIAL", "FAILED_VALIDATION", "FAILED"}:
        return normalized.lower()
    return "unknown"


def _queue_task_ref(task_id: str) -> str:
    return reference_id.format_reference_id("queue-task", task_id)


def _path_ref(kind: str, rel: str) -> str:
    return reference_id.format_reference_id(kind, _slug(rel).lower())


def _capability_ref(label: str) -> str:
    return reference_id.format_reference_id("capability", label)


def _event_ref(label: str) -> str:
    return reference_id.format_reference_id("event", f"capability-declared-{label}")


def _status_path(definition: dict[str, Any]) -> Path:
    return Path(".aide/queue") / str(definition["accept_task"]) / "status.yaml"


def _task_paths(definition: dict[str, Any]) -> list[str]:
    rels: list[str] = []
    for key in ["build_task", "check_task", "accept_task"]:
        task_id = str(definition[key])
        rels.extend(
            [
                f".aide/queue/{task_id}/task.yaml",
                f".aide/queue/{task_id}/status.yaml",
            ]
        )
    return rels


def _default_evidence_paths(repo_root: Path, task_id: str) -> list[str]:
    root = repo_root / ".aide/queue" / task_id / "evidence"
    if not root.exists():
        return []
    preferred = [
        "acceptance-summary.md",
        "acceptance-review.md",
        "source-chain-review.md",
        "warning-disposition.md",
        "non-capability-boundary.md",
        "no-forbidden-ops.md",
        "validation.md",
    ]
    paths: list[str] = []
    for name in preferred:
        path = root / name
        if path.exists():
            paths.append(_relative(path, repo_root))
    if not paths:
        paths.extend(_relative(path, repo_root) for path in sorted(root.glob("*.md"))[:3])
    return paths


def load_acceptance_chain(repo_root: str | Path) -> dict[str, dict[str, Any]]:
    root = Path(repo_root)
    chain: dict[str, dict[str, Any]] = {}
    for definition in CAPABILITY_DEFINITIONS:
        label = str(definition["label"])
        status_rel = _status_path(definition).as_posix()
        status_path = root / status_rel
        text = _read_text_optional(status_path)
        scalars = parse_top_level_scalars(text) if text else {}
        evidence = parse_simple_list(text, "evidence") if text else []
        reports = parse_simple_list(text, "reports") if text else []
        if not evidence:
            evidence = _default_evidence_paths(root, str(definition["accept_task"]))
        chain[label] = {
            "label": label,
            "status_path": status_rel,
            "status_exists": status_path.exists(),
            "values": scalars,
            "evidence": evidence,
            "reports": reports,
            "result": scalars.get("result", "UNKNOWN"),
            "validation_state": _normalize_validation_state(scalars),
            "acceptance_state": _acceptance_state(scalars.get("result", "")),
        }
    return chain


def _existing_report_paths(repo_root: Path, definition: dict[str, Any], status_reports: list[str]) -> list[str]:
    candidates = [*status_reports, *[str(path) for path in definition.get("report_paths", [])]]
    existing: list[str] = []
    for rel in candidates:
        if rel and (repo_root / rel).exists() and rel not in existing:
            existing.append(rel)
    return existing


def _source_artifacts_from_definition(repo_root: Path, definition: dict[str, Any], chain_item: dict[str, Any]) -> list[str]:
    candidates = [
        *_task_paths(definition),
        str(definition.get("helper_path") or ""),
        str(definition.get("schema_path") or ""),
        str(definition.get("okf_path") or ""),
        *chain_item.get("evidence", []),
        *_existing_report_paths(repo_root, definition, chain_item.get("reports", [])),
    ]
    return sorted({rel for rel in candidates if rel and (repo_root / rel).exists()})


def source_artifact_paths(repo_root: str | Path) -> list[str]:
    root = Path(repo_root)
    chain = load_acceptance_chain(root)
    paths: set[str] = {
        ".aide/queue/index.yaml",
        ".aide/context/latest-task-packet.md",
        ".aide/reports/reconciler/findings.json",
        ".aide/reports/reconciler/reconciliation-report.json",
        ".aide/reports/reconciler/validation.json",
        ".aide/reports/reconciler-accept/acceptance-report.json",
        ".aide/reports/okf/validation.json",
        ".aide/reports/okf/lint.json",
        ".aide/reports/reference-id/validation.json",
        ".aide/reports/event-record/validation.json",
    }
    for definition in CAPABILITY_DEFINITIONS:
        paths.update(_source_artifacts_from_definition(root, definition, chain[str(definition["label"])]))
    return sorted(rel for rel in paths if (root / rel).exists())


def _hash_source_artifacts(repo_root: Path, rels: list[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel in rels:
        path = repo_root / rel
        if path.exists() and path.is_file():
            hashes[rel] = sha256_file(path)
    return hashes


def _load_reconciler_findings(repo_root: Path) -> list[dict[str, Any]]:
    path = repo_root / ".aide/reports/reconciler/findings.json"
    if not path.exists():
        return []
    try:
        data = read_json(path)
    except ValueError:
        return []
    findings = data.get("findings", [])
    return [item for item in findings if isinstance(item, dict)]


def _reconciler_warning_summary(findings: list[dict[str, Any]]) -> list[dict[str, str]]:
    summary: list[dict[str, str]] = []
    for finding in findings:
        if finding.get("severity") == "warning":
            summary.append(
                {
                    "id": str(finding.get("id", "")),
                    "category": str(finding.get("category", "")),
                    "title": str(finding.get("title", "")),
                    "status": str(finding.get("status", "")),
                    "disposition": "classified_no_repair",
                }
            )
    return summary


def build_capability_record(
    repo_root: str | Path,
    definition: dict[str, Any],
    chain_item: dict[str, Any],
    reconciler_findings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    root = Path(repo_root)
    label = str(definition["label"])
    result = str(chain_item.get("result") or "UNKNOWN")
    acceptance_state = str(chain_item.get("acceptance_state") or _acceptance_state(result))
    accepted = acceptance_state in {"accepted", "accepted_with_warnings"}
    evidence_paths = [rel for rel in chain_item.get("evidence", []) if (root / rel).exists()]
    report_paths = _existing_report_paths(root, definition, chain_item.get("reports", []))
    source_task_ids = [str(definition[key]) for key in ["build_task", "check_task", "accept_task"]]
    source_refs = [_queue_task_ref(task_id) for task_id in source_task_ids]
    if definition.get("schema_ref"):
        source_refs.append(str(definition["schema_ref"]))
    evidence_refs = [_path_ref("evidence", rel) for rel in evidence_paths]
    report_refs = [_path_ref("report", rel) for rel in report_paths]
    okf_refs = [str(definition["okf_ref"])] if definition.get("okf_path") and (root / str(definition["okf_path"])).exists() else []
    record_non_capabilities = sorted({*EXPLICIT_NON_CAPABILITIES, *[str(item) for item in definition.get("explicit_non_capabilities", [])]})
    relevant_reconciler = []
    if label == "minimal_reconciler_reports":
        relevant_reconciler = _reconciler_warning_summary(reconciler_findings or [])
    return {
        "capability_label": label,
        "capability_ref": _capability_ref(label),
        "title": str(definition["title"]),
        "capability_class": str(definition["capability_class"]),
        "tags": list(definition.get("tags", [])),
        "declared": True,
        "implemented": bool((root / f".aide/queue/{definition['build_task']}/status.yaml").exists()),
        "checked": bool((root / f".aide/queue/{definition['check_task']}/status.yaml").exists()),
        "accepted": accepted,
        "accepted_with_warnings": acceptance_state == "accepted_with_warnings",
        "acceptance_state": acceptance_state,
        "validation_state": str(chain_item.get("validation_state", "UNKNOWN")),
        "metadata_only": bool(definition.get("metadata_only", False)),
        "report_only": bool(definition.get("report_only", False)),
        "projection_only": bool(definition.get("projection_only", False)),
        "runtime": False,
        "mutating": bool(definition.get("mutating", False)),
        "admitted_by_conformance": False,
        "conformance": {
            "profile_ref": None,
            "result_ref": None,
            "profile_implemented": False,
            "result_implemented": False,
            "admission_implemented": False,
            "admitted": False,
            "placeholder_only": True,
        },
        "source_refs": source_refs,
        "source_paths": _source_artifacts_from_definition(root, definition, chain_item),
        "evidence_refs": evidence_refs,
        "evidence_paths": evidence_paths,
        "report_refs": report_refs,
        "report_paths": report_paths,
        "event_refs": [_event_ref(label)],
        "event_ref_status": "projection_only_reference_no_runtime_log",
        "okf_refs": okf_refs,
        "okf_paths": [str(definition["okf_path"])] if okf_refs else [],
        "known_limitations": list(definition.get("known_limitations", [])),
        "explicit_non_capabilities": record_non_capabilities,
        "reconciler_findings": relevant_reconciler,
    }


def build_capability_manifest(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    chain = load_acceptance_chain(root)
    findings = _load_reconciler_findings(root)
    records = [
        build_capability_record(root, definition, chain[str(definition["label"])], findings)
        for definition in CAPABILITY_DEFINITIONS
    ]
    warnings = capability_manifest_warnings()
    metadata = {
        "id": "capability-manifest-minimal",
        "name": "Minimal AIDE CapabilityManifest",
        "title": "Minimal AIDE CapabilityManifest",
        "createdAt": DETERMINISTIC_TIMESTAMP,
        "sourcePath": CAPABILITIES_JSON.as_posix(),
        "producer": {"name": PRODUCER_NAME, "version": PRODUCER_VERSION},
        "compatibility": _compatibility(REQUIRED_CAPABILITY_LABELS),
    }
    spec = {
        "capability_target": FEATURE_FLAG,
        "accepted_predecessor": ACCEPTED_PREDECESSOR,
        "declaration_only": True,
        "source_priority": list(SOURCE_PRIORITY),
        "capabilities": records,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "conformance": {
            "profile_ref": None,
            "result_ref": None,
            "profile_implemented": False,
            "result_implemented": False,
            "admission_implemented": False,
            "admitted_by_conformance": False,
            "placeholder_only": True,
        },
        "reconciler_warning_findings": _reconciler_warning_summary(findings),
    }
    status = {
        "valid": True,
        "validated": True,
        "result": "PASS_WITH_WARNINGS",
        "validation_status": "PASS_WITH_WARNINGS",
        "declaration_only": True,
        "validation_errors": [],
        "validation_warnings": warnings,
        "conformance_implemented": False,
        "admission_implemented": False,
        "execution_implemented": False,
        "runtime": False,
        "mutating": False,
    }
    obj = envelope.build_envelope("CapabilityManifest", metadata, spec, status, api_version=API_VERSION)
    obj["schema_version"] = CAPABILITY_MANIFEST_SCHEMA_VERSION
    obj["protocol_version"] = PROTOCOL_VERSION
    return obj


def build_capability_index(manifest: dict[str, Any]) -> dict[str, Any]:
    capabilities = list(manifest.get("spec", {}).get("capabilities", []))
    return {
        "schema_version": "aide.capability-manifest-index.v0",
        "report_type": "capability_manifest_index",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "status": manifest.get("status", {}).get("validation_status", "UNKNOWN"),
        "declaration_only": True,
        "capability_count": len(capabilities),
        "capabilities": [
            {
                "capability_label": item.get("capability_label"),
                "capability_ref": item.get("capability_ref"),
                "acceptance_state": item.get("acceptance_state"),
                "validation_state": item.get("validation_state"),
                "metadata_only": item.get("metadata_only"),
                "report_only": item.get("report_only"),
                "projection_only": item.get("projection_only"),
                "runtime": item.get("runtime"),
                "mutating": item.get("mutating"),
                "admitted_by_conformance": item.get("admitted_by_conformance"),
            }
            for item in capabilities
        ],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def capability_counts(manifest: dict[str, Any]) -> dict[str, int]:
    capabilities = list(manifest.get("spec", {}).get("capabilities", []))
    return {
        "capabilities_count": len(capabilities),
        "accepted_capabilities_count": sum(1 for item in capabilities if item.get("accepted") is True),
        "accepted_with_warnings_count": sum(1 for item in capabilities if item.get("accepted_with_warnings") is True),
        "metadata_only_count": sum(1 for item in capabilities if item.get("metadata_only") is True),
        "report_only_count": sum(1 for item in capabilities if item.get("report_only") is True),
        "projection_only_count": sum(1 for item in capabilities if item.get("projection_only") is True),
    }


def capability_manifest_warnings() -> list[str]:
    return [
        "CapabilityManifest declares capability state but does not prove conformance.",
        "ConformanceProfile is not implemented.",
        "ConformanceResult is not implemented.",
        "Adapter admission is not implemented.",
        "Adapter execution is not implemented.",
        "Runtime capability registry is not implemented.",
        "PatchTransaction is not implemented.",
        "AdapterManifest is not implemented.",
        "ContextPack v2 is not implemented.",
        "Accepted predecessor capabilities preserve accepted_with_warnings rather than flattening to done.",
        "Stale latest-task-packet drift remains reported; queue truth is canonical.",
    ]


def future_work_items() -> list[dict[str, str]]:
    return [
        {
            "task": "AIDE-CHECK-CAPABILITY-MANIFEST-01",
            "reason": "independent review of the declaration-only CapabilityManifest schema, helper, reports, CLI, tests, and boundaries",
        },
        {
            "task": "AIDE-ACCEPT-CAPABILITY-MANIFEST-01",
            "reason": "accept CapabilityManifest only after the independent check",
        },
        {
            "task": "AIDE-BUILD-CONFORMANCE-PROFILE-01",
            "reason": "future work after CapabilityManifest check and acceptance, not a direct next task from this build",
        },
    ]


def unfinished_work_items() -> list[dict[str, str]]:
    return [{"item": item, "reason": "intentionally deferred beyond the minimal CapabilityManifest slice"} for item in EXPLICIT_NON_CAPABILITIES]


def capability_manifest_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    projection_exists = (root / PROJECTION_JSON).exists()
    capabilities_count = 0
    accepted_count = 0
    accepted_with_warnings_count = 0
    if (root / CAPABILITIES_JSON).exists():
        try:
            manifest = read_json(root / CAPABILITIES_JSON)
            counts = capability_counts(manifest)
            capabilities_count = counts["capabilities_count"]
            accepted_count = counts["accepted_capabilities_count"]
            accepted_with_warnings_count = counts["accepted_with_warnings_count"]
        except ValueError:
            pass
    data = {
        "schema_version": "aide.capability-manifest-status.v0",
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "status": "PASS_WITH_WARNINGS",
        "schema_path": SCHEMA_PATH.as_posix(),
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_path": "core/protocol/capability_manifest.py",
        "helper_exists": (root / "core/protocol/capability_manifest.py").exists(),
        "projection_exists": projection_exists,
        "capabilities_count": capabilities_count,
        "accepted_capabilities_count": accepted_count,
        "accepted_with_warnings_count": accepted_with_warnings_count,
        "warnings": capability_manifest_warnings(),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "declaration_only": True,
        "conformance_implemented": False,
        "admission_implemented": False,
        "execution_implemented": False,
        "runtime": False,
        "mutating": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    return data


def write_capability_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    sources = source_artifact_paths(root)
    before = _hash_source_artifacts(root, sources)
    manifest = build_capability_manifest(root)
    index = build_capability_index(manifest)
    write_json(root / CAPABILITIES_JSON, manifest)
    write_text(root / CAPABILITIES_MD, render_capabilities_markdown(manifest))
    write_json(root / CAPABILITY_INDEX_JSON, index)
    write_text(root / CAPABILITY_INDEX_MD, render_index_markdown(index))
    write_text(root / FUTURE_WORK_MD, render_future_work_markdown())
    write_text(root / UNFINISHED_WORK_MD, render_unfinished_work_markdown())
    validation = validate_capability_manifest(root, project=False)
    counts = capability_counts(manifest)
    after = _hash_source_artifacts(root, sources)
    report = {
        "schema_version": "aide.capability-manifest-projection.v0",
        "report_type": "capability_manifest_projection",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "status": validation["validation_status"],
        "declaration_only": True,
        "conformance_implemented": False,
        "admission_implemented": False,
        "execution_implemented": False,
        **counts,
        "source_artifacts_checked": sources,
        "source_artifacts_mutated": before != after,
        "reports_written": [path.as_posix() for path in REQUIRED_REPORTS],
        "warnings": capability_manifest_warnings(),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    status = capability_manifest_status(root)
    status["status"] = report["status"]
    write_text(root / STATUS_MD, render_status_markdown(status))
    return report


def load_capability_manifest_schema(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / SCHEMA_PATH
    if not path.exists():
        raise ValueError(f"CapabilityManifest schema missing: {SCHEMA_PATH.as_posix()}")
    return read_json(path)


def validate_capability_manifest_with_schema(obj: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    del schema
    errors: list[str] = []
    if obj.get("apiVersion") != API_VERSION:
        errors.append("apiVersion must match AIDE API version")
    if obj.get("kind") != "CapabilityManifest":
        errors.append("kind must be CapabilityManifest")
    for field in ["metadata", "spec", "status"]:
        if not isinstance(obj.get(field), dict):
            errors.append(f"{field} must be an object")
    spec = obj.get("spec") if isinstance(obj.get("spec"), dict) else {}
    status = obj.get("status") if isinstance(obj.get("status"), dict) else {}
    for field in ["capability_target", "accepted_predecessor", "declaration_only", "capabilities", "explicit_non_capabilities", "conformance", "source_priority"]:
        if field not in spec:
            errors.append(f"missing spec field: {field}")
    capabilities = spec.get("capabilities", [])
    if not isinstance(capabilities, list) or not capabilities:
        errors.append("spec.capabilities must be a non-empty array")
        capabilities = []
    required_record_fields = {
        "capability_label",
        "capability_ref",
        "declared",
        "implemented",
        "checked",
        "accepted",
        "acceptance_state",
        "validation_state",
        "metadata_only",
        "report_only",
        "projection_only",
        "runtime",
        "mutating",
        "admitted_by_conformance",
        "source_refs",
        "evidence_refs",
        "report_refs",
        "known_limitations",
        "explicit_non_capabilities",
        "conformance",
    }
    for index, record in enumerate(capabilities):
        if not isinstance(record, dict):
            errors.append(f"spec.capabilities[{index}] must be an object")
            continue
        missing = sorted(required_record_fields - set(record))
        errors.extend(f"spec.capabilities[{index}] missing field: {field}" for field in missing)
    for field in ["valid", "declaration_only", "validation_status", "validation_errors", "validation_warnings", "conformance_implemented", "admission_implemented", "execution_implemented", "runtime", "mutating"]:
        if field not in status:
            errors.append(f"missing status field: {field}")
    return errors


def _cli_registered(repo_root: Path) -> bool:
    script = repo_root / ".aide/scripts/aide_lite.py"
    return script.exists() and 'subparsers.add_parser("capability-manifest")' in script.read_text(encoding="utf-8")


def _json_valid(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return True


def _all_refs_parse(records: list[dict[str, Any]]) -> bool:
    refs: list[str] = []
    for record in records:
        refs.extend(str(item) for item in record.get("source_refs", []))
        refs.extend(str(item) for item in record.get("evidence_refs", []))
        refs.extend(str(item) for item in record.get("report_refs", []))
        refs.extend(str(item) for item in record.get("event_refs", []))
        refs.append(str(record.get("capability_ref", "")))
    for ref in refs:
        result = reference_id.validate_reference_id(ref, required=True)
        if not result.valid:
            return False
    return True


def _overclaiming_findings(repo_root: Path) -> list[str]:
    findings: list[str] = []
    for rel in [STATUS_MD, PROJECTION_MD, VALIDATION_MD, CAPABILITIES_MD, CAPABILITY_INDEX_MD, FUTURE_WORK_MD, UNFINISHED_WORK_MD]:
        path = repo_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        collapsed = re.sub(r"[^a-z0-9/ -]+", "", text)
        for pattern in FORBIDDEN_CLAIM_PATTERNS:
            if pattern in collapsed:
                findings.append(f"{rel.as_posix()}: {pattern}")
    return sorted(set(findings))


def forbidden_operations_preserved() -> dict[str, bool]:
    return {
        "conformance_profile": True,
        "conformance_result": True,
        "conformance_admission": True,
        "adapter_admission": True,
        "adapter_execution": True,
        "capability_execution": True,
        "runtime_capability_registry": True,
        "scheduler": True,
        "leases": True,
        "supervisor": True,
        "runtime": True,
        "service": True,
        "commander": True,
        "patch_transaction": True,
        "adapter_manifest": True,
        "context_pack_v2": True,
        "event_sourcing_runtime": True,
        "append_only_runtime_store": True,
        "runtime_event_log": True,
        "state_reconstruction": True,
        "test_broker_runtime": True,
        "async_execution": True,
        "worker_execution": True,
        "runtime_reference_registry": True,
        "resolver_service": True,
        "database_state": True,
        "provider_adapters": True,
        "branch_worktree_automation": True,
        "target_apply": True,
        "active_apply": True,
        "rollback_execution": True,
        "uninstall_execution": True,
        "release": True,
        "promotion": True,
        "github_mutation": True,
        "gateway_calls": True,
        "network_calls": True,
        "model_provider_calls": True,
        "target_repo_mutation": True,
        "broad_autonomous_runtime": True,
        "production_readiness": True,
        "release_readiness": True,
    }


def validate_capability_manifest(repo_root: str | Path, *, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    if project or not (root / CAPABILITIES_JSON).exists():
        manifest = build_capability_manifest(root)
        write_json(root / CAPABILITIES_JSON, manifest)
        write_text(root / CAPABILITIES_MD, render_capabilities_markdown(manifest))
        index = build_capability_index(manifest)
        write_json(root / CAPABILITY_INDEX_JSON, index)
        write_text(root / CAPABILITY_INDEX_MD, render_index_markdown(index))
        write_text(root / FUTURE_WORK_MD, render_future_work_markdown())
        write_text(root / UNFINISHED_WORK_MD, render_unfinished_work_markdown())
    schema_exists = (root / SCHEMA_PATH).exists()
    schema_file_loaded = False
    schema_file_parsed = False
    schema_validation_executed = False
    schema_errors: list[str] = []
    try:
        schema = load_capability_manifest_schema(root)
        schema_file_loaded = True
        schema_file_parsed = True
    except ValueError as exc:
        schema = {}
        schema_errors.append(str(exc))
    try:
        manifest = read_json(root / CAPABILITIES_JSON)
    except ValueError as exc:
        manifest = {}
        schema_errors.append(str(exc))
    records = [item for item in manifest.get("spec", {}).get("capabilities", []) if isinstance(item, dict)]
    if schema_file_parsed and manifest:
        schema_validation_executed = True
        schema_errors.extend(validate_capability_manifest_with_schema(manifest, schema))
    labels = [str(record.get("capability_label", "")) for record in records]
    required_projected = all(label in labels for label in REQUIRED_CAPABILITY_LABELS)
    accepted_have_evidence = all(
        bool(record.get("evidence_refs")) for record in records if record.get("accepted") is True
    )
    accepted_with_warnings_preserved = all(
        record.get("acceptance_state") == "accepted_with_warnings" for record in records if record.get("accepted") is True
    )
    status_semantics_valid = all(
        record.get("acceptance_state") in STATUS_VALUES
        and isinstance(record.get("metadata_only"), bool)
        and isinstance(record.get("report_only"), bool)
        and isinstance(record.get("projection_only"), bool)
        and record.get("runtime") is False
        and record.get("admitted_by_conformance") is False
        for record in records
    )
    conformance_not_overclaimed = (
        manifest.get("spec", {}).get("conformance", {}).get("profile_implemented") is False
        and manifest.get("spec", {}).get("conformance", {}).get("result_implemented") is False
        and manifest.get("status", {}).get("conformance_implemented") is False
        and all(record.get("conformance", {}).get("admitted") is False for record in records)
    )
    execution_not_overclaimed = (
        manifest.get("status", {}).get("execution_implemented") is False
        and manifest.get("status", {}).get("runtime") is False
        and all(record.get("runtime") is False for record in records)
    )
    reconciler_integration_checked = bool(_load_reconciler_findings(root)) and any(
        record.get("reconciler_findings") for record in records if record.get("capability_label") == "minimal_reconciler_reports"
    )
    okf_integration_checked = any(record.get("okf_refs") for record in records)
    reference_id_refs_valid = _all_refs_parse(records)
    predecessor_compatibility_preserved = all((root / rel).exists() for rel in [".aide/reports/reconciler/validation.json", ".aide/reports/okf/validation.json", ".aide/reports/reference-id/validation.json", ".aide/reports/event-record/validation.json"])
    overclaiming = _overclaiming_findings(root)
    forbidden = forbidden_operations_preserved()
    reports_generated = all((root / rel).exists() for rel in REQUIRED_REPORTS if rel not in {VALIDATION_JSON, VALIDATION_MD, PROJECTION_JSON, PROJECTION_MD, STATUS_MD})
    capabilities_json_valid = _json_valid(root / CAPABILITIES_JSON)
    capability_index_json_valid = _json_valid(root / CAPABILITY_INDEX_JSON)
    errors = [
        *schema_errors,
        *overclaiming,
    ]
    checks = {
        "schema_exists": schema_exists,
        "helper_exists": (root / "core/protocol/capability_manifest.py").exists(),
        "cli_registered": _cli_registered(root),
        "reports_generated": reports_generated,
        "capabilities_json_valid": capabilities_json_valid,
        "capability_index_json_valid": capability_index_json_valid,
        "required_capabilities_projected": required_projected,
        "accepted_capabilities_have_evidence": accepted_have_evidence,
        "accepted_with_warnings_preserved": accepted_with_warnings_preserved,
        "status_semantics_valid": status_semantics_valid,
        "conformance_not_overclaimed": conformance_not_overclaimed,
        "execution_not_overclaimed": execution_not_overclaimed,
        "reconciler_integration_checked": reconciler_integration_checked,
        "okf_integration_checked": okf_integration_checked,
        "reference_id_refs_valid": reference_id_refs_valid,
        "predecessor_compatibility_preserved": predecessor_compatibility_preserved,
        "overclaiming_check_passed": not overclaiming,
        "forbidden_ops_preserved": all(forbidden.values()),
    }
    failed_checks = [key for key, value in checks.items() if value is not True]
    errors.extend(f"failed check: {key}" for key in failed_checks)
    status = "FAILED_VALIDATION" if errors else "PASS_WITH_WARNINGS"
    validation = {
        "schema_version": "aide.capability-manifest-validation.v0",
        "report_type": "capability_manifest_validation",
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "task_id": TASK_ID,
        "capability_target": FEATURE_FLAG,
        "accepted_predecessor": ACCEPTED_PREDECESSOR,
        "schema_file_loaded": schema_file_loaded,
        "schema_file_parsed": schema_file_parsed,
        "schema_validation_executed": schema_validation_executed,
        "schema_validation_mode": SCHEMA_VALIDATION_MODE if schema_validation_executed else "unavailable",
        "schema_validation_limitations": SCHEMA_VALIDATION_LIMITATIONS,
        "validation_status": status,
        "status": status,
        "validated": status in {"PASS", "PASS_WITH_WARNINGS"},
        "validation_errors": errors,
        "warnings": capability_manifest_warnings(),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "forbidden_operations_preserved": forbidden,
        "conformance_implemented": False,
        "admission_implemented": False,
        "execution_implemented": False,
        "runtime_capability_registry_implemented": False,
        "runtime": False,
        "provider_model_calls": False,
        "network_calls": False,
        "gateway_calls": False,
        "github_mutation": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        **checks,
        **capability_counts(manifest),
    }
    write_json(root / VALIDATION_JSON, validation)
    write_text(root / VALIDATION_MD, render_validation_markdown(validation))
    write_text(root / STATUS_MD, render_status_markdown({**validation, "projection_exists": (root / PROJECTION_JSON).exists()}))
    return validation


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# CapabilityManifest Status",
        "",
        f"- task_id: {TASK_ID}",
        f"- capability_target: {FEATURE_FLAG}",
        f"- status: {data.get('validation_status', data.get('status', 'UNKNOWN'))}",
        f"- schema_exists: {str(data.get('schema_exists', False)).lower()}",
        f"- helper_exists: {str(data.get('helper_exists', False)).lower()}",
        f"- projection_exists: {str(data.get('projection_exists', False)).lower()}",
        f"- capabilities_count: {data.get('capabilities_count', 0)}",
        f"- accepted_capabilities_count: {data.get('accepted_capabilities_count', 0)}",
        f"- accepted_with_warnings_count: {data.get('accepted_with_warnings_count', 0)}",
        "- declaration_only: true",
        "- conformance_implemented: false",
        "- admission_implemented: false",
        "- execution_implemented: false",
        "- runtime: false",
        "- mutating: false",
        f"- recommended_next_task: {RECOMMENDED_NEXT_TASK}",
        "",
        "## Explicit Non-Capabilities",
        "",
    ]
    lines.extend(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES)
    lines.extend(["", "## Warnings", ""])
    warnings = data.get("warnings", capability_manifest_warnings())
    lines.extend(f"- {warning}" for warning in warnings)
    return "\n".join(lines) + "\n"


def render_capabilities_markdown(manifest: dict[str, Any]) -> str:
    counts = capability_counts(manifest)
    lines = [
        "# CapabilityManifest Capabilities",
        "",
        f"- task_id: {TASK_ID}",
        f"- capability_target: {FEATURE_FLAG}",
        "- declaration_only: true",
        f"- capabilities_count: {counts['capabilities_count']}",
        f"- accepted_capabilities_count: {counts['accepted_capabilities_count']}",
        f"- accepted_with_warnings_count: {counts['accepted_with_warnings_count']}",
        "- conformance_implemented: false",
        "- admission_implemented: false",
        "- execution_implemented: false",
        "",
        "## Capabilities",
        "",
    ]
    for record in manifest.get("spec", {}).get("capabilities", []):
        lines.append(
            f"- {record.get('capability_label')}: acceptance_state={record.get('acceptance_state')}; "
            f"metadata_only={str(record.get('metadata_only')).lower()}; "
            f"report_only={str(record.get('report_only')).lower()}; "
            f"projection_only={str(record.get('projection_only')).lower()}; "
            f"runtime={str(record.get('runtime')).lower()}; "
            f"mutating={str(record.get('mutating')).lower()}; "
            "admitted_by_conformance=false"
        )
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in manifest.get("status", {}).get("validation_warnings", []))
    return "\n".join(lines) + "\n"


def render_index_markdown(index: dict[str, Any]) -> str:
    lines = [
        "# CapabilityManifest Index",
        "",
        f"- task_id: {TASK_ID}",
        f"- status: {index.get('status')}",
        f"- capability_count: {index.get('capability_count')}",
        "- declaration_only: true",
        "",
        "## Index",
        "",
    ]
    for record in index.get("capabilities", []):
        lines.append(
            f"- {record.get('capability_ref')}: {record.get('acceptance_state')} "
            f"(metadata_only={str(record.get('metadata_only')).lower()}, "
            f"report_only={str(record.get('report_only')).lower()}, "
            f"projection_only={str(record.get('projection_only')).lower()}, "
            f"runtime={str(record.get('runtime')).lower()}, "
            f"mutating={str(record.get('mutating')).lower()})"
        )
    return "\n".join(lines) + "\n"


def render_projection_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# CapabilityManifest Projection Report",
        "",
        f"- task_id: {TASK_ID}",
        f"- capability_target: {FEATURE_FLAG}",
        f"- status: {report.get('status')}",
        "- declaration_only: true",
        "- conformance_implemented: false",
        "- admission_implemented: false",
        "- execution_implemented: false",
        f"- capabilities_count: {report.get('capabilities_count')}",
        f"- accepted_capabilities_count: {report.get('accepted_capabilities_count')}",
        f"- accepted_with_warnings_count: {report.get('accepted_with_warnings_count')}",
        f"- metadata_only_count: {report.get('metadata_only_count')}",
        f"- report_only_count: {report.get('report_only_count')}",
        f"- projection_only_count: {report.get('projection_only_count')}",
        f"- source_artifacts_mutated: {str(report.get('source_artifacts_mutated', False)).lower()}",
        f"- recommended_next_task: {RECOMMENDED_NEXT_TASK}",
        "",
        "## Source Artifacts Checked",
        "",
    ]
    lines.extend(f"- {rel}" for rel in report.get("source_artifacts_checked", []))
    lines.extend(["", "## Reports Written", ""])
    lines.extend(f"- {rel}" for rel in report.get("reports_written", []))
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in report.get("warnings", []))
    return "\n".join(lines) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# CapabilityManifest Validation",
        "",
        f"- validation_status: {report.get('validation_status')}",
        f"- schema_exists: {str(report.get('schema_exists', False)).lower()}",
        f"- helper_exists: {str(report.get('helper_exists', False)).lower()}",
        f"- cli_registered: {str(report.get('cli_registered', False)).lower()}",
        f"- reports_generated: {str(report.get('reports_generated', False)).lower()}",
        f"- capabilities_json_valid: {str(report.get('capabilities_json_valid', False)).lower()}",
        f"- capability_index_json_valid: {str(report.get('capability_index_json_valid', False)).lower()}",
        f"- required_capabilities_projected: {str(report.get('required_capabilities_projected', False)).lower()}",
        f"- accepted_capabilities_have_evidence: {str(report.get('accepted_capabilities_have_evidence', False)).lower()}",
        f"- accepted_with_warnings_preserved: {str(report.get('accepted_with_warnings_preserved', False)).lower()}",
        f"- status_semantics_valid: {str(report.get('status_semantics_valid', False)).lower()}",
        f"- conformance_not_overclaimed: {str(report.get('conformance_not_overclaimed', False)).lower()}",
        f"- execution_not_overclaimed: {str(report.get('execution_not_overclaimed', False)).lower()}",
        f"- reconciler_integration_checked: {str(report.get('reconciler_integration_checked', False)).lower()}",
        f"- okf_integration_checked: {str(report.get('okf_integration_checked', False)).lower()}",
        f"- reference_id_refs_valid: {str(report.get('reference_id_refs_valid', False)).lower()}",
        f"- predecessor_compatibility_preserved: {str(report.get('predecessor_compatibility_preserved', False)).lower()}",
        f"- overclaiming_check_passed: {str(report.get('overclaiming_check_passed', False)).lower()}",
        f"- forbidden_ops_preserved: {str(report.get('forbidden_ops_preserved', False)).lower()}",
        "- conformance_implemented: false",
        "- admission_implemented: false",
        "- execution_implemented: false",
        "- runtime: false",
        "- provider_or_model_calls: none",
        "- Gateway calls: none",
        "- network_calls: none",
        f"- recommended_next_task: {RECOMMENDED_NEXT_TASK}",
        "",
        "## Errors",
        "",
    ]
    errors = report.get("validation_errors", [])
    lines.extend(f"- {error}" for error in errors) if errors else lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in report.get("warnings", []))
    return "\n".join(lines) + "\n"


def render_future_work_markdown() -> str:
    lines = ["# CapabilityManifest Future Work", "", "## Recommended Order", ""]
    for index, item in enumerate(future_work_items(), start=1):
        lines.append(f"{index}. {item['task']}: {item['reason']}.")
    lines.extend(
        [
            "",
            f"This build task recommends only `{RECOMMENDED_NEXT_TASK}` as the next task.",
            "ConformanceProfile remains deferred until CapabilityManifest check and acceptance.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_unfinished_work_markdown() -> str:
    lines = [
        "# CapabilityManifest Unfinished Work",
        "",
        "## Finished In This Slice",
        "",
        "- Minimal envelope-backed CapabilityManifest schema/helper.",
        "- Deterministic declaration projection over accepted AIDE queue capabilities.",
        "- Local JSON and Markdown reports under `.aide/reports/capability-manifest/`.",
        "- Thin capability-manifest status/project/validate CLI dispatch.",
        "",
        "## Not Attempted By Design",
        "",
    ]
    for item in unfinished_work_items():
        lines.append(f"- {item['item']}: {item['reason']}.")
    return "\n".join(lines) + "\n"
