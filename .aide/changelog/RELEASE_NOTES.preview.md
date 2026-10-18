# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: 21625bd6a5cf9610e3b8a5a586fb1290bcdf6fe8..13edc23c88d5db9440f2256a0b178b3d14f5cc96
source_head: 13edc23c88d5db9440f2256a0b178b3d14f5cc96
preview_only: true

## Highlights

- Added: Compact validation with full text and machine-readable result modes. (c96577f7b079)
- Added: Compact validation with full text and machine-readable result modes. (7804bb47d587)
- Added: Compact validation with full text and machine-readable result modes. (28a8033977b6)
- Added: Compact validation with full text and machine-readable result modes. (0dc7d2a0f439)
- Added: Compact validation with full text and machine-readable result modes. (13edc23c88d5)
- Fixed: Document the bounded repair needed before accepting validation delivery. (ec51458bfed7)

## Validation Summary

- c96577f7b079: PASS structural syntax and unchanged collector/existing-test checks.
- 7804bb47d587: PASS36 source methods with no failures, errors or skips; job fully retired.
- ec51458bfed7: PASS ownership6, export, doctor, validate and pack status in attempt2.
- 28a8033977b6: PASS36 source methods with no failures, errors or skips; job fully retired.
- 0dc7d2a0f439: PASS36 source methods with no failures, errors or skips; job fully retired.
- 13edc23c88d5: PASS source10/conserved26, delivered36, ownership6 and actual complete validation.

## Known Risks

- c96577f7b079: Consumers parsing individual PASS lines must request --full or --json.
- 7804bb47d587: Consumers parsing individual PASS lines must request --full or --json.
- ec51458bfed7: Failed export is an incomplete candidate; actual output comparison is unrun.
- 28a8033977b6: Consumers parsing individual PASS lines must request --full or --json.
- 0dc7d2a0f439: Consumers parsing individual PASS lines must request --full or --json.
- 13edc23c88d5: Consumers parsing individual PASS lines must request --full or --json.

## Follow-up

- c96577f7b079: Qualify source/exported consumers, refresh bindings and review integration.
- 7804bb47d587: Qualify source/exported consumers, refresh bindings and review integration.
- ec51458bfed7: Prepare exact fixture repair and independently review allocation3; no automatic retry.
- 28a8033977b6: Qualify source/exported consumers, refresh bindings and review integration.
- 0dc7d2a0f439: Qualify source/exported consumers, refresh bindings and review integration.
- 13edc23c88d5: Qualify source/exported consumers, refresh bindings and review integration.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
