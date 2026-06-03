# AIDE-APPLY-02 Allowed Paths

This packet defines the future implementation allowed paths for `AIDE-APPLY-02 - Scoped Transaction Executor v0`.

Implementation is authorized only inside these paths:

- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/scoped-transaction-executor.yaml`
- `.aide/apply/scoped-transaction-executor.schema.json`
- `.aide/apply/transaction-executor-report.schema.json`
- `.aide/examples/apply/scoped-transaction-executor.*.example.json`
- `.aide/examples/apply/scoped-transaction-executor-fixtures/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_apply_02_scoped_transaction_executor.py`
- `.aide/evals/golden-tasks/scoped_transaction_executor_*/**`
- `.aide/evals/golden-tasks/catalog.yaml`
- `.aide/evals/runs/latest-golden-tasks.json`
- `.aide/evals/runs/latest-golden-tasks.md`
- `.aide/reports/scoped-transaction-executor-*.md`
- `.aide/reports/scoped-transaction-executor-*.json`
- `.aide/reports/transaction-*.md`
- `.aide/reports/transaction-*.json`
- `.aide/reports/managed-section-*.md`
- `.aide/reports/managed-section-*.json`
- `.aide/reports/task-os-*.md`
- `.aide/reports/task-os-*.json`
- `.aide/reports/capability-*.md`
- `.aide/reports/capability-*.json`
- `.aide/verification/latest-verification-report.md`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/generated/manifest.yaml`
- `docs/reference/scoped-transaction-executor.md`
- `docs/reference/transaction-model.md`
- `docs/reference/transactional-apply-roadmap.md`
- `docs/reference/managed-section-operations.md`
- `core/apply/README.md`
- `core/apply/__init__.py`
- `core/apply/transaction_executor.py`
- `core/apply/tests/test_transaction_executor.py`

## Deliberate Omissions

- Existing transaction schemas such as `.aide/apply/transaction.schema.json` are not authorized for modification in this task.
- Existing managed-section implementation file `core/apply/managed_sections.py` is not authorized for modification in this task.
- Release roots, provider/model roots, Gateway roots, target repositories, branch/worktree automation, and unrelated implementation roots are not authorized.

If implementation needs omitted paths, stop at the `permission_widening` review gate and create a narrow authorization update.
