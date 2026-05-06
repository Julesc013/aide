# Q16 Prompt: Outcome Controller v0

Implement deterministic repo-local advisory outcome analysis for AIDE.

## Goal

Read local signals from token reports, verifier reports, review packets,
golden-task reports, context artifacts, validation outcomes, and controller
ledger records, then generate bounded recommendations without automatic
mutation.

## Acceptance

- Q16 queue item exists and ends at `needs_review`.
- `.aide/policies/controller.yaml` exists.
- `.aide/controller/README.md`, `failure-taxonomy.yaml`,
  `outcome-ledger.jsonl`, `latest-outcome-report.md`, and
  `latest-recommendations.md` exist.
- AIDE Lite supports `outcome report` and `optimize suggest`.
- Recommendations include evidence source, expected benefit, risk level,
  next action, rollback condition, and `applies_automatically: false`.
- Unit tests cover outcome records, signal readers, recommendation behavior,
  and selftest integration.
- Latest Q17 compact task packet is generated.
- Evidence and docs explain the advisory-only safety boundary and remaining
  limits.

## Non-Goals

No Gateway, providers, model calls, network, exact tokenizer, provider billing,
real routing, automatic prompt/policy/route mutation, autonomous loop,
Commander, UI, Mobile, MCP/A2A, host behavior, automatic GPT review,
LLM-as-judge, or automatic code repair.
