# AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01

Create and process `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01`.

Independently verify that `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01` closes exactly the nine material findings from `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01` without accepting DistributionManifest v1 or beginning ProjectLock v0.

Verify:

- optional extension surfaces are explicit and preserve optional extension values;
- mutable status/controller fields do not affect distribution identity while immutable spec/metadata/artifact/component changes do;
- component graph integrity, component digest recomputation, artifact-ref closure, dependency closure, and cycle rejection work;
- artifact byte count, digest, media type, compression type, path containment, checksum, and provenance metadata are validated;
- malformed release artifact paths are rejected before stat/open/hash/traversal;
- checksum values match artifact content digests and basename collisions fail closed;
- protocol range, reader/writer, component compatibility, required feature, optional feature, and migration semantics are enforced;
- forbidden local-directory members produce contamination evidence;
- the required fixture corpus exists and validates deterministically;
- no install/update/repair/rollback/uninstall apply, release publication, target mutation, network/provider/model call, Workbench/MCP runtime, source-change preview/apply/rollback, promotion, acceptance, or ProjectLock work occurred.

If all material checks pass, recommend exactly `AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01`.

If a material defect remains, recommend exactly `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-02`.

Stop at `needs_review`.
