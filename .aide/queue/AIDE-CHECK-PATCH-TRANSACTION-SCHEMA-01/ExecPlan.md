# AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01 ExecPlan

## Objective

Independently check the minimal PatchTransaction schema/helper/projection/CLI
slice produced by `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01` and decide whether
it is ready for acceptance review.

## Scope

- Verify the live queue and build source chain.
- Review the PatchTransaction schema/helper/report boundary without repairing it.
- Independently recompute the sample patch artifact digest.
- Probe path-scope validation with adversarial cases.
- Review lifecycle, authority, explicit execution facts, CLI unsupported
  operation closure, report consistency, determinism, and source immutability.
- Write check reports and task-local evidence.
- Stop at `needs_review`.

## Dependencies

- `AIDE-OPERATIONAL-HEALTH-PAUSE-01` result: `PASS_WITH_WARNINGS`.
- `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01` result:
  `PASS_WITH_WARNINGS`.
- Build task evidence reports `missing_evidence: 0`.
- Build commit `2559b1dbc528992451193d942bff741e8cb0a0a7` is live `HEAD`.

## Milestones

- Baseline and queue chain verified.
- Build task and evidence inspected.
- Independent digest and report consistency checks completed.
- Path-scope probes completed.
- Validation matrix run.
- Material findings classified.
- Repair next task prompt generated.

## Verification Intent

Run Git diff checks, compile checks, focused unit tests, PatchTransaction
status/project/validate, predecessor validators, task inspect/evidence checks,
broad AIDE validation, JSON parsing, independent SHA-256 recomputation,
adversarial path-scope probes, unsupported subcommand probes, deterministic
projection comparison, source immutability review, changed-file review,
secret-like scan, and commit policy validation.

## Exit Criteria

The task stops at `needs_review` with `FAILED_VALIDATION`, complete evidence,
no implementation change, no forbidden operation, explicit material findings,
warning disposition, and exactly one next task:
`AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

## Non-Capabilities

This check does not repair the build, change schemas or helpers, change tests,
regenerate build reports to conceal discrepancies, apply a patch, approve a
transaction, mutate target files, execute rollback, evaluate policy, execute
conformance cases, activate a profile, admit or trust a subject, build
AdapterManifest or ContextPack v2, execute workers, implement runtime/Test
Broker/Service/Commander/Workbench, call providers/models/Gateway/network/
GitHub, create branches or worktrees, publish, release, promote, restructure
reports, or edit generated OKF pages.
