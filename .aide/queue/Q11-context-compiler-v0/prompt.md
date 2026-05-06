# Q11 Prompt: Context Compiler v0

Implement Q11 as a bounded queue phase.

## Objective

Build deterministic, repo-local context compiler behavior so future tasks can use compact repo maps, test maps, context indexes, exact refs, and context packets instead of whole-repo prompts or long chat history.

## Required Outputs

- `.aide/context/compiler.yaml`
- `.aide/context/priority.yaml`
- `.aide/context/excerpt-policy.yaml`
- `.aide/context/repo-map.json`
- `.aide/context/repo-map.md`
- `.aide/context/test-map.json`
- `.aide/context/context-index.json`
- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-task-packet.md` for Q12
- AIDE Lite `index` and `context` behavior
- Tests, docs, evidence, and Q11 status `needs_review`

## Boundaries

Do not implement Gateway, providers, routing, local model setup, embeddings, vector search, exact tokenization, provider billing, Q12 verifier, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, or autonomous loops.
