# Next Task Prompt

## Task

`AIDE-CHECK-CONFORMANCE-PROFILE-01`

## Objective

Independently review `AIDE-BUILD-CONFORMANCE-PROFILE-01` and its commit. Confirm
that the ConformanceProfile slice defines profile-scoped requirements without
claiming observed results, admission, execution, adapter trust, runtime behavior,
or mutation authority.

## Required Review Areas

- source-chain review from `AIDE-ACCEPT-CAPABILITY-MANIFEST-01`;
- schema review;
- helper review;
- profile model review;
- case model review;
- versioning review;
- aggregation and fail-closed policy review;
- evidence requirements review;
- CLI dispatch review;
- projection/report determinism review;
- CapabilityManifest integration review;
- governance integration review;
- predecessor compatibility review;
- tests and validation review;
- no-overclaiming review;
- no-forbidden-ops review.

## Expected Result

Stop at `needs_review` with `PASS_WITH_WARNINGS` if no blockers are found.

## Boundary

Do not implement `ConformanceResult`, admission, adapters, runtime,
PatchTransaction, ContextPack, worker execution, provider/model/network/Gateway
calls, target apply, branch/worktree automation, release, promotion, or
production readiness.
