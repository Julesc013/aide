# Q41 Tool Classification Report

Latest classification: `.aide/tools/latest-tool-classification.json`

## Fate Summary

- keep: 2
- wrap: 182
- unknown: 16

`drop_candidate` remains a candidate-only fate and is not deletion approval.
`wrap` is a future plan, not active execution.

## Capability Summary

Capability families are deterministic hints. They are not proof that a tool has
been executed or absorbed.

- validate/test capability hints dominate the inventory because AIDE has many
  queue evidence, test, and validation surfaces.
- release capability hints are treated as elevated risk and remain advisory.
- unknown candidates remain preserved and require future review.

## Caveats

- Classification is heuristic and local.
- Q41 does not semantically inspect tool behavior beyond deterministic path,
  name, extension, shebang, and reference signals.
- Future target repos must generate their own inventories and classifications.
