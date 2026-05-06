# AIDE Cache Key Report

## CACHE_KEYS

- schema_version: q18.cache-keys.v0
- generated_by: aide-lite q20.provider-adapter.v0
- contents_inline: false
- raw_prompt_storage: false
- raw_response_storage: false
- git_commit: b92e20885a3eaf9e65617e545b1f0ffa38f5104e
- dirty_state: true

## LOCAL_STATE_BOUNDARY

- committed_contract_root: .aide/
- local_state_root: .aide.local/
- local_state_ignored: true
- tracked_local_state_paths: 0

## SURFACES

- latest_context_packet: `.aide/context/latest-context-packet.md`
  - surface: context_packet
  - key_id: aide-cache-v0:context_packet:f7b1ec40f8bada6a
  - content_sha256: 342ef33a8c2c36ce8ad3b382542dbdf01e815a48fa6c4ca404d8b3d04728fed4
  - dependency_count: 6
  - dirty_state: true
- latest_golden_tasks_report: `.aide/evals/runs/latest-golden-tasks.json`
  - surface: golden_tasks_report
  - key_id: aide-cache-v0:golden_tasks_report:f63c024240a4831d
  - content_sha256: 5753decd946d8843a07d171f36b69ca930702684a5ee728c15df04b2ecbb5ca2
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
  - key_id: aide-cache-v0:review_packet:8cdd02c88e5465db
  - content_sha256: 35b42f1b81871f408044a26de37577cea81e5cb91952619aa436993ab62f4546
  - dependency_count: 4
  - dirty_state: true
- latest_route_decision: `.aide/routing/latest-route-decision.json`
  - surface: route_decision
  - key_id: aide-cache-v0:route_decision:870da1ae0a9ebaa0
  - content_sha256: f77cf64d61354bcd8482359fc1b17118308142da22483530433a61be51429713
  - dependency_count: 6
  - dirty_state: true
- latest_task_packet: `.aide/context/latest-task-packet.md`
  - surface: task_packet
  - key_id: aide-cache-v0:task_packet:b0aa0ff6c25e4f6f
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
  - key_id: aide-cache-v0:token_savings_summary:00d17381ada82c1e
  - content_sha256: 3e438141f05b79ca6b777ddc86c25930a381e8eccb6389b63b6275f2e4be4743
  - dependency_count: 3
  - dirty_state: true

## LIMITS

- Cache keys are deterministic metadata, not permission to reuse stale or unsafe content.
- Cache hits must not bypass verifier, review gates, or golden tasks.
- Provider response and semantic caches remain disabled until future reviewed policy enables them.
- Raw prompts, raw responses, secrets, traces, and real cache blobs must stay out of committed files.
