# Changed Files

## Queue And Context

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/**`: new WorkUnit scaffold, ExecPlan, status, fixture inventory, scenario coverage, next batch, and task-local evidence.
- `.aide/queue/index.yaml`: indexed `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`.
- `.aide/context/latest-task-packet.md`: refreshed latest task packet to the fixture materialization WorkUnit.

## Static Fixture Repository

- `.aide/examples/apply/lifecycle-fixtures/**`: new static lifecycle fixture repository with source pack files, target baselines, expected states, expected reports, rollback-compatible records, fixture index, scenario metadata, and README.

## Reports

- `.aide/reports/lifecycle-fixtures/**`: new fixture materialization and validation reports plus a report-root rollback-compatible record copy.
- `.aide/reports/lifecycle-schema-*.json` and `.aide/reports/lifecycle-schema-*.md`: refreshed by required lifecycle-schema validation commands.
- `.aide/reports/task-os-*.md`, `.aide/reports/scoped-transaction-executor-status.md`, `.aide/reports/managed-section-*.md`, `.aide/reports/transaction-*.md`, and `.aide/reports/current-aide-roadmap.md`: deterministic report refreshes produced by required status/validation commands.

No files outside the task allowed-path packet were intentionally edited.
