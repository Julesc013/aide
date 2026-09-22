# Stale Worktree Prune Plan

## Candidate

- Registered path: `D:/Projects/AIDE/aide-screensave-pack`.
- Registration state: prunable; gitdir file points to a non-existent location.
- Recorded detached commit: `492faa4f1a8280ba67954aa4fc252e79f2e19c15`.

## Reachability

The recorded commit exists and is an ancestor of:

- current `HEAD`;
- local `main` and `dev`;
- `origin/main` and `origin/dev`;
- local and remote `task/aide-cw-integration-broker-01`.

It is also named relative to `task/aide-continuous-worker-pilot-01`. Removing
the stale worktree registration cannot make this commit unreachable.

## Authorized Effect

Run `git worktree prune --verbose` only after the same candidate appears in
`git worktree prune --dry-run --verbose`. This removes stale administrative
metadata for the already missing directory. It does not delete a working-tree
directory, branch, tag, commit, remote ref, or working file.

Record refs before and after and fail if the live worktree is not retained.
