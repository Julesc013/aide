# Refactor and Root Recycling Plan

## Q39 Refactor Policy And Migration Ledger v0

Define when AIDE may propose refactors, migrations, aliases, shims, and
deprecations. Require dry-run, compatibility notes, rollback notes, and review.

## Q40 Root Inventory And Recycling Plan v0

Inventory root directories, classify authority, identify stale or transitional
roots, and propose recycling candidates without moving anything.

## Q41 Existing Tool Absorption Registry v0

Create a registry for XStack, AuditX, RepoX, TestX, Eureka validators, command
matrices, root inventories, and old task catalogs. Produce wrappers and
evidence mappings, not replacements.

## Q42 Dry-Run Move / Salvage / Alias Planner v0

Generate move maps, salvage maps, path aliases, import compatibility notes, and
rollback plans. Application remains disabled unless a future reviewed task
authorizes a bounded migration.

## Required Schemas

- `aide.refactor-policy.v0`
- `aide.migration-ledger.v0`
- `aide.root-inventory.v0`
- `aide.tool-absorption-registry.v0`
- `aide.move-map.v0`
- `aide.salvage-map.v0`
- `aide.path-aliases.v0`

## Non-Goals

- No physical root moves.
- No deletion.
- No target product changes.
- No broad namespace rewrite.
- No source-control history rewrite.
