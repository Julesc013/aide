# Report Consistency Review

Status: `PASS`

Required PatchTransaction build reports exist:

- `status.md`
- `transaction-index.json`
- `transaction-index.md`
- `transactions.json`
- `projection-report.json`
- `projection-report.md`
- `validation.json`
- `validation.md`
- `scope-report.json`
- `scope-report.md`
- `explicit-non-capabilities.md`
- `future-work.md`
- `next-task-prompt.md`
- `sample-unified.diff`

JSON reports parse. Record counts, transaction references, lifecycle state,
artifact digest, scope-valid flag, explicit non-capabilities, and next-task
references are mutually consistent for the build reports.

The check reports do not claim acceptance, apply, admission, trust, runtime,
provider behavior, branch/worktree mutation, target mutation, release, or
promotion.
