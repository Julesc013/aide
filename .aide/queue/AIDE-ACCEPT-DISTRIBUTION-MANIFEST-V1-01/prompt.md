# AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01

Accept exactly:

`distribution_manifest_v1`

Accepted meaning: stable, deterministic, portable DistributionManifest v1
identity and metadata for one local AIDE distribution.

Do not accept ProjectLock, OwnershipLedger, InstallRecord, MigrationRecord,
UpdatePlan, RollbackBundle, UpdateReceipt, install/update/repair/rollback/
uninstall apply, target mutation, public release readiness, release publication,
Git tags, GitHub Releases, uploads, signature verification, SBOM generation,
network, provider/model calls, worker execution, or Workbench/MCP runtime.

Stop at `needs_review` with `ACCEPTED_WITH_WARNINGS` and recommend exactly:

`AIDE-BUILD-PROJECT-LOCK-V0-01`
