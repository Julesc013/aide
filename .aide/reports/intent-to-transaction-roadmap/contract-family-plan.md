# Contract Family Plan

The future architecture should distinguish four contract families.

## Host Contract

Defines how user-facing shells communicate with AIDE. Candidate objects include
HostIdentity, HostManifest, HostCapabilitySet, WorkspaceDescriptor,
DocumentDescriptor, SelectionDescriptor, ContextDescriptor, Diagnostic,
Refusal, ApprovalRequest, ArtifactReference, and EventEnvelope.

Candidate operations include host description, workspace description, context
capture and preview, WorkUnit inspection, patch preview and request-apply,
validation submission and status, approval response, evidence inspection, and
event subscription or resume.

## Capability Contract

Defines discoverable operations independently of any UI. The missing primitive
is `CapabilityInvocation`, which can represent deterministic validation,
context compilation, graph inspection, scene preview, asset conversion,
simulation, or performance profiling.

## Transaction Contract

Keep PatchTransaction v1 as the accepted file-oriented no-apply protocol slice.
Add a later `DevelopmentTransaction` envelope for heterogeneous governed
changes, with domain-owned mutation bundles such as Dominium transaction
records. AIDE governs the envelope; the domain owns semantics.

## Artifact, Event, And Evidence Contract

Unify portable outputs and state transitions around ArtifactReference,
PreviewArtifact, EventEnvelope, EvidencePacket, Diagnostic, Refusal,
ReplayTrace, and ValidationResult.

## Preview Primitive

Add `PreviewSession` and `ShadowWorkspace` before mutation-capable Workbench
work. Preview should run proposed changes against disposable overlays or
snapshots, emit preview artifacts and evidence, and fail closed when base
revision, preimage, allowed scope, capability, approval, or validation
requirements do not match.
