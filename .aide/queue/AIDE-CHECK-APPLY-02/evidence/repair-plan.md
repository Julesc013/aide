# AIDE-APPLY-02-REPAIR-01 Proposal

## Task ID

AIDE-APPLY-02-REPAIR-01

## Goal

Repair the scoped transaction executor v0 issues found by `AIDE-CHECK-APPLY-02` without widening apply capability or modifying protected paths.

## Exact Defects

1. The required example run command fails with `BLOCKED_PREIMAGE_HASH_MISMATCH` because `.aide/examples/apply/scoped-transaction-executor.dry-run.example.json` contains placeholder preimage and postimage hashes.
2. `core/apply/transaction_executor.py` validates paths lexically but does not resolve final target paths to block symlink or reparse-point escape before read/write.
3. Multi-operation apply mode can leave partial mutation if a later write/read or postimage verification fails after earlier writes.
4. Direct core report output can persist a report missing `report_path`.

## Allowed Paths

Use the existing AIDE-APPLY-02 implementation allowlist only, narrowed to:

- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/**`
- `.aide/policies/scoped-transaction-executor.yaml`
- `.aide/apply/scoped-transaction-executor.schema.json`
- `.aide/apply/transaction-executor-report.schema.json`
- `.aide/examples/apply/scoped-transaction-executor.*.example.json`
- `.aide/examples/apply/scoped-transaction-executor-fixtures/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_apply_02_scoped_transaction_executor.py`
- `.aide/reports/scoped-transaction-executor-*.md`
- `.aide/reports/scoped-transaction-executor-*.json`
- `.aide/reports/transaction-*.md`
- `.aide/reports/transaction-*.json`
- `.aide/reports/managed-section-*.md`
- `.aide/reports/managed-section-*.json`
- `.aide/reports/task-os-*.md`
- `.aide/reports/task-os-*.json`
- `docs/reference/scoped-transaction-executor.md`
- `core/apply/README.md`
- `core/apply/__init__.py`
- `core/apply/transaction_executor.py`
- `core/apply/tests/test_transaction_executor.py`

Do not authorize release roots, provider/model/Gateway roots, target repositories, branch/worktree automation, or broad implementation roots.

## Required Validation

- `git diff --check`
- `py -3 -m unittest core.apply.tests.test_transaction_executor`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_apply_02_scoped_transaction_executor.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_apply_0*.py"`
- `py -3 .aide/scripts/aide_lite.py scoped-transaction fixture-plan`
- `py -3 .aide/scripts/aide_lite.py scoped-transaction fixture-verify`
- `py -3 .aide/scripts/aide_lite.py scoped-transaction validate`
- `py -3 .aide/scripts/aide_lite.py scoped-transaction run --plan .aide/examples/apply/scoped-transaction-executor.dry-run.example.json`
- targeted test for symlink or reparse-point escape where platform support permits, otherwise an explicit platform-skip evidence record
- targeted test for multi-operation apply failure behavior
- targeted test that direct core persisted reports include `report_path`
- local secret scan over changed files

## Review Gate

End at `needs_review` and hand back to `AIDE-CHECK-APPLY-02-REPAIR-REVIEW` or an equivalent checkpoint. Do not mark production-ready, release-ready, target-repo capable, install/upgrade/repair/rollback/uninstall capable, or broad active-repo apply capable.
