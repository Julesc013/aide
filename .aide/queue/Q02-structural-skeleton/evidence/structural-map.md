# Q02 Structural Map Evidence

## Summary

Q02 introduced target skeletons and a structural migration map while preserving current physical locations.

## Skeletons

| Skeleton | Purpose | Status |
| --- | --- | --- |
| `core/**` | Target AIDE Core bands for Contract, Harness, Runtime, Compatibility, Control, SDK, and tests. | README-only skeleton |
| `hosts/cli/**` | Future low-friction CLI Host. | README-only skeleton |
| `hosts/service/**` | Future Service Host. | README-only skeleton |
| `hosts/commander/**` | Future Commander Host. | README-only skeleton |
| `hosts/extensions/**` | Future IDE/editor extension host family placeholders. | README-only skeleton |
| `bridges/**` | Target AIDE Bridges skeleton. | README-only skeleton |
| `bridges/dominium/**` | Dominium Bridge and XStack placeholders. | README-only skeleton |

## Preserved Areas

- `shared/**` remains the executable bootstrap-era shared-core implementation.
- `hosts/apple/**`, `hosts/microsoft/**`, `hosts/metrowerks/**`, and `hosts/templates/**` remain bootstrap-era proof and template records.
- `governance/**`, `inventory/**`, `matrices/**`, `research/**`, `environments/**`, `labs/**`, `evals/**`, `packaging/**`, `scripts/**`, `.agents/**`, and `.aide/**` remain in their current locations.

## Reference Map

The authoritative Q02 map is `docs/reference/structural-migration-map.md`. It records current physical location, conceptual home, move status, and notes.
