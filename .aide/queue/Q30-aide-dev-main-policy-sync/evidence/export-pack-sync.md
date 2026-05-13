# Q30 Export Pack Sync

## Commands

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Pack Result

- Pack path: `.aide/export/aide-lite-pack-v0`
- Included files: 183
- Checksums: valid
- Checksum count: 186
- Boundary result: PASS
- Provenance result: `DIRTY_SOURCE_RECORDED`
- Provider/model calls: none
- Network calls: none

## Exported Q30-Relevant Files

The pack exports portable, generic Git workflow support:

- `.aide/scripts/aide_lite.py`
- `.aide/evals/golden-tasks/catalog.yaml`
- `.aide/policies/git-workflow.yaml`
- `.aide/policies/branch-roles.yaml`
- `.aide/policies/promotion-rules.yaml`
- `.aide/policies/sync-policy.yaml`
- `.aide/policies/prune-policy.yaml`
- `.aide/git/project-profiles.yaml`
- `.aide/git/helper-policy.yaml`
- `.aide/git/helper-commands.md`
- `docs/reference/git-workflow-policy.md`
- `docs/reference/branch-roles.md`
- `docs/reference/promotion-policy.md`

## Excluded AIDE-Specific Live State

The pack does not export these source-repo-specific artifacts as target truth:

- `.aide/git/aide-branch-policy.yaml`
- `.aide/git/aide-dev-main-plan.json`
- `.aide/git/aide-dev-main-plan.md`
- `.aide/git/latest-helper-plan.json`
- `.aide/git/latest-helper-plan.md`
- `.aide/git/workflow-detection.json`
- `.aide/git/workflow-detection.md`
- `docs/reference/aide-dev-main-workflow.md`
- `.aide/evals/golden-tasks/aide_dev_main_policy_golden/**`
- `.aide/evals/golden-tasks/aide_branch_plan_golden/**`
- `.aide/scripts/tests/test_q30_aide_dev_main_policy.py`

Target repositories must generate their own branch-policy and detection state.
