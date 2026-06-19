# AIDE-RESUME-BUILD-CONTEXTPACK-V2-01 ExecPlan

## Purpose

Build the resume ContextPack v2 slice after PatchTransaction and AdapterManifest
resume acceptance. The output is a deterministic, evidence-bound, no-execution
context projection protocol record.

## Scope

- Add `.aide/protocol/aide-context-pack-v2.schema.json`.
- Add `core/protocol/context_pack_v2.py` and export it from `core/protocol`.
- Add thin AIDE Lite `context-pack-v2 status/project/validate` dispatch.
- Add focused ContextPack v2 tests.
- Generate `.aide/reports/context-pack-v2-resume/**`.
- Materialize this queue task packet and task-local evidence.
- Update `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Non-Goals

No model/provider/Gateway/network calls, embedding generation, agent execution,
worker execution, command execution, adapter admission, trust, patch apply,
target repository mutation, runtime, Service, scheduler, leases, supervisor,
Test Broker, Commander, Workbench, branch/worktree automation, release, or
promotion.

## Milestones

- [x] Confirm AdapterManifest resume acceptance and preserve original blocked ContextPack records.
- [x] Add schema/helper/CLI/tests for a projection-only ContextPack v2 slice.
- [x] Generate deterministic reports.
- [x] Run focused and predecessor validation.
- [x] Write complete task evidence.
- [x] Stop at `needs_review` with the next task prompt.

## Validation

Run Python compilation, focused ContextPack v2 tests, ContextPack v2
status/project/validate, predecessor protocol validators, task inspect/evidence,
broad AIDE validation, JSON parsing, repeated projection comparison, source
immutability comparison, secret-like scan, diff checks, and commit policy.

## Recovery

If validation fails, preserve generated evidence, classify the material finding,
and route to a bounded repair task. Do not rewrite the original blocked
ContextPack records.
