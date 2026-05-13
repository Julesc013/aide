# Q29 Remaining Risks

- Q29 implements helpers but does not use them to mutate live AIDE branches.
- The live AIDE repository has no `dev` branch, so task-to-dev landing and dev-to-main promotion remain blocked until Q30 decides the AIDE dev/main policy application.
- `main` is ahead of `origin/main`; Q29 reports this but does not push or reconcile it.
- GitHub branch protection is not managed by Q29.
- CI checks and required status checks are not created by Q29.
- Remote push remains explicit and future-gated.
- Helper validation evidence is report-first; it does not prove branch protection or CI enforcement.
- Existing Harness warnings remain for older review gates and generated-manifest source fingerprint drift.
- Changelog preview still reports malformed pre-Q27 commits.
- Q35 is still needed for GitHub protection and CI advisory.
