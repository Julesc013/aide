# Remaining Risks

- `upgrade-manual-preserved` lacks a static expected report ref. This is non-blocking for checkpoint acceptance but remains repair-worthy.
- Prior install expected-report gaps remain for `install-clean` and `install-existing-manual-preserved`.
- The lifecycle upgrade command namespace is not implemented; this checkpoint used static report-only checks and did not run upgrade apply or lifecycle apply.
- The global Task OS `next-plan` selector still prefers `AIDE-APPLY-LIFECYCLE-PLAN-01`; this checkpoint follows the local next-batch selection.
- Upgrade dry-run reports are not apply evidence. They do not prove upgrade apply, lifecycle apply, fixture apply, active repo apply, target repo apply, rollback execution, uninstall/delete safety, production readiness, release readiness, or broad active-repo apply capability.
