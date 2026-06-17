# ExecPlan: AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01

## Objective

Define AIDE self-management as a Track B doctrine and future queue sequence.
AIDE must manage AIDE as a repo before expecting to manage other repositories
with the same discipline.

## Scope

Allowed writes:

- `.aide/queue/AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/policies/self-management.yaml`
- `.aide/reports/self-management/**`
- `.aide/reports/task-os-*`
- `docs/reference/aide-self-management.md`
- `docs/planning/repository-structure/**`
- `governance/root-authority.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

## Plan

1. Use live Track B inventory and root-authority artifacts as inputs.
2. Write a machine-readable self-management policy.
3. Write a human-readable AIDE self-management reference.
4. Write reports for object backlog, command backlog, queue sequence, and
   current boundary warnings.
5. Update queue/context/planning/documentation surfaces.
6. Validate and stop at `needs_review`.

## Non-Goals

No schema implementation, CLI command implementation, generated-output ledger,
OKF regeneration, docs truth repair, queue acceptance, structure transaction
apply, file movement, target-repo mutation, branch mutation, provider/model
calls, network calls, release work, runtime, Service, Commander, Workbench, or
Track A implementation.

## Exit Criteria

- `.aide/policies/self-management.yaml` exists.
- `docs/reference/aide-self-management.md` exists.
- `.aide/reports/self-management/` reports exist.
- The task has complete evidence and `needs_review` status.
