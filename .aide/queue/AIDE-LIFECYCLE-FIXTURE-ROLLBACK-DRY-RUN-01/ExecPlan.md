# ExecPlan: AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01

## Objective

Run static report-only and dry-run rollback planning checks against reviewed rollback-compatible fixture records. The checks compare rollback records with lifecycle rollback schema requirements, generated lifecycle fixture plans, expected reports, fixture metadata, preimage and postimage hash references, inverse operation descriptions, rollback preconditions, rollback stop conditions, manual preservation rules, protected paths, scoped executor v0 limitations, no-execution flags, and capability labels.

## Scope

Allowed writes are limited to this task directory, `.aide/reports/lifecycle-fixture-rollback-dry-run/**`, queue index, latest task packet, and deterministic status/validation report refreshes. Rollback record files, generated lifecycle fixture plans, expected lifecycle reports, fixture target files, lifecycle schemas, scoped transaction executor source, managed-section implementation, lifecycle apply surfaces, provider/model/Gateway files, release files, and target repositories are read-only or protected.

## Check Model

The check model is static and report-only. It may parse JSON, compare fixture metadata and generated plan reports, compute SHA-256 hashes for referenced static preimage and postimage fixture files, classify the generic rollback example as placeholder-only, inspect inverse operations, inspect rollback preconditions and stop conditions, and confirm no-execution flags. It must not implement or run rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, provider/model calls, Gateway calls, GitHub mutation, network calls, release publication, broad active-repo apply, broad deletes, or broad moves.

## Rollback Scenarios

- `rollback-record-generated`
- `fixture-rollback-install-managed-section`
- `fixture-rollback-upgrade-v2`

Install apply, upgrade apply, lifecycle repair apply, rollback execution, uninstall execution, fixture apply, active repo apply, target repo adoption, Gateway/provider/network work, release work, and broad active-repo apply remain deferred or prohibited.

## Result

Result is `PASS_WITH_WARNINGS`. The two fixture rollback records have matching SHA-256 preimage and postimage hashes for referenced static fixture files, coherent inverse operations, explicit rollback preconditions and stop conditions, manual-preservation notes, protected-path checks, `rollback_execution_implemented=false`, and review gates. The generic rollback example is classified as example-only because it intentionally uses placeholder hashes and fixture-content refs.

## Next WorkUnit

Select `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01` as the next smallest safe WorkUnit. It is an independent checkpoint and does not authorize rollback apply, rollback execution, uninstall apply, uninstall execution, lifecycle apply, scoped transaction fixture apply, active repo apply, target repo mutation, release work, provider/model/Gateway/network calls, or broad active-repo apply.

## Review Gate

Stop at `needs_review`.
