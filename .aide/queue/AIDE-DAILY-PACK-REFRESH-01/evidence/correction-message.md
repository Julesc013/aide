fix(packaging): preserve unknown asset state on early failure

## Summary

- Correct the one independent review finding in the held export wrapper.

## Why

- A failed operation cannot assert unchanged release bytes before observing them.

## Changed

- Initialize comparison status as unknown and attempt guarded finalization comparison.
- Preserve the original exception and unknown outcome if comparison cannot complete.
- Retain actual REQUEST_CHANGES and update the exact wrapper input pin.

## Validation

- PASS: corrected Python AST and input/template consistency.
- PASS REUSED: unchanged accepted product helper and source74-test result.
- NOT RUN: fixtures and conditional reset still require corrected exact effect review.

## Changelog

- Fixed: premature unchanged-asset claim in failed export records.
- Risks: exact reset/dispatch and later clean replay remain held.

## Risks

- No generated export or released byte was changed by this correction.

## Follow-up

- Review exact corrected subject before the one conditional first job.

AIDE-Task: AIDE-DAILY-PACK-REFRESH-01
AIDE-Phase: exact-review-failure-record-correction
AIDE-Result: needs_review
AIDE-Scope: task-local wrapper, pin and retained review evidence
AIDE-Token-Impact: zero model requests; no fixture/reset replay
AIDE-Quality-Gate: source AST and pins PASS; exact effect re-review pending
