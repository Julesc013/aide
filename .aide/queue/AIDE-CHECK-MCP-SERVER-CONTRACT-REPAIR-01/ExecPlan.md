# AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01 ExecPlan

## Objective

Independently recheck `AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01` without
modifying MCP implementation, schema, tests, fixtures, build reports, repair
reports, or predecessor evidence.

## Scope

Allowed outputs are limited to the repair-check task packet/evidence,
`.aide/reports/mcp-server-contract-repair-check/**`, `.aide/queue/index.yaml`,
`PLANS.md`, and `IMPLEMENT.md`.

## Steps

1. Verify the build, failed-check, and repair source chain.
2. Independently parse and inspect MCP JSON fixtures for cursor and
   resource-not-found correctness.
3. Verify validator hardening with temporary in-memory invalid fixtures.
4. Re-run focused tests, MCP CLI status/project/validate, predecessor
   validators, broad validation, unsupported-operation probes, and
   immutability checks.
5. Record findings, warnings, and next-task recommendation.

## Result

The two material defects recheck as fixed. The task stops at `needs_review` with
`PASS_WITH_WARNINGS`.

## Non-Goals

Do not repair implementation, modify fixtures/schema/helper/tests, rewrite the
failed check, accept MCP, download MCP SDKs or schemas, install dependencies,
start servers, bind sockets, send HTTP, implement authorization, serve resources
or prompts, execute tools, dispatch workers, call providers/models/network
services, implement A2A/Host Contract/Dominium Bridge/Workbench, apply
PatchTransactions, mutate target repositories, create branches/worktrees, mutate
GitHub, release, or promote.

## Review Gate

Stop at `needs_review`.
