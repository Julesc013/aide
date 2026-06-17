# Remaining Risks

## Risks

- `.aide/reports` is the highest clutter risk, but the inventory found enough
  hardcoded flat path assumptions that a rewrite should not happen without a
  report index, no-apply reference map, and compatibility plan.
- `core/runtime`, `core/sdk`, and `core/control` are present as tiny stubs even
  though runtime and SDK behavior remain deferred.
- `.aide/tmp` contains tracked fixture-like files and should be reviewed before
  any naming cleanup.
- `.aide/tools`, `.aide/tests`, and `.aide/examples` exist inside `.aide`, while
  top-level `tools`, `tests`, and `examples` remain add-only candidates.
- `evals` and `scripts` are duplicated as top-level roots and `.aide`
  subtrees; this may be correct but needs explicit authority language before
  movement.
- No design acceptance has occurred, so no implementation prompt for
  rationalization was created.

## Recommended Next Gate

`AIDE-CHECK-REPO-LAYOUT-INVENTORY-01`
