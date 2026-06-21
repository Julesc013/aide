# Baseline

- AIDE branch: `main`
- AIDE repair commit resolved locally: `30931ba1f17b1bc4d9d2b9b12ef18133831ad8fd`
- Source build: `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01` at `a75635478be155ef7bc2b62de4ead3837212bbb8`
- Source check: `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01` at `692b4b3469e80a67f3f2f98612ec66c86b7394e9`, result `REQUEST_CHANGES`
- Source repair: `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01`, result `PASS_WITH_WARNINGS`
- Pinned Dominium input: `C:/Projects/Dominium/dominium` at `c92b386027890c1bbf14aef6eaafe0357b7b03dd`
- Check scope: independent repair check only; no repair, acceptance, production seam modification, or Dominium mutation.

The check harness treats this task's own queue and report outputs as allowed outputs for the check run. Pre-existing source task evidence was inspected through AIDE task evidence commands and the source-chain assertions in `independent-repair-check.json`.
