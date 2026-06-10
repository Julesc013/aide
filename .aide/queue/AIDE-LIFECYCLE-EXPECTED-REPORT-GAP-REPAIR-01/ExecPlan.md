# ExecPlan

## Objective

Repair the six static expected-report file gaps identified by `AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01`.

## Scope

Allowed writes are limited to this queue task, `.aide/reports/lifecycle-expected-report-gap-repair/**`, the six expected report files, queue index, latest task packet, and generated validation/status reports.

Generated lifecycle plans and fixture targets are read-only in this WorkUnit. Their embedded `expected_report_ref` fields remain unchanged.

## Plan

1. Add static expected report files for the six missing scenarios.
2. Record a repair summary mapping each scenario to its new report.
3. Validate JSON shape and lifecycle fixture checks.
4. Stop at `needs_review`.

## Result

Six expected report files were added. Static expected report file coverage is complete for the known gap list. A later generator/sync repair may update embedded `expected_report_ref` fields in generated plans if that is desired.
