# Object Model

`DistributionManifest v1` defines:

- distribution identity and release/channel metadata;
- source release-bundle references;
- supported protocol range, reader/writer versions, features and migrations;
- component inventory;
- artifact inventory;
- checksum and provenance references;
- SBOM/signature placeholders and boundaries;
- deterministic payload and distribution digests;
- explicit non-capabilities.

It does not encode target ownership. Target selection and ownership remain for
later `ProjectLock` and `OwnershipLedger` tasks.
