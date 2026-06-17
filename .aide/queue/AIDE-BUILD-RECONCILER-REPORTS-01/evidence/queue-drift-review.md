# Queue Drift Review

Queue truth remains `.aide/queue/index.yaml` and task-local records.

Observed:

- `task_count`: 136
- `needs_review_count`: 82
- `blocked_count`: 1
- `self_task_indexed`: true

Finding recorded:

- `acceptance_gate_debt`: the queue intentionally carries many review-gated items. The Reconciler reports this without accepting, rejecting, superseding, or mutating any task.
