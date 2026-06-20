# AIDE-BUILD-MCP-SERVER-CONTRACT-01 ExecPlan

## Objective

Build a minimal, deterministic, contract-only MCP projection for AIDE after
acceptance of `static_interop_export_previews`.

## Scope

Allowed outputs are limited to:

- the MCP contract schema;
- `core/interop` helper code;
- thin AIDE Lite `mcp-server-contract` dispatch;
- focused MCP contract tests;
- `.aide/interop/mcp/**` generated contract/catalogue/fixture projections;
- `.aide/reports/mcp-server-contract/**`;
- the task-local queue packet and evidence;
- queue index and root planning/execution logs.

## Steps

1. Verify live queue truth and Interop Exports source chain.
2. Add the schema, helper, CLI dispatch, and tests.
3. Generate deterministic MCP contract, catalogues, fixtures, and reports.
4. Verify schema/helper alignment, JSON-RPC fixtures, catalogues, refusal
   mappings, transport and authorization expectations, and runtime facts.
5. Run focused tests, predecessor validators, broad validation, JSON parsing,
   deterministic projection, source immutability, secret-like scan, and
   commit-policy validation.
6. Stop at `needs_review` and recommend `AIDE-CHECK-MCP-SERVER-CONTRACT-01`.

## Non-Goals

Do not start a live MCP server, implement stdio or Streamable HTTP transport,
bind ports, open sockets, send network requests, implement authentication,
serve resources, invoke tools, serve prompts, dispatch workers, call models or
providers, apply patches, mutate branches/worktrees/GitHub/target repositories,
or implement A2A, Host Contract, Dominium Bridge, Workbench, Runtime, Service,
scheduler, leases, supervisor, release, or promotion behavior.

## Review Gate

Stop at `needs_review`.
