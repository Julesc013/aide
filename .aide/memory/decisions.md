# AIDE Compact Decisions

## DEC-Q09-001: Token Survival Precedes Gateway

- Date: 2026-05-06
- Decision: Build compact packets, estimates, evidence review, and validation before Gateway or provider work.
- Rationale: Prompt-size reduction comes first from smaller work packets and mechanical checks, not from a proxy without context discipline.
- Affected areas: `.aide/policies/token-budget.yaml`, `.aide/prompts/**`, `.aide/scripts/aide_lite.py`, future Q10-Q14 work.

## DEC-Q09-002: Preserve Raw Queue Nuance

- Date: 2026-05-06
- Decision: Do not rewrite Q00-Q03 or Q05/Q06 raw statuses during Q09.
- Rationale: Later review evidence permitted dependency use, but raw queue statuses remain useful forensic signals and should not be hidden by a token-survival task.
- Affected areas: `.aide/queue/index.yaml`, `.aide/queue/*/status.yaml`, Q09 evidence.

## DEC-Q09-003: Use Approximate Tokens Only

- Date: 2026-05-06
- Decision: Use `ceil(chars / 4)` for Q09 token estimates.
- Rationale: Q09 must be standard-library only and no-install; exact tokenizers and provider billing ledgers are deferred.
- Affected areas: `.aide/scripts/aide_lite.py`, `.aide/context/latest-task-packet.md`, Q09 token report.

## DEC-Q09-004: Evidence Review By Default

- Date: 2026-05-06
- Decision: GPT-5.5 review should use compact evidence packets by default and ask for more context only when the packet is insufficient.
- Rationale: Reviews should spend frontier tokens on unresolved uncertainty, not repeated project history.
- Affected areas: `.aide/prompts/evidence-review.md`, future Q13 review-pack workflow.
