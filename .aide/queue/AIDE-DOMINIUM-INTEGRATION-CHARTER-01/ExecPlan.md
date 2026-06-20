# ExecPlan: AIDE-DOMINIUM-INTEGRATION-CHARTER-01

## Objective

Create a planning-only AIDE-local charter that freezes semantic ownership and integration boundaries between AIDE, Dominium, Domino, and Workbench before any Host Contract, bridge, service, Workbench, provider, worker, transport, or mutation implementation begins.

## Scope

Allowed writes:

- `.aide/queue/AIDE-DOMINIUM-INTEGRATION-CHARTER-01/**`
- `.aide/reports/dominium-integration-charter/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Dominium is read-only input. No Dominium, Domino, Workbench, sibling repository, branch, worktree, remote ref, GitHub, schema, helper, runtime, host, provider, OKF, RepoGraph, or implementation file may be modified.

## Plan

1. Verify AIDE baseline: clean `main`, A2A acceptance at `ACCEPTED_WITH_WARNINGS`, missing evidence zero, commit `7e80ea2f18b404af68a752502a7491fceaa7abea` at `HEAD` or ancestor, and no existing charter task.
2. Pin Dominium local input state from `C:/Projects/Dominium/dominium`: branch, HEAD, worktree state, queue current task, next task, constraints, validation status, and key source hashes.
3. Materialize charter reports covering source-of-truth hierarchy, namespace ownership, object mapping, command/refusal/diagnostic/evidence/event mapping, transaction composition, host/bridge/provider/experience separation, Workbench non-authority, compatibility, security, recovery, first read-only seam, first validation slice, task DAG, parallel read-only lanes, turn-size policy, milestone gates, non-capabilities, risks, and next check prompt.
4. Register the task in `.aide/queue/index.yaml` and update `PLANS.md` / `IMPLEMENT.md`.
5. Validate JSON, TOML input parsing, task graph uniqueness and acyclicity, ownership uniqueness, generated-projection non-authority, queue evidence completeness, broad AIDE validation, diff checks, no cross-repo modifications, and commit policy.

## Review Gate

Stop at `needs_review` with `PASS_WITH_WARNINGS`. Recommend only `AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01`.

## Warnings

- Dominium local `main` is clean but behind `origin/main` by 24 commits. No fetch was performed because the prompt forbids remote-ref mutation.
- This charter is not an integration implementation and does not claim live cross-repository behavior.
