# Reconciler Integration Review

Reconciler integration is read-only.

Consumed:

- `.aide/reports/reconciler/findings.json`
- `.aide/reports/reconciler/reconciliation-report.json`
- `.aide/reports/reconciler/validation.json`
- `.aide/reports/reconciler-accept/acceptance-report.json`

Recorded warning findings:

- stale latest-task-packet
- acceptance gate debt
- stale generated OKF routing
- OKF source-hash gaps

No Reconciler repair, source mutation, queue mutation, OKF refresh, or context
packet rewrite was performed.
