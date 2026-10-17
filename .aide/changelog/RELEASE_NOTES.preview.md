# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: 19e237cde0864ca56169a14a7bf8ded5180d6def..72d613489ad7a7429cdeeb49724044789f5308c1
source_head: 72d613489ad7a7429cdeeb49724044789f5308c1
preview_only: true

## Highlights

- Added: Portable task-record export and checksum-bound inspection. (40a5740e7eef)
- Added: Safe-installed task-record export and read-only comparison. (72d613489ad7)
- Changed: Record task handoff source proof and prepare portable consumer checks. (579925c7c5ee)

## Validation Summary

- 40a5740e7eef: PASS: syntax; 59 existing test methods unchanged; 20 new regressions prepared.
- 579925c7c5ee: PASS: source79, no skips; collection and retirement verified; binding CURRENT.
- 72d613489ad7: PASS: source79, delivered79, ownership6; no skips; installed consumer PASS.

## Known Risks

- 40a5740e7eef: Observation is not ownership, authorization, authenticity or atomic capture.
- 579925c7c5ee: Bundle inspection does not establish authority, authenticity or atomic capture.
- 72d613489ad7: Observations do not transfer worker ownership or execution authority.

## Follow-up

- 40a5740e7eef: Qualify source and actual safe-installed consumers; review integration separately.
- 579925c7c5ee: Run reviewed export consumer job and fixed preview before integration review.
- 72d613489ad7: Complete fixed preview, terminal review and guarded dev/main synchronization.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
