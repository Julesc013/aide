# DistributionApplyEngine v0 Validation

- result: `PASS_WITH_WARNINGS`
- material_finding_count: `0`
- missing_evidence: `0`
- recommended_next_task: `AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01`

## Scenario Results

| Scenario | Expected | Observed | Code | Pass |
| --- | --- | --- | --- | --- |
| absolute-path-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.absolute_path_refused | true |
| canonical-fixture-mutation-detection | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.canonical_fixture_mutation_detected | true |
| canonical-fixture-unchanged | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| case-collision-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.case_collision_refused | true |
| evidence-only-overwrite-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.evidence_only_overwrite_refused | true |
| evidence-only-preservation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| legacy-preservation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| local-only-overwrite-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.local_only_overwrite_refused | true |
| local-only-preservation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| managed-file-add | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| managed-file-remove | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| managed-file-update | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| managed-section-add | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| managed-section-remove | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| managed-section-update | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| missing-preimage-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.missing_preimage_refused | true |
| missing-rollback-requirement-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.missing_rollback_requirement_refused | true |
| mixed-managed-file-and-section-update | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| never-touch-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.never_touch_update_refused | true |
| no-op-update | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| operation-lacking-rollback-coverage-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.operation_lacking_rollback_coverage_refused | true |
| operation-not-in-plan-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.operation_not_in_plan_refused | true |
| path-traversal-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.path_traversal_refused | true |
| postimage-digest-mismatch-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.postimage_digest_mismatch_refused | true |
| preimage-digest-mismatch-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.preimage_digest_mismatch_refused | true |
| project-overlay-overwrite-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.project_overlay_overwrite_refused | true |
| project-overlay-preservation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| project-owned-overwrite-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.project_owned_overwrite_refused | true |
| project-owned-preservation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| rollback-digest-mismatch-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.rollback_digest_mismatch_refused | true |
| rollback-success | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| runtime-generated-overwrite-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.runtime_generated_overwrite_refused | true |
| runtime-generated-preservation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| symlink-reparse-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.symlink_reparse_refused | true |
| unknown-ownership-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.unknown_ownership_update_refused | true |
| unknown-required-feature-refusal | FAILED_VALIDATION | FAILED_VALIDATION | distribution_apply_engine.unknown_required_feature_refused | true |
| update-receipt-generation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |

## Warnings

- DistributionApplyEngine v0 remains proposed until independent check and acceptance.
- Execution is limited to temp copies of committed fixture scenarios.
- The engine is not real target apply, source repo self-update, release, or canary authority.
