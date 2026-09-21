---
type: AIDE Engineering Specification
title: Structure, naming, purpose and safe reuse
description: Prevent avoidable structural churn, but do not promise perfect names or prohibit justified evolution.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P04
  resource: urn:aide:source-package:b3f3d0d27109a986e537928523c9c34f31e3458986c7632e97abee06d85db64c
  title: AIDE-Spec-Overhaul-2026-09-20(3)(1).zip
- id: P05
  resource: urn:aide:source-package:a247c622c6987787cae0fe18ff9383bb202f185b7e99bf1ce22478d42412e36a
  title: AIDE-Spec-Overhaul-2026-09-20-R2(1)(1).zip
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
  owner: project structure owner
  applicability: structure-intelligence profiles
  requirement_ids:
  - UR-STRUCT-01
  - UR-STRUCT-02
  - UR-STRUCT-03
  - UR-STRUCT-04
  - UR-STRUCT-05
  - UR-STRUCT-06
  - UR-STRUCT-07
---

# Structure, naming, purpose and safe reuse

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Prevent avoidable structural churn, but do not promise perfect names or prohibit justified evolution.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

The physical tree is one human-facing projection of purpose, ownership, dependency direction and lifecycle. Durable roots deserve simple responsibility rules; functions and local variables do not all need handwritten YAML records. Infer routine symbol facts, inherit ownership conservatively and reserve explicit records for public contracts, ambiguity and consequential changes.

Before creating a durable root, public name or shared utility, inspect existing purpose and reuse candidates. Prefer a bounded existing owner when semantics match. Do not ban legitimate conventional names such as common or current globally; require a meaningful scope and owner. Dates and version ranges usually belong in artifact metadata, not reusable source-module names, but ecosystem-native paths and public versioned APIs can justify exceptions.

No file is immortal. Renames, splits, retirement and deletion are normal maintenance when justified. Require an impact map, actual consumer updates or compatibility shims, source-bound preimages, validation and recovery. Unknown ownership is not permission to delete. Preserve manual/untracked content and unique work; model-generated orphan classifications remain advisory. Do not build a directory bureaucracy larger than the code it manages.

## Interface and data boundary

Root/file purpose; ownership class; API stability; naming/placement rationale; consumers; generated status; conflicts; proposed move/alias; validation; disposition; recovery.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-STRUCT-01 — Purpose before durable expansion

New durable roots and shared public names MUST have a clear purpose, owner and dependency direction.

### UR-STRUCT-02 — Proportionate metadata

Structure tooling MUST support inherited/inferred metadata and MUST NOT require separate manual records for every trivial variable or scratch file.

### UR-STRUCT-03 — Reuse before duplicate

A new reusable helper MUST consider existing candidates and record a material non-reuse reason when duplicating equivalent behavior.

### UR-STRUCT-04 — Safe evolution

Rename, move, split or retirement MUST bind impact, consumers, compatibility and recovery rather than rely on aesthetic preference.

### UR-STRUCT-05 — Unknown ownership protection

Unknown or project-owned content MUST NOT be removed by automatic cleanup or updater inference.

### UR-STRUCT-06 — No arbitrary naming bans

Naming policies MUST allow documented ecosystem and domain exceptions and MUST NOT encode transient tool fashion as universal law.

### UR-STRUCT-07 — Structure is not behavior proof

Cohesion, size, complexity and reuse findings MUST remain evidence-qualified recommendations, not proof that a refactor improves correctness or performance.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-STRUCT-01` | An agent proposes a miscellaneous root for unrelated helpers. | Placement is rejected or narrowed to explicit owners. |
| `UC-STRUCT-02` | Index a large generated or local-symbol set. | The metadata cost stays bounded and its inference status is explicit. |
| `UC-STRUCT-03` | A task invents another path-normalization utility. | Existing semantic owners are presented before creation. |
| `UC-STRUCT-04` | Rename a stable public module. | Affected imports, links, packaging and tests are included in the plan. |
| `UC-STRUCT-05` | A scan finds an untracked file under a managed root. | It is preserved or explicitly reviewed, not silently deleted. |
| `UC-STRUCT-06` | An existing public API legitimately uses a versioned path. | It is assessed by compatibility needs rather than rejected by a blanket style rule. |
| `UC-STRUCT-07` | A module exceeds a line-count threshold. | The finding requests analysis without automatic splitting. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
