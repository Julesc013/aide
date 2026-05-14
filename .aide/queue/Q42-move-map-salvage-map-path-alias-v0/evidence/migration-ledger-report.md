# Migration Ledger Report

## Policy And Schemas

- Policy: `.aide/policies/migration-ledger.yaml`
- Ledger schema: `.aide/refactors/migration-ledger.schema.json`
- Entry schema: `.aide/refactors/migration-ledger-entry.schema.json`

Q42 defines ledger event types for `plan_created`, `map_generated`,
`alias_proposed`, `reference_rewrite_proposed`, and future apply/rollback/alias
retirement phases. Q42 may write draft/example events only.

## Current Draft

- Draft ledger: `.aide/refactors/migration-ledger.draft.jsonl`
- Status: draft-only
- Event count: 4

The draft records the current candidate map bundle as planning evidence. It is
not an append-only live migration ledger and contains no future apply or
rollback event.

## Future Use

Future apply-capable phases must append reviewed migration events, evidence
refs, validation refs, and rollback refs. Q42 only establishes the format and
draft planning records.
