# Remaining Risks

- Static expected repair report refs remain absent for `repair-plan-missing-marker` and `repair-plan-malformed-marker`.
- No `lifecycle-repair` command namespace exists; current evidence is static report-only and dry-run-planned.
- Global `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`, while this checkpoint selects a task-local next WorkUnit.
- Prior install/upgrade expected-report evidence gaps remain.
- Rollback-compatible record evidence still requires independent checkpoint review before rollback dry-run or any fixture apply gate.
- Rollback execution, uninstall/delete behavior, lifecycle apply execution, fixture apply, active repo apply, target repo apply, release publication, provider/model calls, Gateway calls, GitHub mutation, network calls, and broad active-repo apply remain unauthorised and unimplemented.
- Review-gated backlog remains.
