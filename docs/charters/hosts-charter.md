# AIDE Hosts Charter

## Purpose

AIDE Hosts are IDE or tool-host shells that present, invoke, or adapt AIDE Core semantics for a specific host family or compatibility technology.

## Owned Responsibilities

- Keep host-specific UI, packaging, environment, and adapter facts local to the host lane.
- Report capability and blocker posture honestly through Compatibility records.
- Use AIDE Core contracts instead of defining durable semantics in host code.
- Preserve existing bootstrap-era Microsoft, Apple, and CodeWarrior proof records.

## Non-goals

- Hosts do not own durable AIDE semantics.
- Hosts do not define the Core contract.
- Q01 does not build, refactor, move, or extend any host implementation.

## Boundaries

- Host lanes may be runnable, degraded, blocked, or candidate depending on evidence.
- Existing `hosts/**` content is mapped, not moved, by Q01.
- Future IDE Hosts remain deferred until queue evidence and review approval support them.

## Relation To AIDE Core / Hosts / Bridges

AIDE Hosts are one public leg of the model. They consume AIDE Core semantics and may use AIDE Bridges where a bridge is the right proof boundary.

## Current Status

Current status: partial. Bootstrap-era host-lane proof records exist, but Q01 performs documentation architecture only and does not implement new host work.
