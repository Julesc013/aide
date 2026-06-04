# Capability Reality

Task: `AIDE-CHECK-APPLY-02-RECHECK-01`

## Approved Labels

Approved after recheck:

- implemented
- repaired
- tested
- fixture-tested
- report-backed
- review-gated
- accepted-with-notes

Acceptance means the scoped transaction executor v0 is accepted as a reviewed, scoped, fixture-tested apply primitive inside the AIDE core repo boundary.

## Prohibited Labels

Not approved:

- production-ready
- release-ready
- target-repo capable
- install-capable
- upgrade-capable
- repair-apply-capable
- rollback-capable
- rollback/uninstall-capable
- broad active-repo apply capable
- autonomous apply capable
- Gateway capable
- provider/model capable

## Overclaim Review

No material overclaim was found. Status, docs, policy, reports, and evidence preserve `production_ready: false`, `release_ready: false`, `target_repo_capable: false`, and `broad_active_repo_apply: false`.

## Remaining Gates

Lifecycle apply planning, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, and broad active-repo apply all require separate future queue authority.
