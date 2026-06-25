# AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01 Prompt

Create and process `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01`.

Repo truth outranks this prompt.

Source task: `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01`

Source commit: `ad975887910f6a7238ef076ce2fef0fd43687e37`

Source capability: `distribution_manifest_v1`

Source result: `PASS_WITH_WARNINGS`

This is an independent, check-only task. Do not repair implementation. Do not
accept DistributionManifest v1. Do not begin ProjectLock v0. Stop at
`needs_review`.

Check whether DistributionManifest v1 is a stable, deterministic, portable,
and independently verifiable identity for one local AIDE distribution. Source
reports and source helper output are evidence inputs, not authority.

The check must scrutinize:

- schema/envelope alignment and optional extension compatibility;
- immutable distribution identity versus mutable queue/status/controller state;
- independent canonicalization and digest recomputation;
- component digest, artifact reference, and dependency graph integrity;
- artifact integrity and source path safety before filesystem access;
- checksum value verification, not only checksum-name presence;
- protocol range semantics;
- Q47 source mapping and Q48 non-authority;
- status/spec authority separation;
- signature, SBOM, and source-contamination boundaries;
- fixture corpus coverage;
- explicit non-capabilities.

If any material finding remains, recommend exactly:

```text
AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01
```

If no material finding remains, recommend exactly:

```text
AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01
```
