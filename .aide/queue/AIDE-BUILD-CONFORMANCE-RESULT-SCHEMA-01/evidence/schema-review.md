# Schema Review

Reviewed `.aide/protocol/aide-conformance-result.schema.json`.

The schema defines a minimal `ConformanceResult` envelope with:

- `spec.result_ref`, `result_id`, and `result_version`;
- `spec.observation.mode: evidence_projection`;
- profile binding fields `ref`, `id`, `version`, and `digest`;
- subject boundary fields `admission_performed`, `subject_admitted`, and
  `trusted`;
- case-result fields for observed outcome, accepted outcomes, evidence refs,
  execution state, and runner ref;
- aggregation fields for record completeness and profile requirement
  satisfaction;
- status fields that keep record validity separate from profile satisfaction and
  admission.

The schema is intentionally permissive enough for future result extensions, but
this slice validates stricter semantics in the helper.
