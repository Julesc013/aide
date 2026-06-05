# Remaining Risks

- Physical fixture tree validation is local parse/hash/evidence based; the lifecycle-schema validator remains schema/example scoped.
- Future plan generation must prove generated dry-run/report-only plans match or explain differences from expected reports.
- Rollback and uninstall/delete safety remain review-gated and must not move to execution without explicit authority and rollback prerequisites.
- Active repo apply and target repo apply remain prohibited pending future queue authority.
- Task OS generated next-plan remains stale relative to task-local sequencing.
