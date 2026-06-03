# AIDE-CHECK-APPLY-02 Checkpoint

## Disposition

NEEDS_REPAIR

## Summary

AIDE-APPLY-02 is implemented, tested, fixture-tested, report-backed, and review-gated. The implementation stayed within authorized paths and preserved forbidden-operation boundaries. The checkpoint found no authority violation and no prohibited operation execution.

The checkpoint does not accept the executor yet because the required checked-in example plan does not pass, and static review identified material repair items for symlink/realpath safety, apply-mode partial mutation handling, and core report self-reference completeness.

## Reviewed Evidence

- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/task.yaml`
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/ExecPlan.md`
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/status.yaml`
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/evidence/**`
- `core/apply/transaction_executor.py`
- `core/apply/tests/test_transaction_executor.py`
- `.aide/scripts/tests/test_aide_apply_02_scoped_transaction_executor.py`
- `.aide/scripts/aide_lite.py`
- `.aide/policies/scoped-transaction-executor.yaml`
- `.aide/apply/scoped-transaction-executor.schema.json`
- `.aide/apply/transaction-executor-report.schema.json`
- `.aide/examples/apply/scoped-transaction-executor.dry-run.example.json`
- `.aide/reports/scoped-transaction-executor-*`

## Repair Handoff

Next task: `AIDE-APPLY-02-REPAIR-01`.

The repair task should keep scope narrow: fix the runnable example/hash evidence mismatch, add resolved-target path safety, address or explicitly bound apply-mode partial mutation risk, ensure direct core reports include `report_path`, and add targeted tests plus evidence for those changes.
