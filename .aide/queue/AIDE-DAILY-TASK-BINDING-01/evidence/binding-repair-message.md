chore(tasks): refresh the tested helper evidence binding

## Summary

- Correct the one stale derived binding identified by independent source review.

## Why

- Current evidence must identify the final tested helper rather than an earlier edit.

## Changed

- Explicitly refresh capability evidence and preserve the actual REQUEST_CHANGES verdict.
- Retain final structural logs/digests and prior failed observations.

## Validation

- PASS: helper bytes match testedfc8a68b7 and refreshed SHAba7f4957.
- PASS REUSED: 74 tests under unchanged production, tests and execution inputs.
- FAIL PRESERVED: only two current-export provenance failures plus doctor aggregate failure.

## Changelog

- Fixed: stale derived source binding for the task preparation helper.
- Risks: exact source re-review and package qualification remain open.

## Risks

- No source test replay or change to the provenance assertions.

## Follow-up

- Review exact corrected candidate, then admit package refresh preparation.

AIDE-Task: AIDE-DAILY-TASK-BINDING-01
AIDE-Phase: independent-review-binding-repair
AIDE-Result: needs_review
AIDE-Scope: explicit capability-derived refresh and exact structural evidence
AIDE-Token-Impact: zero model requests; no repeated source test job
AIDE-Quality-Gate: source unchanged PASS74; structural provenance FAIL retained; re-review pending
