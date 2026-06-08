# Prompt Summary

Task ID: `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`

Review rollback-compatible lifecycle fixture record examples and rollback evidence before rollback dry-run, rollback execution, uninstall execution, fixture apply, active repo apply, or target repo apply gates. Verify schema alignment, record links from generated plans and expected reports, preimage/postimage strategy, inverse operations, rollback preconditions, rollback stop conditions, unsupported rollback cases, manual-content preservation, protected path handling, scoped executor interlock, no-rollback-execution proof, capability labels, validation, and evidence.

End with one checkpoint disposition: `ACCEPTED_WITH_NOTES`, `NEEDS_REPAIR`, `REJECTED`, or `BLOCKED`. End at `needs_review`.

Do not implement rollback apply, execute rollback apply, implement or execute uninstall apply, execute lifecycle apply, run scoped transaction apply against fixture targets, mutate fixture target files, mutate active AIDE repo files through scoped transaction apply, mutate external target repos, mutate branches/worktrees, merge, push, promote, publish releases, call GitHub, call providers/models, call Gateway, use network calls, or perform broad active-repo apply.
