# AIDE Core Charter

## Purpose

AIDE Core owns durable AIDE semantics. It is the conceptual home for Contract, Harness, Runtime, Compatibility, Control, and SDK.

## Owned Responsibilities

- Keep user and host-facing semantics stable across AIDE Hosts and AIDE Bridges.
- Define the public contract vocabulary for profiles, capabilities, requests, responses, diagnostics, and generated artifacts.
- Coordinate Harness and Compatibility evidence so claims remain deterministic and reviewable.
- Keep Control policy and review gates close to the work they govern.

## Non-goals

- AIDE Core is not a host UI, IDE extension family, app surface, provider adapter, or release package.
- Q01 does not build Runtime, Commander, Mobile, IDE Hosts, or broad automation.
- AIDE Core does not replace bootstrap-era `shared/**`, `specs/**`, or `governance/**`; those records are preserved as baseline evidence.

## Boundaries

- AIDE Core may define semantics that hosts consume, but hosts remain shells.
- AIDE Core may define bridge contracts, but each AIDE Bridge must have its own proof boundary.
- Runtime remains deferred until a later queue item authorizes implementation.

## Relation To AIDE Core / Hosts / Bridges

AIDE Core is the center of the public model. AIDE Hosts present or execute Core semantics in IDE-specific shells. AIDE Bridges connect Core semantics to bounded local profiles such as Dominium Bridge.

## Current Status

Current status: partial. Bootstrap-era shared-core architecture and implementation records exist, but the reboot Core split is only documented by Q01 and must be realized by later queue items.
