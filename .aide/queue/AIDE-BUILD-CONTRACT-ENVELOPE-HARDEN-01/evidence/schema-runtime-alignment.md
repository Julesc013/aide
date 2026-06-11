# Schema Runtime Alignment

- schema file path: `.aide/protocol/aide-envelope.schema.json`
- schema parse status: parsed
- schema validation mode: `minimal_json_schema_subset`
- schema validation executed: true
- helper/schema alignment checked: true
- helper/schema alignment result: PASS

## Fields Checked

- top-level required fields: `apiVersion`, `kind`, `metadata`, `spec`, `status`
- top-level basic types: string for `apiVersion` and `kind`; object for
  `metadata`, `spec`, and `status`
- declared nested compatibility field basic types
- array item types for compatibility feature and capability lists

## Compatibility Probes

- Unknown optional fields remain tolerated.
- Unknown required capabilities still fail closed through helper/runtime
  validation.

## Limitations

- This is not full JSON Schema Draft 2020-12 validation.
- Unsupported future schema constructs should be added deliberately or reported
  instead of silently relied on.
