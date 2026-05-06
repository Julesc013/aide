# AIDE Cache Key Report

## CACHE_KEYS

- schema_version: q18.cache-keys.v0
- generated_by: aide-lite q20.provider-adapter.v0
- contents_inline: false
- raw_prompt_storage: false
- raw_response_storage: false
- git_commit: 84b579ce8e50a38aecad23cd6a7408e3646bd8c9
- dirty_state: true

## LOCAL_STATE_BOUNDARY

- committed_contract_root: .aide/
- local_state_root: .aide.local/
- local_state_ignored: true
- tracked_local_state_paths: 0

## SURFACES

- latest_context_packet: `.aide/context/latest-context-packet.md`
  - surface: context_packet
  - key_id: aide-cache-v0:context_packet:5b7e20965918f555
  - content_sha256: b50586ad5bb3191444234c53570b54750ab71dfb0e5dc3fbf06ff3e89c6d8a99
  - dependency_count: 6
  - dirty_state: true
- latest_golden_tasks_report: `.aide/evals/runs/latest-golden-tasks.json`
  - surface: golden_tasks_report
  - key_id: aide-cache-v0:golden_tasks_report:8b632fd4456882ac
  - content_sha256: 73793a28863a2dc09fccae04ac3d013cf6982364f98a725279a6352dc5d2e0fd
  - dependency_count: 2
  - dirty_state: true
- latest_provider_status: `.aide/providers/latest-provider-status.json`
  - surface: provider_status
  - key_id: aide-cache-v0:provider_status:989bef331f8624c6
  - content_sha256: 3ada3ca08f7f6bc49cc0d170abb252cfca70904c50a1db9082804dc79d5d2025
  - dependency_count: 2
  - dirty_state: true
- latest_review_packet: `.aide/context/latest-review-packet.md`
  - surface: review_packet
  - key_id: aide-cache-v0:review_packet:5b566a2dcd2d3bde
  - content_sha256: e5538e72e9162c7430d6563d7376d743f2a5c26b2bfac46af35002f3395b2d63
  - dependency_count: 4
  - dirty_state: true
- latest_route_decision: `.aide/routing/latest-route-decision.json`
  - surface: route_decision
  - key_id: aide-cache-v0:route_decision:b897cdafb5cc5317
  - content_sha256: 859f6e5e96fe75667c1eda5cebc47828c19cec974f028371dcdea16668a585a7
  - dependency_count: 6
  - dirty_state: true
- latest_task_packet: `.aide/context/latest-task-packet.md`
  - surface: task_packet
  - key_id: aide-cache-v0:task_packet:95208c28e9089082
  - content_sha256: 4baf3305842117ad05e2f72f2b54d2074c73526ba9401cddf21772e41e002c7e
  - dependency_count: 5
  - dirty_state: true
- latest_verification_report: `.aide/verification/latest-verification-report.md`
  - surface: verification_report
  - key_id: aide-cache-v0:verification_report:4870874fa79c6246
  - content_sha256: be25e56927f358a4d2896414c6b10bd09349bccbe02667b35a64c304af13b298
  - dependency_count: 4
  - dirty_state: true
- token_savings_summary: `.aide/reports/token-savings-summary.md`
  - surface: token_savings_summary
  - key_id: aide-cache-v0:token_savings_summary:b26c61abbbdf743b
  - content_sha256: 73d19e6c7c0f9c5e7a3c3928ad93bee71caaee4d90e958f77bd7195323e51d1e
  - dependency_count: 3
  - dirty_state: true

## LIMITS

- Cache keys are deterministic metadata, not permission to reuse stale or unsafe content.
- Cache hits must not bypass verifier, review gates, or golden tasks.
- Provider response and semantic caches remain disabled until future reviewed policy enables them.
- Raw prompts, raw responses, secrets, traces, and real cache blobs must stay out of committed files.
