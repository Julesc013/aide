# AIDE Dev/Main Plan

- schema_version: aide.dev-main-plan.v0
- generated_by: aide-lite
- repo_id: julesc013/aide
- non_mutating: true
- live_mutation_performed: false

## Branch Roles

- current_branch: task/aide-cw-integration-broker-01
- current_commit: 83df2b73c96f754561e669080bc4c90108d0bc4b
- current_branch_role: task
- canonical_branch: main
- integration_branch: dev
- dev_is_canonical_truth: false

## Topology

- local_main_exists: true
- remote_origin_main_exists: true
- local_dev_exists: true
- remote_origin_dev_exists: true
- current_branch_tracks_remote: true
- upstream: origin/task/aide-cw-integration-broker-01
- working_tree_clean: false

## Helper Dry-Runs

- plan: blocked
- sync: blocked
- land: blocked
- promote: blocked
- prune: ready_dry_run

## Future Explicit Operator Plan

These commands were not run by Q30:

- none

## Recommended Next Action

verify dev is integration and use Q29 helper dry-runs before any future land/promote operation

## Warnings

- dirty_tree_detected

## Q30 Boundary

Q30 does not create, push, merge, promote, prune, delete, fetch, tag, release, or
mutate live AIDE branches. `main` remains canonical truth and `dev` is planned
as shareable integration truth only.
