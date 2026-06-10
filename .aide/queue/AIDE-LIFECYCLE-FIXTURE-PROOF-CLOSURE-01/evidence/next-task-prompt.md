# Next Task Prompt

Create `AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01` as a no-apply evidence repair WorkUnit. Add or repair static expected report refs for `install-clean`, `install-existing-manual-preserved`, `upgrade-manual-preserved`, `repair-plan-missing-marker`, `repair-plan-malformed-marker`, and `uninstall-manual-preserved` using existing generated plan reports and expected-state evidence as inputs.

Do not execute lifecycle apply, install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, scoped transaction apply against fixture targets, fixture target mutation, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. Stop at `needs_review`.
