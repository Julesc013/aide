# DistributionApplyEngine v0 Refusal Summary

| Scenario | Refusal Code | Expected |
| --- | --- | --- |
| absolute-path-refusal | distribution_apply_engine.absolute_path_refused | true |
| canonical-fixture-mutation-detection | distribution_apply_engine.canonical_fixture_mutation_detected | true |
| case-collision-refusal | distribution_apply_engine.case_collision_refused | true |
| evidence-only-overwrite-refusal | distribution_apply_engine.evidence_only_overwrite_refused | true |
| local-only-overwrite-refusal | distribution_apply_engine.local_only_overwrite_refused | true |
| mismatched-update-plan-rollback-bundle | distribution_apply_engine.update_plan_rollback_bundle_mismatch | true |
| missing-preimage-refusal | distribution_apply_engine.missing_preimage_refused | true |
| missing-rollback-bundle-binding | distribution_apply_engine.rollback_bundle_binding_missing | true |
| missing-rollback-requirement-refusal | distribution_apply_engine.missing_rollback_requirement_refused | true |
| missing-update-plan-binding | distribution_apply_engine.update_plan_binding_missing | true |
| never-touch-refusal | distribution_apply_engine.never_touch_update_refused | true |
| operation-lacking-rollback-coverage-refusal | distribution_apply_engine.operation_lacking_rollback_coverage_refused | true |
| operation-not-in-plan-refusal | distribution_apply_engine.operation_not_in_plan_refused | true |
| path-traversal-refusal | distribution_apply_engine.path_traversal_refused | true |
| postimage-digest-mismatch-refusal | distribution_apply_engine.postimage_digest_mismatch_refused | true |
| predecessor-install-record-mismatch | distribution_apply_engine.predecessor_mismatch | true |
| predecessor-migration-record-mismatch | distribution_apply_engine.predecessor_mismatch | true |
| predecessor-ownership-ledger-mismatch | distribution_apply_engine.predecessor_mismatch | true |
| predecessor-project-lock-mismatch | distribution_apply_engine.predecessor_mismatch | true |
| predecessor-source-distribution-mismatch | distribution_apply_engine.predecessor_mismatch | true |
| preimage-digest-mismatch-refusal | distribution_apply_engine.preimage_digest_mismatch_refused | true |
| project-overlay-overwrite-refusal | distribution_apply_engine.project_overlay_overwrite_refused | true |
| project-owned-overwrite-refusal | distribution_apply_engine.project_owned_overwrite_refused | true |
| rollback-digest-mismatch-refusal | distribution_apply_engine.rollback_digest_mismatch_refused | true |
| run-without-accepted-context | distribution_apply_engine.accepted_context_missing | true |
| runtime-generated-overwrite-refusal | distribution_apply_engine.runtime_generated_overwrite_refused | true |
| symlink-reparse-refusal | distribution_apply_engine.symlink_reparse_refused | true |
| unknown-ownership-refusal | distribution_apply_engine.unknown_ownership_update_refused | true |
| unknown-required-feature-refusal | distribution_apply_engine.unknown_required_feature_refused | true |
