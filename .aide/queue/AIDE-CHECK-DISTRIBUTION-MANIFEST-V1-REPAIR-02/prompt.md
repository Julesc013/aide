# AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-02

Independently check `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-02`.

Do not repair implementation. Do not accept DistributionManifest v1. Do not
begin ProjectLock v0.

Verify the four Repair 02 findings:

- `protocol.future_major_not_implicitly_accepted`
- `contamination.forbidden_path_classification_complete`
- `contamination.directory_forbidden_members_recorded`
- `fixture.future_major_protocol_fixture_present`

If zero material findings remain, recommend exactly:

`AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01`

If any material finding remains, recommend exactly:

`AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-03`
