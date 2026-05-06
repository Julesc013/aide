# Q10 ExecPlan: AIDE Lite Hardening

## Purpose

Q10 hardens the Q09 no-install token-survival workflow so compact task packets, token estimates, adapter guidance, validation, and selftests can be used repeatedly for future AIDE phases.

## Scope

Allowed work is limited to the Q10 queue packet and evidence, `.aide/scripts/aide_lite.py`, its tests, token-survival policy/prompt/context/memory records, generated context outputs, AGENTS token-survival guidance, root docs, and narrow Harness/doc integration when needed.

## Non-Goals

Q10 does not implement Gateway, provider calls, live model routing, local model setup, exact tokenizer dependencies, provider billing ledgers, full context compiler, full verifier, Commander, UI, Mobile, MCP/A2A, Runtime, Service, host implementation, or autonomous loops.

## Current Facts Verified Before Editing

- `git status --short` was clean.
- `py -3 scripts/aide validate` returned `PASS_WITH_WARNINGS` with 149 info, 6 warnings, and 0 errors.
- `py -3 scripts/aide doctor` returned `PASS_WITH_WARNINGS` and recommended Q09 review.
- `py -3 scripts/aide self-check` returned `PASS_WITH_WARNINGS`; Q09 is `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py validate` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py selftest` returned `PASS`.
- Harness tests passed: 17 tests.
- Compatibility tests passed: 5 tests.
- Q09 outputs are present: `.aide/scripts/aide_lite.py`, `.aide/context/latest-task-packet.md`, `.aide/context/repo-snapshot.json`, token-budget policy, prompts, memory, and evidence.

## Milestones

- [x] Inspect Q09 outputs and run baseline validation.
- [x] Create Q10 queue packet and evidence skeleton.
- [x] Harden AIDE Lite command structure, deterministic writes, drift detection, budget checks, and packet rendering.
- [x] Add importable tests, including the requested `.aide/scripts/tests` discovery path.
- [x] Generate Q11 compact task packet, adapt guidance, write evidence, run final validation, and stop at review.

## Validation Plan

Run Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/pack/estimate/adapt/adapt/selftest, `.aide/scripts/tests` unittest discovery, `git diff --check`, and targeted secret scan.

## Recovery

If interrupted, rerun `git status --short`, read this ExecPlan and `status.yaml`, inspect `.aide/scripts/aide_lite.py`, and continue from the first unchecked milestone. Generated packet/snapshot outputs are deterministic and can be regenerated.

## Review Gate

Q10 must end at `needs_review`. Passing Q10 requires independent review evidence.
