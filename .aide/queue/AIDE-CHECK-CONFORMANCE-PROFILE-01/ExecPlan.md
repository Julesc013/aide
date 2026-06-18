# ExecPlan: AIDE-CHECK-CONFORMANCE-PROFILE-01

## Objective

Perform an independent, check-only review of `AIDE-BUILD-CONFORMANCE-PROFILE-01`
and stop at `needs_review`.

## Scope

Allowed writes are limited to this check task packet, the
`conformance-profile-check` reports, `.aide/queue/index.yaml`, `PLANS.md`, and
`IMPLEMENT.md`.

Read-only source artifacts include the built ConformanceProfile schema, helper,
CLI dispatch, tests, and generated profile reports.

## Procedure

1. Confirm live queue truth and build-task status.
2. Review schema, helper, model, generated reports, CLI, tests, boundaries, and
   predecessor compatibility.
3. Classify warnings without repairing implementation artifacts.
4. Write check reports and evidence.
5. Run the validation matrix.
6. Stop at `needs_review` with `PASS_WITH_WARNINGS`.

## Boundaries

This check does not implement `ConformanceResult`, conformance execution,
admission, adapter admission or execution, `PatchTransaction`, runtime behavior,
provider/model calls, target apply, branch/worktree automation, release,
promotion, or production readiness.

## Exit Criteria

- `AIDE-BUILD-CONFORMANCE-PROFILE-01` remains a bounded profile-only build.
- All required check evidence exists.
- The result is `PASS_WITH_WARNINGS`.
- The next recommended task is `AIDE-ACCEPT-CONFORMANCE-PROFILE-01`.
