---
type: AIDE Engineering Specification
title: Local durability, events and artifact storage
description: One durable local implementation is the first runtime; distributed backends are later substitutions, not architectural prerequisites.
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
  owner: service storage owner
  applicability: local service and continuous worker
  requirement_ids:
  - UR-SERVICE-01
  - UR-SERVICE-02
  - UR-SERVICE-03
  - UR-SERVICE-04
  - UR-SERVICE-05
  - UR-SERVICE-06
  - UR-SERVICE-07
---

# Local durability, events and artifact storage

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

One durable local implementation is the first runtime; distributed backends are later substitutions, not architectural prerequisites.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Use transactional storage for object revisions, idempotency and effect intents; append-only trust-bearing events for history; content-addressed artifacts for large immutable payloads; rebuildable projections for queries; and mutable caches for performance. Do not event-source every progress counter or UI preference. Canonical operational state belongs to its named writer, not both SQLite and independently edited JSONL files.

SQLite is a sensible local reference, but journal mode, filesystem and version form part of the qualified deployment profile. WAL is not a universal network-filesystem or removable-media guarantee. USB deployment may be read-only or use a local writable state root with an explicit export checkpoint. A directory path is not volume identity. Failures such as full storage, fsync errors, corrupt journals, missing blobs and interrupted migration need visible classifications.

Store artifacts before referencing them as complete; publish their metadata only after immutable content verification. Record object/event/artifact reachability and retention. Snapshot and compact under a declared watermark while preserving active readers, leases, unresolved effects, releases and holds. Backups must be restored and checked, not merely copied. Durable control records must not include raw credentials; content-addressing does not remove confidentiality concerns.

## Interface and data boundary

Object revision; event sequence per stream; idempotency scope; intent ledger; artifact digest/media/size; storage profile; snapshot watermark; retention; backup/restore receipt.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-SERVICE-01 — Atomic durable transitions

Object updates, trust events and idempotency outcomes that form one semantic transition MUST commit atomically or expose a recoverable incomplete state.

### UR-SERVICE-02 — Qualified storage

Durability claims MUST name storage engine/version, journal mode, filesystem and failure model.

### UR-SERVICE-03 — Artifact custody

Completed artifact references MUST bind verified immutable bytes, size, media type and retention class.

### UR-SERVICE-04 — Rebuildable views

Query indexes, caches and status projections MUST be reconstructable from their declared authoritative sources.

### UR-SERVICE-05 — Restart persistence

Restart MUST preserve cancellations, reservations, unresolved effects, budgets and work lineage.

### UR-SERVICE-06 — Storage exhaustion

Before writing, runtime MUST reserve or check bounded capacity and report whether enforcement is hard, monitored or advisory.

### UR-SERVICE-07 — Restore proof

Backup, snapshot and migration claims MUST include restoration tests for the admitted scope.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-SERVICE-01` | Crash between object update and event publication. | Recovery does not invent a completed transition or lose the pending intent. |
| `UC-SERVICE-02` | Move a WAL database to an unqualified shared filesystem. | The deployment cannot inherit the original durability claim. |
| `UC-SERVICE-03` | Delete or alter a referenced blob. | Consumers flag missing/corrupt evidence rather than trusting the metadata alone. |
| `UC-SERVICE-04` | Delete a derived index. | Rebuild produces the same scoped view or explicit missing-source diagnostics. |
| `UC-SERVICE-05` | Restart after a cancelled attempt with outstanding spend. | Neither cancellation nor liability is reset. |
| `UC-SERVICE-06` | The storage pool becomes full mid-run. | Work stops or degrades according to profile and retains an honest recovery state. |
| `UC-SERVICE-07` | A copied database cannot restore referenced evidence. | Backup status is incomplete rather than recovery-qualified. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
