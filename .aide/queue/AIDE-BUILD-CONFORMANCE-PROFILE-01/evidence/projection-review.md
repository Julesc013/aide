# Projection Review

Generated reports under `.aide/reports/conformance-profile/` are deterministic
projections:

- `profiles.json`
- `profile-index.json`
- `case-index.json`
- `projection-report.json`
- `validation.json`

The projection report records:

- status `PASS_WITH_WARNINGS`;
- one profile;
- ten cases;
- eight required cases;
- source-artifact mutation sentinel `false`;
- no result generation;
- no execution;
- no admission;
- next task `AIDE-CHECK-CONFORMANCE-PROFILE-01`.

The generated reports are outputs, not canonical contract truth beyond this queue
task's review boundary.
