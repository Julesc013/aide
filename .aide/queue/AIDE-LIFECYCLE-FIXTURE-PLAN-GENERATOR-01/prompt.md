# Prompt

Task: `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`

Generate no-apply lifecycle fixture dry-run/report-only plans from the reviewed static lifecycle fixture repository and lifecycle schemas.

Do not implement or execute lifecycle apply. Do not execute scoped transaction apply against fixture targets. Do not mutate active repo files through scoped transaction apply. Do not mutate external target repos. Do not mutate branches/worktrees, merge, push, promote, publish releases, call GitHub, call providers/models, call Gateway, use network calls, or perform broad active-repo apply.

End at `needs_review` with generated plan artifacts, validation evidence, no-apply proof, capability reality labels, and one next WorkUnit.
