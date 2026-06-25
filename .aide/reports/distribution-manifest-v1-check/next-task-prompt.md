# AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01

Create and process `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01`.

Repair only the material findings from `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01` without broadening DistributionManifest v1 into install/apply, publication, target mutation, or ProjectLock work.

Material findings to close:

- schema.optional_extension_boundary_missing
- identity.mutable_status_changes_distribution_digest
- component.graph_integrity_not_validated
- artifact.integrity_metadata_not_validated
- path.preaccess_validation_order_violation
- checksum.value_not_verified
- protocol.range_semantics_incomplete
- contamination.forbidden_members_silently_filtered
- fixture.required_coverage_incomplete

Stop at `needs_review` and recommend exactly `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01`.
