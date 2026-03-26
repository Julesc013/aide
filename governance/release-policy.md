# AIDE Release Policy

## Current Phase

This repository is currently pre-bootstrap and pre-product. Early outputs are architectural and governance-focused rather than implementation-focused.

## Phase Gate

- Implementation prompts should not begin until governance, inventory, and harness prompts are completed and reviewed.
- Host adapter work, shared-core work, packaging, CI, and environment systems should remain deferred until those gates are satisfied.
- Early repository changes should strengthen law, inventory structure, and execution discipline before feature work begins.

## Release Naming Rule

- Release artifacts may contain exact version names, release channels, or target identifiers when that makes the deliverable precise.
- This does not change the source naming law: source directories remain based on compatibility technology or host contract rather than exact versions.

## Planned Phase Order

Future phases are expected to populate the repository in this order:

1. inventory
2. matrix
3. scaffold
4. harness
5. shared core
6. adapters
7. environments
8. evals
9. packaging

## Governance Rule

- Governance and release policy are binding during this phase.
- No release artifact should imply broad compatibility before inventory, matrices, evals, and packaging evidence exist.
- Current outputs should be treated as constitutional inputs for later engineering work rather than as product releases.
