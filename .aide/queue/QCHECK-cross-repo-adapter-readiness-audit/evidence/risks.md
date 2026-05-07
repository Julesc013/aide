# Audit Risks

- Q22 and Q23 were not present as AIDE queue evidence. The available local
  target repos were inspected read-only and also did not show Q21 pack imports.
- Read-only target inspection depends on the local sibling repos available on
  this machine. It is evidence of this workspace, not remote GitHub truth.
- AIDE command sweeps refreshed generated/report artifacts and therefore made
  the worktree dirty with report outputs before the checkpoint reports were
  written.
- `scripts/aide self-check` no longer recommends stale Q09, but still points at
  earlier QFIX-02/Q21 followups after Q24. This is guidance drift, not a hard
  validation failure.
- Export pack manifest records `source_dirty_state: true` because the audit
  sweep refreshed generated artifacts before `export-pack` was run.
- Secret scan broad matches include policy terms, regex definitions, and test
  fixtures. Strict key-shaped scan found no real key-shaped credentials.
- Token estimates remain chars/4 approximations and do not prove exact provider
  billing savings.
- AIDE substrate quality gates pass, but arbitrary coding-quality preservation
  remains unproven without target task pilots.
