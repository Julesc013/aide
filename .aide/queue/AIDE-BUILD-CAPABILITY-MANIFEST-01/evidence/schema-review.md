# Schema Review

Schema path: `.aide/protocol/aide-capability-manifest.schema.json`.

Reviewed:

- Uses the AIDE envelope pattern: `apiVersion`, `kind`, `metadata`, `spec`, and
  `status`.
- `kind` is restricted to `CapabilityManifest`.
- `spec.capabilities` requires stable labels, `aide://capability/*` refs,
  declaration/implementation/check/acceptance booleans, status flags, source
  refs, evidence refs, report refs, known limitations, explicit
  non-capabilities, and conformance placeholders.
- `status` explicitly records declaration-only behavior and false
  conformance/admission/execution/runtime/mutating flags for the manifest.

Gap:

- Full JSON Schema Draft 2020-12 validation remains deferred; the helper uses a
  local structural subset check, matching recent AIDE protocol slices.
