# Changed Files

## Queue And Evidence

- `.aide/queue/index.yaml` - moves `AIDE-APPLY-02-scoped-transaction-executor-v0` to `needs_review`.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/task.yaml` - records implemented-needs-review task state.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/ExecPlan.md` - records implementation progress, validation, and retrospective.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/status.yaml` - records PASS_WITH_WARNINGS, capability reality, preserved forbidden operations, and handoff to `AIDE-CHECK-APPLY-02`.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/evidence/changed-files.md` - records this implementation file list.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/evidence/implementation-summary.md` - records implementation behavior and capability reality.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/evidence/boundary-confirmation.md` - records allowed-path, protected-path, and forbidden-operation confirmation.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/evidence/validation.md` - records preflight, tests, validation, boundary search, and secret scan.
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/evidence/remaining-risks.md` - records review risks and deferred surfaces.

## Implementation

- `core/apply/transaction_executor.py` - implements scoped transaction executor v0.
- `core/apply/__init__.py` - updates package capability summary without overclaiming broad apply.
- `core/apply/README.md` - documents the scoped executor boundary.
- `core/apply/tests/test_transaction_executor.py` - adds targeted executor tests for dry-run, apply in temp fixtures, path safety, marker conflicts, hashes, records, and capability labels.

## AIDE Lite Command Surface

- `.aide/scripts/aide_lite.py` - adds `scoped-transaction` status, validate, fixture-plan, fixture-verify, and explicit run command support plus validation helpers.
- `.aide/scripts/tests/test_aide_apply_02_scoped_transaction_executor.py` - tests scoped-transaction parser, temp fixture reports, validation, and dry-run run behavior.

## Policy, Schemas, Examples, Fixtures, Docs, Reports

- `.aide/policies/scoped-transaction-executor.yaml` - records operation allowlist, boundaries, forbidden operations, and capability reality.
- `.aide/apply/scoped-transaction-executor.schema.json` - defines scoped transaction plan shape.
- `.aide/apply/transaction-executor-report.schema.json` - defines scoped executor report shape.
- `.aide/examples/apply/scoped-transaction-executor.dry-run.example.json` - records an example dry-run plan.
- `.aide/examples/apply/scoped-transaction-executor-fixtures/valid_input.md` - managed-section fixture input.
- `.aide/examples/apply/scoped-transaction-executor-fixtures/replacement.md` - managed-section replacement fixture.
- `.aide/examples/apply/scoped-transaction-executor-fixtures/expected_output.md` - expected managed-section fixture postimage.
- `.aide/reports/scoped-transaction-executor-status.md` - generated scoped executor status report.
- `.aide/reports/scoped-transaction-executor-fixture-plan.json` - generated deterministic fixture plan.
- `.aide/reports/scoped-transaction-executor-fixture-plan.md` - generated fixture plan summary.
- `.aide/reports/scoped-transaction-executor-fixture-report.json` - generated dry-run fixture report with staged-change and rollback-compatible records.
- `.aide/reports/scoped-transaction-executor-fixture-report.md` - generated fixture report summary.
- `.aide/reports/scoped-transaction-executor-fixture-rollback.json` - generated rollback-compatible record.
- `.aide/reports/scoped-transaction-executor-validation.md` - generated validation report.
- `.aide/reports/managed-section-status.md` - authorized validation report refresh from managed-section commands.
- `.aide/reports/managed-section-next-plan.md` - authorized validation report refresh from managed-section commands.
- `.aide/reports/managed-section-fixture-plan.json` - authorized validation report refresh from managed-section commands.
- `.aide/reports/managed-section-fixture-plan.md` - authorized validation report refresh from managed-section commands.
- `.aide/reports/managed-section-fixture-validation.md` - authorized validation report refresh from managed-section commands.
- `.aide/reports/managed-section-conflict-report.md` - authorized validation report refresh from managed-section commands.
- `.aide/reports/transaction-model-status.md` - authorized validation report refresh from transaction commands.
- `.aide/reports/transaction-next-plan.md` - authorized validation report refresh from transaction commands.
- `.aide/reports/transaction-safety-gates.md` - authorized validation report refresh from transaction commands.
- `.aide/reports/transaction-fixture-plan.json` - authorized validation report refresh from transaction commands.
- `.aide/reports/transaction-fixture-plan.md` - authorized validation report refresh from transaction commands.
- `.aide/reports/transaction-fixture-validation.md` - authorized validation report refresh from transaction commands and validation self-reference fix.
- `.aide/reports/task-os-command-status.md` - authorized validation report refresh from task status commands.
- `.aide/reports/task-os-task-status.md` - authorized validation report refresh from task status commands.
- `docs/reference/scoped-transaction-executor.md` - reference documentation for scoped executor v0 and non-goals.
