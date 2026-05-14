# Q39 Refactor Control Plane Report

## Summary

Q39 adds a deterministic, local, dry-run-only Refactor Control Plane. It gives
future structural work a common planning model before any move, delete,
reference rewrite, migration, root recycling, tool absorption, install, upgrade,
rollback, or release phase is allowed to apply changes.

## Policies

- `.aide/policies/refactor.yaml`: active Q39 no-apply refactor policy with
  refactor classes, fate vocabulary, planning inputs, output artifacts, and
  non-goals.
- `.aide/policies/migration.yaml`: observe/plan/dry_run/review/future apply
  migration stages and states.
- `.aide/policies/refactor-safety.yaml`: forbidden-by-default operations and
  future apply prerequisites.
- `.aide/policies/refactor-evidence.yaml`: evidence requirements for future
  refactor WorkUnits.
- `.aide/policies/refactor-application.yaml`: explicit statement that Q39 has
  no apply command and future apply needs a separate reviewed queue item.

## Commands

- `refactor status`: reports policy/schema readiness, Q37/Q38 input presence,
  and no-apply mode.
- `refactor plan`: writes latest no-apply readiness artifacts and example plan.
- `refactor validate`: validates policies, schemas, readiness, and no-apply
  constraints.
- `refactor dry-run`: prints planned no-op summary and proves Q39 apply is
  unavailable.
- `refactor schemas`: lists schema presence.
- `refactor ledger`: reports migration-ledger example/readiness status.

## Generated Readiness Artifacts

- `.aide/refactors/latest-refactor-readiness.json`
- `.aide/refactors/latest-refactor-readiness.md`
- `.aide/refactors/latest-refactor-plan.example.json`
- `.aide/refactors/latest-refactor-plan.example.md`
- `.aide/refactors/migration-ledger.example.jsonl`

The artifacts reference Q37/Q38 inputs by path and identify Q40 Root Recycling
Framework v0 as the next phase. They contain no actual file moves, deletion
instructions, target mutations, or reference rewrites.

## No-Apply Guarantee

Q39 records:

- `no_apply: true`
- `apply_available_in_q39: false`
- `file_moves: false`
- `file_deletes: false`
- `reference_rewrites: false`
- provider/model calls: none
- network calls: none

`drop_candidate` is candidate language only and is not deletion approval.
