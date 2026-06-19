# Accepted Scope

Accepted capability:

```text
minimal_adapter_manifest_schema
```

Accepted behavior:

- represent an adapter declaration;
- project deterministic AdapterManifest records and reports;
- validate the minimal structural and semantic subset;
- inspect reference, capability, conformance, admission, execution, security,
  and explicit non-capability boundaries;
- report status and validation results.

Forbidden interpretation: AIDE can admit, trust, execute, launch, sandbox, or
apply adapter-driven changes.
