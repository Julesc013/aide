# Schema Helper Review

The schema parses, declares `kind: AdapterManifest`, and aligns with the helper
for the implemented minimal subset. The helper projects one deterministic
declaration record and validates required envelope, spec, status, reference,
capability, conformance, admission, execution, security, and non-capability
fields.

Full JSON Schema Draft validation remains future work and is warning-classified.
