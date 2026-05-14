# Validation

## Baseline

- `git status --short`: PASS, clean before Q46 edits.
- `git branch --show-current`: PASS, `main`.
- `git branch --all`: PASS, branch state inspected.
- `git remote -v`: PASS, remotes inspected without mutation.
- `git rev-parse HEAD`: PASS, baseline HEAD recorded.
- `git tag --list`: PASS.
- `git check-ignore .aide.local/`: PASS, `.aide.local/` ignored.
- `git diff --check`: PASS.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, pre-existing stale
  `.aide/generated/manifest.yaml` fingerprint warning.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, same pre-existing warning.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, same pre-existing
  warning.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS.
- Q36-Q45 available validation commands: PASS, except `repo validate` WARN for
  pre-existing unknown file classifications and `core/gateway/tests` timeout
  already recorded by Q45.

## Q46 Commands

- `py -3 .aide/scripts/aide_lite.py rollback observe`: PASS, no_apply true.
- `py -3 .aide/scripts/aide_lite.py rollback plan`: PASS, 229 operations,
  885 preserved paths, 0 blockers, no_apply true.
- `py -3 .aide/scripts/aide_lite.py rollback dry-run`: PASS, 1 future restore,
  4 future removals, 224 preservations, 0 blockers, no_apply true.
- `py -3 .aide/scripts/aide_lite.py rollback validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py rollback status`: PASS, future_actions 5,
  preservations 224, blockers 0.
- `py -3 .aide/scripts/aide_lite.py rollback classes`: PASS.
- `py -3 .aide/scripts/aide_lite.py rollback explain .aide/scripts/aide_lite.py`:
  PASS, no rollback operation planned for that path.
- `py -3 .aide/scripts/aide_lite.py uninstall observe`: PASS, no_apply true.
- `py -3 .aide/scripts/aide_lite.py uninstall plan`: PASS, 1790 operations,
  1557 preserved paths, 0 blockers, no_apply true.
- `py -3 .aide/scripts/aide_lite.py uninstall dry-run`: PASS, 233 future
  removal candidates, 885 preservations, 672 unknown-ownership records, 0
  blockers, no_apply true.
- `py -3 .aide/scripts/aide_lite.py uninstall validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py uninstall status`: PASS.
- `py -3 .aide/scripts/aide_lite.py uninstall classes`: PASS.
- `py -3 .aide/scripts/aide_lite.py uninstall explain .aide/scripts/aide_lite.py`:
  PASS, future portable-file removal candidate only; `apply_allowed: false` and
  `delete_allowed: false`.

## Export, Governance, And Tests

- `py -3 .aide/scripts/tests/test_q46_rollback_uninstall.py`: PASS, 7 tests.
- Q46 golden tasks: PASS for rollback policy, rollback schema, rollback
  no-apply, uninstall policy, uninstall schema, uninstall no-apply,
  uninstall target-state preservation, and no blanket `.aide` deletion.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`:
  PASS, 555 included files, 558 checksums, boundary PASS, no provider/model or
  network calls.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, checksums valid,
  boundary PASS, provenance result `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q47 AIDE Lite Release Bundle v0"`:
  PASS, regenerated `.aide/context/latest-task-packet.md`.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`:
  PASS, 1026 approximate tokens, within budget.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS, preview-only;
  reported 14 malformed historical commits for review.
- `py -3 .aide/scripts/aide_lite.py changelog validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py github validate`: PASS, advisory-only.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: TIMEOUT after 900
  seconds; timed-out `py`/`python` processes were stopped, and no Gateway files
  were edited in Q46.
- Targeted `rg` secret scan over existing requested paths: PASS_AFTER_INSPECTION.
  Matches were policy, docs, generated references, regex definitions, and test
  fixture terms such as `api_key`, `SECRET`, `TOKEN`, `PASSWORD`, `sk-ant`, and
  task-packet references. No actual provider key, `.env` content,
  `.aide.local` state, private key, raw prompt, or raw response was found.

## Final Structural Checks

- `git diff --check`: PASS.
- No provider/model/network calls were introduced.
- No target repo, branch, GitHub, CI, release, tag, install, repair, upgrade,
  rollback, or uninstall apply mutation was performed.
