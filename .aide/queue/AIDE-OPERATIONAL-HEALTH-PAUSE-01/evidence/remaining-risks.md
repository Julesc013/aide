# Remaining Risks

The task is complete for review with warning debt:

- task gate state and capability/acceptance state remain hard to read because
  many accepted or completed historical tasks still show `needs_review`;
- ReportIndex ambiguity remains and can make report navigation expensive;
- GeneratedOutputLedger still has unknown-generator records;
- OKF and Reconciler freshness findings remain warning-class;
- ConformanceResult does not execute, admit, trust, or activate anything;
- PatchTransaction is not implemented by this task.

None of these risks blocks a schema-only PatchTransaction build. They must stay
visible in the next task and must not be flattened into product/runtime claims.
