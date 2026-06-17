# Next Task Prompt

```text
AIDE-ACCEPT-RECONCILER-REPORTS-01
```

This should be a check-only acceptance review for `AIDE-BUILD-RECONCILER-REPORTS-01` and `AIDE-CHECK-RECONCILER-REPORTS-01`.

Accept only the minimal report-only Reconciler reports if live evidence still supports the check result. Preserve the warnings for stale context, acceptance gate debt, stale generated OKF routing, and OKF source-hash gaps. Do not implement repairs, do not mutate source truth, do not refresh OKF or protocol artifacts, and do not recommend CapabilityManifest unless acceptance explicitly records Reconciler as accepted with warnings and routes to the next build task.

Expected result if evidence remains coherent: `ACCEPTED_WITH_WARNINGS`.
