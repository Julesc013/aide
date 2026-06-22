# Operation Guard Review

Guard assertions emphasize exercised evidence rather than static declarations.

| Assertion | Outcome | Severity |
| --- | --- | --- |
| `conformance.unsupported_uses_actual_cli_dispatch` | FAIL | MATERIAL |
| `conformance.no_write_surrounds_actual_operations` | FAIL | MATERIAL |
| `conformance.guard_evidence_is_exercised` | FAIL | MATERIAL |
| `conformance.result_structure` | PASS | WARNING |
| `operation.raw_trace_digest_recomputes` | PASS | MATERIAL |
| `operation.git_classifier_source_covers_remote_and_ref_mutations` | PASS | MATERIAL |
| `operation.aggregate_key_preserves_semantics` | FAIL | MATERIAL |
| `operation.guard_report_is_not_static` | FAIL | MATERIAL |
| `operation.guard_families_present` | PASS | WARNING |
