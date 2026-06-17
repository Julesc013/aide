# Prompt: AIDE-CHECK-EVENT-RECORD-SCHEMA-01

Perform a check-only independent review of `AIDE-BUILD-EVENT-RECORD-SCHEMA-01`.

Do not repair or change the EventRecord implementation. Review the build queue packet, schema, helper, projections, CLI dispatch, reports, tests, predecessor compatibility, source artifact traceability, overclaiming boundaries, forbidden operations, and generated evidence.

Expected result, if live evidence matches, is `PASS_WITH_WARNINGS`.

If the result is `PASS` or `PASS_WITH_WARNINGS`, the next task must be exactly:

```text
AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01
```

Do not recommend OKF directly from this check.
