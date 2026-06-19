# Warning Debt

## Non-Blocking Warnings

- Historical queue review-gate debt remains visible.
- ReportIndex ambiguity remains: 70 ambiguous records out of 479 indexed report
  records.
- GeneratedOutputLedger unknown-generator debt remains: 67 unknown-generator
  records out of 1381 classified generated-output candidates.
- OKF lint reports one stale-context finding.
- Reconciler reports four warning-class findings.
- ConformanceResult remains evidence-projected, runnerless, non-admitting, and
  non-trusting.

## Blocking Findings

None found for a schema-only PatchTransaction build.

## Disposition

The warning debt must be preserved and referenced by PatchTransaction. It does
not require a repair task before defining PatchTransaction as an inspectable,
portable, policy-checkable protocol record with no apply engine.
