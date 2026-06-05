# Next Task Prompt Seed

Task ID: `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`

Create `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` as a no-apply WorkUnit that generates lifecycle fixture dry-run/report-only plans from the reviewed static lifecycle fixtures and lifecycle schemas. Do not execute lifecycle apply, scoped transaction apply against fixture targets, install/upgrade/lifecycle repair/rollback/uninstall apply, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. End at `needs_review` with validation evidence and one next WorkUnit.
