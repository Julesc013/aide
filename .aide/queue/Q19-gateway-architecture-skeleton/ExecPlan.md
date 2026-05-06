# Q19 Gateway Architecture and Skeleton ExecPlan

## Purpose

Q19 creates a local, report-only Gateway skeleton after Q09-Q18 have built the token-survival, verification, review, token ledger, golden task, outcome, routing, cache, and local-state foundations. The goal is to expose those existing repo-local signals through safe status and health surfaces without provider calls, model calls, outbound network calls, proxy forwarding, raw prompt logging, or raw response logging.

## Scope

- Add the Q19 queue packet and evidence records.
- Add `.aide/policies/gateway.yaml`.
- Add `.aide/gateway/` architecture, endpoint, lifecycle, security, and latest-status artifacts.
- Add `core/gateway/` stdlib helpers and a localhost-only HTTP skeleton.
- Add AIDE Lite `gateway` commands for `status`, `endpoints`, `smoke`, and optional `serve`.
- Add unit tests for gateway helper and endpoint behavior.
- Update root docs, prompt guidance, command catalog, memory, and generated Q20 packet/report artifacts.

## Non-Goals

- No provider calls, model calls, outbound network calls, or live routing.
- No OpenAI-compatible or Anthropic-compatible request forwarding.
- No provider adapter implementation.
- No Runtime, Service, Commander, UI, mobile, MCP, or A2A implementation.
- No raw prompt or raw response storage.
- No committed `.aide.local/` state or real cache blobs.

## Milestones

1. Register Q19 in `.aide/queue/index.yaml` and create queue/evidence skeletons.
2. Add Gateway policy and `.aide/gateway/` architecture artifacts.
3. Implement `core/gateway` status readers, endpoint payloads, and localhost-only server skeleton.
4. Wire AIDE Lite gateway commands and validation/selftest readiness checks.
5. Add tests and run targeted/core/harness/compat validation.
6. Generate Q20 compact task packet and latest Gateway status reports.
7. Fill evidence, update docs, set Q19 status to `needs_review`, and commit.

## Validation Intent

- Baseline Harness and Compatibility tests remain passing or failures are recorded.
- Gateway tests cover health, status, route explanation, summaries, version, safe 404, localhost behavior, and no raw prompt/response fields.
- AIDE Lite gateway commands produce compact status and smoke outputs without provider/model calls.
- `aide_lite.py selftest` includes gateway smoke checks.
- Direct hidden-directory unittest discovery gaps are recorded honestly if unchanged.

## Recovery Notes

If Q09-Q18 artifacts are missing or materially incomplete, stop Q19 implementation and record the blocker in Q19 evidence. If generated artifacts drift during validation, keep only Q19-allowed generated refreshes and restore out-of-scope churn before committing.
