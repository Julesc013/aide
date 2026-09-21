---
type: AIDE Engineering Specification
title: Native hosts, legacy relays and offline mailboxes
description: Bring the agent to the workflow without requiring a modern agent binary on every target machine.
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
- id: P20
  resource: urn:aide:source-package:90f79366cb02f34d737950db6708c087db367e36e7ce5ff98f7d953c6a82fb96
  title: AIDE-Specification-Overhaul-2026-09-20(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: host adapter owner
  applicability: host integration profiles
  requirement_ids:
  - UR-NATIVE-01
  - UR-NATIVE-02
  - UR-NATIVE-03
  - UR-NATIVE-04
  - UR-NATIVE-05
  - UR-NATIVE-06
  - UR-NATIVE-07
---

# Native hosts, legacy relays and offline mailboxes

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Bring the agent to the workflow without requiring a modern agent binary on every target machine.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Keep user-facing HostAdapter separate from ExecutionHost. A host captures workspace, active document/symbol, selection, diagnostics, build target and relevant application state, then renders typed plans, outcomes, refusals, evidence and permitted actions. A generic host can use forms/tables; domain experiences provide viewport or graph overlays. Hosts request apply through the owning capability, not arbitrary shell commands.

Preserve the original identify/invoke/report/optional-text-marker boot slice and its explicit host-lane acceptance. Oldest-first ordering remains a compatibility-program strategy, not a global prerequisite for every AIDE runtime feature. An old IDE may use a native extension, sidecar, named pipe, stdio or a file mailbox while a modern control node supplies indexing and inference. Protocol readability, controller execution, native build, target runtime and enforced isolation are separate support claims.

Offline bundles need exact work, source, policy, context and artifact identities; import revalidates permissions and current target state. They do not carry active grants forward blindly. Localhost is not automatically authenticated, and a legacy plaintext relay must terminate at an explicitly trusted gateway with documented constraints. Native ABIs require explicit ownership and versioned layouts; a C ABI is a possible binding, not a requirement to rewrite Core in C.

## Interface and data boundary

Host manifest; supported operations; workspace/context descriptor; protocol range; native adapter; transport; degraded behavior; target capability; evidence; offline bundle identity.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-NATIVE-01 — Host/runtime separation

User-facing hosts MUST NOT own independent WorkUnit state, model credentials or scheduling merely because they render AIDE.

### UR-NATIVE-02 — Preserve host proofs

Existing boot-slice behavior and host acceptance MUST remain preserved unless separately revised.

### UR-NATIVE-03 — Graded legacy support

Legacy integrations MUST declare artifact readability, command availability, build/runtime support and enforcement independently.

### UR-NATIVE-04 — Transport-neutral binding

Core semantics MUST be usable through qualified local IPC, sidecar or offline mailbox bindings without requiring a particular IDE.

### UR-NATIVE-05 — Offline revalidation

Imported continuation or result bundles MUST revalidate exact source, authority, identity and effect state before further action.

### UR-NATIVE-06 — Native apply request

Host UI MUST request typed domain-authoritative apply and MUST NOT redefine mutation meaning inside presentation code.

### UR-NATIVE-07 — Wire and ABI profile

Native and wire bindings MUST declare encoding, framing, ownership, version negotiation and failure semantics.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-NATIVE-01` | Workbench disconnects. | Durable work and approvals remain owned by the named service/records. |
| `UC-NATIVE-02` | The control-plane spec expands beyond IDEs. | The original host fixtures are still valid for their narrow scope. |
| `UC-NATIVE-03` | An old IDE reads a JSON handoff. | That does not imply it can run the current Python controller or provider binary. |
| `UC-NATIVE-04` | The target lacks modern TLS or native AI tooling. | An admitted relay/mailbox can preserve supported semantics with explicit limits. |
| `UC-NATIVE-05` | The target changes while a mailbox request is processed. | Import does not blindly apply the returned proposal. |
| `UC-NATIVE-06` | A scene preview panel offers apply. | The action routes through an admitted domain transaction capability. |
| `UC-NATIVE-07` | A legacy C caller encounters a larger future structure. | The supported binding handles declared version/size rules or refuses safely. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
