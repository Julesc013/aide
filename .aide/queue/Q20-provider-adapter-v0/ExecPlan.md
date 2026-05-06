# Q20 Provider Adapter v0 ExecPlan

## Purpose

Q20 creates AIDE's first offline provider-adapter contract and capability metadata layer after Q09-Q19 have established compact context, verification, review packets, token accounting, golden tasks, advisory outcomes, advisory routes, cache/local-state safety, and a local Gateway skeleton. The goal is to make future provider work auditable and capability-aware without enabling any live provider calls, model calls, outbound network calls, credentials, proxy forwarding, Runtime, or UI behavior.

## Scope

- Add the Q20 queue packet and evidence records.
- Add `.aide/policies/provider-adapters.yaml`.
- Add `.aide/providers/` metadata, catalog, capability matrix, adapter contract, and latest provider status artifacts.
- Add `core/providers/` standard-library contract, registry, and status helpers.
- Add AIDE Lite `provider` commands for `list`, `status`, `validate`, `contract`, and `probe --offline`.
- Integrate provider metadata into Gateway status and route decisions as local metadata only.
- Add tests for provider contracts, metadata validation, and no-call/no-secret boundaries.
- Update root docs, prompt guidance, command catalog, memory, and generated Q21 packet/report artifacts.

## Non-Goals

- No live provider calls, model calls, provider probes, outbound network calls, or live route execution.
- No OpenAI-compatible or Anthropic-compatible request forwarding.
- No credential setup or local model setup/downloads.
- No provider billing, exact tokenizer, semantic cache, provider response cache, vector database, embeddings, MCP/A2A, Runtime, Commander, UI, mobile, or automatic repair.
- No raw prompt or raw response storage.
- No committed `.aide.local/` state, `.env`, secrets, or real cache blobs.

## Milestones

1. Register Q20 in `.aide/queue/index.yaml` and create queue/evidence skeletons.
2. Add provider-adapter policy and `.aide/providers/` metadata artifacts.
3. Implement `core/providers` contracts, registry validation, and status rendering.
4. Wire AIDE Lite provider commands plus validation/doctor/selftest readiness checks.
5. Integrate provider status into Gateway summaries and route decision metadata without forwarding or execution.
6. Add provider unit tests and AIDE Lite command tests.
7. Generate latest provider status, Gateway status, route/cache/token/context artifacts, and Q21 compact task packet.
8. Fill evidence, update docs, set Q20 status to `needs_review`, and commit.

## Validation Intent

- Baseline Harness, Compatibility, Gateway, and AIDE Lite checks remain passing or failures are recorded.
- Provider tests cover metadata contracts, catalog/capability parsing, no-secret validation, local/remote/human/deterministic classification, and no-call boundaries.
- AIDE Lite provider commands produce compact metadata-only status without credentials or live calls.
- Gateway status can reference provider metadata readiness without adding provider forwarding.
- Route explain can reference provider metadata candidates as advisory metadata without execution.
- Direct hidden-directory unittest discovery gaps are recorded honestly if unchanged.

## Recovery Notes

If Q09-Q19 artifacts are missing or materially incomplete, stop Q20 implementation and record the blocker in Q20 evidence. If validation refreshes generated artifacts outside the Q20 allowlist, restore those paths before committing. If provider metadata would require secrets, live probes, pricing claims, or provider-specific measured capability assertions, defer it to a future reviewed queue item.

## Progress

- Milestone 1 complete: Q20 queue packet and queue index entry exist.
- Milestone 2 complete: provider-adapter policy and `.aide/providers/**` metadata artifacts exist.
- Milestone 3 complete: `core/providers/**` contracts, registry validation, and status rendering exist.
- Milestone 4 complete: AIDE Lite provider commands and readiness checks are implemented.
- Milestone 5 complete: Gateway status and route decisions reference provider metadata without forwarding or execution.
- Milestone 6 complete: provider unit tests and AIDE Lite provider command tests pass.
- Milestone 7 complete: latest provider status, Gateway status, route/cache/token artifacts, and Q21 compact task packet were generated.
- Milestone 8 complete: evidence/docs were updated and Q20 status is `needs_review`.
