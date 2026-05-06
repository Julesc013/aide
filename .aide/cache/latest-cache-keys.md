# AIDE Cache Key Report

## CACHE_KEYS

- schema_version: q18.cache-keys.v0
- generated_by: aide-lite q19.gateway-skeleton.v0
- contents_inline: false
- raw_prompt_storage: false
- raw_response_storage: false
- git_commit: 961570230e5b7c3d46b3cb172ce6db04f3144ee0
- dirty_state: true

## LOCAL_STATE_BOUNDARY

- committed_contract_root: .aide/
- local_state_root: .aide.local/
- local_state_ignored: true
- tracked_local_state_paths: 0

## SURFACES

- latest_context_packet: `.aide/context/latest-context-packet.md`
  - surface: context_packet
  - key_id: aide-cache-v0:context_packet:671e6472a0693327
  - content_sha256: b11873ca40b83ae1f2071e23e44251b69ffc4a811dfcd714f7bcd0523535baeb
  - dependency_count: 6
  - dirty_state: true
- latest_golden_tasks_report: `.aide/evals/runs/latest-golden-tasks.json`
  - surface: golden_tasks_report
  - key_id: aide-cache-v0:golden_tasks_report:b37d31830da6ac6b
  - content_sha256: 48ab07d102e2a5d9d0085e1671341536f5fdcc80aa414a19bd98f66232b9afc3
  - dependency_count: 2
  - dirty_state: true
- latest_review_packet: `.aide/context/latest-review-packet.md`
  - surface: review_packet
  - key_id: aide-cache-v0:review_packet:953b8c61f22bee61
  - content_sha256: af0459205f6f715859c219ed7e945c0afa13b95bf87b475ec9bc8f63b247978a
  - dependency_count: 4
  - dirty_state: true
- latest_route_decision: `.aide/routing/latest-route-decision.json`
  - surface: route_decision
  - key_id: aide-cache-v0:route_decision:ffcb62d37f4ca948
  - content_sha256: 348d748c6dbaa4a2561a96e6c17be5a165df3c45bd8f96360b5130b91d575245
  - dependency_count: 6
  - dirty_state: true
- latest_task_packet: `.aide/context/latest-task-packet.md`
  - surface: task_packet
  - key_id: aide-cache-v0:task_packet:d736dbf4b12b9b6c
  - content_sha256: 2cf990c856995c2504335da5f60ef92baf5a498da043165292e1a7a88b219b12
  - dependency_count: 5
  - dirty_state: true
- latest_verification_report: `.aide/verification/latest-verification-report.md`
  - surface: verification_report
  - key_id: aide-cache-v0:verification_report:26df1b2612123602
  - content_sha256: be25e56927f358a4d2896414c6b10bd09349bccbe02667b35a64c304af13b298
  - dependency_count: 4
  - dirty_state: true
- token_savings_summary: `.aide/reports/token-savings-summary.md`
  - surface: token_savings_summary
  - key_id: aide-cache-v0:token_savings_summary:24cb72fb7789ce39
  - content_sha256: bc1ae5f5c603ef9043abaf7b6492b4a92f934a19ce564a9a8f1c24697a734600
  - dependency_count: 3
  - dirty_state: true

## LIMITS

- Cache keys are deterministic metadata, not permission to reuse stale or unsafe content.
- Cache hits must not bypass verifier, review gates, or golden tasks.
- Provider response and semantic caches remain disabled until future reviewed policy enables them.
- Raw prompts, raw responses, secrets, traces, and real cache blobs must stay out of committed files.
