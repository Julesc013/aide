---
type: AIDE Engineering Specification
title: Trust, policy, grants and revocation
description: Conformance demonstrates behavior; admission selects an exact implementation; a grant authorizes one actor in one scope.
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
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P15
  resource: urn:aide:source-package:ddcd7109c50db5ad3bfe6693f5f09e52dd8c276280368af8105ab1b69458ea81
  title: AIDE-Spec-Overhaul-R2-2026-09-20(1).zip
- id: P20
  resource: urn:aide:source-package:90f79366cb02f34d737950db6708c087db367e36e7ce5ff98f7d953c6a82fb96
  title: AIDE-Specification-Overhaul-2026-09-20(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: policy authority and enforcement host
  applicability: effect-capable profiles
  requirement_ids:
  - UR-TRUST-01
  - UR-TRUST-02
  - UR-TRUST-03
  - UR-TRUST-04
  - UR-TRUST-05
  - UR-TRUST-06
  - UR-TRUST-07
---

# Trust, policy, grants and revocation

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Conformance demonstrates behavior; admission selects an exact implementation; a grant authorizes one actor in one scope.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Trust is not self-attested metadata. Bind an admission to exact package/adapter bytes and a conformance profile, then evaluate the intended operation against current target policy, principal identity, data class, effect scope and budgets. Hash equality alone does not prove a legitimate operator or a protected host. Authentication evidence, capability declaration and authorization are separate records.

Compose policy by intersections of applicable ceilings, not a universal last-file-wins merge. User preferences can select among permitted choices; they cannot relax organization or target restrictions. Where policies conflict, return the effective decision and provenance rather than silently choosing a convenient interpretation. A local privacy profile is not automatically a fully offline-verified or physically air-gapped deployment.

Consumption, expiry and revocation must survive restart. Decide explicitly what revocation means for an already running process and for an external effect whose outcome is unknown. Observation needed to reconcile such an effect may remain allowed when new mutations are forbidden. Capability, tool-call, session, integration, signing, publication and purchase permissions need separate predicates. Future break-glass behavior is not a default escape hatch; it needs an owned, narrow, time-bound and audited profile.

## Interface and data boundary

Principal; identity evidence; admission digest; decision inputs; allow/deny/constraints; grant scope; expiry; count/resource limits; delegation; revocation; enforcement receipt.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-TRUST-01 — Admission versus authorization

AIDE MUST distinguish implementation admission from a current capability grant and operation-specific policy decision.

### UR-TRUST-02 — Ceiling composition

Lower-scope settings and descendants MUST only narrow applicable policy ceilings, never widen them implicitly.

### UR-TRUST-03 — Current effect enforcement

Grants, source identity, expiry and target policy MUST be revalidated at each consequential effect boundary.

### UR-TRUST-04 — Durable grant accounting

One-use/count/resource grants MUST be consumed transactionally and remain consumed after timeout, duplicate request or restart.

### UR-TRUST-05 — Bounded delegation

Delegation MUST bind principal, scope, duration, depth and resource limits and prohibit authority amplification.

### UR-TRUST-06 — Explainable policy

Policy results MUST disclose effective constraints, source provenance and reasons without leaking secrets.

### UR-TRUST-07 — No endogenous trust upgrade

Model output, retrieved documents and candidate package metadata MUST NOT grant themselves trust or rewrite their own acceptance criteria.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-TRUST-01` | Invoke an admitted adapter without a matching grant. | The effect is refused before dispatch. |
| `UC-TRUST-02` | A task preference permits a network destination forbidden by project policy. | Effective policy denies the destination and reports both sources. |
| `UC-TRUST-03` | Revoke a grant after planning but before apply. | Apply does not proceed under the stale decision. |
| `UC-TRUST-04` | Replay the same invocation after a lost response. | No second allowance is created; the same effect is reconciled. |
| `UC-TRUST-05` | A child delegates beyond the remaining parent budget. | Delegation refuses without changing the parent limit. |
| `UC-TRUST-06` | A requested model route is clamped by data policy. | The operator sees the permitted alternatives and the responsible rule. |
| `UC-TRUST-07` | A tool result contains instructions to ignore policy. | It is treated as untrusted data and causes no authority change. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
