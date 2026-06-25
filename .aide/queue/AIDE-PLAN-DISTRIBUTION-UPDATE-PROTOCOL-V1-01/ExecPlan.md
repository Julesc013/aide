# AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01 ExecPlan

## Purpose

Produce a bounded distribution/update protocol v1 plan that reconciles the
existing Q43-Q48 install, repair, upgrade, rollback/uninstall, release bundle,
and release-draft foundations. This is not a greenfield distribution design.

## Scope

Allowed writes:

- `.aide/queue/AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01/**`
- `.aide/reports/distribution-update-protocol-v1-plan/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Read-only inputs:

- queue policy and current queue state
- `.aide/profile.yaml`
- source-of-truth reference
- existing Q43-Q48 policies, schemas, generated evidence, and reference docs
- durable WorkerRun acceptance evidence

## Non-Goals

This task does not implement any v1 schema, helper command, apply engine,
release publication, target install, update apply, repair apply, rollback apply,
uninstall apply, Git tag, GitHub Release, upload, network call, provider/model
call, branch/worktree automation, Workbench/MCP runtime, source-change
preview/apply/rollback, or promotion.

## Current Facts To Verify

- `AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01` exists and recommends this
  planning task.
- Q43 install status is no-apply.
- Q44 repair status is no-apply.
- Q45 upgrade status is no-apply.
- Q46 rollback/uninstall status is no-apply.
- Q47 release bundle validates and is no-publish.
- Q48 release draft validates and is no-publish.

## Plan Outputs

- distribution object dependency graph
- Q43-Q48 to v1 compatibility map
- authority/source-of-truth map
- ownership taxonomy
- lifecycle state machines
- migration rules
- refusal-code registry
- artifact/source/channel model
- rollout-ring model
- fixture and conformance matrix
- security and preservation invariants
- public release gates
- exact first build task

## Decisions

- `DistributionManifest v1` is the first build because it gives the rest of the
  distribution/update stack a stable content identity.
- Q43-Q48 schemas and outputs are retained as compatibility inputs. They are not
  copied into targets as target truth.
- The first apply engine remains a later fixture-only task after manifest, lock,
  ownership, install record, migration record, update plan, rollback bundle, and
  update receipt have their own reviewed gates.

## Progress

- [x] Confirm live queue route.
- [x] Inventory Q43-Q48 status and generated artifacts.
- [x] Write v1 dependency and compatibility reports.
- [x] Select first build task.
- [x] Run final validation.
- [x] Stop at `needs_review`.

## Recovery

This is plan-only. A future worker can resume by checking this task's
`status.yaml`, running `task inspect` and `task evidence`, and verifying the
reports listed in `task.yaml`. No implementation or generated lifecycle output
needs to be regenerated to recover this task.
