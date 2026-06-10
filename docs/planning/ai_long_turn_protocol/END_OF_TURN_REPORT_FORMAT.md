# End Of Turn Report Format

Use this format for substantial WorkUnits and long turns.

```text
# <TASK OR TURN ID> Result

## Status

PASS | PASS_WITH_WARNINGS | FAIL | BLOCKED | NEEDS_REVIEW

## Summary

<short factual summary>

## Starting State

- branch:
- starting HEAD:
- worktree:
- queue task:
- allowed paths:
- key gates:

## Work Completed

Grouped by WorkUnit or commit.

## Files Changed

- <path>

## Validation

Actual commands and results only.

## Tests Not Run

List deferred or unavailable checks with the reason.

## Gates

Use GATE_STATUS_TABLE.md.

## Blockers And Deferrals

- <blocker or deferral>

## Risks

- <remaining risk>

## Next Task

Exactly one primary next task or explicit waiting state.

## Sync Recommendation

Report only unless the WorkUnit explicitly authorizes a branch or remote action.
```
