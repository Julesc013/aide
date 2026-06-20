# AIDE-Dominium Integration Charter

## 1. Purpose

The first cross-repository objective is:

```text
Workbench or deterministic fixture context
-> ContextDescriptor
-> AIDE ContextPack v2
-> AIDE WorkUnit
-> Dominium validation command invocation intent
-> typed Dominium result or refusal
-> EvidencePacket and EventRecord references
-> read-only Workbench projection
```

This charter is planning-only. It does not implement a model, provider, worker, mutation, live MCP, live A2A, broad Workbench UI, Host Contract, bridge, service, transport, local store, or command invocation.

Primary doctrine:

```text
Universal semantics at boundaries.
Domain meaning inside domains.
Host presentation inside hosts.
Specialized execution in hot paths.
```

## 2. Source-Of-Truth Hierarchy

AIDE and Dominium retain separate authority orders. AIDE execution truth is `.aide/queue/`; AIDE protocol and evidence truth comes from accepted queue packets, status files, reports, and task-local evidence. Dominium authority starts with `docs/canon/constitution_v1.md`, `docs/canon/glossary_v1.md`, `AGENTS.md`, scope contracts, and `.aide/queue/current.toml`.

Generated reports, OKF, RepoGraph, runtime-local state, chat, and uncommitted notes are consumers or evidence, not canonical owners. Cross-repo conflict resolution is conservative: preserve both native authorities, stop on semantic conflict, and create a bounded check or reconciliation task rather than silently flattening authority.

## 3. Namespace Ownership

`aide://` object references are owned by AIDE. Dominium command, service, document, refusal, diagnostic, package, graph, and capability IDs are owned by Dominium. Domino process and deterministic capability IDs are owned by Domino. Workbench host/workspace/action/view IDs are owned by Workbench under Dominium product law. Bridge mapping IDs are owned by the future AIDE-Dominium bridge contract and must be versioned.

Identity is not a file path. Every namespace has one owner. Remapping requires an explicit versioned bridge translation and evidence.

## 4. Cross-Repository Snapshot

The snapshot is provenance only, recorded in `cross-repo-input-snapshot.json`. It pins AIDE at `7e80ea2f18b404af68a752502a7491fceaa7abea` and Dominium at `c92b386027890c1bbf14aef6eaafe0357b7b03dd`. Dominium is clean but behind `origin/main` by 24; no fetch was performed because remote-ref mutation is out of scope.

## 5. Object Mapping Matrix

The object mapping is recorded in `object-mapping.json` and `object-mapping.md`. Every shared concept is owned directly, referenced by stable ID, projected read-only, translated through a versioned bridge, composed through an envelope, or explicitly not mapped. The charter forbids competing copies of WorkUnit, WorkerRun, TestJob, EvidencePacket, EventRecord, ReferenceID, Capability, ConformanceResult, PatchTransaction, Diagnostic, Refusal, Artifact, Workspace, Command, Result, and Validation.

## 6. Command Mapping

Future invocation maps:

```text
AIDE intent/work
-> registered Dominium command ID
-> capability/refusal check
-> service or deterministic process
-> typed result/refusal
-> diagnostic/evidence
-> view/action projection
```

Correlation fields are WorkUnit ref, ContextPack ref, future principal ref, future grant ref, future invocation ref, result/refusal ref, evidence refs, and event refs. No command invocation is implemented by this charter.

## 7. Refusal Mapping

Refusals stay typed outcomes. AIDE blocked/dependency/capability/conformance/context/transaction refusals map to AIDE-owned reason codes. Dominium command/document/validation/capability refusals map to Dominium-owned reason codes. Domino process refusals and Workbench unavailable/stale-context refusals keep their native owners.

## 8. Diagnostic Mapping

Dominium Diagnostic, AIDE finding, Reconciler finding, TestJob failure, EvidencePacket claim/result, and Workbench diagnostic projection are related by authority class, severity, source reference, and evidence. Not every warning is an execution blocker.

## 9. Evidence Mapping

Dominium owns native command/process evidence meaning. AIDE may reference and aggregate it. Workbench may present it. OKF may summarize accepted evidence. RepoGraph may relate evidence to entities. AIDE must not rewrite native evidence semantics.

## 10. Event Mapping

AIDE EventRecord, Dominium command event, Domino process/replay event, and Workbench interaction event are correlated by causation, sequence, and reference fields. This charter does not claim one universal event store.

## 11. Transaction Composition

`PatchTransaction` stays a current AIDE file-oriented no-apply proposal. `DevelopmentTransaction` is a future generic AIDE governance envelope. `DomainMutationBundle` is Dominium-owned. `PreviewSession` and `ShadowWorkspace` are future disposable validation boundaries. Owning Dominium/Domino process performs authoritative apply/undo. Workbench presents preview, approval, and host-authoritative apply request.

## 12. Host / Bridge / Provider / Experience Separation

Host Contract defines generic context, events, preview, approval, and apply-request language. Host Adapter maps a particular IDE/app into Host Contract. Domain Bridge maps AIDE objects into Dominium law. Capability Provider supplies deterministic Dominium/Domino operations. Experience Pack supplies panels, layouts, commands, and workflows. None of these is implemented here.

## 13. Workbench Non-Authority Law

Workbench binds registered views/actions, captures native context, presents previews, supports approval interaction, and inspects evidence. It does not call private tools directly, become product truth, bypass command/refusal/evidence contracts, own scheduler authority, hold provider credentials, mutate repositories silently, or own AIDE protocol authority.

## 14. Compatibility Policy

The bridge policy is read-old/write-current. Unknown optional fields are preserved or ignored according to owner contract. Unknown required fields refuse. Unknown capability refuses. No silent migration and no compatibility by filename coincidence. Supersession requires owner evidence and versioned mapping.

## 15. Security And Authority

Remote workers never directly mutate authoritative Workbench state. MCP endpoint authorization does not replace AIDE authorization. A2A discovery does not grant trust. AdapterManifest does not grant admission. ConformanceResult does not grant use by itself. Future CapabilityGrant is bounded. Future PolicyDecision applies to one intended use. Owning domain/host performs authoritative apply.

## 16. Failure And Recovery

Fail closed on authority. Fail forward on throughput where read-only work is safe. Preserve failed evidence. Use bounded repair, independent repair check, explicit resume task, and quarantine after retry budget exhaustion.

## 17. First Executable Seam

The next implementation program is `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`, `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01`, and `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`. It may include HostManifest, HostCapabilitySet, WorkspaceDescriptor, ContextDescriptor, ArtifactReference, EventEnvelope, Diagnostic projection, Refusal projection, Evidence refs, DominiumBridgeManifest, mapping fixtures, and conformance expectations. No command execution is included unless later explicitly authorized.

## 18. First Validation Slice

The first validation slice is `AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`, `AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`, and `AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`. Target flow: deterministic context fixture -> ContextDescriptor -> ContextPack v2 -> WorkUnit -> existing Dominium validation command intent -> typed result/refusal -> EvidencePacket/EventRecord refs -> read-only projection. No agent, model, provider, or mutation.

## 19. Critical-Path Task Graph

The task graph is recorded in `critical-path.json` and `task-dependency-graph.json`. The graph includes charter closure, read-only seam, validation slice, read-only Workbench, durable local substrate, trust/invocation, preview, first document preview/apply/rollback, and scene preview/apply/undo evidence nodes. Downstream queue directories were not materialized.

## 20. Parallel Read-Only RepoGraph Lane

Track B2 is planned but not implemented: existing Q37/Q38 facts -> provenance-qualified RepositoryFact model -> deterministic RepoGraph snapshot -> impact reports -> ContextPack integration -> OKF projection -> Reconciler integration -> later symbol/build/semantic producers. It must not block the read-only Dominium seam.

## 21. Task Turn Policy

One authoritative queue task per normal turn. Build implements locally and does local tests; Check independently reviews; Accept accepts only; Repair performs bounded repair only. A mega turn may contain one accepted gate plus one directly dependent planning-only task, maximum two commits. Future prompts must not soft-execute blocked downstream tasks merely to record that they are blocked.

## 22. Milestone Gates

Success is loop-based: read-only cross-repo validation works, local state survives restart, invocation authorization is enforced, preview leaves authority unchanged, apply is domain/host authoritative, rollback restores preimage, scene edit works end-to-end, and legacy host uses the same protocol.
