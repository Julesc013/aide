---
type: "AIDE Protocol Object"
title: "WorkerRun"
description: "Projection-only summary for the AIDE WorkerRun protocol object."
resource: "aide://schema/worker-run"
tags:
  - "aide"
  - "protocol"
  - "worker-run"
timestamp: "2026-06-17T00:00:00+10:00"
aide_uri: "aide://schema/worker-run"
aide_kind: "WorkerRun"
schema_ref: "aide://schema/worker-run"
aide_status: "accepted_with_warnings"
aide_review_state: "accepted_with_warnings"
aide_validation_state: "pass_with_warnings"
aide_acceptance_state: "accepted_with_warnings"
aide_capability_label: "minimal_worker_run_schema"
accepted_capability: true
generated_from:
  - "aide://queue-task/AIDE-ACCEPT-WORKER-RUN-SCHEMA-01"
source_refs:
  - ".aide/protocol/aide-worker-run.schema.json"
  - "core/protocol/worker_run.py"
evidence_refs:
  - ".aide/queue/AIDE-ACCEPT-WORKER-RUN-SCHEMA-01/evidence/acceptance-summary.md"
report_refs:
  - ".aide/reports/worker-run-accept/acceptance-report.json"
source_hashes:
  - path: ".aide/protocol/aide-worker-run.schema.json"
    sha256: "sha256:3b0b6d4e28e70e11cb1b84235964f27187bb28e5ed8722a43fd7f003dbfb14ef"
  - path: "core/protocol/worker_run.py"
    sha256: "sha256:20c9a2be58c1e497be7a105e785260a1479776712495e9a87e4e8619cd013382"
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
# WorkerRun

Protocol executes. Evidence proves. References identify. Events remember. OKF knowledge explains.

WorkerRun is summarized here as an accepted AIDE protocol object with status `accepted_with_warnings`.
This page is explanatory knowledge only. The schema, helper, reports, and queue evidence remain authoritative.

## Source Authority

- Schema: `.aide/protocol/aide-worker-run.schema.json`
- Helper: `core/protocol/worker_run.py`
- Acceptance task: `AIDE-ACCEPT-WORKER-RUN-SCHEMA-01`

## Boundary

- OKF markdown does not execute protocol behavior.
- OKF markdown does not replace protocol schemas or evidence.
- Future runtime concepts remain out of scope unless separately authorized.
