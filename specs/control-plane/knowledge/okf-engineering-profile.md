---
type: AIDE Engineering Specification
title: OKF engineering profile and document codec
description: Use OKF 0.2 as the observed upstream structural profile, with an independently versioned AIDE extension and explicit conformance scope.
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
- id: P10
  resource: urn:aide:source-package:d400ffa075586293031f1c2b82d59a6c5a60aaef97035932a28a59ace1a41014
  title: AIDE-Spec-Overhaul-2026-09-20-R2(6)(1).zip
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
  owner: knowledge codec owner
  applicability: OKF reader/writer profiles
  requirement_ids:
  - UR-OKF-01
  - UR-OKF-02
  - UR-OKF-03
  - UR-OKF-04
  - UR-OKF-05
  - UR-OKF-06
  - UR-OKF-07
  - UR-OKF-08
---

# OKF engineering profile and document codec

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Use OKF 0.2 as the observed upstream structural profile, with an independently versioned AIDE extension and explicit conformance scope.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

The upstream format is not an AIDE execution protocol. The new engineering bundle in this proposal is specs/control-plane/: its concept pages declare type and draft status, its root index declares only okf_version metadata, and its update log uses dated headings. The preserved historical architecture and boot-slice material outside that bundle is not falsely advertised as newly OKF-qualified.

The producer-defined x_aide metadata records document class, owner, adoption state and requirement links without redefining upstream fields. In particular, upstream verified metadata is an advisory provenance signal, not an authorization credential; this generated draft supplies no invented human-verification stamp. AIDE resource identity remains distinct from OKF concept path identity.

Maintain a loss-aware document codec. Preserve original syntax spans, comments, frontmatter ordering, unknown metadata and body bytes for supported no-op operations. Do not canonicalize an authored README just to make JSON comparison convenient. A supported edit changes only authorized regions; a parser unable to round-trip safely can still provide read-only viewing with a precise refusal for writing. Limit YAML aliases, nesting, document sizes and resolver graph traversal. Code, skills, computation and attester references stay inert until separately admitted execution.

Operational knowledge generation from queue/evidence is a different use case from editing authored specifications. Both can emit OKF but have different owners, freshness and review rules. Record upstream/profile/parser versions and source identities. Future 0.3 or other profiles remain unqualified until a concrete source and migration matrix exist.

## Interface and data boundary

Upstream version/source; producer profile; bundle root; concept path; resource ref; document class; generated provenance; sources; review state; parser binding; losses; migration.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-OKF-01 — Independent profile versions

The upstream OKF version, AIDE engineering extension, parser binding and operational projection version MUST be separate.

### UR-OKF-02 — Correct upstream field meaning

AIDE MUST preserve upstream field semantics and MUST NOT treat verified or generated metadata as effect authorization.

### UR-OKF-03 — No-op preservation

Supported no-op document round trips MUST preserve original bytes; scoped edits MUST preserve unrelated authored regions.

### UR-OKF-04 — Safe parsing

Frontmatter, archive and link resolution MUST be bounded and non-executing, with path containment and explicit parse failures.

### UR-OKF-05 — Operation-specific tolerance

Unknown optional metadata or broken explanatory links MAY remain displayable; missing evidence-critical or required semantics MUST block the dependent effect.

### UR-OKF-06 — Authored versus generated

Authored specifications and generated explanations MUST have distinct ownership and update paths even when both use OKF.

### UR-OKF-07 — Explicit migration

Codec/profile upgrades MUST preserve provenance, disclose losses and invalidate dependent reviews where meaning changes.

### UR-OKF-08 — No future-version promise

The profile MUST name qualified versions and MUST NOT claim compatibility with an unspecified future upstream release.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-OKF-01` | An upstream optional field appears. | The reader can preserve it without claiming the AIDE extension has been upgraded. |
| `UC-OKF-02` | A document claims human verification in frontmatter. | No grant is created from that self-declared signal. |
| `UC-OKF-03` | Open and save a document with comments, unusual fences and unknown metadata. | No unrelated formatting or content rewrite occurs. |
| `UC-OKF-04` | A YAML alias expansion or link escape exceeds profile limits. | The reader reports refusal/incomplete coverage without executing or escaping. |
| `UC-OKF-05` | A wiki link is broken but a transaction evidence reference is missing. | Display remains possible while the transaction refuses. |
| `UC-OKF-06` | An agent edits a generated operational page as the new policy source. | The change is rejected or routed to its actual canonical owner. |
| `UC-OKF-07` | A migration renames a meaning-bearing metadata field. | It emits a source-bound plan rather than silently upgrading on read. |
| `UC-OKF-08` | A package advertises OKF 0.3 without a qualified mapping. | The support claim is rejected as unproven. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
