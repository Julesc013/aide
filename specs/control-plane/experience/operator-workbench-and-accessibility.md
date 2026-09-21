---
type: AIDE Engineering Specification
title: Operator experience, Workbench and accessibility
description: The architecture can be rigorous while the interface remains task-oriented and legible.
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
- id: P08
  resource: urn:aide:source-package:17ff6721596aa57145ac767276aab0332f179d474065d81b314d103e71c6d979
  title: AIDE-Spec-Overhaul-2026-09-20-R2(4)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P16
  resource: urn:aide:source-package:635f61aafab254ead0014e09e34a41acf9150282af60afbee0460157301a03a9
  title: AIDE-Spec-Overhaul-Refresh-2026-09-20(1).zip
- id: P18
  resource: urn:aide:source-package:d61e3fe58a17ae0b729d36519b23ba123de87571c55fcf0128f06e34e7c26723
  title: AIDE-Spec-Overhaul-v2-2026-09-20(1)(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: experience owner
  applicability: CLI and optional host experiences
  requirement_ids:
  - UR-UX-01
  - UR-UX-02
  - UR-UX-03
  - UR-UX-04
  - UR-UX-05
  - UR-UX-06
  - UR-UX-07
---

# Operator experience, Workbench and accessibility

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

The architecture can be rigorous while the interface remains task-oriented and legible.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Show the next safe action, current outcome, active constraint and useful evidence by default. Let users expand into exact sources, policy, budgets, telemetry and recovery details. A Context Lens shows what will be sent; a Plan Card shows operations and alternatives; a Preview Canvas uses native diffs/graphs/scenes; an Evidence Drawer shows what was and was not checked; Recovery exposes cancel, retain, undo, repair and export.

Ask, Plan, Preview, Apply and Delegate are interaction stages. Observe, Assist, Execute and Orchestrate are policy profiles. Neither a button label nor a stronger model grants authority. Routine qualified low-risk work should not demand repeated redundant consent; consequential changes require the applicable exact approval. Avoid asking users for information that can be safely retrieved from admitted sources.

Workbench focuses on one project and native authoring; Commander focuses on multiple projects, workers, budgets and estate. They may share a shell but must not share duplicated authority records. Generic schema-derived forms make new capabilities usable before custom UI exists. Native experiences can render scenes, graphs, assets, simulation or performance comparisons. Accessibility—keyboard use, screen readers, non-colour status, scalable text, reduced motion and useful errors—is a first-class acceptance dimension, not a final skin.

## Interface and data boundary

User intent; current work/next-action; context lens; plan; preview; effect/approval state; budget uncertainty; evidence; accessible labels; recovery; host capabilities.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-UX-01 — One semantic surface

Equivalent CLI, TUI, GUI, SDK and host actions MUST call the same application semantics and return the same work/evidence identities.

### UR-UX-02 — Progressive disclosure

Default output MUST explain interpretation, current state, constraints and the exact next safe action without dumping raw logs.

### UR-UX-03 — Inspectable context

Before outbound sensitive work, the user MUST be able to inspect the actual context scope, destination and applicable data constraints.

### UR-UX-04 — No UI authority shortcut

Interaction stages and policy profiles MUST not bypass grants, preview or domain apply authority.

### UR-UX-05 — Generic then native

Capabilities SHOULD supply metadata for a usable generic interface while allowing native domain-specific previews.

### UR-UX-06 — Accessible operation

Qualified interfaces MUST test keyboard, screen-reader, non-colour and error-recovery paths appropriate to the host.

### UR-UX-07 — Human judgments remain explicit

Visual, physical, experiential and other required human judgments MUST remain explicit gates, not inferred automated passes.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-UX-01` | Inspect a task through Workbench and CLI. | Both show the same source-bound acceptance state. |
| `UC-UX-02` | A task blocks on expired authority. | The interface explains the reason and remediation with optional evidence drill-down. |
| `UC-UX-03` | A plan includes private source. | The Context Lens exposes the selected source and allowed destination. |
| `UC-UX-04` | A user clicks an Apply button on a preview-only host. | The host returns a typed unsupported/approval-required response rather than executing. |
| `UC-UX-05` | A new validator lacks a custom panel. | It can still be inspected through a generic typed view. |
| `UC-UX-06` | A warning is visible only as a colour. | Accessibility validation flags missing semantic labeling. |
| `UC-UX-07` | An exact image hash comparison passes. | Artistic acceptance remains separate when the project requires it. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
