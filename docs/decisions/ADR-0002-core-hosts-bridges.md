# ADR-0002: Public Model Is Core / Hosts / Bridges

## Status

accepted

## Context

The bootstrap-era repo mixed shared core, host lanes, governance, proofs, and control-plane records. The reboot needs a smaller public model.

## Decision

Use AIDE Core, AIDE Hosts, and AIDE Bridges as the public model.

## Consequences

- AIDE Core owns durable semantics.
- AIDE Hosts are shells and proof lanes.
- AIDE Bridges are bounded connection layers, starting with Dominium Bridge as a planned target.

## Supersedes / Superseded By

Supersedes: none. Superseded by: none.
