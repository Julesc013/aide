# Q29 Export Pack Sync

## Export Command

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Pack Status

- Pack path: `.aide/export/aide-lite-pack-v0`.
- Included files: 183.
- Checksum count: 186.
- Checksums: valid.
- Provenance: `DIRTY_SOURCE_RECORDED`.
- Boundary: PASS.
- Provider/model calls: none.
- Network calls: none.

## Exported Q29 Helper Files

- `.aide/git/helper-policy.yaml`.
- `.aide/git/helper-commands.md`.
- `.aide/policies/git-workflow.yaml`.
- `.aide/policies/branch-roles.yaml`.
- `.aide/policies/promotion-rules.yaml`.
- `.aide/policies/sync-policy.yaml`.
- `.aide/policies/prune-policy.yaml`.
- `.aide/scripts/aide_lite.py`.
- `.aide/scripts/tests/test_q29_git_helper.py`.
- `.aide/evals/golden-tasks/git_helper_policy_golden/**`.
- `.aide/evals/golden-tasks/git_land_plan_golden/**`.
- `.aide/evals/golden-tasks/git_promote_plan_golden/**`.
- `.aide/evals/golden-tasks/git_prune_guard_golden/**`.
- `.aide/evals/golden-tasks/git_live_repo_no_mutation_golden/**`.
- `docs/reference/git-helper-workflow.md`.

## Deliberate Exclusions

- Live repo-specific `.aide/git/latest-helper-plan.json` and `.aide/git/latest-helper-plan.md` remain source-state reports, not target import truth.
- No `.aide.local/`, `.env`, raw prompt logs, raw response logs, provider keys, source queue history, generated source reports, or local machine traces are exported.

## Target Import Implications

Future target repos that import the pack receive the Q29 dry-run helper policy, command docs, AIDE Lite command implementation, fixture tests, and golden tasks. They still need target-local branch detection and target-local helper plans before any branch action.
