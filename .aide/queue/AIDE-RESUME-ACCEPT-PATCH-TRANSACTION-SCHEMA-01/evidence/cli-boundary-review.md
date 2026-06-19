# CLI Boundary Review

PatchTransaction CLI remains limited to:

- `status`;
- `project`;
- `validate`.

Unsupported apply, approve, execute, and rollback operations fail closed.

No CLI command authorizes target mutation, branch/worktree creation, provider or
network calls, GitHub mutation, release, or promotion.
