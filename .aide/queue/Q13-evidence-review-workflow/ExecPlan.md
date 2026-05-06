# Q13 ExecPlan: Evidence Review Workflow

## Purpose

Q13 implements deterministic review-packet generation so GPT-5.5 high reasoning or a human reviewer can review compact, mechanically checked evidence instead of long chat history, whole repo context, full roadmap dumps, or broad architecture resynthesis.

## Scope

Allowed work is limited to the Q13 queue packet and evidence, review decision policy/template updates, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, generated context/review/task packets, selected prompt/context/memory/catalog updates, root docs, selected reference/roadmap docs, and narrow Harness touchpoints only if clearly justified.

## Non-Goals

Q13 does not implement Gateway, providers, live model routing, local model setup, exact tokenizer support, provider billing ledger, golden tasks, LLM-as-judge automation, automatic GPT-5.5 calls, automatic repair, full semantic diff analysis, embeddings, vector search, semantic cache, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host/app implementation, or autonomous loops.

## Current Facts Verified Before Editing

- `git status --short` was clean before baseline commands.
- `py -3 scripts/aide validate` returned `PASS_WITH_WARNINGS` with 148 info, 7 warnings, and 0 errors.
- `py -3 scripts/aide doctor` returned `PASS_WITH_WARNINGS`.
- `py -3 scripts/aide self-check` returned `PASS_WITH_WARNINGS`; Q09, Q10, Q11, and Q12 are `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py validate` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py snapshot` returned `PASS`, wrote `.aide/context/repo-snapshot.json`, 613 files, no inline contents.
- `py -3 .aide/scripts/aide_lite.py index` returned `PASS`, wrote repo-map and context-index, 613 files, 559 test mappings.
- `py -3 .aide/scripts/aide_lite.py context` returned `PASS`, wrote `.aide/context/latest-context-packet.md`, 462 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q13 Evidence Review Workflow"` returned `PASS`, 775 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify` returned `WARN` only because Python test runs created transient `__pycache__` directories outside the active task allowlist.
- `py -3 .aide/scripts/aide_lite.py verify --task-packet .aide/context/latest-task-packet.md` returned the same transient-cache `WARN`.
- `py -3 .aide/scripts/aide_lite.py selftest` returned `PASS`.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .` failed with the known hidden `.aide` importability limitation.
- `py -3 -m unittest discover -s core/harness/tests -t .` passed, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .` passed, 5 tests.
- Generated manifest fingerprint drift remains visible in Harness validation.

## Milestones

- [x] Inspect Q09-Q12 outputs and run baseline validation.
- [x] Create Q13 queue packet and evidence skeleton.
- [x] Update evidence review prompt, review-packet template, and decision policy.
- [x] Extend AIDE Lite with `review-pack` and review-packet validation.
- [x] Add tests for review packet generation, validation, determinism, and selftest coverage.
- [x] Generate latest review packet and Q14 task packet.
- [x] Update docs/evidence, run final validation, and stop at review.

## Validation Plan

Run Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/pack/estimate/selftest, AIDE Lite test discovery, `git diff --check`, and targeted secret scan.

## Recovery

If interrupted, rerun `git status --short`, read this ExecPlan and `status.yaml`, inspect `.aide/scripts/aide_lite.py`, and continue from the first unchecked milestone. Generated review and context artifacts are deterministic and can be regenerated with `aide_lite.py context`, `verify --write-report`, `review-pack`, and `pack`.

## Review Gate

Q13 must end at `needs_review`. Passing Q13 requires independent review evidence.
