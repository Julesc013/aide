# Changed Files

- `.aide/scripts/aide_lite.py` - added local `lifecycle-schema` status, validate, and fixture-verify commands plus stdlib structural validator helpers.
- `.aide/scripts/tests/test_aide_lifecycle_schema_validator.py` - added focused positive and negative tests for lifecycle schema validation.
- `.aide/reports/lifecycle-schema-status.json` - generated lifecycle schema validator status report.
- `.aide/reports/lifecycle-schema-status.md` - generated lifecycle schema validator status report.
- `.aide/reports/lifecycle-schema-validation.json` - generated lifecycle schema validation report.
- `.aide/reports/lifecycle-schema-validation.md` - generated lifecycle schema validation report.
- `.aide/reports/lifecycle-schema-fixture-validation.json` - generated lifecycle fixture-shape validation report.
- `.aide/reports/lifecycle-schema-fixture-validation.md` - generated lifecycle fixture-shape validation report.
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/**` - task metadata, ExecPlan, status, next batch, validation matrix, and evidence.
- `.aide/queue/index.yaml` - indexed this validator task.
- `.aide/context/latest-task-packet.md` - updated latest task packet to the validator task.
- `README.md` - updated next AIDE-local work summary.
- `docs/reference/apply-lifecycle-schemas.md` - documented local validator command surface.
- deterministic generated status reports under `.aide/reports/task-os-*`, `.aide/reports/scoped-transaction-executor-*`, `.aide/reports/managed-section-*`, `.aide/reports/transaction-*`, and `.aide/reports/current-aide-roadmap.md` - refreshed by required preflight/status commands.
