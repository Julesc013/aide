# Existing Tool Absorption

## Rule

AIDE must not replace existing repo-management systems by deletion. It must use:

`discover -> classify -> wrap -> adapt -> migrate -> retire with evidence`.

Retirement is last, optional, and review-gated. It requires an ownership ledger,
compatibility proof, migration map, rollback route, and target approval.

## Generic Absorption Records Needed

- Tool id and target repo.
- Current entrypoints.
- Current outputs.
- Current authority level.
- Dependencies and local state.
- Source-of-truth status.
- Whether the tool is live, transitional, historical, generated, or obsolete.
- AIDE wrapper command.
- Evidence packet mapping.
- Retirement conditions, if any.

## Target Systems

| System | Target | Preserve | Wrap | Migrate | Retire |
|---|---|---:|---:|---:|---:|
| XStack | Dominium | yes | yes | later | only with evidence |
| AuditX | Dominium | yes | yes | later | only with evidence |
| RepoX | Dominium | yes | yes | later | only with evidence |
| TestX | Dominium | yes | yes | later | only with evidence |
| XStack FAST/STRICT/FULL profiles | Dominium | yes | yes | no now | no |
| Eureka architecture boundary check | Eureka | yes | yes | maybe | no now |
| Eureka WorkUnit seed/review docs | Eureka | yes | classify | later | no now |
| Command matrices | both | yes | yes | later | only with evidence |
| Root inventories | both | yes | yes | later | no now |
| Old task catalogs | both | yes | map | later | only with evidence |

## First AIDE Action

Q41 should create an existing-tool absorption registry and wrappers. It should
not change target tools. It should read target docs and commands, produce an
inventory, classify authority, and map each tool to AIDE validation/evidence
surfaces.

## Non-Goals

- No root moves.
- No XStack extraction.
- No deletion.
- No renaming.
- No live target command execution without a target-reviewed queue item.
- No doctrine rewrite.
