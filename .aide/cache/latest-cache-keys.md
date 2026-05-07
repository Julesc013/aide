# AIDE Cache Key Report

## CACHE_KEYS

- schema_version: q18.cache-keys.v0
- generated_by: aide-lite q24.existing-tool-adapter-compiler.v0
- contents_inline: false
- raw_prompt_storage: false
- raw_response_storage: false
- git_commit: e2088aed6dd32674c00b8d4701ce8c8be784fdde
- dirty_state: true

## LOCAL_STATE_BOUNDARY

- committed_contract_root: .aide/
- local_state_root: .aide.local/
- local_state_ignored: true
- tracked_local_state_paths: 0

## SURFACES

- latest_context_packet: `.aide/context/latest-context-packet.md`
  - surface: context_packet
  - key_id: aide-cache-v0:context_packet:ad2eecd2500bfdf4
  - content_sha256: 879fdc39e4d747e5a690d4450867989fd07b76ba38c79d019e6429c7d4b1c199
  - dependency_count: 6
  - dirty_state: true
- latest_golden_tasks_report: `.aide/evals/runs/latest-golden-tasks.json`
  - surface: golden_tasks_report
  - key_id: aide-cache-v0:golden_tasks_report:5d57665c5a4301df
  - content_sha256: 9fa175a9dfc5cf85ec1d923f2fe69417d049b0825cb51bb394e1d15c9c48bd85
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
  - key_id: aide-cache-v0:review_packet:3ce60134ac0f34b8
  - content_sha256: 12022356d9be4ba6701ec2792fe65a4afa22d9c3219dbbf3059c5b04d0718fc1
  - dependency_count: 4
  - dirty_state: true
- latest_route_decision: `.aide/routing/latest-route-decision.json`
  - surface: route_decision
  - key_id: aide-cache-v0:route_decision:4f4f9dddefa4a571
  - content_sha256: 0f97d8b58be4c6b0ce24f5bd2ed8053b5f7e6dcfd7e6fbca7999cdbc75f2fb84
  - dependency_count: 6
  - dirty_state: true
- latest_task_packet: `.aide/context/latest-task-packet.md`
  - surface: task_packet
  - key_id: aide-cache-v0:task_packet:93918216203611f5
  - content_sha256: b00f7611de5c864e289ce9871c4938efe8c31e711941803f9addf816c20dc980
  - dependency_count: 5
  - dirty_state: true
- latest_verification_report: `.aide/verification/latest-verification-report.md`
  - surface: verification_report
  - key_id: aide-cache-v0:verification_report:436347657947f0ec
  - content_sha256: be25e56927f358a4d2896414c6b10bd09349bccbe02667b35a64c304af13b298
  - dependency_count: 4
  - dirty_state: true
- token_savings_summary: `.aide/reports/token-savings-summary.md`
  - surface: token_savings_summary
  - key_id: aide-cache-v0:token_savings_summary:04649ddf60e7a767
  - content_sha256: fad83c33514da35d0119536d44ed92e012e339ad27c949a9e95adf5714fef52b
  - dependency_count: 3
  - dirty_state: true

## LIMITS

- Cache keys are deterministic metadata, not permission to reuse stale or unsafe content.
- Cache hits must not bypass verifier, review gates, or golden tasks.
- Provider response and semantic caches remain disabled until future reviewed policy enables them.
- Raw prompts, raw responses, secrets, traces, and real cache blobs must stay out of committed files.
