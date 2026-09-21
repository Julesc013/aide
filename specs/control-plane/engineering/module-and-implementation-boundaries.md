---
type: AIDE Engineering Specification
title: Implementation boundaries and modularity
description: Begin with the existing Python reference implementation, clean seams and characterization tests; do not restart the repository.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P05
  resource: urn:aide:source-package:a247c622c6987787cae0fe18ff9383bb202f185b7e99bf1ce22478d42412e36a
  title: AIDE-Spec-Overhaul-2026-09-20-R2(1)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P15
  resource: urn:aide:source-package:ddcd7109c50db5ad3bfe6693f5f09e52dd8c276280368af8105ab1b69458ea81
  title: AIDE-Spec-Overhaul-R2-2026-09-20(1).zip
- id: P18
  resource: urn:aide:source-package:d61e3fe58a17ae0b729d36519b23ba123de87571c55fcf0128f06e34e7c26723
  title: AIDE-Spec-Overhaul-v2-2026-09-20(1)(1).zip
- id: P20
  resource: urn:aide:source-package:90f79366cb02f34d737950db6708c087db367e36e7ce5ff98f7d953c6a82fb96
  title: AIDE-Specification-Overhaul-2026-09-20(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: implementation owners
  applicability: baseline and runtime
  requirement_ids:
  - UR-ARCH-01
  - UR-ARCH-02
  - UR-ARCH-03
  - UR-ARCH-04
  - UR-ARCH-05
  - UR-ARCH-06
  - UR-ARCH-07
---

# Implementation boundaries and modularity

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Begin with the existing Python reference implementation, clean seams and characterization tests; do not restart the repository.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

One conceptual core is not a demand to move every file into shared/. Current core/, historical shared/, host proofs and target-local bridges must be inventoried and assigned an explicit fate. Preserve the accepted shared-core/many-hosts ADR; broaden the client model from IDE requests to repo-native work without discarding host behavior.

Use a modular monolith where it is sufficient. Pure domain values and semantic validation should not import provider SDKs, GitHub, queue-directory IDs or native GUI APIs. Application use cases call narrow ports; adapters bind those ports to native systems. Process boundaries earn their cost through security, incompatibility, fault isolation or measured scaling. Do not create separate classes, packages or microservices merely because a diagram has a box.

Keep capability invocation separate from agent-session hosting. The same execution receipt can describe both without one seventy-method Provider interface. AIDE Lite distributions should be generated or wrapped from the same qualified source implementation, not independently maintained copies. Characterize old CLI outputs, exit codes and side effects before extraction. A new reuse candidate must demonstrate matching purpose and contract; duplication can be the safer temporary choice when domains differ.

## Interface and data boundary

Module owner; input/output contract; permitted dependencies; prohibited dependencies; side effects; compatibility entrypoints; characterization tests; extraction decision.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-ARCH-01 — Preserve existing code

An implementation plan MUST inventory relevant existing mechanisms and tests before replacing them.

### UR-ARCH-02 — Pure semantic boundary

Reusable semantic modules MUST not require a particular self-host queue path, task ID, UI toolkit or provider SDK.

### UR-ARCH-03 — Two execution contracts

Deterministic capability execution and bounded worker-session hosting MUST remain distinct contracts.

### UR-ARCH-04 — Measured decomposition

A new package or service boundary MUST identify a real security, compatibility, dependency, ownership or scale reason.

### UR-ARCH-05 — One source distribution

Portable Lite and managed-runtime distributions MUST derive from one qualified implementation or explicitly tested compatibility wrappers.

### UR-ARCH-06 — Characterize before extraction

Refactors MUST preserve relevant CLI, import, diagnostic and side-effect contracts through characterization tests or explicit migrations.

### UR-ARCH-07 — No speculative universalization

Shared utilities MUST be promoted on matching semantic contracts and representative consumers, not superficial textual similarity.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-ARCH-01` | A new broker proposal overlaps the task-branch broker. | The plan records keep/adapt/extract/supersede dispositions before any replacement build. |
| `UC-ARCH-02` | Run a core validator against a neutral fixture outside the AIDE checkout. | It accepts explicit inputs and returns typed results without reading hidden project state. |
| `UC-ARCH-03` | Add a validator and a long-lived coding session. | Neither is forced to emulate the other’s lifecycle or approval semantics. |
| `UC-ARCH-04` | Propose a microservice for a pure local serializer. | It remains a module unless the added boundary is justified. |
| `UC-ARCH-05` | Fix a shared serializer. | Both distribution forms pick up the same qualified behavior without a second manual patch. |
| `UC-ARCH-06` | Move a mature command into a package. | Its supported behavior remains equal or a documented breaking migration applies. |
| `UC-ARCH-07` | Two domain validators share syntax but different authority rules. | Reuse is rejected or scoped to safe mechanics only. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
