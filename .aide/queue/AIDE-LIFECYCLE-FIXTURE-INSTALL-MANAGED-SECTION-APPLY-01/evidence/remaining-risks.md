# Remaining Risks

- First fixture apply proof remains blocked until a reviewed authority task explicitly authorizes exactly one fixture mutation.
- The prompt pack's later checkpoint, rollback dry-run, rollback apply gate, rollback execution, rollback checkpoint, and token/quality ledger tasks cannot be honestly completed as green because the first apply proof did not run.
- `task next-plan` selector lag may persist independently of task-local next-batch selection.
- No production-ready, release-ready, active-repo-capable, target-repo-capable, rollback-executable, or uninstall-executable claim is supported.
