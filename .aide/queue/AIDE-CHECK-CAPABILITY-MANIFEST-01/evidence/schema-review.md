# Schema Review

Reviewed:

- `.aide/protocol/aide-capability-manifest.schema.json`

Finding: pass with warning.

Confirmed:

- File exists and parses as JSON.
- `kind` is restricted to `CapabilityManifest`.
- Required envelope fields are present: `apiVersion`, `kind`, `metadata`,
  `spec`, and `status`.
- `spec.capabilities` models capability refs, labels, declaration state,
  implementation state, check state, acceptance state, class/tags, source refs,
  evidence refs, report refs, event refs, OKF refs, known limitations,
  explicit non-capabilities, status flags, and conformance placeholders.
- `status` includes declaration-only behavior and false
  conformance/admission/execution/runtime/mutating boundaries.

Warning:

- Full JSON Schema Draft 2020-12 validation remains deferred. The build helper
  uses the same minimal structural validation pattern as recent AIDE protocol
  slices.
