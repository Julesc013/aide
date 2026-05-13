# AIDE Branch Plan Golden Acceptance

This deterministic no-call task passes when:

- `.aide/git/aide-dev-main-plan.json` exists and uses `aide.dev-main-plan.v0`.
- The plan records `main` as canonical and `dev` as integration.
- The plan records `non_mutating: true` and `live_mutation_performed: false`.
- Helper dry-run summaries are present.
- Markdown states that future commands were not run by Q30.
