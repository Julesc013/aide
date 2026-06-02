# Remaining Risks

Task: AIDE-APPLY-00-transaction-model

## Unresolved Or Deferred

- Real apply behavior remains unimplemented and unauthorized.
- Managed-section patching is deferred to AIDE-APPLY-01.
- Rollback execution is deferred; AIDE-APPLY-00 only defines rollback records.
- Transaction validation is structural and fixture-oriented. It does not prove production write safety.
- Target-repository validation remains target-specific and must be generated in each target repository after import.
- `py -3 scripts/aide validate` still reports the known Harness v0 `GENERATED-SOURCE-STALE` warning for `.aide/generated/manifest.yaml`.

## Review Status

The task is intentionally stopped at `needs_review`. No blocked apply behavior should be inferred from this work.
