# Repository Audit Checklist

Use this checklist when reviewing the repository after a substantial phase or before promoting major new work.

## Root Docs Coherence

- [ ] `README.md` matches the current phase and implementation reality
- [ ] `CONTRIBUTING.md` still matches actual repo structure and contributor expectations
- [ ] `ROADMAP.md` distinguishes completed, near-term, medium-term, and long-horizon work
- [ ] `MAINTENANCE.md` still reflects what is manual and what is a future automation candidate
- [ ] `DOCUMENTATION.md` indexes the current authoritative set

## Governance Consistency

- [ ] no new doc or manifest contradicts naming, support, capability, or release policy
- [ ] no source directory name encodes exact versions or vague eras

## Inventory And Matrix Consistency

- [ ] ids referenced in matrices and manifests still exist in inventory
- [ ] support, capability, feature, and test posture still align with actual lane evidence
- [ ] candidate families remain distinct from committed families

## Shared Versus Host Boundary Drift

- [ ] shared-core logic still lives under `shared/`
- [ ] host-specific glue has not leaked into shared modules
- [ ] lane-local wrappers remain thin

## Host-Lane Doc Freshness

- [ ] lane READMEs still describe the current proof posture
- [ ] blocked or deferred native lanes remain explicit
- [ ] run records exist for recent implementation waves

## Environment And Lab Honesty

- [ ] acquisition, bootability, blocker, and provenance posture remain explicit
- [ ] labs still contain experimental or blocked work that has not yet been promoted

## Eval And Report Freshness

- [ ] eval catalogs still match current verification posture
- [ ] run records cover the latest implementation waves
- [ ] audit reports do not overstate support or release maturity

## Deferred And Blocked Explicitness

- [ ] blocked items are still recorded where the repo depends on them
- [ ] deferred items remain distinguished from blocked items
- [ ] unknown or unverified areas are not silently rewritten as complete
