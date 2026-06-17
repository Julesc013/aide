---
type: "AIDE Risk"
title: "Stale Latest Task Packet"
description: "Stale latest-task-packet summary."
resource: "aide://artifact/latest-task-packet-staleness"
tags:
  - "aide"
  - "current-state"
  - "okf"
timestamp: "2026-06-17T00:00:00+10:00"
aide_uri: "aide://artifact/latest-task-packet-staleness"
aide_status: "projection_only"
aide_review_state: "projection_only"
aide_validation_state: "pass"
aide_acceptance_state: "projection_only"
generated_from:
  - ".aide/queue/index.yaml"
source_refs:
  - ".aide/queue/index.yaml"
source_hashes:
  - path: ".aide/queue/index.yaml"
    sha256: "sha256:fbb14b1b460d14f898ccca8956963942e545ffc50debb26b23e135bbfdd8e4a3"
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
# Stale Latest Task Packet

Protocol executes. Evidence proves. References identify. Events remember. OKF knowledge explains.

Observed issue:
.aide/context/latest-task-packet.md may lag .aide/queue/index.yaml.

Resolution:
Use .aide/queue/index.yaml as canonical queue truth.

Impact:
Agents relying only on latest-task-packet may receive stale context.
