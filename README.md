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
- The self-hosting reboot queue is scaffolded under `.aide/queue/`; it is the canonical route for non-trivial future agent work.
- Q00 adds a baseline freeze and reboot audit that keeps AIDE as an in-place refactor, not a greenfield restart.
- Q01 adds a documentation architecture split around AIDE Core, AIDE Hosts, AIDE Bridges, the internal Core split, and the first shipped stack of Contract + Harness + Compatibility + Dominium Bridge.
- Q02 adds README-only skeleton homes for `core/`, future host categories, and `bridges/`, plus a structural migration map. It does not move the bootstrap-era shared core or host proof lanes.
- The repository remains pre-product. Packaging, release automation, deeper native verification, and broader environment bring-up are still incomplete.

## Repository Map

- `.aide/`: self-hosting profile, filesystem queue, and autonomy or review-gate policies
- `core/`: README-only target skeleton for AIDE Core bands; current implementation remains under `shared/`
- `bridges/`: README-only target skeleton for AIDE Bridges, starting with Dominium Bridge placeholders
- `governance/`: repository law, support policy, naming law, capability doctrine, and release policy
- `inventory/`: canonical ids, version records, and machine-readable support inputs
- `matrices/`: support, capability, feature, verification, packaging, and platform posture by lane
- `docs/`: reboot constitution, architecture charters, roadmaps, decisions, design-mining indexes, and operational references
- `research/`: source-backed ecosystem atlases and unresolved-item registers
- `specs/`: architecture contracts and boot-slice specifications
- `shared/`: shared-core implementation, schemas, CLI bridge, and tests
- `hosts/`: bootstrap-era host-lane proofs plus README-only skeletons for CLI, Service, Commander, and extension host categories
- `environments/`: concrete environment control plane and bring-up catalogs
- `labs/`: prototype, blocked, and archival environment-oriented work
- `evals/`: verification models, run records, and audit reports
- `packaging/`: packaging and release-shape control plane
- `scripts/`: repeatable repository maintenance assets and future lightweight automation support
- `.agents/`: repo-local skills and operational guidance for agentic work

## Phase Status

- Completed bootstrap phases: P00 through P09 established governance, research, architecture, environment, evaluation, packaging, and boot-slice planning.
- Completed implementation phases: P10 through P13 delivered the shared-core boot slice plus first Microsoft, Apple, and CodeWarrior host-family proof waves.
- Self-bootstrap phase P15 adds a queue scaffold and first Q00 ExecPlan for future filesystem-driven work; it does not implement later queue items.
- Q01 documentation split makes the reboot documentation families navigable; it remains documentation-only and stops at review.
- Q02 structural skeleton adds target directories and README ownership boundaries; it remains skeleton-only and stops at review.
- Current reality: runnable `cli-bridge` proofs exist for selected lanes, while several native lanes remain explicitly blocked or degraded pending real environments, host tooling, or embedded interop work.
- Next likely work: review Q02, then plan Q03 only after the prior evidence and review gates support it.

## Key Documents

- [AGENTS.md](AGENTS.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [ROADMAP.md](ROADMAP.md)
- [MAINTENANCE.md](MAINTENANCE.md)
- [PLANS.md](PLANS.md)
- [IMPLEMENT.md](IMPLEMENT.md)
- [DOCUMENTATION.md](DOCUMENTATION.md)
- [core/README.md](core/README.md)
- [hosts/README.md](hosts/README.md)
- [bridges/README.md](bridges/README.md)
- [docs/constitution/README.md](docs/constitution/README.md)
- [docs/constitution/bootstrap-era-aide.md](docs/constitution/bootstrap-era-aide.md)
- [docs/constitution/reboot-doctrine.md](docs/constitution/reboot-doctrine.md)
- [docs/charters/README.md](docs/charters/README.md)
- [docs/charters/reboot-charter.md](docs/charters/reboot-charter.md)
- [docs/charters/core-charter.md](docs/charters/core-charter.md)
- [docs/charters/contract-charter.md](docs/charters/contract-charter.md)
- [docs/charters/harness-charter.md](docs/charters/harness-charter.md)
- [docs/charters/compatibility-charter.md](docs/charters/compatibility-charter.md)
- [docs/charters/hosts-charter.md](docs/charters/hosts-charter.md)
- [docs/charters/bridges-charter.md](docs/charters/bridges-charter.md)
- [docs/charters/control-charter.md](docs/charters/control-charter.md)
- [docs/charters/sdk-charter.md](docs/charters/sdk-charter.md)
- [docs/reference/README.md](docs/reference/README.md)
- [docs/reference/repo-census.md](docs/reference/repo-census.md)
- [docs/reference/documentation-migration-map.md](docs/reference/documentation-migration-map.md)
- [docs/reference/structural-migration-map.md](docs/reference/structural-migration-map.md)
- [docs/reference/terminology.md](docs/reference/terminology.md)
- [docs/roadmap/README.md](docs/roadmap/README.md)
- [docs/roadmap/reboot-roadmap.md](docs/roadmap/reboot-roadmap.md)
- [docs/roadmap/queue-roadmap.md](docs/roadmap/queue-roadmap.md)
- [docs/roadmap/staged-expansion-roadmap.md](docs/roadmap/staged-expansion-roadmap.md)
- [docs/reference/self-bootstrap.md](docs/reference/self-bootstrap.md)
- [docs/decisions/README.md](docs/decisions/README.md)
- [docs/design-mining/README.md](docs/design-mining/README.md)

## Status Boundary

This repository is operationally structured and partially implemented, but it is not broadly releasable. Blocked, deferred, degraded, and candidate areas remain explicit by design.
