# Projection Review

Result: PASS

| Projection | Source Report | Result |
| --- | --- | --- |
| `.aide/reports/contract-envelope/projections/lifecycle-fixture-latest-run.envelope.json` | `.aide/reports/lifecycle-fixture-runner/latest-run.json` | PASS |
| `.aide/reports/contract-envelope/projections/lifecycle-fixture-verify.envelope.json` | `.aide/reports/lifecycle-fixture-runner/verify.json` | PASS |
| `.aide/reports/contract-envelope/projections/lifecycle-fixture-acceptance.envelope.json` | `.aide/reports/lifecycle-fixture-runner-acceptance/acceptance-report.json` | PASS |

The projections remain additive under `.aide/reports/contract-envelope/` and do
not destructively migrate accepted lifecycle fixture reports.
