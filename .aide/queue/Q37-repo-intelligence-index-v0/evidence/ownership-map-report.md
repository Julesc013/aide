# Q37 Ownership Map Report

## Ownership Heuristics

Ownership is path-based and deterministic.

- `.aide/**` maps to AIDE control-plane owners by subsystem.
- `core/harness/**` maps to AIDE harness.
- `core/compat/**` maps to compatibility baseline.
- `core/gateway/**` maps to gateway skeleton.
- `core/providers/**` maps to provider metadata and contracts.
- `scripts/aide` maps to harness entrypoint.
- `docs/reference/**` maps to documentation reference.
- Unknown roots remain `unknown`.

## Owner Summary

- AIDE self-hosting queue: 484
- AIDE cross-repo export pack: 250
- unknown: 277
- AIDE evals: 102
- AIDE control plane: 93
- host adapters: 68
- documentation reference: 47
- AIDE governance: 34
- AIDE Lite: 22
- AIDE repo intelligence: 21

## Limitations

The ownership map is not a permissions system and does not prove semantic
ownership. It is a routing aid for future WorkUnits so they know which policies,
docs, and tests to inspect before acting.
