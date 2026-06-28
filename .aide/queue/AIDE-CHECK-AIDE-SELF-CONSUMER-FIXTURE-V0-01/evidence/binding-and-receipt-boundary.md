# Binding And Receipt Boundary

The self-consumer fixture depends on accepted `distribution_apply_engine_v0` for executable fixture behavior.

Verified via DistributionApplyEngine validation:

- accepted context binding remains enforced;
- UpdatePlan binding remains enforced;
- RollbackBundle binding remains enforced;
- predecessor mismatch is refused;
- successful UpdateReceipt-shaped fixture output is emitted only on successful runs;
- refusal paths suppress successful receipt output;
- temp workspace isolation is preserved;
- canonical fixtures remain unchanged after plan/run/verify operations.

This check does not add new apply authority beyond the accepted fixture-only DistributionApplyEngine boundary.
