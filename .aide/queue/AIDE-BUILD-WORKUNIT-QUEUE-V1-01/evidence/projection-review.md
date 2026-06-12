# Projection Review

The projection command writes selected queue tasks into `.aide/reports/workunit-queue/projections/`.

Projected source tasks:

- `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01`
- `AIDE-BUILD-CONTRACT-ENVELOPE-01`
- `AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01`
- `AIDE-ACCEPT-EVIDENCE-PACKET-SCHEMA-01`
- `AIDE-BUILD-WORKUNIT-QUEUE-V1-01`

Projection is additive and records source queue task hashes without modifying source task files.

Generated projections:

- `.aide/reports/workunit-queue/projections/lifecycle-fixture-build.workunit.json`
- `.aide/reports/workunit-queue/projections/contract-envelope-build.workunit.json`
- `.aide/reports/workunit-queue/projections/evidence-packet-build.workunit.json`
- `.aide/reports/workunit-queue/projections/evidence-packet-acceptance.workunit.json`
- `.aide/reports/workunit-queue/projections/workunit-queue-build.workunit.json`

Projection report:

- path: `.aide/reports/workunit-queue/projection-report.json`
- status: PASS
- source_queue_tasks_mutated: false
- destructive_migration_performed: false
- target_mutation: false
- active_repo_apply_mutation: false
- branch_mutation: false
- provider/model/network/Gateway calls: false
