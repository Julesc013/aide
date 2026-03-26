# Open Blockers Summary

## Host-Lane Blockers

- several Microsoft native lanes still depend on real archival or SDK-capable Visual Studio environments
- the Apple `xcodekit` lane still depends on macOS, Xcode tooling, and an honest embedded interop path
- the CodeWarrior archival-native lane still lacks a reproducible historical environment for in-host SDK or COM proof

## Environment And Lab Blockers

- historical environments, toolchains, and acquisition provenance are still mostly framework-level rather than fully populated
- archival environment reconstruction remains a gating cost for deeper native proofs

## Packaging And Release Blockers

- packaging posture is documented, but real manifest maturity, signing or notarization evidence, and release records remain limited
- the repo is not yet at broad release-readiness

## Shared-Core And Verification Boundaries

- the shared-core boot slice is intentionally narrow and does not yet cover richer execution modes or deeper workspace-aware behavior
- current verification is strongest at structural and smoke levels; broader workflow evidence remains future work

## Interpretation Rule

These blockers are explicit repository-state facts, not reasons to flatten or hide incomplete areas. They define what later phases must resolve before stronger support or release claims are honest.
