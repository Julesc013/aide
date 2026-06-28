# DistributionApplyEngine v0 Refusal Summary

| Scenario | Refusal Code | Expected |
| --- | --- | --- |
| absolute-path-refusal | distribution_apply_engine.absolute_path_refused | true |
| canonical-fixture-mutation-detection | distribution_apply_engine.canonical_fixture_mutation_detected | true |
| case-collision-refusal | distribution_apply_engine.case_collision_refused | true |
| evidence-only-overwrite-refusal | distribution_apply_engine.evidence_only_overwrite_refused | true |
| local-only-overwrite-refusal | distribution_apply_engine.local_only_overwrite_refused | true |
| missing-preimage-refusal | distribution_apply_engine.missing_preimage_refused | true |
| missing-rollback-requirement-refusal | distribution_apply_engine.missing_rollback_requirement_refused | true |
| never-touch-refusal | distribution_apply_engine.never_touch_update_refused | true |
| operation-lacking-rollback-coverage-refusal | distribution_apply_engine.operation_lacking_rollback_coverage_refused | true |
| operation-not-in-plan-refusal | distribution_apply_engine.operation_not_in_plan_refused | true |
| path-traversal-refusal | distribution_apply_engine.path_traversal_refused | true |
| postimage-digest-mismatch-refusal | distribution_apply_engine.postimage_digest_mismatch_refused | true |
| preimage-digest-mismatch-refusal | distribution_apply_engine.preimage_digest_mismatch_refused | true |
| project-overlay-overwrite-refusal | distribution_apply_engine.project_overlay_overwrite_refused | true |
| project-owned-overwrite-refusal | distribution_apply_engine.project_owned_overwrite_refused | true |
| rollback-digest-mismatch-refusal | distribution_apply_engine.rollback_digest_mismatch_refused | true |
| runtime-generated-overwrite-refusal | distribution_apply_engine.runtime_generated_overwrite_refused | true |
| symlink-reparse-refusal | distribution_apply_engine.symlink_reparse_refused | true |
| unknown-ownership-refusal | distribution_apply_engine.unknown_ownership_update_refused | true |
| unknown-required-feature-refusal | distribution_apply_engine.unknown_required_feature_refused | true |
