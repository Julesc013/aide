# AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01 ExecPlan

## Objective

Independently check `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01` without repairing the seam, changing production code, modifying build reports, or mutating Dominium.

## Scope

Allowed writes are limited to:

- `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01/**`
- `.aide/reports/dominium-readonly-seam-v0-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

## Plan

1. Verify branch, clean worktree, accepted charter predecessor, seam build result/evidence, build commit ancestry, and absence of superseding seam check/repair/acceptance tasks.
2. Read the live seam build artifacts, schema, modules, CLI, fixtures, reports, evidence, and build diff.
3. Run an evidence-local independent harness that parses JSON, recomputes digests, checks identities/references/cardinality/ownership/capabilities/events, compares selected Dominium inputs, probes production validation as the target under test, and records Dominium immutability.
4. Run focused existing validation commands only where they do not mutate forbidden build outputs, using temp AIDE roots for CLI command probes.
5. Classify material findings, warnings, and non-capabilities.
6. Write consolidated reports and task-local evidence.
7. Run queue validation, broad validation, diff checks, secret scan, commit policy, and stop at `needs_review`.

## Exit Criteria

The task stops at `needs_review` with exactly one next-task recommendation:

- `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01` if no material defect exists.
- `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01` if one or more bounded material defects exist.
