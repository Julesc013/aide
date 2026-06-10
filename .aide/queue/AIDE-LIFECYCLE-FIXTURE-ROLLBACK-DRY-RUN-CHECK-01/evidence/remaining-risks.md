# Remaining Risks

## Non-Blocking Warnings

- The generic rollback-compatible example uses placeholder hashes and remains example-only.
- Rollback records remain static compatibility and fixture evidence only.
- Rollback execution is not implemented or executed.
- Uninstall execution is not implemented or executed.
- Scoped executor v0 does not provide rollback execution, uninstall/delete execution, multi-file atomic apply, active repo apply, or target repo apply.
- Global `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`, so task-local next WorkUnit evidence remains important.
- Deterministic `task-os-*` report refreshes are retained as generated evidence.

## Follow-Up

Run `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01` as the next report-only lifecycle WorkUnit.
