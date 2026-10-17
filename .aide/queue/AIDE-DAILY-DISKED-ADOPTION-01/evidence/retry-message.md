fix(disked): preserve pinned Git installer link identity

## Summary

- Correct the preparation preflight for the exact installed Git executable.

## Why

- The first preparation attempt stopped because that pinned binary has two links.

## Changed

- Accept exactly two links only for the known hash-pinned Git binary.
- Preserve single-link checks for source, dependencies and evidence.
- Retain the failed attempt and explicitly propose reallocation of job two.

## Validation

- PASS: exact Git path/hash/two-link/no-reparse observation and Python import.
- PASS: original failure collection hashes, quiescence and retirement.
- FAIL retained: first preparation preflight; no native input copies occurred.
- NOT RUN: corrected preparation, actual target apply and target validation.

## Changelog

- Fixed: task-local preparation no longer rejects the pinned installer layout.

## Risks

- Maximum remains two jobs; actual target validation requires a later admission.
- Native writer ownership remains pending; target effects stay held.

## Follow-up

- Review the exact repaired source and second preparation allocation before launch.

AIDE-Task: AIDE-DAILY-DISKED-ADOPTION-01
AIDE-Phase: preparation-repair
AIDE-Result: failed-attempt-preserved
AIDE-Scope: pinned-executable-preflight
AIDE-Token-Impact: unknown
AIDE-Quality-Gate: exact-independent-source-effect-review
