# AIDE Cache Key Report

## CACHE_KEYS

- schema_version: q18.cache-keys.v0
- generated_by: aide-lite q18.cache-local-state-boundary.v0
- contents_inline: false
- raw_prompt_storage: false
- raw_response_storage: false
- git_commit: e249a78041e7b6d236b934a0a39e861653ec09ac
- dirty_state: true

## LOCAL_STATE_BOUNDARY

- committed_contract_root: .aide/
- local_state_root: .aide.local/
- local_state_ignored: true
- tracked_local_state_paths: 0

## SURFACES

- latest_context_packet: `.aide/context/latest-context-packet.md`
  - surface: context_packet
  - key_id: aide-cache-v0:context_packet:c4c85dc44a5af5ab
  - content_sha256: 5420c13a8125dbfdd3ff5c92d81b4aa5ec07f8be790dbd1647bf6bd064dcc026
  - dependency_count: 6
  - dirty_state: true
- latest_golden_tasks_report: `.aide/evals/runs/latest-golden-tasks.json`
  - surface: golden_tasks_report
  - key_id: aide-cache-v0:golden_tasks_report:f5f81f19445c1353
  - content_sha256: 57e16d4528ce8ba304ad7a23d7c0aedb7d5f937d70d9c8391f8de1889af28a14
  - dependency_count: 2
  - dirty_state: true
- latest_review_packet: `.aide/context/latest-review-packet.md`
  - surface: review_packet
  - key_id: aide-cache-v0:review_packet:de9e500d3a781903
  - content_sha256: af8389b2a1627ebad2c9a25bfb4d83d204a05faa3454253867de8b2538c41fbc
  - dependency_count: 4
  - dirty_state: true
- latest_route_decision: `.aide/routing/latest-route-decision.json`
  - surface: route_decision
  - key_id: aide-cache-v0:route_decision:3bf78377a12ec72f
  - content_sha256: 3f57f9e6fa9fb2bc2037a4b305cb0a76fc76658ae1c1637ddfc4edd4312a5fae
  - dependency_count: 6
  - dirty_state: true
- latest_task_packet: `.aide/context/latest-task-packet.md`
  - surface: task_packet
  - key_id: aide-cache-v0:task_packet:aedba03918dff9a8
  - content_sha256: 247d5acf871ef70047a8844f0a0f48e6bbb5064543e3a7a4812099053e41251e
  - dependency_count: 5
  - dirty_state: true
- latest_verification_report: `.aide/verification/latest-verification-report.md`
  - surface: verification_report
  - key_id: aide-cache-v0:verification_report:9df1f7786c0f6d62
  - content_sha256: 0565531eaefe3132db0c4fe9d9de093e19b54cab2e9438e41cf8c60ed11fee21
  - dependency_count: 4
  - dirty_state: true
- token_savings_summary: `.aide/reports/token-savings-summary.md`
  - surface: token_savings_summary
  - key_id: aide-cache-v0:token_savings_summary:ef5cb24ad13dd6e9
  - content_sha256: 35343fdcf4ede94cb475c32d93d438b06b663ff6e1cf2a226c490fcd7d3bb29c
  - dependency_count: 3
  - dirty_state: true

## LIMITS

- Cache keys are deterministic metadata, not permission to reuse stale or unsafe content.
- Cache hits must not bypass verifier, review gates, or golden tasks.
- Provider response and semantic caches remain disabled until future reviewed policy enables them.
- Raw prompts, raw responses, secrets, traces, and real cache blobs must stay out of committed files.
