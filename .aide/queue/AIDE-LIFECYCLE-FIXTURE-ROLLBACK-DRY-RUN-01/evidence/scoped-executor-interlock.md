# Scoped Executor Interlock

Report: `.aide/reports/lifecycle-fixture-rollback-dry-run/scoped-executor-interlock.json`

Result: `PASS_WITH_NOTES`

Future scoped transaction classes:

- explicit managed-section restore planning;
- explicit generated-file preimage restore planning.

Scoped executor v0 limitations:

- not multi-file atomic apply;
- rollback execution not implemented;
- uninstall/delete execution gap remains;
- active repo apply remains review-gated;
- target repo apply remains unauthorized.

The interlock does not block this report-only rollback dry-run check. It does block acceptance of rollback execution or lifecycle apply execution without a future reviewed queue task.
