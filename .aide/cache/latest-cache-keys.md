# AIDE Cache Key Report

## CACHE_KEYS

- schema_version: q18.cache-keys.v0
- generated_by: aide-lite q18.cache-local-state-boundary.v0
- contents_inline: false
- raw_prompt_storage: false
- raw_response_storage: false
- git_commit: 6a7ed602706fae044b93cb85cbb21796720953c7
- dirty_state: true

## LOCAL_STATE_BOUNDARY

- committed_contract_root: .aide/
- local_state_root: .aide.local/
- local_state_ignored: true
- tracked_local_state_paths: 0

## SURFACES

- latest_context_packet: `.aide/context/latest-context-packet.md`
  - surface: context_packet
  - key_id: aide-cache-v0:context_packet:797ef764f25124e3
  - content_sha256: 5644b5acebc3bf3d9fba20f65d3b71d95da7145bfd019ec890189a6b4030f70a
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
  - key_id: aide-cache-v0:review_packet:dda5b33e4b1bf7f8
  - content_sha256: fb82cc794f55d1a1d4212bba280b73e252254acee614a35023da8916e7a66088
  - dependency_count: 4
  - dirty_state: true
- latest_route_decision: `.aide/routing/latest-route-decision.json`
  - surface: route_decision
  - key_id: aide-cache-v0:route_decision:afb40fd65f0c1095
  - content_sha256: 1d9bfb480cf367e5f534ea6c006a5413dacf823b47ea37cac79a8834d7aa35bd
  - dependency_count: 6
  - dirty_state: true
- latest_task_packet: `.aide/context/latest-task-packet.md`
  - surface: task_packet
  - key_id: aide-cache-v0:task_packet:76fe3c40566e2da5
  - content_sha256: 27d8209d41329d1dcdaa1a347707ef6907070b905398ce84c0a06fc31f4ef785
  - dependency_count: 5
  - dirty_state: true
- latest_verification_report: `.aide/verification/latest-verification-report.md`
  - surface: verification_report
  - key_id: aide-cache-v0:verification_report:89e49b78ab57141e
  - content_sha256: be25e56927f358a4d2896414c6b10bd09349bccbe02667b35a64c304af13b298
  - dependency_count: 4
  - dirty_state: true
- token_savings_summary: `.aide/reports/token-savings-summary.md`
  - surface: token_savings_summary
  - key_id: aide-cache-v0:token_savings_summary:4769b1989b3f0355
  - content_sha256: 86e745743105595af640bb8dc17788dd99891ca4422e14352c16337225a2f856
  - dependency_count: 3
  - dirty_state: true

## LIMITS

- Cache keys are deterministic metadata, not permission to reuse stale or unsafe content.
- Cache hits must not bypass verifier, review gates, or golden tasks.
- Provider response and semantic caches remain disabled until future reviewed policy enables them.
- Raw prompts, raw responses, secrets, traces, and real cache blobs must stay out of committed files.
