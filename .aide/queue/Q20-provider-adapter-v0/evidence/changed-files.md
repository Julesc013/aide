# Q20 Changed Files

## Queue And Evidence

- `.aide/queue/index.yaml`: Q20 registered and moved to `needs_review`.
- `.aide/queue/Q20-provider-adapter-v0/**`: task packet, ExecPlan, prompt, status, and evidence.

## Provider Policy And Metadata

- `.aide/policies/provider-adapters.yaml`: offline-only provider adapter policy.
- `.aide/providers/README.md`: provider metadata directory guide.
- `.aide/providers/provider-catalog.yaml`: provider family catalog.
- `.aide/providers/capability-matrix.yaml`: conservative capability metadata.
- `.aide/providers/adapter-contract.yaml`: future adapter metadata contract.
- `.aide/providers/status.yaml`: static Q20 no-call state.
- `.aide/providers/latest-provider-status.json`: generated provider status metadata.
- `.aide/providers/latest-provider-status.md`: generated provider status summary.

## Core Code

- `core/providers/**`: standard-library provider dataclasses, registry parsing, validation, status rendering, offline probe helpers, and tests.
- `core/gateway/gateway_status.py`: provider readiness appears in local Gateway status and summaries only.

## AIDE Lite And Tests

- `.aide/scripts/aide_lite.py`: provider commands, provider validation/verification/selftest integration, provider-aware review summaries, route metadata notes, and cache surface awareness.
- `.aide/scripts/tests/test_provider_adapter.py`: AIDE Lite provider command and integration tests.

## Generated Metadata

- `.aide/context/repo-snapshot.json`
- `.aide/context/repo-map.json`
- `.aide/context/repo-map.md`
- `.aide/context/test-map.json`
- `.aide/context/context-index.json`
- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-task-packet.md`: regenerated for `Implement Q21 Existing Tool Adapter Compiler v0`.
- `.aide/context/latest-review-packet.md`: regenerated after Q20 evidence refresh.
- `.aide/cache/latest-cache-keys.json`
- `.aide/cache/latest-cache-keys.md`
- `.aide/routing/latest-route-decision.json`
- `.aide/routing/latest-route-decision.md`
- `.aide/controller/outcome-ledger.jsonl`
- `.aide/gateway/latest-gateway-status.json`
- `.aide/gateway/latest-gateway-status.md`
- `.aide/reports/token-ledger.jsonl`
- `.aide/reports/token-savings-summary.md`

## Guidance And Documentation

- `AGENTS.md`: managed token/provider guidance refreshed by `adapt`.
- `.aide/prompts/compact-task.md`
- `.aide/prompts/evidence-review.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/memory/project-state.md`
- `.aide/memory/decisions.md`
- `.aide/commands/catalog.yaml`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/reference/provider-adapter-v0.md`
- `docs/reference/README.md`
- `docs/reference/gateway-skeleton.md`
- `docs/roadmap/reboot-roadmap.md`
- `docs/roadmap/queue-roadmap.md`

## Scope Boundary

No forbidden live provider, model, network, Gateway forwarding, Runtime,
Service, Commander, UI, Mobile, MCP/A2A, `.aide.local/`, `.env`, secrets, raw
prompt logs, raw response logs, or real cache blobs were added.
