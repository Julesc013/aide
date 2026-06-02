# AIDE-APPLY-00 Readiness

## Classification

PARTIAL_NEEDS_REPAIR.

## Can AIDE-APPLY-00 Start?

Not yet. AIDE-APPLY-00 should wait for `AIDE-FIX-OS-03 - Task OS checkpoint report consistency repair`.

## Required AIDE-APPLY-00 Scope

- transaction schemas
- file operation schemas
- rollback record schemas
- transaction policy
- stage/verify/report-only or fixture-only transaction planner
- validation and golden tasks for no-apply transaction planning

## Forbidden AIDE-APPLY-00 Scope

- install apply
- repair apply
- upgrade apply
- rollback/uninstall apply
- target repo mutation
- branch creation, worktree creation, merge, push, promotion
- release publication, tags, uploads, GitHub API mutation
- provider/model/network calls
- Gateway forwarding
- task scheduler or autonomous loop

## Apply Still Forbidden Until Later

All real file mutations outside fixtures, target installs, target repairs, upgrades, rollbacks, uninstalls, branch/worktree automation, and publication remain forbidden until separately reviewed queue phases authorize them.

## Validation Commands For AIDE-APPLY-00

- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py eval run`
- transaction model validator commands added by AIDE-APPLY-00
- no-apply golden tasks
- targeted secret scan
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## Acceptance Criteria For AIDE-APPLY-00

- Transaction contracts exist and validate.
- Planner outputs are report-only or fixture-only.
- No apply behavior is implemented outside explicitly allowed fixtures.
- Rollback records are modeled, not executed.
- Generated reports do not claim live target mutation.
- No no-apply/no-live boundary is relaxed.
