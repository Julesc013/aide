# Remaining Risks

- RollbackBundle v0 is proposed only. It is not accepted until `AIDE-CHECK-ROLLBACK-BUNDLE-V0-01` and `AIDE-ACCEPT-ROLLBACK-BUNDLE-V0-01` complete.
- Same-session validation is not an independent check.
- The fixture corpus intentionally contains invalid absolute-path, traversal-path, source-latest, authority-claim, and unsafe-ownership cases to prove fail-closed behavior.
- No rollback apply, update apply, install apply, migration apply, uninstall apply, target mutation, release publication, provider/model/network call, canary, UpdateReceipt, or DistributionApplyEngine behavior was started.
