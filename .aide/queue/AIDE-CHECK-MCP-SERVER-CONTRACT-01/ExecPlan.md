# AIDE-CHECK-MCP-SERVER-CONTRACT-01 ExecPlan

## Objective

Independently check `AIDE-BUILD-MCP-SERVER-CONTRACT-01` against the pinned
MCP `2025-11-25` and JSON-RPC `2.0` subset without modifying the MCP contract
implementation, fixtures, schema, tests, or build reports.

## Scope

Allowed outputs are limited to:

- the check task packet and task-local evidence;
- `.aide/reports/mcp-server-contract-check/**`;
- `.aide/queue/index.yaml`;
- `PLANS.md`;
- `IMPLEMENT.md`.

## Steps

1. Confirm the build task, Interop acceptance, commit, evidence, and next-task routing.
2. Parse MCP contract, catalogue, fixture, and build report JSON.
3. Independently inspect JSON-RPC invariants, lifecycle order, version pinning,
   capability direction, resource/tool/prompt catalogues, refusal mappings,
   transport and authorization expectations, runtime facts, and authority boundaries.
4. Run focused tests, MCP CLI status/project/validate, predecessor validators,
   broad validation, unsupported-operation probes, secret scans, and diff checks.
5. Record findings, classify warnings, and stop at `needs_review`.

## Result

The check found material fixture-alignment defects:

- list request/result fixtures use `null` for optional cursor fields;
- the MCP resource-not-found fixture uses `-32043` instead of the pinned
  resource-not-found code `-32002`.

## Non-Goals

Do not repair the implementation, edit schema/helper/tests, regenerate build
reports to conceal discrepancies, start MCP, bind sockets, send HTTP, serve
resources, execute tools, serve prompts, implement authorization, call
providers/models/network services, mutate GitHub, create branches/worktrees,
apply patches, mutate target repositories, implement A2A, Host Contract,
Dominium Bridge, Workbench, runtime, Service, or release behavior.

## Review Gate

Stop at `needs_review`.
