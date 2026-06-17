---
type: "AIDE Protocol Object"
title: "WorkUnit"
description: "Projection-only summary for the AIDE WorkUnit protocol object."
resource: "aide://schema/workunit"
tags:
  - "aide"
  - "protocol"
  - "workunit"
timestamp: "2026-06-17T00:00:00+10:00"
aide_uri: "aide://schema/workunit"
aide_kind: "WorkUnit"
schema_ref: "aide://schema/workunit"
aide_status: "accepted_with_warnings"
aide_review_state: "accepted_with_warnings"
aide_validation_state: "pass_with_warnings"
aide_acceptance_state: "accepted_with_warnings"
aide_capability_label: "minimal_workunit_queue_v1"
accepted_capability: true
generated_from:
  - "aide://queue-task/AIDE-ACCEPT-WORKUNIT-QUEUE-V1-01"
source_refs:
  - ".aide/protocol/aide-workunit.schema.json"
  - "core/protocol/workunit.py"
evidence_refs:
  - ".aide/queue/AIDE-ACCEPT-WORKUNIT-QUEUE-V1-01/evidence/acceptance-review.md"
report_refs:
  - ".aide/reports/workunit-queue-acceptance/acceptance-report.json"
source_hashes:
  - path: ".aide/protocol/aide-workunit.schema.json"
    sha256: "sha256:de82b312e2859191d8dac4153f25ae29237d1e4065a5d4a9837ea52d95dab964"
  - path: "core/protocol/workunit.py"
    sha256: "sha256:f4a74b2d54552244bf1657cbeaad80b164a8bb57e37fb8c388677484086e0311"
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
# WorkUnit

Protocol executes. Evidence proves. References identify. Events remember. OKF knowledge explains.

WorkUnit is summarized here as an accepted AIDE protocol object with status `accepted_with_warnings`.
This page is explanatory knowledge only. The schema, helper, reports, and queue evidence remain authoritative.

## Source Authority

- Schema: `.aide/protocol/aide-workunit.schema.json`
- Helper: `core/protocol/workunit.py`
- Acceptance task: `AIDE-ACCEPT-WORKUNIT-QUEUE-V1-01`

## Boundary

- OKF markdown does not execute protocol behavior.
- OKF markdown does not replace protocol schemas or evidence.
- Future runtime concepts remain out of scope unless separately authorized.
