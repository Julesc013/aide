# InstallRecord v0 Fixture Matrix

| Case | Expected | Observed | Codes | Pass |
| --- | --- | --- | --- | --- |
| existing-observed-install | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| fresh-observed-install | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| managed-file-observation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| managed-section-observation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| optional-extension-preserved | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| warning-only-partial-observation | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | true |
| absolute-path | FAILED_VALIDATION | FAILED_VALIDATION | install_record.absolute_path_forbidden | true |
| apply-claim | FAILED_VALIDATION | FAILED_VALIDATION | install_record.apply_authority_claimed | true |
| extension-required-unknown | FAILED_VALIDATION | FAILED_VALIDATION | install_record.extension_required_unknown | true |
| missing-distribution | FAILED_VALIDATION | FAILED_VALIDATION | install_record.distribution_mismatch, install_record.distribution_missing | true |
| missing-evidence | FAILED_VALIDATION | FAILED_VALIDATION | install_record.evidence_missing | true |
| missing-lock | FAILED_VALIDATION | FAILED_VALIDATION | install_record.project_lock_mismatch, install_record.project_lock_missing | true |
| missing-ownership-ledger | FAILED_VALIDATION | FAILED_VALIDATION | install_record.ownership_ledger_mismatch, install_record.ownership_ledger_missing | true |
| ownership-ledger-mismatch | FAILED_VALIDATION | FAILED_VALIDATION | install_record.ownership_ledger_mismatch | true |
| project-lock-mismatch | FAILED_VALIDATION | FAILED_VALIDATION | install_record.project_lock_mismatch | true |
| source-latest-output | FAILED_VALIDATION | FAILED_VALIDATION | install_record.source_state_contamination | true |
| source-mismatch | FAILED_VALIDATION | FAILED_VALIDATION | install_record.distribution_mismatch | true |
| source-output-target-truth | FAILED_VALIDATION | FAILED_VALIDATION | install_record.source_output_as_target_truth | true |
| target-mutation-claim | FAILED_VALIDATION | FAILED_VALIDATION | install_record.target_mutation_claimed | true |
| traversal-path | FAILED_VALIDATION | FAILED_VALIDATION | install_record.path_traversal_forbidden | true |
| unknown-component-ref | FAILED_VALIDATION | FAILED_VALIDATION | install_record.component_ref_unknown | true |
| unknown-managed-section-ref | FAILED_VALIDATION | FAILED_VALIDATION | install_record.managed_section_ref_unknown | true |
| unknown-ownership-entry-ref | FAILED_VALIDATION | FAILED_VALIDATION | install_record.ownership_entry_ref_unknown | true |
| unknown-required-feature | FAILED_VALIDATION | FAILED_VALIDATION | install_record.unknown_required_feature | true |
