# Q42 ExecPlan: Move Map / Salvage Map / Path Alias v0

## Objective

Create deterministic candidate map infrastructure for future structural
migration planning without applying moves, deletions, aliases, shims, or
reference rewrites.

## Scope

- Add Q42 policies for move maps, salvage maps, path aliases, reference rewrite
  plans, and migration ledger drafts.
- Add or extend `.aide/refactors` schemas for map entries and validation
  reports.
- Extend AIDE Lite with `refactor map`, `move-map`, `salvage-map`, `aliases`,
  `rewrite-plan`, `validate-map`, and `map-status`.
- Generate current AIDE-local candidate map artifacts as evidence only.
- Add tests, golden tasks, documentation, export-pack support, and evidence.

## Boundaries

- No file moves.
- No file deletes.
- No reference rewrites.
- No alias or shim application.
- No target repo mutation.
- No branch mutation.
- No provider, model, or network calls.

## Milestones

1. Completed: queue packet and dependency metadata repair.
2. Completed: policies and schemas.
3. Completed: AIDE Lite command implementation and generated candidate outputs.
4. Completed: unit tests and golden tasks.
5. Completed: documentation and export-pack sync.
6. Completed with notes: final validation and review-gated evidence.

## Verification Intent

Run the Q42 refactor map commands, AIDE Lite validation/test/eval surfaces,
export-pack and pack-status, targeted unit tests, diff checks, commit checks,
core unittest suites where present, and secret scan. Record any residual
pre-existing warnings or timeouts honestly.

## Exit Criteria

Q42 status is `needs_review`, candidate map artifacts exist and validate,
`apply_allowed` remains false, `drop_candidate` is not deletion approval,
source-generated current maps are excluded from target-truth export, evidence is
complete, and no forbidden mutation occurs.

## Validation Notes

- Q42 command validation passed for `refactor map`, `move-map`,
  `salvage-map`, `aliases`, `rewrite-plan`, `validate-map`, and `map-status`.
- Full golden task evaluation passed: 85 tasks, 85 pass, 0 warn, 0 fail.
- Export pack and pack-status passed with `source_repo_current_map_outputs`
  excluded from portable target truth.
- Harness validate/doctor retained a pre-existing stale generated-manifest
  warning.
- `core/gateway/tests` discovery timed out twice; Q42 did not touch gateway
  source and records the timeout as residual validation risk.
