---
type: AIDE Engineering Specification
title: Brownfield adoption and ownership
description: Observe a project before installing anything into it; an AIDE source checkout is not an installed AIDE target.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P04
  resource: urn:aide:source-package:b3f3d0d27109a986e537928523c9c34f31e3458986c7632e97abee06d85db64c
  title: AIDE-Spec-Overhaul-2026-09-20(3)(1).zip
- id: P09
  resource: urn:aide:source-package:fe066ea7e776bdd6f53ae3dc03b90f0da4c97b981acfd345cfb5fc4be343029b
  title: AIDE-Spec-Overhaul-2026-09-20-r2(5)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P16
  resource: urn:aide:source-package:635f61aafab254ead0014e09e34a41acf9150282af60afbee0460157301a03a9
  title: AIDE-Spec-Overhaul-Refresh-2026-09-20(1).zip
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
  owner: target project and install owner
  applicability: baseline lifecycle
  requirement_ids:
  - UR-ADOPT-01
  - UR-ADOPT-02
  - UR-ADOPT-03
  - UR-ADOPT-04
  - UR-ADOPT-05
  - UR-ADOPT-06
  - UR-ADOPT-07
---

# Brownfield adoption and ownership

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Observe a project before installing anything into it; an AIDE source checkout is not an installed AIDE target.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Discover current tools, queue, policy, generated regions, local state, releases, fixtures and target-native validation. A project may keep its own directory layout, native formats and domain contracts. Map them through a profile instead of forcing every repository into AIDE’s self-hosting shape. A static/offline profile can provide useful knowledge, validation and evidence without a daemon.

Keep installed vendor-managed files, managed sections, project-owned source, local overlays, generated outputs, retained evidence, preserved legacy material, local-only state, unknown and never-touch paths distinct. Ownership has a writer, baseline hash, source package and conflict rule. Discovery is not ownership. A new package cannot claim old user files by naming their directory.

Prefer an external versioned runtime plus a small project lock and bootstrap where appropriate, while preserving an embedded portable Lite mode for offline/USB/legacy use. Both derive from the same qualified implementation. Projects generate their own inventories and knowledge; do not transplant the source AIDE queue, runtime logs or accepted-capability claims into consumers. Repeated adoption and interrupted setup need idempotent observation and explicit recovery.

## Interface and data boundary

Project identity; native authorities; adoption profile; installation mode; package lock; owned paths/sections; baseline hashes; protected content; conflicts; target-local outputs; validation.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-ADOPT-01 — Observe before adoption

Adoption MUST inventory target-owned tools, policies, state and conflicts before proposing changes.

### UR-ADOPT-02 — No copied source truth

Distribution/import MUST NOT copy AIDE source-repository queue history, runtime state or generated inventory as target truth.

### UR-ADOPT-03 — Explicit ownership

Each lifecycle-managed file or section MUST have an owner, baseline and preservation policy before destructive modification.

### UR-ADOPT-04 — Portable modes

Managed-runtime and embedded-portable installations MUST preserve equivalent admitted semantics while declaring deployment limits.

### UR-ADOPT-05 — Target layout freedom

Target profiles MUST support project-selected roots and native conventions rather than require an AIDE directory migration.

### UR-ADOPT-06 — Self-consumer separation

AIDE self-install/update qualification MUST use an explicit consumer fixture or admitted target, not overwrite the source checkout as an installed copy.

### UR-ADOPT-07 — Repeated bootstrap recovery

Bootstrap MUST detect an existing partial or repeated installation and plan repair/reconciliation without silent duplication.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-ADOPT-01` | A target already has an authoritative queue. | AIDE adapts to it or proposes an explicit migration rather than installing a competing queue. |
| `UC-ADOPT-02` | Install Lite into MIR. | The target regenerates its own observations and retains its product authority. |
| `UC-ADOPT-03` | A package claims a previously user-authored file. | Unknown ownership blocks overwrite. |
| `UC-ADOPT-04` | Run the portable profile without an external service. | Supported local inspection still works; unsupported live features are refused. |
| `UC-ADOPT-05` | A target stores specs under docs/design. | The mapping uses that root without forced renaming. |
| `UC-ADOPT-06` | Test a new repository pack. | The source authority remains unchanged while the consumer fixture exercises installation. |
| `UC-ADOPT-07` | Interrupt initial setup and rerun it. | Ownership and partial operations are reconciled before new writes. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
