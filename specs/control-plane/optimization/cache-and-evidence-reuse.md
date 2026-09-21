---
type: AIDE Engineering Specification
title: Cache classes, validity and evidence reuse
description: A cache hit is a scoped reuse decision, not a generic proof of validity.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P03
  resource: urn:aide:source-package:dd3e3ea2b1581a03a97c569607fb0157ac47bd2ff7c0f3837c050d8b7f649fc0
  title: AIDE-Spec-Overhaul-2026-09-20(2)(1).zip
- id: P04
  resource: urn:aide:source-package:b3f3d0d27109a986e537928523c9c34f31e3458986c7632e97abee06d85db64c
  title: AIDE-Spec-Overhaul-2026-09-20(3)(1).zip
- id: P06
  resource: urn:aide:source-package:83f9926500c47e3ee8384868c7d4046083e2a75bef0d667fb526c8476446d121
  title: AIDE-Spec-Overhaul-2026-09-20-R2(2)(1).zip
- id: P09
  resource: urn:aide:source-package:fe066ea7e776bdd6f53ae3dc03b90f0da4c97b981acfd345cfb5fc4be343029b
  title: AIDE-Spec-Overhaul-2026-09-20-r2(5)(1).zip
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
  owner: cache and evidence owners
  applicability: cache-enabled profiles
  requirement_ids:
  - UR-CACHE-01
  - UR-CACHE-02
  - UR-CACHE-03
  - UR-CACHE-04
  - UR-CACHE-05
  - UR-CACHE-06
  - UR-CACHE-07
---

# Cache classes, validity and evidence reuse

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

A cache hit is a scoped reuse decision, not a generic proof of validity.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Separate provider prompt caching, local inference KV/prefix state, model-artifact caching, compiled ContextPacks, graph/retrieval indexes, deterministic tool/build outputs, test evidence and semantic answer candidates. Each has its own key, privacy boundary, freshness model, eviction cost and authority consequences. Inference state is often backend/model/template/tenant-specific and not portable merely because two workers share a model name.

Use dependency closure, configuration, source, environment, permission and evaluator identities to determine reuse. TTL can be one input but cannot replace those dependencies. Cache validity does not preserve an expired grant, a changed target ref or a revoked acceptance decision. Reuse of an old test result must disclose the checks intentionally reused and the mandatory fresh checks still required.

Compile deterministic indexes incrementally and compare incremental output with a clean rebuild. Retain material omissions or unknown dynamic dependencies; broaden validation instead of fabricating a sound impact set. Warm caches may reduce cost, but speculative keep-alives and prewarming need their own bounded benefit evidence. Cache encryption, tenant separation, deletion and retention apply equally to embeddings, prompts and model context.

## Interface and data boundary

Cache class; key profile; source and transitive dependency digests; permission/tenant scope; evaluator/runtime identity; freshness; reuse receipt; retained bytes; invalidation cause.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-CACHE-01 — Distinct caches

AIDE MUST classify prompt, KV, model, context, graph, build, tool, test and answer caches separately.

### UR-CACHE-02 — Complete validity key

Reuse MUST bind all known material dependencies, environment, policy and permission identities and disclose incomplete closure.

### UR-CACHE-03 — Current authority

Cache hits MUST NOT bypass current grants, target predicates, independent verification or mandatory fresh checks.

### UR-CACHE-04 — Tenant isolation

Cached context and inference state MUST respect account, tenant, model/backend, sensitivity and data-destination boundaries.

### UR-CACHE-05 — Incremental equivalence

Incremental deterministic indexes and generated outputs MUST be checked against clean rebuild equivalence for their admitted scope.

### UR-CACHE-06 — Reuse receipt

Validation reuse MUST produce a receipt naming retained evidence, validity inputs and fresh checks still required.

### UR-CACHE-07 — Bounded warming

Cache warming and warm-worker retention MUST have explicit resource budgets and a measured or uncertain expected-benefit justification.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-CACHE-01` | Reuse one generic cache entry for a test and a model answer. | The type/validity mismatch refuses. |
| `UC-CACHE-02` | Change a transitive compiler flag without changing the source file. | Affected build/test reuse is invalidated. |
| `UC-CACHE-03` | A cached plan was once approved but the grant expired. | It cannot execute under the stale approval. |
| `UC-CACHE-04` | A cache entry was created for a different private repository. | It is not exposed to an unauthorized consumer. |
| `UC-CACHE-05` | Apply a delete/rename change sequence. | Incremental output matches clean output or reports a bug/incomplete result. |
| `UC-CACHE-06` | Skip a suite based on affectedness. | The report shows the justification and does not call the skipped run newly passed. |
| `UC-CACHE-07` | A host proposes periodic keep-alive model calls. | They do not run by default without authority and a bounded budget. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
