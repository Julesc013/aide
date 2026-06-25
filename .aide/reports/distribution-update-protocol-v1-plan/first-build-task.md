# First Build Task

Selected first build task:

```text
AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01
```

Why this first:

- It defines the distribution identity.
- It binds release/channel to components, digests, protocol ranges,
  compatibility, checksums, provenance, SBOM references, and signature
  placeholders.
- It can map directly onto existing Q47 release-bundle evidence without
  implementing install/update apply.
- Downstream `ProjectLock`, `OwnershipLedger`, `InstallRecord`,
  `MigrationRecord`, `UpdatePlan`, `RollbackBundle`, and `UpdateReceipt` need a
  stable distribution identity to reference.

The task must stop at `needs_review` and recommend
`AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01`.
