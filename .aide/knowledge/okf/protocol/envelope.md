---
type: "AIDE Protocol Object"
title: "Contract Envelope"
description: "Projection-only summary for the AIDE Contract Envelope protocol object."
resource: "aide://schema/envelope"
tags:
  - "aide"
  - "protocol"
  - "envelope"
timestamp: "2026-06-17T00:00:00+10:00"
aide_uri: "aide://schema/envelope"
aide_kind: "ContractEnvelope"
schema_ref: "aide://schema/envelope"
aide_status: "accepted_with_warnings"
aide_review_state: "accepted_with_warnings"
aide_validation_state: "pass_with_warnings"
aide_acceptance_state: "accepted_with_warnings"
aide_capability_label: "minimal_contract_envelope"
accepted_capability: true
generated_from:
  - "aide://queue-task/AIDE-ACCEPT-CONTRACT-ENVELOPE-01"
source_refs:
  - ".aide/protocol/aide-envelope.schema.json"
  - "core/protocol/envelope.py"
evidence_refs:
  - ".aide/queue/AIDE-ACCEPT-CONTRACT-ENVELOPE-01/evidence/acceptance-review.md"
report_refs:
  - ".aide/reports/contract-envelope-acceptance/acceptance-report.json"
source_hashes:
  - path: ".aide/protocol/aide-envelope.schema.json"
    sha256: "sha256:31c16f5fc57157ea0f118b423446123b7a4751e25cfad9ee07016e50393f54c5"
  - path: "core/protocol/envelope.py"
    sha256: "sha256:cce43f1a5b415c37bf2324721c4fbb907bf1a509189f2e0f6fa49ccbda7c9fa7"
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
# Contract Envelope

Protocol executes. Evidence proves. References identify. Events remember. OKF knowledge explains.

Contract Envelope is summarized here as an accepted AIDE protocol object with status `accepted_with_warnings`.
This page is explanatory knowledge only. The schema, helper, reports, and queue evidence remain authoritative.

## Source Authority

- Schema: `.aide/protocol/aide-envelope.schema.json`
- Helper: `core/protocol/envelope.py`
- Acceptance task: `AIDE-ACCEPT-CONTRACT-ENVELOPE-01`

## Boundary

- OKF markdown does not execute protocol behavior.
- OKF markdown does not replace protocol schemas or evidence.
- Future runtime concepts remain out of scope unless separately authorized.
