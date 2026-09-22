# Validation

- Local and remote source and target refs match the exact requested commits.
- Ancestry checks confirm neither parent contains the other.
- Source unique runtime history and net path groups were inventoried.
- `git merge-tree --write-tree dev 75da3310...` identified fourteen conflicts
  and no conflict under `core/runtime/**` or broker-focused test paths.
- The real no-commit merge produced the same fourteen conflicts. All are
  resolved and `git diff --name-only --diff-filter=U` is empty.
- Conflict-marker scanning is clean and the reconciled queue index contains 261
  unique task ids.
- `git diff --check` passes.
- The combined tree leaves current `dev`'s `.codex`, export, release, importer,
  and protected regression-test paths unchanged from the admission parent.
- `py -3 -B -m unittest discover -s .aide/scripts/tests -p
  "test_continuous_worker*.py" -v`: 312 run, 311 passed, one skipped. The skip
  is the pre-existing Windows symlink-creation privilege gap.
- `py -3 -B -m unittest discover -s .aide/scripts/tests -p
  "test_export_import.py" -v`: 25 passed.
- `py -3 -B -m unittest discover -s .aide/scripts/tests -p
  "test_q47_release_bundle.py" -v`: 10 passed.
- `py -3 -B .aide/scripts/aide_lite.py doctor`: `PASS`.
- `py -3 -B .aide/scripts/aide_lite.py validate`: `PASS`.
- `py -3 -B .aide/scripts/aide_lite.py task inspect --task
  AIDE-CW-BROKER-DEV-INTEGRATION-01`: task found, evidence complete, continue
  from status and evidence.
- The pre-commit `git plan` correctly reported
  `dirty_tree_requires_classification`; it did not mutate branches or remotes.
- Commit-policy and post-commit range checks remain pending until the two-parent
  merge commit has an identity.
