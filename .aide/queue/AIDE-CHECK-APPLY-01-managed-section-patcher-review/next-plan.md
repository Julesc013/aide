# Next Plan

- selected_next_task: AIDE-APPLY-02 - Scoped Transaction Executor v0
- reason: AIDE-APPLY-01 is accepted with notes and no-real-apply boundaries are intact.
- start_condition: create a separate queue item and ExecPlan before implementation.

## Guardrails

- Keep AIDE-APPLY-02 limited to explicit operator-provided paths and managed-section operations by default.
- Require preimage hashes, postimage verification, staged-change records, rollback records, ownership checks, and conflict blocks.
- Do not include install, repair, upgrade, rollback/uninstall lifecycle apply.
- Do not touch target repositories, branches, worktrees, releases, GitHub APIs, providers, models, network, or Gateway surfaces.
