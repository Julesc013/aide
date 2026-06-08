# Remaining Risks

- Static expected repair report refs are absent for both repair scenarios. Generated plan reports and expected-state README files are sufficient for this dry-run check but should be independently reviewed.
- Lifecycle repair dry-run remains static/report-only; no lifecycle repair command was implemented or run.
- Related drift evidence was reviewed as upstream context only.
- Rollback dry-run, rollback execution, uninstall/delete safety, fixture apply gates, active repo apply, target repo adoption, release publication, provider/model calls, Gateway calls, network calls, and broad active-repo apply remain deferred or prohibited.
- Global Task OS `next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`, while this task-local next batch selects `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`.
- The review-gated backlog remains.
