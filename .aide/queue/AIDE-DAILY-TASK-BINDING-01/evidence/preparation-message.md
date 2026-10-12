test(tasks): capture selected WorkUnit binding regressions

## Summary

- Prepare admitted AIDE-DAILY-TASK-BINDING-01 and independent regression oracles.

## Why

- Named task packets and verification currently lose the selected WorkUnit meaning.

## Changed

- Add ten focused tests and a bounded no-model test wrapper under existing owners.
- Preserve source unchanged for the baseline managed reproduction.
- Record actual admission and task scope before implementation.

## Validation

- PASS: independent admission accepts exact scope and at most three ordinary test jobs.
- NOT RUN: baseline and final source tests require the frozen managed jobs.
- PASS: task/queue structural preparation and Python AST checks.

## Changelog

- Added: independent selected-task regression preparation.
- Risks: source acceptance and integration remain pending.

## Risks

- No protected filesystem or model route claim follows from trusted tests.

## Follow-up

- Run and preserve baseline failures, repair existing owners, then verify and review source.

AIDE-Task: AIDE-DAILY-TASK-BINDING-01
AIDE-Phase: regression-preparation
AIDE-Result: partial
AIDE-Scope: task binding tests, bounded queue, evidence and root indexes
AIDE-Token-Impact: zero model requests; controller/reviewer usage unknown
AIDE-Quality-Gate: admission ACCEPT; actual machine/source tests pending
