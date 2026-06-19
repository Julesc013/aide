# CLI Boundary Review

Observed:

- `context-pack-v2 status`: `PASS_WITH_WARNINGS`
- focused tests exercised `status`, `project`, and `validate` in temp workspaces
- unsupported `apply`: fails closed
- unsupported `approve`: fails closed
- unsupported `execute`: fails closed
- unsupported `rollback`: fails closed

The CLI does not implement apply, approval, rollback, execution, provider calls,
network calls, branch/worktree automation, or target mutation.
