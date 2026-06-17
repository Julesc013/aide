---
type: "AIDE Protocol Object"
title: "EventRecord"
description: "Projection-only summary for the AIDE EventRecord protocol object."
resource: "aide://schema/event-record"
tags:
  - "aide"
  - "protocol"
  - "event-record"
timestamp: "2026-06-17T00:00:00+10:00"
aide_uri: "aide://schema/event-record"
aide_kind: "EventRecord"
schema_ref: "aide://schema/event-record"
aide_status: "accepted_with_warnings"
aide_review_state: "accepted_with_warnings"
aide_validation_state: "pass_with_warnings"
aide_acceptance_state: "accepted_with_warnings"
aide_capability_label: "minimal_event_record_schema"
accepted_capability: true
generated_from:
  - "aide://queue-task/AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01"
source_refs:
  - ".aide/protocol/aide-event-record.schema.json"
  - "core/protocol/event_record.py"
evidence_refs:
  - ".aide/queue/AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01/evidence/acceptance-summary.md"
report_refs:
  - ".aide/reports/event-record-accept/acceptance-report.json"
event_refs:
  - "aide://event/EVT-EVENT-RECORD-PROJECTION"
source_hashes:
  - path: ".aide/protocol/aide-event-record.schema.json"
    sha256: "sha256:f8f7b9882dcdb4f92a3d281fb9003a44739ccf373cf5ef6c1307ab42736d9698"
  - path: "core/protocol/event_record.py"
    sha256: "sha256:4ed2e1b61d10d52a83e9062539acc4c821ffbc0ad04bd577c52dd42a9f61a4e2"
explicit_non_capabilities:
  - "okf_execution_authority"
  - "protocol_authority_from_markdown"
  - "evidence_authority_from_markdown"
  - "runtime_knowledge_service"
  - "llm_authored_wiki"
  - "network_enrichment"
  - "web_crawling"
  - "provider_model_calls"
  - "search_index_service"
  - "vector_index"
  - "okf_visualizer"
  - "reconciler"
  - "capability_manifest"
  - "conformance_profile"
  - "patch_transaction"
  - "adapter_manifest"
  - "context_pack_v2"
  - "event_sourcing_runtime"
  - "append_only_runtime_store"
  - "runtime_event_log"
  - "state_reconstruction"
  - "scheduler"
  - "leases"
  - "supervisor"
  - "test_broker_runtime"
  - "async_execution"
  - "worker_execution"
  - "service"
  - "commander"
  - "runtime_reference_registry"
  - "resolver_service"
  - "database_state"
  - "provider_adapters"
  - "branch_worktree_automation"
  - "target_apply"
  - "active_apply"
  - "rollback_execution"
  - "uninstall_execution"
  - "release"
  - "promotion"
  - "github_mutation"
  - "gateway_calls"
  - "network_calls"
  - "model_provider_calls"
  - "production_readiness"
  - "release_readiness"
  - "broad_autonomous_runtime"
---
# EventRecord

Protocol executes. Evidence proves. References identify. Events remember. OKF knowledge explains.

EventRecord is summarized here as an accepted AIDE protocol object with status `accepted_with_warnings`.
This page is explanatory knowledge only. The schema, helper, reports, and queue evidence remain authoritative.

## Source Authority

- Schema: `.aide/protocol/aide-event-record.schema.json`
- Helper: `core/protocol/event_record.py`
- Acceptance task: `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01`

## Boundary

- OKF markdown does not execute protocol behavior.
- OKF markdown does not replace protocol schemas or evidence.
- Future runtime concepts remain out of scope unless separately authorized.

## EventRecord Status

EventRecord is accepted with warnings as projection-only protocol metadata. It does not append events, create an event store, or replay state.
