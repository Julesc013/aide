# ProjectLock v0 Validation

- result: PASS_WITH_WARNINGS
- proposed_capability: project_lock_v0
- recommended_next_task: AIDE-CHECK-PROJECT-LOCK-V0-01

## Checks

- schema_exists: true
- helper_exists: true
- cli_registered: true
- lock_generated: true
- lock_valid: true
- schema_alignment: true
- fixture_matrix_passed: true
- distribution_manifest_accepted: true
- selected_distribution_digest_bound: true
- manifest_payload_digest_bound: true
- component_selection_complete: true
- channel_informational: true
- install_apply_not_implemented: true
- update_apply_not_implemented: true
- target_repository_mutation_not_implemented: true
- admission_not_implemented: true
- authorization_not_implemented: true
- absolute_local_paths_suppressed: true

## Fixture Results

- channel-changed-digest-unchanged: true (PASS)
- extension-round-trip: true (PASS)
- full-valid-lock: true (PASS)
- minimal-valid-lock: true (PASS)
- optional-component-omitted: true (PASS)
- optional-component-selected: true (PASS)
- reordered-deterministic-lock: true (PASS)
- unknown-optional-feature-preserved: true (PASS)
- absolute-path: true (FAILED_VALIDATION)
- aide-local-reference: true (FAILED_VALIDATION)
- channel-changed-unapproved-digest: true (FAILED_VALIDATION)
- component-digest-mismatch: true (FAILED_VALIDATION)
- dependency-cycle: true (FAILED_VALIDATION)
- extension-required-unknown: true (FAILED_VALIDATION)
- manifest-digest-mismatch: true (FAILED_VALIDATION)
- manifest-not-accepted: true (FAILED_VALIDATION)
- manifest-payload-digest-mismatch: true (FAILED_VALIDATION)
- missing-required-component: true (FAILED_VALIDATION)
- optional-component-ambiguous: true (FAILED_VALIDATION)
- secret-like-field: true (FAILED_VALIDATION)
- source-latest-reference: true (FAILED_VALIDATION)
- source-report-reference: true (FAILED_VALIDATION)
- target-overlay-invalid: true (FAILED_VALIDATION)
- traversal-path: true (FAILED_VALIDATION)
- unknown-component: true (FAILED_VALIDATION)
- unknown-required-feature: true (FAILED_VALIDATION)
- unsatisfied-dependency: true (FAILED_VALIDATION)
- unsupported-protocol: true (FAILED_VALIDATION)

## Warnings

- ProjectLock v0 is proposed until independent check and acceptance.
- ProjectLock selects an accepted DistributionManifest but performs no install or target mutation.
