# Q10 Compact Implementation Prompt

## Phase

Q10 - AIDE Lite Hardening

## Goal

Harden Q09 AIDE Lite so every future phase can use compact packets, deterministic adapters, validation, estimates, and selftests instead of long chat-history prompts.

## Why

Token survival only works if the no-install workflow is reliable enough to become the default execution path. Q10 makes pack/adapt/validate/snapshot/estimate/selftest repeatable and evidence-backed.

## Context Refs

- `.aide/context/latest-task-packet.md`
- `.aide/scripts/aide_lite.py`
- `.aide/policies/token-budget.yaml`
- `.aide/prompts/compact-task.md`
- `.aide/context/ignore.yaml`
- `.aide/queue/Q09-token-survival-core/evidence/`

## Implementation

- Harden AIDE Lite command output and helper structure.
- Add deterministic writes and adapter drift detection.
- Add budget checks for project state, packets, and forbidden prompt patterns.
- Add `.aide/scripts/tests` discovery-friendly tests.
- Generate the Q11 compact task packet and write Q10 evidence.

## Validation

- `py -3 scripts/aide validate`
- `py -3 scripts/aide doctor`
- `py -3 scripts/aide self-check`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py snapshot`
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q11 Context Compiler v0"`
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`
- `py -3 .aide/scripts/aide_lite.py adapt`
- `py -3 .aide/scripts/aide_lite.py adapt`
- `py -3 .aide/scripts/aide_lite.py selftest`
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`
- `py -3 -m unittest discover -s core/harness/tests -t .`
- `py -3 -m unittest discover -s core/compat/tests -t .`
- `git diff --check`

## Evidence

Write changed files, validation, AIDE Lite hardening, determinism, token savings, and remaining-risk evidence.

## Non-Goals

No Gateway, provider calls, model routing, local models, exact tokenizer, provider billing ledger, full context compiler, full verifier, Runtime, Service, Commander, Mobile, MCP/A2A, host/app implementation, or autonomous loop.

## Acceptance

Q10 ends at `needs_review`; AIDE Lite commands pass; adapt is deterministic; snapshot stores no raw contents; pack emits Q11 packet under budget; tests and evidence are complete.
