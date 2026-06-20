# AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01 ExecPlan

## Objective

Build a minimal, deterministic, contract-only A2A agent-card projection for AIDE
after acceptance of `minimal_mcp_server_contract`.

## Scope

Allowed outputs are limited to:

- the A2A agent-card contract schema;
- `core/interop` helper code;
- thin AIDE Lite `a2a-agent-card-contract` dispatch;
- focused A2A agent-card contract tests;
- `.aide/interop/a2a/**` generated contract/catalogue projections;
- `.aide/reports/a2a-agent-card-contract/**`;
- the task-local queue packet and evidence;
- queue index and root planning/execution logs.

## Steps

1. Verify live queue truth and MCP acceptance baseline.
2. Add the schema, helper, CLI dispatch, and tests.
3. Generate deterministic A2A agent-card contract, skill/catalogue, refusal,
   conformance, and report artifacts.
4. Verify schema/helper alignment, agent-card shape, skill safety, security and
   refusal boundaries, deterministic projection, source immutability, and
   runtime facts.
5. Run focused tests, predecessor validators, broad validation, JSON parsing,
   unsupported command probes, secret-like scan, diff checks, and commit-policy
   validation.
6. Stop at `needs_review` and recommend
   `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01`.

## Non-Goals

Do not start a live A2A endpoint, register an agent, implement authentication,
delegate tasks, dispatch workers, call models or providers, call network
services, implement Host Contract, Dominium Bridge, Workbench, Runtime, Service,
apply PatchTransactions, mutate branches/worktrees/GitHub/target repositories,
or publish release/promotion artifacts.

## Review Gate

Stop at `needs_review`.
