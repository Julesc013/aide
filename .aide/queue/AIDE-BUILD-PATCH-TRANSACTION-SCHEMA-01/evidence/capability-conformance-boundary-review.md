# Capability And Conformance Boundary Review

The record can require capability refs and ConformanceResult refs before any
future apply step. Their presence is not admission or trust.

Preserved boundaries:

- CapabilityManifest still declares; it does not execute.
- ConformanceProfile still defines candidate requirements; it is not activated.
- ConformanceResult remains evidence-projected, runnerless, non-admitting, and
  non-trusting.
- A referenced ConformanceResult does not set `trusted: true`.
- This build does not accept `minimal_patch_transaction_schema`.

PatchTransaction acceptance remains a later check/accept chain.
