test(workflows): conserve completed native tests for final recovery

## Summary

- Preserve actual160-case partial evidence and repair only controller count accounting.

## Why

- Generated fixture cases were omitted from the declared-method count; passing work remains usable.

## Changed

- Retain original exit1, actual158passes/two unavailable checks, streams and receipts.
- Correct106declared plus54generated cases and prepare exact160-result reuse.
- Final third job runs only unfinished recovery stages after transient setup.

## Validation

- PASS: every original stage stream/count/digest, quiescence and full retirement verified.
- PASS: all five new selector cases completed successfully in original native suite.
- PASS: unchanged postimages/tests, AST, input pins, scope, whitespace and structured message.
- NOT RUN: final continuation, target application or general recovery qualification.

## Changelog

- Fixed: task-local count accounting with conserved original native outcomes.

## Risks

- Two original symlink tests remain unavailable; no filesystem qualification claimed.
- Original overall failure remains; third/final job is held for exact independent review.
- Target, upstream runtime, outer containment, whole costs and release remain independent.

## Follow-up

- Review exact reuse/source/final effect, then execute final remaining stages through existing runner.
- Retain outcomes and prepare any real target effect separately.

AIDE-Task: AIDE-DAILY-DISKED-EXPORT-01
AIDE-Phase: final-conserved-native-continuation
AIDE-Result: partial-original-failure-preserved
AIDE-Scope: own orchestration and original evidence only
AIDE-Token-Impact: original98.99second suite conserved without repeat
AIDE-Quality-Gate: exact independent final effect review required
