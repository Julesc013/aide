# AIDE-ACCEPT-INTEROP-EXPORTS-01 ExecPlan

## Objective

Accept or reject static interop export previews after build and independent
check.

## Scope

Allowed outputs are limited to:

- acceptance task packet and task-local evidence;
- `.aide/reports/interop-exports-accept/**`;
- `.aide/queue/index.yaml`;
- `PLANS.md`;
- `IMPLEMENT.md`.

## Steps

1. Verify live build/check source chain.
2. Independently verify artifact inventory, path containment, hashes, duplicate
   paths, duplicate kinds, and format structure.
3. Review queue-authority and projection-authority boundaries.
4. Review AGENTS, Claude, Copilot, Aider, MCP, and A2A preview boundaries.
5. Confirm credential safety, determinism, immutability, and no forbidden
   operations.
6. Write acceptance reports and evidence.
7. Run validation, task evidence checks, broad validation, secret scan, and
   commit-policy validation.
8. Stop at `needs_review`.

## Non-Goals

Do not modify preview artifacts, install live instruction files, start MCP or
A2A, contact external tools, execute workers, call providers/models/network
services, implement Host Contract, implement Dominium Bridge, implement
Workbench, apply PatchTransactions, create branches/worktrees, mutate GitHub,
publish releases, or mutate a target repository.

## Review Gate

Stop at `needs_review`.
