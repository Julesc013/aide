# Imported design chapters: status and source identities

## What is present

The earlier unified package's 40 design chapters now have a place in this
specification family: six existing adopted contracts are preserved without
editing their bytes, and the remaining 34 chapters are imported as explicit
drafts in their intended topic directories. No parallel `specs/v1/`, archive
root, or second master specification is introduced.

Importing a draft makes the actual design text available to readers and future
implementation planning. It does not adopt all its proposed requirements,
change existing schemas, grant execution authority, or certify implementation.
The inline `UR-*` and `UC-*` identifiers are source aliases. The live `AIDE-*`
foundation contracts remain the reviewed reference where scopes overlap.

## Source identity

Source archive SHA-256:

```
61236cb58baa1233c2d110b3d13a4c8a10f83362b58cc3f6bb6595c8f1aa179c
```

The [import manifest](import-manifest.json) gives the exact archive-member path,
ordinal, source-member SHA-256, output SHA-256 and disposition. It accounts for
all 54 files in the original `specs/control-plane/` subtree. Archive-member
ordinals are zero-based positions in the original ZIP central directory.

The only changes to the 34 imported source chapters are an explicit draft
notice after the title and replacement of links to withheld bulk registers.
Their original proposed requirements, rationale, acceptance designs, and source
attribution are otherwise retained. Original generator timestamps describe
source generation, not import time or fresh operational observations.

## Already adopted: preserve these versions

- [contracts/authority-and-decision-provenance.md](contracts/authority-and-decision-provenance.md)
- [contracts/capability-invocation-and-effects.md](contracts/capability-invocation-and-effects.md)
- [contracts/identity-references-and-digests.md](contracts/identity-references-and-digests.md)
- [contracts/status-and-outcome-dimensions.md](contracts/status-and-outcome-dimensions.md)
- [contracts/work-attempts-and-decomposition.md](contracts/work-attempts-and-decomposition.md)
- [product/scope-and-profiles.md](product/scope-and-profiles.md)

The earlier candidate versions of these six files remain in external source
custody. Preservation of the live adaptations is not a claim that every clause
of their longer candidate predecessors has been reconciled.

## Draft chapters copied into this tree

| Chapter | Proposed requirement aliases | Unrun acceptance designs |
|---|---|---|
| [Compatibility and migration](contracts/compatibility-and-migrations.md) | 7 | 7 |
| [Execution hosts, harnesses and session bindings](contracts/execution-hosts-and-workers.md) | 7 | 7 |
| [Trust, policy, grants and revocation](contracts/trust-policy-and-grants.md) | 7 | 7 |
| [Documentation, editorial intent and knowledge truth](engineering/documentation-and-editorial-contracts.md) | 9 | 9 |
| [Languages, builds and toolchain profiles](engineering/languages-builds-and-toolchains.md) | 7 | 7 |
| [Implementation boundaries and modularity](engineering/module-and-implementation-boundaries.md) | 7 | 7 |
| [Performance, efficiency and resource planning](engineering/performance-and-resource-planning.md) | 6 | 6 |
| [Security, privacy and isolation qualification](engineering/security-privacy-and-isolation.md) | 8 | 8 |
| [Self-hosting, planning and code adoption](engineering/self-hosting-and-governance.md) | 7 | 7 |
| [Test jobs, reusable test assets and selective validation](engineering/test-broker-and-reusable-tests.md) | 7 | 7 |
| [Verification, proof claims and evidence](engineering/verification-and-evidence.md) | 8 | 8 |
| [Operator experience, Workbench and accessibility](experience/operator-workbench-and-accessibility.md) | 7 | 7 |
| [Workflows, operating profiles and configuration](experience/workflows-and-operating-profiles.md) | 6 | 6 |
| [Domain bridges and portfolio integration](interop/domain-bridges-and-portfolio.md) | 7 | 7 |
| [Extension packages, roles and SDKs](interop/extensions-packages-and-sdk.md) | 7 | 7 |
| [Native hosts, legacy relays and offline mailboxes](interop/native-and-legacy-hosts.md) | 7 | 7 |
| [Standards profiles and loss-aware translation](interop/standards-and-translation.md) | 7 | 7 |
| [After-action reviews and improvement effectiveness](knowledge/after-action-learning.md) | 6 | 6 |
| [Context compilation and handoffs](knowledge/context-compilation.md) | 7 | 7 |
| [OKF engineering profile and document codec](knowledge/okf-engineering-profile.md) | 8 | 8 |
| [ProjectGraph, provenance and impact](knowledge/project-graph-and-impact.md) | 7 | 7 |
| [Structure, naming, purpose and safe reuse](knowledge/structure-purpose-and-reuse.md) | 7 | 7 |
| [Work-product conservation and harvest](knowledge/work-product-conservation.md) | 7 | 7 |
| [Brownfield adoption and ownership](lifecycle/brownfield-adoption-and-ownership.md) | 7 | 7 |
| [Install, update, repair, rollback and removal](lifecycle/install-update-repair-removal.md) | 8 | 8 |
| [Releases, support and backports](lifecycle/releases-support-and-backports.md) | 8 | 8 |
| [Workspace estate, storage and retirement](lifecycle/workspaces-storage-and-retention.md) | 6 | 6 |
| [Cache classes, validity and evidence reuse](optimization/cache-and-evidence-reuse.md) | 7 | 7 |
| [Model, effort and execution-recipe routing](optimization/model-effort-and-delegation.md) | 8 | 8 |
| [Usage, aggregate budgets and accepted-outcome cost](optimization/usage-budgets-and-economics.md) | 8 | 8 |
| [Local durability, events and artifact storage](runtime/durability-and-storage.md) | 7 | 7 |
| [Integration broker and authoritative closeout](runtime/integration-broker-and-closeout.md) | 8 | 8 |
| [Recovery, cancellation and uncertain effects](runtime/recovery-and-uncertain-effects.md) | 7 | 7 |
| [Supervision, durable controls and continuity](runtime/supervision-and-continuity.md) | 7 | 7 |

The imported chapters contain 244 proposed requirement statements and
244 acceptance designs. These counts describe text, not completed work;
none of those behavioral cases was executed by the import.

## What stays outside specs

Private ZIPs, recovery snapshots, queue evidence, old patches, R3 audit JSON,
the inaccurate historical semantic crosswalk, duplicate generated register
views, and old baseline/delivery-roadmap pages are not copied into this tree.
The Convergence Action Pack's full custody map remains an external review input.

The original unifier's IDs and source attributions have not been independently
ratified clause by clause. Read the prose; do not install the old bulk registers
as machine policy. Current implementation status and queue ordering must be
read from the live repository, not inferred from dated draft paragraphs.

## Next semantic step

Review and adapt related draft clauses in normal bounded increments. Retain
source aliases, record disagreements and supersession scope, and assign live
requirement IDs only through the existing adoption process. File import need
not wait for broker activation, archive cleanup, native UI planning, or a
complete behavioral test campaign. Those are different operations.

This import does not authorize deleting archive duplicates, changing Codex
configuration, merging the active broker branch, or publishing a release.
