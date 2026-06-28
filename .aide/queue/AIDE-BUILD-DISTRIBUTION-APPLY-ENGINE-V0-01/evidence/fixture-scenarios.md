# Fixture Scenarios

Positive scenarios:

- `no-op-update`
- `managed-file-add`
- `managed-file-update`
- `managed-file-remove`
- `managed-section-add`
- `managed-section-update`
- `managed-section-remove`
- `project-owned-preservation`
- `project-overlay-preservation`
- `local-only-preservation`
- `runtime-generated-preservation`
- `evidence-only-preservation`
- `legacy-preservation`
- `mixed-managed-file-and-section-update`
- `rollback-success`
- `update-receipt-generation`
- `canonical-fixture-unchanged`

Negative scenarios:

- `unknown-ownership-refusal`
- `never-touch-refusal`
- `project-owned-overwrite-refusal`
- `project-overlay-overwrite-refusal`
- `local-only-overwrite-refusal`
- `runtime-generated-overwrite-refusal`
- `evidence-only-overwrite-refusal`
- `absolute-path-refusal`
- `path-traversal-refusal`
- `case-collision-refusal`
- `symlink-reparse-refusal`
- `missing-preimage-refusal`
- `preimage-digest-mismatch-refusal`
- `postimage-digest-mismatch-refusal`
- `missing-rollback-requirement-refusal`
- `operation-not-in-plan-refusal`
- `operation-lacking-rollback-coverage-refusal`
- `unknown-required-feature-refusal`
- `rollback-digest-mismatch-refusal`
- `canonical-fixture-mutation-detection`

All scenarios passed with expected result and refusal code.
