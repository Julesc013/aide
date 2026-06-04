# Remaining Risks

- Lifecycle schema validation is structural only in this task; a dedicated validator WorkUnit is selected next.
- Fixture repository target files are not materialized yet.
- Lifecycle fixture dry-run and fixture apply are not implemented or executed.
- Rollback-compatible records are defined, but rollback execution is not implemented.
- Uninstall/delete safety remains unimplemented and must preserve manual content and unknown ownership.
- Scoped transaction executor v0 still blocks multi-mutating apply and does not provide multi-file atomic apply.
- Active AIDE repo apply remains blocked pending a separate gate.
- Target repo adoption remains deferred pending target-local authority.
- Release, provider/model, Gateway, network, GitHub mutation, merge, push, promotion, and branch/worktree mutation remain prohibited.
- Task OS `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; this task records the warning but does not change Task OS selector implementation.
