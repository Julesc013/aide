# Compatibility Charter

## Purpose

Compatibility is a first-class AIDE Core domain for host, platform, version, migration, support, capability, and blocker posture.

## Owned Responsibilities

- Keep support, capability, and compatibility claims tied to evidence.
- Preserve bootstrap-era inventory, matrices, research, environments, labs, and eval reports as inputs.
- Map old host-lane proof records into the reboot model without moving them in Q01.
- Make migration risks explicit before structural refactors happen.

## Non-goals

- Compatibility does not implement host adapters.
- Compatibility does not promote candidate hosts into commitments without queue evidence.
- Q01 does not perform the Q06 compatibility baseline reconciliation.

## Boundaries

- Compatibility owns posture and evidence, not host UI.
- Contract defines shapes; Compatibility records where those shapes apply.
- Harness validates compatibility records where deterministic checks are available.

## Relation To AIDE Core / Hosts / Bridges

Compatibility is an internal AIDE Core domain. It constrains how AIDE Hosts and AIDE Bridges can claim support, capability, migration, and proof status.

## Current Status

Current status: partial. Bootstrap-era inventory, matrices, research, and reports exist. Reboot Compatibility baseline is planned for Q06.
