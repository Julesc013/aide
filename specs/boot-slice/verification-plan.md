# Boot Slice Verification Plan

## Purpose

This plan defines what evidence the first boot slice will eventually need and how it maps onto the existing evaluation vocabulary.

## Universal Evidence

Every lane must eventually produce:

- one recorded entry-point invocation or equivalent companion invocation
- one deterministic boot-slice report artifact or equivalent structured output
- one capability report or equivalent structured availability record
- explicit diagnostics when optional or deferred behavior is unavailable

## Structural Versus Behavioral Checks

### Structural

These checks apply before runnable behavior exists:

- `existence`
- `schema`
- `docs-consistency`

### Behavioral

These checks apply once a lane is runnable:

- `load-smoke` for `boot.slice.invoke`
- `editor-smoke` where lane acceptance requires or optionally exercises `boot.slice.editor-marker`
- `archival-record` for historical or fallback lanes whose evidence depends on preserved environments, provenance, or blocker records

### Deferred For This Slice

These categories are intentionally outside the first boot slice:

- `workspace-smoke`
- `packaging-check`
- `release-shape`

## Lane Evidence Expectations

- `xcodekit` and `vsix-v2-vssdk` need `load-smoke` plus `editor-smoke` to count as full first-wave proofs.
- `com-addin`, `vsix-v1`, `extensibility`, `monodevelop-addin`, and `ide-sdk` can reach accepted first-wave completion through `load-smoke` plus explicit editor-marker posture.
- `visual-studio-mac/companion`, `xcode/companion`, and `codewarrior/companion` need deterministic report output and explicit unavailable or blocked reasons; they do not need native editor proof in the first wave.
- Historical and archival lanes should also carry `archival-record` evidence when the proof depends on preserved or blocked environments.

## Deferred And Blocked Results

- record `deferred` when the lane's richer proof is intentionally postponed but the minimum accepted proof succeeds
- record `blocked` when even the minimum accepted proof cannot be produced honestly
- record `unverifiable` only when the question is meaningful but current evidence or tooling cannot answer it

## Later Evals Growth

Later implementation prompts should extend `evals/` by:

- adding run records under `evals/runs/`
- recording evidence-backed reports under `evals/reports/`
- tightening lane-specific eval definitions once the first implementations exist

Until then, the eval catalog remains a planning surface rather than a pass ledger.
