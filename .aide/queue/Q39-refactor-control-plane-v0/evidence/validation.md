# Q39 Validation

## Git And Local State

- `git status --short`: expected Q39 export/context/refactor/evidence changes before final commit.
- `git diff --check`: PASS; Git reported line-ending normalization warnings only.
- `git branch --show-current`: PASS, `main`.
- `git check-ignore .aide.local/`: PASS, `.aide.local/` is ignored.

## Harness

- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; existing stale generated manifest warning for `.aide/generated/manifest.yaml`.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same generated manifest warning.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; same generated manifest warning.

## AIDE Lite

- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 63/63 golden tasks.
- `py -3 .aide/scripts/aide_lite.py intent validate`: PASS.

## Repo And Quality Inputs

- `py -3 .aide/scripts/aide_lite.py repo inventory`: PASS; 1666 files, 146 unknown, 475 orphan candidates. Generated Q37 outputs were restored after validation and not promoted in Q39.
- `py -3 .aide/scripts/aide_lite.py repo validate`: WARN; 146 unknown file classifications.
- `py -3 .aide/scripts/aide_lite.py repo status`: PASS.
- `py -3 .aide/scripts/aide_lite.py repo explain-file .aide/scripts/aide_lite.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py repo docs`: PASS; stale candidates are conservative.
- `py -3 .aide/scripts/aide_lite.py repo tests`: PASS.
- `py -3 .aide/scripts/aide_lite.py repo deps`: PASS.
- `py -3 .aide/scripts/aide_lite.py quality ledger`: PASS; 1666 files, fail_count 0. Generated Q38 outputs were restored after validation and not promoted in Q39.
- `py -3 .aide/scripts/aide_lite.py quality validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py quality status`: PASS.
- `py -3 .aide/scripts/aide_lite.py quality explain-file .aide/scripts/aide_lite.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py quality docs`: PASS.
- `py -3 .aide/scripts/aide_lite.py quality tests`: PASS.
- `py -3 .aide/scripts/aide_lite.py quality modules`: PASS.
- `py -3 .aide/scripts/aide_lite.py quality reuse`: PASS.

## Refactor Commands

- `py -3 .aide/scripts/aide_lite.py refactor status`: PASS; no_apply true, apply unavailable in Q39.
- `py -3 .aide/scripts/aide_lite.py refactor plan`: PASS; generated readiness/example artifacts.
- `py -3 .aide/scripts/aide_lite.py refactor validate`: PASS; apply-enabled and final-delete states are rejected by validation logic.
- `py -3 .aide/scripts/aide_lite.py refactor dry-run`: PASS; source_files_changed false, file_moves false, file_deletes false, reference_rewrites false.
- `py -3 .aide/scripts/aide_lite.py refactor schemas`: PASS.
- `py -3 .aide/scripts/aide_lite.py refactor ledger`: PASS.

## Commit, Changelog, Git, GitHub, Pack

- `py -3 .aide/scripts/aide_lite.py commit check --range 032f83c..HEAD`: PASS for the Q39 commits before the final export/evidence commit.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS; generated preview outputs were restored when outside Q39 scope.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS, non_mutating true.
- `py -3 .aide/scripts/aide_lite.py github validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS, 335 files, 338 checksums, boundary PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, checksums_valid true, boundary PASS, provenance DIRTY_SOURCE_RECORDED.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q40 Root Recycling Framework v0"`: PASS, `.aide/context/latest-task-packet.md` within budget.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 1026 approximate tokens.

## Tests

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q39_refactor_control.py`: PASS, 8 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests after rerun with longer timeout; the first 120s run timed out.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.
- Canonical `.aide/scripts/tests` command from QFIX-02: `py -3 .aide/scripts/aide_lite.py test`, PASS.

## Secret Scan

- Targeted `rg` scan was run before final report. Matches were inspected as policy/example/test strings only; no raw provider credentials or private keys were found.

## Notes

One `aide_lite validate` run was started concurrently with `export-pack` and saw the pack mid-refresh, producing transient missing-pack failures. It was rerun sequentially and passed; the transient run is not treated as product validation.
