# ExecPlan: AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01

## Objective

Run static report-only and dry-run checks against generated lifecycle fixture repair plans. The checks compare repair plan intent with fixture metadata, generated plan reports, expected repair report evidence, missing marker and malformed marker expectations, path boundaries, managed section behavior, preimage hash references, related drift evidence, no-apply flags, scoped executor interlock, and capability labels.

## Scope

Allowed writes are limited to this task directory, `.aide/reports/lifecycle-fixture-repair-dry-run/**`, queue index, latest task packet, and deterministic status/validation report refreshes. Generated repair plans, static fixture targets, expected states, lifecycle schemas, scoped transaction executor source, managed-section implementation, and lifecycle apply surfaces are read-only.

## Check Model

The check model is static and report-only. It may parse JSON, compare fixture metadata and generated plan reports, inspect expected-state README evidence, compute SHA-256 hashes for referenced static target files, and inspect managed section marker shape. It must not implement or run lifecycle repair apply, lifecycle apply, scoped transaction apply against fixture targets, active repo apply, target repo mutation, branch/worktree mutation, provider/model calls, Gateway calls, GitHub mutation, network calls, release publication, or broad active-repo apply.

## Repair Scenarios

- `repair-plan-missing-marker`
- `repair-plan-malformed-marker`

Install, upgrade, rollback, uninstall, fixture apply, active repo apply, target repo adoption, Gateway/provider/network work, release work, and broad active-repo apply remain deferred or prohibited.

## Result

Result is `PASS_WITH_WARNINGS`. Both repair scenarios were checked and match the expected blocked marker states. Static expected repair report refs are absent for both repair plans, so generated plan reports plus expected-state README files are used as report evidence. This is non-blocking for this dry-run check and should be reviewed independently in the next checkpoint.

## Next WorkUnit

Select `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` as the next smallest safe WorkUnit. It is an independent checkpoint and does not authorize lifecycle repair apply, lifecycle apply, scoped transaction fixture apply, active repo apply, target repo mutation, release work, provider/model/Gateway/network calls, or broad active-repo apply.

## Review Gate

Stop at `needs_review`.
