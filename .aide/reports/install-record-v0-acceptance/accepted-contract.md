# Accepted InstallRecord v0 Contract

InstallRecord v0 is accepted as a record of observed or completed install state.

Accepted fields include:

- install record refs and target project refs
- install mode and install source
- source DistributionManifest ref/digest
- ProjectLock ref/digest
- OwnershipLedger ref/digest
- observed existing state metadata
- installed component refs
- installed file-entry refs
- installed managed-section refs
- validation refs
- evidence refs
- warnings
- explicit non-capabilities
- created-at and created-by metadata
- extension maps

Accepted validation behavior:

- predecessor refs and digests must match accepted DistributionManifest, ProjectLock, and OwnershipLedger.
- installed refs must be present in accepted predecessor objects.
- unknown required features/extensions fail closed.
- unsafe paths and source-output misuse fail closed.
- missing evidence fails closed.
- unknown optional features/extensions are tolerated.
