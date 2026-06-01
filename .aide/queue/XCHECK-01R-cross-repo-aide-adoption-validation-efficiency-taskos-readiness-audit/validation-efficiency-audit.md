# Validation Efficiency Audit

## AIDE

- Normal commands: `py -3 .aide/scripts/aide_lite.py validate`, `test`, `selftest`; `scripts/aide validate`.
- Promotion/checkpoint commands: `eval run`, `pack-status`, release/install/repair/upgrade/rollback/uninstall validators, `commit check`.
- Longest known command: raw `.aide/scripts/tests` discovery passed in about 9 minutes in QFIX-07.
- Tier model: no canonical `.aide/policies/test-tiers.yaml`.
- Impacted-test model: missing.
- Timing summary model: missing.
- Immediate action: `X-TEST-00`.
- Blocks normal X-series: yes, for automation/product waves beyond the tier work.

## Dominium

- Normal target evidence now includes fast/strict tier documents and `tests/validation_tiers.json`.
- Full-suite issue: full CTest remains full-gate/T4 debt in reports; product boot was blocked by RepoX readiness evidence in POST-CONVERGE-11/12.
- Timing/sharding: target has timing/sharding docs and `.dominium.local` timing sample references.
- Immediate action: `X-TEST-03` after AIDE source tier model.
- Blocks normal X-series: yes for Dominium product boot/projection work.

## Eureka

- Normal target evidence includes many targeted fixture/runtime tests and reports.
- Full-suite issue: Q58 reported `eval run` WARN/FAIL; later `eureka-repo-health.md` reports full unittest discovery pass with 4944 tests, but current `dev`/`main` divergence means this must be re-baselined target-locally.
- Tier model: no evidence of AIDE-compatible T0/T1/T2/T3 tier contract.
- Impacted-test model: lane tests exist, but no cross-repo canonical impacted-test selection.
- Immediate action: `X-TEST-01` after AIDE source tier model.
- Blocks normal X-series: yes for more Eureka product expansion.

## Summary Table

| Repo | Tier state | Full-suite issue | Immediate next | Blocking? |
|---|---|---|---|---|
| AIDE | missing canonical tiers | long raw discovery, no telemetry schema | `X-TEST-00` | yes for normal X-series |
| Dominium | target-local partial/advanced | full CTest/RepoX/product boot debt | `X-TEST-03` | yes for Dominium product work |
| Eureka | target-local partial | full/eval evidence changed across branches | `X-TEST-01` | yes for Eureka product expansion |
