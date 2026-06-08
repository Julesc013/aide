# Remaining Risks

- `upgrade-manual-preserved` lacks a static expected report ref. The generated plan report and static file/hash checks cover the dry-run review, but this remains an evidence-completeness warning.
- The lifecycle upgrade command namespace is not implemented; this task used static report-only checks and did not run upgrade apply or lifecycle apply.
- The global Task OS `next-plan` selector still prefers `AIDE-APPLY-LIFECYCLE-PLAN-01`; this task follows the local checkpoint selection from `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01`.
- Upgrade dry-run reports are not apply evidence. They do not prove upgrade apply, lifecycle apply, fixture apply, active repo apply, target repo apply, rollback execution, uninstall/delete safety, production readiness, release readiness, or broad active-repo apply capability.
- A future checkpoint should independently review the warning, report-only evidence, path boundaries, managed-section preservation, drift detection, hashes, scoped executor interlock, no-apply proof, and capability labels.
