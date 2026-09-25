# Validation, 2026-09-25

- RED: `py -3 -B -m unittest discover -s .aide/scripts/tests -p
  test_q48_github_release_draft.py -k distinguishes_legacy_planners -v`
  exited 1 before the fix. The generated draft contained both obsolete
  `remain plan/dry-run models` and `remain preservation-first planning
  surfaces` claims.
- PASS: after the source change, the targeted regression exited 0 and the
  full Q48 suite ran 12 tests, exit 0. External log:
  `D:/Projects/AIDE/_review_scratch/stable-lite-draft-truth-20260925/q48-focused.log`,
  SHA-256 `699688c8fcbfba23aea0eb6db011adaf0c8417e64e9a365b652b7015948d3214`.
- PASS: Python AST parse of `.aide/scripts/aide_lite.py` exited 0.
- FAIL, retained generator dependency: canonical `validate` exited 1, log
  SHA-256 `e4138e22c9ff47dd58475e30572c1a35c5fa2866d6d46f56dd4bed68d95448a9`.
  Its two failures are stale export manifest provenance and pack-status:
  archived source `8365aa61` versus current checkout `75406123`.
- FAIL, same dependency: canonical `doctor` exited 1, log SHA-256
  `3d55365b3a7e6074254a2e1be4b33d727242f59e1f2e32cec3ec78186b210484`;
  its single failure points to validation. This source task does not own the
  required derived projection.
- PASS: `git diff --check` found no whitespace errors before source freeze.
- NOT RUN: export/changelog/release regeneration, committed replay, installed
  consumer, dev effect or stable publication.
