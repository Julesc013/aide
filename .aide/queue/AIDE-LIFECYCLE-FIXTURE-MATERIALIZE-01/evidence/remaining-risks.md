# Remaining Risks

- The existing lifecycle-schema validator was not widened to validate every physical fixture file; this task uses local parse checks and evidence for the materialized tree.
- Future dry-run plan generation must prove that expected reports match planner output.
- Future rollback proof must remain record-only until explicit rollback execution authority exists.
- Uninstall/delete behavior remains especially sensitive and must stay blocked or dry-run/report-only until ownership evidence and rollback prerequisites are reviewed.
- Active repo apply and target repo apply remain prohibited pending separate queue authority.
- Release, provider/model, Gateway, network, and GitHub surfaces remain deferred.
