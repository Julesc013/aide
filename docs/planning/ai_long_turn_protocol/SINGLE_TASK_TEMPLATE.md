# Single Task Template

Use this for a narrow task that should produce one coherent change set.

```text
# <TASK-ID>

## Mode

Single bounded WorkUnit.

## Goal

<one concrete outcome>

## Required Reading

- AGENTS.md
- .aide/queue/README.md
- .aide/queue/policy.yaml
- .aide/queue/<TASK-ID>/task.yaml
- .aide/queue/<TASK-ID>/ExecPlan.md
- .aide/queue/<TASK-ID>/prompt.md
- .aide/queue/<TASK-ID>/status.yaml

## Allowed Paths

Use the task.yaml allowlist. Do not widen it silently.

## Non-Goals

- <explicit exclusion>
- no branch mutation unless the task explicitly authorizes it
- no target-repo mutation unless the task explicitly authorizes it
- no provider/model/network calls unless the task explicitly authorizes them

## Execution

1. Inspect git status and queue state.
2. Confirm dependencies and allowed paths.
3. Update status to running if the task requires it.
4. Make the smallest coherent diff.
5. Run focused validation.
6. Write task-local evidence.
7. Stop at needs_review when review is required.

## Validation

- git diff --check
- task-specific focused validation
- AIDE Lite validation when proportionate

## Final Report

Use END_OF_TURN_REPORT_FORMAT.md.
```
