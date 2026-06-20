# AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01 ExecPlan

## Objective

Accept or reject the planning-only AIDE-Dominium integration charter after reviewing the charter build, independent remote-freshness and semantic check, and acceptance prerequisites.

## Scope

Allowed changes are limited to this acceptance queue packet and evidence, `.aide/reports/dominium-integration-charter-accept/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Dependencies

- `AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01`: `ACCEPTED_WITH_WARNINGS`, evidence complete.
- `AIDE-DOMINIUM-INTEGRATION-CHARTER-01`: `PASS_WITH_WARNINGS`, evidence complete, charter commit `5b80e4c4c3c400e2a3ccf8d2c42cfb44c3d6aa28`.
- `AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01`: `PASS_WITH_WARNINGS`, evidence complete, zero material findings, check commit `2af8bb2108eb5fdf281105c98429ac4491372ed1`.
- Current remote Dominium `main` still equals the independent-check baseline `623ab08ae8c867719d5abc2e60c16a6fbb37b313`.

## Work Plan

1. Verify live AIDE branch, worktree, source-chain tasks, source commits, evidence completeness, and next-task routing.
2. Confirm remote Dominium freshness without fetch, pull, merge, reset, rebase, branch, worktree, GitHub, or local Dominium mutation.
3. Consolidate accepted planning scope, warning debt, and explicit non-capabilities.
4. Review source-of-truth, semantic ownership, namespaces, object mappings, command/refusal, diagnostic/evidence/event, transaction, Workbench, compatibility, security, recovery, seam, validation-slice, DAG, and turn-size policy evidence.
5. Materialize acceptance reports and task-local evidence.
6. Run the validation matrix and record results.
7. Stop at `needs_review` and recommend `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`.

## Non-Goals

No charter repair, Dominium modification, downstream queue task materialization, Host Contract implementation, Dominium Bridge implementation, Workbench implementation, runtime, service, provider/model/network call, worker execution, preview, apply, rollback, mutation, branch/worktree automation, GitHub mutation, release, or promotion is performed or authorized.

## Exit Criteria

The task stops at `needs_review` with `ACCEPTED_WITH_WARNINGS`, complete evidence, no unresolved material finding, current remote Dominium compatibility confirmed, explicit planning-only accepted scope, preserved non-capabilities, warning debt classified, and exactly one next task recommendation.
