---
type: AIDE Engineering Specification
title: Workflows, operating profiles and configuration
description: Let projects tailor AIDE through explicit profiles and bounded capability graphs, not cloned cores or hidden flags.
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
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P15
  resource: urn:aide:source-package:ddcd7109c50db5ad3bfe6693f5f09e52dd8c276280368af8105ab1b69458ea81
  title: AIDE-Spec-Overhaul-R2-2026-09-20(1).zip
- id: P18
  resource: urn:aide:source-package:d61e3fe58a17ae0b729d36519b23ba123de87571c55fcf0128f06e34e7c26723
  title: AIDE-Spec-Overhaul-v2-2026-09-20(1)(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: workflow and policy owner
  applicability: all profiles
  requirement_ids:
  - UR-FLOW-01
  - UR-FLOW-02
  - UR-FLOW-03
  - UR-FLOW-04
  - UR-FLOW-05
  - UR-FLOW-06
---

# Workflows, operating profiles and configuration

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Let projects tailor AIDE through explicit profiles and bounded capability graphs, not cloned cores or hidden flags.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

A workflow composes typed capabilities, workers, validations, approvals and compensations. Dependencies, branching, retries and parallel groups need clear inputs, outputs, stop conditions and resource limits. Not every internal action becomes a public WorkUnit. Preserve one work identity and retain stage/attempt/effect lineage underneath it.

Configuration has two different resolutions: preferences choose among allowed options, while authority applies ceilings and denials. Explain effective values and their sources. Repository, organization, family, target, user and task overlays can compose only within their declared ownership; task settings cannot override protected policy. Pin inherited policy/profile versions for reproducibility and report changed inputs on continuation.

Provide useful archetypes without requiring one universal directory structure. A documentation-only portable project, a native game engine, a web service and an enterprise multi-repo estate can share work/evidence semantics while differing in tools and execution. Escalation and fallback are explicit qualified transitions, not silent changes from local/offline/subscription to cloud/API. The same workflow should retain a no-model alternative where deterministic tools or humans can satisfy the outcome.

## Interface and data boundary

Workflow graph; step types; dependencies; inputs/outputs; conditions; limits; retry/compensation; profile inheritance; effective configuration; source provenance; policy ceilings.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-FLOW-01 — Declarative workflow scope

Workflow steps MUST declare dependencies, acceptance, retries, limits and effect/compensation boundaries.

### UR-FLOW-02 — Preference versus authority

Configuration MUST distinguish overridable preference from non-weakenable authority ceilings.

### UR-FLOW-03 — Explain configuration

Effective values MUST be inspectable with origins, overrides, constraints and portability warnings.

### UR-FLOW-04 — Pinned inheritance

Inherited profiles and overlays MUST be version/digest-bound for admitted work and revalidated on material change.

### UR-FLOW-05 — No silent fallback

Fallback and escalation MUST be explicit permitted transitions with limits and unchanged acceptance floors.

### UR-FLOW-06 — Risk-proportionate governance

Review and evidence depth SHOULD be risk-proportionate while preserving non-negotiable authority and safety boundaries.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-FLOW-01` | A parallel branch has no stop or budget condition. | Admission refuses or requires bounded policy before execution. |
| `UC-FLOW-02` | A user profile requests a destination blocked by target policy. | Effective configuration shows denial and source provenance. |
| `UC-FLOW-03` | A model effort differs from the user preference. | The operator can identify the controlling profile and negotiation result. |
| `UC-FLOW-04` | An organization profile changes during a run. | The run does not silently consume the new authority semantics. |
| `UC-FLOW-05` | A local tool fails and a cloud service is available. | No source is sent remotely without compatible authority. |
| `UC-FLOW-06` | A harmless read-only formatting observation completes. | It need not create a separate permanent task for every internal step. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
