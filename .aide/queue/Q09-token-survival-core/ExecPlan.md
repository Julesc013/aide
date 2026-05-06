# Q09 ExecPlan: State Reconciliation And Token Survival Core

## Purpose

Q09 reconciles post-Q08 live state and creates the first repo-only token-survival loop. The work must make the next Codex prompt smaller immediately while preserving queue discipline, evidence, and review gates.

## Scope

Allowed changes are limited to Q09 queue records and evidence, post-Q08 state metadata, token budget policy, compact memory, prompt templates, context ignore policy, AIDE Lite token-survival tooling, narrow Harness metadata needed for Q09 visibility, root docs, and generated outputs produced through reviewed local commands.

## Non-Goals

Q09 does not implement Gateway, providers, local model setup, Runtime, Service, Commander, Mobile, MCP, A2A, autonomous loops, semantic cache, vector search, or host/app surfaces.

## Current Facts Verified Before Editing

- `git status --short` was clean.
- `py -3 scripts/aide validate` returned `PASS_WITH_WARNINGS` with 148 info, 7 warnings, and 0 errors.
- `py -3 scripts/aide doctor` returned `PASS_WITH_WARNINGS` and recommended post-Q08 foundation review.
- `py -3 scripts/aide self-check` reported Q08 as `passed` with `PASS_WITH_NOTES`.
- Harness tests passed: 10 tests.
- Compatibility tests passed: 5 tests.
- `.aide/runs/self-check/latest.md` was stale and still showed Q08 as `needs_review`.

## Milestones

- [x] Inspect governing docs and baseline validation.
- [x] Create Q09 queue packet and initial evidence placeholders.
- [ ] Reconcile post-Q08 profile, command catalog, root docs, and self-check wording.
- [ ] Add token budget, compact memory, prompt templates, and context ignore policy.
- [ ] Implement AIDE Lite commands and tests.
- [ ] Generate Q10 compact task packet, refresh allowed outputs, run validation, write final evidence, and stop at review.

## Validation Plan

Run the required Harness commands, AIDE Lite commands, unit tests, `git diff --check`, and a targeted secret scan. Record every command and result in `evidence/validation.md`.

## Recovery

All generated outputs are deterministic and can be regenerated from repo state. If Q09 is interrupted, rerun `git status --short`, read this ExecPlan, inspect `status.yaml`, and continue from the first incomplete milestone without widening scope.

## Review Gate

Q09 must end at `needs_review`. Passing Q09 requires independent review evidence.
