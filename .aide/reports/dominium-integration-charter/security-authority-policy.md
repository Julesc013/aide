# Security And Authority Policy

- Remote workers never directly mutate authoritative Workbench state.
- MCP endpoint authorization does not replace AIDE authorization.
- A2A discovery does not grant trust.
- AdapterManifest does not grant admission.
- ConformanceResult does not grant use by itself.
- Future CapabilityGrant is bounded.
- Future PolicyDecision applies to one intended use.
- Owning domain/host performs authoritative apply.
- Workbench approval does not bypass domain command/refusal/evidence law.
- Read-only context projection must carry source revision, digest, authority class, and freshness.
- No raw provider secrets are introduced or recorded by this charter.
- No live provider, model, network, worker, transport, or repository mutation authority is introduced by this charter.
