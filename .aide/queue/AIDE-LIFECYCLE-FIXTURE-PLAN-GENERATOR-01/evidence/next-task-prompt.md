# Next Task Prompt

Task ID: `AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`

Create `AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` as an independent no-apply checkpoint for generated lifecycle fixture plans. Review `.aide/examples/apply/lifecycle-fixtures/generated-plans/**`, `.aide/reports/lifecycle-fixture-plans/**`, and `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` evidence for scenario coverage, lifecycle plan structure, blocker labels, no-apply proof, scoped executor interlock, capability labels, and validation evidence. Do not execute lifecycle apply, scoped transaction apply against fixture targets, install/upgrade/lifecycle repair/rollback/uninstall apply, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. End at `needs_review` with a checkpoint disposition and one next WorkUnit.
