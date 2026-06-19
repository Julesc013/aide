# Schema And Helper Alignment

- Schema path: `.aide/protocol/aide-patch-transaction.schema.json`
- Helper path: `core/protocol/patch_transaction.py`
- Schema title: `AIDE Minimal PatchTransaction`
- Required envelope fields: `apiVersion`, `kind`, `metadata`, `spec`, `status`
- Helper validation mode:
  `minimal_json_schema_subset_plus_patch_transaction_semantics`
- Validation report field:
  `schema_helper_alignment_status: PASS`

The helper performs semantic checks beyond the JSON Schema subset: ReferenceID
syntax, fixed transaction identity, sha256 digest shape and binding, normalized
scope checks, lifecycle/no-apply consistency, required reference kinds,
explicit non-capability preservation, and source immutability.
