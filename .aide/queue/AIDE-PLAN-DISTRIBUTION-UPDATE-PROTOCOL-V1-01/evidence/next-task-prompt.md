# AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01

Create and process `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01`.

Repo truth outranks this prompt. Read the accepted
`AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01` packet and reports before
editing files.

Goal:

Build `DistributionManifest v1` as the first v1 distribution/update protocol
object, mapped onto existing Q47 release-bundle evidence and Q48 release-draft
boundaries without replacing Q43-Q48.

Requirements:

- define a Draft 2020-12 schema for `DistributionManifest v1`;
- provide deterministic helper/projection/validation behavior;
- bind distribution identity to release/channel, components, versions, content
  digests, protocol ranges, required migrations, compatibility, checksums,
  provenance, SBOM references, and signatures or signature placeholders;
- consume existing Q47 release bundle metadata as source evidence;
- preserve no-publish/no-upload/no-tag/no-target-mutation boundaries;
- include valid and invalid fixtures;
- add focused tests;
- emit reports and task-local evidence;
- stop at `needs_review`;
- recommend exactly `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01`.

Forbidden:

- install/update/repair/rollback/uninstall apply;
- release publication;
- Git tags;
- GitHub Releases;
- upload;
- network calls;
- provider/model calls;
- target repository mutation;
- branch/worktree automation;
- Workbench or MCP runtime;
- preview/apply/rollback for source changes;
- promotion.
