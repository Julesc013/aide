# Contract Summary

InstallRecord v0 records observed or completed AIDE installation state without performing installation.

Accepted fields include:

- `install_record_ref`
- `target_project_ref`
- `install_mode`
- `install_source`
- `source_distribution_ref`
- `project_lock_ref`
- `ownership_ledger_ref`
- `observed_existing_state`
- `installed_component_refs`
- `installed_file_entry_refs`
- `installed_managed_section_refs`
- `validation_refs`
- `evidence_refs`
- `warnings`
- `explicit_non_capabilities`
- `created_at`
- `created_by`
- `extensions`

Semantic validation fails closed for missing predecessor refs, predecessor mismatches, unknown installed refs, apply authority claims, target mutation claims, unknown required features, absolute or traversal paths, source-output misuse, missing evidence, digest mismatch, and unknown required extensions.
