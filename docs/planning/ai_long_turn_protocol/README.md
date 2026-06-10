# AI Long-Turn Operating Protocol

This directory defines a docs-only operating protocol for long-running AIDE and
Codex turns. It is for queue-governed work where a future agent may run for a
long time, make several coherent changes, write evidence, and stop cleanly at
manual or external gates.

The protocol does not authorize runtime work, branch mutation, publication,
target-repo mutation, provider/model calls, Gateway calls, network calls,
external discovery execution, or evidence invention. It gives future prompts a
bounded structure so those actions are either excluded or treated as stop
conditions.

## Use This Protocol When

- A WorkUnit spans multiple files or multiple validation phases.
- The agent may need several commits or a resumable chain of subtasks.
- Manual evidence, external evidence, or review gates may stop progress.
- Final reports must be audit-quality rather than conversational summaries.

## Files

- `SINGLE_TASK_TEMPLATE.md`: one bounded task.
- `CONNECTED_QUEUE_TURN_TEMPLATE.md`: related queue tasks until a stop gate.
- `LONG_TURN_PROMPT_TEMPLATE.md`: long-running controller prompt.
- `MULTI_COMMIT_POLICY.md`: commit cadence and commit boundaries.
- `VALIDATION_LADDER.md`: validation tiers and reporting rules.
- `EXTERNAL_DISCOVERY_POLICY.md`: external discovery boundary.
- `EXTERNAL_ARTIFACT_EVIDENCE_POLICY.md`: manual evidence boundary.
- `STOP_CONDITIONS.md`: conditions that require stopping.
- `GATE_STATUS_TABLE.md`: gate table to fill at start and end.
- `END_OF_TURN_REPORT_FORMAT.md`: final report schema.
- `FAILURE_RECOVERY_RULES.md`: recovery and resumption behavior.
- `PROMPT_QUALITY_CHECKLIST.md`: prompt preflight checklist.
- `EXAMPLE_NEXT_TURN_PROMPT.md`: example bounded prompt.
- `VALIDATION_REPORT.md`: validation record for this docs package.

## Authority Order

1. Live repo policies, queue records, and task-local `status.yaml`.
2. The active WorkUnit `task.yaml`, `ExecPlan.md`, and `prompt.md`.
3. Task-local evidence.
4. Current validation output.
5. User prompt, after intake normalization when required.
6. Historical reports or pasted summaries.

If a pasted report conflicts with live repo state, prefer live repo state and
record the difference.
