# Q28 Remaining Risks

- Q28 is report-only. It does not implement merge, land, promote, prune, push,
  fetch, branch creation, or branch deletion helpers.
- The current AIDE repo has no `dev` branch detected; Q29 or later must decide
  how to apply the `dev/main` policy to live AIDE branches.
- Local detection cannot prove GitHub branch protection, required checks, or
  remote freshness without future reviewed GitHub/CI phases.
- `scripts/aide validate`, `doctor`, and `self-check` still report pre-existing
  wider review-gate/generated-manifest warnings outside Q28's branch-policy
  scope.
- Changelog preview still reports malformed older commits from pre-Q27 history;
  Q27 intentionally reports rather than rewrites old history.
- Export pack provenance records `DIRTY_SOURCE_RECORDED` because Q28 artifacts
  were regenerated before the final evidence commit.
- Q29 must test mutation behavior only in temporary fixture repositories and
  must not mutate live AIDE branches during helper implementation.
- Q35 or a later phase is still needed for GitHub protection and CI advisory or
  application.
