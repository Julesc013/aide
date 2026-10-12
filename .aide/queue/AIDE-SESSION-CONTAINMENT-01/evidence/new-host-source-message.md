fix(qualification): bind the actual new-host native prerequisite

## Summary

- Prepare AIDE-SESSION-CONTAINMENT-01 for the actual new host using its existing owner.
- Correct native Windows CLI command syntax and support complete explicit executor pins.

## Why

- The new client uses sandbox followed directly by its workload, without windows.
- Old host, executable and resource identities cannot qualify the new machine.

## Changed

- Add three pure binding/syntax regressions alongside five retained refusal cases.
- Prepare exact local resource selection and source-check/native job templates.
- Preserve the mistaken help attempt and original old-host results.
- Update bounded SESSION planning and root indexes without runtime-owner changes.

## Validation

- PASS: AST parsing of the three task-local Python files and diff preparation.
- NOT RUN: eight pure regressions require the reviewed setup/source-check effect.
- NOT RUN: strict native dispatch remains a separately reviewed later effect.
- PASS: no model or target effect is part of the prepared candidate.

## Changelog

- Fixed: task-local Windows native prerequisite command syntax.
- Added: explicit complete host/backend binding and bounded new-host preparation.
- Risks: actual native editing and whole-session containment remain unqualified.

## Risks

- Setup, source tests and native effects need exact independent review and fresh admission.
- The earlier mistaken default invocation has unknown persistent effects.

## Follow-up

- Review setup/source-check effects, collect passing tests, then review the native effect.

AIDE-Task: AIDE-SESSION-CONTAINMENT-01
AIDE-Phase: new-host-prerequisite-preparation
AIDE-Result: partial
AIDE-Scope: task-local probe, tests, exact effect preparation and current indexes
AIDE-Token-Impact: zero requested models; controller/reviewer usage unknown
AIDE-Quality-Gate: preparation PASS; machine/source/effect verdicts pending
