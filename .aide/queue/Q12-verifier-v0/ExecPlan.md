# Q12 ExecPlan: Verifier v0

## Purpose

Q12 implements the first deterministic repo-local Verifier. It should make future AIDE work cheaper and safer by mechanically checking task packets, evidence packets, file references, changed-file scope, adapter drift, context packet shape, token warnings, and obvious secret risks before GPT-5.5 or another premium model receives a compact review packet.

## Scope

Allowed work is limited to the Q12 queue packet and evidence, `.aide/verification/**`, `.aide/policies/verification.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, selected prompt/context/memory updates, optional command catalog metadata, root docs, selected reference/roadmap docs, and narrow Harness touchpoints only if clearly justified.

## Non-Goals

Q12 does not implement Gateway, providers, live model routing, local model setup, exact tokenizer support, provider billing ledger, golden tasks, LLM-as-judge, automatic repair, embeddings, vector search, semantic cache, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host/app implementation, or autonomous loops.

## Current Facts Verified Before Editing

- `git status --short` was clean before baseline commands.
- `py -3 scripts/aide validate` returned `PASS_WITH_WARNINGS` with 148 info, 7 warnings, and 0 errors.
- `py -3 scripts/aide doctor` returned `PASS_WITH_WARNINGS`.
- `py -3 scripts/aide self-check` returned `PASS_WITH_WARNINGS`; Q09, Q10, and Q11 are `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py validate` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py snapshot` returned `PASS`, action `unchanged`, 594 files, no inline contents.
- `py -3 .aide/scripts/aide_lite.py index` returned `PASS`, action `unchanged`, 594 files, 542 test mappings.
- `py -3 .aide/scripts/aide_lite.py context` returned `PASS`, wrote `.aide/context/latest-context-packet.md`, 464 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q12 Verifier v0"` returned `PASS`, 736 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` returned `PASS`, 736 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py selftest` returned `PASS`.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .` failed with the known hidden `.aide` importability limitation.
- `py -3 -m unittest discover -s core/harness/tests -t .` passed, 22 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .` passed, 5 tests.
- Generated manifest fingerprint drift remains visible in Harness validation.

## Milestones

- [x] Inspect Q09/Q10/Q11 outputs and run baseline validation.
- [x] Create Q12 queue packet and evidence skeleton.
- [x] Add verification policy and evidence/review/diff/file-ref/secret templates.
- [x] Extend AIDE Lite with verify command, report rendering, refs, diff scope, and secret checks.
- [x] Add tests and fixtures for verifier behavior.
- [x] Generate latest verification report and Q13 task packet.
- [x] Update docs/evidence, run final validation, and stop at review.

## Validation Plan

Run Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/pack/estimate/verify/selftest, AIDE Lite test discovery, `git diff --check`, and targeted secret scan.

## Recovery

If interrupted, rerun `git status --short`, read this ExecPlan and `status.yaml`, inspect `.aide/scripts/aide_lite.py`, and continue from the first unchecked milestone. Generated context and verification artifacts are deterministic and can be regenerated with `aide_lite.py index`, `context`, `pack`, and `verify --write-report`.

## Review Gate

Q12 must end at `needs_review`. Passing Q12 requires independent review evidence.
