---
type: AIDE Engineering Specification
title: Integration broker and authoritative closeout
description: Freeze a candidate, verify it, obtain separate authority, then observe the exact integrated result.
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
- id: P09
  resource: urn:aide:source-package:fe066ea7e776bdd6f53ae3dc03b90f0da4c97b981acfd345cfb5fc4be343029b
  title: AIDE-Spec-Overhaul-2026-09-20-r2(5)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P18
  resource: urn:aide:source-package:d61e3fe58a17ae0b729d36519b23ba123de87571c55fcf0128f06e34e7c26723
  title: AIDE-Spec-Overhaul-v2-2026-09-20(1)(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: target owner and broker
  applicability: protected integration
  requirement_ids:
  - UR-INT-01
  - UR-INT-02
  - UR-INT-03
  - UR-INT-04
  - UR-INT-05
  - UR-INT-06
  - UR-INT-07
  - UR-INT-08
---

# Integration broker and authoritative closeout

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Freeze a candidate, verify it, obtain separate authority, then observe the exact integrated result.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

The existing broker task branch contains significant foundation code and source review. Its status remains running/PENDING with full_broker_completion false. Reconcile this code before introducing a replacement. Separate candidate freezing, prepared-generation custody, authority issuance, provider observations, staged effect intents and target-enforced mutation predicates.

A candidate includes exact base identity, changed regular-file bytes, modes and explicit deletions; unchanged objects come from a protected trusted base store, not mutable worker Git objects. Source, index, control metadata, path interpretation and dependency pins need validation. A request-bound receipt is insufficient if its producer did not observe the real target. Preserve the difference between submitted, acknowledged, merged and independently observed integrated content.

Local pre-reads and expected-head APIs do not necessarily implement an atomic exact-base predicate at a remote merge boundary. Qualification must prove the actual target contract or disable that integration mode. Merge, squash, rebase and cherry-pick each need explicit source-to-result mappings; do not infer completion from ancestry alone. A changed base invalidates applicable assurance and requires re-preparation, not a silent rebase of reviewed bytes. Signing, publication and promotion remain separate effects and authorities.

## Interface and data boundary

Frozen candidate; protected base; prepared generation identity; request digest; authority issuer; actor; expected refs; check identity; intent per stage; authoritative observation; receipt.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-INT-01 — Reconcile existing broker

Broker work MUST be inventoried by pinned branch/source and assigned keep/adapt/extract/repair/supersede dispositions before overlapping replacement work.

### UR-INT-02 — Exact candidate binding

Integration MUST bind exact base, changed bytes, modes, deletions, candidate tree, assurance and required checks.

### UR-INT-03 — Protected custody

Broker preparation MUST derive unchanged content from an admitted protected store and revalidate prepared content at the effect boundary.

### UR-INT-04 — Independent integration authority

Coding workers and coordinators MUST NOT mint their own protected integration authority.

### UR-INT-05 — Real atomic predicate

An integration binding MUST qualify the actual server-side or target-side stale-safety predicate rather than infer it from local checks.

### UR-INT-06 — Intent per effect stage

Publication, branch creation, PR creation and merge MUST have distinct durable effect identities and finite attempt budgets where separately consequential.

### UR-INT-07 — Observe closeout

An apply acknowledgement MUST NOT close a WorkUnit; closeout MUST observe the request-bound integrated result and required postconditions.

### UR-INT-08 — Explicit merge method

Integration evidence MUST record merge method and its source-to-result correspondence; changed candidates require renewed assurance.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-INT-01` | A plan proposes a new broker while the task branch exists. | The existing implementation and open qualification gaps are explicitly reconciled. |
| `UC-INT-02` | A worker changes a file after assurance. | The old integration request cannot authorize the changed candidate. |
| `UC-INT-03` | A mutable worker object store supplies altered base objects. | Preparation or apply refuses before target mutation. |
| `UC-INT-04` | The worker provides a self-signed approval boolean. | It is not accepted as issuer authorization. |
| `UC-INT-05` | The base changes after local preflight but before remote merge. | The required exact-base mode refuses or remains unavailable. |
| `UC-INT-06` | A PR-creation response is lost. | The operation is observed by identity rather than repeated from absence. |
| `UC-INT-07` | The provider says submitted. | The task remains pending integration until authoritative result verification. |
| `UC-INT-08` | Switch from ordinary merge to squash. | The old ancestry-only check is not treated as sufficient. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
