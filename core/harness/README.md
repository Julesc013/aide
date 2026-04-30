# Core Harness

## Purpose

Harness is the executable repo machinery for deterministic checks and evidence capture around AIDE Core.

Q04 implements Harness v0 as a small local command surface over the Q03 `.aide/` Profile/Contract. It is intentionally structural: it checks required files, directories, queue packets, source-of-truth references, and simple text anchors without claiming full YAML or schema validation.

## Command Surface

The repo-root entrypoint is `scripts/aide`.

Implemented v0 commands:

- `aide init`: reports initialization posture and refuses to overwrite an existing `.aide/` contract.
- `aide import`: reports importable guidance surfaces without rewriting canonical records.
- `aide compile`: prints a deterministic generation plan by default, can write preview-only output with `--preview`, and can update the approved Q05 managed sections, preview, and manifest with `--write`.
- `aide validate`: performs structural Profile/Contract, queue, generated-artifact, and compatibility baseline checks and returns nonzero on hard errors.
- `aide doctor`: prints actionable diagnostics and next repair steps.
- `aide migrate`: reports the Q06 Compatibility baseline, known v0 versions, and the `baseline-current-noop` migration registry without mutating files.
- `aide bakeoff`: reports eval metadata readiness without provider, model, native-host, browser, network, or external tool calls.

## Boundary

Harness v0 is not Runtime, Dominium Bridge, provider integration, host implementation, app surface, release automation, or autonomous worker execution.

Existing shared tests, fixtures, eval records, host proofs, and queue helpers remain in their bootstrap-era locations until a later reviewed migration exists.

Q05 adds generated artifact v0 support while preserving the boundary that generated downstream artifacts are not canonical truth. The approved Q05 target set is limited to managed sections in `AGENTS.md` and selected AIDE skills, a preview-only Claude guidance file under `.aide/generated/preview/CLAUDE.md`, and `.aide/generated/manifest.yaml`.

Q06 adds Compatibility baseline checks while preserving the boundary that migrations are non-mutating and current-baseline only.

Q07 adds Dominium Bridge structural checks and compile-plan reporting. Harness validates required bridge files and boundary anchors, and `aide compile` lists future Dominium target classes as metadata only. It does not mutate any Dominium repository or emit real Dominium generated outputs.

Harness v0 still does not implement full YAML or JSON Schema validation, mutating Compatibility migration, Dominium product/runtime behavior, Runtime, host implementation, app surfaces, provider/model calls, browser bridges, release automation, or autonomous worker execution.
