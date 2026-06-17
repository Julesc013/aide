"""Deterministic OKF-compatible AIDE knowledge bundle projection.

This module writes and validates markdown knowledge pages. It does not make
markdown execution authority, replace protocol/evidence truth, call networks,
or implement a runtime knowledge service.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.protocol import event_record, reference_id


TASK_ID = "AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01"
CAPABILITY_TARGET = "minimal_okf_knowledge_bundle"
ACCEPTED_PREDECESSOR = "minimal_event_record_schema"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01"
OKF_VERSION_TARGET = "v0.1-compatible"
DETERMINISTIC_TIMESTAMP = "2026-06-17T00:00:00+10:00"
SCHEMA_VERSION = "aide.okf-knowledge-bundle.v0"
FRONTMATTER_MODE = "stdlib_structural_subset"
FRONTMATTER_WARNING = "full YAML parser unavailable; stdlib structural frontmatter validation used"

BUNDLE_ROOT = Path(".aide/knowledge/okf")
REPORT_ROOT = Path(".aide/reports/okf")
STATUS_MD = REPORT_ROOT / "status.md"
PROJECTION_JSON = REPORT_ROOT / "projection-report.json"
PROJECTION_MD = REPORT_ROOT / "projection-report.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
LINT_JSON = REPORT_ROOT / "lint.json"
LINT_MD = REPORT_ROOT / "lint.md"
CONCEPT_INDEX_JSON = REPORT_ROOT / "concept-index.json"
CONCEPT_INDEX_MD = REPORT_ROOT / "concept-index.md"
LINK_INDEX_JSON = REPORT_ROOT / "link-index.json"
LINK_INDEX_MD = REPORT_ROOT / "link-index.md"
FUTURE_WORK_MD = REPORT_ROOT / "future-work.md"
UNFINISHED_WORK_MD = REPORT_ROOT / "unfinished-work.md"

RESERVED_FILENAMES = {"index.md", "log.md"}
AUTHORITY_BOUNDARY = "Protocol executes. Evidence proves. References identify. Events remember. OKF knowledge explains."
AUTHORITY_SUMMARY = [
    "Protocol executes.",
    "Evidence proves.",
    "References identify.",
    "Events remember.",
    "OKF knowledge explains.",
]

EXPLICIT_NON_CAPABILITIES = [
    "okf_execution_authority",
    "protocol_authority_from_markdown",
    "evidence_authority_from_markdown",
    "runtime_knowledge_service",
    "llm_authored_wiki",
    "network_enrichment",
    "web_crawling",
    "provider_model_calls",
    "search_index_service",
    "vector_index",
    "okf_visualizer",
    "reconciler",
    "capability_manifest",
    "conformance_profile",
    "patch_transaction",
    "adapter_manifest",
    "context_pack_v2",
    "event_sourcing_runtime",
    "append_only_runtime_store",
    "runtime_event_log",
    "state_reconstruction",
    "scheduler",
    "leases",
    "supervisor",
    "test_broker_runtime",
    "async_execution",
    "worker_execution",
    "service",
    "commander",
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
    "production_readiness",
    "release_readiness",
    "broad_autonomous_runtime",
]

FORBIDDEN_CLAIM_PATTERNS = [
    "okf pages are execution authority",
    "okf pages are canonical protocol truth",
    "okf pages are canonical evidence truth",
    "okf pages authorize runtime",
    "llm-authored wiki implemented",
    "network enrichment implemented",
    "web crawling implemented",
    "provider/model calls implemented",
    "search index service implemented",
    "vector index implemented",
    "okf visualizer implemented",
    "reconciler implemented",
    "capabilitymanifest implemented",
    "conformanceprofile implemented",
    "patchtransaction implemented",
    "adaptermanifest implemented",
    "contextpack v2 implemented",
    "runtime registry implemented",
    "resolver service implemented",
    "database state implemented",
    "scheduler implemented",
    "leases implemented",
    "supervisor implemented",
    "service implemented",
    "commander implemented",
    "test broker runtime implemented",
    "worker execution implemented",
    "target apply implemented",
    "active apply implemented",
    "release ready",
    "production ready",
    "autonomous runtime ready",
]

FRONTMATTER_FIELD_ORDER = [
    "type",
    "title",
    "description",
    "resource",
    "tags",
    "timestamp",
    "aide_uri",
    "aide_kind",
    "schema_ref",
    "aide_status",
    "aide_review_state",
    "aide_validation_state",
    "aide_acceptance_state",
    "aide_capability_label",
    "accepted_capability",
    "generated_from",
    "source_refs",
    "evidence_refs",
    "report_refs",
    "event_refs",
    "source_hashes",
    "explicit_non_capabilities",
]

REQUIRED_CONCEPT_PATHS = [
    "current-state/queue.md",
    "current-state/review-gates.md",
    "current-state/stale-latest-task-packet.md",
    "current-state/next-work.md",
    "protocol/envelope.md",
    "protocol/evidence-packet.md",
    "protocol/workunit.md",
    "protocol/worker-run.md",
    "protocol/testjob.md",
    "protocol/reference-id.md",
    "protocol/event-record.md",
    "capabilities/minimal-contract-envelope.md",
    "capabilities/minimal-evidence-packet.md",
    "capabilities/minimal-workunit-queue.md",
    "capabilities/minimal-worker-run-schema.md",
    "capabilities/minimal-testjob-schema.md",
    "capabilities/minimal-reference-id-scheme.md",
    "capabilities/minimal-event-record-schema.md",
    "decisions/protocol-vs-knowledge.md",
    "decisions/repo-contract-vs-runtime-state.md",
    "decisions/okf-as-knowledge-plane.md",
    "risks/stale-latest-task-packet.md",
    "risks/acceptance-gate-debt.md",
    "risks/overclaiming.md",
]

PROTOCOLS = [
    {
        "slug": "envelope",
        "title": "Contract Envelope",
        "type": "AIDE Protocol Object",
        "aide_kind": "ContractEnvelope",
        "schema_ref": "aide://schema/envelope",
        "schema_path": ".aide/protocol/aide-envelope.schema.json",
        "helper_path": "core/protocol/envelope.py",
        "status": "accepted_with_warnings",
        "capability": "minimal_contract_envelope",
        "accept_task": "AIDE-ACCEPT-CONTRACT-ENVELOPE-01",
        "evidence": ".aide/queue/AIDE-ACCEPT-CONTRACT-ENVELOPE-01/evidence/acceptance-review.md",
        "report": ".aide/reports/contract-envelope-acceptance/acceptance-report.json",
    },
    {
        "slug": "evidence-packet",
        "title": "EvidencePacket",
        "type": "AIDE Protocol Object",
        "aide_kind": "EvidencePacket",
        "schema_ref": "aide://schema/evidence-packet",
        "schema_path": ".aide/protocol/aide-evidence-packet.schema.json",
        "helper_path": "core/protocol/evidence_packet.py",
        "status": "accepted_with_warnings",
        "capability": "minimal_evidence_packet_schema",
        "accept_task": "AIDE-ACCEPT-EVIDENCE-PACKET-SCHEMA-01",
        "evidence": ".aide/queue/AIDE-ACCEPT-EVIDENCE-PACKET-SCHEMA-01/evidence/acceptance-review.md",
        "report": ".aide/reports/evidence-packet-acceptance/acceptance-report.json",
    },
    {
        "slug": "workunit",
        "title": "WorkUnit",
        "type": "AIDE Protocol Object",
        "aide_kind": "WorkUnit",
        "schema_ref": "aide://schema/workunit",
        "schema_path": ".aide/protocol/aide-workunit.schema.json",
        "helper_path": "core/protocol/workunit.py",
        "status": "accepted_with_warnings",
        "capability": "minimal_workunit_queue_v1",
        "accept_task": "AIDE-ACCEPT-WORKUNIT-QUEUE-V1-01",
        "evidence": ".aide/queue/AIDE-ACCEPT-WORKUNIT-QUEUE-V1-01/evidence/acceptance-review.md",
        "report": ".aide/reports/workunit-queue-acceptance/acceptance-report.json",
    },
    {
        "slug": "worker-run",
        "title": "WorkerRun",
        "type": "AIDE Protocol Object",
        "aide_kind": "WorkerRun",
        "schema_ref": "aide://schema/worker-run",
        "schema_path": ".aide/protocol/aide-worker-run.schema.json",
        "helper_path": "core/protocol/worker_run.py",
        "status": "accepted_with_warnings",
        "capability": "minimal_worker_run_schema",
        "accept_task": "AIDE-ACCEPT-WORKER-RUN-SCHEMA-01",
        "evidence": ".aide/queue/AIDE-ACCEPT-WORKER-RUN-SCHEMA-01/evidence/acceptance-summary.md",
        "report": ".aide/reports/worker-run-accept/acceptance-report.json",
    },
    {
        "slug": "testjob",
        "title": "TestJob",
        "type": "AIDE Protocol Object",
        "aide_kind": "TestJob",
        "schema_ref": "aide://schema/test-job",
        "schema_path": ".aide/protocol/aide-test-job.schema.json",
        "helper_path": "core/protocol/test_job.py",
        "status": "accepted_with_warnings",
        "capability": "minimal_test_job_schema",
        "accept_task": "AIDE-ACCEPT-TESTJOB-SCHEMA-01",
        "evidence": ".aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/evidence/acceptance-summary.md",
        "report": ".aide/reports/test-job-accept/acceptance-report.json",
    },
    {
        "slug": "reference-id",
        "title": "ReferenceID",
        "type": "AIDE Protocol Object",
        "aide_kind": "ReferenceID",
        "schema_ref": "aide://schema/reference-id",
        "schema_path": ".aide/protocol/aide-reference-id.schema.json",
        "helper_path": "core/protocol/reference_id.py",
        "status": "accepted_with_warnings",
        "capability": "minimal_reference_id_scheme",
        "accept_task": "AIDE-ACCEPT-REFERENCE-ID-SCHEME-01",
        "evidence": ".aide/queue/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01/evidence/acceptance-summary.md",
        "report": ".aide/reports/reference-id-accept/acceptance-report.json",
    },
    {
        "slug": "event-record",
        "title": "EventRecord",
        "type": "AIDE Protocol Object",
        "aide_kind": "EventRecord",
        "schema_ref": "aide://schema/event-record",
        "schema_path": ".aide/protocol/aide-event-record.schema.json",
        "helper_path": "core/protocol/event_record.py",
        "status": "accepted_with_warnings",
        "capability": "minimal_event_record_schema",
        "accept_task": "AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01",
        "evidence": ".aide/queue/AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01/evidence/acceptance-summary.md",
        "report": ".aide/reports/event-record-accept/acceptance-report.json",
    },
]


@dataclass(frozen=True)
class FrontmatterValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def status(self) -> str:
        if not self.valid:
            return "FAILED_VALIDATION"
        return "PASS_WITH_WARNINGS" if self.warnings else "PASS"

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "status": self.status,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


@dataclass(frozen=True)
class ConceptPage:
    rel_path: str
    fields: dict[str, Any]
    body: str


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not load JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(obj), encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def hash_file_sha256(path: Path) -> str:
    return _sha256(path)


def _sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _frontmatter_sort_key(item: tuple[str, Any]) -> tuple[int, str]:
    key = item[0]
    try:
        index = FRONTMATTER_FIELD_ORDER.index(key)
    except ValueError:
        index = len(FRONTMATTER_FIELD_ORDER)
    return index, key


def _yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def write_frontmatter(fields: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in sorted(fields.items(), key=_frontmatter_sort_key):
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    sorted_items = sorted(item.items())
                    if not sorted_items:
                        lines.append("  - {}")
                        continue
                    first_key, first_value = sorted_items[0]
                    lines.append(f"  - {first_key}: {_yaml_scalar(first_value)}")
                    for nested_key, nested_value in sorted_items[1:]:
                        lines.append(f"    {nested_key}: {_yaml_scalar(nested_value)}")
                else:
                    lines.append(f"  - {_yaml_scalar(item)}")
        else:
            lines.append(f"{key}: {_yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def _parse_scalar(value: str) -> Any:
    stripped = value.strip()
    if stripped == "true":
        return True
    if stripped == "false":
        return False
    if stripped == "null":
        return None
    if stripped.startswith('"') and stripped.endswith('"'):
        return json.loads(stripped)
    if re.match(r"^-?\d+$", stripped):
        return int(stripped)
    return stripped


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("frontmatter opening delimiter missing")
    delimiter = "\n---\n"
    end = text.find(delimiter, 4)
    if end == -1:
        raise ValueError("frontmatter closing delimiter missing")
    raw = text[4:end]
    body = text[end + len(delimiter) :]
    lines = raw.splitlines()
    fields: dict[str, Any] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith(" "):
            raise ValueError(f"unexpected indentation: {line}")
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            fields[key] = _parse_scalar(value)
            index += 1
            continue
        items: list[Any] = []
        index += 1
        while index < len(lines) and lines[index].startswith("  - "):
            item_text = lines[index][4:].strip()
            if ": " in item_text:
                item_key, item_value = item_text.split(": ", 1)
                item_obj: dict[str, Any] = {item_key.strip(): _parse_scalar(item_value)}
                index += 1
                while index < len(lines) and lines[index].startswith("    "):
                    nested = lines[index][4:]
                    if ": " not in nested:
                        raise ValueError(f"invalid nested frontmatter line: {lines[index]}")
                    nested_key, nested_value = nested.split(": ", 1)
                    item_obj[nested_key.strip()] = _parse_scalar(nested_value)
                    index += 1
                items.append(item_obj)
            else:
                items.append(_parse_scalar(item_text))
                index += 1
        fields[key] = items
    return fields, body


def validate_frontmatter(fields: dict[str, Any], *, reserved: bool = False) -> FrontmatterValidationResult:
    errors: list[str] = []
    warnings: list[str] = [FRONTMATTER_WARNING]
    if not reserved:
        page_type = fields.get("type")
        if not isinstance(page_type, str) or not page_type.strip():
            errors.append("concept document must include non-empty type")
    for forbidden in ["not_capabilities", "non_capabilities"]:
        if forbidden in fields:
            errors.append(f"use explicit_non_capabilities instead of {forbidden}")
    explicit = fields.get("explicit_non_capabilities")
    if explicit is not None:
        if not isinstance(explicit, list) or not all(isinstance(item, str) and item for item in explicit):
            errors.append("explicit_non_capabilities must be a list of non-empty strings")
    for field_name in ["aide_uri", "resource", "schema_ref"]:
        value = fields.get(field_name)
        if isinstance(value, str) and value.startswith("aide://"):
            result = reference_id.validate_reference_id(value, required=True)
            if not result.valid:
                errors.extend(f"{field_name}: {error}" for error in result.errors)
    for list_field in ["generated_from", "event_refs"]:
        values = fields.get(list_field, [])
        if not isinstance(values, list):
            errors.append(f"{list_field} must be a list")
            continue
        for ref in values:
            if isinstance(ref, str) and ref.startswith("aide://"):
                parsed = reference_id.validate_reference_id(ref, required=True)
                if not parsed.valid:
                    errors.extend(f"{list_field}: {error}" for error in parsed.errors)
                if list_field == "event_refs" and parsed.parsed is not None and parsed.parsed.kind != "event":
                    errors.append(f"event_refs entries must use aide://event refs: {ref}")
    return FrontmatterValidationResult(not errors, tuple(errors), tuple(warnings))


def build_concept_page(fields: dict[str, Any], body: str) -> str:
    return write_frontmatter(fields) + body.rstrip() + "\n"


def write_concept_page(repo_root: Path, page: ConceptPage) -> Path:
    target = repo_root / BUNDLE_ROOT / page.rel_path
    write_text(target, build_concept_page(page.fields, page.body))
    return target


def _source_hashes(repo_root: Path, source_refs: list[str]) -> list[dict[str, str]]:
    hashes: list[dict[str, str]] = []
    for rel in source_refs:
        path = repo_root / rel
        if path.exists() and path.is_file():
            hashes.append({"path": rel, "sha256": _sha256(path)})
    return hashes


def _standard_fields(
    *,
    page_type: str,
    title: str,
    description: str,
    tags: list[str],
    aide_uri: str,
    aide_status: str,
    generated_from: list[str],
    source_refs: list[str],
    repo_root: Path,
    evidence_refs: list[str] | None = None,
    report_refs: list[str] | None = None,
    event_refs: list[str] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    fields: dict[str, Any] = {
        "type": page_type,
        "title": title,
        "description": description,
        "resource": aide_uri,
        "tags": tags,
        "timestamp": DETERMINISTIC_TIMESTAMP,
        "aide_uri": aide_uri,
        "aide_status": aide_status,
        "aide_review_state": aide_status,
        "aide_validation_state": "pass_with_warnings" if "warnings" in aide_status else "pass",
        "aide_acceptance_state": aide_status,
        "generated_from": generated_from,
        "source_refs": source_refs,
        "source_hashes": _source_hashes(repo_root, source_refs),
    }
    if evidence_refs:
        fields["evidence_refs"] = evidence_refs
    if report_refs:
        fields["report_refs"] = report_refs
    if event_refs:
        fields["event_refs"] = event_refs
    if extra:
        fields.update(extra)
    return fields


def _protocol_pages(repo_root: Path) -> list[ConceptPage]:
    pages: list[ConceptPage] = []
    for item in PROTOCOLS:
        source_refs = [item["schema_path"], item["helper_path"]]
        body_lines = [
            f"# {item['title']}",
            "",
            AUTHORITY_BOUNDARY,
            "",
            f"{item['title']} is summarized here as an accepted AIDE protocol object with status `{item['status']}`.",
            "This page is explanatory knowledge only. The schema, helper, reports, and queue evidence remain authoritative.",
            "",
            "## Source Authority",
            "",
            f"- Schema: `{item['schema_path']}`",
            f"- Helper: `{item['helper_path']}`",
            f"- Acceptance task: `{item['accept_task']}`",
            "",
            "## Boundary",
            "",
            "- OKF markdown does not execute protocol behavior.",
            "- OKF markdown does not replace protocol schemas or evidence.",
            "- Future runtime concepts remain out of scope unless separately authorized.",
        ]
        if item["slug"] == "event-record":
            body_lines.extend(
                [
                    "",
                    "## EventRecord Status",
                    "",
                    "EventRecord is accepted with warnings as projection-only protocol metadata. It does not append events, create an event store, or replay state.",
                ]
            )
        fields = _standard_fields(
            page_type=item["type"],
            title=item["title"],
            description=f"Projection-only summary for the AIDE {item['title']} protocol object.",
            tags=["aide", "protocol", item["slug"]],
            aide_uri=item["schema_ref"],
            aide_status=item["status"],
            generated_from=[f"aide://queue-task/{item['accept_task']}"],
            source_refs=source_refs,
            repo_root=repo_root,
            evidence_refs=[item["evidence"]],
            report_refs=[item["report"]],
            event_refs=["aide://event/EVT-EVENT-RECORD-PROJECTION"] if item["slug"] == "event-record" else [],
            extra={
                "aide_kind": item["aide_kind"],
                "schema_ref": item["schema_ref"],
                "aide_capability_label": item["capability"],
                "accepted_capability": True,
                "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
            },
        )
        pages.append(ConceptPage(f"protocol/{item['slug']}.md", fields, "\n".join(body_lines)))
    return pages


def _capability_pages(repo_root: Path) -> list[ConceptPage]:
    pages: list[ConceptPage] = []
    for item in PROTOCOLS:
        title = item["capability"]
        rel = {
            "envelope": "minimal-contract-envelope",
            "evidence-packet": "minimal-evidence-packet",
            "workunit": "minimal-workunit-queue",
            "worker-run": "minimal-worker-run-schema",
            "testjob": "minimal-testjob-schema",
            "reference-id": "minimal-reference-id-scheme",
            "event-record": "minimal-event-record-schema",
        }[item["slug"]]
        body = "\n".join(
            [
                f"# {title}",
                "",
                AUTHORITY_BOUNDARY,
                "",
                f"This capability page summarizes `{title}` from queue and report evidence. It does not create or accept capability by itself.",
                "",
                "## Accepted Scope",
                "",
                f"- Accepted status: `{item['status']}`",
                f"- Protocol page: [../protocol/{item['slug']}.md](../protocol/{item['slug']}.md)",
                f"- Acceptance task: `{item['accept_task']}`",
                "",
                "## Explicit Non-Capabilities",
                "",
                "The `explicit_non_capabilities` frontmatter field is the boundary record for this knowledge projection.",
            ]
        )
        fields = _standard_fields(
            page_type="AIDE Capability Summary",
            title=title,
            description=f"Accepted capability summary for {title}.",
            tags=["aide", "capability", item["slug"]],
            aide_uri=f"aide://capability/{title}",
            aide_status=item["status"],
            generated_from=[f"aide://queue-task/{item['accept_task']}"],
            source_refs=[item["schema_path"], item["helper_path"]],
            repo_root=repo_root,
            evidence_refs=[item["evidence"]],
            report_refs=[item["report"]],
            event_refs=["aide://event/EVT-EVENT-RECORD-PROJECTION"] if item["slug"] == "event-record" else [],
            extra={
                "aide_capability_label": title,
                "accepted_capability": True,
                "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
            },
        )
        pages.append(ConceptPage(f"capabilities/{rel}.md", fields, body))
    return pages


def _current_state_pages(repo_root: Path) -> list[ConceptPage]:
    queue_body = "\n".join(
        [
            "# Queue State",
            "",
            AUTHORITY_BOUNDARY,
            "",
            "The filesystem queue under `.aide/queue/` remains canonical for non-trivial AIDE work.",
            "This OKF page summarizes queue state only and links back to the queue index.",
            "",
            "## Current Slice",
            "",
            f"- Current build task: `{TASK_ID}`",
            f"- Accepted predecessor: `{ACCEPTED_PREDECESSOR}`",
            f"- Recommended independent check: `{RECOMMENDED_NEXT_TASK}`",
        ]
    )
    review_body = "\n".join(
        [
            "# Review Gates",
            "",
            AUTHORITY_BOUNDARY,
            "",
            "The OKF build stops at `needs_review`. Review gates continue to live in queue policy and task status files, not in markdown knowledge pages.",
        ]
    )
    stale_body = "\n".join(
        [
            "# Stale Latest Task Packet",
            "",
            AUTHORITY_BOUNDARY,
            "",
            "Observed issue:",
            ".aide/context/latest-task-packet.md may lag .aide/queue/index.yaml.",
            "",
            "Resolution:",
            "Use .aide/queue/index.yaml as canonical queue truth.",
            "",
            "Impact:",
            "Agents relying only on latest-task-packet may receive stale context.",
        ]
    )
    next_body = "\n".join(
        [
            "# Next Work",
            "",
            AUTHORITY_BOUNDARY,
            "",
            f"The only next task recommended by this build slice is `{RECOMMENDED_NEXT_TASK}`.",
            "Do not recommend Reconciler directly from this build task.",
        ]
    )
    common_source = [".aide/queue/index.yaml"]
    pages = [
        ("current-state/queue.md", "AIDE Current State", "Queue truth summary.", "aide://report/okf-queue-state", queue_body),
        ("current-state/review-gates.md", "AIDE Review Gate", "Review-gate summary.", "aide://policy/review-gates", review_body),
        ("current-state/stale-latest-task-packet.md", "AIDE Risk", "Stale latest-task-packet summary.", "aide://artifact/latest-task-packet-staleness", stale_body),
        ("current-state/next-work.md", "AIDE Current State", "Next work summary.", "aide://queue-task/AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01", next_body),
    ]
    result: list[ConceptPage] = []
    for rel, page_type, description, uri, body in pages:
        fields = _standard_fields(
            page_type=page_type,
            title=rel.rsplit("/", 1)[-1].removesuffix(".md").replace("-", " ").title(),
            description=description,
            tags=["aide", "current-state", "okf"],
            aide_uri=uri,
            aide_status="projection_only",
            generated_from=common_source,
            source_refs=common_source,
            repo_root=repo_root,
            extra={"explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES)},
        )
        result.append(ConceptPage(rel, fields, body))
    return result


def _decision_and_risk_pages(repo_root: Path) -> list[ConceptPage]:
    specs = [
        (
            "decisions/protocol-vs-knowledge.md",
            "AIDE Decision",
            "Protocol Vs Knowledge",
            "aide://decision/protocol-vs-knowledge",
            [
                "# Protocol Vs Knowledge",
                "",
                AUTHORITY_BOUNDARY,
                "",
                "Protocol objects, evidence packets, references, and EventRecords remain execution, proof, identity, and event vocabulary truth.",
                "OKF pages explain those sources and must point back to them.",
            ],
        ),
        (
            "decisions/repo-contract-vs-runtime-state.md",
            "AIDE Decision",
            "Repo Contract Vs Runtime State",
            "aide://decision/repo-contract-vs-runtime-state",
            [
                "# Repo Contract Vs Runtime State",
                "",
                "The repository contract is declarative. This OKF slice does not create runtime state, a database, a service, or a scheduler.",
            ],
        ),
        (
            "decisions/okf-as-knowledge-plane.md",
            "AIDE Decision",
            "OKF As Knowledge Plane",
            "aide://decision/okf-as-knowledge-plane",
            [
                "# OKF As Knowledge Plane",
                "",
                "OKF is used here as a deterministic markdown knowledge projection. It is not a platform service and does not execute.",
            ],
        ),
        (
            "risks/stale-latest-task-packet.md",
            "AIDE Risk",
            "Stale Latest Task Packet",
            "aide://artifact/stale-latest-task-packet-risk",
            [
                "# Stale Latest Task Packet",
                "",
                "The latest task packet may lag queue truth. Agents must verify `.aide/queue/index.yaml` and task evidence before acting.",
            ],
        ),
        (
            "risks/acceptance-gate-debt.md",
            "AIDE Risk",
            "Acceptance Gate Debt",
            "aide://artifact/acceptance-gate-debt-risk",
            [
                "# Acceptance Gate Debt",
                "",
                "Many accepted-with-warnings slices stop at review gates. Those warnings remain visible and do not authorize broader runtime work.",
            ],
        ),
        (
            "risks/overclaiming.md",
            "AIDE Risk",
            "Overclaiming",
            "aide://artifact/overclaiming-risk",
            [
                "# Overclaiming",
                "",
                "Knowledge pages must not turn planned runtime concepts into implemented capability claims.",
            ],
        ),
    ]
    pages: list[ConceptPage] = []
    for rel, page_type, title, uri, body_lines in specs:
        normalized_body_lines = list(body_lines)
        if AUTHORITY_BOUNDARY not in normalized_body_lines:
            normalized_body_lines[2:2] = ["", AUTHORITY_BOUNDARY]
        fields = _standard_fields(
            page_type=page_type,
            title=title,
            description=f"{title} summary for the OKF knowledge projection.",
            tags=["aide", "okf", page_type.lower().replace(" ", "-")],
            aide_uri=uri,
            aide_status="projection_only",
            generated_from=[".aide/queue/index.yaml"],
            source_refs=[".aide/queue/index.yaml"],
            repo_root=repo_root,
            extra={"explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES)},
        )
        pages.append(ConceptPage(rel, fields, "\n".join(normalized_body_lines)))
    return pages


def concept_pages(repo_root: str | Path) -> list[ConceptPage]:
    root = Path(repo_root)
    return [
        *_current_state_pages(root),
        *_protocol_pages(root),
        *_capability_pages(root),
        *_decision_and_risk_pages(root),
    ]


def _index_markdown(pages: list[ConceptPage]) -> str:
    lines = [
        "# AIDE OKF Knowledge Bundle",
        "",
        AUTHORITY_BOUNDARY,
        "",
        "This directory is an OKF-compatible markdown bundle generated from current AIDE queue, protocol, evidence, reference, and event records.",
        "It is explanatory projection only.",
        "",
        "## Concepts",
        "",
    ]
    for page in sorted(pages, key=lambda item: item.rel_path):
        title = str(page.fields.get("title", page.rel_path))
        lines.append(f"- [{title}]({page.rel_path})")
    return "\n".join(lines) + "\n"


def _log_markdown() -> str:
    return "\n".join(
        [
            "# AIDE OKF Knowledge Bundle Log",
            "",
            "- 2026-06-17: Generated deterministic OKF-compatible projection for `minimal_okf_knowledge_bundle`.",
            "- Authority boundary preserved: protocol, evidence, references, and events remain source truth.",
        ]
    ) + "\n"


def _bundle_root(repo_root: Path) -> Path:
    return repo_root / BUNDLE_ROOT


def _report_root(repo_root: Path) -> Path:
    return repo_root / REPORT_ROOT


def _all_markdown_files(repo_root: Path) -> list[Path]:
    root = _bundle_root(repo_root)
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def _concept_files(repo_root: Path) -> list[Path]:
    return [path for path in _all_markdown_files(repo_root) if path.name not in RESERVED_FILENAMES]


def _relative(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def build_concept_index(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    concepts: list[dict[str, Any]] = []
    for path in _concept_files(root):
        text = path.read_text(encoding="utf-8")
        fields, _ = parse_frontmatter(text)
        concepts.append(
            {
                "path": _relative(path, root),
                "bundle_path": path.relative_to(_bundle_root(root)).as_posix(),
                "type": fields.get("type", ""),
                "title": fields.get("title", ""),
                "aide_uri": fields.get("aide_uri", ""),
                "aide_status": fields.get("aide_status", ""),
                "tags": fields.get("tags", []),
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "bundle_path": BUNDLE_ROOT.as_posix(),
        "concept_count": len(concepts),
        "concepts": concepts,
    }


LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def build_link_index(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    bundle = _bundle_root(root)
    links: list[dict[str, Any]] = []
    broken: list[dict[str, Any]] = []
    incoming: dict[str, int] = {path.relative_to(bundle).as_posix(): 0 for path in _concept_files(root)}
    for path in _all_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        source_rel = path.relative_to(bundle).as_posix()
        for match in LINK_PATTERN.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "aide://", "#")):
                continue
            target_no_anchor = target.split("#", 1)[0]
            resolved = (path.parent / target_no_anchor).resolve()
            try:
                target_rel = resolved.relative_to(bundle.resolve()).as_posix()
            except ValueError:
                target_rel = target_no_anchor
            exists = (bundle / target_rel).exists() if target_rel else True
            links.append({"source": source_rel, "target": target, "resolved": target_rel, "exists": exists})
            if exists and target_rel in incoming:
                incoming[target_rel] += 1
            if not exists:
                broken.append({"source": source_rel, "target": target, "resolved": target_rel})
    orphan_pages = [{"path": path, "reason": "no incoming markdown links"} for path, count in sorted(incoming.items()) if count == 0]
    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "bundle_path": BUNDLE_ROOT.as_posix(),
        "link_count": len(links),
        "links": links,
        "broken_links": broken,
        "orphan_pages": orphan_pages,
    }


def _source_artifacts() -> list[str]:
    paths = [
        ".aide/queue/index.yaml",
        ".aide/context/latest-task-packet.md",
        ".aide/protocol/aide-envelope.schema.json",
        ".aide/protocol/aide-evidence-packet.schema.json",
        ".aide/protocol/aide-workunit.schema.json",
        ".aide/protocol/aide-worker-run.schema.json",
        ".aide/protocol/aide-test-job.schema.json",
        ".aide/protocol/aide-reference-id.schema.json",
        ".aide/protocol/aide-event-record.schema.json",
        "core/protocol/envelope.py",
        "core/protocol/evidence_packet.py",
        "core/protocol/workunit.py",
        "core/protocol/worker_run.py",
        "core/protocol/test_job.py",
        "core/protocol/reference_id.py",
        "core/protocol/event_record.py",
        ".aide/reports/reference-id/reference-map.json",
        ".aide/reports/event-record/event-family-index.json",
        ".aide/reports/event-record/example-events.json",
        ".aide/reports/event-record-accept/acceptance-report.json",
    ]
    return sorted(set(paths))


def _existing_required_pages(repo_root: Path) -> list[str]:
    return [
        rel
        for rel in ["index.md", "log.md", *REQUIRED_CONCEPT_PATHS]
        if (repo_root / BUNDLE_ROOT / rel).exists()
    ]


def _source_ref_findings(repo_root: Path) -> tuple[list[str], list[str]]:
    missing_source_refs: list[str] = []
    missing_evidence_refs: list[str] = []
    for path in _concept_files(repo_root):
        fields, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        for field_name, sink in [("source_refs", missing_source_refs), ("evidence_refs", missing_evidence_refs)]:
            values = fields.get(field_name, [])
            if not isinstance(values, list):
                continue
            for value in values:
                if isinstance(value, str) and value and not value.startswith("aide://") and not (repo_root / value).exists():
                    sink.append(f"{path.relative_to(repo_root).as_posix()}: {value}")
    return sorted(missing_source_refs), sorted(missing_evidence_refs)


def _aide_ref_findings(repo_root: Path) -> tuple[list[str], list[str]]:
    aide_errors: list[str] = []
    event_errors: list[str] = []
    for path in _concept_files(repo_root):
        fields, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        for key, value in fields.items():
            values = value if isinstance(value, list) else [value]
            for item in values:
                if isinstance(item, str) and item.startswith("aide://"):
                    result = reference_id.validate_reference_id(item, required=True)
                    if not result.valid:
                        aide_errors.extend(f"{path.relative_to(repo_root).as_posix()}:{key}: {error}" for error in result.errors)
                if key == "event_refs" and isinstance(item, str):
                    result = reference_id.validate_reference_id(item, required=True)
                    if not result.valid:
                        event_errors.extend(result.errors)
                    elif result.parsed is not None and result.parsed.kind != "event":
                        event_errors.append(f"event ref must use event kind: {item}")
    return sorted(set(aide_errors)), sorted(set(event_errors))


def _overclaiming_findings(repo_root: Path) -> list[str]:
    findings: list[str] = []
    for path in [*_all_markdown_files(repo_root), *(_report_root(repo_root).glob("*.md") if _report_root(repo_root).exists() else [])]:
        text = path.read_text(encoding="utf-8").lower()
        for pattern in FORBIDDEN_CLAIM_PATTERNS:
            if pattern in text:
                findings.append(f"{path.relative_to(repo_root).as_posix()}: {pattern}")
    return sorted(set(findings))


def lint_okf_bundle(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    link_index = build_link_index(root)
    missing_source_refs, missing_evidence_refs = _source_ref_findings(root)
    stale_context_findings: list[str] = []
    latest_task = root / ".aide/context/latest-task-packet.md"
    if latest_task.exists() and TASK_ID not in latest_task.read_text(encoding="utf-8"):
        stale_context_findings.append(".aide/context/latest-task-packet.md may lag .aide/queue/index.yaml")
    aide_errors, event_errors = _aide_ref_findings(root)
    overclaiming_findings = _overclaiming_findings(root)
    required_missing = [
        rel
        for rel in ["index.md", "log.md", *REQUIRED_CONCEPT_PATHS]
        if not (root / BUNDLE_ROOT / rel).exists()
    ]
    authority_boundary_findings = []
    for page in _concept_files(root):
        text = page.read_text(encoding="utf-8")
        if "OKF knowledge explains" not in text and "protocol_authority_from_markdown" not in text:
            authority_boundary_findings.append(f"{page.relative_to(root).as_posix()}: authority boundary not explicit")
    blocking_findings = [*aide_errors, *event_errors, *overclaiming_findings, *required_missing]
    warnings = [
        *link_index["broken_links"],
        *link_index["orphan_pages"],
        *missing_source_refs,
        *missing_evidence_refs,
        *stale_context_findings,
        FRONTMATTER_WARNING,
    ]
    status = "FAILED_VALIDATION" if blocking_findings else "PASS_WITH_WARNINGS" if warnings else "PASS"
    report = {
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "capability_target": CAPABILITY_TARGET,
        "broken_links": link_index["broken_links"],
        "orphan_pages": link_index["orphan_pages"],
        "missing_source_refs": missing_source_refs,
        "missing_evidence_refs": missing_evidence_refs,
        "stale_context_findings": stale_context_findings,
        "overclaiming_findings": overclaiming_findings,
        "authority_boundary_findings": authority_boundary_findings,
        "aide_ref_findings": aide_errors,
        "event_ref_findings": event_errors,
        "required_missing": required_missing,
        "lint_status": status,
        "warnings": warnings,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
    }
    write_json(root / LINT_JSON, report)
    write_text(root / LINT_MD, render_lint_markdown(report))
    return report


def validate_okf_bundle(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    bundle = _bundle_root(root)
    report_root = _report_root(root)
    concept_errors: list[str] = []
    concept_warnings: list[str] = []
    all_concepts_have_frontmatter = True
    all_concepts_have_non_empty_type = True
    for path in _concept_files(root):
        try:
            fields, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
            result = validate_frontmatter(fields)
            concept_errors.extend(f"{path.relative_to(root).as_posix()}: {error}" for error in result.errors)
            concept_warnings.extend(f"{path.relative_to(root).as_posix()}: {warning}" for warning in result.warnings)
            if not result.valid:
                all_concepts_have_non_empty_type = False
        except ValueError as exc:
            all_concepts_have_frontmatter = False
            all_concepts_have_non_empty_type = False
            concept_errors.append(f"{path.relative_to(root).as_posix()}: {exc}")
    required_pages_exist = all((root / BUNDLE_ROOT / rel).exists() for rel in ["index.md", "log.md", *REQUIRED_CONCEPT_PATHS])
    concept_index = build_concept_index(root) if bundle.exists() else {"concept_count": 0, "concepts": []}
    link_index = build_link_index(root) if bundle.exists() else {"link_count": 0, "links": [], "broken_links": [], "orphan_pages": []}
    write_json(root / CONCEPT_INDEX_JSON, concept_index)
    write_text(root / CONCEPT_INDEX_MD, render_concept_index_markdown(concept_index))
    write_json(root / LINK_INDEX_JSON, link_index)
    write_text(root / LINK_INDEX_MD, render_link_index_markdown(link_index))
    lint_report = lint_okf_bundle(root)
    json_reports_valid = True
    for rel in [PROJECTION_JSON, LINT_JSON, CONCEPT_INDEX_JSON, LINK_INDEX_JSON]:
        path = root / rel
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                json_reports_valid = False
                concept_errors.append(f"invalid JSON report: {rel.as_posix()}")
    aide_ref_errors, event_ref_errors = _aide_ref_findings(root)
    overclaiming_check_passed = not lint_report["overclaiming_findings"]
    forbidden_ops_preserved = True
    blocking = [
        *concept_errors,
        *aide_ref_errors,
        *event_ref_errors,
        *lint_report["required_missing"],
    ]
    if not required_pages_exist:
        blocking.append("required pages missing")
    if not json_reports_valid:
        blocking.append("JSON reports invalid")
    if not overclaiming_check_passed:
        blocking.extend(lint_report["overclaiming_findings"])
    warnings = sorted(set([FRONTMATTER_WARNING, *concept_warnings, *lint_report["warnings"]]))
    status = "FAILED_VALIDATION" if blocking else "PASS_WITH_WARNINGS" if warnings else "PASS"
    report = {
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "capability_target": CAPABILITY_TARGET,
        "helper_exists": (root / "core/knowledge/okf_bundle.py").exists(),
        "cli_registered": _cli_registered(root),
        "bundle_exists": bundle.exists(),
        "index_exists": (bundle / "index.md").exists(),
        "log_exists": (bundle / "log.md").exists(),
        "required_pages_exist": required_pages_exist,
        "required_pages": REQUIRED_CONCEPT_PATHS,
        "concept_index_json_valid": json_reports_valid and (root / CONCEPT_INDEX_JSON).exists(),
        "link_index_json_valid": json_reports_valid and (root / LINK_INDEX_JSON).exists(),
        "all_concepts_have_frontmatter": all_concepts_have_frontmatter,
        "all_concepts_have_non_empty_type": all_concepts_have_non_empty_type,
        "reserved_files_handled": True,
        "aide_refs_parse": not aide_ref_errors,
        "event_refs_parse": not event_ref_errors,
        "source_refs_checked": True,
        "evidence_refs_checked": True,
        "authority_boundary_preserved": not lint_report["authority_boundary_findings"],
        "overclaiming_check_passed": overclaiming_check_passed,
        "forbidden_ops_preserved": forbidden_ops_preserved,
        "frontmatter_validation_mode": FRONTMATTER_MODE,
        "validation_status": status,
        "validation_errors": blocking,
        "warnings": warnings,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "okf_execution_authority": False,
        "protocol_authority_from_markdown": False,
        "evidence_authority_from_markdown": False,
        "runtime_knowledge_service_implemented": False,
        "provider_model_calls": False,
        "network_calls": False,
        "github_mutation": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_markdown(report))
    _write_status(root, report)
    return report


def _cli_registered(repo_root: Path) -> bool:
    script = repo_root / ".aide/scripts/aide_lite.py"
    return script.exists() and "subparsers.add_parser(\"okf\")" in script.read_text(encoding="utf-8")


def project_okf_bundle(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    pages = concept_pages(root)
    source_paths = [root / rel for rel in _source_artifacts() if (root / rel).exists() and (root / rel).is_file()]
    before = {path: _sha256(path) for path in source_paths}
    bundle = _bundle_root(root)
    bundle.mkdir(parents=True, exist_ok=True)
    write_text(bundle / "index.md", _index_markdown(pages))
    write_text(bundle / "log.md", _log_markdown())
    for page in pages:
        write_concept_page(root, page)
    concept_index = build_concept_index(root)
    link_index = build_link_index(root)
    write_json(root / CONCEPT_INDEX_JSON, concept_index)
    write_text(root / CONCEPT_INDEX_MD, render_concept_index_markdown(concept_index))
    write_json(root / LINK_INDEX_JSON, link_index)
    write_text(root / LINK_INDEX_MD, render_link_index_markdown(link_index))
    after = {path: _sha256(path) for path in source_paths}
    source_artifacts_mutated = before != after
    report = {
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "capability_target": CAPABILITY_TARGET,
        "status": "PASS_WITH_WARNINGS",
        "bundle": {
            "path": BUNDLE_ROOT.as_posix(),
            "okf_version_target": OKF_VERSION_TARGET,
            "projection_only": True,
            "execution_authority": False,
        },
        "concepts_count": concept_index["concept_count"],
        "reserved_files": {"index_md": (bundle / "index.md").exists(), "log_md": (bundle / "log.md").exists()},
        "source_artifacts_checked": [_relative(path, root) for path in source_paths],
        "source_artifacts_mutated": source_artifacts_mutated,
        "reports_written": [
            PROJECTION_JSON.as_posix(),
            PROJECTION_MD.as_posix(),
            CONCEPT_INDEX_JSON.as_posix(),
            CONCEPT_INDEX_MD.as_posix(),
            LINK_INDEX_JSON.as_posix(),
            LINK_INDEX_MD.as_posix(),
            FUTURE_WORK_MD.as_posix(),
            UNFINISHED_WORK_MD.as_posix(),
        ],
        "warnings": [
            FRONTMATTER_WARNING,
            "OKF bundle is deterministic knowledge projection only and does not become execution authority.",
            ".aide/context/latest-task-packet.md may lag .aide/queue/index.yaml.",
        ],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "projection_only": True,
        "okf_execution_authority": False,
        "protocol_authority_from_markdown": False,
        "evidence_authority_from_markdown": False,
        "runtime_knowledge_service_implemented": False,
        "provider_model_calls": False,
        "network_calls": False,
        "github_mutation": False,
        "target_mutation": False,
        "active_repo_apply_mutation": False,
        "branch_mutation": False,
    }
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    write_text(root / FUTURE_WORK_MD, render_future_work_markdown())
    write_text(root / UNFINISHED_WORK_MD, render_unfinished_work_markdown())
    validation = validate_okf_bundle(root)
    report["status"] = validation["validation_status"]
    report["reports_written"] = sorted(set([*report["reports_written"], VALIDATION_JSON.as_posix(), VALIDATION_MD.as_posix(), LINT_JSON.as_posix(), LINT_MD.as_posix()]))
    write_json(root / PROJECTION_JSON, report)
    write_text(root / PROJECTION_MD, render_projection_markdown(report))
    _write_status(root, validation)
    return report


def okf_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    bundle = _bundle_root(root)
    concept_count = len(_concept_files(root))
    warnings: list[str] = []
    latest_task = root / ".aide/context/latest-task-packet.md"
    if latest_task.exists() and TASK_ID not in latest_task.read_text(encoding="utf-8"):
        warnings.append(".aide/context/latest-task-packet.md may lag .aide/queue/index.yaml")
    data = {
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "capability_target": CAPABILITY_TARGET,
        "status": "PASS_WITH_WARNINGS" if warnings else "PASS",
        "helper_exists": (root / "core/knowledge/okf_bundle.py").exists(),
        "bundle_exists": bundle.exists(),
        "bundle_path": BUNDLE_ROOT.as_posix(),
        "concept_count": concept_count,
        "warnings": warnings,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "projection_only": True,
        "okf_execution_authority": False,
        "protocol_authority_from_markdown": False,
        "evidence_authority_from_markdown": False,
        "runtime_knowledge_service_implemented": False,
        "provider_model_calls": False,
        "network_calls": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    _write_status(root, data)
    return data


def _write_status(repo_root: Path, data: dict[str, Any]) -> None:
    lines = [
        "# OKF Knowledge Bundle Status",
        "",
        f"- task_id: {TASK_ID}",
        f"- capability_target: {CAPABILITY_TARGET}",
        f"- status: {data.get('validation_status', data.get('status', 'UNKNOWN'))}",
        f"- bundle_path: {BUNDLE_ROOT.as_posix()}",
        f"- concept_count: {data.get('concept_count', data.get('concepts_count', len(_concept_files(repo_root))))}",
        f"- projection_only: {str(data.get('projection_only', True)).lower()}",
        f"- okf_execution_authority: {str(data.get('okf_execution_authority', False)).lower()}",
        f"- runtime_knowledge_service_implemented: {str(data.get('runtime_knowledge_service_implemented', False)).lower()}",
        f"- recommended_next_task: {RECOMMENDED_NEXT_TASK}",
        "",
        "## Explicit Non-Capabilities",
        "",
    ]
    lines.extend(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES)
    write_text(repo_root / STATUS_MD, "\n".join(lines) + "\n")


def render_concept_index_markdown(report: dict[str, Any]) -> str:
    lines = ["# OKF Concept Index", "", f"- concept_count: {report.get('concept_count', 0)}", ""]
    for item in report.get("concepts", []):
        lines.append(f"- `{item['bundle_path']}`: {item.get('type')} - {item.get('title')}")
    return "\n".join(lines) + "\n"


def render_link_index_markdown(report: dict[str, Any]) -> str:
    lines = ["# OKF Link Index", "", f"- link_count: {report.get('link_count', 0)}", ""]
    lines.append("## Broken Links")
    broken = report.get("broken_links", [])
    lines.extend(f"- {item['source']} -> {item['target']}" for item in broken) if broken else lines.append("- none")
    lines.append("")
    lines.append("## Orphan Pages")
    orphans = report.get("orphan_pages", [])
    lines.extend(f"- {item['path']}" for item in orphans) if orphans else lines.append("- none")
    return "\n".join(lines) + "\n"


def render_projection_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# OKF Projection Report",
            "",
            f"- task_id: {TASK_ID}",
            f"- capability_target: {CAPABILITY_TARGET}",
            f"- status: {report.get('status')}",
            f"- bundle_path: {report.get('bundle', {}).get('path')}",
            f"- concepts_count: {report.get('concepts_count')}",
            f"- projection_only: {str(report.get('projection_only', True)).lower()}",
            f"- execution_authority: {str(report.get('okf_execution_authority', False)).lower()}",
            f"- source_artifacts_mutated: {str(report.get('source_artifacts_mutated', False)).lower()}",
            f"- recommended_next_task: {RECOMMENDED_NEXT_TASK}",
            "",
            "## Warnings",
            "",
            *[f"- {warning}" for warning in report.get("warnings", [])],
        ]
    ) + "\n"


def render_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# OKF Validation Report",
        "",
        f"- validation_status: {report.get('validation_status')}",
        f"- helper_exists: {str(report.get('helper_exists', False)).lower()}",
        f"- cli_registered: {str(report.get('cli_registered', False)).lower()}",
        f"- bundle_exists: {str(report.get('bundle_exists', False)).lower()}",
        f"- required_pages_exist: {str(report.get('required_pages_exist', False)).lower()}",
        f"- all_concepts_have_frontmatter: {str(report.get('all_concepts_have_frontmatter', False)).lower()}",
        f"- all_concepts_have_non_empty_type: {str(report.get('all_concepts_have_non_empty_type', False)).lower()}",
        f"- aide_refs_parse: {str(report.get('aide_refs_parse', False)).lower()}",
        f"- event_refs_parse: {str(report.get('event_refs_parse', False)).lower()}",
        f"- overclaiming_check_passed: {str(report.get('overclaiming_check_passed', False)).lower()}",
        f"- forbidden_ops_preserved: {str(report.get('forbidden_ops_preserved', False)).lower()}",
        "",
        "## Validation Errors",
        "",
    ]
    errors = report.get("validation_errors", [])
    lines.extend(f"- {error}" for error in errors) if errors else lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    warnings = report.get("warnings", [])
    lines.extend(f"- {warning}" for warning in warnings) if warnings else lines.append("- none")
    return "\n".join(lines) + "\n"


def render_lint_markdown(report: dict[str, Any]) -> str:
    lines = ["# OKF Lint Report", "", f"- lint_status: {report.get('lint_status')}", ""]
    for section in [
        "broken_links",
        "orphan_pages",
        "missing_source_refs",
        "missing_evidence_refs",
        "stale_context_findings",
        "overclaiming_findings",
        "authority_boundary_findings",
    ]:
        lines.extend([f"## {section}", ""])
        items = report.get(section, [])
        if items:
            for item in items:
                lines.append(f"- {item}")
        else:
            lines.append("- none")
        lines.append("")
    return "\n".join(lines)


def render_future_work_markdown() -> str:
    return "\n".join(
        [
            "# OKF Future Work",
            "",
            f"- Next task: `{RECOMMENDED_NEXT_TASK}`.",
            "- Acceptance must happen before any Reconciler build is recommended.",
            "- Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, and ContextPack v2 remain deferred.",
        ]
    ) + "\n"


def render_unfinished_work_markdown() -> str:
    return "\n".join(
        [
            "# OKF Unfinished Work",
            "",
            "- Full YAML parser integration is deferred; stdlib structural validation is used.",
            "- Broken-link and orphan-page handling is warning-class unless it reveals overclaiming.",
            "- OKF is not execution authority, evidence authority, or protocol truth.",
        ]
    ) + "\n"
