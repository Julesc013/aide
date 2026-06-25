# AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01

Create and process `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01`.

Repo truth outranks this prompt. Read:

- `AGENTS.md`
- `.aide/queue/README.md`
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- `.aide/queue/AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01/**`
- `.aide/reports/distribution-update-protocol-v1-plan/**`
- existing Q43-Q48 lifecycle and release artifacts
- `PLANS.md`
- `IMPLEMENT.md`

Goal:

Build `DistributionManifest v1` as the first v1 distribution/update protocol
object. It must reconcile with existing Q47 local release-bundle metadata and
Q48 release-draft boundaries. It must not replace Q43-Q48 or claim public
release readiness.

Requirements:

- add a Draft 2020-12 schema for `DistributionManifest v1`;
- add deterministic helper/projection/validation behavior;
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
- Git tag creation;
- GitHub Release creation;
- upload;
- network calls;
- provider/model calls;
- target repository mutation;
- branch/worktree automation;
- Workbench or MCP runtime;
- source-change preview/apply/rollback;
- promotion.
