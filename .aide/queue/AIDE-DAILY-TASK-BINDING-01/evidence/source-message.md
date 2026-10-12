fix(tasks): keep selected WorkUnit identity through preparation

## Summary

- Bind compact preparation, verification and review evidence to the selected WorkUnit.

## Why

- Eight independently authored baseline assertions demonstrate identity and scope loss.

## Changed

- Reuse the existing bounded packet parser and project real queue scope for known tasks.
- Refuse invalid explicit declarations without unrelated scope fallback.
- Retain ten original regressions and add seven refusal/consistency/portable identity checks.
- Preserve baseline receipt, full output, collection and retirement evidence.

## Validation

- PASS: baseline collection/retirement, source AST and real named packet preparation.
- FAIL PRESERVED: original eight failures among ten baseline tests, zero errors/skips.
- NOT RUN: repaired source and legacy compatibility tests require the next frozen job.
- FAIL PRESERVED: doctor/validate detect stale current-source export provenance; old export and released assets stay untouched pending separately admitted regeneration/replay.

## Changelog

- Fixed: selected task identity in compact preparation and changed-file scope verification.
- Added: named task scope documentation and refusal regressions.

## Risks

- Legacy generic fallback is retained only for compatibility and conveys no authority.
- Source acceptance, integration and protected/model routes remain separate.

## Follow-up

- Run repaired source/compatibility checks, retain results and obtain exact independent review.

AIDE-Task: AIDE-DAILY-TASK-BINDING-01
AIDE-Phase: source-repair
AIDE-Result: partial
AIDE-Scope: existing task identity, packet, verification and evidence owners
AIDE-Token-Impact: zero model requests; whole-task model accounting unknown
AIDE-Quality-Gate: baseline reproduced; repaired tests and exact source acceptance pending
