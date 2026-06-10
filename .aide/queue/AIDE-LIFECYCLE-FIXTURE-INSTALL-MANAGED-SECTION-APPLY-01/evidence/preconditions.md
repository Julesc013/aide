# Preconditions

| Precondition | Result | Evidence |
| --- | --- | --- |
| Worktree clean before task | PASS | `git status --short --branch` reported clean. |
| Upstream gate exists | PASS | `AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01` exists. |
| Upstream gate selected this task | PASS | Gate selected `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01`. |
| Upstream gate authorized apply execution | FAIL | Gate records `apply_authorized_by_this_gate: false`. |
| Selected scenario coherent | PASS | `install-managed-section` plan, expected report, and rollback record exist. |
| Mutation authority present | FAIL | Missing explicit fixture apply authority. |

The task stops before dry-run or apply.
