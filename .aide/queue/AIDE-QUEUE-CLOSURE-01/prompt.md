# AIDE-QUEUE-CLOSURE-01 Prompt

Build a report-only blocker graph and closure plan for current AIDE queue state.

Do not implement broad queue automation. Do not bypass prohibitions. Do not mutate implementation files, target repositories, branch/worktree state, release state, GitHub state, providers, models, Gateway, network, or apply surfaces.

Outputs must remain under `.aide/queue/AIDE-QUEUE-CLOSURE-01/**` plus the queue index entry.

The selected next safe batch should prefer:

- `AIDE-APPLY-02-IMPLEMENT` when AIDE-APPLY-02 is authorized but not implemented;
- `AIDE-CHECK-APPLY-02` when AIDE-APPLY-02 is implemented but not checked;
- a narrow repair or lifecycle planning task only after AIDE-CHECK-APPLY-02 accepts the executor.
