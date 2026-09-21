---
type: AIDE Engineering Specification
title: ProjectGraph, provenance and impact
description: ProjectGraph is a derived federation of facts, not a new universal source of project truth.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
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
- id: P20
  resource: urn:aide:source-package:90f79366cb02f34d737950db6708c087db367e36e7ce5ff98f7d953c6a82fb96
  title: AIDE-Specification-Overhaul-2026-09-20(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: graph producer and consumer owners
  applicability: project-intelligence profiles
  requirement_ids:
  - UR-GRAPH-01
  - UR-GRAPH-02
  - UR-GRAPH-03
  - UR-GRAPH-04
  - UR-GRAPH-05
  - UR-GRAPH-06
  - UR-GRAPH-07
---

# ProjectGraph, provenance and impact

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

ProjectGraph is a derived federation of facts, not a new universal source of project truth.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Use RepoGraph as the file/repository slice of a broader ProjectGraph. Add code, documentation, tests, requirements, issues, work products, build actions, assets and runtime observations through typed producers. Start with AIDE’s existing inventory and quality facts; do not require a universal compiler, vector database or graph service before the first useful graph query.

Every node and edge records producer, source identity/revision, extraction scope, authority class, confidence, completeness and freshness. Exact compiler references, syntactic guesses, runtime observations, history-derived co-change and model inferences are not equal facts. Logical modules need not coincide with directories. Dependency graphs can be acyclic where required, while ordinary documentation and concept links can contain cycles.

Impact analysis computes a conservative affected set over declared read/write dependencies. Dynamic imports, reflection, generated code, runtime assets and incomplete test mappings require explicit unknown coverage and broader validation. Measure selection precision, recall and miss rates against known corpora; do not call a heuristic test map coverage proof. Keep graph indexes rebuildable, permission-aware and incrementally equivalent to clean snapshots. Stable IDs aid joins, but no graph alias automatically repairs external consumers.

## Interface and data boundary

Entity/relation; producer/version; source revision/span; authority/confidence/completeness; dependency type; freshness; snapshot; impact uncertainty; permission filter; evidence.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-GRAPH-01 — Qualified facts

Graph nodes and edges MUST carry provenance, revision, extraction coverage and epistemic class.

### UR-GRAPH-02 — Reuse existing producers

Initial ProjectGraph work MUST normalize existing authoritative/inventory sources before replacing them with new indexers.

### UR-GRAPH-03 — Derived not authoritative

Graph and retrieval indexes MUST remain rebuildable projections and MUST NOT independently grant deletion, mutation or acceptance.

### UR-GRAPH-04 — Conservative affectedness

Unknown or contradictory dependency coverage MUST broaden required validation or explicitly restrict acceptance scope.

### UR-GRAPH-05 — Measured graph quality

Impact, orphan, reuse and test-selection claims MUST be evaluated against labeled cases with unknown/miss rates.

### UR-GRAPH-06 — Relation-specific constraints

Graph validation MUST enforce constraints by relation type rather than require every link graph to be a DAG.

### UR-GRAPH-07 — Permission-aware graph

Graph expansion, search and export MUST enforce current subject and data permissions.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-GRAPH-01` | A regex-derived call is displayed beside a compiler reference. | The graph preserves their different confidence and completeness. |
| `UC-GRAPH-02` | A file-quality ledger already records ownership. | The graph imports it as attributed data rather than inventing a competing owner. |
| `UC-GRAPH-03` | A node has no observed incoming references. | It is an orphan candidate, not deletion permission. |
| `UC-GRAPH-04` | A changed plugin is loaded dynamically. | An incomplete static graph cannot justify skipping all downstream tests. |
| `UC-GRAPH-05` | A selector saves runtime but misses a regression. | The failure is retained and the selector’s qualified scope is narrowed. |
| `UC-GRAPH-06` | Two explanatory pages cross-link. | The cycle is allowed unless that relation specifically requires acyclicity. |
| `UC-GRAPH-07` | A global graph joins public and private project nodes. | Unauthorized consumers receive neither private content nor disallowed derived disclosure. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
