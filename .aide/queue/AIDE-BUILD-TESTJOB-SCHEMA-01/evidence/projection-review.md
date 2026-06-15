# Projection Review

Status: PASS.

`test-job project --source accepted-artifacts` wrote 9 additive projections under `.aide/reports/test-job/projections/`.

Source reports checked:

- `.aide/reports/worker-run-accept/acceptance-report.json`
- `.aide/reports/worker-run-check/check-report.json`
- `.aide/reports/worker-run/validation.json`
- `.aide/reports/workunit-cli-mutation-acceptance/acceptance-report.json`
- `.aide/reports/workunit-cli-mutation-check/check-report.json`
- `.aide/reports/workunit-cli-acceptance/acceptance-report.json`
- `.aide/reports/workunit-queue-acceptance/acceptance-report.json`
- `.aide/reports/evidence-packet/validation.json`
- `.aide/reports/contract-envelope/validation.json`

Projection result:

- projections_written: 9
- missing_sources: 0
- source_reports_mutated: false
- target_mutation: false
- active_repo_apply_mutation: false
- branch_mutation: false
- provider_model_calls: false
- gateway_calls: false
- network_calls: false
- github_mutation: false

The projections represent observed existing validation/check/acceptance evidence. They do not execute or submit TestJobs.
