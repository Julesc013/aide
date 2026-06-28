# Accepted Binding Model

The self-consumer fixture relies on accepted `distribution_apply_engine_v0` for executable fixture boundaries.

Accepted binding coverage:

- accepted context binding;
- UpdatePlan binding;
- RollbackBundle binding;
- predecessor-match enforcement;
- UpdateReceipt-shaped fixture output for successful runs;
- refusal behavior for missing or mismatched context;
- suppression of successful receipt output on refusal;
- temp-workspace execution only;
- canonical fixture preservation.

This acceptance does not broaden DistributionApplyEngine beyond its accepted fixture-only and temp-workspace-only behavior.
