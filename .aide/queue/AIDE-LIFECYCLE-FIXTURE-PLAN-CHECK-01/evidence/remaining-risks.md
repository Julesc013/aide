# Remaining Risks

- Generated lifecycle fixture plans are static planning artifacts; they have not been executed by a lifecycle dry-run harness.
- The generator remains metadata/report based and does not provide a reusable generator CLI command.
- The plan index does not duplicate `target_files_mutated_expected=false`; that field is present in each generated plan.
- The scoped transaction executor v0 interlock is sufficient for report/dry-run plan classes, but it still blocks multi-mutating lifecycle apply, rollback execution, uninstall/delete execution, active repo apply, and target repo authority.
- Global Task OS `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01` rather than this checkpoint's task-local next WorkUnit.
- Lifecycle apply, fixture apply, target repo adoption, release/provider/Gateway/network work, and broad active-repo apply remain deferred and prohibited without future queue authority.
