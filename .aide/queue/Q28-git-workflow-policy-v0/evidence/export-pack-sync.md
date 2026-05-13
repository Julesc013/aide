# Q28 Export Pack Sync

## Commands

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Pack Result

- pack path: `.aide/export/aide-lite-pack-v0`
- included files: 169
- checksum count: 172
- checksums valid: true
- provenance result: `DIRTY_SOURCE_RECORDED`
- boundary result: PASS
- checksum problems: 0
- provenance problems: 0
- boundary violations: 0

## Exported Q28 Files

- `.aide/policies/git-workflow.yaml`
- `.aide/policies/branch-roles.yaml`
- `.aide/policies/promotion-rules.yaml`
- `.aide/policies/sync-policy.yaml`
- `.aide/policies/prune-policy.yaml`
- `.aide/git/README.md`
- `.aide/git/branch-roles.md`
- `.aide/git/promotion-rules.md`
- `.aide/git/sync-policy.md`
- `.aide/git/prune-policy.md`
- `.aide/git/project-profiles.yaml`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q28_git_workflow.py`
- Q28 golden tasks under `.aide/evals/golden-tasks/**`
- `docs/reference/git-workflow-policy.md`
- `docs/reference/branch-roles.md`
- `docs/reference/promotion-policy.md`

## Excluded Source-Specific Files

- `.aide/git/workflow-detection.json`
- `.aide/git/workflow-detection.md`

These generated reports describe the source repo state and are not exported as
canonical target truth.
