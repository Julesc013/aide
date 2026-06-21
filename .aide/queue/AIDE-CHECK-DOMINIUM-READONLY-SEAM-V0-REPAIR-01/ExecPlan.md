# AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01 ExecPlan

## Objective

Independently check `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01` without repairing the seam, changing production code, modifying repair outputs, or mutating Dominium.

## Scope

Allowed writes are limited to:

- `.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01/**`
- `.aide/reports/dominium-readonly-seam-v0-repair-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

## Plan

1. Verify local queue truth, branch, repair commit resolution, source build/check/repair task evidence, and the absence of superseding seam acceptance or repair tasks.
2. Read the repaired seam outputs, public schema, fixture inventory, conformance results, demo result, repair reports, and relevant source-chain status.
3. Run evidence-local independent checks that do not import production seam validation, production conformance, production negative-fixture mutators, or repair finding-disposition logic as material proof.
4. Independently review repaired identities, revisions, digests, schema constraints, reference closure, ownership, registry projections, negative fixture replay, conformance evidence shape, operation ledger coverage, determinism, immutability, report consistency, and non-capabilities.
5. Classify closed findings, remaining material gaps, warnings, and the single next task.
6. Write consolidated repair-check reports and task-local evidence.
7. Run queue validation, broad validation, diff checks, secret scan, commit policy, and stop at `needs_review`.

## Exit Criteria

The task stops at `needs_review` with exactly one next-task recommendation:

- `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01` if all material findings are closed.
- `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02` if one or more material defects remain.
