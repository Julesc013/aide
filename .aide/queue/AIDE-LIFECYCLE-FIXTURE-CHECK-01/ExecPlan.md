# AIDE-LIFECYCLE-FIXTURE-CHECK-01 ExecPlan

## Purpose

Independently review `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` and decide whether the static lifecycle fixture repository is complete enough for the next no-apply lifecycle WorkUnit.

## Scope

This is a no-apply checkpoint. It may create checkpoint artifacts under `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/**`, update queue routing packets, and retain deterministic reports refreshed by required status commands. It may read materialized fixture files but must not repair them in this task.

## Milestones

1. Verify live preconditions and upstream task evidence.
2. Review fixture inventory, scenario coverage, expected states, expected reports, rollback-compatible records, and hash references.
3. Confirm lifecycle-schema validator interlock and limitations.
4. Confirm no lifecycle apply, scoped transaction fixture apply, active repo apply mutation, target mutation, branch/worktree mutation, provider/model/Gateway/network call, release, or GitHub mutation occurred.
5. Record checkpoint disposition and one safe next WorkUnit.
6. Run validation, commit, and stop at `needs_review`.

## Disposition

`ACCEPTED_WITH_NOTES`: static fixtures are accepted for future dry-run plan generation. This does not authorize lifecycle apply, fixture apply, active repo apply, target repo apply, rollback execution, install/upgrade/repair/uninstall apply, release, provider/model/Gateway/network calls, GitHub mutation, branch/worktree mutation, or broad active-repo apply.
