---
type: AIDE Engineering Specification
title: Usage, aggregate budgets and accepted-outcome cost
description: Unknown cost is not zero, and a wall-time cap is not automatically a currency cap.
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
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: accounting and budget owner
  applicability: all resource-consuming profiles
  requirement_ids:
  - UR-COST-01
  - UR-COST-02
  - UR-COST-03
  - UR-COST-04
  - UR-COST-05
  - UR-COST-06
  - UR-COST-07
  - UR-COST-08
---

# Usage, aggregate budgets and accepted-outcome cost

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Unknown cost is not zero, and a wall-time cap is not automatically a currency cap.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Collect usage even when final-result parsing fails or a run is cancelled. Preserve native provider counters and normalize them through versioned adapter semantics. Counters may be deltas, cumulative snapshots or parent aggregates including children; reconcile rather than summing all observations. Separate cached and uncached billable units and never double-count reasoning/output fields whose tariff semantics overlap.

Report at least estimated consumption, observed provider/resource usage, allowance use and reconciled charges as distinct categories. Use decimal arithmetic and currency/unit-qualified rates with effective dates. Local compute, subscription allowance, purchased credits and API billing are not interchangeable money. Unknown prices and unknown remote continuation produce unresolved liabilities, not fabricated savings.

Reserve aggregate resources transactionally across a task tree, including retries, assurance, integration and recovery. State whether a ceiling is enforced by the provider, enforced locally, reserved conservatively, monitored or advisory. Prevent new dispatch when the bound cannot be respected, but do not promise to retract requests already accepted remotely. Preserve a reserve for mandatory verification. Evaluate future remaining costs separately from sunk cost; report the complete historical cost of accepted and rejected outcomes without survivorship bias.

## Interface and data boundary

Observation identity; native counter semantics; delta/cumulative/aggregate scope; disjoint units; rate provenance/date; estimates; actuals; liabilities; reservations; enforcement class; outcome link.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-COST-01 — Usage survives failure

Usage capture MUST remain independent of final answer parsing, success or task acceptance.

### UR-COST-02 — No double counting

Counter normalization MUST identify deltas, cumulative observations and aggregate-includes-children semantics.

### UR-COST-03 — Unknown is explicit

Missing usage, prices, cache treatment or remote termination MUST be represented as unknown rather than zero.

### UR-COST-04 — Atomic tree reservations

Aggregate budgets MUST atomically reserve children, retries, verification, integration and uncertain liabilities across concurrent work.

### UR-COST-05 — Enforcement class

Every budget claim MUST identify its unit and actual enforcement class, including overshoot or observability limitations.

### UR-COST-06 — Total accepted-outcome cost

Optimization MUST report complete outcome cost including preparation, assimilation, verification, repair and failed attempts.

### UR-COST-07 — Price provenance

Billable amounts MUST use disjoint units, decimal arithmetic and effective sourced tariff semantics; estimates MUST stay labeled.

### UR-COST-08 — Reserve verification

Dispatch MUST preserve the declared resource allowance for mandatory assurance and safe recovery.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-COST-01` | A paid run emits malformed final JSON. | Available usage and unresolved liability are still recorded. |
| `UC-COST-02` | Receive both child usage and a parent total including it. | Accounting reconciles without summing the same consumption twice. |
| `UC-COST-03` | A provider omits cost telemetry. | The report cannot claim a measured zero-cost run. |
| `UC-COST-04` | Two children race for the last budget allocation. | At most the allowed total is reserved and rejected dispatch produces no new spend. |
| `UC-COST-05` | Only a wall-time threshold is enforced. | The interface does not advertise a hard dollar cap. |
| `UC-COST-06` | A low-price model needs repeated repair. | Its accepted-outcome comparison includes that additional work. |
| `UC-COST-07` | A tariff changes or currency is unspecified. | The cost is recomputed with the correct effective schedule or classified unknown. |
| `UC-COST-08` | A coding proposal would exhaust the entire budget. | The run is narrowed, deferred or refused rather than silently skipping verification. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
