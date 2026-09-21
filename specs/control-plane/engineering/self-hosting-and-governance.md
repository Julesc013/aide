---
type: AIDE Engineering Specification
title: Self-hosting, planning and code adoption
description: AIDE should use its own mechanisms without becoming the sole authority that approves them.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P04
  resource: urn:aide:source-package:b3f3d0d27109a986e537928523c9c34f31e3458986c7632e97abee06d85db64c
  title: AIDE-Spec-Overhaul-2026-09-20(3)(1).zip
- id: P06
  resource: urn:aide:source-package:83f9926500c47e3ee8384868c7d4046083e2a75bef0d667fb526c8476446d121
  title: AIDE-Spec-Overhaul-2026-09-20-R2(2)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P15
  resource: urn:aide:source-package:ddcd7109c50db5ad3bfe6693f5f09e52dd8c276280368af8105ab1b69458ea81
  title: AIDE-Spec-Overhaul-R2-2026-09-20(1).zip
- id: P20
  resource: urn:aide:source-package:90f79366cb02f34d737950db6708c087db367e36e7ce5ff98f7d953c6a82fb96
  title: AIDE-Specification-Overhaul-2026-09-20(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: repository policy and maintainers
  applicability: AIDE source project
  requirement_ids:
  - UR-SELF-01
  - UR-SELF-02
  - UR-SELF-03
  - UR-SELF-04
  - UR-SELF-05
  - UR-SELF-06
  - UR-SELF-07
---

# Self-hosting, planning and code adoption

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

AIDE should use its own mechanisms without becoming the sole authority that approves them.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Apply the same work, evidence, preservation and transaction discipline to AIDE itself. Preserve source-repository authority separately from installed Lite state and product runtime. Updating AIDE’s own execution, grants, signing or acceptance logic is a higher-risk change with an independent approval/verification path. Candidate code must not qualify its own altered oracle.

The current queue and active task-branch status remain the source for executable routing. A master roadmap is a dependency graph of proposed outcomes, not a replacement next-task file. Missing materialized tasks or drifted generated packets should be reconciled before action. Do not restore stale June next-task recommendations over the current continuous-worker/broker work.

Use risk-tiered governance and reusable validation. Build/check/accept remain meaningful stages, but the future queue need not create a permanent directory for every micro-step. Preserve failed checks and contradictory evidence. Measure governance overhead, repeated repair rate, evidence reuse, time to first useful outcome and documentation retrieval effort. Tighten checks at real boundaries rather than making every harmless operation a new architecture ceremony.

## Interface and data boundary

Current admitted queue; source baseline; task/attempt/stage; allowed paths; risk tier; oracle; evidence; harvest; next permitted action; branch ownership; migration plan.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-SELF-01 — No roadmap queue override

Roadmap and package adoption notes MUST remain advisory until an authorized task reconciles them with current queue and branch ownership.

### UR-SELF-02 — Self-change independence

AIDE MUST NOT be the sole producer, verifier and promoter of its own consequential authority changes.

### UR-SELF-03 — Historical failures preserved

Failed checks, repairs and superseded tasks MUST retain provenance while current views compact completed history.

### UR-SELF-04 — One active writer by policy

The source repository MUST preserve current concurrency and writer rules until a reviewed migration changes them.

### UR-SELF-05 — Risk-tiered process

Governance SHOULD scale evidence and review effort to the actual change risk without weakening hard authority or security floors.

### UR-SELF-06 — Traceability to code

Every admitted implementation slice MUST connect requirements, source/tests, observed evidence and remaining gaps.

### UR-SELF-07 — Existing gate reuse

Implementation plans MUST reuse accepted foundations and reconcile partial work instead of restarting completed schema or service chains.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-SELF-01` | A draft names a completed old task as next. | It is not executed merely because the draft says so. |
| `UC-SELF-02` | A patch changes both grant enforcement and the only acceptance check. | Independent authority is required before promotion. |
| `UC-SELF-03` | A repair passes after a failed review. | The original failure remains attributable and the current summary shows the repaired state. |
| `UC-SELF-04` | Two tasks propose writes to queue/index and the same modules. | Scheduling serializes them or uses explicitly admitted isolated branches and merge order. |
| `UC-SELF-05` | A tiny read-only documentation observation runs. | It is not forced through unnecessary live-runtime authorization work. |
| `UC-SELF-06` | A requirement has only a prose scenario marked not_run. | The capability stays unqualified until actual evidence is linked. |
| `UC-SELF-07` | The current main includes a continuous-worker prototype. | The plan begins at its actual integration/isolation gaps, not a new empty runtime. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
