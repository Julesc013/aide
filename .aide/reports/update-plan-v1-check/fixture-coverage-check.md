# Fixture Coverage Check

Fixture matrix result: `PASS`

Fixture case count: `29`

Required valid cases present and passing:

- `no-op-update`
- `managed-file-add`
- `managed-file-update`
- `managed-section-add`
- `managed-section-update`
- `project-owned-preservation`
- `local-only-preservation`
- `legacy-preservation`
- `manual-review-item`
- `migration-dependent-plan`
- `conflict-only-plan`

Required invalid cases present and passing:

- `unknown-ownership-auto-update`
- `never-touch-update`
- `project-owned-overwrite`
- `local-only-overwrite`
- `path-traversal`
- `absolute-path`
- `case-collision`
- `symlink-reparse-uncertainty`
- `missing-rollback-requirement`
- `mismatched-distribution`
- `mismatched-project-lock`
- `mismatched-ownership-ledger`
- `unknown-required-feature`

Additional invalid fixtures also cover apply claims, target mutation claims, required extension refusal, and source-output-as-target-truth.
