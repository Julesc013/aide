# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: a0970badeca5b3332505a4158fcfca6b075e07e3..7d2c41f73357acdda6f0ad5c73331b9df842a408
source_head: 7d2c41f73357acdda6f0ad5c73331b9df842a408
preview_only: true

## Highlights

- Added: job effort supplied-attempt view with explicit incomplete accounting. (82d771463a12)
- Added: qualified portable job effort reporting for explicit supplied work sets. (7d2c41f73357)
- Fixed: supplied-usage overlap regression fixture identity. (7c2aec4949cc)

## Validation Summary

- 82d771463a12: PASS: structural validation, static syntax, exact source/effect review at tree200525fe and all895 input pins.
- 7c2aec4949cc: PASS: 41 of 42 original checks, collection digests and retirement.
- 7d2c41f73357: PASS: 42 source and 42 delivered checks without skips; six ownership checks.

## Known Risks

- 82d771463a12: Source is a candidate; whole-work usage, cost and accepted-outcome time remain unknown.
- 7c2aec4949cc: Actual portable behavior remains unqualified until this attempt passes.
- 7d2c41f73357: Partial observations do not establish cost savings or task acceptance.

## Follow-up

- 82d771463a12: Run one bounded source job, then qualify actual portable delivery and integration separately.
- 7c2aec4949cc: Run reviewed source42, real five-attempt consumer and delivered42; stop on failure.
- 7d2c41f73357: Generate and replay the reviewed preview, then obtain exact terminal integration review.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
