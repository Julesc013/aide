---
type: AIDE Engineering Specification
title: After-action reviews and improvement effectiveness
description: Learning should make later work better without silently rewriting the rules that judged the earlier work.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P07
  resource: urn:aide:source-package:cb71d8c332dc49210ad1384a132121bd72878b574d96470c293a652d37093afb
  title: AIDE-Spec-Overhaul-2026-09-20-r2(3)(1).zip
- id: P08
  resource: urn:aide:source-package:17ff6721596aa57145ac767276aab0332f179d474065d81b314d103e71c6d979
  title: AIDE-Spec-Overhaul-2026-09-20-R2(4)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
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
  owner: lesson reviewer and policy owner
  applicability: learning-enabled profiles
  requirement_ids:
  - UR-LEARN-01
  - UR-LEARN-02
  - UR-LEARN-03
  - UR-LEARN-04
  - UR-LEARN-05
  - UR-LEARN-06
---

# After-action reviews and improvement effectiveness

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Learning should make later work better without silently rewriting the rules that judged the earlier work.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

AfterActionReview belongs to a WorkUnit or declared programme scope within harvest, not a parallel diary whose prose becomes policy. Freeze intended outcomes from the admitted task, record actual observations, classify the difference and retain causal uncertainty. Capture successful strategies as well as failures; do not invent a lesson when evidence is inconclusive.

A useful lesson has a trigger, action, scope, exceptions, evidence, confidence, expiry and owner. Separate observation, lesson candidate, reviewed knowledge decision, improvement proposal, admitted implementation and effectiveness result. Cross-project generalization requires contrasting consumers and should preserve local product intent. A doctrine copied through many assistant summaries is not measured effectiveness.

Retrieve only relevant current lessons and expose why they entered a ContextPack. Allow the operator to correct, override or retire them. Measure recurrence, false applicability, intervention, accepted-outcome cost and quality after adoption. Preserve negative and null outcomes; automatically adding more instructions forever is not intelligence. A simpler workflow can replace a complex one when equal or better evidence supports it.

## Interface and data boundary

Intended/actual; causal hypotheses; confidence; source evidence; trigger/action/exceptions; scope; lesson state; reviewer; improvement task; effectiveness metrics; retirement.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-LEARN-01 — Evidence-grounded review

After-action records MUST distinguish observations, causal hypotheses, uncertainty and proposed changes.

### UR-LEARN-02 — Scoped lesson lifecycle

Lessons MUST have applicable scope, trigger/action/exception semantics, provenance and review/supersession state.

### UR-LEARN-03 — No direct policy mutation

Lessons and AARs MUST NOT directly modify prompts, grants, acceptance criteria, policy or source.

### UR-LEARN-04 — Learn from success

Harvest SHOULD record materially effective patterns as well as failures without forcing lessons from every task.

### UR-LEARN-05 — Effectiveness measurement

Adopted lessons and optimizers MUST be evaluated against later eligible outcomes and be narrowed, retired or reverted if ineffective.

### UR-LEARN-06 — Transparent retrieval

Lesson selection MUST record relevance, omission and override reasons and respect current data permissions.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-LEARN-01` | An agent attributes failure to a model without comparative evidence. | The cause remains a hypothesis, not accepted fact. |
| `UC-LEARN-02` | A project-specific workaround is retrieved for another domain. | It is excluded or explicitly treated as an unqualified analogy. |
| `UC-LEARN-03` | A review recommends looser verification. | It becomes a separately reviewed proposal, not an automatic configuration edit. |
| `UC-LEARN-04` | A low-cost strategy produces a verified improvement. | The successful evidence can be reused as a scoped candidate lesson. |
| `UC-LEARN-05` | A new instruction adds context cost but no benefit. | Its null/negative outcome is retained and retirement is supported. |
| `UC-LEARN-06` | A stale lesson conflicts with a current contract. | It does not silently override the current contract. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
