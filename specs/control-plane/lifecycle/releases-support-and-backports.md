---
type: AIDE Engineering Specification
title: Releases, support and backports
description: Qualify a payload once, then promote and publish those exact bytes through separately authorized stages.
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
- id: P09
  resource: urn:aide:source-package:fe066ea7e776bdd6f53ae3dc03b90f0da4c97b981acfd345cfb5fc4be343029b
  title: AIDE-Spec-Overhaul-2026-09-20-r2(5)(1).zip
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
  owner: release authority
  applicability: distribution/release profiles
  requirement_ids:
  - UR-REL-01
  - UR-REL-02
  - UR-REL-03
  - UR-REL-04
  - UR-REL-05
  - UR-REL-06
  - UR-REL-07
  - UR-REL-08
---

# Releases, support and backports

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Qualify a payload once, then promote and publish those exact bytes through separately authorized stages.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

A product release, protocol version, schema version, profile, package composition and channel alias are not one identity. Channels such as canary, stable or LTS are mutable references under release authority; artifacts and locks are immutable digest-pinned subjects. Source, package, signing, publication and support are distinct gates.

Use a manifest-defined composition with dependency closure, licences/notices, SBOM/provenance, supported profiles and explicit unsigned or signed posture. Extract the candidate and test installed behavior without imports from the source checkout. Build-once promotion avoids a different stable rebuild invalidating qualification. Re-download published bytes and compare them with the qualified digest where a publication profile requires this.

Canaries should represent different failure modes: AIDE self-consumer for self-update, MIR for target-native mod/release constraints, ScreenSave for deterministic visual/legacy artifacts, Eureka for provenance, and Dominium for governed domain commands. Current priority is a project decision, not a forever hard-coded order. Backports require semantic-difference and target-validation closure; sharing a code patch does not prove behavior or package parity. Supply-chain signatures establish provenance under a trust policy, not universal safety or licence permission.

## Interface and data boundary

Release identity; composition digest; version axes; channel pointer; dependency closure; qualification matrix; SBOM/provenance; signing/publication authority; canaries; backport differences.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-REL-01 — Exact-byte promotion

Release promotion MUST use the exact qualified payload and composition rather than rebuild them after acceptance.

### UR-REL-02 — Separate release effects

Building, signing, publishing, installing and declaring support MUST require distinct applicable authority and evidence.

### UR-REL-03 — Immutable locks

Locks and artifacts MUST use immutable identities while mutable channel aliases are separately recorded effects.

### UR-REL-04 — Consumer qualification

Release qualification MUST exercise extracted installed packages and representative consumer profiles.

### UR-REL-05 — Canary diversity

Shared lifecycle or provider claims MUST name representative consumers and their project-owned acceptance boundaries.

### UR-REL-06 — Backport intent

Backports MUST record intended semantic parity, target-specific differences and conservative validation closure.

### UR-REL-07 — Publication verification

A publication profile MUST verify visible distributed bytes and metadata against the sealed candidate before release closeout.

### UR-REL-08 — Support evidence

Support matrices MUST distinguish compile, link, runtime, package, upgrade, visual/manual and operational qualification.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-REL-01` | Stable build emits different bytes from the tested candidate. | The candidate qualification cannot be reused for the rebuilt payload. |
| `UC-REL-02` | A local archive builds successfully. | It does not imply permission to publish a release. |
| `UC-REL-03` | A latest alias changes. | An existing locked consumer still resolves the same admitted artifact. |
| `UC-REL-04` | Tests pass only with source-checkout imports. | The package fails installed-artifact qualification. |
| `UC-REL-05` | A bridge passes only its own fixture. | It is not labeled universal across all projects. |
| `UC-REL-06` | A legacy engine lacks a modern feature. | The backport explicitly omits/refuses it rather than advertise parity. |
| `UC-REL-07` | The registry serves a different payload digest. | Publication remains failed/uncertain and support is not promoted. |
| `UC-REL-08` | A Windows binary cross-compiles successfully. | Historical Windows runtime support is not inferred from compilation alone. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
