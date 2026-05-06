# Q14 Prompt: Token Ledger And Savings Report

Implement Q14 as a bounded queue phase.

## Objective

Build deterministic, repo-local estimated token accounting so AIDE can record compact packet sizes, compare them to named naive baselines, warn on budget or regression risk, and prove token-saving direction without storing raw prompts or claiming exact provider billing savings.

## Required Outputs

- `.aide/policies/token-ledger.yaml`
- `.aide/reports/token-ledger.jsonl`
- `.aide/reports/token-baselines.yaml`
- `.aide/reports/token-savings-summary.md`
- AIDE Lite `ledger scan`, `ledger add`, `ledger report`, and `ledger compare` behavior
- Budget status and regression warnings
- `.aide/context/latest-task-packet.md` for Q15
- Tests, docs, evidence, and Q14 status `needs_review`

## Boundaries

Do not implement Gateway, providers, routing, local model setup, exact tokenization, provider billing, real API usage accounting, golden tasks, automatic GPT review, LLM-as-judge behavior, automatic repair, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, or autonomous loops.
