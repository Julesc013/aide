# AIDE Bridges Charter

## Purpose

AIDE Bridges are bounded connection layers between AIDE Core semantics and local proof profiles, host adapters, generated artifacts, companion surfaces, or other constrained execution contexts.

## Owned Responsibilities

- Define bridge-specific proof boundaries.
- Keep local governance profiles visible and scoped.
- Prevent bridges from becoming hidden runtimes or unreviewed host implementations.
- Prepare the Dominium Bridge as the first reboot bridge target.

## Non-goals

- AIDE Bridges do not replace AIDE Core.
- AIDE Bridges do not own durable AIDE semantics.
- Q01 does not implement Dominium Bridge or any bridge runtime.

## Boundaries

- Dominium Bridge is the first planned bridge.
- XStack remains Dominium's strict local governance and proof profile.
- Bridge implementation requires later queue items and review-gated evidence.

## Relation To AIDE Core / Hosts / Bridges

AIDE Bridges are one public leg of the model. They connect AIDE Core to constrained local contexts and may be used by AIDE Hosts, but they do not make hosts semantic owners.

## Current Status

Current status: planned. Q01 documents the bridge family; Dominium Bridge baseline is planned for Q07.
