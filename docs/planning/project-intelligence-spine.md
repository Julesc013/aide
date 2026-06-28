# Project Intelligence Spine

Status: tentative planning evidence.

Source: June 28, 2026 Project Intelligence handoff, reconciled against live
AIDE queue truth on June 29, 2026.

This document does not accept a capability, change queue order, authorize
implementation, or replace `.aide/queue/` as execution truth.

## Purpose

AIDE should treat repository structure as one projection of a deeper project
graph. The directory tree still matters, but it should not be the only source of
placement, ownership, dependency, documentation, validation, or update truth.

The better target is a self-governing project fabric:

- Every durable file, folder, generated artifact, report, evidence packet, and
  installed path has declared authority, ownership, lifecycle, provenance, and
  intended consumers.
- Every move, rename, delete, overwrite, regeneration, update, rollback, or
  repair is planned, previewed, validated, evidenced, and reversible.
- Identity remains stable even when paths evolve.
- Compatibility is preserved through aliases, deprecations, overlays, and
  migrations instead of ungoverned breakage.

## Core Principle

AIDE does not prevent all structural evolution. It prevents ungoverned
structural evolution.

The repository tree is a locator layer. Stable project identity should be based
on records such as `aide://resource/<id>`, `ResourceRef`,
`ArtifactReference`, and `ReferenceID`. A path can change. Identity,
provenance, digest evidence, ownership, consumer references, and compatibility
records must remain coherent.

## Project Graph Model

`ProjectGraph` is the broader planning concept. It should eventually compose
the existing and planned graph layers:

- `RepoGraph` for roots, directories, files, file revisions, generated outputs,
  reports, evidence, transactions, owners, and distribution state.
- `CodeGraph` for modules, classes, functions, symbols, imports, calls, types,
  contracts, and usage.
- `DocGraph` for documentation pages, comments, claims, examples, warnings,
  stale claims, and contradictory statements.
- `UsageGraph` for consumers, importers, runtime entry points, package users,
  target overlays, and context-pack consumers.
- `TestGraph` for tests, fixtures, conformance profiles, validation routines,
  and evidence bindings.
- `IssueGraph` for WorkUnits, blockers, findings, repairs, acceptance gates,
  and review decisions.
- `PerformanceGraph` for measurements, complexity observations, hotspots,
  regressions, and optimization evidence.
- `KnowledgeGraph` for observations, claims, decisions, OKF projections, and
  ContextPack selection.
- `ChangeGraph` for transactions, previews, migrations, aliases,
  deprecations, rollback bundles, update plans, and receipts.

`OKF` remains the human and agent explanation layer. It must not replace
machine-queryable graph truth, queue truth, protocol truth, or evidence truth.

## Required Record Families

The first safe wave should reuse existing AIDE records where they already
exist. It should not create a parallel structure system.

Identity and ownership records:

- `RootAuthorityManifest`
- `PathAuthorityRecord`
- `OwnershipLedger`
- `ResourceRef`
- `ArtifactReference`
- `ReferenceID`
- `ProjectCapsule`
- `ProjectLock`

Naming and placement records:

- `NamingPolicy`
- `PathPolicy`
- `RootPlacementRule`
- `FileKindRegistry`
- `PathReservation`
- `DirectoryContract`
- `StructureLintFinding`
- `NameDecision`
- `PathDecision`

Semantic project records:

- `ProjectGraphSnapshot`
- `SymbolRecord`
- `PurposeRecord`
- `ContractRecord`
- `UsageRecord`
- `DocClaimRecord`
- `KnowledgeObservation`
- `KnowledgeClaim`
- `KnowledgeDecision`
- `KnowledgeProjection`

Change and compatibility records:

- `StructureTransaction`
- `CodeStructureTransaction`
- `DocStructureTransaction`
- `ReferenceRewritePlan`
- `PathAliasRecord`
- `DeprecatedPathRecord`
- `MigrationLedgerEntry`
- `ArchiveFateRecord`
- `RollbackBundle`
- `UpdatePlan`
- `UpdateReceipt`

## Lifecycle And Authority

Every path-like project object should eventually have a lifecycle state:

- `proposed`
- `reserved`
- `active`
- `generated`
- `project_owned`
- `vendor_managed`
- `deprecated`
- `aliased`
- `superseded`
- `archived`
- `quarantined`
- `removed_from_distribution`
- `local_only`
- `never_touch`
- `unknown`

Every durable directory should be treated as an API. A directory contract should
describe authority, allowed contents, forbidden contents, ownership model,
generated/source policy, naming policy, consumer expectations, migration
policy, stability tier, and validation rules.

## Documentation And Comment Truth

AIDE should classify documentation and comments as project facts with status,
not as automatic truth.

Planned truth classes:

- `explanatory`
- `contractual`
- `example`
- `warning`
- `generated`
- `stale`
- `contradicted`
- `unsupported`

Doc and code links must be bidirectional. A doc page can document a symbol, a
symbol can be documented by a page, a test can prove a contract, and an
evidence packet can support or reject a claim. Observations must not become
accepted facts without validation or review.

## ProjectGraph-Driven ContextPack

Future ContextPacks should be selected from ProjectGraph facts instead of only
from file proximity or prompt text.

A ProjectGraph-aware ContextPack should include:

- allowed roots and forbidden roots
- likely destination paths
- similar existing files and naming examples
- ownership and generated-output rules
- stable resource ids
- relevant symbols, contracts, usage edges, and tests
- relevant doc claims and stale-warning records
- related WorkUnits, blockers, decisions, and evidence
- performance or complexity observations when relevant
- explicit non-capabilities and review gates

This should prevent many structure mistakes before they are made.

## Validation Direction

The eventual command shape is report-first:

```text
aide structure validate
```

The first versions should be no-apply observers. They can fail or warn when:

- runtime or local-only files are committed as release truth
- generated outputs lack provenance
- source files appear under export or release-output roots
- reports claim canonical truth
- OKF pages claim acceptance without queue evidence
- path names violate naming policy
- file kinds appear under the wrong root authority
- an install or update would overwrite project-owned truth

No validation finding should directly move, delete, rewrite, repair, or apply.

## Roadmap Shape

The Project Intelligence spine should be queued as narrow, review-gated waves:

1. Preserve current executable queue order. Do not displace the MIR input and
   canary follow-up tasks already selected by live queue evidence.
2. Complete the Structure Intelligence planning and projection slice already
   queued by `AIDE-PLAN-ULTIMATE-SYNTHESIS-ROADMAP-01`.
3. Add naming, path reservation, path authority, and directory contract
   planning as a report-only authority wave.
4. Build a `ProjectGraphSnapshot` projection over existing deterministic repo,
   queue, generated-output, report, evidence, ownership, and distribution
   surfaces.
5. Add semantic records for symbols, doc/code claims, purpose, contracts,
   usage, and reuse opportunities.
6. Add health observers for queue, evidence, schema, code structure, doc
   structure, reference usage, naming/placement, complexity, and performance.
7. Make ContextPack selection graph-aware while preserving existing queue and
   evidence authority.
8. Bind ProjectGraph facts into distribution/update safety, shadow previews,
   transactions, aliases, deprecations, rollback bundles, and receipts.
9. Plan Workbench views for human tree, authority, lifecycle, impact, risk,
   and before/after previews.
10. Preserve scale modes from USB/offline AIDE Lite through workstation, LAN,
   enterprise, cloud, and supercomputer deployments without requiring network
   or service readiness for the first slice.

## Non-Authorization

This document does not authorize implementation changes, queue policy changes,
source-truth promotion for generated outputs, file moves, deletes, reference
rewrites, root creation, alias or shim application, install or update apply,
repair apply, rollback apply, target-repo mutation, release generation,
publication, GitHub API calls, branch or worktree automation, provider/model
calls, network calls, live runtime, Workbench product claims, or public release
readiness.
