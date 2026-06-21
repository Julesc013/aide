# Schema Contract Review

```json
{
  "invalid_case_coverage": {
    "empty_content_digests": true,
    "empty_cross_reference_index": true,
    "empty_manifest": true,
    "empty_source_snapshot": true,
    "empty_status": false,
    "kind_specific_spec_constraints": false,
    "records_additional_properties_closed": true
  },
  "material_gaps": [
    "public schema does not constrain kind-specific spec fields",
    "public schema does not constrain status facts"
  ],
  "required_sections": {
    "content_digests": true,
    "cross_reference_index": true,
    "manifest": true,
    "registry_projection_summary": true,
    "source_snapshot": true,
    "status": true
  },
  "result": "REQUEST_CHANGES"
}
```
