# Routing Comparison

Before source: `.aide/reports/distribution-apply-routing-text-repair/routing-before.md`.

Before repair:

```text
distribution-apply status -> AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01
distribution-apply verify -> AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01
distribution-apply plan -> required --scenario
self_consumer_fixture_started: false
```

After source: independent command runs in this check.

After repair:

```text
distribution-apply status -> AIDE-BUILD-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01
distribution-apply plan -> AIDE-BUILD-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01
distribution-apply verify -> AIDE-BUILD-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01
accepted_fixture_capability: aide_self_consumer_fixture_v0
self_consumer_fixture_started: true
```

The stale build-era routing is no longer visible in status, plan, or verify output.
