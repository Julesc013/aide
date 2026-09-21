---
type: AIDE Engineering Specification
title: Security, privacy and isolation qualification
description: A process limit is not a credential sandbox; a hash is not an authorization; a local model is not an offline guarantee.
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
- id: P06
  resource: urn:aide:source-package:83f9926500c47e3ee8384868c7d4046083e2a75bef0d667fb526c8476446d121
  title: AIDE-Spec-Overhaul-2026-09-20-R2(2)(1).zip
- id: P10
  resource: urn:aide:source-package:d400ffa075586293031f1c2b82d59a6c5a60aaef97035932a28a59ace1a41014
  title: AIDE-Spec-Overhaul-2026-09-20-R2(6)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P18
  resource: urn:aide:source-package:d61e3fe58a17ae0b729d36519b23ba123de87571c55fcf0128f06e34e7c26723
  title: AIDE-Spec-Overhaul-v2-2026-09-20(1)(1).zip
- id: P19
  resource: urn:aide:source-package:dab4e0eb3f7c39b80e03cf84748ec9f88a3603da6edbdebd534628cce325f832
  title: AIDE-Spec-Overhaul-v2-2026-09-20(2).zip
- id: P20
  resource: urn:aide:source-package:90f79366cb02f34d737950db6708c087db367e36e7ce5ff98f7d953c6a82fb96
  title: AIDE-Specification-Overhaul-2026-09-20(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: security and target authority
  applicability: all effect-capable profiles
  requirement_ids:
  - UR-SEC-01
  - UR-SEC-02
  - UR-SEC-03
  - UR-SEC-04
  - UR-SEC-05
  - UR-SEC-06
  - UR-SEC-07
  - UR-SEC-08
---

# Security, privacy and isolation qualification

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

A process limit is not a credential sandbox; a hash is not an authorization; a local model is not an offline guarantee.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Treat repository content, packages, external documents, provider output, tool logs, schemas and archives as untrusted inputs. Parse bounded structures, reject ambiguity at security-sensitive boundaries and keep imported code inert. Resolve paths using actual platform semantics, including symlinks/junctions, reparse points, case and Unicode collisions, device names and archive traversal.

Qualify process, filesystem, credentials, network, storage quota and identity boundaries independently. Windows Job Objects provide useful process containment but do not by themselves isolate same-user authentication files. Linked worktrees can share Git control state. Sanitized environments do not prevent arbitrary file reads by the same principal. Source pinning detects drift but cannot prove that the host performing the check is trusted.

Use explicit data classes and allowed destinations for prompts, logs, embeddings, speech, images, backups and support bundles. Preserve raw artifacts only when lawful and necessary; use redacted derivatives and provenance when full retention is unsafe. Outbound network and paid services require exact allowed identities/destinations, not broad claims that an SDK is safe. Define incident and revocation paths that stop new effects while allowing bounded authoritative reconciliation of uncertain ones.

## Interface and data boundary

Threat model; principal; executable/dependency pins; isolation domains; data class; allowed destinations; secret references; retention; quota class; incident/revocation; qualification scope.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-SEC-01 — Untrusted input boundaries

Repository, archive, tool, package and model inputs MUST be validated before influencing effects.

### UR-SEC-02 — Separate isolation properties

Process, filesystem, credential, network and storage isolation MUST be independently declared and qualified.

### UR-SEC-03 — No ambient secrets

Workers MUST receive only admitted minimum secret access through protected references, without committing or exposing raw credentials.

### UR-SEC-04 — Whole-system offline claim

Offline/privacy qualification MUST cover tools, telemetry, update checks, retrieval, embeddings and auxiliary models, not inference locality alone.

### UR-SEC-05 — Path semantics

Effectful filesystem boundaries MUST test traversal, links, case/Unicode aliases and relevant native path hazards.

### UR-SEC-06 — Independent source/host trust

Executable hashes and matching receipts MUST NOT substitute for authenticated authority and qualified host custody.

### UR-SEC-07 — Private review exports

Support and synthesis exports MUST disclose sensitivity and avoid publishing credentials, raw private prompts or unrestricted source by default.

### UR-SEC-08 — Revocation-aware recovery

Security revocation MUST stop new effects while preserving controlled observation and recovery of already uncertain effects.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-SEC-01` | An uploaded archive contains traversal or a generated instruction claims authority. | Extraction/resolution refuses or the content remains inert data. |
| `UC-SEC-02` | A process host enforces memory limits only. | It is not advertised as a credential/filesystem sandbox. |
| `UC-SEC-03` | A ContextPack contains an authentication file path. | The content is not copied into prompts or source evidence by default. |
| `UC-SEC-04` | A local model calls a cloud tool. | The deployment is not labeled offline-verified. |
| `UC-SEC-05` | A Windows drive-relative path is presented as repository-relative. | It is rejected before access. |
| `UC-SEC-06` | A compromised same-user worker can edit the checker’s state. | Hash equality alone does not qualify the isolation boundary. |
| `UC-SEC-07` | A user prepares a public support bundle. | The plan shows/redacts sensitive material before export. |
| `UC-SEC-08` | A broker token is revoked after a timeout. | The system does not blindly retry or delete the uncertainty record. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
