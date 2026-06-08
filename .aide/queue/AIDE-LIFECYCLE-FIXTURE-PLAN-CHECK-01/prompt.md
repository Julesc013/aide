# Prompt

Task ID: `AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`

Independently review `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` as a no-apply checkpoint. Verify the 13 generated lifecycle fixture plans, plan index, plan reports, scenario coverage, mutation-state fields, blocker labels, expected report and rollback references, scoped executor interlock, no-apply proof, capability labels, validation evidence, and forbidden-operation boundaries. Create task-local checkpoint evidence, update queue index and latest task packet if authorized, stop at `needs_review`, and select one next safe WorkUnit. Do not implement or execute lifecycle apply, scoped transaction fixture apply, active repo apply, target repo mutation, branch/worktree mutation, release, GitHub, provider/model, Gateway, network, or broad active-repo apply.
