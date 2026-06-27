# InstallRecord v0 Validation

- result: PASS_WITH_WARNINGS
- proposed_capability: install_record_v0
- recommended_next_task: AIDE-CHECK-INSTALL-RECORD-V0-01

## Checks

- schema_exists: true
- helper_exists: true
- cli_registered: true
- install_record_generated: true
- install_record_valid: true
- schema_alignment: true
- fixture_matrix_passed: true
- ownership_ledger_accepted: true
- distribution_ref_bound: true
- project_lock_digest_bound: true
- ownership_ledger_digest_bound: true
- component_refs_known: true
- file_entry_refs_known: true
- managed_section_refs_known: true
- install_apply_not_implemented: true
- update_apply_not_implemented: true
- migration_apply_not_implemented: true
- rollback_apply_not_implemented: true
- uninstall_apply_not_implemented: true
- target_repository_mutation_not_implemented: true
- target_scan_authority_not_implemented: true
- release_publication_not_implemented: true
- source_output_not_target_truth: true

## Fixture Results

- existing-observed-install: true (PASS_WITH_WARNINGS)
- fresh-observed-install: true (PASS_WITH_WARNINGS)
- managed-file-observation: true (PASS_WITH_WARNINGS)
- managed-section-observation: true (PASS_WITH_WARNINGS)
- optional-extension-preserved: true (PASS_WITH_WARNINGS)
- warning-only-partial-observation: true (PASS_WITH_WARNINGS)
- absolute-path: true (FAILED_VALIDATION)
- apply-claim: true (FAILED_VALIDATION)
- extension-required-unknown: true (FAILED_VALIDATION)
- missing-distribution: true (FAILED_VALIDATION)
- missing-evidence: true (FAILED_VALIDATION)
- missing-lock: true (FAILED_VALIDATION)
- missing-ownership-ledger: true (FAILED_VALIDATION)
- ownership-ledger-mismatch: true (FAILED_VALIDATION)
- project-lock-mismatch: true (FAILED_VALIDATION)
- source-latest-output: true (FAILED_VALIDATION)
- source-mismatch: true (FAILED_VALIDATION)
- source-output-target-truth: true (FAILED_VALIDATION)
- target-mutation-claim: true (FAILED_VALIDATION)
- traversal-path: true (FAILED_VALIDATION)
- unknown-component-ref: true (FAILED_VALIDATION)
- unknown-managed-section-ref: true (FAILED_VALIDATION)
- unknown-ownership-entry-ref: true (FAILED_VALIDATION)
- unknown-required-feature: true (FAILED_VALIDATION)

## Warnings

- InstallRecord v0 is proposed until independent check and acceptance.
- InstallRecord records install metadata only and performs no install or target mutation.
