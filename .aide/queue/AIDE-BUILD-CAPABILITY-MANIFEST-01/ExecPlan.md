# AIDE-BUILD-CAPABILITY-MANIFEST-01 ExecPlan

## Objective

Build the first declaration-only CapabilityManifest slice after acceptance of
`minimal_reconciler_reports`.

## Scope

- Add `.aide/protocol/aide-capability-manifest.schema.json`.
- Add `core/protocol/capability_manifest.py`.
- Register thin `capability-manifest status/project/validate` dispatch.
- Generate `.aide/reports/capability-manifest/**`.
- Add focused tests and task-local evidence.
- Stop at `needs_review`.

## Non-Goals

No ConformanceProfile, ConformanceResult, admission, adapter execution,
capability execution, runtime registry, scheduler, leases, supervisor, Service,
Commander, PatchTransaction, AdapterManifest, ContextPack v2, provider/model
calls, network/Gateway/GitHub mutation, branch/worktree automation, target
apply, active apply, release, production readiness, or broad autonomous runtime.

## Plan

1. Confirm live queue truth and predecessor acceptance evidence.
2. Add schema/helper/CLI/tests using existing protocol patterns.
3. Project accepted capabilities into deterministic JSON/Markdown reports.
4. Validate with focused tests, CLI checks, JSON parsing, predecessor validators,
   broad validation, task inspect/evidence, and diff checks.
5. Record warnings, non-capabilities, next-task prompt, and stop at review.

## Status

Implementation completed. Awaiting independent check.
