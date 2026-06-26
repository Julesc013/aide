# Ownership Taxonomy

The ledger defines exactly these ownership classes:

- `vendor_managed_file`
- `vendor_managed_section`
- `project_owned`
- `project_overlay`
- `project_generated`
- `runtime_generated`
- `local_only`
- `evidence_only`
- `preserved_legacy`
- `unknown`
- `never_touch`

Every class is represented by at least one ledger record. Automatic apply,
overwrite, and delete are false for all records in v1.
