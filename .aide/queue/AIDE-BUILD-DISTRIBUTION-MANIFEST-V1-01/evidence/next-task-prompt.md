# Next Task Prompt

```text
Create and process AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01.

Repo truth outranks this prompt. Independently check
AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01, its task packet, implementation diff,
schema, helper, fixtures, AIDE Lite commands, generated reports, and evidence.

This is a check-only task. Do not repair implementation.

Verify DistributionManifest v1 is a deterministic distribution identity and
artifact inventory over existing Q47 local release-bundle evidence; Q48 release
draft material remains publication-review evidence only; digest
canonicalization is stable; component and artifact inventories are complete;
duplicate IDs fail; source-kind, protocol, required-feature, migration,
forbidden-member, digest, checksum, signature, and SBOM boundaries fail closed;
valid and invalid fixture coverage is complete; no target ownership is encoded;
no install/update/repair/rollback/uninstall apply, release publication, tags,
GitHub Releases, uploads, target mutation, branch/worktree automation, network,
provider/model calls, Workbench/MCP runtime, source-change preview/apply/
rollback, or promotion is implemented or claimed.

If material checks pass, recommend exactly:
AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01

If material defects remain, recommend exactly:
AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01

Stop at needs_review.
```
