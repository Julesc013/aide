# Remaining Risks

- DistributionManifest v1 is proposed only until independent check and
  acceptance.
- Q47 release artifacts remain local preview/no-publish artifacts.
- The Q47 source provenance records dirty-state metadata from the historical
  local bundle build; this build preserves that as a warning rather than
  claiming public release readiness.
- Signature verification and SBOM generation remain future work.
- Install/update apply remains future work and requires ProjectLock,
  OwnershipLedger, InstallRecord, MigrationRecord, UpdatePlan, RollbackBundle
  and UpdateReceipt gates.
