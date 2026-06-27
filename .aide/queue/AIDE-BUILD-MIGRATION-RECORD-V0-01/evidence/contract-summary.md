# Contract Summary

MigrationRecord v0 models:

- `migration_record_ref`
- `source_object_ref`
- `source_schema_version`
- `target_schema_version`
- `migration_kind`
- `migration_plan_ref`
- `input_digest`
- `output_digest`
- `field_mapping_summary`
- `unknown_field_disposition`
- `manual_review_items`
- `risk_class`
- `validation_refs`
- `rollback_requirements`
- `evidence_refs`
- `explicit_non_capabilities`
- `extensions`

It fails closed for missing source object, missing input digest, output digest mismatch, unknown required feature/extension, destructive migration without rollback requirements, ambiguous migration without manual review, source latest output misuse, source output as target truth, missing evidence, apply authority claims, and target mutation claims.
