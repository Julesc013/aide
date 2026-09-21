---
type: AIDE Engineering Specification
title: Model, effort and execution-recipe routing
description: The operator-selected lead and the set of permitted descendant recipes are independent controls.
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
- id: P09
  resource: urn:aide:source-package:fe066ea7e776bdd6f53ae3dc03b90f0da4c97b981acfd345cfb5fc4be343029b
  title: AIDE-Spec-Overhaul-2026-09-20-r2(5)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
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
  owner: routing policy owner
  applicability: model-enabled profiles
  requirement_ids:
  - UR-ROUTE-01
  - UR-ROUTE-02
  - UR-ROUTE-03
  - UR-ROUTE-04
  - UR-ROUTE-05
  - UR-ROUTE-06
  - UR-ROUTE-07
  - UR-ROUTE-08
---

# Model, effort and execution-recipe routing

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

The operator-selected lead and the set of permitted descendant recipes are independent controls.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Represent a complete execution recipe: harness, provider/account or local backend, exact model/artifact where observable, reasoning effort, context selection/rendering, tools, workflow, verification and recovery. Selection proceeds through authorization, availability, suitability and observability filters. None is reducible to a single ranking of model strength.

Preserve the lead model and reasoning setting unless the operator explicitly permits a change. Descendants may use lower, equal or higher capability configurations only within their own authorized sets; the lead is not an ordinal ceiling. Model strength never widens filesystem, tool, network, secret, integration or spending privileges. Models may expose incomparable effort controls, so negotiation must preserve provider-native meaning and report unsupported selections.

Compare finishing with the warm lead against a deterministic tool, a warm worker, a cold worker, a specialist and a different decomposition. Include setup, context transfer, parent assimilation, output, independent verification, repair, integration and reload. A cheaper token rate can be more expensive per accepted outcome. Reuse verified context while keeping hypotheses separate from facts. Optimizer policies are versioned, evaluated proposals; they may adapt only within granted transitions and cannot rewrite acceptance floors or authority.

## Interface and data boundary

Lead pin; descendant eligibility; effort mapping; provider/account/locality; privileges; budgets; recipe candidates; requested/resolved/observed settings; estimate uncertainty; selected reason.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-ROUTE-01 — Pinned lead

Routing MUST preserve the selected lead model and effort unless a separate explicit permission permits changing either.

### UR-ROUTE-02 — Independent descendant axes

Descendant model sets, efforts, provider/account, locality, depth, tools and privileges MUST be independently constrained.

### UR-ROUTE-03 — No capability rank authority

Model strength or predicted quality MUST NOT enlarge effect permissions or lower acceptance requirements.

### UR-ROUTE-04 — Complete recipe

Routing MUST evaluate and record a complete execution recipe rather than model name alone.

### UR-ROUTE-05 — Warm versus cold comparison

Delegation decisions MUST include warm-lead continuation and applicable deterministic/single-agent alternatives in total remaining-cost comparisons.

### UR-ROUTE-06 — Observed configuration

Requested, resolved and observed model/effort/account settings MUST be distinguishable; missing telemetry MUST remain unknown.

### UR-ROUTE-07 — No paid fallback

Local, subscription, purchased-credit and API routes MUST NOT be substituted without compatible account, data and spending authority.

### UR-ROUTE-08 — Evaluated adaptation

Recipe changes and learned routing improvements MUST be evaluated against relevant acceptance criteria and remain rollbackable.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-ROUTE-01` | A cheaper model becomes available mid-task. | The lead is not silently replaced. |
| `UC-ROUTE-02` | Permit a same-model child at a different effort. | The route can represent that choice without changing parent permissions. |
| `UC-ROUTE-03` | Route to a frontier model. | The same scope and verification floor still apply. |
| `UC-ROUTE-04` | A model runs with different tokenizer, tools or quantization. | It is a different recipe with separately scoped evidence. |
| `UC-ROUTE-05` | A cold child needs the full context and parent review. | Its preparation, transfer and assimilation costs are included before claiming savings. |
| `UC-ROUTE-06` | A hosted harness silently abstracts the actual model revision. | AIDE records unobserved revision rather than inventing an exact one. |
| `UC-ROUTE-07` | Subscription capacity expires. | AIDE waits or requests permission rather than silently charging an API account. |
| `UC-ROUTE-08` | An optimizer reduces tokens but increases repair failures. | The policy is not promoted solely on token reduction. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
