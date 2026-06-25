# Dependency Graph Review

The selected v1 build order is:

1. `DistributionManifest v1`
2. `ProjectLock v0`
3. `OwnershipLedger v1`
4. `InstallRecord v0`
5. `MigrationRecord v0`
6. `UpdatePlan v1`
7. `RollbackBundle v0`
8. `UpdateReceipt v0`
9. fixture-only `DistributionApplyEngine v0`
10. `AIDE self-consumer fixture v0`

Rationale:

- `DistributionManifest v1` must be first because it defines the content and
  component identity that downstream locks, ledgers, records, plans, bundles,
  and receipts bind to.
- `ProjectLock v0` comes before update planning because v1 needs a declared
  selected distribution, not just observed files.
- `OwnershipLedger v1` comes before apply planning because unknown or
  project-owned paths must block automatic apply.
- `InstallRecord v0` records what happened and prevents desired state from
  being confused with observed installed state.
- `MigrationRecord v0` prevents format/ownership transitions from rewriting
  history.
- `UpdatePlan v1` can only be immutable after the manifest, lock, ownership,
  install, and migration records exist.
- `RollbackBundle v0` must exist before apply.
- `UpdateReceipt v0` records the execution and validation result after apply.
- The apply engine must wait until all dependency records have independent
  checks and acceptance.
