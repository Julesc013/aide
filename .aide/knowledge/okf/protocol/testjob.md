---
type: "AIDE Protocol Object"
title: "TestJob"
description: "Projection-only summary for the AIDE TestJob protocol object."
resource: "aide://schema/test-job"
tags:
  - "aide"
  - "protocol"
  - "testjob"
timestamp: "2026-06-17T00:00:00+10:00"
aide_uri: "aide://schema/test-job"
aide_kind: "TestJob"
schema_ref: "aide://schema/test-job"
aide_status: "accepted_with_warnings"
aide_review_state: "accepted_with_warnings"
aide_validation_state: "pass_with_warnings"
aide_acceptance_state: "accepted_with_warnings"
aide_capability_label: "minimal_test_job_schema"
accepted_capability: true
generated_from:
  - "aide://queue-task/AIDE-ACCEPT-TESTJOB-SCHEMA-01"
source_refs:
  - ".aide/protocol/aide-test-job.schema.json"
  - "core/protocol/test_job.py"
evidence_refs:
  - ".aide/queue/AIDE-ACCEPT-TESTJOB-SCHEMA-01/evidence/acceptance-summary.md"
report_refs:
  - ".aide/reports/test-job-accept/acceptance-report.json"
source_hashes:
  - path: ".aide/protocol/aide-test-job.schema.json"
    sha256: "sha256:2b748472b541ce4c3f5ffb5a423606bfe3b4c3d12003b01eb6a6de5a9c7b52bf"
  - path: "core/protocol/test_job.py"
    sha256: "sha256:6a8e31296c73b1f4ce5c2a598fad5b8efa7621ce76db2f3a84da8398449005d1"
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
# TestJob

Protocol executes. Evidence proves. References identify. Events remember. OKF knowledge explains.

TestJob is summarized here as an accepted AIDE protocol object with status `accepted_with_warnings`.
This page is explanatory knowledge only. The schema, helper, reports, and queue evidence remain authoritative.

## Source Authority

- Schema: `.aide/protocol/aide-test-job.schema.json`
- Helper: `core/protocol/test_job.py`
- Acceptance task: `AIDE-ACCEPT-TESTJOB-SCHEMA-01`

## Boundary

- OKF markdown does not execute protocol behavior.
- OKF markdown does not replace protocol schemas or evidence.
- Future runtime concepts remain out of scope unless separately authorized.
