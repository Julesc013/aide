# Prompt

Create and process `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01`.

Repo truth outranks this prompt. Repair exactly the nine material findings from `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01`:

- `schema.optional_extension_boundary_missing`
- `identity.mutable_status_changes_distribution_digest`
- `component.graph_integrity_not_validated`
- `artifact.integrity_metadata_not_validated`
- `path.preaccess_validation_order_violation`
- `checksum.value_not_verified`
- `protocol.range_semantics_incomplete`
- `contamination.forbidden_members_silently_filtered`
- `fixture.required_coverage_incomplete`

Before production edits, create task-local machine-readable `turn-context.json`, `finding-matrix.json`, `allowed-paths.json`, `validation-plan.json`, `stop-conditions.json`, and `campaign-state.json`.

Do not start ProjectLock v0. Do not accept DistributionManifest v1. Stop at `needs_review` and recommend exactly `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01`.
