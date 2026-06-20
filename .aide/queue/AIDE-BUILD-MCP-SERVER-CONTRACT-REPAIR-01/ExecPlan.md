# AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01 ExecPlan

## Objective

Repair only the two material MCP contract fixture defects found by
`AIDE-CHECK-MCP-SERVER-CONTRACT-01`.

## Scope

Allowed implementation changes are limited to the MCP contract helper,
focused MCP tests, affected generated MCP fixtures/reports, the repair task
packet/evidence, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Steps

1. Verify the build/check source chain and failed-check evidence.
2. Repair pagination fixture generation so absent cursors are omitted and
   present cursors must be strings.
3. Repair `resource-not-found-refusal.json` to use MCP Resources code `-32002`.
4. Harden `validate_fixtures()` so the old defects fail validation.
5. Add focused regression tests for null/non-string cursors, valid opaque
   string cursors, standard resource-not-found, and preserved custom refusals.
6. Regenerate only affected MCP contract artifacts and reports.
7. Record task evidence, run validation, and stop at `needs_review`.

## Result

The repair is complete and awaits independent recheck.

## Non-Goals

Do not accept the MCP contract, erase the failed check, implement a live MCP
server, install MCP SDKs, add dependencies, bind sockets, send HTTP, create
sessions, implement OAuth, serve resources/prompts, execute tools, dispatch
workers, call providers/models/network services, implement A2A, Host Contract,
Dominium Bridge, Workbench, PatchTransaction apply, branch/worktree automation,
GitHub mutation, release, promotion, or target-repository mutation.

## Review Gate

Stop at `needs_review` and recommend
`AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01`.
