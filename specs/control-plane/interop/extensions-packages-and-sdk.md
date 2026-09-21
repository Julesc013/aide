---
type: AIDE Engineering Specification
title: Extension packages, roles and SDKs
description: One package lifecycle is useful; one giant operational plugin interface is not.
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
  owner: extension lifecycle and capability owners
  applicability: extension profiles
  requirement_ids:
  - UR-EXT-01
  - UR-EXT-02
  - UR-EXT-03
  - UR-EXT-04
  - UR-EXT-05
  - UR-EXT-06
  - UR-EXT-07
---

# Extension packages, roles and SDKs

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

One package lifecycle is useful; one giant operational plugin interface is not.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Use a common versioned package envelope for identity, provenance, dependency and compatibility metadata. Components implement role-specific contracts: capability provider, worker harness, execution host, inference backend, host adapter, domain bridge, sandbox, test backend, knowledge source, workflow, policy or experience. Multiple roles can live in one package without inheriting each other’s privileges.

Prefer declarative packages when no executable behavior is required. Optional execution forms include sandboxed components, out-of-process native sidecars, containers, remote services, protocol bindings and host-native extensions. Native host bridges remain necessary for old IDEs and genuine editor APIs; WASI or OCI is not a mandatory lowest common denominator.

Discover, inspect, validate, conformance-test, admit an exact digest, grant scoped use, observe, revoke, upgrade and retire. Installation alone never makes a component callable. SDKs should be generated or contract-checked where practical and expose explicit ownership, version negotiation, cancellation and diagnostics. Do not build a marketplace or every language SDK before one local worker and one contrasting host prove the boundary.

## Interface and data boundary

Package identity/digest; publisher/licence; components/roles; dependencies; required capabilities; permissions; runtime form; conformance; admission; migration/rollback; known limits.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-EXT-01 — Role-specific interfaces

A common extension envelope MUST contain role-specific contracts rather than one interface with unrelated optional methods.

### UR-EXT-02 — Install is not admission

Installing or discovering a package MUST NOT activate capabilities or grant execution authority.

### UR-EXT-03 — Exact implementation admission

Admission MUST bind exact component digest, dependency closure and conformance profile.

### UR-EXT-04 — Contained extension execution

Untrusted executable extensions MUST use a qualified isolation boundary; in-process loading requires an explicit trusted profile.

### UR-EXT-05 — Ownership-aware updates

Extension upgrade, disable, rollback and removal MUST respect resource ownership, active runs and compatibility.

### UR-EXT-06 — SDK conformance

SDKs and generated bindings MUST be tested against the same versioned contract and failure fixtures.

### UR-EXT-07 — Ecosystem sequencing

Marketplace and broad SDK rollout MUST follow demonstrated package admission, revocation, update and recovery behavior.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-EXT-01` | Add a UI experience and a model backend to one package. | Each declares its own inputs, permissions and qualification. |
| `UC-EXT-02` | A package is downloaded from a registry. | Its capabilities remain unadmitted until relevant gates pass. |
| `UC-EXT-03` | An admitted package dependency changes. | The changed closure does not inherit admission silently. |
| `UC-EXT-04` | An arbitrary plugin requests direct kernel imports. | The default binding refuses ambient in-process authority. |
| `UC-EXT-05` | Upgrade changes a component while an unresolved run uses it. | The old binding remains retained or the run is reconciled before retirement. |
| `UC-EXT-06` | Two SDKs serialize unknown optional data differently. | Round-trip loss is detected and qualified per binding. |
| `UC-EXT-07` | Only a manifest format exists. | The roadmap does not claim a trustworthy package ecosystem. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
