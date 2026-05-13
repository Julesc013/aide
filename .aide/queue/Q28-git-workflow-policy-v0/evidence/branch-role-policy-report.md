# Q28 Branch Role Policy Report

## Policy Files

- `.aide/policies/git-workflow.yaml`
- `.aide/policies/branch-roles.yaml`
- `.aide/policies/promotion-rules.yaml`
- `.aide/policies/sync-policy.yaml`
- `.aide/policies/prune-policy.yaml`

## Role Semantics

- `main`: canonical accepted truth, protected, no force push, no deletion.
- `dev`: integration truth, shareable latest work, not canonical release truth.
- `task/*`, `codex/*`, `aide/*`, `fix/*`, `repair/*`: bounded work that lands to `dev` by default.
- `review/*`: review staging and evidence inspection.
- `quarantine/*`: isolated risky or disputed work.
- `release/*`: maintained release lines only when release support exists.
- `hotfix/*`: urgent focused repair with explicit backmerge targets.
- `gh-pages`: generated deploy branch only.
- unknown names: conservative fallback; no mutation recommendation.

## Promotion And Sync Gates

- `task_to_dev` requires clean or understood state, task evidence, validation, commit checks, and synchronized target branch state.
- `dev_to_main` requires review packet, full validation classification, changelog preview, generated artifact review, blocked-queue classification, and explicit promotion evidence.
- Sync policy forbids implicit merge/rebase and records no automatic remote mutation in Q28.

## Prune Guards

- Prune requires ancestor containment proof.
- Protected roles are never routine prune candidates.
- Release and hotfix retention require explicit policy.
- Q28 implements no branch-deletion command.
