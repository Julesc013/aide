# AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-02 ExecPlan

## Objective

Independently verify that `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-02`
closed the four remaining DistributionManifest v1 material findings without
modifying implementation or accepting the capability.

## Scope

This is check-only. Allowed changes are task-local check evidence, check reports,
queue index routing, and planning/execution logs.

## Checks

1. Future-major protocol ranges fail closed.
2. `files/` package members are classified against the target-root member view.
3. Directory forbidden members are recorded and make contamination explicit.
4. Future-major invalid fixtures exist and are exercised from disk.

## Exit

If zero material findings remain, stop at `needs_review` and recommend exactly
`AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01`.

If any material finding remains, stop at `needs_review` and recommend exactly
`AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-03`.
