# Long-Turn Prompt Template

Use this for a long-running controller turn where the agent may perform several
coherent subtasks while staying inside queue authority.

```text
# <LONG-TURN-ID>

Use this prompt from the repository root.

## Mode

Long-running queue-governed development turn.

## Goal

<bounded goal tied to the current queue or an explicit safe split>

## Required Start

1. Inspect repository state.
2. Read governing documents and active queue records.
3. Compile raw intent first when the prompt is broad, repeated, vague,
   branch-sensitive, publication-sensitive, target-repo-sensitive, destructive,
   install-like, or otherwise risky.
4. Write a short plan before edits.
5. Confirm allowed paths.

## Turn Budget

- maximum commits:
- maximum WorkUnits:
- maximum task families:
- maximum runtime behavior slices:
- docs/evidence/control-only allowance:

## Hard Non-Goals

- no unqueued product work
- no branch mutation without explicit reviewed authority
- no publication action without explicit reviewed authority
- no target-repo mutation without explicit reviewed authority
- no provider/model/Gateway/network calls without explicit reviewed authority
- no external discovery execution inside the AI turn
- no fabricated evidence

## Execution Loop

For each allowed task:

1. Re-read status and evidence.
2. Update the ExecPlan if facts changed.
3. Make one coherent diff.
4. Run focused validation.
5. Write evidence.
6. Commit when queue policy requires it and commit checks pass.
7. Recompute gates before continuing.

## Stop Conditions

Use STOP_CONDITIONS.md.

## Final Report

Use END_OF_TURN_REPORT_FORMAT.md and include actual commands only.
```
