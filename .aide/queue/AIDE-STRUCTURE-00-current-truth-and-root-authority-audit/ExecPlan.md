# AIDE-STRUCTURE-00 ExecPlan

## Objective

Create a fresh, check-only structure audit that reconciles live repo truth
before any repository reshaping.

## Scope

- Add the `AIDE-STRUCTURE-00-current-truth-and-root-authority-audit` queue
  packet and task-local evidence.
- Refresh or inspect existing repo intelligence, root recycling, refactor-map,
  Task OS, and Git status surfaces.
- Produce structure-current-state reports and root authority candidate reports.
- Add a planning note under `docs/planning/repository-structure/`.
- Update root planning/execution/documentation indexes only as audit records.
- Stop at `needs_review`.

## Non-Goals

No file moves, file deletes, reference rewrites, path alias application,
shim creation, new top-level root creation, generated-output source-of-truth
promotion, source truth mutation, queue acceptance mutation, branch mutation,
target-repo mutation, release work, GitHub mutation, provider/model calls,
network calls, runtime, Service, Commander, host runtime, provider runtime, or
product/release readiness claim.

## Plan

1. Create the queue packet with a check-only allowlist and review gate.
2. Run fresh repo/root/refactor/task/Git status commands and capture results.
3. Compare live queue/status/report facts against root docs and OKF posture.
4. Write current-state and root-authority-candidate reports.
5. Record changed files, validation, forbidden-operation review, remaining
   risks, and recommended next tasks.
6. Update status to `needs_review`, run validation, and commit the bounded
   audit artifact set.

## Status

Audit completed with warnings. Awaiting review.
