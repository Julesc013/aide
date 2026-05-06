AIDE self-check
mode: report-only
mutation: none
canonical: false
external_calls: none
provider_or_model_calls: none
network_calls: none
automatic_worker_invocation: false
queue_auto_merge: false

validation:
- status: PASS_WITH_WARNINGS
- info: 149
- warning: 6
- error: 0

queue_health:
- Q00-bootstrap-audit: status=needs_review; planning_state=active; review_outcome=none; accepted_for_dependency=no
- Q01-documentation-split: status=needs_review; planning_state=implemented; review_outcome=none; accepted_for_dependency=no
- Q02-structural-skeleton: status=needs_review; planning_state=implemented; review_outcome=none; accepted_for_dependency=no
- Q03-profile-contract-v0: status=needs_review; planning_state=implemented; review_outcome=none; accepted_for_dependency=no
- Q04-harness-v0: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q05-generated-artifacts-v0: status=needs_review; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes-by-review-evidence
- Q06-compatibility-baseline: status=needs_review; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes-by-review-evidence
- Q07-dominium-bridge-baseline: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q08-self-hosting-automation: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q09-token-survival-core: status=needs_review; planning_state=implemented; review_outcome=none; accepted_for_dependency=no

review_gate_nuance:
- Q00-Q03 raw statuses remain needs_review; foundation review evidence allowed later work to proceed with notes.
- Q05 and Q06 raw statuses remain needs_review even though review evidence records PASS_WITH_NOTES.
- Q07 is passed; doctor guidance should no longer point to Q07 review.

generated_artifact_drift:
- source_fingerprint: sha256:1c9e3f3f7fdb544c2982ef1b7f96ae5beef0659d79fc3a6b76ad6ec9550310e5
- manifest_source_fingerprint: current
- manifest_operation_if_compile_write: would_keep (manifest)
- generated_artifacts_refreshed: false

compatibility_smoke:
- baseline_version: aide.compat-baseline.v0
- profile_contract: aide.profile-contract.v0 (current)
- profile: aide.profile.v0 (current)
- toolchain_lock: aide.toolchain-lock.v0 (current)
- queue_index: aide.queue-index.v0 (current)
- queue_policy: aide.queue-policy.v0 (current)
- queue_status: aide.queue-status.v0 (current)
- commands_catalog: aide.commands-catalog.v0 (current)
- compat_schema_versions: aide.compat-schema-versions.v0 (current)
- compatibility_baseline: aide.compat-baseline.v0 (current)
- migration_baseline: aide.migration-baseline.v0 (current-noop)
- replay_corpus: aide.replay-corpus.v0 (current)
- upgrade_gates: aide.upgrade-gates.v0 (current)
- deprecations: aide.deprecations.v0 (current)
- generated_manifest: aide.generated-manifest.v0 (current)
- generated_artifact_generator: q05.generated-artifacts.v0 (current)
- harness_command_surface: aide.harness-command-surface.v0 (current)
- mutating_migrations_available: false

dominium_bridge_status:
- status: structural baseline present
- external_dominium_repo_mutation: prohibited
- real_dominium_outputs_written: false

proposed_followups:
- Q09 token-survival review after this implementation stops at needs_review.
- Reviewed generated-artifact refresh if .aide/generated/manifest.yaml source fingerprint drift remains.
- Queue/status reconciliation QFIX if future automation needs raw statuses to match accepted review evidence.
- Continue to keep Runtime, Service, Commander, Hosts, providers, Gateway, mobile, MCP/A2A, and autonomous loops deferred until reviewed queue items authorize them.

next_recommended_step: Q09-token-survival-core review according to .aide/queue/Q09-token-survival-core/status.yaml
