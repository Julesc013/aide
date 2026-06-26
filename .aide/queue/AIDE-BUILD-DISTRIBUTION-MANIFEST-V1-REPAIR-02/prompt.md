# AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-02

Create and process the bounded build repair for DistributionManifest v1.

Repair exactly the four material findings from
`AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01`:

- `protocol.future_major_not_implicitly_accepted`
- `contamination.forbidden_path_classification_complete`
- `contamination.directory_forbidden_members_recorded`
- `fixture.future_major_protocol_fixture_present`

Do not redesign DistributionManifest v1. Do not start ProjectLock v0,
OwnershipLedger v1, InstallRecord v0, install/update/repair/rollback/uninstall
apply, release publication, target mutation, Workbench/MCP/runtime/provider,
worker, preview/apply/rollback, or promotion work.

Stop at `needs_review` with complete evidence and recommend exactly:

`AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-02`
