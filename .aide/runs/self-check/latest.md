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
- info: 148
- warning: 7
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
- Q09-token-survival-core: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q10-aide-lite-hardening: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q11-context-compiler-v0: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q12-verifier-v0: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q13-evidence-review-workflow: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q14-token-ledger-savings-report: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q15-golden-tasks-v0: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q16-outcome-controller-v0: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q17-router-profile-v0: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q18-cache-local-state-boundary: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q19-gateway-architecture-skeleton: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- Q20-provider-adapter-v0: status=passed; planning_state=implemented; review_outcome=PASS_WITH_NOTES; accepted_for_dependency=yes
- QCHECK-token-survival-foundation-audit: status=needs_review; planning_state=review; review_outcome=none; accepted_for_dependency=no
- QFIX-01-foundation-review-reconciliation: status=needs_review; planning_state=review; review_outcome=none; accepted_for_dependency=no

review_gate_nuance:
- Q00-Q03 raw statuses remain needs_review; foundation review evidence allowed later work to proceed with notes.
- Q05 and Q06 raw statuses remain needs_review even though review evidence records PASS_WITH_NOTES.
- Q07 and Q08 are passed with notes.
- Q09-Q20 are accepted with notes as the token-survival foundation, not product readiness.

generated_artifact_drift:
- source_fingerprint: sha256:bc0aca38a44bbc19b4dbaa98516168d1b2cd712e9fbc8fccee251636d2a70792
- manifest_source_fingerprint: stale
- handling: report-only; Q08 does not refresh generated artifacts
- manifest_operation_if_compile_write: would_replace (manifest)
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
- QFIX-02 AIDE Lite Test Discovery and Runner Fix before Q21 export/import work.
- Reviewed generated-artifact refresh if .aide/generated/manifest.yaml source fingerprint drift remains.
- Cross-repo Q21 export/import only after QFIX-02 makes validation routine and discoverable.
- Continue to keep Runtime, Service, Commander, Hosts, live providers, Gateway forwarding, mobile, MCP/A2A, and autonomous loops deferred until reviewed queue items authorize them.

next_recommended_step: QFIX-02 AIDE Lite Test Discovery and Runner Fix after QFIX-01 review; do not proceed to Q21 until test discovery is repaired
