# Branch Role Policy Report

Status: superseded pre-repair blocker record.

Q28 was expected to add:

- `.aide/policies/git-workflow.yaml`;
- `.aide/policies/branch-roles.yaml`;
- `.aide/policies/promotion-rules.yaml`;
- `.aide/policies/sync-policy.yaml`;
- `.aide/policies/prune-policy.yaml`;
- `.aide/git/branch-roles.md`;
- `.aide/git/promotion-rules.md`;
- `.aide/git/sync-policy.md`;
- `.aide/git/prune-policy.md`.

No branch-role policy files were implemented because Q27 is materially
incomplete.

## Required Future Semantics

When Q28 is reopened, policy must preserve these core rules:

- `main` is accepted canonical truth.
- `dev` is shareable integration truth, not canonical truth.
- `task/*` branches are bounded short-lived work.
- `release/*` branches are retained only for maintained release lines.
- `hotfix/*` branches are urgent repairs with backmerge requirements.
- `gh-pages` is generated deploy state only when a repo uses it.
- Q28 detection remains report-only and does not mutate Git state.
