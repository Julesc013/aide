# Before Routing Text

Before repair, operator-facing commands still exposed build-era routing from DistributionApplyEngine v0:

```text
distribution-apply status
recommended_next_task: AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01
self_consumer_fixture_started: false
```

```text
distribution-apply plan
error: the following arguments are required: --scenario
```

```text
distribution-apply verify
recommended_next_task: AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01
self_consumer_fixture_started: false
material_finding_count: 0
missing_evidence: 0
```

The stale routing was warning-class because accepted non-capability boundary flags remained false.
