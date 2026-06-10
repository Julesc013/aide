# Example Next Turn Prompt

```text
# <TASK-ID>

Use this prompt from the repository root.

## Goal

Advance <one queue item> only.

## Required Reading

- AGENTS.md
- .aide/queue/README.md
- .aide/queue/policy.yaml
- .aide/queue/<TASK-ID>/task.yaml
- .aide/queue/<TASK-ID>/ExecPlan.md
- .aide/queue/<TASK-ID>/prompt.md
- .aide/queue/<TASK-ID>/status.yaml

## Allowed Scope

Use only the task.yaml allowlist.

## Turn Budget

- max commits: 2
- max task families: 1
- stop at review gates

## Validation

- git diff --check
- py -3 .aide/scripts/aide_lite.py task inspect --task-id <TASK-ID>
- py -3 .aide/scripts/aide_lite.py task evidence --task-id <TASK-ID>
- task-specific focused checks

## Stop Conditions

Use docs/planning/ai_long_turn_protocol/STOP_CONDITIONS.md.

## Final Report

Use docs/planning/ai_long_turn_protocol/END_OF_TURN_REPORT_FORMAT.md.
```
