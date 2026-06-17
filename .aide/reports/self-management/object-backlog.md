# Self-Management Object Backlog

All objects in this backlog should start report-only unless a later reviewed
queue item authorizes stronger behavior.

## Priority 1

### RootAuthorityManifest

Answers what belongs where.

Initial outputs:

- `.aide/protocol/aide-root-authority-manifest.schema.json`
- `.aide/roots/root-authority/**`
- `.aide/reports/root-authority-status.md`

Boundary: no file moves.

### RepoLayoutInventory

Formalizes the current report-only layout inventory shape.

Initial outputs:

- `.aide/reports/repo-layout/inventory.*`
- `.aide/reports/repo-layout/authority-overlaps.md`

Boundary: no rationalization apply.

## Priority 2

### DocTruthFinding

Records stale README, DOCUMENTATION, roadmap, OKF, queue, and protocol claims.

### KnowledgeDriftFinding

Records OKF stale pages, missing backlinks, source-ref gaps, and evidence-ref
gaps.

### GeneratedOutputRecord

Records generator, source refs, stale status, canonicality, regeneration
command, and validation status for generated outputs.

### QueueHealthFinding

Records review-gate debt, blocked task state, latest-task drift, duplicate task
risks, and missing evidence surfaces.

## Priority 3

### FileAuthorityRecord

Classifies path-level source, evidence, report, generated, fixture, example,
policy, schema, local-state, and runtime-state authority.

### ReviewGateDebtRecord

Models why a task is still review-gated and what evidence is required to close
it.

### StructureTransaction

Future apply object for tiny reviewed self-mutations. Must depend on accepted
authority manifests, no-apply maps, validation plans, rollback notes, and human
review.

### ReferenceRewritePlan

No-apply record for references that would need edits before movement.

### PathAliasRecord

No-apply compatibility record for old paths that may need temporary aliases or
shims.

### MigrationLedgerEntry

Evidence record for future applied structural changes.

### ArchiveFateRecord

Review-gated fate record for retired, superseded, or quarantined material.
