fix(packaging): bind task imports under isolated managed Python

## Summary

- Correct demonstrated wrapper startup and preserve the original failed attempt.

## Why

- The existing managed runpy route deliberately does not add sibling module directories.

## Changed

- Load the two exact pinned task-local modules by file path without executor changes.
- Preserve actual effect ACCEPT, original exit/stderr, unchanged pack and verified retirement.
- Prepare three total bounded attempts for failed startup, corrected refresh and required replay.

## Validation

- PASS: complete unchanged prior pack comparison and failed-job collection/retirement.
- PASS: corrected AST and exact input/template binding checks.
- FAIL PRESERVED: attemptc02cac0e import failure before fixtures or reset.
- NOT RUN: corrected refresh and replay need their exact independent reviews.

## Changelog

- Fixed: isolated wrapper sibling module loading.
- Added: exact startup failure and bounded retry/replay amendment evidence.

## Risks

- Attempt-budget amendment is pending review; no reset or reserve change was performed.

## Follow-up

- Review the exact source/amendment/conditional corrected job before another allocation.

AIDE-Task: AIDE-DAILY-PACK-REFRESH-01
AIDE-Phase: demonstrated-isolated-import-repair
AIDE-Result: needs_review
AIDE-Scope: task-local imports, retained failure and bounded attempt amendment
AIDE-Token-Impact: zero model requests; no unchanged retry
AIDE-Quality-Gate: original failure preserved; exact corrected effect review pending
