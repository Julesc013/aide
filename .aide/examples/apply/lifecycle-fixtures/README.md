# Lifecycle Fixture Repository

This directory contains static lifecycle fixture inputs and expected states for future report-only and dry-run lifecycle proof tasks.

These files are checked-in fixture artifacts. They were not produced by lifecycle apply execution, scoped transaction apply execution, target repository mutation, branch/worktree mutation, network calls, provider/model calls, Gateway calls, GitHub calls, release publication, or broad active-repo apply.

## Layout

- `source-pack/` contains desired source content for fixture lifecycle planning.
- `target/` contains static target baselines and blocked-case inputs.
- `expected/` contains expected static end states or blocked-state notes.
- `expected-reports/` contains lifecycle report examples for fixture scenarios.
- `rollback-records/` contains rollback-compatible record examples with rollback execution disabled.

All scenarios remain review-gated and planned-only for lifecycle apply.
