# Q13 Prompt: Evidence Review Workflow

Implement Q13 as a bounded queue phase.

## Objective

Build deterministic, repo-local review-packet generation so GPT-5.5 can review compact evidence, verifier output, changed-file summaries, validation outcomes, and risks without receiving full repo dumps, full chat history, or broad roadmap resynthesis.

## Required Outputs

- `.aide/prompts/evidence-review.md`
- `.aide/verification/review-packet.template.md`
- `.aide/verification/review-decision-policy.yaml`
- `.aide/context/latest-review-packet.md`
- AIDE Lite `review-pack` behavior
- Review-packet validation through validate, verify, and selftest where feasible
- `.aide/context/latest-task-packet.md` for Q14
- Tests, docs, evidence, and Q13 status `needs_review`

## Boundaries

Do not implement Gateway, providers, routing, local model setup, embeddings, vector search, exact tokenization, provider billing, golden tasks, LLM-as-judge automation, automatic GPT-5.5 calls, automatic repair, full semantic diff analysis, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, or autonomous loops.
