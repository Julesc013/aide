---
type: AIDE Engineering Specification
title: Recovery, cancellation and uncertain effects
description: Absence of a receipt is not evidence that an operation did not happen.
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
- id: P09
  resource: urn:aide:source-package:fe066ea7e776bdd6f53ae3dc03b90f0da4c97b981acfd345cfb5fc4be343029b
  title: AIDE-Spec-Overhaul-2026-09-20-r2(5)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
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
  owner: effect owner
  applicability: effect-capable profiles
  requirement_ids:
  - UR-REC-01
  - UR-REC-02
  - UR-REC-03
  - UR-REC-04
  - UR-REC-05
  - UR-REC-06
  - UR-REC-07
---

# Recovery, cancellation and uncertain effects

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Absence of a receipt is not evidence that an operation did not happen.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Represent known-no-effect, observed-effect, partial-effect and unknown-effect independently of process and transport state. After durable intent and a lost response, first observe the authoritative effect owner. Retry only with proven idempotency, confirmed no-effect or a fresh explicit recovery decision. Local rollback, remote compensation and forward repair are different mechanisms with different limits.

Preserve the best verified candidate, neutral failure evidence, remaining acceptance obligations and actual resource consumption. A failed parser should not destroy the raw data needed for diagnosis; a failed aggregate evaluator may invalidate its evaluation while leaving sound observations reusable. Repeated identical failures should lead to a different hypothesis, tool, context, decomposition or escalation—not unbounded identical retries. A model's predicted low success rate alone does not prohibit a bounded authorized investigation.

Offline waiting can remain durable indefinitely subject to retention, while active retry bursts and provider spend remain bounded. Reconnection revalidates identity, policy, source and budgets. An old grant or conversation is not a replay script. Clock semantics must distinguish wall timestamps, monotonic elapsed time, external deadlines and restart interpretation. Cancellation, revocation and late success need explicit precedence: late data may aid reconciliation, but may not erase an already final cancellation.

## Interface and data boundary

Effect identity; intent; latest authoritative observation; certainty; retry budget; ownership; cancellation phases; retained candidate; compensation/forward repair; unknown liabilities.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-REC-01 — Observe before replay

Unknown effects MUST be reconciled through authoritative observation before replay, rollback or conflicting new work.

### UR-REC-02 — Typed cancellation evidence

Cancellation MUST separate request, acknowledgement, local termination, remote outcome and retained artifacts.

### UR-REC-03 — Bounded differentiated retry

Retries MUST preserve history and consume a finite budget; repeated equivalent failures MUST require changed evidence or strategy.

### UR-REC-04 — Preserve valid partial work

Recovery MUST retain independently valid observations, best verified candidates and obligations subject to privacy/retention policy.

### UR-REC-05 — Clock contract

Deadlines and leases MUST use declared wall/monotonic/skew semantics and be tested across restart and clock discontinuity.

### UR-REC-06 — No false rollback

Operations without complete rollback MUST declare irreversible consequences and compensation/forward-repair options.

### UR-REC-07 — Bounded exploration

An authorized contained investigation MAY use better tools, context or decomposition when no stronger permitted model exists; acceptance evidence MUST remain unchanged.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-REC-01` | Lose a reply after a remote mutation intent. | The coordinator queries effect state rather than submitting the mutation again. |
| `UC-REC-02` | Local process termination succeeds but remote submission may have arrived. | Remote effect remains unknown until observed. |
| `UC-REC-03` | The same failure signature recurs repeatedly. | AIDE pauses/escalates or uses an admitted different remedy, not an unlimited loop. |
| `UC-REC-04` | A later candidate fails verification. | Earlier qualified candidate and failure learning are not overwritten. |
| `UC-REC-05` | The wall clock jumps backwards. | A time-limited grant does not silently gain extra authorized lifetime. |
| `UC-REC-06` | An external notification has already been delivered. | Recovery does not claim it can be undone merely by restoring local files. |
| `UC-REC-07` | The selected lead predicts low success. | A bounded attempt may proceed, but unverified output cannot be accepted. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
