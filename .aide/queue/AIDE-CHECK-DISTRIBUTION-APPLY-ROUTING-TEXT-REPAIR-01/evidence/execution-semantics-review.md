# Execution Semantics Review

The build repair changed CLI routing text in `.aide/scripts/aide_lite.py` and added a focused regression test.

The check found no evidence that the build changed:

- core DistributionApplyEngine execution;
- accepted-context enforcement;
- UpdatePlan binding;
- RollbackBundle binding;
- UpdateReceipt generation semantics;
- rollback verification;
- fixture corpus generation;
- real target apply behavior;
- source repo apply behavior;
- release behavior;
- canary behavior.

Bare `distribution-apply plan` now renders a non-mutating default plan view for `managed-file-update`. This is operator text/reporting behavior and not apply execution.
