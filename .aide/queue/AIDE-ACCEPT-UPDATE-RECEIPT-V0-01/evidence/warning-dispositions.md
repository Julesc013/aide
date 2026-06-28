# Warning Dispositions

Accepted warnings:

1. UpdateReceipt was proposed until acceptance.
   - Disposition: resolved by this acceptance task for the no-apply receipt contract.
2. Some operation receipt classes and skipped-operation reasons are schema/helper validated but not each represented by a distinct positive fixture row.
   - Disposition: accepted as warning-class. Full enum surfaces are represented and unknown values fail closed; optional future hardening may broaden positive fixture granularity.
3. Check independence occurred on the same local checkout lineage as the build.
   - Disposition: accepted as warning-class because no implementation repair was performed by the check and validation/evidence remained independent in task scope.

No warning authorizes apply behavior, target mutation, release readiness, or DistributionApplyEngine work.
