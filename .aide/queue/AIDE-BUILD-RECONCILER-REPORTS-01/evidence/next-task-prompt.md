# Next Task Prompt

```text
AIDE-CHECK-RECONCILER-REPORTS-01
```

This should be an independent check-only review of `AIDE-BUILD-RECONCILER-REPORTS-01`.

Review the report-only Reconciler implementation, finding taxonomy, generated reports, CLI dispatch, tests, evidence, no-repair boundary, no source truth mutation boundary, and no overclaiming boundary.

Do not implement CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime Reconciler service, repair behavior, provider/model/network/Gateway/GitHub behavior, branch/worktree automation, target apply, active apply, release, or promotion.

Expected result is `PASS` or `PASS_WITH_WARNINGS`, stopping at `needs_review`. If the check passes, recommend `AIDE-ACCEPT-RECONCILER-REPORTS-01` next. Do not recommend CapabilityManifest directly from the check unless an acceptance gate has first accepted the Reconciler reports.
