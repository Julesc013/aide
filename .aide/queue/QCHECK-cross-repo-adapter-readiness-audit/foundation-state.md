# Foundation State

## QFIX-01

QFIX-01 reconciled the Q09-Q20 token-survival foundation.

| Item | State |
| --- | --- |
| Q09-Q20 review decisions | `PASS_WITH_NOTES` in task-local `evidence/review.md` files |
| Q09-Q20 queue index state | `passed` |
| Q09-Q20 status files | `status: passed`, review gate `passed_with_notes` |
| Q18 drift | fixed |
| profile focus | no longer Q09-era |
| command catalog | updated for self-check, AIDE Lite, Gateway no-call, provider metadata |
| QFIX-01 status | `needs_review` |

## Remaining Foundation Warnings

- QFIX-01 correctly stopped for review.
- Q09-Q20 are accepted for dependency with limitations, not flawless.
- Token estimates remain approximate.
- Golden tasks prove AIDE substrate behavior, not arbitrary coding work.
- Gateway/provider surfaces remain no-call.
- Generated downstream artifacts remain outputs, not canonical truth.

## Self-Check State

`scripts/aide self-check` no longer points at stale Q09. During this checkpoint
it still produced QFIX-02/Q21-era followup guidance after Q24 was already
implemented. That is a low-risk guidance drift that should be reconciled in the
next state-truth cleanup, but it does not block the pack or adapter commands.

## Queue Truth

QFIX-01, QFIX-02, Q21, and Q24 all remain `needs_review`, which is appropriate
because each phase was instructed to stop at review. Q22 and Q23 are absent from
the AIDE queue and should not be treated as completed based on chat history.
