# Status Semantics Review

Validation confirms:

- accepted_with_warnings is preserved and not flattened to done
- WorkerRun and TestJob are `metadata_only: true`
- Reconciler is `report_only: true`
- WorkUnit queue, ReferenceID, EventRecord, and OKF are projection-oriented
- runtime is false for all projected current capabilities
- admitted_by_conformance is false for all projected current capabilities
- the only mutating projected capability is the accepted queue-local WorkUnit
  metadata mutation CLI

CapabilityManifest itself is `declaration_only: true` and `mutating: false`.
