# DistributionApply Routing Text Before Repair

Before repair:

- `distribution-apply status` routed to `AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01`.
- `distribution-apply verify` routed to `AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01`.
- `distribution-apply plan` required `--scenario` and did not support the required non-mutating default plan view.
- `self_consumer_fixture_started` printed as `false`.

Boundary flags remained false, so the stale text was warning-class.
