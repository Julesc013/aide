# Q09 Compact Implementation Prompt

## Phase

Q09 - State Reconciliation + Token Survival Core

## Goal

Make the repo's live state coherent after Q08 and add a no-install token-survival layer that generates compact task packets and evidence-review prompts for future work.

## Why

Long chat-history prompts and stale state force agents to spend tokens re-reading and re-litigating facts. Q09 replaces that with repo-derived task packets, approximate token estimates, compact project memory, and review-from-evidence discipline.

## Context Refs

- `.aide/queue/Q08-self-hosting-automation/status.yaml`
- `.aide/queue/Q08-self-hosting-automation/evidence/review.md`
- `.aide/profile.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/runs/self-check/latest.md`
- `docs/reference/source-of-truth.md`

## Implementation

- Reconcile post-Q08 state without rewriting older raw queue nuance.
- Add token budget policy, compact memory, prompt templates, and context ignore policy.
- Add stdlib-only `.aide/scripts/aide_lite.py` with doctor, validate, estimate, snapshot, pack, adapt, and selftest.
- Add focused unit tests and generate a Q10 compact task packet.
- Write Q09 evidence and stop at review.

## Validation

Run Harness validation, doctor, self-check, Harness tests, Compatibility tests, AIDE Lite commands, AIDE Lite tests, `git diff --check`, and a targeted secret scan.

## Evidence

Write changed files, validation, token survival, state reconciliation, and remaining-risk evidence under `.aide/queue/Q09-token-survival-core/evidence/`.

## Non-Goals

No Gateway, providers, router, local model setup, Runtime, Service, Commander, Mobile, MCP, A2A, cloud, autonomous loop, vector DB, semantic cache, host implementation, or broad restructuring.

## Acceptance

Q09 status ends as `needs_review`, Q10 compact task packet exists with an approximate token estimate, AGENTS.md contains token-survival guidance, validation is recorded, and no secrets or local state are committed.
