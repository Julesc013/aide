# Q36-Q48 Phase Completion Matrix

| Phase | Status | Evidence | Commands | Tests | Exported | Warnings | Downstream-ready |
|---|---|---|---|---|---|---|---|
| Q36 intent compiler | needs_review | present | intent compile/validate/status pass | golden tasks present under intent_compile_* and workunit_* | included | exact legacy golden ID differs from later naming | yes with review gate |
| Q37 repo intelligence | needs_review | present | repo inventory/validate/status pass with warnings | repo map golden tasks present | included | unknown classifications remain advisory | yes with review gate |
| Q38 file quality ledger | needs_review | present | quality ledger/validate/status pass | quality golden tasks present | included | many advisory quality warnings | yes with review gate |
| Q39 refactor control | needs_review | present | refactor status/validate/dry-run pass | refactor golden tasks present | included | no-apply only | yes with review gate |
| Q40 root recycling | needs_review | present | roots inventory/validate/status pass | root recycling golden tasks present | included | unknown/high-risk roots are advisory | yes with review gate |
| Q41 tool absorption | needs_review | present | tools inventory/validate/status pass | tool absorption golden tasks present | included | no execution by default | yes with review gate |
| Q42 move/salvage/path-alias | needs_review | present | refactor map-status/validate-map pass | map golden tasks present | included | no map application | yes with review gate |
| Q43 install model | needs_review | present | observe/plan/dry-run/validate/status pass | install golden tasks present | included | no apply mode | yes with review gate |
| Q44 repair doctor | needs_review | present | observe/diagnose/plan/dry-run/validate/status pass | repair golden tasks present | included | no apply mode | yes with review gate |
| Q45 upgrade model | needs_review | present | observe-source/current, compare, plan, dry-run, validate/status pass | upgrade golden tasks present | included | no apply mode | yes with review gate |
| Q46 rollback/uninstall | needs_review | present | rollback/uninstall observe/plan/dry-run/validate/status pass | rollback/uninstall golden tasks present | included | no apply/removal mode | yes with review gate |
| Q47 release bundle | needs_review | present | release validate/status/assets/manifest/checksums/provenance/clean pass | release bundle golden tasks present | local release support included | local-only; dirty source recorded | yes with review gate |
| Q48 release draft | needs_review | present | draft-validate/status/upload-plan/checklist/publication-boundary pass | release draft golden tasks present | draft support included | unpublished only | yes with review gate |

## Notes

- All listed phases are implemented to filesystem artifacts and stopped at `needs_review`.
- None are marked `passed`; review remains required before public-release claims.
- `.aide/scripts/aide_lite.py eval run` passed 132/132 golden tasks.
- Q49 should consume this as a checkpoint, not as automatic acceptance.
