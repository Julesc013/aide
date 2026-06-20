# AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01

Create and process `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`.

Use `.aide/queue/index.yaml` as canonical AIDE queue truth. Re-read live repository state before writing anything.

This is a milestone-sized BUILD task. Implement the complete offline, deterministic, read-only AIDE-Dominium seam v0 authorized by `AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01`.

Deliver a working vertical slice with contracts, implementation, projection, CLI, fixtures, validation, tests, reports, and an end-to-end offline demonstration.

Required seam objects:

- HostManifest
- HostCapabilitySet
- WorkspaceDescriptor
- ContextDescriptor
- ArtifactReference
- EventEnvelope
- DiagnosticProjection
- RefusalProjection
- EvidenceReferenceSet
- DominiumBridgeManifest
- deterministic SeamBundle

Required CLI commands:

- `dominium-seam status`
- `dominium-seam snapshot`
- `dominium-seam project`
- `dominium-seam validate`
- `dominium-seam diff`
- `dominium-seam demo`

Unsupported verbs must fail closed: `run`, `invoke`, `execute`, `apply`, `write`, `sync`, `push`, `serve`, `connect`, `dispatch`.

Stop at `needs_review` and recommend only `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01`.
