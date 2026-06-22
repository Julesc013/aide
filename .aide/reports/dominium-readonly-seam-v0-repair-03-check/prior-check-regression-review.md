# Prior Check Regression Review

Earlier findings were resampled through current artifacts and source inspection.

| Assertion | Outcome | Severity |
| --- | --- | --- |
| `schema.draft_2020_12_and_refs` | PASS | MATERIAL |
| `schema.false_boundaries_const_false` | PASS | MATERIAL |
| `schema.kind_specific_defs_present` | FAIL | MATERIAL |
| `schema.authority_extensions_bounded` | FAIL | MATERIAL |
| `schema.current_bundle_has_expected_identity` | PASS | MATERIAL |
| `fixture.committed_negative_replay_digest` | PASS | MATERIAL |
| `fixture.production_requires_value` | FAIL | MATERIAL |
| `fixture.production_rejects_unicode_decimal_indexes` | FAIL | MATERIAL |
| `fixture.production_forbidden_key_set_complete` | FAIL | MATERIAL |
| `fixture.production_remove_missing_refused` | PASS | MATERIAL |
| `fixture.production_replace_missing_refused` | PASS | MATERIAL |
| `operation.raw_trace_digest_recomputes` | PASS | MATERIAL |
| `operation.git_classifier_source_covers_remote_and_ref_mutations` | PASS | MATERIAL |
| `operation.aggregate_key_preserves_semantics` | FAIL | MATERIAL |
| `operation.guard_report_is_not_static` | FAIL | MATERIAL |
| `operation.guard_families_present` | PASS | WARNING |
| `portability.required_child_output_set_complete` | FAIL | MATERIAL |
| `portability.environment_sanitized` | PASS | MATERIAL |
| `portability.no_absolute_path_leaks_reported` | PASS | WARNING |
