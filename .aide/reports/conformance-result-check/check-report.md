# ConformanceResult Check Report

- task_id: AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01
- checked_task_id: AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01
- status: FAILED_VALIDATION
- review_gate: needs_review
- checked_commit_reported: 2bf53e5
- checked_commit_live: 2bf53e5
- result_ref: aide://conformance-result/minimal_capability_manifest-v1.0.0-evidence-projection-01
- profile_ref: aide://conformance-profile/minimal_capability_manifest-v1.0.0
- subject_ref: aide://capability/minimal_capability_manifest
- observation_mode: evidence_projection
- result_lifecycle_state: projected
- results_count: 1
- case_results_count: 10
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

## Finding

The recorded profile digest does not match the raw accepted ConformanceProfile
report payload.

- recorded: `sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8`
- recomputed from `.aide/reports/conformance-profile/profiles.json`:
  `sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d`

The likely cause is in `core/protocol/conformance_result.py`:
`load_accepted_conformance_profile` appends a lifecycle warning to an in-memory
profile copy before `profile_digest` is computed. Validation then recomputes the
same mutated-view digest, so the build validator reports `profile_digest_matches:
true` even though the digest does not bind the raw accepted profile report.

## Passing Checks

- Schema parses and identifies `kind: ConformanceResult`.
- Exactly one projected result exists.
- All 10 profile cases have case results.
- No duplicate case ids were accepted.
- Case refs bind to the expected profile.
- Case evidence refs exist.
- Required case aggregation recomputes to `PASS_WITH_WARNINGS`.
- Result remains evidence-projected.
- Execution, runner, admission, subject admission, and trust remain absent.
- No forbidden runtime, adapter, target, provider, network, Gateway, GitHub,
  branch/worktree, release, or production behavior was found.

## Disposition

This is a material profile-binding defect. The check does not repair it.

Recommended next task:

```text
AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
```
