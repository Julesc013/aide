# AIDE-RESUME-CHECK-CONTEXTPACK-V2-01 ExecPlan

## Purpose

Independently check the resume ContextPack v2 build without modifying its
schema, helper, tests, or build reports.

## Scope

- Check task packet and task-local evidence.
- `.aide/reports/context-pack-v2-resume-check/**`.
- Queue index, planning log, and implementation log updates.

## Non-Goals

No implementation repair, schema edits, helper edits, test edits, build report
rewrites, acceptance, model/provider/network calls, embeddings, execution,
admission, trust, patch apply, target mutation, runtime, Service, Commander,
Workbench, branch/worktree automation, release, or promotion.

## Milestones

- [x] Confirm build task source chain and evidence completeness.
- [x] Independently recompute source hashes.
- [x] Verify deterministic projection and source immutability in a temp workspace.
- [x] Probe CLI no-execution boundaries.
- [x] Write reports and evidence.
- [x] Stop at `needs_review`.

## Validation

Run Python compilation, focused ContextPack v2 tests, live ContextPack status,
unsupported-command probes, JSON parsing, task inspect/evidence, broad AIDE
validation, secret-like scan, diff checks, and commit policy.
