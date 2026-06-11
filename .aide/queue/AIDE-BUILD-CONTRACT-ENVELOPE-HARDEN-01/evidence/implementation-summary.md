# Implementation Summary

## Changed

- Added `load_envelope_schema(repo_root)` in `core/protocol/envelope.py`.
- Added `validate_envelope_with_schema(obj, schema)` for the current schema's
  minimal JSON Schema subset.
- Added `validate_envelope_runtime(obj, schema, allowed_kinds)` so helper and
  schema validation run together.
- Added `check_schema_helper_alignment(schema)` for the helper/schema required
  field and basic type contract.
- Updated `contract_envelope_validate` to report schema load, parse, validation,
  helper alignment, helper errors, schema errors, compatibility probes, and
  limitations.
- Updated `contract-envelope validate` stdout to show schema validation status.
- Added focused tests for runtime schema validation and helper/schema agreement.

## Runtime Validation Approach

The validator is intentionally local and small. It supports the schema keywords
used by `.aide/protocol/aide-envelope.schema.json`: `type`, `required`,
`properties`, simple `additionalProperties`, and homogeneous array `items`.

## Limitations

- Full JSON Schema Draft 2020-12 validation is not implemented.
- Formats, refs, oneOf/anyOf/allOf, conditionals, numeric bounds, and pattern
  checks are not implemented.

## Not Implemented

No EvidencePacket schema, WorkUnit schema, WorkUnit CLI, TestJob schema, Test
Broker, Service, Commander, provider adapter, branch/worktree automation,
target repo apply, active repo apply, rollback execution, release, promotion,
network, Gateway, GitHub mutation, or model/provider call was added.
