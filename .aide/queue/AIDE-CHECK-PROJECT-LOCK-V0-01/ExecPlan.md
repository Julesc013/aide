# AIDE-CHECK-PROJECT-LOCK-V0-01 ExecPlan

## Objective

Independently verify `AIDE-BUILD-PROJECT-LOCK-V0-01` and the proposed
`project_lock_v0` capability without repairing implementation, accepting the
capability, or beginning OwnershipLedger work.

## Scope

Allowed outputs are this check task directory, the
`.aide/reports/project-lock-v0-check/` report directory, `.aide/queue/index.yaml`,
`PLANS.md`, and `IMPLEMENT.md`.

Forbidden outputs include ProjectLock implementation, schema, tests, fixtures,
source build reports, release archives, target repositories, and downstream
distribution objects.

## Verification Plan

- Inspect the source build task, evidence, reports, and commit.
- Recompute ProjectLock identity digest with a check-local canonicalizer.
- Probe identity mutations for status, queue routing, channel, project identity,
  selected distribution digest, component digest, and policy overlay refs.
- Verify selected distribution digest and manifest payload digest match the
  accepted DistributionManifest.
- Verify selected components resolve to manifest components, artifact refs
  resolve, dependencies resolve, and fixtures pass expected outcomes.
- Exercise the `project-lock validate` command as the system under test and
  verify unsupported apply-like command refusal.
- Run focused ProjectLock tests, broad AIDE validation, task inspect/evidence,
  diff checks, and commit-policy check.

## Result

`PASS_WITH_WARNINGS`. No material findings remain. The next serialized task is
exactly `AIDE-ACCEPT-PROJECT-LOCK-V0-01`.
