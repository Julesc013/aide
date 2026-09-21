---
type: AIDE Engineering Specification
title: Documentation, editorial intent and knowledge truth
description: Correctness includes reader usefulness and continuity, not only link validity or a terse status paragraph.
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
  owner: document owner and reviewer
  applicability: all documentation profiles
  requirement_ids:
  - UR-DOC-01
  - UR-DOC-02
  - UR-DOC-03
  - UR-DOC-04
  - UR-DOC-05
  - UR-DOC-06
  - UR-DOC-07
  - UR-DOC-08
  - UR-DOC-09
---

# Documentation, editorial intent and knowledge truth

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Correctness includes reader usefulness and continuity, not only link validity or a terse status paragraph.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Distinguish create, maintain, restore, redesign, translate and retire. Ordinary requests to update documentation mean bounded maintenance unless a redesign is explicitly requested. Preserve the purpose, audience, useful explanations, voice, identity, badges, licences and notices of a README; do not turn it into an execution log. A useful catalogue or important warning may belong on the front page—there is no universal rule that all technical detail must be moved away.

A reader brief records intended users, starting knowledge, tasks they must complete and allowed editorial change. Approval may cover only identity text or one factual section; being at HEAD, merged, test-green or unchanged after silence does not make the whole document a golden editorial baseline. Review the actual semantic diff and the resulting reader experience independently of the writer’s description.

Keep authored contracts, explanatory reference, tutorials, generated operational views and historical evidence visibly distinct. Mixed documents require managed regions with exact ownership boundaries. Comments may record domain rationale, invariants, warnings or obsolete assumptions: classify and preserve useful meaning rather than delete by style. Trace factual claims to qualified source/evidence and test instructions within their own execution authorization. Learn from before/request/facts/after examples, not only finished templates or a list of forbidden words.

## Interface and data boundary

Reader brief; edit mode; source/approval scope; authored/generated regions; fact evidence; semantic diff; reader tasks; cumulative baseline; exceptions; publication digest.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-DOC-01 — Bounded maintenance

Documentation updates MUST default to scoped maintenance and allow a justified no-change result rather than assume a rewrite.

### UR-DOC-02 — Preserve purpose

Edits MUST preserve the document’s reader purpose, useful voice, identity and protected licence/notice material unless explicitly authorized.

### UR-DOC-03 — Reader tasks

New and maintained documents MUST be evaluated against intended reader tasks as well as factual and structural checks.

### UR-DOC-04 — Scoped editorial approval

Approval evidence MUST state which text, purpose or change scope was approved and MUST NOT infer global approval from a merge or silence.

### UR-DOC-05 — Generated ownership

Generated regions MUST name generator, source cutoff and edit owner; malformed or overlapping managed boundaries MUST refuse rewriting.

### UR-DOC-06 — Independent semantic review

Documentation review MUST compare actual changed meaning and final reader experience, not only the writer’s summary.

### UR-DOC-07 — Factual freshness

Current implementation and readiness statements MUST be source-bound and not copied from stale chat milestones.

### UR-DOC-08 — Cumulative drift

Where an approved editorial baseline exists, repeated maintenance MUST be checked for cumulative meaning or purpose drift.

### UR-DOC-09 — Publication binding

Publication MUST use the reviewed rendered output and relevant dependency identities; changed regeneration invalidates affected approval.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-DOC-01` | The user requests a status correction. | Unrelated explanation, structure and voice remain intact. |
| `UC-DOC-02` | A model replaces a README with a queue report. | Editorial validation rejects the purpose regression. |
| `UC-DOC-03` | All links resolve but a new user cannot find installation prerequisites. | The documentation does not pass the reader-usefulness gate. |
| `UC-DOC-04` | A badge update is approved. | Unrelated wording does not become a new approved baseline by implication. |
| `UC-DOC-05` | A document contains nested or broken managed markers. | The updater preserves bytes and reports a conflict. |
| `UC-DOC-06` | A harmless-looking rewrite drops a safety exception. | The omission is detected as a substantive change. |
| `UC-DOC-07` | A June report says no runtime while main has a prototype. | The status distinguishes historical report and current prototype qualification. |
| `UC-DOC-08` | Many small edits gradually remove required explanations. | Review can detect regression against the scoped approved baseline. |
| `UC-DOC-09` | Rebuild docs with a different template after review. | The prior publication approval is not silently reused. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
