# Admission baseline

- 2026-09-25: primary `dev` and `origin/dev` were observed at
  `5dfa75e632b09f732a8150376db6840bcf149ed3`; the primary tree was clean.
- `git plan` reported `ready_dry_run` for branch-sensitive work. Its generated
  four helper reports were restored to their exact prior contents before a
  separate task worktree was created.
- Worktree: `D:/Projects/AIDE/aide-lifecycle-removal-apply`;
  branch: `task/aide-lifecycle-removal-apply-01`.
- Existing `plan-removal` source returns a read-only plan with
  `apply_allowed: false`, `delete_allowed: false`, receipt and observed-state
  digests. This task is the separate actual apply implementation.
- No real target, hosted resource, native effect, main, or public release was
  changed by task admission.
