# Accepted Context Binding

The accepted context gate is part of `core/distribution/apply_context.py` and is required by `core/distribution/apply_engine.py` before temp workspace setup, operation execution, rollback verification, or successful UpdateReceipt fixture output.

Accepted binding requirements:

- accepted predecessor reports must exist and report `ACCEPTED` or `ACCEPTED_WITH_WARNINGS`;
- accepted capability names must match the expected predecessor capability;
- predecessor reports must have zero material findings and zero missing evidence;
- each fixture scenario must bind to the accepted UpdatePlan ref;
- each fixture scenario must bind to the accepted RollbackBundle ref;
- RollbackBundle must be bound to the selected UpdatePlan;
- DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, and MigrationRecord refs must match expected accepted refs;
- operation refs must be present in both accepted UpdatePlan operation refs and RollbackBundle rollback-operation refs.

Original material findings closed:

- `distribution_apply_engine.update_plan_binding_not_enforced`
- `distribution_apply_engine.rollback_bundle_binding_not_enforced`
- `distribution_apply_engine.predecessor_mismatch_not_refused`
- `distribution_apply_engine.run_without_accepted_context`
