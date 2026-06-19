# Schema Helper Review

Added `.aide/protocol/aide-adapter-manifest.schema.json` and
`core/protocol/adapter_manifest.py`.

The helper projects one deterministic declaration-only AdapterManifest record,
loads the schema, validates the schema/helper structural subset, writes
deterministic reports, and preserves explicit no-execution facts.

Validation mode remains a minimal JSON Schema subset plus AdapterManifest
semantic checks, not full JSON Schema Draft compliance.
