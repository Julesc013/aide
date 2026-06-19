# CLI Boundary Review

The supported PatchTransaction commands remain:

- `patch-transaction status`
- `patch-transaction project`
- `patch-transaction validate`

All three returned `PASS_WITH_WARNINGS` before this report set was written.

Unsupported execution-like operations failed closed with argparse exit code `2`:

- `patch-transaction apply`
- `patch-transaction approve`
- `patch-transaction execute`
- `patch-transaction rollback`

No CLI command performed patch application, approval, target mutation, branch or
worktree creation, provider/model/Gateway/network calls, GitHub mutation, release,
or promotion.
