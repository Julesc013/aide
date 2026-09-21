---
type: AIDE Engineering Specification
title: Execution hosts, harnesses and session bindings
description: ExecutionHost is a bounded session host. It is not a new owner of WorkUnits or project policy.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P05
  resource: urn:aide:source-package:a247c622c6987787cae0fe18ff9383bb202f185b7e99bf1ce22478d42412e36a
  title: AIDE-Spec-Overhaul-2026-09-20-R2(1)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
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
  owner: execution-host owner
  applicability: worker profiles
  requirement_ids:
  - UR-HOST-01
  - UR-HOST-02
  - UR-HOST-03
  - UR-HOST-04
  - UR-HOST-05
  - UR-HOST-06
  - UR-HOST-07
---

# Execution hosts, harnesses and session bindings

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

ExecutionHost is a bounded session host. It is not a new owner of WorkUnits or project policy.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

ModelProvider performs inference; WorkerHarness implements the agent loop; InferenceBackend serves a model artifact; ExecutionHost supervises a bounded session; SandboxBackend establishes isolation properties. DomainBridge and user-facing HostAdapter serve different purposes again. Use role-specific contracts under a common extension envelope instead of calling every component a provider.

A run binding records the WorkUnit and attempt, external session ID, exact harness/backend recipe, workspace base, context digest, policy digest, grants, adapter version and resource budgets. Foreign session IDs are locators or correlations, not replacements for AIDE work identity. A host's internal subagents are child execution observations unless explicitly admitted as WorkUnits.

Qualify one deterministic local reference and one genuinely different binding before asserting general host interchangeability. Omnigent is a candidate adapter, not pre-certified infrastructure or a mandatory backend. Raw host events must be retained subject to privacy policy and translated with loss receipts. Runtime tool approval cannot stand in for permission to mutate the authoritative project. Generic conformance includes interruption, malformed events, duplicate terminal messages, scope escapes, missing artifacts, usage gaps and reconnect behavior.

## Interface and data boundary

ExecutionHost descriptor; run binding; harness/backend/model identity; session ID; workspace/context/policy digests; grants; event cursor; artifacts; usage; limitations; cancellation.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-HOST-01 — Role separation

ExecutionHost, WorkerHarness, ModelProvider, InferenceBackend, DomainBridge and HostAdapter MUST remain distinct semantic roles.

### UR-HOST-02 — Immutable session binding

Every hosted attempt MUST bind exact work, context, workspace revision, grants and implementation identities.

### UR-HOST-03 — Host does not own work

External session databases MUST NOT become the only owner of canonical AIDE work or evidence.

### UR-HOST-04 — No double orchestration

Nested agents MUST operate only under explicitly qualified tree-wide limits and MUST NOT silently create independent canonical work authority.

### UR-HOST-05 — Separate approval domains

Runtime tool permission MUST remain distinct from authoritative transaction approval.

### UR-HOST-06 — Candidate integrations

Named external products MUST remain version-pinned candidates until exact integration and security conformance pass.

### UR-HOST-07 — Preserve foreign evidence

Event translation MUST retain available raw event identity and disclose unmapped semantics.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-HOST-01` | Replace a model server while retaining the coding harness. | Only the affected recipe and qualification change, not WorkUnit identity. |
| `UC-HOST-02` | Reattach a session to a different task or source revision. | The mismatch refuses or creates a separately admitted new attempt. |
| `UC-HOST-03` | Remove an optional host installation. | Portable work records and retained artifacts remain interpretable. |
| `UC-HOST-04` | A harness spawns undeclared children. | The binding refuses or records a qualification violation rather than assuming budgets cover them. |
| `UC-HOST-05` | A sandbox grants a shell command. | That grant does not authorize merging or applying its output to the target. |
| `UC-HOST-06` | A package manifest names Omnigent. | The package is not labeled certified merely by installation or documentation. |
| `UC-HOST-07` | An external host emits an unfamiliar terminal event. | The result stays unknown/degraded and the raw reference remains available. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
