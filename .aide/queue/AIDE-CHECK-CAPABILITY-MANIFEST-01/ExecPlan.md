# AIDE-CHECK-CAPABILITY-MANIFEST-01 ExecPlan

## Objective

Independently check `AIDE-BUILD-CAPABILITY-MANIFEST-01` as a bounded,
check-only WorkUnit.

## Scope

- Review the CapabilityManifest schema, helper, projection reports, CLI,
  tests, and build evidence.
- Generate task-local check evidence and aggregate check reports.
- Update the queue index and root planning/execution logs for this check.
- Stop at `needs_review`.

## Non-Goals

No CapabilityManifest repair, ConformanceProfile, ConformanceResult,
conformance admission, adapter admission, adapter execution, capability
execution, runtime registry, scheduler, leases, supervisor, Service,
Commander, PatchTransaction, AdapterManifest, ContextPack v2, provider/model
calls, network/Gateway/GitHub mutation, branch/worktree automation, target
apply, active apply, release, production readiness, or broad autonomous
runtime.

## Plan

1. Verify live queue truth and record prompt drift.
2. Read build task, evidence, reports, schema, helper, CLI, and tests.
3. Check capability inventory, status semantics, evidence refs, conformance
   boundary, integrations, compatibility, overclaiming, and forbidden ops.
4. Generate check-only evidence and aggregate reports.
5. Run focused tests, JSON parsing, task evidence checks, predecessor
   validators, broad validation, diff checks, and commit policy check.

## Status

Check completed with warnings and awaiting review.
