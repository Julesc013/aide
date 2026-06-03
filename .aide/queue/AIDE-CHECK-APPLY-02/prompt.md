# AIDE-CHECK-APPLY-02 Prompt

Review and checkpoint `AIDE-APPLY-02 - Scoped Transaction Executor v0`.

This task is review-only. Inspect implementation, tests, reports, evidence, queue state, capability labels, and preserved forbidden-operation boundaries. Rerun validation. Do not implement new features or repair executor behavior. If code repair is required, produce an `AIDE-APPLY-02-REPAIR-01` proposal.

Required preserved boundaries:

- no install apply;
- no upgrade apply;
- no repair apply;
- no rollback/uninstall apply;
- no target repo mutation;
- no branch/worktree mutation;
- no merge;
- no push;
- no promotion;
- no release publication;
- no GitHub mutation;
- no provider/model calls;
- no Gateway calls;
- no network calls;
- no broad active-repo apply.

Final disposition must be one of `ACCEPTED_WITH_NOTES`, `NEEDS_REPAIR`, `REJECTED`, or `BLOCKED`.
