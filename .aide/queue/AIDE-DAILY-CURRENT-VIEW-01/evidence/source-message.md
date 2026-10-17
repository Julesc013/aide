feat(tasks): explain current outcomes and next actions

## Summary

- Extend the existing current-task command with bounded human and JSON views.

## Why

- Task status alone hides unfinished obligations and evidence uncertainty.

## Changed

- Add explicit task selection and one public-record projection for both views.
- Preserve recorded outcome provenance and expose missing or conflicting facts.
- Refuse unsafe references and retain unknown evidence applicability.
- Add behavioral tests and prepare one finite source qualification job.

## Validation

- PASS: AST and unchanged original binding/Task OS test bytes.
- PASS: bounded scope and static input/controller inspection.
- PASS: task packet generation, refreshed full validation and doctor.
- NOT RUN: focused qualification and actual CLI smoke until exact effect review.

## Changelog

- Added: named read-only task observations and structured output.

## Risks

- Observation is not evidence acceptance or whole-client containment.
- New source is not yet a qualified distribution or release.

## Follow-up

- Execute the exact reviewed finite job, collect evidence and review the outcome.

AIDE-Task: AIDE-DAILY-CURRENT-VIEW-01
AIDE-Phase: source-and-qualification-preparation
AIDE-Result: source_candidate
AIDE-Scope: existing task CLI and bounded observers
AIDE-Token-Impact: expose useful current state without reconstructing history
AIDE-Quality-Gate: exact independent source and effect review required
