---
type: AIDE Engineering Specification
title: Context compilation and handoffs
description: A ContextPack is a source-bound selection and rendering contract, not a bag of tokens or a replacement for source truth.
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
- id: P10
  resource: urn:aide:source-package:d400ffa075586293031f1c2b82d59a6c5a60aaef97035932a28a59ace1a41014
  title: AIDE-Spec-Overhaul-2026-09-20-R2(6)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P20
  resource: urn:aide:source-package:90f79366cb02f34d737950db6708c087db367e36e7ce5ff98f7d953c6a82fb96
  title: AIDE-Specification-Overhaul-2026-09-20(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: context compiler
  applicability: all profiles
  requirement_ids:
  - UR-CTX-01
  - UR-CTX-02
  - UR-CTX-03
  - UR-CTX-04
  - UR-CTX-05
  - UR-CTX-06
  - UR-CTX-07
---

# Context compilation and handoffs

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

A ContextPack is a source-bound selection and rendering contract, not a bag of tokens or a replacement for source truth.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Start with admitted intent and mandatory constraints. Add direct target resources, relevant definitions and dependencies, tests, accepted decisions, explanatory OKF concepts, recent evidence and known failure lessons. Exact/lexical retrieval and graph navigation remain first-class; embeddings are optional derived indexes. Permissions apply before retrieval, graph expansion, summarization, caching and export—not only at the final model call.

Keep a reference map, selected source excerpts and actual provider rendering distinct. Record why each item was selected, what was redacted or omitted, its trust class, instruction authority, revision and dependency closure. Compression must preserve negation, units, safety constraints, ownership boundaries and acceptance obligations. Missing required context is a blocker or explicit narrowing decision; it is not a license to guess.

Provider rendering depends on tool schemas, chat templates, tokenizer and harness behavior. Budget the actual rendered request, output and continuation needs rather than a global characters/4 estimate. Handoffs contain verified facts separately from hypotheses. A restarted writer receives the actual document, reader brief, permitted edit scope and qualified facts; memory of an earlier chat is not enough. The operator can inspect a Context Lens before sensitive context leaves the boundary.

## Interface and data boundary

Selected segments; source/revision/range; selection reason; required coverage; omissions/redactions; trust/sensitivity; instruction authority; renderer/tokenizer; rendered digest; budget.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-CTX-01 — Source-bound context

ContextPack MUST bind task, target revision, relevant policy and exact selected sources.

### UR-CTX-02 — Mandatory coverage

Compression MUST preserve required constraints and report missing mandatory context rather than silently dropping it.

### UR-CTX-03 — Permission before retrieval

Data permissions MUST apply before retrieval, graph expansion, cache lookup and outbound rendering.

### UR-CTX-04 — Three representations

Reference maps, selected excerpts and actual provider renderings MUST be separately identifiable.

### UR-CTX-05 — No instruction laundering

Source code, docs, web pages, tool output and summaries MUST remain data unless a separate admitted source grants instructional authority.

### UR-CTX-06 — Omission visibility

Context receipts MUST expose selection reasons, omissions, truncation and uncertainty with bounded cost.

### UR-CTX-07 — Useful handoff

Continuation packs MUST preserve neutral failure evidence, best verified work, remaining requirements and unresolved effects.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-CTX-01` | Source changes after compilation. | The pack is stale for affected execution until recompiled or explicitly revalidated. |
| `UC-CTX-02` | A token limit would remove a forbidden-path rule. | Compilation refuses or narrows scope instead of deleting the rule. |
| `UC-CTX-03` | A graph edge points to a restricted project. | The restricted content is not retrieved merely to redact it later. |
| `UC-CTX-04` | Two harnesses render the same references differently. | Receipts retain the actual rendering identity for each attempt. |
| `UC-CTX-05` | A retrieved README contains hostile tool instructions. | Those instructions cannot widen effective grants. |
| `UC-CTX-06` | A large document is summarized rather than read in full. | The receipt does not claim full-document coverage. |
| `UC-CTX-07` | A successor changes harness. | It can resume safely without proprietary session memory. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
