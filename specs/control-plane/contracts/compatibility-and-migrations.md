---
type: AIDE Engineering Specification
title: Compatibility and migration
description: Compatibility is a tested relation between exact profiles, not a promise about every future implementation.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
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
  owner: compatibility owner
  applicability: all profiles
  requirement_ids:
  - UR-COMP-01
  - UR-COMP-02
  - UR-COMP-03
  - UR-COMP-04
  - UR-COMP-05
  - UR-COMP-06
  - UR-COMP-07
---

# Compatibility and migration

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Compatibility is a tested relation between exact profiles, not a promise about every future implementation.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Version the product, protocol family, object schema, persisted state, adapter, conformance profile, OKF profile and package independently where their compatibility changes independently. Do not force every version into one SemVer number or create redundant minReader fields with no defined comparison semantics.

Readers may preserve unfamiliar optional data without using it to authorize an effect. Unknown required semantics must refuse the affected operation. This is not a reason to discard an entire document that can still be displayed safely. Distinguish parse compatibility, semantic compatibility, round-trip preservation, execution equivalence and supported migration. Migrations must disclose loss, invalidate dependent review and preserve recoverable preimages where lawful.

Prefer explicit compatibility fixtures over a permissive parser as proof. Test old client/new service and new client/old service, disconnected clients, retired enums, unknown capabilities, duplicate JSON keys, nullable fields, missing fields and cross-version event resumption. Upgrading on open or on discovery of a new upstream standard is prohibited. Stable source paths may coexist with versioned schema identities; neither requires version-number directory proliferation.

## Interface and data boundary

Compatibility profile; source/target versions; supported operations; losses; aliases; required features; migration ID; pre/postimage; review invalidation; recovery.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-COMP-01 — Independent version axes

Compatibility decisions MUST use explicit relevant version axes rather than infer all behavior from product version.

### UR-COMP-02 — Unknown optional data

Supported round trips MUST preserve safe unknown optional data or explicitly report loss before writing.

### UR-COMP-03 — Required semantics

Unknown required capabilities or security-relevant meaning MUST block the affected operation.

### UR-COMP-04 — Bounded support

Support claims MUST name tested reader/writer/profile combinations and MUST NOT promise unspecified future-version compatibility.

### UR-COMP-05 — Migration plan

Migration MUST bind source bytes, target profile, semantic changes, losses, review invalidations and rollback/forward-repair classification.

### UR-COMP-06 — No auto-upgrade on read

Reading, indexing or discovering a new format MUST NOT migrate authoritative content.

### UR-COMP-07 — Real compatibility aliases

Path or symbol compatibility claims MUST prove the relevant consumer actually resolves the alias/shim.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-COMP-01` | An adapter upgrades without changing the WorkUnit schema. | Only the affected adapter qualification is invalidated. |
| `UC-COMP-02` | Open an extension-bearing document with an older reader. | Read-only display works and no silent extension removal occurs. |
| `UC-COMP-03` | A newer transaction requires a capability the reader cannot interpret. | Execution refuses even if the generic JSON structure parses. |
| `UC-COMP-04` | An unseen OKF or external protocol revision appears. | It is a candidate profile, not automatically certified. |
| `UC-COMP-05` | Modify source after approving a migration. | Apply refuses stale preimages. |
| `UC-COMP-06` | A parser sees a newer advertised upstream version. | Content bytes remain unchanged unless a separate migration is authorized. |
| `UC-COMP-07` | Record an old import name only in metadata. | The system does not claim import compatibility without an executable import test. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
