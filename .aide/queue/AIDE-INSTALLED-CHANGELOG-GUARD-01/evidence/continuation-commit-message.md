test(changelog): conserve export and isolate remaining checks

## Summary

- Preserve completed export and correct the remaining-stage job recipe.

## Why

- The prior recipe pinned mutable generated output as immutable input, causing its next diagnostic to refuse.

## Changed

- Retain the original failed job and exact generated payload.
- Prepare an explicit one-job continuation amendment without reset or rebuild.
- Separate generated changelog output from immutable inputs.

## Validation

- PASS: ten source methods, six ownership tests, export and unchanged published assets.
- FAIL: post-export doctor admission from the recipe mismatch, preserved.
- NOT RUN: remaining diagnostics and actual consumers.

## Changelog

- Changed: development payload contains the qualified installed-changelog source.

## Risks

- Original two-job ceiling is exhausted; only exact review of the explicit amendment can authorize continuation.
- Main remains gated; no published release or real target changes.

## Follow-up

- Complete only unrun stages and review actual outcomes before integration.

AIDE-Task: AIDE-INSTALLED-CHANGELOG-GUARD-01
AIDE-Phase: remaining-stage-amendment
AIDE-Result: export-conserved-consumers-pending
AIDE-Scope: generated-pack-and-continuation-recipe
AIDE-Token-Impact: unknown
AIDE-Quality-Gate: exact-independent-amendment-and-effect-review
