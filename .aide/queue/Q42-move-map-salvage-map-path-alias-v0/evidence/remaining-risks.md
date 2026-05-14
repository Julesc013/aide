# Remaining Risks

- Q42 is candidate-only and no-apply. It does not approve real migration.
- No target-local Dominium or Eureka maps were generated; target repos must
  regenerate their own maps from their own state.
- Move-map generation is intentionally sparse until a future reviewed task
  selects a concrete root or migration target.
- Salvage and reference rewrite candidates are heuristic and require review.
- No aliases, shims, reference rewrites, moves, deletes, or migrations were
  applied.
- `drop_candidate` remains a review candidate and is not deletion approval.
- Export pack provenance is `DIRTY_SOURCE_RECORDED`, which is expected for a
  pack generated from the in-progress Q42 source tree before the final commit.
- Harness validate/doctor/self-check still report the pre-existing stale
  `.aide/generated/manifest.yaml` source fingerprint warning.
- Q37 repo validation still reports existing unknown file classification
  warnings.
- `core/gateway/tests` discovery timed out twice; Q42 did not modify gateway
  code, but the timeout remains a validation gap to investigate separately.
- Q43 Install Plan Model v0 is needed before install/repair/upgrade/rollback
  phases can consume map and alias planning safely.
