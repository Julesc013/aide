# Interop Export Boundary

Accepted predecessors are sufficient to create static preview exports:

- the queue identifies serialized task order;
- ContextPack v2 supplies a deterministic projection boundary;
- PatchTransaction remains no-apply;
- AdapterManifest remains declaration-only and non-admitting;
- CapabilityManifest declares but does not admit;
- ConformanceResult records observations but does not grant trust.

This build task does not accept any interop capability. It only creates preview
artifacts and evidence for independent check.

The future Host Contract, CapabilityInvocation, DevelopmentTransaction,
PreviewSession, Dominium Bridge conformance, Workbench, Commander, Service, and
runtime lanes remain deferred queue work.
