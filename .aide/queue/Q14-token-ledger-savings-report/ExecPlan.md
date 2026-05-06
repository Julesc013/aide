# Q14 ExecPlan: Token Ledger And Savings Report

## Purpose

Q14 implements the first formal estimated token ledger so AIDE can measure compact task, context, review, verification, evidence, prompt, and baseline surfaces using the repo-local `chars / 4` approximation. The phase turns token saving from a claim into reviewable metadata while keeping raw prompts and responses out of committed records.

## Scope

Allowed work is limited to the Q14 queue packet and evidence, token ledger policy, `.aide/reports/**`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, generated Q14/Q15 packet and report updates, selected prompt/context/memory/catalog updates, root docs, selected reference/roadmap docs, and narrow Harness touchpoints only if clearly justified.

## Non-Goals

Q14 does not implement Gateway, live model routing, provider calls, local model setup, OpenAI/Anthropic-compatible APIs, exact tokenization, provider billing integration, real API usage accounting, reasoning-token accounting, cached-token accounting, golden tasks, automatic GPT review, LLM-as-judge behavior, automatic repair, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host/app implementation, or autonomous loops.

## Current Facts Verified Before Editing

- `git status --short` was clean before baseline commands.
- `py -3 scripts/aide validate` returned `PASS_WITH_WARNINGS` with 148 info, 7 warnings, and 0 errors.
- `py -3 scripts/aide doctor` returned `PASS_WITH_WARNINGS`.
- `py -3 scripts/aide self-check` returned `PASS_WITH_WARNINGS`; Q09 through Q13 are `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py validate` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py snapshot` returned `PASS`, wrote `.aide/context/repo-snapshot.json`, 625 files, and no inline contents.
- `py -3 .aide/scripts/aide_lite.py index` returned `PASS`, wrote repo-map and context-index, 625 files, and 570 test mappings.
- `py -3 .aide/scripts/aide_lite.py context` returned `PASS`, wrote `.aide/context/latest-context-packet.md`, 465 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify` returned `WARN` because baseline test discovery created transient `__pycache__` directories outside the active task allowlist.
- `py -3 .aide/scripts/aide_lite.py review-pack` returned `PASS`, wrote `.aide/context/latest-review-packet.md`, 1,811 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` returned `PASS`, 806 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md` returned `PASS`, 1,811 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py selftest` returned `PASS`.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .` failed with the known hidden `.aide` importability limitation.
- `py -3 -m unittest discover -s core/harness/tests -t .` passed, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .` passed, 5 tests.
- Generated manifest fingerprint drift remains visible in Harness validation.

## Milestones

- [x] Inspect Q09-Q13 outputs and run baseline validation.
- [ ] Create Q14 queue packet and evidence skeleton.
- [ ] Add token ledger policy and baseline report scaffolds.
- [ ] Extend AIDE Lite with ledger scan/add/report/compare, budget status, and regression warnings.
- [ ] Add tests for ledger records, baselines, budget status, regression warnings, and raw-content exclusion.
- [ ] Generate ledger records, savings summary, review packet if needed, and Q15 task packet.
- [ ] Update docs/evidence, run final validation, and stop at review.

## Validation Plan

Run Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger scan/ledger report/ledger compare/pack/estimate/selftest, AIDE Lite test discovery, `git diff --check`, and targeted secret scan.

## Recovery

If interrupted, rerun `git status --short`, read this ExecPlan and `status.yaml`, inspect `.aide/scripts/aide_lite.py`, and continue from the first unchecked milestone. Generated token reports are deterministic enough to regenerate with `aide_lite.py ledger scan`, `ledger report`, and `ledger compare`.

## Review Gate

Q14 must end at `needs_review`. Passing Q14 requires independent review evidence.
