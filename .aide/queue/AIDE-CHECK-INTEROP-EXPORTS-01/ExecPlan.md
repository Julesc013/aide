# AIDE-CHECK-INTEROP-EXPORTS-01 ExecPlan

## Objective

Independently check the static interop export previews produced by
`AIDE-BUILD-INTEROP-EXPORTS-01`.

## Scope

Allowed outputs are limited to:

- the check task packet and evidence;
- `.aide/reports/interop-exports-check/**`;
- `.aide/queue/index.yaml`;
- `PLANS.md`;
- `IMPLEMENT.md`.

## Steps

1. Confirm the build task exists, is complete, and recommends this check.
2. Independently recompute preview artifact hashes.
3. Parse preview and report JSON.
4. Check manifest/report consistency.
5. Review explicit non-capabilities and queue-authority wording.
6. Confirm build artifacts remain unchanged.
7. Run task evidence, broad validation, secret scan, and commit-policy checks.
8. Stop at `needs_review` and recommend acceptance if no material findings
   exist.

## Non-Goals

Do not modify preview artifacts, build reports, implementation, schemas,
helpers, tests, accepted predecessors, generated OKF pages, runtime, provider,
host, VCS, GitHub, release, or target-repository files.

## Review Gate

Stop at `needs_review`.
