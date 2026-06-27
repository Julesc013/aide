# Fail-Closed Check

Independent fail-closed probes passed for:

- unknown ownership
- never-touch target
- project-owned overwrite attempt
- project-overlay overwrite attempt
- local-only overwrite attempt
- runtime-generated overwrite attempt
- evidence-only overwrite attempt
- case-fold collision
- symlink/reparse uncertainty
- path traversal
- absolute path
- source distribution mismatch
- project lock mismatch
- ownership ledger mismatch
- install record mismatch
- migration record mismatch
- missing preimage digest
- missing postimage digest where required
- missing rollback requirement
- unknown required feature
- update plan claiming apply authority
- source output as target truth
- target mutation claim

Unknown optional features and extensions were tolerated after recomputing the canonical digest. Unknown required features failed closed.
