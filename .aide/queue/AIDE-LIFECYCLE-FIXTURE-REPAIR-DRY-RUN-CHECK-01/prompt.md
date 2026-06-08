# Prompt Summary

Task ID: `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`

Review and checkpoint `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` as an independent report-only WorkUnit. Verify generated lifecycle fixture repair dry-run reports for `repair-plan-missing-marker` and `repair-plan-malformed-marker`, generated repair plans, generated plan reports, expected-state README fallback evidence, missing static expected repair report refs, path boundary checks, managed-section marker checks, hash reference checks, drift context, scoped executor interlock, no-apply proof, capability labels, validation, and forbidden-operation boundaries.

End with one checkpoint disposition: `ACCEPTED_WITH_NOTES`, `NEEDS_REPAIR`, `REJECTED`, or `BLOCKED`. End at `needs_review`.

Do not implement lifecycle repair apply, execute lifecycle repair apply, execute lifecycle apply, run scoped transaction apply against fixture targets, mutate fixture target files, mutate active AIDE repo files through scoped transaction apply, mutate external target repos, mutate branches/worktrees, merge, push, promote, publish releases, call GitHub, call providers/models, call Gateway, use network calls, or perform broad active-repo apply.
