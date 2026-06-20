# AIDE-ACCEPT-MCP-SERVER-CONTRACT-01 ExecPlan

## Objective

Accept or reject the minimal contract-only MCP projection after reviewing the complete build, failed-check, repair, and repair-check chain.

## Scope

Allowed changes are limited to this acceptance task packet and evidence, `.aide/reports/mcp-server-contract-accept/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Dependencies

- `AIDE-BUILD-MCP-SERVER-CONTRACT-01`: `PASS_WITH_WARNINGS`, evidence complete.
- `AIDE-CHECK-MCP-SERVER-CONTRACT-01`: `FAILED_VALIDATION`, evidence complete and preserved.
- `AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01`: `PASS_WITH_WARNINGS`, evidence complete.
- `AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01`: `PASS_WITH_WARNINGS`, evidence complete, zero material findings, recommends this acceptance task.

## Work Plan

1. Verify the live queue and source-chain task evidence.
2. Independently inspect MCP fixtures, catalogues, runtime facts, refusal codes, and fixture hashes.
3. Consolidate acceptance scope and warning debt.
4. Materialize acceptance reports and task-local evidence.
5. Run the required validation matrix.
6. Stop at `needs_review` and recommend `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01`.

## Non-Goals

No MCP server, transport, endpoint, authorization, resource serving, prompt serving, tool execution, worker execution, provider/model/network call, PatchTransaction apply, target mutation, A2A, Host Contract, Dominium Bridge, Workbench, Runtime, Service, release, or promotion is implemented or authorized.

## Exit Criteria

The task stops at `needs_review` with `ACCEPTED_WITH_WARNINGS`, complete evidence, no unresolved material findings, preserved historical failure evidence, explicit non-capabilities, and exactly one serialized next task.
