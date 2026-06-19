# AIDE-BUILD-INTEROP-EXPORTS-01 ExecPlan

## Objective

Build static, deterministic, report-only interop export previews after
ContextPack v2 acceptance.

## Scope

Allowed outputs are limited to:

- the task-local queue packet and evidence;
- `.aide/interop/exports/**`;
- `.aide/reports/interop-exports/**`;
- queue index and root planning/documentation logs.

## Steps

1. Verify live queue truth and source chain.
2. Materialize static preview artifacts.
3. Record artifact hashes in manifest and reports.
4. Preserve explicit non-capabilities.
5. Run structural validation, JSON parsing, evidence checks, broad AIDE
   validation, secret scan, and commit-policy validation.
6. Stop at `needs_review` and recommend `AIDE-CHECK-INTEROP-EXPORTS-01`.

## Non-Goals

Do not implement live MCP, A2A, Host Contract, Dominium Bridge conformance,
Workbench, Commander, Service, runtime, worker execution, provider/model calls,
network calls, PatchTransaction apply, branch/worktree automation, GitHub
mutation, release, promotion, or target-repository mutation.

## Review Gate

Stop at `needs_review`.
