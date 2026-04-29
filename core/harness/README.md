# Core Harness

## Purpose

Harness is the executable repo machinery for deterministic checks and evidence capture around AIDE Core.

Q04 implements Harness v0 as a small local command surface over the Q03 `.aide/` Profile/Contract. It is intentionally structural: it checks required files, directories, queue packets, source-of-truth references, and simple text anchors without claiming full YAML or schema validation.

## Command Surface

The repo-root entrypoint is `scripts/aide`.

Implemented v0 commands:

- `aide init`: reports initialization posture and refuses to overwrite an existing `.aide/` contract.
- `aide import`: reports importable guidance surfaces without rewriting canonical records.
- `aide compile`: prints a deterministic compile plan only; generated artifacts remain Q05.
- `aide validate`: performs structural Profile/Contract and queue checks and returns nonzero on hard errors.
- `aide doctor`: prints actionable diagnostics and next repair steps.
- `aide migrate`: reports no-op baseline migration posture; real compatibility work remains Q06.
- `aide bakeoff`: reports eval metadata readiness without provider, model, native-host, browser, network, or external tool calls.

## Boundary

Harness v0 is not Runtime, generated artifacts, Compatibility baseline, Dominium Bridge, provider integration, host implementation, app surface, release automation, or autonomous worker execution.

Existing shared tests, fixtures, eval records, host proofs, and queue helpers remain in their bootstrap-era locations until a later reviewed migration exists.

Q04 does not mutate final `.aide/` contract catalogs. Some Q03 records still describe Harness as planned or not implemented; the v0 Harness reports that as a warning and leaves contract refresh to a later review-gated task.
