# Q11 ExecPlan: Context Compiler v0

## Purpose

Q11 implements the first deterministic repo-local Context Compiler. The goal is to make future AIDE work use repo maps, test maps, context indexes, exact refs, and compact context packets rather than long chat history, whole-repo prompts, or repeated broad documentation dumps.

## Scope

Allowed work is limited to the Q11 queue packet and evidence, `.aide/context/**`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, selected token-survival prompts/memory/config, optional command catalog metadata, root docs, selected reference/roadmap docs, and narrow Harness touchpoints only if clearly justified.

## Non-Goals

Q11 does not implement Gateway, providers, live model routing, local model setup, exact tokenizer, provider billing ledger, embeddings, vector search, semantic cache, Q12 verifier behavior, Q14 ledger formalization, Q15 golden tasks, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host/app implementation, or autonomous loops.

## Current Facts Verified Before Editing

- `git status --short` was clean.
- `py -3 scripts/aide validate` returned `PASS_WITH_WARNINGS` with 149 info, 6 warnings, and 0 errors.
- `py -3 scripts/aide doctor` returned `PASS_WITH_WARNINGS`.
- `py -3 scripts/aide self-check` returned `PASS_WITH_WARNINGS`; Q09 and Q10 are both `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py validate` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py snapshot` returned `PASS`, action `unchanged`, 581 files, no inline contents.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q11 Context Compiler v0"` returned `PASS`, action `unchanged`, 2,566 chars, 642 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` returned `PASS`, 642 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py adapt` returned `PASS`, action `unchanged`.
- `py -3 .aide/scripts/aide_lite.py selftest` returned `PASS`.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .` failed with the known hidden `.aide` importability limitation.
- `py -3 -m unittest discover -s core/harness/tests -t .` passed, 20 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .` passed, 5 tests.
- `.aide/profile.yaml` still names Q09 as current focus, but Q11 does not allow profile edits; this remains visible nuance.

## Milestones

- [x] Inspect Q09/Q10 outputs and run baseline validation.
- [x] Create Q11 queue packet and evidence skeleton.
- [x] Add context compiler config files.
- [x] Extend AIDE Lite with index/context/map behavior and context-aware pack output.
- [x] Generate repo-map, test-map, context-index, latest-context-packet, and Q12 task packet.
- [x] Add tests for role classification, ignored paths, maps, context packets, refs, and validation.
- [x] Update docs/evidence, run final validation, and stop at review.

## Validation Plan

Run Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/pack/estimate/adapt/adapt/selftest, `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scan.

## Recovery

If interrupted, rerun `git status --short`, read this ExecPlan and `status.yaml`, inspect `.aide/scripts/aide_lite.py`, and continue from the first unchecked milestone. Generated context artifacts are deterministic and can be regenerated with `aide_lite.py index` and `aide_lite.py context`.

## Review Gate

Q11 must end at `needs_review`. Passing Q11 requires independent review evidence.
