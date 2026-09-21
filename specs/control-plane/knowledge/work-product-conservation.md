---
type: AIDE Engineering Specification
title: Work-product conservation and harvest
description: Conserve development value, not every temporary byte forever.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P04
  resource: urn:aide:source-package:b3f3d0d27109a986e537928523c9c34f31e3458986c7632e97abee06d85db64c
  title: AIDE-Spec-Overhaul-2026-09-20(3)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P15
  resource: urn:aide:source-package:ddcd7109c50db5ad3bfe6693f5f09e52dd8c276280368af8105ab1b69458ea81
  title: AIDE-Spec-Overhaul-R2-2026-09-20(1).zip
- id: P16
  resource: urn:aide:source-package:635f61aafab254ead0014e09e34a41acf9150282af60afbee0460157301a03a9
  title: AIDE-Spec-Overhaul-Refresh-2026-09-20(1).zip
- id: P20
  resource: urn:aide:source-package:90f79366cb02f34d737950db6708c087db367e36e7ce5ff98f7d953c6a82fb96
  title: AIDE-Specification-Overhaul-2026-09-20(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: work product owner
  applicability: all work profiles
  requirement_ids:
  - UR-HARV-01
  - UR-HARV-02
  - UR-HARV-03
  - UR-HARV-04
  - UR-HARV-05
  - UR-HARV-06
  - UR-HARV-07
---

# Work-product conservation and harvest

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Conserve development value, not every temporary byte forever.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Every material task output should be discoverable and have a proportionate fate: accepted source, reusable test or tool, retained evidence, generated projection, candidate improvement, cache, archive, quarantine or justified deletion. Preserve useful learning from failures, not only successful artifacts. Source history and content-addressed storage can preserve value without copying every old file into the active tree.

Scratch work is allowed. A short one-off probe may be the fastest reliable way to test a hypothesis; it should not be forced into an SDK prematurely. When it reveals a real defect or reusable mechanism, harvest the fixture, assertion, method and result into an appropriate maintained asset. Do not let independent review harnesses collapse into production validators: share process/fixture mechanics where safe, but keep the acceptance oracle independent.

Retention is constrained by privacy, licence, security, storage and user intent. A secret-bearing prompt may need redaction or deletion rather than archival. Record provenance and a safe disposition without retaining forbidden content. Task closeout should produce a compact harvest record by default, expanding only for high-risk, failed, rescued, novel or repeated work. Promotion itself is a scoped change with tests, ownership and review, not a cleanup side effect.

## Interface and data boundary

Work product ID; producer/attempt; purpose; artifact; owner; reuse class; sensitivity/licence; retention; disposition; promotion candidate; regression link; evidence.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-HARV-01 — Material output disposition

Terminal work MUST enumerate material outputs and assign a purpose, owner, retention and disposition appropriate to risk.

### UR-HARV-02 — Failures become assets

Material defects MUST be considered for regression tests, negative fixtures, validator rules or scoped lessons.

### UR-HARV-03 — Scratch is permitted

One-off work MAY remain task-local when reuse is unjustified; conservation MUST NOT force premature framework extraction.

### UR-HARV-04 — Independent oracle preserved

Promoting test assets MUST preserve the independence of acceptance oracles from candidate production validation logic.

### UR-HARV-05 — Retention overrides hoarding

Conservation MUST obey privacy, licence, secrets, retention and deletion obligations, including redaction or justified disposal.

### UR-HARV-06 — Bounded harvest overhead

Harvest MUST be proportional and support compact automated classification with reviewed escalation for consequential promotion.

### UR-HARV-07 — Promotion is controlled change

Moving task-local assets into canonical tools, tests, docs or packages MUST use normal ownership, validation and review gates.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-HARV-01` | A task leaves a useful check script in evidence. | Harvest records its reusable candidate status instead of losing it in a task directory. |
| `UC-HARV-02` | An independent check catches a path escape. | The failure reproduction and its maintained regression disposition remain linked. |
| `UC-HARV-03` | A small experiment has no reusable consumer. | Its result and rationale are retained appropriately without inventing a package. |
| `UC-HARV-04` | A reusable harness imports the function it is meant to independently validate as its only oracle. | Conformance does not accept that circular evidence. |
| `UC-HARV-05` | An artifact contains credentials. | The system does not retain the secret merely to satisfy a no-work-lost slogan. |
| `UC-HARV-06` | A tiny documentation fix produces no new reusable behavior. | It can close with a compact disposition rather than many permanent forms. |
| `UC-HARV-07` | Harvest detects a reusable script. | It emits a candidate plan, not an unapproved move into core. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
