# Accepted Context Binding

The internal `AcceptedDistributionApplyContext` is represented by `core/distribution/apply_context.py`.

Required accepted reports:

- DistributionManifest v1 acceptance
- ProjectLock v0 acceptance
- OwnershipLedger v1 acceptance
- InstallRecord v0 acceptance
- MigrationRecord v0 acceptance
- UpdatePlan v1 acceptance
- RollbackBundle v0 acceptance
- UpdateReceipt v0 acceptance

Required bound refs:

- `source_distribution_ref`
- `candidate_distribution_ref`
- `current_project_lock_ref`
- `candidate_project_lock_ref`
- `ownership_ledger_ref`
- `install_record_refs`
- `migration_record_refs`
- `target_project_ref`
- `update_plan_ref`
- `rollback_bundle_ref`

The context check runs before static refusals, temp workspace creation, operation execution, rollback verification, or UpdateReceipt fixture output generation.
