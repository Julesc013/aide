# Failure Recovery Rules

Recovery starts from repo state, not chat memory.

## First Checks

1. `git status --short`
2. active queue item and `status.yaml`
3. `ExecPlan.md`
4. task-local evidence
5. latest task and context packets
6. validation reports

## If Work Is Complete

Verify evidence and report `noop_already_complete` or `needs_review` as
appropriate. Do not replay the work.

## If Work Is Partial

Resume only inside the allowlist. Update the ExecPlan with current facts and
record which files were already changed.

## If Generated Drift Appears

Classify it as one of:

- required evidence
- generated report side effect
- unrelated user change
- unknown

Restore only side effects you caused and that are outside the task scope.

## If Validation Fails

Fix only failures local to the current task. Stop when the failure family is
broad, unrelated, or requires scope widening.

## If Manual Input Is Required

Record the exact missing input, why it matters, and the next safe resume point.
