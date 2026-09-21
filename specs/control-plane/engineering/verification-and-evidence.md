---
type: AIDE Engineering Specification
title: Verification, proof claims and evidence
description: Evidence supports a proposition within a scope; it does not make every surrounding claim true.
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
  owner: independent evaluator and domain owner
  applicability: all acceptance profiles
  requirement_ids:
  - UR-VERIFY-01
  - UR-VERIFY-02
  - UR-VERIFY-03
  - UR-VERIFY-04
  - UR-VERIFY-05
  - UR-VERIFY-06
  - UR-VERIFY-07
  - UR-VERIFY-08
---

# Verification, proof claims and evidence

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Evidence supports a proposition within a scope; it does not make every surrounding claim true.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Define the proposition, subject revision, semantic dependencies, evaluator, environment, coverage and limitations before claiming success. Separate execution of a computation, adequacy of its method and the engineering claim it supports. A model verdict, a valid JSON result, repeated agreement and a large test count are not substitutes for the required oracle.

Verification independence is multidimensional. Different sessions on the same model can reduce some correlations but do not automatically prove independent assumptions. Record shared model, provider, prompt/context, code, fixture, data and environment dependencies. Do not require every verifier to be entirely unrelated; require the independence appropriate to the risk and disclose the remaining shared failure modes.

Evidence reuse is a dependency and non-interference claim. Revoking an evaluator may invalidate its evaluations while sound raw observations remain valuable. A failed aggregate can be rebuilt from sound members rather than rerunning everything blindly. Contradictory pass/fail under the same exact fingerprint is a nondeterminism incident. Human/manual evidence, corpus sufficiency and environment absence remain first-class. Package validation proves package properties, not the behavior of an unexecuted runtime.

## Interface and data boundary

Proposition; subject/base/candidate; read dependencies; evaluator identity; environment; raw observations; evaluation; review; limitations; freshness/revocation; result; proof closure.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-VERIFY-01 — Exact evidence subject

Acceptance evidence MUST bind exact inputs, subject/candidate, evaluator, environment and limitations.

### UR-VERIFY-02 — Claims versus evidence

Worker confidence, prose, schema validity and repeated agreement MUST NOT substitute for required functional or safety evidence.

### UR-VERIFY-03 — Independent oracle

High-risk verification MUST use an independently trusted oracle and disclose shared dependencies.

### UR-VERIFY-04 — Result taxonomy

Passed, failed, blocked, skipped, not-run, inconclusive and limited-scope outcomes MUST remain explicit.

### UR-VERIFY-05 — Scoped invalidation

Evidence revocation MUST propagate through affected evaluations and claims while preserving independently sound observations.

### UR-VERIFY-06 — Nondeterminism incident

Conflicting results under an identical qualified fingerprint MUST be recorded as nondeterminism or environment incompleteness.

### UR-VERIFY-07 — Package versus runtime proof

Artifact checks and proposed acceptance scenarios MUST NOT be presented as executed AIDE behavioral qualification.

### UR-VERIFY-08 — Manual and corpus gates

Required human judgment and corpus sufficiency MUST be recorded separately from automated test count.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-VERIFY-01` | The candidate changes after tests. | The prior result cannot prove the changed subject without valid reuse evidence. |
| `UC-VERIFY-02` | Two agents agree a patch is correct but tests are missing. | The task remains unverified under a test-required policy. |
| `UC-VERIFY-03` | A candidate changes both implementation and its only golden expectation. | It cannot self-certify the changed expectation. |
| `UC-VERIFY-04` | A suite unexpectedly selects zero tests. | It is not reported as full passing coverage. |
| `UC-VERIFY-05` | An evaluator bug is found. | Dependent acceptances are invalidated without automatically destroying raw captures. |
| `UC-VERIFY-06` | A deterministic test alternates pass/fail with the same key. | AIDE does not select only the passing run. |
| `UC-VERIFY-07` | This specification bundle validates successfully. | Its behavioral scenarios remain not_run. |
| `UC-VERIFY-08` | A small fixture set passes. | It does not certify broad product or artistic compatibility. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
