# AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01 Prompt

Create and process `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01`.

Repository truth outranks this prompt. Use `.aide/queue/index.yaml`,
the accepted distribution/update protocol v1 plan, Q47 release bundle evidence,
Q48 release-draft boundaries, `PLANS.md`, `IMPLEMENT.md`, and task-local
evidence before changing files.

Build `DistributionManifest v1` as the first dependency for distribution and
update protocol v1. It must define distribution identity, release/channel,
component inventory, artifact inventory, protocol compatibility, migrations,
checksums, provenance, SBOM/signature metadata boundaries, deterministic
digests, source contamination refusals, and explicit non-capabilities.

Promote only existing Q47 local bundle evidence into distribution identity.
Treat Q48 GitHub Release drafts as publication-review material only. Do not
implement install/update/repair/rollback/uninstall apply, public release
publication, Git tags, GitHub Releases, uploads, target mutation,
branch/worktree automation, network calls, provider/model calls, Workbench or
MCP runtime, source-change preview/apply/rollback, or promotion.

Stop at `needs_review` and recommend exactly:

```text
AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01
```
