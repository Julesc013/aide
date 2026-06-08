# Remaining Risks

- Install dry-run reports are static check evidence, not output from a reusable `lifecycle-install` command.
- Two install scenarios have no static expected report examples; generated plan reports were used as report evidence.
- No lifecycle dry-run harness executed the generated plans.
- No fixture apply gate is authorized.
- Scoped transaction executor v0 remains limited: no lifecycle apply execution, no multi-file atomic apply, no rollback execution, no uninstall/delete execution, no target repo authority, and no active repo apply gate.
- Global Task OS `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01` rather than this task-local next WorkUnit.
- Lifecycle apply, fixture apply, target repo adoption, release/provider/Gateway/network work, and broad active-repo apply remain deferred and prohibited without future queue authority.
