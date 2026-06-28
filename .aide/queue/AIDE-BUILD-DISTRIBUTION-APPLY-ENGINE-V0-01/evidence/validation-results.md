# Validation Results

- py_compile: PASS
- focused DistributionApplyEngine tests: PASS, 7 tests
- `distribution-apply status`: PASS_WITH_WARNINGS
- `distribution-apply plan --scenario managed-file-update`: PASS_WITH_WARNINGS
- `distribution-apply run --scenario managed-file-update --mode apply-temp`: PASS_WITH_WARNINGS
- `distribution-apply verify`: PASS_WITH_WARNINGS
- predecessor regression validation: PASS
- Q43-Q48 no-apply/no-publish validators: PASS
- broad `aide_lite.py validate`: PASS

Build report counters:

- material_finding_count: `0`
- missing_evidence: `0`
- fixture_matrix_passed: `true`
- canonical_fixture_unchanged: `true`
- rollback_verified: `true`
- update_receipt_generated: `true`
- real_target_repo_modified: `false`
- source_repo_apply_occurred: `false`
- external_repo_touched: `false`
- release_publication_occurred: `false`
- network_calls_occurred: `false`
- provider_model_calls_occurred: `false`
