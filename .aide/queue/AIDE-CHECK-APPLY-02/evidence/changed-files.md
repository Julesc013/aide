# Changed Files

## Checkpoint Files

- `.aide/queue/AIDE-CHECK-APPLY-02/task.yaml`: checkpoint task metadata, allowed paths, protected paths, forbidden operations, and disposition.
- `.aide/queue/AIDE-CHECK-APPLY-02/ExecPlan.md`: restartable checkpoint execution plan.
- `.aide/queue/AIDE-CHECK-APPLY-02/prompt.md`: bounded review prompt seed.
- `.aide/queue/AIDE-CHECK-APPLY-02/status.yaml`: checkpoint status and capability reality.
- `.aide/queue/AIDE-CHECK-APPLY-02/review.md`: review decision and findings.
- `.aide/queue/AIDE-CHECK-APPLY-02/checkpoint.md`: checkpoint summary and repair handoff.
- `.aide/queue/AIDE-CHECK-APPLY-02/evidence/changed-files.md`: this changed-file record.
- `.aide/queue/AIDE-CHECK-APPLY-02/evidence/validation.md`: validation command log.
- `.aide/queue/AIDE-CHECK-APPLY-02/evidence/static-review.md`: static review details.
- `.aide/queue/AIDE-CHECK-APPLY-02/evidence/boundary-review.md`: allowed/protected/forbidden boundary review.
- `.aide/queue/AIDE-CHECK-APPLY-02/evidence/capability-reality.md`: capability label review.
- `.aide/queue/AIDE-CHECK-APPLY-02/evidence/remaining-risks.md`: unresolved risks.
- `.aide/queue/AIDE-CHECK-APPLY-02/evidence/repair-plan.md`: `AIDE-APPLY-02-REPAIR-01` proposal.
- `.aide/queue/AIDE-CHECK-APPLY-02/evidence/secret-scan.md`: local secret scan result.
- `.aide/queue/index.yaml`: adds the checkpoint task to the live queue.

## Generated Report Refreshes

The review commands refreshed deterministic reports under checkpoint-allowed report paths:

- `.aide/reports/current-aide-roadmap.md`
- `.aide/reports/managed-section-*.md`
- `.aide/reports/managed-section-*.json`
- `.aide/reports/scoped-transaction-executor-*.md`
- `.aide/reports/scoped-transaction-executor-*.json`
- `.aide/reports/task-os-*.md`
- `.aide/reports/transaction-*.md`
- `.aide/reports/transaction-*.json`

The failed example-plan validation created blocked-run evidence:

- `.aide/reports/scoped-transaction-executor-example-report.json`
- `.aide/reports/scoped-transaction-executor-example-rollback.json`

## Implementation Files Reviewed But Not Changed

- `core/apply/transaction_executor.py`
- `core/apply/tests/test_transaction_executor.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_apply_02_scoped_transaction_executor.py`
- `.aide/policies/scoped-transaction-executor.yaml`
- `.aide/apply/scoped-transaction-executor.schema.json`
- `.aide/apply/transaction-executor-report.schema.json`
- `.aide/examples/apply/scoped-transaction-executor.dry-run.example.json`
- `docs/reference/scoped-transaction-executor.md`
