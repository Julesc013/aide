# Remaining Risks

- Rollback records are static compatibility examples and have not been exercised by a rollback dry-run harness.
- The rollback record schema uses `rollback_execution_implemented=false`; it does not require a separate `rollback_apply_executed` field.
- Rollback execution, uninstall/delete execution, lifecycle apply execution, fixture apply, active repo apply, and target repo apply remain unauthorized and unimplemented.
- Future rollback dry-run must prove rollback record consumption, current-hash checks, path boundaries, manual preservation, and no mutation.
- Global `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`, while this checkpoint selects a task-local next WorkUnit.
- Prior install/upgrade/repair expected-report evidence gaps remain.
- Review-gated backlog remains.
