# Report Consistency Review Evidence

Required PatchTransaction build reports exist and parse where JSON:

- `.aide/reports/patch-transaction/transaction-index.json`
- `.aide/reports/patch-transaction/transactions.json`
- `.aide/reports/patch-transaction/projection-report.json`
- `.aide/reports/patch-transaction/validation.json`
- `.aide/reports/patch-transaction/scope-report.json`

Report counts, transaction refs, lifecycle states, artifact digest, scope flag,
explicit execution facts, explicit non-capabilities, and next-task references
agree.

Check reports were written under `.aide/reports/patch-transaction-check/` and
do not claim acceptance, apply, admission, trust, runtime, provider behavior,
branch/worktree mutation, target mutation, release, or promotion.

Result: `PASS`
