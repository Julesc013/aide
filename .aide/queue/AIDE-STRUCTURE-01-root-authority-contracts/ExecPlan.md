# ExecPlan: AIDE-STRUCTURE-01-root-authority-contracts

## Objective

Create the first root authority contract layer for Track B using the completed
`AIDE-STRUCTURE-00-current-truth-and-root-authority-audit` reports as input.

This task is allowed to add policy, governance, reference, planning, report, and
queue evidence artifacts. It is not allowed to reorganize the repository.

## Scope

Allowed write scope:

- `.aide/queue/AIDE-STRUCTURE-01-root-authority-contracts/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/policies/root-authority.yaml`
- `.aide/reports/root-authority-contracts.*`
- `governance/root-authority.md`
- `docs/reference/repository-layout.md`
- `docs/planning/repository-structure/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

Read-only inputs include the AIDE operating law, queue policy, review gates,
source-of-truth reference, repo intelligence/root/refactor references, and the
Track B structure audit reports.

## Plan

1. Reconfirm live queue and dependency state from `.aide/queue/`.
2. Write a machine-readable root authority policy.
3. Write human governance and reference docs that explain the root model,
   overlaps, migration rules, and validation expectations.
4. Write a compact report and follow-up prompt plan for the remaining Track B
   tasks.
5. Update root planning, implementation, documentation, queue index, and latest
   task packet records.
6. Run proportionate validation, write evidence, and stop at `needs_review`.

## Review Gates

This task reaches a review gate because it adds new root authority contracts.
It does not change generated-artifact source-of-truth rules, apply root maps, or
mutate `.aide/policies/autonomy.yaml`, `.aide/policies/bypass.yaml`, or
`.aide/policies/review-gates.yaml`.

## Validation Intent

- `git status --short --branch`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-STRUCTURE-01-root-authority-contracts`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-STRUCTURE-01-root-authority-contracts`
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## Exit Criteria

- Root authority contract artifacts exist and are linked from docs and queue
  surfaces.
- Overlap, candidate target structure, migration rules, validation plan, and
  follow-up prompts are recorded.
- No file moves, deletes, reference rewrites, aliases, shims, branch mutation,
  target mutation, provider/model/network calls, or release actions occur.
- Task status is `needs_review` with validation and remaining-risk evidence.
