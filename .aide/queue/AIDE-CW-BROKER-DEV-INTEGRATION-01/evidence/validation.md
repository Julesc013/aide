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
- Two-parent merge commit:
  `091382e81f08b6e7363380cd3190c7483234d9ab`; tree:
  `4f75f5a9d1686a9fc5cfce9a484477237d9fbc2c`; second parent:
  `75da33108995ba63fc7148c6b4137349d7013798`.
- `aide_lite.py commit check --latest`: `PASS` for the merge commit.
- The incoming range check reports older policy-format failures in published
  history as well as passing implementation commits. No historical result is
  forged and no published history is rewritten.
- `git push origin task/aide-cw-broker-dev-integration-01`: passed; remote
  observation matched `091382e81f08b6e7363380cd3190c7483234d9ab`.
- `aide_lite.py git land --dry-run --source
  task/aide-cw-broker-dev-integration-01 --target dev --validation-ok --push`:
  `ready_dry_run`, with no local or remote mutation.
