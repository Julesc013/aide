# AIDE Dev/Main Plan

- schema_version: aide.dev-main-plan.v0
- generated_by: aide-lite
- repo_id: julesc013/aide
- non_mutating: true
- live_mutation_performed: false

## Branch Roles

- current_branch: main
- current_commit: d6c660d72d3cb019f74c74274228cfbbca60e6ba
- current_branch_role: canonical
- canonical_branch: main
- integration_branch: dev
- dev_is_canonical_truth: false

## Topology

- local_main_exists: true
- remote_origin_main_exists: true
- local_dev_exists: false
- remote_origin_dev_exists: false
- current_branch_tracks_remote: true
- upstream: origin/main
- working_tree_clean: false

## Helper Dry-Runs

- plan: blocked
- sync: blocked
- land: blocked
- promote: blocked
- prune: ready_dry_run

## Future Explicit Operator Plan

These commands were not run by Q30:

- git switch -c dev main
- git push -u origin dev

## Recommended Next Action

review future explicit dev creation plan; do not create or push dev during Q30

## Warnings

- dirty_tree_detected
- local_dev_missing
- remote_origin_dev_missing

## Q30 Boundary

Q30 does not create, push, merge, promote, prune, delete, fetch, tag, release, or
mutate live AIDE branches. `main` remains canonical truth and `dev` is planned
as shareable integration truth only.
