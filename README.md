# AIDE

Automated Integrated Development Environment.

## Mission

AIDE is a long-horizon engineering repository for a cross-IDE extension and companion platform that spans modern and historical development environments without flattening their differences. It combines source-backed ecosystem research, explicit support metadata, shared-core contracts, thin host adapters, environment tracking, and verification records inside one governed system.

## Core Doctrine

- AIDE is one project with one shared core and many host adapters.
- Source directories are named for compatibility technology or host contract, not exact version ranges.
- Exact version coverage belongs in inventory, manifests, and matrices.
- Support is expressed through support tiers, support states, support modes, and capability levels.
- Different host families may top out at different capability ceilings.

## Current State

- Governance, inventory, matrices, research corpora, architecture docs, environment or lab control-plane records, eval scaffolding, and packaging scaffolding are in place.
- The shared-core boot slice is implemented under `shared/` as a deterministic Python standard-library runtime with CLI bridge, fixtures, and tests.
- First-wave host proofs now exist for Microsoft, Apple, and CodeWarrior lanes, with a mix of runnable `cli-bridge` proofs and explicit blocked or deferred native lanes.
- The repository remains pre-product. Packaging, release automation, deeper native verification, and broader environment bring-up are still incomplete.

## Repository Map

- `governance/`: repository law, support policy, naming law, capability doctrine, and release policy
- `inventory/`: canonical ids, version records, and machine-readable support inputs
- `matrices/`: support, capability, feature, verification, packaging, and platform posture by lane
- `research/`: source-backed ecosystem atlases and unresolved-item registers
- `specs/`: architecture contracts and boot-slice specifications
- `shared/`: shared-core implementation, schemas, CLI bridge, and tests
- `hosts/`: thin host-lane proofs and blocked or deferred native records
- `environments/`: concrete environment control plane and bring-up catalogs
- `labs/`: prototype, blocked, and archival environment-oriented work
- `evals/`: verification models, run records, and audit reports
- `packaging/`: packaging and release-shape control plane
- `scripts/`: repeatable repository maintenance assets and future lightweight automation support
- `.agents/`: repo-local skills and operational guidance for agentic work

## Phase Status

- Completed bootstrap phases: P00 through P09 established governance, research, architecture, environment, evaluation, packaging, and boot-slice planning.
- Completed implementation phases: P10 through P13 delivered the shared-core boot slice plus first Microsoft, Apple, and CodeWarrior host-family proof waves.
- Current reality: runnable `cli-bridge` proofs exist for selected lanes, while several native lanes remain explicitly blocked or degraded pending real environments, host tooling, or embedded interop work.
- Next likely work: deepen runnable native proofs, advance environment bring-up, tighten packaging and release evidence, and promote future host work from the candidate backlog only when the repo evidence supports it.

## Key Documents

- [AGENTS.md](AGENTS.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [ROADMAP.md](ROADMAP.md)
- [MAINTENANCE.md](MAINTENANCE.md)
- [PLANS.md](PLANS.md)
- [IMPLEMENT.md](IMPLEMENT.md)
- [DOCUMENTATION.md](DOCUMENTATION.md)

## Status Boundary

This repository is operationally structured and partially implemented, but it is not broadly releasable. Blocked, deferred, degraded, and candidate areas remain explicit by design.
