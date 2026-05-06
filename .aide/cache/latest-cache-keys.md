# AIDE Cache Key Report

## CACHE_KEYS

- schema_version: q18.cache-keys.v0
- generated_by: aide-lite q18.cache-local-state-boundary.v0
- contents_inline: false
- raw_prompt_storage: false
- raw_response_storage: false
- git_commit: 37e080492a7984167243a2547adf90c04be15bc3
- dirty_state: true

## LOCAL_STATE_BOUNDARY

- committed_contract_root: .aide/
- local_state_root: .aide.local/
- local_state_ignored: true
- tracked_local_state_paths: 0

## SURFACES

- latest_context_packet: `.aide/context/latest-context-packet.md`
  - surface: context_packet
  - key_id: aide-cache-v0:context_packet:049593b82d5b35dc
  - content_sha256: 6f9af2f5c57cf62474c7d35f0f0d2a0cde77a5651d40f3130d72bcfc8fc5454b
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
  - key_id: aide-cache-v0:review_packet:99972e996e971113
  - content_sha256: 3d4a5b8de45008407dcf088a4f628aa3cffdde12e8ee047465de09926f76b422
  - dependency_count: 4
  - dirty_state: true
- latest_route_decision: `.aide/routing/latest-route-decision.json`
  - surface: route_decision
  - key_id: aide-cache-v0:route_decision:289dc305068ef49f
  - content_sha256: ca567a047fc920c1f42652183fb486c90f6bb4f7663f5beacae025e67d72cee7
  - dependency_count: 6
  - dirty_state: true
- latest_task_packet: `.aide/context/latest-task-packet.md`
  - surface: task_packet
  - key_id: aide-cache-v0:task_packet:f6196eec2cfffefe
  - content_sha256: 247d5acf871ef70047a8844f0a0f48e6bbb5064543e3a7a4812099053e41251e
  - dependency_count: 5
  - dirty_state: true
- latest_verification_report: `.aide/verification/latest-verification-report.md`
  - surface: verification_report
  - key_id: aide-cache-v0:verification_report:0c9477208328b524
  - content_sha256: be25e56927f358a4d2896414c6b10bd09349bccbe02667b35a64c304af13b298
  - dependency_count: 4
  - dirty_state: true
- token_savings_summary: `.aide/reports/token-savings-summary.md`
  - surface: token_savings_summary
  - key_id: aide-cache-v0:token_savings_summary:9ec3ea44b604c626
  - content_sha256: 6545b28e3f451478cc2f4e9b31ffe3d028c58d863afb71c3e9ba754326bb0574
  - dependency_count: 3
  - dirty_state: true

## LIMITS

- Cache keys are deterministic metadata, not permission to reuse stale or unsafe content.
- Cache hits must not bypass verifier, review gates, or golden tasks.
- Provider response and semantic caches remain disabled until future reviewed policy enables them.
- Raw prompts, raw responses, secrets, traces, and real cache blobs must stay out of committed files.
