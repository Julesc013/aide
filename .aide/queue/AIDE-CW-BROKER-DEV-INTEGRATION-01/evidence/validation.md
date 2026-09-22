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
- Dev landing commit:
  `bed5a57aed4f7686de4b9137dbb3afc8e7995436`; parents:
  `13fc9a6a0aa02bd4c2343c640e8b83a95d89c6ab` and
  `2ef1fb7476bb350ad2a8da84c6093fa9ae5a7953`.
- Pre-commit landing-tree `aide_lite.py doctor` and `aide_lite.py validate`:
  `PASS`; at that point Git `HEAD` still named the old dev parent.
- Landing commit message check: `PASS`; staged whitespace and conflict checks:
  `PASS`.
- `git push origin dev`: passed. Local `dev`, `origin/dev`, and
  `git ls-remote origin refs/heads/dev` all observed the landing identity.
- `git merge-base --is-ancestor 75da3310... dev`: passed.
- Post-commit canonical validation: `FAIL` only for export-pack and pack-status
  provenance. The committed manifest source is `31bd91bd10ed57e98e658380cd9372e074867f63`
  while the new dev head is `bed5a57aed4f7686de4b9137dbb3afc8e7995436`
  and portable inputs changed. This requires a clean-source derived-artifact
  refresh; it is not recorded as a broker runtime failure or a pass.
- Follow-up `AIDE-BROKER-DEV-PACK-REFRESH-01` regenerated the export manifest,
  local bundle, and preview release draft from clean post-integration source,
  then closed committed provenance derivation. Its landing is
  `088b20ba76ae09b19277b4aed7dff7d1d324cdbe`.
- Final `pack-status`, release validation, release draft checksums, canonical
  `validate`, and `doctor`: `PASS`. No tag, upload, publication, network API,
  or target mutation occurred.
