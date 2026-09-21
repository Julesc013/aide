---
type: AIDE Engineering Specification
title: Test jobs, reusable test assets and selective validation
description: Run long tests as durable jobs, not as expensive conversations waiting for output.
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
- id: P05
  resource: urn:aide:source-package:a247c622c6987787cae0fe18ff9383bb202f185b7e99bf1ce22478d42412e36a
  title: AIDE-Spec-Overhaul-2026-09-20-R2(1)(1).zip
- id: P06
  resource: urn:aide:source-package:83f9926500c47e3ee8384868c7d4046083e2a75bef0d667fb526c8476446d121
  title: AIDE-Spec-Overhaul-2026-09-20-R2(2)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
- id: P15
  resource: urn:aide:source-package:ddcd7109c50db5ad3bfe6693f5f09e52dd8c276280368af8105ab1b69458ea81
  title: AIDE-Spec-Overhaul-R2-2026-09-20(1).zip
- id: P18
  resource: urn:aide:source-package:d61e3fe58a17ae0b729d36519b23ba123de87571c55fcf0128f06e34e7c26723
  title: AIDE-Spec-Overhaul-v2-2026-09-20(1)(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: test owner and broker
  applicability: test profiles
  requirement_ids:
  - UR-TEST-01
  - UR-TEST-02
  - UR-TEST-03
  - UR-TEST-04
  - UR-TEST-05
  - UR-TEST-06
  - UR-TEST-07
---

# Test jobs, reusable test assets and selective validation

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Run long tests as durable jobs, not as expensive conversations waiting for output.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

A TestJob records exact command or native test binding, source/build configuration, environment, timeout, resource limits, output artifacts, result parser and failure semantics. Preserve stdout/stderr or equivalent raw native results under data policy, then expose bounded summaries with hashes and sizes. Import JUnit/TAP/SARIF/coverage through loss-aware adapters; these formats are not interchangeable evidence authorities.

Test assets should be modular by semantic responsibility: fixtures, execution harness, environment adapters, assertions/oracles and reporting can be reused at different levels. A real defect should leave a regression or a recorded reason not to create one. A one-off exploratory test may remain task-local, but its durable finding should not disappear. Reuse mechanics without making the independent checker call the production validator as its sole evidence.

Selective validation starts from source and generator dependencies, not filename guesses alone. Cache exact prior results only under a complete qualified validity key and retain mandatory fresh checks. Run focused checks first, widen when uncertainty requires, and periodically compare selection with broader validation to measure misses. Avoid the previous rule that every tiny change must rerun all predecessor validators forever. Cache validity itself must be tested and auditable.

## Interface and data boundary

Test definition/asset; source/build/env; execution binding; fixtures/oracle; resource budget; raw artifacts; parser/loss; result; validity key; fresh/reused flags; miss-rate evidence.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-TEST-01 — Durable non-agentic tests

Long validation MUST run as durable non-agentic jobs with typed status/resume conditions.

### UR-TEST-02 — Reusable assets

Material test findings MUST link to maintainable test/fixture assets or an explicit task-local disposition.

### UR-TEST-03 — Bounded log exposure

Model-visible test output MUST be bounded while retained artifacts carry size/hash and inspection references.

### UR-TEST-04 — Selective validation proof

Affected-test selection MUST use declared dependency coverage and retain conservative broadening plus miss-rate evaluation.

### UR-TEST-05 — Evidence reuse explicit

Reused test evidence MUST be distinguished from freshly executed tests and preserve required fresh checks.

### UR-TEST-06 — Native result preservation

Normalized test/diagnostic results MUST preserve original result references and report translation loss.

### UR-TEST-07 — Proportionate validation

Validation plans SHOULD minimize redundant work through qualified caching and staged checks without weakening mandatory safety gates.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-TEST-01` | A suite runs for an hour. | No model session is required merely to poll its progress. |
| `UC-TEST-02` | A one-off probe catches a real regression. | The reproduction is discoverable and its promotion or retention is recorded. |
| `UC-TEST-03` | A tool emits a gigabyte of output. | The model receives a bounded summary and truncation/custody status, not unbounded text. |
| `UC-TEST-04` | Dependency coverage is incomplete. | The selector widens tests or limits the acceptance claim. |
| `UC-TEST-05` | A cache serves yesterday’s result. | The report names the reused evidence and current validity inputs. |
| `UC-TEST-06` | A native runner has outcomes absent from JUnit. | They remain represented in AIDE metadata rather than silently becoming pass. |
| `UC-TEST-07` | Only a generated index changes. | Unrelated expensive suites can be reused when validity is proven, with a receipt. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
