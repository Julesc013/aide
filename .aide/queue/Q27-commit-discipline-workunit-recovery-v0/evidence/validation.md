# Validation

Interpreter notes:

- `py -3`: FAIL, command not found in this shell.
- `python`: Python 3.8.1; existing Harness validation failed at the time on
  `str.removeprefix`, which requires a newer interpreter.
- `python3`: Python 3.9.13; used for Q27 baseline validation.

## Baseline Before Edits

- `git status --short`: PASS, clean.
- `git branch --show-current`: PASS, `main`.
- `git rev-parse HEAD`: PASS,
  `fe2ba90ebe63fa1b2b12c61335c647356b084b43`.
- `git log --oneline -20`: PASS; latest commit was
  `fe2ba90 docs: record q25 repair evidence`.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: FAIL, `py` command not found.
- `python scripts/aide validate`: FAIL, Python 3.8.1 cannot run existing
  Harness code using `str.removeprefix`.
- `python3 scripts/aide validate`: PASS_WITH_WARNINGS; 148 info, 7 warning,
  0 error. Warnings are existing review gates and generated manifest source
  fingerprint drift.
- `python3 scripts/aide doctor`: PASS_WITH_WARNINGS; same warning class.
- `python3 scripts/aide self-check`: PASS_WITH_WARNINGS; next recommended
  step remains Q25 review.
- `python3 .aide/scripts/aide_lite.py validate`: FAIL before Q27 edits at the
  time of this superseded attempt.
- `python3 .aide/scripts/aide_lite.py pack-status`: FAIL before Q27 edits at
  the time of this superseded attempt.

## Blocking Failures

`python3 .aide/scripts/aide_lite.py validate` failed on the then-current HEAD
with:

- missing required file `.aide.local.example/secrets/README.md`;
- export pack checksum mismatch for README/local-state-template payloads.

`python3 .aide/scripts/aide_lite.py pack-status` failed on the then-current
HEAD with:

- `checksums_valid: false`;
- `boundary_result: PASS`;
- `checksum_problems: 125`;
- example mismatches include `README.md`,
  `files/.aide.local.example/README.md`,
  `files/.aide.local.example/cache/README.md`,
  `files/.aide.local.example/config.example.yaml`, and
  `files/.aide.local.example/ledgers/README.md`.

## Q25 Acceptance Criteria Not Currently Met

- `pack_status_passes`: not met at the then-current HEAD.
- `export_pack_checksum_convention_coherent`: not met at the then-current HEAD because
  committed pack checksums no longer validate.
- `tests_and_validation_recorded`: Q25 evidence records a pass at Q25 time,
  but repo-local validation did not reproduce that pass at the time.

## Commands Not Run

The rest of the Q27 implementation validation suite was not run because the
task stopped on the explicit prerequisite blocker rule.

## Scoped Validation After Blocker Packet

- `git status --short`: PASS_WITH_CHANGES; only Q27 queue/index files are
  modified or untracked.
- `git diff --check`: PASS; Git reported only Windows line-ending warnings for
  `.aide/queue/index.yaml`.
- `python3 scripts/aide validate`: PASS_WITH_WARNINGS; existing review-gate and
  generated-manifest warnings only.
- `python3 .aide/scripts/aide_lite.py validate`: FAIL at the time; same
  prerequisite failures as baseline.
- `python3 .aide/scripts/aide_lite.py pack-status`: FAIL at the time; same
  prerequisite checksum failure as baseline.

## Current Supersession Note

Q25 has since repaired the pack/local-state baseline and Q26 supersedes this
pre-repair Q27 blocker packet for redo.
