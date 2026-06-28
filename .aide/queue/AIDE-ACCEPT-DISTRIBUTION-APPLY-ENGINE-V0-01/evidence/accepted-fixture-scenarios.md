# Accepted Fixture Scenarios

Accepted fixture matrix:

- scenario count: `46`
- positive scenarios: `17`
- negative scenarios: `29`

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

Negative scenarios include context-binding refusals, ownership refusals, unsafe path refusals, digest/preimage refusals, rollback coverage refusals, unknown feature refusal, rollback digest mismatch refusal, and canonical fixture mutation detection.
