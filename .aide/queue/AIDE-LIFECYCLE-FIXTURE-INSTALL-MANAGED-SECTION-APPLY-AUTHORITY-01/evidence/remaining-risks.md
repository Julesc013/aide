# Remaining Risks

- The future apply task has not yet executed and may still fail dry-run, preimage validation, postimage validation, or no-extra-mutation checks.
- This authority does not prove rollback execution.
- This authority does not implement general lifecycle apply.
- Active repo apply and target repo apply remain blocked.
- The global `task next-plan` selector may continue to lag behind task-local next-batch records.
