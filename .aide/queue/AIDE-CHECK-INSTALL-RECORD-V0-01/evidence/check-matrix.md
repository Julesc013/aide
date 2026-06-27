# Check Matrix

| Objective | Result | Evidence |
| --- | --- | --- |
| Build task exists and stopped at needs_review | PASS | `task inspect` and build status file |
| Required task-local evidence exists | PASS | `task evidence` reported `missing_evidence: 0` |
| Required InstallRecord fields are modeled | PASS | schema, helper, tests, generated record |
| DistributionManifest binding is validated | PASS | `install_record.distribution_missing`, `install_record.distribution_mismatch` fixtures/tests |
| ProjectLock binding is validated | PASS | `install_record.project_lock_missing`, `install_record.project_lock_mismatch` fixtures/tests |
| OwnershipLedger binding is validated | PASS | `install_record.ownership_ledger_missing`, `install_record.ownership_ledger_mismatch` fixtures/tests |
| Installed component refs must be known | PASS | `install_record.component_ref_unknown` fixture/test |
| Installed file-entry refs must be known | PASS | `install_record.ownership_entry_ref_unknown` fixture/test |
| Installed managed-section refs must be known | PASS | `install_record.managed_section_ref_unknown` fixture/test |
| Apply authority claims fail closed | PASS | `install_record.apply_authority_claimed` fixture/test |
| Target mutation claims fail closed | PASS | `install_record.target_mutation_claimed` fixture/test |
| Unknown required feature fails closed | PASS | `install_record.unknown_required_feature` fixture/test |
| Unknown required extension fails closed | PASS | `install_record.extension_required_unknown` fixture/test |
| Absolute and traversal paths fail closed | PASS | `install_record.absolute_path_forbidden`, `install_record.path_traversal_forbidden` fixtures/tests |
| Source latest output misuse fails closed | PASS | `install_record.source_state_contamination` fixture/test |
| Source output as target truth fails closed | PASS | `install_record.source_output_as_target_truth` fixture/test |
| Missing evidence fails closed | PASS | `install_record.evidence_missing` fixture/test |
| Unknown optional features/extensions are tolerated | PASS | focused unit test |
| Non-capabilities preserved | PASS | status/report fields and Q43-Q48 validators |

Material finding count: `0`.
