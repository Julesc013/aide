# Q15 Prompt: Golden Tasks v0

Implement deterministic repo-local golden tasks for AIDE's token-saving workflow.

## Goal

Make quality preservation measurable by adding golden tasks that check compact task packets, context packets, verifier failures, review packets, token ledger behavior, and adapter managed-section determinism without model calls, provider calls, network, exact tokenizers, or external dependencies.

## Acceptance

- Q15 queue item exists and ends at `needs_review`.
- `.aide/policies/evals.yaml` exists.
- `.aide/evals/golden-tasks/README.md` and catalog exist.
- At least five deterministic golden tasks exist.
- AIDE Lite supports `eval list`, `eval run`, and `eval report`.
- Eval reports are written to `.aide/evals/runs/latest-golden-tasks.json` and `.aide/evals/runs/latest-golden-tasks.md`.
- Unit tests cover golden task runner behavior.
- Latest Q16 compact task packet is generated.
- Evidence and docs explain the quality-preservation workflow and remaining limits.

## Non-Goals

No Gateway, providers, model calls, network, exact tokenizer, provider billing, external coding benchmarks, LLM-as-judge, automatic review, automatic repair, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, or Q16 Outcome Controller recommendation logic.
