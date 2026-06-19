# Warning Disposition

`PASS_WITH_WARNINGS` is the correct classification.

Non-blocking warning debt:

- review-gate/capability-state split remains difficult for operators;
- ReportIndex ambiguity remains;
- GeneratedOutputLedger unknown-generator records remain;
- OKF stale-context warning remains;
- Reconciler drift findings remain warning-class and report-only;
- ConformanceResult remains runnerless, evidence-projected, non-admitting, and
  non-trusting;
- PatchTransaction is not yet implemented.

No warning found in this pause invalidates accepted predecessor integrity,
makes live queue truth ambiguous, or makes a schema-only PatchTransaction build
unsafe.
