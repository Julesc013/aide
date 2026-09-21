---
type: AIDE Engineering Specification
title: Performance, efficiency and resource planning
description: Optimize accepted outcomes and developer effort; prefer avoided work before lower-level rewrites.
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
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P15
  resource: urn:aide:source-package:ddcd7109c50db5ad3bfe6693f5f09e52dd8c276280368af8105ab1b69458ea81
  title: AIDE-Spec-Overhaul-R2-2026-09-20(1).zip
- id: P18
  resource: urn:aide:source-package:d61e3fe58a17ae0b729d36519b23ba123de87571c55fcf0128f06e34e7c26723
  title: AIDE-Spec-Overhaul-v2-2026-09-20(1)(1).zip
- id: P19
  resource: urn:aide:source-package:dab4e0eb3f7c39b80e03cf84748ec9f88a3603da6edbdebd534628cce325f832
  title: AIDE-Spec-Overhaul-v2-2026-09-20(2).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: scheduler and evaluation owner
  applicability: measured optimization profiles
  requirement_ids:
  - UR-PERF-01
  - UR-PERF-02
  - UR-PERF-03
  - UR-PERF-04
  - UR-PERF-05
  - UR-PERF-06
---

# Performance, efficiency and resource planning

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Optimize accepted outcomes and developer effort; prefer avoided work before lower-level rewrites.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Measure cold/warm startup, repository scan, incremental graph update, context compile, test queue, artifact throughput, accepted outcome latency, cost and operator intervention. Bind results to source, dataset, workload, hardware, operating system, filesystem, tools, cache state, model recipe and worker counts. Numeric targets are proposed SLOs until qualified on a named matrix.

Optimize algorithms, incremental recomputation, complete validity keys, batching, streaming, bounded data, locality and reusable evidence before JIT flags, language rewrites or a new database. Parallelism must account for nested compiler/test/model concurrency and shared memory/disk/network budgets. A resource scheduler can broker reservations without owning all internal worker orchestration.

USB, laptop, workstation, LAN and HPC deployments share semantic contracts but not performance or durability guarantees. A weak offline node can be a reader/relay, while build, inference and indexing are placed elsewhere under data policy. Thermal, energy and model residency observations are useful on relevant device profiles; they are not mandatory global metadata for every task. Enterprise scaling requires measured single-node limits, partitioned ownership, authenticated transport and fault qualification before claims of distributed capability.

## Interface and data boundary

Benchmark subject; dataset/workload; environment; cache state; latency/cost/resource metrics; concurrency; energy where relevant; regression budget; confidence; accepted outcome.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-PERF-01 — Reproducible performance claims

Efficiency and scalability claims MUST bind reproducible workload, source, environment, cache state and outcome quality.

### UR-PERF-02 — Optimize avoided work first

Optimization SHOULD prioritize algorithms, incremental state, bounded I/O, locality and cache validity before runtime/language replacement.

### UR-PERF-03 — No nested oversubscription

Resource planning MUST account for nested process, compiler, test and model concurrency under aggregate ceilings.

### UR-PERF-04 — Measured scale boundaries

Distributed services and heavier indexes MUST be introduced for demonstrated scale/security needs with compatibility and recovery evidence.

### UR-PERF-05 — Profile-specific SLOs

Latency, throughput, durability and energy targets MUST name the deployment profile and remain proposed until measured.

### UR-PERF-06 — Optimization outcome quality

Token/time/resource savings MUST be evaluated with acceptance, defect, repair and human-intervention outcomes.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-PERF-01` | A warm microbenchmark is compared with a cold full workflow. | The report does not label the difference a measured end-to-end improvement. |
| `UC-PERF-02` | A scan is repeatedly recomputing unchanged data. | The plan evaluates invalidation and reuse before a rewrite. |
| `UC-PERF-03` | Four workers each start an unbounded parallel build. | The scheduler constrains total resources or refuses the plan. |
| `UC-PERF-04` | A graph fits comfortably in local storage. | No distributed graph database becomes a compulsory baseline dependency. |
| `UC-PERF-05` | A laptop performance target is advertised for an old relay. | The unsupported transfer of SLO is rejected. |
| `UC-PERF-06` | A faster recipe creates more downstream bugs. | It is not promoted on speed alone. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
