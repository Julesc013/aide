# ConformanceResult Check Status

- task_id: AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01
- checked_task_id: AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01
- status: FAILED_VALIDATION
- planning_state: failed_validation
- review_gate: needs_review
- result_ref: aide://conformance-result/minimal_capability_manifest-v1.0.0-evidence-projection-01
- profile_ref: aide://conformance-profile/minimal_capability_manifest-v1.0.0
- subject_ref: aide://capability/minimal_capability_manifest
- profile_digest_recorded: sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8
- profile_digest_recomputed_raw_profile: sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d
- profile_digest_matches_raw_profile: false
- record_valid: true
- record_complete: true
- aggregate_outcome: PASS_WITH_WARNINGS
- profile_requirements_satisfied: true
- execution_performed: false
- runner_ref: null
- admission_performed: false
- subject_admitted: false
- trusted: false
- recommended_next_task: AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01

## Findings

- ERROR profile_digest_mismatch: recorded profile digest does not match the raw
  accepted profile payload.

## Blockers

- none
