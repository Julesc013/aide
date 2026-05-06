# Q15 ExecPlan: Golden Tasks v0

## Purpose

Q15 implements deterministic repo-local golden tasks for the AIDE token-saving workflow. Q14 measures packet/report size; Q15 checks that smaller artifacts still preserve required sections, references, evidence, verifier behavior, review packet shape, ledger metadata, and managed guidance determinism.

## Scope

Allowed work is limited to the Q15 queue packet and evidence, `.aide/policies/evals.yaml`, `.aide/evals/**`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, generated eval/context/review/token report updates, selected prompt/memory/catalog updates, root docs, selected reference/roadmap docs, and narrow Harness touchpoints only if clearly justified.

## Non-Goals

Q15 does not implement Gateway, live model routing, provider calls, local model setup, OpenAI/Anthropic-compatible APIs, exact tokenization, provider billing, real API usage accounting, external coding benchmarks, SWE-bench, LLM-as-judge behavior, automatic GPT review, automatic repair, Q16 Outcome Controller recommendations, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host/app behavior, or autonomous loops.

## Current Facts Verified Before Editing

- `git status --short` was clean before baseline commands.
- `py -3 scripts/aide validate` returned `PASS_WITH_WARNINGS` with 148 info, 7 warnings, and 0 errors.
- `py -3 scripts/aide doctor` returned `PASS_WITH_WARNINGS`.
- `py -3 scripts/aide self-check` returned `PASS_WITH_WARNINGS`; Q09 through Q14 are `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py validate` returned `PASS`; Q14 review packet had no hard over-budget issue.
- `py -3 .aide/scripts/aide_lite.py snapshot`, `index`, `context`, `review-pack`, `ledger scan`, and `ledger report` ran before edits and refreshed generated context/review/ledger artifacts.
- `py -3 .aide/scripts/aide_lite.py verify` returned `WARN` before cache cleanup because Python tests created transient `__pycache__` directories.
- `py -3 .aide/scripts/aide_lite.py selftest` returned `PASS`.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .` failed with the known hidden `.aide` importability limitation.
- `py -3 -m unittest discover -s core/harness/tests -t .` passed, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .` passed, 5 tests.

## Milestones

- [x] Inspect Q09-Q14 outputs and run baseline validation.
- [ ] Create Q15 queue packet and evidence skeleton.
- [ ] Add golden task policy, README, catalog, tasks, and fixtures.
- [ ] Extend AIDE Lite with eval list/run/report, deterministic report writing, and command integrations.
- [ ] Add tests for golden task loading, pass/fail behavior, reports, and selftest integration.
- [ ] Generate latest golden-task reports, Q16 task packet, review packet, and token summary.
- [ ] Update docs/evidence, run final validation, and stop at review.

## Validation Plan

Run Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger scan/ledger report/eval list/eval run/eval report/pack/estimate/selftest, AIDE Lite test discovery, `git diff --check`, and targeted secret scan.

## Recovery

If interrupted, rerun `git status --short`, read this ExecPlan and `status.yaml`, inspect `.aide/scripts/aide_lite.py`, and continue from the first unchecked milestone. Generated eval reports can be regenerated with `py -3 .aide/scripts/aide_lite.py eval run`.

## Review Gate

Q15 must end at `needs_review`. Passing Q15 requires independent review evidence.
