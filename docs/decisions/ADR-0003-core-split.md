# ADR-0003: Internal Core Split

## Status

accepted

## Context

AIDE Core needs internal boundaries that support contracts, proof, compatibility honesty, governance, and future extension surfaces without turning every idea into runtime work.

## Decision

Split AIDE Core internally into Contract, Harness, Runtime, Compatibility, Control, and SDK.

## Consequences

- Contract and Harness can advance before Runtime.
- Compatibility becomes a first-class Core domain.
- Control keeps queue, autonomy, evidence, and review-gate policy visible.
- SDK remains future/deferred until earlier evidence exists.

## Supersedes / Superseded By

Supersedes: none. Superseded by: none.
