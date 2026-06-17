# ExecPlan: AIDE-BUILD-REPO-LAYOUT-INVENTORY-01

## Objective

Create a report-only Track B inventory of the current `.aide` and `core`
layouts. The output should support later design review, not apply structural
change.

## Scope

Allowed writes:

- `.aide/queue/AIDE-BUILD-REPO-LAYOUT-INVENTORY-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/repo-layout/**`
- `.aide/reports/task-os-*`
- `docs/planning/repository-structure/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

## Plan

1. Inspect live queue and Track B root authority contracts.
2. Inventory tracked `.aide` and `core` immediate subtrees.
3. Classify subtrees by authority plane and portability.
4. Record report/check/accept layout inconsistencies and hardcoded flat report
   path assumptions.
5. Write inventory, recommendations, and migration-risk reports.
6. Record no-apply evidence and stop at `needs_review`.

## Non-Goals

No file moves, deletes, renames, schema churn, reference rewrites, report
directory restructuring, generated OKF edits, generated-output authority
changes, branch mutation, target-repo mutation, network/provider calls, release
work, or Track A product-protocol implementation.

## Validation Intent

- `git status --short --branch`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py repo status`
- `py -3 .aide/scripts/aide_lite.py roots status`
- `py -3 .aide/scripts/aide_lite.py refactor map-status`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-REPO-LAYOUT-INVENTORY-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-REPO-LAYOUT-INVENTORY-01`
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## Exit Criteria

- `.aide/reports/repo-layout/inventory.*`,
  `.aide/reports/repo-layout/recommendations.*`, and
  `.aide/reports/repo-layout/migration-risks.md` exist.
- The task status is `needs_review`.
- Evidence records no forbidden operations and remaining design risks.
