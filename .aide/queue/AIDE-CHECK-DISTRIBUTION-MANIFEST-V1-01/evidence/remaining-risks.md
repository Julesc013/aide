# Remaining Risks

The check result is `REQUEST_CHANGES`. The next task must repair exactly these
material findings before acceptance or ProjectLock work:

- `schema.optional_extension_boundary_missing`
- `identity.mutable_status_changes_distribution_digest`
- `component.graph_integrity_not_validated`
- `artifact.integrity_metadata_not_validated`
- `path.preaccess_validation_order_violation`
- `checksum.value_not_verified`
- `protocol.range_semantics_incomplete`
- `contamination.forbidden_members_silently_filtered`
- `fixture.required_coverage_incomplete`

Deliberate deferrals:

- no implementation repair in this check task;
- no DistributionManifest v1 acceptance;
- no ProjectLock v0 work;
- no install/update/repair/rollback/uninstall apply;
- no release publication, tag, upload, target mutation, Workbench/MCP runtime,
  provider/model call, source-change preview/apply/rollback, or promotion.
