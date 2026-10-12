test(workflows): preserve shipped pass and fix fixture report paths

## Summary

- Preserve the original partial consumer outcome and prepare the final fixture-only repair.

## Why

- All17shipped assertions passed; remaining CLI checks stopped on an unsupported fixture report destination.

## Changed

- Use admitted selected-task evidence paths without changing production writer policy.
- Preserve original full failure/receipt/stage digests and exact source-effect acceptance.
- Reuse valid shipped17PASS with pinned original result and unchanged helper/test/Python subjects.

## Validation

- PASS: original17assertions, safe import, Git baseline and named packet before failure.
- PASS: full collection/stream digests, quiescence, scratch retirement and reservation release.
- PASS: corrected AST and exact1710pins; remaining runtime NOT RUN.

## Changelog

- Fixed: proposed fixture verification-report destinations.
- Added: preserved partial outcomes and bounded completed-test reuse.

## Risks

- Final attempt2of2 requires exact independent repair/effect and actual reuse-evidence review.
- Cached17PASS is not a newly executed test or full consumer result.

## Follow-up

- Review exact repair and final effect, then run only remaining consumer qualification.

AIDE-Task: AIDE-DAILY-INSTALLED-BINDING-01
AIDE-Phase: preserved-partial-and-final-fixture-repair
AIDE-Result: needs_review
AIDE-Scope: task-local wrapper/evidence and queue/compiler coherence only
AIDE-Token-Impact: retain completed17tests without rerunning; no model jobs
AIDE-Quality-Gate: final repair/effect and completed-test reuse review held
