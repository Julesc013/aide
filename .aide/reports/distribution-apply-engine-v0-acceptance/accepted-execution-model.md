# Accepted Execution Model

DistributionApplyEngine v0 is accepted as the first fixture-only executable distribution component.

Accepted behavior:

- validates accepted predecessor context before execution;
- refuses missing or mismatched UpdatePlan, RollbackBundle, predecessor, or accepted-context bindings;
- copies fixture target contents into a temporary workspace;
- executes only bounded fixture operations in the temporary workspace;
- verifies rollback for successful fixture runs;
- emits UpdateReceipt-shaped fixture output for successful fixture runs;
- suppresses successful UpdateReceipt output on refusal;
- verifies canonical fixtures remain unchanged.

Non-accepted behavior:

- no real target apply;
- no source repo apply;
- no public release readiness;
- no project canary mutation;
- no provider/model/network call;
- no branch/worktree automation.
