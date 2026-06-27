# Remaining Risks

- RollbackBundle v0 is proposed only. It is not accepted until `AIDE-ACCEPT-ROLLBACK-BUNDLE-V0-01` completes.
- Same-session validation is not a fully external independent review.
- The current live projection does not exercise every reverse operation class because it derives from the accepted UpdatePlan source operations; fixtures cover the remaining required classes.
- No rollback apply, update apply, install apply, migration apply, uninstall apply, target mutation, release publication, provider/model/network call, canary, UpdateReceipt, or DistributionApplyEngine behavior was started.
