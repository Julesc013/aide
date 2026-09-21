---
type: AIDE Engineering Specification
title: Standards profiles and loss-aware translation
description: Use open standards at the edges while retaining AIDE and target semantic authority.
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
- id: P10
  resource: urn:aide:source-package:d400ffa075586293031f1c2b82d59a6c5a60aaef97035932a28a59ace1a41014
  title: AIDE-Spec-Overhaul-2026-09-20-R2(6)(1).zip
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
  owner: binding owner
  applicability: interop profiles
  requirement_ids:
  - UR-INTEROP-01
  - UR-INTEROP-02
  - UR-INTEROP-03
  - UR-INTEROP-04
  - UR-INTEROP-05
  - UR-INTEROP-06
  - UR-INTEROP-07
---

# Standards profiles and loss-aware translation

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Use open standards at the edges while retaining AIDE and target semantic authority.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

MCP maps tool/resource interaction; A2A maps communication between independent agents; Agent Client Protocol maps editor/agent sessions. These descriptions are roles, not a guarantee that any current implementation supports every desired behavior. Expand ambiguous names and pin the actual upstream specification, schema, adapter and selected subset before implementation.

OpenAPI, CloudEvents, OpenTelemetry, SARIF, JUnit/TAP, SBOM and provenance standards address different boundaries. Do not emit a look-alike object and label it conformant. Keep domain proof and authority distinct from telemetry and transport acknowledgements. Future UI, identity, payment or network-agent standards such as AG-UI, A2UI, AP2 or ANP are candidate profiles only; they do not become mandatory core dependencies by appearing in a source pack.

Every material translation records source and target identity, mapped/native/emulated fields, unsupported optional semantics, missing required meaning and fidelity. Retain raw foreign payload references when lawful. Unknown required meaning refuses the dependent operation. Do not advertise an unimplemented skill or endpoint in a live-shaped discovery record; inactive fixtures must be explicitly non-publishable. Avoid pairwise adapters: normalize through owned AIDE contracts, while preserving domain-specific meaning in domain payloads.

## Interface and data boundary

Expanded standard name; steward/source URI; exact version/blob; subset/deviations; adapter digest; security relation; mapping/loss receipt; conformance; maturity; lifecycle.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-INTEROP-01 — Pinned standards

Bindings MUST name the exact upstream identity/version/profile and disambiguate protocol acronyms.

### UR-INTEROP-02 — No core authority transfer

External tools, transports, cards and schemas MUST remain adapters/projections rather than replacements for AIDE policy or work authority.

### UR-INTEROP-03 — Loss receipt

Material translation MUST report native, emulated, dropped and unsupported semantics and refuse missing required meaning.

### UR-INTEROP-04 — Honest discovery

Published capability/skill discovery MUST advertise only the actually admitted and available live surface.

### UR-INTEROP-05 — Independent conformance

Interop claims MUST use version-pinned positive and adversarial tests rather than only self-produced schema fixtures.

### UR-INTEROP-06 — Raw semantic preservation

Foreign payloads and exact source identifiers SHOULD be retained by reference under data policy to support audit and future remapping.

### UR-INTEROP-07 — Candidate standards stay optional

Unimplemented future standards MUST remain explicitly scoped candidate adapters with no automatic effect or purchase authority.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-INTEROP-01` | A package says ACP without specifying which protocol. | Qualification remains blocked until the intended standard is identified. |
| `UC-INTEROP-02` | A remote task object claims broader permissions. | AIDE applies its own grant and target policy constraints. |
| `UC-INTEROP-03` | A host cannot preserve cancellation semantics required by the task. | The execution mode refuses rather than silently degrade. |
| `UC-INTEROP-04` | A fixture Agent Card contains planned skills. | It remains non-publishable or removes those skills from the official live shape. |
| `UC-INTEROP-05` | A serializer emits legacy fields accepted by its own helper. | An independent upstream-profile check detects the mismatch. |
| `UC-INTEROP-06` | A normalizer cannot map one optional event field. | The loss is recorded and permitted raw evidence remains recoverable. |
| `UC-INTEROP-07` | An AP2-related proposal appears in a spec pack. | It does not authorize payments or become a baseline dependency. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
