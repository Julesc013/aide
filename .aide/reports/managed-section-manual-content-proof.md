# Managed Section Manual Content Proof

- task: AIDE-CHECK-APPLY-01-managed-section-patcher-review
- result: PASS

## Evidence

- Manual content outside markers is policy-defined as user-owned.
- Fixture patch evidence records preimage and postimage content.
- Core tests verify content outside markers is preserved while generated content inside markers changes.
- No active repository files are patched as product behavior.

## Decision

Manual-content preservation is adequate for AIDE-APPLY-02 planning with transaction-level hash and rollback gates.
