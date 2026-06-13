# ExecPlan: AIDE-CHECK-WORKUNIT-CLI-01

## Objective

Independently check the read-only WorkUnit CLI implementation from `AIDE-BUILD-WORKUNIT-CLI-01`.

## Scope

- Verify `workunit status`, `workunit list`, `workunit inspect --task-id`, and `workunit validate`.
- Verify unsupported mutation commands fail closed.
- Verify safe task id handling and source queue task non-mutation.
- Verify compatibility with lifecycle fixture, contract-envelope, EvidencePacket, and WorkUnit Queue V1 surfaces.
- Write check-only reports and evidence.

## Boundaries

- No implementation code changes.
- No WorkUnit mutation CLI, runtime, scheduler, supervisor, WorkerRun, TestJob, Test Broker, Service, Commander, provider adapter, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, network, Gateway, GitHub, or model/provider calls.
- No destructive migration of accepted reports, evidence, or queue tasks.

## Verification

Run static review, direct shell command checks, focused tests, predecessor tests, queue mutation hash checks, path-safety probes, compatibility commands, report parsing, overclaim scans, secret scans, and commit policy validation for check artifacts.

## Stop State

Stop at `needs_review`.
