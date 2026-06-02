# Command Surface

Task: AIDE-APPLY-00-transaction-model

## Added Commands

- `py -3 .aide/scripts/aide_lite.py transaction status`
- `py -3 .aide/scripts/aide_lite.py transaction validate`
- `py -3 .aide/scripts/aide_lite.py transaction fixture-plan`
- `py -3 .aide/scripts/aide_lite.py transaction fixture-verify`

## Report Outputs

- `.aide/reports/transaction-model-status.md`
- `.aide/reports/transaction-safety-gates.md`
- `.aide/reports/transaction-fixture-plan.json`
- `.aide/reports/transaction-fixture-plan.md`
- `.aide/reports/transaction-fixture-validation.md`
- `.aide/reports/transaction-next-plan.md`

## Boundary

- No `transaction apply` command exists.
- No transaction command writes outside `.aide/reports/**`.
- No transaction command mutates target repositories, branches, tags, releases, GitHub, providers, models, Gateway, or network state.
- Transaction fixture commands only generate and validate deterministic local reports.
