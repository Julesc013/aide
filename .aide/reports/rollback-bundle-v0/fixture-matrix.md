# RollbackBundle v0 Fixture Matrix

| Case | Expected | Observed | Codes | Pass |
| --- | --- | --- | --- | --- |
| conflict-only-rollback-bundle | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| install-record-restore-plan | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| managed-file-preimage-rollback-plan | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| managed-section-preimage-rollback-plan | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| manual-review-limitation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| mixed-managed-file-and-section-plan | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| no-op-rollback-bundle | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| optional-extensions-preservation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| ownership-ledger-restore-plan | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| project-lock-restore-plan | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| remove-added-managed-file-reverse-plan | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| remove-added-managed-section-reverse-plan | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| rollback-unavailable-limitation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| absolute-path | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.absolute_path_forbidden | true |
| missing-ownership-ledger | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.ownership_ledger_mismatch, rollback_bundle.ownership_ledger_missing | true |
| missing-preimage | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.preimage_artifact_missing | true |
| missing-prior-lock | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.project_lock_mismatch, rollback_bundle.project_lock_missing | true |
| missing-rollback-evidence | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.reverse_operation_evidence_missing | true |
| missing-update-plan-ref | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.update_plan_missing | true |
| preimage-digest-mismatch | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.preimage_digest_mismatch | true |
| reverse-local-only-mutation | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.local_only_reverse_mutation, rollback_bundle.preimage_artifact_missing | true |
| reverse-never-touch-mutation | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.never_touch_reverse_mutation, rollback_bundle.preimage_artifact_missing | true |
| reverse-project-owned-mutation | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.preimage_artifact_missing, rollback_bundle.project_owned_reverse_mutation | true |
| rollback-apply-authority-claim | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.rollback_apply_authority_claimed | true |
| source-latest-as-target-truth | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.source_state_contamination | true |
| target-mutation-authority-claim | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.target_mutation_claimed | true |
| traversal-path | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.path_traversal_forbidden | true |
| unknown-ownership-reverse-operation | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.preimage_artifact_missing, rollback_bundle.unknown_ownership_reverse_operation | true |
| unknown-required-feature | FAILED_VALIDATION | FAILED_VALIDATION | rollback_bundle.unknown_required_feature | true |
