# ExecPlan: Distribution Fixture Portability Integration

## Objective

Turn the published source-only portability candidate into a complete-checkout,
Windows-tested, independently reviewed integration candidate and land it on
`dev` only when its exact combined tree passes.

## Scope

- Preserve `e73ac0b269df3a47214588ae2d025d1b97f2f2c7` through a two-parent merge.
- Recheck behavior against current `dev` rather than its older source base.
- Verify portable names, aliases, links, snapshot consistency, preflight,
  rollback-input validation, and add-file non-overwrite behavior.
- Refresh generated portable artifacts only if canonical validation proves the
  combined source changed an owned export input.

## Non-Goals

- Real-target apply, hostile concurrent-writer confinement, or crash-atomic
  production rollback.
- Main promotion, tag creation, release publication, or fleet rollout.
- Broker, isolated-host, GitHub target-policy, or `.codex` changes.

## Dependencies

- `dev@c6fdc754844cf7d42302218ce08307a7e05dcb61`.
- Published source candidate `e73ac0b269df3a47214588ae2d025d1b97f2f2c7`.
- Completed delivered-pack safe-update behavior already integrated into `dev`.

## Progress

- [x] Inspect exact source history, message conformance, diff, and retained limits.
- [x] Create an isolated current-dev task branch and admit this WorkUnit.
- [x] Merge the exact source candidate with both parents preserved.
- [x] Run focused and adjacent Windows tests against the combined tree.
- [x] Run canonical validation and classify generated-artifact drift.
- [x] Record exact source, test, and boundary evidence.
- [x] Preserve the first independent `REQUEST_CHANGES` review and repair its
  reproduced Windows 8.3 alias mutation with an actual short-name regression.
- [x] Obtain independent exact-commit review.
- [x] Publish the qualified task ref at `6cb0a9ac8856a4e733b1d48ef2a86d50badb5d22`.
- [x] Prepare, validate, integrate, and observe the exact `dev` candidate at
  `bb689227c6a65292f4728d7ae0f8759c22e77bd3`.
- [ ] Refresh and validate commit-bound portable artifact provenance from the
  landed `dev` source.

## Test Oracle

All path and fixture inputs must be fully rejected before payload mutation when
they are nonportable, aliased, linked, special, stale, destructive, or already
owned by another file. Valid disposable fixture behavior must remain compatible
with existing distribution and delivered-pack lifecycle tests.

## Recovery

The source branch and commit remain immutable. The integration branch can be
recreated from exact `dev` plus the source merge. Tests use disposable temporary
directories. Shared history is never rewritten.

## Exit Criteria

The exact combined candidate is clean, pushed, independently reviewed, and
passes focused, adjacent, canonical, provenance, and commit-range checks. Dev
integration must preserve both histories and pass post-merge validation.
