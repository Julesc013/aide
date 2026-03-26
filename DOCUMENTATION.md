# AIDE Documentation Index

## Purpose

`DOCUMENTATION.md` is the root guide and index for repository documentation. It defines how documentation should be organized, how authoritative documents relate to each other, and how documentation is kept aligned with reality.

## Documentation Families

- Governance docs define repository law, naming law, support policy, capability doctrine, release policy, and long-term architectural intent.
- Inventory docs will record exact host families, extension technologies, manifests, and version coverage claims.
- Architecture docs under `specs/` describe shared-core boundaries, host adapter design, interfaces, and cross-cutting technical decisions.
- Shared contract docs and schemas under `shared/` describe implementation-facing data shapes and subsystem boundaries that must remain aligned with the architecture docs.
- Environment docs will describe reproducible labs, execution environments, and verification setups.
- User-facing docs will describe how to use released artifacts, bounded by what is actually shipped.

## Organization Conventions

- Keep authoritative governance material under `governance/`.
- Keep inventory and matrix material separate from architecture narratives.
- Keep durable product and contract architecture under `specs/architecture/`.
- Keep implementation-facing shared subsystem guides and schemas under `shared/`.
- Keep environment and evaluation evidence close to the systems they verify.
- Prefer small authoritative documents over large mixed-purpose documents.

## Maintenance Conventions

- Documentation must describe reality, not aspiration.
- Update authoritative docs in the same change set that changes the governed behavior or policy.
- If a claim depends on future work, mark it as planned rather than writing it as present fact.
- When a document becomes obsolete, update or supersede it explicitly rather than leaving silent contradictions.

## Current Authoritative Set

- `README.md`: top-level project overview and phase summary.
- `AGENTS.md`: root operating law for human contributors and coding agents.
- `PLANS.md`: working plan index for substantial work.
- `IMPLEMENT.md`: engineering execution log.
- `DOCUMENTATION.md`: documentation guide and index.
- `governance/vision.md`: durable project vision and non-goals.
- `governance/support-policy.md`: support tiers, states, modes, and honesty rules.
- `governance/naming-policy.md`: naming doctrine for directories, manifests, adapters, and artifacts.
- `governance/capability-levels.md`: capability levels `L0` through `L4`.
- `governance/release-policy.md`: phase gating and release law.
- `specs/README.md`: root index for architecture and product contracts.
- `specs/architecture/**`: canonical shared-core and host-adapter architecture docs plus ADRs.
- `shared/README.md`: root guide for the shared implementation subtree.
- `shared/schemas/**`: conservative machine-readable shared contract shapes that support later implementation.

## Current Status

The repository is still pre-product, but it now has governance, inventory, matrices, host-atlas research, and a canonical shared-core architecture layer. Shared-core and host-adapter implementation, environments, evals, and packaging remain future phases.
